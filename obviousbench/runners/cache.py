"""Shared Inspect generation-cache defaults for developer runners."""

from __future__ import annotations

import argparse
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CACHE_EXPIRY = "10Y"
DEFAULT_CACHE_DIR = ROOT / ".cache" / "inspect"


def add_cache_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--cache",
        default=DEFAULT_CACHE_EXPIRY,
        help=f"Inspect model-generation cache expiry. Defaults to {DEFAULT_CACHE_EXPIRY}.",
    )
    parser.add_argument(
        "--cache-dir",
        default=DEFAULT_CACHE_DIR,
        type=Path,
        help="Inspect cache directory. Defaults to .cache/inspect in this repo.",
    )
    parser.add_argument("--no-cache", action="store_true")


def cache_from_args(args: argparse.Namespace) -> str | None:
    return None if args.no_cache else args.cache


def inspect_cache_env(cache_dir: Path | None) -> dict[str, str]:
    env = os.environ.copy()
    if cache_dir is not None and not env.get("INSPECT_CACHE_DIR"):
        env["INSPECT_CACHE_DIR"] = str(cache_dir)
    return env


def append_cache_args(command: list[str], cache: str | None) -> None:
    if cache is not None:
        command.extend(["--cache", cache])
