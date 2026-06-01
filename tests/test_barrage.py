import json
from collections import Counter

from obviousbench.barrage import (
    BarrageProfile,
    build_barrage,
    load_split_items,
    write_barrage_jsonl,
)
from obviousbench.datasets.schemas import FAMILY_SHORT_NAMES, BenchmarkItem
from tests.datasets.test_schemas import valid_record


def _record(family: str, subfamily: str, index: int) -> dict:
    family_short = FAMILY_SHORT_NAMES[family]
    return valid_record(
        id=f"obviousbench.{family_short}.en.v0.public.{index:06d}",
        family=family,
        subfamily=subfamily,
        question=f"{family} {subfamily} {index}?",
        prompt=f"Question: {family} {subfamily} {index}?\nAnswer:",
        target="A",
        answer_type="multiple_choice",
        scorer="multiple_choice_letter_v0",
        source_type="generated_variant",
        source_refs=[f"src_{family}_{subfamily}"],
        metadata={
            **valid_record()["metadata"],
            "choices": ["A", "B"],
            "variant_of": f"{family}_{subfamily}",
        },
    )


def _item(family: str, subfamily: str, index: int) -> BenchmarkItem:
    return BenchmarkItem.model_validate(_record(family, subfamily, index))


def _metamorphic_item(
    family: str,
    subfamily: str,
    index: int,
    group_id: str,
) -> BenchmarkItem:
    record = _record(family, subfamily, index)
    record["metadata"] = {
        **record["metadata"],
        "metamorphic_group_id": group_id,
        "metamorphic_role": f"variant_{index}",
        "metamorphic_relation": "equivalent",
        "metamorphic_expected_behavior": "The answer should not change.",
    }
    return BenchmarkItem.model_validate(record)


def test_parse_balanced_profile_name():
    profile = BarrageProfile.parse("balanced_8x10")

    assert profile.family_count == 8
    assert profile.per_family == 10
    assert profile.name == "balanced_8x10"
    assert profile.strategy == "balanced"


def test_parse_hard_obvious_profile_name():
    profile = BarrageProfile.parse("hard_obvious_8x10")

    assert profile.family_count == 8
    assert profile.per_family == 10
    assert profile.name == "hard_obvious_8x10"
    assert profile.strategy == "hard_obvious"


def test_build_barrage_balances_families_and_round_robins_subfamilies():
    items = [
        *[_item("character_count", "letters", index) for index in range(1, 5)],
        *[_item("character_count", "positions", index) for index in range(5, 9)],
        *[_item("word_count", "sentences", index) for index in range(9, 13)],
        *[_item("word_count", "commas", index) for index in range(13, 17)],
    ]

    selected = build_barrage(
        items,
        BarrageProfile(name="balanced_2x4", family_count=2, per_family=4),
        seed=123,
    )

    assert Counter(item.family for item in selected) == {
        "character_count": 4,
        "word_count": 4,
    }
    assert Counter(
        (item.family, item.subfamily) for item in selected
    ) == {
        ("character_count", "letters"): 2,
        ("character_count", "positions"): 2,
        ("word_count", "sentences"): 2,
        ("word_count", "commas"): 2,
    }
    assert [item.family for item in selected[:4]] == [
        "character_count",
        "word_count",
        "character_count",
        "word_count",
    ]


def test_build_barrage_is_seed_stable():
    items = [
        _item(family, "one", index)
        for index, family in enumerate(
            ["character_count"] * 8 + ["word_count"] * 8,
            1,
        )
    ]
    profile = BarrageProfile(name="balanced_2x3", family_count=2, per_family=3)

    first = [item.id for item in build_barrage(items, profile, seed=42)]
    second = [item.id for item in build_barrage(items, profile, seed=42)]
    different = [item.id for item in build_barrage(items, profile, seed=43)]

    assert first == second
    assert first != different


def test_build_barrage_default_limits_metamorphic_siblings_per_group():
    items = [
        _metamorphic_item("character_count", "letters", 1, "g1"),
        _metamorphic_item("character_count", "letters", 2, "g1"),
        _item("character_count", "letters", 3),
        _item("character_count", "letters", 4),
        _item("word_count", "sentences", 5),
        _item("word_count", "sentences", 6),
        _item("word_count", "sentences", 7),
        _item("word_count", "sentences", 8),
    ]

    selected = build_barrage(
        items,
        BarrageProfile(name="balanced_2x2", family_count=2, per_family=2),
        seed=1,
    )

    assert Counter(
        item.metadata.metamorphic_group_id
        for item in selected
        if item.metadata.metamorphic_group_id
    ) == {"g1": 1}


def test_build_barrage_can_include_more_metamorphic_siblings_when_requested():
    items = [
        _metamorphic_item("character_count", "letters", 1, "g1"),
        _metamorphic_item("character_count", "letters", 2, "g1"),
        _item("word_count", "sentences", 5),
        _item("word_count", "sentences", 6),
    ]

    selected = build_barrage(
        items,
        BarrageProfile(name="balanced_2x2", family_count=2, per_family=2),
        seed=1,
        max_metamorphic_siblings_per_group=2,
    )

    assert Counter(
        item.metadata.metamorphic_group_id
        for item in selected
        if item.metadata.metamorphic_group_id
    ) == {"g1": 2}


def test_metamorphic_sibling_cap_is_namespaced_by_family():
    items = [
        _metamorphic_item("character_count", "letters", 1, "g1"),
        _metamorphic_item("word_count", "sentences", 2, "g1"),
    ]

    selected = build_barrage(
        items,
        BarrageProfile(name="balanced_2x1", family_count=2, per_family=1),
        seed=1,
    )

    assert Counter((item.family, item.metadata.metamorphic_group_id) for item in selected) == {
        ("character_count", "g1"): 1,
        ("word_count", "g1"): 1,
    }


def test_hard_obvious_profile_prioritizes_hard_subfamilies():
    items = [
        _item("arithmetic", "small_integer_arithmetic", 1),
        _item("arithmetic", "numeric_comparison", 2),
        _item("character_count", "single_letter_count", 3),
    ]

    selected = build_barrage(
        items,
        BarrageProfile.parse("hard_obvious_2x1"),
        seed=1,
    )

    selected_by_family = {item.family: item.subfamily for item in selected}
    assert selected_by_family == {
        "arithmetic": "numeric_comparison",
        "character_count": "single_letter_count",
    }


def test_write_and_load_materialized_barrage(tmp_path):
    out = tmp_path / "barrage.jsonl"
    items = [_item("character_count", "letters", 1)]

    write_barrage_jsonl(items, out)

    assert json.loads(out.read_text(encoding="utf-8"))["id"] == items[0].id


def test_load_split_items_reads_all_split_jsonl_files(tmp_path):
    split_dir = tmp_path / "public_v0"
    split_dir.mkdir()
    (split_dir / "character_count.jsonl").write_text(
        json.dumps(_record("character_count", "letters", 1)) + "\n",
        encoding="utf-8",
    )
    (split_dir / "word_count.jsonl").write_text(
        json.dumps(_record("word_count", "sentences", 2)) + "\n",
        encoding="utf-8",
    )

    items = load_split_items("public_v0", data_dir=tmp_path)

    assert [item.family for item in items] == ["character_count", "word_count"]
