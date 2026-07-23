"""Inspect provider adapter for LongCat's OpenAI-compatible Chat API.

LongCat exposes one current text model through a standard chat-completions
endpoint. Its reasoning switch is provider-specific, so this module registers
the endpoint and rejects malformed ``thinking.type`` values without pretending
that LongCat exposes a tunable low/medium/high effort scale.
"""

from __future__ import annotations

import os
from typing import Any

from inspect_ai.model import GenerateConfig, modelapi
from inspect_ai.model._providers.openai_compatible import OpenAICompatibleAPI
from inspect_ai.model._providers.util import environment_prerequisite_error

DEFAULT_LONGCAT_BASE_URL = "https://api.longcat.chat/openai/v1"
LONGCAT_API_KEY_VARS = ("LONGCAT_API_KEY",)
LONGCAT_BASE_URL_VARS = ("LONGCAT_BASE_URL", "LONGCAT_OPENAI_BASE_URL")
LONGCAT_THINKING_TYPES = frozenset({"enabled", "disabled"})


@modelapi("longcat")
class LongCatAPI(OpenAICompatibleAPI):
    """LongCat's OpenAI-compatible chat-completions provider.

    Use ``GenerateConfig.extra_body`` to supply the documented switch, for
    example ``{"thinking": {"type": "disabled"}}`` or ``{"thinking":
    {"type": "enabled"}}``. The benchmark registry records these as the two
    vendor settings; it does not infer unsupported effort levels.
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
        resolved_api_key, _ = resolve_longcat_api_key(api_key)
        super().__init__(
            model_name=model_name,
            base_url=resolve_longcat_base_url(base_url),
            api_key=resolved_api_key,
            config=config or GenerateConfig(),
            service="longcat",
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
        """Build a request while validating LongCat's finite thinking switch."""
        params = super().completion_params(config, tools)
        thinking = (params.get("extra_body") or {}).get("thinking")
        if thinking is None:
            return params
        if not isinstance(thinking, dict) or thinking.get("type") not in LONGCAT_THINKING_TYPES:
            allowed = ", ".join(sorted(LONGCAT_THINKING_TYPES))
            raise ValueError(
                "LongCat thinking must be an object with type one of "
                f"{allowed}; received {thinking!r}."
            )
        return params


def resolve_longcat_api_key(api_key: str | None = None) -> tuple[str, str]:
    """Resolve a LongCat API key without exposing it in diagnostics."""
    if api_key:
        return api_key, LONGCAT_API_KEY_VARS[0]
    for env_var in LONGCAT_API_KEY_VARS:
        value = os.environ.get(env_var)
        if value:
            return value, env_var
    raise environment_prerequisite_error("longcat", list(LONGCAT_API_KEY_VARS))


def resolve_longcat_base_url(base_url: str | None = None) -> str:
    """Resolve LongCat's hosted endpoint or an explicit compatible endpoint."""
    if base_url:
        return base_url.rstrip("/")
    for env_var in LONGCAT_BASE_URL_VARS:
        value = os.environ.get(env_var)
        if value:
            return value.rstrip("/")
    return DEFAULT_LONGCAT_BASE_URL
