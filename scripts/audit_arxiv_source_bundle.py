#!/usr/bin/env python
"""Audit an arXiv source bundle for obvious packaging mistakes."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from obviousbench.research.arxiv_source_bundle import (  # noqa: E402
    ArxivBundleAuditInputs,
    audit_arxiv_source_bundle,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="audit_arxiv_source_bundle.py")
    parser.add_argument("--bundle", default="paper/arxiv-src.tar.gz")
    parser.add_argument(
        "--out",
        default="docs/research/2026-06-01-obviousbench-arxiv-source-bundle-audit.md",
    )
    args = parser.parse_args(argv)

    result = audit_arxiv_source_bundle(
        ArxivBundleAuditInputs(
            bundle_path=Path(args.bundle),
            output_path=Path(args.out),
        )
    )
    print(
        f"Audited {len(result.members)} arXiv bundle member(s): "
        f"{result.issue_count} issue(s)"
    )
    return 0 if result.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
