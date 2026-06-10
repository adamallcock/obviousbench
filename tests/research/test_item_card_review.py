from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import yaml

from obviousbench.research.item_card_review import (
    ItemCardPromotionInputs,
    promote_paper_item_cards,
)
from tests.datasets.test_schemas import valid_record


def _write_jsonl(path: Path, rows: list[dict]) -> None:
    path.write_text("\n".join(json.dumps(row) for row in rows) + "\n", encoding="utf-8")


def _draft_card(item_id: str, *, expected_answer: str = "3") -> dict:
    return {
        "item_id": item_id,
        "archetype_id": "src_strawberry_public_discussion",
        "source_refs": ["src_strawberry_public_discussion"],
        "source_type": "generated_variant",
        "source_summary": "TODO(review): summarize source evidence before trusted use.",
        "answer_derivation": (
            "TODO(review): explain why the expected answer follows unambiguously "
            f"from the prompt. Draft target: {expected_answer}"
        ),
        "expected_answer": expected_answer,
        "scorer_contract": {
            "scorer": "exact_integer_extract_first_v0",
            "answer_type": "integer",
            "strict_format": False,
            "acceptable_outputs": [expected_answer],
            "unacceptable_outputs": [],
        },
        "ambiguity_notes": [
            "TODO(review): record ambiguity checks and acceptable interpretation boundaries."
        ],
        "split_policy": {
            "allowed_splits": ["public_v0"],
            "leakage_risk": "low",
            "publishable": True,
            "rationale": "TODO(review): confirm split eligibility and publication safety.",
        },
        "review": {
            "status": "draft",
            "reviewer": "unreviewed",
            "reviewed_on": "2026-05-31",
            "notes": "Generated card stub requiring human review.",
        },
    }


def _write_source_catalog(path: Path) -> None:
    _write_jsonl(
        path,
        [
            {
                "source_id": "src_strawberry_public_discussion",
                "platform": "news",
                "url": "https://example.com/strawberry",
                "date_seen": "2026-05-30",
                "author_or_handle": None,
                "original_prompt": "Public simple-failure archetype.",
                "claimed_model": None,
                "claimed_output": None,
                "failure_description": "Lead source for character-count failures.",
                "engagement_signal": {"comments": None, "likes": None, "shares": None},
                "media_type": "article",
                "rights_status": "link_only_do_not_republish",
                "notes": "Treat as a lead or archetype; reproduce independently.",
            }
        ],
    )


def test_promote_paper_item_cards_updates_only_manifest_cards(tmp_path: Path):
    dataset_path = tmp_path / "items.jsonl"
    manifest_path = tmp_path / "paper_v1_manifest.jsonl"
    source_catalog_path = tmp_path / "sources.jsonl"
    cards_path = tmp_path / "cards.yaml"
    paper_item = valid_record()
    non_paper_item = valid_record(id="obviousbench.char_count.en.v0.public.000002")
    _write_jsonl(dataset_path, [paper_item, non_paper_item])
    _write_jsonl(manifest_path, [{"item_id": paper_item["id"]}])
    _write_source_catalog(source_catalog_path)
    cards_path.write_text(
        yaml.safe_dump(
            {
                "cards": [
                    _draft_card(paper_item["id"]),
                    _draft_card(non_paper_item["id"]),
                ]
            },
            sort_keys=False,
        ),
        encoding="utf-8",
    )

    result = promote_paper_item_cards(
        ItemCardPromotionInputs(
            manifest_path=manifest_path,
            dataset_paths=[dataset_path],
            source_catalog_path=source_catalog_path,
            cards_path=cards_path,
            reviewed_on="2026-06-01",
        )
    )

    payload = yaml.safe_load(cards_path.read_text(encoding="utf-8"))
    paper_card, non_paper_card = payload["cards"]
    assert result.promoted_count == 1
    assert result.missing_card_ids == ()
    assert paper_card["review"]["status"] == "reviewed"
    assert paper_card["review"]["reviewer"] == "codex-paper-review-v1"
    assert "strawberry contains 3 occurrence(s) of 'r'" in paper_card["answer_derivation"]
    assert "TODO" not in json.dumps(paper_card)
    assert non_paper_card["review"]["status"] == "draft"
    assert "TODO(review)" in non_paper_card["source_summary"]


def test_promote_paper_item_cards_script_updates_cards_yaml(tmp_path: Path):
    dataset_path = tmp_path / "items.jsonl"
    manifest_path = tmp_path / "paper_v1_manifest.jsonl"
    source_catalog_path = tmp_path / "sources.jsonl"
    cards_path = tmp_path / "cards.yaml"
    item = valid_record()
    _write_jsonl(dataset_path, [item])
    _write_jsonl(manifest_path, [{"item_id": item["id"]}])
    _write_source_catalog(source_catalog_path)
    cards_path.write_text(
        yaml.safe_dump({"cards": [_draft_card(item["id"])]}, sort_keys=False),
        encoding="utf-8",
    )

    result = subprocess.run(
        [
            sys.executable,
            "scripts/promote_paper_item_cards.py",
            "--manifest",
            str(manifest_path),
            "--dataset",
            str(dataset_path),
            "--source-catalog",
            str(source_catalog_path),
            "--cards",
            str(cards_path),
        ],
        cwd=Path(__file__).parents[2],
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0
    assert "Promoted 1 paper item card" in result.stdout
    payload = yaml.safe_load(cards_path.read_text(encoding="utf-8"))
    assert payload["cards"][0]["review"]["status"] == "reviewed"
