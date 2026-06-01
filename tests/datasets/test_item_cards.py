from __future__ import annotations

import json
from pathlib import Path

import pytest

from obviousbench.datasets.item_cards import ItemCardLoadError, load_item_cards
from obviousbench.datasets.validation import validate_dataset_paths
from tests.datasets.test_schemas import valid_record


def _write_jsonl(path: Path, rows: list[dict]) -> None:
    path.write_text("\n".join(json.dumps(row) for row in rows) + "\n", encoding="utf-8")


def _card_yaml(
    *,
    item_id: str = "obviousbench.char_count.en.v0.public.000001",
    expected_answer: str = "3",
    scorer: str = "exact_integer_extract_first_v0",
    answer_type: str = "integer",
    status: str = "reviewed",
    allowed_splits: list[str] | None = None,
    answer_derivation: str = "Counting the r characters in strawberry gives 3.",
    ambiguity_notes: list[str] | None = None,
) -> str:
    allowed_splits = allowed_splits or ["public_v0"]
    ambiguity_notes = ambiguity_notes or ["The spelling and character are explicit."]
    return (
        "cards:\n"
        f"  - item_id: {item_id}\n"
        "    archetype_id: generated.character_count.unit_test.000001\n"
        "    source_refs: [src_strawberry_public_discussion]\n"
        "    source_type: public_archetype\n"
        "    source_summary: Unit test item card.\n"
        f"    answer_derivation: {answer_derivation}\n"
        f"    expected_answer: {expected_answer!r}\n"
        "    scorer_contract:\n"
        f"      scorer: {scorer}\n"
        f"      answer_type: {answer_type}\n"
        "      strict_format: false\n"
        f"      acceptable_outputs: [{expected_answer!r}]\n"
        "      unacceptable_outputs: ['2']\n"
        "    ambiguity_notes:\n"
        + "".join(f"      - {note}\n" for note in ambiguity_notes)
        + "    split_policy:\n"
        f"      allowed_splits: {allowed_splits}\n"
        "      leakage_risk: low\n"
        "      publishable: true\n"
        "      rationale: Generated control item.\n"
        "    review:\n"
        f"      status: {status}\n"
        "      reviewer: test\n"
        "      reviewed_on: '2026-05-31'\n"
        "      notes: Unit test card.\n"
    )


def _write_card(cards_dir: Path, yaml_text: str, filename: str = "cards.yaml") -> Path:
    split_dir = cards_dir / "public_v0"
    split_dir.mkdir(parents=True, exist_ok=True)
    path = split_dir / filename
    path.write_text(yaml_text, encoding="utf-8")
    return path


def test_load_item_cards_indexes_by_item_id(tmp_path: Path):
    cards_dir = tmp_path / "data" / "item_cards"
    _write_card(cards_dir, _card_yaml())

    cards = load_item_cards(cards_dir)

    assert "obviousbench.char_count.en.v0.public.000001" in cards.by_item_id
    assert cards.by_item_id["obviousbench.char_count.en.v0.public.000001"].expected_answer == "3"


def test_load_item_cards_rejects_duplicate_item_ids(tmp_path: Path):
    cards_dir = tmp_path / "data" / "item_cards"
    _write_card(cards_dir, _card_yaml(), "a.yaml")
    _write_card(cards_dir, _card_yaml(), "b.yaml")

    with pytest.raises(ItemCardLoadError, match="Duplicate item card"):
        load_item_cards(cards_dir)


def test_load_item_cards_rejects_missing_directory(tmp_path: Path):
    with pytest.raises(ItemCardLoadError, match="directory does not exist"):
        load_item_cards(tmp_path / "missing_cards")


def test_card_validation_reports_missing_cards_directory(tmp_path: Path):
    dataset_path = tmp_path / "items.jsonl"
    _write_jsonl(dataset_path, [valid_record()])

    report = validate_dataset_paths(
        [dataset_path], item_cards_dir=tmp_path / "missing_cards"
    )

    assert "invalid_item_card" in {issue.code for issue in report.issues}


def test_card_required_validation_reports_missing_card(tmp_path: Path):
    dataset_path = tmp_path / "items.jsonl"
    cards_dir = tmp_path / "item_cards"
    cards_dir.mkdir()
    _write_jsonl(dataset_path, [valid_record()])

    report = validate_dataset_paths(
        [dataset_path], item_cards_dir=cards_dir, require_item_cards=True
    )

    assert "missing_item_card" in {issue.code for issue in report.issues}


