#!/usr/bin/env python
"""Build the ObviousBench paper claim-evidence ledger."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from obviousbench.research.paper_claim_ledger import (  # noqa: E402
    PaperClaimLedgerInputs,
    build_paper_claim_ledger,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="build_paper_claim_ledger.py")
    parser.add_argument("--paper-dir", default="paper")
    parser.add_argument(
        "--out",
        default="docs/research/2026-06-01-obviousbench-paper-claim-evidence-ledger.md",
    )
    args = parser.parse_args(argv)

    result = build_paper_claim_ledger(
        PaperClaimLedgerInputs(
            paper_dir=Path(args.paper_dir),
            output_path=Path(args.out),
        )
    )
    print(
        f"Wrote paper claim ledger to {result.output_path}: "
        f"{result.blocked_count} blocked entrie(s)"
    )
    return 0 if result.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
