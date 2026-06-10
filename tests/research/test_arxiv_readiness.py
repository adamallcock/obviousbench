from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from obviousbench.research.arxiv_readiness import (
    ArxivReadinessInputs,
    audit_arxiv_readiness,
)
from tests.datasets.test_schemas import valid_record

MANIFEST_ROW = '{"item_id":"obviousbench.char_count.en.v0.public.000001"}\n'


def _write_jsonl(path: Path, rows: list[dict]) -> None:
    path.write_text("\n".join(json.dumps(row) for row in rows) + "\n", encoding="utf-8")


def _write_card(
    cards_dir: Path,
    *,
    status: str = "reviewed",
    source_summary: str = "Generated control item derived from a public archetype.",
    answer_derivation: str = "Counting the r characters in strawberry gives 3.",
    ambiguity_note: str = "The spelling and character are explicit.",
) -> None:
    split_dir = cards_dir / "public_v0"
    split_dir.mkdir(parents=True, exist_ok=True)
    (split_dir / "cards.yaml").write_text(
        f"""
cards:
  - item_id: obviousbench.char_count.en.v0.public.000001
    archetype_id: generated.character_count.unit_test.000001
    source_refs: [src_strawberry_public_discussion]
    source_type: public_archetype
    source_summary: {source_summary!r}
    answer_derivation: {answer_derivation!r}
    expected_answer: "3"
    scorer_contract:
      scorer: exact_integer_extract_first_v0
      answer_type: integer
      strict_format: false
      acceptable_outputs: ["3"]
      unacceptable_outputs: ["2"]
    ambiguity_notes:
      - {ambiguity_note!r}
    split_policy:
      allowed_splits: [public_v0]
      leakage_risk: low
      publishable: true
      rationale: Generated control item is safe for public release.
    review:
      status: {status}
      reviewer: test
      reviewed_on: "2026-06-01"
      notes: Unit test card.
""".lstrip(),
        encoding="utf-8",
    )


def _write_gold(gold_dir: Path, *, count: int = 2) -> None:
    gold_dir.mkdir(parents=True, exist_ok=True)
    examples = []
    for index in range(count):
        examples.append(
            f"""
  - id: exact_integer.unit.{index}
    scorer: exact_integer_extract_first_v0
    target: "3"
    output: "3"
    expected:
      answer_correct: true
      format_correct: true
      strict_correct: true
      failure_type: none
    notes: Unit test example {index}.
""".rstrip()
        )
    (gold_dir / "exact_integer_extract_first_v0.yaml").write_text(
        "examples:\n" + "\n".join(examples) + "\n",
        encoding="utf-8",
    )


def test_audit_passes_when_required_paper_readiness_inputs_exist(tmp_path: Path):
    dataset_path = tmp_path / "items.jsonl"
    cards_dir = tmp_path / "item_cards"
    gold_dir = tmp_path / "scorer_gold"
    human_baseline = tmp_path / "human_baseline.csv"
    paper_manifest = tmp_path / "paper_v1_manifest.jsonl"
    _write_jsonl(dataset_path, [valid_record()])
    _write_card(cards_dir)
    _write_gold(gold_dir)
    human_baseline.write_text(
        (
            "item_id,participant_id,answer,seconds,correct,notes\n"
            "obviousbench.char_count.en.v0.public.000001,p1,3,2.4,true,\n"
        ),
        encoding="utf-8",
    )
    paper_manifest.write_text(MANIFEST_ROW, encoding="utf-8")

    report = audit_arxiv_readiness(
        ArxivReadinessInputs(
            dataset_paths=[dataset_path],
            item_cards_dir=cards_dir,
            scorer_gold_dir=gold_dir,
            human_baseline_path=human_baseline,
            paper_manifest_path=paper_manifest,
            min_gold_examples_per_scorer=2,
            min_human_participants=1,
        )
    )

    assert report.ok
    assert {gate.name for gate in report.gates} == {
        "dataset validation",
        "item-card review",
        "scorer-gold coverage",
        "human baseline",
        "paper split manifest",
    }


