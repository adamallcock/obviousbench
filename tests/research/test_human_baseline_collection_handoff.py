from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from obviousbench.research.human_baseline_collection_handoff import (
    HumanBaselineCollectionHandoffInputs,
    build_human_baseline_collection_handoff,
)


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _fixture(tmp_path: Path, *, complete: bool) -> HumanBaselineCollectionHandoffInputs:
    assignments = tmp_path / "assignments.csv"
    responses = tmp_path / "responses.csv"
    answer_key = tmp_path / "answer-key.csv"
    participant_packets = tmp_path / "participant-packets.md"
    collection_packet = tmp_path / "collection-packet.md"
    collection_audit = tmp_path / "collection-audit.md"
    output_path = tmp_path / "handoff.md"
    _write(
        assignments,
        "participant_id,sequence,item_id,family,prompt\n"
        "p01,1,item-1,character_count,Prompt one\n"
        "p01,2,item-2,word_count,Prompt two\n"
        "p02,1,item-1,character_count,Prompt one\n",
    )
    if complete:
        response_text = (
            "item_id,participant_id,answer,seconds,correct,notes\n"
            "item-1,p01,3,1.2,,\n"
            "item-2,p01,4,2.0,,\n"
            "item-1,p02,3,1.7,,\n"
        )
        audit_status = "PASS"
    else:
        response_text = (
            "item_id,participant_id,answer,seconds,correct,notes\n"
            "item-1,p01,,,,\n"
            "item-2,p01,4,abc,,\n"
            "item-1,p02,3,1.7,,\n"
        )
        audit_status = "BLOCKED"
    _write(responses, response_text)
    _write(answer_key, "item_id,target\nitem-1,3\n")
    _write(participant_packets, "# Participant packets\n")
    _write(collection_packet, "Overall status: PASS\n")
    _write(collection_audit, f"Overall status: {audit_status}\n")
    return HumanBaselineCollectionHandoffInputs(
        output_path=output_path,
        assignments_path=assignments,
        responses_path=responses,
        answer_key_path=answer_key,
        participant_packets_path=participant_packets,
        collection_packet_path=collection_packet,
        collection_audit_path=collection_audit,
    )


def test_collection_handoff_blocks_incomplete_rows(tmp_path: Path):
    inputs = _fixture(tmp_path, complete=False)

    result = build_human_baseline_collection_handoff(inputs)

    assert not result.ok
    assert result.completed_rows == 1
    assert result.missing_answers == 1
    assert result.invalid_seconds == 2
    p01 = next(row for row in result.participants if row.participant_id == "p01")
    assert p01.complete_rows == 0
    text = inputs.output_path.read_text(encoding="utf-8")
    assert "Overall status: BLOCKED" in text
    assert "Do not show `data/human_baseline/paper_v1_answer_key.csv`" in text


def test_collection_handoff_passes_complete_rows(tmp_path: Path):
    inputs = _fixture(tmp_path, complete=True)

    result = build_human_baseline_collection_handoff(inputs)

    assert result.ok
    assert result.completed_rows == 3
    assert result.missing_answers == 0
    assert result.invalid_seconds == 0
    assert "Overall status: PASS" in inputs.output_path.read_text(encoding="utf-8")


def test_collection_handoff_script_can_fail_strictly(tmp_path: Path):
    inputs = _fixture(tmp_path, complete=False)

    result = subprocess.run(
        [
            sys.executable,
            "scripts/build_human_baseline_collection_handoff.py",
            "--assignments",
            str(inputs.assignments_path),
            "--responses",
            str(inputs.responses_path),
            "--answer-key",
            str(inputs.answer_key_path),
            "--participant-packets",
            str(inputs.participant_packets_path),
            "--collection-packet",
            str(inputs.collection_packet_path),
            "--collection-audit",
            str(inputs.collection_audit_path),
            "--out",
            str(inputs.output_path),
            "--strict",
        ],
        cwd=Path(__file__).parents[2],
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 1
    assert "Wrote human-baseline collection handoff" in result.stdout
    assert inputs.output_path.exists()
