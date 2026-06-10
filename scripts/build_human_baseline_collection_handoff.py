#!/usr/bin/env python
"""Build the ObviousBench human-baseline collection handoff."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from obviousbench.research.human_baseline_collection_handoff import (  # noqa: E402
    HumanBaselineCollectionHandoffInputs,
    build_human_baseline_collection_handoff,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="build_human_baseline_collection_handoff.py")
    parser.add_argument("--assignments", default="data/human_baseline/paper_v1_assignments.csv")
    parser.add_argument(
        "--responses",
        default="data/human_baseline/paper_v1_response_template.csv",
    )
    parser.add_argument("--answer-key", default="data/human_baseline/paper_v1_answer_key.csv")
    parser.add_argument(
        "--participant-packets",
        default=(
            "docs/research/"
            "2026-06-01-paper-v1-human-baseline-participant-packets.md"
        ),
    )
    parser.add_argument(
        "--collection-packet",
        default=(
            "docs/research/2026-06-01-paper-v1-human-baseline-collection-packet.md"
        ),
    )
    parser.add_argument(
        "--collection-audit",
        default=(
            "docs/research/2026-06-01-paper-v1-human-baseline-collection-audit.md"
        ),
    )
    parser.add_argument(
        "--out",
        default=(
            "docs/research/2026-06-01-paper-v1-human-baseline-collection-handoff.md"
        ),
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit nonzero until the collection handoff is ready for scoring.",
    )
    args = parser.parse_args(argv)

    result = build_human_baseline_collection_handoff(
        HumanBaselineCollectionHandoffInputs(
            output_path=Path(args.out),
            assignments_path=Path(args.assignments),
            responses_path=Path(args.responses),
            answer_key_path=Path(args.answer_key),
            participant_packets_path=Path(args.participant_packets),
            collection_packet_path=Path(args.collection_packet),
            collection_audit_path=Path(args.collection_audit),
        )
    )
    print(
        f"Wrote human-baseline collection handoff to {result.output_path}: "
        f"{result.status}, {result.completed_rows}/{result.response_rows} complete"
    )
    return 0 if result.ok or not args.strict else 1


if __name__ == "__main__":
    raise SystemExit(main())
