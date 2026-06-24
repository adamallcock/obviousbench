"""Tests for v0.2 local release asset generation."""

from __future__ import annotations

import csv
import json
from pathlib import Path

import yaml

from scripts.release.build_v0_2_release_assets import build_release_assets


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def _write_yaml(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")


def test_build_v0_2_release_assets_writes_public_safe_surfaces(tmp_path: Path) -> None:
    summary_csv = tmp_path / "reports/summary.csv"
    _write_csv(
        summary_csv,
        [
            {
                "answer_pass3_accuracy": "1.0",
                "complete_for_pass3": "True",
                "estimated_cost_usd": "0.25",
                "model_entry_id": "top",
                "provider_errors": "0",
                "provider_model": "openai/gpt-test",
                "reasoning_effort": "high",
                "reasoning_tokens": "120",
                "strict_pass3_accuracy": "1.0",
            },
            {
                "answer_pass3_accuracy": "0.25",
                "complete_for_pass3": "True",
                "estimated_cost_usd": "0.01",
                "model_entry_id": "small",
                "provider_errors": "0",
                "provider_model": "small/model",
                "reasoning_effort": "none",
                "reasoning_tokens": "0",
                "strict_pass3_accuracy": "0.2",
            },
        ],
    )
    report_summary = tmp_path / "reports/build_summary.json"
    review_summary = tmp_path / "reports/review_summary.json"
    _write_json(
        report_summary,
        {
            "attempt_rows": 864,
            "blank_provider_fault_attempt_rows": 3,
            "manual_adjusted_attempt_rows": 3,
            "summary_rows": 2,
        },
    )
    _write_json(
        review_summary,
        {
            "question_failure_review_data_mode": "split",
            "raw_hydrated_attempts": 4,
        },
    )
    out_dir = tmp_path / "docs/release/v0_2/generated"
    internal_dir = tmp_path / "docs/internal/release/v0_2/generated"
    config = tmp_path / "configs/releases/release_v0_2_0.yaml"
    _write_yaml(
        config,
        {
            "claim_limits": {"caveats": [], "summary": "test"},
            "generated": {
                "internal_output_dir": str(internal_dir),
                "output_dir": str(out_dir),
            },
            "public_links": {},
            "public_safety": {
                "bundle_policy": "aggregate_private_results_plus_public_examples",
                "private_prompts_in_public_bundle": False,
                "private_raw_logs_in_public_bundle": False,
                "private_review_html_in_public_bundle": False,
                "private_row_level_outcomes_in_public_bundle": False,
            },
            "release": {
                "date": "2026-06-15",
                "id": "test",
                "publication_intent": "non_arxiv_public_release",
                "status": "local-publication-prep",
                "version": "0.2.0",
            },
            "snapshot": {
                "name": "test-snapshot",
                "private_item_count": 144,
                "primary_metric": "answer_pass3",
                "primary_metric_label": "non-strict answer pass^3",
                "report_markdown": "reports/report.md",
                "report_summary": str(report_summary),
                "summary_csv": str(summary_csv),
                "review_summary": str(review_summary),
            },
            "source_docs": {
                "evidence_packet": "docs/research/evidence.md",
                "results_memo": "docs/research/results.md",
                "sanity_supplement": "docs/research/sanity.md",
            },
        },
    )

    result = build_release_assets(config_path=config)

    assert result.output_dir == out_dir
    assert (out_dir / "README.md").exists()
    readme = (out_dir / "README.md").read_text(encoding="utf-8")
    assert "## Generated Artifact Notice" in readme
    assert "Source config:" in readme
    assert "https://obviousbench.com" in readme
    assert "project-page.md" not in readme
    assert "launch-essay-draft.md" not in readme
    assert not (out_dir / "project-page.md").exists()
    assert not (out_dir / "launch-essay-draft.md").exists()
    assert not (out_dir / "background-and-rhetoric.md").exists()
    assert not (out_dir / "social-snippets.md").exists()
    assert not (out_dir / "public-release-checklist.md").exists()
    metadata = json.loads((out_dir / "release-metadata.json").read_text(encoding="utf-8"))
    assert metadata["version"] == "0.2.0"
    provenance = json.loads((out_dir / "provenance.json").read_text(encoding="utf-8"))
    assert "report_summary" not in provenance
    assert "summary_csv" not in provenance
    evidence = json.loads((internal_dir / "release-evidence.json").read_text(encoding="utf-8"))
    assert evidence["summary"]["model_setting_rows"] == 2
    assert evidence["summary"]["scored_attempts"] == 864
    assert evidence["summary"]["provider_error_attempts"] == 0
    assert evidence["summary"]["manual_adjusted_attempts"] == 3
    assert evidence["summary"]["blank_provider_fault_attempts"] == 3
    assert evidence["top_saturated_rows"][0]["provider_model"] == "openai/gpt-test"
