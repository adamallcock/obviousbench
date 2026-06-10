---
title: ObviousBench arXiv Blocker Dashboard
date: 2026-06-01
type: status
status: blocked
---

# ObviousBench arXiv Blocker Dashboard

This generated dashboard aggregates the current paper audits into a
single action view. It does not run model providers, collect human data,
choose release metadata, or compile the PDF.

Publication mode: `preprint`

Overall status: BLOCKED

Summary: 8 passed, 3 blocked, 0 waiting.

| Area | Status | Dependency | Evidence | Next action | Source |
| --- | --- | --- | --- | --- | --- |
| human-baseline validation | PASS | deferred validation | Deferred under the fast-preprint path; empirical human-baseline claims must be omitted or labeled as future validation. | Collect only after `paper_v1` is frozen for a strict benchmark version. | `docs/research/2026-06-01-paper-v1-human-baseline-collection-audit.md` |
| human-triviality thresholds | PASS | deferred validation | No core-H0 set is required for the fast-preprint path; human-trivial wording is a design target, not a measured result. | Run thresholding later only after audited human rows exist. | `docs/research/2026-06-01-paper-v1-human-baseline-threshold-audit.md` |
| final model sweep | PASS | provider run after readiness | Evidence-run artifacts are present for 234 planned model row(s). | None. | `docs/research/2026-06-01-paper-v1-final-result-artifact-audit.md` |
| final result artifacts | PASS | provider run after readiness | PASS planned model rows: 234 | None. | `docs/research/2026-06-01-paper-v1-final-result-artifact-audit.md` |
| claim and section closure | PASS | paper writing after evidence | 0 blocked section(s); 0 unresolved marker(s); 0 placeholder mention(s). | None. | `docs/research/2026-06-01-obviousbench-report-section-tracker.md` |
| source and PDF build | PASS | local writing and LaTeX environment | source: 6 passed, 0 failed. PDF: 4 passed, 0 failed. | None. | `docs/research/2026-06-01-obviousbench-paper-pdf-build-audit.md` |
| arXiv submission preflight | BLOCKED | aggregate release gate | 11 passed, 1 failed. | Rerun `make -C paper preflight` after claims, PDF, toolchain, release, and metadata blockers are resolved. | `docs/research/2026-06-01-obviousbench-arxiv-submission-checklist.md` |
| internal research review | PASS | aggregate research gate | 7 passed, 0 failed. | None. | `docs/research/2026-06-01-obviousbench-arxiv-internal-review.md` |
| manuscript completeness | PASS | paper writing after evidence | 11 passed, 0 blocked, 0 missing. | None. | `docs/research/2026-06-01-obviousbench-manuscript-completeness-audit.md` |
| public release artifacts | BLOCKED | release decision | 5 passed, 1 failed. | Confirm license, citation metadata, archive metadata, and public repository/dataset URLs before confirming arXiv metadata. | `docs/research/2026-06-01-obviousbench-public-release-artifact-audit.md` |
| submission metadata | BLOCKED | author/release decision | metadata_status confirmed: no; TODO placeholders: no; false fields: endorsement_checked. | Confirm final title, abstract, authors, category, release links, submitter status, endorsement status, and AI-tool disclosure. | `docs/research/2026-06-01-obviousbench-arxiv-submission-metadata.md` |

## Blockers By Dependency

### aggregate release gate

- arXiv submission preflight: Rerun `make -C paper preflight` after claims, PDF, toolchain, release, and metadata blockers are resolved.

### author/release decision

- submission metadata: Confirm final title, abstract, authors, category, release links, submitter status, endorsement status, and AI-tool disclosure.

### release decision

- public release artifacts: Confirm license, citation metadata, archive metadata, and public repository/dataset URLs before confirming arXiv metadata.
