"""Generic Inspect eval runner with ObviousBench cache defaults."""

from __future__ import annotations

import argparse
import subprocess
import sys
from collections.abc import Sequence
from dataclasses import dataclass, field
from pathlib import Path

from obviousbench.runners.cache import (
    DEFAULT_CACHE_DIR,
    DEFAULT_CACHE_EXPIRY,
    ROOT,
    add_cache_args,
    append_cache_args,
    cache_from_args,
    inspect_cache_env,
)


@dataclass(frozen=True)
class InspectEvalConfig:
    task: str
    model: str
    log_dir: Path
    task_args: tuple[str, ...] = ()
    inspect_args: tuple[str, ...] = ()
    cache: str | None = DEFAULT_CACHE_EXPIRY
    cache_dir: Path | None = DEFAULT_CACHE_DIR
    env: dict[str, str] = field(default_factory=dict)
    dry_run: bool = False


def build_inspect_eval_command(config: InspectEvalConfig) -> list[str]:
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
    for task_arg in config.task_args:
        command.extend(["-T", task_arg])
    command.extend(config.inspect_args)
    return command


def inspect_eval_env(config: InspectEvalConfig) -> dict[str, str]:
    env = inspect_cache_env(config.cache_dir)
    env.update(config.env)
    return env


def run_inspect_eval(config: InspectEvalConfig) -> int:
    command = build_inspect_eval_command(config)
    if config.dry_run:
        print(" ".join(command))
        return 0
    return subprocess.run(command, cwd=ROOT, env=inspect_eval_env(config), check=False).returncode


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
    add_cache_args(parser)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)
    return InspectEvalConfig(
        task=args.task,
        model=args.model,
        log_dir=args.log_dir,
        task_args=tuple(args.task_arg),
        inspect_args=tuple(args.inspect_arg),
        cache=cache_from_args(args),
        cache_dir=args.cache_dir,
        dry_run=args.dry_run,
    )


def main(argv: Sequence[str] | None = None) -> int:
    return run_inspect_eval(parse_args(argv))


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
