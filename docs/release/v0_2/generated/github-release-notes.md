# ObviousBench v0.2.0 Draft Release Notes

## Generated Artifact Notice

- Source config: `configs/releases/release_v0_2_0.yaml`
- Generator: `uv run --extra dev python scripts/release/build_v0_2_release_assets.py --config configs/releases/release_v0_2_0.yaml`
- Release date: `2026-07-08`
- Status: `local-publication-prep`
- Public/private boundary: excludes private held-out prompts, raw outputs,
  item-level private outcomes, private review HTML, and attempt-level outcomes.


Start with the public launch site:
[https://obviousbench.com](https://obviousbench.com). It is the canonical
release essay, interactive chart, and public results surface. This repository
is the public source/data companion for code, public examples, aggregate CSVs,
license, citation, and reproducibility materials.

Status: local prep only. Do not publish until repository visibility,
dataset publication, website link checks, and bundle-audit gates are
complete.

## What Is ObviousBench?

ObviousBench is a compact reliability benchmark for mistakes users
notice immediately: letter counts, spelling transforms, small
arithmetic, ordering, negation, format compliance, word counting,
and simple constraint awareness.

The benchmark is intentionally narrow. It is not a general
intelligence score and it is not a shame board. It is a preflight
surface for checking whether a model/configuration still makes
obvious literal mistakes before those mistakes reach users.

## v0.2 Headline

The v0.2 private pass^3 snapshot has the desired shape: top
model/config rows saturate or near-saturate the benchmark, while
smaller, no-thinking, or lower-test-time-compute rows still fail
visibly. That means the tasks are solvable by sufficiently capable
systems, and still useful for measuring obvious-mistake risk below
the top end.

## Evidence Shape

| Metric | Value |
|---|---|
| Private held-out items | 144 |
| Model/config rows | 312 |
| Included headline rows | 312 |
| Attempt rows | 134784 |
| Scored attempts | 134784 |
| Estimated cost | $142.87 |

Rows affected by provider unavailability or route-level blank-output
failures are excluded from headline comparisons rather than treated
as model-quality evidence.

The canonical public narrative and interactive charts are on
[obviousbench.com](https://obviousbench.com). This repository is the
public source/data companion for those results.

## Release Contents

- Public example items for orientation, documentation, and smoke
  testing.
- Public-safe aggregate private-set results at model/configuration
  level.
- Public model/config panel and registry metadata.
- Runnable package code, deterministic scoring policy, methodology,
  license, and citation metadata.

## How To Read The Results

A high score means the model/configuration reliably answers these
simple tasks under the frozen snapshot. A low score does not mean
the model is generally bad; it means this configuration is more
likely to make visible obvious mistakes unless product safeguards,
more capable models, or more test-time compute are used.

## Caveats

- Do not claim a global model ranking.
- Do not claim measured human accuracy or response time.
- Do not publish private held-out prompts, raw outputs, item-level
  private outcomes, or private review HTML.
- Treat scores as a dated frozen snapshot, not permanent provider
  behavior.
