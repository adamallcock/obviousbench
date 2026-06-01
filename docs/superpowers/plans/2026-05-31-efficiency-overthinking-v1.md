---
title: Efficiency And Overthinking V1 Implementation Plan
date: 2026-05-31
type: plan
status: implemented
---

# Efficiency And Overthinking V1 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make token efficiency, cost efficiency, and overthinking visible as first-class ObviousBench outcomes, especially for questions that are meant to be obvious.

**Architecture:** Add derived efficiency metrics on top of existing usage fields, write efficiency CSVs during summarization and comparison, and surface accuracy-vs-effort charts in the existing static report. Avoid a single opaque leaderboard score in v1.

**Tech Stack:** Existing Inspect usage parsing, CSV summaries, runcost integration, static HTML/SVG report builder, pytest.

---

## Implementation Status

Implemented on 2026-05-31. The shipped version includes token/cost efficiency
metrics, overthinking diagnostics, effort curves, report warnings, and usage
rollups by model, family, section, and question.

## Principles

- For obvious prompts, excessive reasoning is diagnostic even when the final answer is correct.
- Accuracy remains primary. Efficiency explains how expensive or overcomplicated that accuracy was.
- Prefer transparent derived metrics over a magic composite score.
- Keep provider differences visible: some providers may not expose reasoning tokens.

## Current Repo Touchpoints

- Usage fields already exist in `obviousbench/analysis/metrics.py`.
- Cost export already exists in `obviousbench/analysis/usage.py` and `obviousbench/analysis/costing.py`.
- Report builder already shows total tokens and cost per correct in `obviousbench/analysis/benchmark_report.py`.
- Comparison builder already carries `reasoning_effort` and `reasoning_summary`.

## Metric Contract

Add these derived metrics:

- `tokens_per_scored_sample = total_tokens / scored_samples`
- `output_tokens_per_scored_sample = output_tokens / scored_samples`
- `reasoning_tokens_per_scored_sample = reasoning_tokens / scored_samples`
- `tokens_per_correct = total_tokens / correct`
- `cost_per_correct_usd = estimated_cost_usd / correct`
- `reasoning_token_share = reasoning_tokens / total_tokens`
- `overthinking_index = reasoning_tokens / max(output_tokens, 1)`

Interpretation:

- `overthinking_index = 0` means no tracked reasoning tokens.
- Higher `overthinking_index` means hidden reasoning dominates visible answer text.
- Missing reasoning token support should be reported as `reasoning_token_share` blank or `0` with `reasoning_token_source=not_reported`, not as evidence that the model did not reason.

## Functional Requirements

- `summary.csv` includes derived efficiency fields.
- `usage_by_family.csv`, `usage_by_section.csv`, and `usage_by_question.csv` include derived efficiency fields where meaningful.
- `comparison.csv` includes the same fields for leaderboard sorting.
- `effort_curve.csv` groups runs by model and profile across `reasoning_effort` values.
- Report HTML includes an accuracy-vs-tokens chart and an accuracy-vs-cost chart.
- Report flags cases where higher reasoning effort costs more and does not improve accuracy.

## Technical Requirements

- Do not set or recommend max token caps as part of this plan.
- Do not assume every provider reports reasoning tokens.
- Keep divisions safe: blank output for unavailable cost, `0` only when a denominator exists and numerator is zero.
- Round display metrics but keep CSV values parseable as floats.

## Task 1: Add Efficiency Helper Functions

**Files:**
- Create: `obviousbench/analysis/efficiency.py`
- Test: `tests/analysis/test_efficiency.py`

- [x] **Step 1: Write helper tests**

```python
from obviousbench.analysis.efficiency import safe_ratio, tokens_per_correct


def test_safe_ratio_returns_none_for_zero_denominator():
    assert safe_ratio(10, 0) is None


def test_tokens_per_correct_uses_total_tokens_and_correct_count():
    assert tokens_per_correct(total_tokens=120, correct=3) == 40.0
```

- [x] **Step 2: Implement helper functions**

```python
def safe_ratio(numerator: float | int | None, denominator: float | int | None) -> float | None:
    if numerator is None or denominator in {None, 0}:
        return None
    return float(numerator) / float(denominator)


def tokens_per_correct(*, total_tokens: int, correct: int) -> float | None:
    return safe_ratio(total_tokens, correct)


def overthinking_index(*, reasoning_tokens: int, output_tokens: int) -> float | None:
    return safe_ratio(reasoning_tokens, max(output_tokens, 1))
```

- [x] **Step 3: Run helper tests**

Run: `.venv/bin/python -m pytest tests/analysis/test_efficiency.py -q`

Expected: PASS.

## Task 2: Add Derived Metrics To Summary Rows

