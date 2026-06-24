"""Provider-generated error/refusal text helpers."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ProviderOutputClassification:
    failure_type: str
    message: str


PROVIDER_TRANSIENT_OUTPUT_CLASSIFIERS = (
    (
        (
            "real-time cyber safeguards",
            "violative cyber content",
        ),
        ProviderOutputClassification(
            failure_type="provider_safeguard",
            message=(
                "Provider safeguard block: Anthropic real-time safeguards "
                "classified this response as cyber-related."
            ),
        ),
    ),
    (
        (
            "usage policy",
            "potentially violating our usage policy",
            "violating our usage policy",
        ),
        ProviderOutputClassification(
            failure_type="provider_safeguard",
            message="Provider safeguard block: usage-policy filter response.",
        ),
    ),
    (
        (
            "content violates usage guidelines",
            "failed check: safety_check_",
        ),
        ProviderOutputClassification(
            failure_type="provider_safety_check",
            message="Provider safety-check block returned as assistant text.",
        ),
    ),
)


PROVIDER_TRANSIENT_OUTPUT_MARKERS = tuple(
    marker
    for markers, _classification in PROVIDER_TRANSIENT_OUTPUT_CLASSIFIERS
    for marker in markers
)


def classify_provider_transient_output(
    output: str | None,
) -> ProviderOutputClassification | None:
    """Return a display-oriented classification for provider error payloads."""
    if not output:
        return None
    normalized = output.strip().casefold()
    for markers, classification in PROVIDER_TRANSIENT_OUTPUT_CLASSIFIERS:
        if any(marker in normalized for marker in markers):
            return classification
    return None


def is_provider_transient_output(output: str | None) -> bool:
    """Return true for provider error payloads delivered as assistant text."""
    return classify_provider_transient_output(output) is not None
