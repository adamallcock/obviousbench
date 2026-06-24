#!/usr/bin/env python
"""Generate draft item-card YAML stubs from benchmark JSONL rows."""

from __future__ import annotations

import argparse
from pathlib import Path

import yaml

from obviousbench.datasets.load import load_benchmark_jsonl
from obviousbench.datasets.schemas import BenchmarkItem


def build_card_stub(item: BenchmarkItem, *, generated_on: str) -> dict:
    """Build a draft item-card mapping for a benchmark item."""
    return {
        "item_id": item.id,
        "archetype_id": item.metadata.variant_of or f"{item.family}.{item.subfamily}",
        "source_refs": list(item.source_refs),
        "source_type": item.source_type,
        "source_summary": "TODO(review): summarize source evidence before trusted use.",
        "answer_derivation": (
            "TODO(review): explain why the expected answer follows unambiguously "
            f"from the prompt. Draft target: {item.target}"
        ),
        "expected_answer": item.target,
        "scorer_contract": {
            "scorer": item.scorer,
            "answer_type": item.answer_type,
            "strict_format": item.metadata.strict_format,
            "acceptable_outputs": [item.target],
            "unacceptable_outputs": [],
        },
        "ambiguity_notes": [
            "TODO(review): record ambiguity checks and acceptable interpretation boundaries."
        ],
        "split_policy": {
            "allowed_splits": [item.split],
            "leakage_risk": "low",
            "publishable": item.source_type == "generated_variant",
            "rationale": "TODO(review): confirm split eligibility and publication safety.",
        },
        "review": {
            "status": "draft",
            "reviewer": "unreviewed",
            "reviewed_on": generated_on,
            "notes": "Generated card stub requiring human review.",
        },
    }


def generate_item_card_stubs(dataset_paths: list[Path], out: Path, *, generated_on: str) -> Path:
    cards = []
    seen_ids: set[str] = set()
    for dataset_path in dataset_paths:
        for item in load_benchmark_jsonl(dataset_path):
            if item.id in seen_ids:
                raise ValueError(f"Duplicate dataset item ID while generating cards: {item.id}")
            seen_ids.add(item.id)
            cards.append(build_card_stub(item, generated_on=generated_on))

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        yaml.safe_dump({"cards": cards}, sort_keys=False, allow_unicode=False),
        encoding="utf-8",
    )
    return out


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("dataset_paths", nargs="*")
    parser.add_argument("--dataset", action="append", default=[])
    parser.add_argument("--out", required=True)
    parser.add_argument("--generated-on", default="2026-05-31")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    dataset_paths = [*args.dataset, *args.dataset_paths]
    if not dataset_paths:
        parser.error("at least one dataset path is required")
    output_path = generate_item_card_stubs(
        [Path(path) for path in dataset_paths],
        Path(args.out),
        generated_on=args.generated_on,
    )
    print(f"Wrote {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
