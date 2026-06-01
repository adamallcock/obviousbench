---
title: Split Strategy V1 Implementation Plan
date: 2026-05-31
type: plan
status: parked
---

# Split Strategy V1 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Define the future public, dev, private, live, and canary split strategy so ObviousBench can grow without turning the public examples into the whole benchmark.

**Architecture:** This is a parked implementation plan. The current milestone should only document the split model and avoid code changes unless work resumes explicitly. Future implementation extends the existing dataset directory layout, item-card split policy, and validator.

**Tech Stack:** Existing JSONL datasets, item-card YAML from `item-cards-v1`, Pydantic validation, pytest.

---

## Current Decision

We agree ObviousBench needs better splits, but split migration is not part of
the current implementation batch. The policy has been documented; new split
directories and code-path activation remain parked until the user resumes this
work explicitly.

## Why Better Splits Are Needed

- `public_v0` is generated seed data and useful for proof points, but it should not be the final leaderboard source.
- Public examples can become contaminated once shared.
- Local development needs a stable set that can be re-run frequently.
- A credible benchmark needs a private or live set for claims that are stronger than demos.
- Canary items help detect memorization, leakage, and accidental overfitting.

## Proposed Split Model

| Split | Purpose | Committed Publicly | Requires Item Cards | Used For Claims |
| --- | --- | --- | --- | --- |
| `public_v1` | Small inspectable example set | Yes | Yes | Demos only |
| `dev_v1` | Local iteration and regression | Yes or private repo only | Yes | No public leaderboard claims |
| `private_v1` | Held-out evaluation | No | Yes | Yes, if procedure is documented |
| `live_vYYYY_MM` | Dated refresh from recent sources | Partially or not at all | Yes | Yes, with date stated |
| `canary_v1` | Leakage and overfitting controls | No | Yes | Diagnostic only |

## Split Admission Rules

- Every trusted split item must have a reviewed item card.
- Exact prompts must not overlap across protected splits.
- Near-duplicate archetype siblings must be capped per split.
- Source refs must be tracked in item cards even when the source itself cannot be republished.
- Public split items must be safe to show in docs and failure galleries.
- Private and canary items must not be promoted into shareable bundles.

## Future File Structure

- Create: `data/public_v1/*.jsonl`
- Create: `data/dev_v1/*.jsonl`
- Create locally, ignored if needed: `data/private_v1/*.jsonl`
- Create locally or release-dated: `data/live_v2026_06/*.jsonl`
- Create locally, ignored if needed: `data/canary_v1/*.jsonl`
- Modify: `obviousbench/datasets/schemas.py`
  - Add split short names for v1 IDs.
- Modify: `obviousbench/datasets/validation.py`
  - Add overlap and split-policy checks.
- Modify: `.gitignore`
  - Ignore private and canary data if those directories are local-only.
- Modify: `docs/methodology.md`
  - Add split policy.
- Modify: `docs/benchmark_card.md`
  - Make claims explicitly name the split.

## Future Functional Requirements

- Validation rejects duplicate item IDs across all supplied split files.
- Validation rejects exact duplicate prompts across protected splits.
- Validation rejects the same `source_ref` in protected splits unless the item card marks it as a deliberate public/dev sibling.
- `obviousbench make-barrage --split private_v1` works if local files exist.
- `obviousbench build-shareable` refuses private and canary source directories unless `--allow-private-artifacts` is explicitly added in a future plan.
- Reports state split name and data vintage.

## Future Technical Requirements

- Do not require a central registry service.
- Keep split directories under `data/`.
- Use item-card `split_policy.allowed_splits` as the source of truth for which splits an item may enter.
- Use deterministic ID short names in `FAMILY_SHORT_NAMES` and `SPLIT_SHORT_NAMES`.
- Keep public `public_v1` small enough for humans to inspect.

## Future Task 1: Add Split Names And Validation

**Files:**
- Modify: `obviousbench/datasets/schemas.py`
- Modify: `obviousbench/datasets/validation.py`
- Test: `tests/datasets/test_split_policy.py`

- [ ] **Step 1: Add split short-name tests**

```python
from obviousbench.datasets.schemas import parse_item_id


def test_parse_public_v1_item_id():
    parsed = parse_item_id("obviousbench.spell.en.v1.public.000001")
    assert parsed.version == "v1"
    assert parsed.split_short == "public"
```

- [ ] **Step 2: Update ID parser**

Change `_ID_RE` to accept `v0` or `v1`:

```python
r"(?P<version>v[01])\."
```

- [ ] **Step 3: Add overlap validation**

Track prompts and source refs across supplied files and emit:

- `duplicate_prompt_across_splits`,
- `source_ref_overlap_across_protected_splits`.

## Future Task 2: Add Split Policy Docs

**Files:**
- Modify: `docs/methodology.md`
- Modify: `docs/benchmark_card.md`

- [x] **Step 1: Add methodology section**

```markdown
Split policy:

- Public split: inspectable examples and demos.
- Dev split: local iteration, not headline claims.
- Private split: held-out model comparison.
- Live split: dated refresh with frozen source cards.
- Canary split: leakage diagnostics only.
```

- [x] **Step 2: Add benchmark-card caveat**

Every shareable benchmark card must state the exact split and date.

## Parked Acceptance Criteria

This parked plan is complete when:

- The policy exists in this document.
- Immediate plans avoid hardcoding assumptions that only one public split exists.
- Future item-card schema includes `split_policy.allowed_splits`.
- No code changes are required by this parked plan until the user resumes it.
