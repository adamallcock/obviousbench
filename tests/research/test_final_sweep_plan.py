from __future__ import annotations

import csv
import subprocess
import sys
from pathlib import Path
from typing import Literal

import yaml

from obviousbench.research.final_sweep_plan import (
    FinalSweepPlanInputs,
    build_final_sweep_plan,
)
from tests.datasets.test_schemas import valid_record
from tests.research.test_arxiv_readiness import _write_card, _write_gold, _write_jsonl


def _write_panel(path: Path) -> None:
    path.write_text(
        yaml.safe_dump(
            {
                "schema_version": "paper-model-panel-v1",
                "run_status": "planned_not_run",
                "profile": "hard_obvious_8x10",
                "seed": 20260531,
                "defaults": {
                    "temperature": 0,
                    "max_tokens": 64,
                    "inspect_args": ["--no-log-model-api", "--no-log-realtime"],
                },
                "entries": [
                    {
                        "id": "paper-unit",
                        "label": "Unit Model",
                        "provider_route": "openai",
                        "inspect_model": "openai/unit",
                        "temperature": 0,
                        "max_tokens": 64,
                        "reasoning_effort": "minimal",
                        "run_status": "planned",
                    }
                ],
            },
            sort_keys=False,
        ),
        encoding="utf-8",
    )


def _write_smoke_status(path: Path, *, status: str = "ready") -> None:
    path.write_text(
        "\n".join(
            [
                "---",
                "title: Paper V1 Smoke Status",
                "date: 2026-06-01",
                "type: research",
                f"status: {status}",
                "---",
                "",
                "# Paper V1 Smoke Status",
                "",
            ]
        ),
        encoding="utf-8",
    )


def _fixture(tmp_path: Path, *, human_rows: bool) -> dict[str, Path]:
    dataset_path = tmp_path / "paper_items.jsonl"
    manifest_path = tmp_path / "paper_v1_manifest.jsonl"
    cards_dir = tmp_path / "item_cards"
    gold_dir = tmp_path / "scorer_gold"
    human_baseline = tmp_path / "human_baseline.csv"
    panel_path = tmp_path / "panel.yaml"
    cost_estimates = tmp_path / "costs.md"
    smoke_status = tmp_path / "smoke-status.md"
    _write_jsonl(dataset_path, [valid_record()])
    manifest_path.write_text(
        '{"item_id":"obviousbench.char_count.en.v0.public.000001"}\n',
        encoding="utf-8",
    )
    _write_card(cards_dir)
    _write_gold(gold_dir)
    human_baseline.write_text(
        (
            "item_id,participant_id,answer,seconds,correct,notes\n"
            "obviousbench.char_count.en.v0.public.000001,p1,3,2.4,true,\n"
        )
        if human_rows
        else "item_id,participant_id,answer,seconds,correct,notes\n",
        encoding="utf-8",
    )
    _write_panel(panel_path)
    cost_estimates.write_text("# Costs\n", encoding="utf-8")
    _write_smoke_status(smoke_status)
    return {
        "dataset_path": dataset_path,
        "manifest_path": manifest_path,
        "cards_dir": cards_dir,
        "gold_dir": gold_dir,
        "human_baseline": human_baseline,
        "panel_path": panel_path,
        "cost_estimates": cost_estimates,
        "smoke_status": smoke_status,
    }


def _inputs(
    fixture: dict[str, Path],
    output_path: Path,
    *,
    readiness_profile: Literal["strict", "preprint"] = "preprint",
) -> FinalSweepPlanInputs:
    return FinalSweepPlanInputs(
        panel_path=fixture["panel_path"],
        dataset_path=fixture["dataset_path"],
        paper_manifest_path=fixture["manifest_path"],
        item_cards_dir=fixture["cards_dir"],
        scorer_gold_dir=fixture["gold_dir"],
        human_baseline_path=fixture["human_baseline"],
        cost_estimates_path=fixture["cost_estimates"],
        output_path=output_path,
        comparison_manifest_path=output_path.parent / "comparison-manifest.csv",
        smoke_status_path=fixture["smoke_status"],
        raw_root=output_path.parent / "raw",
        summary_root=output_path.parent / "summaries",
        comparison_dir=output_path.parent / "comparison",
        report_dir=output_path.parent / "report",
        min_gold_examples_per_scorer=2,
        min_human_participants=1,
        generated_on="2026-06-01",
        readiness_profile=readiness_profile,
    )


