from __future__ import annotations

import json
from pathlib import Path

import yaml

from scripts.generate_item_card_stubs import generate_item_card_stubs, main
from tests.datasets.test_schemas import valid_record


def test_generate_item_card_stubs_writes_draft_cards(tmp_path: Path):
    dataset_path = tmp_path / "items.jsonl"
    out = tmp_path / "item_cards" / "public_v0" / "cards.yaml"
    row = valid_record(
        id="obviousbench.char_count.en.v0.public.000777",
        target="3",
        answer_type="integer",
        scorer="exact_integer_extract_first_v0",
        source_refs=["src_fixture"],
    )
    dataset_path.write_text(json.dumps(row) + "\n", encoding="utf-8")

    generate_item_card_stubs([dataset_path], out, generated_on="2026-05-31")

    payload = yaml.safe_load(out.read_text(encoding="utf-8"))
    card = payload["cards"][0]
    assert card["item_id"] == "obviousbench.char_count.en.v0.public.000777"
    assert card["expected_answer"] == "3"
    assert card["source_refs"] == ["src_fixture"]
    assert card["scorer_contract"]["answer_type"] == "integer"
    assert card["scorer_contract"]["scorer"] == "exact_integer_extract_first_v0"
    assert card["review"]["status"] == "draft"
    assert "TODO(review)" in card["answer_derivation"]
    assert "TODO(review)" in card["ambiguity_notes"][0]


def test_generate_item_card_stubs_cli_accepts_positional_datasets(tmp_path: Path):
    dataset_path = tmp_path / "items.jsonl"
    out = tmp_path / "cards.yaml"
    row = valid_record(id="obviousbench.char_count.en.v0.public.000778")
    dataset_path.write_text(json.dumps(row) + "\n", encoding="utf-8")

    result = main(
        [
            str(dataset_path),
            "--out",
            str(out),
            "--generated-on",
            "2026-05-31",
        ]
    )

    assert result == 0
    assert yaml.safe_load(out.read_text(encoding="utf-8"))["cards"][0]["item_id"] == (
        "obviousbench.char_count.en.v0.public.000778"
    )
