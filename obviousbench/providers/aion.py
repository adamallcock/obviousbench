"""Inspect provider adapter for AionLabs' OpenAI-compatible API."""

from __future__ import annotations

import os
from typing import Any

from inspect_ai.model import GenerateConfig, modelapi
from inspect_ai.model._providers.openai_compatible import OpenAICompatibleAPI
from inspect_ai.model._providers.util import environment_prerequisite_error

DEFAULT_AION_BASE_URL = "https://api.aionlabs.ai/v1"
AION_API_KEY_VARS = ("AIONLABS_API_KEY", "AION_API_KEY")
AION_BASE_URL_VARS = ("AIONLABS_BASE_URL", "AION_BASE_URL")
AION_2_0_MODEL_IDS = frozenset({"aion-2.0", "aion-labs/aion-2.0"})
AION_2_0_REASONING_EFFORTS = frozenset({"none", "low", "medium", "high"})


@modelapi("aion")
class AionAPI(OpenAICompatibleAPI):
    """AionLabs' OpenAI-compatible chat-completions provider.

    The documented selectable effort control belongs to Aion 2.0. Other active
    Aion models can be benchmarked at their provider default, but this adapter
    refuses to imply that they expose the same effort parameter.
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
        resolved_api_key, _ = resolve_aion_api_key(api_key)
        super().__init__(
            model_name=model_name,
            base_url=resolve_aion_base_url(base_url),
            api_key=resolved_api_key,
            config=config or GenerateConfig(),
            service="aion",
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
        """Validate Aion's documented model-specific reasoning control."""
        params = super().completion_params(config, tools)
        effort = params.get("reasoning_effort")
        if effort is None:
            return params
        model_id = self.service_model_name()
        if model_id not in AION_2_0_MODEL_IDS:
            raise ValueError(
                f"{model_id} has no documented selectable Aion reasoning_effort; "
                "run it at provider default instead."
            )
        if effort not in AION_2_0_REASONING_EFFORTS:
            allowed = ", ".join(sorted(AION_2_0_REASONING_EFFORTS))
            raise ValueError(
                f"{model_id} supports reasoning_effort values: {allowed}; "
                f"received {effort!r}."
            )
        return params


def resolve_aion_api_key(api_key: str | None = None) -> tuple[str, str]:
    """Resolve an AionLabs API key without exposing it in diagnostics."""
    if api_key:
        return api_key, AION_API_KEY_VARS[0]
    for env_var in AION_API_KEY_VARS:
        value = os.environ.get(env_var)
        if value:
            return value, env_var
    raise environment_prerequisite_error("aion", list(AION_API_KEY_VARS))


def resolve_aion_base_url(base_url: str | None = None) -> str:
    """Resolve AionLabs' hosted endpoint or an explicit compatible endpoint."""
    if base_url:
        return base_url.rstrip("/")
    for env_var in AION_BASE_URL_VARS:
        value = os.environ.get(env_var)
        if value:
            return value.rstrip("/")
    return DEFAULT_AION_BASE_URL
