"""Validation for benchmark JSONL datasets."""

from __future__ import annotations

import json
from collections.abc import Sequence
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from pydantic import ValidationError

from obviousbench.datasets.item_cards import ItemCard, ItemCardLoadError, load_item_cards
from obviousbench.datasets.schemas import (
    BenchmarkItem,
    HumanTriviality,
    ReviewStatus,
    parse_item_id,
)


@dataclass(frozen=True)
class ValidationIssue:
    path: Path
    line: int | None
    field: str | None
    code: str
    message: str

    def format(self) -> str:
        location = str(self.path)
        if self.line is not None:
            location = f"{location}:{self.line}"
        field = f" field={self.field}" if self.field else ""
        return f"{location}{field} {self.code}: {self.message}"


@dataclass
class ValidationReport:
    issues: list[ValidationIssue] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.issues

    def add(self, issue: ValidationIssue) -> None:
        self.issues.append(issue)


def _field_path(error: dict[str, Any]) -> str | None:
    loc = error.get("loc")
    if not loc:
        return None
    return ".".join(str(part) for part in loc)


def validate_dataset_paths(
    paths: Sequence[Path | str],
    *,
    item_cards_dir: Path | str | None = None,
    require_item_cards: bool = False,
    allow_extra_item_cards: bool = False,
) -> ValidationReport:
    """Validate benchmark JSONL files and return structured issues."""
    report = ValidationReport()
    seen_ids: dict[str, tuple[Path, int]] = {}
    seen_dataset_item_ids: set[str] = set()

    loaded_cards = None
    if require_item_cards and item_cards_dir is None:
        report.add(
            ValidationIssue(
                path=Path("<item-cards-dir>"),
                line=None,
                field="item_cards_dir",
                code="missing_item_cards_dir",
                message="--require-item-cards requires --item-cards-dir",
            )
        )
        return report

    if item_cards_dir is not None:
        try:
            loaded_cards = load_item_cards(item_cards_dir)
        except ItemCardLoadError as exc:
            field = "cards"
            if exc.yaml_index is not None:
                field = f"cards[{exc.yaml_index}]"
            report.add(
                ValidationIssue(
                    path=exc.path,
                    line=None,
                    field=field,
                    code=(
                        "duplicate_item_card"
                        if "Duplicate item card" in str(exc)
                        else "invalid_item_card"
                    ),
                    message=str(exc),
                )
            )
            return report

    for raw_path in paths:
        path = Path(raw_path)
        if not path.exists():
            report.add(ValidationIssue(path, None, None, "missing_file", "File does not exist"))
            continue

        for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            if not line.strip():
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError as exc:
                report.add(
                    ValidationIssue(path, line_number, None, "invalid_json", exc.msg)
                )
                continue

            try:
                item = BenchmarkItem.model_validate(record)
            except ValidationError as exc:
                for error in exc.errors():
                    report.add(
                        ValidationIssue(
                            path=path,
                            line=line_number,
                            field=_field_path(error),
                            code="validation_error",
                            message=str(error.get("msg", "Invalid value")),
                        )
                    )
                continue

            try:
                parse_item_id(item.id)
            except ValueError as exc:
                report.add(
                    ValidationIssue(path, line_number, "id", "invalid_id", str(exc))
                )

            if item.id in seen_ids:
                first_path, first_line = seen_ids[item.id]
                report.add(
                    ValidationIssue(
                        path=path,
                        line=line_number,
                        field="id",
                        code="duplicate_id",
                        message=(
                            f"{item.id} appears at {first_path.name}:{first_line} "
                            f"and {path.name}:{line_number}"
                        ),
                    )
                )
            else:
                seen_ids[item.id] = (path, line_number)
            seen_dataset_item_ids.add(item.id)

            if item.split == "public_v0" and not item.source_refs:
                report.add(
                    ValidationIssue(
                        path,
                        line_number,
                        "source_refs",
                        "missing_source_refs",
                        "Public items must reference at least one source",
                    )
                )
            if item.split == "public_v0" and item.review_status != ReviewStatus.REVIEWED:
                report.add(
                    ValidationIssue(
                        path,
                        line_number,
                        "review_status",
                        "unreviewed_public_item",
                        "Public items must be reviewed",
                    )
                )
            if item.human_triviality == HumanTriviality.H3:
                report.add(
                    ValidationIssue(
                        path,
                        line_number,
                        "human_triviality",
                        "excluded_human_triviality",
                        "H3 items are excluded from benchmark splits",
                    )
                )
            _validate_metamorphic_metadata(report, path, line_number, item)
            if loaded_cards is not None:
                _validate_item_card_for_item(
                    report=report,
                    path=path,
                    line_number=line_number,
                    item=item,
                    card=loaded_cards.by_item_id.get(item.id),
                    require_item_cards=require_item_cards,
                )

    if loaded_cards is not None and not allow_extra_item_cards:
        for item_id, location in loaded_cards.locations_by_item_id.items():
            if item_id not in seen_dataset_item_ids:
                report.add(
                    ValidationIssue(
                        path=location.path,
                        line=None,
                        field=f"cards[{location.yaml_index}].item_id",
                        code="extra_item_card",
                        message=f"Item card {item_id} does not match a validated dataset item",
                    )
                )

    return report


