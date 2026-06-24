---
title: Configuration Index
date: 2026-06-16
type: index
status: active
---

# Configuration Index

Configuration files are grouped by the public workflow that owns them. Prefer
these lanes over adding more root-level YAML or CSV files under `configs/`.

## Active Lanes

- `configs/model_panels/`: example model/config panels for running the public
  example set.
- `configs/registries/`: public model metadata, pricing, thinking-setting, and
  display registries used by reports and release views.

Historical private release configs, private run policies, dataset split recipes,
and paper/arXiv working configs are intentionally absent from this public
preview. They live in the internal repository and feed this repo through a
public export process.

## Rules

- Do not store API keys, provider balances, raw private outputs, private
  held-out prompts, item-level private outcomes, or local cache pointers in
  config.
- Add reusable public model matrices under `configs/model_panels/`.
- Add reusable public model metadata under `configs/registries/`.
