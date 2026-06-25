"""Exact string scorer."""

import re
from collections.abc import Iterable
from decimal import Decimal, InvalidOperation

from inspect_ai.scorer import Score, Target, scorer
from inspect_ai.solver import TaskState

from obviousbench.scorers.common import (
    ScoreDecision,
    inspect_score,
    is_non_answer,
    normalize_token_artifacts,
    strip_confidence_annotation,
)

SCORER_NAME = "exact_string_trim_v0"
_NUMBER_RE = re.compile(r"(?<![\w.])-?(?:\d+(?:\.\d+)?|\.\d+)(?![\w.])")
_FINAL_ANSWER_RE = re.compile(
    r"(?:^|[\s.;,:])(?:answer|final answer|result|therefore|so answer)\s*[:=]\s*"
    r"(?P<answer>[^\n.;,]+)[\s.;,!]*$",
    re.IGNORECASE,
)
_ARROW_SUFFIX_RE = re.compile(r"(?:->|→)\s*(?P<answer>[^\n.;,]+)[\s.;,!]*$")
_BECOMES_SUFFIX_RE = re.compile(
    r"^\s*[\w@#$%&*'\"]+\s+becomes\s+(?P<answer>[^\n.;,]+)[\s.;,!]*$",
    re.IGNORECASE,
)
_QUOTED_EQUALS_RE = re.compile(r"=\s*['\"](?P<answer>[^'\"]+)['\"]\s*[.!]?$")
_COLON_SUFFIX_RE = re.compile(r":\s*(?P<answer>[^\n.;,]+)[\s.;,!]*$")
_FINAL_COPULA_RE = re.compile(
    r"\b(?:is|are|was|were)\s+(?P<answer>[^\s\n.;,!?]+)[\s.;,!]*$",
    re.IGNORECASE,
)
_ANSWER_CUE_RE = re.compile(r"\b(?:answer|final answer|result|therefore)\b", re.IGNORECASE)
_REMOVE_LETTER_SUFFIX_RE = re.compile(
    r"without\s+(?:the\s+)?letter\s+['\"]?[A-Za-z]['\"]?\.?",
    re.IGNORECASE,
)
_REPLACEMENT_MARKERS = frozenset("@#$%&*+0")


def score_exact_string_trim(
    output: str,
    target: str,
    accepted_targets: Iterable[str] | None = None,
) -> ScoreDecision:
    primary_decision = _score_exact_string_against_target(output, target)
    if primary_decision.correct:
        return primary_decision
    for accepted_target in _alternate_targets(target, accepted_targets):
        alternate_decision = _score_exact_string_against_target(output, accepted_target)
        if alternate_decision.correct:
            return alternate_decision
    return primary_decision


