#!/usr/bin/env python
"""Audit ObviousBench paper TeX source references without compiling."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from obviousbench.research.paper_source_audit import (  # noqa: E402
    PaperSourceAuditInputs,
    audit_paper_source,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="audit_paper_source.py")
    parser.add_argument("--paper-dir", default="paper")
    parser.add_argument(
        "--out",
        default="docs/research/2026-06-01-obviousbench-paper-source-audit.md",
    )
    args = parser.parse_args(argv)

    result = audit_paper_source(
        PaperSourceAuditInputs(
            paper_dir=Path(args.paper_dir),
            output_path=Path(args.out),
        )
    )
    print(
        f"Wrote paper source audit to {result.output_path}: "
        f"{result.passed_count} passed, {result.failed_count} failed"
    )
    return 0 if result.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