def test_audit_blocks_draft_or_placeholder_item_cards(tmp_path: Path):
    dataset_path = tmp_path / "items.jsonl"
    cards_dir = tmp_path / "item_cards"
    gold_dir = tmp_path / "scorer_gold"
    _write_jsonl(dataset_path, [valid_record()])
    _write_card(
        cards_dir,
        status="draft",
        source_summary="TODO(review): summarize source evidence.",
    )
    _write_gold(gold_dir)

    report = audit_arxiv_readiness(
        ArxivReadinessInputs(
            dataset_paths=[dataset_path],
            item_cards_dir=cards_dir,
            scorer_gold_dir=gold_dir,
            human_baseline_path=None,
            paper_manifest_path=None,
            min_gold_examples_per_scorer=2,
        )
    )

    assert not report.ok
    item_gate = report.gate_by_name("item-card review")
    assert item_gate.status == "fail"
    assert "draft item cards" in item_gate.message
    assert "placeholder text" in item_gate.message


def test_audit_blocks_missing_gold_for_used_scorer(tmp_path: Path):
    dataset_path = tmp_path / "items.jsonl"
    cards_dir = tmp_path / "item_cards"
    gold_dir = tmp_path / "scorer_gold"
    human_baseline = tmp_path / "human_baseline.csv"
    paper_manifest = tmp_path / "paper_v1_manifest.jsonl"
    _write_jsonl(dataset_path, [valid_record()])
    _write_card(cards_dir)
    _write_gold(gold_dir, count=1)
    human_baseline.write_text(
        (
            "item_id,participant_id,answer,seconds,correct,notes\n"
            "obviousbench.char_count.en.v0.public.000001,p1,3,2.4,true,\n"
        ),
        encoding="utf-8",
    )
    paper_manifest.write_text(MANIFEST_ROW, encoding="utf-8")

    report = audit_arxiv_readiness(
        ArxivReadinessInputs(
            dataset_paths=[dataset_path],
            item_cards_dir=cards_dir,
            scorer_gold_dir=gold_dir,
            human_baseline_path=human_baseline,
            paper_manifest_path=paper_manifest,
            min_gold_examples_per_scorer=2,
        )
    )

    assert not report.ok
    assert report.gate_by_name("scorer-gold coverage").status == "fail"
    assert "exact_integer_extract_first_v0 has 1/2" in report.to_markdown()


def test_audit_script_writes_markdown_report(tmp_path: Path):
    dataset_path = tmp_path / "items.jsonl"
    cards_dir = tmp_path / "item_cards"
    gold_dir = tmp_path / "scorer_gold"
    human_baseline = tmp_path / "human_baseline.csv"
    paper_manifest = tmp_path / "paper_v1_manifest.jsonl"
    output_path = tmp_path / "audit.md"
    _write_jsonl(dataset_path, [valid_record()])
    _write_card(cards_dir)
    _write_gold(gold_dir)
    human_baseline.write_text(
        (
            "item_id,participant_id,answer,seconds,correct,notes\n"
            "obviousbench.char_count.en.v0.public.000001,p1,3,2.4,true,\n"
        ),
        encoding="utf-8",
    )
    paper_manifest.write_text(MANIFEST_ROW, encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "scripts/audit_arxiv_readiness.py",
            "--dataset",
            str(dataset_path),
            "--item-cards-dir",
            str(cards_dir),
            "--scorer-gold-dir",
            str(gold_dir),
            "--human-baseline",
            str(human_baseline),
            "--paper-manifest",
            str(paper_manifest),
            "--min-gold-examples-per-scorer",
            "2",
            "--min-human-participants",
            "1",
            "--out",
            str(output_path),
        ],
        cwd=Path(__file__).parents[2],
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0
    assert "Overall status: PASS" in result.stdout
    assert "Overall status: PASS" in output_path.read_text(encoding="utf-8")


