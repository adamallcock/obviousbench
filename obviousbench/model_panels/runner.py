"""Run model-panel YAML entries through Inspect and ObviousBench rescoring."""

from __future__ import annotations

import argparse
import csv
import json
import shlex
import subprocess
import sys
from collections.abc import Callable, Sequence
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Literal

import yaml

from obviousbench.runners.cache import DEFAULT_CACHE_DIR, DEFAULT_CACHE_EXPIRY, ROOT
from obviousbench.runners.generation_config import write_generation_config
from obviousbench.runners.inspect_eval import (
    InspectEvalConfig,
    build_inspect_eval_command,
    run_inspect_eval,
)

RunMode = Literal["smoke", "full"]

_KNOWN_GENERATION_KEYS = (
    "temperature",
    "max_tokens",
    "reasoning_effort",
    "reasoning_summary",
    "reasoning_tokens",
    "thinking_budget",
    "thinking_budget_tokens",
    "seed",
)

_GENERATION_KEY_ALIASES = {
    "max_output_tokens": "max_tokens",
}


@dataclass(frozen=True)
class ModelPanelRunInputs:
    panel_path: Path
    dataset_path: Path
    raw_root: Path
    summary_root: Path
    manifest_out: Path
    status_out: Path
    mode: RunMode = "smoke"
    smoke_sample_ids: tuple[str, ...] = ()
    task: str = "obviousbench/tasks/barrage.py"
    only: tuple[str, ...] = ()
    limit: int | None = None
    skip_completed: bool = True
    dry_run: bool = False
    cost: Literal["none", "runcost"] = "runcost"
    cache: str | None = DEFAULT_CACHE_EXPIRY
    cache_dir: Path | None = DEFAULT_CACHE_DIR


@dataclass(frozen=True)
class ModelPanelStatusRow:
    entry_id: str
    label: str
    model: str
    provider_route: str
    mode: RunMode
    status: str
    log_dir: str
    summary_dir: str
    inspect_command: str
    summarize_command: str
    generation_settings: dict[str, Any] = field(default_factory=dict)
    returncode: int = 0
    error: str = ""


@dataclass(frozen=True)
class ModelPanelRunResult:
    manifest_out: Path
    status_out: Path
    rows: tuple[ModelPanelStatusRow, ...]

    @property
    def failed_count(self) -> int:
        return sum(1 for row in self.rows if row.returncode != 0)

    @property
    def ok(self) -> bool:
        return self.failed_count == 0


InspectRunner = Callable[[InspectEvalConfig], int]
RescoreRunner = Callable[[Path, Path, str], int]


def run_model_panel(
    inputs: ModelPanelRunInputs,
    *,
    inspect_runner: InspectRunner = run_inspect_eval,
    rescore_runner: RescoreRunner | None = None,
) -> ModelPanelRunResult:
    """Run selected model-panel entries and append a status row per entry."""
    panel = _load_panel(inputs.panel_path)
    entries = _select_entries(panel.get("entries") or [], inputs.only, inputs.limit)
    expected_samples = _expected_sample_count(inputs)
    inputs.manifest_out.parent.mkdir(parents=True, exist_ok=True)
    inputs.status_out.parent.mkdir(parents=True, exist_ok=True)
    inputs.status_out.write_text("", encoding="utf-8")
    _write_manifest(inputs.manifest_out, entries, inputs.summary_root)

    rows: list[ModelPanelStatusRow] = []
    for entry in entries:
        config = _inspect_config(inputs, panel, entry)
        summary_dir = inputs.summary_root / str(entry["id"])
        summarize_command = _summarize_command(config.log_dir, summary_dir, inputs.cost)
        inspect_command = shlex.join(
            build_inspect_eval_command(config, sample_ids=config.sample_ids)
        )

        if inputs.skip_completed and _summary_complete(
            summary_dir, expected_samples=expected_samples
        ):
            row = _status_row(
                inputs,
                entry,
                config,
                summary_dir,
                inspect_command,
                summarize_command,
                status="skipped_completed",
            )
            _append_status(inputs.status_out, row)
            rows.append(row)
            continue

        write_generation_config(config.log_dir, config.generation_settings)
        if inputs.dry_run:
            row = _status_row(
                inputs,
                entry,
                config,
                summary_dir,
                inspect_command,
                summarize_command,
                status="dry_run",
            )
            _append_status(inputs.status_out, row)
            rows.append(row)
            continue

        inspect_returncode = inspect_runner(config)
        if inspect_returncode != 0:
            row = _status_row(
                inputs,
                entry,
                config,
                summary_dir,
                inspect_command,
                summarize_command,
                status="failed_inspect",
                returncode=inspect_returncode,
            )
            _append_status(inputs.status_out, row)
            rows.append(row)
            continue

        summarize_returncode = (rescore_runner or _run_rescore_command)(
            config.log_dir,
            summary_dir,
            inputs.cost,
        )
        if summarize_returncode == 0:
            summary_ok, summary_error = _validate_summary(
                summary_dir, expected_samples=expected_samples
            )
            if not summary_ok:
                row = _status_row(
                    inputs,
                    entry,
                    config,
                    summary_dir,
                    inspect_command,
                    summarize_command,
                    status="failed_summary_validation",
                    returncode=1,
                    error=summary_error,
                )
                _append_status(inputs.status_out, row)
                rows.append(row)
                continue
        row = _status_row(
            inputs,
            entry,
            config,
            summary_dir,
            inspect_command,
            summarize_command,
            status="passed" if summarize_returncode == 0 else "failed_rescore",
            returncode=summarize_returncode,
        )
        _append_status(inputs.status_out, row)
        rows.append(row)

    return ModelPanelRunResult(
        manifest_out=inputs.manifest_out,
        status_out=inputs.status_out,
        rows=tuple(rows),
    )


