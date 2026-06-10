#!/usr/bin/env python
"""Build the ObviousBench related-work positioning matrix."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from obviousbench.research.related_work_matrix import (  # noqa: E402
    RelatedWorkMatrixInputs,
    build_related_work_matrix,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="build_related_work_matrix.py")
    parser.add_argument("--config", default="configs/paper_v1_related_work.yaml")
    parser.add_argument("--paper-dir", default="paper")
    parser.add_argument("--bib", default="paper/references.bib")
    parser.add_argument(
        "--markdown-out",
        default="docs/research/2026-06-01-obviousbench-related-work-positioning.md",
    )
    parser.add_argument(
        "--tex-out",
        default="paper/tables/related_work_positioning.tex",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit nonzero when required related-work coverage is missing.",
    )
    args = parser.parse_args(argv)

    result = build_related_work_matrix(
        RelatedWorkMatrixInputs(
            config_path=Path(args.config),
            paper_dir=Path(args.paper_dir),
            bib_path=Path(args.bib),
            markdown_path=Path(args.markdown_out),
            tex_path=Path(args.tex_out),
        )
    )
    print(
        f"Wrote related-work matrix to {result.markdown_path} "
        f"and {result.tex_path}: "
        f"{result.passed_count} passed, {result.blocked_count} blocked"
    )
    return 0 if result.ok or not args.strict else 1


if __name__ == "__main__":
    raise SystemExit(main())
