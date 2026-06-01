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
401 total items
399 generated variants
2 public archetype items
8 task families
3 items with metamorphic group metadata
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

To also validate item-card contracts against the current public seed data:

```bash
.venv/bin/python scripts/validate_dataset.py \
  data/public_v0/*.jsonl \
  --item-cards-dir data/item_cards \
  --allow-extra-item-cards
```

Trusted future splits should require reviewed item cards:

```bash
.venv/bin/obviousbench validate \
  data/public_v0/*.jsonl \
  --item-cards-dir data/item_cards \
  --require-item-cards
```

`public_v0` currently has generated draft card stubs, so the strict
`--require-item-cards` mode is for reviewed/trusted split promotion, not for the
current draft-card seed set.

## Generate Item-Card Stubs

Use this when JSONL rows have changed and draft review cards need to be created
or regenerated:

```bash
.venv/bin/python scripts/generate_item_card_stubs.py \
  data/public_v0/*.jsonl \
  --out data/item_cards/public_v0/cards.yaml \
  --generated-on 2026-05-31
```

Generated cards are intentionally `review.status: draft` and contain
`TODO(review)` fields. They are provenance/review scaffolding, not evidence that
an item is trusted.

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
- The wrapper enables Inspect's local generation cache by default with
  `--cache 10Y` and `INSPECT_CACHE_DIR=.cache/inspect`. This caches provider
  completions only; summaries and scorers are recomputed when logs are
  summarized.
- Use `--no-cache` for fresh provider-behavior sweeps, or `--cache <duration>`
  for another expiry.
- Provider safety/error strings that arrive as assistant text, for example
  `SAFETY_CHECK_TYPE_*`, are retried by default as transient provider failures.
  These retry attempts bypass the Inspect cache so a cached refusal is not
  replayed. Use `--no-retry-provider-refusals` to disable this behavior.
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

## Run Any Inspect Eval With Cache Defaults

For non-OpenRouter runs, prefer the generic wrapper rather than calling
`inspect eval` directly during development:

```bash
.venv/bin/python scripts/run_inspect_eval.py \
  --task obviousbench/tasks/barrage.py \
  --model openai/gpt-5.4 \
  --log-dir results/raw \
  -T profile=hard_obvious_8x10 \
  -T seed=20260531 \
  --inspect-arg=--no-log-model-api
```

Defaults:

- `--cache 10Y`
- `--cache-dir .cache/inspect`
- raw Inspect flags are passed only when supplied via `--inspect-arg`

Use `--no-cache` to force fresh provider calls. Use repeated `--inspect-arg`
values to pass raw Inspect flags; use `--inspect-arg=--flag-name` when the raw
argument itself starts with `--`.

Like the OpenRouter batch runner, the generic wrapper retries provider
safety/error strings returned as assistant text once by default, rerunning only
the affected sample ids without Inspect cache. Use
`--no-retry-provider-refusals` or `--provider-refusal-retries <n>` to tune this.

## Summarize Logs

```bash
.venv/bin/obviousbench summarize --logs results/raw --out results/summaries
```

The summarizer always writes:

- `summary.csv`: run-level accuracy, failure, token, and optional cost totals.
- `failure_gallery.md`: high-legibility strict-failure examples, including
  answer-correct but format-noncompliant responses.
- `usage_by_sample.csv`: one row per sample.
- `usage_by_family.csv`: family-level rollups.
- `usage_by_section.csv`: section rollups, where section is
  `family + subfamily`.
- `usage_by_question.csv`: question-level rollups for spotting specific prompt
  lines that are costly or failure-prone.

When evaluated samples include metamorphic metadata, the summarizer also writes
`metamorphic_consistency.csv`. Provider errors, provider safety/error strings,
and timeouts are counted in `samples`, but accuracy-like correctness columns
use `scored_samples` so infrastructure failures do not become model-answer
failures.

Estimated cost uses the local Node 20+ `runcost` bridge by default:

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

When deterministic scorer logic changes, rescore existing logs instead of
calling providers again:

```bash
.venv/bin/obviousbench rescore \
  --logs results/raw/<run-dir> \
  --out results/summaries/<run-dir>-rescored
```

Summaries and rollups report three related metrics:

- `answer_accuracy`: the model gave the right answer content.
- `format_accuracy`: the model followed the required output format.
- `strict_accuracy`: answer and format were both correct.

Summaries also include Wilson 95% confidence intervals for `accuracy`,
`answer_accuracy`, and `strict_accuracy`. Treat them as uncertainty bands over
the scored samples, not as guarantees about future samples.

Use `build-comparison` to aggregate one-row run summaries into the model,
family, and section CSVs consumed by reports:

```bash
.venv/bin/obviousbench build-comparison \
  --manifest results/summaries/hard-obvious-panel-20260531/manifest.csv \
  --out results/summaries/hard-obvious-panel-20260531
```

If a comparison is being regenerated after rescoring, pass the old comparison as
`--baseline-comparison` to write `delta.csv`. When both the old and new summary
directories still contain `usage_by_sample.csv`, deltas are paired by
`sample_id` and include matched counts, wins, losses, ties, and a deterministic
bootstrap interval. If sample rows are missing, `delta.csv` falls back to
aggregate unpaired deltas and marks `delta_method=aggregate_unpaired`; use those
as directional checks rather than strong model-comparison claims. For direct xAI
Grok runs, add `--manual-xai-costs` when the local `runcost` card set does not
price the `grok/*` aliases.

