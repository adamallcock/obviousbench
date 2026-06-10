"""Dry-run cost estimates for the frozen paper model panel."""

from __future__ import annotations

import csv
import shlex
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from obviousbench.estimation.cost import (
    CostEstimate,
    CostEstimateInputs,
)
from obviousbench.estimation.cost import (
    estimate_benchmark_cost as default_estimator,
)

Estimator = Callable[[CostEstimateInputs], CostEstimate]

_KNOWN_GENERATION_KEYS = (
    "temperature",
    "max_tokens",
    "reasoning_effort",
    "reasoning_summary",
    "reasoning_tokens",
    "seed",
    "attempt_timeout",
)
_INSPECT_ARG_GENERATION_SETTINGS = {
    "attempt-timeout": "attempt_timeout",
}


@dataclass(frozen=True)
class ModelPanelCostInputs:
    panel_path: Path
    csv_path: Path
    markdown_path: Path
    data_dir: Path = Path("data")
    summary_root: Path = Path("results/summaries")
    cache: str | None = None
    cache_dir: Path | None = None
    estimator: Estimator = default_estimator


@dataclass(frozen=True)
class ModelPanelCostResult:
    csv_path: Path
    markdown_path: Path
    row_count: int


def estimate_model_panel_costs(inputs: ModelPanelCostInputs) -> ModelPanelCostResult:
    """Estimate costs for every planned model-panel entry without provider calls."""
    panel = yaml.safe_load(inputs.panel_path.read_text(encoding="utf-8")) or {}
    profile = str(panel.get("profile") or "hard_obvious_8x10")
    seed = int(panel.get("seed") or 20260531)
    defaults = panel.get("defaults") or {}
    rows = []
    for entry in panel.get("entries") or []:
        estimate_inputs = CostEstimateInputs(
            model=str(entry["inspect_model"]),
            profile=profile,
            seed=seed,
            data_dir=inputs.data_dir,
            summary_root=inputs.summary_root,
            settings=_generation_settings(entry, defaults),
            cache=inputs.cache,
            cache_dir=inputs.cache_dir,
        )
        estimate = inputs.estimator(estimate_inputs)
        rows.append(_row_from_estimate(entry, estimate))

    inputs.csv_path.parent.mkdir(parents=True, exist_ok=True)
    inputs.markdown_path.parent.mkdir(parents=True, exist_ok=True)
    _write_csv(inputs.csv_path, rows)
    inputs.markdown_path.write_text(_render_markdown(rows), encoding="utf-8")
    return ModelPanelCostResult(
        csv_path=inputs.csv_path,
        markdown_path=inputs.markdown_path,
        row_count=len(rows),
    )


def _generation_settings(
    entry: dict[str, Any],
    defaults: dict[str, Any] | None = None,
) -> dict[str, str]:
    settings: dict[str, Any] = {}
    for source in (defaults or {}, entry):
        settings.update(
            {
                str(key): value
                for key, value in (source.get("generation_settings") or {}).items()
                if value is not None
            }
        )
        for key in _KNOWN_GENERATION_KEYS:
            if source.get(key) is not None:
                settings[key] = source[key]
        _merge_inspect_arg_generation_settings(
            settings,
            tuple(str(arg) for arg in source.get("inspect_args") or ()),
        )
    return {str(key): str(value) for key, value in settings.items() if value is not None}


def _merge_inspect_arg_generation_settings(
    settings: dict[str, Any],
    inspect_args: tuple[str, ...],
) -> None:
    args = _split_inspect_args(inspect_args)
    index = 0
    while index < len(args):
        arg = args[index]
        if not arg.startswith("--"):
            index += 1
            continue
        key_value = arg[2:]
        if "=" in key_value:
            raw_key, value = key_value.split("=", 1)
        elif index + 1 < len(args) and not args[index + 1].startswith("--"):
            raw_key = key_value
            value = args[index + 1]
            index += 1
        else:
            raw_key = key_value
            value = None
        setting_key = _INSPECT_ARG_GENERATION_SETTINGS.get(raw_key)
        if setting_key is not None and value is not None:
            settings[setting_key] = value
        index += 1


