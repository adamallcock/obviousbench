---
title: ObviousBench arXiv Article Completion Plan
date: 2026-06-01
type: plan
status: draft
---

# ObviousBench arXiv Article Completion Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Move ObviousBench from the current proof-point and manuscript scaffold to a publication-ready arXiv article with audited data, reproducible tables, final results, and a clean source bundle.

**Architecture:** Keep the article LaTeX-first, generate claim-bearing tables from repository artifacts, and gate final model sweeps behind data-review and human-baseline readiness. The paper should remain claim-safe until the readiness audit passes and final sweeps are frozen.

**Tech Stack:** Python 3.11+, existing ObviousBench package, Inspect AI, deterministic scorers, local JSONL/YAML/CSV artifacts, LaTeX source under `paper/`, generated `.tex` tables, optional Jupyter notebooks for future analysis figures.

---

## Current State

Already present:

- `paper/main.tex` and section scaffold.
- `paper/references.bib`.
- `paper/Makefile`.
- `data/splits/paper_v1_manifest.jsonl` with 80 candidates.
- `scripts/audit_arxiv_readiness.py`.
- `scripts/build_paper_assets.py`.
- `paper/tables/dataset_composition.tex`.
- `paper/tables/scorer_gold_coverage.tex`.
- `paper/tables/readiness_gates.tex`.
- `docs/research/2026-06-01-obviousbench-arxiv-submission-checklist.md`.
- `docs/research/2026-06-01-obviousbench-arxiv-submission-handoff.md`.
- `docs/research/2026-06-01-obviousbench-arxiv-submission-metadata.md`.
- `docs/research/2026-06-01-obviousbench-arxiv-blocker-dashboard.md`.
- `docs/research/2026-06-01-obviousbench-public-release-artifact-audit.md`.
- `scripts/build_arxiv_submission_handoff.py`.
- `scripts/audit_manuscript_completeness.py`.
- `docs/research/2026-06-01-obviousbench-manuscript-completeness-audit.md`.
- `scripts/build_public_release_decision_packet.py`.
- `docs/research/2026-06-01-obviousbench-public-release-decision-packet.md`.
- `scripts/build_human_baseline_operations.py`.
- `docs/research/2026-06-01-paper-v1-human-baseline-operations.md`.
- `scripts/build_human_baseline_collection_handoff.py`.
- `docs/research/2026-06-01-paper-v1-human-baseline-collection-handoff.md`.
- `configs/paper_v1_related_work.yaml`.
- `scripts/build_related_work_matrix.py`.
- `docs/research/2026-06-01-obviousbench-related-work-positioning.md`.
- `paper/tables/related_work_positioning.tex`.
- `scripts/build_pdf_build_handoff.py`.
- `docs/research/2026-06-01-obviousbench-pdf-build-handoff.md`.
- `docs/research/2026-06-01-obviousbench-paper-authoring-toolchain.md`.
- `docs/status/2026-06-01-obviousbench-arxiv-paper-progress.md`.

Do not run expensive full model arrays until Tasks 1 through 6 pass.

## Task 1: Restrict Readiness Audit To Paper Manifest Items

Status: completed.

**Files:**

- Modify: `obviousbench/research/arxiv_readiness.py`
- Modify: `scripts/audit_arxiv_readiness.py`
- Modify: `tests/research/test_arxiv_readiness.py`
- Update: `docs/status/2026-06-01-obviousbench-arxiv-paper-progress.md`

Steps:

- [x] Add a test showing that the audit checks only item cards referenced by
      `paper_v1_manifest.jsonl` when `manifest_scope=True`.
- [x] Implement manifest-scoped item-card review by loading manifest item IDs
      before counting draft cards and placeholder text.
- [x] Add a CLI flag such as `--manifest-scope` and make paper helpers use it.
- [x] Run:

```bash
.venv/bin/python -m pytest tests/research/test_arxiv_readiness.py -q
.venv/bin/python -m ruff check obviousbench/research scripts/audit_arxiv_readiness.py tests/research/test_arxiv_readiness.py
```

Acceptance:

- Audit output reports blockers for the 80 paper candidates, not all 401 public
  item cards, when manifest scope is enabled.

## Task 2: Generate Paper Item-Card Review Queue

Status: completed.

**Files:**

- Create: `obviousbench/research/item_review_queue.py`
- Create: `scripts/build_item_review_queue.py`
- Create: `tests/research/test_item_review_queue.py`
- Create generated output: `docs/research/2026-06-01-paper-v1-item-review-queue.md`

Steps:

- [x] Write a test that reads a small manifest and draft card fixture and emits
      a Markdown review queue grouped by family.
- [x] Implement queue rows with item ID, family, subfamily, source refs, target,
      scorer, current review status, and missing fields.
- [x] Generate the real queue from `data/splits/paper_v1_manifest.jsonl`.
- [x] Run:

```bash
.venv/bin/python -m pytest tests/research/test_item_review_queue.py -q
.venv/bin/python -m ruff check obviousbench/research scripts/build_item_review_queue.py tests/research/test_item_review_queue.py
```

Acceptance:

- The review queue lists exactly 80 candidate items and makes review work
  mechanically actionable.

## Task 3: Review The 80 Paper Item Cards

Status: completed.

**Files:**

- Modify: `data/item_cards/public_v0/cards.yaml`
- Create: `obviousbench/research/item_card_review.py`
- Create: `scripts/promote_paper_item_cards.py`
- Create: `tests/research/test_item_card_review.py`
- Update: `docs/research/2026-06-01-paper-v1-item-review-queue.md`
- Update: `docs/status/2026-06-01-obviousbench-arxiv-paper-progress.md`