def test_audit_blocks_human_baseline_with_no_rows(tmp_path: Path):
    dataset_path = tmp_path / "items.jsonl"
    cards_dir = tmp_path / "item_cards"
    gold_dir = tmp_path / "scorer_gold"
    human_baseline = tmp_path / "human_baseline.csv"
    paper_manifest = tmp_path / "paper_v1_manifest.jsonl"
    _write_jsonl(dataset_path, [valid_record()])
    _write_card(cards_dir)
    _write_gold(gold_dir)
    human_baseline.write_text(
        "item_id,participant_id,answer,seconds,correct,notes\n",
        encoding="utf-8",
    )
    paper_manifest.write_text(MANIFEST_ROW, encoding="utf-8")

    report = audit_arxiv_readiness(
        ArxivReadinessInputs(
            dataset_paths=[dataset_path],
            item_cards_dir=cards_dir,
            scorer_gold_dir=gold_dir,
            human_baseline_path=human_baseline,
            paper_manifest_path=paper_manifest,
            min_gold_examples_per_scorer=2,
        )
    )

    assert not report.ok
    assert report.gate_by_name("human baseline").status == "fail"
    assert "no response rows" in report.gate_by_name("human baseline").message


def test_preprint_profile_does_not_block_on_missing_human_rows(tmp_path: Path):
    dataset_path = tmp_path / "items.jsonl"
    cards_dir = tmp_path / "item_cards"
    gold_dir = tmp_path / "scorer_gold"
    human_baseline = tmp_path / "human_baseline.csv"
    paper_manifest = tmp_path / "paper_v1_manifest.jsonl"
    _write_jsonl(dataset_path, [valid_record()])
    _write_card(cards_dir)
    _write_gold(gold_dir)
    human_baseline.write_text(
        "item_id,participant_id,answer,seconds,correct,notes\n",
        encoding="utf-8",
    )
    paper_manifest.write_text(MANIFEST_ROW, encoding="utf-8")

    report = audit_arxiv_readiness(
        ArxivReadinessInputs(
            dataset_paths=[dataset_path],
            item_cards_dir=cards_dir,
            scorer_gold_dir=gold_dir,
            human_baseline_path=human_baseline,
            paper_manifest_path=paper_manifest,
            min_gold_examples_per_scorer=2,
            manifest_scope=True,
            readiness_profile="preprint",
        )
    )

    assert report.ok
    human_gate = report.gate_by_name("human baseline")
    assert human_gate.status == "pass"
    assert "optional under the preprint profile" in human_gate.message
    assert "no response rows" in human_gate.details[0]


def test_audit_blocks_human_baseline_with_too_few_participants(tmp_path: Path):
    dataset_path = tmp_path / "items.jsonl"
    cards_dir = tmp_path / "item_cards"
    gold_dir = tmp_path / "scorer_gold"
    human_baseline = tmp_path / "human_baseline.csv"
    paper_manifest = tmp_path / "paper_v1_manifest.jsonl"
    _write_jsonl(dataset_path, [valid_record()])
    _write_card(cards_dir)
    _write_gold(gold_dir)
    human_baseline.write_text(
        (
            "item_id,participant_id,answer,seconds,correct,notes\n"
            "obviousbench.char_count.en.v0.public.000001,p1,3,2.4,true,\n"
        ),
        encoding="utf-8",
    )
    paper_manifest.write_text(MANIFEST_ROW, encoding="utf-8")

    report = audit_arxiv_readiness(
        ArxivReadinessInputs(
            dataset_paths=[dataset_path],
            item_cards_dir=cards_dir,
            scorer_gold_dir=gold_dir,
            human_baseline_path=human_baseline,
            paper_manifest_path=paper_manifest,
            min_gold_examples_per_scorer=2,
            min_human_participants=2,
        )
    )

    assert not report.ok
    human_gate = report.gate_by_name("human baseline")
    assert human_gate.status == "fail"
    assert "1/2 participant" in human_gate.details[0]


