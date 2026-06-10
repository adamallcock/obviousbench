---
title: Effort Cost Curves V1 Implementation Plan
date: 2026-06-02
type: plan
status: draft
---

# Effort Cost Curves V1 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add publication-ready effort-level curves with run cost on the x axis and ObviousBench answer accuracy on the y axis.

**Architecture:** Reuse the existing comparison output and static report generator. Strengthen `effort_curve.csv` so explicit provider effort settings are captured for Anthropic and OpenAI, then render a small SVG curve chart from that artifact instead of introducing a separate plotting stack.

**Tech Stack:** Python CSV processing, existing `obviousbench analysis` modules, static HTML/SVG in `obviousbench/analysis/benchmark_report.py`, pytest.

---

## Decision

This is worth testing. The current 2026-06-02 combined overline run already contains enough signal to justify a first chart:

- OpenAI families show the expected cost/performance frontier: higher effort often raises accuracy until saturation, then mostly raises cost.
- Anthropic families show a different pattern on this obvious-task set: Claude Opus 4.8 low through xhigh are tied near 92.5 percent answer accuracy, while max is more expensive and worse on this run.
- The chart answers a paper-useful question: on obvious tasks, when does extra reasoning spend buy capability, and when does it become overthinking?

Primary-source facts checked on 2026-06-02:

- Anthropic lists Claude Opus 4.8 as the most capable current model for complex reasoning and agentic coding, with `effort` available on Opus 4.8, Opus 4.7, Opus 4.6, Sonnet 4.6, and Opus 4.5. Source: https://platform.claude.com/docs/en/about-claude/models/overview and https://platform.claude.com/docs/en/build-with-claude/effort
- Anthropic documents effort levels `low`, `medium`, `high`, `xhigh`, and `max`, with `high` as default and effort as a behavioral signal rather than a strict token budget. Source: https://platform.claude.com/docs/en/build-with-claude/effort
- OpenAI lists GPT-5.5 as the current frontier model and documents `reasoning.effort` values `none`, `low`, `medium`, `high`, and `xhigh`. Source: https://developers.openai.com/api/docs/models/gpt-5.5/
- OpenAI pricing bills reasoning tokens as output tokens. Source: https://platform.openai.com/docs/pricing/

## Existing Evidence From The Current Report

Source comparison:

- `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/comparison/comparison.csv`
- Current published report: `docs/reports/2026-06-02-paper-v1-combined-234-overline/report.html`

Observed curve candidates:

| Model | Best low-cost point | Higher-effort observation |
|---|---:|---|
| `anthropic/claude-opus-4-8` | low: 92.5%, $0.033340 | max: 91.25%, $0.039630 |
| `anthropic/claude-sonnet-4-6` | low: 91.25%, $0.018060 | max: 87.50%, $0.019860 |
| `openai/gpt-5.5` | none: 91.25%, $0.030905 | low reaches 100%; xhigh remains 100% at higher cost |
| `openai/gpt-5.4` | no thinking: 90.0%, $0.016200 | xhigh: 98.75%, $0.100038 |
| `openai/gpt-5.4-nano` | no thinking: 80.0%, $0.001312 | high reaches 100%; xhigh drops to 98.75% |

Note: the numeric table above is a quick candidate read, not the final paper table. The implementation should compute display text directly from CSV values to avoid transcription mistakes.

## Non-Goals

- Do not run a broad new panel before rendering existing curves.
- Do not add a JavaScript charting dependency.
- Do not compare Anthropic effort as if it were a strict token budget; label it as provider adaptive effort.
- Do not treat reported reasoning tokens as the configured effort setting.

## File Structure

- Modify `obviousbench/analysis/effort_curves.py`: derive explicit effort levels from summary rows robustly enough for current Anthropic/OpenAI labels.
- Modify `tests/analysis/test_effort_curves.py`: pin effort ordering and label inference.
- Modify `obviousbench/analysis/benchmark_report.py`: add the effort-cost SVG section.
- Modify `tests/analysis/test_benchmark_report.py`: assert the new section, SVG classes, axis labels, and omission behavior.
- Regenerate `docs/reports/2026-06-02-paper-v1-combined-234-overline/report.html` after tests pass.

