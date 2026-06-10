#!/usr/bin/env python
"""Create a draft arXiv submission metadata note for ObviousBench."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from obviousbench.research.arxiv_metadata import (  # noqa: E402
    ArxivMetadataInputs,
    build_submission_metadata_template,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="build_arxiv_submission_metadata.py")
    parser.add_argument(
        "--out",
        default="docs/research/2026-06-01-obviousbench-arxiv-submission-metadata.md",
    )
    parser.add_argument(
        "--article-title",
        default=(
            "ObviousBench: Measuring Human-Trivial Failure Modes in "
            "Public-Facing Language Models"
        ),
    )
    parser.add_argument("--primary-category", default="cs.CL")
    parser.add_argument(
        "--secondary-category",
        action="append",
        dest="secondary_categories",
        default=None,
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite an existing metadata note.",
    )
    args = parser.parse_args(argv)

    output_path = Path(args.out)
    if output_path.exists() and not args.force:
        print(
            f"Metadata note already exists: {output_path}. "
            "Use --force to regenerate it.",
            file=sys.stderr,
        )
        return 2

    result = build_submission_metadata_template(
        ArxivMetadataInputs(
            output_path=output_path,
            article_title=args.article_title,
            primary_category=args.primary_category,
            secondary_categories=tuple(args.secondary_categories or ("cs.AI",)),
        )
    )
    print(f"Wrote arXiv submission metadata template to {result.output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
