"""Token usage and cost artifact helpers."""

from __future__ import annotations

import csv
import json
from collections import defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from obviousbench.analysis.efficiency import (
    cost_per_correct_usd,
    overthinking_index,
    reasoning_token_share,
    safe_ratio,
    tokens_per_correct,
)
from obviousbench.analysis.metrics import EvalRecord


@dataclass(frozen=True)
class UsageBreakdownRow:
    run_variant: str
    model: str
    family: str
    subfamily: str
    sample_id: str
    question: str
    samples: int
    scored_samples: int
    provider_errors: int
    timeouts: int
    correct: int
    failures: int
    answer_correct: int
    format_correct: int
    strict_correct: int
    input_tokens: int
    output_tokens: int
    reasoning_tokens: int
    cache_read_tokens: int
    cache_write_tokens: int
    total_tokens: int
    estimated_cost_usd: float | None
    tokens_per_scored_sample: float | None
    tokens_per_correct: float | None
    cost_per_correct_usd: float | None
    reasoning_token_share: float | None
    overthinking_index: float | None
    cost_source: str
    cost_warnings: str


UsageByFamilyRow = UsageBreakdownRow
UsageBySectionRow = UsageBreakdownRow
UsageByQuestionRow = UsageBreakdownRow


def export_usage_by_sample_csv(records: list[EvalRecord], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "run_variant",
        "model",
        "barrage_profile",
        "barrage_seed",
        "reasoning_effort",
        "reasoning_summary",
        "sample_id",
        "family",
        "subfamily",
        "question",
        "metamorphic_group_id",
        "metamorphic_role",
        "metamorphic_relation",
        "correct",
        "failure_type",
        "answer_correct",
        "format_correct",
        "strict_correct",
        "provider_error",
        "timeout",
        "input_tokens",
        "output_tokens",
        "reasoning_tokens",
        "cache_read_tokens",
        "cache_write_tokens",
        "total_tokens",
        "estimated_cost_usd",
        "cost_source",
        "cost_warnings",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for record in records:
            writer.writerow(
                {
                    "run_variant": record.run_variant,
                    "model": record.model,
                    "barrage_profile": record.barrage_profile,
                    "barrage_seed": record.barrage_seed,
                    "reasoning_effort": record.reasoning_effort,
                    "reasoning_summary": record.reasoning_summary,
                    "sample_id": record.sample_id,
                    "family": record.family,
                    "subfamily": record.subfamily,
                    "question": record.question,
                    "metamorphic_group_id": record.metamorphic_group_id,
                    "metamorphic_role": record.metamorphic_role,
                    "metamorphic_relation": record.metamorphic_relation,
                    "correct": record.correct,
                    "failure_type": record.failure_type,
                    "answer_correct": record.answer_ok,
                    "format_correct": record.format_ok,
                    "strict_correct": record.strict_ok,
                    "provider_error": record.provider_error,
                    "timeout": record.timeout,
                    "input_tokens": record.input_tokens,
                    "output_tokens": record.output_tokens,
                    "reasoning_tokens": record.reasoning_tokens,
                    "cache_read_tokens": record.cache_read_tokens,
                    "cache_write_tokens": record.cache_write_tokens,
                    "total_tokens": record.total_tokens,
                    "estimated_cost_usd": record.estimated_cost_usd,
                    "cost_source": record.cost_source or "",
                    "cost_warnings": record.cost_warnings,
                }
            )


def compute_usage_by_family(records: list[EvalRecord]) -> list[UsageByFamilyRow]:
    return _compute_breakdown(records, "family")


def compute_usage_by_section(records: list[EvalRecord]) -> list[UsageBySectionRow]:
    return _compute_breakdown(records, "section")


def compute_usage_by_question(records: list[EvalRecord]) -> list[UsageByQuestionRow]:
    return _compute_breakdown(records, "question")


def _compute_breakdown(
    records: list[EvalRecord],
    level: str,
) -> list[UsageBreakdownRow]:
    grouped: dict[tuple[str, ...], list[EvalRecord]] = defaultdict(list)
    for record in records:
        if level == "family":
            key = (record.run_variant, record.family)
        elif level == "section":
            key = (record.run_variant, record.family, record.subfamily)
        elif level == "question":
            key = (
                record.run_variant,
                record.family,
                record.subfamily,
                record.sample_id,
                record.question,
            )
        else:
            raise ValueError(f"Unknown usage breakdown level: {level}")
        grouped[key].append(record)

    rows: list[UsageBreakdownRow] = []
    for _key, family_records in sorted(grouped.items()):
        first = family_records[0]
        scored_records = family_records
        costs = [
            record.estimated_cost_usd
            for record in family_records
            if record.estimated_cost_usd is not None
        ]
        correct = sum(record.correct for record in scored_records)
        output_tokens = sum(record.output_tokens for record in family_records)
        reasoning_tokens = sum(record.reasoning_tokens for record in family_records)
        total_tokens = sum(record.total_tokens for record in family_records)
        scored_count = len(scored_records)
        estimated_cost_usd = round(sum(costs), 12) if costs else None
        rows.append(
            UsageBreakdownRow(
                run_variant=first.run_variant,
                model=first.model,
                family=first.family,
                subfamily=first.subfamily if level in {"section", "question"} else "",
                sample_id=first.sample_id if level == "question" else "",
                question=first.question if level == "question" else "",
                samples=len(family_records),
                scored_samples=scored_count,
                provider_errors=sum(record.provider_error for record in family_records),
                timeouts=sum(record.timeout for record in family_records),
                correct=correct,
                failures=scored_count - correct,
                answer_correct=sum(record.answer_ok for record in scored_records),
                format_correct=sum(record.format_ok for record in scored_records),
                strict_correct=sum(record.strict_ok for record in scored_records),
                input_tokens=sum(record.input_tokens for record in family_records),
                output_tokens=output_tokens,
                reasoning_tokens=reasoning_tokens,
                cache_read_tokens=sum(
                    record.cache_read_tokens for record in family_records
                ),
                cache_write_tokens=sum(
                    record.cache_write_tokens for record in family_records
                ),
                total_tokens=total_tokens,
                estimated_cost_usd=estimated_cost_usd,
                tokens_per_scored_sample=safe_ratio(total_tokens, scored_count),
                tokens_per_correct=tokens_per_correct(
                    total_tokens=total_tokens,
                    correct=correct,
                ),
                cost_per_correct_usd=cost_per_correct_usd(
                    estimated_cost_usd=estimated_cost_usd,
                    correct=correct,
                ),
                reasoning_token_share=reasoning_token_share(
                    reasoning_tokens=reasoning_tokens,
                    total_tokens=total_tokens,
                ),
                overthinking_index=overthinking_index(
                    reasoning_tokens=reasoning_tokens,
                    output_tokens=output_tokens,
                ),
                cost_source=_join_unique(
                    record.cost_source for record in family_records
                ),
                cost_warnings=_join_unique(
                    record.cost_warnings for record in family_records
                ),
            )
        )
    return rows


def export_usage_by_family_csv(rows: list[UsageByFamilyRow], path: Path) -> None:
    _export_breakdown_csv(
        rows,
        path,
        [
            "run_variant",
            "model",
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
        ],
    )


def export_usage_by_section_csv(rows: list[UsageBySectionRow], path: Path) -> None:
    _export_breakdown_csv(
        rows,
        path,
        [
            "run_variant",
            "model",
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
        ],
    )


def export_usage_by_question_csv(rows: list[UsageByQuestionRow], path: Path) -> None:
    _export_breakdown_csv(
        rows,
        path,
        [
            "run_variant",
            "model",
            "family",
            "subfamily",
            "sample_id",
            "question",
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
        ],
    )


def _export_breakdown_csv(
    rows: list[UsageBreakdownRow],
    path: Path,
    fieldnames: list[str],
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            data = asdict(row)
            writer.writerow({field: data[field] for field in fieldnames})


def build_cost_input(records: list[EvalRecord]) -> dict[str, Any]:
    return {
        "records": [
            {
                "sample_id": record.sample_id,
                "model": record.model,
                "provider": _provider_from_model(record.model),
                "surface": "normalized.usage",
                "usage": {
                    "input_tokens": record.input_tokens,
                    "output_tokens": record.output_tokens,
                    "reasoning_tokens": record.reasoning_tokens,
                    "cache_read_tokens": record.cache_read_tokens,
                    "cache_write_tokens": record.cache_write_tokens,
                    "total_tokens": record.total_tokens,
                },
            }
            for record in records
        ]
    }


def write_cost_ledger(ledger: dict[str, Any], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(ledger, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _provider_from_model(model: str) -> str:
    return model.split("/", 1)[0] if "/" in model else "unknown"


def _join_unique(values) -> str:
    unique = sorted({str(value) for value in values if value})
    return "; ".join(unique)
