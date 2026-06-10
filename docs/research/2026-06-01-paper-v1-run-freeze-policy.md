---
title: Paper V1 Run Freeze Policy
date: 2026-06-01
type: runbook
status: draft
---

# Paper V1 Run Freeze Policy

This policy defines what must stay fixed for a claim-bearing ObviousBench paper
run, and how retries are allowed.

## Frozen Inputs

| Surface | Frozen value |
| --- | --- |
| Paper item manifest | `data/splits/paper_v1_manifest.jsonl` |
| Paper dataset | `data/barrages/hard_obvious_8x10_seed_20260531.jsonl` |
| Item count | 80 |
| Prompt policy | `native_provider_no_system_prompt_v0` |
| Scoring policy | `deterministic_v0` |
| Scorer gold evidence | `tests/fixtures/scorer_gold` |
| Paper model panel | `configs/paper_v1_model_panel.yaml` |
| Broad configuration panel | `configs/model_thinking_settings_v1.yaml` |
| Per-request provider timeout | `--timeout=60` for the paper panel unless explicitly revised before the run |
| Inspect model API retries | `--max-retries=0` for smoke/final paper-panel runs; wrapper-level exact-entry retries are recorded separately |
| Final paper raw root | `results/raw/paper-v1-final-high-cap` |
| Final paper summary root | `results/summaries/paper-v1-final-high-cap` |

## Readiness Profiles

Preprint readiness:

- `make -C paper readiness-preprint` must pass.
- Human baseline rows may be absent.
- The paper must not report empirical human accuracy, response time, or
  model-versus-human gaps.
- Human-trivial language must be grounded in item cards, derivations, ambiguity
  reviews, and scorer-gold evidence.

Strict readiness:

- `make -C paper readiness` must pass.
- `data/human_baseline/paper_v1.csv` must contain real participant rows that
  satisfy the human-baseline thresholds.
- Human results may be reported only after this profile passes.

## Smoke Gate

Before a claim-bearing final run, run a one-sample smoke with cache disabled:

```bash
.venv/bin/python scripts/run_model_panel.py \
  --panel configs/paper_v1_model_panel.yaml \
  --dataset data/barrages/hard_obvious_8x10_seed_20260531.jsonl \
  --raw-root results/raw/paper-v1-smoke-10k-cap \
  --summary-root results/summaries/paper-v1-smoke-10k-cap \
  --manifest-out configs/paper_v1_smoke_manifest.csv \
  --status-out results/summaries/paper-v1-smoke-10k-cap/status.jsonl \
  --mode smoke \
  --sample-id obviousbench.char_count.en.v0.public.000040 \
  --no-cache \
  --no-skip-completed \
  --cost none
```

A smoke entry passes only if its summary has at least one scored sample. A
provider-error summary with zero scored samples is a failed smoke, even if
Inspect and rescore wrote output files.

## Final Run Policy

For a paper-final run:

- Use a clean raw root and summary root.
- Use the frozen dataset and model/config panel exactly as written.
- Disable cache for the first claim-bearing run unless the user explicitly
  chooses a cached reproducibility run instead of a fresh-current run.
- Record the exact command, timestamp, git diff state, model panel, and status
  ledger.
- Do not cherry-pick successful duplicate runs into a leaderboard.
- Do not rank incomplete models against complete runs.

Preferred execution wrapper:

```bash
.venv/bin/python scripts/run_model_panel.py \
  --panel configs/paper_v1_model_panel.yaml \
  --dataset data/barrages/hard_obvious_8x10_seed_20260531.jsonl \
  --raw-root results/raw/paper-v1-final-high-cap \
  --summary-root results/summaries/paper-v1-final-high-cap \
  --manifest-out configs/paper_v1_final_sweep_manifest.csv \
  --status-out results/summaries/paper-v1-final-high-cap/status.jsonl \
  --mode full \
  --no-cache
```

For the broader hundreds-of-configurations run, use the same wrapper with
`--panel configs/model_thinking_settings_v1.yaml` and separate output roots.

## Retry Policy

Allowed retries:

- Exact same frozen entry after a transient transport/provider outage.
- Exact same entry after a provider-refusal retry handled by the existing
  Inspect wrapper.
- Exact same entry after local infrastructure repair, such as a missing optional
  provider dependency.

Disallowed retries:

- Changing prompts, answer keys, scorer logic, item selection, or generation
  settings after seeing final model results.
- Replacing a failed model alias with a new alias without documenting it as a
  panel change.
- Combining outputs from different datasets, scorer revisions, or prompt
  policies in the same claim-bearing table.

If a provider retires or removes an alias before the final run, mark the entry
as unavailable in the status ledger and decide before inspecting result quality
whether to replace it. Replacement requires updating the model panel, cost
estimate, coverage refresh, and run plan.

## Exclusions

Provider errors and timeouts are retried under the configured provider-refusal
policy. After retries are exhausted, final provider errors and timeouts count as
incorrect scored attempts and must also be reported as counts and rates. Entries
with no completed final attempts are not eligible for leaderboard ranking.

## Post-Run Outputs

After all accepted model runs:

```bash
.venv/bin/python -m obviousbench.cli build-comparison \
  --manifest configs/paper_v1_final_sweep_manifest.csv \
  --out results/summaries/paper-v1-final-high-cap/comparison \
  --manual-xai-costs
```

```bash
.venv/bin/python -m obviousbench.cli build-report \
  --comparison-dir results/summaries/paper-v1-final-high-cap/comparison \
  --out docs/reports/2026-06-01-paper-v1-final-high-cap-sweep \
  --generated-on 2026-06-01 \
  --title "ObviousBench Paper V1 Final Sweep"
```

Then regenerate paper tables and figures from the final comparison artifacts.
