---
title: ObviousBench arXiv Submission Checklist
date: 2026-06-01
type: review
status: blocked
---

# ObviousBench arXiv Submission Checklist

Overall status: BLOCKED

Summary: 11 passed, 1 failed.

| Check | Status | Evidence | Next action |
| --- | --- | --- | --- |
| dataset validation | PASS | 9 dataset file(s) passed strict validation. | None. |
| item-card review | PASS | 80 item cards are reviewed and placeholder-free. | None. |
| scorer-gold coverage | PASS | 6 used scorer(s) meet the 20-example threshold. | None. |
| human baseline | PASS | Human baseline is optional under the preprint profile; empirical human-triviality claims must be omitted or labeled as planned validation.; Human baseline CSV has no response rows. | None. |
| paper split manifest | PASS | Paper split manifest lists 80 item(s). | None. |
| paper claim blockers | PASS | 0 unresolved marker(s): 0 claimblocked, 0 obtodo. Audit: docs/research/2026-06-01-paper-claim-blocker-audit.md | None. |
| source bundle audit | PASS | 64 bundle member(s), 0 issue(s). Audit: docs/research/2026-06-01-obviousbench-arxiv-source-bundle-audit.md | None. |
| model panel freeze | PASS | Frozen model-panel file exists. Path: configs/paper_v1_combined_234_overline_attempt_scored_20260602_manifest.csv | None. |
| model cost estimates | PASS | Dry-run cost-estimate note exists. Path: docs/research/2026-06-01-paper-v1-model-panel-cost-estimates.md | None. |
| PDF build artifact | PASS | Local paper PDF exists. Path: paper/main.pdf | None. |
| LaTeX build toolchain | PASS | Available command(s): tectonic | None. |
| submission metadata confirmation | FAIL | metadata_status must be confirmed; status must be confirmed; endorsement_checked must be true | Confirm final abstract, authors, arXiv category, license, release links, submitter status, and AI-tool disclosure. |
