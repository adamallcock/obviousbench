import csv
import json

from obviousbench.analysis.metrics import EvalRecord
from obviousbench.analysis.usage import (
    build_cost_input,
    compute_usage_by_family,
    compute_usage_by_question,
    compute_usage_by_section,
    export_usage_by_family_csv,
    export_usage_by_question_csv,
    export_usage_by_sample_csv,
    export_usage_by_section_csv,
    write_cost_ledger,
)


def _records():
    return [
        EvalRecord(
            model="openai/gpt-5-nano",
            sample_id="id1",
            family="character_count",
            correct=True,
            failure_type="none",
            provider_error=False,
            timeout=False,
            subfamily="single_letter_count",
            question="How many r's are in strawberry?",
            barrage_profile="balanced_8x10",
            barrage_seed=1,
            reasoning_effort="minimal",
            reasoning_summary="none",
            input_tokens=10,
            output_tokens=5,
            reasoning_tokens=0,
            total_tokens=15,
            estimated_cost_usd=0.1,
            cost_source="runcost",
            metamorphic_group_id="char_count.strawberry.001",
            metamorphic_role="base",
            metamorphic_relation="equivalent",
        ),
        EvalRecord(
            model="openai/gpt-5-nano",
            sample_id="id2",
            family="character_count",
            correct=False,
            failure_type="incorrect_count",
            provider_error=False,
            timeout=False,
            subfamily="single_letter_count",
            question="How many e's are in responsiveness?",
            barrage_profile="balanced_8x10",
            barrage_seed=1,
            reasoning_effort="minimal",
            reasoning_summary="none",
            input_tokens=20,
            output_tokens=7,
            reasoning_tokens=1,
            total_tokens=28,
            estimated_cost_usd=0.2,
            cost_source="runcost",
            cost_warnings="fallback price",
        ),
    ]


def test_export_usage_by_sample_csv(tmp_path):
    path = tmp_path / "usage_by_sample.csv"

    export_usage_by_sample_csv(_records(), path)

    rows = list(csv.DictReader(path.open(encoding="utf-8")))
    assert rows[0]["run_variant"] == (
        "openai/gpt-5-nano|profile=balanced_8x10|seed=1|"
        "reasoning_effort=minimal|reasoning_summary=none"
    )
    assert rows[0]["sample_id"] == "id1"
    assert rows[0]["input_tokens"] == "10"
    assert rows[0]["service_tier"] == ""
    assert rows[0]["answer_correct"] == "True"
    assert rows[0]["format_correct"] == "True"
    assert rows[0]["strict_correct"] == "True"
    assert rows[0]["metamorphic_group_id"] == "char_count.strawberry.001"
    assert rows[0]["metamorphic_role"] == "base"
    assert rows[0]["metamorphic_relation"] == "equivalent"
    assert rows[0]["estimated_cost_usd"] == "0.1"


def test_export_usage_by_family_csv(tmp_path):
    path = tmp_path / "usage_by_family.csv"

    export_usage_by_family_csv(compute_usage_by_family(_records()), path)

    rows = list(csv.DictReader(path.open(encoding="utf-8")))
    assert rows == [
        {
            "run_variant": (
                "openai/gpt-5-nano|profile=balanced_8x10|seed=1|"
                "reasoning_effort=minimal|reasoning_summary=none"
            ),
            "model": "openai/gpt-5-nano",
            "family": "character_count",
            "samples": "2",
            "scored_samples": "2",
            "provider_errors": "0",
            "timeouts": "0",
            "correct": "1",
            "failures": "1",
            "answer_correct": "1",
            "format_correct": "2",
            "strict_correct": "1",
            "input_tokens": "30",
            "output_tokens": "12",
            "reasoning_tokens": "1",
            "cache_read_tokens": "0",
            "cache_write_tokens": "0",
            "total_tokens": "43",
            "estimated_cost_usd": "0.3",
            "tokens_per_scored_sample": "21.5",
            "tokens_per_correct": "43.0",
            "cost_per_correct_usd": "0.3",
            "reasoning_token_share": "0.023255813953488372",
            "overthinking_index": "0.08333333333333333",
            "cost_source": "runcost",
            "cost_warnings": "fallback price",
        }
    ]


