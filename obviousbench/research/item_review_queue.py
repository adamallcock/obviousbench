"""Build a Markdown review queue for paper-candidate item cards."""

from __future__ import annotations

import json
from collections import defaultdict
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path

from obviousbench.datasets.item_cards import ItemCard, load_item_cards
from obviousbench.datasets.schemas import BenchmarkItem
from obviousbench.research.arxiv_readiness import PLACEHOLDER_MARKERS


@dataclass(frozen=True)
class ItemReviewQueueInputs:
    manifest_path: Path
    dataset_paths: Sequence[Path]
    item_cards_dir: Path
    output_path: Path


@dataclass(frozen=True)
class ItemReviewQueueResult:
    output_path: Path
    item_count: int
    blocked_count: int


@dataclass(frozen=True)
class ReviewQueueRow:
    item_id: str
    family: str
    subfamily: str
    scorer: str
    target: str
    source_refs: str
    review_status: str
    blockers: tuple[str, ...]


def build_item_review_queue(inputs: ItemReviewQueueInputs) -> ItemReviewQueueResult:
    manifest_rows = _load_manifest_rows(inputs.manifest_path)
    item_ids = [str(row["item_id"]) for row in manifest_rows]
    dataset_items = _load_dataset_items(inputs.dataset_paths, set(item_ids))
    loaded_cards = load_item_cards(inputs.item_cards_dir)

    rows = []
    for manifest_row in manifest_rows:
        item_id = str(manifest_row["item_id"])
        item = dataset_items.get(item_id)
        card = loaded_cards.by_item_id.get(item_id)
        rows.append(_build_row(manifest_row, item, card))

    markdown = _render_markdown(rows)
    inputs.output_path.parent.mkdir(parents=True, exist_ok=True)
    inputs.output_path.write_text(markdown, encoding="utf-8")
    return ItemReviewQueueResult(
        output_path=inputs.output_path,
        item_count=len(rows),
        blocked_count=sum(1 for row in rows if row.blockers),
    )


def _load_manifest_rows(path: Path) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def _load_dataset_items(
    paths: Sequence[Path],
    include_item_ids: set[str],
) -> dict[str, BenchmarkItem]:
    items: dict[str, BenchmarkItem] = {}
    for path in paths:
        if not path.exists():
            continue
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            raw = json.loads(line)
            if raw.get("id") not in include_item_ids:
                continue
            item = BenchmarkItem.model_validate(raw)
            items[item.id] = item
    return items


def _build_row(
    manifest_row: dict[str, object],
    item: BenchmarkItem | None,
    card: ItemCard | None,
) -> ReviewQueueRow:
    item_id = str(manifest_row["item_id"])
    blockers = []
    if item is None:
        blockers.append("missing_dataset_item")
    if card is None:
        blockers.append("missing_item_card")
    elif card.review.status != "reviewed":
        blockers.append("draft_card")
    if card is not None and _card_contains_placeholder(card):
        blockers.append("placeholder_text")

    family = str(manifest_row.get("family") or (item.family if item else "unknown"))
    subfamily = str(
        manifest_row.get("subfamily") or (item.subfamily if item else "unknown")
    )
    scorer = str(manifest_row.get("scorer") or (item.scorer if item else "unknown"))
    return ReviewQueueRow(
        item_id=item_id,
        family=family,
        subfamily=subfamily,
        scorer=scorer,
        target=item.target if item else "",
        source_refs=", ".join(item.source_refs) if item else "",
        review_status=card.review.status if card else "missing",
        blockers=tuple(blockers),
    )


def _render_markdown(rows: Sequence[ReviewQueueRow]) -> str:
    grouped: dict[str, list[ReviewQueueRow]] = defaultdict(list)
    for row in rows:
        grouped[row.family].append(row)

    lines = [
        "---",
        "title: Paper V1 Item Review Queue",
        "date: 2026-06-01",
        "type: review",
        "status: draft",
        "---",
        "",
        "# Paper V1 Item Review Queue",
        "",
        f"Total items: {len(rows)}",
        "",
        f"Blocked items: {sum(1 for row in rows if row.blockers)}",
        "",
    ]
    for family in sorted(grouped):
        lines.extend(
            [
                f"## {family}",
                "",
                "| Item ID | Subfamily | Scorer | Target | Source refs | Status | Blockers |",
                "| --- | --- | --- | --- | --- | --- | --- |",
            ]
        )
        for row in sorted(grouped[family], key=lambda value: value.item_id):
            blockers = ", ".join(row.blockers) if row.blockers else "none"
            lines.append(
                "| "
                + " | ".join(
                    _markdown_cell(value)
                    for value in (
                        row.item_id,
                        row.subfamily,
                        row.scorer,
                        row.target,
                        row.source_refs,
                        row.review_status,
                        blockers,
                    )
                )
                + " |"
            )
        lines.append("")
    return "\n".join(lines)


def _card_contains_placeholder(card: ItemCard) -> bool:
    text_parts = [
        card.source_summary,
        card.answer_derivation,
        card.split_policy.rationale,
        card.review.reviewer,
        card.review.notes,
        *card.ambiguity_notes,
    ]
    text = "\n".join(text_parts)
    return any(marker in text for marker in PLACEHOLDER_MARKERS)


def _markdown_cell(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")
