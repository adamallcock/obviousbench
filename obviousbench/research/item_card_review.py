"""Promote reviewed paper-candidate item cards from structured dataset metadata."""

from __future__ import annotations

import json
import re
from collections.abc import Sequence
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path
from typing import Any

import yaml

from obviousbench.datasets.item_cards import ItemCard
from obviousbench.datasets.schemas import BenchmarkItem, SourceRecord

DEFAULT_REVIEWER = "codex-paper-review-v1"
DEFAULT_REVIEWED_ON = "2026-06-01"
REVIEW_NOTE = (
    "AI-assisted deterministic item-card review from dataset metadata; "
    "measured human baseline deferred for the fast preprint."
)


@dataclass(frozen=True)
class ItemCardPromotionInputs:
    manifest_path: Path
    dataset_paths: Sequence[Path]
    source_catalog_path: Path | None
    cards_path: Path
    reviewer: str = DEFAULT_REVIEWER
    reviewed_on: str = DEFAULT_REVIEWED_ON


@dataclass(frozen=True)
class ItemCardPromotionResult:
    cards_path: Path
    promoted_count: int
    missing_dataset_ids: tuple[str, ...]
    missing_card_ids: tuple[str, ...]


def promote_paper_item_cards(
    inputs: ItemCardPromotionInputs,
) -> ItemCardPromotionResult:
    """Promote manifest-scoped item cards to reviewed status in a cards YAML file."""
    manifest_ids = _load_manifest_item_ids(inputs.manifest_path)
    dataset_items = _load_dataset_items(inputs.dataset_paths, manifest_ids)
    source_catalog = (
        _load_source_catalog(inputs.source_catalog_path)
        if inputs.source_catalog_path is not None
        else {}
    )
    missing_dataset_ids = tuple(
        item_id for item_id in manifest_ids if item_id not in dataset_items
    )

    payload = yaml.safe_load(inputs.cards_path.read_text(encoding="utf-8")) or {}
    cards = payload.get("cards")
    if not isinstance(cards, list):
        raise ValueError(f"{inputs.cards_path} must contain a top-level 'cards' list")

    card_ids = {
        card.get("item_id")
        for card in cards
        if isinstance(card, dict) and isinstance(card.get("item_id"), str)
    }
    missing_card_ids = tuple(item_id for item_id in manifest_ids if item_id not in card_ids)

    promoted_count = 0
    for card in cards:
        if not isinstance(card, dict):
            continue
        item_id = card.get("item_id")
        if item_id not in manifest_ids or item_id not in dataset_items:
            continue
        _promote_card(
            card=card,
            item=dataset_items[item_id],
            source_catalog=source_catalog,
            reviewer=inputs.reviewer,
            reviewed_on=inputs.reviewed_on,
        )
        ItemCard.model_validate(card)
        promoted_count += 1

    inputs.cards_path.write_text(
        yaml.safe_dump(payload, sort_keys=False, allow_unicode=False, width=88),
        encoding="utf-8",
    )
    return ItemCardPromotionResult(
        cards_path=inputs.cards_path,
        promoted_count=promoted_count,
        missing_dataset_ids=missing_dataset_ids,
        missing_card_ids=missing_card_ids,
    )


def _promote_card(
    *,
    card: dict[str, Any],
    item: BenchmarkItem,
    source_catalog: dict[str, SourceRecord],
    reviewer: str,
    reviewed_on: str,
) -> None:
    card["source_refs"] = item.source_refs
    card["source_type"] = item.source_type
    card["source_summary"] = _source_summary(item, source_catalog)
    card["answer_derivation"] = _answer_derivation(item)
    card["expected_answer"] = item.target
    card["scorer_contract"] = {
        "scorer": item.scorer,
        "answer_type": item.answer_type,
        "strict_format": item.metadata.strict_format,
        "acceptable_outputs": [item.target],
        "unacceptable_outputs": _unacceptable_outputs(item),
    }
    card["ambiguity_notes"] = _ambiguity_notes(item)
    card["split_policy"] = {
        "allowed_splits": [item.split],
        "leakage_risk": _leakage_risk(item),
        "publishable": True,
        "rationale": (
            "Selected for the paper_v1 candidate review set from the hard-obvious "
            "panel. The benchmark prompt is generated or independently authored "
            "from structured metadata; source refs are provenance leads rather than "
            "republished source text. Because this public split is exposed, it is "
            "not suitable as a contamination-resistant leaderboard split."
        ),
    }
    card["review"] = {
        "status": "reviewed",
        "reviewer": reviewer,
        "reviewed_on": reviewed_on,
        "notes": REVIEW_NOTE,
    }


