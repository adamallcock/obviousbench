---
title: OpenRouter Nemotron Eval Smoke
date: 2026-05-30
type: status
status: draft
---

# OpenRouter Nemotron Eval Smoke

## Purpose

Validate that ObviousBench can run through Inspect against an OpenRouter-hosted
model with no benchmark tools enabled.

Model:

```text
openai/nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free
```

Inspect provider wiring:

```text
--model-base-url https://openrouter.ai/api/v1
OPENAI_API_KEY loaded from Keychain service OPENROUTER_API_KEY
```

The benchmark task uses Inspect `generate()` without tools. No search, file, or
function tools were provided to the model during these evals.

## Commands

Smoke:

```bash
OPENAI_API_KEY="$(security find-generic-password -s OPENROUTER_API_KEY -w)" \
  .venv/bin/inspect eval obviousbench/tasks/smoke.py \
  --model openai/nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free \
  --model-base-url https://openrouter.ai/api/v1 \
  --log-dir results/raw \
  --limit 3 \
  --max-connections 1 \
  --max-retries 1 \
  --timeout 120 \
  --no-log-realtime \
  --no-log-model-api
```

Character-count subset:

```bash
OPENAI_API_KEY="$(security find-generic-password -s OPENROUTER_API_KEY -w)" \
  .venv/bin/inspect eval obviousbench/tasks/character_count.py \
  --model openai/nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free \
  --model-base-url https://openrouter.ai/api/v1 \
  --log-dir results/raw \
  --limit 10 \
  --max-connections 1 \
  --max-retries 1 \
  --timeout 120 \
  --no-log-realtime \
  --no-log-model-api
```

Archetype-expansion subset:

```bash
OPENAI_API_KEY="$(security find-generic-password -s OPENROUTER_API_KEY -w)" \
  .venv/bin/inspect eval obviousbench/tasks/archetype_expansions.py \
  --model openai/nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free \
  --model-base-url https://openrouter.ai/api/v1 \
  --log-dir results/raw \
  --limit 20 \
  --max-connections 1 \
  --max-retries 1 \
  --timeout 120 \
  --no-log-realtime \
  --no-log-model-api
```

## Results

Completed logs:

```text
results/raw/2026-05-30T23-18-50-00-00_smoke_kTnvqiG7enXGvN75Uqg8Yv.eval
results/raw/2026-05-30T23-19-06-00-00_character-count_4aGapBDFVSUZ82VRnQu7H2.eval
```

Partial expansion log:

```text
results/raw/2026-05-30T23-20-00-00-00_archetype-expansions_N4QbXRJ3qmmfJLf6zkR4kT.eval
```

Summary outputs:

```text
results/summaries/openrouter-nemotron-smoke/summary.csv
results/summaries/openrouter-nemotron-character-count/summary.csv
results/summaries/openrouter-nemotron-expansion-partial/summary.csv
```

Observed metrics:

```text
smoke: 3 total, 3 scored, 3 correct, 0 failures
character_count: 10 total, 10 scored, 10 correct, 0 failures
archetype_expansions partial: 19 total, 17 scored, 15 correct, 2 scored failures, 2 provider errors
```

The two scored expansion failures were numerically correct but included units:

```text
Expected 4.827, got 4.827 km
Expected 0.75, got 0.75 kilograms
```

Interpretation: the model solved the arithmetic, but the exact-string scorer
penalized unit suffixes. This is useful signal for scorer/prompt policy before
larger decimal/unit-conversion runs.

Follow-up: `exact_string_trim_v0` now accepts a single matching numeric value
with unit text for numeric targets, while rejecting outputs with multiple
numeric values as ambiguous. The historical summary CSV above was produced
before that scorer adjustment.

## Operational Notes

- The OpenRouter free model rate-limited during the expansion subset after 17
  logged samples.
- A second 10-sample expansion attempt hit rate limits after 2 logged samples.
- For larger OpenRouter runs, use smaller batches, wait between runs, or use a
  paid/rate-limit-stable OpenRouter model.
- Keep `--no-log-model-api` enabled unless raw provider request/response logs
  are explicitly needed.

## 429 Follow-Up

Added a 429-aware batch wrapper:

```text
scripts/run_openrouter_batches.py
obviousbench/runners/openrouter_batches.py
```

The wrapper uses the native Inspect `openrouter/...` provider, reads
`OPENROUTER_API_KEY` from Keychain, batches sample IDs, and retries a failed
batch after OpenRouter's embedded `X-RateLimit-Reset` timestamp when a 429
escapes Inspect's internal retry loop.

Recommended starting point for the free Nemotron model:

```bash
.venv/bin/python scripts/run_openrouter_batches.py \
  --task obviousbench/tasks/archetype_expansions.py \
  --dataset data/public_v0/archetype_expansions_2026-05-30.jsonl \
  --batch-size 8 \
  --inspect-max-retries 6 \
  --timeout 900 \
  --attempt-timeout 120
```
