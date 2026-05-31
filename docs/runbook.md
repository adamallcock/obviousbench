---
title: ObviousBench Runbook
date: 2026-05-30
type: runbook
status: draft
---

# ObviousBench Runbook

This runbook describes the local ObviousBench v0.1 workflow.

## Current Reality

ObviousBench currently has runnable benchmark infrastructure and a generated v0
seed dataset. The dataset is inspired by source archetypes, not mined item by
item from the web.

Current public dataset:

```text
318 total items
316 generated variants
2 public archetype items
8 task families
```

## Install

```bash
python -m venv .venv
.venv/bin/python -m pip install -e ".[dev]"
```

## Validate Datasets

```bash
.venv/bin/python scripts/validate_dataset.py data/public_v0/*.jsonl data/calibration_v0/smoke_test.jsonl
```

Expected output:

```text
Validation passed.
```

## Regenerate Public V0 Data

Preview counts:

```bash
.venv/bin/python scripts/generate_public_v0.py --dry-run
```

Write generated JSONL files:

```bash
.venv/bin/python scripts/generate_public_v0.py --write
```

## Run A Local Mock Smoke Eval

This checks Inspect task loading, prompting, scoring, logs, and summarization
without calling an external model provider.

```bash
.venv/bin/inspect eval obviousbench/tasks/smoke.py \
  --model mockllm/model \
  --log-dir results/raw \
  --limit 3 \
  --no-log-realtime
```

## Run An OpenAI Smoke Eval

The repo does not store an API key. The command below assumes a Keychain item
with service name `OPENAI_API_KEY`.

```bash
OPENAI_API_KEY="$(security find-generic-password -s OPENAI_API_KEY -w)" \
  .venv/bin/inspect eval obviousbench/tasks/smoke.py \
  --model openai/gpt-4.1 \
  --log-dir results/raw \
  --limit 3 \
  --max-connections 1 \
  --max-retries 1 \
  --timeout 90 \
  --no-log-realtime
```

Do not echo, print, commit, or store the plaintext key.

## Run An OpenRouter Smoke Eval

The command below uses OpenRouter's OpenAI-compatible endpoint. It assumes a
Keychain item with service name `OPENROUTER_API_KEY`.

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

This benchmark path does not provide tools to the model. `--no-log-model-api`
keeps raw provider requests and responses out of the Inspect log.

The free OpenRouter model may rate-limit on larger subsets. Prefer small
batches first.

## Run OpenRouter In 429-Aware Batches

For free OpenRouter models, prefer the batch wrapper. It uses the native Inspect
OpenRouter provider, loads `OPENROUTER_API_KEY` from Keychain, runs one
connection, and retries a failed batch after OpenRouter's
`X-RateLimit-Reset` timestamp when a 429 escapes Inspect's internal retries.

Dry run:

```bash
.venv/bin/python scripts/run_openrouter_batches.py \
  --task obviousbench/tasks/archetype_expansions.py \
  --dataset data/public_v0/archetype_expansions_2026-05-30.jsonl \
  --batch-size 8 \
  --dry-run
```

Actual run:

```bash
.venv/bin/python scripts/run_openrouter_batches.py \
  --task obviousbench/tasks/archetype_expansions.py \
  --dataset data/public_v0/archetype_expansions_2026-05-30.jsonl \
  --batch-size 4 \
  --inspect-max-retries 6 \
  --timeout 900 \
  --attempt-timeout 180 \
  --independent-batches \
  --resume \
  --continue-after-batch-error
```

Notes:

- Use `openrouter/...` model strings with this wrapper, not `openai/...` plus a
  base URL.
- Keep `--batch-size` below the provider's per-minute free-model limit. The
  observed OpenRouter free-model limit was 16 requests per minute.
- `--attempt-timeout` is the per-request generation timeout passed to Inspect.
  The 2026-05-30 Nemotron run used `45` seconds and several slow reasoning
  responses timed out. Prefer `180` seconds for this model unless you want
  provider-error rows quickly.
- `--independent-batches` writes each batch to its own log directory and records
  a `batch-manifest.jsonl`.
