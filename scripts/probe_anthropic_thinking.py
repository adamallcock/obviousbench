#!/usr/bin/env python
"""Audit Anthropic thinking request shape against completed usage summaries."""

from __future__ import annotations

import sys

from obviousbench.research.anthropic_thinking_probe import main

if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
