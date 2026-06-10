---
title: GPT-5.5 And Sonnet 4.6 8x28 Pass^3 Results
date: 2026-06-06
type: report
status: complete
---

# GPT-5.5 And Sonnet 4.6 8x28 Pass^3 Results

## Run

- Panel: `configs/gpt_5_5_sonnet_4_6_pass3_8x28_20260606_panel.yaml`
- Dataset: `data/barrages/hard_obvious_8x28_seed_20260531.jsonl`
- Status ledger: `results/summaries/gpt-5-5-sonnet-4-6-pass3-8x28-20260606/status.jsonl`
- Entries: 27 passed / 27 total.
- Cache busting: launched with `--no-cache --no-skip-completed`.
- Concurrency: each Inspect eval used `--max-connections=128`.
- Scoring: `--score-on-error` was enabled, so provider-error samples count as scored failures.

OpenAI Responses emitted the expected provider warning that the `seed` parameter is unsupported. Anthropic adaptive-thinking entries were generated with `reasoning_effort` settings.

## Answer-Correct Pass^3

Primary score here is `answer_correct` pass^3. `strict_correct` pass^3 is shown beside it for format-sensitive comparison.

| model | mode | answer pass1 | answer pass^3 | strict pass^3 | pass^3 cost | provider errors |
|---|---:|---:|---:|---:|---:|---:|
| GPT-5.5 | none | 95.7% | 94.6% | 94.6% | $0.2775 | 1 |
| GPT-5.5 | low | 100.0% | 100.0% | 100.0% | $0.8757 | 0 |
| GPT-5.5 | medium | 99.7% | 99.1% | 99.1% | $1.013 | 1 |
| GPT-5.5 | high | 99.6% | 98.7% | 98.7% | $1.268 | 0 |
| GPT-5.5 | xhigh | 99.3% | 98.7% | 98.7% | $1.575 | 2 |
| Claude Sonnet 4.6 | low | 88.1% | 87.1% | 83.9% | $0.1641 | 0 |
| Claude Sonnet 4.6 | medium | 95.1% | 94.2% | 89.3% | $0.2253 | 0 |
| Claude Sonnet 4.6 | high | 98.1% | 97.3% | 80.4% | $0.6980 | 0 |
| Claude Sonnet 4.6 | max | 99.1% | 98.2% | 83.9% | $0.9569 | 0 |

Total measured cost for these 27 runs: $7.054. Provider-error samples scored: 4.

## Provider-Error Samples

- `gpt-5-5-medium-trial-02` `obviousbench.arith.en.v0.public.000015` (arithmetic)
- `gpt-5-5-none-trial-02` `obviousbench.negation.en.v0.public.000030` (negation)
- `gpt-5-5-xhigh-trial-01` `obviousbench.negation.en.v0.public.000026` (negation)
- `gpt-5-5-xhigh-trial-03` `obviousbench.char_count.en.v0.public.000010` (character_count)

## Chart

The combined pass^3 cost curve is in `docs/reports/2026-06-06-pass3-effort-cost-curves/pass3-answer-log-cost.svg`.
