---
title: ObviousBench v0.2 Public Aggregate Report
date: 2026-06-18
type: report
status: public-release-candidate
---

# ObviousBench v0.2 Public Aggregate Report

Canonical narrative and interactive charts:
[https://obviousbench.com](https://obviousbench.com)

This report is the public-safe aggregate evidence for the v0.2 held-out
`pass^3` run. It contains model/configuration-level aggregate metrics only. It
does not include private prompts, raw completions, provider logs, private review
HTML, or item-level private outcomes.

## Snapshot

| Metric | Value |
| --- | ---: |
| Held-out items | 144 |
| Model/config rows | 293 |
| Complete model/config rows | 293 |
| Attempt rows | 126,576 |
| Scored attempts | 126,576 |
| Estimated measured run cost | $131.00 |
| Provider errors in public snapshot | 0 |
| Aggregate manual-adjustment footprint | 14 attempts across 9 rows |

The public aggregate CSV is
[`summary.csv`](summary.csv). It includes a `manual_adjusted_attempts` column for
aggregate transparency; attempt-level source rows are outside the public release
surface.

## Headline Metric

The headline metric is answer `pass^3`: all three sampled attempts for an item
must contain the correct answer. Strict and format metrics remain useful
diagnostically, but the public story emphasizes non-strict answer correctness
because a correct answer inside a verbose response and a wrong answer are
different product risks.

## Top Rows By Answer pass^3

Rows below are sorted by answer `pass^3`, then lower measured run cost.

| Model/config | Effort | Answer pass^3 | Est. cost | Reasoning tokens |
| --- | --- | ---: | ---: | ---: |
| Google: Gemma 4 31B high | high | 100.0% | $0.025 | 43,350 |
| Google: Gemma 4 31B low | low | 100.0% | $0.027 | 44,722 |
| Qwen: Qwen3.5-27B | default | 100.0% | $0.273 | 160,625 |
| OpenRouter openai/o3 medium | medium | 100.0% | $0.536 | 46,428 |
| OpenRouter openai/o3 high | high | 100.0% | $0.621 | 56,094 |
| OpenAI openai/gpt-5 medium | medium | 100.0% | $0.708 | 51,584 |
| OpenAI GPT-5.5 medium | medium | 100.0% | $0.744 | 17,991 |
| Google: Gemini 3.5 Flash high | high | 100.0% | $0.996 | 106,673 |
| OpenAI GPT-5.5 xhigh | xhigh | 100.0% | $1.090 | 29,507 |
| OpenAI openai/gpt-5 high | high | 100.0% | $1.174 | 97,728 |
| Grok Build 0.1 | default | 99.3% | $0.022 | 299,679 |
| Google: Gemma 4 31B medium | medium | 99.3% | $0.025 | 41,697 |

## Cost-Efficient Near-Ceiling Rows

Rows below are the cheapest rows at or above 95.0% answer `pass^3`.

| Model/config | Effort | Answer pass^3 | Est. cost | Reasoning tokens |
| --- | --- | ---: | ---: | ---: |
| Grok Build 0.1 | default | 99.3% | $0.022 | 299,679 |
| Google: Gemma 4 31B high | high | 100.0% | $0.025 | 43,350 |
| Google: Gemma 4 31B medium | medium | 99.3% | $0.025 | 41,697 |
| Google: Gemma 4 31B low | low | 100.0% | $0.027 | 44,722 |
| Google: Gemma 4 26B A4B medium | medium | 96.5% | $0.035 | 88,645 |
| Google: Gemma 4 26B A4B high | high | 95.8% | $0.036 | 83,789 |
| Google: Gemma 4 26B A4B low | low | 96.5% | $0.038 | 95,033 |
| OpenAI GPT-5 nano medium | medium | 95.1% | $0.055 | 118,656 |
| OpenAI openai/gpt-5-nano high | high | 97.2% | $0.110 | 256,507 |
| Google: Gemini 3.1 Flash Lite medium | medium | 95.8% | $0.118 | 74,360 |
| Qwen: Qwen3 30B A3B Thinking 2507 | default | 96.5% | $0.137 | 334,987 |
| OpenAI openai/gpt-5-mini medium | medium | 95.1% | $0.140 | 50,432 |

## Public / Private Boundary

The public repository is the source and data companion for the release: runnable
benchmark code, public examples, model/config metadata, public aggregate CSVs,
and reproducibility documentation. The launch website is the canonical narrative
and interactive chart surface.

Do not add private held-out prompts, raw completions, provider logs, private
review HTML, local caches, or item-level private outcomes to this repository.
