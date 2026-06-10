"""Audit human-baseline collection completeness before scoring."""

from __future__ import annotations

import csv
from collections import Counter, defaultdict
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path

from obviousbench.research.human_baseline_packet import (
    ANSWER_KEY_COLUMNS,
    ASSIGNMENT_COLUMNS,
    RESPONSE_COLUMNS,
)


@dataclass(frozen=True)
class HumanBaselineCollectionAuditInputs:
    assignments_path: Path
    responses_path: Path
    answer_key_path: Path
    report_path: Path
    expected_participants: int = 5
    generated_on: str = "2026-06-01"


@dataclass(frozen=True)
class ParticipantCollectionSummary:
    participant_id: str
    expected_rows: int
    response_rows: int
    completed_rows: int
    missing_answer_count: int
    invalid_seconds_count: int
    missing_response_count: int


@dataclass(frozen=True)
class FamilyCollectionSummary:
    family: str
    expected_rows: int
    completed_rows: int
    missing_answer_count: int
    invalid_seconds_count: int


@dataclass(frozen=True)
class HumanBaselineCollectionAuditResult:
    report_path: Path
    expected_response_rows: int
    response_row_count: int
    completed_row_count: int
    participant_count: int
    item_count: int
    missing_response_count: int
    missing_answer_count: int
    invalid_seconds_count: int
    duplicate_assignment_count: int
    duplicate_response_count: int
    unknown_response_count: int
    issue_count: int
    participants: tuple[ParticipantCollectionSummary, ...]
    families: tuple[FamilyCollectionSummary, ...]

    @property
    def ok(self) -> bool:
        return (
            self.expected_response_rows > 0
            and self.response_row_count == self.expected_response_rows
            and self.completed_row_count == self.expected_response_rows
            and self.missing_response_count == 0
            and self.missing_answer_count == 0
            and self.invalid_seconds_count == 0
            and self.issue_count == 0
        )


