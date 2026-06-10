---
title: ObviousBench Paper Figures
date: 2026-06-01
type: note
status: draft
---

# ObviousBench Paper Figures

Generated current figures:

- `leaderboard.pdf`: answer-correctness leaderboard.
- `family_heatmap.pdf`: answer correctness by model and task family.
- `answer_format_gap.pdf`: strict-compliance gap relative to answer correctness.
- `cost_frontier.pdf`: answer correctness versus estimated cost.

Build them with `make -C paper assets` or the repeatable notebook at
`../../notebooks/2026-06-01-obviousbench-paper-figures.ipynb`.

Do not manually edit generated PDFs. Fix figure logic in
`../../obviousbench/research/paper_assets.py`, then regenerate.

Do not place raw provider logs or private/canary data in this directory.
