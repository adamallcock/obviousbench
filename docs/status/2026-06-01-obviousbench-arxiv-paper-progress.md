---
title: ObviousBench arXiv Paper Progress
date: 2026-06-01
type: status
status: in-progress
---

# ObviousBench arXiv Paper Progress

## Current Objective

Build ObviousBench toward a publication-ready arXiv article without running
large expensive model arrays yet.

The current work is focused on:

- a standard paper authoring setup,
- a full manuscript scaffold,
- cheap report helpers,
- a repeatable readiness gate,
- a concrete plan from current state to final arXiv submission.

## Current Authoring Decision

Canonical article source: LaTeX.

Decision record:

- [docs/research/2026-06-01-obviousbench-paper-authoring-toolchain.md](../research/2026-06-01-obviousbench-paper-authoring-toolchain.md)

Rationale:

- arXiv processes TeX/LaTeX directly.
- `pandoc`, `quarto`, `latexmk`, `pdflatex`, and `tectonic` are not installed
  in this workspace.
- R is installed, but R Markdown would add a conversion layer that arXiv does
  not need.
- Markdown remains the repo format for plans, status, and research notes.

## Skill And Tooling Check

Curated online skills were checked.

- No curated arXiv/LaTeX research-paper-writing skill was available.
- `pdf` was already installed.
- `jupyter-notebook` was installed as a relevant support skill for future
  reproducible analysis/figure notebooks.
- Restart Codex before expecting the newly installed `jupyter-notebook` skill to
  appear in the available skills list.

## Paper Scaffold

Created:

- `paper/README.md`
- `paper/Makefile`
- `paper/main.tex`
- `paper/references.bib`
- `paper/sections/01_introduction.tex`
- `paper/sections/02_related_work.tex`
- `paper/sections/03_benchmark.tex`
- `paper/sections/04_data_review.tex`
- `paper/sections/05_scoring_protocol.tex`
- `paper/sections/06_results.tex`
- `paper/sections/07_analysis.tex`
- `paper/sections/08_discussion.tex`
- `paper/sections/09_limitations_ethics_reproducibility.tex`
- `paper/sections/appendix.tex`
- `paper/figures/README.md`
- `paper/figures/answer_format_gap.pdf`
- `paper/figures/cost_frontier.pdf`
- `paper/figures/family_heatmap.pdf`
- `paper/figures/leaderboard.pdf`
- `paper/.gitignore`

The paper is claim-safe: it lays out the final report structure but marks
blocked claims with `\claimblocked{...}` until evidence exists.

## Cheap Helpers

Created:

