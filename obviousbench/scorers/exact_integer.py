"""Integer extraction scorer."""

from inspect_ai.scorer import Score, Target, scorer
from inspect_ai.solver import TaskState

from obviousbench.scorers.common import (
    ScoreDecision,
    extract_integer_candidates,
    extract_single_integer,
    inspect_score,
    is_non_answer,
)

SCORER_NAME = "exact_integer_extract_first_v0"


def score_exact_integer_extract_first(output: str, target: str) -> ScoreDecision:
    if is_non_answer(output):
        return ScoreDecision(False, None, "non_answer", "Output was empty.")
    candidates = extract_integer_candidates(output)
    normalized_target = str(target)
    if len(set(candidates)) > 1 and candidates[0] == normalized_target:
        return ScoreDecision(
            True,
            candidates[0],
            "verbose_noncompliance",
            f"Leading integer matched {normalized_target}.",
        )
    extracted, ambiguous = extract_single_integer(output)
    if ambiguous:
        return ScoreDecision(False, None, "ambiguous_output", f"Ambiguous output: {output}")
    if extracted is None:
        return ScoreDecision(False, None, "non_answer", f"No integer found: {output}")
    if extracted == normalized_target:
        return ScoreDecision(True, extracted, "none", f"Extracted {extracted}.")
    return ScoreDecision(False, extracted, "incorrect_count", f"Extracted {extracted}.")


@scorer(metrics=[])
def exact_integer_extract_first():
    async def score(state: TaskState, target: Target) -> Score:
        decision = score_exact_integer_extract_first(state.output.completion, target.text)
        return inspect_score(decision, SCORER_NAME)

    return score
