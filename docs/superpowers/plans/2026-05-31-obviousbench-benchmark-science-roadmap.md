---
title: ObviousBench Benchmark Science Roadmap
date: 2026-05-31
type: plan
status: implemented
---

# ObviousBench Benchmark Science Roadmap

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Sequence the agreed benchmark-quality improvements so they compound cleanly and preserve ObviousBench's simplicity.

**Architecture:** Implement credibility infrastructure first, reporting improvements second, and diagnostic expansion third. Keep object presence out of this batch until the separate item-quality work lands.

**Tech Stack:** Existing ObviousBench Python package, Inspect AI logs, deterministic scorers, CSV/Markdown/HTML artifacts.

---

## Included Plans

1. [Item Cards V1](2026-05-31-item-cards-v1.md)
2. [Scorer Gold V1](2026-05-31-scorer-gold-v1.md)
3. [Report Confidence Intervals V0](2026-05-31-report-ci-v0.md)
4. [Split Strategy V1](2026-05-31-split-strategy-v1.md)
5. [Metamorphic Variants V1](2026-05-31-metamorphic-variants-v1.md)
6. [Efficiency And Overthinking V1](2026-05-31-efficiency-overthinking-v1.md)

## Recommended Implementation Order

### Phase 1: Trust The Data And Scorers

- [x] Implement `item-cards-v1`.
- [x] Implement `scorer-gold-v1`.
- [x] Run full validation:

```bash
.venv/bin/python -m pytest tests -q
.venv/bin/python -m ruff check .
.venv/bin/python scripts/validate_dataset.py data/public_v0/*.jsonl data/calibration_v0/smoke_test.jsonl
git diff --check
```

Reason: new categories and panels should not expand until provenance and scorer behavior are auditable.

### Phase 2: Trust The Numbers

- [x] Implement `report-ci-v0`.
- [x] Implement `efficiency-overthinking-v1`.
- [x] Rebuild known comparison reports from cached/local summaries.

Reason: once scorer results are trustworthy, reports should show uncertainty, cost, token burden, and effort tradeoffs.

### Phase 3: Improve Diagnostic Power

- [x] Implement `metamorphic-variants-v1`.
- [x] Add a small seed set of grouped variants only after item cards exist.
- [x] Keep object presence out of this phase until the separate object-presence category work is ready.

Reason: paired variants are most useful when their provenance and intended relation are explicit.

### Parked Track: Split Strategy

- [x] Keep `split-strategy-v1` as a policy document for now.
- [x] Do not create `public_v1`, `private_v1`, `live_vYYYY_MM`, or `canary_v1` until the user resumes split work.

Reason: better splits are important, but premature split migration would distract from the current scorer/reporting foundation.

## Simplicity Guardrails

- No database.
- No LLM judge for primary scoring.
- No pandas/SciPy requirement for v1.
- No benchmark server.
- No max-token caps introduced by reporting work.
- No private/canary data promoted into shareable artifacts.
- No object-presence category changes in this batch.

## Cross-Plan Acceptance Criteria

- Existing `public_v0` eval and summarize workflows still run.
- `obviousbench summarize` defaults remain compatible with cached Inspect logs.
- Scorer behavior changes are protected by gold fixtures.
- Reports show confidence, paired deltas, token burden, and cost burden.
- Metamorphic groups are opt-in metadata, not a requirement for every item.
- The split policy is documented but not activated.

## Final Verification Gate

Run these after all non-parked plans are implemented:

```bash
.venv/bin/python -m pytest tests -q
.venv/bin/python -m ruff check .
.venv/bin/python -m compileall -q obviousbench
.venv/bin/python scripts/validate_dataset.py data/public_v0/*.jsonl data/calibration_v0/smoke_test.jsonl
.venv/bin/python -m obviousbench.cli summarize --logs results/evals/mock-smoke --out /tmp/obviousbench-summary-smoke --cost none
git diff --check
```

If the mock-smoke path does not exist locally, replace it with a fresh mock run:

```bash
inspect eval obviousbench/tasks/smoke.py --model mockllm/model --log-dir /tmp/obviousbench-mock-smoke --limit 3 --no-log-realtime
.venv/bin/python -m obviousbench.cli summarize --logs /tmp/obviousbench-mock-smoke --out /tmp/obviousbench-summary-smoke --cost none
```
