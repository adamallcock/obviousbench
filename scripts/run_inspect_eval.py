#!/usr/bin/env python
# ruff: noqa: E402, I001
"""Run Inspect evals with ObviousBench developer defaults."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from obviousbench.runners.inspect_eval import main


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
