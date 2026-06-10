---
title: GPT-5.4 Nano 8x28 Passk Run Plan
date: 2026-06-06
type: plan
status: active
---

# GPT-5.4 Nano 8x28 Passk Run Plan

## Goal

Run a cache-disabled reliability experiment for `openai/gpt-5.4-nano` on
`data/barrages/hard_obvious_8x28_seed_20260531.jsonl`.

The run covers four reasoning modes:

- `none`
- `low`
- `medium`
- `high`

Each mode gets five independent full 224-item trials. This supports empirical
`pass^3`, `pass@3`, `pass^5`, and `pass@5` calculations.

## Run Artifacts

- Panel: `configs/gpt_5_4_nano_passk_8x28_20260606_panel.yaml`
- Raw root: `results/raw/gpt-5-4-nano-passk-8x28-20260606`
- Summary root: `results/summaries/gpt-5-4-nano-passk-8x28-20260606`
- Manifest: `configs/gpt_5_4_nano_passk_8x28_20260606_manifest.csv`
- Status: `results/summaries/gpt-5-4-nano-passk-8x28-20260606/status.jsonl`
- Planned report: `docs/research/2026-06-06-gpt-5-4-nano-8x28-passk-results.md`

## Protocol

Use direct OpenAI via Inspect:

```bash
OPENAI_API_KEY="$(security find-generic-password -s OPENAI_API_KEY -w)" \
.venv/bin/python scripts/run_model_panel.py \
  --panel configs/gpt_5_4_nano_passk_8x28_20260606_panel.yaml \
  --dataset data/barrages/hard_obvious_8x28_seed_20260531.jsonl \
  --raw-root results/raw/gpt-5-4-nano-passk-8x28-20260606 \
  --summary-root results/summaries/gpt-5-4-nano-passk-8x28-20260606/runs \
  --manifest-out configs/gpt_5_4_nano_passk_8x28_20260606_manifest.csv \
  --status-out results/summaries/gpt-5-4-nano-passk-8x28-20260606/status.jsonl \
  --mode full \
  --no-cache \
  --no-skip-completed \
  --cost runcost
```

The panel sets `--max-connections=32`, `--timeout=900`, `--attempt-timeout=180`,
`--max-retries=1`, `--continue-on-fail`, and `--score-on-error`.

## Acceptance Criteria

- All 20 entries complete with 224 attempted samples.
- Accepted reliability metrics use only entries with 224 scored samples, unless
  provider errors are explicitly reported as reliability failures.
- Cache is disabled in every status row: inspect commands must not include
  `--cache`.
- Every mode has exactly five summary directories.
- The result report includes `answer_pass^3`, `answer_pass@3`, `answer_pass^5`,
  `answer_pass@5`, `strict_pass^3`, `strict_pass@3`, `strict_pass^5`,
  `strict_pass@5`, and per-mode disagreement rates.

## Expected Monitoring

This is a 4,480-sample provider run. With `--max-connections=32`, the next
meaningful check after launch is roughly 8 to 12 minutes, unless startup fails
quickly from credentials, schema, or provider validation.
