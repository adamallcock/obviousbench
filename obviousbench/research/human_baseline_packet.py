"""Build human-baseline assignment packets for the ObviousBench paper split."""

from __future__ import annotations

import csv
import json
import random
from collections import Counter
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path

from obviousbench.datasets.schemas import BenchmarkItem

ASSIGNMENT_COLUMNS = (
    "participant_id",
    "sequence",
    "item_id",
    "family",
    "subfamily",
    "answer_type",
    "scorer",
    "prompt",
)
RESPONSE_COLUMNS = ("item_id", "participant_id", "answer", "seconds", "correct", "notes")
ANSWER_KEY_COLUMNS = (
    "item_id",
    "family",
    "subfamily",
    "target",
    "answer_type",
    "scorer",
)


@dataclass(frozen=True)
class HumanBaselinePacketInputs:
    manifest_path: Path
    dataset_paths: Sequence[Path]
    summary_path: Path
    participant_packets_path: Path
    assignment_csv_path: Path
    response_template_path: Path
    answer_key_path: Path
    participant_count: int = 5
    seed: int = 20260601
    generated_on: str = "2026-06-01"


@dataclass(frozen=True)
class HumanBaselinePacketResult:
    summary_path: Path
    participant_packets_path: Path
    assignment_csv_path: Path
    response_template_path: Path
    answer_key_path: Path
    participant_count: int
    item_count: int
    assignment_count: int
    response_row_count: int

    @property
    def expected_response_rows(self) -> int:
        return self.participant_count * self.item_count

    @property
    def ok(self) -> bool:
        return (
            self.item_count > 0
            and self.participant_count > 0
            and self.assignment_count == self.expected_response_rows
            and self.response_row_count == self.expected_response_rows
        )


def build_human_baseline_packet(
    inputs: HumanBaselinePacketInputs,
) -> HumanBaselinePacketResult:
    """Generate participant-facing and scoring assets without collecting data."""
    if inputs.participant_count <= 0:
        raise ValueError("participant_count must be positive")
    manifest_ids = _load_manifest_item_ids(inputs.manifest_path)
    item_by_id = _load_dataset_items(inputs.dataset_paths, manifest_ids)
    items = [item_by_id[item_id] for item_id in manifest_ids if item_id in item_by_id]
    participant_ids = tuple(f"p{index:02d}" for index in range(1, inputs.participant_count + 1))
    assignments = _assign_items(items, participant_ids, seed=inputs.seed)

    for path in (
        inputs.summary_path,
        inputs.participant_packets_path,
        inputs.assignment_csv_path,
        inputs.response_template_path,
        inputs.answer_key_path,
    ):
        path.parent.mkdir(parents=True, exist_ok=True)

    _write_assignments(inputs.assignment_csv_path, assignments)
    _write_response_template(inputs.response_template_path, assignments)
    _write_answer_key(inputs.answer_key_path, items)
    inputs.participant_packets_path.write_text(
        _render_participant_packets(assignments, inputs),
        encoding="utf-8",
    )
    result = HumanBaselinePacketResult(
        summary_path=inputs.summary_path,
        participant_packets_path=inputs.participant_packets_path,
        assignment_csv_path=inputs.assignment_csv_path,
        response_template_path=inputs.response_template_path,
        answer_key_path=inputs.answer_key_path,
        participant_count=len(participant_ids),
        item_count=len(items),
        assignment_count=len(assignments),
        response_row_count=len(assignments),
    )
    inputs.summary_path.write_text(
        _render_summary(result, inputs, items, assignments),
        encoding="utf-8",
    )
    return result


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


def _assign_items(
    items: Sequence[BenchmarkItem],
    participant_ids: Sequence[str],
    *,
    seed: int,
) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for participant_index, participant_id in enumerate(participant_ids, start=1):
        ordered = list(items)
        rng = random.Random(seed + participant_index)
        rng.shuffle(ordered)
        for sequence, item in enumerate(ordered, start=1):
            rows.append(
                {
                    "participant_id": participant_id,
                    "sequence": str(sequence),
                    "item_id": item.id,
                    "family": str(item.family),
                    "subfamily": item.subfamily,
                    "answer_type": str(item.answer_type),
                    "scorer": str(item.scorer),
                    "prompt": item.prompt,
                }
            )
    return rows


