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
            "correct": "1",
            "failures": "1",
            "input_tokens": "30",
            "output_tokens": "12",
            "reasoning_tokens": "1",
            "cache_read_tokens": "0",
            "cache_write_tokens": "0",
            "total_tokens": "43",
            "estimated_cost_usd": "0.3",
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
            "correct": "1",
            "failures": "1",
            "input_tokens": "30",
            "output_tokens": "12",
            "reasoning_tokens": "1",
            "cache_read_tokens": "0",
            "cache_write_tokens": "0",
            "total_tokens": "43",
            "estimated_cost_usd": "0.3",
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
    assert rows[0]["correct"] == "1"
    assert rows[1]["sample_id"] == "id2"
    assert rows[1]["failures"] == "1"


def test_build_cost_input_uses_normalized_usage_fields():
    payload = build_cost_input(_records())

    assert payload["records"][0] == {
        "sample_id": "id1",
        "model": "openai/gpt-5-nano",
        "provider": "openai",
        "surface": "normalized.usage",
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
