from datetime import UTC, datetime

import obviousbench.runners.openrouter_batches as openrouter_batches
from obviousbench.runners.openrouter_batches import (
    RunnerConfig,
    batch_sample_ids,
    batch_status_path,
    build_inspect_command,
    load_manifest,
    parse_openrouter_reset_epoch,
    retry_sleep_seconds,
    run_batches,
    write_manifest_entry,
)


def test_parse_openrouter_reset_epoch_from_error_metadata():
    output = """
    Error code: 429 - {'error': {'metadata': {'headers': {
      'X-RateLimit-Limit': '16',
      'X-RateLimit-Remaining': '0',
      'X-RateLimit-Reset': '1780183260000'
    }}}}
    """

    assert parse_openrouter_reset_epoch(output) == 1780183260.0


def test_retry_sleep_seconds_uses_reset_timestamp_with_buffer():
    now = datetime.fromtimestamp(1780183200, tz=UTC)

    assert retry_sleep_seconds(
        output="X-RateLimit-Reset': '1780183260000'",
        attempt=1,
        now=now,
        reset_buffer_seconds=5,
        fallback_initial_seconds=10,
        fallback_max_seconds=120,
    ) == 65


def test_retry_sleep_seconds_falls_back_to_exponential_backoff():
    now = datetime.fromtimestamp(1780183200, tz=UTC)

    assert retry_sleep_seconds(
        output="Rate limit exceeded",
        attempt=3,
        now=now,
        reset_buffer_seconds=5,
        fallback_initial_seconds=10,
        fallback_max_seconds=120,
    ) == 40


def test_batch_sample_ids_preserves_order():
    assert batch_sample_ids(["a", "b", "c", "d", "e"], 2) == [
        ["a", "b"],
        ["c", "d"],
        ["e"],
    ]


def test_manifest_round_trip(tmp_path):
    manifest = tmp_path / "manifest.jsonl"
    write_manifest_entry(
        manifest,
        {
            "batch_index": 1,
            "status": "success",
            "sample_ids": ["a", "b"],
            "attempt": 1,
        },
    )
    write_manifest_entry(
        manifest,
        {
            "batch_index": 2,
            "status": "failed",
            "sample_ids": ["c"],
            "attempt": 1,
        },
    )

    assert load_manifest(manifest) == {
        1: {
            "batch_index": 1,
            "status": "success",
            "sample_ids": ["a", "b"],
            "attempt": 1,
        },
        2: {
            "batch_index": 2,
            "status": "failed",
            "sample_ids": ["c"],
            "attempt": 1,
        },
    }


def test_batch_status_path_is_stable(tmp_path):
    assert batch_status_path(tmp_path, 12).name == "batch-0012"


def test_strict_batch_errors_omits_inspect_error_scoring_flags(tmp_path):
    config = RunnerConfig(
        task="task.py",
        dataset=tmp_path / "dataset.jsonl",
        model="openrouter/example/free",
        log_dir=tmp_path / "logs",
        batch_size=2,
        max_batch_retries=1,
        reset_buffer_seconds=5,
        fallback_initial_seconds=10,
        fallback_max_seconds=300,
        inspect_max_retries=1,
        timeout=900,
        attempt_timeout=180,
        keychain_service=None,
        strict_batch_errors=True,
        cache="10Y",
        cache_dir=tmp_path / "cache",
    )

    command = build_inspect_command(config, ["sample-1"])

    assert "--score-on-error" not in command
    assert "--no-fail-on-error" not in command
    assert "--continue-on-fail" not in command
    assert "--cache" in command
    assert command[command.index("--cache") + 1] == "10Y"
    assert "-T" in command
    assert command[command.index("-T") + 1] == f"dataset={tmp_path / 'dataset.jsonl'}"


def test_build_inspect_command_can_disable_cache(tmp_path):
    config = RunnerConfig(
        task="task.py",
        dataset=tmp_path / "dataset.jsonl",
        model="openrouter/example/free",
        log_dir=tmp_path / "logs",
        batch_size=2,
        max_batch_retries=1,
        reset_buffer_seconds=5,
        fallback_initial_seconds=10,
        fallback_max_seconds=300,
        inspect_max_retries=1,
        timeout=900,
        attempt_timeout=180,
        keychain_service=None,
        cache=None,
        cache_dir=tmp_path / "cache",
    )

    command = build_inspect_command(config, ["sample-1"])

    assert "--cache" not in command


def test_openrouter_env_sets_inspect_cache_dir(tmp_path, monkeypatch):
    monkeypatch.delenv("INSPECT_CACHE_DIR", raising=False)
    config = RunnerConfig(
        task="task.py",
        dataset=tmp_path / "dataset.jsonl",
        model="openrouter/example/free",
        log_dir=tmp_path / "logs",
        batch_size=2,
        max_batch_retries=1,
        reset_buffer_seconds=5,
        fallback_initial_seconds=10,
        fallback_max_seconds=300,
        inspect_max_retries=1,
        timeout=900,
        attempt_timeout=180,
        keychain_service=None,
        cache="10Y",
        cache_dir=tmp_path / "cache",
    )

    env = openrouter_batches.openrouter_env(config)

    assert env["INSPECT_CACHE_DIR"] == str(tmp_path / "cache")


def test_continue_after_batch_error_records_failure_and_keeps_going(
    tmp_path, monkeypatch
):
    dataset = tmp_path / "dataset.jsonl"
    dataset.write_text(
        "\n".join(
            [
                '{"id": "sample-1"}',
                '{"id": "sample-2"}',
                '{"id": "sample-3"}',
                '{"id": "sample-4"}',
            ]
        ),
        encoding="utf-8",
    )
    calls = []

    def fake_run_batch(command, *, env, dry_run=False):
        calls.append(command)
        if len(calls) == 1:
            return 2, "AttemptTimeoutError"
        return 0, "ok"

    monkeypatch.setattr(openrouter_batches, "openrouter_env", lambda config: {})
    monkeypatch.setattr(openrouter_batches, "run_batch", fake_run_batch)

    returncode = run_batches(
        RunnerConfig(
            task="task.py",
            dataset=dataset,
            model="openrouter/example/free",
            log_dir=tmp_path / "logs",
            batch_size=2,
            max_batch_retries=1,
            reset_buffer_seconds=5,
            fallback_initial_seconds=10,
            fallback_max_seconds=300,
            inspect_max_retries=1,
            timeout=900,
            attempt_timeout=180,
            keychain_service=None,
            independent_batches=True,
            strict_batch_errors=True,
            continue_after_batch_error=True,
        )
    )

    assert returncode == 2
    assert len(calls) == 2
    assert load_manifest(tmp_path / "logs" / "batch-manifest.jsonl") == {
        1: {
            "attempt": 1,
            "batch_index": 1,
            "log_dir": str(tmp_path / "logs" / "batch-0001"),
            "returncode": 2,
            "sample_ids": ["sample-1", "sample-2"],
            "status": "failed",
        },
        2: {
            "attempt": 1,
            "batch_index": 2,
            "log_dir": str(tmp_path / "logs" / "batch-0002"),
            "sample_ids": ["sample-3", "sample-4"],
            "status": "success",
        },
    }
