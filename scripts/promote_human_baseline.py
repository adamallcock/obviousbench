#!/usr/bin/env python
"""Audit and optionally apply ObviousBench human-baseline promotion."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from obviousbench.research.human_baseline_promotion import (  # noqa: E402
    HumanBaselinePromotionInputs,
    build_human_baseline_promotion_report,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="promote_human_baseline.py")
    parser.add_argument("--scored", default="data/human_baseline/paper_v1_scored_draft.csv")
    parser.add_argument("--promoted", default="data/human_baseline/paper_v1.csv")
    parser.add_argument(
        "--collection-audit",
        default=(
            "docs/research/2026-06-01-paper-v1-human-baseline-collection-audit.md"
        ),
    )
    parser.add_argument(
        "--scoring-report",
        default="docs/research/2026-06-01-paper-v1-human-baseline-scoring-report.md",
    )
    parser.add_argument(
        "--threshold-audit",
        default="docs/research/2026-06-01-paper-v1-human-baseline-threshold-audit.md",
    )
    parser.add_argument(
        "--threshold-items",
        default="data/human_baseline/paper_v1_threshold_items.csv",
    )
    parser.add_argument(
        "--out",
        default="docs/research/2026-06-01-paper-v1-human-baseline-promotion-report.md",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Write the promoted CSV when all promotion checks pass.",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit nonzero until promotion checks pass.",
    )
    args = parser.parse_args(argv)

    result = build_human_baseline_promotion_report(
        HumanBaselinePromotionInputs(
            output_path=Path(args.out),
            scored_path=Path(args.scored),
            promoted_path=Path(args.promoted),
            collection_audit_path=Path(args.collection_audit),
            scoring_report_path=Path(args.scoring_report),
            threshold_audit_path=Path(args.threshold_audit),
            threshold_items_path=Path(args.threshold_items),
        ),
        apply=args.apply,
    )
    action = "applied" if result.applied else "audited"
    print(
        f"Human-baseline promotion {action}: {result.status}, "
        f"{result.source_rows} source row(s), {result.promoted_rows} target row(s)"
    )
    if args.apply and not result.ok:
        return 1
    return 0 if result.ok or not args.strict else 1


if __name__ == "__main__":
    raise SystemExit(main())
