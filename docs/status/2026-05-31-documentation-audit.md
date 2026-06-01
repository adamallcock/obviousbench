---
title: Documentation Audit
date: 2026-05-31
type: review
status: draft
---

# Documentation Audit

## Scope

Reviewed the tracked documentation surface against the current code and data
shape:

- `README.md`
- `.github/pull_request_template.md`
- `docs/*.md`
- `docs/status/*.md`
- `docs/superpowers/plans/*.md`
- `docs/shareable/2026-05-31-obviousbench-proof-point/*.md`
- tracked benchmark report Markdown/HTML outputs
- `obviousbench_build_plan.md`

Generated cache/vendor docs, ignored raw result galleries, and local Python
cache files were not treated as authoritative documentation.

## Verified Against Code

- CLI commands match `obviousbench/cli.py`: `validate`, `summarize`, `rescore`,
  `make-barrage`, `build-shareable`, `build-report`, and `build-comparison`.
- Dataset validation accepts the current `public_v0` and calibration data.
- Card-aware validation accepts current draft item cards when extra card stubs
  are explicitly allowed.
- Current `public_v0` composition is 401 rows, 8 families, 399 generated
  variants, 2 public archetype items, and 3 rows with metamorphic metadata.
- Summarization and comparison docs now match current code paths for scored
  samples, confidence intervals, metamorphic consistency, provider-refusal
  retry handling, and efficiency fields.

## Minor Updates Applied

- Added the item-card validation path and current dataset snapshot to
  `README.md`.
- Clarified README accuracy denominators and Wilson interval output.
- Updated `.github/pull_request_template.md` to use the repo `.venv` commands
  and include card-aware validation.
- Updated the shareable benchmark card's dataset-vintage and public-seed-data
  caveats to match `docs/benchmark_card.md` and current data.

## Deferred Larger Changes

These are significant enough to require confirmation before changing them:

- Normalize frontmatter across all existing documentation. Several tracked docs
  intentionally or historically lack YAML frontmatter, including policy docs and
  generated leaderboard Markdown.
- Rewrite `obviousbench_build_plan.md` from a historical build plan into a
  current architecture document. The file is useful history but contains planned
  scaffolding that differs from the shipped code.
- Regenerate shareable artifacts from the latest report outputs. The promoted
  bundle is a dated 2026-05-31 proof point, while later local reports and
  rescored comparisons exist in other directories.
- Regenerate or rebaseline generated `docs/reports/**` files. They are already
  modified in the worktree and should be handled as generated artifacts, not
  hand-edited prose.
- Decide whether historical status documents should remain point-in-time
  snapshots or receive explicit stale/historical notices throughout.
