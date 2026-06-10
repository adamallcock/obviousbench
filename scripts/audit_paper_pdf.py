#!/usr/bin/env python
"""Audit the ObviousBench paper PDF build state."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from obviousbench.research.paper_pdf_audit import (  # noqa: E402
    PaperPdfAuditInputs,
    audit_paper_pdf_build,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="audit_paper_pdf.py")
    parser.add_argument("--paper-dir", default="paper")
    parser.add_argument(
        "--out",
        default="docs/research/2026-06-01-obviousbench-paper-pdf-build-audit.md",
    )
    parser.add_argument(
        "--source-audit-out",
        default="docs/research/2026-06-01-obviousbench-paper-source-audit.md",
    )
    parser.add_argument("--pdf", default=None)
    parser.add_argument("--log", default=None)
    parser.add_argument(
        "--available-tool",
        action="append",
        default=None,
        help="Testing override for an available LaTeX command.",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Return nonzero when the PDF build audit is blocked.",
    )
    args = parser.parse_args(argv)

    result = audit_paper_pdf_build(
        PaperPdfAuditInputs(
            paper_dir=Path(args.paper_dir),
            output_path=Path(args.out),
            source_audit_output_path=Path(args.source_audit_out),
            pdf_path=Path(args.pdf) if args.pdf else None,
            log_path=Path(args.log) if args.log else None,
            available_latex_tools=tuple(args.available_tool)
            if args.available_tool is not None
            else None,
        )
    )
    print(
        f"Wrote paper PDF build audit to {result.output_path}: "
        f"{result.passed_count} passed, {result.failed_count} failed"
    )
    return 0 if result.ok or not args.strict else 1


if __name__ == "__main__":
    raise SystemExit(main())
