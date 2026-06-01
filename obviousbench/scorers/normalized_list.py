"""Normalized list scorer."""

import re

from inspect_ai.scorer import Score, Target, scorer
from inspect_ai.solver import TaskState

from obviousbench.scorers.common import (
    ScoreDecision,
    inspect_score,
    normalize_list,
    strip_confidence_annotation,
)

SCORER_NAME = "normalized_list_v0"
_FINAL_LIST_RE = re.compile(
    r"(?:^|[\s.;,:])(?:answer|final answer|result|therefore|so answer)\s*[:=]\s*"
    r"(?P<answer>[^\n]+)$",
    re.IGNORECASE,
)


def score_normalized_list(output: str, target: str) -> ScoreDecision:
    cleaned_output = strip_confidence_annotation(output)
    extracted_parts = normalize_list(cleaned_output)
    target_parts = normalize_list(target)
    extracted = ", ".join(extracted_parts) if extracted_parts else None
    if not extracted_parts:
        return ScoreDecision(False, None, "non_answer", "No list items found.")
    if extracted_parts == target_parts:
        failure_type = (
            "verbose_noncompliance"
            if cleaned_output.strip() != output.strip()
            else "none"
        )
        return ScoreDecision(
            True,
            ", ".join(extracted_parts),
            failure_type,
            "List matched.",
            format_correct=False if failure_type == "verbose_noncompliance" else None,
        )
    final_parts = _extract_final_list_parts(output)
    if final_parts == target_parts:
        return ScoreDecision(
            True,
            ", ".join(final_parts),
            "verbose_noncompliance",
            "Matched final list candidate.",
            format_correct=False,
        )
    if _starts_with_target_list(output.strip(), target.strip()):
        return ScoreDecision(
            True,
            ", ".join(target_parts),
            "verbose_noncompliance",
            "Matched leading list with extra text.",
            format_correct=False,
        )
    return ScoreDecision(False, extracted, "ordering_error", "List did not match target order.")


def _extract_final_list_parts(output: str) -> tuple[str, ...] | None:
    match = _FINAL_LIST_RE.search(output.strip())
    if match is None:
        return None
    return normalize_list(match.group("answer"))


def _starts_with_target_list(output: str, target: str) -> bool:
    if not target or not output.startswith(target) or len(output) == len(target):
        return False
    remainder = output[len(target) :].lstrip()
    if not remainder:
        return False
    return remainder.startswith(("(", "[", "{", ":", "-"))


@scorer(metrics=[])
def normalized_list_scorer():
    async def score(state: TaskState, target: Target) -> Score:
        decision = score_normalized_list(state.output.completion, target.text)
        return inspect_score(decision, SCORER_NAME)

    return score
