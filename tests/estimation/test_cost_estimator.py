import csv
import json
import pickle
from pathlib import Path

from inspect_ai.model._cache import CacheEntry, CachePolicy, epoch
from inspect_ai.model._chat_message import ChatMessageUser
from inspect_ai.model._generate_config import GenerateConfig
from inspect_ai.model._model_output import ModelOutput

from obviousbench.datasets.schemas import FAMILY_SHORT_NAMES
from obviousbench.estimation.cost import CostEstimateInputs, estimate_benchmark_cost
from tests.datasets.test_schemas import valid_record


def _record(family: str, index: int) -> dict:
    family_short = FAMILY_SHORT_NAMES[family]
    question = f"How many r's are in strawberry number {index}?"
    return valid_record(
        id=f"obviousbench.{family_short}.en.v0.public.{index:06d}",
        family=family,
        subfamily="one",
        prompt=(
            "Answer the question. Return only the final answer, with no explanation.\n\n"
            f"Question: {question}\n"
            "Answer:"
        ),
        question=question,
        source_type="generated_variant",
        source_refs=[f"src_{family}"],
    )


def _write_split(root: Path) -> list[dict]:
    split_dir = root / "public_v0"
    split_dir.mkdir(parents=True)
    rows = [_record("character_count", 1), _record("word_count", 2)]
    for row in rows:
        (split_dir / f"{row['family']}.jsonl").write_text(
            json.dumps(row) + "\n",
            encoding="utf-8",
        )
    return rows


def _write_usage(summary_root: Path, rows: list[dict]) -> None:
    summary_dir = summary_root / "run"
    summary_dir.mkdir(parents=True)
    with (summary_dir / "usage_by_sample.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "model",
                "barrage_profile",
                "barrage_seed",
                "reasoning_effort",
                "reasoning_summary",
                "sample_id",
                "family",
                "input_tokens",
                "output_tokens",
                "reasoning_tokens",
                "cache_read_tokens",
                "cache_write_tokens",
                "total_tokens",
                "estimated_cost_usd",
            ],
        )
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def _write_cache_hit(
    cache_dir: Path,
    *,
    model: str,
    prompt: str,
    base_url: str | None = None,
    config: GenerateConfig | None = None,
) -> None:
    token = epoch.set(1)
    try:
        entry = CacheEntry(
            base_url=base_url,
            config=config or GenerateConfig(reasoning_effort="low"),
            input=[ChatMessageUser(content=prompt, source="input")],
            model=model,
            policy=CachePolicy.from_string("10Y"),
            tool_choice="none",
            tools=[],
        )
        cache_path = cache_dir / "generate" / model / entry.key
        cache_path.parent.mkdir(parents=True)
        with cache_path.open("wb") as handle:
            pickle.dump(
                (None, ModelOutput.from_content(model="test-model", content="ok")),
                handle,
            )
    finally:
        epoch.reset(token)


def test_estimate_uses_historical_usage_and_cache_hits(tmp_path):
    rows = _write_split(tmp_path / "data")
    _write_usage(
        tmp_path / "summaries",
        [
            {
                "model": "openai/gpt-5-nano",
                "barrage_profile": "balanced_2x1",
                "barrage_seed": "7",
                "reasoning_effort": "low",
                "reasoning_summary": "",
                "sample_id": rows[0]["id"],
                "family": rows[0]["family"],
                "input_tokens": "40",
                "output_tokens": "10",
                "reasoning_tokens": "4",
                "cache_read_tokens": "0",
                "cache_write_tokens": "0",
                "total_tokens": "50",
                "estimated_cost_usd": "0.00002",
            },
            {
                "model": "openai/gpt-5-nano",
                "barrage_profile": "balanced_2x1",
                "barrage_seed": "7",
                "reasoning_effort": "low",
                "reasoning_summary": "",
                "sample_id": rows[1]["id"],
                "family": rows[1]["family"],
                "input_tokens": "60",
                "output_tokens": "20",
                "reasoning_tokens": "8",
                "cache_read_tokens": "0",
                "cache_write_tokens": "0",
                "total_tokens": "80",
                "estimated_cost_usd": "0.00004",
            },
        ],
    )
    _write_cache_hit(
        tmp_path / "cache",
        model="openai/gpt-5-nano",
        prompt=rows[0]["prompt"],
    )

    estimate = estimate_benchmark_cost(
        CostEstimateInputs(
            model="openai/gpt-5-nano",
            profile="balanced_2x1",
            seed=7,
            data_dir=tmp_path / "data",
            summary_root=tmp_path / "summaries",
            cache_dir=tmp_path / "cache",
            settings={"reasoning_effort": "low"},
        )
    )

    assert estimate.total_samples == 2
    assert estimate.cache_hits == 1
    assert estimate.billable_samples == 1
    assert estimate.estimated_billable_cost_usd is not None
    assert estimate.estimated_billable_cost_usd > 0
    assert estimate.rows[0].cache_hit
    assert estimate.rows[0].estimated_cost_usd == 0
    assert estimate.rows[1].usage_source == "historical_sample"


def test_estimate_detects_openrouter_cache_hits(tmp_path):
    rows = _write_split(tmp_path / "data")
    _write_cache_hit(
        tmp_path / "cache",
        model="openrouter/test/model",
        prompt=rows[0]["prompt"],
        base_url="https://openrouter.ai/api/v1",
        config=GenerateConfig(reasoning_effort="low", attempt_timeout=180),
    )

    estimate = estimate_benchmark_cost(
        CostEstimateInputs(
            model="openrouter/test/model",
            profile="balanced_2x1",
            seed=7,
            data_dir=tmp_path / "data",
            summary_root=tmp_path / "summaries",
            cache_dir=tmp_path / "cache",
            settings={"reasoning_effort": "low", "attempt_timeout": "180"},
        )
    )

    assert estimate.cache_hits == 1
    assert estimate.billable_samples == 1
    assert estimate.rows[0].cache_hit


def test_estimate_falls_back_to_model_average_when_sample_history_missing(tmp_path):
    _write_split(tmp_path / "data")
    _write_usage(
        tmp_path / "summaries",
        [
            {
                "model": "openai/gpt-5-nano",
                "barrage_profile": "balanced_8x10",
                "barrage_seed": "1",
                "reasoning_effort": "",
                "reasoning_summary": "",
                "sample_id": "other-sample",
                "family": "other",
                "input_tokens": "30",
                "output_tokens": "12",
                "reasoning_tokens": "0",
                "cache_read_tokens": "0",
                "cache_write_tokens": "0",
                "total_tokens": "42",
                "estimated_cost_usd": "0.00001",
            }
        ],
    )

    estimate = estimate_benchmark_cost(
        CostEstimateInputs(
            model="openai/gpt-5-nano",
            profile="balanced_2x1",
            seed=7,
            data_dir=tmp_path / "data",
            summary_root=tmp_path / "summaries",
            cache_dir=tmp_path / "cache",
        )
    )

    assert estimate.billable_samples == 2
    assert {row.usage_source for row in estimate.rows} == {"historical_model_average"}