def test_final_sweep_plan_strict_profile_blocks_without_human_rows(tmp_path: Path):
    fixture = _fixture(tmp_path, human_rows=False)
    output_path = tmp_path / "final-sweep-plan.md"

    result = build_final_sweep_plan(
        _inputs(fixture, output_path, readiness_profile="strict")
    )

    assert not result.run_allowed
    assert result.command_count == 1
    assert any("human baseline" in blocker for blocker in result.blockers)
    text = output_path.read_text(encoding="utf-8")
    assert "Run allowed: NO" in text
    assert "openai/unit" in text
    assert "--generation-setting reasoning_effort=minimal" in text
    assert "-T dataset=" in text
    manifest_rows = list(
        csv.DictReader(result.comparison_manifest_path.open(encoding="utf-8"))
    )
    assert manifest_rows == [
        {
            "label": "Unit Model",
            "model": "openai/unit",
            "summary_dir": str(tmp_path / "summaries" / "paper-unit"),
        }
    ]


def test_final_sweep_plan_allows_run_when_readiness_and_costs_pass(tmp_path: Path):
    fixture = _fixture(tmp_path, human_rows=True)

    result = build_final_sweep_plan(_inputs(fixture, tmp_path / "plan.md"))

    assert result.run_allowed
    assert result.blockers == ()


def test_final_sweep_plan_blocks_on_blocked_smoke_status(tmp_path: Path):
    fixture = _fixture(tmp_path, human_rows=True)
    _write_smoke_status(fixture["smoke_status"], status="blocked")

    result = build_final_sweep_plan(_inputs(fixture, tmp_path / "plan.md"))

    assert not result.run_allowed
    assert any("smoke status is not accepted" in blocker for blocker in result.blockers)
    assert "Run allowed: NO" in (tmp_path / "plan.md").read_text(encoding="utf-8")


def test_build_final_sweep_plan_script_writes_outputs(tmp_path: Path):
    fixture = _fixture(tmp_path, human_rows=False)
    output_path = tmp_path / "final-sweep-plan.md"
    comparison_manifest = tmp_path / "comparison-manifest.csv"

    result = subprocess.run(
        [
            sys.executable,
            "scripts/build_final_sweep_plan.py",
            "--panel",
            str(fixture["panel_path"]),
            "--dataset",
            str(fixture["dataset_path"]),
            "--paper-manifest",
            str(fixture["manifest_path"]),
            "--item-cards-dir",
            str(fixture["cards_dir"]),
            "--scorer-gold-dir",
            str(fixture["gold_dir"]),
            "--human-baseline",
            str(fixture["human_baseline"]),
            "--cost-estimates",
            str(fixture["cost_estimates"]),
            "--out",
            str(output_path),
            "--comparison-manifest",
            str(comparison_manifest),
            "--smoke-status",
            str(fixture["smoke_status"]),
            "--min-gold-examples-per-scorer",
            "2",
            "--min-human-participants",
            "1",
            "--readiness-profile",
            "strict",
        ],
        cwd=Path(__file__).parents[2],
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0
    assert "Wrote final sweep plan" in result.stdout
    assert "Run allowed: NO" in output_path.read_text(encoding="utf-8")
    assert comparison_manifest.exists()


def test_final_sweep_plan_script_defaults_to_preprint_profile(tmp_path: Path):
    fixture = _fixture(tmp_path, human_rows=False)
    output_path = tmp_path / "final-sweep-plan.md"
    comparison_manifest = tmp_path / "comparison-manifest.csv"

    result = subprocess.run(
        [
            sys.executable,
            "scripts/build_final_sweep_plan.py",
            "--panel",
            str(fixture["panel_path"]),
            "--dataset",
            str(fixture["dataset_path"]),
            "--paper-manifest",
            str(fixture["manifest_path"]),
            "--item-cards-dir",
            str(fixture["cards_dir"]),
            "--scorer-gold-dir",
            str(fixture["gold_dir"]),
            "--human-baseline",
            str(fixture["human_baseline"]),
            "--cost-estimates",
            str(fixture["cost_estimates"]),
            "--out",
            str(output_path),
            "--comparison-manifest",
            str(comparison_manifest),
            "--smoke-status",
            str(fixture["smoke_status"]),
            "--min-gold-examples-per-scorer",
            "2",
            "--min-human-participants",
            "1",
        ],
        cwd=Path(__file__).parents[2],
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0
    text = output_path.read_text(encoding="utf-8")
    assert "Readiness profile: `preprint`" in text
    assert "Run allowed: YES" in text
