"""Generate human-baseline collection assets for the paper candidate split."""

from __future__ import annotations

import csv
import json
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path

from obviousbench.datasets.schemas import BenchmarkItem

CSV_COLUMNS = ("item_id", "participant_id", "answer", "seconds", "correct", "notes")


@dataclass(frozen=True)
class HumanBaselineFormInputs:
    manifest_path: Path
    dataset_paths: Sequence[Path]
    form_path: Path
    csv_path: Path


@dataclass(frozen=True)
class HumanBaselineFormResult:
    form_path: Path
    csv_path: Path
    item_count: int


def build_human_baseline_form(
    inputs: HumanBaselineFormInputs,
) -> HumanBaselineFormResult:
    manifest_ids = _load_manifest_item_ids(inputs.manifest_path)
    dataset_items = _load_dataset_items(inputs.dataset_paths, manifest_ids)
    ordered_items = [dataset_items[item_id] for item_id in manifest_ids if item_id in dataset_items]

    inputs.form_path.parent.mkdir(parents=True, exist_ok=True)
    inputs.form_path.write_text(_render_form(ordered_items), encoding="utf-8")

    inputs.csv_path.parent.mkdir(parents=True, exist_ok=True)
    with inputs.csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_COLUMNS)
        writer.writeheader()

    return HumanBaselineFormResult(
        form_path=inputs.form_path,
        csv_path=inputs.csv_path,
        item_count=len(ordered_items),
    )


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


def _render_form(items: Sequence[BenchmarkItem]) -> str:
    lines = [
        "---",
        "title: Paper V1 Human Baseline Form",
        "date: 2026-06-01",
        "type: research",
        "status: draft",
        "---",
        "",
        "# Paper V1 Human Baseline Form",
        "",
        "Use this form to collect timed human answers for the paper candidate split.",
        "Do not show expected-answer fields or item-card derivations to participants.",
        "",
        "Record one CSV row per participant response with these columns:",
        "",
        "`item_id,participant_id,answer,seconds,correct,notes`",
        "",
        f"Total items: {len(items)}",
        "",
    ]
    for index, item in enumerate(items, start=1):
        lines.extend(
            [
                f"## Item {index}: {item.id}",
                "",
                f"- Family: `{item.family}`",
                f"- Subfamily: `{item.subfamily}`",
                f"- Answer type: `{item.answer_type}`",
                f"- Scorer: `{item.scorer}`",
                "",
                "Prompt shown to participant:",
                "",
                "```text",
                item.prompt,
                "```",
                "",
            ]
        )
    return "\n".join(lines)
