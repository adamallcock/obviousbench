---
title: Metamorphic Variants V1 Implementation Plan
date: 2026-05-31
type: plan
status: implemented
---

# Metamorphic Variants V1 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add paired and metamorphic variant tracking so ObviousBench can measure whether models answer equivalent or trivially transformed prompts consistently.

**Architecture:** Store metamorphic group metadata on benchmark items, compute group-level consistency from existing per-sample summaries, and add panel-builder constraints so balanced barrages can include or avoid sibling variants intentionally.

**Tech Stack:** Existing JSONL metadata, Pydantic schema additions, CSV analysis modules, pytest.

---

## Implementation Status

Implemented on 2026-05-31. The shipped version includes optional metamorphic
metadata, validation, per-sample exports, group consistency summaries, report
surfacing, barrage sibling caps, and a small strawberry spelling-transform seed
group in `public_v0`.

## Principles

- Metamorphic testing should diagnose inconsistency, not inflate sample count with near-duplicates.
- Equivalent questions should preserve the same answer. Contrastive questions should declare the expected answer change.
- Group metadata must be explicit and inspectable.
- The default balanced barrage should avoid too many siblings from one group; stress profiles may include them deliberately.

## Current Repo Touchpoints

- Dataset schema: `obviousbench/datasets/schemas.py`
- Barrage builder: `obviousbench/barrage.py`
- Per-sample export: `obviousbench/analysis/usage.py`
- Comparison builder: `obviousbench/analysis/comparison.py`
- Report builder: `obviousbench/analysis/benchmark_report.py`
- Current hard selection: `HARD_SUBFAMILY_ORDER` in `obviousbench/barrage.py`

## Proposed Metadata Contract

Add optional fields to `BenchmarkMetadata`:

```python
metamorphic_group_id: str | None = None
metamorphic_role: str | None = None
metamorphic_relation: str | None = None
metamorphic_expected_behavior: str | None = None
```

Recommended values:

- `metamorphic_role`: `base`, `paraphrase`, `choice_order_swap`, `irrelevant_detail_change`, `negation_inversion`, `count_vs_list`, `format_shift`, `contrast_control`
- `metamorphic_relation`: `equivalent`, `answer_changes`, `format_changes_only`
- `metamorphic_expected_behavior`: human sentence explaining the relation.

Example:

```json
{
  "metadata": {
    "metamorphic_group_id": "object_presence.car_wash.drive_or_walk.001",
    "metamorphic_role": "irrelevant_detail_change",
    "metamorphic_relation": "equivalent",
    "metamorphic_expected_behavior": "Changing 100m to next door should not change that the car must be brought."
  }
}
```

## Functional Requirements

- Dataset validation accepts optional metamorphic fields and fails when only some required group fields are present.
- Per-sample exports include `metamorphic_group_id`, `metamorphic_role`, and `metamorphic_relation`.
- Analysis writes `metamorphic_consistency.csv` per summary directory.
- Comparison reports can aggregate group consistency by model and family.
- Barrage builder supports `--max-metamorphic-siblings-per-group`, default `1`, for normal balanced profiles.
- A future stress profile can set the sibling cap above 1 to test robustness.

## Technical Requirements

- Do not require every item to be in a metamorphic group.
- Do not make group consistency the primary score in v1.
- Treat provider errors and timeouts as unscored for group consistency, but report group coverage.
- Keep all group computations deterministic and CSV-based.

## Task 1: Add Schema Fields And Validation

**Files:**
- Modify: `obviousbench/datasets/schemas.py`
- Modify: `obviousbench/datasets/validation.py`
- Test: `tests/datasets/test_metamorphic_metadata.py`

- [x] **Step 1: Write failing schema tests**

```python
from obviousbench.datasets.schemas import BenchmarkItem


def test_metamorphic_metadata_is_accepted():
    record = {
        "id": "obviousbench.spell.en.v0.public.000001",
        "family": "spelling_transform",
        "subfamily": "reverse_word",
        "prompt": "Question: Reverse abc.\nAnswer:",
        "question": "Reverse abc.",
        "target": "cba",
        "answer_type": "string",
        "scorer": "exact_string_trim_v0",
        "split": "public_v0",
        "source_type": "generated_variant",
        "source_refs": ["generated:test"],
        "human_triviality": "H0",
        "review_status": "reviewed",
        "metadata": {
            "prompt_template_id": "final_answer_only_v0",
            "metamorphic_group_id": "spell.reverse.001",
            "metamorphic_role": "paraphrase",
            "metamorphic_relation": "equivalent",
            "metamorphic_expected_behavior": "The answer stays cba.",
        },
    }

    item = BenchmarkItem.model_validate(record)

    assert item.metadata.metamorphic_group_id == "spell.reverse.001"
```

- [x] **Step 2: Add optional metadata fields**

Add the four optional fields to `BenchmarkMetadata`.

- [x] **Step 3: Add validation rule**

If one metamorphic field is present, require all of:

