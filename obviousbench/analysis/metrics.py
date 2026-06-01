"""Summary metric computation."""

from __future__ import annotations

from dataclasses import dataclass
from itertools import groupby
from typing import Any

from obviousbench.analysis.efficiency import (
    cost_per_correct_usd,
    overthinking_index,
    reasoning_token_share,
    safe_ratio,
    tokens_per_correct,
)
from obviousbench.analysis.statistics import wilson_interval
from obviousbench.scorers.common import FORMAT_FAILURE_TYPES


@dataclass(frozen=True)
class EvalRecord:
    model: str
    sample_id: str
    family: str
    correct: bool
    failure_type: str
    provider_error: bool
    timeout: bool
    subfamily: str = ""
    question: str = ""
    barrage_profile: str | None = None
    barrage_seed: int | None = None
    reasoning_effort: str | None = None
    reasoning_summary: str | None = None
    input_tokens: int = 0
    output_tokens: int = 0
    reasoning_tokens: int = 0
    cache_read_tokens: int = 0
    cache_write_tokens: int = 0
    total_tokens: int = 0
    estimated_cost_usd: float | None = None
    cost_source: str | None = None
    cost_warnings: str = ""
    answer_correct: bool | None = None
    format_correct: bool | None = None
    strict_correct: bool | None = None
    metamorphic_group_id: str = ""
    metamorphic_role: str = ""
    metamorphic_relation: str = ""

    @property
    def run_variant(self) -> str:
        return run_variant_key(
            model=self.model,
            barrage_profile=self.barrage_profile,
            barrage_seed=self.barrage_seed,
            reasoning_effort=self.reasoning_effort,
            reasoning_summary=self.reasoning_summary,
        )

    @property
    def answer_ok(self) -> bool:
        return self.correct if self.answer_correct is None else self.answer_correct

    @property
    def format_ok(self) -> bool:
        if self.format_correct is not None:
            return self.format_correct
        return self.failure_type not in FORMAT_FAILURE_TYPES

    @property
    def strict_ok(self) -> bool:
        if self.strict_correct is not None:
            return self.strict_correct
        return self.answer_ok and self.format_ok


@dataclass(frozen=True)
class SummaryRow:
    run_variant: str
    model: str
    barrage_profile: str | None
    barrage_seed: int | None
    reasoning_effort: str | None
    reasoning_summary: str | None
    total_samples: int
    scored_samples: int
    correct: int
    failures: int
    answer_correct: int
    format_correct: int
    strict_correct: int
    obvious_failure_rate: float
    accuracy: float
    accuracy_ci_low: float
    accuracy_ci_high: float
    answer_accuracy: float
    answer_accuracy_ci_low: float
    answer_accuracy_ci_high: float
    format_accuracy: float
    strict_accuracy: float
    strict_accuracy_ci_low: float
    strict_accuracy_ci_high: float
    failures_per_1000: int
    provider_errors: int
    timeouts: int
    non_answers: int
    format_failures: int
    input_tokens: int
    output_tokens: int
    reasoning_tokens: int
    cache_read_tokens: int
    cache_write_tokens: int
    total_tokens: int
    estimated_cost_usd: float | None
    tokens_per_scored_sample: float | None
    output_tokens_per_scored_sample: float | None
    reasoning_tokens_per_scored_sample: float | None
    tokens_per_correct: float | None
    cost_per_correct_usd: float | None
    reasoning_token_share: float | None
    overthinking_index: float | None
    reasoning_token_source: str
    cost_source: str
    cost_warnings: str


def run_variant_key(
    *,
    model: str,
    barrage_profile: str | None,
    barrage_seed: int | None,
    reasoning_effort: str | None,
    reasoning_summary: str | None,
) -> str:
    return (
        f"{model}|profile={barrage_profile or ''}|seed={barrage_seed or ''}|"
        f"reasoning_effort={reasoning_effort or ''}|"
        f"reasoning_summary={reasoning_summary or ''}"
    )


