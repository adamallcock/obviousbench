"""Multiple-choice letter scorer."""

import re

from inspect_ai.scorer import Score, Target, scorer
from inspect_ai.solver import TaskState

from obviousbench.scorers.common import ScoreDecision, inspect_score, is_non_answer

SCORER_NAME = "multiple_choice_letter_v0"
_LETTER_RE = re.compile(r"^[A-D]$")


def score_multiple_choice_letter(output: str, target: str) -> ScoreDecision:
    if is_non_answer(output):
        return ScoreDecision(False, None, "non_answer", "Output was empty.")
    extracted = output.strip().upper()
    if _LETTER_RE.fullmatch(extracted):
        if extracted == target.strip().upper():
            return ScoreDecision(True, extracted, "none", "Choice matched.")
        return ScoreDecision(False, extracted, "negation_error", "Choice did not match.")
    if target.strip().upper() in extracted:
        return ScoreDecision(False, extracted, "verbose_noncompliance", "Output was verbose.")
    return ScoreDecision(
        False,
        extracted,
        "format_noncompliance",
        "Output was not a choice letter.",
    )


@scorer(metrics=[])
def multiple_choice_letter():
    async def score(state: TaskState, target: Target) -> Score:
        decision = score_multiple_choice_letter(state.output.completion, target.text)
        return inspect_score(decision, SCORER_NAME, strict_format=True)

    return score
