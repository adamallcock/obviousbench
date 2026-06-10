#!/usr/bin/env python
"""Audit a config-driven ObviousBench release snapshot."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from obviousbench.research.release_snapshot import (  # noqa: E402
    ReleaseSnapshotInputs,
    audit_release_snapshot,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="audit_release_snapshot.py")
    parser.add_argument("--config", default="configs/release_v0_1_0.yaml")
    parser.add_argument(
        "--out",
        default="docs/release/generated/release-snapshot-audit.md",
    )
    parser.add_argument(
        "--include-public",
        action="store_true",
        help="Also require live/confirmed public URLs and identifiers.",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Return nonzero when the local release snapshot audit fails.",
    )
    args = parser.parse_args(argv)

    result = audit_release_snapshot(
        ReleaseSnapshotInputs(
            config_path=Path(args.config),
            output_path=Path(args.out),
            include_public=args.include_public,
        )
    )
    status = "PASS" if result.ok else "BLOCKED"
    print(
        f"Wrote release snapshot audit to {result.output_path}: "
        f"{status}, {result.failed_count} failure(s), {result.warning_count} warning(s)"
    )
    return 0 if result.ok or not args.strict else 1


if __name__ == "__main__":
    raise SystemExit(main())
