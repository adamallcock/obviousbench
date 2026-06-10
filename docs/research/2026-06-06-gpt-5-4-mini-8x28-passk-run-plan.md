---
title: GPT-5.4 Mini 8x28 Pass-k Run Plan
date: 2026-06-06
type: plan
status: complete
---

# GPT-5.4 Mini 8x28 Pass-k Run Plan

## Objective

Run the same pass-k reliability probe used for GPT-5.4 nano against `openai/gpt-5.4-mini` on the 224-item hard-obvious 8x28 barrage.

## Design

- Model: `openai/gpt-5.4-mini`
- Dataset: `data/barrages/hard_obvious_8x28_seed_20260531.jsonl`
- Modes: `none`, `low`, `medium`, `high`
- Trials: 5 independent cache-disabled trials per mode
- Total entries: 20
- Total attempts: 4,480
- Primary metric: `strict_correct`
- Secondary metric: `answer_correct`
- Pass-k views: pass^3, pass@3, pass^5, pass@5, unstable item rate, pairwise disagreement

## Execution

- Panel: `configs/gpt_5_4_mini_passk_8x28_20260606_panel.yaml`
- Raw root: `results/raw/gpt-5-4-mini-passk-8x28-20260606`
- Summary root: `results/summaries/gpt-5-4-mini-passk-8x28-20260606/runs`
- Manifest: `configs/gpt_5_4_mini_passk_8x28_20260606_manifest.csv`
- Status: `results/summaries/gpt-5-4-mini-passk-8x28-20260606/status.jsonl`

Full run command:

```bash
OPENAI_API_KEY="$(security find-generic-password -s OPENAI_API_KEY -w)" \
.venv/bin/python scripts/run_model_panel.py \
  --panel configs/gpt_5_4_mini_passk_8x28_20260606_panel.yaml \
  --dataset data/barrages/hard_obvious_8x28_seed_20260531.jsonl \
  --raw-root results/raw/gpt-5-4-mini-passk-8x28-20260606 \
  --summary-root results/summaries/gpt-5-4-mini-passk-8x28-20260606/runs \
  --manifest-out configs/gpt_5_4_mini_passk_8x28_20260606_manifest.csv \
  --status-out results/summaries/gpt-5-4-mini-passk-8x28-20260606/status.jsonl \
  --mode full \
  --no-cache \
  --no-skip-completed \
  --cost runcost
```

## Concurrency

This run uses `--max-connections=128` inside the panel defaults to reduce wall-clock time. The runner still executes panel entries sequentially, but each 224-sample Inspect eval can issue far more concurrent provider calls than the nano run's 32-connection setting.

## Acceptance Criteria

- 20 status rows exist and all have `returncode=0`.
- Every mode has exactly five independent trials.
- Every trial summary has 224 rows in `usage_by_sample.csv`.
- Status inspect commands contain no `--cache` flag.
- Results note and aggregate/item CSVs are written under `docs/research/`.
