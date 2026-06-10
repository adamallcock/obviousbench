---
title: ObviousBench Paper Analysis Plan
date: 2026-06-01
type: research
status: ready
---

# ObviousBench Paper Analysis Plan

This document records the paper's reporting and statistical analysis
policy for the selected evidence run. It is generated from
`configs/paper_v1_analysis_plan.yaml` and does not run provider calls.

Overall status: PASS

Plan status: `frozen_for_first_draft_evidence_run`
Applies to: `paper_v1`
No provider calls: `True`

## Summary

- Primary metrics: 1
- Secondary metrics: 7
- Reported tables: 5
- Reported figures: 4

## Frozen Inputs

| Input | Path |
| --- | --- |
| `dataset_manifest` | `data/splits/paper_v1_manifest.jsonl` |
| `model_panel` | `configs/paper_v1_combined_234_overline_attempt_scored_20260602_manifest.csv` |
| `human_baseline` | `data/human_baseline/paper_v1.csv (deferred; not reported in fast preprint)` |
| `final_comparison_dir` | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/comparison` |
| `final_report_dir` | `docs/reports/2026-06-02-paper-v1-combined-234-overline` |
| `scoring_gold_dir` | `tests/fixtures/scorer_gold` |
| `evidence_run` | `paper-v1-combined-234-overline-attempt-scored-20260602` |
| `wrong_answer_review` | `docs/reports/2026-06-02-paper-v1-combined-234-overline/wrong-answer-review.csv` |

## Primary Metrics

| ID | Label | Source column | Interpretation |
| --- | --- | --- | --- |
| answer_accuracy | Answer correctness | answer_accuracy | Primary model reliability metric; accepts correct answers even when surrounding prose violates a strict interface. |

## Secondary Metrics

| ID | Label | Source column | Interpretation |
| --- | --- | --- | --- |
| obvious_failure_rate | Obvious failure rate | obvious_failure_rate | One minus answer-level correctness over scored samples. |
| format_accuracy | Format accuracy | format_accuracy | Secondary compliance diagnostic; not the headline benchmark score. |
| strict_accuracy | Strict accuracy | strict_accuracy | Secondary exact-interface diagnostic equal to answer-and-format success. |
| provider_errors | Provider errors | provider_errors | Reported separately; final provider errors count as incorrect scored attempts after retries. |
| cost_per_correct_usd | Cost per correct answer | cost_per_correct_usd | Secondary efficiency metric; never outranks accuracy. |
| tokens_per_correct | Tokens per correct answer | tokens_per_correct | Secondary token-efficiency metric. |
| overthinking_index | Overthinking index | overthinking_index | Exploratory when reasoning-token reporting is available. |

## Intervals

| Estimate | Method | Implementation |
| --- | --- | --- |
| binomial | Wilson score interval | obviousbench.analysis.statistics.wilson_interval |
| paired_deltas | deterministic percentile bootstrap over matched item IDs | obviousbench.analysis.statistics.paired_boolean_delta |

## Reported Tables

| ID | Path | Source | Pre-sweep status |
| --- | --- | --- | --- |
| main_results | `paper/tables/main_results.tex` | final comparison leaderboard |  |
| family_results | `paper/tables/family_results.tex` | final family comparison |  |
| thinking_group_results | `paper/tables/thinking_group_results.tex` | final comparison grouped by inferred thinking mode |  |
| model_family_results | `paper/tables/model_family_results.tex` | final comparison grouped by model family |  |
| failure_type_summary | `paper/tables/failure_type_summary.tex` | wrong-answer review failure-type taxonomy |  |

## Audit Artifacts

| ID | Path | Source | Pre-sweep status |
| --- | --- | --- | --- |
| provider_exclusions | `paper/tables/provider_exclusions.tex` | final provider error and timeout accounting | audit_artifact_not_manuscript_table |

## Reported Figures

| ID | Path | Source | Pre-sweep status |
| --- | --- | --- | --- |
| leaderboard | `paper/figures/leaderboard.pdf` | final answer-correctness leaderboard |  |
| family_heatmap | `paper/figures/family_heatmap.pdf` | final family answer-correctness comparison |  |
| answer_format_gap | `paper/figures/answer_format_gap.pdf` | answer correctness minus strict accuracy by model |  |
| cost_frontier | `paper/figures/cost_frontier.pdf` | answer correctness versus estimated cost |  |

## Exclusion Policy

- `provider_errors`: Count final provider errors as incorrect scored attempts after configured retries; report counts and rates separately.
- `timeouts`: Count final timeouts as incorrect scored attempts after configured retries; report counts and rates separately.
- `parse_errors`: Score as incorrect when a response was delivered but not parseable by the deterministic scorer.
- `duplicate_runs`: Use the frozen model-panel run manifest; do not cherry-pick retries.
- `incomplete_models`: Keep visible in provider exclusions; do not rank against complete runs.

## Human Baseline Policy

- `status`: deferred_for_fast_preprint
- `current_use`: Do not report human accuracy, response time, or model-versus-human gaps in v1.
- `item_validity_substitute`: Use reviewed item cards, answer derivations, ambiguity notes, and scorer-gold evidence.
- `future_minimum_participants`: 5
- `future_collection_trigger`: Collect only after paper_v1 items, instructions, answer key, scorers, and thresholds are frozen.

## Claim Policy

- `reporting_vs_hypothesis_generation`: Final article should be primarily reporting and measurement, with hypothesis generation limited to clearly labeled discussion.
- `solution_policy`: Mitigation ideas belong in discussion or future work; they must not dominate the results section.
- `ranking_policy`: Rank by answer correctness with intervals and denominators visible; report strict accuracy as a secondary compliance diagnostic.
- `release_policy`: Every headline claim must cite a frozen local artifact or generated table/figure.
