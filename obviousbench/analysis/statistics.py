"""Small standard-library statistics helpers for benchmark reports."""

from __future__ import annotations

import random
from dataclasses import dataclass
from math import ceil, floor

BOOTSTRAP_SEED = 20260531
BOOTSTRAP_RESAMPLES = 1_000


@dataclass(frozen=True)
class PairedDelta:
    matched_samples: int
    baseline_only: int
    comparison_only: int
    wins: int
    losses: int
    ties: int
    delta: float
    ci_low: float
    ci_high: float


def wilson_interval(
    successes: int,
    n: int,
    z: float = 1.959963984540054,
) -> tuple[float, float]:
    """Return the Wilson score interval for a binomial proportion."""
    if n <= 0:
        return (0.0, 0.0)
    p = successes / n
    denominator = 1 + z * z / n
    center = (p + z * z / (2 * n)) / denominator
    margin = z * ((p * (1 - p) / n + z * z / (4 * n * n)) ** 0.5) / denominator
    return (max(0.0, center - margin), min(1.0, center + margin))


def paired_boolean_delta(
    *,
    baseline: dict[str, bool],
    comparison: dict[str, bool],
    seed: int = BOOTSTRAP_SEED,
    resamples: int = BOOTSTRAP_RESAMPLES,
) -> PairedDelta:
    """Compute paired boolean deltas over matched sample IDs."""
    baseline_ids = set(baseline)
    comparison_ids = set(comparison)
    matched_ids = sorted(baseline_ids & comparison_ids)
    deltas = [
        int(comparison[sample_id]) - int(baseline[sample_id])
        for sample_id in matched_ids
    ]
    wins = sum(delta == 1 for delta in deltas)
    losses = sum(delta == -1 for delta in deltas)
    ties = sum(delta == 0 for delta in deltas)
    delta = sum(deltas) / len(deltas) if deltas else 0.0
    ci_low, ci_high = bootstrap_mean_interval(deltas, seed=seed, resamples=resamples)
    return PairedDelta(
        matched_samples=len(matched_ids),
        baseline_only=len(baseline_ids - comparison_ids),
        comparison_only=len(comparison_ids - baseline_ids),
        wins=wins,
        losses=losses,
        ties=ties,
        delta=delta,
        ci_low=ci_low,
        ci_high=ci_high,
    )


def bootstrap_mean_interval(
    values: list[int],
    *,
    seed: int = BOOTSTRAP_SEED,
    resamples: int = BOOTSTRAP_RESAMPLES,
) -> tuple[float, float]:
    """Return a deterministic percentile bootstrap interval for a mean."""
    if not values:
        return (0.0, 0.0)
    if len(values) == 1 or resamples <= 0:
        mean = float(values[0])
        return (mean, mean)

    rng = random.Random(seed)
    count = len(values)
    means = [
        sum(values[rng.randrange(count)] for _ in range(count)) / count
        for _ in range(resamples)
    ]
    means.sort()
    lower_index = floor((resamples - 1) * 0.025)
    upper_index = ceil((resamples - 1) * 0.975)
    return (means[lower_index], means[upper_index])
