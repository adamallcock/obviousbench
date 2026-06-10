#!/usr/bin/env python
"""Build the ObviousBench public-release decision packet."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from obviousbench.research.public_release_decision_packet import (  # noqa: E402
    PublicReleaseDecisionPacketInputs,
    build_public_release_decision_packet,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="build_public_release_decision_packet.py")
    parser.add_argument("--root", default=".")
    parser.add_argument(
        "--metadata",
        default="docs/research/2026-06-01-obviousbench-arxiv-submission-metadata.md",
    )
    parser.add_argument(
        "--release-audit",
        default="docs/research/2026-06-01-obviousbench-public-release-artifact-audit.md",
    )
    parser.add_argument(
        "--out",
        default="docs/research/2026-06-01-obviousbench-public-release-decision-packet.md",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Return nonzero while release decisions still need confirmation.",
    )
    args = parser.parse_args(argv)

    result = build_public_release_decision_packet(
        PublicReleaseDecisionPacketInputs(
            root_dir=Path(args.root),
            output_path=Path(args.out),
            metadata_path=Path(args.metadata),
            release_audit_path=Path(args.release_audit),
        )
    )
    print(
        f"Wrote public release decision packet to {result.output_path}: "
        f"{result.ready_count} ready, "
        f"{result.needs_confirmation_count} need confirmation"
    )
    return 0 if result.ok or not args.strict else 1


if __name__ == "__main__":
    raise SystemExit(main())
