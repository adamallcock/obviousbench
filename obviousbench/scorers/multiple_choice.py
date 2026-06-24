"""Multiple-choice letter scorer."""

import re
from collections.abc import Iterable

from inspect_ai.scorer import Score, Target, scorer
from inspect_ai.solver import TaskState

from obviousbench.scorers.common import ScoreDecision, inspect_score, is_non_answer

SCORER_NAME = "multiple_choice_letter_v0"
_LETTER_RE = re.compile(r"^[A-D]$")
_LEADING_CHOICE_RE = re.compile(r"^\s*(?P<choice>[A-D])(?:[\s.)}:,-]|$)", re.IGNORECASE)
_LEADING_MARKDOWN_CHOICE_RE = re.compile(
    r"^\s*(?:[*_`~]+)?(?P<choice>[A-D])(?:[*_`~]+)?(?:[\s.)}:,-]|$)",
    re.IGNORECASE,
)
_BARE_PUNCTUATED_CHOICE_RE = re.compile(
    r"^\s*(?:[*_`~]+)?(?P<choice>[A-D])(?:[*_`~]+)?\.?\s*$",
    re.IGNORECASE,
)
_ANSWER_CHOICE_RE = re.compile(
    r"\b(?:correct\s+)?(?:answer|choice|option|final answer)\s*"
    r"(?:is\s*)?(?:[:=]\s*)?"
    r"(?:[*_`~]+)?(?P<choice>[A-D])(?:[*_`~]+)?\b",
    re.IGNORECASE,
)
_FINAL_STANDALONE_CHOICE_RE = re.compile(
    r"(?:^|[\r\n])\s*(?:[*_`~]+)?(?P<choice>[A-D])(?:[*_`~]+)?[.)]?\s*$",
    re.IGNORECASE,
)
_BOXED_CHOICE_RE = re.compile(
    r"\\boxed\{\s*(?P<choice>[A-D])\s*\}",
    re.IGNORECASE,
)
_ANSWER_OPTION_TEXT_RE = re.compile(
    r"^\s*(?:the\s+)?(?:answer|choice|option|final answer)\s*(?:is|:|=)\s*"
    r"(?P<option>.+?)\s*$",
    re.IGNORECASE,
)


def score_multiple_choice_letter(
    output: str,
    target: str,
    *,
    accepted_targets: Iterable[str] | None = None,
) -> ScoreDecision:
    if is_non_answer(output):
        return ScoreDecision(False, None, "non_answer", "Output was empty.")
    stripped = output.strip()
    extracted = stripped.upper()
    normalized_target = target.strip().upper()
    if _LETTER_RE.fullmatch(extracted):
        if extracted == normalized_target:
            return ScoreDecision(True, extracted, "none", "Choice matched.")
        return ScoreDecision(False, extracted, "negation_error", "Choice did not match.")

    choice = _extract_choice(stripped)
    if choice is not None:
        if choice == normalized_target:
            if _is_bare_punctuated_choice(stripped, choice):
                return ScoreDecision(
                    True,
                    choice,
                    "none",
                    "Choice matched.",
                )
            if _matches_leading_choice_with_accepted_option_text(
                stripped,
                accepted_targets,
            ):
                return ScoreDecision(
                    True,
                    choice,
                    "none",
                    "Choice and option text matched.",
                )
            return ScoreDecision(
                True,
                choice,
                "verbose_noncompliance",
                "Choice matched in verbose output.",
            )
        return ScoreDecision(False, choice, "negation_error", "Choice did not match.")
    if _LETTER_RE.fullmatch(normalized_target) and _matches_accepted_option_text(
        stripped,
        accepted_targets,
    ):
        return ScoreDecision(
            True,
            normalized_target,
            "none",
            "Matched correct option text.",
        )
    return ScoreDecision(
        False,
        extracted,
        "format_noncompliance",
        "Output was not a choice letter.",
    )


def _extract_choice(output: str) -> str | None:
    for pattern in (
        _LEADING_CHOICE_RE,
        _LEADING_MARKDOWN_CHOICE_RE,
        _ANSWER_CHOICE_RE,
        _FINAL_STANDALONE_CHOICE_RE,
        _BOXED_CHOICE_RE,
    ):
        match = pattern.search(output)
        if match:
            return match.group("choice").upper()
    return None


def _is_bare_punctuated_choice(output: str, choice: str) -> bool:
    match = _BARE_PUNCTUATED_CHOICE_RE.fullmatch(output)
    return match is not None and match.group("choice").upper() == choice


def _matches_leading_choice_with_accepted_option_text(
    output: str,
    accepted_targets: Iterable[str] | None,
) -> bool:
    match = _LEADING_CHOICE_RE.search(output) or _LEADING_MARKDOWN_CHOICE_RE.search(output)
    if match is None:
        return False
    option_text = output[match.end() :].strip().strip("*_`~")
    return bool(option_text) and _matches_accepted_option_text(
        option_text,
        accepted_targets,
    )


def _matches_accepted_option_text(
    output: str,
    accepted_targets: Iterable[str] | None,
) -> bool:
    if accepted_targets is None:
        return False
    candidates = {_normalize_option_text(output)}
    match = _ANSWER_OPTION_TEXT_RE.fullmatch(output)
    if match is not None:
        candidates.add(_normalize_option_text(match.group("option")))
    return any(
        _normalize_option_text(target) in candidates
        for target in accepted_targets
        if str(target).strip()
    )


def _normalize_option_text(value: str) -> str:
    normalized = str(value).strip().strip("*_`~")
    if len(normalized) >= 2 and normalized[0] == normalized[-1] and normalized[0] in {
        '"',
        "'",
    }:
        normalized = normalized[1:-1].strip()
    return normalized.rstrip(".!?").casefold()


@scorer(metrics=[])
def multiple_choice_letter():
    async def score(state: TaskState, target: Target) -> Score:
        decision = score_multiple_choice_letter(state.output.completion, target.text)
        return inspect_score(decision, SCORER_NAME, strict_format=True)

    return score
