---
title: ObviousBench arXiv Readiness Audit
date: 2026-06-01
type: review
status: current
---

# ObviousBench arXiv Readiness Audit

Generated from:

```bash
.venv/bin/python scripts/audit_arxiv_readiness.py \
  --human-baseline data/human_baseline/paper_v1.csv \
  --paper-manifest data/splits/paper_v1_manifest.jsonl \
  --manifest-scope
```

## Overall Status

FAIL.

This is now a narrow and useful failure: the data, item-card, scorer-gold, and
manifest gates pass for the 80-item paper candidate split. The remaining blocker
is empirical human-baseline collection.

## Gate Results

| Gate | Status | Finding |
| --- | --- | --- |
| Dataset validation | PASS | 9 dataset files pass strict manifest-scoped validation. |
| Item-card review | PASS | 80 paper-candidate item cards are reviewed and placeholder-free. |
| Scorer-gold coverage | PASS | 6 scorers used by the paper candidates meet the 20-example threshold. |
| Human baseline | FAIL | `data/human_baseline/paper_v1.csv` exists as a template but has no response rows. |
| Paper split manifest | PASS | `data/splits/paper_v1_manifest.jsonl` lists 80 item candidates. |

## Completed Foundation

The paper candidate split now has reviewed item cards for all 80 manifest items:

- source summaries are filled from `data/source_catalog/sources_v0.jsonl`,
- answer derivations are generated from structured item metadata,
- ambiguity notes and scorer contracts are explicit,
- split-policy rationales mark the public split as publishable but not
  contamination-resistant,
- review notes disclose deterministic AI-assisted review and keep the human
  baseline as a separate blocker.

The review queue at
`docs/research/2026-06-01-paper-v1-item-review-queue.md` now reports
`Blocked items: 0`.

The following human-baseline collection assets also exist:

- `docs/research/2026-06-01-paper-v1-human-baseline-form.md`
- `data/human_baseline/paper_v1.csv`

The CSV is intentionally header-only until real responses are collected.

The paper model panel and dry-run cost estimates also exist:

- `configs/paper_v1_model_panel.yaml`
- `docs/research/2026-06-01-paper-v1-model-panel-cost-estimates.md`

These are planning artifacts only. No final model sweep has been run.

The draft arXiv source bundle also exists and passes the local source-bundle
audit, but it is not submission-ready while claim blockers and human-baseline
blockers remain:

- `paper/arxiv-src.tar.gz`
- `docs/research/2026-06-01-obviousbench-arxiv-source-bundle-audit.md`
- `docs/research/2026-06-01-paper-claim-blocker-audit.md`

## Remaining Blocker

The readiness gate requires a real human baseline before paper claims can say
that the dataset is empirically human-trivial.

Current minimum audit requirements:

- required columns:
  `item_id,participant_id,answer,seconds,correct,notes`,
- parseable non-negative `seconds`,
- boolean `correct`,
- at least 5 distinct participants by default,
- at least one response covering every manifest item.

The current CSV has no response rows, so the paper should still avoid final
human-triviality, model-result, and leaderboard claims.

## Interpretation

Current state:

- Ready for: paper scaffold, data-review methods, scorer-contract discussion,
  item-card appendix generation, human-baseline collection, and planned model
  panel review.
- Not ready for: arXiv submission, public leaderboard-grade claims, final model
  ranking, or strong "human-trivial" claims.

Next foundation slice:

1. Collect human-baseline rows from at least 5 participants across all 80
   `paper_v1` items.
2. Rerun the readiness audit and verify the human-baseline gate passes.
3. Regenerate the human-baseline summary table for the paper.
4. Re-verify model aliases and cost estimates immediately before running.
5. Only then run final model arrays for the report.
