#!/usr/bin/env python
"""Audit whether local ObviousBench artifacts are ready for an arXiv report."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from obviousbench.research.arxiv_readiness import (  # noqa: E402
    ArxivReadinessInputs,
    audit_arxiv_readiness,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="audit_arxiv_readiness.py")
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
    parser.add_argument("--human-baseline")
    parser.add_argument("--paper-manifest")
    parser.add_argument(
        "--manifest-scope",
        action="store_true",
        help="Audit item-card and dataset readiness only for manifest item IDs.",
    )
    parser.add_argument("--min-gold-examples-per-scorer", type=int, default=20)
    parser.add_argument("--min-human-participants", type=int, default=5)
    parser.add_argument(
        "--readiness-profile",
        choices=("strict", "preprint"),
        default="strict",
        help=(
            "strict requires human-baseline evidence; preprint treats it as "
            "optional and disables empirical human-triviality claims."
        ),
    )
    parser.add_argument("--out", help="Optional markdown output path.")
    args = parser.parse_args(argv)

    datasets = (
        [Path(path) for path in args.datasets]
        if args.datasets
        else sorted(Path("data/public_v0").glob("*.jsonl"))
    )
    report = audit_arxiv_readiness(
        ArxivReadinessInputs(
            dataset_paths=datasets,
            item_cards_dir=Path(args.item_cards_dir),
            scorer_gold_dir=Path(args.scorer_gold_dir),
            human_baseline_path=(
                Path(args.human_baseline) if args.human_baseline else None
            ),
            paper_manifest_path=Path(args.paper_manifest) if args.paper_manifest else None,
            min_gold_examples_per_scorer=args.min_gold_examples_per_scorer,
            min_human_participants=args.min_human_participants,
            manifest_scope=args.manifest_scope,
            readiness_profile=args.readiness_profile,
        )
    )
    markdown = report.to_markdown()
    print(markdown, end="")
    if args.out:
        output_path = Path(args.out)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(markdown, encoding="utf-8")
    return 0 if report.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
