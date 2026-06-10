---
title: ObviousBench Paper Figure Workflow
date: 2026-06-01
type: runbook
status: draft
---

# ObviousBench Paper Figure Workflow

This is the repeatable path for paper figures. The rule is simple: generated
charts are rebuilt from versioned CSV artifacts, not manually recreated.

## Source Of Truth

- Figure code: `obviousbench/research/paper_assets.py`
- CLI entrypoint: `scripts/build_paper_assets.py`
- Notebook control surface:
  `notebooks/2026-06-01-obviousbench-paper-figures.ipynb`
- Current draft result source:
  `docs/shareable/2026-05-31-obviousbench-proof-point`
- Future final result source: `results/paper_v1_final`
- Manuscript figure outputs: `paper/figures/*.pdf`

The notebook automatically uses `results/paper_v1_final` when that directory
exists. Until then it uses the proof-point bundle and the generated tables and
figures keep the placeholder status visible.

## Command Ladder

Regenerate all paper tables and figures from the Makefile:

```bash
make -C paper assets
```

Regenerate directly from the asset builder:

```bash
.venv/bin/python scripts/build_paper_assets.py \
  --manifest data/splits/paper_v1_manifest.jsonl \
  --human-baseline data/human_baseline/paper_v1.csv \
  --placeholder-results-dir docs/shareable/2026-05-31-obviousbench-proof-point \
  --figure-renderer chrome-svg \
  --out paper/tables \
  --figures-out paper/figures
```

After final results exist, replace the placeholder argument:

```bash
.venv/bin/python scripts/build_paper_assets.py \
  --manifest data/splits/paper_v1_manifest.jsonl \
  --human-baseline data/human_baseline/paper_v1.csv \
  --final-results-dir results/paper_v1_final \
  --figure-renderer chrome-svg \
  --out paper/tables \
  --figures-out paper/figures
```

## Visual Quality Rules

- Use restrained, consistent colors across all result figures.
- Put source and placeholder/final status in every figure subtitle.
- Keep chart annotations sparse enough to read in a two-column paper.
- Prefer compact family labels over raw snake-case when axis space is tight.
- Fix figure logic in code, then rerun the notebook or Makefile target.
- Do not edit the generated PDFs directly.

## Current Figure Set

- `leaderboard.pdf`: answer-correctness leaderboard with Wilson confidence
  intervals.
- `family_heatmap.pdf`: answer correctness by model and task family.
- `answer_format_gap.pdf`: answer-only and format-only gaps versus strict
  accuracy.
- `cost_frontier.pdf`: answer correctness versus estimated cost on a log cost
  axis.

Optional notebook previews are written under `tmp/paper-figure-previews` when
`pdftoppm` is available. Those previews are for local review only and are not
paper artifacts.
