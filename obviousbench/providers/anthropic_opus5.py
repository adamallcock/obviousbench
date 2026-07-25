"""Claude Opus 5 compatibility route for the installed Inspect Anthropic API.

Anthropic documents ``thinking: {"type": "disabled"}`` as valid for Claude
Opus 5 at high or lower effort.  The installed Inspect release conservatively
excludes non-Sonnet Claude 5 models from that request shape.  This narrow route
keeps the upstream Anthropic transport while correcting only the documented
Opus 5 capability needed by the benchmark's explicit no-thinking row.
"""

from __future__ import annotations

from typing import Any

from inspect_ai.model import GenerateConfig, modelapi
from inspect_ai.model._providers.anthropic import AnthropicAPI


@modelapi("anthropic-opus5")
class AnthropicOpus5API(AnthropicAPI):
    """Anthropic API with the documented Opus 5 disable-thinking capability."""

    def _supports_disabling_thinking(self) -> bool:
        if self.model_family().startswith("claude-opus-5"):
            return True
        return super()._supports_disabling_thinking()

    def completion_config(
        self, config: GenerateConfig
    ) -> tuple[dict[str, Any], dict[str, Any], dict[str, str], list[str]]:
        """Preserve the documented Opus 5 no-thinking wire contract.

        Inspect's Anthropic provider has changed where it applies disabled
        thinking across releases.  Enforce the documented Opus 5 request shape
        after the upstream configuration path so the explicit no-thinking row
        cannot silently become an adaptive-thinking request after an upgrade.
        """
        params, extra_body, headers, betas = super().completion_config(config)
        if config.reasoning_effort == "none" and self._supports_disabling_thinking():
            params["thinking"] = {"type": "disabled"}
        return params, extra_body, headers, betas
