---
title: Paper V1 Final Sweep Plan
date: 2026-06-01
type: runbook
status: ready
---

# Paper V1 Final Sweep Plan

This is a dry-run handoff. It writes commands and manifests but does not
run model providers.

Run allowed: YES

`Run allowed` covers readiness, cost, and smoke-status gates. Provider
execution is still blocked if credentials or provider access are
unavailable at runtime.

Panel: `configs/paper_v1_model_panel.yaml`
Dataset: `data/barrages/hard_obvious_8x10_seed_20260531.jsonl`
Paper manifest: `data/splits/paper_v1_manifest.jsonl`
Readiness profile: `preprint`
Comparison manifest: `configs/paper_v1_final_sweep_manifest.csv`
Raw log root: `results/raw/paper-v1-final-high-cap`
Summary root: `results/summaries/paper-v1-final-high-cap`
Comparison dir: `results/summaries/paper-v1-final-high-cap/comparison`
Report dir: `docs/reports/2026-06-01-paper-v1-final-high-cap-sweep`
Panel entries: 12
Smoke status: `docs/research/2026-06-01-paper-v1-smoke-status.md`
Run freeze policy: `docs/research/2026-06-01-paper-v1-run-freeze-policy.md`

## Preconditions

- `make -C paper readiness-preprint` passes.
- The manuscript omits empirical human-baseline claims or labels them as planned validation.
- Any `human-trivial` wording is grounded in item-card design and review, not participant measurements.
- Model aliases and pricing are re-verified immediately before running.
- The expected cost is accepted.
- The operator confirms credentials and provider access.

## Manifest Runner

Preferred final execution wrapper:

```bash
.venv/bin/python scripts/run_model_panel.py --panel configs/paper_v1_model_panel.yaml --dataset data/barrages/hard_obvious_8x10_seed_20260531.jsonl --raw-root results/raw/paper-v1-final-high-cap --summary-root results/summaries/paper-v1-final-high-cap --manifest-out configs/paper_v1_final_sweep_manifest.csv --status-out results/summaries/paper-v1-final-high-cap/status.jsonl --mode full --no-cache
```

## Model Commands

### OpenAI GPT-5 nano minimal

- Entry ID: `paper-openai-gpt-5-nano-minimal`
- Provider route: `openai`
- Inspect model: `openai/gpt-5-nano`

Inspect run:

```bash
.venv/bin/python -m obviousbench.runners.inspect_eval --task obviousbench/tasks/barrage.py --model openai/gpt-5-nano --log-dir results/raw/paper-v1-final-high-cap/paper-openai-gpt-5-nano-minimal -T dataset=/Users/adamallcock/Documents/Coding/benchmark-obviousbench/data/barrages/hard_obvious_8x10_seed_20260531.jsonl --inspect-arg=--no-log-model-api --inspect-arg=--no-log-realtime --inspect-arg=--timeout=60 --inspect-arg=--max-retries=0 --generation-setting temperature=0 --generation-setting max_tokens=10000 --generation-setting reasoning_effort=minimal
```

Summarize/rescore:

```bash
.venv/bin/python -m obviousbench.cli rescore --logs results/raw/paper-v1-final-high-cap/paper-openai-gpt-5-nano-minimal --out results/summaries/paper-v1-final-high-cap/paper-openai-gpt-5-nano-minimal --cost runcost
```

### OpenAI GPT-4.1

- Entry ID: `paper-openai-gpt-4-1`
- Provider route: `openai`
- Inspect model: `openai/gpt-4.1`

Inspect run:

```bash
.venv/bin/python -m obviousbench.runners.inspect_eval --task obviousbench/tasks/barrage.py --model openai/gpt-4.1 --log-dir results/raw/paper-v1-final-high-cap/paper-openai-gpt-4-1 -T dataset=/Users/adamallcock/Documents/Coding/benchmark-obviousbench/data/barrages/hard_obvious_8x10_seed_20260531.jsonl --inspect-arg=--no-log-model-api --inspect-arg=--no-log-realtime --inspect-arg=--timeout=60 --inspect-arg=--max-retries=0 --generation-setting temperature=0 --generation-setting max_tokens=10000
```

Summarize/rescore:

```bash
.venv/bin/python -m obviousbench.cli rescore --logs results/raw/paper-v1-final-high-cap/paper-openai-gpt-4-1 --out results/summaries/paper-v1-final-high-cap/paper-openai-gpt-4-1 --cost runcost
```

