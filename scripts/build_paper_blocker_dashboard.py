#!/usr/bin/env python
"""Build the ObviousBench arXiv blocker dashboard."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from obviousbench.research.paper_blocker_dashboard import (  # noqa: E402
    PaperBlockerDashboardInputs,
    build_paper_blocker_dashboard,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="build_paper_blocker_dashboard.py")
    parser.add_argument(
        "--out",
        default="docs/research/2026-06-01-obviousbench-arxiv-blocker-dashboard.md",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Return nonzero when any blocker remains blocked or waiting.",
    )
    parser.add_argument(
        "--publication-mode",
        choices=("strict", "preprint"),
        default="preprint",
        help=(
            "strict treats human collection as a blocker; preprint defers "
            "human-baseline validation and blocks measured-human claims instead."
        ),
    )
    args = parser.parse_args(argv)

    result = build_paper_blocker_dashboard(
        PaperBlockerDashboardInputs(
            output_path=Path(args.out),
            publication_mode=args.publication_mode,
        )
    )
    print(
        f"Wrote paper blocker dashboard to {result.output_path}: "
        f"{result.pass_count} passed, {result.blocked_count} blocked, "
        f"{result.waiting_count} waiting"
    )
    return 0 if result.ok or not args.strict else 1


if __name__ == "__main__":
    raise SystemExit(main())
