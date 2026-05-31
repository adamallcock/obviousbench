---
title: Mega Model Sweep
date: 2026-05-31
type: status
status: complete
---

# Mega Model Sweep

## Scope

Ran the `balanced_8x10` barrage across 29 clean 80-sample model rows, with no
max-token cap on the new runs.

Primary artifacts:

- `results/summaries/mega-model-sweep-20260531-0820/comparison.csv`
- `results/summaries/mega-model-sweep-20260531-0820/family_comparison.csv`
- `results/summaries/mega-model-sweep-20260531-0820/section_comparison.csv`
- `docs/reports/2026-05-31-mega-model-sweep/report.html`
- `docs/reports/2026-05-31-mega-model-sweep/leaderboard.md`

## Run Notes

- OpenAI runs used the OpenAI API key from Keychain.
- Anthropic Opus runs used the Anthropic API key from Keychain.
- Direct Grok runs used the xAI key found under Keychain service
  `codex-xai-api-key`.
- No Google AI Studio API key was found in Keychain, so Gemini 3.x coverage was
  run through OpenRouter after credits were added.
- The first OpenRouter Gemini/Grok attempt failed with account credit errors and
  is excluded from the primary comparison.
- The first OpenAI GPT-5.4 no-thinking run used a max-token cap and is excluded
  from the primary comparison.
- Anthropic Opus was not stable as a nine-way parallel sweep because of rate
  limits, so Opus 4.6/4.7/4.8 low/medium/high were rerun sequentially with
  `max_connections=1`.

## Cost Notes

- Costing is enabled by default through the local `runcost` bridge where a price
  card exists.
- Direct xAI `grok/*` models are not priced by the local `runcost` card set, so
  their aggregate comparison rows use manual prices from the official xAI
  pricing page as of 2026-05-31:
  <https://docs.x.ai/developers/pricing>
- xAI direct-run cost assumptions:
  - input tokens: `$1.25 / 1M`
  - cached input tokens: `$0.20 / 1M`
  - output tokens: `$2.50 / 1M`
  - reasoning tokens: priced as output tokens, based on xAI's docs saying
    reasoning tokens are billed token usage for the model.

## Headline Leaderboard

| Rank | Model | Accuracy | Estimated cost |
| --- | --- | ---: | ---: |
| 1 | GPT-5.5 medium | 100.00% | $0.110635 |
| 2 | GPT-5.5 high | 100.00% | $0.139195 |
| 3 | Gemini 3.5 Flash OR | 100.00% | $0.149019 |
| 4 | Gemini 3.1 Pro Preview OR | 100.00% | $0.182912 |
| 5 | GPT-5 low | 98.75% | $0.067441 |
| 6 | GPT-5.4 high | 98.75% | $0.071712 |
| 7 | GPT-5.4 low | 97.50% | $0.040587 |
| 8 | GPT-5.4 medium | 97.50% | $0.059353 |
| 9 | Claude Opus 4.6 medium | 96.25% | $0.033880 |
| 10 | Claude Opus 4.6 high | 95.00% | $0.044155 |

## Excluded Or Superseded Runs

- `gemini-3-*-uncapped-balanced_8x10-20260531-075524`: OpenRouter credit errors.
- `grok-4-*-openrouter-balanced_8x10-20260531-075524`: OpenRouter credit errors.
- `gpt-5-4-none-balanced_8x10-20260531-075226`: superseded capped run.
- parallel Anthropic Opus attempt: superseded by sequential Opus runs.

## Current Read

The 100% cohort on this barrage is GPT-5.5 medium/high, Gemini 3.5 Flash through
OpenRouter, and Gemini 3.1 Pro Preview through OpenRouter. GPT-5 low and GPT-5.4
high both landed at 98.75%, one miss each.

The strongest cost/accuracy frontier in this exact run is mixed:

- very low cost, lower accuracy: Gemini 3.1 Flash Lite OR and GPT-5 Nano
- low cost, strong accuracy: Gemini 3 Flash Preview OR
- high accuracy with moderate cost: GPT-5 low, GPT-5.4 high, Claude Opus 4.6
  medium
- perfect score at higher cost: GPT-5.5 medium/high and Gemini 3.5/3.1 Pro via
  OpenRouter
