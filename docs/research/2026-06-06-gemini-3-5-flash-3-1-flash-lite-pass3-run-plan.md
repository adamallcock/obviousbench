---
title: Gemini 3.5 Flash And 3.1 Flash Lite Pass^3 Run Plan
date: 2026-06-06
type: plan
status: complete
---

# Gemini 3.5 Flash And 3.1 Flash Lite Pass^3 Run Plan

## Objective

Run the same pass^3 reliability slice on Gemini 3.5 Flash and Gemini 3.1
Flash Lite thinking variants, then add them to the existing answer-correct
pass^3 versus log-cost curve.

## Design

- Dataset: `data/barrages/hard_obvious_8x28_seed_20260531.jsonl`
- Trials: 3 cache-disabled trials per setting
- Total entries: 24
- Total attempts: 5,376
- Models: `google/gemini-3.5-flash`, `google/gemini-3.1-flash-lite`
- Thinking settings: `minimal`, `low`, `medium`, `high`
- Primary plotted metric: `answer_correct` pass^3
- Secondary table metric: `strict_correct` pass^3
- Thinking control: Inspect `reasoning_effort`, which maps to Gemini
  `thinkingLevel` for Gemini 3 models.

## Execution

- Panel: `configs/gemini_3_5_flash_3_1_flash_lite_pass3_8x28_20260606_panel.yaml`
- Raw root: `results/raw/gemini-3-5-flash-3-1-flash-lite-pass3-8x28-20260606`
- Summary root: `results/summaries/gemini-3-5-flash-3-1-flash-lite-pass3-8x28-20260606/runs`
- Manifest: `configs/gemini_3_5_flash_3_1_flash_lite_pass3_8x28_20260606_manifest.csv`
- Status: `results/summaries/gemini-3-5-flash-3-1-flash-lite-pass3-8x28-20260606/status.jsonl`

Full run command:

```bash
GOOGLE_API_KEY="$(security find-generic-password -s GOOGLE_AI_STUDIO_API_KEY -w)" \
.venv/bin/python scripts/run_model_panel.py \
  --panel configs/gemini_3_5_flash_3_1_flash_lite_pass3_8x28_20260606_panel.yaml \
  --dataset data/barrages/hard_obvious_8x28_seed_20260531.jsonl \
  --raw-root results/raw/gemini-3-5-flash-3-1-flash-lite-pass3-8x28-20260606 \
  --summary-root results/summaries/gemini-3-5-flash-3-1-flash-lite-pass3-8x28-20260606/runs \
  --manifest-out configs/gemini_3_5_flash_3_1_flash_lite_pass3_8x28_20260606_manifest.csv \
  --status-out results/summaries/gemini-3-5-flash-3-1-flash-lite-pass3-8x28-20260606/status.jsonl \
  --mode full \
  --no-cache \
  --no-skip-completed \
  --cost runcost
```

## Acceptance Criteria

- 24 status rows exist and all have `status=passed` and `returncode=0`.
- Every trial summary has 224 rows in `usage_by_sample.csv`.
- Status inspect commands contain no `--cache` flag.
- Gemini result CSV and Markdown note are written under `docs/research/`.
- Gemini rows are added to the combined log-cost pass^3 chart under
  `docs/reports/2026-06-06-pass3-effort-cost-curves/`.

## Outcome

Completed on 2026-06-06. The run produced 24 passed status rows, 224 scored
samples per entry, and zero provider-error samples. Results were written to
`docs/research/2026-06-06-gemini-3-5-flash-3-1-flash-lite-8x28-pass3-results.md`,
and the combined pass^3 curve was rebuilt at
`docs/reports/2026-06-06-pass3-effort-cost-curves/pass3-answer-log-cost.svg`.
