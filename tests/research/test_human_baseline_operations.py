from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from obviousbench.research.human_baseline_operations import (
    HumanBaselineOperationsInputs,
    build_human_baseline_operations_packet,
)


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _inputs(tmp_path: Path, *, complete: bool) -> HumanBaselineOperationsInputs:
    packet = tmp_path / "packet.md"
    collection = tmp_path / "collection.md"
    scoring = tmp_path / "scoring.md"
    thresholds = tmp_path / "thresholds.md"
    promotion = tmp_path / "promotion.md"
    readiness = tmp_path / "readiness.md"
    response_template = tmp_path / "responses.csv"
    baseline = tmp_path / "paper_v1.csv"
    _write(
        packet,
        "Overall status: PASS\n- Participants: 5\n- Preallocated response rows: 400\n",
    )
    _write(response_template, "item_id,participant_id,answer,seconds,correct,notes\n")
    _write(
        collection,
        (
            f"Overall status: {'PASS' if complete else 'BLOCKED'}\n"
            "- Expected response rows: 400\n"
            f"- Completed answer+timing rows: {'400' if complete else '0'}\n"
            f"- Missing answers: {'0' if complete else '400'}\n"
            f"- Invalid timings: {'0' if complete else '400'}\n"
        ),
    )
    _write(
        scoring,
        (
            f"Overall status: {'PASS' if complete else 'BLOCKED'}\n"
            "- Response rows: 400\n"
            f"- Scored rows: {'400' if complete else '0'}\n"
            f"- Issues: {'0' if complete else '800'}\n"
        ),
    )
    _write(
        thresholds,
        (
            f"Overall status: {'PASS' if complete else 'BLOCKED'}\n"
            f"- Core H0 items: {'80' if complete else '0'}\n"
            f"- Items with no scored data: {'0' if complete else '80'}\n"
            f"- Ignored scored rows: {'0' if complete else '400'}\n"
        ),
    )
    _write(readiness, "Overall status: PASS\n" if complete else "Overall status: FAIL\n")
    _write(
        promotion,
        (
            f"Overall status: {'PASS' if complete else 'BLOCKED'}\n"
            "- Source scored rows: 400\n"
            f"- Target rows after run: {'400' if complete else '0'}\n"
        ),
    )
    if complete:
        _write(
            baseline,
            "item_id,participant_id,answer,seconds,correct,notes\nitem,p01,x,1,true,\n",
        )
    else:
        _write(baseline, "item_id,participant_id,answer,seconds,correct,notes\n")
    return HumanBaselineOperationsInputs(
        output_path=tmp_path / "ops.md",
        collection_packet_path=packet,
        collection_audit_path=collection,
        scoring_report_path=scoring,
        threshold_audit_path=thresholds,
        promotion_report_path=promotion,
        readiness_audit_path=readiness,
        response_template_path=response_template,
        promoted_baseline_path=baseline,
    )


def test_human_baseline_operations_blocks_empty_collection(tmp_path: Path):
    inputs = _inputs(tmp_path, complete=False)

    result = build_human_baseline_operations_packet(inputs)

    assert not result.ok
    assert result.check_by_name("collection packet").status == "pass"
    assert result.check_by_name("response collection").status == "blocked"
    assert result.check_by_name("promotion preflight").status == "blocked"
    assert result.check_by_name("paper readiness").status == "blocked"
    text = inputs.output_path.read_text(encoding="utf-8")
    assert "Overall status: BLOCKED" in text
    assert "Do not run final model arrays" in text


def test_human_baseline_operations_can_pass_complete_surface(tmp_path: Path):
    inputs = _inputs(tmp_path, complete=True)

    result = build_human_baseline_operations_packet(inputs)

    assert result.ok
    assert result.blocked_count == 0
    assert "Overall status: PASS" in inputs.output_path.read_text(encoding="utf-8")


def test_human_baseline_operations_script_writes_report(tmp_path: Path):
    output_path = tmp_path / "ops.md"

    result = subprocess.run(
        [
            sys.executable,
            "scripts/build_human_baseline_operations.py",
            "--out",
            str(output_path),
        ],
        cwd=Path(__file__).parents[2],
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0
    assert "Wrote human-baseline operations packet" in result.stdout
    assert output_path.exists()