Steps:

- [x] Review 10 character-count cards.
- [x] Review 10 spelling-transform cards.
- [x] Review 10 arithmetic cards.
- [x] Review 10 word-count cards.
- [x] Review 10 ordering cards.
- [x] Review 10 negation cards.
- [x] Review 10 format-compliance cards.
- [x] Review 10 constraint-awareness cards.
- [x] For each card, remove placeholder text, write a concrete answer
      derivation, write ambiguity notes, confirm source refs, confirm scorer
      contract, and set review status to `reviewed`.
- [x] Run the manifest-scoped readiness audit.

Acceptance:

- Manifest-scoped item-card gate passes for all 80 paper candidates.

## Task 4: Create Human-Baseline Collection Asset

Status: partially completed. Collection assets, participant assignment packets,
collection handoff, scoring helpers, threshold audit helpers, and stronger
audit checks exist; real participant rows are still required.

**Files:**

- Create: `docs/research/2026-06-01-paper-v1-human-baseline-form.md`
- Create: `docs/research/2026-06-01-paper-v1-human-baseline-collection-packet.md`
- Create: `docs/research/2026-06-01-paper-v1-human-baseline-participant-packets.md`
- Create: `docs/research/2026-06-01-paper-v1-human-baseline-collection-audit.md`
- Create: `docs/research/2026-06-01-paper-v1-human-baseline-scoring-report.md`
- Create: `docs/research/2026-06-01-paper-v1-human-baseline-threshold-audit.md`
- Create: `data/human_baseline/paper_v1.csv`
- Create: `data/human_baseline/paper_v1_assignments.csv`
- Create: `data/human_baseline/paper_v1_response_template.csv`
- Create: `data/human_baseline/paper_v1_answer_key.csv`
- Create: `data/human_baseline/paper_v1_scored_draft.csv`
- Create: `data/human_baseline/paper_v1_threshold_items.csv`
- Create: `data/human_baseline/paper_v1_threshold_families.csv`
- Create: `obviousbench/research/human_baseline_collection_audit.py`
- Create: `obviousbench/research/human_baseline_form.py`
- Create: `obviousbench/research/human_baseline_packet.py`
- Create: `obviousbench/research/human_baseline_scoring.py`
- Create: `obviousbench/research/human_baseline_thresholds.py`
- Create: `scripts/build_human_baseline_form.py`
- Create: `scripts/build_human_baseline_packet.py`
- Create: `scripts/audit_human_baseline_collection.py`
- Create: `scripts/score_human_baseline.py`
- Create: `scripts/audit_human_baseline_thresholds.py`
- Create: `tests/research/test_human_baseline_form.py`
- Create: `tests/research/test_human_baseline_collection_audit.py`
- Create: `tests/research/test_human_baseline_packet.py`
- Create: `tests/research/test_human_baseline_scoring.py`
- Create: `tests/research/test_human_baseline_thresholds.py`
- Modify: `obviousbench/research/arxiv_readiness.py`
- Modify: `tests/research/test_arxiv_readiness.py`

Steps:

- [x] Generate a review form or CSV template from the 80 paper items.
- [x] Generate randomized participant assignments, participant-facing packets,
      response template rows, and a local answer key for 5 participants x 80
      paper items.
- [x] Add audit tests for required columns, at least 5 participants, every item
      covered, `seconds` parseable, and `correct` boolean.
- [x] Implement the stronger audit checks.
- [x] Add a `make -C paper human-baseline-packet` target.
- [x] Add a `make -C paper human-baseline-audit` target that checks
      participant/item coverage, answer/timing completeness, duplicate rows,
      and unknown response rows before scoring.
- [x] Add a `make -C paper human-baseline-collection-handoff` target that
      records the operator checklist, participant instruction block, answer-key
      privacy boundary, and scoring stop rules for real response collection.
- [x] Add a `make -C paper human-baseline-score` target that scores filled
      response rows with benchmark scorer contracts and remains blocked while
      responses are empty.
- [x] Add a `make -C paper human-baseline-thresholds` target that classifies
      scored rows as `core_h0`, `borderline`, `exclude`, or `no_data` using the
      predeclared threshold policy.
- [ ] Add baseline rows after real collection.
- [x] Run:

```bash
.venv/bin/python -m pytest tests/research/test_arxiv_readiness.py -q
```

Acceptance:

- Human-baseline gate passes with real participant rows.

## Task 5: Build Human-Baseline Summary Tables

Status: completed for generation mechanics. The generated table remains a
placeholder until real human-baseline rows are collected under Task 4.

**Files:**

- Modify: `obviousbench/research/paper_assets.py`
- Modify: `scripts/build_paper_assets.py`
- Modify: `tests/research/test_paper_assets.py`
- Generate: `paper/tables/human_baseline_summary.tex`

Steps:

- [x] Add a failing test for baseline summary generation.
- [x] Implement family-level human accuracy, item count, participant count, and
      median response time.
- [x] Add the table to `paper/sections/06_results.tex`.
- [x] Run:

```bash
.venv/bin/python -m pytest tests/research/test_paper_assets.py -q
make -C paper assets
```

Acceptance:

- The paper has a generated human-baseline table and does not rely on prose-only
  claims.

## Task 6: Freeze Model Panel And Cost Estimates

Status: completed for planning and dry-run cost estimates. No model arrays have
been run.

**Files:**