def _load_panel(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"model panel does not exist: {path}")
    panel = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(panel, dict):
        raise ValueError(f"model panel must contain a YAML object: {path}")
    return panel


def _select_entries(
    entries: Sequence[dict[str, Any]],
    only: Sequence[str],
    limit: int | None,
) -> list[dict[str, Any]]:
    selected = [entry for entry in entries if entry.get("run_status") != "excluded"]
    if only:
        wanted = set(only)
        selected = [entry for entry in selected if str(entry.get("id")) in wanted]
        found = {str(entry.get("id")) for entry in selected}
        missing = sorted(wanted - found)
        if missing:
            raise ValueError(f"model panel entries not found: {', '.join(missing)}")
    if limit is not None:
        selected = selected[:limit]
    return [_normalize_entry_controls(entry) for entry in selected]


def _normalize_entry_controls(entry: dict[str, Any]) -> dict[str, Any]:
    """Restore control metadata that can be lost in CSV-derived panel expansion."""
    normalized = dict(entry)
    if _needs_anthropic_adaptive_control_style(normalized):
        normalized["control_style"] = "anthropic_adaptive_thinking_effort"
    return normalized


def _needs_anthropic_adaptive_control_style(entry: dict[str, Any]) -> bool:
    if entry.get("control_style"):
        return False
    inspect_model = str(entry.get("inspect_model") or "")
    if not inspect_model.startswith("anthropic/"):
        return False
    generation_settings = entry.get("generation_settings") or {}
    return (
        isinstance(generation_settings, dict)
        and generation_settings.get("effort") is not None
    ) or entry.get("effort") is not None


def _inspect_config(
    inputs: ModelPanelRunInputs,
    panel: dict[str, Any],
    entry: dict[str, Any],
) -> InspectEvalConfig:
    defaults = panel.get("defaults") or {}
    entry_id = str(entry["id"])
    inspect_args = tuple(str(arg) for arg in defaults.get("inspect_args") or ())
    inspect_args += tuple(str(arg) for arg in entry.get("inspect_args") or ())
    sample_ids = inputs.smoke_sample_ids if inputs.mode == "smoke" else ()
    return InspectEvalConfig(
        task=inputs.task,
        model=str(entry["inspect_model"]),
        log_dir=inputs.raw_root / entry_id,
        task_args=(f"dataset={inputs.dataset_path.resolve()}",),
        inspect_args=inspect_args,
        generation_settings=_generation_settings(entry, defaults),
        cache=inputs.cache,
        cache_dir=inputs.cache_dir,
        sample_ids=sample_ids,
    )


