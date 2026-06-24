"""Regex scorer for strict format tasks."""

import re

from inspect_ai.scorer import Score, Target, scorer
from inspect_ai.solver import TaskState

from obviousbench.scorers.common import ScoreDecision, inspect_score, is_non_answer
from obviousbench.scorers.yes_no import score_yes_no_target

SCORER_NAME = "regex_match_v0"


def score_regex_match(output: str, target_pattern: str) -> ScoreDecision:
    if is_non_answer(output):
        return ScoreDecision(
            False,
            None,
            "non_answer",
            "Output was empty.",
            format_correct=False,
        )
    extracted = output.strip()
    if re.fullmatch(target_pattern, extracted):
        return ScoreDecision(True, extracted, "none", "Regex matched.")
    yes_no_target = _yes_no_target_for_pattern(target_pattern)
    if yes_no_target is not None:
        return score_yes_no_target(extracted, yes_no_target)
    leading_answer = _first_non_empty_line(extracted)
    if leading_answer != extracted:
        if re.fullmatch(target_pattern, leading_answer):
            return ScoreDecision(
                True,
                leading_answer,
                "verbose_noncompliance",
                "Leading answer matched regex.",
                format_correct=False,
            )
        return ScoreDecision(
            False,
            leading_answer,
            "format_noncompliance",
            "Leading answer did not match regex.",
        )
    return ScoreDecision(False, extracted, "format_noncompliance", "Regex did not match.")


def _yes_no_target_for_pattern(target_pattern: str) -> str | None:
    try:
        matches_yes = re.fullmatch(target_pattern, "yes") is not None
        matches_no = re.fullmatch(target_pattern, "no") is not None
    except re.error:
        return None
    if matches_yes == matches_no:
        return None
    return "yes" if matches_yes else "no"


def _first_non_empty_line(value: str) -> str:
    return next((line.strip() for line in value.splitlines() if line.strip()), value)


@scorer(metrics=[])
def regex_match_scorer():
    async def score(state: TaskState, target: Target) -> Score:
        decision = score_regex_match(state.output.completion, target.text)
        return inspect_score(decision, SCORER_NAME, strict_format=True)

    return score