def audit_human_baseline_collection(
    inputs: HumanBaselineCollectionAuditInputs,
) -> HumanBaselineCollectionAuditResult:
    """Write a collection-progress audit without scoring answers."""
    issues: list[str] = []
    assignments = _read_csv(inputs.assignments_path, ASSIGNMENT_COLUMNS, issues)
    responses = _read_csv(inputs.responses_path, RESPONSE_COLUMNS, issues)
    answer_key_rows = _read_csv(inputs.answer_key_path, ANSWER_KEY_COLUMNS, issues)

    item_to_family = {
        row["item_id"].strip(): row["family"].strip()
        for row in answer_key_rows
        if row.get("item_id")
    }
    expected_pairs: set[tuple[str, str]] = set()
    assignment_pair_counts: Counter[tuple[str, str]] = Counter()
    expected_by_participant: Counter[str] = Counter()
    expected_by_family: Counter[str] = Counter()
    family_by_pair: dict[tuple[str, str], str] = {}
    item_ids: set[str] = set()

    for row in assignments:
        participant_id = row["participant_id"].strip()
        item_id = row["item_id"].strip()
        family = (row.get("family") or "").strip() or item_to_family.get(item_id, "")
        pair = (participant_id, item_id)
        assignment_pair_counts[pair] += 1
        expected_pairs.add(pair)
        expected_by_participant[participant_id] += 1
        expected_by_family[family] += 1
        family_by_pair[pair] = family
        item_ids.add(item_id)

    duplicate_assignment_count = sum(
        count - 1 for count in assignment_pair_counts.values() if count > 1
    )
    if duplicate_assignment_count:
        issues.append(
            f"{duplicate_assignment_count} duplicate assignment row(s) by participant/item"
        )

    response_pair_counts: Counter[tuple[str, str]] = Counter()
    response_by_pair: dict[tuple[str, str], dict[str, str]] = {}
    duplicate_response_count = 0
    unknown_response_count = 0
    missing_answer_count = 0
    invalid_seconds_count = 0
    completed_pairs: set[tuple[str, str]] = set()
    response_rows_on_assignment = 0

    for row in responses:
        participant_id = row["participant_id"].strip()
        item_id = row["item_id"].strip()
        pair = (participant_id, item_id)
        response_pair_counts[pair] += 1
        if response_pair_counts[pair] > 1:
            duplicate_response_count += 1
            continue
        if pair not in expected_pairs:
            unknown_response_count += 1
            continue
        response_rows_on_assignment += 1
        response_by_pair[pair] = row
        has_answer = bool(row["answer"].strip())
        has_valid_seconds = _valid_seconds(row["seconds"].strip())
        if not has_answer:
            missing_answer_count += 1
        if not has_valid_seconds:
            invalid_seconds_count += 1
        if has_answer and has_valid_seconds:
            completed_pairs.add(pair)

    if duplicate_response_count:
        issues.append(
            f"{duplicate_response_count} duplicate response row(s) by participant/item"
        )
    if unknown_response_count:
        issues.append(
            f"{unknown_response_count} response row(s) do not match assignments"
        )

    participant_ids = sorted(expected_by_participant)
    if len(participant_ids) < inputs.expected_participants:
        issues.append(
            f"{len(participant_ids)} participant(s) present; "
            f"expected at least {inputs.expected_participants}"
        )

    missing_pairs = expected_pairs - set(response_by_pair)
    participant_summaries = _participant_summaries(
        participant_ids,
        expected_by_participant,
        response_by_pair,
        completed_pairs,
        missing_pairs,
    )
    family_summaries = _family_summaries(
        expected_by_family,
        expected_pairs,
        family_by_pair,
        response_by_pair,
        completed_pairs,
    )
    result = HumanBaselineCollectionAuditResult(
        report_path=inputs.report_path,
        expected_response_rows=len(expected_pairs),
        response_row_count=response_rows_on_assignment,
        completed_row_count=len(completed_pairs),
        participant_count=len(participant_ids),
        item_count=len(item_ids),
        missing_response_count=len(missing_pairs),
        missing_answer_count=missing_answer_count,
        invalid_seconds_count=invalid_seconds_count,
        duplicate_assignment_count=duplicate_assignment_count,
        duplicate_response_count=duplicate_response_count,
        unknown_response_count=unknown_response_count,
        issue_count=len(issues),
        participants=tuple(participant_summaries),
        families=tuple(family_summaries),
    )
    inputs.report_path.parent.mkdir(parents=True, exist_ok=True)
    inputs.report_path.write_text(_render_markdown(result, inputs, issues), encoding="utf-8")
    return result


def _read_csv(
    path: Path,
    required_columns: tuple[str, ...],
    issues: list[str],
) -> list[dict[str, str]]:
    if not path.exists():
        issues.append(f"missing file: {path}")
        return []
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        missing = sorted(set(required_columns) - set(reader.fieldnames or ()))
        if missing:
            issues.append(f"{path} missing columns: {', '.join(missing)}")
            return []
        return [dict(row) for row in reader]


def _valid_seconds(value: str) -> bool:
    try:
        return float(value) >= 0
    except ValueError:
        return False


def _participant_summaries(
    participant_ids: Iterable[str],
    expected_by_participant: Counter[str],
    response_by_pair: dict[tuple[str, str], dict[str, str]],
    completed_pairs: set[tuple[str, str]],
    missing_pairs: set[tuple[str, str]],
) -> list[ParticipantCollectionSummary]:
    rows: list[ParticipantCollectionSummary] = []
    for participant_id in participant_ids:
        pairs = [pair for pair in response_by_pair if pair[0] == participant_id]
        rows.append(
            ParticipantCollectionSummary(
                participant_id=participant_id,
                expected_rows=expected_by_participant[participant_id],
                response_rows=len(pairs),
                completed_rows=sum(pair in completed_pairs for pair in pairs),
                missing_answer_count=sum(
                    not response_by_pair[pair]["answer"].strip() for pair in pairs
                ),
                invalid_seconds_count=sum(
                    not _valid_seconds(response_by_pair[pair]["seconds"].strip())
                    for pair in pairs
                ),
                missing_response_count=sum(
                    pair[0] == participant_id for pair in missing_pairs
                ),
            )
        )
    return rows


