"""Multiple-choice letter scorer."""

import re

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
_ANSWER_CHOICE_RE = re.compile(
    r"\b(?:answer|choice|option|final answer)\s*(?:is|:|=)?\s*"
    r"(?:[*_`~]+)?(?P<choice>[A-D])(?:[*_`~]+)?\b",
    re.IGNORECASE,
)


def score_multiple_choice_letter(output: str, target: str) -> ScoreDecision:
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
            return ScoreDecision(
                True,
                choice,
                "verbose_noncompliance",
                "Choice matched in verbose output.",
            )
        return ScoreDecision(False, choice, "negation_error", "Choice did not match.")
    return ScoreDecision(
        False,
        extracted,
        "format_noncompliance",
        "Output was not a choice letter.",
    )


def _extract_choice(output: str) -> str | None:
    for pattern in (_LEADING_CHOICE_RE, _LEADING_MARKDOWN_CHOICE_RE, _ANSWER_CHOICE_RE):
        match = pattern.search(output)
        if match:
            return match.group("choice").upper()
    return None


@scorer(metrics=[])
def multiple_choice_letter():
    async def score(state: TaskState, target: Target) -> Score:
        decision = score_multiple_choice_letter(state.output.completion, target.text)
        return inspect_score(decision, SCORER_NAME, strict_format=True)

    return score