Small panels such as 40 or 80 items are useful for fast regression checks, but
their intervals can be wide. Close rankings should be treated as directional
until repeated on a larger or more targeted panel.

Efficiency metrics are secondary diagnostics, not ranking keys. `summary.csv`,
comparison outputs, and usage rollups include token and cost efficiency fields
such as `tokens_per_scored_sample`, `tokens_per_correct`,
`cost_per_correct_usd`, `reasoning_token_share`, and `overthinking_index`.
Reasoning tokens are not reported by every provider; use
`reasoning_token_source` to distinguish reported reasoning usage from missing or
zero values.

Comparison builds also write `effort_curve.csv` and
`metamorphic_consistency.csv` when the source summaries contain the relevant
fields. Warnings such as `higher_cost_no_accuracy_gain` and
`higher_tokens_lower_accuracy` flag cases where extra effort spends more tokens
or cost without an accuracy improvement.

## Build Benchmark Reports

Use `build-report` for the table-and-chart view of a completed comparison:

```bash
.venv/bin/obviousbench build-report \
  --comparison-dir results/summaries/expanded-model-sweep-20260531-0028 \
  --out docs/reports/2026-05-31-expanded-model-sweep \
  --generated-on 2026-05-31 \
  --title "ObviousBench Expanded Model Sweep"
```

Outputs:

```text
docs/reports/2026-05-31-expanded-model-sweep/report.html
docs/reports/2026-05-31-expanded-model-sweep/leaderboard.csv
docs/reports/2026-05-31-expanded-model-sweep/leaderboard.md
docs/reports/2026-05-31-expanded-model-sweep/family-heatmap.csv
```

The report follows a few benchmark-reporting conventions:

- Show aggregate accuracy alongside cost, tokens, cost per correct answer, and
  overthinking index.
- Show confidence intervals beside accuracy so close rankings are not
  over-interpreted.
- Preserve family slices so aggregate scores cannot hide brittle categories.
- Keep provider errors and pricing warnings visible in the same report.
- Rank only comparable sample cohorts; shorter smoke/free runs are shown but
  marked `n/a` for rank when the main panel used more scored samples.

## Barrage Profiles

The default profile family is `balanced_XxY`, for example `balanced_8x10`. It
selects `X` eligible families and `Y` samples per family, round-robinning across
subfamilies to keep broad coverage.

Use `hard_obvious_XxY` when the goal is model separation rather than broad
coverage. It keeps the same family balance but selects from the subfamilies that
have been most failure-prone in sweep results:

```bash
.venv/bin/obviousbench make-barrage \
  --profile hard_obvious_8x10 \
  --split public_v0 \
  --seed 20260531 \
  --out data/barrages/hard_obvious_8x10_seed_20260531.jsonl
```

Current hard-obvious priorities are:

- `character_count`: single-letter counts.
- `spelling_transform`: remove-letter, replace-letter, reverse-word.
- `constraint_awareness`: object-must-be-present tasks.
- `arithmetic`: numeric comparison, unit conversion, small arithmetic.
- `format_compliance`: exact JSON, JSON field, instruction conflict.
- `negation`: without-constraint, not-choice.
- `ordering`: numeric sort before alphabetical sort.
- `word_count`: comma-list counts before sentence word counts.

## Build Shareable Artifacts

Use this when you want a tracked external-facing bundle from ignored local
summary outputs:

```bash
.venv/bin/obviousbench build-shareable \
  --comparison-dir results/summaries/model-comparison-balanced-8x10-nothinking-20260530-2136 \
  --out docs/shareable/2026-05-31-obviousbench-proof-point \
  --generated-on 2026-05-31
```

Outputs:

```text
docs/shareable/2026-05-31-obviousbench-proof-point/README.md
docs/shareable/2026-05-31-obviousbench-proof-point/benchmark-card.md
docs/shareable/2026-05-31-obviousbench-proof-point/failure-gallery.md
docs/shareable/2026-05-31-obviousbench-proof-point/model-comparison.csv
docs/shareable/2026-05-31-obviousbench-proof-point/family-comparison.csv
docs/shareable/2026-05-31-obviousbench-proof-point/model-matrix.yaml
```

The shareable builder copies compact summaries and curated failure examples. It
does not promote raw Inspect logs, raw provider requests, credentials, or local
cache files.

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
INSPECT_CACHE_DIR=.cache/inspect \
.venv/bin/inspect eval obviousbench/tasks/barrage.py \
  --model <provider/model> \
  --cache 10Y \
  --log-dir results/raw \
  -T profile=balanced_8x10 \
  -T seed=20260531
```

Run a materialized barrage:

```bash
INSPECT_CACHE_DIR=.cache/inspect \
.venv/bin/inspect eval obviousbench/tasks/barrage.py \
  --model <provider/model> \
  --cache 10Y \
  --log-dir results/raw \
  -T dataset=data/barrages/balanced_8x10_seed_20260531.jsonl
```

Inspect's cache key includes model/base URL, prompt message history, epoch,
generate config, tools, and tool choice. That is the desired developer loop:
when one or two questions are added, unchanged calls are reused, but upgraded
scorers and summaries still run over the cached raw completions. Avoid semantic
or similarity caches for benchmark runs.

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
.venv/bin/python scripts/validate_dataset.py data/public_v0/*.jsonl --item-cards-dir data/item_cards --allow-extra-item-cards
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
- Expand beyond the current small comparison panel when a broader claim is needed.
- Manually inspect real model failures for scorer false positives and false negatives.
- Decide when a promoted proof-point bundle should become a versioned release artifact.
