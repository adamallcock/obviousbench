"""JSON exact-field scorer."""

import json

from inspect_ai.scorer import Score, Target, scorer
from inspect_ai.solver import TaskState

from obviousbench.scorers.common import (
    ScoreDecision,
    inspect_score,
    is_non_answer,
    normalize_token_artifacts,
)

SCORER_NAME = "json_exact_field_v0"


def score_json_exact_field(output: str, target: str, field: str = "answer") -> ScoreDecision:
    if is_non_answer(output):
        return ScoreDecision(False, None, "non_answer", "Output was empty.")
    raw_stripped = output.strip()
    stripped = normalize_token_artifacts(raw_stripped).strip()
    had_token_artifacts = stripped != raw_stripped
    json_text, was_fenced = _strip_json_fence(stripped)
    try:
        parsed = json.loads(json_text)
    except json.JSONDecodeError as exc:
        return ScoreDecision(False, None, "json_malformed", exc.msg)
    if not isinstance(parsed, dict) or field not in parsed:
        return ScoreDecision(False, None, "format_noncompliance", f"Missing field {field!r}.")
    extracted = _json_value_to_answer_text(parsed[field])
    if extracted == target:
        if was_fenced or had_token_artifacts:
            reason = (
                "JSON field matched after removing token artifacts."
                if had_token_artifacts
                else "JSON field matched inside fenced block."
            )
            return ScoreDecision(
                True,
                extracted,
                "verbose_noncompliance",
                reason,
                format_correct=False,
            )
        return ScoreDecision(True, extracted, "none", "JSON field matched.")
    return ScoreDecision(False, extracted, "wrong_letter_or_substring", "JSON field mismatch.")


def _json_value_to_answer_text(value) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if value is None:
        return "null"
    return str(value)


def _strip_json_fence(output: str) -> tuple[str, bool]:
    lines = output.splitlines()
    if len(lines) >= 3 and lines[0].strip().startswith("```") and lines[-1].strip() == "```":
        return "\n".join(lines[1:-1]).strip(), True
    return output, False


@scorer(metrics=[])
def json_exact_field():
    async def score(state: TaskState, target: Target) -> Score:
        decision = score_json_exact_field(state.output.completion, target.text)
        return inspect_score(decision, SCORER_NAME, strict_format=True)

    return score
