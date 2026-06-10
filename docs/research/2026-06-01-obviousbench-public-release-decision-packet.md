---
title: ObviousBench Public Release Decision Packet
date: 2026-06-01
type: decision-record
status: blocked
---

# ObviousBench Public Release Decision Packet

This packet turns the release-side arXiv blockers into explicit
human decisions and draft file templates. It does not create a
`LICENSE`, `CITATION.cff`, `.zenodo.json`, publish a repository,
choose a license, or confirm arXiv metadata.

Overall status: BLOCKED

Summary: 5 ready, 1 need confirmation.

## Decision Matrix

| Decision | Status | Target artifact | Current state | Next action |
| --- | --- | --- | --- | --- |
| license selection | READY | LICENSE and arXiv metadata `license` | LICENSE present: yes; metadata license: CC BY 4.0 | None. |
| citation metadata | READY | CITATION.cff | CITATION.cff present and de-placeholdered: yes | None. |
| archive metadata | READY | .zenodo.json | .zenodo.json present and de-placeholdered: yes | None. |
| package license metadata | READY | pyproject.toml | project.license: Apache-2.0; license classifier present: yes | None. |
| public repository and artifact URLs | READY | arXiv metadata `repository_url` and `dataset_url` | repository_url: https://github.com/adamallcock/obviousbench (planned public release URL; confirm live before submission); dataset_url: https://huggingface.co/datasets/adamallcock/obviousbench (planned public dataset URL; confirm live before submission) | None. |
| submitter and final metadata confirmation | NEEDS-CONFIRMATION | arXiv metadata confirmation fields | false or unconfirmed fields: endorsement_checked; metadata_status: draft | Confirm submitter account, endorsement status, title/abstract match, and metadata status after the final PDF is inspected. |

## Draft File Templates

These are templates to apply only after the release decision is made.
Leave the hard public-release audit blocked until the real files are
filled with confirmed values.

### CITATION.cff

```yaml
cff-version: 1.2.0
message: "If you use ObviousBench, please cite the archived release."
title: "ObviousBench: Measuring Human-Trivial Failure Modes in Public-Facing Language Models"
version: "0.1.0"
date-released: "2026-06-01"
authors:
  - family-names: "TODO"
    given-names: "TODO"
repository-code: "TODO(confirm public repository URL)"
url: "TODO(confirm project or release URL)"
license: "TODO(confirm license)"
```

### .zenodo.json

```json
{
  "title": "ObviousBench: Measuring Human-Trivial Failure Modes in Public-Facing Language Models",
  "upload_type": "software",
  "description": "TODO(confirm release description after final paper artifacts are frozen)",
  "creators": [
    {"name": "TODO", "affiliation": "TODO"}
  ],
  "license": "TODO",
  "keywords": ["language-model-evaluation", "benchmark", "reliability"],
  "related_identifiers": []
}
```

### pyproject.toml

```toml
# Add after license is confirmed.
license = "TODO"
classifiers = [
  "License :: OSI Approved :: TODO",
]
```
