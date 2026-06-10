#!/usr/bin/env python
"""Build the ObviousBench arXiv submission handoff."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from obviousbench.research.arxiv_submission_handoff import (  # noqa: E402
    ArxivSubmissionHandoffInputs,
    build_arxiv_submission_handoff,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="build_arxiv_submission_handoff.py")
    parser.add_argument(
        "--out",
        default="docs/research/2026-06-01-obviousbench-arxiv-submission-handoff.md",
    )
    parser.add_argument("--source-bundle", default="paper/arxiv-src.tar.gz")
    parser.add_argument(
        "--source-bundle-audit",
        default="docs/research/2026-06-01-obviousbench-arxiv-source-bundle-audit.md",
    )
    parser.add_argument(
        "--pdf-audit",
        default="docs/research/2026-06-01-obviousbench-paper-pdf-build-audit.md",
    )
    parser.add_argument(
        "--preflight",
        default="docs/research/2026-06-01-obviousbench-arxiv-submission-checklist.md",
    )
    parser.add_argument(
        "--release-audit",
        default="docs/research/2026-06-01-obviousbench-public-release-artifact-audit.md",
    )
    parser.add_argument(
        "--metadata",
        default="docs/research/2026-06-01-obviousbench-arxiv-submission-metadata.md",
    )
    parser.add_argument(
        "--blocker-dashboard",
        default="docs/research/2026-06-01-obviousbench-arxiv-blocker-dashboard.md",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Return nonzero when the upload handoff is not ready.",
    )
    args = parser.parse_args(argv)

    result = build_arxiv_submission_handoff(
        ArxivSubmissionHandoffInputs(
            output_path=Path(args.out),
            source_bundle_path=Path(args.source_bundle),
            source_bundle_audit_path=Path(args.source_bundle_audit),
            pdf_audit_path=Path(args.pdf_audit),
            preflight_path=Path(args.preflight),
            release_audit_path=Path(args.release_audit),
            metadata_path=Path(args.metadata),
            blocker_dashboard_path=Path(args.blocker_dashboard),
        )
    )
    print(
        f"Wrote arXiv submission handoff to {result.output_path}: "
        f"{result.passed_count} passed, {result.failed_count} failed"
    )
    return 0 if result.ok or not args.strict else 1


if __name__ == "__main__":
    raise SystemExit(main())
