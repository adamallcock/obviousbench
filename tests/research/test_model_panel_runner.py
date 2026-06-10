from __future__ import annotations

import csv
import json
import subprocess
import sys
from pathlib import Path

import yaml

from obviousbench.research.model_panel_runner import (
    ModelPanelRunInputs,
    _generation_settings,
    _select_entries,
    run_model_panel,
)


def _write_panel(path: Path) -> None:
    path.write_text(
        yaml.safe_dump(
            {
                "schema_version": "unit-model-panel-v1",
                "run_status": "planned_not_run",
                "defaults": {
                    "inspect_args": ["--no-log-model-api", "--no-log-realtime"],
                    "generation_settings": {
                        "temperature": 0,
                        "max_tokens": 64,
                    },
                },
                "entries": [
                    {
                        "id": "entry-complete",
                        "label": "Complete Model",
                        "provider_route": "openai",
                        "inspect_model": "openai/complete",
                        "generation_settings": {
                            "reasoning_effort": "minimal",
                        },
                        "run_status": "planned",
                    },
                    {
                        "id": "entry-new",
                        "label": "New Model",
                        "provider_route": "anthropic",
                        "inspect_model": "anthropic/new",
                        "reasoning_effort": "high",
                        "run_status": "planned",
                    },
                ],
            },
            sort_keys=False,
        ),
        encoding="utf-8",
    )


def _write_dataset(path: Path, *, sample_count: int = 1) -> None:
    path.write_text(
        "".join(
            f'{{"id":"sample-{index}","input":"x","target":"y"}}\n'
            for index in range(sample_count)
        ),
        encoding="utf-8",
    )


def _inputs(tmp_path: Path, *, dry_run: bool = False) -> ModelPanelRunInputs:
    panel_path = tmp_path / "panel.yaml"
    dataset_path = tmp_path / "dataset.jsonl"
    _write_panel(panel_path)
    _write_dataset(dataset_path)
    return ModelPanelRunInputs(
        panel_path=panel_path,
        dataset_path=dataset_path,
        raw_root=tmp_path / "raw",
        summary_root=tmp_path / "summaries",
        manifest_out=tmp_path / "manifest.csv",
        status_out=tmp_path / "status.jsonl",
        mode="smoke",
        smoke_sample_ids=("sample-a",),
        dry_run=dry_run,
    )


def test_model_panel_runner_dry_run_writes_manifest_and_status(tmp_path: Path):
    inputs = _inputs(tmp_path, dry_run=True)

    result = run_model_panel(
        inputs,
        inspect_runner=lambda config: (_ for _ in ()).throw(AssertionError("called")),
    )

    assert result.ok
    status_rows = [
        json.loads(line) for line in inputs.status_out.read_text(encoding="utf-8").splitlines()
    ]
    assert [row["status"] for row in status_rows] == ["dry_run", "dry_run"]
    assert "--sample-id sample-a" in status_rows[0]["inspect_command"]
    assert "--generate-config" in status_rows[0]["inspect_command"]
    assert "reasoning_effort" in status_rows[0]["generation_settings"]

    manifest_rows = list(csv.DictReader(inputs.manifest_out.open(encoding="utf-8")))
    assert manifest_rows == [
        {
            "label": "Complete Model",
            "model": "openai/complete",
            "summary_dir": str(tmp_path / "summaries" / "entry-complete"),
        },
        {
            "label": "New Model",
            "model": "anthropic/new",
            "summary_dir": str(tmp_path / "summaries" / "entry-new"),
        },
    ]


def test_model_panel_runner_translates_anthropic_adaptive_effort(tmp_path: Path):
    panel_path = tmp_path / "panel.yaml"
    dataset_path = tmp_path / "dataset.jsonl"
    panel_path.write_text(
        yaml.safe_dump(
            {
                "schema_version": "unit-model-panel-v1",
                "defaults": {
                    "generation_settings": {
                        "max_tokens": 2000,
                        "seed": 20260531,
                    },
                },
                "entries": [
                    {
                        "id": "anthropic-adaptive",
                        "label": "Claude Sonnet 4.6 max",
                        "provider_route": "anthropic",
                        "inspect_model": "anthropic/claude-sonnet-4-6",
                        "control_style": "anthropic_adaptive_thinking_effort",
                        "generation_settings": {
                            "effort": "max",
                        },
                        "provider_request_settings": {
                            "thinking": {"type": "adaptive"},
                            "output_config": {"effort": "max"},
                        },
                        "run_status": "planned",
                    }
                ],
            },
            sort_keys=False,
        ),
        encoding="utf-8",
    )
    _write_dataset(dataset_path)
    inputs = ModelPanelRunInputs(
        panel_path=panel_path,
        dataset_path=dataset_path,
        raw_root=tmp_path / "raw",
        summary_root=tmp_path / "summaries",
        manifest_out=tmp_path / "manifest.csv",
        status_out=tmp_path / "status.jsonl",
        mode="smoke",
        smoke_sample_ids=("sample-a",),
        dry_run=True,
    )

    result = run_model_panel(inputs)

    assert result.ok
    assert result.rows[0].generation_settings == {
        "max_tokens": 2000,
        "reasoning_effort": "max",
        "seed": 20260531,
    }
    generate_configs = list((tmp_path / "raw" / "anthropic-adaptive").glob("*.json"))
    assert len(generate_configs) == 1
    assert json.loads(generate_configs[0].read_text(encoding="utf-8")) == {
        "max_tokens": 2000,
        "reasoning_effort": "max",
        "seed": 20260531,
    }


