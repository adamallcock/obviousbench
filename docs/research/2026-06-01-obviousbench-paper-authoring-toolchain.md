---
title: ObviousBench Paper Authoring Toolchain
date: 2026-06-01
type: decision-record
status: accepted
---

# ObviousBench Paper Authoring Toolchain

## Decision

Write the arXiv article in LaTeX, with `paper/main.tex` as the source of record.

Use Markdown for planning, progress tracking, and human-readable research notes.
Do not use R Markdown, Quarto, Typst, or Pandoc as the canonical arXiv source
for this paper unless the toolchain decision is revisited later.

## Why LaTeX

arXiv's submission flow is built around TeX/LaTeX source. The arXiv TeX
submission guide says TeX submissions are automatically processed, that authors
must inspect the resulting PDF, and that TeX source bundles should include only
the files required to process the paper. It also notes that PDFLaTeX is
supported and that `.bib` or `.bbl` files are required when using BibTeX or
Biber.

Sources:

- arXiv TeX/LaTeX submission guide:
  <https://info.arxiv.org/help/submit_tex.html>
- arXiv submission overview:
  <https://info.arxiv.org/help/submit/index.html>
- arXiv accepted submission formats:
  <https://info.arxiv.org/help/submit_formats.html>

For a `cs.CL`-positioned paper, the ACL style files are the relevant conference
template family, but this project is not yet targeting a specific ACL venue.
The official ACL style repository says ACL conference submissions must use
official ACL style templates. For an arXiv-first preprint, a conservative
`article`-class LaTeX draft is lower friction; it can be converted to ACL style
later if there is a venue target.

Source:

- ACL official style files: <https://github.com/acl-org/acl-style-files>

## Why Not R Markdown As Source Of Record

R Markdown can be useful for analysis-heavy reports, but it is not the
standard source format expected by arXiv. It would add an R/Pandoc dependency
between the paper and the actual source arXiv processes. This workspace has R
installed, but not `pandoc`, `quarto`, `latexmk`, `pdflatex`, or `tectonic`.

R or notebooks may still be useful for figure generation after the paper data
is frozen. They should write explicit assets under `paper/figures/` and
`paper/tables/`, not become the canonical manuscript.

## Why Not Quarto As Source Of Record

Quarto manuscripts are useful for scholarly writing with notebooks and
multi-format outputs. Quarto's documentation says manuscript projects can use
one or more notebooks or `.qmd` files and produce multiple formats including
LaTeX or Word. That is useful for a companion website or reproducible analysis
package, but it introduces an extra conversion layer.

Source:

- Quarto manuscripts: <https://quarto.org/docs/manuscripts/>

Given that Quarto is not installed here and arXiv ultimately processes LaTeX,
the safer path is direct LaTeX for the paper and Python-generated `.tex` tables
for reproducible quantitative content.

## Working Standard

Use this structure:

```text
paper/
  README.md
  main.tex
  references.bib
  sections/
    01_introduction.tex
    02_related_work.tex
    03_benchmark.tex
    04_data_review.tex
    05_scoring_protocol.tex
    06_results.tex
    07_analysis.tex
    08_discussion.tex
    09_limitations_ethics_reproducibility.tex
    appendix.tex
  tables/
    dataset_composition.tex
    scorer_gold_coverage.tex
    readiness_gates.tex
  figures/
    README.md
  Makefile
```

Authoring rules:

- Keep claim-bearing result numbers in generated tables, not hand-edited prose.
- Use `\input{...}` section files so reviews can happen section by section.
- Use `\obtodo{...}` for known paper blockers.
- Keep expensive model sweeps out of the build scripts.
- Make `make assets` cheap and deterministic.
- Make `make pdf` optional; it should fail clearly if LaTeX is unavailable.
- Do not include raw provider logs, credentials, private prompts, or large
  ignored result directories in the arXiv source bundle.

## Revisit Triggers

Revisit this decision if:

- the paper targets a specific conference with a required template,
- Quarto or Pandoc becomes part of the repo's normal toolchain,
- a collaborator strongly prefers `.qmd` or `.Rmd`,
- a companion manuscript website becomes a first-class deliverable.
