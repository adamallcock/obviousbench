"""Native Inspect provider adapter for Cohere's v2 Chat API.

This adapter deliberately uses Cohere's native ``POST /v2/chat`` contract,
rather than its OpenAI compatibility endpoint. In particular, Cohere's
``thinking`` object has a required ``type`` field; a bounded request therefore
uses ``{"type": "enabled", "token_budget": <positive integer>}``.
"""

from __future__ import annotations

import json
import os
import time
from collections.abc import Mapping
from typing import Any

import httpx
from inspect_ai._util.content import ContentReasoning, ContentText
from inspect_ai._util.httpx import httpx_classify_retry
from inspect_ai.model import GenerateConfig, modelapi
from inspect_ai.model._call_tools import parse_tool_call
from inspect_ai.model._chat_message import (
    ChatMessage,
    ChatMessageAssistant,
    ChatMessageSystem,
    ChatMessageTool,
    ChatMessageUser,
)
from inspect_ai.model._model import ModelAPI, RetryDecision
from inspect_ai.model._model_call import ModelCall
from inspect_ai.model._model_output import (
    ChatCompletionChoice,
    ModelOutput,
    ModelUsage,
    StopReason,
)
from inspect_ai.model._providers.util import environment_prerequisite_error
from inspect_ai.tool import ToolCall, ToolChoice, ToolFunction, ToolInfo
from inspect_ai.util._json import json_schema_dump

DEFAULT_COHERE_BASE_URL = "https://api.cohere.ai/v2"
# Prefer a separately stored production credential when it is supplied, while
# preserving the original variable for existing local setups and CI.
COHERE_API_KEY_VARS = ("COHEREPROD_API_KEY", "COHERE_API_KEY")
COHERE_BASE_URL_VARS = ("COHERE_BASE_URL",)

# These are ObviousBench experiment budgets, not Cohere-defined effort names.
COHERE_BENCHMARK_THINKING_TOKEN_BUDGETS = (512, 2048, 8192)

_COHERE_MANAGED_REQUEST_FIELDS = frozenset(
    {
        "model",
        "messages",
        "tools",
        "tool_choice",
        "stream",
        "max_tokens",
        "stop_sequences",
        "temperature",
        "seed",
        "frequency_penalty",
        "presence_penalty",
        "k",
        "p",
        "logprobs",
    }
)


def resolve_cohere_api_key(api_key: str | None = None) -> tuple[str, str]:
    """Resolve the Cohere API key without including it in diagnostics."""
    if api_key:
        return api_key, COHERE_API_KEY_VARS[0]
    for env_var in COHERE_API_KEY_VARS:
        value = os.environ.get(env_var)
        if value:
            return value, env_var
    raise environment_prerequisite_error("cohere", list(COHERE_API_KEY_VARS))


def resolve_cohere_base_url(base_url: str | None = None) -> str:
    """Resolve Cohere's v2 API root or an explicitly supplied v2-compatible root."""
    if base_url:
        return base_url.rstrip("/")
    for env_var in COHERE_BASE_URL_VARS:
        value = os.environ.get(env_var)
        if value:
            return value.rstrip("/")
    return DEFAULT_COHERE_BASE_URL


def normalize_cohere_model_name(model_name: str) -> str:
    """Remove only the local Inspect route prefix from a Cohere model ID."""
    normalized = model_name.strip().removeprefix("cohere/")
    if not normalized:
        raise ValueError("Cohere model name must not be empty.")
    return normalized


def cohere_chat_url(base_url: str) -> str:
    """Return the native Cohere Chat v2 endpoint for a v2 API root."""
    return f"{base_url.rstrip('/')}/chat"


def cohere_thinking_disabled() -> dict[str, str]:
    """Return Cohere's explicit native request shape for disabled thinking."""
    return {"type": "disabled"}


def cohere_thinking_enabled(token_budget: int) -> dict[str, int | str]:
    """Return Cohere's explicit native request shape for a thinking budget."""
    _validate_token_budget(token_budget)
    return {"type": "enabled", "token_budget": token_budget}


