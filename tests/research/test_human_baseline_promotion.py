from __future__ import annotations

import csv
import subprocess
import sys
from pathlib import Path

from obviousbench.research.human_baseline_promotion import (
    HumanBaselinePromotionInputs,
    build_human_baseline_promotion_report,
)
from obviousbench.research.human_baseline_scoring import RESPONSE_COLUMNS


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _fixture(tmp_path: Path, *, ready: bool) -> HumanBaselinePromotionInputs:
    scored = tmp_path / "scored.csv"
    promoted = tmp_path / "paper_v1.csv"
    collection_audit = tmp_path / "collection.md"
    scoring_report = tmp_path / "scoring.md"
    threshold_audit = tmp_path / "thresholds.md"
    threshold_items = tmp_path / "threshold-items.csv"
    output_path = tmp_path / "promotion.md"
    status = "PASS" if ready else "BLOCKED"
    _write(collection_audit, f"Overall status: {status}\n")
    _write(scoring_report, f"Overall status: {status}\n")
    _write(threshold_audit, f"Overall status: {status}\n")
    if ready:
        _write(
            scored,
            "item_id,participant_id,answer,seconds,correct,notes,scorer,target,"
            "extracted,failure_type,format_correct,strict_correct\n"
            "item-1,p01,3,1.2,true,,exact_match,3,3,,true,true\n"
            "item-2,p01,4,2.0,false,,exact_match,5,4,wrong,true,false\n",
        )
        _write(
            threshold_items,
            "item_id,family,subfamily,scorer,response_count,correct_count,"
            "accuracy,median_seconds,confusion_note_count,status,reason\n"
            "item-1,arithmetic,add,exact_match,1,1,1,1.2,0,core_h0,ok\n"
            "item-2,arithmetic,add,exact_match,1,0,0,2,0,exclude,low accuracy\n",
        )
    else:
        _write(
            scored,
            "item_id,participant_id,answer,seconds,correct,notes,scorer,target,"
            "extracted,failure_type,format_correct,strict_correct\n"
            "item-1,p01,,bad,,,exact_match,3,,,,\n",
        )
        _write(
            threshold_items,
            "item_id,family,subfamily,scorer,response_count,correct_count,"
            "accuracy,median_seconds,confusion_note_count,status,reason\n"
            "item-1,arithmetic,add,exact_match,0,0,,,0,no_data,no rows\n",
        )
    _write(promoted, "item_id,participant_id,answer,seconds,correct,notes\n")
    return HumanBaselinePromotionInputs(
        output_path=output_path,
        scored_path=scored,
        promoted_path=promoted,
        collection_audit_path=collection_audit,
        scoring_report_path=scoring_report,
        threshold_audit_path=threshold_audit,
        threshold_items_path=threshold_items,
    )


def test_promotion_report_blocks_incomplete_inputs(tmp_path: Path):
    inputs = _fixture(tmp_path, ready=False)

    result = build_human_baseline_promotion_report(inputs)

    assert not result.ok
    assert result.applied is False
    assert result.check_by_name("collection audit").status == "blocked"
    assert result.check_by_name("threshold item states").status == "blocked"
    assert "Overall status: BLOCKED" in inputs.output_path.read_text(encoding="utf-8")
    assert inputs.promoted_path.read_text(encoding="utf-8").count("\n") == 1


def test_promotion_report_passes_ready_dry_run_without_writing(tmp_path: Path):
    inputs = _fixture(tmp_path, ready=True)

    result = build_human_baseline_promotion_report(inputs)

    assert result.ok
    assert result.applied is False
    assert result.source_rows == 2
    assert result.promoted_rows == 0
    assert "Overall status: PASS" in inputs.output_path.read_text(encoding="utf-8")
    assert inputs.promoted_path.read_text(encoding="utf-8").count("\n") == 1


def test_promotion_apply_writes_readiness_columns(tmp_path: Path):
    inputs = _fixture(tmp_path, ready=True)

    result = build_human_baseline_promotion_report(inputs, apply=True)

    assert result.ok
    assert result.applied
    assert result.promoted_rows == 2
    with inputs.promoted_path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        assert tuple(reader.fieldnames or ()) == RESPONSE_COLUMNS
        rows = list(reader)
    assert rows[0]["item_id"] == "item-1"
    assert rows[0]["correct"] == "true"
    assert "scorer" not in rows[0]


def test_promotion_script_fails_strictly_when_blocked(tmp_path: Path):
    inputs = _fixture(tmp_path, ready=False)

    result = subprocess.run(
        [
            sys.executable,
            "scripts/promote_human_baseline.py",
            "--scored",
            str(inputs.scored_path),
            "--promoted",
            str(inputs.promoted_path),
            "--collection-audit",
            str(inputs.collection_audit_path),
            "--scoring-report",
            str(inputs.scoring_report_path),
            "--threshold-audit",
            str(inputs.threshold_audit_path),
            "--threshold-items",
            str(inputs.threshold_items_path),
            "--out",
            str(inputs.output_path),
            "--strict",
        ],
        cwd=Path(__file__).parents[2],
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 1
    assert "Human-baseline promotion audited: blocked" in result.stdout
    assert inputs.output_path.exists()
