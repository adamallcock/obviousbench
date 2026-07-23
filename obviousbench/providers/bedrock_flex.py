"""Bedrock Converse adapter for the explicit Flex service tier.

Inspect's bundled Bedrock client currently predates the Converse ``serviceTier``
field.  This adapter retains Inspect's mature Bedrock message conversion and
response parsing, but signs the JSON Converse request itself so an evaluation
can explicitly request Flex rather than silently using the Standard default.

It is intentionally a distinct ``bedrock-flex`` model route.  Standard-only
models should continue using Inspect's native ``bedrock`` route.
"""

from __future__ import annotations

import json
import os
import time
from collections.abc import Callable, Mapping
from typing import Any
from urllib.parse import quote

import httpx
from botocore.auth import SigV4Auth
from botocore.awsrequest import AWSRequest
from botocore.credentials import ReadOnlyCredentials
from botocore.session import Session
from inspect_ai.log._samples import set_active_model_event_call
from inspect_ai.model import ChatMessage, GenerateConfig, modelapi
from inspect_ai.model._model import RetryDecision
from inspect_ai.model._model_call import ModelCall
from inspect_ai.model._model_output import ModelOutput
from inspect_ai.model._providers.bedrock import (
    BedrockAPI,
    ConverseClientConverseRequest,
    ConverseInferenceConfig,
    ConverseResponse,
    ConverseToolConfig,
    converse_messages,
    converse_tool_choice,
    converse_tools,
    model_output_from_response,
    replace_bytes_with_placeholder,
)
from inspect_ai.model._providers.util import environment_prerequisite_error
from inspect_ai.tool import ToolChoice, ToolInfo

BEDROCK_FLEX_SERVICE_TIER = {"type": "flex"}
BEDROCK_REGION_ENV_VARS = ("AWS_REGION", "AWS_DEFAULT_REGION")
BEDROCK_BEARER_TOKEN_ENV_VARS = ("AWS_BEARER_TOKEN_BEDROCK", "BEDROCK_API_KEY")
BEDROCK_FLEX_READ_TIMEOUT_SECONDS = 60 * 60

# Flex capability is model-specific. Keep this deliberately small and explicit:
# a Flex request to a Standard-only model must fail before a paid call.
_NOVA_STANDARD_ONLY_MODEL_IDS = frozenset(
    {
        "amazon.nova-micro-v1:0",
        "amazon.nova-lite-v1:0",
    }
)
_NOVA_FLEX_NO_REASONING_MODEL_IDS = frozenset(
    {
        "amazon.nova-pro-v1:0",
        "amazon.nova-premier-v1:0",
    }
)
_NOVA_FLEX_REASONING_MODEL_IDS = frozenset({"amazon.nova-2-lite-v1:0"})
_NOVA_FLEX_REASONING_EFFORTS = frozenset({"low", "medium", "high"})


def resolve_bedrock_region(
    *,
    region_name: str | None = None,
    profile_name: str | None = None,
) -> str:
    """Resolve a Bedrock region from an explicit value, env, or AWS profile."""
    if region_name:
        return region_name
    # Botocore's current profile resolver recognizes AWS_DEFAULT_REGION but not
    # AWS_REGION. Honour both advertised variables here so this direct HTTP
    # adapter behaves consistently with the runner's normalized environment.
    for env_var in ("AWS_DEFAULT_REGION", "AWS_REGION"):
        configured_env = os.environ.get(env_var)
        if configured_env:
            return configured_env
    session = Session(profile=profile_name)
    configured = session.get_config_variable("region")
    if configured:
        return str(configured)
    raise environment_prerequisite_error("bedrock-flex", list(BEDROCK_REGION_ENV_VARS))


def bedrock_runtime_endpoint(*, region_name: str, profile_name: str | None = None) -> str:
    """Resolve the partition-correct Bedrock Runtime endpoint without a request."""
    session = Session(profile=profile_name)
    resolver = session.get_component("endpoint_resolver")
    endpoint = resolver.construct_endpoint("bedrock-runtime", region_name)
    hostname = endpoint.get("hostname") if endpoint else None
    if not hostname:
        raise ValueError(
            "No Bedrock Runtime endpoint is known for region " f"{region_name!r}."
        )
    return f"https://{hostname}"


