import json
from pathlib import Path
from types import SimpleNamespace

import obviousbench.runners.inspect_eval as inspect_eval
from obviousbench.runners.inspect_eval import (
    InspectEvalConfig,
    build_inspect_eval_command,
    inspect_eval_env,
    parse_args,
    run_inspect_eval,
)


def test_generic_runner_adds_cache_by_default(tmp_path):
    config = InspectEvalConfig(
        task="obviousbench/tasks/barrage.py",
        model="openai/gpt-5.4",
        log_dir=tmp_path / "logs",
        task_args=("profile=hard_obvious_8x10", "seed=20260531"),
        inspect_args=("--no-log-model-api",),
        cache_dir=tmp_path / "cache",
    )

    command = build_inspect_eval_command(config)

    assert "--cache" in command
    assert command[command.index("--cache") + 1] == "10Y"
    assert command[command.index("-T") : command.index("-T") + 2] == [
        "-T",
        "profile=hard_obvious_8x10",
    ]
    assert "--no-log-model-api" in command


def test_generic_runner_can_disable_cache(tmp_path):
    config = InspectEvalConfig(
        task="obviousbench/tasks/barrage.py",
        model="openai/gpt-5.4",
        log_dir=tmp_path / "logs",
        cache=None,
        cache_dir=tmp_path / "cache",
    )

    assert "--cache" not in build_inspect_eval_command(config)


def test_generic_runner_sets_cache_env(tmp_path, monkeypatch):
    monkeypatch.delenv("INSPECT_CACHE_DIR", raising=False)
    config = InspectEvalConfig(
        task="task.py",
        model="openai/gpt-5.4",
        log_dir=tmp_path / "logs",
        cache_dir=tmp_path / "cache",
    )

    assert inspect_eval_env(config)["INSPECT_CACHE_DIR"] == str(tmp_path / "cache")


def test_generic_runner_preserves_existing_cache_env(tmp_path, monkeypatch):
    monkeypatch.setenv("INSPECT_CACHE_DIR", "/tmp/custom-cache")
    config = InspectEvalConfig(
        task="task.py",
        model="openai/gpt-5.4",
        log_dir=tmp_path / "logs",
        cache_dir=tmp_path / "cache",
    )

    assert inspect_eval_env(config)["INSPECT_CACHE_DIR"] == "/tmp/custom-cache"


def test_parse_args_uses_default_cache_and_accepts_raw_inspect_args():
    config = parse_args(
        [
            "--task",
            "obviousbench/tasks/barrage.py",
            "--model",
            "openai/gpt-5.4",
            "-T",
            "profile=hard_obvious_8x10",
            "--inspect-arg=--no-log-model-api",
        ]
    )

    assert config.cache == "10Y"
    assert config.cache_dir == Path.cwd() / ".cache" / "inspect"
    assert config.task_args == ("profile=hard_obvious_8x10",)
    assert config.inspect_args == ("--no-log-model-api",)


def test_generic_runner_passes_generation_settings_via_generate_config(tmp_path):
    config = InspectEvalConfig(
        task="obviousbench/tasks/barrage.py",
        model="openai/gpt-5.5",
        log_dir=tmp_path / "logs",
        generation_settings={
            "reasoning_effort": "low",
            "reasoning_summary": "none",
        },
    )

    command = build_inspect_eval_command(config)

    assert "--generate-config" in command
    config_path = Path(command[command.index("--generate-config") + 1])
    assert config_path.parent == tmp_path / "logs"
    assert config_path.name.startswith("_generate_config_")
    assert "-M" not in command


def test_generation_settings_separate_thinking_variants_in_command(tmp_path):
    base = {
        "task": "obviousbench/tasks/barrage.py",
        "model": "openai/gpt-5.5",
        "log_dir": tmp_path / "logs",
    }
    low_command = build_inspect_eval_command(
        InspectEvalConfig(
            **base,
            generation_settings={
                "reasoning_effort": "low",
                "reasoning_summary": "none",
            },
        )
    )
    high_command = build_inspect_eval_command(
        InspectEvalConfig(
            **base,
            generation_settings={
                "reasoning_effort": "high",
                "reasoning_summary": "none",
            },
        )
    )

    assert low_command != high_command
    assert low_command[low_command.index("--generate-config") + 1] != high_command[
        high_command.index("--generate-config") + 1
    ]


