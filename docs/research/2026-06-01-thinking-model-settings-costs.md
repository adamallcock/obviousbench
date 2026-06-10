---
title: Thinking Model Settings And Cost Estimates
date: 2026-06-01
type: research
status: draft
---

# Thinking Model Settings And Cost Estimates

Dry-run cost estimates using measured token-usage calibration. The calibration run made a small number of provider calls; the full panel was not run.

This panel keeps expensive frontier thinking settings separate from the broad small/free failure registry.

## Sources

- OpenAI model, reasoning, and pricing docs: https://developers.openai.com/api/docs/models and https://developers.openai.com/api/docs/pricing
- Anthropic extended thinking and effort docs: https://platform.claude.com/docs/en/build-with-claude/extended-thinking and https://platform.claude.com/docs/en/build-with-claude/effort
- Gemini thinking and pricing docs: https://ai.google.dev/gemini-api/docs/thinking and https://ai.google.dev/gemini-api/docs/pricing
- xAI Grok reasoning docs: https://docs.x.ai/developers/model-capabilities/text/reasoning
- OpenRouter live model API and reasoning-token docs: https://openrouter.ai/api/v1/models and https://openrouter.ai/docs/guides/best-practices/reasoning-tokens
- Local npm `runcost` default price cards for normalized provider price lookup.
- Historical usage summaries: `results/summaries/*/usage_by_sample.csv`.
- Live calibration probe: `results/summaries/thinking-usage-calibration-20260601-live/results.jsonl`.
- Calibration note: `docs/research/2026-06-01-thinking-usage-calibration.md`.

## Estimate Method

- Profile: `hard_obvious_8x10`, seed `20260531`, 80 samples.
- Estimated input tokens: 3309 total, 41.36 per sample.
- Visible output assumption: 8 tokens per sample, calibrated from prior final-answer runs.
- Thinking token estimates use measured historical runs plus the live calibration probe, with a buffer by provider family and depth.
- The configured provider thinking budget is still preserved as a run cap; it is not treated as expected usage.
- Thinking and reasoning tokens are costed as output tokens unless a live source exposes a separate reasoning-token price.

## Calibration Notes

- Historical hard-obvious and balanced runs show GPT-5.4/5.5 medium/high using tens of reasoning tokens per sample, with high p95 values around 95-116.
- The 2026-06-01 live probe measured gpt-5 high at 128 reasoning tokens, Grok 4.3 high at 228, OpenRouter Gemini 3.5 Flash high at 190, and DeepSeek R1 high at the 512-token probe cap.
- Configured thinking budgets remain in provider_request_settings as run caps; estimated_usage uses calibrated expected usage for this short-answer benchmark.

## Totals

- Entries: 227
- Priced entries: 227
- Estimated full-panel cost: $30.395715
- Most expensive single planned setting: $0.865635

## Settings

