#!/usr/bin/env python
"""Build the ObviousBench PDF build handoff."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from obviousbench.research.pdf_build_handoff import (  # noqa: E402
    PdfBuildHandoffInputs,
    build_pdf_build_handoff,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="build_pdf_build_handoff.py")
    parser.add_argument(
        "--pdf-audit",
        default="docs/research/2026-06-01-obviousbench-paper-pdf-build-audit.md",
    )
    parser.add_argument(
        "--source-audit",
        default="docs/research/2026-06-01-obviousbench-paper-source-audit.md",
    )
    parser.add_argument(
        "--out",
        default="docs/research/2026-06-01-obviousbench-pdf-build-handoff.md",
    )
    parser.add_argument(
        "--available-command",
        action="append",
        default=None,
        help=(
            "Override detected commands for tests. May be repeated. "
            "Omit to inspect PATH."
        ),
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit nonzero while the PDF handoff remains blocked.",
    )
    args = parser.parse_args(argv)

    result = build_pdf_build_handoff(
        PdfBuildHandoffInputs(
            output_path=Path(args.out),
            pdf_audit_path=Path(args.pdf_audit),
            source_audit_path=Path(args.source_audit),
            available_commands=(
                tuple(args.available_command)
                if args.available_command is not None
                else None
            ),
        )
    )
    print(
        f"Wrote PDF build handoff to {result.output_path}: "
        f"{result.status}, {len(result.blockers)} blocker(s)"
    )
    return 0 if result.ok or not args.strict else 1


if __name__ == "__main__":
    raise SystemExit(main())
