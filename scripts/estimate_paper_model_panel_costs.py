#!/usr/bin/env python
"""Estimate dry-run costs for the frozen paper model panel."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from obviousbench.research.model_panel_costs import (  # noqa: E402
    ModelPanelCostInputs,
    estimate_model_panel_costs,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="estimate_paper_model_panel_costs.py")
    parser.add_argument("--panel", default="configs/paper_v1_model_panel.yaml")
    parser.add_argument(
        "--csv-out",
        default="docs/research/2026-06-01-paper-v1-model-panel-cost-estimates.csv",
    )
    parser.add_argument(
        "--md-out",
        default="docs/research/2026-06-01-paper-v1-model-panel-cost-estimates.md",
    )
    parser.add_argument("--data-dir", default="data")
    parser.add_argument("--summary-root", default="results/summaries")
    parser.add_argument(
        "--cache",
        default=None,
        help="Inspect cache policy for cost estimates; default disables cache.",
    )
    parser.add_argument("--cache-dir", type=Path)
    args = parser.parse_args(argv)

    result = estimate_model_panel_costs(
        ModelPanelCostInputs(
            panel_path=Path(args.panel),
            csv_path=Path(args.csv_out),
            markdown_path=Path(args.md_out),
            data_dir=Path(args.data_dir),
            summary_root=Path(args.summary_root),
            cache=args.cache,
            cache_dir=args.cache_dir,
        )
    )
    print(
        f"Wrote {result.row_count} dry-run model-panel cost estimate(s) to "
        f"{result.csv_path} and {result.markdown_path}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