def test_card_required_validation_requires_cards_directory(tmp_path: Path):
    dataset_path = tmp_path / "items.jsonl"
    _write_jsonl(dataset_path, [valid_record()])

    report = validate_dataset_paths([dataset_path], require_item_cards=True)

    assert "missing_item_cards_dir" in {issue.code for issue in report.issues}


def test_card_required_validation_reports_draft_card(tmp_path: Path):
    dataset_path = tmp_path / "items.jsonl"
    cards_dir = tmp_path / "item_cards"
    _write_jsonl(dataset_path, [valid_record()])
    _write_card(cards_dir, _card_yaml(status="draft"))

    report = validate_dataset_paths(
        [dataset_path], item_cards_dir=cards_dir, require_item_cards=True
    )

    assert "draft_item_card" in {issue.code for issue in report.issues}


@pytest.mark.parametrize(
    ("card_kwargs", "expected_code"),
    [
        ({"expected_answer": "4"}, "item_card_target_mismatch"),
        ({"scorer": "exact_string_trim_v0"}, "item_card_scorer_mismatch"),
        ({"answer_type": "string"}, "item_card_answer_type_mismatch"),
        ({"allowed_splits": ["calibration_v0"]}, "item_card_split_mismatch"),
    ],
)
def test_card_validation_reports_card_dataset_mismatch(
    tmp_path: Path, card_kwargs: dict, expected_code: str
):
    dataset_path = tmp_path / "items.jsonl"
    cards_dir = tmp_path / "item_cards"
    _write_jsonl(dataset_path, [valid_record()])
    _write_card(cards_dir, _card_yaml(**card_kwargs))

    report = validate_dataset_paths([dataset_path], item_cards_dir=cards_dir)

    assert expected_code in {issue.code for issue in report.issues}


def test_card_validation_reports_extra_cards_by_default(tmp_path: Path):
    dataset_path = tmp_path / "items.jsonl"
    cards_dir = tmp_path / "item_cards"
    _write_jsonl(dataset_path, [valid_record()])
    _write_card(
        cards_dir,
        _card_yaml(
            item_id="obviousbench.char_count.en.v0.public.999999",
            expected_answer="9",
        ),
    )

    report = validate_dataset_paths([dataset_path], item_cards_dir=cards_dir)

    assert "extra_item_card" in {issue.code for issue in report.issues}


def test_card_validation_allows_extra_cards_when_requested(tmp_path: Path):
    dataset_path = tmp_path / "items.jsonl"
    cards_dir = tmp_path / "item_cards"
    _write_jsonl(dataset_path, [valid_record()])
    _write_card(
        cards_dir,
        _card_yaml(
            item_id="obviousbench.char_count.en.v0.public.999999",
            expected_answer="9",
        ),
    )

    report = validate_dataset_paths(
        [dataset_path],
        item_cards_dir=cards_dir,
        allow_extra_item_cards=True,
    )

    assert "extra_item_card" not in {issue.code for issue in report.issues}


def test_card_validation_reports_blank_answer_derivation(tmp_path: Path):
    dataset_path = tmp_path / "items.jsonl"
    cards_dir = tmp_path / "item_cards"
    _write_jsonl(dataset_path, [valid_record()])
    _write_card(cards_dir, _card_yaml(answer_derivation='""'))

    report = validate_dataset_paths([dataset_path], item_cards_dir=cards_dir)

    assert "invalid_item_card" in {issue.code for issue in report.issues}


@pytest.mark.parametrize(
    "card_kwargs",
    [
        {"scorer": "not_a_scorer_v0"},
        {"answer_type": "not_an_answer_type"},
        {"allowed_splits": ["dev_v1"]},
    ],
)
def test_load_item_cards_rejects_unknown_contract_domains(
    tmp_path: Path, card_kwargs: dict
):
    cards_dir = tmp_path / "item_cards"
    _write_card(cards_dir, _card_yaml(**card_kwargs))

    with pytest.raises(ItemCardLoadError, match="Invalid item card"):
        load_item_cards(cards_dir)
