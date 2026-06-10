---
title: ObviousBench PDF Build Handoff
date: 2026-06-01
type: runbook
status: blocked
---

# ObviousBench PDF Build Handoff

This generated handoff records the local PDF build state, off-the-shelf
toolchain options, and final inspection ladder for the arXiv manuscript.
It does not install software, compile LaTeX, collect data, or run model
providers.

Overall status: BLOCKED

PDF audit status: BLOCKED

Source audit status: BLOCKED

Available LaTeX commands: `tectonic`

Available support commands: `brew`

## Current Blockers

- PDF build audit is blocked.
- Static source audit is blocked.
- Draft submission markers remain in TeX source.

## Recommended Toolchain

1. For the smallest local install, use Tectonic. The official Tectonic
   documentation describes it as a single executable that downloads
   TeX support files on demand. With Homebrew available, use:

   ```bash
   brew install tectonic
   ```

2. For maximum arXiv/TeX Live parity on macOS, use MacTeX. The official
   MacTeX distribution includes TeX, LaTeX, XeTeX, LuaTeX, and related
   tooling. With Homebrew available, use:

   ```bash
   brew install --cask mactex
   ```

3. If a system TeX Live install already exists, ensure `latexmk` or
   `pdflatex` is on PATH and rerun the audit before treating the build
   as reproducible.

## Build Ladder

```bash
make -C paper related-work
make -C paper assets
make -C paper source-audit
make -C paper pdf
make -C paper pdf-audit
make -C paper arxiv-audit
make -C paper preflight
```

The source audit is expected to stay blocked while draft markers remain.
A draft PDF may still be useful for layout review, but the final PDF
handoff is not ready until the source audit and PDF audit both pass.

## Inspection Checklist

- Title, author block, and abstract match the final metadata note.
- Every table fits the page and preserves readable captions.
- Every figure renders and is not a placeholder shell.
- Bibliography and citation references resolve.
- `paper/main.log` has no fatal errors, undefined references, missing
  citations, or overfull boxes that affect readability.
- The rebuilt `paper/arxiv-src.tar.gz` excludes local logs, raw provider
  outputs, credentials, private prompts, and generated caches.

## Stop Rules

- Do not mark the source bundle upload-ready while this handoff is
  blocked.
- Do not use a hand-built PDF as evidence unless `make -C paper pdf-audit`
  has been rerun after that build.
- Do not replace claim blockers just because the PDF compiles; claim
  blockers require human-baseline, final-result, metadata, or release
  evidence.

## Source Notes

- Tectonic install docs: <https://tectonic-typesetting.github.io/book/latest/installation/>
- MacTeX project: <https://tug.org/mactex/>
- arXiv TeX submission help: <https://info.arxiv.org/help/submit_tex.html>

## Audit Inputs

- PDF audit: `docs/research/2026-06-01-obviousbench-paper-pdf-build-audit.md` (3 passed, 1 failed.)
- Source audit: `docs/research/2026-06-01-obviousbench-paper-source-audit.md` (5 passed, 1 failed.)
