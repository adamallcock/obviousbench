---
title: Scorer Gold V1 Implementation Plan
date: 2026-05-31
type: plan
status: implemented
---

# Scorer Gold V1 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a scorer gold suite that locks expected scoring behavior for realistic raw model outputs before scorer changes affect benchmark claims.

**Architecture:** Store scorer gold examples in YAML fixtures, load them through a small typed helper, and run one parameterized pytest file against `obviousbench.analysis.rescore.rescore_output`. Keep this as developer-side test infrastructure, not runtime benchmark data.

**Tech Stack:** Python 3.11, PyYAML, Pydantic, pytest, existing deterministic scorer registry.

---

## Implementation Status

Implemented on 2026-05-31. The shipped version includes typed gold-fixture
loading, deterministic scorer contract tests, observed-failure regressions, and
scoring-policy documentation.

## Principles

- Scorer behavior is benchmark-critical product behavior.
- Gold examples should model messy outputs seen in logs: wrappers, arrays, verbose answers, units, refusals, and answers buried in reasoning.
- The suite must distinguish answer correctness, format correctness, and strict correctness.
- Do not use LLM judges for scorer gold. Expected outcomes are hand-authored and deterministic.

## Current Repo Touchpoints

- Rescore entrypoint: `obviousbench/analysis/rescore.py`
- Dynamic scorer registry: `obviousbench/scorers/dynamic.py`
- Shared decision type: `obviousbench/scorers/common.py`
- Individual scorer tests: `tests/scorers/test_*.py`
- Existing rescore tests: `tests/analysis/test_rescore.py`
- Scoring policy docs: `docs/scoring_policy.md`

## Proposed File Structure

- Create: `tests/fixtures/scorer_gold/exact_integer_extract_first_v0.yaml`
- Create: `tests/fixtures/scorer_gold/exact_string_trim_v0.yaml`
- Create: `tests/fixtures/scorer_gold/normalized_list_v0.yaml`
- Create: `tests/fixtures/scorer_gold/multiple_choice_letter_v0.yaml`
- Create: `tests/fixtures/scorer_gold/json_exact_field_v0.yaml`
- Create: `tests/fixtures/scorer_gold/word_count_v0.yaml`
- Create: `tests/fixtures/scorer_gold/normalized_string_v0.yaml`
- Create: `tests/fixtures/scorer_gold/regex_match_v0.yaml`
- Create: `tests/scorers/test_gold_contracts.py`
- Create: `obviousbench/scorers/gold.py`
- Modify: `docs/scoring_policy.md`

## Gold Fixture Contract

```yaml
examples:
  - id: normalized_list.bracketed_decimal_order.correct
    scorer: normalized_list_v0
    target: "3.01, 3.1, 3.2"
    output: "[3.01,3.1, 3.2]"
    expected:
      answer_correct: true
      format_correct: true
      strict_correct: true
      extracted: "3.01, 3.1, 3.2"
      failure_type: none
    notes: Bracketed arrays are acceptable for non-strict ordering tasks.
```

## Required Example Classes

Each scorer with public benchmark coverage should have at least these classes:

- exact correct answer,
- correct answer with harmless whitespace,
- correct answer with common wrapper,
- verbose but answer-correct output,
- wrong answer with clean format,
- refusal or non-answer,
- ambiguous output with multiple incompatible answers,
- answer-correct but format-wrong where strict format applies,
- prior observed failure regression.

For `exact_string_trim_v0`, include the observed "model rewrote the prompt or operated on the whole prompt" class.

For `normalized_list_v0`, include bracketed arrays such as `[3.01,3.1, 3.2]`.

For integer/count scorers, include unit suffixes and number words.

## Functional Requirements

- `pytest tests/scorers/test_gold_contracts.py -q` runs all gold examples.
- A gold example asserts `answer_correct`, `format_correct`, `strict_correct`, `failure_type`, and optional `extracted`.
- Fixture loading fails if an example id is duplicated.
- Fixture loading fails if an example references an unknown scorer.
- Fixture loading fails if expected booleans are missing.
- Gold examples are small, reviewable YAML, not generated automatically from current scorer output.
- Scorer changes that alter gold behavior must update fixture expectations and `docs/scoring_policy.md` in the same change.

## Technical Requirements

- Use `rescore_output(scorer_name=..., output=..., target=...)` as the only scoring entrypoint in the gold test.
- Do not import Inspect sample objects into the gold helper.
- Avoid snapshot-style raw output dumps that hide expected decisions.
- Keep fixture schema in `obviousbench/scorers/gold.py` so tests and future CLI tools can reuse it.

## Task 1: Add Gold Fixture Loader

**Files:**
- Create: `obviousbench/scorers/gold.py`
- Test: `tests/scorers/test_gold_contracts.py`

- [x] **Step 1: Write failing loader test**

```python
from pathlib import Path

from obviousbench.scorers.gold import load_gold_examples


def test_load_gold_examples_validates_duplicate_ids(tmp_path: Path):
    fixture = tmp_path / "gold.yaml"
    fixture.write_text(
        """
examples:
  - id: duplicate
    scorer: exact_string_trim_v0
    target: yes
    output: yes
    expected:
      answer_correct: true
      format_correct: true
      strict_correct: true
      failure_type: none
  - id: duplicate
    scorer: exact_string_trim_v0
    target: yes
    output: yes
    expected:
      answer_correct: true
      format_correct: true
      strict_correct: true
      failure_type: none
""",
        encoding="utf-8",
    )

    try:
        load_gold_examples([fixture])
    except ValueError as exc:
        assert "Duplicate scorer gold example id" in str(exc)
    else:
        raise AssertionError("Expected duplicate fixture id to fail")
```