def test_parse_args_accepts_generation_settings():
    config = parse_args(
        [
            "--task",
            "obviousbench/tasks/barrage.py",
            "--model",
            "openai/gpt-5.5",
            "--generation-setting",
            "reasoning_effort=low",
            "--generation-setting",
            "reasoning_summary=none",
            "--generation-setting",
            "seed=1",
        ]
    )

    assert config.generation_settings == {
        "reasoning_effort": "low",
        "reasoning_summary": "none",
        "seed": 1,
    }


def test_run_writes_generation_config_file(tmp_path, monkeypatch):
    calls = []

    def fake_run(command, *, cwd, env, check):
        calls.append(command)
        return SimpleNamespace(returncode=0)

    monkeypatch.setattr(inspect_eval.subprocess, "run", fake_run)
    monkeypatch.setattr(inspect_eval, "provider_refusal_sample_ids", lambda *a, **k: [])

    returncode = run_inspect_eval(
        InspectEvalConfig(
            task="obviousbench/tasks/barrage.py",
            model="openai/gpt-5.5",
            log_dir=tmp_path / "logs",
            generation_settings={
                "reasoning_effort": "low",
                "reasoning_summary": "none",
            },
        )
    )

    assert returncode == 0
    config_path = Path(calls[0][calls[0].index("--generate-config") + 1])
    assert json.loads(config_path.read_text()) == {
        "reasoning_effort": "low",
        "reasoning_summary": "none",
    }


def test_run_passes_configured_sample_ids(tmp_path, monkeypatch):
    calls = []

    def fake_run(command, *, cwd, env, check):
        calls.append(command)
        return SimpleNamespace(returncode=0)

    monkeypatch.setattr(inspect_eval.subprocess, "run", fake_run)
    monkeypatch.setattr(inspect_eval, "provider_refusal_sample_ids", lambda *a, **k: [])

    returncode = run_inspect_eval(
        InspectEvalConfig(
            task="obviousbench/tasks/barrage.py",
            model="openai/gpt-5.5",
            log_dir=tmp_path / "logs",
            sample_ids=("sample-a", "sample-b"),
        )
    )

    assert returncode == 0
    assert calls[0][calls[0].index("--sample-id") + 1] == "sample-a,sample-b"


def test_parse_args_can_disable_cache():
    config = parse_args(
        [
            "--task",
            "obviousbench/tasks/barrage.py",
            "--model",
            "openai/gpt-5.4",
            "--no-cache",
        ]
    )

    assert config.cache is None


def test_generic_runner_retries_provider_refusal_without_cache(tmp_path, monkeypatch):
    calls = []
    provider_checks = []

    def fake_run(command, *, cwd, env, check):
        calls.append(command)
        return SimpleNamespace(returncode=0)

    def fake_provider_refusal_sample_ids(log_dir, sample_ids=None, *, existing_logs=None):
        provider_checks.append(sample_ids)
        return ["sample-1"] if len(provider_checks) == 1 else []

    monkeypatch.setattr(inspect_eval.subprocess, "run", fake_run)
    monkeypatch.setattr(
        inspect_eval,
        "provider_refusal_sample_ids",
        fake_provider_refusal_sample_ids,
    )

    returncode = run_inspect_eval(
        InspectEvalConfig(
            task="obviousbench/tasks/barrage.py",
            model="xai/grok-4.3",
            log_dir=tmp_path / "logs",
            cache="10Y",
            cache_dir=tmp_path / "cache",
        )
    )

    assert returncode == 0
    assert len(calls) == 2
    assert "--sample-id" not in calls[0]
    assert calls[0][calls[0].index("--cache") + 1] == "10Y"
    assert calls[1][calls[1].index("--sample-id") + 1] == "sample-1"
    assert "--cache" not in calls[1]
