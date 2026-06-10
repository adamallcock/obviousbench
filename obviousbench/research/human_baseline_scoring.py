"""Score filled human-baseline response templates for the paper split."""

from __future__ import annotations

import csv
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

from obviousbench.scorers.dynamic import score_by_name

RESPONSE_COLUMNS = ("item_id", "participant_id", "answer", "seconds", "correct", "notes")
SCORED_COLUMNS = (
    "item_id",
    "participant_id",
    "answer",
    "seconds",
    "correct",
    "notes",
    "scorer",
    "target",
    "extracted",
    "failure_type",
    "format_correct",
    "strict_correct",
)


@dataclass(frozen=True)
class AnswerKeyEntry:
    item_id: str
    family: str
    subfamily: str
    target: str
    answer_type: str
    scorer: str


@dataclass(frozen=True)
class HumanBaselineScoringInputs:
    responses_path: Path
    answer_key_path: Path
    scored_path: Path
    report_path: Path
    generated_on: str = "2026-06-01"


@dataclass(frozen=True)
class HumanBaselineScoringResult:
    scored_path: Path
    report_path: Path
    row_count: int
    scored_count: int
    correct_count: int
    participant_count: int
    item_count: int
    issue_count: int

    @property
    def ok(self) -> bool:
        return self.row_count > 0 and self.issue_count == 0


def score_human_baseline_responses(
    inputs: HumanBaselineScoringInputs,
) -> HumanBaselineScoringResult:
    """Score response rows with the benchmark scorer contracts."""
    answer_key = _load_answer_key(inputs.answer_key_path)
    scored_rows: list[dict[str, str]] = []
    issues: list[str] = []
    participant_ids: set[str] = set()
    item_ids: set[str] = set()
    family_counts: Counter[str] = Counter()

    rows = _load_response_rows(inputs.responses_path, issues)
    for row_number, row in enumerate(rows, start=2):
        scored, row_issues = _score_row(row, row_number, answer_key)
        issues.extend(row_issues)
        scored_rows.append(scored)
        item_id = scored["item_id"]
        participant_id = scored["participant_id"]
        if participant_id:
            participant_ids.add(participant_id)
        if item_id:
            item_ids.add(item_id)
        key = answer_key.get(item_id)
        if key is not None:
            family_counts[key.family] += 1

    inputs.scored_path.parent.mkdir(parents=True, exist_ok=True)
    inputs.report_path.parent.mkdir(parents=True, exist_ok=True)
    _write_scored(inputs.scored_path, scored_rows)
    result = HumanBaselineScoringResult(
        scored_path=inputs.scored_path,
        report_path=inputs.report_path,
        row_count=len(scored_rows),
        scored_count=sum(row["correct"] in {"true", "false"} for row in scored_rows),
        correct_count=sum(row["correct"] == "true" for row in scored_rows),
        participant_count=len(participant_ids),
        item_count=len(item_ids),
        issue_count=len(issues),
    )
    inputs.report_path.write_text(
        _render_report(result, inputs, issues, family_counts),
        encoding="utf-8",
    )
    return result


def _load_answer_key(path: Path) -> dict[str, AnswerKeyEntry]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        return {
            str(row["item_id"]): AnswerKeyEntry(
                item_id=str(row["item_id"]),
                family=str(row["family"]),
                subfamily=str(row["subfamily"]),
                target=str(row["target"]),
                answer_type=str(row["answer_type"]),
                scorer=str(row["scorer"]),
            )
            for row in reader
        }


def _load_response_rows(path: Path, issues: list[str]) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = set(reader.fieldnames or [])
        missing = sorted(set(RESPONSE_COLUMNS) - fieldnames)
        if missing:
            issues.append(f"{path} missing columns: {', '.join(missing)}")
            return []
        return [dict(row) for row in reader]


