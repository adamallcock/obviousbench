---
title: Public Release Surface
date: 2026-06-24
type: reference
status: current
---

# Public Release Surface

The live launch site is the canonical narrative and interactive-results surface:

- [https://obviousbench.com](https://obviousbench.com)

This GitHub repository is the source/data companion. It should link prominently
to the website, and the website should link back here for public examples,
aggregate data, source code, license, citation, and reproducibility material.
The deployable website source, static build output, long-form launch page, and
interactive chart application should stay in the website release lane unless we
make a separate explicit decision to move that site source into this repository.

## Included

The public repository includes:

- Runnable benchmark package code under `obviousbench/`.
- Public example items under `data/public_examples/`.
- Public model/config metadata under `configs/`.
- Public-safe aggregate v0.2 result files under `reports/v0_2/aggregate/`.
- Generated public release notes and metadata under `docs/release/v0_2/generated/`.
- Public reference docs, license files, citation metadata, and archive metadata.

## Excluded

The public repository must not include:

- Private held-out prompts or private/reserve split manifests.
- Raw completions, raw Inspect logs, provider logs, or attempt-level private
  outcomes.
- Private review HTML, wrong-answer review HTML, question-failure review HTML,
  or provider-residual investigation reports.
- Local caches, generated distribution bundles, recovery artifacts, or temporary
  run outputs.
- Website deployment artifacts copied from the website lane.

## Audit Decisions

| Area | Public decision |
| --- | --- |
| Aggregate curve artifacts | Removed `answer_pass3_cost_curve.*` and `effort_curve.*`; the release keeps `summary.csv` and `report.md` as the aggregate evidence. |
| Aggregate report provenance | `reports/v0_2/aggregate/report.md` is the v0.2 public aggregate summary dated 2026-06-18. |
| Manual adjustments | Reported only as aggregate adjustment counts; private source rows and raw completions stay out of the public repo. |
| Probe helpers | Retired from the public surface; provider smoke/probe scripts belong in the internal lane. |
| Paper V1 cost helper | Retired from the public surface; old paper dry-run cost helpers are not part of the v0.2 source release. |
| Empty release package | Retired from the public package. |
| Generators | Retired from the public surface; public examples are materialized data, not regenerated from private pools. |
| Analysis helpers | Kept only where they support public aggregate inspection and source-level reproducibility. |
| Model panel | `configs/model_panels/models_v0_2_public.yaml` is included because it is public configuration metadata, not private data. |
| Documentation | Active public docs are limited to benchmark reference, website boundary, release metadata, and this public-surface record; narrative positioning lives on the launch site and in the internal lane. |
| Registries | `configs/registries/model_registry_v1.yaml` is included because public model metadata is necessary to interpret aggregate rows. Pre-final thinking-panel planning metadata is internal and not part of the published result. |
| Tests | Tests are scoped to public package behavior, public datasets, scoring, registries, hygiene, and release-bundle guards. |
| Package layout | The `obviousbench/` package remains nested in the repository so users can install and import it normally. |

Ignored local remnants such as `.venv/`, `node_modules/`, internal-only docs
folders, old deleted helper directories, and local cache folders may exist in a
working checkout. They must remain ignored and must not be staged.