- Create: `configs/paper_v1_model_panel.yaml`
- Create: `docs/research/2026-06-01-paper-v1-model-panel.md`
- Create: `docs/research/2026-06-01-paper-v1-model-panel-cost-estimates.csv`
- Create: `docs/research/2026-06-01-paper-v1-model-panel-cost-estimates.md`
- Create: `obviousbench/research/model_panel_costs.py`
- Create: `scripts/estimate_paper_model_panel_costs.py`
- Create: `tests/configs/test_paper_v1_model_panel.py`
- Create: `tests/research/test_model_panel_costs.py`
- Update: `paper/sections/05_scoring_protocol.tex`

Steps:

- [x] Select model aliases and reasoning settings without making calls.
- [x] Record provider, alias, access route, expected cost surface, and run
      setting for each model.
- [x] Run only dry-run cost estimates where supported.
- [x] Do not run full model arrays.

Acceptance:

- The paper has a frozen intended model panel and cost estimate notes, but no
  expensive final sweep has been run.

## Task 7: Run Final Paper Sweep

Status: partially completed for dry-run handoff only. The final sweep must not
run until the readiness gate passes. A generated run plan and comparison
manifest now exist so the eventual expensive run can be executed and audited
model by model.

Roadmap update: `docs/research/2026-06-01-obviousbench-arxiv-completion-roadmap.md`
now provides the ordered dependency plan from the current scaffold to final
arXiv submission. It must be regenerated after material audit, metadata,
human-baseline, or result-integration changes.

Result-artifact update:
`docs/research/2026-06-01-paper-v1-final-result-artifact-audit.md` now defines
and checks the expected final sweep output contract. It should remain blocked
until the final model sweep has produced all per-model summaries, comparison
CSVs, and generated report files.

**Do not run model providers until Tasks 1 through 6 pass.**

**Files:**

- Create raw logs under ignored `results/raw/`.
- Create summaries under ignored `results/summaries/`.
- Generate tracked report under `docs/reports/<paper-v1-report>/`.
- Create: `docs/research/2026-06-01-paper-v1-final-sweep-plan.md`
- Create: `configs/paper_v1_final_sweep_manifest.csv`
- Create: `obviousbench/research/final_sweep_plan.py`
- Create: `scripts/build_final_sweep_plan.py`
- Create: `tests/research/test_final_sweep_plan.py`
- Update: `docs/status/2026-06-01-obviousbench-arxiv-paper-progress.md`

Steps:

- [x] Generate the dry-run final-sweep handoff without provider calls.
- [x] Generate the expected comparison manifest from the frozen model panel.
- [ ] Confirm readiness audit passes.
- [ ] Confirm model panel and cost estimates are accepted.
- [ ] Run final Inspect sweeps model by model.
- [ ] Summarize logs.
- [ ] Build comparison.
- [ ] Build report.
- [ ] Record provider errors and exclusions.

Acceptance:

- Final result directory exists with comparison, family comparison, section
  comparison, effort curves where applicable, and report artifacts.

## Task 8: Generate Final Paper Tables And Figures

Status: completed for placeholder/generator mechanics. Final numerical tables
and plotted figures still require the final paper sweep from Task 7.

**Files:**

- Modify: `obviousbench/research/paper_assets.py`
- Generate: `paper/tables/main_results.tex`
- Generate: `paper/tables/family_results.tex`
- Generate: `paper/tables/model_panel.tex`
- Generate: `paper/tables/provider_exclusions.tex`
- Generate: `paper/figures/*.pdf`

Steps:

- [x] Add table generators for main results, family results, model panel, and
      provider exclusions.
- [x] Add figure generators for leaderboard, family heatmap, answer/format gap,
      and cost frontier.
- [x] Add cheap tests with fixture CSVs.
- [x] Run paper asset generation.

Acceptance:

- All claim-bearing numerical content in the paper is generated from frozen
  artifacts.

## Task 9: Replace Claim Blockers With Evidence-Backed Text

Status: not completed. A claim-blocker audit helper and claim-evidence ledger
exist and currently report unresolved blockers, as intended before
human-baseline and final-sweep evidence exists.

**Files:**

- Modify all `paper/sections/*.tex`
- Update: `paper/main.tex`
- Create: `obviousbench/research/paper_claims.py`
- Create: `obviousbench/research/paper_claim_ledger.py`
- Create: `scripts/audit_paper_claims.py`
- Create: `scripts/build_paper_claim_ledger.py`
- Create: `tests/research/test_paper_claims.py`
- Create: `tests/research/test_paper_claim_ledger.py`
- Generate: `docs/research/2026-06-01-paper-claim-blocker-audit.md`
- Generate: `docs/research/2026-06-01-obviousbench-paper-claim-evidence-ledger.md`

Steps:

- [x] Search for `claimblocked` and `obtodo`.
- [x] Generate a ledger mapping each unresolved marker to required evidence,
      source artifacts, and acceptance criteria.
- [ ] Replace each marker only when there is a table, figure, command output,
      or source artifact proving the claim.
- [ ] Keep limitations explicit.
- [ ] Avoid global model-ranking claims.
- [ ] Keep solution/remediation text secondary.

Acceptance:

- `rg "claimblocked|obtodo" paper` returns no result except possibly author
  metadata if intentionally unresolved before submission.

## Task 10: Build And Inspect PDF

Status: partially completed for static source and PDF-build auditability. A
real PDF build still requires a LaTeX engine, but local audits now verify TeX
inputs, figures, bibliography files, citation keys, build-toolchain
availability, PDF artifact presence, and LaTeX log state.

**Files:**