### OpenAI GPT-4.1 mini

- Entry ID: `paper-openai-gpt-4-1-mini`
- Provider route: `openai`
- Inspect model: `openai/gpt-4.1-mini`

Inspect run:

```bash
.venv/bin/python -m obviousbench.runners.inspect_eval --task obviousbench/tasks/barrage.py --model openai/gpt-4.1-mini --log-dir results/raw/paper-v1-final-high-cap/paper-openai-gpt-4-1-mini -T dataset=/Users/adamallcock/Documents/Coding/benchmark-obviousbench/data/barrages/hard_obvious_8x10_seed_20260531.jsonl --inspect-arg=--no-log-model-api --inspect-arg=--no-log-realtime --inspect-arg=--timeout=60 --inspect-arg=--max-retries=0 --generation-setting temperature=0 --generation-setting max_tokens=10000
```

Summarize/rescore:

```bash
.venv/bin/python -m obviousbench.cli rescore --logs results/raw/paper-v1-final-high-cap/paper-openai-gpt-4-1-mini --out results/summaries/paper-v1-final-high-cap/paper-openai-gpt-4-1-mini --cost runcost
```

### Anthropic Claude Sonnet 4.6

- Entry ID: `paper-anthropic-claude-sonnet-4-6`
- Provider route: `anthropic`
- Inspect model: `anthropic/claude-sonnet-4-6`

Inspect run:

```bash
.venv/bin/python -m obviousbench.runners.inspect_eval --task obviousbench/tasks/barrage.py --model anthropic/claude-sonnet-4-6 --log-dir results/raw/paper-v1-final-high-cap/paper-anthropic-claude-sonnet-4-6 -T dataset=/Users/adamallcock/Documents/Coding/benchmark-obviousbench/data/barrages/hard_obvious_8x10_seed_20260531.jsonl --inspect-arg=--no-log-model-api --inspect-arg=--no-log-realtime --inspect-arg=--timeout=60 --inspect-arg=--max-retries=0 --generation-setting temperature=0 --generation-setting max_tokens=10000
```

Summarize/rescore:

```bash
.venv/bin/python -m obviousbench.cli rescore --logs results/raw/paper-v1-final-high-cap/paper-anthropic-claude-sonnet-4-6 --out results/summaries/paper-v1-final-high-cap/paper-anthropic-claude-sonnet-4-6 --cost runcost
```

### Anthropic Claude Haiku 4.5

- Entry ID: `paper-anthropic-claude-haiku-4-5`
- Provider route: `anthropic`
- Inspect model: `anthropic/claude-haiku-4-5`

Inspect run:

```bash
.venv/bin/python -m obviousbench.runners.inspect_eval --task obviousbench/tasks/barrage.py --model anthropic/claude-haiku-4-5 --log-dir results/raw/paper-v1-final-high-cap/paper-anthropic-claude-haiku-4-5 -T dataset=/Users/adamallcock/Documents/Coding/benchmark-obviousbench/data/barrages/hard_obvious_8x10_seed_20260531.jsonl --inspect-arg=--no-log-model-api --inspect-arg=--no-log-realtime --inspect-arg=--timeout=60 --inspect-arg=--max-retries=0 --generation-setting temperature=0 --generation-setting max_tokens=10000
```

Summarize/rescore:

```bash
.venv/bin/python -m obviousbench.cli rescore --logs results/raw/paper-v1-final-high-cap/paper-anthropic-claude-haiku-4-5 --out results/summaries/paper-v1-final-high-cap/paper-anthropic-claude-haiku-4-5 --cost runcost
```

### Gemini 3.5 Flash

- Entry ID: `paper-gemini-3-5-flash`
- Provider route: `gemini`
- Inspect model: `google/gemini-3.5-flash`

Inspect run:

```bash
.venv/bin/python -m obviousbench.runners.inspect_eval --task obviousbench/tasks/barrage.py --model google/gemini-3.5-flash --log-dir results/raw/paper-v1-final-high-cap/paper-gemini-3-5-flash -T dataset=/Users/adamallcock/Documents/Coding/benchmark-obviousbench/data/barrages/hard_obvious_8x10_seed_20260531.jsonl --inspect-arg=--no-log-model-api --inspect-arg=--no-log-realtime --inspect-arg=--timeout=60 --inspect-arg=--max-retries=0 --generation-setting temperature=0 --generation-setting max_tokens=10000
```