def test_generation_settings_enables_thinking_when_control_style_dropped():
    # Panels reconstructed from comparison/leaderboard CSVs lose control_style;
    # a bare anthropic effort entry must still translate to reasoning_effort so
    # extended thinking is not silently disabled (the expand222 regression).
    entry = {
        "id": "expand222-top-thinking-015-anthropic-claude-opus-4-8-max",
        "inspect_model": "anthropic/claude-opus-4-8",
        "control_style": None,
        "generation_settings": {"effort": "max", "max_tokens": 32840},
    }
    settings = _generation_settings(entry, defaults={})
    assert settings.get("reasoning_effort") == "max"
    assert "effort" not in settings


def test_select_entries_restores_anthropic_control_style_when_dropped():
    entries = [
        {
            "id": "expand222-top-thinking-015-anthropic-claude-opus-4-8-max",
            "inspect_model": "anthropic/claude-opus-4-8",
            "generation_settings": {"effort": "max", "max_tokens": 32840},
            "run_status": "planned",
        },
        {
            "id": "expand222-paper-anthropic-claude-sonnet-4-6",
            "inspect_model": "anthropic/claude-sonnet-4-6",
            "generation_settings": {"max_tokens": 64, "temperature": 0},
            "run_status": "planned",
        },
    ]

    selected = _select_entries(entries, only=(), limit=None)

    assert selected[0]["control_style"] == "anthropic_adaptive_thinking_effort"
    assert "control_style" not in selected[1]
    assert "control_style" not in entries[0]


def test_generation_settings_leaves_effortless_anthropic_default_thinking_off():
    # No-effort baseline entries (provider default) must stay thinking-off:
    # there is no effort to rename, so no reasoning_effort is added.
    entry = {
        "id": "expand222-paper-anthropic-claude-sonnet-4-6",
        "inspect_model": "anthropic/claude-sonnet-4-6",
        "control_style": None,
        "generation_settings": {"max_tokens": 64, "temperature": 0},
    }
    settings = _generation_settings(entry, defaults={})
    assert "reasoning_effort" not in settings
    assert "effort" not in settings


def test_model_panel_runner_skips_completed_and_executes_remaining(tmp_path: Path):
    inputs = _inputs(tmp_path)
    completed_summary = tmp_path / "summaries" / "entry-complete" / "summary.csv"
    completed_summary.parent.mkdir(parents=True)
    completed_summary.write_text(
        "model,total_samples,scored_samples,provider_errors\nopenai/complete,1,1,0\n",
        encoding="utf-8",
    )
    inspect_calls = []
    rescore_calls = []

    def fake_inspect_runner(config):
        inspect_calls.append(config)
        return 0

    def fake_rescore_runner(log_dir: Path, summary_dir: Path, cost: str) -> int:
        rescore_calls.append((log_dir, summary_dir, cost))
        summary_dir.mkdir(parents=True, exist_ok=True)
        (summary_dir / "summary.csv").write_text(
            "model,total_samples,scored_samples,provider_errors\nanthropic/new,1,1,0\n",
            encoding="utf-8",
        )
        return 0

    result = run_model_panel(
        inputs,
        inspect_runner=fake_inspect_runner,
        rescore_runner=fake_rescore_runner,
    )

    assert result.ok
    assert [row.status for row in result.rows] == ["skipped_completed", "passed"]
    assert len(inspect_calls) == 1
    assert inspect_calls[0].sample_ids == ("sample-a",)
    assert inspect_calls[0].generation_settings["reasoning_effort"] == "high"
    assert rescore_calls == [
        (
            tmp_path / "raw" / "entry-new",
            tmp_path / "summaries" / "entry-new",
            "runcost",
        )
    ]


