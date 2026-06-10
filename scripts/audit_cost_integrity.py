#!/usr/bin/env python
"""Audit paper comparison costs for missing or partial accounting."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from obviousbench.research.cost_integrity import (  # noqa: E402
    CostIntegrityInputs,
    audit_cost_integrity,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="audit_cost_integrity.py")
    parser.add_argument(
        "--comparison",
        default=(
            "results/summaries/paper-v1-8x28-current-222-final-20260602/"
            "comparison/comparison.csv"
        ),
    )
    parser.add_argument(
        "--selection-audit",
        default="results/summaries/paper-v1-8x28-current-222-final-20260602/selection-audit.csv",
    )
    parser.add_argument(
        "--out",
        default="docs/research/2026-06-03-paper-v1-cost-integrity-audit.md",
    )
    parser.add_argument("--low-usd-per-mtok", type=float, default=0.01)
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Return nonzero when cost integrity issues are present.",
    )
    args = parser.parse_args(argv)

    result = audit_cost_integrity(
        CostIntegrityInputs(
            comparison_path=Path(args.comparison),
            selection_audit_path=Path(args.selection_audit) if args.selection_audit else None,
            output_path=Path(args.out),
            low_usd_per_mtok=args.low_usd_per_mtok,
        )
    )
    status = "PASS" if result.ok else "BLOCKED"
    print(
        f"Wrote cost integrity audit to {result.output_path}: "
        f"{status}, {len(result.findings)} finding(s)"
    )
    return 0 if result.ok or not args.strict else 1


if __name__ == "__main__":
    raise SystemExit(main())