**Files:**
- Modify: `obviousbench/analysis/metrics.py`
- Test: `tests/analysis/test_metrics.py`

- [x] **Step 1: Extend `SummaryRow`**

Add:

```python
tokens_per_scored_sample: float | None
output_tokens_per_scored_sample: float | None
reasoning_tokens_per_scored_sample: float | None
tokens_per_correct: float | None
cost_per_correct_usd: float | None
reasoning_token_share: float | None
overthinking_index: float | None
reasoning_token_source: str
```

- [x] **Step 2: Populate in `compute_summary`**

Use helper functions and set:

```python
reasoning_token_source = "reported" if reasoning_tokens else "not_reported_or_zero"
```

- [x] **Step 3: Test a row with correct answers and reasoning tokens**

Assert:

```python
assert row.tokens_per_correct == 50.0
assert row.reasoning_token_share == 0.6
assert row.overthinking_index == 3.0
```

- [x] **Step 4: Run metrics tests**

Run: `.venv/bin/python -m pytest tests/analysis/test_metrics.py -q`

Expected: PASS.

## Task 3: Add Efficiency Fields To Usage Breakdowns

**Files:**
- Modify: `obviousbench/analysis/usage.py`
- Test: `tests/analysis/test_usage_exports.py`

- [x] **Step 1: Extend `UsageBreakdownRow`**

Add:

```python
tokens_per_scored_sample: float | None
tokens_per_correct: float | None
cost_per_correct_usd: float | None
reasoning_token_share: float | None
overthinking_index: float | None
```

- [x] **Step 2: Add CSV columns**

Add these fields to family, section, and question exports.

- [x] **Step 3: Run usage tests**

Run: `.venv/bin/python -m pytest tests/analysis/test_usage_exports.py -q`

Expected: PASS.

## Task 4: Add Effort Curve Artifact

**Files:**
- Create: `obviousbench/analysis/effort_curves.py`
- Modify: `obviousbench/analysis/comparison.py`
- Test: `tests/analysis/test_effort_curves.py`

- [x] **Step 1: Define effort curve row**

Fields:

- `model_base`,
- `barrage_profile`,
- `reasoning_summary`,
- `effort_order`,
- `reasoning_effort`,
- `accuracy`,
- `strict_accuracy`,
- `total_tokens`,
- `reasoning_tokens`,
- `estimated_cost_usd`,
- `accuracy_delta_from_min_effort`,
- `token_delta_from_min_effort`,
- `cost_delta_from_min_effort`,
- `efficiency_warning`.

- [x] **Step 2: Implement model-base normalization**

For v1, use the full model string minus only obvious effort suffixes if those are represented in labels. Do not attempt provider-specific model alias parsing.

- [x] **Step 3: Emit warnings**

Set `efficiency_warning` to:

- `higher_cost_no_accuracy_gain` when accuracy is unchanged and cost increases,
- `higher_tokens_lower_accuracy` when total tokens increase and accuracy decreases,
- empty string otherwise.

- [x] **Step 4: Write `effort_curve.csv` from comparison builder**

Add `effort_curve` to `ComparisonBuildPaths`.

- [x] **Step 5: Run tests**

Run: `.venv/bin/python -m pytest tests/analysis/test_effort_curves.py tests/analysis/test_comparison.py -q`

Expected: PASS.

## Task 5: Surface Efficiency In Report

**Files:**
- Modify: `obviousbench/analysis/benchmark_report.py`
- Test: `tests/analysis/test_benchmark_report.py`
- Modify: `docs/runbook.md`

- [x] **Step 1: Add report assertions**

Assert report HTML includes:

```text
Accuracy vs tokens
Overthinking index
```

- [x] **Step 2: Add columns to leaderboard**

Include:

- `Tokens/correct`,
- `Cost/correct`,
- `Overthinking index`.

- [x] **Step 3: Add SVG scatter**

Plot x-axis `tokens_per_correct`, y-axis `accuracy`. Continue to show the existing cost scatter.

- [x] **Step 4: Add runbook notes**

Explain:

- reasoning tokens may be missing by provider,
- efficiency metrics are secondary,
- high accuracy with very high token spend is still a meaningful product tradeoff.

## Acceptance Criteria

- Efficiency metrics are present in summary, usage, comparison, and report artifacts.
- Reasoning-token missingness is explicit.
- Reports identify effort settings that cost more without improving accuracy.
- No max-token caps are introduced.
- Accuracy remains the primary ranking metric unless a future decision changes that policy.

## Verification Commands

```bash
.venv/bin/python -m pytest tests/analysis/test_efficiency.py tests/analysis/test_effort_curves.py tests/analysis/test_metrics.py tests/analysis/test_usage_exports.py tests/analysis/test_benchmark_report.py -q
.venv/bin/python -m ruff check obviousbench tests
git diff --check
```
