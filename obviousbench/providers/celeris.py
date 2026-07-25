"""Inspect provider adapter for Celeris' OpenAI-compatible Chat API.

Celeris exposes its single ``celeris-1`` model on a model-scoped,
OpenAI-compatible chat-completions endpoint.  The provider requires a positive
``max_tokens`` value that is a multiple of 256, so validate that contract here
instead of allowing a generic benchmark configuration to fail at runtime.
"""

from __future__ import annotations

import os
from typing import Any

from inspect_ai.model import GenerateConfig, modelapi
from inspect_ai.model._providers.openai_compatible import OpenAICompatibleAPI
from inspect_ai.model._providers.util import environment_prerequisite_error

DEFAULT_CELERIS_BASE_URL = "https://inference.celeris.ai/celeris-1/v1"
CELERIS_API_KEY_VARS = ("CELERIS_API_KEY",)
CELERIS_BASE_URL_VARS = ("CELERIS_BASE_URL", "CELERIS_OPENAI_BASE_URL")
CELERIS_MAX_CONTEXT_TOKENS = 8192
CELERIS_MAX_TOKENS_MULTIPLE = 256


@modelapi("celeris")
class CelerisAPI(OpenAICompatibleAPI):
    """Celeris' documented OpenAI-compatible chat-completions provider."""

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
        resolved_api_key, _ = resolve_celeris_api_key(api_key)
        super().__init__(
            model_name=model_name,
            base_url=resolve_celeris_base_url(base_url),
            api_key=resolved_api_key,
            config=config or GenerateConfig(),
            service="celeris",
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
        """Build a request while enforcing Celeris' documented output cap."""
        params = super().completion_params(config, tools)
        max_tokens = params.get("max_tokens")
        if max_tokens is None:
            return params
        if not isinstance(max_tokens, int) or isinstance(max_tokens, bool):
            raise ValueError(
                "Celeris max_tokens must be a positive integer multiple of "
                f"{CELERIS_MAX_TOKENS_MULTIPLE}; received {max_tokens!r}."
            )
        if max_tokens <= 0 or max_tokens % CELERIS_MAX_TOKENS_MULTIPLE:
            raise ValueError(
                "Celeris max_tokens must be a positive integer multiple of "
                f"{CELERIS_MAX_TOKENS_MULTIPLE}; received {max_tokens!r}."
            )
        if max_tokens > CELERIS_MAX_CONTEXT_TOKENS:
            raise ValueError(
                "Celeris max_tokens cannot exceed its documented "
                f"{CELERIS_MAX_CONTEXT_TOKENS}-token context window; received "
                f"{max_tokens}."
            )
        return params


def resolve_celeris_api_key(api_key: str | None = None) -> tuple[str, str]:
    """Resolve a Celeris API key without exposing it in diagnostics."""
    if api_key:
        return api_key, CELERIS_API_KEY_VARS[0]
    for env_var in CELERIS_API_KEY_VARS:
        value = os.environ.get(env_var)
        if value:
            return value, env_var
    raise environment_prerequisite_error("celeris", list(CELERIS_API_KEY_VARS))


def resolve_celeris_base_url(base_url: str | None = None) -> str:
    """Resolve Celeris' hosted endpoint or an explicit compatible endpoint."""
    if base_url:
        return base_url.rstrip("/")
    for env_var in CELERIS_BASE_URL_VARS:
        value = os.environ.get(env_var)
        if value:
            return value.rstrip("/")
    return DEFAULT_CELERIS_BASE_URL
