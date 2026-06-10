#!/usr/bin/env python
"""Build the ObviousBench arXiv submission preflight checklist."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from obviousbench.research.arxiv_preflight import (  # noqa: E402
    DEFAULT_LATEX_TOOLCHAIN_COMMANDS,
    ArxivPreflightInputs,
    build_arxiv_preflight,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="build_arxiv_submission_checklist.py")
    parser.add_argument(
        "--dataset",
        action="append",
        dest="datasets",
        help=(
            "Dataset JSONL file to audit. Repeat for multiple files. "
            "Defaults to data/public_v0/*.jsonl."
        ),
    )
    parser.add_argument("--item-cards-dir", default="data/item_cards")
    parser.add_argument("--scorer-gold-dir", default="tests/fixtures/scorer_gold")
    parser.add_argument("--human-baseline", default="data/human_baseline/paper_v1.csv")
    parser.add_argument("--paper-manifest", default="data/splits/paper_v1_manifest.jsonl")
    parser.add_argument("--paper-dir", default="paper")
    parser.add_argument("--bundle", default="paper/arxiv-src.tar.gz")
    parser.add_argument(
        "--model-panel",
        default="configs/paper_v1_combined_234_overline_attempt_scored_20260602_manifest.csv",
    )
    parser.add_argument(
        "--model-costs",
        default="docs/research/2026-06-01-paper-v1-model-panel-cost-estimates.md",
    )
    parser.add_argument(
        "--metadata-confirmation",
        default="docs/research/2026-06-01-obviousbench-arxiv-submission-metadata.md",
    )
    parser.add_argument(
        "--out",
        default="docs/research/2026-06-01-obviousbench-arxiv-submission-checklist.md",
    )
    parser.add_argument(
        "--claim-audit-out",
        default="docs/research/2026-06-01-paper-claim-blocker-audit.md",
    )
    parser.add_argument(
        "--bundle-audit-out",
        default="docs/research/2026-06-01-obviousbench-arxiv-source-bundle-audit.md",
    )
    parser.add_argument("--min-gold-examples-per-scorer", type=int, default=20)
    parser.add_argument("--min-human-participants", type=int, default=5)
    parser.add_argument(
        "--readiness-profile",
        choices=("strict", "preprint"),
        default="preprint",
        help=(
            "strict requires human-baseline evidence; preprint treats it as "
            "deferred validation and requires measured-human claims to be omitted."
        ),
    )
    parser.add_argument(
        "--latex-toolchain-command",
        action="append",
        dest="latex_toolchain_commands",
        help=(
            "Command name to probe for local PDF builds. Repeat to override "
            "the default latexmk/pdflatex/tectonic probe list."
        ),
    )
    parser.add_argument(
        "--no-manifest-scope",
        action="store_true",
        help="Audit all loaded dataset items instead of the paper manifest subset.",
    )
    args = parser.parse_args(argv)

    datasets = (
        [Path(path) for path in args.datasets]
        if args.datasets
        else sorted(Path("data/public_v0").glob("*.jsonl"))
    )
    result = build_arxiv_preflight(
        ArxivPreflightInputs(
            dataset_paths=datasets,
            item_cards_dir=Path(args.item_cards_dir),
            scorer_gold_dir=Path(args.scorer_gold_dir),
            human_baseline_path=Path(args.human_baseline),
            paper_manifest_path=Path(args.paper_manifest),
            paper_dir=Path(args.paper_dir),
            bundle_path=Path(args.bundle),
            output_path=Path(args.out),
            claim_audit_output_path=Path(args.claim_audit_out),
            bundle_audit_output_path=Path(args.bundle_audit_out),
            model_panel_path=Path(args.model_panel),
            model_costs_path=Path(args.model_costs),
            metadata_confirmation_path=Path(args.metadata_confirmation),
            latex_toolchain_commands=tuple(
                args.latex_toolchain_commands or DEFAULT_LATEX_TOOLCHAIN_COMMANDS
            ),
            min_gold_examples_per_scorer=args.min_gold_examples_per_scorer,
            min_human_participants=args.min_human_participants,
            manifest_scope=not args.no_manifest_scope,
            readiness_profile=args.readiness_profile,
        )
    )
    print(
        f"Wrote arXiv submission checklist to {result.output_path}: "
        f"{result.passed_count} passed, {result.failed_count} failed"
    )
    return 0 if result.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
