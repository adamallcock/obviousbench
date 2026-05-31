"""Validation for benchmark JSONL datasets."""

from __future__ import annotations

import json
from collections.abc import Sequence
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from pydantic import ValidationError

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


def validate_dataset_paths(paths: Sequence[Path | str]) -> ValidationReport:
    """Validate benchmark JSONL files and return structured issues."""
    report = ValidationReport()
    seen_ids: dict[str, tuple[Path, int]] = {}

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

    return report
