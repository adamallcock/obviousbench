from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import yaml

from obviousbench.research.paper_analysis_plan import (
    PaperAnalysisPlanInputs,
    build_paper_analysis_plan,
)


def _valid_plan() -> dict:
    return {
        "schema_version": "paper-analysis-plan-v1",
        "created_at": "2026-06-01",
        "status": "frozen_before_final_sweep",
        "applies_to": "paper_v1",
        "no_provider_calls": True,
        "analysis_freeze": {
            "frozen_before_final_sweep": True,
            "post_hoc_policy": ["Label exploratory slices."],
        },
        "primary_question": "How often do models fail obvious tasks?",
        "inputs": {
            "dataset_manifest": "data/splits/paper_v1_manifest.jsonl",
            "model_panel": "configs/paper_v1_model_panel.yaml",
            "human_baseline": "data/human_baseline/paper_v1.csv",
            "final_comparison_dir": "results/summaries/paper-v1-final-high-cap/comparison",
            "final_report_dir": "docs/reports/2026-06-01-paper-v1-final-high-cap-sweep",
            "scoring_gold_dir": "tests/fixtures/scorer_gold",
        },
        "primary_metrics": [
            {
                "id": "answer_accuracy",
                "label": "Answer correctness",
                "numerator": "answer_correct",
                "denominator": "scored_samples",
                "source_column": "answer_accuracy",
                "interval": "wilson_95",
                "paper_role": "Primary metric.",
            },
        ],
        "secondary_metrics": [
            {
                "id": "strict_accuracy",
                "label": "Strict accuracy",
                "source_column": "strict_accuracy",
                "interpretation": "Compliance diagnostic.",
            },
            {
                "id": "format_accuracy",
                "label": "Format accuracy",
                "source_column": "format_accuracy",
                "interpretation": "Format diagnostic.",
            },
            {
                "id": "tokens_per_correct",
                "label": "Tokens per correct",
                "source_column": "tokens_per_correct",
                "interpretation": "Efficiency.",
            }
        ],
        "intervals": {
            "binomial": {
                "method": "Wilson score interval",
                "implementation": "obviousbench.analysis.statistics.wilson_interval",
            },
            "paired_deltas": {
                "method": "deterministic percentile bootstrap over matched item IDs",
                "implementation": "obviousbench.analysis.statistics.paired_boolean_delta",
                "seed": 20260531,
            },
        },
        "stratification": {"required": ["task_family"], "optional": ["subfamily"]},
        "reported_tables": [
            {
                "id": "main_results",
                "path": "paper/tables/main_results.tex",
                "source": "final comparison",
                "status_before_sweep": "placeholder",
            }
        ],
        "reported_figures": [
            {
                "id": "leaderboard",
                "path": "paper/figures/leaderboard.pdf",
                "source": "final comparison",
                "status_before_sweep": "placeholder",
            }
        ],
        "exclusion_policy": {"provider_errors": "Report separately."},
        "human_baseline_policy": {"minimum_participants": 5},
        "claim_policy": {
            "reporting_vs_hypothesis_generation": "Mostly reporting.",
            "solution_policy": "Secondary.",
            "ranking_policy": "Visible intervals.",
            "release_policy": "Artifact-backed.",
        },
    }


def test_analysis_plan_renders_valid_plan(tmp_path: Path):
    plan_path = tmp_path / "analysis-plan.yaml"
    output_path = tmp_path / "analysis-plan.md"
    plan_path.write_text(yaml.safe_dump(_valid_plan()), encoding="utf-8")

    result = build_paper_analysis_plan(
        PaperAnalysisPlanInputs(plan_path=plan_path, output_path=output_path)
    )

    assert result.ok
    assert result.primary_metric_count == 1
    text = output_path.read_text(encoding="utf-8")
    assert "Overall status: PASS" in text
    assert "Answer correctness" in text
    assert "obviousbench.analysis.statistics.wilson_interval" in text


def test_analysis_plan_blocks_missing_required_policy(tmp_path: Path):
    plan = _valid_plan()
    del plan["claim_policy"]["release_policy"]
    plan_path = tmp_path / "analysis-plan.yaml"
    output_path = tmp_path / "analysis-plan.md"
    plan_path.write_text(yaml.safe_dump(plan), encoding="utf-8")

    result = build_paper_analysis_plan(
        PaperAnalysisPlanInputs(plan_path=plan_path, output_path=output_path)
    )

    assert not result.ok
    assert "claim_policy.release_policy is required" in result.issues
    assert "Overall status: BLOCKED" in output_path.read_text(encoding="utf-8")


def test_real_paper_v1_analysis_plan_is_valid():
    result = build_paper_analysis_plan(
        PaperAnalysisPlanInputs(
            plan_path=Path("configs/paper_v1_analysis_plan.yaml"),
            output_path=Path("/tmp/obviousbench-paper-analysis-plan-test.md"),
        )
    )

    assert result.ok
    assert result.primary_metric_count == 1
    assert result.figure_count == 4
    reported_table_ids = {row["id"] for row in result.plan["reported_tables"]}
    audit_artifact_ids = {row["id"] for row in result.plan["audit_artifacts"]}
    assert "provider_exclusions" not in reported_table_ids
    assert "provider_exclusions" in audit_artifact_ids


def test_analysis_plan_script_writes_report(tmp_path: Path):
    plan_path = tmp_path / "analysis-plan.yaml"
    output_path = tmp_path / "analysis-plan.md"
    plan_path.write_text(yaml.safe_dump(_valid_plan()), encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "scripts/build_paper_analysis_plan.py",
            "--plan",
            str(plan_path),
            "--out",
            str(output_path),
        ],
        cwd=Path(__file__).parents[2],
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0
    assert "Wrote paper analysis plan" in result.stdout
    assert output_path.exists()
