---
title: ObviousBench arXiv Submission Metadata
date: 2026-06-01
type: review
status: draft
metadata_status: draft
article_title: "ObviousBench: Where Obvious Tasks Still Break Language Models"
authors:
  - "Adam Allcock (Independent Researcher)"
contact_email: "adamallcock@gmail.com"
abstract: >-
  ObviousBench is a compact benchmark for short prompts that should be easy for
  a careful human but still produce visible failures in public-facing language
  models. The v0.1 paper_v1 split contains 224 questions across character
  counting, spelling transforms, small arithmetic, ordering, negation, format
  compliance, word counting, and simple constraint awareness. Each item has an
  objective target and a deterministic scorer. We report a frozen 2026-06-03
  evidence snapshot covering 223 model/settings rows. The paper does not report
  a measured human baseline for v0.1; human-triviality is treated as an
  item-design target supported by reviewed item cards, answer derivations, and
  scorer-gold artifacts.
primary_category: "cs.CL"
secondary_categories:
  - "cs.AI"
  - "cs.LG"
license: "CC BY 4.0"
comments: "Public repository, website, dataset, and archive links must be live before submission."
repository_url: "https://github.com/adamallcock/obviousbench (planned public release URL; confirm live before submission)"
project_url: "https://obviousbench.com (planned public project URL; confirm release page is live before submission)"
dataset_url: "TBD"
proposed_repository_url: "https://github.com/adamallcock/obviousbench"
proposed_project_url: "https://obviousbench.com"
proposed_dataset_url: "TBD"
proposed_archive_url: "Zenodo DOI for the public GitHub release, to be minted after release"
ai_tool_disclosure: "AI coding and writing-assistance tools were used during code development, artifact generation, literature triage, drafting, editing, and consistency checks. The author reviewed the manuscript and release artifacts and takes responsibility for all content, analyses, citations, and claims."
submitter_registered_author: true
endorsement_checked: false
endorsement_required: true
endorsement_required_for:
  - "cs.CL"
  - "cs.AI"
submitter_is_author_or_authorized_proxy: true
title_and_abstract_checked: true
---

# ObviousBench arXiv Submission Metadata

This note is the human-confirmed metadata handoff for the arXiv upload form.
It intentionally starts as `draft`; the submission preflight should not pass
until `status` and `metadata_status` are changed to `confirmed`, placeholders
are removed, and all boolean confirmation fields are true.

Official arXiv references checked for this template:

- https://info.arxiv.org/help/submit/index.html
- https://info.arxiv.org/help/prep.html
- https://info.arxiv.org/help/license/index.html
- https://arxiv.org/category_taxonomy

Submission-specific decisions still required:

- Obtain an arXiv endorsement. The submitter checked arXiv and endorsement is
  required for both `cs.CL` and `cs.AI`; do not save endorsement codes in the
  repository.
- Confirm whether arXiv accepts the selected category set: primary `cs.CL`,
  cross-lists `cs.AI` and `cs.LG`.
- Confirm final public repository, dataset, and archive links are live.
- Confirm whether the Hugging Face dataset URL remains
  `https://huggingface.co/datasets/adamallcock/obviousbench` or changes before
  public release.
- Reconfirm final title and abstract exactly match the reviewed manuscript
  immediately before submission.

## Current Metadata Decisions

| Field | Current decision | Notes |
| --- | --- | --- |
| Author | Adam Allcock | Single-author paper. |
| Affiliation | Independent Researcher | Use the current affiliation only. Do not list inactive education or employer affiliations. |
| Contact | `adamallcock@gmail.com` | Use in the PDF unless a project alias is created before submission. |
| Submitter | Adam Allcock | Registered arXiv account exists and the submitter is the author. |
| Title | ObviousBench: Where Obvious Tasks Still Break Language Models | Must match `paper/main.tex` at submission time. |
| Primary category | `cs.CL` | Recommended fit because comparable language-model evaluation benchmarks such as BIG-bench, HELM, and SWE-bench use `cs.CL` primary. |
| Cross-lists | `cs.AI`, `cs.LG` | Recommended cross-lists for AI-evaluation and model-evaluation relevance. Add `cs.SE` only if the paper is reframed around software-engineering/coding tasks. Moderators may remove inappropriate cross-lists. |
| arXiv paper license | CC BY 4.0 | Open reuse with attribution. This choice is irrevocable for the submitted version. |
| AI tool disclosure | Included in the manuscript ethics/reproducibility section | Do not list AI tools as authors. |
| Endorsement | Required for `cs.CL` and `cs.AI` | Unique endorsement codes were received by email. Keep them out of Git and docs; forward the arXiv email to a qualified endorser. |

## Release Strategy

Recommended release layout:

- Keep this development repository private until it has been scrubbed.
- Create a clean public release repository for code, reviewed data, paper
  source, tests, and reproducibility scripts.
- Publish the dataset separately as a Hugging Face dataset repository with a
  dataset card and license metadata.
- Mint a Zenodo DOI from a tagged public GitHub release for archival citation.

Proposed public URLs, subject to account/namespace availability:

- Repository: `https://github.com/adamallcock/obviousbench`
- Dataset: `https://huggingface.co/datasets/adamallcock/obviousbench`
- Archive: Zenodo DOI generated from the public release tag.

Recommended licenses:

- arXiv paper: CC BY 4.0.
- Code/package: Apache-2.0.
- Dataset, item cards, and documentation: CC BY 4.0.

The public release should include `LICENSE` or clearly scoped license files,
`CITATION.cff`, `.zenodo.json`, a dataset card, and explicit citation text.
