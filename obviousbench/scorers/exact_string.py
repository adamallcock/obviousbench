"""Exact string scorer."""

import re
from decimal import Decimal, InvalidOperation

from inspect_ai.scorer import Score, Target, scorer
from inspect_ai.solver import TaskState

from obviousbench.scorers.common import (
    ScoreDecision,
    inspect_score,
    is_non_answer,
    strip_confidence_annotation,
)

SCORER_NAME = "exact_string_trim_v0"
_NUMBER_RE = re.compile(r"(?<![\w.])-?(?:\d+(?:\.\d+)?|\.\d+)(?![\w.])")
_FINAL_ANSWER_RE = re.compile(
    r"(?:^|[\s.;,:])(?:answer|final answer|result|therefore|so answer)\s*[:=]\s*"
    r"(?P<answer>[^\n.;,]+)[\s.;,!]*$",
    re.IGNORECASE,
)
_QUOTED_EQUALS_RE = re.compile(r"=\s*['\"](?P<answer>[^'\"]+)['\"]\s*[.!]?$")
_COLON_SUFFIX_RE = re.compile(r":\s*(?P<answer>[^\n.;,]+)[\s.;,!]*$")
_ANSWER_CUE_RE = re.compile(r"\b(?:answer|final answer|result|therefore)\b", re.IGNORECASE)


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
            "verbose_noncompliance",
            f"Matched final answer candidate {target}, with extra text.",
            format_correct=False,
        )
    confidence_stripped = strip_confidence_annotation(extracted)
    if confidence_stripped == target:
        return ScoreDecision(
            True,
            target,
            "verbose_noncompliance",
            f"Matched {target} after removing confidence annotation.",
            format_correct=False,
        )
    if _starts_with_target(extracted, target):
        return ScoreDecision(
            True,
            target,
            "verbose_noncompliance",
            f"Matched {target}, with extra text.",
            format_correct=False,
        )
    numeric_decision = _score_single_numeric_with_optional_units(extracted, target)
    if numeric_decision is not None:
        return numeric_decision
    if _ends_with_target_after_answer_cue(extracted, target):
        return ScoreDecision(
            True,
            target,
            "verbose_noncompliance",
            f"Matched {target}, with extra text.",
            format_correct=False,
        )
    return ScoreDecision(
        False,
        extracted,
        "wrong_letter_or_substring",
        f"Expected {target!r}, got {extracted!r}.",
    )


def _extract_final_answer_candidate(output: str) -> str | None:
    for pattern in (_QUOTED_EQUALS_RE, _FINAL_ANSWER_RE, _COLON_SUFFIX_RE):
        match = pattern.search(output)
        if match:
            return _clean_candidate(match.group("answer"))
    return None


def _starts_with_target(output: str, target: str) -> bool:
    if not target:
        return False
    if not output.startswith(target) or len(output) == len(target):
        return False
    remainder = output[len(target) :].lstrip()
    if not remainder:
        return False
    return remainder.startswith(("(", "[", "{", ":", "-"))


def _ends_with_target_after_answer_cue(output: str, target: str) -> bool:
    if not output.endswith(target) or not _ANSWER_CUE_RE.search(output):
        return False
    prefix = output[: -len(target)]
    return bool(prefix) and prefix[-1] in " \t\r\n:=-"


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
