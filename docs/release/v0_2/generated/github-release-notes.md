# ObviousBench v0.2.0 Draft Release Notes

## Generated Artifact Notice

- Source config: `configs/releases/release_v0_2_0.yaml`
- Generator: `uv run --extra dev python scripts/release/build_v0_2_release_assets.py --config configs/releases/release_v0_2_0.yaml`
- Release date: `2026-06-18`
- Status: `local-publication-prep`
- Public/private boundary: excludes private held-out prompts, raw outputs,
  item-level private outcomes, private review HTML, and attempt-level outcomes.


Status: local prep only. Do not publish until repository, dataset,
project-page, and bundle-audit gates are complete.

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
| Model/config rows | 293 |
| Included headline rows | 293 |
| Attempt rows | 126576 |
| Scored attempts | 126576 |
| Estimated cost | $131.00 |

Rows affected by provider unavailability or route-level blank-output
failures are excluded from headline comparisons rather than treated
as model-quality evidence.

## What Changed Since v0.1

- v0.2 rebalances toward subfamilies that still separate modern
  models.
- Saturated low-signal forms are reduced or removed.
- Ambiguous wording found during private review was corrected before
  the final run.
- The primary headline metric is non-strict answer pass^3; strict
  and format correctness remain diagnostics.

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
