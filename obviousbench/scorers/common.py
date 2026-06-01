"""Shared scorer helpers."""

from __future__ import annotations

import re
from dataclasses import dataclass

from inspect_ai.scorer import CORRECT, INCORRECT, Score


@dataclass(frozen=True)
class ScoreDecision:
    correct: bool
    extracted: str | None
    failure_type: str
    explanation: str
    format_correct: bool | None = None

    @property
    def answer_correct(self) -> bool:
        return self.correct

    @property
    def resolved_format_correct(self) -> bool:
        if self.format_correct is not None:
            return self.format_correct
        return self.failure_type not in FORMAT_FAILURE_TYPES

    @property
    def strict_correct(self) -> bool:
        return self.answer_correct and self.resolved_format_correct


FORMAT_FAILURE_TYPES = {
    "format_noncompliance",
    "verbose_noncompliance",
    "json_malformed",
}

_CONFIDENCE_ANNOTATION_RE = re.compile(
    r"\s*(?:\\+confidence\s*\{[^{}]*\}|\[?confidence\s*[:=]\s*\d+(?:\.\d+)?%?\]?)\s*$",
    re.IGNORECASE,
)


def inspect_score(
    decision: ScoreDecision,
    scorer_name: str,
    *,
    strict_format: bool = False,
) -> Score:
    return Score(
        value=CORRECT if decision.correct else INCORRECT,
        answer=decision.extracted,
        explanation=decision.explanation,
        metadata={
            "failure_type": decision.failure_type,
            "scorer_name": scorer_name,
            "strict_format": strict_format,
            "answer_correct": decision.answer_correct,
            "format_correct": decision.resolved_format_correct,
            "strict_correct": decision.strict_correct,
        },
    )


def is_non_answer(output: str) -> bool:
    return not output or not output.strip()


def normalize_string(value: str) -> str:
    return value.strip()


def normalize_string_casefold(value: str) -> str:
    return value.strip().casefold()


def strip_confidence_annotation(value: str) -> str:
    return _CONFIDENCE_ANNOTATION_RE.sub("", value).strip()


_INTEGER_RE = re.compile(r"(?<![\w.])-?\d+(?![\w])")
_INTEGER_WORDS = {
    "zero": "0",
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
    "ten": "10",
    "eleven": "11",
    "twelve": "12",
    "thirteen": "13",
    "fourteen": "14",
    "fifteen": "15",
    "sixteen": "16",
    "seventeen": "17",
    "eighteen": "18",
    "nineteen": "19",
    "twenty": "20",
}
_INTEGER_WORD_RE = re.compile(
    r"\b(" + "|".join(sorted(_INTEGER_WORDS, key=len, reverse=True)) + r")\b",
    re.IGNORECASE,
)


def extract_integer_candidates(output: str) -> list[str]:
    digit_candidates = _INTEGER_RE.findall(output)
    word_candidates = [
        _INTEGER_WORDS[match.group(1).casefold()]
        for match in _INTEGER_WORD_RE.finditer(output)
    ]
    return [*digit_candidates, *word_candidates]


def extract_single_integer(output: str) -> tuple[str | None, bool]:
    candidates = extract_integer_candidates(output)
    if not candidates:
        return None, False
    unique = set(candidates)
    if len(unique) > 1:
        return None, True
    return candidates[0], False


def normalize_list(value: str) -> tuple[str, ...]:
    normalized = _strip_enclosing_list_markup(strip_confidence_annotation(value))
    if not normalized:
        return ()
    parts = normalized.split(",") if "," in normalized else normalized.split()
    return tuple(_normalize_list_part(part) for part in parts if part.strip())


def _strip_enclosing_list_markup(value: str) -> str:
    if len(value) < 2:
        return value
    pairs = {"[": "]", "(": ")", "{": "}"}
    expected_close = pairs.get(value[0])
    if expected_close is not None and value[-1] == expected_close:
        return value[1:-1].strip()
    return value


def _normalize_list_part(value: str) -> str:
    normalized = value.strip()
    if len(normalized) >= 2 and normalized[0] == normalized[-1] and normalized[0] in {
        '"',
        "'",
    }:
        normalized = normalized[1:-1].strip()
    return normalized.casefold()
