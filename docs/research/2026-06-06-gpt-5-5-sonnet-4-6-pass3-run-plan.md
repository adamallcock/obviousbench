---
title: GPT-5.5 And Sonnet 4.6 Pass^3 Run Plan
date: 2026-06-06
type: plan
status: complete
---

# GPT-5.5 And Sonnet 4.6 Pass^3 Run Plan

## Objective

Run a narrow pass^3 reliability slice on the 224-item hard-obvious 8x28 barrage, then plot answer-correct pass^3 against log run cost.

## Design

- Dataset: `data/barrages/hard_obvious_8x28_seed_20260531.jsonl`
- Trials: 3 independent cache-disabled trials per setting
- Total entries: 27
- Total attempts: 6,048
- GPT-5.5 settings: `none`, `low`, `medium`, `high`, `xhigh`
- Claude Sonnet 4.6 adaptive-thinking settings: `low`, `medium`, `high`, `max`
- Primary plotted metric: `answer_correct` pass^3
- Secondary table metric: `strict_correct` pass^3

## Execution

- Panel: `configs/gpt_5_5_sonnet_4_6_pass3_8x28_20260606_panel.yaml`
- Raw root: `results/raw/gpt-5-5-sonnet-4-6-pass3-8x28-20260606`
- Summary root: `results/summaries/gpt-5-5-sonnet-4-6-pass3-8x28-20260606/runs`
- Manifest: `configs/gpt_5_5_sonnet_4_6_pass3_8x28_20260606_manifest.csv`
- Status: `results/summaries/gpt-5-5-sonnet-4-6-pass3-8x28-20260606/status.jsonl`

Full run command:

```bash
OPENAI_API_KEY="$(security find-generic-password -s OPENAI_API_KEY -w)" \
ANTHROPIC_API_KEY="$(security find-generic-password -s ANTHROPIC_API_KEY -w)" \
.venv/bin/python scripts/run_model_panel.py \
  --panel configs/gpt_5_5_sonnet_4_6_pass3_8x28_20260606_panel.yaml \
  --dataset data/barrages/hard_obvious_8x28_seed_20260531.jsonl \
  --raw-root results/raw/gpt-5-5-sonnet-4-6-pass3-8x28-20260606 \
  --summary-root results/summaries/gpt-5-5-sonnet-4-6-pass3-8x28-20260606/runs \
  --manifest-out configs/gpt_5_5_sonnet_4_6_pass3_8x28_20260606_manifest.csv \
  --status-out results/summaries/gpt-5-5-sonnet-4-6-pass3-8x28-20260606/status.jsonl \
  --mode full \
  --no-cache \
  --no-skip-completed \
  --cost runcost
```

## Acceptance Criteria

- 27 status rows exist and all have `status=passed` and `returncode=0`.
- Every trial summary has 224 rows in `usage_by_sample.csv`.
- Status inspect commands contain no `--cache` flag.
- Aggregate pass^3 CSV and Markdown result note are written under `docs/research/`.
- A log-cost SVG/PNG curve is generated with cost on x and answer-correct pass^3 on y.

## Outcome

Completed on 2026-06-06. Results were written to
`docs/research/2026-06-06-gpt-5-5-sonnet-4-6-8x28-pass3-results.md`,
and the combined pass^3 curve was written to
`docs/reports/2026-06-06-pass3-effort-cost-curves/pass3-answer-log-cost.svg`.
