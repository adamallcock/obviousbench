"""Shared Inspect GenerateConfig helpers for developer runners."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections.abc import Sequence
from pathlib import Path
from typing import Any


def add_generation_setting_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--generation-setting",
        "--generate-setting",
        action="append",
        default=[],
        help=(
            "Inspect GenerateConfig setting as key=value, e.g. "
            "reasoning_effort=low. May be repeated."
        ),
    )


def generation_config_payload(settings: dict[str, Any]) -> str:
    return json.dumps(settings, sort_keys=True, separators=(",", ":"))


def generation_config_path(log_dir: Path, settings: dict[str, Any]) -> Path:
    payload = generation_config_payload(settings)
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()[:12]
    return log_dir / f"_generate_config_{digest}.json"


def write_generation_config(log_dir: Path, settings: dict[str, Any]) -> None:
    if not settings:
        return
    path = generation_config_path(log_dir, settings)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(generation_config_payload(settings) + "\n")


def parse_generation_settings(values: Sequence[str]) -> dict[str, Any]:
    settings: dict[str, Any] = {}
    for raw_value in values:
        if "=" not in raw_value:
            raise ValueError(
                f"Generation setting must be key=value, got {raw_value!r}."
            )
        key, value = raw_value.split("=", 1)
        key = key.strip()
        if not key:
            raise ValueError(
                f"Generation setting must include a non-empty key, got {raw_value!r}."
            )
        settings[key] = parse_generation_value(value.strip())
    return settings


def parse_generation_value(value: str) -> Any:
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return value
