---
title: Paper V1 Model Panel Cost Estimates
date: 2026-06-01
type: research
status: draft
---

# Paper V1 Model Panel Cost Estimates

Dry-run estimates only. No model provider calls were made.

| Model | Inspect model | Samples | Billable | Estimated cost | Pricing source |
| --- | --- | ---: | ---: | ---: | --- |
| OpenAI GPT-5 nano minimal | openai/gpt-5-nano | 80 | 80 | $0.000721 | runcost |
| OpenAI GPT-4.1 | openai/gpt-4.1 | 80 | 80 | $0.008582 | runcost |
| OpenAI GPT-4.1 mini | openai/gpt-4.1-mini | 80 | 80 | $0.006264 | runcost |
| Anthropic Claude Sonnet 4.6 | anthropic/claude-sonnet-4-6 | 80 | 80 | $0.021243 | runcost |
| Anthropic Claude Haiku 4.5 | anthropic/claude-haiku-4-5 | 80 | 80 | $0.006696 | runcost |
| Gemini 3.5 Flash | google/gemini-3.5-flash | 80 | 80 | $0.003204 | runcost |
| Gemini 2.5 Flash-Lite | google/gemini-2.5-flash-lite | 80 | 80 | $0.000214 | runcost |
| Grok 4.3 | grok/grok-4.3 | 80 | 80 | $0.296574 | panel_price_metadata |
| Xiaomi MiMo-V2-Flash | openrouter/xiaomi/mimo-v2-flash | 80 | 80 | $0.000214 | runcost |
| NVIDIA Nemotron 3 Nano 30B A3B | openrouter/nvidia/nemotron-3-nano-30b-a3b | 80 | 80 | $0.000104 | runcost |
| OpenAI GPT-OSS 20B | openrouter/openai/gpt-oss-20b | 80 | 80 | $0.000062 | runcost |
| Qwen3 Next 80B A3B Instruct | openrouter/qwen/qwen3-next-80b-a3b-instruct | 80 | 80 | $0.000187 | runcost |

## Warnings

- `paper-gemini-3-5-flash`: No price found for output_reasoning_tokens (token).
- `paper-gemini-2-5-flash-lite`: No price found for output_reasoning_tokens (token).
- `paper-grok-4-3`: runcost price card missing; used panel price metadata
- `paper-openrouter-xiaomi-mimo-v2-flash`: No price found for output_reasoning_tokens (token).
- `paper-openrouter-nemotron-3-nano`: No price found for input_cache_read_tokens (token).; No price found for output_reasoning_tokens (token).
- `paper-openrouter-gpt-oss-20b`: No price found for input_cache_read_tokens (token).; No price found for output_reasoning_tokens (token).
- `paper-openrouter-qwen3-next`: No price found for input_cache_read_tokens (token).; No price found for output_reasoning_tokens (token).
