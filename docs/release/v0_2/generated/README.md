---
title: ObviousBench v0.2.0 Local Release Surfaces
date: 2026-07-31
type: release
status: local-prep
---

## Generated Artifact Notice

- Source config: `configs/releases/release_v0_2_0.yaml`
- Generator: `uv run --extra dev python scripts/release/build_v0_2_release_assets.py --config configs/releases/release_v0_2_0.yaml`
- Release date: `2026-07-31`
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
| Measured model/config rows | 453 |
| Headline model/config rows | 445 |
| Diagnostic duplicates excluded from headline rows | 7 |
| Complete headline rows | 445 |
| Attempts | 195696 |
| Scored attempts | 195696 |
| Estimated cost | $210.93 |
| Headline cost | $204.28 |
| Primary metric | non-strict answer pass^3 |

## Generated Files

- `release-metadata.json`
- `github-release-notes.md`
- `huggingface-dataset-card.md`
- `project-page.md`
- `launch-essay-draft.md`
- `background-and-rhetoric.md`
- `interactive-results.html`
- `model-size-review.csv`
- `social-snippets.md`
- `public-release-checklist.md`
- `provenance.json`

## Source Evidence

- Results memo: `docs/research/2026-06-18-obviousbench-v0-2-final-no-minimaxm1-rhetoric-packet.md`
- Evidence packet: `docs/research/2026-06-18-obviousbench-v0-2-final-no-minimaxm1-evidence-packet.md`
- Sanity supplement: `docs/research/2026-06-18-obviousbench-v0-2-final-no-minimaxm1-sanity-supplement.md`
- Split inventory: `docs/research/2026-06-15-obviousbench-v0-2-split-inventory-and-question-supply.md`
- Aggregate report: copied into the public bundle under
  `reports/v0_2/aggregate/report.md` after bundle build.
