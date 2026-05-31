"""Normalized list scorer."""

from inspect_ai.scorer import Score, Target, scorer
from inspect_ai.solver import TaskState

from obviousbench.scorers.common import ScoreDecision, inspect_score, normalize_list

SCORER_NAME = "normalized_list_v0"


def score_normalized_list(output: str, target: str) -> ScoreDecision:
    extracted_parts = normalize_list(output)
    target_parts = normalize_list(target)
    extracted = ", ".join(extracted_parts) if extracted_parts else None
    if not extracted_parts:
        return ScoreDecision(False, None, "non_answer", "No list items found.")
    if extracted_parts == target_parts:
        return ScoreDecision(True, ", ".join(extracted_parts), "none", "List matched.")
    return ScoreDecision(False, extracted, "ordering_error", "List did not match target order.")


@scorer(metrics=[])
def normalized_list_scorer():
    async def score(state: TaskState, target: Target) -> Score:
        decision = score_normalized_list(state.output.completion, target.text)
        return inspect_score(decision, SCORER_NAME)

    return score