def _score_exact_string_against_target(output: str, target: str) -> ScoreDecision:
    if is_non_answer(output):
        return ScoreDecision(False, None, "non_answer", "Output was empty.")
    extracted = output.strip()
    if _answers_equal(extracted, target):
        return ScoreDecision(True, extracted, "none", f"Matched {target}.")
    artifact_normalized = normalize_token_artifacts(extracted).strip()
    if artifact_normalized != extracted:
        if _answers_equal(artifact_normalized, target):
            return ScoreDecision(
                True,
                target,
                "verbose_noncompliance",
                f"Matched {target} after removing token artifacts.",
                format_correct=False,
            )
        extracted = artifact_normalized
    extracted_final = _extract_final_answer_candidate(extracted)
    if _answers_equal(extracted_final, target):
        return ScoreDecision(
            True,
            extracted_final or target,
            "verbose_noncompliance",
            f"Matched final answer candidate {target}, with extra text.",
            format_correct=False,
        )
    punctuation_stripped = _strip_terminal_answer_punctuation(extracted)
    if _answers_equal(punctuation_stripped, target):
        return ScoreDecision(
            True,
            target,
            "verbose_noncompliance",
            f"Matched {target} after removing terminal punctuation.",
            format_correct=False,
        )
    confidence_stripped = strip_confidence_annotation(extracted)
    if _answers_equal(confidence_stripped, target):
        return ScoreDecision(
            True,
            target,
            "verbose_noncompliance",
            f"Matched {target} after removing confidence annotation.",
            format_correct=False,
        )
    markdown_stripped = _clean_candidate(extracted)
    if _answers_equal(markdown_stripped, target):
        return ScoreDecision(
            True,
            target,
            "verbose_noncompliance",
            f"Matched {target} after removing markdown wrapper.",
            format_correct=False,
        )
    if _repeated_letter_with_separators_equal(extracted, target):
        return ScoreDecision(
            True,
            extracted,
            "verbose_noncompliance",
            f"Matched repeated-letter target {target} after removing separators.",
            format_correct=False,
        )
    if _replacement_token_with_spacing_equal(extracted, target):
        return ScoreDecision(
            True,
            extracted,
            "verbose_noncompliance",
            f"Matched replacement target {target} after removing internal spacing.",
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
    if _starts_with_target_remove_letter_explanation(extracted, target):
        return ScoreDecision(
            True,
            target,
            "verbose_noncompliance",
            f"Matched {target}, with remove-letter explanation.",
            format_correct=False,
        )
    first_line = _first_line_candidate(extracted)
    if _answers_equal(first_line, target):
        return ScoreDecision(
            True,
            target,
            "verbose_noncompliance",
            f"Matched first-line answer {target}, with extra text.",
            format_correct=False,
        )
    last_line = _last_line_candidate(extracted)
    if _answers_equal(last_line, target):
        return ScoreDecision(
            True,
            last_line or target,
            "verbose_noncompliance",
            f"Matched final-line answer {target}, with extra text.",
            format_correct=False,
        )
    equation_rhs_decision = _score_numeric_equation_rhs(extracted, target)
    if equation_rhs_decision is not None and equation_rhs_decision.correct:
        return equation_rhs_decision
    numeric_decision = _score_single_numeric_with_optional_units(extracted, target)
    if numeric_decision is not None and numeric_decision.correct:
        return numeric_decision
    copula_candidate = _extract_final_copula_candidate(extracted)
    if _answers_equal(copula_candidate, target):
        return ScoreDecision(
            True,
            copula_candidate or target,
            "verbose_noncompliance",
            f"Matched final sentence answer {target}, with extra text.",
            format_correct=False,
        )
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


def _alternate_targets(
    target: str,
    accepted_targets: Iterable[str] | None,
) -> tuple[str, ...]:
    if accepted_targets is None:
        return ()
    targets: list[str] = []
    seen = {target.strip().casefold()}
    for accepted_target in accepted_targets:
        normalized = str(accepted_target).strip()
        if not normalized:
            continue
        key = normalized.casefold()
        if key in seen:
            continue
        seen.add(key)
        targets.append(normalized)
    return tuple(targets)


def _answers_equal(candidate: str | None, target: str) -> bool:
    if candidate is None:
        return False
    return candidate.strip().casefold() == target.strip().casefold()


def _extract_final_answer_candidate(output: str) -> str | None:
    for pattern in (
        _QUOTED_EQUALS_RE,
        _ARROW_SUFFIX_RE,
        _BECOMES_SUFFIX_RE,
        _FINAL_ANSWER_RE,
        _COLON_SUFFIX_RE,
    ):
        match = pattern.search(output)
        if match:
            return _clean_candidate(match.group("answer"))
    return None


def _extract_final_copula_candidate(output: str) -> str | None:
    match = _FINAL_COPULA_RE.search(output)
    if match is None:
        return None
    return _clean_candidate(match.group("answer"))


def _starts_with_target(output: str, target: str) -> bool:
    if not target:
        return False
    if not output.casefold().startswith(target.casefold()) or len(output) == len(target):
        return False
    remainder = output[len(target) :].lstrip()
    if not remainder:
        return False
    if remainder.startswith(("(", "[", "{", ":", "-")):
        return True
    return re.match(r"^(?:is|are|was|were)\b", remainder, re.IGNORECASE) is not None


def _starts_with_target_remove_letter_explanation(output: str, target: str) -> bool:
    if (
        not target
        or not output.casefold().startswith(target.casefold())
        or len(output) == len(target)
    ):
        return False
    remainder = output[len(target) :].strip()
    return bool(_REMOVE_LETTER_SUFFIX_RE.fullmatch(remainder))


def _ends_with_target_after_answer_cue(output: str, target: str) -> bool:
    if not output.endswith(target) or not _ANSWER_CUE_RE.search(output):
        return False
    prefix = output[: -len(target)]
    return bool(prefix) and prefix[-1] in " \t\r\n:=-"


def _clean_candidate(value: str) -> str:
    candidate = normalize_token_artifacts(value).strip()
    for wrapper in ("**", "__", "~~", "`"):
        if candidate.startswith(wrapper) and candidate.endswith(wrapper):
            candidate = candidate[len(wrapper) : -len(wrapper)].strip()
    if len(candidate) >= 2 and candidate[0] == candidate[-1] and candidate[0] in {
        '"',
        "'",
    }:
        candidate = candidate[1:-1].strip()
    return candidate


def _repeated_letter_with_separators_equal(candidate: str, target: str) -> bool:
    normalized_target = target.strip().casefold()
    if len(normalized_target) < 2 or len(set(normalized_target)) != 1:
        return False
    if not normalized_target.isalpha():
        return False
    normalized_candidate = normalize_token_artifacts(candidate).strip().casefold()
    if not normalized_candidate:
        return False
    if normalized_candidate == normalized_target:
        return False
    if any(char.isalnum() and char != normalized_target[0] for char in normalized_candidate):
        return False
    letters_only = "".join(char for char in normalized_candidate if char.isalpha())
    return letters_only == normalized_target


def _replacement_token_with_spacing_equal(candidate: str, target: str) -> bool:
    normalized_target = target.strip().casefold()
    if not normalized_target or any(char.isspace() for char in normalized_target):
        return False
    if not any(char.isalpha() for char in normalized_target):
        return False
    if not any(char in _REPLACEMENT_MARKERS for char in normalized_target):
        return False
    normalized_candidate = normalize_token_artifacts(candidate).strip().casefold()
    if normalized_candidate == normalized_target:
        return False
    if "\n" in normalized_candidate or "\r" in normalized_candidate:
        return False
    if not any(char in " \t" for char in normalized_candidate):
        return False
    without_spacing = re.sub(r"[ \t]+", "", normalized_candidate)
    return without_spacing == normalized_target


def _strip_terminal_answer_punctuation(value: str) -> str | None:
    stripped = value.strip()
    if not stripped:
        return None
    without_punctuation = stripped.rstrip(".!?;,").strip()
    if without_punctuation == stripped:
        return None
    return without_punctuation or None


def _first_line_candidate(output: str) -> str | None:
    lines = output.splitlines()
    if len(lines) < 2:
        return None
    first_nonempty_index = next(
        (index for index, line in enumerate(lines) if line.strip()),
        None,
    )
    if first_nonempty_index is None:
        return None
    if not any(line.strip() for line in lines[first_nonempty_index + 1 :]):
        return None
    return _clean_candidate(lines[first_nonempty_index])


def _last_line_candidate(output: str) -> str | None:
    lines = output.splitlines()
    if len(lines) < 2:
        return None
    last_nonempty_index = next(
        (index for index in range(len(lines) - 1, -1, -1) if lines[index].strip()),
        None,
    )
    if last_nonempty_index is None:
        return None
    if not any(line.strip() for line in lines[:last_nonempty_index]):
        return None
    return _clean_candidate(lines[last_nonempty_index])


def _score_numeric_equation_rhs(output: str, target: str) -> ScoreDecision | None:
    if "=" not in output:
        return None
    try:
        target_decimal = Decimal(target)
    except InvalidOperation:
        return None

    rhs = output.rsplit("=", 1)[1]
    candidates = _NUMBER_RE.findall(rhs)
    if len(candidates) != 1:
        return None
    extracted = candidates[0]
    try:
        extracted_decimal = Decimal(extracted)
    except InvalidOperation:
        return None
    if extracted_decimal != target_decimal:
        return None
    return ScoreDecision(
        True,
        extracted,
        "verbose_noncompliance",
        f"Matched numeric equation result {target}, with extra text.",
        format_correct=False,
    )


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
