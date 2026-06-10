---
title: ObviousBench Paper Claim Evidence Ledger
date: 2026-06-01
type: review
status: blocked
---

# ObviousBench Paper Claim Evidence Ledger

This ledger turns unresolved manuscript markers into artifact-backed
replacement work. It is editorial guidance; the claim-blocker audit
remains the hard gate.

Overall status: BLOCKED

Blocked entries: 6

| Location | Marker | Category | Required evidence | Source artifacts | Acceptance |
| --- | --- | --- | --- | --- | --- |
| main.tex:39 | claimblocked | final model results | Frozen paper-sweep summaries, comparison tables, and generated figures. | docs/research/2026-06-01-paper-v1-final-sweep-plan.md, configs/paper_v1_final_sweep_manifest.csv, results/summaries/paper-v1-final-high-cap/comparison, paper/tables/main_results.tex, paper/figures/leaderboard.pdf | Final sweep is complete and paper assets are regenerated from it. |
| sections/01_introduction.tex:33 | claimblocked | introduction contributions | Exact paper split counts, review counts, model-panel size, and release links. | data/splits/paper_v1_manifest.jsonl, data/item_cards/public_v0/cards.yaml, configs/paper_v1_model_panel.yaml, docs/research/2026-06-01-obviousbench-arxiv-submission-metadata.md | Contribution list uses exact artifact-backed counts and links. |
| sections/03_benchmark.tex:38 | claimblocked | data and item-card review | Manifest-scoped readiness audit and reviewed item cards. | data/splits/paper_v1_manifest.jsonl, data/item_cards/public_v0/cards.yaml, docs/research/2026-06-01-obviousbench-arxiv-readiness-audit.md | Readiness and item-card gates pass for all paper items. |
| sections/06_results.tex:61 | claimblocked | final model results | Frozen paper-sweep summaries, comparison tables, and generated figures. | docs/research/2026-06-01-paper-v1-final-sweep-plan.md, configs/paper_v1_final_sweep_manifest.csv, results/summaries/paper-v1-final-high-cap/comparison, paper/tables/main_results.tex, paper/figures/leaderboard.pdf | Final sweep is complete and paper assets are regenerated from it. |
| sections/07_analysis.tex:50 | claimblocked | final model results | Frozen paper-sweep summaries, comparison tables, and generated figures. | docs/research/2026-06-01-paper-v1-final-sweep-plan.md, configs/paper_v1_final_sweep_manifest.csv, results/summaries/paper-v1-final-high-cap/comparison, paper/tables/main_results.tex, paper/figures/leaderboard.pdf | Final sweep is complete and paper assets are regenerated from it. |
| sections/08_discussion.tex:18 | claimblocked | discussion interpretation | Final result patterns plus limitations-reviewed interpretation. | results/summaries/paper-v1-final-high-cap/comparison, docs/research/2026-06-01-obviousbench-arxiv-internal-review.md, paper/sections/08_discussion.tex | Discussion cites observed patterns without unsupported rankings or mechanisms. |

## Marker Text

- `main.tex:39` `claimblocked`: Replace placeholder result language with final split size, model panel size, headline score ranges, release links, and run dates after the frozen paper sweep.
- `sections/01_introduction.tex:33` `claimblocked`: Replace this contribution list with exact split size, review counts, scorer-gold counts, and artifact links after the final release artifacts are frozen.
- `sections/03_benchmark.tex:38` `claimblocked`: Before submission, every \paperSplit{} item must have a reviewed item card with source summary, answer derivation, ambiguity notes, scorer contract, and split-policy rationale.
- `sections/06_results.tex:61` `claimblocked`: Replace every draft proof-point table and figure with the frozen paper sweep before final submission. Do not hand-copy values from exploratory or superseded reports.
- `sections/07_analysis.tex:50` `claimblocked`: Populate this section from final generated comparison artifacts: family comparison, paired variants, usage exports, and failure galleries.
- `sections/08_discussion.tex:18` `claimblocked`: After final results, add a brief discussion of observed model families, effort settings, and cost/quality tradeoffs without overstating rankings.
