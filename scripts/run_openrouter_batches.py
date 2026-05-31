#!/usr/bin/env python
"""Run Inspect tasks against OpenRouter in 429-aware batches."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from obviousbench.runners.openrouter_batches import main

if __name__ == "__main__":
    raise SystemExit(main())
