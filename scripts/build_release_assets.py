#!/usr/bin/env python
"""Build local ObviousBench release-prep assets from one release config."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from obviousbench.research.release_snapshot import build_local_release_assets  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="build_release_assets.py")
    parser.add_argument("--config", default="configs/release_v0_1_0.yaml")
    args = parser.parse_args(argv)

    outputs = build_local_release_assets(Path(args.config))
    for output in outputs:
        print(f"Wrote {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
