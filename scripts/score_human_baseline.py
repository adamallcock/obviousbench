#!/usr/bin/env python
"""Score paper human-baseline responses."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from obviousbench.research.human_baseline_scoring import (  # noqa: E402
    HumanBaselineScoringInputs,
    score_human_baseline_responses,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="score_human_baseline.py")
    parser.add_argument(
        "--responses",
        default="data/human_baseline/paper_v1_response_template.csv",
    )
    parser.add_argument("--answer-key", default="data/human_baseline/paper_v1_answer_key.csv")
    parser.add_argument(
        "--scored-out",
        default="data/human_baseline/paper_v1_scored_draft.csv",
    )
    parser.add_argument(
        "--report-out",
        default="docs/research/2026-06-01-paper-v1-human-baseline-scoring-report.md",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Return nonzero when the scored response file has issues.",
    )
    args = parser.parse_args(argv)

    result = score_human_baseline_responses(
        HumanBaselineScoringInputs(
            responses_path=Path(args.responses),
            answer_key_path=Path(args.answer_key),
            scored_path=Path(args.scored_out),
            report_path=Path(args.report_out),
        )
    )
    print(
        f"Wrote human-baseline scoring report to {result.report_path}: "
        f"{result.scored_count}/{result.row_count} scored row(s), "
        f"{result.issue_count} issue(s)"
    )
    return 0 if result.ok or not args.strict else 1


if __name__ == "__main__":
    raise SystemExit(main())
