"""Build a collection execution handoff for the ObviousBench human baseline."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

CollectionHandoffStatus = Literal["pass", "blocked"]


@dataclass(frozen=True)
class HumanBaselineCollectionHandoffInputs:
    output_path: Path
    assignments_path: Path = Path("data/human_baseline/paper_v1_assignments.csv")
    responses_path: Path = Path("data/human_baseline/paper_v1_response_template.csv")
    answer_key_path: Path = Path("data/human_baseline/paper_v1_answer_key.csv")
    participant_packets_path: Path = Path(
        "docs/research/2026-06-01-paper-v1-human-baseline-participant-packets.md"
    )
    collection_packet_path: Path = Path(
        "docs/research/2026-06-01-paper-v1-human-baseline-collection-packet.md"
    )
    collection_audit_path: Path = Path(
        "docs/research/2026-06-01-paper-v1-human-baseline-collection-audit.md"
    )
    generated_on: str = "2026-06-01"


@dataclass(frozen=True)
class ParticipantCollectionStatus:
    participant_id: str
    expected_rows: int
    present_rows: int
    complete_rows: int
    missing_answers: int
    invalid_seconds: int


@dataclass(frozen=True)
class HumanBaselineCollectionHandoffResult:
    output_path: Path
    status: CollectionHandoffStatus
    participants: tuple[ParticipantCollectionStatus, ...]
    assignment_rows: int
    response_rows: int
    completed_rows: int
    missing_answers: int
    invalid_seconds: int
    packet_ready: bool
    participant_packets_present: bool
    answer_key_present: bool

    @property
    def ok(self) -> bool:
        return self.status == "pass"

    @property
    def participant_count(self) -> int:
        return len(self.participants)


def build_human_baseline_collection_handoff(
    inputs: HumanBaselineCollectionHandoffInputs,
) -> HumanBaselineCollectionHandoffResult:
    """Write a participant-collection execution handoff without collecting data."""
    assignments = _read_csv(inputs.assignments_path)
    responses = _read_csv(inputs.responses_path)
    participants = _participant_statuses(assignments, responses)
    completed_rows = sum(participant.complete_rows for participant in participants)
    missing_answers = sum(participant.missing_answers for participant in participants)
    invalid_seconds = sum(participant.invalid_seconds for participant in participants)
    response_rows = len(responses)
    packet_ready = _overall_status(inputs.collection_packet_path) == "PASS"
    status: CollectionHandoffStatus = (
        "pass"
        if packet_ready
        and bool(participants)
        and response_rows > 0
        and completed_rows == response_rows
        and missing_answers == 0
        and invalid_seconds == 0
        else "blocked"
    )
    result = HumanBaselineCollectionHandoffResult(
        output_path=inputs.output_path,
        status=status,
        participants=participants,
        assignment_rows=len(assignments),
        response_rows=response_rows,
        completed_rows=completed_rows,
        missing_answers=missing_answers,
        invalid_seconds=invalid_seconds,
        packet_ready=packet_ready,
        participant_packets_present=inputs.participant_packets_path.exists(),
        answer_key_present=inputs.answer_key_path.exists(),
    )
    inputs.output_path.parent.mkdir(parents=True, exist_ok=True)
    inputs.output_path.write_text(_render_markdown(result, inputs), encoding="utf-8")
    return result


def _read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def _overall_status(path: Path) -> str:
    if not path.exists():
        return "MISSING"
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("Overall status:"):
            return line.split(":", 1)[1].strip()
    return "MISSING"


def _participant_statuses(
    assignments: list[dict[str, str]],
    responses: list[dict[str, str]],
) -> tuple[ParticipantCollectionStatus, ...]:
    participant_ids = sorted(
        {
            row.get("participant_id", "")
            for row in assignments + responses
            if row.get("participant_id", "")
        }
    )
    statuses = []
    for participant_id in participant_ids:
        expected = [
            row for row in assignments if row.get("participant_id") == participant_id
        ]
        present = [
            row for row in responses if row.get("participant_id") == participant_id
        ]
        missing_answers = sum(1 for row in present if not row.get("answer", "").strip())
        invalid_seconds = sum(
            1 for row in present if not _valid_seconds(row.get("seconds", ""))
        )
        complete = sum(
            1
            for row in present
            if row.get("answer", "").strip() and _valid_seconds(row.get("seconds", ""))
        )
        statuses.append(
            ParticipantCollectionStatus(
                participant_id=participant_id,
                expected_rows=len(expected),
                present_rows=len(present),
                complete_rows=complete,
                missing_answers=missing_answers,
                invalid_seconds=invalid_seconds,
            )
        )
    return tuple(statuses)


def _valid_seconds(value: str | None) -> bool:
    if value is None or not value.strip():
        return False
    try:
        return float(value) >= 0
    except ValueError:
        return False


def _render_markdown(
    result: HumanBaselineCollectionHandoffResult,
    inputs: HumanBaselineCollectionHandoffInputs,
) -> str:
    lines = [
        "---",
        "title: Paper V1 Human Baseline Collection Handoff",
        f"date: {inputs.generated_on}",
        "type: runbook",
        f"status: {'ready' if result.ok else 'blocked'}",
        "---",
        "",
        "# Paper V1 Human Baseline Collection Handoff",
        "",
        "This generated handoff is the operator runbook for collecting the real",
        "human-baseline answer and timing rows. It does not create participant",
        "data, reveal answer keys to participants, score responses, or run model",
        "providers.",
        "",
        f"Overall status: {'PASS' if result.ok else 'BLOCKED'}",
        "",
        f"- Participants: {result.participant_count}",
        f"- Assignment rows: {result.assignment_rows}",
        f"- Response rows: {result.response_rows}",
        f"- Completed answer+timing rows: {result.completed_rows}",
        f"- Missing answers: {result.missing_answers}",
        f"- Invalid seconds: {result.invalid_seconds}",
        f"- Collection packet ready: {'yes' if result.packet_ready else 'no'}",
        (
            "- Participant packets present: "
            f"{'yes' if result.participant_packets_present else 'no'}"
        ),
        f"- Local answer key present: {'yes' if result.answer_key_present else 'no'}",
        "",
        "## Files",
        "",
        f"- Participant packets: `{inputs.participant_packets_path}`",
        f"- Assignment CSV: `{inputs.assignments_path}`",
        f"- Response template CSV: `{inputs.responses_path}`",
        f"- Local answer key: `{inputs.answer_key_path}`",
        f"- Collection audit: `{inputs.collection_audit_path}`",
        "",
        "Only participant packets and assignment rows are participant-facing. The",
        "answer key is local scoring material and must not be shown to",
        "participants.",
        "",
        "## Participant Progress",
        "",
        (
            "| Participant | Expected rows | Present rows | Complete rows | "
            "Missing answers | Invalid seconds |"
        ),
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for participant in result.participants:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{participant.participant_id}`",
                    str(participant.expected_rows),
                    str(participant.present_rows),
                    str(participant.complete_rows),
                    str(participant.missing_answers),
                    str(participant.invalid_seconds),
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Operator Checklist",
            "",
            "- [ ] Assign one pseudonymous participant ID per participant.",
            "- [ ] Give each participant only their own packet section.",
            "- [ ] Confirm participants answer without search, calculators, model",
            "      assistance, or external tools.",
            "- [ ] Time each item or have participants record elapsed seconds per item.",
            "- [ ] Enter answer text exactly as given into the response template.",
            "- [ ] Enter non-negative elapsed seconds for every row.",
            "- [ ] Leave `correct` blank until scorer-based grading is run.",
            "- [ ] Store no names, emails, demographics, payment details, or free-form",
            "      personal data in repository files.",
            "- [ ] Rerun `make -C paper human-baseline-audit` after every collection",
            "      batch.",
            "",
            "## Participant Instructions",
            "",
            "Use this neutral instruction block when distributing each packet:",
            "",
            "```text",
            "Please answer each item without search, calculators, AI/model help, or",
            "other external tools. Answer as quickly and accurately as you can.",
            "Record the elapsed seconds for each item. If an item is unclear, enter",
            "your best answer or leave it blank; skipped or blank items are treated",
            "as incorrect for the baseline.",
            "```",
            "",
            "## Completion Contract",
            "",
            "The collection stage is ready for scoring only when:",
            "",
            "- every preallocated response row is present,",
            "- every `answer` cell is non-empty,",
            "- every `seconds` cell is parseable and non-negative,",
            "- each participant has the expected number of complete rows,",
            "- the collection audit reports `Ready for scoring: yes`.",
            "",
            "## Command Ladder",
            "",
            "```bash",
            "make -C paper human-baseline-packet",
            "make -C paper human-baseline-collection-handoff",
            "# Fill answer and seconds cells in data/human_baseline/paper_v1_response_template.csv",
            "make -C paper human-baseline-audit",
            "make -C paper human-baseline-score",
            "make -C paper human-baseline-thresholds",
            "make -C paper human-baseline-ops",
            "```",
            "",
            "## Stop Rules",
            "",
            "- Do not show `data/human_baseline/paper_v1_answer_key.csv` to participants.",
            "- Do not infer missing answers or timings.",
            "- Do not mark `correct` by hand before the scoring helper runs.",
            "- Do not promote rows to `data/human_baseline/paper_v1.csv` until",
            "  collection, scoring, and threshold audits are reviewed.",
            "- Do not run final model arrays while this handoff is blocked.",
            "",
        ]
    )
    return "\n".join(lines)
