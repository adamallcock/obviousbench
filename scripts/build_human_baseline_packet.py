#!/usr/bin/env python
"""Build paper human-baseline assignment packets."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from obviousbench.research.human_baseline_packet import (  # noqa: E402
    HumanBaselinePacketInputs,
    build_human_baseline_packet,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="build_human_baseline_packet.py")
    parser.add_argument("--manifest", default="data/splits/paper_v1_manifest.jsonl")
    parser.add_argument(
        "--dataset",
        action="append",
        dest="datasets",
        help=(
            "Dataset JSONL file. Repeat for multiple files. "
            "Defaults to data/public_v0/*.jsonl."
        ),
    )
    parser.add_argument("--participants", type=int, default=5)
    parser.add_argument("--seed", type=int, default=20260601)
    parser.add_argument(
        "--summary-out",
        default="docs/research/2026-06-01-paper-v1-human-baseline-collection-packet.md",
    )
    parser.add_argument(
        "--participant-packets-out",
        default="docs/research/2026-06-01-paper-v1-human-baseline-participant-packets.md",
    )
    parser.add_argument(
        "--assignments-out",
        default="data/human_baseline/paper_v1_assignments.csv",
    )
    parser.add_argument(
        "--response-template-out",
        default="data/human_baseline/paper_v1_response_template.csv",
    )
    parser.add_argument(
        "--answer-key-out",
        default="data/human_baseline/paper_v1_answer_key.csv",
    )
    args = parser.parse_args(argv)

    datasets = (
        [Path(path) for path in args.datasets]
        if args.datasets
        else sorted(Path("data/public_v0").glob("*.jsonl"))
    )
    result = build_human_baseline_packet(
        HumanBaselinePacketInputs(
            manifest_path=Path(args.manifest),
            dataset_paths=datasets,
            summary_path=Path(args.summary_out),
            participant_packets_path=Path(args.participant_packets_out),
            assignment_csv_path=Path(args.assignments_out),
            response_template_path=Path(args.response_template_out),
            answer_key_path=Path(args.answer_key_out),
            participant_count=args.participants,
            seed=args.seed,
        )
    )
    print(
        f"Wrote human-baseline packet to {result.summary_path}: "
        f"{result.item_count} item(s), {result.participant_count} participant(s), "
        f"{result.assignment_count} assignment row(s)"
    )
    return 0 if result.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
