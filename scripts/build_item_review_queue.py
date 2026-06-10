#!/usr/bin/env python
"""Generate a Markdown review queue for the paper candidate split."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from obviousbench.research.item_review_queue import (  # noqa: E402
    ItemReviewQueueInputs,
    build_item_review_queue,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="build_item_review_queue.py")
    parser.add_argument("--manifest", default="data/splits/paper_v1_manifest.jsonl")
    parser.add_argument(
        "--dataset",
        action="append",
        dest="datasets",
        help=(
            "Dataset JSONL file. Repeat for multiple files. "
            "Defaults to data/public_v0/*.jsonl."
        ),
    )
    parser.add_argument("--item-cards-dir", default="data/item_cards")
    parser.add_argument(
        "--out",
        default="docs/research/2026-06-01-paper-v1-item-review-queue.md",
    )
    args = parser.parse_args(argv)
    datasets = (
        [Path(path) for path in args.datasets]
        if args.datasets
        else sorted(Path("data/public_v0").glob("*.jsonl"))
    )
    result = build_item_review_queue(
        ItemReviewQueueInputs(
            manifest_path=Path(args.manifest),
            dataset_paths=datasets,
            item_cards_dir=Path(args.item_cards_dir),
            output_path=Path(args.out),
        )
    )
    print(
        f"Wrote {result.item_count} item review rows to "
        f"{result.output_path} ({result.blocked_count} blocked)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
