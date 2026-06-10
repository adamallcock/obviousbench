#!/usr/bin/env python
"""Audit the ObviousBench manuscript for component completeness."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from obviousbench.research.manuscript_completeness import (  # noqa: E402
    ManuscriptCompletenessInputs,
    audit_manuscript_completeness,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="audit_manuscript_completeness.py")
    parser.add_argument("--paper-dir", default="paper")
    parser.add_argument(
        "--out",
        default="docs/research/2026-06-01-obviousbench-manuscript-completeness-audit.md",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Return nonzero while manuscript components remain blocked or missing.",
    )
    args = parser.parse_args(argv)

    result = audit_manuscript_completeness(
        ManuscriptCompletenessInputs(
            paper_dir=Path(args.paper_dir),
            output_path=Path(args.out),
        )
    )
    print(
        f"Wrote manuscript completeness audit to {result.output_path}: "
        f"{result.passed_count} passed, {result.blocked_count} blocked, "
        f"{result.missing_count} missing"
    )
    return 0 if result.ok or not args.strict else 1


if __name__ == "__main__":
    raise SystemExit(main())