def _score_row(
    row: dict[str, str],
    row_number: int,
    answer_key: dict[str, AnswerKeyEntry],
) -> tuple[dict[str, str], list[str]]:
    issues: list[str] = []
    item_id = (row.get("item_id") or "").strip()
    participant_id = (row.get("participant_id") or "").strip()
    answer = (row.get("answer") or "").strip()
    seconds = (row.get("seconds") or "").strip()
    notes = row.get("notes") or ""
    key = answer_key.get(item_id)
    scored = {
        "item_id": item_id,
        "participant_id": participant_id,
        "answer": answer,
        "seconds": seconds,
        "correct": "",
        "notes": notes,
        "scorer": key.scorer if key else "",
        "target": key.target if key else "",
        "extracted": "",
        "failure_type": "",
        "format_correct": "",
        "strict_correct": "",
    }
    if not item_id:
        issues.append(f"row {row_number}: missing item_id")
    elif key is None:
        issues.append(f"row {row_number}: unknown item_id {item_id}")
    if not participant_id:
        issues.append(f"row {row_number}: missing participant_id")
    if not answer:
        issues.append(f"row {row_number}: missing answer")
    if not _valid_seconds(seconds):
        issues.append(f"row {row_number}: invalid seconds {seconds!r}")
    if key is None or not answer:
        return scored, issues

    decision = score_by_name(key.scorer, answer, key.target)
    scored.update(
        {
            "correct": "true" if decision.answer_correct else "false",
            "extracted": decision.extracted or "",
            "failure_type": decision.failure_type,
            "format_correct": "true" if decision.resolved_format_correct else "false",
            "strict_correct": "true" if decision.strict_correct else "false",
        }
    )
    return scored, issues


def _valid_seconds(value: str) -> bool:
    try:
        return float(value) >= 0
    except ValueError:
        return False


def _write_scored(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=SCORED_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)


def _render_report(
    result: HumanBaselineScoringResult,
    inputs: HumanBaselineScoringInputs,
    issues: list[str],
    family_counts: Counter[str],
) -> str:
    lines = [
        "---",
        "title: Paper V1 Human Baseline Scoring Report",
        f"date: {inputs.generated_on}",
        "type: research",
        f"status: {'ready' if result.ok else 'blocked'}",
        "---",
        "",
        "# Paper V1 Human Baseline Scoring Report",
        "",
        "This report scores collected human-baseline response rows with the same",
        "deterministic scorer contracts used by ObviousBench. It does not create",
        "participant data and does not run model providers.",
        "",
        f"Overall status: {'PASS' if result.ok else 'BLOCKED'}",
        "",
        f"- Input responses: `{inputs.responses_path}`",
        f"- Answer key: `{inputs.answer_key_path}`",
        f"- Scored CSV: `{inputs.scored_path}`",
        f"- Response rows: {result.row_count}",
        f"- Scored rows: {result.scored_count}",
        f"- Correct rows: {result.correct_count}",
        f"- Participants: {result.participant_count}",
        f"- Items with rows: {result.item_count}",
        f"- Issues: {result.issue_count}",
        "",
    ]
    lines.extend(_family_lines(family_counts))
    if issues:
        lines.extend(["## Issues", ""])
        for issue in issues[:40]:
            lines.append(f"- {issue}")
        if len(issues) > 40:
            lines.append(f"- {len(issues) - 40} additional issue(s) omitted.")
        lines.append("")
    lines.extend(
        [
            "## Promotion Rule",
            "",
            "Do not copy this scored CSV to `data/human_baseline/paper_v1.csv`",
            "until all response rows have real answers, parseable timings, and",
            "`make -C paper readiness` can pass after promotion.",
            "",
        ]
    )
    return "\n".join(lines)


def _family_lines(family_counts: Counter[str]) -> list[str]:
    lines = ["## Family Row Counts", "", "| Family | Rows |", "| --- | ---: |"]
    if not family_counts:
        lines.append("| n/a | 0 |")
    else:
        for family, count in sorted(family_counts.items()):
            lines.append(f"| `{family}` | {count} |")
    lines.append("")
    return lines
