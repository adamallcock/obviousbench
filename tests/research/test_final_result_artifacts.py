from __future__ import annotations

import csv
import subprocess
import sys
from pathlib import Path

from obviousbench.analysis.comparison import (
    COMPARISON_FIELDS,
    DELTA_FIELDS,
    EFFORT_CURVE_FIELDS,
    FAMILY_COMPARISON_FIELDS,
    METAMORPHIC_COMPARISON_FIELDS,
    SECTION_COMPARISON_FIELDS,
)
from obviousbench.research.final_result_artifacts import (
    FinalResultArtifactInputs,
    audit_final_result_artifacts,
)


def _write_csv(path: Path, fieldnames: tuple[str, ...], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def _write(path: Path, text: str = "content\n") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _manifest(path: Path, summary_dir: Path) -> None:
    _write_csv(
        path,
        ("label", "model", "summary_dir"),
        [
            {
                "label": "Unit Model",
                "model": "provider/unit",
                "summary_dir": str(summary_dir),
            }
        ],
    )


def test_final_result_artifact_audit_blocks_missing_outputs(tmp_path: Path):
    manifest = tmp_path / "manifest.csv"
    summary_dir = tmp_path / "summaries" / "unit"
    _manifest(manifest, summary_dir)

    result = audit_final_result_artifacts(
        FinalResultArtifactInputs(
            manifest_path=manifest,
            comparison_dir=tmp_path / "comparison",
            report_dir=tmp_path / "report",
            output_path=tmp_path / "audit.md",
            expected_models=1,
        )
    )

    assert not result.ok
    assert result.planned_model_count == 1
    assert result.missing_summary_file_count == 6
    assert result.missing_comparison_file_count == 6
    assert result.missing_report_file_count == 4
    text = result.output_path.read_text(encoding="utf-8")
    assert "Overall status: BLOCKED" in text
    assert "Paper result prose may cite this evidence run only when this audit passes" in text


def test_final_result_artifact_audit_passes_complete_contract(tmp_path: Path):
    manifest = tmp_path / "manifest.csv"
    summary_dir = tmp_path / "summaries" / "unit"
    comparison_dir = tmp_path / "comparison"
    report_dir = tmp_path / "report"
    _manifest(manifest, summary_dir)
    for filename in (
        "summary.csv",
        "usage_by_family.csv",
        "usage_by_section.csv",
        "usage_by_question.csv",
        "usage_by_sample.csv",
    ):
        _write_csv(summary_dir / filename, ("label",), [{"label": "Unit Model"}])
    _write(summary_dir / "failure_gallery.md")
    comparison_row = {field: "" for field in COMPARISON_FIELDS}
    comparison_row.update(
        {
            "label": "Unit Model",
            "model": "provider/unit",
            "scored_samples": "80",
            "answer_accuracy": "0.8",
        }
    )
    family_row = {field: "" for field in FAMILY_COMPARISON_FIELDS}
    family_row.update({"label": "Unit Model", "family": "character_count", "samples": "10"})
    _write_csv(comparison_dir / "comparison.csv", tuple(COMPARISON_FIELDS), [comparison_row])
    _write_csv(
        comparison_dir / "family_comparison.csv",
        tuple(FAMILY_COMPARISON_FIELDS),
        [family_row],
    )
    _write_csv(
        comparison_dir / "section_comparison.csv",
        tuple(SECTION_COMPARISON_FIELDS),
        [],
    )
    _write_csv(comparison_dir / "effort_curve.csv", tuple(EFFORT_CURVE_FIELDS), [])
    _write_csv(
        comparison_dir / "metamorphic_consistency.csv",
        tuple(METAMORPHIC_COMPARISON_FIELDS),
        [],
    )
    _write_csv(comparison_dir / "delta.csv", tuple(DELTA_FIELDS), [])
    for filename in ("report.html", "leaderboard.csv", "leaderboard.md", "family-heatmap.csv"):
        _write(report_dir / filename)

    result = audit_final_result_artifacts(
        FinalResultArtifactInputs(
            manifest_path=manifest,
            comparison_dir=comparison_dir,
            report_dir=report_dir,
            output_path=tmp_path / "audit.md",
            expected_models=1,
        )
    )

    assert result.ok
    assert result.present_summary_file_count == 6
    assert result.present_comparison_file_count == 6
    assert result.present_report_file_count == 4
    assert "Overall status: PASS" in result.output_path.read_text(encoding="utf-8")


def test_final_result_artifact_script_writes_report(tmp_path: Path):
    manifest = tmp_path / "manifest.csv"
    summary_dir = tmp_path / "summaries" / "unit"
    output_path = tmp_path / "audit.md"
    _manifest(manifest, summary_dir)

    result = subprocess.run(
        [
            sys.executable,
            "scripts/audit_final_result_artifacts.py",
            "--manifest",
            str(manifest),
            "--comparison-dir",
            str(tmp_path / "comparison"),
            "--report-dir",
            str(tmp_path / "report"),
            "--out",
            str(output_path),
            "--expected-models",
            "1",
        ],
        cwd=Path(__file__).parents[2],
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0
    assert "Wrote final result artifact audit" in result.stdout
    assert output_path.exists()
