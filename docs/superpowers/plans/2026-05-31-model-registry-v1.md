---
title: Model Registry V1 Implementation Plan
date: 2026-05-31
type: plan
status: complete
---

# Model Registry V1 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a roughly 200-entry ObviousBench model-and-settings registry focused on free, small, open-weight, and no-thinking model runs.

**Architecture:** Keep the registry generated from primary model catalogs where possible, with a small curated direct-provider baseline section. Store the generated test matrix as repo data, document the selection rules and source dates, and add offline tests that validate the registry shape without calling providers.

**Tech Stack:** Node 20, npm `runcost`, OpenRouter Models API, PyYAML-based pytest validation.

---

### Task 1: Registry Generator

**Files:**
- Create: `scripts/build_model_registry.mjs`
- Create: `configs/model_registry_v1.yaml`

- [x] **Step 1: Add a Node generator**

Create `scripts/build_model_registry.mjs` that fetches `https://openrouter.ai/api/v1/models`, reads `defaultPriceCards()` from npm `runcost`, scores text-output OpenRouter models for free pricing, open-weight/open-source families, small-model likelihood, and no-thinking suitability, then writes `configs/model_registry_v1.yaml`.

- [x] **Step 2: Generate the registry**

Run:

```bash
node scripts/build_model_registry.mjs
```

Expected: `configs/model_registry_v1.yaml` contains about 200 runnable entries with `inspect_model`, `profile`, `seed`, `generation_settings`, price metadata, source metadata, and tags.

### Task 2: Registry Documentation

**Files:**
- Create: `docs/research/2026-05-31-model-registry-v1.md`

- [x] **Step 1: Document sources and scope**

Create `docs/research/2026-05-31-model-registry-v1.md` with YAML frontmatter, source links, current source counts, selection rules, and exact example commands for dry-run estimation and provider execution.

- [x] **Step 2: Document exclusions**

Explicitly note that image/audio-only models, embedding models, deprecated endpoints, and high-cost frontier duplicates are not the focus of this registry.

### Task 3: Registry Tests

**Files:**
- Create: `tests/configs/test_model_registry_v1.py`

- [x] **Step 1: Add offline schema tests**

Add pytest coverage that loads `configs/model_registry_v1.yaml` and verifies:

```python
assert 190 <= len(entries) <= 230
assert len({entry["id"] for entry in entries}) == len(entries)
assert {"openrouter", "openai", "anthropic", "gemini", "grok"}.issubset(provider_routes)
assert free_openrouter_count >= 20
assert small_or_open_weight_count >= 100
```

- [x] **Step 2: Add run-setting tests**

Verify every non-local entry has `temperature: 0`, a bounded `max_tokens`, `profile: hard_obvious_8x10`, and no secret-bearing fields.

### Task 4: Verification

**Files:**
- Modify only if tests reveal a real issue.

- [x] **Step 1: Run focused tests**

Run:

```bash
.venv/bin/python -m pytest tests/configs/test_model_registry_v1.py tests/configs/test_model_matrix.py -q
```

Expected: all tests pass.

- [x] **Step 2: Run formatting check**

Run:

```bash
.venv/bin/python -m ruff check scripts tests/configs
```

Expected: no lint errors.
