"""arXiv paper-readiness audit for ObviousBench benchmark artifacts."""

from __future__ import annotations

import csv
import json
from collections import Counter
from collections.abc import Sequence
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal

from pydantic import ValidationError

from obviousbench.datasets.item_cards import ItemCard, ItemCardLoadError, load_item_cards
from obviousbench.datasets.schemas import BenchmarkItem
from obviousbench.datasets.validation import validate_dataset_paths
from obviousbench.scorers.gold import load_gold_examples

GateStatus = Literal["pass", "fail"]
ReadinessProfile = Literal["strict", "preprint"]

PLACEHOLDER_MARKERS = (
    "TODO(",
    "TODO:",
    "TODO ",
    "todo(",
    "todo:",
    "todo ",
    "Draft target:",
    "Generated card stub requiring human review",
)


@dataclass(frozen=True)
class ArxivReadinessInputs:
    dataset_paths: Sequence[Path]
    item_cards_dir: Path
    scorer_gold_dir: Path
    human_baseline_path: Path | None
    paper_manifest_path: Path | None
    min_gold_examples_per_scorer: int = 20
    min_human_participants: int = 5
    manifest_scope: bool = False
    readiness_profile: ReadinessProfile = "strict"


@dataclass(frozen=True)
class ReadinessGate:
    name: str
    status: GateStatus
    message: str
    details: tuple[str, ...] = ()


@dataclass(frozen=True)
class ArxivReadinessReport:
    gates: tuple[ReadinessGate, ...] = field(default_factory=tuple)

    @property
    def ok(self) -> bool:
        return all(gate.status == "pass" for gate in self.gates)

    def gate_by_name(self, name: str) -> ReadinessGate:
        for gate in self.gates:
            if gate.name == name:
                return gate
        raise KeyError(name)

    def to_markdown(self) -> str:
        lines = ["# ObviousBench arXiv Readiness Audit", ""]
        lines.append(f"Overall status: {'PASS' if self.ok else 'FAIL'}")
        for gate in self.gates:
            marker = "PASS" if gate.status == "pass" else "FAIL"
            lines.extend(["", f"## {gate.name}", "", f"{marker}: {gate.message}"])
            if gate.details:
                lines.append("")
                lines.extend(f"- {detail}" for detail in gate.details)
        lines.append("")
        return "\n".join(lines)


def audit_arxiv_readiness(inputs: ArxivReadinessInputs) -> ArxivReadinessReport:
    """Audit whether local benchmark artifacts are ready to support an arXiv paper."""
    manifest_ids = _load_manifest_item_ids(inputs.paper_manifest_path)
    include_item_ids = manifest_ids if inputs.manifest_scope else None
    dataset_items = _load_dataset_items(
        inputs.dataset_paths,
        include_item_ids=include_item_ids,
    )
    gates = [
        _dataset_validation_gate(inputs, include_item_ids=include_item_ids),
        _item_card_review_gate(inputs.item_cards_dir, include_item_ids=include_item_ids),
        _scorer_gold_gate(
            scorer_gold_dir=inputs.scorer_gold_dir,
            used_scorers=sorted({item.scorer for item in dataset_items}),
            min_examples=inputs.min_gold_examples_per_scorer,
        ),
        _human_baseline_gate(
            inputs.human_baseline_path,
            dataset_items,
            min_participants=inputs.min_human_participants,
            readiness_profile=inputs.readiness_profile,
        ),
        _paper_manifest_gate(inputs.paper_manifest_path, dataset_items),
    ]
    return ArxivReadinessReport(gates=tuple(gates))


def _dataset_validation_gate(
    inputs: ArxivReadinessInputs,
    *,
    include_item_ids: set[str] | None,
) -> ReadinessGate:
    report = validate_dataset_paths(
        inputs.dataset_paths,
        item_cards_dir=inputs.item_cards_dir,
        require_item_cards=True,
        allow_extra_item_cards=True,
        include_item_ids=include_item_ids,
    )
    if report.ok:
        return ReadinessGate(
            "dataset validation",
            "pass",
            f"{len(inputs.dataset_paths)} dataset file(s) passed strict validation.",
        )
    details = tuple(issue.format() for issue in report.issues[:20])
    suffix = "" if len(report.issues) <= 20 else f" ({len(report.issues) - 20} more)"
    return ReadinessGate(
        "dataset validation",
        "fail",
        f"{len(report.issues)} validation issue(s) found{suffix}.",
        details,
    )


