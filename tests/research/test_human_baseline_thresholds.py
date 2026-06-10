from __future__ import annotations

import csv
import subprocess
import sys
from pathlib import Path

from obviousbench.research.human_baseline_thresholds import (
    HumanBaselineThresholdInputs,
    audit_human_baseline_thresholds,
)


def _write_csv(path: Path, fieldnames: tuple[str, ...], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def _rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def _write_answer_key(path: Path) -> None:
    _write_csv(
        path,
        ("item_id", "family", "subfamily", "target", "answer_type", "scorer"),
        [
            {
                "item_id": "item-core",
                "family": "character_count",
                "subfamily": "single_letter_count",
                "target": "3",
                "answer_type": "integer",
                "scorer": "exact_integer_extract_first_v0",
            },
            {
                "item_id": "item-borderline",
                "family": "character_count",
                "subfamily": "single_letter_count",
                "target": "4",
                "answer_type": "integer",
                "scorer": "exact_integer_extract_first_v0",
            },
            {
                "item_id": "item-exclude",
                "family": "spelling_transform",
                "subfamily": "remove_letter",
                "target": "strawbrry",
                "answer_type": "string",
                "scorer": "exact_string_trim_v0",
            },
            {
                "item_id": "item-empty",
                "family": "spelling_transform",
                "subfamily": "remove_letter",
                "target": "banana",
                "answer_type": "string",
                "scorer": "exact_string_trim_v0",
            },
        ],
    )


def _scored_row(
    item_id: str,
    correct: str,
    seconds: str,
    *,
    participant: str = "p01",
    notes: str = "",
) -> dict[str, str]:
    return {
        "item_id": item_id,
        "participant_id": participant,
        "answer": "answer",
        "seconds": seconds,
        "correct": correct,
        "notes": notes,
        "scorer": "exact_string_trim_v0",
        "target": "answer",
        "extracted": "answer",
        "failure_type": "",
        "format_correct": correct,
        "strict_correct": correct,
    }


def _write_scored(path: Path) -> None:
    rows = []
    for index, seconds in enumerate(("2", "3", "4", "5", "6"), start=1):
        rows.append(
            _scored_row(
                "item-core",
                "true",
                seconds,
                participant=f"p{index:02d}",
            )
        )
    for index, (correct, seconds) in enumerate(
        (("true", "9"), ("true", "11"), ("true", "12"), ("true", "13"), ("false", "14")),
        start=1,
    ):
        rows.append(
            _scored_row(
                "item-borderline",
                correct,
                seconds,
                participant=f"p{index:02d}",
            )
        )
    for index, correct in enumerate(("true", "true", "true", "false", "false"), start=1):
        rows.append(
            _scored_row(
                "item-exclude",
                correct,
                "4",
                participant=f"p{index:02d}",
            )
        )
    _write_csv(
        path,
        (
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
        ),
        rows,
    )


def test_audit_human_baseline_thresholds_classifies_items(tmp_path: Path):
    answer_key = tmp_path / "answer-key.csv"
    scored = tmp_path / "scored.csv"
    item_out = tmp_path / "threshold-items.csv"
    family_out = tmp_path / "threshold-families.csv"
    report = tmp_path / "threshold-report.md"
    _write_answer_key(answer_key)
    _write_scored(scored)

    result = audit_human_baseline_thresholds(
        HumanBaselineThresholdInputs(
            scored_path=scored,
            answer_key_path=answer_key,
            item_output_path=item_out,
            family_output_path=family_out,
            report_path=report,
        )
    )

    assert not result.ok
    assert result.core_h0_count == 1
    assert result.borderline_count == 1
    assert result.exclude_count == 1
    assert result.no_data_count == 1
    rows = {row["item_id"]: row for row in _rows(item_out)}
    assert rows["item-core"]["status"] == "core_h0"
    assert rows["item-borderline"]["status"] == "borderline"
    assert rows["item-exclude"]["status"] == "exclude"
    assert rows["item-empty"]["status"] == "no_data"
    family_rows = _rows(family_out)
    assert {row["family"] for row in family_rows} == {
        "character_count",
        "spelling_transform",
    }
    text = report.read_text(encoding="utf-8")
    assert "Overall status: BLOCKED" in text
    assert "Use only `core_h0` rows" in text


def test_audit_human_baseline_thresholds_blocks_empty_scored_template(tmp_path: Path):
    answer_key = tmp_path / "answer-key.csv"
    scored = tmp_path / "scored.csv"
    _write_answer_key(answer_key)
    _write_csv(
        scored,
        (
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
        ),
        [
            _scored_row("item-core", "", ""),
            _scored_row("item-borderline", "", ""),
        ],
    )

    result = audit_human_baseline_thresholds(
        HumanBaselineThresholdInputs(
            scored_path=scored,
            answer_key_path=answer_key,
            item_output_path=tmp_path / "items.csv",
            family_output_path=tmp_path / "families.csv",
            report_path=tmp_path / "report.md",
        )
    )

    assert not result.ok
    assert result.ignored_row_count == 2
    assert result.no_data_count == 4
    assert result.response_count == 0


def test_human_baseline_threshold_script_writes_outputs(tmp_path: Path):
    answer_key = tmp_path / "answer-key.csv"
    scored = tmp_path / "scored.csv"
    item_out = tmp_path / "threshold-items.csv"
    family_out = tmp_path / "threshold-families.csv"
    report = tmp_path / "threshold-report.md"
    _write_answer_key(answer_key)
    _write_scored(scored)

    result = subprocess.run(
        [
            sys.executable,
            "scripts/audit_human_baseline_thresholds.py",
            "--scored",
            str(scored),
            "--answer-key",
            str(answer_key),
            "--item-out",
            str(item_out),
            "--family-out",
            str(family_out),
            "--report-out",
            str(report),
        ],
        cwd=Path(__file__).parents[2],
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0
    assert "Wrote human-baseline threshold audit" in result.stdout
    assert item_out.exists()
    assert family_out.exists()
    assert report.exists()
