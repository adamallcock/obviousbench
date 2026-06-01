---
title: Item Cards V1 Implementation Plan
date: 2026-05-31
type: plan
status: implemented
---

# Item Cards V1 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a lightweight item-card layer that records provenance, answer derivation, ambiguity review, scorer contract, and split policy for every benchmark item that is allowed into trusted splits.

**Architecture:** Keep JSONL benchmark items as the runtime dataset format. Add human-readable YAML item-card files beside the datasets, validate them with Pydantic, and wire the existing `obviousbench validate` command so trusted splits can require item cards without changing Inspect task loading.

**Tech Stack:** Python 3.11, Pydantic, PyYAML, existing `obviousbench.datasets.validation`, pytest, ruff.

---

## Implementation Status

Implemented on 2026-05-31. The shipped version includes typed item-card loading,
dataset/CLI validation hooks, generated public-v0 draft cards, lifecycle docs,
and regression tests.

## Principles

- Keep cards separate from JSONL rows so provenance and review notes can be verbose without making task loading heavy.
- Require cards only for higher-trust splits first. Existing `public_v0` can be migrated gradually; `public_v1` must require cards.
- Do not introduce a database, migration framework, or bespoke document parser. PyYAML is already a project dependency.
- Treat a card as benchmark evidence, not scoring logic. Scorers remain deterministic Python functions.

## Current Repo Touchpoints

- Runtime dataset schema: `obviousbench/datasets/schemas.py`
- Dataset validation: `obviousbench/datasets/validation.py`
- CLI validation entrypoint: `obviousbench/cli.py`
- Existing validation shim: `scripts/validate_dataset.py`
- Dataset files: `data/public_v0/*.jsonl`, `data/calibration_v0/*.jsonl`
- Existing source policy docs: `docs/source_policy.md`, `docs/source_archetypes_v0.md`
- Tests: `tests/test_cli.py`, plus new item-card tests under `tests/datasets/`

## Proposed File Structure

- Create: `obviousbench/datasets/item_cards.py`
  - Owns item-card Pydantic models, YAML loading, duplicate detection, and lookup by `item_id`.
- Modify: `obviousbench/datasets/validation.py`
  - Adds optional card-aware validation and checks dataset rows against loaded cards.
- Modify: `obviousbench/cli.py`
  - Adds `--item-cards-dir` and `--require-item-cards` to `obviousbench validate`.
- Create: `scripts/generate_item_card_stubs.py`
  - Generates reviewed-or-draft YAML stubs from JSONL files for human completion.
- Create: `data/item_cards/public_v0/cards.yaml`
  - Initial generated stubs for current `public_v0`, with explicit `review_status: draft` unless already manually reviewed.
- Create: `tests/datasets/test_item_cards.py`
  - Unit tests for schema validation, duplicate detection, and cross-checks.
- Modify: `tests/test_cli.py`
  - CLI tests for card-aware validation flags.
- Modify: `docs/methodology.md`
  - Documents item-card lifecycle and trust boundary.

## Item Card YAML Contract

Use one YAML file per split at first. This minimizes file churn while keeping review diffs readable. The loader can support multiple `*.yaml` files inside a split directory, but the initial implementation should only create `cards.yaml`.

```yaml
cards:
  - item_id: obviousbench.constraint.en.v0.public.000001
    archetype_id: public_failure.car_wash.object_transport.2026_05
    source_refs:
      - user_screenshot:2026-05-31-car-wash
    source_type: user_provided_screenshot_do_not_republish
    source_summary: User-provided screenshot of a model correctly answering the car wash prompt.
    answer_derivation: A car wash requires the car to be present, so the answer is drive.
    expected_answer: B
    scorer_contract:
      scorer: multiple_choice_letter_v0
      answer_type: multiple_choice
      strict_format: true
      acceptable_outputs:
        - B
        - drive
      unacceptable_outputs:
        - A
        - walk
    ambiguity_notes:
      - Walking is not equivalent because the car would remain at home.
    split_policy:
      allowed_splits:
        - public_v0
        - dev_v1
      leakage_risk: medium
      publishable: false
      rationale: The exact screenshot should not be republished, but a generated variant can be public.
    review:
      status: draft
      reviewer: local
      reviewed_on: 2026-05-31
      notes: Generated card stub requiring human review.
```

## Functional Requirements

- `obviousbench validate data/public_v0/*.jsonl --item-cards-dir data/item_cards` loads cards but does not fail on missing cards unless `--require-item-cards` is present.
- `obviousbench validate data/public_v1/*.jsonl --item-cards-dir data/item_cards --require-item-cards` fails for every item without exactly one card.
- Validation fails when a card `item_id` is duplicated across YAML files.
- Validation fails when a card references an item not present in the validated dataset, unless `--allow-extra-item-cards` is explicitly passed.
- Validation fails when card `expected_answer`, `scorer_contract.scorer`, or `scorer_contract.answer_type` contradicts the dataset row.
- Validation fails when `review.status` is `draft` for a split configured as card-required.
- Validation fails when `ambiguity_notes` or `answer_derivation` is blank.
- Validation preserves existing public-item rules: reviewed rows, valid IDs, source refs, and no H3 items.

