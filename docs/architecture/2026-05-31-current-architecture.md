---
title: Current ObviousBench Architecture
date: 2026-05-31
type: architecture
status: current
---

# Current ObviousBench Architecture

This document describes the current local architecture. The archived
`obviousbench_build_plan.md` remains historical planning context and should not
be treated as the implementation contract.

## Purpose

ObviousBench is a local Inspect AI benchmark package for short, human-trivial
model reliability checks. It is optimized for deterministic scoring,
auditable datasets, reproducible local runs, and compact shareable artifacts.

The current system is not a hosted leaderboard, dataset service, web dashboard,
LLM-judge framework, tool-use benchmark, RAG benchmark, or long-context eval.

## Runtime Data Flow

```text
JSONL benchmark rows
  -> Pydantic dataset validation
  -> Inspect task wrappers
  -> native provider generation
  -> deterministic Python scoring
  -> Inspect eval logs
  -> local summaries, comparisons, reports, and shareable bundles
```

Raw provider logs and caches stay under ignored local result/cache directories.
Tracked docs and shareable bundles should contain compact metrics and curated
examples only.

## Core Boundaries

- `data/public_v0/*.jsonl`: current public seed dataset. It is generated
  proof-point data, not held-out leaderboard evidence.
- `data/calibration_v0/smoke_test.jsonl`: small local smoke dataset for runner
  and scoring plumbing.
- `data/item_cards/**/*.yaml`: draft provenance and review scaffolding. Item
  cards are validation evidence, not runtime scoring logic.
- `obviousbench/datasets/`: schemas, loading, validation, and item-card checks.
- `obviousbench/tasks/`: Inspect task entrypoints and task factories.
- `obviousbench/scorers/`: deterministic scorer implementations and scorer
  registry behavior.
- `obviousbench/analysis/`: log parsing, rescoring, metrics, usage rollups,
  cost integration, comparisons, confidence intervals, metamorphic consistency,
  static reports, and shareable artifact generation.
- `obviousbench/runners/`: local wrappers around Inspect for repo cache defaults
  and provider-refusal retry handling.
- `scripts/`: thin command wrappers and dataset/card generation helpers.
- `docs/reports/**`: generated report outputs. Regenerate these from comparison
  directories rather than hand-editing them.
- `docs/shareable/**`: curated external-facing bundles generated from selected
  comparison outputs.

## Dataset Contract

Every benchmark item is a JSONL object validated by
`obviousbench.datasets.schemas.BenchmarkItem`. Required fields include stable
ID, family, subfamily, prompt, question, target, answer type, scorer, split,
source refs, human-triviality label, review status, and metadata.

`public_v0` currently contains 401 items across eight families. It includes
399 generated variants, two public archetype items, and a small metamorphic
seed group. Public seed results must be described as proof-point evidence
unless a future trusted split with reviewed item cards is explicitly used.

Item-card validation is optional for the current seed split unless
`--require-item-cards` is passed. Trusted future splits should require reviewed
cards and should fail on missing, draft, mismatched, or extra cards unless the
caller explicitly allows extras for migration work.

## Execution Model

Inspect AI owns model execution. ObviousBench task modules load local JSONL,
convert rows to Inspect samples, call `generate()`, and attach deterministic
scorers through dynamic metadata.

The prompt policy is intentionally narrow:

- native provider mode
- no explicit system prompt
- one user message where possible
- deterministic or nearest-provider deterministic settings
- no tool calls, browsing, or chain-of-thought request

Local runner wrappers add cache defaults and retry provider safety/error text
that arrives as assistant output. Those retries bypass the Inspect cache so a
cached refusal is not replayed.

## Scoring And Metrics

Scoring is deterministic Python code. No model output is scored by another LLM.
Scorer behavior is locked by focused scorer tests and YAML gold fixtures.

Summaries distinguish:

- `answer_accuracy`: answer content is correct.
- `format_accuracy`: required output format is followed.
- `strict_accuracy`: answer and format are both correct.

Provider errors and timeouts remain visible in totals. After configured retries,
final provider errors and timeouts count as incorrect attempts in
`scored_samples`, so a model cannot improve its headline accuracy by refusing or
failing an item. Reports include Wilson 95% intervals for accuracy-like metrics
and paired deltas when matched per-sample rows are available.

Efficiency metrics such as tokens per correct answer, cost per correct answer,
reasoning token share, and overthinking index are diagnostics. They should not
replace accuracy or strict correctness as the primary benchmark result.

## Generated Artifacts

`obviousbench summarize` writes run summaries, failure galleries, usage rollups,
optional cost ledgers, and metamorphic consistency outputs when group metadata
is present.

`obviousbench build-comparison` aggregates run summaries into model, family,
section, effort-curve, metamorphic, and delta CSVs.

`obviousbench build-report` produces static HTML/CSV/Markdown report artifacts
from a comparison directory. Treat `docs/reports/**` as generated.

`obviousbench build-shareable` promotes selected comparison outputs into a
tracked external-facing bundle without raw Inspect logs, provider payloads,
credentials, or local filesystem paths.

## Validation Gates

Use these before treating docs or generated artifacts as current:

```bash
.venv/bin/python scripts/validate_dataset.py data/public_v0/*.jsonl data/calibration_v0/smoke_test.jsonl
.venv/bin/python scripts/validate_dataset.py data/public_v0/*.jsonl --item-cards-dir data/item_cards --allow-extra-item-cards
.venv/bin/python -m pytest tests -q
.venv/bin/python -m ruff check .
.venv/bin/python -m compileall -q obviousbench
git diff --check
```

For external bundles, also scan promoted files for secrets, raw provider logs,
local filesystem paths, and private source material before sharing.

## Current Limitations

- `public_v0` is transparent seed data and can be inspected or copied.
- Many item cards are draft stubs and need human review before trusted-split
  claims.
- Current report outputs are local snapshots, not a hosted benchmark service.
- Provider pricing and model aliases can drift; current claims should name the
  exact run date, comparison directory, model string, and split.
- Historical status files are point-in-time records and can be superseded by
  later rescoring or report generation.