- Generate ignored local PDF: `paper/main.pdf`
- Create: `docs/research/2026-06-01-obviousbench-paper-source-audit.md`
- Create: `docs/research/2026-06-01-obviousbench-paper-pdf-build-audit.md`
- Create: `obviousbench/research/paper_source_audit.py`
- Create: `obviousbench/research/paper_pdf_audit.py`
- Create: `scripts/audit_paper_source.py`
- Create: `scripts/audit_paper_pdf.py`
- Create: `tests/research/test_paper_source_audit.py`
- Create: `tests/research/test_paper_pdf_audit.py`
- Update: `docs/status/2026-06-01-obviousbench-arxiv-paper-progress.md`

Steps:

- [x] Add a static paper-source audit for TeX inputs, figures, bibliography
      files, citation keys, and submission markers.
- [x] Add a PDF build audit for LaTeX toolchain availability, static source
      audit status, `paper/main.pdf`, and `paper/main.log`.
- [x] Add a `make -C paper pdf-audit` target.
- [ ] Install or use a LaTeX engine in an appropriate environment.
- [ ] Run:

```bash
make -C paper pdf
```

- [ ] Inspect compile warnings, missing references, overfull boxes, table fit,
      and bibliography.
- [ ] Run `make -C paper pdf-audit` after the build and resolve every blocker.
- [ ] Fix source issues.

Acceptance:

- `paper/main.pdf` builds cleanly enough for review, with all tables and
  citations resolved.
- `make -C paper pdf-audit` passes after the real PDF build and inspection.

## Task 11: Internal Research Audit

Status: partially completed. The internal research-review helper and generated
review document exist. The review is intentionally blocked until human-baseline
evidence, final claim evidence, and final result artifacts exist.

**Files:**

- Create: `docs/research/2026-06-01-obviousbench-arxiv-internal-review.md`
- Create: `obviousbench/research/internal_review.py`
- Create: `scripts/audit_internal_research_review.py`
- Create: `tests/research/test_internal_review.py`

Steps:

- [x] Audit data claims against artifacts.
- [x] Audit code/reproducibility commands.
- [x] Audit source safety and privacy.
- [x] Audit related work coverage.
- [x] Audit limitations against actual claims.
- [ ] Resolve internal-review blockers after human-baseline evidence and final
      model-sweep artifacts exist.

Acceptance:

- Review document lists no unresolved blocking findings.

## Task 12: Prepare arXiv Source Bundle

Status: partially completed. A draft source bundle, bundle audit, submission
preflight checklist, and public release audit exist, but the bundle is not
submission-ready until claim blockers are resolved, release metadata is
confirmed, and a PDF build has been inspected.

**Files:**

- Generate: `paper/arxiv-src.tar.gz`
- Create: `docs/research/2026-06-01-obviousbench-arxiv-submission-checklist.md`
- Create: `docs/research/2026-06-01-obviousbench-arxiv-submission-metadata.md`
- Create: `obviousbench/research/arxiv_metadata.py`
- Create: `obviousbench/research/arxiv_preflight.py`
- Create: `obviousbench/research/arxiv_source_bundle.py`
- Create: `scripts/build_arxiv_submission_checklist.py`
- Create: `scripts/build_arxiv_submission_metadata.py`
- Create: `scripts/audit_arxiv_source_bundle.py`
- Create: `tests/research/test_arxiv_metadata.py`
- Create: `tests/research/test_arxiv_preflight.py`
- Create: `tests/research/test_arxiv_source_bundle.py`
- Generate: `docs/research/2026-06-01-obviousbench-arxiv-source-bundle-audit.md`
- Create: `docs/research/2026-06-01-obviousbench-public-release-artifact-audit.md`
- Create: `obviousbench/research/public_release_audit.py`
- Create: `scripts/audit_public_release_artifacts.py`
- Create: `tests/research/test_public_release_audit.py`

Steps:

- [x] Run `make -C paper arxiv-package`.
- [x] Inspect tar contents.
- [x] Confirm no raw logs, credentials, private/canary data, generated caches,
      or large ignored result directories are included.
- [x] Generate a submission checklist that aggregates readiness, claim audit,
      source-bundle audit, model-panel artifacts, PDF build status, LaTeX
      toolchain status, and final metadata confirmation.
- [x] Generate a draft arXiv metadata note with machine-audited confirmation
      fields for title, authors, abstract, category, license, release links,
      submitter status, and AI-tool disclosure.
- [x] Ensure draft metadata remains a failing preflight gate until explicitly
      confirmed and de-placeholdered.
- [x] Add a public release audit for required public docs, frozen paper data,
      license/citation/archive files, package license metadata, public URLs,
      and metadata confirmation.
- [x] Keep the public release audit blocked until LICENSE, CITATION.cff,
      `.zenodo.json`, package license metadata, public repository/dataset URLs,
      and confirmed metadata exist.
- [ ] Resolve submission-checklist blockers: human baseline, paper claim
      markers, PDF artifact, local LaTeX toolchain, and final metadata note.
- [ ] Resolve public-release blockers: license/citation files, archive
      metadata, package license metadata, public release URLs, and metadata
      confirmation.
- [ ] Confirm `.bib` or `.bbl` handling matches arXiv requirements.
- [ ] Confirm final abstract, title, author list, category, license, and AI-tool
      disclosure.

Acceptance:

- Source bundle is ready for arXiv upload and local checklist is complete.

## Task 13: Build Paper Reproducibility Manifest

Status: completed for current local artifacts. The manifest should be
regenerated after human-baseline collection, final model sweeps, final paper
asset generation, and source-bundle refreshes.

**Files:**

- Create: `docs/research/2026-06-01-obviousbench-paper-reproducibility-manifest.md`
- Create: `obviousbench/research/paper_repro_manifest.py`
- Create: `scripts/build_paper_repro_manifest.py`
- Create: `tests/research/test_paper_repro_manifest.py`
- Include: `configs/paper_v1_analysis_plan.yaml`
- Include: `docs/research/2026-06-01-obviousbench-paper-analysis-plan.md`
- Include: `docs/research/2026-06-01-obviousbench-report-section-tracker.md`
- Modify: `paper/Makefile`
- Update: `paper/README.md`
- Update: `docs/status/2026-06-01-obviousbench-arxiv-paper-progress.md`