def _split_inspect_args(inspect_args: tuple[str, ...]) -> list[str]:
    args: list[str] = []
    for arg in inspect_args:
        args.extend(shlex.split(arg))
    return args


def _row_from_estimate(entry: dict[str, Any], estimate: CostEstimate) -> dict[str, str]:
    estimated_cost, pricing_source, warnings = _cost_from_estimate(entry, estimate)
    return {
        "id": str(entry["id"]),
        "label": str(entry["label"]),
        "provider_route": str(entry["provider_route"]),
        "inspect_model": str(entry["inspect_model"]),
        "total_samples": str(estimate.total_samples),
        "billable_samples": str(estimate.billable_samples),
        "cache_hits": str(estimate.cache_hits),
        "estimated_billable_cost_usd": _cost_cell(estimated_cost),
        "pricing_source": pricing_source,
        "warnings": "; ".join(warnings),
    }


def _cost_from_estimate(
    entry: dict[str, Any],
    estimate: CostEstimate,
) -> tuple[float | None, str, tuple[str, ...]]:
    warnings = tuple(str(warning) for warning in estimate.warnings)
    if not _needs_panel_price_fallback(warnings):
        return (
            estimate.estimated_billable_cost_usd,
            str(estimate.pricing_source),
            warnings,
        )

    input_price = _optional_float(entry.get("input_price_per_mtok_usd"))
    output_price = _optional_float(entry.get("output_price_per_mtok_usd"))
    if input_price is None or output_price is None:
        return (
            estimate.estimated_billable_cost_usd,
            str(estimate.pricing_source),
            warnings,
        )

    cost = 0.0
    for row in estimate.rows:
        if getattr(row, "cache_hit", False):
            continue
        input_tokens = int(getattr(row, "input_tokens", 0) or 0)
        output_tokens = int(getattr(row, "output_tokens", 0) or 0)
        reasoning_tokens = int(getattr(row, "reasoning_tokens", 0) or 0)
        cost += (input_tokens * input_price) / 1_000_000
        cost += ((output_tokens + reasoning_tokens) * output_price) / 1_000_000

    cleaned_warnings = tuple(
        warning for warning in warnings if "No price card found" not in warning
    )
    return (
        cost,
        "panel_price_metadata",
        cleaned_warnings
        + ("runcost price card missing; used panel price metadata",),
    )


def _needs_panel_price_fallback(warnings: tuple[str, ...]) -> bool:
    return any("No price card found" in warning for warning in warnings)


def _optional_float(value: Any) -> float | None:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    fieldnames = [
        "id",
        "label",
        "provider_route",
        "inspect_model",
        "total_samples",
        "billable_samples",
        "cache_hits",
        "estimated_billable_cost_usd",
        "pricing_source",
        "warnings",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def _render_markdown(rows: list[dict[str, str]]) -> str:
    lines = [
        "---",
        "title: Paper V1 Model Panel Cost Estimates",
        "date: 2026-06-01",
        "type: research",
        "status: draft",
        "---",
        "",
        "# Paper V1 Model Panel Cost Estimates",
        "",
        "Dry-run estimates only. No model provider calls were made.",
        "",
        "| Model | Inspect model | Samples | Billable | Estimated cost | Pricing source |",
        "| --- | --- | ---: | ---: | ---: | --- |",
    ]
    for row in rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    _markdown_cell(row["label"]),
                    _markdown_cell(row["inspect_model"]),
                    row["total_samples"],
                    row["billable_samples"],
                    f"${row['estimated_billable_cost_usd']}",
                    _markdown_cell(row["pricing_source"]),
                ]
            )
            + " |"
        )
    warnings = [row for row in rows if row["warnings"]]
    if warnings:
        lines.extend(["", "## Warnings", ""])
        for row in warnings:
            lines.append(f"- `{row['id']}`: {row['warnings']}")
    lines.append("")
    return "\n".join(lines)


def _cost_cell(value: float | None) -> str:
    if value is None:
        return "unknown"
    return f"{value:.6f}"


def _markdown_cell(value: str) -> str:
    return value.replace("|", "\\|")
