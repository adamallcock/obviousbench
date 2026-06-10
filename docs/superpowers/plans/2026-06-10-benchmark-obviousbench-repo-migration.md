---
title: Benchmark ObviousBench Repo Migration Plan
date: 2026-06-10
type: plan
status: active
---

# Benchmark ObviousBench Repo Migration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Safely preserve, commit, merge, and rename the local `benchmark-oops` checkout to `benchmark-obviousbench` without losing work or breaking release surfaces.

**Architecture:** Treat this as a staged repository migration, not a filesystem-only rename. First freeze recoverable state, then commit reviewable work waves, then merge to `main`, then rename the local folder and repair path-sensitive runtime state. Remote repo creation or restructuring happens only after the current work is clean and recoverable.

**Tech Stack:** Git, GitHub CLI, Python 3.11, Inspect AI, pytest, ruff, npm, runcost, local Codex worktrees.

---

## Current Facts

- Primary checkout: `/Users/adamallcock/Documents/Coding/benchmark-oops`.
- Desired local checkout name: `/Users/adamallcock/Documents/Coding/benchmark-obviousbench`.
- Current branch: `fix/anthropic-opus-4-8-thinking-telemetry-cost`, tracking `origin/fix/anthropic-opus-4-8-thinking-telemetry-cost`.
- Current benchmark remote: `https://github.com/adamallcock/obviousbench`, private, default branch `main`, current user has `ADMIN`.
- Current website repo found by GitHub inventory: `adamallcock/website-obviousbench-com`, private.
- No separate working-set repo was found in the first inventory pass.
- `main` on `adamallcock/obviousbench` is not currently protected.
- Existing Codex side worktree: `/Users/adamallcock/.codex/worktrees/22f0/benchmark-oops`, detached at `c6e3068`, with separate constraint-awareness/question-expansion work.
- Local safety snapshot created before edits: `/Users/adamallcock/Documents/Coding/.repo-safety/benchmark-oops-20260610-140559`.
- Validation before this plan:
  - PASS: `.venv/bin/python -m pytest tests -q` (`579 passed`).
  - PASS: `.venv/bin/python -m compileall -q obviousbench`.
  - PASS: `.venv/bin/python scripts/validate_dataset.py data/public_v0/*.jsonl data/calibration_v0/smoke_test.jsonl`.
  - PASS: `.venv/bin/python scripts/validate_dataset.py data/public_v0/*.jsonl --item-cards-dir data/item_cards --allow-extra-item-cards`.
  - PASS: `npm ls runcost` (`runcost@0.1.4`).
  - FAIL: `.venv/bin/python -m ruff check .`; failures are concentrated in untracked experiment scripts/notebook cells plus a few import/style issues.

## Commit-Wave Rules

- Do not stage `AGENTS.md`, `tmp/`, `reports/runs/`, raw `results/`, `.venv/`, `node_modules/`, provider logs, API outputs, or local screenshots.
- Treat `docs/reports/**`, `docs/release/**`, `docs/research/**`, `paper/**`, and `configs/**` as eligible release artifacts only when tied to source generators or reproducible notes.
- Keep Python package and CLI names as `obviousbench`.
- Rename the private npm package name from `benchmark-oops` only in the final local-folder rename wave, unless a prior commit explicitly owns package metadata cleanup.
- Do not delete the side worktree. Convert it to a named branch and commit it separately after the primary checkout is clean.

### Task 1: Safety And Hygiene Baseline

**Files:**
- Modify: `.gitignore`
- Create: `docs/superpowers/plans/2026-06-10-benchmark-obviousbench-repo-migration.md`

- [x] **Step 1: Create a local safety snapshot**

Run:

```bash
ls /Users/adamallcock/Documents/Coding/.repo-safety/benchmark-oops-20260610-140559
```

Expected: `primary/` and `worktree-22f0/` exist, each with `committed-refs.bundle`, `tracked-changes.patch`, `untracked-files.tar.gz`, and `SHA256SUMS`.

- [x] **Step 2: Verify current repository roles**

Run:

```bash
gh repo view --json nameWithOwner,isPrivate,defaultBranchRef,url,viewerPermission
gh repo list adamallcock --limit 200 --json nameWithOwner,isPrivate,url
```

