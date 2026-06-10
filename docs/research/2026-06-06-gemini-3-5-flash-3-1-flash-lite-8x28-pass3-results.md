---
title: Gemini 3.5 Flash And 3.1 Flash Lite 8x28 Pass^3 Results
date: 2026-06-06
type: report
status: complete
---

# Gemini 3.5 Flash And 3.1 Flash Lite 8x28 Pass^3 Results

## Run

- Panel: `configs/gemini_3_5_flash_3_1_flash_lite_pass3_8x28_20260606_panel.yaml`
- Dataset: `data/barrages/hard_obvious_8x28_seed_20260531.jsonl`
- Status ledger: `results/summaries/gemini-3-5-flash-3-1-flash-lite-pass3-8x28-20260606/status.jsonl`
- Entries: 24 passed / 24 total.
- Cache busting: launched with `--no-cache --no-skip-completed`.
- Concurrency: each Inspect eval used `--max-connections=128`.
- Scoring: `--score-on-error` was enabled, so provider-error samples count as scored failures.
- Direct Gemini route: `google/gemini-3.5-flash` and `google/gemini-3.1-flash-lite`.

Gemini thinking settings were sent through Inspect `reasoning_effort`, which maps
to Gemini `thinkingLevel` for Gemini 3 models. The panel does not set explicit
generation seeds.

Cost note: with `runcost` 0.1.4, reported Gemini reasoning tokens are emitted as
`output_reasoning_tokens` ledger components and priced using the Gemini output
token rate. The component metadata records
`pricing_policy=gemini_thinking_tokens_priced_as_output_tokens`.

## Answer-Correct Pass^3

Primary score here is `answer_correct` pass^3. `strict_correct` pass^3 is shown beside it for format-sensitive comparison.

| model | mode | answer pass1 | answer pass^3 | strict pass^3 | pass^3 cost | provider errors |
|---|---:|---:|---:|---:|---:|---:|
| Gemini 3.5 Flash | minimal | 92.1% | 90.6% | 90.6% | $0.0596 | 0 |
| Gemini 3.5 Flash | low | 99.0% | 97.8% | 97.8% | $0.8070 | 0 |
| Gemini 3.5 Flash | medium | 98.8% | 98.7% | 98.7% | $1.323 | 0 |
| Gemini 3.5 Flash | high | 98.7% | 98.2% | 98.2% | $1.392 | 0 |
| Gemini 3.1 Flash Lite | minimal | 90.5% | 89.3% | 89.3% | $0.0097 | 0 |
| Gemini 3.1 Flash Lite | low | 94.2% | 91.1% | 91.1% | $0.1347 | 0 |
| Gemini 3.1 Flash Lite | medium | 98.8% | 97.8% | 97.8% | $0.1504 | 0 |
| Gemini 3.1 Flash Lite | high | 98.8% | 97.3% | 97.3% | $0.2528 | 0 |

Total measured cost for these 24 runs: $4.130. Provider-error samples scored: 0.

## Provider-Error Samples

- None.

## Chart

The combined pass^3 cost curve is in `docs/reports/2026-06-06-pass3-effort-cost-curves/pass3-answer-log-cost.svg`.