def _validate_metamorphic_metadata(
    report: ValidationReport,
    path: Path,
    line_number: int,
    item: BenchmarkItem,
) -> None:
    required_fields = (
        "metamorphic_group_id",
        "metamorphic_role",
        "metamorphic_relation",
        "metamorphic_expected_behavior",
    )
    present = [
        field_name
        for field_name in required_fields
        if getattr(item.metadata, field_name) is not None
    ]
    if present and len(present) != len(required_fields):
        missing = sorted(set(required_fields) - set(present))
        report.add(
            ValidationIssue(
                path=path,
                line=line_number,
                field="metadata",
                code="incomplete_metamorphic_metadata",
                message=(
                    "Metamorphic metadata must include all required fields; "
                    f"missing: {', '.join(missing)}"
                ),
            )
        )


def _validate_item_card_for_item(
    *,
    report: ValidationReport,
    path: Path,
    line_number: int,
    item: BenchmarkItem,
    card: ItemCard | None,
    require_item_cards: bool,
) -> None:
    if card is None:
        if require_item_cards:
            report.add(
                ValidationIssue(
                    path=path,
                    line=line_number,
                    field="id",
                    code="missing_item_card",
                    message=f"{item.id} has no item card",
                )
            )
        return

    if require_item_cards and card.review.status == ReviewStatus.DRAFT:
        report.add(
            ValidationIssue(
                path=path,
                line=line_number,
                field="review.status",
                code="draft_item_card",
                message=f"{item.id} has only a draft item card",
            )
        )
    if card.expected_answer != item.target:
        report.add(
            ValidationIssue(
                path=path,
                line=line_number,
                field="target",
                code="item_card_target_mismatch",
                message=(
                    f"{item.id} target is {item.target!r} but item card expects "
                    f"{card.expected_answer!r}"
                ),
            )
        )
    if card.scorer_contract.scorer != item.scorer:
        report.add(
            ValidationIssue(
                path=path,
                line=line_number,
                field="scorer",
                code="item_card_scorer_mismatch",
                message=(
                    f"{item.id} scorer is {item.scorer!r} but item card declares "
                    f"{card.scorer_contract.scorer!r}"
                ),
            )
        )
    if card.scorer_contract.answer_type != item.answer_type:
        report.add(
            ValidationIssue(
                path=path,
                line=line_number,
                field="answer_type",
                code="item_card_answer_type_mismatch",
                message=(
                    f"{item.id} answer_type is {item.answer_type!r} but item card declares "
                    f"{card.scorer_contract.answer_type!r}"
                ),
            )
        )
    if item.split not in card.split_policy.allowed_splits:
        report.add(
            ValidationIssue(
                path=path,
                line=line_number,
                field="split",
                code="item_card_split_mismatch",
                message=(
                    f"{item.id} split {item.split!r} is not allowed by item card "
                    f"{card.split_policy.allowed_splits!r}"
                ),
            )
        )