def normalize_cohere_thinking(value: object) -> dict[str, int | str]:
    """Validate and copy a Cohere-native ``thinking`` object.

    Cohere's generated v2 schema requires ``type``. ``enabled`` may omit a
    budget for unlimited thinking, while an explicitly bounded request must use
    a positive integer ``token_budget``. A disabled request must not carry a
    budget, because it would make the requested state ambiguous.
    """
    if not isinstance(value, Mapping):
        raise ValueError("Cohere thinking must be an object with a 'type' field.")

    unknown = set(value).difference({"type", "token_budget"})
    if unknown:
        fields = ", ".join(sorted(str(field) for field in unknown))
        raise ValueError(f"Unsupported Cohere thinking field(s): {fields}.")

    thinking_type = value.get("type")
    if thinking_type not in {"enabled", "disabled"}:
        raise ValueError(
            "Cohere thinking.type must be 'enabled' or 'disabled'; "
            f"received {thinking_type!r}."
        )

    token_budget = value.get("token_budget")
    if thinking_type == "disabled":
        if token_budget is not None:
            raise ValueError(
                "Cohere thinking.type='disabled' cannot include token_budget."
            )
        return cohere_thinking_disabled()

    if token_budget is None:
        return {"type": "enabled"}
    _validate_token_budget(token_budget)
    return cohere_thinking_enabled(token_budget)


def cohere_chat_request(
    *,
    model_name: str,
    input: list[ChatMessage],
    tools: list[ToolInfo],
    tool_choice: ToolChoice,
    config: GenerateConfig,
) -> dict[str, Any]:
    """Build one non-streaming native ``POST /v2/chat`` JSON body.

    This is intentionally a pure provider-specific helper so registry and
    smoke code can prove request shaping without network access.
    """
    _validate_cohere_generation_config(config)

    request: dict[str, Any] = {
        "model": normalize_cohere_model_name(model_name),
        "messages": [cohere_chat_message(message) for message in input],
        "stream": False,
    }
    _copy_config_field(config, request, "max_tokens", "max_tokens")
    _copy_config_field(config, request, "stop_seqs", "stop_sequences")
    _copy_config_field(config, request, "temperature", "temperature")
    _copy_config_field(config, request, "seed", "seed")
    _copy_config_field(config, request, "frequency_penalty", "frequency_penalty")
    _copy_config_field(config, request, "presence_penalty", "presence_penalty")
    _copy_config_field(config, request, "top_k", "k")
    _copy_config_field(config, request, "top_p", "p")
    _copy_config_field(config, request, "logprobs", "logprobs")

    if tools:
        request["tools"] = cohere_chat_tools(tools)
        normalized_tool_choice = cohere_tool_choice(tool_choice, tools)
        if normalized_tool_choice is not None:
            request["tool_choice"] = normalized_tool_choice

    extra_body = _cohere_extra_body(config)
    thinking = extra_body.pop("thinking", None)
    if thinking is not None:
        request["thinking"] = normalize_cohere_thinking(thinking)
    request.update(extra_body)
    return request


