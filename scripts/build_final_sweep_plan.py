#!/usr/bin/env python
"""Build the dry-run final paper-sweep plan."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from obviousbench.research.final_sweep_plan import (  # noqa: E402
    FinalSweepPlanInputs,
    build_final_sweep_plan,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="build_final_sweep_plan.py")
    parser.add_argument("--panel", default="configs/paper_v1_model_panel.yaml")
    parser.add_argument(
        "--dataset",
        default="data/barrages/hard_obvious_8x10_seed_20260531.jsonl",
    )
    parser.add_argument("--paper-manifest", default="data/splits/paper_v1_manifest.jsonl")
    parser.add_argument("--item-cards-dir", default="data/item_cards")
    parser.add_argument("--scorer-gold-dir", default="tests/fixtures/scorer_gold")
    parser.add_argument("--human-baseline", default="data/human_baseline/paper_v1.csv")
    parser.add_argument(
        "--cost-estimates",
        default="docs/research/2026-06-01-paper-v1-model-panel-cost-estimates.md",
    )
    parser.add_argument(
        "--out",
        default="docs/research/2026-06-01-paper-v1-final-sweep-plan.md",
    )
    parser.add_argument(
        "--comparison-manifest",
        default="configs/paper_v1_final_sweep_manifest.csv",
    )
    parser.add_argument(
        "--smoke-status",
        default="docs/research/2026-06-01-paper-v1-smoke-status.md",
        help="Smoke-status document to gate provider execution; pass an empty value to skip.",
    )
    parser.add_argument("--raw-root", default="results/raw/paper-v1-final-high-cap")
    parser.add_argument(
        "--summary-root",
        default="results/summaries/paper-v1-final-high-cap",
    )
    parser.add_argument(
        "--comparison-dir",
        default="results/summaries/paper-v1-final-high-cap/comparison",
    )
    parser.add_argument(
        "--report-dir",
        default="docs/reports/2026-06-01-paper-v1-final-high-cap-sweep",
    )
    parser.add_argument("--generated-on", default="2026-06-01")
    parser.add_argument("--min-gold-examples-per-scorer", type=int, default=20)
    parser.add_argument("--min-human-participants", type=int, default=5)
    parser.add_argument(
        "--readiness-profile",
        choices=("strict", "preprint"),
        default="preprint",
        help=(
            "strict requires human-baseline evidence; preprint allows the dry-run "
            "handoff after non-human evidence gates pass."
        ),
    )
    args = parser.parse_args(argv)

    result = build_final_sweep_plan(
        FinalSweepPlanInputs(
            panel_path=Path(args.panel),
            dataset_path=Path(args.dataset),
            paper_manifest_path=Path(args.paper_manifest),
            item_cards_dir=Path(args.item_cards_dir),
            scorer_gold_dir=Path(args.scorer_gold_dir),
            human_baseline_path=Path(args.human_baseline),
            cost_estimates_path=Path(args.cost_estimates),
            output_path=Path(args.out),
            comparison_manifest_path=Path(args.comparison_manifest),
            smoke_status_path=Path(args.smoke_status) if args.smoke_status else None,
            raw_root=Path(args.raw_root),
            summary_root=Path(args.summary_root),
            comparison_dir=Path(args.comparison_dir),
            report_dir=Path(args.report_dir),
            generated_on=args.generated_on,
            min_gold_examples_per_scorer=args.min_gold_examples_per_scorer,
            min_human_participants=args.min_human_participants,
            readiness_profile=args.readiness_profile,
        )
    )
    print(
        f"Wrote final sweep plan to {result.output_path}: "
        f"{result.command_count} model command(s), "
        f"run_allowed={'yes' if result.run_allowed else 'no'}"
    )
    print(f"Wrote comparison manifest to {result.comparison_manifest_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