def _generation_settings(
    entry: dict[str, Any],
    defaults: dict[str, Any],
) -> dict[str, Any]:
    settings: dict[str, Any] = {}
    for key, value in (defaults.get("generation_settings") or {}).items():
        _set_generation_setting(settings, key, value)
    for key in _KNOWN_GENERATION_KEYS:
        if key in defaults:
            _set_generation_setting(settings, key, defaults[key])
    for key, value in _GENERATION_KEY_ALIASES.items():
        if key in defaults:
            _set_generation_setting(settings, value, defaults[key])
    for key, value in (entry.get("generation_settings") or {}).items():
        _set_generation_setting(settings, key, value)
    for key in _KNOWN_GENERATION_KEYS:
        if key in entry:
            _set_generation_setting(settings, key, entry[key])
    for key, value in _GENERATION_KEY_ALIASES.items():
        if key in entry:
            _set_generation_setting(settings, value, entry[key])
    _translate_control_style_generation_settings(entry, settings)
    return settings


def _set_generation_setting(settings: dict[str, Any], key: str, value: Any) -> None:
    if value is None or value == "provider_default":
        return
    settings[key] = value


def _translate_control_style_generation_settings(
    entry: dict[str, Any],
    settings: dict[str, Any],
) -> None:
    """Map a panel entry's generic ``effort`` onto Anthropic adaptive thinking.

    ``control_style: anthropic_adaptive_thinking_effort`` renames ``effort`` to
    ``reasoning_effort`` -- the key Inspect uses to send ``thinking:{type:adaptive}``.
    Bare ``effort`` only sets ``output_config.effort`` and leaves extended thinking
    OFF on Claude 4.x, so the rename is what actually enables thinking.

    Panels reconstructed from comparison/leaderboard CSVs lose ``control_style``
    (those tables have no such column). Without a guard that silently disables
    thinking for every Anthropic effort entry. So we also translate when
    ``control_style`` is absent but the entry targets an Anthropic model and sets
    ``effort``. An explicit non-adaptive ``control_style`` still opts out, and
    effort-less Anthropic baselines stay thinking-off (there is nothing to rename).
    """
    control_style = entry.get("control_style")
    inspect_model = str(entry.get("inspect_model") or "")
    is_adaptive = control_style == "anthropic_adaptive_thinking_effort"
    anthropic_without_control_style = (
        not control_style and inspect_model.startswith("anthropic/")
    )
    if not (is_adaptive or anthropic_without_control_style):
        return
    effort = settings.pop("effort", None)
    if effort is not None and settings.get("reasoning_effort") is None:
        settings["reasoning_effort"] = effort


def _expected_sample_count(inputs: ModelPanelRunInputs) -> int:
    if inputs.mode == "smoke" and inputs.smoke_sample_ids:
        return len(inputs.smoke_sample_ids)
    return _dataset_sample_count(inputs.dataset_path)


def _dataset_sample_count(path: Path) -> int:
    if not path.exists():
        raise FileNotFoundError(f"dataset does not exist: {path}")
    with path.open(encoding="utf-8") as handle:
        return sum(1 for line in handle if line.strip())


def _summary_complete(summary_dir: Path, *, expected_samples: int) -> bool:
    ok, _error = _validate_summary(summary_dir, expected_samples=expected_samples)
    return ok


def _validate_summary(
    summary_dir: Path, *, expected_samples: int
) -> tuple[bool, str]:
    summary_path = summary_dir / "summary.csv"
    if not summary_path.exists() or summary_path.stat().st_size == 0:
        return False, f"summary.csv missing or empty: {summary_path}"
    with summary_path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        return False, f"summary.csv has no data rows: {summary_path}"
    row = rows[0]
    total_samples = _summary_int(row.get("total_samples"))
    scored_samples = _summary_int(row.get("scored_samples"))
    provider_errors = _summary_int(row.get("provider_errors"))
    if total_samples <= 0:
        return False, f"summary has no attempted samples: {summary_path}"
    if scored_samples <= 0:
        return (
            False,
            f"summary scored 0/{total_samples} samples; provider_errors={provider_errors}",
        )
    if total_samples != expected_samples or scored_samples != expected_samples:
        return (
            False,
            (
                f"summary has total_samples={total_samples} and "
                f"scored_samples={scored_samples}; expected {expected_samples} "
                f"total samples and expected {expected_samples} scored samples; "
                f"provider_errors={provider_errors}"
            ),
        )
    return True, ""


def _summary_int(value: str | None) -> int:
    if value is None or value == "":
        return 0
    try:
        return int(value)
    except ValueError:
        return int(float(value))


