"""Approximate benchmark run cost estimation."""

from __future__ import annotations

import csv
import os
from collections import Counter
from collections.abc import Mapping
from contextlib import contextmanager
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from inspect_ai.model._cache import CacheEntry, CachePolicy, cache_fetch, epoch
from inspect_ai.model._chat_message import ChatMessageUser
from inspect_ai.model._generate_config import GenerateConfig
from pydantic import ValidationError

from obviousbench.analysis.costing import price_records_with_runcost
from obviousbench.analysis.metrics import EvalRecord
from obviousbench.barrage import BarrageProfile, build_barrage, load_split_items
from obviousbench.datasets.schemas import BenchmarkItem
from obviousbench.runners.cache import DEFAULT_CACHE_DIR, DEFAULT_CACHE_EXPIRY

DEFAULT_SUMMARY_ROOT = Path("results/summaries")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
GENERATE_CONFIG_FIELDS = frozenset(GenerateConfig.model_fields)


@dataclass(frozen=True)
class CostEstimateInputs:
    model: str
    profile: str = "balanced_8x5"
    seed: int = 20260531
    split: str = "public_v0"
    data_dir: Path = Path("data")
    summary_root: Path = DEFAULT_SUMMARY_ROOT
    cache_dir: Path | None = DEFAULT_CACHE_DIR
    cache: str | None = DEFAULT_CACHE_EXPIRY
    base_url: str | None = None
    settings: Mapping[str, str] = field(default_factory=dict)
    max_metamorphic_siblings_per_group: int = 1


@dataclass(frozen=True)
class CostEstimateRow:
    sample_id: str
    family: str
    cache_hit: bool
    input_tokens: int
    output_tokens: int
    reasoning_tokens: int
    cache_read_tokens: int
    cache_write_tokens: int
    total_tokens: int
    estimated_cost_usd: float | None
    uncached_estimated_cost_usd: float | None
    usage_source: str
    pricing_source: str
    warnings: tuple[str, ...] = ()


@dataclass(frozen=True)
class CostEstimate:
    model: str
    profile: str
    seed: int
    total_samples: int
    cache_hits: int
    billable_samples: int
    estimated_billable_cost_usd: float | None
    estimated_cached_cost_avoided_usd: float | None
    usage_source: str
    pricing_source: str
    warnings: tuple[str, ...]
    rows: tuple[CostEstimateRow, ...]


@dataclass(frozen=True)
class _UsageBasis:
    input_tokens: int
    output_tokens: int
    reasoning_tokens: int
    cache_read_tokens: int
    cache_write_tokens: int
    total_tokens: int
    historical_cost_usd: float | None
    source: str


def estimate_benchmark_cost(inputs: CostEstimateInputs) -> CostEstimate:
    """Estimate provider cost for a benchmark barrage without making model calls."""
    profile = BarrageProfile.parse(inputs.profile)
    items = build_barrage(
        load_split_items(inputs.split, data_dir=inputs.data_dir),
        profile,
        seed=inputs.seed,
        max_metamorphic_siblings_per_group=inputs.max_metamorphic_siblings_per_group,
    )
    history = _HistoryIndex.load(inputs.summary_root)
    rows = [
        _estimate_uncached_row(
            item,
            inputs=inputs,
            usage=history.usage_for(item, inputs),
            cache_hit=_cache_hit(item, inputs),
        )
        for item in items
    ]
    rows, pricing_warnings = _price_rows(inputs.model, rows)
    billable_cost = _sum_optional(row.estimated_cost_usd for row in rows)
    avoided_cost = _sum_optional(
        row.uncached_estimated_cost_usd
        for row in rows
        if row.cache_hit
    )
    warnings = sorted(
        {
            warning
            for row in rows
            for warning in row.warnings
        }
        | set(pricing_warnings)
    )
    return CostEstimate(
        model=inputs.model,
        profile=inputs.profile,
        seed=inputs.seed,
        total_samples=len(rows),
        cache_hits=sum(row.cache_hit for row in rows),
        billable_samples=sum(not row.cache_hit for row in rows),
        estimated_billable_cost_usd=billable_cost,
        estimated_cached_cost_avoided_usd=avoided_cost,
        usage_source=_join_unique(row.usage_source for row in rows),
        pricing_source=_join_unique(row.pricing_source for row in rows),
        warnings=tuple(warnings),
        rows=tuple(rows),
    )


