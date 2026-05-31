"""Exact string scorer."""

import re
from decimal import Decimal, InvalidOperation

from inspect_ai.scorer import Score, Target, scorer
from inspect_ai.solver import TaskState

from obviousbench.scorers.common import ScoreDecision, inspect_score, is_non_answer

SCORER_NAME = "exact_string_trim_v0"
_NUMBER_RE = re.compile(r"(?<![\w.])-?(?:\d+(?:\.\d+)?|\.\d+)(?![\w.])")
_FINAL_ANSWER_RE = re.compile(
    r"(?:^|[\s.;,:])(?:answer|final answer|result|therefore|so answer)\s*[:=]\s*"
    r"(?P<answer>[^\n.;,]+)[\s.;,!]*$",
    re.IGNORECASE,
)
_QUOTED_EQUALS_RE = re.compile(r"=\s*['\"](?P<answer>[^'\"]+)['\"]\s*[.!]?$")


def score_exact_string_trim(output: str, target: str) -> ScoreDecision:
    if is_non_answer(output):
        return ScoreDecision(False, None, "non_answer", "Output was empty.")
    extracted = output.strip()
    if extracted == target:
        return ScoreDecision(True, extracted, "none", f"Matched {target}.")
    extracted_final = _extract_final_answer_candidate(extracted)
    if extracted_final == target:
        return ScoreDecision(
            True,
            extracted_final,
            "none",
            f"Matched final answer candidate {target}.",
        )
    numeric_decision = _score_single_numeric_with_optional_units(extracted, target)
    if numeric_decision is not None:
        return numeric_decision
    return ScoreDecision(
        False,
        extracted,
        "wrong_letter_or_substring",
        f"Expected {target!r}, got {extracted!r}.",
    )


def _extract_final_answer_candidate(output: str) -> str | None:
    for pattern in (_QUOTED_EQUALS_RE, _FINAL_ANSWER_RE):
        match = pattern.search(output)
        if match:
            return _clean_candidate(match.group("answer"))
    return None


def _clean_candidate(value: str) -> str:
    candidate = value.strip()
    if len(candidate) >= 2 and candidate[0] == candidate[-1] and candidate[0] in {
        '"',
        "'",
    }:
        candidate = candidate[1:-1].strip()
    return candidate


def _score_single_numeric_with_optional_units(output: str, target: str) -> ScoreDecision | None:
    try:
        target_decimal = Decimal(target)
    except InvalidOperation:
        return None

    candidates = _NUMBER_RE.findall(output)
    if not candidates:
        return None
    if len(candidates) > 1:
        return ScoreDecision(
            False,
            output,
            "ambiguous_output",
            f"Ambiguous numeric output: {output}",
        )

    extracted = candidates[0]
    try:
        extracted_decimal = Decimal(extracted)
    except InvalidOperation:
        return None

    if extracted_decimal == target_decimal:
        return ScoreDecision(
            True,
            extracted,
            "none",
            f"Matched numeric value {target} with optional unit text.",
        )
    return None


@scorer(metrics=[])
def exact_string_trim():
    async def score(state: TaskState, target: Target) -> Score:
        decision = score_exact_string_trim(state.output.completion, target.text)
        return inspect_score(decision, SCORER_NAME, strict_format=True)

    return score
