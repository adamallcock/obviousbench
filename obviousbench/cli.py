"""Command-line interface for local ObviousBench workflows."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from obviousbench.analysis.summarize_results import summarize_results
from obviousbench.barrage import (
    BarrageProfile,
    build_barrage,
    load_split_items,
    write_barrage_jsonl,
)
from obviousbench.datasets.validation import validate_dataset_paths


def _validate(args: argparse.Namespace) -> int:
    report = validate_dataset_paths([Path(path) for path in args.paths])
    if report.ok:
        print("Validation passed.")
        return 0
    for issue in report.issues:
        print(issue.format(), file=sys.stderr)
    return 1


def _summarize(args: argparse.Namespace) -> int:
    try:
        output_paths = summarize_results(
            Path(args.logs),
            Path(args.out),
            cost_mode=args.cost,
        )
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        return 1
    for output_path in output_paths:
        print(f"Wrote {output_path}")
    return 0


def _make_barrage(args: argparse.Namespace) -> int:
    try:
        profile = BarrageProfile.parse(args.profile)
        items = build_barrage(
            load_split_items(args.split, data_dir=Path(args.data_dir)),
            profile,
            seed=args.seed,
        )
        output = write_barrage_jsonl(items, Path(args.out))
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(f"Wrote {len(items)} barrage samples to {output}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="obviousbench")
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate = subparsers.add_parser("validate", help="Validate benchmark JSONL files")
    validate.add_argument("paths", nargs="+")
    validate.set_defaults(func=_validate)

    summarize = subparsers.add_parser("summarize", help="Summarize Inspect logs")
    summarize.add_argument("--logs", required=True)
    summarize.add_argument("--out", required=True)
    summarize.add_argument("--cost", choices=["none", "runcost"], default="runcost")
    summarize.set_defaults(func=_summarize)

    make_barrage = subparsers.add_parser(
        "make-barrage",
        help="Materialize a deterministic balanced barrage JSONL file",
    )
    make_barrage.add_argument("--profile", default="balanced_8x10")
    make_barrage.add_argument("--split", default="public_v0")
    make_barrage.add_argument("--seed", default=20260531, type=int)
    make_barrage.add_argument("--data-dir", default="data")
    make_barrage.add_argument("--out", required=True)
    make_barrage.set_defaults(func=_make_barrage)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
