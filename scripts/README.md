---
title: Script Index
date: 2026-06-24
type: index
status: active
---

# Script Index

This public repository keeps only the scripts needed to inspect, run, and
package the public ObviousBench surface. Private split construction, private
pass^3 collection, raw-log review builders, and paper/arXiv draft machinery live
in the internal repository and are intentionally not part of this export.

## Dataset Scripts

| Script | Purpose |
|---|---|
| `scripts/datasets/validate_dataset.py` | Validate public example item schema and scorer metadata. |
| `scripts/datasets/generate_item_card_stubs.py` | Generate review-card stubs for public example curation. |

## Runner Scripts

| Script | Purpose |
|---|---|
| `scripts/runners/run_inspect_eval.py` | Run an Inspect eval over a public model panel. |
| `scripts/runners/run_model_panel.py` | Run a YAML model panel through the package runner. |
| `scripts/runners/run_openrouter_batches.py` | Batch OpenRouter-compatible public runs. |
| `scripts/runners/price_usage_with_runcost.mjs` | Price usage exports with the public runcost integration. |

These scripts are for reproducing public examples or running new public-facing
experiments. They are not the source of the v0.2 private held-out results.

## Model Registry Scripts

| Script | Purpose |
|---|---|
| `scripts/model_registry/build_model_registry.mjs` | Build or refresh model-registry metadata from public provider catalogs. |
| `scripts/model_registry/smoke_model_registry.py` | Smoke-check the public model registry and example panel metadata. |

## Public Release Scripts

| Script | Purpose |
|---|---|
| `scripts/release/build_v0_2_release_assets.py` | Regenerate public-safe v0.2 docs and aggregate release assets from aggregate inputs. |
| `scripts/release/build_v0_2_public_release_bundle.py` | Build the allowlisted public release bundle from the internal release config. |
| `scripts/release/audit_v0_2_public_bundle.py` | Audit a public bundle or checkout for private prompts, raw logs, private review pages, and stale local paths. |
| `scripts/release/check_repo_hygiene.py` | Check this public checkout for tracked private data, retired lanes, and missing public docs. |

Recommended public validation sequence:

```bash
uv run --extra dev python -m pytest tests -q
uv run --extra dev python -m ruff check .
uv run --extra dev python -m compileall -q obviousbench scripts
node --check scripts/runners/price_usage_with_runcost.mjs
uv run --extra dev python scripts/release/check_repo_hygiene.py
git diff --check
```
