---
title: ObviousBench Draft Result Placeholders
date: 2026-06-01
type: decision-record
status: draft
---

# ObviousBench Draft Result Placeholders

## Decision

Use the existing 2026-05-31 proof-point result bundle as a draft-only
placeholder input for the manuscript while the full `paper_v1` model sweep is
deferred.

This lets the paper be reviewed as a complete technical report with populated
tables and figures before spending money on the final provider run.

## Placeholder Source

Draft-only source directory:

```text
docs/shareable/2026-05-31-obviousbench-proof-point
```

Inputs used by the paper asset builder:

- `model-comparison.csv`
- `family-comparison.csv`

The Makefile target gives final results priority when a final result directory
is supplied. The proof-point source is only the default draft input for
`make -C paper assets`. The Makefile renders draft figures through local
Chrome's headless SVG-to-PDF path so that labels, axes, and legends are visible
in the review PDF; the pure-Python fallback remains available for tests and
minimal environments.

The repeatable review surface is
`notebooks/2026-06-01-obviousbench-paper-figures.ipynb`, with the durable
workflow recorded in
`docs/research/2026-06-01-obviousbench-paper-figure-workflow.md`.

## Generated Draft Assets

Tables:

- `paper/tables/main_results.tex`
- `paper/tables/family_results.tex`
- `paper/tables/provider_exclusions.tex`

Figures:

- `paper/figures/leaderboard.pdf`
- `paper/figures/family_heatmap.pdf`
- `paper/figures/answer_format_gap.pdf`
- `paper/figures/cost_frontier.pdf`

## Claim Boundary

These placeholder values are not final arXiv claims.

Allowed uses:

- Check manuscript flow.
- Check table widths, captions, and terminology.
- Check whether the selected figures make the results section readable.
- Critique the analysis narrative before running the final benchmark.

Disallowed uses:

- Headline claims about final model performance.
- Claims about the frozen `paper_v1` model panel.
- Claims about human performance or model-versus-human gaps.
- Public release as final benchmark results.

## Replacement Rule

Before final submission, every draft proof-point table and figure must be
rebuilt from the frozen final comparison directory produced by the approved
`paper_v1` sweep. The paper source keeps claim blockers in the results section
until that replacement happens.