## Technical Requirements

- Do not make Inspect task loading depend on item-card files.
- Do not require cards for `calibration_v0` smoke tests.
- Use Pydantic models with `extra="forbid"` for item-card fields so typoed review metadata does not silently pass.
- Loader must preserve file path and YAML index in validation errors.
- CLI errors must use the existing `ValidationIssue.format()` path/field/code pattern.
- The generator script must never mark generated stubs as reviewed.

## Task 1: Add Item-Card Models And Loader

**Files:**
- Create: `obviousbench/datasets/item_cards.py`
- Test: `tests/datasets/test_item_cards.py`

- [x] **Step 1: Write failing loader tests**

```python
from pathlib import Path

from obviousbench.datasets.item_cards import load_item_cards


def test_load_item_cards_indexes_by_item_id(tmp_path: Path):
    cards_dir = tmp_path / "data" / "item_cards"
    split_dir = cards_dir / "public_v0"
    split_dir.mkdir(parents=True)
    (split_dir / "cards.yaml").write_text(
        """
cards:
  - item_id: obviousbench.spell.en.v0.public.000001
    archetype_id: generated.spelling.reverse_word.000001
    source_refs: ["generated:public_v0"]
    source_type: generated_variant
    source_summary: Generated spelling transform control.
    answer_derivation: Reversing abc gives cba.
    expected_answer: cba
    scorer_contract:
      scorer: exact_string_trim_v0
      answer_type: string
      strict_format: false
      acceptable_outputs: ["cba"]
      unacceptable_outputs: ["abc"]
    ambiguity_notes: ["No ambiguity; exact reversal."]
    split_policy:
      allowed_splits: ["public_v0"]
      leakage_risk: low
      publishable: true
      rationale: Generated control item.
    review:
      status: reviewed
      reviewer: test
      reviewed_on: 2026-05-31
      notes: Unit test card.
""",
        encoding="utf-8",
    )

    cards = load_item_cards(cards_dir)

    assert "obviousbench.spell.en.v0.public.000001" in cards.by_item_id
    assert cards.by_item_id["obviousbench.spell.en.v0.public.000001"].expected_answer == "cba"
```

- [x] **Step 2: Run the failing test**

Run: `.venv/bin/python -m pytest tests/datasets/test_item_cards.py -q`

Expected: FAIL with `ModuleNotFoundError` or missing `load_item_cards`.

- [x] **Step 3: Implement `obviousbench/datasets/item_cards.py`**

```python
"""Item-card provenance and review metadata for benchmark rows."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Literal

import yaml
from pydantic import BaseModel, ConfigDict, StrictStr, field_validator


class ScorerContract(BaseModel):
    model_config = ConfigDict(extra="forbid")

    scorer: StrictStr
    answer_type: StrictStr
    strict_format: bool = False
    acceptable_outputs: list[StrictStr] = []
    unacceptable_outputs: list[StrictStr] = []


class SplitPolicy(BaseModel):
    model_config = ConfigDict(extra="forbid")

    allowed_splits: list[StrictStr]
    leakage_risk: Literal["low", "medium", "high"]
    publishable: bool
    rationale: StrictStr


class ReviewBlock(BaseModel):
    model_config = ConfigDict(extra="forbid")

    status: Literal["draft", "reviewed", "retired"]
    reviewer: StrictStr
    reviewed_on: StrictStr
    notes: StrictStr = ""


class ItemCard(BaseModel):
    model_config = ConfigDict(extra="forbid")

    item_id: StrictStr
    archetype_id: StrictStr
    source_refs: list[StrictStr]
    source_type: StrictStr
    source_summary: StrictStr
    answer_derivation: StrictStr
    expected_answer: StrictStr
    scorer_contract: ScorerContract
    ambiguity_notes: list[StrictStr]
    split_policy: SplitPolicy
    review: ReviewBlock

    @field_validator("source_refs", "ambiguity_notes")
    @classmethod
    def non_empty_list(cls, value: list[str]) -> list[str]:
        if not value or any(not item.strip() for item in value):
            raise ValueError("list must contain at least one non-blank value")
        return value


@dataclass(frozen=True)
class LoadedItemCards:
    by_item_id: dict[str, ItemCard]


def load_item_cards(cards_dir: Path | str) -> LoadedItemCards:
    root = Path(cards_dir)
    by_item_id: dict[str, ItemCard] = {}
    for path in sorted(root.rglob("*.yaml")):
        payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        for raw_card in payload.get("cards", []):
            card = ItemCard.model_validate(raw_card)
            if card.item_id in by_item_id:
                raise ValueError(f"Duplicate item card for {card.item_id}")
            by_item_id[card.item_id] = card
    return LoadedItemCards(by_item_id=by_item_id)
```

- [x] **Step 4: Run loader tests**

Run: `.venv/bin/python -m pytest tests/datasets/test_item_cards.py -q`

Expected: PASS.

## Task 2: Wire Card-Aware Dataset Validation