Summarize/rescore:

```bash
.venv/bin/python -m obviousbench.cli rescore --logs results/raw/paper-v1-final-high-cap/paper-gemini-3-5-flash --out results/summaries/paper-v1-final-high-cap/paper-gemini-3-5-flash --cost runcost
```

### Gemini 2.5 Flash-Lite

- Entry ID: `paper-gemini-2-5-flash-lite`
- Provider route: `gemini`
- Inspect model: `google/gemini-2.5-flash-lite`

Inspect run:

```bash
.venv/bin/python -m obviousbench.runners.inspect_eval --task obviousbench/tasks/barrage.py --model google/gemini-2.5-flash-lite --log-dir results/raw/paper-v1-final-high-cap/paper-gemini-2-5-flash-lite -T dataset=/Users/adamallcock/Documents/Coding/benchmark-obviousbench/data/barrages/hard_obvious_8x10_seed_20260531.jsonl --inspect-arg=--no-log-model-api --inspect-arg=--no-log-realtime --inspect-arg=--timeout=60 --inspect-arg=--max-retries=0 --generation-setting temperature=0 --generation-setting max_tokens=10000
```

Summarize/rescore:

```bash
.venv/bin/python -m obviousbench.cli rescore --logs results/raw/paper-v1-final-high-cap/paper-gemini-2-5-flash-lite --out results/summaries/paper-v1-final-high-cap/paper-gemini-2-5-flash-lite --cost runcost
```

### Grok 4.3

- Entry ID: `paper-grok-4-3`
- Provider route: `grok`
- Inspect model: `grok/grok-4.3`

Inspect run:

```bash
.venv/bin/python -m obviousbench.runners.inspect_eval --task obviousbench/tasks/barrage.py --model grok/grok-4.3 --log-dir results/raw/paper-v1-final-high-cap/paper-grok-4-3 -T dataset=/Users/adamallcock/Documents/Coding/benchmark-obviousbench/data/barrages/hard_obvious_8x10_seed_20260531.jsonl --inspect-arg=--no-log-model-api --inspect-arg=--no-log-realtime --inspect-arg=--timeout=60 --inspect-arg=--max-retries=0 --generation-setting temperature=0 --generation-setting max_tokens=10000
```

Summarize/rescore:

```bash
.venv/bin/python -m obviousbench.cli rescore --logs results/raw/paper-v1-final-high-cap/paper-grok-4-3 --out results/summaries/paper-v1-final-high-cap/paper-grok-4-3 --cost runcost
```

### Xiaomi MiMo-V2-Flash

- Entry ID: `paper-openrouter-xiaomi-mimo-v2-flash`
- Provider route: `openrouter`
- Inspect model: `openrouter/xiaomi/mimo-v2-flash`

Inspect run:

```bash
.venv/bin/python -m obviousbench.runners.inspect_eval --task obviousbench/tasks/barrage.py --model openrouter/xiaomi/mimo-v2-flash --log-dir results/raw/paper-v1-final-high-cap/paper-openrouter-xiaomi-mimo-v2-flash -T dataset=/Users/adamallcock/Documents/Coding/benchmark-obviousbench/data/barrages/hard_obvious_8x10_seed_20260531.jsonl --inspect-arg=--no-log-model-api --inspect-arg=--no-log-realtime --inspect-arg=--timeout=60 --inspect-arg=--max-retries=0 --generation-setting temperature=0 --generation-setting max_tokens=10000
```

Summarize/rescore:

```bash
.venv/bin/python -m obviousbench.cli rescore --logs results/raw/paper-v1-final-high-cap/paper-openrouter-xiaomi-mimo-v2-flash --out results/summaries/paper-v1-final-high-cap/paper-openrouter-xiaomi-mimo-v2-flash --cost runcost
```

### NVIDIA Nemotron 3 Nano 30B A3B

- Entry ID: `paper-openrouter-nemotron-3-nano`
- Provider route: `openrouter`
- Inspect model: `openrouter/nvidia/nemotron-3-nano-30b-a3b`

Inspect run:

```bash
.venv/bin/python -m obviousbench.runners.inspect_eval --task obviousbench/tasks/barrage.py --model openrouter/nvidia/nemotron-3-nano-30b-a3b --log-dir results/raw/paper-v1-final-high-cap/paper-openrouter-nemotron-3-nano -T dataset=/Users/adamallcock/Documents/Coding/benchmark-obviousbench/data/barrages/hard_obvious_8x10_seed_20260531.jsonl --inspect-arg=--no-log-model-api --inspect-arg=--no-log-realtime --inspect-arg=--timeout=60 --inspect-arg=--max-retries=0 --generation-setting temperature=0 --generation-setting max_tokens=10000
```

Summarize/rescore:

```bash
.venv/bin/python -m obviousbench.cli rescore --logs results/raw/paper-v1-final-high-cap/paper-openrouter-nemotron-3-nano --out results/summaries/paper-v1-final-high-cap/paper-openrouter-nemotron-3-nano --cost runcost
```

### OpenAI GPT-OSS 20B

- Entry ID: `paper-openrouter-gpt-oss-20b`
- Provider route: `openrouter`
- Inspect model: `openrouter/openai/gpt-oss-20b`

Inspect run:

```bash
.venv/bin/python -m obviousbench.runners.inspect_eval --task obviousbench/tasks/barrage.py --model openrouter/openai/gpt-oss-20b --log-dir results/raw/paper-v1-final-high-cap/paper-openrouter-gpt-oss-20b -T dataset=/Users/adamallcock/Documents/Coding/benchmark-obviousbench/data/barrages/hard_obvious_8x10_seed_20260531.jsonl --inspect-arg=--no-log-model-api --inspect-arg=--no-log-realtime --inspect-arg=--timeout=60 --inspect-arg=--max-retries=0 --generation-setting temperature=0 --generation-setting max_tokens=10000
```

Summarize/rescore:

```bash
.venv/bin/python -m obviousbench.cli rescore --logs results/raw/paper-v1-final-high-cap/paper-openrouter-gpt-oss-20b --out results/summaries/paper-v1-final-high-cap/paper-openrouter-gpt-oss-20b --cost runcost
```

### Qwen3 Next 80B A3B Instruct

- Entry ID: `paper-openrouter-qwen3-next`
- Provider route: `openrouter`
- Inspect model: `openrouter/qwen/qwen3-next-80b-a3b-instruct`

Inspect run:

```bash
.venv/bin/python -m obviousbench.runners.inspect_eval --task obviousbench/tasks/barrage.py --model openrouter/qwen/qwen3-next-80b-a3b-instruct --log-dir results/raw/paper-v1-final-high-cap/paper-openrouter-qwen3-next -T dataset=/Users/adamallcock/Documents/Coding/benchmark-obviousbench/data/barrages/hard_obvious_8x10_seed_20260531.jsonl --inspect-arg=--no-log-model-api --inspect-arg=--no-log-realtime --inspect-arg=--timeout=60 --inspect-arg=--max-retries=0 --generation-setting temperature=0 --generation-setting max_tokens=10000
```

Summarize/rescore:

```bash
.venv/bin/python -m obviousbench.cli rescore --logs results/raw/paper-v1-final-high-cap/paper-openrouter-qwen3-next --out results/summaries/paper-v1-final-high-cap/paper-openrouter-qwen3-next --cost runcost
```

## Post-Run Aggregation

Build the comparison tables:

```bash
.venv/bin/python -m obviousbench.cli build-comparison --manifest configs/paper_v1_final_sweep_manifest.csv --out results/summaries/paper-v1-final-high-cap/comparison --manual-xai-costs
```

Build the static report:

```bash
.venv/bin/python -m obviousbench.cli build-report --comparison-dir results/summaries/paper-v1-final-high-cap/comparison --out docs/reports/2026-06-01-paper-v1-final-high-cap-sweep --generated-on 2026-06-01 --title 'ObviousBench Paper V1 Final Sweep'
```

Regenerate paper tables and figures from final results:

```bash
.venv/bin/python scripts/build_paper_assets.py --manifest data/splits/paper_v1_manifest.jsonl --dataset data/barrages/hard_obvious_8x10_seed_20260531.jsonl --human-baseline data/human_baseline/paper_v1.csv --model-panel configs/paper_v1_model_panel.yaml --final-results-dir results/summaries/paper-v1-final-high-cap/comparison --out paper/tables --figures-out paper/figures
```

## Panel Notes

- Config run status: `planned_not_run`
- Profile: `hard_obvious_8x10`
- Seed: `20260531`
