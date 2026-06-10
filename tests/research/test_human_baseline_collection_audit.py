from __future__ import annotations

import csv
import subprocess
import sys
from pathlib import Path

from obviousbench.research.human_baseline_collection_audit import (
    HumanBaselineCollectionAuditInputs,
    audit_human_baseline_collection,
)


def _write_csv(path: Path, fieldnames: tuple[str, ...], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def _fixture(tmp_path: Path, *, complete: bool) -> HumanBaselineCollectionAuditInputs:
    assignments = tmp_path / "assignments.csv"
    responses = tmp_path / "responses.csv"
    answer_key = tmp_path / "answer-key.csv"
    assignment_rows = [
        {
            "participant_id": participant,
            "sequence": str(sequence),
            "item_id": item_id,
            "family": family,
            "subfamily": "sub",
            "answer_type": "integer",
            "scorer": "exact_integer_extract_first_v0",
            "prompt": f"Prompt for {item_id}",
        }
        for participant in ("p01", "p02")
        for sequence, (item_id, family) in enumerate(
            (("item-1", "family-a"), ("item-2", "family-b")),
            start=1,
        )
    ]
    response_rows = [
        {
            "item_id": row["item_id"],
            "participant_id": row["participant_id"],
            "answer": "3" if complete else "",
            "seconds": "2.5" if complete else "",
            "correct": "",
            "notes": "",
        }
        for row in assignment_rows
    ]
    _write_csv(
        assignments,
        (
            "participant_id",
            "sequence",
            "item_id",
            "family",
            "subfamily",
            "answer_type",
            "scorer",
            "prompt",
        ),
        assignment_rows,
    )
    _write_csv(
        responses,
        ("item_id", "participant_id", "answer", "seconds", "correct", "notes"),
        response_rows,
    )
    _write_csv(
        answer_key,
        ("item_id", "family", "subfamily", "target", "answer_type", "scorer"),
        [
            {
                "item_id": "item-1",
                "family": "family-a",
                "subfamily": "sub",
                "target": "3",
                "answer_type": "integer",
                "scorer": "exact_integer_extract_first_v0",
            },
            {
                "item_id": "item-2",
                "family": "family-b",
                "subfamily": "sub",
                "target": "3",
                "answer_type": "integer",
                "scorer": "exact_integer_extract_first_v0",
            },
        ],
    )
    return HumanBaselineCollectionAuditInputs(
        assignments_path=assignments,
        responses_path=responses,
        answer_key_path=answer_key,
        report_path=tmp_path / "collection-audit.md",
        expected_participants=2,
    )


def test_collection_audit_blocks_empty_response_template(tmp_path: Path):
    inputs = _fixture(tmp_path, complete=False)

    result = audit_human_baseline_collection(inputs)

    assert not result.ok
    assert result.expected_response_rows == 4
    assert result.completed_row_count == 0
    assert result.missing_answer_count == 4
    assert result.invalid_seconds_count == 4
    assert result.issue_count == 0
    text = inputs.report_path.read_text(encoding="utf-8")
    assert "Overall status: BLOCKED" in text
    assert "Ready for scoring: no" in text


def test_collection_audit_passes_completed_responses(tmp_path: Path):
    inputs = _fixture(tmp_path, complete=True)

    result = audit_human_baseline_collection(inputs)

    assert result.ok
    assert result.completed_row_count == 4
    assert result.missing_response_count == 0
    assert result.missing_answer_count == 0
    assert result.invalid_seconds_count == 0
    assert "Overall status: PASS" in inputs.report_path.read_text(encoding="utf-8")


def test_collection_audit_script_writes_report(tmp_path: Path):
    inputs = _fixture(tmp_path, complete=False)

    result = subprocess.run(
        [
            sys.executable,
            "scripts/audit_human_baseline_collection.py",
            "--assignments",
            str(inputs.assignments_path),
            "--responses",
            str(inputs.responses_path),
            "--answer-key",
            str(inputs.answer_key_path),
            "--out",
            str(inputs.report_path),
            "--expected-participants",
            "2",
        ],
        cwd=Path(__file__).parents[2],
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0
    assert "Wrote human-baseline collection audit" in result.stdout
    assert inputs.report_path.exists()
