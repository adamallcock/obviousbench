"""Cost pricing integration for normalized Inspect usage."""

from __future__ import annotations

import json
import subprocess
from dataclasses import replace
from pathlib import Path
from typing import Any

from obviousbench.analysis.metrics import EvalRecord
from obviousbench.analysis.usage import build_cost_input

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def price_records_with_runcost(
    records: list[EvalRecord],
) -> tuple[list[EvalRecord], dict[str, Any]]:
    """Price normalized usage via the local Node runcost bridge."""
    payload = build_cost_input(records)
    result = subprocess.run(
        ["node", str(PROJECT_ROOT / "scripts" / "runners" / "price_usage_with_runcost.mjs")],
        input=json.dumps(payload),
        capture_output=True,
        text=True,
        check=True,
        cwd=PROJECT_ROOT,
    )
    ledger = json.loads(result.stdout)
    return apply_cost_ledger(records, ledger), ledger


def apply_cost_ledger(records: list[EvalRecord], ledger: dict[str, Any]) -> list[EvalRecord]:
    by_sample_id = {
        str(entry.get("sample_id")): entry for entry in ledger.get("records", [])
    }
    priced: list[EvalRecord] = []
    for record in records:
        entry = by_sample_id.get(record.sample_id)
        if entry is None:
            priced.append(record)
            continue
        priced.append(
            replace(
                record,
                estimated_cost_usd=_optional_float(entry.get("estimated_cost_usd")),
                cost_source=str(entry.get("cost_source") or ""),
                cost_warnings=_warning_messages(entry.get("warnings") or []),
            )
        )
    return priced


def _optional_float(value) -> float | None:
    if value in {None, ""}:
        return None
    return float(value)


def _warning_messages(warnings: list[Any]) -> str:
    messages: list[str] = []
    for warning in warnings:
        if isinstance(warning, dict):
            message = warning.get("message") or warning.get("code")
        else:
            message = str(warning)
        if message:
            messages.append(str(message))
    return "; ".join(sorted(set(messages)))
