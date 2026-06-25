"""Deterministic yes/no scorer with separate answer and format correctness."""

from __future__ import annotations

import re

from inspect_ai.scorer import Score, Target, scorer
from inspect_ai.solver import TaskState

from obviousbench.scorers.common import (
    ScoreDecision,
    inspect_score,
    is_non_answer,
    normalize_token_artifacts,
)

SCORER_NAME = "yes_no_v0"

_STRICT_YES_NO_RE = re.compile(r"(yes|no)", re.IGNORECASE)
_YES_NO_TOKEN_RE = re.compile(r"\b(yes|no)\b", re.IGNORECASE)
_FINAL_CUE_RE = re.compile(
    r"\b(?:final\s+answer|answer|the\s+answer\s+is)\s*[:\-]?\s*(yes|no)\b",
    re.IGNORECASE,
)
_CORRECTION_CUE_RE = re.compile(
    r"\b(?:correct\s+(?:response|answer)|right\s+answer|actual\s+answer)\b"
    r"[^\n.]{0,80}\b(yes|no)\b"
    r"|\b(?:should\s+be|would\s+have\s+been|would\s+be|is\s+actually)"
    r"\s*[:\-]?\s*(yes|no)\b",
    re.IGNORECASE,
)
_ANSWER_LIKE_LINE_START_RE = re.compile(r"^(yes|no)\s*(?:[.!?:;,\-]|$)", re.IGNORECASE)


def score_yes_no(output: str, target: str) -> ScoreDecision:
    target_answer = _normalize_target(target)
    if target_answer is None:
        return ScoreDecision(
            False,
            None,
            "format_noncompliance",
            f"Unsupported yes/no target: {target}",
            format_correct=False,
        )
    return score_yes_no_target(output, target_answer)


def score_yes_no_target(output: str, target_answer: str) -> ScoreDecision:
    if is_non_answer(output):
        return ScoreDecision(
            False,
            None,
            "non_answer",
            "Output was empty.",
            format_correct=False,
        )
    normalized = normalize_token_artifacts(output).strip()
    strict = _STRICT_YES_NO_RE.fullmatch(normalized)
    if strict:
        answer = strict.group(1)
        if answer.casefold() == target_answer:
            return ScoreDecision(True, answer, "none", "Yes/no answer matched.")
        return ScoreDecision(
            False,
            answer,
            "wrong_letter_or_substring",
            "Yes/no answer did not match target.",
            format_correct=True,
        )

    first_line = _first_non_empty_line(normalized)
    final_cues = [match.group(1) for match in _FINAL_CUE_RE.finditer(normalized)]
    if final_cues:
        folded = [answer.casefold() for answer in final_cues]
        if (
            (first_match := _STRICT_YES_NO_RE.fullmatch(first_line or ""))
            and first_match.group(1).casefold() not in set(folded)
        ):
            return ScoreDecision(
                False,
                first_match.group(1),
                "ambiguous_output",
                "Leading yes/no answer conflicts with a later final answer cue.",
                format_correct=False,
            )
        if len(set(folded)) > 1:
            return ScoreDecision(
                False,
                final_cues[-1],
                "ambiguous_output",
                "Conflicting final yes/no cues.",
                format_correct=False,
            )
        return _verbose_decision(
            final_cues[-1],
            target_answer,
            "Final yes/no cue",
        )

    tokens = [match.group(1) for match in _YES_NO_TOKEN_RE.finditer(normalized)]
    answer_only_lines = [
        match.group(1)
        for line in normalized.splitlines()
        if (match := _STRICT_YES_NO_RE.fullmatch(line.strip()))
    ]
    last_line = _last_non_empty_line(normalized)
    if answer_only_lines and _STRICT_YES_NO_RE.fullmatch(last_line or ""):
        if len({answer.casefold() for answer in answer_only_lines}) > 1:
            return ScoreDecision(
                False,
                answer_only_lines[-1],
                "ambiguous_output",
                "Conflicting answer-only yes/no lines.",
                format_correct=False,
            )
        return _verbose_decision(
            answer_only_lines[-1],
            target_answer,
            "Answer-only yes/no line",
        )
    if (
        answer_only_lines
        and _STRICT_YES_NO_RE.fullmatch(first_line or "")
        and len({answer.casefold() for answer in answer_only_lines}) == 1
    ):
        token_answers = {token.casefold() for token in tokens}
        if len(token_answers) > 1 and _has_later_answer_like_cue(normalized):
            return ScoreDecision(
                False,
                answer_only_lines[0],
                "ambiguous_output",
                "Leading answer conflicts with a later yes/no answer cue.",
                format_correct=False,
            )
        return _verbose_decision(
            answer_only_lines[0],
            target_answer,
            "Leading answer-only yes/no line",
        )
    if len({token.casefold() for token in tokens}) > 1:
        return ScoreDecision(
            False,
            tokens[0],
            "ambiguous_output",
            "Output contains both yes and no.",
            format_correct=False,
        )
    if tokens:
        first = tokens[0]
        if _starts_with_independent_yes_no(normalized):
            return _verbose_decision(first, target_answer, "Leading yes/no token")
        return _verbose_decision(first, target_answer, "First yes/no token")

    return ScoreDecision(
        False,
        None,
        "format_noncompliance",
        "No yes/no answer found.",
        format_correct=False,
    )


def _verbose_decision(answer: str, target_answer: str, source: str) -> ScoreDecision:
    if answer.casefold() == target_answer:
        return ScoreDecision(
            True,
            answer,
            "verbose_noncompliance",
            f"{source} matched target.",
            format_correct=False,
        )
    return ScoreDecision(
        False,
        answer,
        "wrong_letter_or_substring",
        f"{source} did not match target.",
        format_correct=False,
    )


def _normalize_target(target: str) -> str | None:
    target = str(target).strip().casefold()
    return target if target in {"yes", "no"} else None


def _starts_with_independent_yes_no(value: str) -> bool:
    return _YES_NO_TOKEN_RE.match(value) is not None


def _last_non_empty_line(value: str) -> str:
    return next(
        (line.strip() for line in reversed(value.splitlines()) if line.strip()),
        "",
    )


def _first_non_empty_line(value: str) -> str:
    return next((line.strip() for line in value.splitlines() if line.strip()), "")


def _has_later_answer_like_cue(value: str) -> bool:
    lines = [line.strip() for line in value.splitlines() if line.strip()]
    later_text = "\n".join(lines[1:])
    if not later_text:
        return False
    if _CORRECTION_CUE_RE.search(later_text):
        return True
    return any(_ANSWER_LIKE_LINE_START_RE.match(line) for line in lines[1:])


@scorer(metrics=[])
def yes_no_scorer():
    async def score(state: TaskState, target: Target) -> Score:
        decision = score_yes_no(state.output.completion, target.text)
        return inspect_score(decision, SCORER_NAME, strict_format=True)

    return score
