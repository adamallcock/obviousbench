"""Word/list-count scorer."""

from inspect_ai.scorer import Score, Target, scorer
from inspect_ai.solver import TaskState

from obviousbench.scorers.common import inspect_score
from obviousbench.scorers.exact_integer import score_exact_integer_extract_first

SCORER_NAME = "word_count_v0"


def score_word_count(output: str, target: str):
    decision = score_exact_integer_extract_first(output, target)
    if not decision.correct and decision.failure_type == "incorrect_count":
        return decision.__class__(
            decision.correct,
            decision.extracted,
            "list_count_error",
            decision.explanation,
        )
    return decision


@scorer(metrics=[])
def word_count_scorer():
    async def score(state: TaskState, target: Target) -> Score:
        decision = score_word_count(state.output.completion, target.text)
        return inspect_score(decision, SCORER_NAME)

    return score