**Files:**
- Modify: `obviousbench/datasets/validation.py`
- Modify: `obviousbench/cli.py`
- Test: `tests/datasets/test_item_cards.py`
- Test: `tests/test_cli.py`

- [x] **Step 1: Add tests for missing and contradictory cards**

Add tests that call `validate_dataset_paths([...], item_cards_dir=cards_dir, require_item_cards=True)` and assert these issue codes:

```python
assert "missing_item_card" in {issue.code for issue in report.issues}
assert "item_card_target_mismatch" in {issue.code for issue in report.issues}
assert "draft_item_card" in {issue.code for issue in report.issues}
```

- [x] **Step 2: Extend validation signature**

Add optional arguments:

```python
def validate_dataset_paths(
    paths: Sequence[Path | str],
    *,
    item_cards_dir: Path | str | None = None,
    require_item_cards: bool = False,
    allow_extra_item_cards: bool = False,
) -> ValidationReport:
```

- [x] **Step 3: Add cross-checks after each valid item**

Implement checks for:

- missing card when required,
- draft card when required,
- `expected_answer != item.target`,
- scorer mismatch,
- answer type mismatch,
- split not in `allowed_splits`,
- extra cards not represented by validated items unless explicitly allowed.

- [x] **Step 4: Add CLI flags**

Add to the `validate` subparser:

```python
validate.add_argument("--item-cards-dir")
validate.add_argument("--require-item-cards", action="store_true")
validate.add_argument("--allow-extra-item-cards", action="store_true")
```

Then pass those values into `validate_dataset_paths`.

- [x] **Step 5: Run focused tests**

Run: `.venv/bin/python -m pytest tests/datasets/test_item_cards.py tests/test_cli.py -q`

Expected: PASS.

## Task 3: Add Stub Generator

**Files:**
- Create: `scripts/generate_item_card_stubs.py`
- Test: `tests/datasets/test_item_card_stub_generator.py`

- [x] **Step 1: Write generator test**

Test a one-row JSONL fixture and assert the generated card:

- uses the same `item_id`, `target`, `answer_type`, and `scorer`,
- copies dataset `source_refs`,
- writes `review.status: draft`,
- includes `answer_derivation` and `ambiguity_notes` strings that clearly require review.

- [x] **Step 2: Implement generator**

Use `load_benchmark_jsonl` and `yaml.safe_dump`. The generated output path should be explicit:

Run shape:

```bash
.venv/bin/python scripts/generate_item_card_stubs.py \
  --dataset data/public_v0/character_count.jsonl \
  --out data/item_cards/public_v0/character_count.yaml
```

- [x] **Step 3: Run generator test**

Run: `.venv/bin/python -m pytest tests/datasets/test_item_card_stub_generator.py -q`

Expected: PASS.

## Task 4: Migrate Public V0 To Draft Cards

**Files:**
- Create or update: `data/item_cards/public_v0/cards.yaml`
- Modify: `docs/methodology.md`

- [x] **Step 1: Generate draft cards**

Run:

```bash
.venv/bin/python scripts/generate_item_card_stubs.py \
  --dataset data/public_v0/character_count.jsonl \
  --dataset data/public_v0/spelling_transform.jsonl \
  --dataset data/public_v0/arithmetic.jsonl \
  --dataset data/public_v0/word_count.jsonl \
  --dataset data/public_v0/ordering.jsonl \
  --dataset data/public_v0/format_compliance.jsonl \
  --dataset data/public_v0/negation.jsonl \
  --dataset data/public_v0/constraint_awareness.jsonl \
  --out data/item_cards/public_v0/cards.yaml
```

- [x] **Step 2: Validate without requiring reviewed cards**

Run:

```bash
.venv/bin/python scripts/validate_dataset.py data/public_v0/*.jsonl \
  --item-cards-dir data/item_cards \
  --allow-extra-item-cards
```

Expected: PASS.

- [x] **Step 3: Document lifecycle**

Add to `docs/methodology.md`:

```markdown
Item-card lifecycle:

1. Generated or mined item receives a draft card.
2. Reviewer fills answer derivation, ambiguity notes, and scorer contract.
3. Trusted splits require reviewed cards.
4. Runtime JSONL stays compact; cards preserve provenance and review evidence.
```

## Acceptance Criteria

- `obviousbench validate` remains backward-compatible when card flags are absent.
- Card-aware validation passes for current `public_v0` with draft cards when `--require-item-cards` is absent.
- Card-aware validation fails for a trusted split with missing, draft, contradictory, or duplicate cards.
- Generated cards never claim human review.
- No Inspect task depends on item-card loading.
- `docs/methodology.md` clearly explains why item cards exist and when they are required.

## Verification Commands

```bash
.venv/bin/python -m pytest tests/datasets/test_item_cards.py tests/test_cli.py -q
.venv/bin/python scripts/validate_dataset.py data/public_v0/*.jsonl --item-cards-dir data/item_cards --allow-extra-item-cards
.venv/bin/python -m ruff check obviousbench tests scripts
git diff --check
```
