---
title: Model Coverage Refresh
date: 2026-06-01
type: research
status: draft
---

# Model Coverage Refresh

This refresh answers two separate questions:

1. whether the 12-entry paper panel is enough for a fast preprint, and
2. whether the repo is ready for the broader run the paper should eventually
   claim.

## Short Answer

The 12-entry `configs/paper_v1_model_panel.yaml` is too thin for the final
large benchmark story. It is acceptable as a draft/preprint smoke surface only
if the manuscript labels it as a small paper panel and does not imply broad
state-of-the-market coverage.

The 227-entry `configs/model_thinking_settings_v1.yaml` is much closer to the
run shape we want: hundreds of model/configuration rows. It is not hundreds of
unique models. It currently contains 227 settings over 59 unique model IDs.

## Current Local Coverage

| Config | Entries | Unique model IDs | Role |
| --- | ---: | ---: | --- |
| `configs/paper_v1_model_panel.yaml` | 12 | 12 | Small draft paper panel. |
| `configs/model_thinking_settings_v1.yaml` | 227 | 59 | Broad thinking/non-thinking configuration sweep. |

Broad config route counts:

| Provider route | Entries |
| --- | ---: |
| `openai` | 37 |
| `anthropic` | 26 |
| `gemini` | 26 |
| `grok` | 8 |
| `openrouter` | 130 |

Broad config thinking-depth counts:

| Thinking depth | Entries |
| --- | ---: |
| `none` | 16 |
| `minimal` | 12 |
| `low` | 59 |
| `medium` | 57 |
| `high` | 59 |
| `xhigh` | 17 |
| `max` | 7 |

Estimated full-panel cost from the local cost artifact is `$30.39571523`.

## Missing Or Stale Coverage

### Direct Providers

- OpenAI: add `gpt-5.5`, `gpt-5.4`, `gpt-5.4-mini`, and `gpt-5.4-nano` to the
  paper-facing panel if we want current OpenAI coverage. The OpenAI models docs
  currently recommend `gpt-5.5` as the flagship starting point and smaller
  `gpt-5.4-mini`/`gpt-5.4-nano` for lower latency and cost:
  https://developers.openai.com/api/docs/models
- Anthropic: add `claude-opus-4.8` if the paper wants an Anthropic flagship
  entry, not only Sonnet/Haiku. Anthropic pricing docs list Opus 4.8 alongside
  Opus 4.7/4.6:
  https://platform.claude.com/docs/en/about-claude/pricing
- Gemini: `gemini-3.5-flash` is already in the paper panel. Google's launch
  post says Gemini 3.5 Flash is generally available via the Gemini API, and that
  3.5 Pro was still expected later; do not add 3.5 Pro until it appears in the
  API model list:
  https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-5/
- xAI/Grok: `grok-4.3` is a good current direct-provider inclusion. xAI docs
  list it as the model name, with pricing at `$1.25` input and `$2.50` output
  per 1M tokens:
  https://docs.x.ai/developers/models/grok-4.3

### OpenRouter

Live OpenRouter catalog check returned 343 models from
`https://openrouter.ai/api/v1/models`.

Current newer/free candidates worth adding or reconciling before the large run:

| Candidate | Live OpenRouter API status | Local broad config status |
| --- | --- | --- |
| `openai/gpt-oss-120b:free` | present | missing |
| `moonshotai/kimi-k2.6:free` | present | present |
| `z-ai/glm-4.5-air:free` | present | present |
| `poolside/laguna-m.1:free` | present | missing |
| `nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free` | present | missing |
| `qwen/qwen3-next-80b-a3b-instruct:free` | present | missing from broad config; replaced in the paper panel by paid sibling after free-route smoke failure |
| `qwen/qwen3-next-80b-a3b-instruct` | present | present in paper panel; missing from broad config |

There is also a mismatch between the paper panel and the broad config: several
paper entries are not represented in `configs/model_thinking_settings_v1.yaml`.
Before running hundreds of configurations, either make the broad config a true
superset of the paper panel or explicitly treat them as separate experiments.

## Pricing Freshness

`runcost` itself is current in this repo:

| Source | Version |
| --- | --- |
| `package.json` | `^0.1.2` |
| `package-lock.json` | `0.1.2` |
| `npm view runcost version` | `0.1.2` |

The idempotent refresh command is:

```bash
npm install runcost@latest
```

That command was run on 2026-06-01 and reported `up to date`; it did not change
`package.json` or `package-lock.json`.

The Grok 4.3 panel price has been updated to xAI's current `$1.25/$2.50` per
1M input/output tokens. Re-check Gemini pricing immediately before the final
sweep, because local `runcost` and provider docs may differ for new Gemini
releases.

## Recommendation

Use the 12-entry paper panel only for draft mechanics, smoke testing, and
possibly a fast preprint if explicitly framed as small. For the benchmark claim
the user wants, promote the broad 227-entry config, then add the missing current
OpenAI/Anthropic/OpenRouter entries above and rerun cost estimation before any
provider calls.
