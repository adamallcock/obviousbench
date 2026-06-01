"""Helpers for retrying provider errors returned as assistant text."""

from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path

from inspect_ai.log import read_eval_log

from obviousbench.provider_errors import is_provider_transient_output


def provider_refusal_sample_ids(
    log_dir: Path,
    sample_ids: Sequence[str] | None = None,
    *,
    existing_logs: set[Path] | None = None,
) -> list[str]:
    """Return sample ids with provider error text in newly written eval logs."""
    existing_logs = existing_logs or set()
    candidate_ids = set(sample_ids) if sample_ids is not None else None
    refused: set[str] = set()
    seen_order: list[str] = []
    seen_ids: set[str] = set()
    for log_file in sorted(log_dir.rglob("*.eval")):
        if log_file in existing_logs:
            continue
        eval_log = read_eval_log(log_file)
        for sample in eval_log.samples or []:
            sample_id = str(sample.id)
            if candidate_ids is not None and sample_id not in candidate_ids:
                continue
            if sample_id not in seen_ids:
                seen_order.append(sample_id)
                seen_ids.add(sample_id)
            if is_provider_transient_output(sample.output.completion):
                refused.add(sample_id)
    if sample_ids is not None:
        return [sample_id for sample_id in sample_ids if sample_id in refused]
    return [sample_id for sample_id in seen_order if sample_id in refused]
