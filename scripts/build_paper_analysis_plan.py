#!/usr/bin/env python
"""Build the ObviousBench paper analysis-plan report."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from obviousbench.research.paper_analysis_plan import (  # noqa: E402
    PaperAnalysisPlanInputs,
    build_paper_analysis_plan,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="build_paper_analysis_plan.py")
    parser.add_argument("--plan", default="configs/paper_v1_analysis_plan.yaml")
    parser.add_argument(
        "--out",
        default="docs/research/2026-06-01-obviousbench-paper-analysis-plan.md",
    )
    args = parser.parse_args(argv)

    result = build_paper_analysis_plan(
        PaperAnalysisPlanInputs(
            plan_path=Path(args.plan),
            output_path=Path(args.out),
        )
    )
    print(
        f"Wrote paper analysis plan to {result.output_path}: "
        f"{len(result.issues)} issue(s), "
        f"{result.primary_metric_count} primary metric(s)"
    )
    return 0 if result.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