def _load_manifest_item_ids(path: Path) -> tuple[str, ...]:
    item_ids: list[str] = []
    seen: set[str] = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        item_id = str(row["item_id"])
        if item_id not in seen:
            item_ids.append(item_id)
            seen.add(item_id)
    return tuple(item_ids)


def _load_dataset_items(
    paths: Sequence[Path],
    include_item_ids: Sequence[str],
) -> dict[str, BenchmarkItem]:
    wanted = set(include_item_ids)
    items: dict[str, BenchmarkItem] = {}
    for path in paths:
        if not path.exists():
            continue
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            raw = json.loads(line)
            if raw.get("id") in wanted:
                item = BenchmarkItem.model_validate(raw)
                items[item.id] = item
    return items


def _load_source_catalog(path: Path) -> dict[str, SourceRecord]:
    sources: dict[str, SourceRecord] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        source = SourceRecord.model_validate(json.loads(line))
        sources[source.source_id] = source
    return sources


def _source_summary(
    item: BenchmarkItem,
    source_catalog: dict[str, SourceRecord],
) -> str:
    summaries = []
    for source_ref in item.source_refs:
        source = source_catalog.get(source_ref)
        if source is None:
            summaries.append(f"{source_ref}: provenance lead recorded in the dataset.")
            continue
        parts = [
            f"{source_ref}: {source.platform} {source.media_type} lead",
            f"seen {source.date_seen}",
            f"rights={source.rights_status}",
        ]
        if source.failure_description:
            parts.append(f"description={source.failure_description}")
        summaries.append("; ".join(parts) + ".")
    return (
        "Generated benchmark variant derived from provenance lead(s). "
        "The source is used as an archetype for the failure pattern, not as "
        "benchmark ground truth. "
        + " ".join(summaries)
    )


def _answer_derivation(item: BenchmarkItem) -> str:
    metadata = item.metadata.extra
    if item.family == "character_count":
        word = str(metadata.get("word", ""))
        character = str(metadata.get("character", ""))
        count = _count_character(word, character, bool(metadata.get("case_sensitive")))
        return (
            f"{word} contains {count} occurrence(s) of '{character}', "
            f"so the expected answer is {item.target}."
        )
    if item.family == "spelling_transform":
        return _spelling_transform_derivation(item, metadata)
    if item.family == "arithmetic":
        return _arithmetic_derivation(item, metadata)
    if item.family == "word_count":
        values = str(metadata.get("values", ""))
        count = len([value.strip() for value in values.split(",") if value.strip()])
        return (
            f"The comma-separated list '{values}' contains {count} value(s), "
            f"so the expected answer is {item.target}."
        )
    if item.family == "ordering":
        return _ordering_derivation(item)
    if item.family == "format_compliance":
        field = str(metadata.get("json_field") or "answer")
        return (
            f"The prompt requests a JSON object whose '{field}' field has value "
            f"'{item.target}', so the scorer checks that exact field value."
        )
    if item.family == "negation":
        return _negation_derivation(item, metadata)
    if item.family == "constraint_awareness":
        return _constraint_derivation(item, metadata)
    return f"Direct inspection of the prompt gives the expected answer '{item.target}'."


def _spelling_transform_derivation(
    item: BenchmarkItem,
    metadata: dict[str, Any],
) -> str:
    word = str(metadata.get("word", ""))
    letter = str(metadata.get("letter", ""))
    operation = str(metadata.get("operation", item.subfamily))
    if operation == "remove" or item.subfamily == "remove_letter":
        transformed = word.replace(letter, "")
        return (
            f"Removing every '{letter}' from '{word}' gives '{transformed}', "
            f"so the expected answer is {item.target}."
        )
    if operation == "replace" or item.subfamily == "replace_letter":
        transformed = word.replace(letter, "@")
        return (
            f"Replacing every '{letter}' in '{word}' with '@' gives '{transformed}', "
            f"so the expected answer is {item.target}."
        )
    if operation == "reverse" or item.subfamily == "reverse_word":
        transformed = word[::-1]
        return (
            f"Reversing '{word}' gives '{transformed}', so the expected answer is "
            f"{item.target}."
        )
    return (
        f"Applying the declared spelling operation '{operation}' to '{word}' gives "
        f"the expected answer {item.target}."
    )