def _item_card_review_gate(
    item_cards_dir: Path,
    *,
    include_item_ids: set[str] | None,
) -> ReadinessGate:
    try:
        cards = load_item_cards(item_cards_dir)
    except ItemCardLoadError as exc:
        return ReadinessGate(
            "item-card review",
            "fail",
            "Item cards could not be loaded.",
            (str(exc),),
        )

    scoped_cards = {
        item_id: card
        for item_id, card in cards.by_item_id.items()
        if include_item_ids is None or item_id in include_item_ids
    }
    draft_ids = [
        item_id
        for item_id, card in sorted(scoped_cards.items())
        if card.review.status != "reviewed"
    ]
    placeholder_ids = [
        item_id
        for item_id, card in sorted(scoped_cards.items())
        if _card_contains_placeholder(card)
    ]
    details = []
    if draft_ids:
        details.append(_summarize_ids("draft", draft_ids))
    if placeholder_ids:
        details.append(_summarize_ids("placeholder", placeholder_ids))
    if details:
        parts = []
        if draft_ids:
            parts.append(f"{len(draft_ids)} draft item cards")
        if placeholder_ids:
            parts.append(f"{len(placeholder_ids)} cards with placeholder text")
        return ReadinessGate(
            "item-card review",
            "fail",
            " and ".join(parts) + " block paper-ready claims.",
            tuple(details),
        )
    return ReadinessGate(
        "item-card review",
        "pass",
        f"{len(scoped_cards)} item cards are reviewed and placeholder-free.",
    )


def _scorer_gold_gate(
    *,
    scorer_gold_dir: Path,
    used_scorers: Sequence[str],
    min_examples: int,
) -> ReadinessGate:
    if not scorer_gold_dir.exists():
        return ReadinessGate(
            "scorer-gold coverage",
            "fail",
            f"Scorer-gold directory does not exist: {scorer_gold_dir}",
        )
    try:
        examples = load_gold_examples(sorted(scorer_gold_dir.glob("*.yaml")))
    except ValueError as exc:
        return ReadinessGate(
            "scorer-gold coverage",
            "fail",
            "Scorer-gold fixtures could not be loaded.",
            (str(exc),),
        )
    counts = Counter(example.scorer for example in examples)
    failures = [
        f"{scorer} has {counts.get(scorer, 0)}/{min_examples} examples"
        for scorer in used_scorers
        if counts.get(scorer, 0) < min_examples
    ]
    if failures:
        return ReadinessGate(
            "scorer-gold coverage",
            "fail",
            "One or more scorers used by the paper dataset lack enough gold examples.",
            tuple(failures),
        )
    return ReadinessGate(
        "scorer-gold coverage",
        "pass",
        f"{len(used_scorers)} used scorer(s) meet the {min_examples}-example threshold.",
    )


def _required_file_gate(name: str, path: Path | None) -> ReadinessGate:
    if path is None:
        return ReadinessGate(name, "fail", f"No {name} path was provided.")
    if not path.exists():
        return ReadinessGate(name, "fail", f"Required {name} file is missing: {path}")
    if path.stat().st_size == 0:
        return ReadinessGate(name, "fail", f"Required {name} file is empty: {path}")
    return ReadinessGate(name, "pass", f"Required {name} file exists: {path}")