- `obviousbench/research/arxiv_readiness.py`
- `obviousbench/research/arxiv_metadata.py`
- `obviousbench/research/arxiv_preflight.py`
- `obviousbench/research/arxiv_submission_handoff.py`
- `obviousbench/research/arxiv_source_bundle.py`
- `obviousbench/research/final_result_artifacts.py`
- `obviousbench/research/final_sweep_plan.py`
- `obviousbench/research/human_baseline_collection_audit.py`
- `obviousbench/research/human_baseline_collection_handoff.py`
- `obviousbench/research/human_baseline_packet.py`
- `obviousbench/research/human_baseline_form.py`
- `obviousbench/research/human_baseline_scoring.py`
- `obviousbench/research/human_baseline_thresholds.py`
- `obviousbench/research/human_baseline_operations.py`
- `obviousbench/research/internal_review.py`
- `obviousbench/research/item_card_review.py`
- `obviousbench/research/item_review_queue.py`
- `obviousbench/research/manuscript_completeness.py`
- `obviousbench/research/model_panel_costs.py`
- `obviousbench/research/paper_analysis_plan.py`
- `obviousbench/research/paper_claim_ledger.py`
- `obviousbench/research/paper_claims.py`
- `obviousbench/research/paper_completion_roadmap.py`
- `obviousbench/research/paper_pdf_audit.py`
- `obviousbench/research/pdf_build_handoff.py`
- `obviousbench/research/paper_assets.py`
- `obviousbench/research/paper_blocker_dashboard.py`
- `obviousbench/research/paper_repro_manifest.py`
- `obviousbench/research/paper_source_audit.py`
- `obviousbench/research/public_release_audit.py`
- `obviousbench/research/public_release_decision_packet.py`
- `obviousbench/research/related_work_matrix.py`
- `obviousbench/research/report_section_tracker.py`
- `scripts/audit_arxiv_readiness.py`
- `scripts/audit_arxiv_source_bundle.py`
- `scripts/audit_paper_claims.py`
- `scripts/audit_paper_source.py`
- `scripts/audit_paper_pdf.py`
- `scripts/audit_final_result_artifacts.py`
- `scripts/build_paper_analysis_plan.py`
- `scripts/build_paper_claim_ledger.py`
- `scripts/build_paper_completion_roadmap.py`
- `scripts/build_paper_repro_manifest.py`
- `scripts/build_pdf_build_handoff.py`
- `scripts/build_report_section_tracker.py`
- `scripts/build_final_sweep_plan.py`
- `scripts/build_arxiv_submission_checklist.py`
- `scripts/build_arxiv_submission_handoff.py`
- `scripts/build_arxiv_submission_metadata.py`
- `scripts/audit_human_baseline_collection.py`
- `scripts/build_human_baseline_packet.py`
- `scripts/build_human_baseline_form.py`
- `scripts/score_human_baseline.py`
- `scripts/audit_human_baseline_thresholds.py`
- `scripts/build_human_baseline_collection_handoff.py`
- `scripts/build_human_baseline_operations.py`
- `scripts/audit_public_release_artifacts.py`
- `scripts/build_public_release_decision_packet.py`
- `scripts/build_related_work_matrix.py`
- `scripts/build_item_review_queue.py`
- `scripts/build_paper_assets.py`
- `scripts/build_paper_blocker_dashboard.py`
- `scripts/audit_internal_research_review.py`
- `scripts/audit_manuscript_completeness.py`
- `scripts/estimate_paper_model_panel_costs.py`
- `scripts/promote_paper_item_cards.py`
- `tests/research/test_arxiv_readiness.py`
- `tests/research/test_arxiv_metadata.py`
- `tests/research/test_arxiv_preflight.py`
- `tests/research/test_arxiv_submission_handoff.py`
- `tests/research/test_arxiv_source_bundle.py`
- `tests/research/test_final_result_artifacts.py`
- `tests/research/test_final_sweep_plan.py`
- `tests/research/test_human_baseline_collection_audit.py`
- `tests/research/test_human_baseline_collection_handoff.py`
- `tests/research/test_human_baseline_packet.py`
- `tests/research/test_human_baseline_form.py`
- `tests/research/test_human_baseline_scoring.py`
- `tests/research/test_human_baseline_thresholds.py`
- `tests/research/test_human_baseline_operations.py`
- `tests/research/test_internal_review.py`
- `tests/research/test_item_card_review.py`
- `tests/research/test_item_review_queue.py`
- `tests/research/test_manuscript_completeness.py`
- `tests/research/test_model_panel_costs.py`
- `tests/research/test_paper_analysis_plan.py`
- `tests/research/test_paper_claim_ledger.py`
- `tests/research/test_paper_claims.py`
- `tests/research/test_paper_completion_roadmap.py`
- `tests/research/test_paper_pdf_audit.py`
- `tests/research/test_pdf_build_handoff.py`
- `tests/research/test_paper_repro_manifest.py`
- `tests/research/test_paper_source_audit.py`
- `tests/research/test_paper_assets.py`
- `tests/research/test_paper_blocker_dashboard.py`
- `tests/research/test_public_release_audit.py`
- `tests/research/test_public_release_decision_packet.py`
- `tests/research/test_related_work_matrix.py`
- `tests/research/test_report_section_tracker.py`
- `tests/configs/test_paper_v1_model_panel.py`

Generated tables:

- `paper/tables/dataset_composition.tex`
- `paper/tables/scorer_gold_coverage.tex`
- `paper/tables/readiness_gates.tex`
- `paper/tables/human_baseline_summary.tex`
- `paper/tables/main_results.tex`
- `paper/tables/family_results.tex`
- `paper/tables/model_panel.tex`
- `paper/tables/provider_exclusions.tex`
- `paper/tables/related_work_positioning.tex`

Cheap commands:

```bash
.venv/bin/python scripts/build_paper_assets.py \
  --manifest data/splits/paper_v1_manifest.jsonl \
  --human-baseline data/human_baseline/paper_v1.csv \
  --out paper/tables

.venv/bin/python scripts/audit_arxiv_readiness.py \
  --human-baseline data/human_baseline/paper_v1.csv \
  --paper-manifest data/splits/paper_v1_manifest.jsonl \
  --manifest-scope

.venv/bin/python scripts/promote_paper_item_cards.py \
  --manifest data/splits/paper_v1_manifest.jsonl \
  --source-catalog data/source_catalog/sources_v0.jsonl \
  --cards data/item_cards/public_v0/cards.yaml

.venv/bin/python scripts/build_human_baseline_form.py \
  --manifest data/splits/paper_v1_manifest.jsonl \
  --form-out docs/research/2026-06-01-paper-v1-human-baseline-form.md \
  --csv-out data/human_baseline/paper_v1.csv

.venv/bin/python scripts/build_human_baseline_packet.py \
  --manifest data/splits/paper_v1_manifest.jsonl \
  --participants 5

.venv/bin/python scripts/audit_human_baseline_collection.py \
  --assignments data/human_baseline/paper_v1_assignments.csv \
  --responses data/human_baseline/paper_v1_response_template.csv \
  --answer-key data/human_baseline/paper_v1_answer_key.csv \
  --out docs/research/2026-06-01-paper-v1-human-baseline-collection-audit.md

.venv/bin/python scripts/build_human_baseline_collection_handoff.py

.venv/bin/python scripts/score_human_baseline.py \
  --responses data/human_baseline/paper_v1_response_template.csv \
  --answer-key data/human_baseline/paper_v1_answer_key.csv \
  --scored-out data/human_baseline/paper_v1_scored_draft.csv \
  --report-out docs/research/2026-06-01-paper-v1-human-baseline-scoring-report.md

.venv/bin/python scripts/audit_human_baseline_thresholds.py \
  --scored data/human_baseline/paper_v1_scored_draft.csv \
  --answer-key data/human_baseline/paper_v1_answer_key.csv \
  --item-out data/human_baseline/paper_v1_threshold_items.csv \
  --family-out data/human_baseline/paper_v1_threshold_families.csv \
  --report-out docs/research/2026-06-01-paper-v1-human-baseline-threshold-audit.md

.venv/bin/python scripts/build_human_baseline_operations.py

.venv/bin/python scripts/build_related_work_matrix.py

.venv/bin/python scripts/estimate_paper_model_panel_costs.py \
  --panel configs/paper_v1_model_panel.yaml \
  --csv-out docs/research/2026-06-01-paper-v1-model-panel-cost-estimates.csv \
  --md-out docs/research/2026-06-01-paper-v1-model-panel-cost-estimates.md

.venv/bin/python scripts/audit_paper_claims.py \
  --paper-dir paper \
  --out docs/research/2026-06-01-paper-claim-blocker-audit.md

.venv/bin/python scripts/build_paper_claim_ledger.py \
  --paper-dir paper \
  --out docs/research/2026-06-01-obviousbench-paper-claim-evidence-ledger.md

.venv/bin/python scripts/audit_paper_source.py \
  --paper-dir paper \
  --out docs/research/2026-06-01-obviousbench-paper-source-audit.md

.venv/bin/python scripts/audit_paper_pdf.py \
  --paper-dir paper \
  --out docs/research/2026-06-01-obviousbench-paper-pdf-build-audit.md

make -C paper arxiv-package

.venv/bin/python scripts/audit_arxiv_source_bundle.py \
  --bundle paper/arxiv-src.tar.gz \
  --out docs/research/2026-06-01-obviousbench-arxiv-source-bundle-audit.md

.venv/bin/python scripts/build_arxiv_submission_checklist.py

.venv/bin/python scripts/build_arxiv_submission_metadata.py

.venv/bin/python scripts/build_arxiv_submission_handoff.py

.venv/bin/python scripts/audit_internal_research_review.py

.venv/bin/python scripts/audit_manuscript_completeness.py

.venv/bin/python scripts/build_final_sweep_plan.py

.venv/bin/python scripts/audit_final_result_artifacts.py \
  --manifest configs/paper_v1_final_sweep_manifest.csv \
  --comparison-dir results/summaries/paper-v1-final-high-cap/comparison \
  --report-dir docs/reports/2026-06-01-paper-v1-final-high-cap-sweep \
  --out docs/research/2026-06-01-paper-v1-final-result-artifact-audit.md

.venv/bin/python scripts/audit_public_release_artifacts.py \
  --metadata docs/research/2026-06-01-obviousbench-arxiv-submission-metadata.md \
  --out docs/research/2026-06-01-obviousbench-public-release-artifact-audit.md

.venv/bin/python scripts/build_public_release_decision_packet.py

.venv/bin/python scripts/build_paper_analysis_plan.py

.venv/bin/python scripts/build_report_section_tracker.py

.venv/bin/python scripts/build_paper_blocker_dashboard.py

.venv/bin/python scripts/build_paper_completion_roadmap.py

.venv/bin/python scripts/build_paper_repro_manifest.py

.venv/bin/python scripts/build_pdf_build_handoff.py
```

## Current Paper Split

`data/splits/paper_v1_manifest.jsonl` exists.

Composition:

- 80 candidate items.
- 10 items from each of 8 families.
- Seeded from `data/barrages/hard_obvious_8x10_seed_20260531.jsonl`.
- 80 unique item IDs.

This is a candidate review target, not a paper-ready split.

Review queue:

- [docs/research/2026-06-01-paper-v1-item-review-queue.md](../research/2026-06-01-paper-v1-item-review-queue.md)
- 80 item review rows.
- 0 currently blocked.
- All 80 paper candidate item cards are reviewed and placeholder-free.

Human baseline collection assets:

- [docs/research/2026-06-01-paper-v1-human-baseline-form.md](../research/2026-06-01-paper-v1-human-baseline-form.md)
- [docs/research/2026-06-01-paper-v1-human-baseline-collection-packet.md](../research/2026-06-01-paper-v1-human-baseline-collection-packet.md)
- [docs/research/2026-06-01-paper-v1-human-baseline-participant-packets.md](../research/2026-06-01-paper-v1-human-baseline-participant-packets.md)
- [docs/research/2026-06-01-paper-v1-human-baseline-collection-audit.md](../research/2026-06-01-paper-v1-human-baseline-collection-audit.md)
- [docs/research/2026-06-01-paper-v1-human-baseline-collection-handoff.md](../research/2026-06-01-paper-v1-human-baseline-collection-handoff.md)
- [docs/research/2026-06-01-paper-v1-human-baseline-scoring-report.md](../research/2026-06-01-paper-v1-human-baseline-scoring-report.md)
- [docs/research/2026-06-01-paper-v1-human-baseline-threshold-audit.md](../research/2026-06-01-paper-v1-human-baseline-threshold-audit.md)
- [docs/research/2026-06-01-paper-v1-human-baseline-operations.md](../research/2026-06-01-paper-v1-human-baseline-operations.md)
- `data/human_baseline/paper_v1.csv`
- `data/human_baseline/paper_v1_assignments.csv`
- `data/human_baseline/paper_v1_response_template.csv`
- `data/human_baseline/paper_v1_scored_draft.csv`
- `data/human_baseline/paper_v1_answer_key.csv`
- `data/human_baseline/paper_v1_threshold_items.csv`
- `data/human_baseline/paper_v1_threshold_families.csv`
- The CSV is intentionally header-only until real participant responses are
  collected.
