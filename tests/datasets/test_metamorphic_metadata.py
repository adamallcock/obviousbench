import json

from obviousbench.datasets.schemas import BenchmarkItem
from obviousbench.datasets.validation import validate_dataset_paths
from tests.datasets.test_schemas import valid_record


def test_metamorphic_metadata_is_accepted():
    record = valid_record(
        id="obviousbench.spell.en.v0.public.000001",
        family="spelling_transform",
        subfamily="reverse_word",
        prompt="Question: Reverse abc.\nAnswer:",
        question="Reverse abc.",
        target="cba",
        answer_type="string",
        scorer="exact_string_trim_v0",
        source_type="generated_variant",
        source_refs=["generated:test"],
        metadata={
            **valid_record()["metadata"],
            "prompt_template_id": "final_answer_only_v0",
            "metamorphic_group_id": "spell.reverse.001",
            "metamorphic_role": "paraphrase",
            "metamorphic_relation": "equivalent",
            "metamorphic_expected_behavior": "The answer stays cba.",
        },
    )

    item = BenchmarkItem.model_validate(record)

    assert item.metadata.metamorphic_group_id == "spell.reverse.001"
    assert item.metadata.metamorphic_role == "paraphrase"
    assert item.metadata.metamorphic_relation == "equivalent"
    assert item.metadata.metamorphic_expected_behavior == "The answer stays cba."


def test_validation_rejects_partial_metamorphic_metadata(tmp_path):
    path = tmp_path / "items.jsonl"
    record = valid_record(
        metadata={
            **valid_record()["metadata"],
            "metamorphic_group_id": "spell.reverse.001",
            "metamorphic_role": "paraphrase",
        }
    )
    path.write_text(json.dumps(record) + "\n", encoding="utf-8")

    report = validate_dataset_paths([path])

    assert not report.ok
    assert [issue.code for issue in report.issues] == [
        "incomplete_metamorphic_metadata"
    ]


def test_validation_treats_blank_metamorphic_metadata_as_absent(tmp_path):
    path = tmp_path / "items.jsonl"
    record = valid_record(
        metadata={
            **valid_record()["metadata"],
            "metamorphic_group_id": "   ",
            "metamorphic_role": "\t",
        }
    )
    path.write_text(json.dumps(record) + "\n", encoding="utf-8")

    report = validate_dataset_paths([path])

    assert report.ok


def test_validation_allows_items_without_metamorphic_metadata(tmp_path):
    path = tmp_path / "items.jsonl"
    path.write_text(json.dumps(valid_record()) + "\n", encoding="utf-8")

    report = validate_dataset_paths([path])

    assert report.ok
