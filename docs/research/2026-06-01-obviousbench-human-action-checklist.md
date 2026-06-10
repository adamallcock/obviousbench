---
title: ObviousBench Human Action Checklist
date: 2026-06-01
type: runbook
status: draft
---

# ObviousBench Human Action Checklist

This checklist contains the remaining decisions and actions that require the
human owner. It excludes work Codex can do autonomously after a decision is
made, such as regenerating tables, rerunning audits, editing LaTeX, or building
the PDF.

## Current Local Setup

- LaTeX build path is installed: `tectonic 0.16.9`.
- PDF rendering path is installed: `pdftoppm 26.04.0` from Poppler.
- `make -C paper pdf` builds `paper/main.pdf`.
- `make -C paper pdf-audit` now reports 3 passed checks and 1 failed check.
- The remaining PDF-audit failure is the static source audit, because the
  manuscript still contains intentional `\claimblocked{...}` and `\obtodo{...}`
  markers.

## Human Decisions

1. Paper posture.
   - Selected for now: faster arXiv preprint.
   - Skip human collection for v1.
   - Treat human-triviality as a design and reviewer-adjudicated target
     supported by item cards, answer derivations, ambiguity notes, and
     scorer-gold tests.
   - Remove measured-human-baseline language from the manuscript.
   - Keep the strict benchmark paper as a future path if a frozen split needs
     empirical human-performance claims.
   - See
     `docs/research/2026-06-01-obviousbench-fast-human-baseline-options.md`
     for the fast-baseline options and precedent survey.

2. Confirm author metadata.
   - Author: Adam Allcock.
   - Affiliation: Independent Researcher.
   - Contact email: `adamallcock@gmail.com`.
   - AI-tool assistance disclosure: include a concise disclosure in the
     manuscript and do not list AI tools as authors.

3. Confirm arXiv submission details.
   - Primary category: `cs.CL`.
   - Proposed cross-lists: `cs.AI` and `cs.LG`, subject to arXiv acceptance and
     endorsement status.
   - Submitter account: registered and verified.
   - Whether endorsement is needed for the selected category remains to be
     checked during submission.
   - Submitter is the author.

4. Confirm release metadata.
   - Paper license: CC BY 4.0.
   - Code/package license: Apache-2.0.
   - Dataset and documentation license: CC BY 4.0.
   - Citation metadata: draft values recorded; final DOI and arXiv ID pending.
   - Create a Zenodo archive from a tagged public GitHub release.
   - Proposed public repository URL:
     `https://github.com/adamallcock/obviousbench`.
   - Proposed public dataset URL:
     `https://huggingface.co/datasets/adamallcock/obviousbench`.

5. Approve final model-sweep scope before any paid/provider run.
   - Confirm the final model panel.
   - Confirm provider accounts and credentials are available.
   - Confirm expected cost ceiling.
   - Confirm whether free/OpenRouter models should remain in the paper panel.
   - Confirm run date/time because model aliases and pricing can drift.

6. Future strict benchmark path only: collect the human baseline.
   - Use the participant packets already generated under `docs/research/`.
   - Keep answer keys private.
   - Fill `data/human_baseline/paper_v1_response_template.csv` with answer and
     seconds values only.
   - Do not hand-fill `correct`; the scoring helper does that.
   - Rerun the collection if the item set, instructions, answer key, scorer
     contract, or inclusion thresholds change.

7. Review the final PDF before upload.
   - Check title, author block, abstract, section order, tables, figures,
     references, and page breaks.
   - Confirm no private material or raw provider logs are included.
   - Confirm the PDF content matches the arXiv metadata exactly.

8. Upload or authorize upload to arXiv.
   - Use the final audited source bundle.
   - Record the arXiv identifier after announcement.
   - Update release links with the arXiv URL without changing reported results.

## Codex Can Continue After These Decisions

- Apply the chosen paper posture to the manuscript and readiness gates.
- Regenerate all paper reports and audits.
- Run the approved final model sweep only after explicit approval.
- Build final tables and figures from frozen results.
- Replace claim markers with evidence-backed prose.
- Rebuild and inspect the final PDF.
- Prepare the final arXiv source bundle and upload handoff.
