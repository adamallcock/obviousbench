---
title: Website Boundary
date: 2026-06-24
type: reference
status: current
---

# Website Boundary

The canonical public launch site is:

- [https://obviousbench.com](https://obviousbench.com)

This repository should link to the website prominently, but it should not copy
the full website source as a second editing surface. In particular, do not
vendor website build directories, launch-site HTML, or deployed website assets
into this repository. The public repository is the source/data companion:
benchmark code, public examples, model metadata, release aggregate CSVs, and
reproducibility documentation.

The website is the narrative and interactive visualization surface. It can be
built from the same public-safe aggregate data, but the deployable site source
belongs in the website release lane so prose, styling, and deployment are not
maintained in two places.

It is fine for this repository to include short release summaries, README links,
benchmark-card language, and generated release notes that point to the website.
It should not include a second copy of the long-form website essay or chart
application unless that content is intentionally moved into the public-source
release process.

For that reason, this repository should expose durable, linkable public
materials that the website can reference:

- public examples under `data/public_examples/`
- model/config metadata under `configs/`
- aggregate v0.2 result files under `reports/v0_2/aggregate/`
- release metadata under `docs/release/v0_2/generated/`

Public-safe aggregate result files may be linked from both places. Private
held-out prompts, raw completions, provider logs, private review HTML, and
item-level private outcomes must not be copied into either the public repository
or the public website.

Recommended link pattern:

- Website links to GitHub for public examples, aggregate CSVs, release metadata,
  license, and citation files.
- GitHub links to [https://obviousbench.com](https://obviousbench.com) as the
  canonical narrative, interactive chart, and public explanation surface.