def _estimate_uncached_row(
    item: BenchmarkItem,
    *,
    inputs: CostEstimateInputs,
    usage: _UsageBasis,
    cache_hit: bool,
) -> CostEstimateRow:
    return CostEstimateRow(
        sample_id=item.id,
        family=item.family,
        cache_hit=cache_hit,
        input_tokens=usage.input_tokens,
        output_tokens=usage.output_tokens,
        reasoning_tokens=usage.reasoning_tokens,
        cache_read_tokens=usage.cache_read_tokens,
        cache_write_tokens=usage.cache_write_tokens,
        total_tokens=usage.total_tokens,
        estimated_cost_usd=None,
        uncached_estimated_cost_usd=usage.historical_cost_usd,
        usage_source=usage.source,
        pricing_source="unpriced",
        warnings=(),
    )


def _price_rows(
    model: str,
    rows: list[CostEstimateRow],
) -> tuple[list[CostEstimateRow], list[str]]:
    if not rows:
        return [], []

    try:
        priced_records, _ledger = price_records_with_runcost(
            [
                EvalRecord(
                    model=model,
                    sample_id=row.sample_id,
                    family=row.family,
                    correct=False,
                    failure_type="none",
                    provider_error=False,
                    timeout=False,
                    input_tokens=row.input_tokens,
                    output_tokens=row.output_tokens,
                    reasoning_tokens=row.reasoning_tokens,
                    cache_read_tokens=row.cache_read_tokens,
                    cache_write_tokens=row.cache_write_tokens,
                    total_tokens=row.total_tokens,
                )
                for row in rows
            ]
        )
        costs_by_sample = {
            record.sample_id: (record.estimated_cost_usd, record.cost_warnings)
            for record in priced_records
        }
        priced: list[CostEstimateRow] = []
        for row in rows:
            runcost_cost, warning_text = costs_by_sample.get(row.sample_id, (None, ""))
            uncached_cost = (
                runcost_cost
                if runcost_cost is not None
                else row.uncached_estimated_cost_usd
            )
            pricing_source = "runcost" if runcost_cost is not None else "historical_cost_average"
            warnings = tuple(_split_warnings(warning_text))
            priced.append(
                _replace_row(
                    row,
                    estimated_cost_usd=0.0 if row.cache_hit else uncached_cost,
                    uncached_estimated_cost_usd=uncached_cost,
                    pricing_source=pricing_source,
                    warnings=warnings,
                )
            )
        return priced, []
    except Exception as exc:
        return [
            _replace_row(
                row,
                estimated_cost_usd=0.0 if row.cache_hit else row.uncached_estimated_cost_usd,
                pricing_source="historical_cost_average",
                warnings=("runcost pricing failed; used historical cost averages",),
            )
            for row in rows
        ], [f"runcost pricing failed: {exc}"]


class _HistoryIndex:
    def __init__(self, rows: list[dict[str, str]]):
        self.rows = rows

    @classmethod
    def load(cls, summary_root: Path) -> _HistoryIndex:
        if not summary_root.exists():
            return cls([])
        rows: list[dict[str, str]] = []
        for path in sorted(summary_root.glob("*/usage_by_sample.csv")):
            with path.open(newline="", encoding="utf-8") as handle:
                rows.extend(csv.DictReader(handle))
        return cls(rows)

    def usage_for(self, item: BenchmarkItem, inputs: CostEstimateInputs) -> _UsageBasis:
        model_rows = [
            row
            for row in self.rows
            if row.get("model") == inputs.model
            and _settings_match(row, inputs.settings)
        ]
        profile_rows = [
            row
            for row in model_rows
            if _profile_matches(row.get("barrage_profile", ""), inputs.profile, inputs.seed)
            and _seed_matches(row.get("barrage_seed", ""), inputs.seed)
        ]
        sample_rows = [
            row for row in profile_rows if row.get("sample_id") == item.id
        ] or [
            row for row in model_rows if row.get("sample_id") == item.id
        ]
        if sample_rows:
            return _average_usage(sample_rows, "historical_sample")
        if profile_rows:
            return _average_usage(profile_rows, "historical_profile_average")
        if model_rows:
            return _average_usage(model_rows, "historical_model_average")
        if self.rows:
            return _average_usage(self.rows, "historical_global_average")
        return _heuristic_usage(item, inputs.settings)


def _cache_hit(item: BenchmarkItem, inputs: CostEstimateInputs) -> bool:
    if inputs.cache is None or inputs.cache_dir is None:
        return False
    policy = CachePolicy.from_string(inputs.cache)
    if policy is None:
        return False
    config = _generate_config_from_settings(inputs.settings)
    with _inspect_cache_dir(inputs.cache_dir):
        token = epoch.set(1)
        try:
            entry = CacheEntry(
                base_url=_cache_base_url(inputs),
                config=config,
                input=[ChatMessageUser(content=item.prompt, source="input")],
                model=inputs.model,
                policy=policy,
                tool_choice="none",
                tools=[],
            )
            return cache_fetch(entry) is not None
        finally:
            epoch.reset(token)