- The generated collection packet assigns all 80 paper items to 5 participants
  for 400 planned response rows, with participant-facing packets separated from
  the local answer key.
- The collection audit currently reports 400/400 response rows present, 0/400
  answer+timing rows complete, 400 missing answers, 400 invalid timings, and 0
  duplicate or unknown response-row issues. This makes the real collection
  blocker explicit before scoring.
- The collection handoff is the operator runbook for collecting the 400 real
  answer/timing rows. It currently reports 5 participants, 400 response rows,
  0 completed rows, and preserves the privacy/answer-key stop rules before
  scoring.
- The scoring report currently evaluates the empty response template and is
  blocked with 0/400 scored rows and 800 missing-answer/timing issues. After
  real answers are collected, the same helper writes a scored draft for
  promotion into `data/human_baseline/paper_v1.csv`.
- The threshold audit currently evaluates the empty scored draft and is blocked
  with 80 `no_data` items. After real answers are collected and scored, the
  same helper classifies each item as `core_h0`, `borderline`, `exclude`, or
  `no_data` for paper claim gating.
- The operations packet coordinates collection, collection audit, scoring,
  thresholding, promotion, and readiness gates. It currently reports 1 passed
  gate and 5 blocked gates, so the next action remains real response
  collection rather than model-array execution.

Related-work assets:

- `configs/paper_v1_related_work.yaml`
- [docs/research/2026-06-01-obviousbench-related-work-positioning.md](../research/2026-06-01-obviousbench-related-work-positioning.md)
- `paper/tables/related_work_positioning.tex`
- The generated matrix currently covers 11 required comparators with 0
  coverage blockers, including the benchmark-aging paper surfaced during the
  related-work refresh.

Paper model panel:

- `configs/paper_v1_analysis_plan.yaml`
- `configs/paper_v1_model_panel.yaml`
- `configs/paper_v1_final_sweep_manifest.csv`
- [docs/research/2026-06-01-paper-v1-model-panel.md](../research/2026-06-01-paper-v1-model-panel.md)
- [docs/research/2026-06-01-obviousbench-paper-analysis-plan.md](../research/2026-06-01-obviousbench-paper-analysis-plan.md)
- [docs/research/2026-06-01-paper-v1-model-panel-cost-estimates.md](../research/2026-06-01-paper-v1-model-panel-cost-estimates.md)
- [docs/research/2026-06-01-paper-v1-final-sweep-plan.md](../research/2026-06-01-paper-v1-final-sweep-plan.md)
- [docs/research/2026-06-01-paper-v1-final-result-artifact-audit.md](../research/2026-06-01-paper-v1-final-result-artifact-audit.md)
- 12 planned models.
- The paper analysis plan freezes 3 primary metrics, 5 secondary metrics, 4
  reported tables, 4 reported figures, Wilson intervals, paired bootstrap
  delta policy, exclusion rules, and claim-language policy before final model
  results exist.
- Dry-run cost estimates were generated without provider calls.
- A dry-run final-sweep handoff was generated without provider calls. It writes
  12 per-model Inspect commands, 12 summarize/rescore commands, post-run
  comparison/report/paper-asset commands, and the expected comparison manifest.
- The final-sweep handoff currently says `Run allowed: NO` because the
  human-baseline gate is still failing.
- The final-result artifact audit currently reports the 12 planned model
  summary directories, final comparison CSVs, and generated report files as
  missing. This is expected until the final paper sweep is authorized and run.
- No final paper model array has been run.

Paper claim and source-bundle audits:

- [docs/research/2026-06-01-paper-claim-blocker-audit.md](../research/2026-06-01-paper-claim-blocker-audit.md)
- [docs/research/2026-06-01-obviousbench-paper-claim-evidence-ledger.md](../research/2026-06-01-obviousbench-paper-claim-evidence-ledger.md)
- [docs/research/2026-06-01-obviousbench-paper-source-audit.md](../research/2026-06-01-obviousbench-paper-source-audit.md)
- [docs/research/2026-06-01-obviousbench-paper-pdf-build-audit.md](../research/2026-06-01-obviousbench-paper-pdf-build-audit.md)
- [docs/research/2026-06-01-obviousbench-arxiv-source-bundle-audit.md](../research/2026-06-01-obviousbench-arxiv-source-bundle-audit.md)
- [docs/research/2026-06-01-obviousbench-arxiv-submission-checklist.md](../research/2026-06-01-obviousbench-arxiv-submission-checklist.md)
- [docs/research/2026-06-01-obviousbench-arxiv-submission-handoff.md](../research/2026-06-01-obviousbench-arxiv-submission-handoff.md)
- [docs/research/2026-06-01-obviousbench-arxiv-submission-metadata.md](../research/2026-06-01-obviousbench-arxiv-submission-metadata.md)
- [docs/research/2026-06-01-obviousbench-arxiv-internal-review.md](../research/2026-06-01-obviousbench-arxiv-internal-review.md)
- [docs/research/2026-06-01-obviousbench-manuscript-completeness-audit.md](../research/2026-06-01-obviousbench-manuscript-completeness-audit.md)
- [docs/research/2026-06-01-obviousbench-report-section-tracker.md](../research/2026-06-01-obviousbench-report-section-tracker.md)
- [docs/research/2026-06-01-obviousbench-arxiv-blocker-dashboard.md](../research/2026-06-01-obviousbench-arxiv-blocker-dashboard.md)
- [docs/research/2026-06-01-obviousbench-arxiv-completion-roadmap.md](../research/2026-06-01-obviousbench-arxiv-completion-roadmap.md)
- [docs/research/2026-06-01-obviousbench-paper-reproducibility-manifest.md](../research/2026-06-01-obviousbench-paper-reproducibility-manifest.md)
- [docs/research/2026-06-01-obviousbench-public-release-artifact-audit.md](../research/2026-06-01-obviousbench-public-release-artifact-audit.md)
- [docs/research/2026-06-01-obviousbench-public-release-decision-packet.md](../research/2026-06-01-obviousbench-public-release-decision-packet.md)
- The claim audit currently fails with 11 unresolved markers: 10
  `claimblocked` uses and 1 author metadata `obtodo`.
- The claim-evidence ledger maps all 11 unresolved markers to the concrete
  artifacts needed before replacement: submission metadata, abstract/headline
  facts, contribution counts, item-card review, human baseline, final model
  results, and discussion interpretation.
- The static paper-source audit currently reports 5 passing checks and 1
  blocking check. TeX inputs, figures, bibliography files, and citation keys
  resolve; submission markers and placeholders still block final upload.
- The PDF build audit currently reports 0 passing checks and 4 blocking
  checks: no local LaTeX toolchain, static source audit still blocked, no
  `paper/main.pdf`, and no `paper/main.log`.
- The draft arXiv source-bundle audit passes with 58 members and 0 packaging
  issues.
- The submission preflight currently reports 7 passing checks and 5 blocking
  checks: human baseline, paper claim blockers, PDF build artifact, LaTeX build
  toolchain, and submission metadata confirmation.
- The arXiv submission handoff currently reports upload readiness as `NO`.
  The source bundle check passes; PDF inspection, preflight, public release
  links, metadata confirmation, and the blocker dashboard still stop upload.
- The arXiv metadata handoff exists as a machine-audited draft. It intentionally
  fails preflight until the final title, abstract, authors, category, license,
  release links, submitter status, and AI-tool disclosure are confirmed.
- The internal research review currently reports 4 passing checks and 3
  blocking checks. Passing checks cover reproducibility commands, source safety,
  related-work coverage, and limitations/interpretation discipline. Blocking
  checks cover data claims, claim evidence, and final result/analysis artifacts.
- The manuscript completeness audit currently reports 3 passing components, 8
  blocked components, and 0 missing components. Passing components cover related
  work, limitations/ethics/reproducibility, and appendix coverage. Blocked
  components are blocked by unresolved markers, placeholder language, human
  baseline evidence, final model results, metadata, and release facts.
- The report section tracker currently tracks 11 manuscript section entries, 7
  blocked sections, 11 unresolved markers, and 10 draft-placeholder mentions.
  It maps blocked sections to their remaining evidence dependencies.
- The blocker dashboard currently aggregates the paper audits into 11 tracked
  gates: 0 passing, 10 blocked, and 1 waiting. It groups blockers by human data
  collection, provider run after readiness, paper writing after evidence,
  local writing/LaTeX environment, release decisions, and aggregate gates.
- The completion roadmap currently reports the ordered path from scaffold to
  arXiv submission: source/repro inventory passes; human baseline, result
  integration, and submission package phases are blocked; final sweep and
  public release phases are waiting on the earlier gates.
- The public release artifact audit currently reports 2 passing checks and 4
  blocking checks. Public documentation and paper release data are present;
  license/citation files, `pyproject.toml` license metadata, public release
  URLs, and metadata confirmation remain unresolved.
- The public release decision packet currently reports 0 ready decisions and 6
  decisions needing confirmation. It provides draft templates for `LICENSE`,
  `CITATION.cff`, `.zenodo.json`, and `pyproject.toml` metadata, but does not
  create those files or choose a license.
- The reproducibility manifest records byte sizes and SHA-256 hashes for the
  manuscript source, generated paper assets, frozen paper data, model-panel
  configs, human-baseline collection and threshold-audit assets, analysis-plan
  artifacts, audit reports, report section tracker, final-sweep handoff, and
  draft arXiv source bundle. It deliberately omits provider output directories
  and does not make provider calls.

