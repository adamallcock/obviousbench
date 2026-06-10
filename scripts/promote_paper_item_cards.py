#!/usr/bin/env python
"""Promote reviewed item cards for the paper candidate split."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from obviousbench.research.item_card_review import (  # noqa: E402
    DEFAULT_REVIEWED_ON,
    DEFAULT_REVIEWER,
    ItemCardPromotionInputs,
    promote_paper_item_cards,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="promote_paper_item_cards.py")
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
    parser.add_argument(
        "--source-catalog",
        default="data/source_catalog/sources_v0.jsonl",
    )
    parser.add_argument("--cards", default="data/item_cards/public_v0/cards.yaml")
    parser.add_argument("--reviewer", default=DEFAULT_REVIEWER)
    parser.add_argument("--reviewed-on", default=DEFAULT_REVIEWED_ON)
    args = parser.parse_args(argv)

    datasets = (
        [Path(path) for path in args.datasets]
        if args.datasets
        else sorted(Path("data/public_v0").glob("*.jsonl"))
    )
    result = promote_paper_item_cards(
        ItemCardPromotionInputs(
            manifest_path=Path(args.manifest),
            dataset_paths=datasets,
            source_catalog_path=Path(args.source_catalog),
            cards_path=Path(args.cards),
            reviewer=args.reviewer,
            reviewed_on=args.reviewed_on,
        )
    )
    print(f"Promoted {result.promoted_count} paper item card(s) in {result.cards_path}")
    if result.missing_dataset_ids:
        print(
            "Missing dataset item(s): " + ", ".join(result.missing_dataset_ids),
            file=sys.stderr,
        )
    if result.missing_card_ids:
        print(
            "Missing item card(s): " + ", ".join(result.missing_card_ids),
            file=sys.stderr,
        )
    return 1 if result.missing_dataset_ids or result.missing_card_ids else 0


if __name__ == "__main__":
    raise SystemExit(main())