def cohere_chat_headers(
    api_key: str,
    extra_headers: Mapping[str, str] | None = None,
) -> dict[str, str]:
    """Build headers for Cohere's native bearer-authenticated Chat endpoint."""
    headers = dict(extra_headers or {})
    headers.update(
        {
            "Accept": "application/json",
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
    )
    return headers


def cohere_chat_message(message: ChatMessage) -> dict[str, Any]:
    """Translate Inspect text, reasoning, and tool messages to Cohere v2."""
    if isinstance(message, ChatMessageSystem):
        return {"role": "system", "content": _cohere_message_content(message)}
    if isinstance(message, ChatMessageUser):
        return {"role": "user", "content": _cohere_message_content(message)}
    if isinstance(message, ChatMessageTool):
        if not message.tool_call_id:
            raise ValueError("Cohere tool messages require an Inspect tool_call_id.")
        return {
            "role": "tool",
            "tool_call_id": message.tool_call_id,
            "content": _cohere_message_content(message),
        }
    if isinstance(message, ChatMessageAssistant):
        request: dict[str, Any] = {"role": "assistant"}
        content = _cohere_message_content(message, allow_reasoning=True)
        if content or not message.tool_calls:
            request["content"] = content
        if message.tool_calls:
            request["tool_calls"] = [
                _cohere_request_tool_call(tool_call)
                for tool_call in message.tool_calls
            ]
        return request
    raise TypeError(f"Unsupported Inspect chat message for Cohere: {type(message)!r}")


def cohere_chat_tools(tools: list[ToolInfo]) -> list[dict[str, Any]]:
    """Translate Inspect function specifications to Cohere v2 tool definitions."""
    return [
        {
            "type": "function",
            "function": {
                "name": tool.name,
                "description": tool.description,
                "parameters": json_schema_dump(tool.parameters),
            },
        }
        for tool in tools
    ]


def cohere_tool_choice(
    tool_choice: ToolChoice,
    tools: list[ToolInfo],
) -> str | None:
    """Map Inspect's tool policy to Cohere's ``REQUIRED``/``NONE`` contract."""
    if tool_choice == "auto":
        return None
    if tool_choice == "any":
        return "REQUIRED"
    if tool_choice == "none":
        return "NONE"
    if isinstance(tool_choice, ToolFunction):
        if len(tools) != 1 or tools[0].name != tool_choice.name:
            raise ValueError(
                "Cohere only supports REQUIRED or NONE tool_choice; a selected "
                "Inspect tool must be the sole supplied tool."
            )
        return "REQUIRED"
    raise TypeError(f"Unsupported Cohere tool_choice: {tool_choice!r}")


def cohere_model_output(
    response: Mapping[str, Any],
    *,
    model_name: str,
    tools: list[ToolInfo],
) -> ModelOutput:
    """Parse the core Cohere v2 response and usage objects into Inspect types."""
    message = response.get("message")
    if not isinstance(message, Mapping):
        raise ValueError("Cohere Chat response is missing an object-valued message.")

    content = _cohere_response_content(message.get("content"))
    tool_calls = _cohere_response_tool_calls(message.get("tool_calls"), tools)
    assistant = ChatMessageAssistant(
        content=content,
        model=model_name,
        source="generate",
        tool_calls=tool_calls or None,
    )

    metadata: dict[str, Any] = {}
    response_id = response.get("id")
    if isinstance(response_id, str) and response_id:
        metadata["cohere_response_id"] = response_id
    billed_units = _cohere_billed_units(response)
    if billed_units:
        metadata["cohere_billed_units"] = billed_units

    return ModelOutput(
        model=model_name,
        choices=[
            ChatCompletionChoice(
                message=assistant,
                stop_reason=cohere_stop_reason(response.get("finish_reason")),
            )
        ],
        usage=cohere_model_usage(response),
        metadata=metadata or None,
    )


def cohere_model_usage(response: Mapping[str, Any]) -> ModelUsage | None:
    """Map Cohere's token counts while preserving cache reads when reported."""
    usage = _cohere_usage_object(response)
    if usage is None:
        return None

    tokens = usage.get("tokens")
    billed_units = usage.get("billed_units")
    token_counts = tokens if isinstance(tokens, Mapping) else billed_units
    if not isinstance(token_counts, Mapping):
        return None

    input_tokens = _cohere_token_count(token_counts.get("input_tokens"), "input_tokens")
    output_tokens = _cohere_token_count(
        token_counts.get("output_tokens"), "output_tokens"
    )
    cached_value = usage.get("cached_tokens")
    cached_tokens = _cohere_token_count(cached_value, "cached_tokens")
    if cached_value is not None and input_tokens == 0:
        input_tokens = cached_tokens
    if cached_tokens > input_tokens:
        raise ValueError(
            "Cohere usage.cached_tokens cannot exceed usage.tokens.input_tokens."
        )

    return ModelUsage(
        input_tokens=input_tokens - cached_tokens,
        output_tokens=output_tokens,
        total_tokens=input_tokens + output_tokens,
        input_tokens_cache_read=cached_tokens if cached_value is not None else None,
    )


def cohere_stop_reason(value: object) -> StopReason:
    """Map Cohere Chat v2 finish reasons to Inspect's stable stop-reason set."""
    normalized = value.upper() if isinstance(value, str) else ""
    if normalized in {"COMPLETE", "STOP_SEQUENCE"}:
        return "stop"
    if normalized in {"MAX_TOKENS", "ERROR_LIMIT"}:
        return "max_tokens"
    if normalized == "TOOL_CALL":
        return "tool_calls"
    return "unknown"

@modelapi("cohere")
class CohereAPI(ModelAPI):
    """Cohere's native non-streaming Chat v2 API for Inspect evaluations."""

    def __init__(
        self,
        model_name: str,
        base_url: str | None = None,
        api_key: str | None = None,
        config: GenerateConfig | None = None,
        *,
        http_client: httpx.AsyncClient | None = None,
        **model_args: Any,
    ) -> None:
        if model_args:
            fields = ", ".join(sorted(model_args))
            raise TypeError(f"Unsupported Cohere model argument(s): {fields}.")
        resolved_api_key, _ = resolve_cohere_api_key(api_key)
        super().__init__(
            model_name=normalize_cohere_model_name(model_name),
            base_url=resolve_cohere_base_url(base_url),
            api_key=resolved_api_key,
            api_key_vars=list(COHERE_API_KEY_VARS),
            config=config or GenerateConfig(),
        )
        self._http_client = http_client or httpx.AsyncClient()
        self._owns_http_client = http_client is None

    def canonical_name(self) -> str:
        """Return the stable Inspect spelling for Cohere's service model ID."""
        return f"cohere/{self.service_model_name()}"

    def service_model_name(self) -> str:
        """Return the model ID sent directly to Cohere's API."""
        return normalize_cohere_model_name(self.model_name)

    def connection_key(self) -> str:
        """Scope concurrency by Cohere credential and the served model."""
        return f"{self.initial_api_key}:{self.service_model_name()}"

    async def aclose(self) -> None:
        """Close only the HTTP client allocated by this adapter."""
        if self._owns_http_client:
            await self._http_client.aclose()

    async def generate(
        self,
        input: list[ChatMessage],
        tools: list[ToolInfo],
        tool_choice: ToolChoice,
        config: GenerateConfig,
    ) -> tuple[ModelOutput | Exception, ModelCall]:
        """POST a native v2 Chat request and return Inspect's parsed output."""
        request = cohere_chat_request(
            model_name=self.service_model_name(),
            input=input,
            tools=tools,
            tool_choice=tool_choice,
            config=config,
        )
        model_call = ModelCall.create(request=request, response=None)
        started = time.monotonic()

        try:
            response = await self._http_client.post(
                cohere_chat_url(self.base_url or DEFAULT_COHERE_BASE_URL),
                json=request,
                headers=cohere_chat_headers(
                    self.api_key or "", config.extra_headers
                ),
                timeout=config.timeout,
            )
            elapsed = time.monotonic() - started
            response_data = _cohere_response_data(response)
            if response.is_error:
                model_call.set_error(response_data, elapsed)
                response.raise_for_status()

            if not isinstance(response_data, Mapping):
                error = ValueError("Cohere Chat returned a non-object JSON response.")
                model_call.set_error(response_data, elapsed)
                return error, model_call

            try:
                output = cohere_model_output(
                    response_data,
                    model_name=self.service_model_name(),
                    tools=tools,
                )
            except (TypeError, ValueError) as error:
                model_call.set_error(response_data, elapsed)
                return error, model_call

            model_call.set_response(response_data, elapsed)
            return output, model_call
        except httpx.HTTPStatusError as error:
            return error, model_call
        except httpx.HTTPError as error:
            model_call.set_error({"error": str(error)}, time.monotonic() - started)
            return error, model_call

    def should_retry(self, ex: Exception) -> bool | RetryDecision:
        """Use Inspect's standard HTTP retry classification for Cohere errors."""
        decision = httpx_classify_retry(ex)
        return decision if decision is not None else False

    def is_auth_failure(self, ex: Exception) -> bool:
        """Cohere documents 401 and 498 as invalid authentication states."""
        return isinstance(ex, httpx.HTTPStatusError) and ex.response.status_code in {
            401,
            498,
        }


def _validate_token_budget(value: object) -> None:
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise ValueError(
            "Cohere thinking.token_budget must be a positive integer; "
            f"received {value!r}."
        )


def _validate_cohere_generation_config(config: GenerateConfig) -> None:
    if config.reasoning_effort is not None:
        raise ValueError(
            "Cohere Chat v2 does not accept Inspect reasoning_effort. Use "
            "extra_body={'thinking': {'type': 'disabled'}} or a native "
            "thinking token_budget instead."
        )
    if config.reasoning_tokens is not None:
        raise ValueError(
            "Cohere thinking budgets must be explicit native "
            "extra_body['thinking']['token_budget'] values."
        )
    if config.effort is not None:
        raise ValueError(
            "Cohere Chat v2 does not accept Inspect effort. Use the native "
            "thinking object instead."
        )


def _copy_config_field(
    config: GenerateConfig,
    request: dict[str, Any],
    source: str,
    destination: str,
) -> None:
    value = getattr(config, source)
    if value is not None:
        request[destination] = value


def _cohere_extra_body(config: GenerateConfig) -> dict[str, Any]:
    extra_body = dict(config.extra_body or {})
    managed = set(extra_body).intersection(_COHERE_MANAGED_REQUEST_FIELDS)
    if managed:
        fields = ", ".join(sorted(managed))
        raise ValueError(
            "Cohere extra_body cannot override adapter-managed field(s): "
            f"{fields}."
        )
    return extra_body


def _cohere_message_content(
    message: ChatMessage,
    *,
    allow_reasoning: bool = False,
) -> str | list[dict[str, str]]:
    if isinstance(message.content, str):
        return message.content

    content: list[dict[str, str]] = []
    for part in message.content:
        if isinstance(part, ContentText):
            content.append({"type": "text", "text": part.text})
        elif allow_reasoning and isinstance(part, ContentReasoning):
            content.append({"type": "thinking", "thinking": part.reasoning})
        else:
            raise TypeError(
                "Cohere Chat v2 adapter currently supports text input and "
                "assistant reasoning history only; received "
                f"{type(part)!r}."
            )
    return content


def _cohere_request_tool_call(tool_call: ToolCall) -> dict[str, Any]:
    return {
        "id": tool_call.id,
        "type": "function",
        "function": {
            "name": tool_call.function,
            "arguments": json.dumps(tool_call.arguments),
        },
    }


def _cohere_response_content(value: object) -> list[ContentText | ContentReasoning]:
    if value is None:
        return []
    if isinstance(value, str):
        return [ContentText(text=value)]
    if not isinstance(value, list):
        raise ValueError("Cohere message.content must be a string or list.")

    content: list[ContentText | ContentReasoning] = []
    for block in value:
        if not isinstance(block, Mapping):
            raise ValueError("Cohere message.content blocks must be objects.")
        block_type = block.get("type")
        if block_type == "text" and isinstance(block.get("text"), str):
            content.append(ContentText(text=block["text"]))
        elif block_type == "thinking" and isinstance(block.get("thinking"), str):
            content.append(ContentReasoning(reasoning=block["thinking"]))
        else:
            raise ValueError(
                "Unsupported Cohere message.content block: " f"{block!r}."
            )
    return content


def _cohere_response_tool_calls(
    value: object,
    tools: list[ToolInfo],
) -> list[ToolCall]:
    if value is None:
        return []
    if not isinstance(value, list):
        raise ValueError("Cohere message.tool_calls must be a list when present.")

    tool_calls: list[ToolCall] = []
    for raw_call in value:
        if not isinstance(raw_call, Mapping):
            raise ValueError("Cohere tool calls must be objects.")
        call_id = raw_call.get("id")
        function = raw_call.get("function")
        if not isinstance(call_id, str) or not isinstance(function, Mapping):
            raise ValueError("Cohere tool calls require string id and function fields.")
        name = function.get("name")
        arguments = function.get("arguments", "{}")
        if not isinstance(name, str):
            raise ValueError("Cohere tool call function.name must be a string.")
        if not isinstance(arguments, str):
            arguments = json.dumps(arguments)
        tool_calls.append(parse_tool_call(call_id, name, arguments, tools))
    return tool_calls


def _cohere_usage_object(response: Mapping[str, Any]) -> Mapping[str, Any] | None:
    usage = response.get("usage")
    if isinstance(usage, Mapping):
        return usage
    # Older v2 examples documented the equivalent object under ``meta``.
    meta = response.get("meta")
    return meta if isinstance(meta, Mapping) else None


def _cohere_billed_units(response: Mapping[str, Any]) -> dict[str, int] | None:
    usage = _cohere_usage_object(response)
    if usage is None or not isinstance(usage.get("billed_units"), Mapping):
        return None
    billed_units = usage["billed_units"]
    return {
        "input_tokens": _cohere_token_count(
            billed_units.get("input_tokens"), "billed_units.input_tokens"
        ),
        "output_tokens": _cohere_token_count(
            billed_units.get("output_tokens"), "billed_units.output_tokens"
        ),
    }


def _cohere_token_count(value: object, field: str) -> int:
    if value is None:
        return 0
    if isinstance(value, bool) or not isinstance(value, int | float):
        raise ValueError(f"Cohere usage.{field} must be a non-negative number.")
    if value < 0 or int(value) != value:
        raise ValueError(f"Cohere usage.{field} must be a non-negative integer.")
    return int(value)


def _cohere_response_data(response: httpx.Response) -> object:
    try:
        return response.json()
    except json.JSONDecodeError:
        return {"body": response.text}