- [x] **Step 2: Implement loader**

Create Pydantic models for:

```python
class ExpectedGoldDecision(BaseModel):
    answer_correct: bool
    format_correct: bool
    strict_correct: bool
    failure_type: StrictStr
    extracted: StrictStr | None = None


class ScorerGoldExample(BaseModel):
    id: StrictStr
    scorer: StrictStr
    target: StrictStr
    output: StrictStr
    expected: ExpectedGoldDecision
    notes: StrictStr = ""
```

`load_gold_examples(paths)` should return `list[ScorerGoldExample]` and raise on duplicate ids.

- [x] **Step 3: Run loader test**

Run: `.venv/bin/python -m pytest tests/scorers/test_gold_contracts.py -q`

Expected: PASS for loader tests once implemented.

## Task 2: Add Parameterized Gold Contract Test

**Files:**
- Modify: `tests/scorers/test_gold_contracts.py`
- Create: `tests/fixtures/scorer_gold/*.yaml`

- [x] **Step 1: Add parameterized test**

```python
from pathlib import Path

import pytest

from obviousbench.analysis.rescore import rescore_output
from obviousbench.scorers.gold import load_gold_examples


FIXTURE_DIR = Path(__file__).parents[1] / "fixtures" / "scorer_gold"


@pytest.mark.parametrize("example", load_gold_examples(sorted(FIXTURE_DIR.glob("*.yaml"))), ids=lambda example: example.id)
def test_scorer_gold_contract(example):
    decision = rescore_output(
        scorer_name=example.scorer,
        output=example.output,
        target=example.target,
    )

    assert decision.answer_correct is example.expected.answer_correct
    assert decision.resolved_format_correct is example.expected.format_correct
    assert decision.strict_correct is example.expected.strict_correct
    assert decision.failure_type == example.expected.failure_type
    if example.expected.extracted is not None:
        assert decision.extracted == example.expected.extracted
```

- [x] **Step 2: Seed minimum fixtures**

Create at least 10 examples for the first pass:

- `exact_integer_extract_first_v0`: digit, number word, unit suffix, multiple conflicting numbers, empty output.
- `exact_string_trim_v0`: exact reverse string, final-answer cue, prompt rewrite rejection.
- `normalized_list_v0`: comma list, bracketed array, wrong order.
- `multiple_choice_letter_v0`: letter answer, natural-language choice answer if supported, wrong choice.

- [x] **Step 3: Run focused tests**

Run: `.venv/bin/python -m pytest tests/scorers/test_gold_contracts.py tests/scorers/test_exact_string.py tests/scorers/test_normalized_list.py -q`

Expected: PASS.

## Task 3: Expand Coverage To Every Active Scorer

**Files:**
- Modify: `tests/fixtures/scorer_gold/*.yaml`
- Modify: `docs/scoring_policy.md`

- [x] **Step 1: Add at least 20 examples for each active public scorer**

Active public scorers are the values in `ScorerName` in `obviousbench/datasets/schemas.py`.

- [x] **Step 2: Add policy notes for tolerated wrappers**

Document decisions such as:

- bracketed arrays accepted for non-strict list tasks,
- unit suffixes accepted only when they do not introduce conflicting numbers,
- final-answer cues accepted when exactly one compatible answer is present,
- prompt rewrites rejected for exact string transformations.

- [x] **Step 3: Run all scorer tests**

Run: `.venv/bin/python -m pytest tests/scorers -q`

Expected: PASS.

## Task 4: Add Rescore Regression Fixture From Real Logs

**Files:**
- Create: `tests/fixtures/scorer_gold/observed_failures.yaml`
- Modify: `tests/scorers/test_gold_contracts.py`

- [x] **Step 1: Add observed examples**

Include manually minimized versions of observed failures:

```yaml
examples:
  - id: observed.ordering.bracketed_array.regression
    scorer: normalized_list_v0
    target: "3.01, 3.1, 3.2"
    output: "[3.01,3.1, 3.2]"
    expected:
      answer_correct: true
      format_correct: true
      strict_correct: true
      extracted: "3.01, 3.1, 3.2"
      failure_type: none
    notes: Regression for a previously suspicious failure that was actually correct.
```

- [x] **Step 2: Run scorer and rescore tests**

Run: `.venv/bin/python -m pytest tests/scorers tests/analysis/test_rescore.py -q`

Expected: PASS.

## Acceptance Criteria

- Gold tests cover every scorer referenced by `ScorerName`.
- Every gold example has explicit expected answer, format, strict, failure type, and notes.
- Tests fail when a scorer accidentally changes extraction or correctness behavior.
- `docs/scoring_policy.md` names accepted wrappers and rejected ambiguous outputs.
- Known prior cases such as bracketed lists and prompt-wide string rewrites are represented.
- No LLM judge or provider call is used anywhere in scorer gold tests.

## Verification Commands

```bash
.venv/bin/python -m pytest tests/scorers tests/analysis/test_rescore.py -q
.venv/bin/python -m ruff check obviousbench tests
git diff --check
```
