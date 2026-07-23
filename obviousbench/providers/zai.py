"""Inspect provider adapter for Z.AI's OpenAI-compatible GLM API.

GLM-5.2 uses an OpenAI-compatible chat-completions endpoint but has a paired
``thinking`` object and ``reasoning_effort`` control.  This route preserves
those vendor fields and rejects ambiguous combinations before a paid request.
"""

from __future__ import annotations

import os
from typing import Any

from inspect_ai.model import GenerateConfig, modelapi
from inspect_ai.model._providers.openai_compatible import OpenAICompatibleAPI
from inspect_ai.model._providers.util import environment_prerequisite_error

DEFAULT_ZAI_BASE_URL = "https://api.z.ai/api/paas/v4"
ZAI_API_KEY_VARS = ("ZAI_API_KEY",)
ZAI_BASE_URL_VARS = ("ZAI_BASE_URL",)
ZAI_REASONING_EFFORTS = frozenset(
    {"none", "minimal", "low", "medium", "high", "xhigh", "max"}
)
ZAI_THINKING_TYPES = frozenset({"enabled", "disabled"})


@modelapi("zai")
class ZAIAPI(OpenAICompatibleAPI):
    """Z.AI's OpenAI-compatible GLM-5.2 chat-completions provider.

    The release registry emits only the distinct requested benchmark settings:
    disabled thinking, enabled/high, and enabled/xhigh. The adapter accepts
    every documented Z.AI spelling so it remains a faithful transport, while
    explicitly rejecting a reasoning-effort value paired with disabled or
    omitted thinking.
    """

    def __init__(
        self,
        model_name: str,
        base_url: str | None = None,
        api_key: str | None = None,
        config: GenerateConfig | None = None,
        responses_api: bool | None = False,
        responses_store: bool | None = None,
        stream: bool | None = None,
        strict_tools: bool = True,
        client_timeout: float | None = None,
        **model_args: Any,
    ) -> None:
        resolved_api_key, _ = resolve_zai_api_key(api_key)
        super().__init__(
            model_name=model_name,
            base_url=resolve_zai_base_url(base_url),
            api_key=resolved_api_key,
            config=config or GenerateConfig(),
            service="zai",
            responses_api=responses_api,
            responses_store=responses_store,
            stream=stream,
            strict_tools=strict_tools,
            client_timeout=client_timeout,
            **model_args,
        )

    def completion_params(
        self,
        config: GenerateConfig,
        tools: bool,
    ) -> dict[str, Any]:
        """Validate GLM's coupled deep-thinking request controls."""
        params = super().completion_params(config, tools)
        extra_body = params.get("extra_body") or {}
        thinking = extra_body.get("thinking")
        effort = params.get("reasoning_effort")

        if thinking is None:
            if effort is not None:
                raise ValueError(
                    "Z.AI reasoning_effort requires explicit "
                    "extra_body.thinking.type='enabled'."
                )
            return params
        if not isinstance(thinking, dict) or thinking.get("type") not in ZAI_THINKING_TYPES:
            allowed = ", ".join(sorted(ZAI_THINKING_TYPES))
            raise ValueError(
                "Z.AI thinking must be an object with type one of "
                f"{allowed}; received {thinking!r}."
            )
        if thinking["type"] == "disabled":
            if effort is not None:
                raise ValueError(
                    "Z.AI disabled thinking cannot be combined with reasoning_effort."
                )
            return params
        if effort is not None and effort not in ZAI_REASONING_EFFORTS:
            allowed = ", ".join(sorted(ZAI_REASONING_EFFORTS))
            raise ValueError(
                f"Z.AI reasoning_effort must be one of {allowed}; received {effort!r}."
            )
        return params


def resolve_zai_api_key(api_key: str | None = None) -> tuple[str, str]:
    """Resolve a Z.AI API key without exposing it in diagnostics."""
    if api_key:
        return api_key, ZAI_API_KEY_VARS[0]
    for env_var in ZAI_API_KEY_VARS:
        value = os.environ.get(env_var)
        if value:
            return value, env_var
    raise environment_prerequisite_error("zai", list(ZAI_API_KEY_VARS))


def resolve_zai_base_url(base_url: str | None = None) -> str:
    """Resolve Z.AI's hosted OpenAI-compatible endpoint."""
    if base_url:
        return base_url.rstrip("/")
    for env_var in ZAI_BASE_URL_VARS:
        value = os.environ.get(env_var)
        if value:
            return value.rstrip("/")
    return DEFAULT_ZAI_BASE_URL
