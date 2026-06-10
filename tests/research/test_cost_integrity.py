from __future__ import annotations

import csv
import subprocess
import sys
from pathlib import Path

from obviousbench.research.cost_integrity import (
    CostIntegrityInputs,
    audit_cost_integrity,
)


def _write_csv(path: Path, fieldnames: tuple[str, ...], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


COMPARISON_FIELDS = (
    "label",
    "model",
    "scored_samples",
    "provider_errors",
    "timeouts",
    "total_tokens",
    "estimated_cost_usd",
    "cost_source",
    "cost_warnings",
)


def test_cost_integrity_audit_passes_clean_cumulative_repair(tmp_path: Path):
    comparison = tmp_path / "comparison.csv"
    selection = tmp_path / "selection-audit.csv"
    _write_csv(
        comparison,
        COMPARISON_FIELDS,
        [
            {
                "label": "Clean Model",
                "model": "openrouter/test/model",
                "scored_samples": "224",
                "provider_errors": "0",
                "timeouts": "0",
                "total_tokens": "10000",
                "estimated_cost_usd": "0.01",
                "cost_source": "cumulative_attempts:base+repair1",
                "cost_warnings": "",
            }
        ],
    )
    _write_csv(
        selection,
        ("label", "selected_source", "summary_dir"),
        [
            {
                "label": "Clean Model",
                "selected_source": "repair1",
                "summary_dir": "results/final/cumulative-cost-runs/model",
            }
        ],
    )

    result = audit_cost_integrity(
        CostIntegrityInputs(
            comparison_path=comparison,
            selection_audit_path=selection,
            output_path=tmp_path / "audit.md",
        )
    )

    assert result.ok
    assert result.findings == []
    assert "Overall status: PASS" in (tmp_path / "audit.md").read_text(encoding="utf-8")


def test_cost_integrity_audit_flags_successful_zero_usage(tmp_path: Path):
    comparison = tmp_path / "comparison.csv"
    _write_csv(
        comparison,
        COMPARISON_FIELDS,
        [
            {
                "label": "Missing Usage",
                "model": "openrouter/test/model",
                "scored_samples": "224",
                "provider_errors": "0",
                "timeouts": "0",
                "total_tokens": "0",
                "estimated_cost_usd": "0",
                "cost_source": "runcost",
                "cost_warnings": "",
            }
        ],
    )

    result = audit_cost_integrity(CostIntegrityInputs(comparison_path=comparison))

    assert not result.ok
    assert result.findings[0].check == "missing_usage_telemetry"


def test_cost_integrity_audit_flags_repair_source_without_cumulative_cost(tmp_path: Path):
    comparison = tmp_path / "comparison.csv"
    selection = tmp_path / "selection-audit.csv"
    _write_csv(
        comparison,
        COMPARISON_FIELDS,
        [
            {
                "label": "Repair Model",
                "model": "openrouter/test/model",
                "scored_samples": "224",
                "provider_errors": "0",
                "timeouts": "0",
                "total_tokens": "10000",
                "estimated_cost_usd": "0.01",
                "cost_source": "runcost",
                "cost_warnings": "",
            }
        ],
    )
    _write_csv(
        selection,
        ("label", "selected_source", "summary_dir"),
        [
            {
                "label": "Repair Model",
                "selected_source": "repair1",
                "summary_dir": "results/summaries/repair/runs/model",
            }
        ],
    )

    result = audit_cost_integrity(
        CostIntegrityInputs(comparison_path=comparison, selection_audit_path=selection)
    )

    assert not result.ok
    assert [finding.check for finding in result.findings] == ["repair_source_not_cumulative"]


def test_cost_integrity_audit_allows_telemetry_rerun_source(tmp_path: Path):
    comparison = tmp_path / "comparison.csv"
    selection = tmp_path / "selection-audit.csv"
    _write_csv(
        comparison,
        COMPARISON_FIELDS,
        [
            {
                "label": "Telemetry Model",
                "model": "openrouter/test/model",
                "scored_samples": "224",
                "provider_errors": "0",
                "timeouts": "0",
                "total_tokens": "10000",
                "estimated_cost_usd": "0.01",
                "cost_source": "runcost",
                "cost_warnings": "",
            }
        ],
    )
    _write_csv(
        selection,
        ("label", "selected_source", "summary_dir"),
        [
            {
                "label": "Telemetry Model",
                "selected_source": "telemetry_rerun",
                "summary_dir": "results/summaries/telemetry-rerun/runs/model",
            }
        ],
    )

    result = audit_cost_integrity(
        CostIntegrityInputs(comparison_path=comparison, selection_audit_path=selection)
    )

    assert result.ok


def test_cost_integrity_script_writes_report(tmp_path: Path):
    comparison = tmp_path / "comparison.csv"
    output_path = tmp_path / "audit.md"
    _write_csv(
        comparison,
        COMPARISON_FIELDS,
        [
            {
                "label": "Missing Usage",
                "model": "openrouter/test/model",
                "scored_samples": "224",
                "provider_errors": "0",
                "timeouts": "0",
                "total_tokens": "0",
                "estimated_cost_usd": "0",
                "cost_source": "runcost",
                "cost_warnings": "",
            }
        ],
    )

    result = subprocess.run(
        [
            sys.executable,
            "scripts/audit_cost_integrity.py",
            "--comparison",
            str(comparison),
            "--selection-audit",
            "",
            "--out",
            str(output_path),
        ],
        cwd=Path(__file__).parents[2],
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0
    assert "BLOCKED, 1 finding(s)" in result.stdout
    assert "missing_usage_telemetry" in output_path.read_text(encoding="utf-8")