def compute_summary(records: list[EvalRecord]) -> list[SummaryRow]:
    rows: list[SummaryRow] = []
    sorted_records = sorted(records, key=lambda record: record.run_variant)
    for _variant, grouped in groupby(sorted_records, key=lambda record: record.run_variant):
        model_records = list(grouped)
        first = model_records[0]
        provider_errors = sum(record.provider_error for record in model_records)
        timeouts = sum(record.timeout for record in model_records)
        scored = [
            record
            for record in model_records
            if not record.provider_error and not record.timeout
        ]
        correct = sum(record.correct for record in scored)
        failures = len(scored) - correct
        scored_count = len(scored)
        answer_correct = sum(record.answer_ok for record in scored)
        format_correct = sum(record.format_ok for record in scored)
        strict_correct = sum(record.strict_ok for record in scored)
        failure_rate = failures / scored_count if scored_count else 0.0
        accuracy = correct / scored_count if scored_count else 0.0
        accuracy_ci_low, accuracy_ci_high = wilson_interval(correct, scored_count)
        answer_ci_low, answer_ci_high = wilson_interval(answer_correct, scored_count)
        strict_ci_low, strict_ci_high = wilson_interval(strict_correct, scored_count)
        output_tokens = sum(record.output_tokens for record in model_records)
        reasoning_tokens = sum(record.reasoning_tokens for record in model_records)
        total_tokens = sum(record.total_tokens for record in model_records)
        estimated_cost_usd = _sum_optional_costs(model_records)
        rows.append(
            SummaryRow(
                run_variant=first.run_variant,
                model=first.model,
                barrage_profile=first.barrage_profile,
                barrage_seed=first.barrage_seed,
                reasoning_effort=first.reasoning_effort,
                reasoning_summary=first.reasoning_summary,
                total_samples=len(model_records),
                scored_samples=scored_count,
                correct=correct,
                failures=failures,
                answer_correct=answer_correct,
                format_correct=format_correct,
                strict_correct=strict_correct,
                obvious_failure_rate=failure_rate,
                accuracy=accuracy,
                accuracy_ci_low=round(accuracy_ci_low, 6),
                accuracy_ci_high=round(accuracy_ci_high, 6),
                answer_accuracy=answer_correct / scored_count if scored_count else 0.0,
                answer_accuracy_ci_low=round(answer_ci_low, 6),
                answer_accuracy_ci_high=round(answer_ci_high, 6),
                format_accuracy=format_correct / scored_count if scored_count else 0.0,
                strict_accuracy=strict_correct / scored_count if scored_count else 0.0,
                strict_accuracy_ci_low=round(strict_ci_low, 6),
                strict_accuracy_ci_high=round(strict_ci_high, 6),
                failures_per_1000=round(failure_rate * 1000),
                provider_errors=provider_errors,
                timeouts=timeouts,
                non_answers=sum(record.failure_type == "non_answer" for record in scored),
                format_failures=sum(
                    record.failure_type
                    in FORMAT_FAILURE_TYPES
                    for record in scored
                ),
                input_tokens=sum(record.input_tokens for record in model_records),
                output_tokens=output_tokens,
                reasoning_tokens=reasoning_tokens,
                cache_read_tokens=sum(record.cache_read_tokens for record in model_records),
                cache_write_tokens=sum(
                    record.cache_write_tokens for record in model_records
                ),
                total_tokens=total_tokens,
                estimated_cost_usd=estimated_cost_usd,
                tokens_per_scored_sample=safe_ratio(total_tokens, scored_count),
                output_tokens_per_scored_sample=safe_ratio(output_tokens, scored_count),
                reasoning_tokens_per_scored_sample=safe_ratio(
                    reasoning_tokens,
                    scored_count,
                ),
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
                reasoning_token_source=(
                    "reported" if reasoning_tokens else "not_reported_or_zero"
                ),
                cost_source=_join_unique(record.cost_source for record in model_records),
                cost_warnings=_join_unique(record.cost_warnings for record in model_records),
            )
        )
    return rows


def _sum_optional_costs(records: list[EvalRecord]) -> float | None:
    costs = [
        record.estimated_cost_usd
        for record in records
        if record.estimated_cost_usd is not None
    ]
    return round(sum(costs), 12) if costs else None


def _join_unique(values: Any) -> str:
    unique = sorted({str(value) for value in values if value})
    return "; ".join(unique)