| ID | Model | Route | Depth | Configured cap/sample | Est. reasoning/sample | Estimated cost | Pricing source |
| --- | --- | --- | --- | ---: | ---: | ---: | --- |
| openai-gpt-5-5-none | OpenAI GPT-5.5 none | openai | none | 0 | 0 | $0.035745 | runcost_default_price_cards |
| openai-gpt-5-5-low | OpenAI GPT-5.5 low | openai | low | 256 | 64 | $0.189345 | runcost_default_price_cards |
| openai-gpt-5-5-medium | OpenAI GPT-5.5 medium | openai | medium | 1024 | 96 | $0.266145 | runcost_default_price_cards |
| openai-gpt-5-5-high | OpenAI GPT-5.5 high | openai | high | 4096 | 160 | $0.419745 | runcost_default_price_cards |
| openai-gpt-5-5-xhigh | OpenAI GPT-5.5 xhigh | openai | xhigh | 8192 | 320 | $0.803745 | runcost_default_price_cards |
| openai-gpt-5-4-none | OpenAI GPT-5.4 none | openai | none | 0 | 0 | $0.017872 | runcost_default_price_cards |
| openai-gpt-5-4-low | OpenAI GPT-5.4 low | openai | low | 256 | 64 | $0.094673 | runcost_default_price_cards |
| openai-gpt-5-4-medium | OpenAI GPT-5.4 medium | openai | medium | 1024 | 96 | $0.133073 | runcost_default_price_cards |
| openai-gpt-5-4-high | OpenAI GPT-5.4 high | openai | high | 4096 | 160 | $0.209872 | runcost_default_price_cards |
| openai-gpt-5-4-xhigh | OpenAI GPT-5.4 xhigh | openai | xhigh | 8192 | 320 | $0.401873 | runcost_default_price_cards |
| openai-gpt-5-4-mini-none | OpenAI GPT-5.4 mini none | openai | none | 0 | 0 | $0.005362 | runcost_default_price_cards |
| openai-gpt-5-4-mini-low | OpenAI GPT-5.4 mini low | openai | low | 256 | 64 | $0.028402 | runcost_default_price_cards |
| openai-gpt-5-4-mini-medium | OpenAI GPT-5.4 mini medium | openai | medium | 1024 | 96 | $0.039922 | runcost_default_price_cards |
| openai-gpt-5-4-mini-high | OpenAI GPT-5.4 mini high | openai | high | 4096 | 160 | $0.062962 | runcost_default_price_cards |
| openai-gpt-5-4-mini-xhigh | OpenAI GPT-5.4 mini xhigh | openai | xhigh | 8192 | 320 | $0.120562 | runcost_default_price_cards |
| openai-gpt-5-4-nano-none | OpenAI GPT-5.4 nano none | openai | none | 0 | 0 | $0.001462 | runcost_default_price_cards |
| openai-gpt-5-4-nano-low | OpenAI GPT-5.4 nano low | openai | low | 256 | 64 | $0.007862 | runcost_default_price_cards |
| openai-gpt-5-4-nano-medium | OpenAI GPT-5.4 nano medium | openai | medium | 1024 | 96 | $0.011062 | runcost_default_price_cards |
| openai-gpt-5-4-nano-high | OpenAI GPT-5.4 nano high | openai | high | 4096 | 160 | $0.017462 | runcost_default_price_cards |
| openai-gpt-5-4-nano-xhigh | OpenAI GPT-5.4 nano xhigh | openai | xhigh | 8192 | 320 | $0.033462 | runcost_default_price_cards |
| openai-gpt-5-2-none | OpenAI GPT-5.2 none | openai | none | 0 | 0 | $0.014751 | runcost_default_price_cards |
| openai-gpt-5-2-low | OpenAI GPT-5.2 low | openai | low | 256 | 64 | $0.086431 | runcost_default_price_cards |
| openai-gpt-5-2-medium | OpenAI GPT-5.2 medium | openai | medium | 1024 | 96 | $0.122271 | runcost_default_price_cards |
| openai-gpt-5-2-high | OpenAI GPT-5.2 high | openai | high | 4096 | 160 | $0.193951 | runcost_default_price_cards |
| openai-gpt-5-2-xhigh | OpenAI GPT-5.2 xhigh | openai | xhigh | 8192 | 320 | $0.373151 | runcost_default_price_cards |
| openai-gpt-5-minimal | OpenAI GPT-5 minimal | openai | minimal | 64 | 16 | $0.023336 | runcost_default_price_cards |
| openai-gpt-5-low | OpenAI GPT-5 low | openai | low | 256 | 64 | $0.061736 | runcost_default_price_cards |
| openai-gpt-5-medium | OpenAI GPT-5 medium | openai | medium | 1024 | 96 | $0.087336 | runcost_default_price_cards |
| openai-gpt-5-high | OpenAI GPT-5 high | openai | high | 4096 | 160 | $0.138536 | runcost_default_price_cards |
| openai-gpt-5-mini-minimal | OpenAI GPT-5 mini minimal | openai | minimal | 64 | 16 | $0.004667 | runcost_default_price_cards |
| openai-gpt-5-mini-low | OpenAI GPT-5 mini low | openai | low | 256 | 64 | $0.012347 | runcost_default_price_cards |
| openai-gpt-5-mini-medium | OpenAI GPT-5 mini medium | openai | medium | 1024 | 96 | $0.017467 | runcost_default_price_cards |
| openai-gpt-5-mini-high | OpenAI GPT-5 mini high | openai | high | 4096 | 160 | $0.027707 | runcost_default_price_cards |
| openai-gpt-5-nano-minimal | OpenAI GPT-5 nano minimal | openai | minimal | 64 | 16 | $0.000933 | runcost_default_price_cards |
| openai-gpt-5-nano-low | OpenAI GPT-5 nano low | openai | low | 256 | 64 | $0.002469 | runcost_default_price_cards |
| openai-gpt-5-nano-medium | OpenAI GPT-5 nano medium | openai | medium | 1024 | 96 | $0.003493 | runcost_default_price_cards |
| openai-gpt-5-nano-high | OpenAI GPT-5 nano high | openai | high | 4096 | 160 | $0.005541 | runcost_default_price_cards |
| anthropic-claude-opus-4-8-low | Claude Opus 4.8 low | anthropic | low | 512 | 16 | $0.064545 | runcost_default_price_cards |
| anthropic-claude-opus-4-8-medium | Claude Opus 4.8 medium | anthropic | medium | 2048 | 48 | $0.128545 | runcost_default_price_cards |
| anthropic-claude-opus-4-8-high | Claude Opus 4.8 high | anthropic | high | 8192 | 128 | $0.288545 | runcost_default_price_cards |
| anthropic-claude-opus-4-8-xhigh | Claude Opus 4.8 xhigh | anthropic | xhigh | 16384 | 256 | $0.544545 | runcost_default_price_cards |
| anthropic-claude-opus-4-8-max | Claude Opus 4.8 max | anthropic | max | 32768 | 384 | $0.800545 | runcost_default_price_cards |
| anthropic-claude-opus-4-7-low | Claude Opus 4.7 low | anthropic | low | 512 | 16 | $0.064545 | runcost_default_price_cards |
| anthropic-claude-opus-4-7-medium | Claude Opus 4.7 medium | anthropic | medium | 2048 | 48 | $0.128545 | runcost_default_price_cards |
| anthropic-claude-opus-4-7-high | Claude Opus 4.7 high | anthropic | high | 8192 | 128 | $0.288545 | runcost_default_price_cards |
| anthropic-claude-opus-4-7-xhigh | Claude Opus 4.7 xhigh | anthropic | xhigh | 16384 | 256 | $0.544545 | runcost_default_price_cards |
| anthropic-claude-opus-4-7-max | Claude Opus 4.7 max | anthropic | max | 32768 | 384 | $0.800545 | runcost_default_price_cards |
| anthropic-claude-opus-4-6-low | Claude Opus 4.6 low | anthropic | low | 512 | 16 | $0.064545 | runcost_default_price_cards |
| anthropic-claude-opus-4-6-medium | Claude Opus 4.6 medium | anthropic | medium | 2048 | 48 | $0.128545 | runcost_default_price_cards |
| anthropic-claude-opus-4-6-high | Claude Opus 4.6 high | anthropic | high | 8192 | 128 | $0.288545 | runcost_default_price_cards |
| anthropic-claude-opus-4-6-max | Claude Opus 4.6 max | anthropic | max | 32768 | 384 | $0.800545 | runcost_default_price_cards |
| anthropic-claude-opus-4-5-low | Claude Opus 4.5 low_budget_512 | anthropic | low | 512 | 16 | $0.064545 | runcost_default_price_cards |
| anthropic-claude-opus-4-5-medium | Claude Opus 4.5 medium_budget_2048 | anthropic | medium | 2048 | 48 | $0.128545 | runcost_default_price_cards |
| anthropic-claude-opus-4-5-high | Claude Opus 4.5 high_budget_8192 | anthropic | high | 8192 | 128 | $0.288545 | runcost_default_price_cards |
| anthropic-claude-opus-4-5-max | Claude Opus 4.5 max_budget_32768 | anthropic | max | 32768 | 384 | $0.800545 | runcost_default_price_cards |
| anthropic-claude-sonnet-4-6-low | Claude Sonnet 4.6 low | anthropic | low | 512 | 16 | $0.038727 | runcost_default_price_cards |
| anthropic-claude-sonnet-4-6-medium | Claude Sonnet 4.6 medium | anthropic | medium | 2048 | 48 | $0.077127 | runcost_default_price_cards |
| anthropic-claude-sonnet-4-6-high | Claude Sonnet 4.6 high | anthropic | high | 8192 | 128 | $0.173127 | runcost_default_price_cards |
| anthropic-claude-sonnet-4-6-max | Claude Sonnet 4.6 max | anthropic | max | 32768 | 384 | $0.480327 | runcost_default_price_cards |
| anthropic-claude-sonnet-4-5-low | Claude Sonnet 4.5 low_budget_512 | anthropic | low | 512 | 16 | $0.038727 | runcost_default_price_cards |
| anthropic-claude-sonnet-4-5-medium | Claude Sonnet 4.5 medium_budget_2048 | anthropic | medium | 2048 | 48 | $0.077127 | runcost_default_price_cards |
| anthropic-claude-sonnet-4-5-high | Claude Sonnet 4.5 high_budget_8192 | anthropic | high | 8192 | 128 | $0.173127 | runcost_default_price_cards |
| anthropic-claude-sonnet-4-5-max | Claude Sonnet 4.5 max_budget_32768 | anthropic | max | 32768 | 384 | $0.480327 | runcost_default_price_cards |
| gemini-gemini-2-5-pro-low | Gemini 2.5 Pro low_budget_1024 | gemini | low | 1024 | 64 | $0.061736 | runcost_default_price_cards |
| gemini-gemini-2-5-pro-medium | Gemini 2.5 Pro medium_budget_8192 | gemini | medium | 8192 | 192 | $0.164136 | runcost_default_price_cards |
| gemini-gemini-2-5-pro-high | Gemini 2.5 Pro high_budget_24576 | gemini | high | 24576 | 384 | $0.317736 | runcost_default_price_cards |
| gemini-gemini-2-5-pro-max | Gemini 2.5 Pro max_budget_32768 | gemini | max | 32768 | 512 | $0.420136 | runcost_default_price_cards |
| gemini-gemini-2-5-flash-none | Gemini 2.5 Flash thinking_budget_0 | gemini | none | 0 | 0 | $0.002593 | runcost_default_price_cards |
| gemini-gemini-2-5-flash-low | Gemini 2.5 Flash low_budget_1024 | gemini | low | 1024 | 64 | $0.015393 | runcost_default_price_cards |
| gemini-gemini-2-5-flash-medium | Gemini 2.5 Flash medium_budget_8192 | gemini | medium | 8192 | 192 | $0.040993 | runcost_default_price_cards |
| gemini-gemini-2-5-flash-high | Gemini 2.5 Flash high_budget_24576 | gemini | high | 24576 | 384 | $0.079393 | runcost_default_price_cards |
| gemini-gemini-2-5-flash-lite-none | Gemini 2.5 Flash-Lite thinking_budget_0 | gemini | none | 0 | 0 | $0.000587 | runcost_default_price_cards |
| gemini-gemini-2-5-flash-lite-low | Gemini 2.5 Flash-Lite low_budget_1024 | gemini | low | 1024 | 64 | $0.002635 | runcost_default_price_cards |
| gemini-gemini-2-5-flash-lite-medium | Gemini 2.5 Flash-Lite medium_budget_8192 | gemini | medium | 8192 | 192 | $0.006731 | runcost_default_price_cards |
| gemini-gemini-2-5-flash-lite-high | Gemini 2.5 Flash-Lite high_budget_24576 | gemini | high | 24576 | 384 | $0.012875 | runcost_default_price_cards |
| gemini-gemini-3-1-pro-preview-low | Gemini 3.1 Pro Preview low_budget_1024 | gemini | low | 1024 | 64 | $0.075738 | runcost_default_price_cards |
| gemini-gemini-3-1-pro-preview-high | Gemini 3.1 Pro Preview high_budget_24576 | gemini | high | 24576 | 384 | $0.382938 | runcost_default_price_cards |
| gemini-gemini-3-5-flash-minimal | Gemini 3.5 Flash minimal_budget_1024 | gemini | minimal | 1024 | 32 | $0.033764 | runcost_default_price_cards |
| gemini-gemini-3-5-flash-low | Gemini 3.5 Flash low_budget_1024 | gemini | low | 1024 | 64 | $0.056803 | runcost_default_price_cards |
| gemini-gemini-3-5-flash-medium | Gemini 3.5 Flash medium_budget_8192 | gemini | medium | 8192 | 192 | $0.148963 | runcost_default_price_cards |
| gemini-gemini-3-5-flash-high | Gemini 3.5 Flash high_budget_24576 | gemini | high | 24576 | 384 | $0.287204 | runcost_default_price_cards |
| gemini-gemini-3-flash-preview-minimal | Gemini 3 Flash Preview minimal_budget_1024 | gemini | minimal | 1024 | 32 | $0.011255 | runcost_default_price_cards |
| gemini-gemini-3-flash-preview-low | Gemini 3 Flash Preview low_budget_1024 | gemini | low | 1024 | 64 | $0.018934 | runcost_default_price_cards |
| gemini-gemini-3-flash-preview-medium | Gemini 3 Flash Preview medium_budget_8192 | gemini | medium | 8192 | 192 | $0.049654 | runcost_default_price_cards |
| gemini-gemini-3-flash-preview-high | Gemini 3 Flash Preview high_budget_24576 | gemini | high | 24576 | 384 | $0.095735 | runcost_default_price_cards |
| gemini-gemini-3-1-flash-lite-minimal | Gemini 3.1 Flash-Lite minimal_budget_1024 | gemini | minimal | 1024 | 32 | $0.005627 | runcost_default_price_cards |
| gemini-gemini-3-1-flash-lite-low | Gemini 3.1 Flash-Lite low_budget_1024 | gemini | low | 1024 | 64 | $0.009467 | runcost_default_price_cards |
| gemini-gemini-3-1-flash-lite-medium | Gemini 3.1 Flash-Lite medium_budget_8192 | gemini | medium | 8192 | 192 | $0.024827 | runcost_default_price_cards |
| gemini-gemini-3-1-flash-lite-high | Gemini 3.1 Flash-Lite high_budget_24576 | gemini | high | 24576 | 384 | $0.047867 | runcost_default_price_cards |
| grok-grok-4-3-none | Grok 4.3 none | grok | none | 0 | 0 | $0.005736 | runcost_default_price_cards |
| grok-grok-4-3-low | Grok 4.3 low | grok | low | 256 | 128 | $0.031336 | runcost_default_price_cards |
| grok-grok-4-3-medium | Grok 4.3 medium | grok | medium | 1024 | 256 | $0.056936 | runcost_default_price_cards |
| grok-grok-4-3-high | Grok 4.3 high | grok | high | 4096 | 512 | $0.108136 | runcost_default_price_cards |
| grok-grok-4-20-multi-agent-low | Grok 4.20 Multi-Agent low | grok | low | 256 | 128 | $0.071898 | openrouter_models_api_proxy_price |
| grok-grok-4-20-multi-agent-medium | Grok 4.20 Multi-Agent medium | grok | medium | 1024 | 256 | $0.133338 | openrouter_models_api_proxy_price |
| grok-grok-4-20-multi-agent-high | Grok 4.20 Multi-Agent high | grok | high | 4096 | 512 | $0.256218 | openrouter_models_api_proxy_price |
| grok-grok-4-20-multi-agent-xhigh | Grok 4.20 Multi-Agent xhigh | grok | xhigh | 8192 | 1024 | $0.501978 | openrouter_models_api_proxy_price |
| openrouter-openai-gpt-5-5-none | OpenAI: GPT-5.5 none | openrouter | none | 0 | 0 | $0.035745 | openrouter_models_api |
| openrouter-openai-gpt-5-5-low | OpenAI: GPT-5.5 low | openrouter | low | 512 | 64 | $0.189345 | openrouter_models_api |
| openrouter-openai-gpt-5-5-medium | OpenAI: GPT-5.5 medium | openrouter | medium | 2048 | 96 | $0.266145 | openrouter_models_api |
| openrouter-openai-gpt-5-5-high | OpenAI: GPT-5.5 high | openrouter | high | 8192 | 160 | $0.419745 | openrouter_models_api |
| openrouter-openai-gpt-5-5-xhigh | OpenAI: GPT-5.5 xhigh | openrouter | xhigh | 16384 | 320 | $0.803745 | openrouter_models_api |
| openrouter-openai-gpt-5-4-image-2-none | OpenAI: GPT-5.4 Image 2 none | openrouter | none | 0 | 0 | $0.036072 | openrouter_models_api |
| openrouter-openai-gpt-5-4-image-2-low | OpenAI: GPT-5.4 Image 2 low | openrouter | low | 512 | 64 | $0.112872 | openrouter_models_api |
| openrouter-openai-gpt-5-4-image-2-medium | OpenAI: GPT-5.4 Image 2 medium | openrouter | medium | 2048 | 96 | $0.151272 | openrouter_models_api |
| openrouter-openai-gpt-5-4-image-2-high | OpenAI: GPT-5.4 Image 2 high | openrouter | high | 8192 | 160 | $0.228072 | openrouter_models_api |
| openrouter-openai-gpt-5-4-image-2-xhigh | OpenAI: GPT-5.4 Image 2 xhigh | openrouter | xhigh | 16384 | 320 | $0.420072 | openrouter_models_api |
| openrouter-openai-gpt-5-4-nano-none | OpenAI: GPT-5.4 Nano none | openrouter | none | 0 | 0 | $0.001462 | openrouter_models_api |
| openrouter-openai-gpt-5-4-nano-low | OpenAI: GPT-5.4 Nano low | openrouter | low | 512 | 64 | $0.007862 | openrouter_models_api |
| openrouter-openai-gpt-5-4-nano-medium | OpenAI: GPT-5.4 Nano medium | openrouter | medium | 2048 | 96 | $0.011062 | openrouter_models_api |
| openrouter-openai-gpt-5-4-nano-high | OpenAI: GPT-5.4 Nano high | openrouter | high | 8192 | 160 | $0.017462 | openrouter_models_api |
| openrouter-openai-gpt-5-4-nano-xhigh | OpenAI: GPT-5.4 Nano xhigh | openrouter | xhigh | 16384 | 320 | $0.033462 | openrouter_models_api |
| openrouter-openai-gpt-5-4-mini-none | OpenAI: GPT-5.4 Mini none | openrouter | none | 0 | 0 | $0.005362 | openrouter_models_api |
| openrouter-openai-gpt-5-4-mini-low | OpenAI: GPT-5.4 Mini low | openrouter | low | 512 | 64 | $0.028402 | openrouter_models_api |
| openrouter-openai-gpt-5-4-mini-medium | OpenAI: GPT-5.4 Mini medium | openrouter | medium | 2048 | 96 | $0.039922 | openrouter_models_api |
| openrouter-openai-gpt-5-4-mini-high | OpenAI: GPT-5.4 Mini high | openrouter | high | 8192 | 160 | $0.062962 | openrouter_models_api |
| openrouter-openai-gpt-5-4-mini-xhigh | OpenAI: GPT-5.4 Mini xhigh | openrouter | xhigh | 16384 | 320 | $0.120562 | openrouter_models_api |
| openrouter-openai-gpt-5-4-none | OpenAI: GPT-5.4 none | openrouter | none | 0 | 0 | $0.017872 | openrouter_models_api |
| openrouter-openai-gpt-5-4-low | OpenAI: GPT-5.4 low | openrouter | low | 512 | 64 | $0.094673 | openrouter_models_api |
| openrouter-openai-gpt-5-4-medium | OpenAI: GPT-5.4 medium | openrouter | medium | 2048 | 96 | $0.133073 | openrouter_models_api |
| openrouter-openai-gpt-5-4-high | OpenAI: GPT-5.4 high | openrouter | high | 8192 | 160 | $0.209872 | openrouter_models_api |
| openrouter-openai-gpt-5-4-xhigh | OpenAI: GPT-5.4 xhigh | openrouter | xhigh | 16384 | 320 | $0.401873 | openrouter_models_api |
| openrouter-openai-gpt-5-2-codex-none | OpenAI: GPT-5.2-Codex none | openrouter | none | 0 | 0 | $0.014751 | openrouter_models_api |
| openrouter-openai-gpt-5-2-codex-low | OpenAI: GPT-5.2-Codex low | openrouter | low | 512 | 64 | $0.086431 | openrouter_models_api |
| openrouter-openai-gpt-5-2-codex-medium | OpenAI: GPT-5.2-Codex medium | openrouter | medium | 2048 | 96 | $0.122271 | openrouter_models_api |
| openrouter-openai-gpt-5-2-codex-high | OpenAI: GPT-5.2-Codex high | openrouter | high | 8192 | 160 | $0.193951 | openrouter_models_api |
| openrouter-openai-gpt-5-2-codex-xhigh | OpenAI: GPT-5.2-Codex xhigh | openrouter | xhigh | 16384 | 320 | $0.373151 | openrouter_models_api |
| openrouter-openai-gpt-5-2-none | OpenAI: GPT-5.2 none | openrouter | none | 0 | 0 | $0.014751 | openrouter_models_api |
| openrouter-openai-gpt-5-2-low | OpenAI: GPT-5.2 low | openrouter | low | 512 | 64 | $0.086431 | openrouter_models_api |
| openrouter-openai-gpt-5-2-medium | OpenAI: GPT-5.2 medium | openrouter | medium | 2048 | 96 | $0.122271 | openrouter_models_api |
| openrouter-openai-gpt-5-2-high | OpenAI: GPT-5.2 high | openrouter | high | 8192 | 160 | $0.193951 | openrouter_models_api |
| openrouter-openai-gpt-5-2-xhigh | OpenAI: GPT-5.2 xhigh | openrouter | xhigh | 16384 | 320 | $0.373151 | openrouter_models_api |
| openrouter-openai-gpt-5-image-mini-minimal | OpenAI: GPT-5 Image Mini minimal | openrouter | minimal | 64 | 16 | $0.012113 | openrouter_models_api |
| openrouter-openai-gpt-5-image-mini-low | OpenAI: GPT-5 Image Mini low | openrouter | low | 512 | 64 | $0.019793 | openrouter_models_api |
| openrouter-openai-gpt-5-image-mini-medium | OpenAI: GPT-5 Image Mini medium | openrouter | medium | 2048 | 96 | $0.024913 | openrouter_models_api |
| openrouter-openai-gpt-5-image-mini-high | OpenAI: GPT-5 Image Mini high | openrouter | high | 8192 | 160 | $0.035153 | openrouter_models_api |
| openrouter-openai-gpt-5-image-minimal | OpenAI: GPT-5 Image minimal | openrouter | minimal | 64 | 16 | $0.052290 | openrouter_models_api |
| openrouter-openai-gpt-5-image-low | OpenAI: GPT-5 Image low | openrouter | low | 512 | 64 | $0.090690 | openrouter_models_api |
| openrouter-openai-gpt-5-image-medium | OpenAI: GPT-5 Image medium | openrouter | medium | 2048 | 96 | $0.116290 | openrouter_models_api |
| openrouter-openai-gpt-5-image-high | OpenAI: GPT-5 Image high | openrouter | high | 8192 | 160 | $0.167490 | openrouter_models_api |
| openrouter-openai-o3-deep-research-low | OpenAI: o3 Deep Research low_budget_512 | openrouter | low | 512 | 64 | $0.263490 | openrouter_models_api |
| openrouter-openai-o3-deep-research-medium | OpenAI: o3 Deep Research medium_budget_2048 | openrouter | medium | 2048 | 96 | $0.365890 | openrouter_models_api |
| openrouter-openai-o3-deep-research-high | OpenAI: o3 Deep Research high_budget_8192 | openrouter | high | 8192 | 160 | $0.570690 | openrouter_models_api |
| openrouter-openai-o4-mini-deep-research-low | OpenAI: o4 Mini Deep Research low_budget_512 | openrouter | low | 512 | 64 | $0.052698 | openrouter_models_api |
| openrouter-openai-o4-mini-deep-research-medium | OpenAI: o4 Mini Deep Research medium_budget_2048 | openrouter | medium | 2048 | 96 | $0.073178 | openrouter_models_api |
| openrouter-openai-o4-mini-deep-research-high | OpenAI: o4 Mini Deep Research high_budget_8192 | openrouter | high | 8192 | 160 | $0.114138 | openrouter_models_api |
| openrouter-anthropic-claude-opus-4-8-low | Anthropic: Claude Opus 4.8 low_budget_512 | openrouter | low | 512 | 16 | $0.064545 | openrouter_models_api |
| openrouter-anthropic-claude-opus-4-8-medium | Anthropic: Claude Opus 4.8 medium_budget_2048 | openrouter | medium | 2048 | 48 | $0.128545 | openrouter_models_api |
| openrouter-anthropic-claude-opus-4-8-high | Anthropic: Claude Opus 4.8 high_budget_8192 | openrouter | high | 8192 | 128 | $0.288545 | openrouter_models_api |
| openrouter-anthropic-claude-opus-4-7-low | Anthropic: Claude Opus 4.7 low_budget_512 | openrouter | low | 512 | 16 | $0.064545 | openrouter_models_api |
| openrouter-anthropic-claude-opus-4-7-medium | Anthropic: Claude Opus 4.7 medium_budget_2048 | openrouter | medium | 2048 | 48 | $0.128545 | openrouter_models_api |
| openrouter-anthropic-claude-opus-4-7-high | Anthropic: Claude Opus 4.7 high_budget_8192 | openrouter | high | 8192 | 128 | $0.288545 | openrouter_models_api |
| openrouter-anthropic-claude-sonnet-4-6-low | Anthropic: Claude Sonnet 4.6 low_budget_512 | openrouter | low | 512 | 16 | $0.038727 | openrouter_models_api |
| openrouter-anthropic-claude-sonnet-4-6-medium | Anthropic: Claude Sonnet 4.6 medium_budget_2048 | openrouter | medium | 2048 | 48 | $0.077127 | openrouter_models_api |
| openrouter-anthropic-claude-sonnet-4-6-high | Anthropic: Claude Sonnet 4.6 high_budget_8192 | openrouter | high | 8192 | 128 | $0.173127 | openrouter_models_api |
| openrouter-anthropic-claude-opus-4-6-low | Anthropic: Claude Opus 4.6 low_budget_512 | openrouter | low | 512 | 16 | $0.064545 | openrouter_models_api |
| openrouter-anthropic-claude-opus-4-6-medium | Anthropic: Claude Opus 4.6 medium_budget_2048 | openrouter | medium | 2048 | 48 | $0.128545 | openrouter_models_api |
| openrouter-anthropic-claude-opus-4-6-high | Anthropic: Claude Opus 4.6 high_budget_8192 | openrouter | high | 8192 | 128 | $0.288545 | openrouter_models_api |
| openrouter-anthropic-claude-opus-4-5-low | Anthropic: Claude Opus 4.5 low_budget_512 | openrouter | low | 512 | 16 | $0.064545 | openrouter_models_api |
| openrouter-anthropic-claude-opus-4-5-medium | Anthropic: Claude Opus 4.5 medium_budget_2048 | openrouter | medium | 2048 | 48 | $0.128545 | openrouter_models_api |
| openrouter-anthropic-claude-opus-4-5-high | Anthropic: Claude Opus 4.5 high_budget_8192 | openrouter | high | 8192 | 128 | $0.288545 | openrouter_models_api |
| openrouter-anthropic-claude-sonnet-4-5-low | Anthropic: Claude Sonnet 4.5 low_budget_512 | openrouter | low | 512 | 16 | $0.038727 | openrouter_models_api |
| openrouter-anthropic-claude-sonnet-4-5-medium | Anthropic: Claude Sonnet 4.5 medium_budget_2048 | openrouter | medium | 2048 | 48 | $0.077127 | openrouter_models_api |
| openrouter-anthropic-claude-sonnet-4-5-high | Anthropic: Claude Sonnet 4.5 high_budget_8192 | openrouter | high | 8192 | 128 | $0.173127 | openrouter_models_api |
| openrouter-anthropic-claude-opus-4-1-low | Anthropic: Claude Opus 4.1 low_budget_512 | openrouter | low | 512 | 16 | $0.193635 | openrouter_models_api |
| openrouter-anthropic-claude-opus-4-1-medium | Anthropic: Claude Opus 4.1 medium_budget_2048 | openrouter | medium | 2048 | 48 | $0.385635 | openrouter_models_api |
| openrouter-anthropic-claude-opus-4-1-high | Anthropic: Claude Opus 4.1 high_budget_8192 | openrouter | high | 8192 | 128 | $0.865635 | openrouter_models_api |
| openrouter-x-ai-grok-4-3-none | xAI: Grok 4.3 none | openrouter | none | 0 | 0 | $0.005736 | openrouter_models_api |
| openrouter-x-ai-grok-4-3-low | xAI: Grok 4.3 low | openrouter | low | 512 | 128 | $0.031336 | openrouter_models_api |
| openrouter-x-ai-grok-4-3-medium | xAI: Grok 4.3 medium | openrouter | medium | 2048 | 256 | $0.056936 | openrouter_models_api |
| openrouter-x-ai-grok-4-3-high | xAI: Grok 4.3 high | openrouter | high | 8192 | 512 | $0.108136 | openrouter_models_api |
| openrouter-x-ai-grok-4-3-xhigh | xAI: Grok 4.3 xhigh | openrouter | xhigh | 16384 | 1024 | $0.210536 | openrouter_models_api |
| openrouter-x-ai-grok-4-20-multi-agent-low | xAI: Grok 4.20 Multi-Agent low | openrouter | low | 512 | 128 | $0.071898 | openrouter_models_api |
| openrouter-x-ai-grok-4-20-multi-agent-medium | xAI: Grok 4.20 Multi-Agent medium | openrouter | medium | 2048 | 256 | $0.133338 | openrouter_models_api |
| openrouter-x-ai-grok-4-20-multi-agent-high | xAI: Grok 4.20 Multi-Agent high | openrouter | high | 8192 | 512 | $0.256218 | openrouter_models_api |
| openrouter-x-ai-grok-4-20-multi-agent-xhigh | xAI: Grok 4.20 Multi-Agent xhigh | openrouter | xhigh | 16384 | 1024 | $0.501978 | openrouter_models_api |
| openrouter-x-ai-grok-4-20-low | xAI: Grok 4.20 low_budget_512 | openrouter | low | 512 | 128 | $0.031336 | openrouter_models_api |
| openrouter-x-ai-grok-4-20-medium | xAI: Grok 4.20 medium_budget_2048 | openrouter | medium | 2048 | 256 | $0.056936 | openrouter_models_api |
| openrouter-x-ai-grok-4-20-high | xAI: Grok 4.20 high_budget_8192 | openrouter | high | 8192 | 512 | $0.108136 | openrouter_models_api |
| openrouter-google-gemini-3-5-flash-minimal | Google: Gemini 3.5 Flash minimal | openrouter | minimal | 64 | 32 | $0.033764 | openrouter_models_api |
| openrouter-google-gemini-3-5-flash-low | Google: Gemini 3.5 Flash low | openrouter | low | 512 | 64 | $0.056803 | openrouter_models_api |
| openrouter-google-gemini-3-5-flash-medium | Google: Gemini 3.5 Flash medium | openrouter | medium | 2048 | 192 | $0.148963 | openrouter_models_api |
| openrouter-google-gemini-3-5-flash-high | Google: Gemini 3.5 Flash high | openrouter | high | 8192 | 384 | $0.287204 | openrouter_models_api |
| openrouter-google-gemini-3-1-flash-lite-minimal | Google: Gemini 3.1 Flash Lite minimal | openrouter | minimal | 64 | 32 | $0.005627 | openrouter_models_api |
| openrouter-google-gemini-3-1-flash-lite-low | Google: Gemini 3.1 Flash Lite low | openrouter | low | 512 | 64 | $0.009467 | openrouter_models_api |
| openrouter-google-gemini-3-1-flash-lite-medium | Google: Gemini 3.1 Flash Lite medium | openrouter | medium | 2048 | 192 | $0.024827 | openrouter_models_api |
| openrouter-google-gemini-3-1-flash-lite-high | Google: Gemini 3.1 Flash Lite high | openrouter | high | 8192 | 384 | $0.047867 | openrouter_models_api |
| openrouter-google-gemini-3-1-flash-lite-preview-minimal | Google: Gemini 3.1 Flash Lite Preview minimal | openrouter | minimal | 64 | 32 | $0.005627 | openrouter_models_api |
| openrouter-google-gemini-3-1-flash-lite-preview-low | Google: Gemini 3.1 Flash Lite Preview low | openrouter | low | 512 | 64 | $0.009467 | openrouter_models_api |
| openrouter-google-gemini-3-1-flash-lite-preview-medium | Google: Gemini 3.1 Flash Lite Preview medium | openrouter | medium | 2048 | 192 | $0.024827 | openrouter_models_api |
| openrouter-google-gemini-3-1-flash-lite-preview-high | Google: Gemini 3.1 Flash Lite Preview high | openrouter | high | 8192 | 384 | $0.047867 | openrouter_models_api |
| openrouter-google-gemini-3-1-flash-image-preview-minimal | Google: Nano Banana 2 (Gemini 3.1 Flash Image Preview) minimal | openrouter | minimal | 64 | 32 | $0.011255 | openrouter_models_api |
| openrouter-google-gemini-3-1-flash-image-preview-low | Google: Nano Banana 2 (Gemini 3.1 Flash Image Preview) low | openrouter | low | 512 | 64 | $0.018934 | openrouter_models_api |
| openrouter-google-gemini-3-1-flash-image-preview-medium | Google: Nano Banana 2 (Gemini 3.1 Flash Image Preview) medium | openrouter | medium | 2048 | 192 | $0.049654 | openrouter_models_api |
| openrouter-google-gemini-3-1-flash-image-preview-high | Google: Nano Banana 2 (Gemini 3.1 Flash Image Preview) high | openrouter | high | 8192 | 384 | $0.095735 | openrouter_models_api |
| openrouter-google-gemini-3-1-pro-preview-customtools-low | Google: Gemini 3.1 Pro Preview Custom Tools low | openrouter | low | 512 | 64 | $0.075738 | openrouter_models_api |
| openrouter-google-gemini-3-1-pro-preview-customtools-high | Google: Gemini 3.1 Pro Preview Custom Tools high | openrouter | high | 8192 | 384 | $0.382938 | openrouter_models_api |
| openrouter-moonshotai-kimi-k2-6-free-low | MoonshotAI: Kimi K2.6 (free) low_budget_512 | openrouter | low | 512 | 64 | $0.000000 | openrouter_models_api |
| openrouter-moonshotai-kimi-k2-6-free-medium | MoonshotAI: Kimi K2.6 (free) medium_budget_2048 | openrouter | medium | 2048 | 128 | $0.000000 | openrouter_models_api |
| openrouter-moonshotai-kimi-k2-6-free-high | MoonshotAI: Kimi K2.6 (free) high_budget_8192 | openrouter | high | 8192 | 256 | $0.000000 | openrouter_models_api |
| openrouter-z-ai-glm-4-5-air-free-low | Z.ai: GLM 4.5 Air (free) low_budget_512 | openrouter | low | 512 | 64 | $0.000000 | openrouter_models_api |
| openrouter-z-ai-glm-4-5-air-free-medium | Z.ai: GLM 4.5 Air (free) medium_budget_2048 | openrouter | medium | 2048 | 128 | $0.000000 | openrouter_models_api |
| openrouter-z-ai-glm-4-5-air-free-high | Z.ai: GLM 4.5 Air (free) high_budget_8192 | openrouter | high | 8192 | 256 | $0.000000 | openrouter_models_api |
| openrouter-qwen-qwen3-7-max-low | Qwen: Qwen3.7 Max low_budget_512 | openrouter | low | 512 | 64 | $0.025736 | openrouter_models_api |
| openrouter-qwen-qwen3-7-max-medium | Qwen: Qwen3.7 Max medium_budget_2048 | openrouter | medium | 2048 | 128 | $0.044936 | openrouter_models_api |
| openrouter-qwen-qwen3-7-max-high | Qwen: Qwen3.7 Max high_budget_8192 | openrouter | high | 8192 | 256 | $0.083336 | openrouter_models_api |
| openrouter-qwen-qwen3-5-plus-20260420-low | Qwen: Qwen3.5 Plus 2026-04-20 low_budget_512 | openrouter | low | 512 | 64 | $0.011361 | openrouter_models_api |
| openrouter-qwen-qwen3-5-plus-20260420-medium | Qwen: Qwen3.5 Plus 2026-04-20 medium_budget_2048 | openrouter | medium | 2048 | 128 | $0.020577 | openrouter_models_api |
| openrouter-qwen-qwen3-5-plus-20260420-high | Qwen: Qwen3.5 Plus 2026-04-20 high_budget_8192 | openrouter | high | 8192 | 256 | $0.039009 | openrouter_models_api |
| openrouter-qwen-qwen3-6-flash-low | Qwen: Qwen3.6 Flash low_budget_512 | openrouter | low | 512 | 64 | $0.007100 | openrouter_models_api |
| openrouter-qwen-qwen3-6-flash-medium | Qwen: Qwen3.6 Flash medium_budget_2048 | openrouter | medium | 2048 | 128 | $0.012860 | openrouter_models_api |
| openrouter-qwen-qwen3-6-flash-high | Qwen: Qwen3.6 Flash high_budget_8192 | openrouter | high | 8192 | 256 | $0.024380 | openrouter_models_api |
| openrouter-qwen-qwen3-6-35b-a3b-low | Qwen: Qwen3.6 35B A3B low_budget_512 | openrouter | low | 512 | 64 | $0.006223 | openrouter_models_api |
| openrouter-qwen-qwen3-6-35b-a3b-medium | Qwen: Qwen3.6 35B A3B medium_budget_2048 | openrouter | medium | 2048 | 128 | $0.011343 | openrouter_models_api |
| openrouter-qwen-qwen3-6-35b-a3b-high | Qwen: Qwen3.6 35B A3B high_budget_8192 | openrouter | high | 8192 | 256 | $0.021583 | openrouter_models_api |
| openrouter-deepseek-deepseek-r1-0528-low | DeepSeek: R1 0528 low_budget_512 | openrouter | low | 512 | 128 | $0.025046 | openrouter_models_api |
| openrouter-deepseek-deepseek-r1-0528-medium | DeepSeek: R1 0528 medium_budget_2048 | openrouter | medium | 2048 | 384 | $0.069079 | openrouter_models_api |
| openrouter-deepseek-deepseek-r1-0528-high | DeepSeek: R1 0528 high_budget_8192 | openrouter | high | 8192 | 1024 | $0.179158 | openrouter_models_api |
| openrouter-deepseek-deepseek-r1-distill-qwen-32b-low | DeepSeek: R1 Distill Qwen 32B low_budget_512 | openrouter | low | 512 | 128 | $0.004115 | openrouter_models_api |
| openrouter-deepseek-deepseek-r1-distill-qwen-32b-medium | DeepSeek: R1 Distill Qwen 32B medium_budget_2048 | openrouter | medium | 2048 | 384 | $0.010054 | openrouter_models_api |
| openrouter-deepseek-deepseek-r1-distill-qwen-32b-high | DeepSeek: R1 Distill Qwen 32B high_budget_8192 | openrouter | high | 8192 | 1024 | $0.024902 | openrouter_models_api |
| openrouter-deepseek-deepseek-r1-distill-llama-70b-low | DeepSeek: R1 Distill Llama 70B low_budget_512 | openrouter | low | 512 | 128 | $0.011020 | openrouter_models_api |
| openrouter-deepseek-deepseek-r1-distill-llama-70b-medium | DeepSeek: R1 Distill Llama 70B medium_budget_2048 | openrouter | medium | 2048 | 384 | $0.027404 | openrouter_models_api |
| openrouter-deepseek-deepseek-r1-distill-llama-70b-high | DeepSeek: R1 Distill Llama 70B high_budget_8192 | openrouter | high | 8192 | 1024 | $0.068364 | openrouter_models_api |
| openrouter-minimax-minimax-m3-low | MiniMax: MiniMax M3 low_budget_512 | openrouter | low | 512 | 64 | $0.007905 | openrouter_models_api |
| openrouter-minimax-minimax-m3-medium | MiniMax: MiniMax M3 medium_budget_2048 | openrouter | medium | 2048 | 128 | $0.014049 | openrouter_models_api |
| openrouter-minimax-minimax-m3-high | MiniMax: MiniMax M3 high_budget_8192 | openrouter | high | 8192 | 256 | $0.026337 | openrouter_models_api |