Steps:

- [x] Hash manuscript source, generated paper tables/figures, frozen paper data,
      item cards, human-baseline CSV, collection assets, and scoring artifacts,
      model-panel configs, analysis-plan artifacts, audit reports, report
      section tracker, final-sweep handoff, and the draft arXiv source bundle.
- [x] Record cheap rebuild and audit commands without running provider calls.
- [x] Record git head and dirty/clean status summary when available.
- [x] Keep provider logs and post-sweep summary directories outside the
      manifest inventory.
- [x] Add a `make -C paper repro-manifest` target.
- [x] Add focused tests for hashing, missing required artifacts, git-state
      rendering, and script output.

Acceptance:

- `make -C paper repro-manifest` writes a passing manifest while all required
  current local artifacts exist, and the manifest can be rerun after every
  evidence-producing paper milestone.

## Task 14: Build Report Section Tracker

Status: completed for the current manuscript scaffold. The tracker should be
regenerated after every claim-replacement, result-table, figure, or metadata
edit.

**Files:**

- Create: `docs/research/2026-06-01-obviousbench-report-section-tracker.md`
- Create: `obviousbench/research/report_section_tracker.py`
- Create: `scripts/build_report_section_tracker.py`
- Create: `tests/research/test_report_section_tracker.py`
- Modify: `paper/Makefile`
- Update: `paper/README.md`
- Update: `docs/status/2026-06-01-obviousbench-arxiv-paper-progress.md`

Steps:

- [x] Scan `paper/main.tex` and `paper/sections/*.tex`.
- [x] Extract section titles, word counts, generated table inputs, figure
      references, citation counts, unresolved claim markers, draft-placeholder
      mentions, section roles, and next actions.
- [x] Map unresolved sections to evidence dependencies so final writing work is
      not hidden in prose.
- [x] Add a `make -C paper report-tracker` target.
- [x] Add focused tests for clean sections, blocked sections with dependencies,
      and script output.
- [x] Include the generated tracker in the reproducibility manifest.

Acceptance:

- `make -C paper report-tracker` writes a section-level dashboard that shows
  the current article state and the exact evidence dependencies blocking final
  prose.

## Task 15: Freeze Paper Statistical Analysis Plan

Status: completed for the current pre-sweep reporting policy. The plan must be
updated only deliberately before final provider runs, and post-hoc additions
must remain labeled exploratory.

**Files:**

- Create: `configs/paper_v1_analysis_plan.yaml`
- Create: `docs/research/2026-06-01-obviousbench-paper-analysis-plan.md`
- Create: `obviousbench/research/paper_analysis_plan.py`
- Create: `scripts/build_paper_analysis_plan.py`
- Create: `tests/research/test_paper_analysis_plan.py`
- Modify: `paper/Makefile`
- Update: `paper/README.md`
- Update: `docs/status/2026-06-01-obviousbench-arxiv-paper-progress.md`

Steps:

- [x] Freeze the primary question before final model results exist.
- [x] Freeze primary metrics: strict accuracy, answer accuracy, and format
      accuracy.
- [x] Freeze secondary metrics: obvious failure rate, provider errors,
      cost-per-correct, tokens-per-correct, and overthinking index.
- [x] Tie binomial intervals to
      `obviousbench.analysis.statistics.wilson_interval`.
- [x] Tie paired deltas to
      `obviousbench.analysis.statistics.paired_boolean_delta` with seed
      `20260531`.
- [x] Freeze reported tables, figures, exclusions, human-baseline policy, and
      claim-language policy.
- [x] Add a `make -C paper analysis-plan` target.
- [x] Include the generated analysis plan and source YAML in the reproducibility
      manifest.

Acceptance:

- `make -C paper analysis-plan` writes a passing analysis-plan report with no
  issues and no provider calls.

## Task 16: Prepare Human-Baseline Collection Packet

Status: completed for collection preparation. Real participant responses are
still required before the readiness gate can pass.

**Files:**

- Create: `docs/research/2026-06-01-paper-v1-human-baseline-collection-packet.md`
- Create: `docs/research/2026-06-01-paper-v1-human-baseline-participant-packets.md`
- Create: `docs/research/2026-06-01-paper-v1-human-baseline-collection-audit.md`
- Create: `data/human_baseline/paper_v1_assignments.csv`
- Create: `data/human_baseline/paper_v1_response_template.csv`
- Create: `data/human_baseline/paper_v1_answer_key.csv`
- Create: `obviousbench/research/human_baseline_collection_audit.py`
- Create: `obviousbench/research/human_baseline_packet.py`
- Create: `scripts/audit_human_baseline_collection.py`
- Create: `scripts/build_human_baseline_packet.py`
- Create: `tests/research/test_human_baseline_collection_audit.py`
- Create: `tests/research/test_human_baseline_packet.py`
- Modify: `paper/Makefile`
- Update: `paper/README.md`
- Update: `docs/research/2026-06-01-obviousbench-human-baseline-protocol.md`
- Update: `docs/status/2026-06-01-obviousbench-arxiv-paper-progress.md`

Steps:

- [x] Assign all 80 paper items to 5 pseudonymous participants.
- [x] Randomize item order per participant with a recorded seed.
- [x] Generate 400 assignment rows and 400 preallocated response rows.
- [x] Keep target answers out of participant-facing assignments and packets.
- [x] Generate a separate local answer key for scoring.
- [x] Add a `make -C paper human-baseline-packet` target.
- [x] Add a `make -C paper human-baseline-audit` target.
- [x] Generate a collection audit that reports 400/400 rows present, 0/400
      answer+timing rows complete, and no duplicate or unknown response rows
      for the current empty template.
- [x] Include collection assets in the reproducibility manifest.

Acceptance:

- `make -C paper human-baseline-packet` writes a passing collection packet with
  80 items, 5 participants, and 400 assignment rows without collecting real
  participant data or running provider calls.
- `make -C paper human-baseline-audit` writes a blocked collection audit until
  every preallocated response row has a real answer and parseable timing.

## Task 17: Add Human-Baseline Scoring Handoff

Status: completed for the current empty response template. Real participant
answers are still required before the scored draft can be promoted.

**Files:**

- Create: `docs/research/2026-06-01-paper-v1-human-baseline-scoring-report.md`
- Create: `data/human_baseline/paper_v1_scored_draft.csv`
- Create: `obviousbench/research/human_baseline_scoring.py`
- Create: `scripts/score_human_baseline.py`
- Create: `tests/research/test_human_baseline_scoring.py`
- Modify: `paper/Makefile`
- Update: `paper/README.md`
- Update: `docs/research/2026-06-01-obviousbench-human-baseline-protocol.md`
- Update: `docs/status/2026-06-01-obviousbench-arxiv-paper-progress.md`

Steps:

- [x] Read filled participant response rows and the local answer key.
- [x] Score non-empty answers through `obviousbench.scorers.dynamic.score_by_name`.
- [x] Preserve blank response rows as blocked rather than inventing correctness.
- [x] Write a draft scored CSV with target, extracted answer, failure type,
      format correctness, and strict correctness for audit.
- [x] Write a scoring report that remains blocked until all answers and timings
      are filled.
- [x] Add a `make -C paper human-baseline-score` target.
- [x] Include scoring artifacts in the reproducibility manifest.

Acceptance:

- `make -C paper human-baseline-score` runs without provider calls and reports
  the current empty-template blocker rather than fabricating human-baseline
  evidence.

## Task 18: Build Consolidated Blocker Dashboard

Status: completed for the current audit surface. The dashboard should be
regenerated after any human-baseline, result, claim, source, PDF, preflight,
release, or metadata artifact changes.

**Files:**

- Create: `docs/research/2026-06-01-obviousbench-arxiv-blocker-dashboard.md`
- Create: `obviousbench/research/paper_blocker_dashboard.py`
- Create: `scripts/build_paper_blocker_dashboard.py`
- Create: `tests/research/test_paper_blocker_dashboard.py`
- Modify: `paper/Makefile`
- Update: `paper/README.md`
- Update: `obviousbench/research/paper_completion_roadmap.py`
- Update: `obviousbench/research/paper_repro_manifest.py`
- Update: `docs/status/2026-06-01-obviousbench-arxiv-paper-progress.md`

Steps:

- [x] Aggregate the human collection, threshold, final-sweep, result-artifact,
      claim/section, source/PDF, preflight, internal-review, release, and
      metadata gates into one generated status document.
- [x] Classify each row as `PASS`, `BLOCKED`, or `WAITING`.
- [x] Group non-passing rows by dependency type: human data collection,
      provider run after readiness, paper writing after evidence, local
      writing/LaTeX environment, release decision, author/release decision,
      and aggregate gates.
- [x] Add a `make -C paper blocker-dashboard` target.
- [x] Include the blocker dashboard in the completion roadmap and
      reproducibility manifest.

Acceptance:

- `make -C paper blocker-dashboard` writes a single action dashboard without
  collecting data, running providers, compiling LaTeX, or choosing release
  metadata.

## Task 19: Build arXiv Submission Handoff

Status: completed for the current audit surface. The handoff should be
regenerated after source-bundle, PDF, preflight, release, metadata, or blocker
dashboard changes. It is intentionally blocked until all upload-facing checks
pass.

**Files:**

- Create: `docs/research/2026-06-01-obviousbench-arxiv-submission-handoff.md`
- Create: `obviousbench/research/arxiv_submission_handoff.py`
- Create: `scripts/build_arxiv_submission_handoff.py`
- Create: `tests/research/test_arxiv_submission_handoff.py`
- Modify: `paper/Makefile`
- Update: `paper/README.md`
- Update: `obviousbench/research/internal_review.py`
- Update: `obviousbench/research/paper_completion_roadmap.py`
- Update: `obviousbench/research/paper_repro_manifest.py`
- Update: `docs/status/2026-06-01-obviousbench-arxiv-paper-progress.md`
- Update: `docs/research/2026-06-01-obviousbench-arxiv-report-plan.md`

Steps:

- [x] Build a generated handoff that reads the source bundle audit, PDF audit,
      submission preflight, public release audit, metadata note, and blocker
      dashboard.
- [x] Report `Upload readiness: YES` only when every upload-facing check passes.
- [x] Keep strict mode failing while the packet is not ready.
- [x] Add a `make -C paper submission-handoff` target.
- [x] Add the handoff artifact and command to the reproducibility manifest.
- [x] Add the handoff to the completion roadmap as a hard stop before upload.
- [x] Add focused tests for blocked, complete, and script-output paths.

Acceptance:

- `make -C paper submission-handoff` writes an upload-facing handoff without
  submitting, compiling, publishing, collecting data, or running providers.
- `scripts/build_arxiv_submission_handoff.py --strict` exits nonzero until the
  source bundle, PDF audit, preflight, release audit, metadata audit, and
  blocker dashboard all pass.