def test_model_panel_runner_does_not_skip_partial_full_summary(tmp_path: Path):
    inputs = _inputs(tmp_path)
    _write_dataset(inputs.dataset_path, sample_count=2)
    inputs = ModelPanelRunInputs(
        panel_path=inputs.panel_path,
        dataset_path=inputs.dataset_path,
        raw_root=inputs.raw_root,
        summary_root=inputs.summary_root,
        manifest_out=inputs.manifest_out,
        status_out=inputs.status_out,
        mode="full",
    )
    partial_summary = tmp_path / "summaries" / "entry-complete" / "summary.csv"
    partial_summary.parent.mkdir(parents=True)
    partial_summary.write_text(
        "model,total_samples,scored_samples,provider_errors\nopenai/complete,1,1,0\n",
        encoding="utf-8",
    )
    inspect_calls = []

    def fake_inspect_runner(config):
        inspect_calls.append(config)
        return 0

    def fake_rescore_runner(log_dir: Path, summary_dir: Path, cost: str) -> int:
        summary_dir.mkdir(parents=True, exist_ok=True)
        (summary_dir / "summary.csv").write_text(
            "model,total_samples,scored_samples,provider_errors\n"
            f"{summary_dir.name},2,2,0\n",
            encoding="utf-8",
        )
        return 0

    result = run_model_panel(
        inputs,
        inspect_runner=fake_inspect_runner,
        rescore_runner=fake_rescore_runner,
    )

    assert result.ok
    assert result.rows[0].status == "passed"
    assert len(inspect_calls) == 2
    assert all(call.sample_ids == () for call in inspect_calls)


def test_model_panel_runner_fails_partial_full_summary_after_rescore(tmp_path: Path):
    inputs = _inputs(tmp_path)
    _write_dataset(inputs.dataset_path, sample_count=2)
    inputs = ModelPanelRunInputs(
        panel_path=inputs.panel_path,
        dataset_path=inputs.dataset_path,
        raw_root=inputs.raw_root,
        summary_root=inputs.summary_root,
        manifest_out=inputs.manifest_out,
        status_out=inputs.status_out,
        mode="full",
    )

    def fake_inspect_runner(config):
        return 0

    def fake_rescore_runner(log_dir: Path, summary_dir: Path, cost: str) -> int:
        summary_dir.mkdir(parents=True, exist_ok=True)
        (summary_dir / "summary.csv").write_text(
            "model,total_samples,scored_samples,provider_errors\n"
            f"{summary_dir.name},1,1,0\n",
            encoding="utf-8",
        )
        return 0

    result = run_model_panel(
        inputs,
        inspect_runner=fake_inspect_runner,
        rescore_runner=fake_rescore_runner,
    )

    assert not result.ok
    assert result.rows[0].status == "failed_summary_validation"
    assert "expected 2 scored samples" in result.rows[0].error


def test_model_panel_runner_fails_zero_scored_smoke_summary(tmp_path: Path):
    inputs = _inputs(tmp_path)

    def fake_inspect_runner(config):
        return 0

    def fake_rescore_runner(log_dir: Path, summary_dir: Path, cost: str) -> int:
        summary_dir.mkdir(parents=True, exist_ok=True)
        (summary_dir / "summary.csv").write_text(
            (
                "model,total_samples,scored_samples,provider_errors\n"
                "anthropic/new,1,0,1\n"
            ),
            encoding="utf-8",
        )
        return 0

    result = run_model_panel(
        inputs,
        inspect_runner=fake_inspect_runner,
        rescore_runner=fake_rescore_runner,
    )

    assert not result.ok
    assert result.rows[0].status == "failed_summary_validation"
    assert "scored 0/1 samples" in result.rows[0].error


def test_model_panel_runner_absolutizes_dataset_path(tmp_path: Path):
    panel_path = tmp_path / "panel.yaml"
    _write_panel(panel_path)
    inputs = ModelPanelRunInputs(
        panel_path=panel_path,
        dataset_path=Path("relative_dataset.jsonl"),
        raw_root=tmp_path / "raw",
        summary_root=tmp_path / "summaries",
        manifest_out=tmp_path / "manifest.csv",
        status_out=tmp_path / "status.jsonl",
        mode="smoke",
        smoke_sample_ids=("sample-a",),
        dry_run=True,
        limit=1,
    )

    result = run_model_panel(inputs)

    assert result.ok
    assert f"dataset={Path('relative_dataset.jsonl').resolve()}" in result.rows[
        0
    ].inspect_command


def test_run_model_panel_script_supports_dry_run(tmp_path: Path):
    panel_path = tmp_path / "panel.yaml"
    dataset_path = tmp_path / "dataset.jsonl"
    _write_panel(panel_path)
    _write_dataset(dataset_path)

    result = subprocess.run(
        [
            sys.executable,
            "scripts/run_model_panel.py",
            "--panel",
            str(panel_path),
            "--dataset",
            str(dataset_path),
            "--raw-root",
            str(tmp_path / "raw"),
            "--summary-root",
            str(tmp_path / "summaries"),
            "--manifest-out",
            str(tmp_path / "manifest.csv"),
            "--status-out",
            str(tmp_path / "status.jsonl"),
            "--mode",
            "smoke",
            "--sample-id",
            "sample-a",
            "--dry-run",
        ],
        cwd=Path(__file__).parents[2],
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert "Wrote run status" in result.stdout
    assert (tmp_path / "manifest.csv").exists()
    assert (tmp_path / "status.jsonl").exists()
