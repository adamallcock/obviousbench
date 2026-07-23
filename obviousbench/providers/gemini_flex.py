"""Direct Gemini Developer API adapter that always requests Flex inference.

Inspect's bundled :class:`GoogleGenAIAPI` provides the Gemini Developer API
transport and native Gemini 3 thinking-level mapping.  Its current public
surface does not expose ``GenerateContentConfig.service_tier``, however.  This
adapter installs a per-client request decorator so only ``generateContent``
and ``streamGenerateContent`` bodies receive ``serviceTier: \"flex\"``.

The route intentionally supports just the two released Flash models in this
panel.  Both expose the documented named thinking levels ``minimal``, ``low``,
``medium``, and ``high``; neither is registered with a pretend no-thinking
setting.
"""

from __future__ import annotations

import os
from collections.abc import Awaitable, Callable
from typing import Any, cast

from google.genai import Client
from google.genai.types import HttpOptions
from inspect_ai.model import ChatMessage, GenerateConfig, ModelOutput, modelapi
from inspect_ai.model._model_call import ModelCall
from inspect_ai.model._providers.google import GoogleGenAIAPI
from inspect_ai.model._providers.util import environment_prerequisite_error
from inspect_ai.tool import ToolChoice, ToolInfo

GEMINI_API_KEY_ENV_VAR = "GEMINI_API_KEY"
GEMINI_FLEX_SERVICE_TIER = "flex"
GEMINI_FLEX_MODEL_IDS = frozenset({"gemini-3.6-flash", "gemini-3.5-flash-lite"})
GEMINI_FLEX_REASONING_EFFORTS = frozenset({"minimal", "low", "medium", "high"})


def normalize_gemini_flex_model_name(model_name: str) -> str:
    """Return a direct Gemini model ID from this adapter's local route."""
    normalized = model_name.strip()
    for prefix in ("gemini-flex/", "gemini/"):
        if normalized.startswith(prefix):
            normalized = normalized.removeprefix(prefix)
            break
    if normalized not in GEMINI_FLEX_MODEL_IDS:
        supported = ", ".join(sorted(GEMINI_FLEX_MODEL_IDS))
        raise ValueError(
            "gemini-flex supports only the verified released models "
            f"{supported}; got {model_name!r}."
        )
    return normalized


def resolve_gemini_api_key(api_key: str | None = None) -> str:
    """Resolve the direct Gemini key without exposing it in diagnostics."""
    if api_key:
        return api_key
    configured = os.environ.get(GEMINI_API_KEY_ENV_VAR)
    if configured:
        return configured
    raise environment_prerequisite_error("gemini-flex", [GEMINI_API_KEY_ENV_VAR])


def validate_gemini_flex_execution_mode(execution_mode: str) -> str:
    """Keep this provider route unambiguously Flex-only."""
    normalized = execution_mode.strip().lower().replace("_", "-")
    if normalized != GEMINI_FLEX_SERVICE_TIER:
        raise ValueError(
            "gemini-flex always uses the Gemini Developer API Flex tier; "
            f"received execution_mode={execution_mode!r}."
        )
    return normalized


def validate_gemini_flex_config(config: GenerateConfig) -> None:
    """Reject settings that would misrepresent the documented Flex panel."""
    if config.batch:
        raise ValueError(
            "gemini-flex is an online Gemini Developer API route; use a "
            "separate batch workflow rather than Inspect's batch setting."
        )
    if config.reasoning_tokens is not None:
        raise ValueError(
            "gemini-flex accepts documented Gemini thinking levels, not a "
            "reasoning-token budget. Use minimal, low, medium, or high."
        )
    if config.reasoning_effort is not None:
        if config.reasoning_effort == "none":
            raise ValueError(
                "Gemini 3.6 Flash and Gemini 3.5 Flash-Lite do not expose a "
                "documented fully-disabled thinking setting. Use minimal, low, "
                "medium, or high."
            )
        if config.reasoning_effort not in GEMINI_FLEX_REASONING_EFFORTS:
            allowed = ", ".join(sorted(GEMINI_FLEX_REASONING_EFFORTS))
            raise ValueError(
                "gemini-flex reasoning_effort must be one of "
                f"{allowed}; received {config.reasoning_effort!r}."
            )
    if config.extra_body and (
        "serviceTier" in config.extra_body or "service_tier" in config.extra_body
    ):
        raise ValueError(
            "gemini-flex always sends serviceTier='flex'; do not override it "
            "through extra_body."
        )


