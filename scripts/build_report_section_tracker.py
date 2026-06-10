#!/usr/bin/env python
"""Build the ObviousBench report section tracker."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from obviousbench.research.report_section_tracker import (  # noqa: E402
    ReportSectionTrackerInputs,
    build_report_section_tracker,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="build_report_section_tracker.py")
    parser.add_argument("--paper-dir", default="paper")
    parser.add_argument(
        "--out",
        default="docs/research/2026-06-01-obviousbench-report-section-tracker.md",
    )
    args = parser.parse_args(argv)

    result = build_report_section_tracker(
        ReportSectionTrackerInputs(
            paper_dir=Path(args.paper_dir),
            output_path=Path(args.out),
        )
    )
    print(
        f"Wrote report section tracker to {result.output_path}: "
        f"{len(result.entries)} section entrie(s), "
        f"{result.blocked_count} blocked"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
