---
title: ObviousBench arXiv Completion Roadmap
date: 2026-06-01
type: plan
status: blocked
---

# ObviousBench arXiv Completion Roadmap

This roadmap converts the current paper audits into an ordered path from
the local manuscript scaffold to a final arXiv submission. It is
generated from repository evidence and does not run model providers.

Publication mode: `preprint`

Overall status: BLOCKED

Phase summary: 4 passed, 1 blocked, 1 waiting.

## Operating Rule

The current fast-preprint package uses the passing evidence run; do not run additional provider calls unless intentionally creating a new evidence snapshot. Human-baseline collection is deferred and must not appear as measured evidence in the fast preprint.

## Phase Matrix

| Phase | Name | Status | Key evidence | Next action |
| ---: | --- | --- | --- | --- |
| 1 | Source scaffold and reproducibility inventory | PASS | Manuscript source: present at `paper/main.tex`. | Keep `paper/main.tex` as the canonical article source. |
| 2 | Human-baseline policy and deferred validation | PASS | Fast-preprint path selected: measured human-baseline collection is deferred until the benchmark split is frozen. | Remove empirical human-baseline claims from the manuscript. |
| 3 | Final model sweep authorization and execution | PASS | Result artifact audit: present at `docs/research/2026-06-01-paper-v1-final-result-artifact-audit.md`. | Do not run additional provider calls for the first draft unless a new evidence-run decision is made. |
| 4 | Result integration and claim closure | PASS | Internal research review: present at `docs/research/2026-06-01-obviousbench-arxiv-internal-review.md`. | Regenerate `paper/tables/main_results.tex`, `family_results.tex`, `provider_exclusions.tex`, and final figures from frozen comparison artifacts. |
| 5 | PDF, metadata, and arXiv source package | BLOCKED | Submission checklist: present at `docs/research/2026-06-01-obviousbench-arxiv-submission-checklist.md`. | Confirm author list, arXiv category, license, release links, submitter status, endorsement status, and AI-tool disclosure. |
| 6 | Public release and arXiv submission | WAITING | Metadata confirmed: no. | Tag or archive the exact code/data state used for the paper and record permanent repository/dataset URLs. |

## Phase 1: Source scaffold and reproducibility inventory

Status: PASS

Evidence:

- Manuscript source: present at `paper/main.tex`.
- arXiv report plan: present at `docs/research/2026-06-01-obviousbench-arxiv-report-plan.md`.
- blocker dashboard: present at `docs/research/2026-06-01-obviousbench-arxiv-blocker-dashboard.md`.
- reproducibility manifest: present at `docs/research/2026-06-01-obviousbench-paper-reproducibility-manifest.md`.
- Reproducibility manifest missing required artifacts: 0.

Actions:

- Keep `paper/main.tex` as the canonical article source.
- Regenerate `make -C paper report-tracker` and `make -C paper blocker-dashboard` after paper artifact changes.
- Regenerate `make -C paper repro-manifest` after generated paper artifacts are refreshed.
- Do not move provider logs or private material into the arXiv source bundle.

Exit criteria:

- `paper/main.tex`, section TeX files, generated tables, generated figures, and `paper/arxiv-src.tar.gz` are present.
- The blocker dashboard exists and classifies every known open gate.
- The reproducibility manifest reports 0 missing required artifacts.

## Phase 2: Human-baseline policy and deferred validation

Status: PASS

Evidence:

- Fast-preprint path selected: measured human-baseline collection is deferred until the benchmark split is frozen.
- Collection audit: present at `docs/research/2026-06-01-paper-v1-human-baseline-collection-audit.md`.
- Human-baseline operations packet: present at `docs/research/2026-06-01-paper-v1-human-baseline-operations.md`.

Actions:

- Remove empirical human-baseline claims from the manuscript.
- Describe human-triviality as a design target supported by reviewed item cards, answer derivations, ambiguity notes, and deterministic scorer-gold coverage.
- Keep participant packets and threshold tooling as future validation artifacts, not blockers for the fast preprint.

Exit criteria:

- `make -C paper readiness-preprint` passes.
- The manuscript does not report human accuracy, response-time statistics, or core-H0 thresholds.
- Human-baseline collection is listed as future work or appendix infrastructure rather than completed evidence.

## Phase 3: Final model sweep authorization and execution

Status: PASS

Evidence:

- Result artifact audit: present at `docs/research/2026-06-01-paper-v1-final-result-artifact-audit.md`.
- Final evidence-run artifacts pass. Planned model rows: 234.

Actions:

- Do not run additional provider calls for the first draft unless a new evidence-run decision is made.
- Use the passing evidence-run manifest, summaries, comparison CSVs, and report artifacts for manuscript claims.

Exit criteria:

- Result artifact audit passes.
- Paper tables and figures are regenerated from the same evidence run.

## Phase 4: Result integration and claim closure

Status: PASS

Evidence:

