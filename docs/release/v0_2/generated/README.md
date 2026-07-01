---
title: ObviousBench v0.2.0 Local Release Surfaces
date: 2026-07-01
type: release
status: local-prep
---

## Generated Artifact Notice

- Source config: `configs/releases/release_v0_2_0.yaml`
- Generator: `uv run --extra dev python scripts/release/build_v0_2_release_assets.py --config configs/releases/release_v0_2_0.yaml`
- Release date: `2026-07-01`
- Status: `local-publication-prep`
- Public/private boundary: excludes private held-out prompts, raw outputs,
  item-level private outcomes, private review HTML, and attempt-level outcomes.


# ObviousBench v0.2.0 Local Release Surfaces

These files are local publication-prep artifacts. They do not publish
anything and they intentionally exclude private held-out prompts, raw
outputs, item-level private outcomes, and private review HTML.

## Snapshot

| Field | Value |
|---|---|
| Private items | 144 |
| Model/config rows | 301 |
| Complete rows | 301 |
| Attempts | 130032 |
| Scored attempts | 130032 |
| Estimated cost | $135.58 |
| Primary metric | non-strict answer pass^3 |

Canonical public launch site:
[https://obviousbench.com](https://obviousbench.com)

## Generated Files

- `README.md`
- `release-metadata.json`
- `github-release-notes.md`
- `provenance.json`

The launch-site narrative and interactive charts live at
[https://obviousbench.com](https://obviousbench.com). This repository
keeps the public-safe source data, configs, aggregate CSVs, and
reproducibility materials rather than duplicating the deployable website
source.

## Source Evidence

- Aggregate report: copied into the public bundle under
  `reports/v0_2/aggregate/report.md` after bundle build.
