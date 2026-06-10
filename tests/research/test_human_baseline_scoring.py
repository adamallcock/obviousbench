from __future__ import annotations

import csv
import subprocess
import sys
from pathlib import Path

from obviousbench.research.human_baseline_scoring import (
    HumanBaselineScoringInputs,
    score_human_baseline_responses,
)


def _write_csv(path: Path, fieldnames: tuple[str, ...], rows: list[dict[str, str]]) -> None:
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
                "item_id": "item-1",
                "family": "character_count",
                "subfamily": "single_letter_count",
                "target": "3",
                "answer_type": "integer",
                "scorer": "exact_integer_extract_first_v0",
            },
            {
                "item_id": "item-2",
                "family": "spelling_transform",
                "subfamily": "remove_letter",
                "target": "strawbrry",
                "answer_type": "string",
                "scorer": "exact_string_trim_v0",
            },
        ],
    )


def test_score_human_baseline_responses_scores_completed_rows(tmp_path: Path):
    responses = tmp_path / "responses.csv"
    answer_key = tmp_path / "answer-key.csv"
    scored = tmp_path / "scored.csv"
    report = tmp_path / "report.md"
    _write_answer_key(answer_key)
    _write_csv(
        responses,
        ("item_id", "participant_id", "answer", "seconds", "correct", "notes"),
        [
            {
                "item_id": "item-1",
                "participant_id": "p01",
                "answer": "3",
                "seconds": "2.4",
                "correct": "",
                "notes": "",
            },
            {
                "item_id": "item-2",
                "participant_id": "p01",
                "answer": "strawberry",
                "seconds": "3.1",
                "correct": "",
                "notes": "",
            },
        ],
    )

    result = score_human_baseline_responses(
        HumanBaselineScoringInputs(
            responses_path=responses,
            answer_key_path=answer_key,
            scored_path=scored,
            report_path=report,
        )
    )

    rows = _rows(scored)
    assert result.ok
    assert result.row_count == 2
    assert result.scored_count == 2
    assert result.correct_count == 1
    assert rows[0]["correct"] == "true"
    assert rows[1]["correct"] == "false"
    assert "Overall status: PASS" in report.read_text(encoding="utf-8")


def test_score_human_baseline_responses_blocks_blank_template_rows(tmp_path: Path):
    responses = tmp_path / "responses.csv"
    answer_key = tmp_path / "answer-key.csv"
    scored = tmp_path / "scored.csv"
    report = tmp_path / "report.md"
    _write_answer_key(answer_key)
    _write_csv(
        responses,
        ("item_id", "participant_id", "answer", "seconds", "correct", "notes"),
        [
            {
                "item_id": "item-1",
                "participant_id": "p01",
                "answer": "",
                "seconds": "",
                "correct": "",
                "notes": "",
            }
        ],
    )

    result = score_human_baseline_responses(
        HumanBaselineScoringInputs(
            responses_path=responses,
            answer_key_path=answer_key,
            scored_path=scored,
            report_path=report,
        )
    )

    assert not result.ok
    assert result.scored_count == 0
    assert result.issue_count == 2
    assert _rows(scored)[0]["correct"] == ""
    text = report.read_text(encoding="utf-8")
    assert "missing answer" in text
    assert "invalid seconds" in text


def test_score_human_baseline_script_writes_outputs(tmp_path: Path):
    responses = tmp_path / "responses.csv"
    answer_key = tmp_path / "answer-key.csv"
    scored = tmp_path / "scored.csv"
    report = tmp_path / "report.md"
    _write_answer_key(answer_key)
    _write_csv(
        responses,
        ("item_id", "participant_id", "answer", "seconds", "correct", "notes"),
        [
            {
                "item_id": "item-1",
                "participant_id": "p01",
                "answer": "3",
                "seconds": "2.4",
                "correct": "",
                "notes": "",
            }
        ],
    )

    result = subprocess.run(
        [
            sys.executable,
            "scripts/score_human_baseline.py",
            "--responses",
            str(responses),
            "--answer-key",
            str(answer_key),
            "--scored-out",
            str(scored),
            "--report-out",
            str(report),
            "--strict",
        ],
        cwd=Path(__file__).parents[2],
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0
    assert "Wrote human-baseline scoring report" in result.stdout
    assert scored.exists()
    assert report.exists()