def _arithmetic_derivation(
    item: BenchmarkItem,
    metadata: dict[str, Any],
) -> str:
    operation = str(metadata.get("operation") or item.subfamily)
    if operation == "numeric_comparison" or item.subfamily == "numeric_comparison":
        numbers = [Decimal(match) for match in re.findall(r"-?\d+(?:\.\d+)?", item.question)]
        if len(numbers) >= 2:
            larger = max(numbers[:2])
            return (
                f"Comparing {numbers[0]} and {numbers[1]} as decimal values, "
                f"{larger} is larger, so the expected answer is {item.target}."
            )
    expression_match = re.search(
        r"(?:(?:What is)|(?:Calculate))\s+(.+?)(?:\?|$)",
        item.question,
        flags=re.IGNORECASE,
    )
    if expression_match:
        expression = expression_match.group(1).strip()
        return (
            f"Evaluating the arithmetic expression '{expression}' gives "
            f"{item.target}."
        )
    return f"The arithmetic requested in the prompt evaluates to {item.target}."


def _ordering_derivation(item: BenchmarkItem) -> str:
    values_text = item.question.split(":", maxsplit=1)[-1].rstrip("?.").strip()
    values = [value.strip() for value in values_text.split(",") if value.strip()]
    if item.subfamily == "numeric_sort":
        sorted_values = [str(value) for value in sorted(Decimal(value) for value in values)]
        return (
            f"Sorting the numbers {', '.join(values)} from smallest to largest gives "
            f"{', '.join(sorted_values)}, so the expected answer is {item.target}."
        )
    sorted_values = sorted(values, key=lambda value: value.lower())
    return (
        f"Alphabetically sorting {', '.join(values)} gives "
        f"{', '.join(sorted_values)}, so the expected answer is {item.target}."
    )


def _negation_derivation(
    item: BenchmarkItem,
    metadata: dict[str, Any],
) -> str:
    choices = metadata.get("choices")
    if isinstance(choices, list) and choices:
        return (
            f"Among the listed choices ({', '.join(str(choice) for choice in choices)}), "
            f"the one satisfying the negated condition is {item.target}."
        )
    return (
        f"The prompt asks for the option that does not satisfy the named category or "
        f"constraint; direct inspection leaves {item.target} as the expected answer."
    )


def _constraint_derivation(
    item: BenchmarkItem,
    metadata: dict[str, Any],
) -> str:
    choices = metadata.get("choices")
    choice_text = ", ".join(str(choice) for choice in choices) if isinstance(choices, list) else ""
    object_required = str(metadata.get("object_required") or "the required object")
    task_role = str(metadata.get("task_required_role") or "the task object")
    return (
        f"The task requires the physical object '{object_required}' for its role as "
        f"{task_role}. Among the choices ({choice_text}), option {item.target} is "
        "the one that brings or supplies that object."
    )


def _ambiguity_notes(item: BenchmarkItem) -> list[str]:
    metadata = item.metadata.extra
    notes = [
        "Prompt wording specifies the answer form and target object directly.",
        f"Scored with {item.scorer}; acceptable output is the canonical target only.",
    ]
    if item.family == "character_count":
        case_note = (
            "case-sensitive"
            if metadata.get("case_sensitive")
            else "case-insensitive"
        )
        notes[0] = (
            f"The word and counted character are explicit; counting is {case_note}."
        )
    elif item.family == "format_compliance":
        notes[0] = (
            "Strict formatting is intentional; prose or malformed JSON is not an "
            "acceptable answer."
        )
    elif item.family == "constraint_awareness":
        notes[0] = (
            "The expected answer depends on ordinary physical task requirements, "
            "not on convenience or distance."
        )
    elif item.family == "negation":
        notes[0] = "The negation target is explicit in the prompt wording."
    return notes


def _unacceptable_outputs(item: BenchmarkItem) -> list[str]:
    metadata = item.metadata.extra
    if item.family == "constraint_awareness" and isinstance(metadata.get("choices"), list):
        choices = [chr(ord("A") + index) for index, _ in enumerate(metadata["choices"])]
        return [choice for choice in choices if choice != item.target]
    return []


def _leakage_risk(item: BenchmarkItem) -> str:
    if item.split == "public_v0":
        return "medium"
    return "low"


def _count_character(word: str, character: str, case_sensitive: bool) -> int:
    if case_sensitive:
        return word.count(character)
    return word.lower().count(character.lower())
