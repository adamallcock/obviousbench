#!/usr/bin/env python
"""Run an ObviousBench model-panel manifest."""

from __future__ import annotations

import sys

from obviousbench.model_panels.runner import main

if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
