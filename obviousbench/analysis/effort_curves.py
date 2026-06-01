"""Build effort-curve rows for comparing reasoning effort profiles."""

from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path

EFFORT_CURVE_FIELDS = [
    "model_base",
    "barrage_profile",
    "reasoning_summary",
    "effort_order",
    "reasoning_effort",
    "accuracy",
    "strict_accuracy",
    "total_tokens",
    "reasoning_tokens",
    "estimated_cost_usd",
    "accuracy_delta_from_min_effort",
    "token_delta_from_min_effort",
    "cost_delta_from_min_effort",
    "efficiency_warning",
]

_EFFORT_ORDER = {
    "none": 0,
    "minimal": 0,
    "low": 1,
    "medium": 2,
    "high": 3,
}


def build_effort_curve_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    grouped: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        key = (
            _model_base(row.get("model", "")),
            row.get("barrage_profile", ""),
        )
        grouped[key].append(row)

    effort_rows: list[dict[str, str]] = []
    for key, group_rows in sorted(grouped.items()):
        sorted_group = sorted(
            group_rows,
            key=lambda row: (
                _effort_order(row.get("reasoning_effort", "")),
                row.get("reasoning_effort", ""),
            ),
        )
        baseline = sorted_group[0]
        baseline_accuracy = _float(baseline.get("accuracy"))
        baseline_tokens = _int(baseline.get("total_tokens"))
        baseline_cost = _optional_float(baseline.get("estimated_cost_usd"))
        for row in sorted_group:
            accuracy = _float(row.get("accuracy"))
            total_tokens = _int(row.get("total_tokens"))
            cost = _optional_float(row.get("estimated_cost_usd"))
            effort_rows.append(
                {
                    "model_base": key[0],
                    "barrage_profile": key[1],
                    "reasoning_summary": row.get("reasoning_summary", ""),
                    "effort_order": str(_effort_order(row.get("reasoning_effort", ""))),
                    "reasoning_effort": row.get("reasoning_effort", ""),
                    "accuracy": row.get("accuracy", ""),
                    "strict_accuracy": row.get("strict_accuracy", ""),
                    "total_tokens": row.get("total_tokens", ""),
                    "reasoning_tokens": row.get("reasoning_tokens", ""),
                    "estimated_cost_usd": row.get("estimated_cost_usd", ""),
                    "accuracy_delta_from_min_effort": _format_decimal(
                        accuracy - baseline_accuracy
                    ),
                    "token_delta_from_min_effort": str(total_tokens - baseline_tokens),
                    "cost_delta_from_min_effort": _format_optional_decimal(
                        None
                        if cost is None or baseline_cost is None
                        else cost - baseline_cost
                    ),
                    "efficiency_warning": _efficiency_warning(
                        accuracy=accuracy,
                        baseline_accuracy=baseline_accuracy,
                        total_tokens=total_tokens,
                        baseline_tokens=baseline_tokens,
                        cost=cost,
                        baseline_cost=baseline_cost,
                    ),
                }
            )
    return effort_rows


def write_effort_curve_csv(rows: list[dict[str, str]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=EFFORT_CURVE_FIELDS, lineterminator="\n"
        )
        writer.writeheader()
        writer.writerows(rows)


def _model_base(model: str) -> str:
    for suffix in ("-minimal", "-low", "-medium", "-high", "-none"):
        if model.endswith(suffix):
            return model[: -len(suffix)]
    return model


def _effort_order(reasoning_effort: str) -> int:
    normalized = reasoning_effort.strip().lower()
    return _EFFORT_ORDER.get(normalized, 99)


def _efficiency_warning(
    *,
    accuracy: float,
    baseline_accuracy: float,
    total_tokens: int,
    baseline_tokens: int,
    cost: float | None,
    baseline_cost: float | None,
) -> str:
    if total_tokens > baseline_tokens and accuracy < baseline_accuracy:
        return "higher_tokens_lower_accuracy"
    if (
        cost is not None
        and baseline_cost is not None
        and cost > baseline_cost
        and accuracy <= baseline_accuracy
    ):
        return "higher_cost_no_accuracy_gain"
    return ""


def _optional_float(value: str | None) -> float | None:
    if value in (None, ""):
        return None
    return float(value)


def _float(value: str | None) -> float:
    return _optional_float(value) or 0.0


def _int(value: str | None) -> int:
    return int(_float(value))


def _format_optional_decimal(value: float | None) -> str:
    return "" if value is None else _format_decimal(value)


def _format_decimal(value: float) -> str:
    return f"{value:.6f}".rstrip("0").rstrip(".")
