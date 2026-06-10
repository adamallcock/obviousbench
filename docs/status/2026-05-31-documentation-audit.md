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

## Confirmed Follow-Up Applied

- Added frontmatter to hand-authored policy/reference docs. Generated
  leaderboard Markdown remains frontmatter-free.
- Marked `obviousbench_build_plan.md` as archived historical planning context.
- Added `docs/architecture/2026-05-31-current-architecture.md` as the current
  implementation map.
- Regenerated the shareable proof-point bundle from the rescored V2 comparison.
- Rebuilt generated reports from their comparison directories.
- Added snapshot or current-status notices to historical status documents.

## Still Deferred

- Whether to promote the regenerated shareable bundle as a new dated directory
  instead of reusing `2026-05-31-obviousbench-proof-point/`.
- Whether to add a first-class CLI option that derives `model-matrix.yaml` from
  comparison CSVs instead of requiring a separate matrix source file.
