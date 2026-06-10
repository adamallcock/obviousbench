---
title: ObviousBench Paper Workspace
date: 2026-06-01
type: runbook
status: draft
---

# ObviousBench Paper Workspace

This directory contains the arXiv paper scaffold.

Source of record:

```text
paper/main.tex
```

The paper is intentionally LaTeX-first because arXiv processes TeX/LaTeX
source directly. Markdown remains the planning and progress format for this
repo, not the canonical article source.

## Cheap Commands

Build generated paper tables without running model sweeps:

```bash
make assets
```

This renders dataset, scorer, model-run, result, and figure assets from the
current release-prep evidence snapshot:
`results/summaries/paper-v1-8x28-current-223-final-20260603`.
The Makefile uses local Chrome's headless SVG-to-PDF path for readable figure
labels; the Python asset builder also has a dependency-light PDF fallback for
tests and minimal environments.

For repeatable figure review, use
`../notebooks/2026-06-01-obviousbench-paper-figures.ipynb`. The companion
workflow note is
`../docs/research/2026-06-01-obviousbench-paper-figure-workflow.md`. Figure
logic should be changed in `../obviousbench/research/paper_assets.py`, not by
manually editing generated PDFs.

Run the fast-preprint paper-readiness gate:

```bash
make readiness-preprint
```

This keeps dataset validation, item-card review, scorer-gold coverage, and the
paper manifest as hard gates, but treats human-baseline collection as optional
future validation. Use this path only while the manuscript avoids empirical
human accuracy, response-time, or model-versus-human claims.

Run the strict benchmark-readiness gate:

```bash
make readiness
```

This still requires real response rows in
`data/human_baseline/paper_v1.csv`. Use it only for a later strict benchmark
paper or revision that makes measured human-triviality claims.

Build the related-work positioning matrix:

```bash
make related-work
```

This renders the comparator matrix from `configs/paper_v1_related_work.yaml`,
checks that required citation keys are present in the bibliography and related
work section, and writes both a Markdown research artifact and a LaTeX table.
It does not search the web or make result claims.

Build the optional future human-baseline collection packet:

```bash
make human-baseline-packet
```

This generates randomized participant assignments, participant-facing prompt
packets, a preallocated response template, and a separate local answer key.
It does not collect real participant responses and is not a fast-preprint
blocker.

Audit collection completeness before scoring:

```bash
make human-baseline-audit
```

This checks participant progress, missing answers, invalid timings,
participant/item coverage, duplicate rows, and unknown response rows. It does
not score answers or run providers, and it remains blocked until every
preallocated response row has a real answer and parseable timing.

Build the human-baseline collection execution handoff:

```bash
make human-baseline-collection-handoff
```

This writes the operator-facing runbook for collecting the 400 real
answer/timing rows: participant progress, privacy boundaries, data-entry
contract, neutral participant instructions, command ladder, and stop rules. It
does not collect responses, score answers, or expose the answer key.

Score filled human-baseline responses:

```bash
make human-baseline-score
```

This scores the response template with the local answer key and writes a draft
scored CSV plus a scoring report. It remains blocked until real answers and
timings are filled in.

Audit scored rows against the predeclared human-triviality thresholds:

```bash
make human-baseline-thresholds
```

This writes item-level and family-level threshold CSVs plus a Markdown audit.
It classifies items as `core_h0`, `borderline`, `exclude`, or `no_data` without
collecting participant data or running providers. It remains blocked while the
scored draft contains no real participant answers.

Audit promotion readiness for the paper human-baseline CSV:

```bash
make human-baseline-promotion
```

This validates that collection, scoring, thresholding, and scored-row checks
all pass before any rows are copied into `data/human_baseline/paper_v1.csv`.
The make target is dry-run only. To apply after the report says `PASS`, run
`.venv/bin/python scripts/promote_human_baseline.py --apply`.

Build the human-baseline operations packet:

```bash
make human-baseline-ops
```

This coordinates collection, audit, scoring, thresholding, promotion, and
readiness gates in one handoff. It does not collect participant data, score
blank rows, or authorize final model arrays.

Build the editorial claim-evidence ledger:

```bash
make claim-ledger
```

This maps every `\claimblocked{...}` and `\obtodo{...}` marker to the exact
artifact evidence needed before the marker can be replaced.

Run a static TeX source audit without compiling:

```bash
make source-audit
```

This checks `\input{...}`, `\includegraphics{...}`, bibliography files,
citation keys, and unresolved submission markers. It complements `make pdf`;
it does not replace a real PDF build in a LaTeX-enabled environment.

Audit the current PDF build state without compiling:

```bash
make pdf-audit
```

This records whether a LaTeX toolchain is available, whether the static source
audit passes, whether `main.pdf` exists, and whether `main.log` contains fatal,
undefined-reference, or overfull-box markers. It is expected to stay blocked
until a real PDF has been built and inspected.

Build the PDF toolchain and inspection handoff:

```bash
make pdf-handoff
```

This records the current local PDF blockers, available off-the-shelf toolchain
commands, recommended Tectonic/MacTeX install paths, build ladder, inspection
checklist, and stop rules. It does not install software or compile LaTeX.

Build the source bundle and run the submission preflight:

```bash
make preflight
```

This currently fails intentionally while final claim-backed prose, a local PDF
build/audit surface, and final arXiv metadata confirmation are still
unresolved. Under the fast-preprint profile, missing human-baseline rows are
not a blocker as long as measured-human claims are absent.

Build the arXiv upload handoff:

```bash
make submission-handoff
```

This summarizes the upload packet, source bundle audit, PDF audit, preflight,
release audit, metadata note, and blocker dashboard. It does not submit
anything and should remain blocked until every upload-facing check passes.

Run the internal research-review gate:

```bash
make internal-review
```

This checks data claims against artifacts, claim blockers, result placeholders,
reproducibility commands, source safety, related-work coverage, and limitations
discipline.

Generate the dry-run final-sweep handoff without making provider calls:

```bash
make sweep-plan
```

This writes the per-model Inspect commands, per-model summarize commands, and
the comparison manifest for the future final paper sweep. It is not permission
to run the sweep while the readiness gate is still failing.

Audit the final result artifact contract:

```bash
make result-artifacts
```

This checks the expected per-model summary directories, comparison CSVs, and
generated report files for the current paper evidence run. It does not run
providers or rescore logs. For the first arXiv draft, it should pass against
the 2026-06-03 release-prep snapshot before result prose is treated as
claim-backed.

Audit the public release artifact contract:

```bash
make release-audit
```

This checks the release-side files needed for final arXiv metadata: public docs,
paper data artifacts, license/citation/archive metadata, package license
metadata, and confirmed repository/dataset URLs. It does not publish anything
or choose a license.

Build the public release decision packet:

```bash
make release-packet
```

This turns the release-side blockers into explicit human decisions and draft
templates for `LICENSE`, `CITATION.cff`, `.zenodo.json`, `pyproject.toml`
license metadata, and final public URLs. It does not create those release
files, choose a license, publish a repository, or confirm arXiv metadata.

Build the frozen paper analysis plan:

```bash
make analysis-plan
```

This renders and audits the reporting policy for primary metrics, secondary
metrics, confidence intervals, exclusions, tables, figures, and claim language.
For the first arXiv draft, it points at the 2026-06-03 release-prep evidence
snapshot and records human-baseline collection as deferred validation.

Audit manuscript component completeness:

```bash
make manuscript-completeness
```

This checks that the LaTeX source has every expected arXiv report component,
required citations, generated tables, generated figures, and no hidden
placeholder/claim-marker blockers. It does not collect data, run providers,
compile LaTeX, or publish anything.

Build the report section tracker:

```bash
make report-tracker
```

This scans the LaTeX manuscript section by section and records current status,
unresolved evidence dependencies, tables, figures, citations, and next editorial
actions.

Build the consolidated blocker dashboard:

```bash
make blocker-dashboard
```

This aggregates the current paper audits into a single action view grouped by
dependency type. It does not collect data, run providers, choose release
metadata, or compile the PDF.

Build the ordered completion roadmap:

```bash
make completion-roadmap
```

This converts the current paper audits into an ordered path from the local
manuscript scaffold to final arXiv submission. In the fast-preprint path,
human-baseline rows are deferred; blocked or waiting phases should instead
come from final model results, claim replacements, PDF build evidence,
release metadata, and submission metadata.

Build the reproducibility manifest:

```bash
make repro-manifest
```

This records SHA-256 hashes and byte sizes for paper source, generated paper
assets, frozen paper data, the evidence-run manifest, audit reports, and the
draft arXiv source bundle. It does not run provider calls or inventory provider
outputs.

Create the draft arXiv metadata handoff note if it is missing:

```bash
make metadata
```

The metadata note must remain `draft` until the final title, abstract, author
list, category, license, release links, submitter status, and AI-tool
disclosure have been confirmed.

## PDF Build

Build a local PDF if a LaTeX engine is installed:

```bash
make pdf
```

The current workspace has successfully built with `tectonic`. If `latexmk`,
`pdflatex`, or `tectonic` are unavailable on another machine, the scaffold and
generated tables can still be reviewed as source.

## Expensive Work Boundary

Do not run full model arrays from paper helpers. The paper helpers only inspect
local metadata, manifests, item cards, scorer-gold fixtures, and existing
result summaries.

Frozen model sweeps should happen only after:

- `paper_v1` item cards are reviewed,
- scorer-gold coverage and item-card evidence pass,
- `make -C paper readiness-preprint` passes for the paper split,
- model aliases and run settings are frozen.

For a later strict benchmark version that makes empirical human-triviality
claims, also require audited human-baseline evidence and a passing
`make -C paper readiness` run before model arrays.
