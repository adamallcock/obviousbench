#!/usr/bin/env python
"""Build human-baseline collection assets for the paper candidate split."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from obviousbench.research.human_baseline_form import (  # noqa: E402
    HumanBaselineFormInputs,
    build_human_baseline_form,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="build_human_baseline_form.py")
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
        "--form-out",
        default="docs/research/2026-06-01-paper-v1-human-baseline-form.md",
    )
    parser.add_argument("--csv-out", default="data/human_baseline/paper_v1.csv")
    args = parser.parse_args(argv)

    datasets = (
        [Path(path) for path in args.datasets]
        if args.datasets
        else sorted(Path("data/public_v0").glob("*.jsonl"))
    )
    result = build_human_baseline_form(
        HumanBaselineFormInputs(
            manifest_path=Path(args.manifest),
            dataset_paths=datasets,
            form_path=Path(args.form_out),
            csv_path=Path(args.csv_out),
        )
    )
    print(
        f"Wrote {result.item_count} human-baseline form item(s) to "
        f"{result.form_path} and CSV template to {result.csv_path}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
