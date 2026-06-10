from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from obviousbench.research.item_review_queue import (
    ItemReviewQueueInputs,
    build_item_review_queue,
)
from tests.datasets.test_schemas import valid_record
from tests.research.test_arxiv_readiness import _write_card

MANIFEST_ROW = (
    '{"item_id":"obviousbench.char_count.en.v0.public.000001",'
    '"family":"character_count","subfamily":"single_letter_count",'
    '"scorer":"exact_integer_extract_first_v0"}\n'
)


def _write_jsonl(path: Path, rows: list[dict]) -> None:
    path.write_text("\n".join(json.dumps(row) for row in rows) + "\n", encoding="utf-8")


def test_build_item_review_queue_groups_manifest_items_by_family(tmp_path: Path):
    dataset_path = tmp_path / "items.jsonl"
    manifest_path = tmp_path / "paper_v1_manifest.jsonl"
    cards_dir = tmp_path / "item_cards"
    output_path = tmp_path / "queue.md"
    _write_jsonl(dataset_path, [valid_record()])
    manifest_path.write_text(MANIFEST_ROW, encoding="utf-8")
    _write_card(cards_dir, status="draft")

    result = build_item_review_queue(
        ItemReviewQueueInputs(
            manifest_path=manifest_path,
            dataset_paths=[dataset_path],
            item_cards_dir=cards_dir,
            output_path=output_path,
        )
    )

    text = output_path.read_text(encoding="utf-8")
    assert result.item_count == 1
    assert result.blocked_count == 1
    assert "## character_count" in text
    assert "obviousbench.char_count.en.v0.public.000001" in text
    assert "draft_card" in text
    assert "placeholder_text" not in text


def test_item_review_queue_script_writes_markdown(tmp_path: Path):
    dataset_path = tmp_path / "items.jsonl"
    manifest_path = tmp_path / "paper_v1_manifest.jsonl"
    cards_dir = tmp_path / "item_cards"
    output_path = tmp_path / "queue.md"
    _write_jsonl(dataset_path, [valid_record()])
    manifest_path.write_text(MANIFEST_ROW, encoding="utf-8")
    _write_card(cards_dir, status="reviewed")

    result = subprocess.run(
        [
            sys.executable,
            "scripts/build_item_review_queue.py",
            "--manifest",
            str(manifest_path),
            "--dataset",
            str(dataset_path),
            "--item-cards-dir",
            str(cards_dir),
            "--out",
            str(output_path),
        ],
        cwd=Path(__file__).parents[2],
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0
    assert "Wrote 1 item review rows" in result.stdout
    assert output_path.exists()