## Task 20: Build Manuscript Completeness Audit

Status: completed for the current manuscript scaffold. The audit should be
regenerated after any LaTeX section, generated table, generated figure,
reference, claim marker, or placeholder-language change.

**Files:**

- Create: `docs/research/2026-06-01-obviousbench-manuscript-completeness-audit.md`
- Create: `obviousbench/research/manuscript_completeness.py`
- Create: `scripts/audit_manuscript_completeness.py`
- Create: `tests/research/test_manuscript_completeness.py`
- Modify: `paper/Makefile`
- Update: `paper/README.md`
- Update: `obviousbench/research/internal_review.py`
- Update: `obviousbench/research/paper_blocker_dashboard.py`
- Update: `obviousbench/research/paper_completion_roadmap.py`
- Update: `obviousbench/research/paper_repro_manifest.py`
- Update: `docs/status/2026-06-01-obviousbench-arxiv-paper-progress.md`
- Update: `docs/research/2026-06-01-obviousbench-arxiv-report-plan.md`

Steps:

- [x] Define expected arXiv manuscript components: title/abstract,
      introduction, related work, benchmark definition, data review, scoring,
      results, analysis, discussion, limitations/reproducibility, and appendix.
- [x] Check required phrases, citations, generated table references, generated
      figure references, unresolved claim markers, and placeholder mentions.
- [x] Generate a component matrix with pass/blocked/missing status and next
      actions.
- [x] Add a `make -C paper manuscript-completeness` target.
- [x] Add the audit to the blocker dashboard, completion roadmap, internal
      review command check, and reproducibility manifest.
- [x] Add focused tests for passing, blocked, and script-output paths.

Acceptance:

- `make -C paper manuscript-completeness` writes an audit proving that all
  expected report components exist while preserving blockers for evidence that
  does not exist yet.
- The blocker dashboard includes manuscript completeness as a paper-writing
  gate before final copyedit and upload.

## Task 21: Build Public Release Decision Packet

Status: completed for the current release decision surface. The packet should
be regenerated after any arXiv metadata, license, citation, archive, package
metadata, public URL, or release-audit change.

**Files:**

- Create: `docs/research/2026-06-01-obviousbench-public-release-decision-packet.md`
- Create: `obviousbench/research/public_release_decision_packet.py`
- Create: `scripts/build_public_release_decision_packet.py`
- Create: `tests/research/test_public_release_decision_packet.py`
- Modify: `paper/Makefile`
- Update: `paper/README.md`
- Update: `obviousbench/research/internal_review.py`
- Update: `obviousbench/research/paper_completion_roadmap.py`
- Update: `obviousbench/research/paper_repro_manifest.py`
- Update: `docs/status/2026-06-01-obviousbench-arxiv-paper-progress.md`
- Update: `docs/research/2026-06-01-obviousbench-arxiv-report-plan.md`

Steps:

- [x] Read the draft arXiv metadata and current release audit.
- [x] Record the six remaining release decisions: license selection, citation
      metadata, archive metadata, package license metadata, public URLs, and
      submitter/final metadata confirmation.
- [x] Include draft templates for `CITATION.cff`, `.zenodo.json`, and
      `pyproject.toml` license metadata without creating final files or
      choosing a license.
- [x] Add a `make -C paper release-packet` target that also refreshes the
      public release audit.
- [x] Include the release packet in the completion roadmap and reproducibility
      manifest.
- [x] Add focused tests for blocked, complete, and script-output paths.

Acceptance:

- `make -C paper release-packet` writes a decision packet with explicit
  release decisions and templates while preserving the public-release audit as
  blocked until the decisions are real.
- No `LICENSE`, `CITATION.cff`, `.zenodo.json`, package license field, public
  URL, or arXiv confirmation field is invented by the helper.

## Task 22: Build Human-Baseline Operations Packet

Status: completed for the current empty-response baseline state. The packet
should be regenerated after every response collection, scoring, thresholding,
promotion, or readiness-audit change.

**Files:**

- Create: `docs/research/2026-06-01-paper-v1-human-baseline-operations.md`
- Create: `obviousbench/research/human_baseline_operations.py`
- Create: `scripts/build_human_baseline_operations.py`
- Create: `tests/research/test_human_baseline_operations.py`
- Modify: `paper/Makefile`
- Update: `paper/README.md`
- Update: `obviousbench/research/internal_review.py`
- Update: `obviousbench/research/paper_completion_roadmap.py`
- Update: `obviousbench/research/paper_repro_manifest.py`
- Update: `docs/status/2026-06-01-obviousbench-arxiv-paper-progress.md`
- Update: `docs/research/2026-06-01-obviousbench-arxiv-report-plan.md`

Steps:

- [x] Read the collection packet, collection audit, scoring report, threshold
      audit, promotion CSV, and readiness audit.
- [x] Record the human-baseline command ladder from response collection through
      promotion and readiness.
- [x] Mark structural collection packet generation as passed while preserving
      blockers for empty responses, unscored rows, no-data thresholds,
      promotion, and readiness.
- [x] Add a `make -C paper human-baseline-ops` target that refreshes packet,
      audit, scoring, thresholding, and operations handoff artifacts.
- [x] Include the operations packet in the completion roadmap and
      reproducibility manifest.
- [x] Add focused tests for blocked, complete, and script-output paths.

Acceptance:

- `make -C paper human-baseline-ops` writes an operations packet with the
  current 1 passed and 5 blocked gates.
- `scripts/build_human_baseline_operations.py --strict` fails until real
  responses are collected, scored, thresholded, promoted, and readiness can
  pass.

## Task 23: Build Related-Work Positioning Matrix

