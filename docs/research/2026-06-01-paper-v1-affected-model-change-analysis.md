---
title: Paper V1 Affected Model Change Analysis
date: 2026-06-01
type: research
status: draft
---

# Paper V1 Affected Model Change Analysis

This note separates two effects discovered while reviewing wrong answers in the paper-v1 final sweep: current deterministic rescoring of old outputs, and fresh reruns under the 10,000-token output safety cap.

## Inputs

- Original report: `docs/reports/2026-06-01-paper-v1-final-sweep/leaderboard.csv`.
- Old-output rescore manifest: `configs/paper_v1_final_rescored_20260601_manifest.csv`.
- Old-output rescore comparison: `results/summaries/paper-v1-final-rescored-20260601/comparison/comparison.csv`.
- Major affected rerun: `configs/paper_v1_affected_rerun_10k_manifest.csv` and `results/summaries/paper-v1-affected-rerun-10k/comparison/comparison.csv`.
- Minor cap-affected rerun: `configs/paper_v1_minor_cap_rerun_10k_manifest.csv` and `results/summaries/paper-v1-minor-cap-rerun-10k/comparison/comparison.csv`.
- Combined affected rerun: `configs/paper_v1_cap_affected_rerun_10k_manifest.csv` and `results/summaries/paper-v1-cap-affected-rerun-10k/comparison/comparison.csv`.
- Comparison CSV: `docs/research/2026-06-01-paper-v1-affected-model-change-analysis.csv`.

## Result

| Model | Original answer | Rescored answer | 10k answer | Original strict | Rescored strict | 10k strict | Old max-token stops | 10k max-token stops | 10k provider errors |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| OpenAI GPT-5 nano minimal | 63/80 | 63/80 | 64/79 | 62/80 | 62/80 | 64/79 | 1 | 0 | 1 |
| Anthropic Claude Sonnet 4.6 | 67/80 | 71/80 | 71/80 | 67/80 | 68/80 | 67/80 | 1 | 0 | 0 |
| Anthropic Claude Haiku 4.5 | 68/80 | 69/80 | 69/80 | 58/80 | 59/80 | 59/80 | 1 | 0 | 0 |
| Gemini 3.5 Flash | 33/80 | 33/80 | 80/80 | 33/80 | 33/80 | 80/80 | 62 | 0 | 0 |
| Grok 4.3 | 65/70 | 69/70 | 68/70 | 39/70 | 39/70 | 38/70 | 4 | 0 | 10 |
| NVIDIA Nemotron 3 Nano 30B A3B | 12/80 | 12/80 | 73/80 | 11/80 | 11/80 | 73/80 | 77 | 1 | 0 |
| OpenAI GPT-OSS 20B | 30/80 | 30/80 | 76/80 | 30/80 | 30/80 | 76/80 | 51 | 1 | 0 |

## Interpretation

- Rescoring alone produces modest movement on normal text-edge cases, but it does not materially change the three heavily truncation-hit models.
- Rerunning under the 10,000-token cap materially changes Gemini 3.5 Flash, GPT-OSS 20B, and Nemotron 3 Nano. These old 64-token results should be treated as invalid for paper claims.
- Gemini 3.5 Flash moves from 33/80 answer-correct to 80/80, with max-token stops dropping from 62 to 0. This confirms the old JSON/empty-answer issue was generation truncation, not a parser failure.
- GPT-OSS 20B moves from 30/80 answer-correct to 76/80, with max-token stops dropping from 51 to 1. The remaining capped sample produced an empty completion and should be disclosed or rerun manually if GPT-OSS is central.
- Nemotron 3 Nano moves from 12/80 answer-correct to 73/80, with max-token stops dropping from 77 to 1. The remaining capped sample spirals on a spelling item and is a genuine model/output-control failure, not just a parser issue.
- Claude Sonnet, Claude Haiku, and GPT-5 nano had only one old max-token stop each. Their 10k reruns move only modestly compared with the three heavily truncated models.
- GPT-5 nano rerun has one provider/content-filter refusal. The analysis parser now treats structured `content_filter` stops as provider errors, so the rerun denominator is 79 scored samples.
- Grok 4.3 remains operationally awkward: answer correctness is high on scored samples, but the run still has 10 provider/content-filter errors and poor format compliance. The panel command failed only because the refusal retry path remained; this note summarizes the first 80-sample eval directly for comparability.
- The GPT-5 nano rerun emitted the provider warning that reasoning-enabled OpenAI models ignore `temperature`; this should be documented in the methods, but it did not fail the run.

## Recommendation

Do not use the original `paper-v1-final` 64-token model results in the paper. The minimum next step is to rebuild the final paper report from the 10k-cap affected reruns, but the cleaner paper-grade path is to run a fresh 12-model final sweep under the current 10k cap and current scorer, then regenerate all figures/tables from that single frozen run.

For Grok, either keep it explicitly unranked with provider-error disclosure, or exclude it from the main leaderboard and mention it in an appendix/limitations note until the content-filter path is resolved.

If GPT-OSS or Nemotron become headline models, inspect or rerun their single residual 10k-capped samples before making a tight claim about exact accuracy. Their overall movement is already material enough to invalidate the 64-token results.

## Stop Reason Detail

| Model | Original stop counts | 10k stop counts |
|---|---|---|
| OpenAI GPT-5 nano minimal | `{'stop': 79, 'max_tokens': 1}` | `{'stop': 79, 'content_filter': 1}` |
| Anthropic Claude Sonnet 4.6 | `{'stop': 79, 'max_tokens': 1}` | `{'stop': 80}` |
| Anthropic Claude Haiku 4.5 | `{'stop': 79, 'max_tokens': 1}` | `{'stop': 80}` |
| Gemini 3.5 Flash | `{'stop': 18, 'max_tokens': 62}` | `{'stop': 80}` |
| Grok 4.3 | `{'stop': 66, 'max_tokens': 4, 'content_filter': 10}` | `{'stop': 70, 'content_filter': 10}` |
| NVIDIA Nemotron 3 Nano 30B A3B | `{'max_tokens': 77, 'stop': 3}` | `{'stop': 79, 'max_tokens': 1}` |
| OpenAI GPT-OSS 20B | `{'stop': 29, 'max_tokens': 51}` | `{'stop': 79, 'max_tokens': 1}` |