- Internal research review: present at `docs/research/2026-06-01-obviousbench-arxiv-internal-review.md`.
- Section tracker: present at `docs/research/2026-06-01-obviousbench-report-section-tracker.md`.
- Manuscript completeness audit: present at `docs/research/2026-06-01-obviousbench-manuscript-completeness-audit.md`.
- Final result artifact audit: present at `docs/research/2026-06-01-paper-v1-final-result-artifact-audit.md`.
- Summary: 7 passed, 0 failed.
- Overall status: PASS
- Summary: 11 passed, 0 blocked, 0 missing.
- Overall status: PASS
- Section tracker: 0 blocked section(s), 0 unresolved marker(s), 0 placeholder mention(s).

Actions:

- Regenerate `paper/tables/main_results.tex`, `family_results.tex`, `provider_exclusions.tex`, and final figures from frozen comparison artifacts.
- Run `make -C paper result-artifacts` before replacing result placeholders in TeX.
- Replace each `\claimblocked{...}` and `\obtodo{...}` marker only where the claim-evidence ledger points to supporting artifacts.
- Keep causal explanations in analysis/discussion framed as hypotheses unless a direct ablation supports them.
- Rerun `make -C paper internal-review`, `make -C paper claims`, `make -C paper manuscript-completeness`, and `make -C paper report-tracker` after prose changes.

Exit criteria:

- The claim audit reports 0 unresolved markers.
- The final result artifact audit passes.
- The manuscript completeness audit passes.
- The section tracker reports 0 blocked sections and 0 placeholder mentions.
- The internal research review reports 0 failed checks.

## Phase 5: PDF, metadata, and arXiv source package

Status: BLOCKED

Evidence:

- Submission checklist: present at `docs/research/2026-06-01-obviousbench-arxiv-submission-checklist.md`.
- Submission handoff: present at `docs/research/2026-06-01-obviousbench-arxiv-submission-handoff.md`.
- PDF build audit: present at `docs/research/2026-06-01-obviousbench-paper-pdf-build-audit.md`.
- Submission metadata note: present at `docs/research/2026-06-01-obviousbench-arxiv-submission-metadata.md`.
- Summary: 11 passed, 1 failed.
- Upload readiness: NO
- Summary: 2 passed, 4 failed.
- Overall status: PASS
- Summary: 4 passed, 0 failed.

Actions:

- Confirm author list, arXiv category, license, release links, submitter status, endorsement status, and AI-tool disclosure.
- Install or use a LaTeX-enabled environment with `latexmk`, `pdflatex`, or `tectonic` and run `make -C paper pdf`.
- Inspect the generated PDF for table overflow, figure rendering, citation resolution, and abstract/title consistency.
- Run `make -C paper pdf-audit` after every PDF build and resolve toolchain, PDF artifact, source, and log blockers.
- Run `make -C paper arxiv-audit` and `make -C paper preflight` after the final PDF/source build.
- Run `make -C paper submission-handoff` before upload and treat `Upload readiness: NO` as a hard stop.

Exit criteria:

- `paper/main.pdf` exists and has been inspected.
- The PDF build audit passes.
- The source bundle audit passes with only upload-safe files.
- The submission checklist reports 0 failed checks.
- The submission handoff reports `Upload readiness: YES`.

## Phase 6: Public release and arXiv submission

Status: WAITING

Evidence:

- Metadata confirmed: no.
- Metadata TODO placeholders present: no.
- Public release artifact audit: present at `docs/research/2026-06-01-obviousbench-public-release-artifact-audit.md`.
- Public release decision packet: present at `docs/research/2026-06-01-obviousbench-public-release-decision-packet.md`.
- Earlier roadmap phases still open: yes.
- Overall status: BLOCKED
- Summary: 5 passed, 1 failed.
- Overall status: BLOCKED
- Summary: 5 ready, 1 need confirmation.

Actions:

- Tag or archive the exact code/data state used for the paper and record permanent repository/dataset URLs.
- Run `make -C paper release-packet` and resolve every explicit license, citation, archive, URL, and submitter decision.
- Run `make -C paper release-audit` and resolve license, citation, archive metadata, and public URL blockers.
- Confirm the arXiv submitter is an author or authorized proxy and has any needed endorsement for the selected category.
- Submit the final TeX source bundle and matching metadata after all checks pass.
- After announcement, record the arXiv identifier and update release links without changing reported results.

Exit criteria:

- Repository and dataset/artifact URLs are public and immutable enough for citation.
- The public release decision packet reports 0 decisions needing confirmation.
- The public release artifact audit passes.
- arXiv metadata is confirmed and matches the final PDF exactly.
- The arXiv submission is uploaded from the final audited source bundle.

## Final Verification Ladder

Run this ladder only after the relevant inputs exist; failing commands
before that point should be treated as evidence, not hidden.

```bash
make -C paper readiness-preprint
make -C paper result-artifacts
# Provider calls are already audited for this evidence snapshot.
# Rerun providers only when intentionally creating a new evidence run.
make -C paper assets
make -C paper claim-ledger
make -C paper claims
make -C paper manuscript-completeness
make -C paper report-tracker
make -C paper blocker-dashboard
make -C paper arxiv-package
make -C paper arxiv-audit
make -C paper metadata
make -C paper release-packet
make -C paper pdf-audit
make -C paper release-audit
make -C paper submission-handoff
make -C paper preflight
make -C paper internal-review
make -C paper repro-manifest
```
