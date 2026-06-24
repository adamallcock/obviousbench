# ObviousBench v0.2 Public Release Checklist

## Generated Artifact Notice

- Source config: `configs/releases/release_v0_2_0.yaml`
- Generator: `uv run --extra dev python scripts/release/build_v0_2_release_assets.py --config configs/releases/release_v0_2_0.yaml`
- Release date: `2026-06-18`
- Status: `local-publication-prep`
- Public/private boundary: excludes private held-out prompts, raw outputs,
  item-level private outcomes, private review HTML, and attempt-level outcomes.


## Local Gates

- [x] Final v0.2 private pass^3 evidence selected.
- [x] Aggregate report and review summaries built.
- [x] Public-safe release surfaces generated locally.
- [x] Public bundle script/audit available for v0.2 aggregate release.
- [!] Public examples are currently a filtered safe placeholder;
  materialize a v0.2 public example manifest before final launch
  if the release should include a polished 64-row public split.

## Public Gates Still Pending

- [ ] Materialize and audit v0.2 public/dev/reserve split policy,
  or explicitly publish with aggregate-only private results plus
  filtered public examples.
- [ ] Publish or update the public repository target.
- [ ] Publish or update the dataset page with public examples
  and aggregate results.
- [ ] Publish project page URL.
- [ ] Replace local paths with public URLs in release copy.
- [ ] Rerun strict public bundle audit after final URL substitution.

No public launch copy should be posted before the pending gates are done.