Expected: `adamallcock/obviousbench` and `adamallcock/website-obviousbench-com` are visible and private.

- [x] **Step 3: Verify ignore hardening**

Run:

```bash
git check-ignore -v AGENTS.md tmp/pilot_reestimate.md reports/runs/2026-06-07T19-10-05-337Z-chatgpt-run-report.json results/.DS_Store
```

Expected: each path is ignored by `.gitignore`.

- [x] **Step 4: Commit baseline plan and ignore hygiene**

Run:

```bash
git add .gitignore docs/superpowers/plans/2026-06-10-benchmark-obviousbench-repo-migration.md
git diff --cached --check
git commit -m "chore: plan safe repo migration"
```

Expected: one small commit with no source behavior changes.

### Task 2: Complete And Commit Primary Checkout Work

**Files:**
- Modify: tracked Python source, tests, docs, configs, release artifacts, and generated report artifacts that are already present in `/Users/adamallcock/Documents/Coding/benchmark-oops`.

- [ ] **Step 1: Re-run a clean status after Task 1**

Run:

```bash
git status --short --branch
git diff --name-status
git ls-files --others --exclude-standard | sed -n '1,200p'
```

Expected: volatile `AGENTS.md`, `tmp/`, `reports/runs/`, and raw `results/` files no longer appear as untracked work.

- [ ] **Step 2: Fix or defer ruff-red untracked surfaces**

Run:

```bash
.venv/bin/python -m ruff check .
```

Expected: either ruff passes, or each remaining ruff-red file is explicitly left untracked and ignored/deferred with a note in the final migration log.

- [ ] **Step 3: Commit dependency and metadata changes**

Candidate files:

```text
README.md
package.json
package-lock.json
pyproject.toml
scripts/price_usage_with_runcost.mjs
```

Commit message:

```bash
git commit -m "chore: update benchmark costing dependencies"
```

- [ ] **Step 4: Commit scorer and normalization changes**

Candidate files:

```text
obviousbench/scorers/**
tests/scorers/**
tests/fixtures/scorer_gold/**
docs/scoring_policy.md
```

Commit message:

```bash
git commit -m "fix: harden scorer normalization"
```

- [ ] **Step 5: Commit analysis/report generation changes**

Candidate files:

```text
obviousbench/analysis/**
tests/analysis/**
docs/shareable/2026-05-31-obviousbench-proof-point/**
docs/reports/**
```

Commit message:

```bash
git commit -m "feat: improve benchmark report artifacts"
```

- [ ] **Step 6: Commit provider runner and panel provenance changes**

Candidate files:

```text
obviousbench/runners/**
obviousbench/research/model_panel_runner.py
tests/runners/**
tests/research/test_model_panel_runner.py
configs/*panel*.yaml
configs/*manifest*.csv
```

Commit message:

```bash
git commit -m "feat: capture model panel provenance"
```

- [ ] **Step 7: Commit paper/release research pipeline**

Candidate files:

```text
obviousbench/research/**
scripts/audit_*.py
scripts/build_*.py
scripts/estimate_paper_model_panel_costs.py
scripts/promote_*.py
tests/research/**
tests/scripts/**
docs/research/**
docs/release/**
paper/**
```

Commit message:

```bash
git commit -m "feat: add paper release evidence pipeline"
```

- [ ] **Step 8: Commit dataset and item-card refreshes**

Candidate files:

```text
data/public_v0/**
data/item_cards/**
data/barrages/**
data/splits/**
data/human_baseline/**
data/experiments/**
docs/benchmark_card.md
docs/methodology.md
docs/prompt_policy.md
docs/runbook.md
docs/source_archetypes_v0.md
docs/source_policy.md
docs/status/**
```

Commit message:

```bash
git commit -m "data: refresh benchmark release artifacts"
```

- [ ] **Step 9: Validate the fully committed branch**

Run:

