import pytest
from pydantic import ValidationError

from obviousbench.datasets.schemas import BenchmarkItem, SourceRecord, parse_item_id


def valid_record(**overrides):
    record = {
        "id": "obviousbench.char_count.en.v0.public.000001",
        "family": "character_count",
        "subfamily": "single_letter_count",
        "prompt": (
            "Answer the question. Return only the final answer, with no explanation.\n\n"
            "Question: How many r's are in strawberry?\n"
            "Answer:"
        ),
        "question": "How many r's are in strawberry?",
        "target": "3",
        "answer_type": "integer",
        "scorer": "exact_integer_extract_first_v0",
        "split": "public_v0",
        "source_type": "public_archetype",
        "source_refs": ["src_strawberry_public_discussion"],
        "human_triviality": "H0",
        "review_status": "reviewed",
        "metadata": {
            "word": "strawberry",
            "character": "r",
            "case_sensitive": False,
            "generated": False,
            "variant_of": None,
            "prompt_template_id": "final_answer_only_v0",
            "system_prompt": None,
        },
    }
    record.update(overrides)
    return record


def test_complete_benchmark_item_parses():
    item = BenchmarkItem.model_validate(valid_record())

    assert item.id == "obviousbench.char_count.en.v0.public.000001"
    assert item.target == "3"
    assert item.metadata.prompt_template_id == "final_answer_only_v0"


def test_missing_prompt_template_id_fails():
    record = valid_record()
    del record["metadata"]["prompt_template_id"]

    with pytest.raises(ValidationError):
        BenchmarkItem.model_validate(record)


def test_target_must_be_string():
    with pytest.raises(ValidationError):
        BenchmarkItem.model_validate(valid_record(target=3))


def test_source_record_accepts_user_provided_screenshot_without_url():
    source = SourceRecord.model_validate(
        {
            "source_id": "src_google_d_user_screenshot",
            "platform": "user_provided_screenshot",
            "url": None,
            "date_seen": "2026-05-30",
            "original_prompt": "How many d is in google?",
            "claimed_output": 'There is exactly 1 "d" in Google.',
            "failure_description": "The model claims google contains one d.",
            "engagement_signal": {"likes": None, "shares": None, "comments": None},
            "media_type": "screenshot",
            "rights_status": "user_provided_screenshot_do_not_republish",
            "notes": "Do not republish screenshot.",
        }
    )

    assert source.url is None


def test_parse_item_id_accepts_canonical_id():
    parsed = parse_item_id("obviousbench.char_count.en.v0.public.000001")

    assert parsed.family_short == "char_count"
    assert parsed.language == "en"
    assert parsed.version == "v0"
    assert parsed.split_short == "public"
    assert parsed.index == 1


@pytest.mark.parametrize(
    "sample_id",
    [
        "char_count.en.v0.public.000001",
        "obviousbench.unknown.en.v0.public.000001",
        "obviousbench.char_count.fr.v0.public.000001",
        "obviousbench.char_count.en.v1.public.000001",
        "obviousbench.char_count.en.v0.unknown.000001",
        "obviousbench.char_count.en.v0.public.1",
    ],
)
def test_parse_item_id_rejects_invalid_ids(sample_id):
    with pytest.raises(ValueError):
        parse_item_id(sample_id)
