"""Transparent derived efficiency metrics."""

from __future__ import annotations


def safe_ratio(
    numerator: float | int | None,
    denominator: float | int | None,
) -> float | None:
    if numerator is None or denominator in {None, 0}:
        return None
    return float(numerator) / float(denominator)


def tokens_per_correct(*, total_tokens: int, correct: int) -> float | None:
    return safe_ratio(total_tokens, correct)


def cost_per_correct_usd(
    *,
    estimated_cost_usd: float | None,
    correct: int,
) -> float | None:
    return safe_ratio(estimated_cost_usd, correct)


def overthinking_index(*, reasoning_tokens: int, output_tokens: int) -> float | None:
    return safe_ratio(reasoning_tokens, max(output_tokens, 1))


def reasoning_token_share(
    *,
    reasoning_tokens: int,
    total_tokens: int,
) -> float | None:
    return safe_ratio(reasoning_tokens, total_tokens)
