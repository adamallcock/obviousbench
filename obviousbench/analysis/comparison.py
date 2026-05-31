"""Aggregate per-run summaries into model comparison artifacts."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

XAI_INPUT_PER_MILLION = 1.25
XAI_CACHED_INPUT_PER_MILLION = 0.20
XAI_OUTPUT_PER_MILLION = 2.50
XAI_COST_SOURCE = "xai_docs_2026-05-31"


@dataclass(frozen=True)
class ComparisonBuildInputs:
    manifest: Path
    output_dir: Path
    summary_root: Path | None = None
    baseline_comparison: Path | None = None
    manual_xai_costs: bool = False


@dataclass(frozen=True)
class ComparisonBuildPaths:
    comparison: Path
    family_comparison: Path
    section_comparison: Path
    delta: Path


COMPARISON_FIELDS = [
    "label",
    "model",
    "barrage_profile",
    "reasoning_effort",
    "reasoning_summary",
    "total_samples",
    "scored_samples",
    "correct",
    "failures",
    "answer_correct",
    "format_correct",
    "strict_correct",
    "provider_errors",
    "timeouts",
    "accuracy",
    "answer_accuracy",
    "format_accuracy",
    "strict_accuracy",
    "obvious_failure_rate",
    "failures_per_1000",
    "non_answers",
    "format_failures",
    "input_tokens",
    "output_tokens",
    "reasoning_tokens",
    "cache_read_tokens",
    "cache_write_tokens",
    "total_tokens",
    "estimated_cost_usd",
    "cost_source",
    "cost_warnings",
    "summary_dir",
]

FAMILY_COMPARISON_FIELDS = [
    "label",
    "model",
    "barrage_profile",
    "reasoning_effort",
    "reasoning_summary",
    "family",
    "samples",
    "correct",
    "failures",
    "answer_correct",
    "format_correct",
    "strict_correct",
    "input_tokens",
    "output_tokens",
    "reasoning_tokens",
    "cache_read_tokens",
    "cache_write_tokens",
    "total_tokens",
    "estimated_cost_usd",
    "cost_source",
    "cost_warnings",
    "summary_dir",
]

SECTION_COMPARISON_FIELDS = [
    "label",
    "model",
    "barrage_profile",
    "reasoning_effort",
    "reasoning_summary",
    "family",
    "subfamily",
    "samples",
    "correct",
    "failures",
    "answer_correct",
    "format_correct",
    "strict_correct",
    "input_tokens",
    "output_tokens",
    "reasoning_tokens",
    "cache_read_tokens",
    "cache_write_tokens",
    "total_tokens",
    "estimated_cost_usd",
    "cost_source",
    "cost_warnings",
    "summary_dir",
]

DELTA_FIELDS = [
    "label",
    "model",
    "old_correct",
    "new_correct",
    "correct_delta",
    "old_answer_correct",
    "new_answer_correct",
    "answer_correct_delta",
    "old_format_correct",
    "new_format_correct",
    "format_correct_delta",
    "old_strict_correct",
    "new_strict_correct",
    "strict_correct_delta",
    "old_accuracy",
    "new_accuracy",
    "accuracy_delta",
    "old_answer_accuracy",
    "new_answer_accuracy",
    "answer_accuracy_delta",
    "old_format_accuracy",
    "new_format_accuracy",
    "format_accuracy_delta",
    "old_strict_accuracy",
    "new_strict_accuracy",
    "strict_accuracy_delta",
    "old_failures",
    "new_failures",
    "failures_delta",
    "summary_dir",
]


def build_comparison_from_manifest(
    inputs: ComparisonBuildInputs,
) -> ComparisonBuildPaths:
    """Build comparison CSVs from a manifest containing labels and summary dirs."""
    inputs.output_dir.mkdir(parents=True, exist_ok=True)

    manifest_rows = _read_csv(inputs.manifest)
    comparison_rows: list[dict[str, str]] = []
    family_rows: list[dict[str, str]] = []
    section_rows: list[dict[str, str]] = []

    for manifest_row in manifest_rows:
        summary_dir = _resolve_summary_dir(
            raw=manifest_row.get("summary_dir", ""),
            manifest_path=inputs.manifest,
            summary_root=inputs.summary_root,
        )
        summary = _first_row(summary_dir / "summary.csv")
        summary = dict(summary)
        label = manifest_row.get("label") or summary.get("model") or summary_dir.name
        context = {
            "label": label,
            "summary_dir": str(summary_dir),
            "barrage_profile": summary.get("barrage_profile", ""),
            "reasoning_effort": summary.get("reasoning_effort", ""),
            "reasoning_summary": summary.get("reasoning_summary", ""),
        }
        if inputs.manual_xai_costs:
            _apply_manual_xai_cost(summary)
        comparison_rows.append(_project_row({**summary, **context}, COMPARISON_FIELDS))

        for family_row in _read_csv(summary_dir / "usage_by_family.csv"):
            merged = {**family_row, **context}
            if inputs.manual_xai_costs:
                _apply_manual_xai_cost(merged)
            family_rows.append(_project_row(merged, FAMILY_COMPARISON_FIELDS))

        for section_row in _read_csv(summary_dir / "usage_by_section.csv"):
            merged = {**section_row, **context}
            if inputs.manual_xai_costs:
                _apply_manual_xai_cost(merged)
            section_rows.append(_project_row(merged, SECTION_COMPARISON_FIELDS))

    paths = ComparisonBuildPaths(
        comparison=inputs.output_dir / "comparison.csv",
        family_comparison=inputs.output_dir / "family_comparison.csv",
        section_comparison=inputs.output_dir / "section_comparison.csv",
        delta=inputs.output_dir / "delta.csv",
    )
    _write_csv(paths.comparison, comparison_rows, COMPARISON_FIELDS)
    _write_csv(paths.family_comparison, family_rows, FAMILY_COMPARISON_FIELDS)
    _write_csv(paths.section_comparison, section_rows, SECTION_COMPARISON_FIELDS)
    _write_csv(
        paths.delta,
        _delta_rows(inputs.baseline_comparison, comparison_rows),
        DELTA_FIELDS,
    )
    return paths


def _resolve_summary_dir(
    *,
    raw: str,
    manifest_path: Path,
    summary_root: Path | None,
) -> Path:
    if not raw:
        raise ValueError("Manifest row is missing summary_dir")
    path = Path(raw)
    if summary_root is not None:
        return summary_root / path.name
    if path.is_absolute():
        return path
    manifest_relative = manifest_path.parent / path
    if manifest_relative.exists():
        return manifest_relative
    return path


def _first_row(path: Path) -> dict[str, str]:
    rows = _read_csv(path)
    if not rows:
        raise ValueError(f"Expected at least one row in {path}")
    return rows[0]


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _write_csv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def _project_row(row: dict[str, str], fields: list[str]) -> dict[str, str]:
    return {field: row.get(field, "") for field in fields}


def _apply_manual_xai_cost(row: dict[str, str]) -> None:
    model = row.get("model", "")
    if not model.startswith("grok/"):
        return
    cost = (
        _float(row.get("input_tokens")) * XAI_INPUT_PER_MILLION
        + _float(row.get("cache_read_tokens")) * XAI_CACHED_INPUT_PER_MILLION
        + (
            _float(row.get("output_tokens"))
            + _float(row.get("reasoning_tokens"))
        )
        * XAI_OUTPUT_PER_MILLION
    ) / 1_000_000
    row["estimated_cost_usd"] = _format_decimal(cost)
    row["cost_source"] = XAI_COST_SOURCE
    row["cost_warnings"] = ""


def _delta_rows(
    baseline_comparison: Path | None,
    comparison_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    if baseline_comparison is None:
        return []
    baseline_by_label = {
        row.get("label", ""): row for row in _read_csv(baseline_comparison)
    }
    rows: list[dict[str, str]] = []
    for new in comparison_rows:
        label = new.get("label", "")
        old = baseline_by_label.get(label)
        if old is None:
            continue
        rows.append(
            {
                "label": label,
                "model": new.get("model", ""),
                "old_correct": _metric(old, "correct"),
                "new_correct": _metric(new, "correct"),
                "correct_delta": _int_delta(old, new, "correct"),
                "old_answer_correct": _metric(old, "answer_correct", fallback="correct"),
                "new_answer_correct": _metric(new, "answer_correct", fallback="correct"),
                "answer_correct_delta": _int_delta(
                    old,
                    new,
                    "answer_correct",
                    fallback="correct",
                ),
                "old_format_correct": _metric(old, "format_correct", fallback="correct"),
                "new_format_correct": _metric(new, "format_correct", fallback="correct"),
                "format_correct_delta": _int_delta(
                    old,
                    new,
                    "format_correct",
                    fallback="correct",
                ),
                "old_strict_correct": _metric(old, "strict_correct", fallback="correct"),
                "new_strict_correct": _metric(new, "strict_correct", fallback="correct"),
                "strict_correct_delta": _int_delta(
                    old,
                    new,
                    "strict_correct",
                    fallback="correct",
                ),
                "old_accuracy": _metric(old, "accuracy"),
                "new_accuracy": _metric(new, "accuracy"),
                "accuracy_delta": _float_delta(old, new, "accuracy"),
                "old_answer_accuracy": _metric(
                    old,
                    "answer_accuracy",
                    fallback="accuracy",
                ),
                "new_answer_accuracy": _metric(
                    new,
                    "answer_accuracy",
                    fallback="accuracy",
                ),
                "answer_accuracy_delta": _float_delta(
                    old,
                    new,
                    "answer_accuracy",
                    fallback="accuracy",
                ),
                "old_format_accuracy": _metric(
                    old,
                    "format_accuracy",
                    fallback="accuracy",
                ),
                "new_format_accuracy": _metric(
                    new,
                    "format_accuracy",
                    fallback="accuracy",
                ),
                "format_accuracy_delta": _float_delta(
                    old,
                    new,
                    "format_accuracy",
                    fallback="accuracy",
                ),
                "old_strict_accuracy": _metric(
                    old,
                    "strict_accuracy",
                    fallback="accuracy",
                ),
                "new_strict_accuracy": _metric(
                    new,
                    "strict_accuracy",
                    fallback="accuracy",
                ),
                "strict_accuracy_delta": _float_delta(
                    old,
                    new,
                    "strict_accuracy",
                    fallback="accuracy",
                ),
                "old_failures": _metric(old, "failures"),
                "new_failures": _metric(new, "failures"),
                "failures_delta": _int_delta(old, new, "failures"),
                "summary_dir": new.get("summary_dir", ""),
            }
        )
    return rows


def _metric(row: dict[str, str], field: str, *, fallback: str | None = None) -> str:
    value = row.get(field, "")
    if value != "":
        return value
    if fallback is not None:
        return row.get(fallback, "")
    return ""


def _int_delta(
    old: dict[str, str],
    new: dict[str, str],
    field: str,
    *,
    fallback: str | None = None,
) -> str:
    old_value = int(_float(_metric(old, field, fallback=fallback)))
    new_value = int(_float(_metric(new, field, fallback=fallback)))
    return str(new_value - old_value)


def _float_delta(
    old: dict[str, str],
    new: dict[str, str],
    field: str,
    *,
    fallback: str | None = None,
) -> str:
    return _format_decimal(
        _float(_metric(new, field, fallback=fallback))
        - _float(_metric(old, field, fallback=fallback))
    )


def _float(value: str | None) -> float:
    if value in (None, ""):
        return 0.0
    return float(value)


def _format_decimal(value: float) -> str:
    return f"{value:.12f}".rstrip("0").rstrip(".")