## Task 1: Capture Explicit Effort Levels

**Files:**
- Modify: `obviousbench/analysis/effort_curves.py`
- Test: `tests/analysis/test_effort_curves.py`

- [ ] **Step 1: Write failing effort extraction tests**

Add tests that cover direct settings and current Anthropic labels:

```python
from obviousbench.analysis.effort_curves import build_effort_curve_rows


def test_effort_curve_infers_anthropic_effort_from_label():
    rows = [
        {
            "label": "Claude Opus 4.8 low",
            "model": "anthropic/claude-opus-4-8",
            "barrage_profile": "hard_obvious_8x10",
            "accuracy": "0.925",
            "strict_accuracy": "0.925",
            "total_tokens": "501",
            "reasoning_tokens": "0",
            "estimated_cost_usd": "0.033",
        },
        {
            "label": "Claude Opus 4.8 max",
            "model": "anthropic/claude-opus-4-8",
            "barrage_profile": "hard_obvious_8x10",
            "accuracy": "0.900",
            "strict_accuracy": "0.850",
            "total_tokens": "600",
            "reasoning_tokens": "0",
            "estimated_cost_usd": "0.040",
        },
    ]

    effort_rows = build_effort_curve_rows(rows)

    assert [row["reasoning_effort"] for row in effort_rows] == ["low", "max"]
    assert [row["effort_order"] for row in effort_rows] == ["1", "5"]
```

- [ ] **Step 2: Verify the test fails**

Run:

```bash
.venv/bin/python -m pytest tests/analysis/test_effort_curves.py -q
```

Expected: FAIL because Anthropic labels are currently emitted with blank effort and order `99`.

- [ ] **Step 3: Implement explicit effort extraction**

Update `effort_curves.py` with:

```python
_EFFORT_ORDER = {
    "none": 0,
    "minimal": 0,
    "low": 1,
    "medium": 2,
    "high": 3,
    "xhigh": 4,
    "max": 5,
}

_EFFORT_LABEL_RE = re.compile(
    r"\b(none|minimal|low|medium|high|xhigh|max)\b", re.IGNORECASE
)


def _explicit_effort(row: dict[str, str]) -> str:
    effort = row.get("reasoning_effort", "").strip().lower()
    if effort:
        return effort
    label = row.get("label", "").strip().lower()
    model = row.get("model", "")
    if model.startswith(("anthropic/", "openai/")):
        match = _EFFORT_LABEL_RE.search(label)
        if match:
            return match.group(1).lower()
    return ""
```

Then call `_explicit_effort(row)` wherever `row.get("reasoning_effort", "")` is currently used by the effort curve builder.

- [ ] **Step 4: Run effort curve tests**

Run:

```bash
.venv/bin/python -m pytest tests/analysis/test_effort_curves.py -q
```

Expected: PASS.

## Task 2: Render Cost-X-Axis Effort Curves

**Files:**
- Modify: `obviousbench/analysis/benchmark_report.py`
- Test: `tests/analysis/test_benchmark_report.py`

- [ ] **Step 1: Add failing report test assertions**

Extend the existing benchmark report test fixture so `effort_curve.csv` has at least two rows for one model base, then assert:

```python
assert "Effort Curves: Accuracy vs Run Cost" in html
assert "effort-curve-line" in html
assert "effort-curve-point" in html
assert "Estimated total run cost, USD" in html
assert "Answer accuracy (%)" in html
```

- [ ] **Step 2: Verify the test fails**

Run:

```bash
.venv/bin/python -m pytest tests/analysis/test_benchmark_report.py -q
```

Expected: FAIL because no effort-curve chart section exists.

- [ ] **Step 3: Add `_effort_curve_svg`**

Implement a helper that:

- reads rows from `effort_curve.csv`,
- keeps only groups with at least two distinct nonblank effort levels and nonblank `estimated_cost_usd`,
- uses `estimated_cost_usd` as x,
- uses `accuracy` as y,
- draws one polyline per `model_base`,
- labels each point by `reasoning_effort`,
- omits non-costed or single-effort groups with a short note.

Use existing SVG primitives where practical:

```python
def _effort_curve_svg(rows: list[dict[str, str]]) -> str:
    grouped = _effort_curve_groups(rows)
    if not grouped:
        return "<p>No multi-effort costed runs available.</p>"
    # Render static SVG using the same margins, gridline, tick-label,
    # axis-label, and point-label class conventions as _scatter_plot_svg.
```

- [ ] **Step 4: Insert the report section**

Add the section after the global cost scatter:

```python
"<h2>Effort Curves: Accuracy vs Run Cost</h2>",
_effort_curve_svg(effort_rows),
_effort_curve_note(effort_rows),
```

- [ ] **Step 5: Run report tests**

Run:

```bash
.venv/bin/python -m pytest tests/analysis/test_benchmark_report.py -q
```

Expected: PASS.

## Task 3: Regenerate And Inspect The Current Report

**Files:**
- Modify generated artifact: `docs/reports/2026-06-02-paper-v1-combined-234-overline/report.html`

- [ ] **Step 1: Regenerate comparison if effort extraction changed**

Run:

```bash
.venv/bin/obviousbench compare \
  --manifest configs/paper_v1_combined_234_overline_attempt_scored_20260602_manifest.csv \
  --out results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/comparison
```

Expected: `effort_curve.csv` now contains nonblank Anthropic effort values for the Claude Opus 4.8 and Sonnet 4.6 rows.

- [ ] **Step 2: Regenerate the report**

Run:

```bash
.venv/bin/obviousbench build-report \
  --comparison-dir results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/comparison \
  --out docs/reports/2026-06-02-paper-v1-combined-234-overline \
  --generated-on 2026-06-02 \
  --title "Paper V1 Combined 234 Overline"
```

Expected: `report.html`, `leaderboard.csv`, `leaderboard.md`, and `family-heatmap.csv` regenerate.

- [ ] **Step 3: Inspect rendered HTML without relying on file URL browser support**

Run:

```bash
rg -n "Effort Curves|effort-curve-line|Claude Opus 4.8|OpenAI GPT-5.5" docs/reports/2026-06-02-paper-v1-combined-234-overline/report.html
```

Expected: the new chart section and both provider curve labels are present.

## Task 4: Decide Whether To Spend More Benchmark Money

**Files:**
- Create if needed: `docs/research/2026-06-02-effort-cost-curves-run-summary.md`

- [ ] **Step 1: Write a short curve-read summary**

Summarize which provider families already have sufficient curve coverage and which do not.

- [ ] **Step 2: Only run missing slices**

If current data is missing clean curves, prefer this order:

1. Anthropic: Claude Opus 4.8 `low`, `medium`, `high`, `xhigh`, `max`.
2. OpenAI: GPT-5.5 `none`, `low`, `medium`, `high`, `xhigh`.
3. OpenAI cheap frontier: GPT-5.4 nano `none`, `low`, `medium`, `high`, `xhigh`.
4. Gemini/OpenRouter only after labels and request settings are verified against the thinking-controls note.

- [ ] **Step 3: Respect benchmark wait windows**

- Estimate the run cost from existing usage before launching.
- After launch, confirm logs are writing once, then wait until the expected completion boundary before checking completion.
- Do not poll frequently.

## Acceptance Criteria

- The generated report contains an effort-curve section with cost on the x axis and answer accuracy on the y axis.
- Anthropic and OpenAI explicit effort rows are represented as curves, not just isolated leaderboard points.
- The chart labels provider controls accurately: OpenAI `reasoning.effort`, Anthropic adaptive/provider effort.
- Existing leaderboard, global cost scatter, tokens scatter, heatmap, and metamorphic sections still render.
- Tests pass:

```bash
.venv/bin/python -m pytest tests/analysis/test_effort_curves.py tests/analysis/test_benchmark_report.py -q
```