Status: completed for the current comparator set. The matrix should be
regenerated after adding or removing related-work comparators or changing
`paper/sections/02_related_work.tex`.

**Files:**

- Create: `configs/paper_v1_related_work.yaml`
- Create: `docs/research/2026-06-01-obviousbench-related-work-positioning.md`
- Create: `paper/tables/related_work_positioning.tex`
- Create: `obviousbench/research/related_work_matrix.py`
- Create: `scripts/build_related_work_matrix.py`
- Create: `tests/research/test_related_work_matrix.py`
- Modify: `paper/sections/02_related_work.tex`
- Modify: `paper/references.bib`
- Modify: `paper/Makefile`
- Update: `paper/README.md`
- Update: `obviousbench/research/internal_review.py`
- Update: `obviousbench/research/manuscript_completeness.py`
- Update: `obviousbench/research/paper_repro_manifest.py`
- Update: `docs/status/2026-06-01-obviousbench-arxiv-paper-progress.md`
- Update: `docs/research/2026-06-01-obviousbench-arxiv-report-plan.md`

Steps:

- [x] Create a YAML source of record for the required related-work comparator
      set, evidence standard, and ObviousBench positioning stance.
- [x] Add the benchmark-aging comparator surfaced by the related-work refresh
      and cite the official arXiv record.
- [x] Generate both a Markdown positioning artifact and a LaTeX table for the
      manuscript.
- [x] Check that every required comparator has a bibliography entry and is
      cited in the related-work section.
- [x] Add a `make -C paper related-work` target and wire it into source-bundle
      generation.
- [x] Include the generated related-work artifacts in the reproducibility
      manifest and manuscript completeness audit.
- [x] Add focused tests for passing coverage, missing-citation blocking, and
      script-output paths.

Acceptance:

- `make -C paper related-work` writes a positioning matrix with 11 passed
  comparator checks and 0 blocked checks.
- The related-work section contains the generated matrix and cites every
  required comparator before final copyedit.

## Task 24: Build PDF Toolchain And Inspection Handoff

Status: completed for the current local PDF blocker state. The handoff should
be regenerated after installing a LaTeX toolchain, changing TeX source,
building `paper/main.pdf`, or rerunning the PDF audit.

**Files:**

- Create: `docs/research/2026-06-01-obviousbench-pdf-build-handoff.md`
- Create: `obviousbench/research/pdf_build_handoff.py`
- Create: `scripts/build_pdf_build_handoff.py`
- Create: `tests/research/test_pdf_build_handoff.py`
- Modify: `paper/Makefile`
- Update: `paper/README.md`
- Update: `obviousbench/research/internal_review.py`
- Update: `obviousbench/research/paper_repro_manifest.py`
- Update: `docs/status/2026-06-01-obviousbench-arxiv-paper-progress.md`
- Update: `docs/research/2026-06-01-obviousbench-arxiv-report-plan.md`

Steps:

- [x] Read the current PDF build audit and static source audit.
- [x] Detect available local commands for LaTeX build and support tooling.
- [x] Record off-the-shelf install options for Tectonic and MacTeX without
      installing software or compiling LaTeX.
- [x] Record the build ladder, inspection checklist, and stop rules for final
      PDF readiness.
- [x] Add a `make -C paper pdf-handoff` target that refreshes the PDF audit and
      then writes the handoff.
- [x] Include the PDF handoff in internal review and the reproducibility
      manifest.
- [x] Add focused tests for blocked, passing, and strict script-output paths.

Acceptance:

- `make -C paper pdf-handoff` writes a PDF toolchain and inspection handoff
  without installing software, compiling LaTeX, or running model providers.
- `scripts/build_pdf_build_handoff.py --strict` fails until the PDF audit,
  static source audit, toolchain, PDF artifact, and build log are all clean.

## Task 25: Build Human-Baseline Collection Execution Handoff

Status: completed for the current empty-response baseline state. The handoff
should be regenerated after every response collection batch and before scoring.

**Files:**

- Create: `docs/research/2026-06-01-paper-v1-human-baseline-collection-handoff.md`
- Create: `obviousbench/research/human_baseline_collection_handoff.py`
- Create: `scripts/build_human_baseline_collection_handoff.py`
- Create: `tests/research/test_human_baseline_collection_handoff.py`
- Modify: `paper/Makefile`
- Update: `paper/README.md`
- Update: `obviousbench/research/internal_review.py`
- Update: `obviousbench/research/paper_repro_manifest.py`
- Update: `docs/status/2026-06-01-obviousbench-arxiv-paper-progress.md`
- Update: `docs/research/2026-06-01-obviousbench-arxiv-report-plan.md`

Steps:

- [x] Read the assignment CSV, response template, participant packets,
      collection packet, answer key presence, and collection audit state.
- [x] Generate participant progress rows with expected rows, present rows,
      complete answer+timing rows, missing answers, and invalid timings.
- [x] Record the operator checklist, neutral participant instructions,
      completion contract, command ladder, and stop rules.
- [x] Keep answer-key handling local and explicitly non-participant-facing.
- [x] Add a `make -C paper human-baseline-collection-handoff` target and make
      `human-baseline-ops` depend on it.
- [x] Include the handoff in internal review coverage and the reproducibility
      manifest.
- [x] Add focused tests for blocked, complete, and strict script-output paths.

Acceptance:

- `make -C paper human-baseline-collection-handoff` writes an operator runbook
  with 5 participants, 400 response rows, and the current 0/400 complete
  collection state.
- `scripts/build_human_baseline_collection_handoff.py --strict` fails until
  every preallocated response row has a non-empty answer and parseable,
  non-negative timing.