## Current Readiness State

Current readiness status: FAIL.

Passing:

- Dataset validation under manifest-scoped strict paper-readiness mode.
- Item-card review for all 80 paper candidates.
- Scorer-gold coverage.
- Paper split manifest existence and item-ID validation.

Failing:

- Human baseline.

Known blocker details:

- The readiness audit is now manifest-scoped.
- `data/human_baseline/paper_v1.csv` exists as a template but has no response
  rows.
- `data/human_baseline/paper_v1_response_template.csv` has all 400 expected
  participant/item rows, but the collection audit reports no completed
  answer+timing rows yet.
- The stronger human-baseline audit now requires parseable timings, boolean
  correctness, at least 5 participants by default, and coverage for every
  manifest item.
- The paper should not run expensive final model arrays until the human-baseline
  gate passes.

## Verification Run This Turn

Cheap tests only:

```bash
.venv/bin/python -m pytest tests/research/test_arxiv_readiness.py -q
.venv/bin/python -m pytest tests/research/test_arxiv_metadata.py -q
.venv/bin/python -m pytest tests/research/test_arxiv_preflight.py -q
.venv/bin/python -m pytest tests/research/test_arxiv_submission_handoff.py -q
.venv/bin/python -m pytest tests/research/test_arxiv_source_bundle.py -q
.venv/bin/python -m pytest tests/research/test_final_result_artifacts.py -q
.venv/bin/python -m pytest tests/research/test_final_sweep_plan.py -q
.venv/bin/python -m pytest tests/research/test_human_baseline_collection_audit.py -q
.venv/bin/python -m pytest tests/research/test_human_baseline_collection_handoff.py -q
.venv/bin/python -m pytest tests/research/test_item_review_queue.py -q
.venv/bin/python -m pytest tests/research/test_item_card_review.py -q
.venv/bin/python -m pytest tests/research/test_human_baseline_packet.py -q
.venv/bin/python -m pytest tests/research/test_human_baseline_form.py -q
.venv/bin/python -m pytest tests/research/test_human_baseline_scoring.py -q
.venv/bin/python -m pytest tests/research/test_human_baseline_thresholds.py -q
.venv/bin/python -m pytest tests/research/test_human_baseline_operations.py -q
.venv/bin/python -m pytest tests/research/test_internal_review.py -q
.venv/bin/python -m pytest tests/research/test_model_panel_costs.py -q
.venv/bin/python -m pytest tests/research/test_manuscript_completeness.py -q
.venv/bin/python -m pytest tests/research/test_paper_analysis_plan.py -q
.venv/bin/python -m pytest tests/research/test_paper_claim_ledger.py -q
.venv/bin/python -m pytest tests/research/test_paper_claims.py -q
.venv/bin/python -m pytest tests/research/test_paper_completion_roadmap.py -q
.venv/bin/python -m pytest tests/research/test_paper_pdf_audit.py -q
.venv/bin/python -m pytest tests/research/test_pdf_build_handoff.py -q
.venv/bin/python -m pytest tests/research/test_paper_repro_manifest.py -q
.venv/bin/python -m pytest tests/research/test_paper_source_audit.py -q
.venv/bin/python -m pytest tests/research/test_paper_assets.py -q
.venv/bin/python -m pytest tests/research/test_paper_blocker_dashboard.py -q
.venv/bin/python -m pytest tests/research/test_public_release_audit.py -q
.venv/bin/python -m pytest tests/research/test_public_release_decision_packet.py -q
.venv/bin/python -m pytest tests/research/test_related_work_matrix.py -q
.venv/bin/python -m pytest tests/research/test_report_section_tracker.py -q
.venv/bin/python -m pytest tests/configs/test_paper_v1_model_panel.py -q
```

Latest combined result after item-card promotion, human-baseline form work,
model-panel scaffolding, final-sweep dry-run planning, claim-evidence ledger
wiring, static paper-source auditing, submission-preflight wiring, arXiv
metadata template/audit wiring, internal-review wiring, reproducibility
manifest wiring, report-section tracker wiring, analysis-plan wiring, and
human-baseline scoring and threshold-audit wiring, completion-roadmap wiring,
final-result artifact-audit wiring, public-release artifact-audit wiring, and
human-baseline collection-audit wiring, PDF build-audit wiring,
blocker-dashboard wiring, submission-handoff wiring, manuscript-completeness
wiring, release-decision-packet wiring, and human-baseline operations-packet
wiring, related-work matrix wiring, PDF build-handoff wiring, and
human-baseline collection-handoff wiring:

```text
106 passed across the research/model-panel helper test files.
```

Lint/format checks:

```bash
.venv/bin/python -m ruff check obviousbench/research \
  scripts/audit_arxiv_readiness.py \
  scripts/audit_arxiv_source_bundle.py \
  scripts/audit_paper_claims.py \
  scripts/audit_paper_source.py \
  scripts/audit_paper_pdf.py \
  scripts/audit_final_result_artifacts.py \
  scripts/build_paper_analysis_plan.py \
  scripts/build_paper_claim_ledger.py \
  scripts/build_paper_repro_manifest.py \
  scripts/build_pdf_build_handoff.py \
  scripts/build_report_section_tracker.py \
  scripts/build_paper_completion_roadmap.py \
  scripts/build_final_sweep_plan.py \
  scripts/build_arxiv_submission_checklist.py \
  scripts/build_arxiv_submission_handoff.py \
  scripts/build_arxiv_submission_metadata.py \
  scripts/audit_internal_research_review.py \
  scripts/audit_manuscript_completeness.py \
  scripts/audit_human_baseline_collection.py \
  scripts/build_human_baseline_packet.py \
  scripts/build_human_baseline_form.py \
  scripts/score_human_baseline.py \
  scripts/audit_human_baseline_thresholds.py \
  scripts/build_human_baseline_collection_handoff.py \
  scripts/build_human_baseline_operations.py \
  scripts/audit_public_release_artifacts.py \
  scripts/build_public_release_decision_packet.py \
  scripts/build_related_work_matrix.py \
  scripts/build_item_review_queue.py \
  scripts/build_paper_assets.py \
  scripts/build_paper_blocker_dashboard.py \
  scripts/estimate_paper_model_panel_costs.py \
  scripts/promote_paper_item_cards.py \
  tests/research/test_arxiv_readiness.py \
  tests/research/test_arxiv_metadata.py \
  tests/research/test_arxiv_preflight.py \
  tests/research/test_arxiv_submission_handoff.py \
  tests/research/test_arxiv_source_bundle.py \
  tests/research/test_final_result_artifacts.py \
  tests/research/test_final_sweep_plan.py \
  tests/research/test_human_baseline_collection_audit.py \
  tests/research/test_human_baseline_form.py \
  tests/research/test_internal_review.py \
  tests/research/test_item_card_review.py \
  tests/research/test_item_review_queue.py \
  tests/research/test_manuscript_completeness.py \
  tests/research/test_human_baseline_packet.py \
  tests/research/test_human_baseline_scoring.py \
  tests/research/test_human_baseline_thresholds.py \
  tests/research/test_human_baseline_collection_handoff.py \
  tests/research/test_human_baseline_operations.py \
  tests/research/test_model_panel_costs.py \
  tests/research/test_paper_analysis_plan.py \
  tests/research/test_paper_claim_ledger.py \
  tests/research/test_paper_claims.py \
  tests/research/test_paper_completion_roadmap.py \
  tests/research/test_paper_pdf_audit.py \
  tests/research/test_pdf_build_handoff.py \
  tests/research/test_paper_repro_manifest.py \
  tests/research/test_paper_source_audit.py \
  tests/research/test_paper_assets.py \
  tests/research/test_paper_blocker_dashboard.py \
  tests/research/test_public_release_audit.py \
  tests/research/test_public_release_decision_packet.py \
  tests/research/test_related_work_matrix.py \
  tests/research/test_report_section_tracker.py

git diff --check -- <new paper/research files>
```

Latest results:

- Ruff: `All checks passed!`
- `git diff --check`: no whitespace errors for the new paper/research files.
- ASCII scan: no non-ASCII characters in the new paper/research files.
- `make -C paper assets`: passed and regenerated eight current table assets
  and four placeholder PDF figure assets.
- `make -C paper readiness`: failed as expected. Current manifest-scoped
  blocker is the header-only human-baseline CSV with no response rows.
- `make -C paper related-work`: passed and generated the related-work
  positioning matrix with 11 passed comparator coverage checks and 0 blocked
  checks.
- `scripts/build_related_work_matrix.py --strict`: passed with 11 required
  comparator coverage checks present in both the bibliography and related-work
  section.
- `make -C paper human-baseline-packet`: passed and generated 400 assignment
  rows across 5 participants and 80 paper items.
- `make -C paper human-baseline-audit`: passed and generated a blocked
  collection audit with 400/400 response rows present, 0/400 answer+timing rows
  complete, 400 missing answers, 400 invalid timings, and 0 structural issues.
- `scripts/audit_human_baseline_collection.py --strict`: failed as expected
  because 0/400 answer+timing rows are complete.
- `make -C paper human-baseline-collection-handoff`: passed and generated the
  collection execution handoff with 5 participants, 400 response rows, 0
  completed rows, answer-key privacy stop rules, and scoring stop rules.
- `scripts/build_human_baseline_collection_handoff.py --strict`: failed as
  expected because 0/400 answer+timing rows are complete.
- `make -C paper human-baseline-score`: passed and generated a blocked scoring
  report from the empty response template with 0/400 scored rows and 800
  missing-answer/timing issues.
- `make -C paper human-baseline-thresholds`: passed and generated a blocked
  threshold audit from the empty scored draft with 0 core H0 items, 0
  borderline items, 0 excluded items, and 80 `no_data` items.
- `make -C paper human-baseline-ops`: passed and generated the human-baseline
  operations packet with 1 passed gate and 5 blocked gates.
