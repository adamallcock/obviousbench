---
title: ObviousBench arXiv Submission Handoff
date: 2026-06-01
type: runbook
status: blocked
---

# ObviousBench arXiv Submission Handoff

This generated handoff describes the current upload packet and the
checks that must pass before using arXiv's submission form. It does not
submit anything, compile LaTeX, publish releases, or run providers.

Upload readiness: NO

Summary: 2 passed, 4 failed.

## Upload Packet

- Source bundle: `paper/arxiv-src.tar.gz`
- Metadata note: `docs/research/2026-06-01-obviousbench-arxiv-submission-metadata.md`
- Source-bundle audit: `docs/research/2026-06-01-obviousbench-arxiv-source-bundle-audit.md`
- PDF audit: `docs/research/2026-06-01-obviousbench-paper-pdf-build-audit.md`
- Submission preflight: `docs/research/2026-06-01-obviousbench-arxiv-submission-checklist.md`
- Public release audit: `docs/research/2026-06-01-obviousbench-public-release-artifact-audit.md`
- Blocker dashboard: `docs/research/2026-06-01-obviousbench-arxiv-blocker-dashboard.md`

## Readiness Checks

| Check | Status | Evidence | Next action |
| --- | --- | --- | --- |
| source bundle | PASS | paper/arxiv-src.tar.gz exists (227898 bytes); bundle audit PASS with 64 member(s), 0 issue(s). | None. |
| PDF build and inspection | PASS | 4 passed, 0 failed. | None. |
| submission preflight | FAIL | 11 passed, 1 failed. | Rerun `make -C paper preflight` after upstream blockers are fixed. |
| public release artifacts | FAIL | 5 passed, 1 failed. | Confirm final release metadata and endorsement status; then set metadata status fields to confirmed. |
| arXiv metadata | FAIL | metadata_status must be confirmed; status must be confirmed; endorsement_checked must be true | Confirm final title, abstract, authors, category, license, release links, submitter status, endorsement status, and AI-tool disclosure. |
| blocker dashboard | FAIL | 8 passed, 3 blocked, 0 waiting. | Use `make -C paper blocker-dashboard` to drive remaining fixes. |

## Upload Rule

Do not upload to arXiv until this handoff says `Upload readiness: YES`,
the final PDF has been visually inspected, and the metadata note exactly
matches the final PDF and public release links.
