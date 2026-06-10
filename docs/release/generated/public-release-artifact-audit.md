---
title: ObviousBench Public Release Artifact Audit
date: 2026-06-01
type: review
status: blocked
---

# ObviousBench Public Release Artifact Audit

This audit checks the release-side artifacts needed before the arXiv
metadata can contain final public code and data links. It does not
publish a repository, choose a license, or upload data archives.

Overall status: BLOCKED

Summary: 5 passed, 1 failed.

| Check | Status | Evidence | Next action |
| --- | --- | --- | --- |
| public documentation | PASS | 7/7 required file(s) present. | None. |
| paper release data | PASS | 5/5 required file(s) present. | None. |
| license and citation files | PASS | LICENSE, CITATION.cff, and .zenodo.json are present. | None. |
| pyproject license metadata | PASS | project license metadata is present. | None. |
| public release URLs | PASS | repository_url and dataset_url are confirmed. | None. |
| release metadata confirmation | FAIL | metadata_status is not confirmed; false fields: endorsement_checked | Confirm submitter, endorsement, title/abstract, and metadata status. |

## Final Release Rule

Do not mark the arXiv metadata note as confirmed until this audit
passes, the repository and dataset/artifact URLs are public, and the
license and citation files match the final release decision.
