#!/usr/bin/env python
"""Build the ObviousBench arXiv internal research-review report."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from obviousbench.research.internal_review import (  # noqa: E402
    InternalReviewInputs,
    audit_internal_research_review,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="audit_internal_research_review.py")
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
        "--out",
        default="docs/research/2026-06-01-obviousbench-arxiv-internal-review.md",
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
    result = audit_internal_research_review(
        InternalReviewInputs(
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
            min_gold_examples_per_scorer=args.min_gold_examples_per_scorer,
            min_human_participants=args.min_human_participants,
            manifest_scope=not args.no_manifest_scope,
            readiness_profile=args.readiness_profile,
        )
    )
    print(
        f"Wrote internal research review to {result.output_path}: "
        f"{result.passed_count} passed, {result.failed_count} failed"
    )
    return 0 if result.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