def test_export_usage_by_section_csv(tmp_path):
    path = tmp_path / "usage_by_section.csv"

    export_usage_by_section_csv(compute_usage_by_section(_records()), path)

    rows = list(csv.DictReader(path.open(encoding="utf-8")))
    assert rows == [
        {
            "run_variant": (
                "openai/gpt-5-nano|profile=balanced_8x10|seed=1|"
                "reasoning_effort=minimal|reasoning_summary=none"
            ),
            "model": "openai/gpt-5-nano",
            "family": "character_count",
            "subfamily": "single_letter_count",
            "samples": "2",
            "scored_samples": "2",
            "provider_errors": "0",
            "timeouts": "0",
            "correct": "1",
            "failures": "1",
            "answer_correct": "1",
            "format_correct": "2",
            "strict_correct": "1",
            "input_tokens": "30",
            "output_tokens": "12",
            "reasoning_tokens": "1",
            "cache_read_tokens": "0",
            "cache_write_tokens": "0",
            "total_tokens": "43",
            "estimated_cost_usd": "0.3",
            "tokens_per_scored_sample": "21.5",
            "tokens_per_correct": "43.0",
            "cost_per_correct_usd": "0.3",
            "reasoning_token_share": "0.023255813953488372",
            "overthinking_index": "0.08333333333333333",
            "cost_source": "runcost",
            "cost_warnings": "fallback price",
        }
    ]


def test_export_usage_by_question_csv(tmp_path):
    path = tmp_path / "usage_by_question.csv"

    export_usage_by_question_csv(compute_usage_by_question(_records()), path)

    rows = list(csv.DictReader(path.open(encoding="utf-8")))
    assert rows[0]["sample_id"] == "id1"
    assert rows[0]["question"] == "How many r's are in strawberry?"
    assert rows[0]["scored_samples"] == "1"
    assert rows[0]["provider_errors"] == "0"
    assert rows[0]["timeouts"] == "0"
    assert rows[0]["correct"] == "1"
    assert rows[0]["answer_correct"] == "1"
    assert rows[0]["format_correct"] == "1"
    assert rows[0]["strict_correct"] == "1"
    assert rows[0]["tokens_per_scored_sample"] == "15.0"
    assert rows[0]["tokens_per_correct"] == "15.0"
    assert rows[0]["cost_per_correct_usd"] == "0.1"
    assert rows[0]["reasoning_token_share"] == "0.0"
    assert rows[0]["overthinking_index"] == "0.0"
    assert rows[1]["sample_id"] == "id2"
    assert rows[1]["failures"] == "1"
    assert rows[1]["tokens_per_correct"] == ""


def test_usage_breakdowns_count_provider_errors_and_timeouts_as_incorrect_attempts(tmp_path):
    path = tmp_path / "usage_by_family.csv"
    records = [
        *_records(),
        EvalRecord(
            model="openai/gpt-5-nano",
            sample_id="id3",
            family="character_count",
            correct=False,
            failure_type="provider_error",
            provider_error=True,
            timeout=False,
            subfamily="single_letter_count",
            question="Provider failed",
            barrage_profile="balanced_8x10",
            barrage_seed=1,
            reasoning_effort="minimal",
            reasoning_summary="none",
            input_tokens=3,
            output_tokens=0,
            total_tokens=3,
        ),
        EvalRecord(
            model="openai/gpt-5-nano",
            sample_id="id4",
            family="character_count",
            correct=False,
            failure_type="timeout",
            provider_error=False,
            timeout=True,
            subfamily="single_letter_count",
            question="Provider timed out",
            barrage_profile="balanced_8x10",
            barrage_seed=1,
            reasoning_effort="minimal",
            reasoning_summary="none",
            input_tokens=4,
            output_tokens=0,
            total_tokens=4,
        ),
    ]

    export_usage_by_family_csv(compute_usage_by_family(records), path)

    row = next(csv.DictReader(path.open(encoding="utf-8")))
    assert row["samples"] == "4"
    assert row["scored_samples"] == "4"
    assert row["provider_errors"] == "1"
    assert row["timeouts"] == "1"
    assert row["correct"] == "1"
    assert row["failures"] == "3"
    assert row["answer_correct"] == "1"
    assert row["format_correct"] == "2"
    assert row["strict_correct"] == "1"
    assert row["tokens_per_scored_sample"] == "12.5"


def test_build_cost_input_uses_normalized_usage_fields():
    payload = build_cost_input(_records())

    assert payload["records"][0] == {
        "sample_id": "id1",
        "model": "openai/gpt-5-nano",
        "provider": "openai",
        "surface": "normalized.usage",
        "service_tier": "",
        "usage": {
            "input_tokens": 10,
            "output_tokens": 5,
            "reasoning_tokens": 0,
            "cache_read_tokens": 0,
            "cache_write_tokens": 0,
            "total_tokens": 15,
        },
    }


def test_write_cost_ledger(tmp_path):
    path = tmp_path / "cost_ledger.json"
    ledger = {"records": [{"sample_id": "id1", "estimated_cost_usd": 0.1}]}

    write_cost_ledger(ledger, path)

    assert json.loads(path.read_text(encoding="utf-8")) == ledger
