#!/usr/bin/env python
"""Audit expected final paper result artifacts."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from obviousbench.research.final_result_artifacts import (  # noqa: E402
    FinalResultArtifactInputs,
    audit_final_result_artifacts,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="audit_final_result_artifacts.py")
    parser.add_argument(
        "--manifest",
        default="configs/paper_v1_combined_234_overline_attempt_scored_20260602_manifest.csv",
    )
    parser.add_argument(
        "--comparison-dir",
        default=(
            "results/summaries/"
            "paper-v1-combined-234-overline-attempt-scored-20260602/comparison"
        ),
    )
    parser.add_argument(
        "--report-dir",
        default="docs/reports/2026-06-02-paper-v1-combined-234-overline",
    )
    parser.add_argument(
        "--out",
        default="docs/research/2026-06-01-paper-v1-final-result-artifact-audit.md",
    )
    parser.add_argument("--expected-models", type=int, default=234)
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Return nonzero when final result artifacts are incomplete.",
    )
    args = parser.parse_args(argv)

    result = audit_final_result_artifacts(
        FinalResultArtifactInputs(
            manifest_path=Path(args.manifest),
            comparison_dir=Path(args.comparison_dir),
            report_dir=Path(args.report_dir),
            output_path=Path(args.out),
            expected_models=args.expected_models,
        )
    )
    print(
        f"Wrote final result artifact audit to {result.output_path}: "
        f"{result.planned_model_count} planned model(s), "
        f"{result.present_comparison_file_count}/{len(result.comparison_checks)} "
        "comparison file(s) present"
    )
    return 0 if result.ok or not args.strict else 1


if __name__ == "__main__":
    raise SystemExit(main())
