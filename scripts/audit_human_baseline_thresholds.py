#!/usr/bin/env python
"""Audit scored human-baseline rows against paper thresholds."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from obviousbench.research.human_baseline_thresholds import (  # noqa: E402
    HumanBaselineThresholdInputs,
    audit_human_baseline_thresholds,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="audit_human_baseline_thresholds.py")
    parser.add_argument(
        "--scored",
        default="data/human_baseline/paper_v1_scored_draft.csv",
    )
    parser.add_argument("--answer-key", default="data/human_baseline/paper_v1_answer_key.csv")
    parser.add_argument(
        "--item-out",
        default="data/human_baseline/paper_v1_threshold_items.csv",
    )
    parser.add_argument(
        "--family-out",
        default="data/human_baseline/paper_v1_threshold_families.csv",
    )
    parser.add_argument(
        "--report-out",
        default="docs/research/2026-06-01-paper-v1-human-baseline-threshold-audit.md",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Return nonzero when threshold audit data is incomplete or invalid.",
    )
    args = parser.parse_args(argv)

    result = audit_human_baseline_thresholds(
        HumanBaselineThresholdInputs(
            scored_path=Path(args.scored),
            answer_key_path=Path(args.answer_key),
            item_output_path=Path(args.item_out),
            family_output_path=Path(args.family_out),
            report_path=Path(args.report_out),
        )
    )
    print(
        f"Wrote human-baseline threshold audit to {result.report_path}: "
        f"{result.core_h0_count} core H0, "
        f"{result.borderline_count} borderline, "
        f"{result.exclude_count} exclude, "
        f"{result.no_data_count} no-data item(s)"
    )
    return 0 if result.ok or not args.strict else 1


if __name__ == "__main__":
    raise SystemExit(main())