def converse_payload(
    request: ConverseClientConverseRequest,
    *,
    service_tier: Mapping[str, str] | None,
) -> tuple[str, dict[str, Any]]:
    """Convert an Inspect Converse request model into a direct HTTP payload."""
    payload = request.model_dump(exclude_none=True, exclude_defaults=True)
    model_id = payload.pop("modelId")
    if not isinstance(model_id, str) or not model_id:
        raise ValueError("Bedrock Converse request requires a non-empty modelId.")
    for optional_field in (
        "inferenceConfig",
        "additionalModelRequestFields",
        "toolConfig",
    ):
        if payload.get(optional_field) == {}:
            payload.pop(optional_field)
    if service_tier is not None:
        payload["serviceTier"] = dict(service_tier)
    return model_id, payload


def flex_converse_payload(request: ConverseClientConverseRequest) -> tuple[str, dict[str, Any]]:
    """Convert Inspect's Converse request model into the Flex wire payload."""
    return converse_payload(request, service_tier=BEDROCK_FLEX_SERVICE_TIER)


def standard_converse_payload(
    request: ConverseClientConverseRequest,
) -> tuple[str, dict[str, Any]]:
    """Convert a Standard request while intentionally omitting ``serviceTier``."""
    return converse_payload(request, service_tier=None)


def normalized_nova_model_id(model_id: str) -> str:
    """Remove AWS's cross-region prefix while retaining the real model identity."""
    return model_id.removeprefix("us.").removeprefix("eu.").removeprefix("apac.")


def validate_flex_model(model_id: str, config: GenerateConfig) -> None:
    """Reject unsupported Nova/tier/reasoning combinations before invocation."""
    normalized = normalized_nova_model_id(model_id)
    if normalized in _NOVA_STANDARD_ONLY_MODEL_IDS:
        raise ValueError(
            f"{model_id} is Standard-only on Bedrock and cannot use bedrock-flex."
        )
    if normalized not in (
        _NOVA_FLEX_NO_REASONING_MODEL_IDS | _NOVA_FLEX_REASONING_MODEL_IDS
    ):
        raise ValueError(
            "bedrock-flex currently supports only the documented Nova Pro, "
            "Nova Premier, and Nova 2 Lite model identities; got "
            f"{model_id!r}."
        )

    effort = config.reasoning_effort
    if normalized in _NOVA_FLEX_NO_REASONING_MODEL_IDS:
        if effort is not None:
            raise ValueError(
                f"{model_id} has no documented selectable Bedrock Nova reasoning "
                "control; omit reasoning_effort."
            )
        return

    if effort is None:
        return
    if effort not in _NOVA_FLEX_REASONING_EFFORTS:
        allowed = ", ".join(sorted(_NOVA_FLEX_REASONING_EFFORTS))
        raise ValueError(
            f"{model_id} supports only Nova 2 Lite reasoning_effort values: "
            f"{allowed}; omit it to disable extended thinking."
        )
    if effort == "high":
        forbidden = {
            "temperature": config.temperature,
            "top_p": config.top_p,
            "top_k": config.top_k,
        }
        configured = [name for name, value in forbidden.items() if value is not None]
        if configured:
            raise ValueError(
                "Nova 2 Lite high reasoning requires these controls to be unset: "
                f"{', '.join(configured)}."
            )


def validate_standard_model(model_id: str, config: GenerateConfig) -> None:
    """Reject Nova combinations that cannot use the Standard-only adapter."""
    normalized = normalized_nova_model_id(model_id)
    if normalized not in _NOVA_STANDARD_ONLY_MODEL_IDS:
        raise ValueError(
            "bedrock-standard currently supports only the documented Standard-only "
            f"Nova Micro and Nova Lite identities; got {model_id!r}."
        )
    if config.reasoning_effort is not None:
        raise ValueError(
            f"{model_id} has no documented selectable Bedrock Nova reasoning "
            "control; omit reasoning_effort."
        )


def flex_service_tier_from_response(response: Mapping[str, Any]) -> str:
    """Require the Bedrock response to attest that Flex actually served the call."""
    tier = response.get("serviceTier")
    if not isinstance(tier, Mapping) or not isinstance(tier.get("type"), str):
        raise ValueError(
            "Bedrock Flex response omitted serviceTier.type; refusing to label "
            "an unverified served tier as Flex."
        )
    return tier["type"]


