from __future__ import annotations

import csv
import json
import subprocess
import sys
from pathlib import Path

from obviousbench.research.human_baseline_packet import (
    HumanBaselinePacketInputs,
    build_human_baseline_packet,
)
from tests.datasets.test_schemas import valid_record


def _write_jsonl(path: Path, rows: list[dict]) -> None:
    path.write_text("\n".join(json.dumps(row) for row in rows) + "\n", encoding="utf-8")


def _rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def _inputs(tmp_path: Path, *, participants: int = 2) -> HumanBaselinePacketInputs:
    dataset_path = tmp_path / "items.jsonl"
    manifest_path = tmp_path / "paper_v1_manifest.jsonl"
    item_one = valid_record()
    item_two = valid_record(
        id="obviousbench.word_count.en.v0.public.000002",
        family="word_count",
        subfamily="comma_list_count",
        question="How many items are in this list: red, blue?",
        prompt=(
            "Answer the question. Return only the final answer, with no explanation.\n\n"
            "Question: How many items are in this list: red, blue?\n"
            "Answer:"
        ),
        target="TARGET_ONLY",
        answer_type="integer",
        scorer="word_count_v0",
    )
    _write_jsonl(dataset_path, [item_one, item_two])
    _write_jsonl(
        manifest_path,
        [{"item_id": item_one["id"]}, {"item_id": item_two["id"]}],
    )
    return HumanBaselinePacketInputs(
        manifest_path=manifest_path,
        dataset_paths=[dataset_path],
        summary_path=tmp_path / "collection-packet.md",
        participant_packets_path=tmp_path / "participant-packets.md",
        assignment_csv_path=tmp_path / "assignments.csv",
        response_template_path=tmp_path / "responses.csv",
        answer_key_path=tmp_path / "answer-key.csv",
        participant_count=participants,
        seed=20260601,
    )


def test_human_baseline_packet_assigns_every_item_to_every_participant(tmp_path: Path):
    inputs = _inputs(tmp_path, participants=2)

    result = build_human_baseline_packet(inputs)

    assignments = _rows(inputs.assignment_csv_path)
    responses = _rows(inputs.response_template_path)
    assert result.ok
    assert result.item_count == 2
    assert result.participant_count == 2
    assert result.assignment_count == 4
    assert len(assignments) == 4
    assert len(responses) == 4
    assert {row["participant_id"] for row in assignments} == {"p01", "p02"}
    assert {row["item_id"] for row in assignments} == {
        "obviousbench.char_count.en.v0.public.000001",
        "obviousbench.word_count.en.v0.public.000002",
    }
    assert all(not row["answer"] for row in responses)
    assert all(not row["correct"] for row in responses)


def test_human_baseline_packet_keeps_targets_out_of_participant_files(tmp_path: Path):
    inputs = _inputs(tmp_path, participants=1)

    build_human_baseline_packet(inputs)

    participant_text = inputs.participant_packets_path.read_text(encoding="utf-8")
    assignment_text = inputs.assignment_csv_path.read_text(encoding="utf-8")
    answer_key_text = inputs.answer_key_path.read_text(encoding="utf-8")
    assert "strawberry" in participant_text
    assert "TARGET_ONLY" not in participant_text
    assert "TARGET_ONLY" not in assignment_text
    assert "TARGET_ONLY" in answer_key_text


def test_human_baseline_packet_script_writes_outputs(tmp_path: Path):
    inputs = _inputs(tmp_path, participants=2)

    result = subprocess.run(
        [
            sys.executable,
            "scripts/build_human_baseline_packet.py",
            "--manifest",
            str(inputs.manifest_path),
            "--dataset",
            str(inputs.dataset_paths[0]),
            "--participants",
            "2",
            "--summary-out",
            str(inputs.summary_path),
            "--participant-packets-out",
            str(inputs.participant_packets_path),
            "--assignments-out",
            str(inputs.assignment_csv_path),
            "--response-template-out",
            str(inputs.response_template_path),
            "--answer-key-out",
            str(inputs.answer_key_path),
        ],
        cwd=Path(__file__).parents[2],
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0
    assert "Wrote human-baseline packet" in result.stdout
    assert inputs.summary_path.exists()
    assert inputs.participant_packets_path.exists()
