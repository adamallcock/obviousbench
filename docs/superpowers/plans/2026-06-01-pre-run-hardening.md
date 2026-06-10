---
title: Pre-Run Hardening
date: 2026-06-01
type: plan
status: complete
---

# Pre-Run Hardening Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Prepare ObviousBench for large manifest-driven benchmark runs without hand-running model commands or relying on stale readiness docs.

**Architecture:** Add a resumable run executor that reads model-panel YAML entries and executes smoke or full runs one entry at a time. Keep final-run policy in generated docs and make preprint-vs-strict readiness gates explicit so the benchmark can scale from the current paper panel to hundreds of model/config rows.

**Tech Stack:** Python stdlib, existing Inspect runner wrapper, existing `obviousbench rescore`, YAML model-panel configs, pytest, ruff, generated Markdown docs.

---

## Task 1: Resumable Model-Panel Executor

Status: complete.

**Files:**

- Create: `obviousbench/research/model_panel_runner.py`
- Create: `scripts/run_model_panel.py`
- Test: `tests/research/test_model_panel_runner.py`
- Modify: `obviousbench/cli.py` only if a first-class CLI command is required after the script proves useful.

Acceptance:

- Supports `--mode smoke` and `--mode full`.
- Supports `--limit`, `--only`, `--skip-completed`, `--dry-run`, `--sample-id`, `--manifest-out`, `--status-out`.
- Uses `obviousbench.runners.inspect_eval` for provider execution.
- Uses `obviousbench.cli rescore` for summaries.
- Writes a JSONL status ledger after every entry.
- Returns non-zero when any selected entry fails.

## Task 2: Exact Smoke Gate

Status: complete; blocked by missing provider credentials rather than runner
logic.

**Files:**

- Create: `docs/research/2026-06-01-paper-v1-smoke-status.md`
- Modify: `docs/research/2026-06-01-paper-v1-final-sweep-plan.md` after smoke state is known.

Acceptance:

- Smoke status is based on exact `inspect_model`, generation settings, dataset, and output contract.
- Previously similar runs are listed as prior evidence, not final smoke pass evidence.
- Missing or blocked entries are explicit.

## Task 3: Model Coverage Refresh

Status: complete; broad-panel expansion decisions remain intentionally
deferred until the next model-selection pass.

**Files:**

- Create: `docs/research/2026-06-01-model-coverage-refresh.md`
- Optionally modify: `configs/model_thinking_settings_v1.yaml` after an explicit selection decision.

Acceptance:

- Compares local direct-provider and OpenRouter configs against live catalog evidence.
- Separates “missing because unavailable”, “missing because expensive/duplicative”, and “missing because registry/pricing needs refresh”.
- Records whether local `runcost` package metadata is current enough for the intended run.

## Task 4: Align State Docs

Status: complete.

**Files:**

- Modify: `docs/research/2026-06-01-paper-v1-model-panel.md`
- Modify: `configs/paper_v1_model_panel.yaml`
- Modify: `configs/paper_v1_analysis_plan.yaml`
- Regenerate: `docs/research/2026-06-01-obviousbench-paper-analysis-plan.md`

Acceptance:

- Fast-preprint path does not require human response rows.
- Strict benchmark path still requires human rows.
- Provider exclusions are described as an audit artifact, not a manuscript table unless re-added.

## Task 5: Freeze Run And Retry Policy

Status: complete.

**Files:**

- Create: `docs/research/2026-06-01-paper-v1-run-freeze-policy.md`
- Modify: `docs/research/2026-06-01-paper-v1-final-sweep-plan.md` if the generated plan needs a link to the policy.

Acceptance:

- States frozen dataset, item IDs, scorers, prompt template, generation settings, output roots, retry rules, exclusion rules, and rerun policy.
- Distinguishes smoke retries from final-result retries.
- Defines how to handle provider outages and model alias removals.

## Task 6: Verification

Status: complete.

**Files:**

- No new source files beyond the tasks above.

Acceptance commands:

```bash
.venv/bin/ruff check obviousbench/research/model_panel_runner.py scripts/run_model_panel.py tests/research/test_model_panel_runner.py
```

```bash
.venv/bin/python -m pytest tests/research/test_model_panel_runner.py tests/research/test_final_sweep_plan.py tests/research/test_paper_analysis_plan.py -q
```

```bash
make -C paper readiness-preprint
```

```bash
make -C paper analysis-plan sweep-plan
```