def standard_service_tier_from_response(response: Mapping[str, Any]) -> str:
    """Return a Standard-tier attestation without fabricating an omitted field."""
    tier = response.get("serviceTier")
    if tier is None:
        return "unreported_default"
    if not isinstance(tier, Mapping) or not isinstance(tier.get("type"), str):
        raise ValueError("Bedrock Standard response has an invalid serviceTier field.")
    if tier["type"] != "default":
        raise ValueError(
            "Bedrock served a non-Standard tier for a bedrock-standard request: "
            f"{tier['type']!r}."
        )
    return "default"


def signed_flex_converse_request(
    *,
    endpoint: str,
    region_name: str,
    model_id: str,
    payload: Mapping[str, Any],
    credentials: ReadOnlyCredentials,
) -> tuple[str, dict[str, str], bytes]:
    """Create one SigV4-signed Bedrock Converse HTTP request without sending it."""
    body = json.dumps(payload, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    url = f"{endpoint.rstrip('/')}/model/{quote(model_id, safe='')}/converse"
    request = AWSRequest(
        method="POST",
        url=url,
        data=body,
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
    )
    SigV4Auth(credentials, "bedrock", region_name).add_auth(request)
    prepared = request.prepare()
    return (
        url,
        {str(name): str(value) for name, value in prepared.headers.items()},
        body,
    )


def bearer_flex_converse_request(
    *,
    endpoint: str,
    model_id: str,
    payload: Mapping[str, Any],
    bearer_token: str,
) -> tuple[str, dict[str, str], bytes]:
    """Create a Bedrock API-key-authenticated Converse request without sending it."""
    if not bearer_token:
        raise ValueError("Bedrock bearer token must not be empty.")
    body = json.dumps(payload, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    url = f"{endpoint.rstrip('/')}/model/{quote(model_id, safe='')}/converse"
    return (
        url,
        {
            "Accept": "application/json",
            "Authorization": f"Bearer {bearer_token}",
            "Content-Type": "application/json",
        },
        body,
    )


def resolve_bedrock_bearer_token(api_key: str | None = None) -> str | None:
    """Resolve an optional Bedrock API key without putting it in diagnostics."""
    if api_key:
        return api_key
    for env_var in BEDROCK_BEARER_TOKEN_ENV_VARS:
        value = os.environ.get(env_var)
        if value:
            return value
    return None


class _BedrockConverseAPI(BedrockAPI):
    """Shared direct-HTTP Converse transport for the two supported tiers.

    Authentication prefers an explicitly supplied/current Amazon Bedrock API
    key (the official ``AWS_BEARER_TOKEN_BEDROCK`` spelling, with a local
    ``BEDROCK_API_KEY`` compatibility alias). Otherwise it uses the ordinary
    AWS credential chain (profile, SSO, environment, role, or instance
    identity). Pass ``-M region_name=<region>`` or configure an AWS default
    region.
    """

    _route_name = "bedrock-converse"

    def __init__(
        self,
        model_name: str,
        base_url: str | None = None,
        api_key: str | None = None,
        config: GenerateConfig | None = None,
        *,
        region_name: str | None = None,
        profile_name: str | None = None,
        http_client: httpx.AsyncClient | None = None,
        credentials_resolver: Callable[[], ReadOnlyCredentials] | None = None,
        **model_args: Any,
    ) -> None:
        self._bearer_token = resolve_bedrock_bearer_token(api_key)
        self._region_name = region_name
        self._profile_name = profile_name
        self._http_client = http_client or httpx.AsyncClient(
            timeout=BEDROCK_FLEX_READ_TIMEOUT_SECONDS
        )
        self._owns_http_client = http_client is None
        self._credentials_resolver = credentials_resolver
        super().__init__(
            model_name=model_name,
            base_url=base_url,
            api_key=None,
            config=config or GenerateConfig(),
            **model_args,
        )

    async def aclose(self) -> None:
        """Close only the direct HTTP client allocated by this adapter."""
        if self._owns_http_client:
            await self._http_client.aclose()

    def max_tokens_for_config(self, config: GenerateConfig) -> int | None:
        """Keep every Nova 2 Lite condition uncapped by the Inspect default."""
        if normalized_nova_model_id(self.model_name) in _NOVA_FLEX_REASONING_MODEL_IDS:
            return None
        return super().max_tokens_for_config(config)

    def max_tokens(self) -> int | None:
        """Leave Nova 2 Lite uncapped unless the caller supplies an allowed cap."""
        if normalized_nova_model_id(self.model_name) in _NOVA_FLEX_REASONING_MODEL_IDS:
            return None
        return super().max_tokens()

    async def generate(
        self,
        input: list[ChatMessage],
        tools: list[ToolInfo],
        tool_choice: ToolChoice,
        config: GenerateConfig,
    ) -> tuple[ModelOutput | Exception, ModelCall]:
        """Generate through Converse with the route's declared service tier."""
        request = await self._converse_request(input, tools, tool_choice, config)
        model_id, payload = self._converse_payload(request)
        model_call = set_active_model_event_call(
            request=replace_bytes_with_placeholder({"modelId": model_id, **payload})
        )
        started = time.monotonic()

        try:
            self._validate_model(config)
            region = resolve_bedrock_region(
                region_name=self._region_name,
                profile_name=self._profile_name,
            )
            endpoint = self.base_url or bedrock_runtime_endpoint(
                region_name=region,
                profile_name=self._profile_name,
            )
            if self._bearer_token is not None:
                url, headers, body = bearer_flex_converse_request(
                    endpoint=endpoint,
                    model_id=model_id,
                    payload=payload,
                    bearer_token=self._bearer_token,
                )
            else:
                credentials = self._resolve_credentials()
                url, headers, body = signed_flex_converse_request(
                    endpoint=endpoint,
                    region_name=region,
                    model_id=model_id,
                    payload=payload,
                    credentials=credentials,
                )
            response = await self._http_client.post(
                url,
                content=body,
                headers=headers,
                timeout=config.timeout,
            )
            elapsed = time.monotonic() - started
            response_data = _bedrock_response_data(response)
            if response.is_error:
                model_call.set_error(response_data, elapsed)
                response.raise_for_status()
            if not isinstance(response_data, Mapping):
                error = ValueError("Bedrock Converse returned a non-object JSON response.")
                model_call.set_error(response_data, elapsed)
                return error, model_call
            try:
                output = model_output_from_response(
                    self.model_name,
                    ConverseResponse(**response_data),
                    tools,
                )
            except (TypeError, ValueError) as error:
                model_call.set_error(response_data, elapsed)
                return error, model_call
            try:
                served_tier = self._served_tier_from_response(response_data)
            except ValueError as error:
                model_call.set_error(response_data, elapsed)
                return error, model_call
            output.metadata = {
                **dict(output.metadata or {}),
                self._metadata_key(): self._metadata(
                    model_id=model_id,
                    region=region,
                    served_tier=served_tier,
                ),
            }
            model_call.set_response(response_data, elapsed)
            return output, model_call
        except httpx.HTTPStatusError as error:
            return error, model_call
        except httpx.HTTPError as error:
            model_call.set_error({"error": str(error)}, time.monotonic() - started)
            return error, model_call

    def should_retry(self, ex: Exception) -> bool | RetryDecision:
        """Classify raw Converse HTTP failures when the old SDK is bypassed."""
        if isinstance(ex, httpx.HTTPStatusError):
            status = ex.response.status_code
            if status == 429:
                return RetryDecision.rate_limit()
            if status in {500, 502, 503, 504}:
                return RetryDecision.transient()
        return super().should_retry(ex)

    def is_auth_failure(self, ex: Exception) -> bool:
        """Treat ordinary AWS authentication and authorization HTTP failures as auth."""
        if isinstance(ex, httpx.HTTPStatusError):
            return ex.response.status_code in {401, 403}
        return super().is_auth_failure(ex)

    async def _converse_request(
        self,
        input: list[ChatMessage],
        tools: list[ToolInfo],
        tool_choice: ToolChoice,
        config: GenerateConfig,
    ) -> ConverseClientConverseRequest:
        if config.extra_body and (
            "serviceTier" in config.extra_body or "service_tier" in config.extra_body
        ):
            raise ValueError(
                f"{self._route_name} manages serviceTier itself; do not override it "
                "in extra_body."
            )

        self._validate_model(config)
        resolved_tools = converse_tools(tools)
        tool_config = None
        if resolved_tools is not None:
            tool_config = ConverseToolConfig(
                tools=resolved_tools,
                toolChoice=converse_tool_choice(tool_choice),
            )
        system, messages = await converse_messages(
            input, emulate_reasoning=self.is_claude()
        )
        forbid_sampling_params = self.is_claude_4_7_or_later()
        additional_fields = self._additional_model_request_fields(
            config, forbid_sampling_params
        )
        reasoning_cfg = self.reasoning_config(config)
        additional_fields = additional_fields | reasoning_cfg
        nova_2_lite = (
            normalized_nova_model_id(self.model_name)
            in _NOVA_FLEX_REASONING_MODEL_IDS
        )

        return ConverseClientConverseRequest(
            modelId=self.model_name,
            messages=messages,
            system=system,
            inferenceConfig=ConverseInferenceConfig(
                # The owner-approved Nova 2 Lite contract has no artificial
                # output cap for none, low, medium, or high. Drop a caller's
                # inherited Inspect default rather than sending it to Bedrock.
                maxTokens=None if nova_2_lite else config.max_tokens,
                temperature=None if forbid_sampling_params else config.temperature,
                topP=None if forbid_sampling_params else config.top_p,
                stopSequences=config.stop_seqs,
            ),
            additionalModelRequestFields=additional_fields,
            toolConfig=tool_config,
        )

    def _resolve_credentials(self) -> ReadOnlyCredentials:
        if self._credentials_resolver is not None:
            return self._credentials_resolver()
        session = Session(profile=self._profile_name)
        credentials = session.get_credentials()
        if credentials is None:
            raise environment_prerequisite_error(
                "bedrock-flex",
                ["AWS_PROFILE", "AWS_ACCESS_KEY_ID", "AWS_ROLE_ARN"],
            )
        return credentials.get_frozen_credentials()

    def reasoning_config(self, config: GenerateConfig) -> dict[str, Any]:
        """Emit the documented Nova 2 Lite extended-thinking request field."""
        normalized = normalized_nova_model_id(self.model_name)
        if normalized not in _NOVA_FLEX_REASONING_MODEL_IDS:
            return {}
        if config.reasoning_effort is None:
            return {}
        return {
            "reasoningConfig": {
                "type": "enabled",
                "maxReasoningEffort": config.reasoning_effort,
            }
        }

    def _converse_payload(
        self, request: ConverseClientConverseRequest
    ) -> tuple[str, dict[str, Any]]:
        return flex_converse_payload(request)

    def _validate_model(self, config: GenerateConfig) -> None:
        validate_flex_model(self.model_name, config)

    def _served_tier_from_response(self, response: Mapping[str, Any]) -> str:
        served_tier = flex_service_tier_from_response(response)
        if served_tier != "flex":
            raise ValueError(
                "Bedrock served a non-Flex tier for a bedrock-flex request: "
                f"{served_tier!r}."
            )
        return served_tier

    def _metadata_key(self) -> str:
        return "bedrock_flex"

    def _metadata(
        self,
        *,
        model_id: str,
        region: str,
        served_tier: str,
    ) -> dict[str, str]:
        return {
            "auth_mode": (
                "bedrock_api_key" if self._bearer_token is not None else "aws_sigv4"
            ),
            "model_id": model_id,
            "region": region,
            "requested_service_tier": "flex",
            "served_service_tier": served_tier,
        }


@modelapi("bedrock-flex")
class BedrockFlexAPI(_BedrockConverseAPI):
    """Converse provider that explicitly requests Amazon Bedrock Flex."""

    _route_name = "bedrock-flex"


@modelapi("bedrock-standard")
class BedrockStandardAPI(_BedrockConverseAPI):
    """Converse provider for Standard-only Nova models with bearer-key support.

    Standard is selected by omitting ``serviceTier`` entirely. This keeps the
    request on Amazon's documented default tier while reusing the direct HTTP
    Bearer-auth path needed by the pinned Inspect/AWS SDK stack.
    """

    _route_name = "bedrock-standard"

    def _converse_payload(
        self, request: ConverseClientConverseRequest
    ) -> tuple[str, dict[str, Any]]:
        return standard_converse_payload(request)

    def _validate_model(self, config: GenerateConfig) -> None:
        validate_standard_model(self.model_name, config)

    def _served_tier_from_response(self, response: Mapping[str, Any]) -> str:
        return standard_service_tier_from_response(response)

    def _metadata_key(self) -> str:
        return "bedrock_standard"

    def _metadata(
        self,
        *,
        model_id: str,
        region: str,
        served_tier: str,
    ) -> dict[str, str]:
        return {
            "auth_mode": (
                "bedrock_api_key" if self._bearer_token is not None else "aws_sigv4"
            ),
            "model_id": model_id,
            "region": region,
            "requested_service_tier": "standard",
            "wire_service_tier": "omitted",
            "served_service_tier": served_tier,
        }


def _bedrock_response_data(response: httpx.Response) -> object:
    try:
        return response.json()
    except json.JSONDecodeError:
        return {"body": response.text}