def _write_assignments(path: Path, rows: Sequence[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=ASSIGNMENT_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)


def _write_response_template(path: Path, rows: Sequence[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=RESPONSE_COLUMNS)
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {
                    "item_id": row["item_id"],
                    "participant_id": row["participant_id"],
                    "answer": "",
                    "seconds": "",
                    "correct": "",
                    "notes": "",
                }
            )


def _write_answer_key(path: Path, items: Sequence[BenchmarkItem]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=ANSWER_KEY_COLUMNS)
        writer.writeheader()
        for item in items:
            writer.writerow(
                {
                    "item_id": item.id,
                    "family": item.family,
                    "subfamily": item.subfamily,
                    "target": item.target,
                    "answer_type": item.answer_type,
                    "scorer": item.scorer,
                }
            )


def _render_participant_packets(
    assignments: Sequence[dict[str, str]],
    inputs: HumanBaselinePacketInputs,
) -> str:
    lines = [
        "---",
        "title: Paper V1 Human Baseline Participant Packets",
        f"date: {inputs.generated_on}",
        "type: research",
        "status: draft",
        "---",
        "",
        "# Paper V1 Human Baseline Participant Packets",
        "",
        "Participant-facing prompts only. This file intentionally excludes target",
        "answers and item-card derivations.",
        "",
        "Instructions for participants:",
        "",
        "- Answer without search, calculators, external tools, or model assistance.",
        "- Answer as quickly and accurately as you can.",
        "- Record elapsed seconds per item.",
        "- Skip unclear items only when needed; skipped items are scored incorrect.",
        "",
    ]
    by_participant: dict[str, list[dict[str, str]]] = {}
    for row in assignments:
        by_participant.setdefault(row["participant_id"], []).append(row)
    for participant_id, rows in sorted(by_participant.items()):
        lines.extend([f"## Participant {participant_id}", ""])
        for row in sorted(rows, key=lambda item: int(item["sequence"])):
            lines.extend(
                [
                    f"### {participant_id}-{int(row['sequence']):03d}",
                    "",
                    f"- Item ID: `{row['item_id']}`",
                    f"- Family: `{row['family']}`",
                    f"- Answer type: `{row['answer_type']}`",
                    "",
                    "```text",
                    row["prompt"],
                    "```",
                    "",
                ]
            )
    return "\n".join(lines)


def _render_summary(
    result: HumanBaselinePacketResult,
    inputs: HumanBaselinePacketInputs,
    items: Sequence[BenchmarkItem],
    assignments: Sequence[dict[str, str]],
) -> str:
    family_counts = Counter(str(item.family) for item in items)
    assignment_counts = Counter(row["item_id"] for row in assignments)
    min_assignments = min(assignment_counts.values(), default=0)
    max_assignments = max(assignment_counts.values(), default=0)
    lines = [
        "---",
        "title: Paper V1 Human Baseline Collection Packet",
        f"date: {inputs.generated_on}",
        "type: research",
        f"status: {'ready' if result.ok else 'blocked'}",
        "---",
        "",
        "# Paper V1 Human Baseline Collection Packet",
        "",
        "This packet prepares human-baseline collection for the paper split. It",
        "does not contain real participant responses and does not make model",
        "provider calls.",
        "",
        f"Overall status: {'PASS' if result.ok else 'BLOCKED'}",
        "",
        f"- Participants: {result.participant_count}",
        f"- Paper items: {result.item_count}",
        f"- Assignment rows: {result.assignment_count}",
        f"- Preallocated response rows: {result.response_row_count}",
        f"- Assignments per item: {min_assignments} to {max_assignments}",
        f"- Randomization seed: {inputs.seed}",
        "",
        "## Generated Files",
        "",
        f"- Assignment CSV: `{inputs.assignment_csv_path}`",
        f"- Response template CSV: `{inputs.response_template_path}`",
        f"- Local answer key CSV: `{inputs.answer_key_path}`",
        f"- Participant packets: `{inputs.participant_packets_path}`",
        "",
        "The assignment CSV and participant packets are participant-facing and do",
        "not include targets. The answer key is local scoring material and should",
        "not be shown to participants.",
        "",
        "## Family Coverage",
        "",
        "| Family | Items | Assignment rows |",
        "| --- | ---: | ---: |",
    ]
    for family, count in sorted(family_counts.items()):
        lines.append(
            f"| `{family}` | {count} | {count * result.participant_count} |"
        )
    lines.extend(
        [
            "",
            "## Collection Procedure",
            "",
            "1. Give each participant only their section from the participant packet.",
            "2. Record answer text and elapsed seconds for every assigned item.",
            "3. Copy completed rows into `data/human_baseline/paper_v1.csv`.",
            "4. Score `correct` with the target/scorer contract and item cards.",
            "5. Run `make -C paper readiness` before any final model sweep.",
            "",
            "## Privacy Boundary",
            "",
            "Use pseudonymous participant IDs only. Do not store participant names,",
            "emails, demographics, payment details, or other personal data in the",
            "paper baseline files.",
            "",
        ]
    )
    return "\n".join(lines)