def _cache_base_url(inputs: CostEstimateInputs) -> str | None:
    if inputs.base_url:
        return inputs.base_url
    if inputs.model.startswith("openrouter/"):
        return OPENROUTER_BASE_URL
    return None


def _generate_config_from_settings(settings: Mapping[str, str]) -> GenerateConfig:
    values: dict[str, Any] = {}
    for key, value in settings.items():
        if key not in GENERATE_CONFIG_FIELDS:
            continue
        values[key] = _coerce_setting(value)
    try:
        return GenerateConfig(**values)
    except ValidationError:
        return GenerateConfig()


@contextmanager
def _inspect_cache_dir(cache_dir: Path):
    previous = os.environ.get("INSPECT_CACHE_DIR")
    os.environ["INSPECT_CACHE_DIR"] = str(cache_dir)
    try:
        yield
    finally:
        if previous is None:
            os.environ.pop("INSPECT_CACHE_DIR", None)
        else:
            os.environ["INSPECT_CACHE_DIR"] = previous


def _average_usage(rows: list[dict[str, str]], source: str) -> _UsageBasis:
    return _UsageBasis(
        input_tokens=_round_mean(_ints(rows, "input_tokens")),
        output_tokens=_round_mean(_ints(rows, "output_tokens")),
        reasoning_tokens=_round_mean(_ints(rows, "reasoning_tokens")),
        cache_read_tokens=_round_mean(_ints(rows, "cache_read_tokens")),
        cache_write_tokens=_round_mean(_ints(rows, "cache_write_tokens")),
        total_tokens=_round_mean(_ints(rows, "total_tokens")),
        historical_cost_usd=_mean_optional(_floats(rows, "estimated_cost_usd")),
        source=source,
    )


def _heuristic_usage(item: BenchmarkItem, settings: Mapping[str, str]) -> _UsageBasis:
    input_tokens = max(round(len(item.prompt) / 4), 1)
    reasoning_effort = settings.get("reasoning_effort", "")
    reasoning_tokens = {
        "none": 0,
        "minimal": 4,
        "low": 8,
        "medium": 16,
        "high": 32,
    }.get(reasoning_effort, 8 if reasoning_effort else 0)
    output_tokens = 16 + reasoning_tokens
    return _UsageBasis(
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        reasoning_tokens=reasoning_tokens,
        cache_read_tokens=0,
        cache_write_tokens=0,
        total_tokens=input_tokens + output_tokens,
        historical_cost_usd=None,
        source="heuristic",
    )


def _profile_matches(value: str, profile: str, seed: int) -> bool:
    if not value:
        return True
    return value in {profile, f"{profile}_seed_{seed}"}


def _seed_matches(value: str, seed: int) -> bool:
    return value in {"", str(seed)}


def _settings_match(row: Mapping[str, str], settings: Mapping[str, str]) -> bool:
    for key, value in settings.items():
        if key in {"reasoning_effort", "reasoning_summary"} and (
            row.get(key) or ""
        ) != value:
            return False
    return True


def _coerce_setting(value: str) -> Any:
    if value.lower() == "none":
        return "none"
    if value.lower() == "true":
        return True
    if value.lower() == "false":
        return False
    try:
        return int(value)
    except ValueError:
        try:
            return float(value)
        except ValueError:
            return value


def _ints(rows: list[dict[str, str]], field: str) -> list[int]:
    values: list[int] = []
    for row in rows:
        try:
            values.append(int(float(row.get(field) or 0)))
        except ValueError:
            continue
    return values


def _floats(rows: list[dict[str, str]], field: str) -> list[float]:
    values: list[float] = []
    for row in rows:
        try:
            value = row.get(field)
            if value not in {None, ""}:
                values.append(float(value))
        except ValueError:
            continue
    return values


def _round_mean(values: list[int]) -> int:
    if not values:
        return 0
    return round(sum(values) / len(values))


def _mean_optional(values: list[float]) -> float | None:
    if not values:
        return None
    return round(sum(values) / len(values), 12)


def _sum_optional(values) -> float | None:
    numbers = [value for value in values if value is not None]
    if not numbers:
        return None
    return round(sum(numbers), 12)


def _join_unique(values) -> str:
    counts = Counter(str(value) for value in values if value)
    return "; ".join(sorted(counts))


def _split_warnings(value: str | None) -> list[str]:
    if not value:
        return []
    return [part.strip() for part in value.split(";") if part.strip()]


def _replace_row(row: CostEstimateRow, **changes: Any) -> CostEstimateRow:
    data = row.__dict__ | changes
    return CostEstimateRow(**data)
