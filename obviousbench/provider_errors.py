"""Provider-generated error/refusal text helpers."""

from __future__ import annotations

PROVIDER_TRANSIENT_OUTPUT_MARKERS = (
    "content violates usage guidelines",
    "failed check: safety_check_",
)


def is_provider_transient_output(output: str | None) -> bool:
    """Return true for provider error payloads delivered as assistant text."""
    if not output:
        return False
    normalized = output.strip().casefold()
    return any(marker in normalized for marker in PROVIDER_TRANSIENT_OUTPUT_MARKERS)
