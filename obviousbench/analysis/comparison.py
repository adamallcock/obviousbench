"""Aggregate per-run summaries into model comparison artifacts."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

from obviousbench.analysis.efficiency import (
    cost_per_correct_usd,
    overthinking_index,
    reasoning_token_share,
    safe_ratio,
    tokens_per_correct,
)
from obviousbench.analysis.effort_curves import (
    EFFORT_CURVE_FIELDS,
    build_effort_curve_rows,
)
from obviousbench.analysis.statistics import paired_boolean_delta, wilson_interval

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
    effort_curve: Path
    metamorphic_consistency: Path
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
    "accuracy_ci_low",
    "accuracy_ci_high",
    "answer_accuracy",
    "answer_accuracy_ci_low",
    "answer_accuracy_ci_high",
    "format_accuracy",
    "strict_accuracy",
    "strict_accuracy_ci_low",
    "strict_accuracy_ci_high",
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
    "tokens_per_scored_sample",
    "output_tokens_per_scored_sample",
    "reasoning_tokens_per_scored_sample",
    "tokens_per_correct",
    "cost_per_correct_usd",
    "reasoning_token_share",
    "overthinking_index",
    "reasoning_token_source",
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
    "scored_samples",
    "provider_errors",
    "timeouts",
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
    "tokens_per_scored_sample",
    "tokens_per_correct",
    "cost_per_correct_usd",
    "reasoning_token_share",
    "overthinking_index",
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
    "scored_samples",
    "provider_errors",
    "timeouts",
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
    "tokens_per_scored_sample",
    "tokens_per_correct",
    "cost_per_correct_usd",
    "reasoning_token_share",
    "overthinking_index",
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
    "delta_method",
    "matched_samples",
    "baseline_only_samples",
    "comparison_only_samples",
    "paired_wins",
    "paired_losses",
    "paired_ties",
    "paired_accuracy_delta",
    "paired_accuracy_ci_low",
    "paired_accuracy_ci_high",
    "summary_dir",
]

METAMORPHIC_COMPARISON_FIELDS = [
    "label",
    "model",
    "barrage_profile",
    "reasoning_effort",
    "reasoning_summary",
    "family",
    "groups",
    "samples",
    "scored_samples",
    "assessable_groups",
    "unassessable_groups",
    "consistent_groups",
    "inconsistent_groups",
    "mixed_outcome_groups",
    "consistency_rate",
    "mixed_group_ids",
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
    metamorphic_rows: list[dict[str, str]] = []

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
        _backfill_ci_fields(summary)
        _backfill_efficiency_fields(summary)
        comparison_rows.append(_project_row({**summary, **context}, COMPARISON_FIELDS))

        for family_row in _read_csv(summary_dir / "usage_by_family.csv"):
            merged = {**family_row, **context}
            if inputs.manual_xai_costs:
                _apply_manual_xai_cost(merged)
            _backfill_usage_efficiency_fields(merged)
            family_rows.append(_project_row(merged, FAMILY_COMPARISON_FIELDS))

        for section_row in _read_csv(summary_dir / "usage_by_section.csv"):
            merged = {**section_row, **context}
            if inputs.manual_xai_costs:
                _apply_manual_xai_cost(merged)
            _backfill_usage_efficiency_fields(merged)
            section_rows.append(_project_row(merged, SECTION_COMPARISON_FIELDS))

        metamorphic_rows.extend(
            _metamorphic_comparison_rows(summary_dir, summary, context)
        )

    paths = ComparisonBuildPaths(
        comparison=inputs.output_dir / "comparison.csv",
        family_comparison=inputs.output_dir / "family_comparison.csv",
        section_comparison=inputs.output_dir / "section_comparison.csv",
        effort_curve=inputs.output_dir / "effort_curve.csv",
        metamorphic_consistency=inputs.output_dir / "metamorphic_consistency.csv",
        delta=inputs.output_dir / "delta.csv",
    )
    _write_csv(paths.comparison, comparison_rows, COMPARISON_FIELDS)
    _write_csv(paths.family_comparison, family_rows, FAMILY_COMPARISON_FIELDS)
    _write_csv(paths.section_comparison, section_rows, SECTION_COMPARISON_FIELDS)
    _write_csv(
        paths.effort_curve,
        build_effort_curve_rows(comparison_rows),
        EFFORT_CURVE_FIELDS,
    )
    _write_csv(
        paths.metamorphic_consistency,
        metamorphic_rows,
        METAMORPHIC_COMPARISON_FIELDS,
    )
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


def _read_optional_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    return _read_csv(path)


def _write_csv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def _metamorphic_comparison_rows(
    summary_dir: Path,
    summary: dict[str, str],
    context: dict[str, str],
) -> list[dict[str, str]]:
    rows = _read_optional_csv(summary_dir / "metamorphic_consistency.csv")
    grouped: dict[str, list[dict[str, str]]] = {}
    for row in rows:
        grouped.setdefault(row.get("family", ""), []).append(row)

    comparison_rows: list[dict[str, str]] = []
    for family, family_rows in sorted(grouped.items()):
        groups = len(family_rows)
        samples = sum(int(_float(row.get("samples"))) for row in family_rows)
        scored_samples = sum(
            int(_float(row.get("scored_samples"))) for row in family_rows
        )
        assessable_rows = [row for row in family_rows if _truthy(row.get("assessable"))]
        assessable_groups = len(assessable_rows)
        consistent_groups = sum(_truthy(row.get("consistent")) for row in assessable_rows)
        mixed_rows = [row for row in family_rows if _truthy(row.get("mixed_outcomes"))]
        mixed_group_ids = [
            row.get("metamorphic_group_id", "")
            for row in mixed_rows
            if row.get("metamorphic_group_id", "")
        ]
        comparison_rows.append(
            {
                **context,
                "model": summary.get("model", ""),
                "family": family,
                "groups": str(groups),
                "samples": str(samples),
                "scored_samples": str(scored_samples),
                "assessable_groups": str(assessable_groups),
                "unassessable_groups": str(groups - assessable_groups),
                "consistent_groups": str(consistent_groups),
                "inconsistent_groups": str(assessable_groups - consistent_groups),
                "mixed_outcome_groups": str(len(mixed_rows)),
                "consistency_rate": (
                    _format_decimal(consistent_groups / assessable_groups)
                    if assessable_groups
                    else ""
                ),
                "mixed_group_ids": ";".join(mixed_group_ids),
            }
        )
    return [
        _project_row(row, METAMORPHIC_COMPARISON_FIELDS)
        for row in comparison_rows
    ]


def _backfill_ci_fields(row: dict[str, str]) -> None:
    scored_samples = int(_float(row.get("scored_samples")))
    _backfill_interval(
        row,
        count_field="correct",
        low_field="accuracy_ci_low",
        high_field="accuracy_ci_high",
        scored_samples=scored_samples,
    )
    _backfill_interval(
        row,
        count_field="answer_correct",
        low_field="answer_accuracy_ci_low",
        high_field="answer_accuracy_ci_high",
        scored_samples=scored_samples,
        fallback_count_field="correct",
    )
    _backfill_interval(
        row,
        count_field="strict_correct",
        low_field="strict_accuracy_ci_low",
        high_field="strict_accuracy_ci_high",
        scored_samples=scored_samples,
        fallback_count_field="correct",
    )


def _backfill_interval(
    row: dict[str, str],
    *,
    count_field: str,
    low_field: str,
    high_field: str,
    scored_samples: int,
    fallback_count_field: str | None = None,
) -> None:
    if row.get(low_field) and row.get(high_field):
        return
    raw_count = row.get(count_field, "")
    if raw_count == "" and fallback_count_field is not None:
        raw_count = row.get(fallback_count_field, "")
    successes = int(_float(raw_count))
    low, high = wilson_interval(successes, scored_samples)
    row[low_field] = _format_decimal(low)
    row[high_field] = _format_decimal(high)


def _backfill_efficiency_fields(row: dict[str, str]) -> None:
    scored_samples = int(_float(row.get("scored_samples")))
    correct = int(_float(row.get("correct")))
    output_tokens = int(_float(row.get("output_tokens")))
    reasoning_tokens = int(_float(row.get("reasoning_tokens")))
    total_tokens = int(_float(row.get("total_tokens")))
    estimated_cost_usd = _optional_float(row.get("estimated_cost_usd"))
    _set_missing(
        row,
        "tokens_per_scored_sample",
        _format_optional_decimal(safe_ratio(total_tokens, scored_samples)),
    )
    _set_missing(
        row,
        "output_tokens_per_scored_sample",
        _format_optional_decimal(safe_ratio(output_tokens, scored_samples)),
    )
    _set_missing(
        row,
        "reasoning_tokens_per_scored_sample",
        _format_optional_decimal(safe_ratio(reasoning_tokens, scored_samples)),
    )
    _set_missing(
        row,
        "tokens_per_correct",
        _format_optional_decimal(
            tokens_per_correct(total_tokens=total_tokens, correct=correct)
        ),
    )
    _set_missing(
        row,
        "cost_per_correct_usd",
        _format_optional_decimal(
            cost_per_correct_usd(
                estimated_cost_usd=estimated_cost_usd,
                correct=correct,
            )
        ),
    )
    _set_missing(
        row,
        "reasoning_token_share",
        _format_optional_decimal(
            reasoning_token_share(
                reasoning_tokens=reasoning_tokens,
                total_tokens=total_tokens,
            )
        ),
    )
    _set_missing(
        row,
        "overthinking_index",
        _format_optional_decimal(
            overthinking_index(
                reasoning_tokens=reasoning_tokens,
                output_tokens=output_tokens,
            )
        ),
    )
    _set_missing(
        row,
        "reasoning_token_source",
        "reported" if reasoning_tokens else "not_reported_or_zero",
    )


def _backfill_usage_efficiency_fields(row: dict[str, str]) -> None:
    scored_samples = _optional_int(row.get("scored_samples"))
    correct = int(_float(row.get("correct")))
    output_tokens = int(_float(row.get("output_tokens")))
    reasoning_tokens = int(_float(row.get("reasoning_tokens")))
    total_tokens = int(_float(row.get("total_tokens")))
    estimated_cost_usd = _optional_float(row.get("estimated_cost_usd"))
    _set_missing(
        row,
        "tokens_per_scored_sample",
        _format_optional_decimal(safe_ratio(total_tokens, scored_samples)),
    )
    _set_missing(
        row,
        "tokens_per_correct",
        _format_optional_decimal(
            tokens_per_correct(total_tokens=total_tokens, correct=correct)
        ),
    )
    _set_missing(
        row,
        "cost_per_correct_usd",
        _format_optional_decimal(
            cost_per_correct_usd(
                estimated_cost_usd=estimated_cost_usd,
                correct=correct,
            )
        ),
    )
    _set_missing(
        row,
        "reasoning_token_share",
        _format_optional_decimal(
            reasoning_token_share(
                reasoning_tokens=reasoning_tokens,
                total_tokens=total_tokens,
            )
        ),
    )
    _set_missing(
        row,
        "overthinking_index",
        _format_optional_decimal(
            overthinking_index(
                reasoning_tokens=reasoning_tokens,
                output_tokens=output_tokens,
            )
        ),
    )


def _set_missing(row: dict[str, str], field: str, value: str) -> None:
    if row.get(field, "") == "":
        row[field] = value


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
        paired = _paired_delta_for_rows(old, new)
        paired_fields = (
            {
                "delta_method": "paired_sample",
                "matched_samples": str(paired.matched_samples),
                "baseline_only_samples": str(paired.baseline_only),
                "comparison_only_samples": str(paired.comparison_only),
                "paired_wins": str(paired.wins),
                "paired_losses": str(paired.losses),
                "paired_ties": str(paired.ties),
                "paired_accuracy_delta": _format_decimal(paired.delta),
                "paired_accuracy_ci_low": _format_decimal(paired.ci_low),
                "paired_accuracy_ci_high": _format_decimal(paired.ci_high),
            }
            if paired is not None
            else {
                "delta_method": "aggregate_unpaired",
                "matched_samples": "",
                "baseline_only_samples": "",
                "comparison_only_samples": "",
                "paired_wins": "",
                "paired_losses": "",
                "paired_ties": "",
                "paired_accuracy_delta": "",
                "paired_accuracy_ci_low": "",
                "paired_accuracy_ci_high": "",
            }
        )
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
                **paired_fields,
                "summary_dir": new.get("summary_dir", ""),
            }
        )
    return rows


def _paired_delta_for_rows(
    old: dict[str, str],
    new: dict[str, str],
):
    old_usage = _read_usage_correctness(Path(old.get("summary_dir", "")))
    new_usage = _read_usage_correctness(Path(new.get("summary_dir", "")))
    if old_usage is None or new_usage is None:
        return None
    paired = paired_boolean_delta(baseline=old_usage, comparison=new_usage)
    if paired.matched_samples == 0:
        return None
    return paired


def _read_usage_correctness(summary_dir: Path) -> dict[str, bool] | None:
    if not str(summary_dir):
        return None
    path = summary_dir / "usage_by_sample.csv"
    if not path.exists():
        return None
    rows = _read_csv(path)
    usage: dict[str, bool] = {}
    for row in rows:
        sample_id = row.get("sample_id", "")
        if sample_id and not _truthy(row.get("provider_error")) and not _truthy(row.get("timeout")):
            usage[sample_id] = _truthy(row.get("correct"))
    return usage


def _truthy(value: str | None) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


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


def _optional_float(value: str | None) -> float | None:
    if value in (None, ""):
        return None
    return float(value)


def _optional_int(value: str | None) -> int | None:
    if value in (None, ""):
        return None
    return int(_float(value))


def _format_optional_decimal(value: float | None) -> str:
    return "" if value is None else _format_decimal(value)


def _format_decimal(value: float) -> str:
    return f"{value:.6f}".rstrip("0").rstrip(".")