def gemini_flex_request_body(path: str, request_dict: dict[str, object]) -> dict[str, object]:
    """Return a copied GenerateContent body with a non-overridable Flex tier.

    The Google SDK emits ``serviceTier`` at the top level of a GenerateContent
    body, not inside ``generationConfig``.  Restrict the injection to the two
    generate-content paths so file conversion and token counting requests stay
    unchanged.
    """
    is_generate_content = (
        ":generateContent" in path or ":streamGenerateContent" in path
    )
    if not is_generate_content:
        return request_dict

    existing = request_dict.get("serviceTier")
    existing_value = getattr(existing, "value", existing)
    if existing_value not in (None, GEMINI_FLEX_SERVICE_TIER):
        raise ValueError(
            "gemini-flex refuses a non-Flex serviceTier in the outgoing "
            f"request: {existing_value!r}."
        )
    return {**request_dict, "serviceTier": GEMINI_FLEX_SERVICE_TIER}


@modelapi("gemini-flex")
class GeminiFlexAPI(GoogleGenAIAPI):
    """Gemini Developer API route with an explicit, Flex-only service tier.

    Authentication uses an externally supplied ``GEMINI_API_KEY`` (normally
    injected from Keychain by the runner).  The adapter never reads or records
    the raw key outside the Google SDK client it constructs for each request.
    """

    def __init__(
        self,
        model_name: str,
        base_url: str | None = None,
        api_key: str | None = None,
        config: GenerateConfig | None = None,
        *,
        execution_mode: str = GEMINI_FLEX_SERVICE_TIER,
        **model_args: Any,
    ) -> None:
        self.execution_mode = validate_gemini_flex_execution_mode(execution_mode)
        super().__init__(
            model_name=normalize_gemini_flex_model_name(model_name),
            base_url=base_url,
            api_key=resolve_gemini_api_key(api_key),
            config=config or GenerateConfig(),
            **model_args,
        )

    def model_client(self, http_options: HttpOptions | None = None) -> Client:
        """Build a fresh direct SDK client and decorate only generation calls."""
        client = super().model_client(http_options)
        api_client = client._api_client
        original_async_request = cast(
            Callable[
                [str, str, dict[str, object], HttpOptions | None],
                Awaitable[Any],
            ],
            api_client.async_request,
        )
        original_async_request_streamed = cast(
            Callable[
                [str, str, dict[str, object], HttpOptions | None],
                Awaitable[Any],
            ],
            api_client.async_request_streamed,
        )

        async def flex_async_request(
            http_method: str,
            path: str,
            request_dict: dict[str, object],
            request_http_options: HttpOptions | None = None,
        ) -> Any:
            return await original_async_request(
                http_method,
                path,
                gemini_flex_request_body(path, request_dict),
                request_http_options,
            )

        async def flex_async_request_streamed(
            http_method: str,
            path: str,
            request_dict: dict[str, object],
            request_http_options: HttpOptions | None = None,
        ) -> Any:
            return await original_async_request_streamed(
                http_method,
                path,
                gemini_flex_request_body(path, request_dict),
                request_http_options,
            )

        api_client.async_request = flex_async_request
        api_client.async_request_streamed = flex_async_request_streamed
        return client

    async def generate(
        self,
        input: list[ChatMessage],
        tools: list[ToolInfo],
        tool_choice: ToolChoice,
        config: GenerateConfig,
    ) -> ModelOutput | tuple[ModelOutput | Exception, ModelCall]:
        """Validate the panel setting and record its forced service tier."""
        validate_gemini_flex_config(config)
        result = await super().generate(input, tools, tool_choice, config)
        if isinstance(result, tuple):
            output, model_call = result
            generation_config = model_call.request.get("generation_config")
            if isinstance(generation_config, dict):
                generation_config["service_tier"] = GEMINI_FLEX_SERVICE_TIER
            if isinstance(output, ModelOutput):
                output.metadata = {
                    **dict(output.metadata or {}),
                    "gemini_flex": {
                        "model_id": self.service_model_name(),
                        "requested_service_tier": GEMINI_FLEX_SERVICE_TIER,
                    },
                }
        return result
