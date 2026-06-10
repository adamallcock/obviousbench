#!/usr/bin/env python
"""Generate cheap LaTeX table assets for the ObviousBench paper draft."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from obviousbench.research.paper_assets import (  # noqa: E402
    PaperAssetInputs,
    build_paper_assets,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="build_paper_assets.py")
    parser.add_argument("--manifest", default="data/splits/paper_v1_manifest.jsonl")
    parser.add_argument(
        "--dataset",
        action="append",
        dest="datasets",
        help=(
            "Dataset JSONL file used for readiness checks. Repeat for multiple files. "
            "Defaults to data/public_v0/*.jsonl."
        ),
    )
    parser.add_argument("--item-cards-dir", default="data/item_cards")
    parser.add_argument("--scorer-gold-dir", default="tests/fixtures/scorer_gold")
    parser.add_argument("--human-baseline")
    parser.add_argument("--model-panel", default="configs/paper_v1_model_panel.yaml")
    parser.add_argument("--final-results-dir")
    parser.add_argument("--placeholder-results-dir")
    parser.add_argument("--wrong-answer-review")
    parser.add_argument(
        "--figure-renderer",
        choices=("pdf", "chrome-svg"),
        default="pdf",
        help=(
            "Renderer for generated figure PDFs. The default pure-Python PDF "
            "renderer is dependency-light; chrome-svg uses local Chrome for "
            "visible SVG text in manuscript review figures."
        ),
    )
    parser.add_argument("--out", default="paper/tables")
    parser.add_argument("--figures-out", default="paper/figures")
    parser.add_argument("--min-gold-examples-per-scorer", type=int, default=20)
    parser.add_argument(
        "--readiness-profile",
        choices=("strict", "preprint"),
        default="preprint",
        help=(
            "strict requires human-baseline evidence; preprint treats it as "
            "deferred validation."
        ),
    )
    args = parser.parse_args(argv)

    datasets = (
        [Path(path) for path in args.datasets]
        if args.datasets
        else sorted(Path("data/public_v0").glob("*.jsonl"))
    )
    outputs = build_paper_assets(
        PaperAssetInputs(
            manifest_path=Path(args.manifest),
            dataset_paths=datasets,
            item_cards_dir=Path(args.item_cards_dir),
            scorer_gold_dir=Path(args.scorer_gold_dir),
            human_baseline_path=(
                Path(args.human_baseline) if args.human_baseline else None
            ),
            output_dir=Path(args.out),
            figures_dir=Path(args.figures_out),
            model_panel_path=Path(args.model_panel) if args.model_panel else None,
            final_results_dir=(
                Path(args.final_results_dir) if args.final_results_dir else None
            ),
            placeholder_results_dir=(
                Path(args.placeholder_results_dir)
                if args.placeholder_results_dir
                else None
            ),
            wrong_answer_review_path=(
                Path(args.wrong_answer_review) if args.wrong_answer_review else None
            ),
            figure_renderer=args.figure_renderer,
            min_gold_examples_per_scorer=args.min_gold_examples_per_scorer,
            readiness_profile=args.readiness_profile,
        )
    )
    output_paths = [
        outputs.dataset_composition,
        outputs.scorer_gold_coverage,
        outputs.readiness_gates,
        outputs.human_baseline_summary,
        outputs.main_results,
        outputs.family_results,
        outputs.thinking_group_results,
        outputs.model_family_results,
        outputs.failure_type_summary,
        outputs.provider_exclusions,
        *outputs.figures,
    ]
    if outputs.model_panel is not None:
        output_paths.append(outputs.model_panel)
    for output_path in output_paths:
        print(f"Wrote {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