- `--resume` skips manifest entries whose latest status is `success`, so a
  failed provider run can continue without repeating good batches.
- The wrapper adds `--no-fail-on-error`, `--continue-on-fail`, and
  `--score-on-error` so a few provider errors do not discard the entire run.
- Use `--strict-batch-errors` when you want 429s and timeouts to fail a batch
  and trigger outer retry/sleep behavior instead of becoming provider-error
  samples.
- Use `--continue-after-batch-error` with independent batches when one failed
  batch should be recorded in the manifest while later batches continue to run.
  The process still exits non-zero if any batch failed, but completed batch logs
  remain usable and `--resume` can retry only the incomplete parts.
- The wrapper keeps `--no-log-model-api` enabled so raw model requests and
  responses are not written to the Inspect log.

## Summarize Logs

```bash
.venv/bin/obviousbench summarize --logs results/raw --out results/summaries
```

The summarizer always writes:

- `summary.csv`: run-level accuracy, failure, token, and optional cost totals.
- `failure_gallery.md`: high-legibility failure examples.
- `usage_by_sample.csv`: one row per sample.
- `usage_by_family.csv`: family-level rollups.
- `usage_by_section.csv`: section rollups, where section is
  `family + subfamily`.
- `usage_by_question.csv`: question-level rollups for spotting specific prompt
  lines that are costly or failure-prone.

Estimated cost uses the local Node `runcost` bridge by default:

```bash
npm install
.venv/bin/obviousbench summarize \
  --logs results/raw \
  --out results/summaries
```

Costed summaries also write `cost_ledger.json`, with one runcost ledger per
sample. The bridge uses normalized Inspect usage rather than raw provider
responses, so `--no-log-model-api` runs can still be priced. Use `--cost none`
to skip pricing.

## Build A Balanced Barrage

Balanced barrage profiles use the shape `balanced_<families>x<items>`.
`balanced_8x10` is the default diagnostic barrage: 8 task families, 10 samples
per family, 80 samples total. Selection is deterministic for a given seed and
round-robins across subfamilies inside each family before interleaving families
in the final sample order.

Materialize a barrage JSONL:

```bash
.venv/bin/obviousbench make-barrage \
  --profile balanced_8x10 \
  --seed 20260531 \
  --out data/barrages/balanced_8x10_seed_20260531.jsonl
```

Run the dynamic barrage task directly without writing a JSONL file:

```bash
.venv/bin/inspect eval obviousbench/tasks/barrage.py \
  --model <provider/model> \
  --log-dir results/raw \
  -T profile=balanced_8x10 \
  -T seed=20260531
```

Run a materialized barrage:

```bash
.venv/bin/inspect eval obviousbench/tasks/barrage.py \
  --model <provider/model> \
  --log-dir results/raw \
  -T dataset=data/barrages/balanced_8x10_seed_20260531.jsonl
```

Outputs:

```text
results/summaries/summary.csv
results/summaries/failure_gallery.md
```

These paths are ignored by git.

## Quality Gates

```bash
.venv/bin/python -m pytest tests -q
.venv/bin/python -m ruff check .
.venv/bin/python -m compileall obviousbench
.venv/bin/python scripts/validate_dataset.py data/public_v0/*.jsonl data/calibration_v0/smoke_test.jsonl
```

## Inspect Current Dataset Composition

```bash
.venv/bin/python - <<'PY'
import json
from collections import Counter
from pathlib import Path

rows = []
for path in Path("data/public_v0").glob("*.jsonl"):
    for line in path.read_text().splitlines():
        rows.append(json.loads(line))

print("total", len(rows))
print("source_type", dict(Counter(row["source_type"] for row in rows)))
print("families", dict(Counter(row["family"] for row in rows)))
PY
```

## What Still Needs Human Work

- Mine and normalize real public examples beyond the current small source catalog.
- Reproduce source claims against a model panel.
- Human-review generated variants for ambiguity and scorer suitability.
- Run the full chosen 5-8 model panel.
- Manually inspect real model failures for scorer false positives and false negatives.
- Decide which result artifacts should be promoted out of ignored `results/`.