- `metamorphic_group_id`,
- `metamorphic_role`,
- `metamorphic_relation`,
- `metamorphic_expected_behavior`.

Emit issue code `incomplete_metamorphic_metadata`.

- [x] **Step 4: Run tests**

Run: `.venv/bin/python -m pytest tests/datasets/test_metamorphic_metadata.py -q`

Expected: PASS.

## Task 2: Export Metamorphic Metadata In Sample Rows

**Files:**
- Modify: `obviousbench/analysis/metrics.py`
- Modify: `obviousbench/analysis/logs.py`
- Modify: `obviousbench/analysis/usage.py`
- Test: `tests/analysis/test_usage_exports.py`

- [x] **Step 1: Add fields to `EvalRecord`**

```python
metamorphic_group_id: str = ""
metamorphic_role: str = ""
metamorphic_relation: str = ""
```

- [x] **Step 2: Populate fields from sample metadata**

In log parsing:

```python
metadata = sample.metadata or {}
benchmark_metadata = metadata.get("benchmark_metadata", {})
metamorphic_group_id = str(benchmark_metadata.get("metamorphic_group_id") or metadata.get("metamorphic_group_id") or "")
```

Use whichever shape current Inspect samples actually preserve.

- [x] **Step 3: Add columns to `usage_by_sample.csv`**

Columns:

- `metamorphic_group_id`,
- `metamorphic_role`,
- `metamorphic_relation`.

- [x] **Step 4: Run usage export tests**

Run: `.venv/bin/python -m pytest tests/analysis/test_usage_exports.py -q`

Expected: PASS.

## Task 3: Add Group Consistency Analysis

**Files:**
- Create: `obviousbench/analysis/metamorphic.py`
- Modify: `obviousbench/analysis/summarize_results.py`
- Test: `tests/analysis/test_metamorphic.py`

- [x] **Step 1: Write consistency tests**

```python
from obviousbench.analysis.metamorphic import compute_metamorphic_consistency
from obviousbench.analysis.metrics import EvalRecord


def test_equivalent_group_consistency_requires_same_correctness():
    rows = compute_metamorphic_consistency([
        EvalRecord(model="m", sample_id="a", family="spelling_transform", correct=True, failure_type="none", provider_error=False, timeout=False, metamorphic_group_id="g1", metamorphic_relation="equivalent"),
        EvalRecord(model="m", sample_id="b", family="spelling_transform", correct=False, failure_type="string_transform_error", provider_error=False, timeout=False, metamorphic_group_id="g1", metamorphic_relation="equivalent"),
    ])

    assert rows[0].consistent is False
```

- [x] **Step 2: Implement row dataclass**

Fields:

- `run_variant`,
- `model`,
- `family`,
- `metamorphic_group_id`,
- `metamorphic_relation`,
- `samples`,
- `scored_samples`,
- `all_correct`,
- `all_incorrect`,
- `mixed_outcomes`,
- `consistent`.

- [x] **Step 3: Export CSV from summarization**

`summarize_results` should write `metamorphic_consistency.csv` when any records have a group id.

- [x] **Step 4: Run tests**

Run: `.venv/bin/python -m pytest tests/analysis/test_metamorphic.py tests/analysis/test_usage_exports.py -q`

Expected: PASS.

## Task 4: Add Barrage Sibling Cap

**Files:**
- Modify: `obviousbench/barrage.py`
- Modify: `obviousbench/cli.py`
- Test: `tests/test_barrage.py`
- Test: `tests/test_cli.py`

- [x] **Step 1: Extend barrage builder signature**

```python
def build_barrage(
    items: list[BenchmarkItem],
    profile: BarrageProfile,
    *,
    seed: int,
    max_metamorphic_siblings_per_group: int = 1,
) -> list[BenchmarkItem]:
```

- [x] **Step 2: Enforce cap during selection**

When selecting candidates, skip an item if its group id has already reached the cap for the current barrage.

- [x] **Step 3: Add CLI flag**

```python
make_barrage.add_argument("--max-metamorphic-siblings-per-group", default=1, type=int)
```

- [x] **Step 4: Run barrage tests**

Run: `.venv/bin/python -m pytest tests/test_barrage.py tests/test_cli.py -q`

Expected: PASS.

## Acceptance Criteria

- Metamorphic metadata is optional but validated when present.
- Per-sample summaries preserve group metadata.
- Summaries produce group consistency CSVs for grouped items.
- Default barrages avoid overloading one metamorphic group.
- Stress profiles can intentionally include multiple siblings.
- Reports can identify models that pass one variant and fail its obvious sibling.

## Verification Commands

```bash
.venv/bin/python -m pytest tests/datasets/test_metamorphic_metadata.py tests/analysis/test_metamorphic.py tests/test_barrage.py tests/test_cli.py -q
.venv/bin/python scripts/validate_dataset.py data/public_v0/*.jsonl
.venv/bin/python -m ruff check obviousbench tests
git diff --check
```
