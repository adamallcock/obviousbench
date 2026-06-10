#!/usr/bin/env python
"""Build a combined grader-review queue for final sweep failures."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from obviousbench.research.grader_review import (  # noqa: E402
    GraderReviewInputs,
    build_grader_review,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="build_grader_review.py")
    parser.add_argument(
        "--manifest",
        default="configs/paper_v1_final_sweep_manifest.csv",
    )
    parser.add_argument(
        "--raw-root",
        default="results/raw/paper-v1-final-high-cap",
    )
    parser.add_argument(
        "--csv-out",
        default=(
            "docs/reports/2026-06-01-paper-v1-final-high-cap-sweep/"
            "wrong-answer-review.csv"
        ),
    )
    parser.add_argument(
        "--html-out",
        default=(
            "docs/reports/2026-06-01-paper-v1-final-high-cap-sweep/"
            "wrong-answer-review.html"
        ),
    )
    parser.add_argument(
        "--no-rescore",
        action="store_true",
        help="Use scores already stored in Inspect logs instead of rescoring outputs.",
    )
    parser.add_argument(
        "--source",
        choices=("raw-logs", "summary-galleries"),
        default="raw-logs",
        help=(
            "raw-logs reads Inspect .eval files under --raw-root; "
            "summary-galleries rebuilds the same review schema from each "
            "manifest summary_dir/failure_gallery.md plus usage_by_sample.csv."
        ),
    )
    args = parser.parse_args(argv)

    result = build_grader_review(
        GraderReviewInputs(
            manifest_path=Path(args.manifest),
            raw_root=Path(args.raw_root),
            csv_output_path=Path(args.csv_out),
            html_output_path=Path(args.html_out),
            rescore=not args.no_rescore,
            source=args.source.replace("-", "_"),
        )
    )
    print(
        f"Wrote grader review: {result.row_count} row(s), "
        f"{result.answer_wrong_count} answer-wrong, "
        f"{result.format_only_count} format-only, "
        f"{result.warning_count} warning(s)"
    )
    print(f"CSV: {result.csv_output_path}")
    print(f"HTML: {result.html_output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
