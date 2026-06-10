---
title: Paper V1 8x28 Pilot Run Summary
date: 2026-06-02
type: report
status: complete
---

# Paper V1 8x28 Pilot Run Summary

## Scope

Ran a six-model OpenRouter-only pilot on `hard_obvious_8x28`, a 224-sample
balanced hard-obvious slice with 28 items from each of the 8 task families.

Primary artifacts:

- Dataset: `data/barrages/hard_obvious_8x28_seed_20260531.jsonl`
- Panel: `configs/paper_v1_8x28_pilot_20260602_panel.yaml`
- Manifest: `configs/paper_v1_8x28_pilot_20260602_manifest.csv`
- Raw logs: `results/raw/paper-v1-8x28-pilot-20260602/`
- Summaries: `results/summaries/paper-v1-8x28-pilot-20260602/`
- Report: `docs/reports/2026-06-02-paper-v1-8x28-pilot/report.html`
- Cost estimate: `docs/research/2026-06-02-paper-v1-8x28-pilot-cost-estimates.md`

## Result Delta

| Model | 80-sample answer | 80-sample CI | 224-sample answer | 224-sample CI | Delta | Correct change | Provider errors |
| --- | ---: | --- | ---: | --- | ---: | --- | ---: |
| NVIDIA: Nemotron 3 Super | 100.0% | 95.4-100.0% | 96.9% | 93.7-98.5% | -3.1 pp | 80/80 -> 217/224 | 1 |
| MiniMax: MiniMax M3 | 98.8% | 93.3-99.8% | 97.8% | 94.9-99.0% | -1.0 pp | 79/80 -> 219/224 | 0 |
| OpenAI GPT-OSS 20B | 97.5% | 91.3-99.3% | 93.3% | 89.2-95.9% | -4.2 pp | 78/80 -> 209/224 | 2 |
| DeepSeek: DeepSeek V4 Flash | 96.2% | 89.5-98.7% | 92.4% | 88.2-95.2% | -3.8 pp | 77/80 -> 207/224 | 0 |
| Google: Gemma 3 27B | 81.2% | 71.3-88.3% | 81.2% | 75.6-85.8% | +0.0 pp | 65/80 -> 182/224 | 0 |
| Qwen: Qwen3 Coder Flash | 68.8% | 57.9-77.8% | 67.0% | 60.6-72.8% | -1.8 pp | 55/80 -> 150/224 | 0 |

## Observations

- The 8x28 run did not merely narrow confidence intervals; it changed observed
  accuracies for several high-performing models.
- MiniMax M3 moved ahead of Nemotron 3 Super in this pilot because MiniMax held
  219/224 while Nemotron dropped to 217/224 with one provider error.
- The larger slice exposed top-model failures mainly in `spelling_transform`,
  `constraint_awareness`, and, for weaker models, `character_count` and
  `word_count`.
- All six model entries passed summary validation. Total scored attempts were
  1,344/1,344.
- Summarized run cost was `$0.05972016`. MiniMax pricing depended on the
  comparison/report registry fallback because the dry-run `runcost` estimate had
  no direct price card for `minimax/minimax-m3`.

## Interpretation

The current 80-sample leaderboard appears directionally useful but optimistic
for the near-perfect band. A larger balanced hard-obvious slice reduces the CI
width and also uncovers additional failures, especially in transformation and
constraint-heavy families. For paper results, the next stronger step is to run a
larger 8x28 panel across the main top cohort rather than repeating the exact
80-item barrage.
