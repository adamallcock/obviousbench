"""Regex scorer for strict format tasks."""

import re

from inspect_ai.scorer import Score, Target, scorer
from inspect_ai.solver import TaskState

from obviousbench.scorers.common import ScoreDecision, inspect_score, is_non_answer

SCORER_NAME = "regex_match_v0"


def score_regex_match(output: str, target_pattern: str) -> ScoreDecision:
    if is_non_answer(output):
        return ScoreDecision(False, None, "non_answer", "Output was empty.")
    extracted = output.strip()
    if re.fullmatch(target_pattern, extracted):
        return ScoreDecision(True, extracted, "none", "Regex matched.")
    return ScoreDecision(False, extracted, "format_noncompliance", "Regex did not match.")


@scorer(metrics=[])
def regex_match_scorer():
    async def score(state: TaskState, target: Target) -> Score:
        decision = score_regex_match(state.output.completion, target.text)
        return inspect_score(decision, SCORER_NAME, strict_format=True)

    return score