def _write_manifest(
    path: Path,
    entries: Sequence[dict[str, Any]],
    summary_root: Path,
) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["label", "model", "summary_dir"],
            lineterminator="\n",
        )
        writer.writeheader()
        for entry in entries:
            writer.writerow(
                {
                    "label": str(entry["label"]),
                    "model": str(entry["inspect_model"]),
                    "summary_dir": str(summary_root / str(entry["id"])),
                }
            )


def _status_row(
    inputs: ModelPanelRunInputs,
    entry: dict[str, Any],
    config: InspectEvalConfig,
    summary_dir: Path,
    inspect_command: str,
    summarize_command: str,
    *,
    status: str,
    returncode: int = 0,
    error: str = "",
) -> ModelPanelStatusRow:
    return ModelPanelStatusRow(
        entry_id=str(entry["id"]),
        label=str(entry["label"]),
        model=str(entry["inspect_model"]),
        provider_route=str(entry.get("provider_route", "")),
        mode=inputs.mode,
        status=status,
        log_dir=str(config.log_dir),
        summary_dir=str(summary_dir),
        inspect_command=inspect_command,
        summarize_command=summarize_command,
        generation_settings=dict(config.generation_settings),
        returncode=returncode,
        error=error,
    )


def _append_status(path: Path, row: ModelPanelStatusRow) -> None:
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(asdict(row), sort_keys=True) + "\n")


def _summarize_command(log_dir: Path, summary_dir: Path, cost: str) -> str:
    return shlex.join(
        [
            sys.executable,
            "-m",
            "obviousbench.cli",
            "rescore",
            "--logs",
            str(log_dir),
            "--out",
            str(summary_dir),
            "--cost",
            cost,
        ]
    )


def _run_rescore_command(log_dir: Path, summary_dir: Path, cost: str) -> int:
    command = [
        sys.executable,
        "-m",
        "obviousbench.cli",
        "rescore",
        "--logs",
        str(log_dir),
        "--out",
        str(summary_dir),
        "--cost",
        cost,
    ]
    return subprocess.run(command, cwd=ROOT, check=False).returncode


def parse_args(argv: Sequence[str] | None = None) -> ModelPanelRunInputs:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--panel", required=True, type=Path)
    parser.add_argument("--dataset", required=True, type=Path)
    parser.add_argument("--raw-root", required=True, type=Path)
    parser.add_argument("--summary-root", required=True, type=Path)
    parser.add_argument("--manifest-out", required=True, type=Path)
    parser.add_argument("--status-out", required=True, type=Path)
    parser.add_argument("--mode", choices=("smoke", "full"), default="smoke")
    parser.add_argument(
        "--sample-id",
        action="append",
        default=[],
        help="Smoke sample ID or comma-separated IDs. May be repeated.",
    )
    parser.add_argument(
        "--only",
        action="append",
        default=[],
        help="Run only a model-panel entry ID. May be repeated.",
    )
    parser.add_argument("--limit", type=int)
    parser.add_argument("--no-skip-completed", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--cost", choices=("none", "runcost"), default="runcost")
    parser.add_argument("--cache", default=DEFAULT_CACHE_EXPIRY)
    parser.add_argument("--cache-dir", default=DEFAULT_CACHE_DIR, type=Path)
    parser.add_argument("--no-cache", action="store_true")
    args = parser.parse_args(argv)

    return ModelPanelRunInputs(
        panel_path=args.panel,
        dataset_path=args.dataset,
        raw_root=args.raw_root,
        summary_root=args.summary_root,
        manifest_out=args.manifest_out,
        status_out=args.status_out,
        mode=args.mode,
        smoke_sample_ids=tuple(_parse_repeated_csv(args.sample_id)),
        only=tuple(_parse_repeated_csv(args.only)),
        limit=args.limit,
        skip_completed=not args.no_skip_completed,
        dry_run=args.dry_run,
        cost=args.cost,
        cache=None if args.no_cache else args.cache,
        cache_dir=None if args.no_cache else args.cache_dir,
    )


def _parse_repeated_csv(values: Sequence[str]) -> list[str]:
    parsed: list[str] = []
    for value in values:
        parsed.extend(item.strip() for item in value.split(",") if item.strip())
    return parsed


def main(argv: Sequence[str] | None = None) -> int:
    try:
        result = run_model_panel(parse_args(argv))
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        return 1

    print(f"Wrote run manifest to {result.manifest_out}")
    print(f"Wrote run status to {result.status_out}")
    if result.failed_count:
        print(f"Failed entries: {result.failed_count}", file=sys.stderr)
    return 0 if result.ok else 1