def test_audit_blocks_human_baseline_missing_item_coverage(tmp_path: Path):
    dataset_path = tmp_path / "items.jsonl"
    cards_dir = tmp_path / "item_cards"
    gold_dir = tmp_path / "scorer_gold"
    human_baseline = tmp_path / "human_baseline.csv"
    paper_manifest = tmp_path / "paper_v1_manifest.jsonl"
    paper_item = valid_record()
    uncovered_item = valid_record(id="obviousbench.char_count.en.v0.public.000002")
    _write_jsonl(dataset_path, [paper_item, uncovered_item])
    _write_card(cards_dir)
    _write_gold(gold_dir)
    human_baseline.write_text(
        (
            "item_id,participant_id,answer,seconds,correct,notes\n"
            "obviousbench.char_count.en.v0.public.000001,p1,3,2.4,true,\n"
        ),
        encoding="utf-8",
    )
    paper_manifest.write_text(
        MANIFEST_ROW + '{"item_id":"obviousbench.char_count.en.v0.public.000002"}\n',
        encoding="utf-8",
    )

    report = audit_arxiv_readiness(
        ArxivReadinessInputs(
            dataset_paths=[dataset_path],
            item_cards_dir=cards_dir,
            scorer_gold_dir=gold_dir,
            human_baseline_path=human_baseline,
            paper_manifest_path=paper_manifest,
            min_gold_examples_per_scorer=2,
            min_human_participants=1,
            manifest_scope=True,
        )
    )

    human_gate = report.gate_by_name("human baseline")
    assert human_gate.status == "fail"
    assert "missing responses for 1 item" in human_gate.details[0]


def test_manifest_scoped_audit_ignores_non_paper_item_card_placeholders(tmp_path: Path):
    dataset_path = tmp_path / "items.jsonl"
    cards_dir = tmp_path / "item_cards"
    gold_dir = tmp_path / "scorer_gold"
    human_baseline = tmp_path / "human_baseline.csv"
    paper_manifest = tmp_path / "paper_v1_manifest.jsonl"
    paper_item = valid_record()
    non_paper_item = valid_record()
    non_paper_item["id"] = "obviousbench.char_count.en.v0.public.000002"
    _write_jsonl(dataset_path, [paper_item, non_paper_item])
    cards_split = cards_dir / "public_v0"
    cards_split.mkdir(parents=True)
    cards_split.joinpath("cards.yaml").write_text(
        """
cards:
  - item_id: obviousbench.char_count.en.v0.public.000001
    archetype_id: generated.character_count.unit_test.000001
    source_refs: [src_strawberry_public_discussion]
    source_type: public_archetype
    source_summary: Reviewed source summary.
    answer_derivation: Counting the r characters in strawberry gives 3.
    expected_answer: "3"
    scorer_contract:
      scorer: exact_integer_extract_first_v0
      answer_type: integer
      strict_format: false
      acceptable_outputs: ["3"]
      unacceptable_outputs: ["2"]
    ambiguity_notes: [The spelling and character are explicit.]
    split_policy:
      allowed_splits: [public_v0]
      leakage_risk: low
      publishable: true
      rationale: Generated control item is safe for public release.
    review:
      status: reviewed
      reviewer: test
      reviewed_on: "2026-06-01"
      notes: Unit test card.
  - item_id: obviousbench.char_count.en.v0.public.000002
    archetype_id: generated.character_count.unit_test.000002
    source_refs: [src_strawberry_public_discussion]
    source_type: public_archetype
    source_summary: "TODO(review): summarize source evidence."
    answer_derivation: "TODO(review): derive answer. Draft target: 3"
    expected_answer: "3"
    scorer_contract:
      scorer: exact_integer_extract_first_v0
      answer_type: integer
      strict_format: false
      acceptable_outputs: ["3"]
      unacceptable_outputs: ["2"]
    ambiguity_notes: ["TODO(review): ambiguity notes."]
    split_policy:
      allowed_splits: [public_v0]
      leakage_risk: low
      publishable: true
      rationale: "TODO(review): split rationale."
    review:
      status: draft
      reviewer: unreviewed
      reviewed_on: "2026-06-01"
      notes: Generated card stub requiring human review.
""".lstrip(),
        encoding="utf-8",
    )
    _write_gold(gold_dir)
    human_baseline.write_text(
        (
            "item_id,participant_id,answer,seconds,correct,notes\n"
            "obviousbench.char_count.en.v0.public.000001,p1,3,2.4,true,\n"
        ),
        encoding="utf-8",
    )
    paper_manifest.write_text(MANIFEST_ROW, encoding="utf-8")

    report = audit_arxiv_readiness(
        ArxivReadinessInputs(
            dataset_paths=[dataset_path],
            item_cards_dir=cards_dir,
            scorer_gold_dir=gold_dir,
            human_baseline_path=human_baseline,
            paper_manifest_path=paper_manifest,
            min_gold_examples_per_scorer=2,
            min_human_participants=1,
            manifest_scope=True,
        )
    )

    assert report.ok
