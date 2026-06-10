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

To include the current draft item-card layer in validation:

```bash
.venv/bin/python scripts/validate_dataset.py \
  data/public_v0/*.jsonl \
  --item-cards-dir data/item_cards \
  --allow-extra-item-cards
```

The current `public_v0` snapshot has 401 items across 8 task families, including
399 generated variants, 2 public archetype items, and 3 items with metamorphic
group metadata. Its item cards are generated draft review scaffolding, not a
claim that every public seed item has been human-reviewed for trusted benchmark
release.

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
plus a `cost_ledger.json` artifact. The Node bridge supports Node 20 and newer.
Run `npm install` before summarizing in a fresh checkout:

```bash
npm install
.venv/bin/obviousbench summarize \
  --logs results/raw \
  --out results/summaries
```

Use `--cost none` to skip pricing.

Use `rescore` when scorer logic changes and you want to re-evaluate existing
raw model completions without making new provider calls:

```bash
.venv/bin/obviousbench rescore \
  --logs results/raw/<run-dir> \
  --out results/summaries/<run-dir>-rescored
```

`summary.csv` and all usage rollups include three score views:

- `answer_accuracy`: whether the answer content is correct.
- `format_accuracy`: whether the response obeyed the expected output format.
- `strict_accuracy`: answer and format both correct.

Summaries also include Wilson 95% confidence intervals for accuracy-like
metrics. Provider errors and timeouts remain visible in sample counts, but
accuracy denominators use scored samples so infrastructure failures do not get
reported as wrong model answers.

Aggregate per-run summaries into comparison inputs for reports:

```bash
.venv/bin/obviousbench build-comparison \
  --manifest results/summaries/hard-obvious-panel-20260531/manifest.csv \
  --out results/summaries/hard-obvious-panel-20260531
```

## Build A Benchmark Report

Turn a comparison directory into a static HTML report with leaderboard tables,
cost-efficiency columns, provider-error caveats, and inline SVG charts:

```bash
.venv/bin/obviousbench build-report \
  --comparison-dir results/summaries/expanded-model-sweep-20260531-0028 \
  --out docs/reports/2026-05-31-expanded-model-sweep \
  --generated-on 2026-05-31 \
  --title "ObviousBench Expanded Model Sweep"
```

The report assigns ranks only within the largest scored sample cohort so short
smoke/free-model runs stay visible without being ranked against full runs.

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
  --cache 10Y \
  --log-dir results/raw \
  -T profile=balanced_8x10 \
  -T seed=20260531
```

For local development, prefer the generic runner. It keeps Inspect's response
cache in the repo-local ignored cache directory, uses a 10-year cache expiry by
default, and still reruns parsing, scoring, and summaries:

```bash
.venv/bin/python scripts/run_inspect_eval.py \
  --task obviousbench/tasks/barrage.py \
  --model <provider/model> \
  --log-dir results/raw \
  -T profile=hard_obvious_8x10 \
  -T seed=20260531 \
  --inspect-arg=--no-log-model-api
```

Use `--no-cache` for fresh published sweeps where current provider behavior
matters more than iteration speed. The cache stores model generations, not
parsed scores.

For a more discriminative stress run, use the hard-obvious profile. It keeps the
same `XxY` shape but prioritizes subfamilies that separated models in the
expanded sweeps, such as character counting, remove-letter transforms, object
presence, numeric comparison, and JSON/fenced-output handling:

```bash
.venv/bin/obviousbench make-barrage \
  --profile hard_obvious_8x10 \
  --seed 20260531 \
  --out data/barrages/hard_obvious_8x10_seed_20260531.jsonl
```

Any positive `XxY` shape is valid when enough public items exist, for example
`hard_obvious_8x5` for a faster 40-sample pass.

## Runbook

For a fuller local workflow, including the Keychain-backed OpenAI smoke command,
see [docs/runbook.md](docs/runbook.md).

## Release Evidence Bundle

The v0.1 release-prep config generates a machine-readable snapshot registry,
claim ledger, internal review artifacts, and SVG charts:

```bash
.venv/bin/python scripts/build_release_assets.py --config configs/release_v0_1_0.yaml
.venv/bin/python scripts/audit_release_snapshot.py --config configs/release_v0_1_0.yaml --strict
```

The reader-facing entrypoint is [docs/evidence-and-claims.md](docs/evidence-and-claims.md).
Internal review artifacts are written under `docs/internal/`; they should not
be copied into public release surfaces.

## Current Dataset Reality

The current public v0 dataset is generated seed data inspired by source
archetypes. It is not yet a fully mined, item-by-item corpus of public online
examples.

## V0 Non-Goals

ObviousBench v0.1 does not include a hosted leaderboard, web dashboard, user accounts, Hugging Face hosting, OpenAI Evals adapter, LLM-as-judge scoring, tool-use evals, RAG evals, long-context evals, or multi-turn agent tasks.
