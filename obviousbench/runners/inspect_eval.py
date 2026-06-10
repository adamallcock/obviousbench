"""Generic Inspect eval runner with ObviousBench cache defaults."""

from __future__ import annotations

import argparse
import subprocess
import sys
from collections.abc import Sequence
from dataclasses import dataclass, field, replace
from pathlib import Path
from typing import Any

from obviousbench.runners.cache import (
    DEFAULT_CACHE_DIR,
    DEFAULT_CACHE_EXPIRY,
    ROOT,
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


@dataclass(frozen=True)
class InspectEvalConfig:
    task: str
    model: str
    log_dir: Path
    task_args: tuple[str, ...] = ()
    inspect_args: tuple[str, ...] = ()
    generation_settings: dict[str, Any] = field(default_factory=dict)
    cache: str | None = DEFAULT_CACHE_EXPIRY
    cache_dir: Path | None = DEFAULT_CACHE_DIR
    retry_provider_refusals: bool = True
    provider_refusal_retries: int = 1
    env: dict[str, str] = field(default_factory=dict)
    sample_ids: tuple[str, ...] = ()
    dry_run: bool = False


def build_inspect_eval_command(
    config: InspectEvalConfig,
    *,
    sample_ids: Sequence[str] | None = None,
) -> list[str]:
    command = [
        str(ROOT / ".venv" / "bin" / "inspect"),
        "eval",
        config.task,
        "--model",
        config.model,
        "--log-dir",
        str(config.log_dir),
    ]
    append_cache_args(command, config.cache)
    if sample_ids:
        command.extend(["--sample-id", ",".join(sample_ids)])
    if config.generation_settings:
        command.extend(
            [
                "--generate-config",
                str(generation_config_path(config.log_dir, config.generation_settings)),
            ]
        )
    for task_arg in config.task_args:
        command.extend(["-T", task_arg])
    command.extend(config.inspect_args)
    return command


def inspect_eval_env(config: InspectEvalConfig) -> dict[str, str]:
    env = inspect_cache_env(config.cache_dir)
    env.update(config.env)
    return env


def run_inspect_eval(config: InspectEvalConfig) -> int:
    write_generation_config(config.log_dir, config.generation_settings)
    command = build_inspect_eval_command(config, sample_ids=config.sample_ids)
    if config.dry_run:
        print(" ".join(command))
        return 0
    existing_logs = set(config.log_dir.rglob("*.eval"))
    returncode = _run_command(command, config)
    if returncode != 0 or not config.retry_provider_refusals:
        return returncode

    for _attempt in range(config.provider_refusal_retries):
        refused_sample_ids = provider_refusal_sample_ids(
            config.log_dir,
            sample_ids=config.sample_ids or None,
            existing_logs=existing_logs,
        )
        if not refused_sample_ids:
            return 0
        print(
            "provider refusal text detected; retrying "
            f"{len(refused_sample_ids)} sample(s) without cache",
            flush=True,
        )
        existing_logs = set(config.log_dir.rglob("*.eval"))
        retry_config = replace(config, cache=None)
        write_generation_config(retry_config.log_dir, retry_config.generation_settings)
        returncode = _run_command(
            build_inspect_eval_command(retry_config, sample_ids=refused_sample_ids),
            retry_config,
        )
        if returncode != 0:
            return returncode

    remaining = provider_refusal_sample_ids(
        config.log_dir,
        sample_ids=config.sample_ids or None,
        existing_logs=existing_logs,
    )
    return 1 if remaining else 0


def _run_command(command: Sequence[str], config: InspectEvalConfig) -> int:
    return subprocess.run(
        list(command),
        cwd=ROOT,
        env=inspect_eval_env(config),
        check=False,
    ).returncode


def parse_args(argv: Sequence[str] | None = None) -> InspectEvalConfig:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--task", required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--log-dir", default=Path("results/raw"), type=Path)
    parser.add_argument(
        "-T",
        "--task-arg",
        action="append",
        default=[],
        help="Task argument, e.g. profile=hard_obvious_8x10. May be repeated.",
    )
    parser.add_argument(
        "--inspect-arg",
        action="append",
        default=[],
        help="Raw Inspect CLI argument. May be repeated for flags or values.",
    )
    add_generation_setting_args(parser)
    add_cache_args(parser)
    parser.add_argument(
        "--sample-id",
        action="append",
        default=[],
        help=(
            "Inspect sample ID or comma-separated sample IDs. May be repeated. "
            "Useful for smoke tests."
        ),
    )
    parser.add_argument(
        "--no-retry-provider-refusals",
        action="store_true",
        help=(
            "Do not retry provider safety/error strings returned as assistant text. "
            "By default these are retried without Inspect cache."
        ),
    )
    parser.add_argument("--provider-refusal-retries", default=1, type=int)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)
    try:
        generation_settings = parse_generation_settings(args.generation_setting)
    except ValueError as exc:
        parser.error(str(exc))
    return InspectEvalConfig(
        task=args.task,
        model=args.model,
        log_dir=args.log_dir,
        task_args=tuple(args.task_arg),
        inspect_args=tuple(args.inspect_arg),
        generation_settings=generation_settings,
        cache=cache_from_args(args),
        cache_dir=args.cache_dir,
        retry_provider_refusals=not args.no_retry_provider_refusals,
        provider_refusal_retries=args.provider_refusal_retries,
        sample_ids=tuple(_parse_sample_ids(args.sample_id)),
        dry_run=args.dry_run,
    )


def _parse_sample_ids(values: Sequence[str]) -> list[str]:
    sample_ids: list[str] = []
    for value in values:
        sample_ids.extend(
            sample_id.strip() for sample_id in value.split(",") if sample_id.strip()
        )
    return sample_ids


def main(argv: Sequence[str] | None = None) -> int:
    return run_inspect_eval(parse_args(argv))


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
