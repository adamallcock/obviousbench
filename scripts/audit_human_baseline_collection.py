#!/usr/bin/env python
"""Audit human-baseline response collection before scoring."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from obviousbench.research.human_baseline_collection_audit import (  # noqa: E402
    HumanBaselineCollectionAuditInputs,
    audit_human_baseline_collection,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="audit_human_baseline_collection.py")
    parser.add_argument(
        "--assignments",
        default="data/human_baseline/paper_v1_assignments.csv",
    )
    parser.add_argument(
        "--responses",
        default="data/human_baseline/paper_v1_response_template.csv",
    )
    parser.add_argument("--answer-key", default="data/human_baseline/paper_v1_answer_key.csv")
    parser.add_argument(
        "--out",
        default="docs/research/2026-06-01-paper-v1-human-baseline-collection-audit.md",
    )
    parser.add_argument("--expected-participants", type=int, default=5)
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Return nonzero when collection is incomplete or structurally invalid.",
    )
    args = parser.parse_args(argv)

    result = audit_human_baseline_collection(
        HumanBaselineCollectionAuditInputs(
            assignments_path=Path(args.assignments),
            responses_path=Path(args.responses),
            answer_key_path=Path(args.answer_key),
            report_path=Path(args.out),
            expected_participants=args.expected_participants,
        )
    )
    print(
        f"Wrote human-baseline collection audit to {result.report_path}: "
        f"{result.completed_row_count}/{result.expected_response_rows} complete row(s), "
        f"{result.issue_count} structural issue(s)"
    )
    return 0 if result.ok or not args.strict else 1


if __name__ == "__main__":
    raise SystemExit(main())
