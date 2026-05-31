# ObviousBench

ObviousBench is a lightweight reliability benchmark for public-facing AI systems. It tests short, human-trivial questions that users expect models to answer correctly every time: letter counting, spelling transforms, simple arithmetic, list counting, ordering, format compliance, negation, and simple constraint-awareness tasks.

The goal is not to prove that models are bad. The goal is to catch obvious AI mistakes before users do.

ObviousBench is built on Inspect AI, uses local JSONL datasets, runs in native provider mode with no explicit system prompt, and uses deterministic Python scorers.

## Install

```bash
python -m venv .venv
.venv/bin/python -m pip install -e ".[dev]"
```

## Validate Datasets

```bash
.venv/bin/python scripts/validate_dataset.py data/public_v0/*.jsonl data/calibration_v0/smoke_test.jsonl
```

Expected:

```text
Validation passed.
```

## Run A Smoke Eval

For a local plumbing check that does not call a real provider, use Inspect's
mock model:

```bash
.venv/bin/inspect eval obviousbench/tasks/smoke.py \
  --model mockllm/model \
  --log-dir results/raw \
  --limit 3 \
  --no-log-realtime
```

Then summarize the smoke log:

```bash
.venv/bin/obviousbench summarize \
  --logs results/raw \
  --out results/summaries \
  --cost none
```

The mock model returns default text, so the summary is expected to show model
failures while proving that task loading, scoring, logging, and reporting run
cleanly.

## Summarize Logs

```bash
.venv/bin/obviousbench summarize --logs results/raw --out results/summaries
```

The summary command emits run, sample, family, section, and question-level CSVs.
Costing with `runcost` is enabled by default and writes estimated cost columns
plus a `cost_ledger.json` artifact. Run `npm install` before summarizing in a
fresh checkout:

```bash
npm install
.venv/bin/obviousbench summarize \
  --logs results/raw \
  --out results/summaries
```

Use `--cost none` to skip pricing.

## Build Shareable Artifacts

Promote a selected comparison summary into a tracked recruiter-safe bundle:

```bash
.venv/bin/obviousbench build-shareable \
  --comparison-dir results/summaries/model-comparison-balanced-8x10-nothinking-20260530-2136 \
  --out docs/shareable/2026-05-31-obviousbench-proof-point \
  --generated-on 2026-05-31
```

The bundle contains a benchmark card, curated failure gallery, model/family CSVs,
and the exact model matrix. Raw Inspect logs stay ignored under `results/raw/`.

## Build A Balanced Barrage

Create an 80-sample barrage with 10 samples from each of the 8 families:

```bash
.venv/bin/obviousbench make-barrage \
  --profile balanced_8x10 \
  --seed 20260531 \
  --out data/barrages/balanced_8x10_seed_20260531.jsonl
```

Or run the barrage task directly:

```bash
.venv/bin/inspect eval obviousbench/tasks/barrage.py \
  --model <provider/model> \
  --log-dir results/raw \
  -T profile=balanced_8x10 \
  -T seed=20260531
```

## Runbook

For a fuller local workflow, including the Keychain-backed OpenAI smoke command,
see [docs/runbook.md](docs/runbook.md).

## Current Dataset Reality

The current public v0 dataset is generated seed data inspired by source
archetypes. It is not yet a fully mined, item-by-item corpus of public online
examples.

## V0 Non-Goals

ObviousBench v0.1 does not include a hosted leaderboard, web dashboard, user accounts, Hugging Face hosting, OpenAI Evals adapter, LLM-as-judge scoring, tool-use evals, RAG evals, long-context evals, or multi-turn agent tasks.