def _human_baseline_gate(
    path: Path | None,
    dataset_items: Sequence[BenchmarkItem],
    *,
    min_participants: int,
    readiness_profile: ReadinessProfile,
) -> ReadinessGate:
    if readiness_profile == "preprint":
        strict_gate = _human_baseline_gate(
            path,
            dataset_items,
            min_participants=min_participants,
            readiness_profile="strict",
        )
        if strict_gate.status == "pass":
            return ReadinessGate(
                "human baseline",
                "pass",
                (
                    "Human baseline passes and may be reported, but the preprint "
                    "profile does not require it."
                ),
            )
        return ReadinessGate(
            "human baseline",
            "pass",
            (
                "Human baseline is optional under the preprint profile; empirical "
                "human-triviality claims must be omitted or labeled as planned "
                "validation."
            ),
            (strict_gate.message, *strict_gate.details[:10]),
        )

    base_gate = _required_file_gate("human baseline", path)
    if base_gate.status == "fail" or path is None:
        return base_gate

    required_columns = {"item_id", "participant_id", "answer", "seconds", "correct", "notes"}
    dataset_ids = {item.id for item in dataset_items}
    issues: list[str] = []
    participant_ids: set[str] = set()
    covered_item_ids: set[str] = set()
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = set(reader.fieldnames or [])
        missing_columns = sorted(required_columns - fieldnames)
        if missing_columns:
            return ReadinessGate(
                "human baseline",
                "fail",
                "Human baseline CSV is missing required columns.",
                (f"missing columns: {', '.join(missing_columns)}",),
            )
        row_count = 0
        for row_number, row in enumerate(reader, start=2):
            row_count += 1
            item_id = (row.get("item_id") or "").strip()
            participant_id = (row.get("participant_id") or "").strip()
            seconds = (row.get("seconds") or "").strip()
            correct = (row.get("correct") or "").strip().lower()
            if not item_id:
                issues.append(f"{path}:{row_number} missing item_id")
            elif item_id not in dataset_ids:
                issues.append(f"{path}:{row_number} unknown item_id: {item_id}")
            else:
                covered_item_ids.add(item_id)
            if not participant_id:
                issues.append(f"{path}:{row_number} missing participant_id")
            else:
                participant_ids.add(participant_id)
            try:
                if float(seconds) < 0:
                    issues.append(f"{path}:{row_number} seconds must be non-negative")
            except ValueError:
                issues.append(f"{path}:{row_number} invalid seconds: {seconds!r}")
            if correct not in {"true", "false", "1", "0"}:
                issues.append(f"{path}:{row_number} correct must be true/false")
    if row_count == 0:
        return ReadinessGate(
            "human baseline",
            "fail",
            "Human baseline CSV has no response rows.",
        )
    if len(participant_ids) < min_participants:
        issues.append(
            f"only {len(participant_ids)}/{min_participants} participant(s) present"
        )
    missing_item_ids = sorted(dataset_ids - covered_item_ids)
    if missing_item_ids:
        issues.append(
            _summarize_ids(
                f"missing responses for {len(missing_item_ids)} item(s)",
                missing_item_ids,
            )
        )
    if issues:
        return ReadinessGate(
            "human baseline",
            "fail",
            "Human baseline CSV is present but not sufficient.",
            tuple(issues[:20]),
        )
    return ReadinessGate(
        "human baseline",
        "pass",
        (
            f"Human baseline CSV contains {row_count} response row(s) from "
            f"{len(participant_ids)} participant(s) covering {len(covered_item_ids)} "
            "item(s)."
        ),
    )


def _paper_manifest_gate(
    path: Path | None,
    dataset_items: Sequence[BenchmarkItem],
) -> ReadinessGate:
    base_gate = _required_file_gate("paper split manifest", path)
    if base_gate.status == "fail" or path is None:
        return base_gate

    dataset_ids = {item.id for item in dataset_items}
    manifest_ids: list[str] = []
    issues: list[str] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError as exc:
            issues.append(f"{path}:{line_number} invalid JSON: {exc.msg}")
            continue
        item_id = record.get("item_id")
        if not isinstance(item_id, str) or not item_id:
            issues.append(f"{path}:{line_number} missing non-empty item_id")
            continue
        manifest_ids.append(item_id)
        if item_id not in dataset_ids:
            issues.append(f"{path}:{line_number} unknown item_id: {item_id}")
    if not manifest_ids:
        issues.append(f"{path} has no manifest item rows")
    if issues:
        return ReadinessGate(
            "paper split manifest",
            "fail",
            "Paper split manifest is present but not valid.",
            tuple(issues[:20]),
        )
    return ReadinessGate(
        "paper split manifest",
        "pass",
        f"Paper split manifest lists {len(manifest_ids)} item(s).",
    )


def _load_dataset_items(
    paths: Sequence[Path],
    *,
    include_item_ids: set[str] | None = None,
) -> list[BenchmarkItem]:
    items: list[BenchmarkItem] = []
    for path in paths:
        if not path.exists():
            continue
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            if include_item_ids is not None:
                try:
                    raw = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if raw.get("id") not in include_item_ids:
                    continue
            try:
                items.append(BenchmarkItem.model_validate_json(line))
            except (ValueError, ValidationError):
                continue
    return items


def _load_manifest_item_ids(path: Path | None) -> set[str] | None:
    if path is None or not path.exists():
        return None
    item_ids: set[str] = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            continue
        item_id = record.get("item_id")
        if isinstance(item_id, str) and item_id:
            item_ids.add(item_id)
    return item_ids


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


def _summarize_ids(label: str, item_ids: Sequence[str], *, limit: int = 10) -> str:
    shown = ", ".join(item_ids[:limit])
    if len(item_ids) > limit:
        shown += f", ... ({len(item_ids) - limit} more)"
    return f"{label}: {shown}"
