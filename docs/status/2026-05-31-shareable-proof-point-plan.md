---
title: Shareable Proof Point Plan
date: 2026-05-31
type: plan
status: in-progress
---

# Shareable Proof Point Plan

Goal: make this checkout externally referenceable for the June 1 ClickUp intro
call and June 5 Scale hiring-manager screen without requiring hand-edited
result files.

## Current Verified Baseline

- Dataset validation passes for `data/public_v0/*.jsonl` and
  `data/calibration_v0/smoke_test.jsonl`.
- Focused tests pass for CLI, task instantiation, and failure-gallery rendering.
- The mock Inspect smoke path runs and summarizes cleanly using
  `mockllm/model`; the mock model returns default text, so the summary correctly
  reports scoring failures while proving the local eval/summarize plumbing.
- Existing generated results are under ignored `results/` paths and should not
  be the only recruiter-safe artifacts.

## Implementation Tasks

- Replace placeholder model config with a small real matrix using exact Inspect
  model strings and recruiter-safe labels.
- Add an artifact builder that promotes selected existing summaries and failure
  galleries into a tracked shareable directory.
- Generate a polished benchmark card, compact model comparison, and curated
  failure gallery from CSV/Markdown inputs instead of hand-editing prose.
- Update README/runbook commands so the smoke path and shareable artifact path
  are copy-paste runnable.
- Validate with focused tests, dataset validation, mock smoke eval,
  summarization, and a generated artifact smoke check.

## Recruiter-Safe Boundary

- No API keys, account IDs, raw provider payloads, or private notes in promoted
  artifacts.
- Raw Inspect logs remain ignored under `results/raw/`.
- Promoted artifacts should explain that `public_v0` is generated seed data
  inspired by source archetypes, not a public leaderboard or vendor claim.
