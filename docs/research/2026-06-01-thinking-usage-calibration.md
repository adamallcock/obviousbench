---
title: Thinking Usage Calibration
date: 2026-06-01
type: research
status: complete
---

# Thinking Usage Calibration

The first thinking-panel estimate treated configured thinking budgets as expected
usage. That was too pessimistic for ObviousBench short-answer prompts.

This calibration separates:

- configured cap: the provider request budget or effort depth we want to test,
- estimated usage: expected billed reasoning or thinking tokens per sample.

## Live Probe

Live probe path:
`results/summaries/thinking-usage-calibration-20260601-live/results.jsonl`

Prompt: one hard-obvious style numeric-comparison item.

| Probe | Status | Input | Output | Reasoning | Notes |
| --- | --- | ---: | ---: | ---: | --- |
| `openai-gpt-5-low-live` | ok | 38 | 51 | 0 | OpenAI reported no reasoning tokens for this low-effort sample. |
| `openai-gpt-5-high-live` | ok | 38 | 192 | 128 | Far below the previous 4096-token high estimate. |
| `anthropic-sonnet-4-5-thinking-1024-live` | ok | 71 | 91 | n/a | Anthropic did not expose a separate reasoning-token field; 1024 budget was not fully consumed. |
| `anthropic-opus-4-8-adaptive-low-live` | ok | 52 | 5 | n/a | Adaptive low returned a short direct answer. |
| `grok-4-3-high-live` | ok | 156 | 3 | 228 | Higher than OpenAI/Gemini on this prompt, but still far below the old 4096-token high estimate. |
| `openrouter-gemini-3-5-flash-high-live` | ok | 35 | 193 | 190 | Matches prior Gemini OpenRouter runs around ~180-200 reasoning tokens/sample. |
| `openrouter-deepseek-r1-0528-high-live` | ok | 37 | 522 | 512 | Hit the 512-token probe cap; estimate keeps a larger buffer for DeepSeek R1 high. |

## Historical Runs

Existing measured summaries under `results/summaries/*/usage_by_sample.csv`
already contain full 80-sample usage reports.

| Run | Model | Effort | Avg reasoning | P95 reasoning | Max reasoning |
| --- | --- | --- | ---: | ---: | ---: |
| `hard-obvious-gpt-5-5-medium-v2-20260531` | `openai/gpt-5.5` | medium | 24.4 | 70 | 143 |
| `hard-obvious-gpt-5-4-high-v2-20260531` | `openai/gpt-5.4` | high | 37.3 | 116 | 272 |
| `gpt-5-4-high-balanced_8x10-20260531-075312` | `openai/gpt-5.4` | high | 44.4 | 113 | 233 |
| `gpt-5-low-balanced_8x10-20260531-001449` | `openai/gpt-5` | low | 33.6 | 128 | 320 |
| `grok-4-3-xai-balanced_8x10-20260531-075934` | `grok/grok-4.3` | default | 274.8 | 490 | 631 |
| `grok-4-20-xai-balanced_8x10-20260531-075934` | `grok/grok-4.20` | default | 633.8 | 1266 | 6339 |
| `gemini-3-5-flash-openrouter-balanced_8x10-20260531-080345` | `openrouter/google/gemini-3.5-flash` | default | 197.9 | 307 | 446 |
| `gemini-3-1-pro-preview-openrouter-balanced_8x10-20260531-080345` | `openrouter/google/gemini-3.1-pro-preview` | default | 181.5 | 284 | 314 |
| `openrouter-free-gpt-oss-120b-balanced_8x2-20260531-002234` | `openrouter/openai/gpt-oss-120b:free` | default | 15.0 | 29 | 34 |

## Adjustment

`scripts/build_thinking_model_panel.mjs` now preserves configured caps in
`provider_request_settings`, but estimates cost from calibrated expected usage.

New total for `configs/model_thinking_settings_v1.yaml`: `$68.108235` for 231
settings, down from `$2635.264155`.
