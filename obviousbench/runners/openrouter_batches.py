"""429-aware OpenRouter Inspect batch runner."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import time
from collections.abc import Sequence
from dataclasses import dataclass, field, replace
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from obviousbench.runners.cache import (
    DEFAULT_CACHE_DIR,
    DEFAULT_CACHE_EXPIRY,
    add_cache_args,
    append_cache_args,
    cache_from_args,
    inspect_cache_env,
)
from obviousbench.runners.generation_config import (
    add_generation_setting_args,
    generation_config_path,
    parse_generation_settings,
    write_generation_config,
)
from obviousbench.runners.provider_refusals import provider_refusal_sample_ids

ROOT = Path(__file__).resolve().parents[2]
OPENROUTER_RESET_RE = re.compile(
    r"['\"]?X-RateLimit-Reset['\"]?\s*:\s*['\"](?P<value>\d{10,16})['\"]",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class RunnerConfig:
    task: str
    dataset: Path
    model: str
    log_dir: Path
    batch_size: int
    max_batch_retries: int
    reset_buffer_seconds: int
    fallback_initial_seconds: int
    fallback_max_seconds: int
    inspect_max_retries: int
    timeout: int
    attempt_timeout: int
    keychain_service: str | None
    cache: str | None = DEFAULT_CACHE_EXPIRY
    cache_dir: Path | None = DEFAULT_CACHE_DIR
    generation_settings: dict[str, Any] = field(default_factory=dict)
    retry_provider_refusals: bool = True
    independent_batches: bool = False
    resume: bool = False
    strict_batch_errors: bool = False
    continue_after_batch_error: bool = False
    dry_run: bool = False


def parse_openrouter_reset_epoch(output: str) -> float | None:
    """Return epoch seconds from OpenRouter's embedded X-RateLimit-Reset value."""
    match = OPENROUTER_RESET_RE.search(output)
    if not match:
        return None

    value = int(match.group("value"))
    if value > 10_000_000_000:
        return value / 1000
    return float(value)


def retry_sleep_seconds(
    *,
    output: str,
    attempt: int,
    now: datetime | None = None,
    reset_buffer_seconds: int = 5,
    fallback_initial_seconds: int = 10,
    fallback_max_seconds: int = 300,
) -> int:
    """Compute sleep before retrying a failed batch."""
    now = now or datetime.now(UTC)
    reset_epoch = parse_openrouter_reset_epoch(output)
    if reset_epoch is not None:
        reset_at = datetime.fromtimestamp(reset_epoch, tz=UTC)
        seconds = int((reset_at - now).total_seconds()) + reset_buffer_seconds
        return max(seconds, reset_buffer_seconds)

    fallback = fallback_initial_seconds * (2 ** max(attempt - 1, 0))
    return min(fallback, fallback_max_seconds)


def batch_sample_ids(sample_ids: Sequence[str], batch_size: int) -> list[list[str]]:
    if batch_size < 1:
        raise ValueError("batch_size must be positive")
    return [
        list(sample_ids[index : index + batch_size])
        for index in range(0, len(sample_ids), batch_size)
    ]


def batch_status_path(log_dir: Path, batch_index: int) -> Path:
    return log_dir / f"batch-{batch_index:04d}"


def manifest_path(log_dir: Path) -> Path:
    return log_dir / "batch-manifest.jsonl"


def write_manifest_entry(path: Path, entry: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(entry, sort_keys=True) + "\n")


def load_manifest(path: Path) -> dict[int, dict[str, object]]:
    if not path.exists():
        return {}
    entries: dict[int, dict[str, object]] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        entry = json.loads(line)
        entries[int(entry["batch_index"])] = entry
    return entries


