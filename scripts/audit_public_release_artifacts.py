#!/usr/bin/env python
"""Audit public release artifacts for the ObviousBench paper."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from obviousbench.research.public_release_audit import (  # noqa: E402
    PublicReleaseAuditInputs,
    audit_public_release_artifacts,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="audit_public_release_artifacts.py")
    parser.add_argument("--root", default=".")
    parser.add_argument(
        "--metadata",
        default="docs/research/2026-06-01-obviousbench-arxiv-submission-metadata.md",
    )
    parser.add_argument(
        "--out",
        default="docs/research/2026-06-01-obviousbench-public-release-artifact-audit.md",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Return nonzero when public release artifacts are incomplete.",
    )
    args = parser.parse_args(argv)

    result = audit_public_release_artifacts(
        PublicReleaseAuditInputs(
            root_dir=Path(args.root),
            output_path=Path(args.out),
            metadata_path=Path(args.metadata),
        )
    )
    print(
        f"Wrote public release artifact audit to {result.output_path}: "
        f"{result.passed_count} passed, {result.failed_count} failed"
    )
    return 0 if result.ok or not args.strict else 1


if __name__ == "__main__":
    raise SystemExit(main())
