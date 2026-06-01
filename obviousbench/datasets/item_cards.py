"""Item-card provenance and review metadata for benchmark rows."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Literal

import yaml
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    StrictStr,
    ValidationError,
    field_validator,
)

from obviousbench.datasets.schemas import SPLIT_SHORT_NAMES, AnswerType, ScorerName


@dataclass(frozen=True)
class ItemCardLocation:
    path: Path
    yaml_index: int


class ItemCardLoadError(ValueError):
    """Raised when item-card YAML cannot be loaded into a unique card index."""

    def __init__(
        self,
        message: str,
        *,
        path: Path,
        yaml_index: int | None = None,
        item_id: str | None = None,
        cause: Exception | None = None,
    ) -> None:
        super().__init__(message)
        self.path = path
        self.yaml_index = yaml_index
        self.item_id = item_id
        self.__cause__ = cause


class ScorerContract(BaseModel):
    model_config = ConfigDict(extra="forbid")

    scorer: ScorerName
    answer_type: AnswerType
    strict_format: bool = False
    acceptable_outputs: list[StrictStr] = Field(default_factory=list)
    unacceptable_outputs: list[StrictStr] = Field(default_factory=list)


class SplitPolicy(BaseModel):
    model_config = ConfigDict(extra="forbid")

    allowed_splits: list[StrictStr]
    leakage_risk: Literal["low", "medium", "high"]
    publishable: bool
    rationale: StrictStr

    @field_validator("allowed_splits")
    @classmethod
    def non_empty_allowed_splits(cls, value: list[str]) -> list[str]:
        value = _non_empty_list(value)
        unknown = sorted(set(value) - set(SPLIT_SHORT_NAMES))
        if unknown:
            raise ValueError(f"unknown split names: {', '.join(unknown)}")
        return value

    @field_validator("rationale")
    @classmethod
    def non_blank_rationale(cls, value: str) -> str:
        return _non_blank(value)


class ReviewBlock(BaseModel):
    model_config = ConfigDict(extra="forbid")

    status: Literal["draft", "reviewed", "retired"]
    reviewer: StrictStr
    reviewed_on: StrictStr
    notes: StrictStr = ""

    @field_validator("reviewer", "reviewed_on")
    @classmethod
    def non_blank_required_review_text(cls, value: str) -> str:
        return _non_blank(value)


class ItemCard(BaseModel):
    model_config = ConfigDict(extra="forbid")

    item_id: StrictStr
    archetype_id: StrictStr
    source_refs: list[StrictStr]
    source_type: StrictStr
    source_summary: StrictStr
    answer_derivation: StrictStr
    expected_answer: StrictStr
    scorer_contract: ScorerContract
    ambiguity_notes: list[StrictStr]
    split_policy: SplitPolicy
    review: ReviewBlock

    @field_validator("source_refs", "ambiguity_notes")
    @classmethod
    def non_empty_text_list(cls, value: list[str]) -> list[str]:
        return _non_empty_list(value)

    @field_validator(
        "item_id",
        "archetype_id",
        "source_type",
        "source_summary",
        "answer_derivation",
        "expected_answer",
    )
    @classmethod
    def non_blank_text(cls, value: str) -> str:
        return _non_blank(value)


@dataclass(frozen=True)
class LoadedItemCards:
    by_item_id: dict[str, ItemCard]
    locations_by_item_id: dict[str, ItemCardLocation]


def load_item_cards(cards_dir: Path | str) -> LoadedItemCards:
    """Load all item-card YAML files below a directory and index by item ID."""
    root = Path(cards_dir)
    if not root.exists():
        raise ItemCardLoadError("Item-card directory does not exist", path=root)
    if not root.is_dir():
        raise ItemCardLoadError("Item-card path is not a directory", path=root)

    by_item_id: dict[str, ItemCard] = {}
    locations_by_item_id: dict[str, ItemCardLocation] = {}

    for path in sorted(root.rglob("*.yaml")):
        try:
            payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        except yaml.YAMLError as exc:
            raise ItemCardLoadError(
                f"Invalid item-card YAML: {exc}", path=path, cause=exc
            ) from exc
        if not isinstance(payload, dict):
            raise ItemCardLoadError("Item-card YAML root must be a mapping", path=path)

        raw_cards = payload.get("cards", [])
        if not isinstance(raw_cards, list):
            raise ItemCardLoadError("Item-card YAML 'cards' must be a list", path=path)

        for yaml_index, raw_card in enumerate(raw_cards):
            try:
                card = ItemCard.model_validate(raw_card)
            except ValidationError as exc:
                raise ItemCardLoadError(
                    f"Invalid item card at cards[{yaml_index}]: {exc.errors()[0]['msg']}",
                    path=path,
                    yaml_index=yaml_index,
                    cause=exc,
                ) from exc

            if card.item_id in by_item_id:
                first_location = locations_by_item_id[card.item_id]
                raise ItemCardLoadError(
                    (
                        f"Duplicate item card for {card.item_id}; first seen in "
                        f"{first_location.path}:cards[{first_location.yaml_index}]"
                    ),
                    path=path,
                    yaml_index=yaml_index,
                    item_id=card.item_id,
                )
            by_item_id[card.item_id] = card
            locations_by_item_id[card.item_id] = ItemCardLocation(path, yaml_index)

    return LoadedItemCards(by_item_id=by_item_id, locations_by_item_id=locations_by_item_id)


def _non_blank(value: str) -> str:
    if not value.strip():
        raise ValueError("value cannot be blank")
    return value


def _non_empty_list(value: list[str]) -> list[str]:
    if not value or any(not item.strip() for item in value):
        raise ValueError("list must contain at least one non-blank value")
    return value