def load_sample_ids(dataset: Path) -> list[str]:
    sample_ids: list[str] = []
    for line_number, line in enumerate(dataset.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        record = json.loads(line)
        try:
            sample_ids.append(str(record["id"]))
        except KeyError as exc:
            raise ValueError(f"{dataset}:{line_number} missing id") from exc
    return sample_ids


def build_inspect_command(config: RunnerConfig, sample_ids: Sequence[str]) -> list[str]:
    command = [
        str(ROOT / ".venv" / "bin" / "inspect"),
        "eval",
        config.task,
        "--model",
        config.model,
        "--log-dir",
        str(config.log_dir),
        "-T",
        f"dataset={config.dataset}",
        "--sample-id",
        ",".join(sample_ids),
        "--max-connections",
        "1",
        "--max-retries",
        str(config.inspect_max_retries),
        "--timeout",
        str(config.timeout),
        "--attempt-timeout",
        str(config.attempt_timeout),
        "--no-log-realtime",
        "--no-log-model-api",
    ]
    append_cache_args(command, config.cache)
    if config.generation_settings:
        command.extend(
            [
                "--generate-config",
                str(generation_config_path(config.log_dir, config.generation_settings)),
            ]
        )
    if not config.strict_batch_errors:
        command.extend(
            [
                "--no-fail-on-error",
                "--continue-on-fail",
                "--score-on-error",
            ]
        )
    return command


def openrouter_env(config: RunnerConfig) -> dict[str, str]:
    env = inspect_cache_env(config.cache_dir)
    if env.get("OPENROUTER_API_KEY"):
        return env
    if config.keychain_service is None:
        return env

    result = subprocess.run(
        ["security", "find-generic-password", "-s", config.keychain_service, "-w"],
        check=True,
        capture_output=True,
        text=True,
    )
    env["OPENROUTER_API_KEY"] = result.stdout.strip()
    return env


def run_batch(
    command: Sequence[str],
    *,
    env: dict[str, str],
    dry_run: bool = False,
) -> tuple[int, str]:
    if dry_run:
        return 0, "DRY RUN: " + " ".join(command)
    result = subprocess.run(
        list(command),
        env=env,
        capture_output=True,
        text=True,
        cwd=ROOT,
    )
    return result.returncode, result.stdout + result.stderr


def run_batches(config: RunnerConfig) -> int:
    sample_ids = load_sample_ids(config.dataset)
    batches = batch_sample_ids(sample_ids, config.batch_size)
    env = openrouter_env(config)
    prior_manifest = load_manifest(manifest_path(config.log_dir)) if config.resume else {}
    final_returncode = 0

    for batch_index, batch in enumerate(batches, 1):
        previous = prior_manifest.get(batch_index)
        if config.resume and previous and previous.get("status") == "success":
            print(f"batch {batch_index}/{len(batches)} already succeeded; skipping")
            continue

        batch_log_dir = (
            batch_status_path(config.log_dir, batch_index)
            if config.independent_batches
            else config.log_dir
        )
        active_batch = list(batch)
        bypass_cache = False
        for attempt in range(1, config.max_batch_retries + 1):
            batch_config = replace(
                config,
                log_dir=batch_log_dir,
                cache=None if bypass_cache else config.cache,
            )
            write_generation_config(
                batch_config.log_dir,
                batch_config.generation_settings,
            )
            command = build_inspect_command(batch_config, active_batch)
            print(
                f"batch {batch_index}/{len(batches)} attempt {attempt}: "
                f"{active_batch[0]}..{active_batch[-1]}",
                flush=True,
            )
            existing_logs = set(batch_log_dir.rglob("*.eval"))
            returncode, output = run_batch(command, env=env, dry_run=config.dry_run)
            print(output, end="" if output.endswith("\n") else "\n")
            if returncode == 0:
                refused_sample_ids = (
                    []
                    if not config.retry_provider_refusals or config.dry_run
                    else provider_refusal_sample_ids(
                        batch_log_dir,
                        active_batch,
                        existing_logs=existing_logs,
                    )
                )
                if refused_sample_ids:
                    print(
                        "provider refusal text detected; retrying "
                        f"{len(refused_sample_ids)} sample(s) without cache",
                        flush=True,
                    )
                    if attempt < config.max_batch_retries:
                        active_batch = refused_sample_ids
                        bypass_cache = True
                        continue
                    write_manifest_entry(
                        manifest_path(config.log_dir),
                        {
                            "attempt": attempt,
                            "batch_index": batch_index,
                            "log_dir": str(batch_log_dir),
                            "returncode": 1,
                            "sample_ids": list(batch),
                            "status": "provider_refusal",
                            "transient_sample_ids": refused_sample_ids,
                        },
                    )
                    if not config.continue_after_batch_error:
                        return 1
                    final_returncode = 1
                    break
                write_manifest_entry(
                    manifest_path(config.log_dir),
                    {
                        "attempt": attempt,
                        "batch_index": batch_index,
                        "log_dir": str(batch_log_dir),
                        "sample_ids": list(batch),
                        "status": "success",
                    },
                )
                break

            if "429" not in output and "RateLimitError" not in output:
                write_manifest_entry(
                    manifest_path(config.log_dir),
                    {
                        "attempt": attempt,
                        "batch_index": batch_index,
                        "log_dir": str(batch_log_dir),
                        "sample_ids": list(batch),
                        "status": "failed",
                        "returncode": returncode,
                    },
                )
                if not config.continue_after_batch_error:
                    return returncode
                final_returncode = returncode
                break

            if attempt >= config.max_batch_retries:
                write_manifest_entry(
                    manifest_path(config.log_dir),
                    {
                        "attempt": attempt,
                        "batch_index": batch_index,
                        "log_dir": str(batch_log_dir),
                        "sample_ids": list(batch),
                        "status": "rate_limited",
                        "returncode": returncode,
                    },
                )
                if not config.continue_after_batch_error:
                    return returncode
                final_returncode = returncode
                break

            sleep_seconds = retry_sleep_seconds(
                output=output,
                attempt=attempt,
                reset_buffer_seconds=config.reset_buffer_seconds,
                fallback_initial_seconds=config.fallback_initial_seconds,
                fallback_max_seconds=config.fallback_max_seconds,
            )
            print(f"rate limited; sleeping {sleep_seconds}s before retry", flush=True)
            time.sleep(sleep_seconds)

    return final_returncode


def parse_args(argv: Sequence[str] | None = None) -> RunnerConfig:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--task", required=True)
    parser.add_argument("--dataset", required=True, type=Path)
    parser.add_argument(
        "--model",
        default="openrouter/nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free",
    )
    parser.add_argument("--log-dir", default=Path("results/raw"), type=Path)
    parser.add_argument("--batch-size", default=8, type=int)
    parser.add_argument("--max-batch-retries", default=5, type=int)
    parser.add_argument("--reset-buffer-seconds", default=5, type=int)
    parser.add_argument("--fallback-initial-seconds", default=10, type=int)
    parser.add_argument("--fallback-max-seconds", default=300, type=int)
    parser.add_argument("--inspect-max-retries", default=6, type=int)
    parser.add_argument("--timeout", default=900, type=int)
    parser.add_argument("--attempt-timeout", default=180, type=int)
    parser.add_argument("--keychain-service", default="OPENROUTER_API_KEY")
    add_generation_setting_args(parser)
    add_cache_args(parser)
    parser.add_argument("--independent-batches", action="store_true")
    parser.add_argument("--resume", action="store_true")
    parser.add_argument(
        "--no-retry-provider-refusals",
        action="store_true",
        help=(
            "Do not retry provider safety/error strings returned as assistant text. "
            "By default these are retried without Inspect cache."
        ),
    )
    parser.add_argument("--strict-batch-errors", action="store_true")
    parser.add_argument("--continue-after-batch-error", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)
    try:
        generation_settings = parse_generation_settings(args.generation_setting)
    except ValueError as exc:
        parser.error(str(exc))
    return RunnerConfig(
        task=args.task,
        dataset=args.dataset,
        model=args.model,
        log_dir=args.log_dir,
        batch_size=args.batch_size,
        max_batch_retries=args.max_batch_retries,
        reset_buffer_seconds=args.reset_buffer_seconds,
        fallback_initial_seconds=args.fallback_initial_seconds,
        fallback_max_seconds=args.fallback_max_seconds,
        inspect_max_retries=args.inspect_max_retries,
        timeout=args.timeout,
        attempt_timeout=args.attempt_timeout,
        keychain_service=args.keychain_service,
        cache=cache_from_args(args),
        cache_dir=args.cache_dir,
        generation_settings=generation_settings,
        retry_provider_refusals=not args.no_retry_provider_refusals,
        independent_batches=args.independent_batches,
        resume=args.resume,
        strict_batch_errors=args.strict_batch_errors,
        continue_after_batch_error=args.continue_after_batch_error,
        dry_run=args.dry_run,
    )


def main(argv: Sequence[str] | None = None) -> int:
    return run_batches(parse_args(argv))


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
