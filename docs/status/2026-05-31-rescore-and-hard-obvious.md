---
title: Rescore And Hard Obvious Pass
date: 2026-05-31
type: status
status: complete
---

# Rescore And Hard Obvious Pass

## Scope

Completed work items 1, 2, 3, and 5 from the next-step list. Object-presence
generation is intentionally excluded because it is being worked separately.

## Implemented

- Added first-class rescoring through `obviousbench rescore`.
- Added comparison aggregation through `obviousbench build-comparison`.
- Added answer-vs-format-vs-strict reporting to summaries, usage exports,
  comparison CSVs, leaderboards, and HTML reports.
- Made log discovery recursive so independent batch runs can be summarized from
  their parent directory.
- Fixed materialized-dataset profile reporting so hard-obvious runs use
  `hard_obvious_8x10_seed_20260531` instead of the task default profile.

## Rescored Mega Sweep

Primary artifacts:

- `results/summaries/mega-model-sweep-20260531-0820-rescored-v2-comparison/comparison.csv`
- `results/summaries/mega-model-sweep-20260531-0820-rescored-v2-comparison/delta.csv`
- `docs/reports/2026-05-31-mega-model-sweep-rescored-v2/report.html`
- `docs/reports/2026-05-31-mega-model-sweep-rescored-v2/leaderboard.md`

Notable rescoring deltas:

| Model | Original correct | Rescored answer correct | Strict correct | Main effect |
| --- | ---: | ---: | ---: | --- |
| Grok 4.20 xAI | 16/80 | 46/80 | 16/80 | Many answer-correct responses were format failures. |
| Grok 4.3 xAI | 50/80 | 70/80 | 50/80 | Suspiciously low score was largely grader strictness. |
| GPT-4o none | 59/80 | 71/80 | 59/80 | Correct answers embedded in noncompliant formats are now visible. |
| GPT-4.1 none | 64/80 | 66/80 | 64/80 | Small answer recovery, strict unchanged. |
| GPT-5 Nano minimal | 60/80 | 62/80 | 62/80 | Small answer recovery. |

Direct xAI runs still use manual cost repair in comparison outputs because the
local `runcost` card set does not price `grok/*` direct-provider aliases.

## Hard-Obvious Panel

Ran `hard_obvious_8x10` across an eight-model top/mid/weak panel.

Primary artifacts:

- `data/barrages/hard_obvious_8x10_seed_20260531.jsonl`
- `results/summaries/hard-obvious-panel-20260531/comparison.csv`
- `results/summaries/hard-obvious-panel-20260531/family_comparison.csv`
- `results/summaries/hard-obvious-panel-20260531/section_comparison.csv`
- `docs/reports/2026-05-31-hard-obvious-panel/report.html`
- `docs/reports/2026-05-31-hard-obvious-panel/leaderboard.md`

Headline hard-obvious results:

| Model | Answer | Format | Strict | Cost |
| --- | ---: | ---: | ---: | ---: |
| Gemini 3.5 Flash OR | 98.75% | 100.00% | 98.75% | $0.022346 |
| GPT-5.4 high | 97.50% | 100.00% | 97.50% | $0.058730 |
| GPT-5.5 medium | 97.50% | 100.00% | 97.50% | $0.086560 |
| Claude Opus 4.6 medium | 93.75% | 100.00% | 93.75% | $0.027220 |
| Gemini 3 Flash Preview OR | 88.75% | 100.00% | 88.75% | $0.000273 |
| Grok 4.3 xAI | 83.75% | 80.00% | 65.00% | $0.048708 |
| GPT-4o none | 81.25% | 82.50% | 63.75% | $0.008130 |
| GPT-5 Nano minimal | 72.50% | 100.00% | 72.50% | $0.000665 |

Early read:

- The hard profile is not saturated. The best answer score in this panel is
  79/80, not 80/80.
- Format separation matters. Grok 4.3 xAI is 67/80 answer-correct but only
  52/80 strict; GPT-4o is 65/80 answer-correct but only 51/80 strict.
- The car-wash/object-must-be-present pattern is still discriminating: GPT-4o
  missed four variants in the failure gallery, and GPT-5 Nano missed four.
- The hardest families in this panel were spelling transforms, character
  counts, constraint/object presence, and selected ordering/negation sections.

## Commands

```bash
.venv/bin/obviousbench rescore --logs <raw-log-dir> --out <summary-dir>
.venv/bin/obviousbench build-comparison --manifest <manifest.csv> --out <comparison-dir>
.venv/bin/obviousbench build-report --comparison-dir <comparison-dir> --out <report-dir>
```
