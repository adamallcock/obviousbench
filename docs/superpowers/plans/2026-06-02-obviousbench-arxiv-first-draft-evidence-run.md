---
title: ObviousBench Arxiv First Draft Evidence Run
date: 2026-06-02
type: plan
status: in_progress
---

# ObviousBench Arxiv First Draft Evidence Run

## Decision

Use `paper-v1-combined-234-overline-attempt-scored-20260602` as the evidence
base for the first arXiv draft.

This replaces the older proof-point placeholder and the earlier 12-model
high-cap sweep contract for manuscript drafting. Human-baseline rows remain
deferred for the fast-preprint version; the manuscript must not report measured
human accuracy, response-time distributions, or model-versus-human gaps.

## Source Artifacts

- Dataset manifest: `data/splits/paper_v1_manifest.jsonl`
- Evidence manifest:
  `configs/paper_v1_combined_234_overline_attempt_scored_20260602_manifest.csv`
- Comparison directory:
  `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/comparison`
- HTML report:
  `docs/reports/2026-06-02-paper-v1-combined-234-overline/report.html`
- Wrong-answer review:
  `docs/reports/2026-06-02-paper-v1-combined-234-overline/wrong-answer-review.csv`

## Paper Claims Allowed

- The split has 80 reviewed paper items across eight families.
- The evidence run has 234 model settings and 189 unique model identifiers.
- Full rows have 80 scored attempts; final provider errors, refusals, and
  timeouts count as incorrect attempts after the configured retry policy.
- The run has 24 perfect answer-correctness rows, 77 rows at or above 95%
  answer correctness, and 45 rows below 80%.
- Character counting and spelling transforms are the main aggregate weak
  families in the current evidence run.
- Failure taxonomy claims may use the generated wrong-answer review CSV.

## Paper Claims Not Allowed

- Measured human accuracy or human response-time claims.
- Model-versus-human gaps.
- Causal claims about hidden model mechanisms.
- Stable market-wide rankings beyond the recorded model aliases, routes,
  generation settings, pricing assumptions, and run date.

## Execution Checklist

- [x] Point `make -C paper assets` at the current evidence run.
- [x] Point `make -C paper result-artifacts` at the current evidence run.
- [x] Update the analysis-plan YAML to the current evidence paths.
- [x] Replace proof-point language in abstract, results, analysis, and
  discussion.
- [x] Regenerate paper tables, figures, and paper audit reports.
- [x] Run the claim, manuscript-completeness, result-artifact, source, and
  internal-review gates.
- [x] Build and inspect the PDF.
- [ ] Finalize release metadata, public repository/dataset URLs, and arXiv
  submission handoff.

## Definition Of Done For First Draft

- `make -C paper result-artifacts` passes.
- `make -C paper claims` passes with zero unresolved manuscript markers.
- `make -C paper manuscript-completeness --strict` passes.
- `make -C paper internal-review` passes or reports only explicitly accepted
  release/PDF blockers.
- `paper/main.pdf` builds from the regenerated source and is manually
  inspectable.
- The arXiv source bundle contains TeX source, tables, figures, and references,
  but no raw provider logs or credentials.
