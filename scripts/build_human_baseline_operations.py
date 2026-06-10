#!/usr/bin/env python
"""Build the ObviousBench human-baseline operations packet."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from obviousbench.research.human_baseline_operations import (  # noqa: E402
    HumanBaselineOperationsInputs,
    build_human_baseline_operations_packet,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="build_human_baseline_operations.py")
    parser.add_argument(
        "--out",
        default="docs/research/2026-06-01-paper-v1-human-baseline-operations.md",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Return nonzero while human-baseline operations remain blocked.",
    )
    args = parser.parse_args(argv)

    result = build_human_baseline_operations_packet(
        HumanBaselineOperationsInputs(output_path=Path(args.out))
    )
    print(
        f"Wrote human-baseline operations packet to {result.output_path}: "
        f"{result.passed_count} passed, {result.blocked_count} blocked"
    )
    return 0 if result.ok or not args.strict else 1


if __name__ == "__main__":
    raise SystemExit(main())