```bash
.venv/bin/python -m pytest tests -q
.venv/bin/python -m ruff check .
.venv/bin/python -m compileall -q obviousbench
.venv/bin/python scripts/validate_dataset.py data/public_v0/*.jsonl data/calibration_v0/smoke_test.jsonl
.venv/bin/python scripts/validate_dataset.py data/public_v0/*.jsonl --item-cards-dir data/item_cards --allow-extra-item-cards
git diff --check
```

Expected: all commands pass before merge to `main`.

### Task 3: Preserve Side Worktree Work

**Files:**
- Operate in `/Users/adamallcock/.codex/worktrees/22f0/benchmark-oops`.

- [ ] **Step 1: Convert detached side worktree to a named branch**

Run:

```bash
cd /Users/adamallcock/.codex/worktrees/22f0/benchmark-oops
git switch -c codex/constraint-awareness-reset
```

Expected: the side worktree remains intact, no files are lost, and future commits have a branch name.

- [ ] **Step 2: Commit side worktree changes separately**

Run the same ignore, ruff, dataset, and pytest gates that apply to the touched files. Use commit messages that name constraint-awareness/question-expansion work, not the Anthropic telemetry branch.

### Task 4: Merge Primary Branch To Main

**Files:**
- Git history only.

- [ ] **Step 1: Merge after Task 2 passes**

Run:

```bash
git switch main
git merge --no-ff fix/anthropic-opus-4-8-thinking-telemetry-cost
```

Expected: clean merge or explicit conflict list. Do not delete the source branch until the rename and GitHub checks are complete.

- [ ] **Step 2: Validate on main**

Run the full validation set from Task 2 Step 9.

- [ ] **Step 3: Push main**

Run:

```bash
git push origin main
```

Expected: `origin/main` contains the complete committed work.

### Task 5: Rename Local Folder To `benchmark-obviousbench`

**Files:**
- Local filesystem folder.
- Potentially modify: `package.json`, `package-lock.json`, docs that intentionally mention the old local checkout path.

- [ ] **Step 1: Require a clean `main` worktree**

Run:

```bash
git status --short --branch
```

Expected: clean `main`. Do not rename with uncommitted work present.

- [ ] **Step 2: Rename the folder from the parent directory**

Run:

```bash
cd /Users/adamallcock/Documents/Coding
mv benchmark-oops benchmark-obviousbench
cd benchmark-obviousbench
```

Expected: `git status --short --branch` still works.

- [ ] **Step 3: Rebuild path-sensitive local runtime state**

Run:

```bash
rm -rf .venv
python -m venv .venv
.venv/bin/python -m pip install -e ".[dev]"
npm ci
```

Expected: `.venv` entrypoints use the new absolute path.

- [ ] **Step 4: Audit old path references**

Run:

```bash
rg -n -I '/Users/adamallcock/Documents/Coding/benchmark-oops|benchmark-oops' --hidden -g '!/.git/**' -g '!node_modules/**' -g '!results/**' -g '!tmp/**' -g '!reports/**'
```

Expected: no stale absolute paths in tracked source/docs. Historical mentions are allowed only in migration notes. Keep Python package/CLI names as `obviousbench`.

- [ ] **Step 5: Commit the local rename metadata**

If package metadata is still named `benchmark-oops`, update only the private npm package metadata to `benchmark-obviousbench`; keep Python package metadata unchanged.

Commit message:

```bash
git commit -m "chore: rename local benchmark workspace"
```

### Task 6: GitHub Repo Hygiene After Merge

**Files:**
- GitHub repository settings.

- [ ] **Step 1: Decide repo roles**

Record a short decision note answering:

```text
website repo: adamallcock/website-obviousbench-com
future public benchmark repo: adamallcock/obviousbench
private working-set repo: create only if current private benchmark repo should stay clean for public release
```

- [ ] **Step 2: Protect `main` on `adamallcock/obviousbench`**

Use GitHub settings or `gh api` to require PR review and the `site-check` workflow before direct merges. Do this after `main` is already green.

- [ ] **Step 3: Create a private working-set repo only if still needed**

If the decision is to keep `adamallcock/obviousbench` as the future-public benchmark repo, create a separate private working repo. Suggested name:

```text
adamallcock/benchmark-obviousbench-working
```

Expected setup: private visibility, protected `main`, CI enabled, generated/private artifacts ignored, no raw provider logs.
