"""JSON exact-field scorer."""

import json

from inspect_ai.scorer import Score, Target, scorer
from inspect_ai.solver import TaskState

from obviousbench.scorers.common import ScoreDecision, inspect_score, is_non_answer

SCORER_NAME = "json_exact_field_v0"


def score_json_exact_field(output: str, target: str, field: str = "answer") -> ScoreDecision:
    if is_non_answer(output):
        return ScoreDecision(False, None, "non_answer", "Output was empty.")
    try:
        parsed = json.loads(output)
    except json.JSONDecodeError as exc:
        return ScoreDecision(False, None, "json_malformed", exc.msg)
    if not isinstance(parsed, dict) or field not in parsed:
        return ScoreDecision(False, None, "format_noncompliance", f"Missing field {field!r}.")
    extracted = str(parsed[field])
    if extracted == target:
        return ScoreDecision(True, extracted, "none", "JSON field matched.")
    return ScoreDecision(False, extracted, "wrong_letter_or_substring", "JSON field mismatch.")


@scorer(metrics=[])
def json_exact_field():
    async def score(state: TaskState, target: Target) -> Score:
        decision = score_json_exact_field(state.output.completion, target.text)
        return inspect_score(decision, SCORER_NAME, strict_format=True)

    return score

