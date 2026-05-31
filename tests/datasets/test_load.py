import json

from obviousbench.datasets.load import load_benchmark_jsonl, to_sample
from tests.datasets.test_schemas import valid_record


def test_load_preserves_order_and_metadata(tmp_path):
    first = valid_record()
    second = valid_record(
        id="obviousbench.char_count.en.v0.public.000002",
        question="How many s's are in mississippi?",
        target="4",
    )
    path = tmp_path / "items.jsonl"
    path.write_text(
        json.dumps(first) + "\n" + json.dumps(second) + "\n",
        encoding="utf-8",
    )

    items = load_benchmark_jsonl(path)

    assert [item.id for item in items] == [
        "obviousbench.char_count.en.v0.public.000001",
        "obviousbench.char_count.en.v0.public.000002",
    ]


def test_to_sample_preserves_contract():
    item = load_benchmark_jsonl_from_record(valid_record())
    sample = to_sample(item)

    assert sample.id == item.id
    assert sample.input == item.prompt
    assert sample.target == item.target
    assert sample.metadata["family"] == "character_count"
    assert sample.metadata["scorer"] == "exact_integer_extract_first_v0"
    assert sample.metadata["benchmark_metadata"]["word"] == "strawberry"


def load_benchmark_jsonl_from_record(record):
    from obviousbench.datasets.schemas import BenchmarkItem

    return BenchmarkItem.model_validate(record)

