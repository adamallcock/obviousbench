---
language: en
license: cc-by-4.0
task_categories:
- text-generation
pretty_name: ObviousBench v0.2
---

## Generated Artifact Notice

- Source config: `configs/releases/release_v0_2_0.yaml`
- Generator: `uv run --extra dev python scripts/release/build_v0_2_release_assets.py --config configs/releases/release_v0_2_0.yaml`
- Release date: `2026-06-18`
- Status: `local-publication-prep`
- Public/private boundary: excludes private held-out prompts, raw outputs,
  item-level private outcomes, private review HTML, and attempt-level outcomes.


# ObviousBench v0.2

This is draft dataset-card copy for the future public release.
The intended public bundle contains documentation, public examples,
and aggregate v0.2 private benchmark results. It does not include
private held-out prompts, private raw completions, private review
HTML, or private item-level outcome rows.

## Intended Use

ObviousBench measures whether models miss simple literal tasks that
humans normally regard as obvious, and how those failures change with
model size and test-time compute.

Appropriate uses include model-selection preflight, regression
testing, prompt/interface QA, and inspecting how much obvious-mistake
risk remains when thinking depth or model size is reduced.

Inappropriate uses include global model ranking, broad intelligence
claims, or treating one visible failure as proof that a model is
generally unsuitable.

## Final Private Snapshot

| Metric | Value |
|---|---|
| Private items | 144 |
| Model/config rows | 293 |
| Attempts | 126576 |
| Primary metric | non-strict answer pass^3 |
| Estimated cost | $131.00 |

## Public-Safety Boundary

The private evaluation set remains held out. Public materials should
use only public examples and aggregate private results.

## Scoring

The benchmark uses deterministic Python scorers. The headline metric
for v0.2 is non-strict answer pass^3: all three attempts for an
item/model/config must be answer-correct. Strict and format
correctness remain available as diagnostics.
