#!/usr/bin/env python
"""Audit unresolved claim blockers in the paper source."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from obviousbench.research.paper_claims import (  # noqa: E402
    PaperClaimAuditInputs,
    audit_paper_claims,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="audit_paper_claims.py")
    parser.add_argument("--paper-dir", default="paper")
    parser.add_argument(
        "--out",
        default="docs/research/2026-06-01-paper-claim-blocker-audit.md",
    )
    args = parser.parse_args(argv)

    result = audit_paper_claims(
        PaperClaimAuditInputs(
            paper_dir=Path(args.paper_dir),
            output_path=Path(args.out),
        )
    )
    print(
        f"Found {len(result.markers)} unresolved paper marker(s): "
        f"{result.claimblocked_count} claimblocked, {result.obtodo_count} obtodo"
    )
    return 0 if result.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