def _family_summaries(
    expected_by_family: Counter[str],
    expected_pairs: set[tuple[str, str]],
    family_by_pair: dict[tuple[str, str], str],
    response_by_pair: dict[tuple[str, str], dict[str, str]],
    completed_pairs: set[tuple[str, str]],
) -> list[FamilyCollectionSummary]:
    pairs_by_family: dict[str, list[tuple[str, str]]] = defaultdict(list)
    for pair in expected_pairs:
        pairs_by_family[family_by_pair.get(pair, "")].append(pair)
    rows: list[FamilyCollectionSummary] = []
    for family in sorted(expected_by_family):
        pairs = pairs_by_family[family]
        response_pairs = [pair for pair in pairs if pair in response_by_pair]
        rows.append(
            FamilyCollectionSummary(
                family=family or "unknown",
                expected_rows=expected_by_family[family],
                completed_rows=sum(pair in completed_pairs for pair in pairs),
                missing_answer_count=sum(
                    pair in response_by_pair
                    and not response_by_pair[pair]["answer"].strip()
                    for pair in response_pairs
                ),
                invalid_seconds_count=sum(
                    pair in response_by_pair
                    and not _valid_seconds(response_by_pair[pair]["seconds"].strip())
                    for pair in response_pairs
                ),
            )
        )
    return rows


def _render_markdown(
    result: HumanBaselineCollectionAuditResult,
    inputs: HumanBaselineCollectionAuditInputs,
    issues: list[str],
) -> str:
    lines = [
        "---",
        "title: Paper V1 Human Baseline Collection Audit",
        f"date: {inputs.generated_on}",
        "type: research",
        f"status: {'ready' if result.ok else 'blocked'}",
        "---",
        "",
        "# Paper V1 Human Baseline Collection Audit",
        "",
        "This audit checks collection completeness before scorer-based grading.",
        "It does not create participant data, score answers, or run model providers.",
        "",
        f"Overall status: {'PASS' if result.ok else 'BLOCKED'}",
        "",
        f"- Assignments: `{inputs.assignments_path}`",
        f"- Responses: `{inputs.responses_path}`",
        f"- Answer key: `{inputs.answer_key_path}`",
        f"- Expected response rows: {result.expected_response_rows}",
        f"- Response rows present: {result.response_row_count}",
        f"- Completed answer+timing rows: {result.completed_row_count}",
        f"- Participants: {result.participant_count}",
        f"- Items: {result.item_count}",
        f"- Missing response rows: {result.missing_response_count}",
        f"- Missing answers: {result.missing_answer_count}",
        f"- Invalid timings: {result.invalid_seconds_count}",
        f"- Duplicate assignment rows: {result.duplicate_assignment_count}",
        f"- Duplicate response rows: {result.duplicate_response_count}",
        f"- Unknown response rows: {result.unknown_response_count}",
        f"- Structural issues: {result.issue_count}",
        f"- Ready for scoring: {'yes' if result.ok else 'no'}",
        "",
        "## Participant Progress",
        "",
        "| Participant | Expected | Present | Complete | Missing response | "
        "Missing answer | Invalid seconds |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in result.participants:
        lines.append(
            "| "
            + " | ".join(
                [
                    row.participant_id,
                    str(row.expected_rows),
                    str(row.response_rows),
                    str(row.completed_rows),
                    str(row.missing_response_count),
                    str(row.missing_answer_count),
                    str(row.invalid_seconds_count),
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Family Progress",
            "",
            "| Family | Expected | Complete | Missing answer | Invalid seconds |",
            "| --- | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in result.families:
        lines.append(
            "| "
            + " | ".join(
                [
                    row.family,
                    str(row.expected_rows),
                    str(row.completed_rows),
                    str(row.missing_answer_count),
                    str(row.invalid_seconds_count),
                ]
            )
            + " |"
        )
    if issues:
        lines.extend(["", "## Structural Issues", ""])
        for issue in issues[:40]:
            lines.append(f"- {issue}")
        if len(issues) > 40:
            lines.append(f"- {len(issues) - 40} additional issue(s) omitted.")
    lines.extend(
        [
            "",
            "## Next Step Rule",
            "",
            "Run scoring only after this audit passes. After scoring, run the",
            "threshold audit and promote checked rows to",
            "`data/human_baseline/paper_v1.csv` only when readiness can pass.",
            "",
        ]
    )
    return "\n".join(lines)