- `scripts/build_human_baseline_operations.py --strict`: failed as expected
  while response collection, scoring, thresholding, promotion, and readiness
  remain blocked.
- `scripts/audit_paper_claims.py`: failed as expected with 11 unresolved paper
  markers.
- `make -C paper claim-ledger`: failed as expected after generating the
  claim-evidence ledger with 11 blocked entries.
- `make -C paper source-audit`: failed as expected after generating the source
  audit with 5 passed checks and 1 failed submission-marker check.
- `make -C paper pdf-audit`: passed and generated a blocked PDF build audit
  with 0 passed checks and 4 failed checks: missing LaTeX toolchain, blocked
  static source audit, missing `paper/main.pdf`, and missing `paper/main.log`.
- `scripts/audit_paper_pdf.py --strict`: failed as expected while those four
  PDF build blockers remain unresolved.
- `make -C paper pdf-handoff`: passed and generated the PDF build handoff with
  the current blocked PDF state, available Homebrew support, Tectonic and
  MacTeX install options, build ladder, inspection checklist, and stop rules.
- `scripts/build_pdf_build_handoff.py --strict`: failed as expected while the
  PDF audit and static source audit remain blocked.
- `make -C paper arxiv-package`: passed and generated `paper/arxiv-src.tar.gz`.
- `scripts/audit_arxiv_source_bundle.py`: passed with 0 bundle issues.
- `make -C paper preflight`: failed as expected after generating the submission
  checklist with 7 passed checks and 5 failed checks.
- `make -C paper submission-handoff`: passed and generated the upload-facing
  handoff with `Upload readiness: NO`, 1 passed check, and 5 failed checks.
- `scripts/build_arxiv_submission_handoff.py --strict`: failed as expected
  while PDF inspection, preflight, release links, metadata confirmation, and
  blocker dashboard checks remain unresolved.
- `make -C paper metadata`: passed. The metadata target preserves an existing
  draft note instead of overwriting it.
- `make -C paper internal-review`: failed as expected after generating the
  internal review with 4 passed checks and 3 failed checks.
- `make -C paper manuscript-completeness`: passed and generated a blocked
  manuscript completeness audit with 3 passed components, 8 blocked components,
  and 0 missing components.
- `scripts/audit_manuscript_completeness.py --strict`: failed as expected
  while 8 manuscript components still depend on metadata, human-baseline,
  final-result, release, and placeholder-removal evidence.
- `make -C paper sweep-plan`: passed and generated the final-sweep handoff with
  12 model commands and `Run allowed: NO`.
- `make -C paper result-artifacts`: passed and generated the final-result
  artifact audit with 12 planned models, 0/6 comparison files present, and
  missing per-model summaries/reports as expected before the final sweep.
- `make -C paper release-audit`: passed and generated the public release
  artifact audit with 2 passing checks and 4 blocking checks: missing
  license/citation/archive metadata files, missing package license metadata,
  placeholder public URLs, and unconfirmed arXiv metadata.
- `make -C paper release-packet`: passed and generated the public release
  decision packet with 0 ready decisions and 6 decisions needing confirmation.
- `scripts/build_public_release_decision_packet.py --strict`: failed as
  expected while license, citation, archive, package license metadata, public
  URLs, and submitter/final metadata decisions remain unconfirmed.
- `make -C paper analysis-plan`: passed and generated the frozen analysis plan
  with 0 issues and 3 primary metrics.
- `make -C paper report-tracker`: passed and generated the report section
  tracker with 11 section entries, 7 blocked sections, 11 unresolved markers,
  and 10 draft-placeholder mentions.
- `make -C paper blocker-dashboard`: passed and generated the consolidated
  blocker dashboard with 0 passing gates, 10 blocked gates, and 1 waiting gate.
- `scripts/build_paper_blocker_dashboard.py --strict`: failed as expected while
  the dashboard still has 10 blocked gates and 1 waiting gate.
- `make -C paper completion-roadmap`: passed and generated the ordered arXiv
  completion roadmap with 1 passing phase, 3 blocked phases, and 2 waiting
  phases.
- `make -C paper repro-manifest`: passed and generated the reproducibility
  manifest for 64 current paper artifacts with 0 missing required files.

## Next To Do

1. Collect real participant answers in
   `data/human_baseline/paper_v1_response_template.csv`, rerun the collection
   audit until it passes, rerun scoring and threshold classification, then
   promote the checked scored data to
   `data/human_baseline/paper_v1.csv` once readiness can pass.
2. Add final model-result table and figure generators after real sweeps exist.
3. Replace placeholder PDF figures with real plots after final sweeps exist.
4. Run final model arrays only after the data/human gates are green, using the
   generated final-sweep handoff.
5. Replace `\claimblocked{...}` paper markers with evidence-backed final prose.
6. Build and inspect the final PDF in a LaTeX-enabled environment, then rerun
   `make -C paper pdf-audit` until the toolchain, source, PDF, and log checks
   pass.
7. Confirm final arXiv submission metadata in the generated metadata note.
8. Confirm public release license, citation, archive metadata, repository URL,
   and dataset/artifact URL before marking metadata as confirmed.
