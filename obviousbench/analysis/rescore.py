"""Recompute deterministic scorer decisions from logged model completions."""

from __future__ import annotations

from obviousbench.scorers.common import ScoreDecision
from obviousbench.scorers.dynamic import score_by_name


def rescore_output(
    *,
    scorer_name: str,
    output: str,
    target: str,
    accepted_targets: tuple[str, ...] = (),
) -> ScoreDecision:
    """Score an existing model completion with the current scorer implementation."""
    return score_by_name(
        scorer_name,
        output,
        target,
        accepted_targets=accepted_targets,
    )
