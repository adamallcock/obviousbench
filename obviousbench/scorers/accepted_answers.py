"""Accepted-answer overrides for reviewed ambiguous items."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

PLANET_ITEM_ACCEPTED_ANSWERS = ("mars", "saturn", "uranus", "pluto")

ITEM_ACCEPTED_ANSWER_OVERRIDES: dict[str, tuple[str, ...]] = {
    "obviousbench.spell.en.v0.public.000014": PLANET_ITEM_ACCEPTED_ANSWERS,
}


def accepted_answers_for_sample(
    *,
    sample_id: str | None = None,
    metadata: Mapping[str, Any] | None = None,
    target: str | None = None,
    scorer_name: str | None = None,
) -> tuple[str, ...]:
    answers: list[str] = []
    if metadata:
        answers.extend(_metadata_accepted_answers(metadata))
        answers.extend(
            _multiple_choice_option_text_answers(
                metadata,
                target=target,
                scorer_name=scorer_name,
            )
        )
        benchmark_metadata = metadata.get("benchmark_metadata")
        if isinstance(benchmark_metadata, Mapping):
            answers.extend(_metadata_accepted_answers(benchmark_metadata))
            answers.extend(
                _multiple_choice_option_text_answers(
                    benchmark_metadata,
                    target=target,
                    scorer_name=scorer_name,
                )
            )
    if sample_id:
        answers.extend(ITEM_ACCEPTED_ANSWER_OVERRIDES.get(sample_id, ()))
    return _dedupe_answers(answers)


def _metadata_accepted_answers(metadata: Mapping[str, Any]) -> tuple[str, ...]:
    return (
        *_coerce_answers(metadata.get("accepted_answers")),
        *_coerce_answers(metadata.get("accepted_targets")),
    )


def _coerce_answers(value: Any) -> tuple[str, ...]:
    if value is None:
        return ()
    if isinstance(value, str):
        return (value,)
    if isinstance(value, Sequence):
        return tuple(str(answer) for answer in value if str(answer).strip())
    return ()


def _multiple_choice_option_text_answers(
    metadata: Mapping[str, Any],
    *,
    target: str | None,
    scorer_name: str | None,
) -> tuple[str, ...]:
    if scorer_name != "multiple_choice_letter_v0" or target is None:
        return ()
    normalized_target = str(target).strip().upper()
    if normalized_target not in {"A", "B", "C", "D"}:
        return ()
    choices = metadata.get("choices")
    if not isinstance(choices, Sequence) or isinstance(choices, str):
        return ()
    index = ord(normalized_target) - ord("A")
    if index >= len(choices):
        return ()
    choice = str(choices[index]).strip()
    return (choice,) if choice else ()


def _dedupe_answers(values: Sequence[str]) -> tuple[str, ...]:
    answers: list[str] = []
    seen: set[str] = set()
    for value in values:
        answer = str(value).strip()
        if not answer:
            continue
        key = answer.casefold()
        if key in seen:
            continue
        seen.add(key)
        answers.append(answer)
    return tuple(answers)
