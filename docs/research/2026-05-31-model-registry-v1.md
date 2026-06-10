---
title: Model Registry V1
date: 2026-05-31
type: research
status: complete
---

# Model Registry V1

Generated registry: `configs/model_registry_v1.yaml`
Generator: `scripts/build_model_registry.mjs`
Generation timestamp: stored in `configs/model_registry_v1.yaml` as `generated_at`
Target run profile: `hard_obvious_8x10` with seed `20260531`

## Scope

This registry is a provider-call plan for a broad ObviousBench sweep. It favors
models that are likely to expose simple-task failures:

- free OpenRouter endpoints,
- open-weight or open-source model families,
- small, lite, mini, nano, flash, and cheap variants,
- non-thinking or reasoning-disabled settings,
- a small direct-provider baseline for existing OpenAI, Anthropic, Gemini, and
  Grok credentials.

The generated file currently contains 214 entries:

| Route | Entries |
| --- | ---: |
| OpenRouter | 185 |
| OpenAI direct | 16 |
| Anthropic direct | 5 |
| Gemini direct | 5 |
| Grok direct | 3 |

Coverage checks from the generated registry:

- 25 OpenRouter entries are tagged `free`.
- 195 entries are tagged `small`, `open-weight`, or both.
- 211 entries have price metadata from OpenRouter live metadata or `runcost`.
- 3 entries are marked `manual_lookup_required` for pricing: OpenAI direct
  `gpt-oss-120b`, OpenAI direct `gpt-oss-20b`, and direct `grok-4.20`.

## Sources

Primary source links:

- OpenRouter Models API documentation:
  <https://openrouter.ai/docs/api-reference/models/get-models>
- OpenRouter model metadata endpoint:
  <https://openrouter.ai/api/v1/models>
- OpenAI model docs:
  <https://platform.openai.com/docs/models>
- Anthropic Claude model overview:
  <https://docs.anthropic.com/en/docs/about-claude/models/overview>
- Google Gemini model docs:
  <https://ai.google.dev/gemini-api/docs/models>
- xAI model docs:
  <https://docs.x.ai/developers/models>
- npm `runcost` package used in this checkout:
  <https://www.npmjs.com/package/runcost>

Observed source counts when the generator ran:

| Source | Count |
| --- | ---: |
| OpenRouter live models fetched | 345 |
| OpenRouter eligible text models | 343 |
| OpenRouter selected entries | 185 |
| `runcost` default price cards | 7,480 |
| `runcost` `llm-prices` cards | 112 |
| `runcost` LiteLLM cards | 2,283 |
| `runcost` models.dev cards | 4,727 |
| `runcost` OpenRouter cards | 358 |

## Selection Rules

The generator scores OpenRouter entries with strong weight for:

- zero input and output token prices,
- recognizable open-weight families such as Qwen, DeepSeek, Mistral, Gemma,
  Llama, Nemotron, GLM, Kimi, Hermes, and GPT-OSS,
- model names suggesting smaller variants,
- low listed token prices,
- names that do not imply thinking or reasoning mode.

Direct-provider entries are curated baselines rather than generated from account
model-list calls. They reflect providers already used by this repo or explicitly
available for future runs:

- OpenAI direct entries include no-thinking variants for GPT-5-family models,
  GPT-4.1/4o non-thinking baselines, and GPT-OSS open-weight models.
- Anthropic direct entries include current Claude Opus, Sonnet, and Haiku
  baselines.
- Gemini direct entries use Inspect's `google/` provider route and require the
  Google optional dependency before live runs.
- Grok direct entries use Inspect's `grok/` provider route and use xAI pricing
  where `runcost` has a matching card.

Excluded from the registry:

- image-only, audio-only, and embedding-only models,
- expired endpoints,
- high-cost frontier duplicates that do not add likely failure coverage,
- provider routes that are not available through the repo's current Inspect
  workflow.

## Default Settings

Every registry entry targets the hard-obvious barrage:

```yaml
profile: hard_obvious_8x10
seed: 20260531
generation_settings:
  temperature: 0
  max_tokens: 64
```

OpenAI reasoning-model baselines additionally set `reasoning_effort` only to
values supported by the selected model. `gpt-5` and `gpt-5-mini` do not support
`none`, so the registry uses `minimal` for those two 5.0-era aliases. The main
comparison pass should start with the no-thinking and small-model entries before
spending budget on frontier reasoning variants.

## Usage

Regenerate the registry:

```bash
node scripts/build_model_registry.mjs
```

Validate the registry offline:

```bash
.venv/bin/python -m pytest tests/configs/test_model_registry_v1.py -q
```

Run compact provider smoke checks without creating one Inspect log directory per
model:

```bash
.venv/bin/python scripts/smoke_model_registry.py \
  --batch-size 8 \
  --max-workers 2 \
  --batch-sleep 0.5 \
  --timeout 20 \
  --out-dir results/summaries/model-registry-smoke-20260601-full
```

The smoke runner writes one compact output directory:

- `results.jsonl`: append-only attempt log, including retries.
- `latest_results.jsonl`: one current row per registry entry.
- `summary.csv`: status counts by provider and exact-answer result.
- `summary.md`: compact human-readable status table and non-OK entries.

Dry-run estimate one entry:

```bash
.venv/bin/obviousbench estimate-cost \
  --model openrouter/poolside/laguna-xs.2:free \
  --profile hard_obvious_8x10 \
  --seed 20260531 \
  --setting temperature=0 \
  --setting max_tokens=64
```

Run one entry through the generic Inspect runner:

```bash
.venv/bin/python scripts/run_inspect_eval.py \
  --task obviousbench/tasks/barrage.py \
  --model openrouter/poolside/laguna-xs.2:free \
  --log-dir results/raw/model-registry-v1/poolside-laguna-xs-2-free \
  -T profile=hard_obvious_8x10 \
  -T seed=20260531 \
  --generation-setting temperature=0 \
  --generation-setting max_tokens=64 \
  --inspect-arg=--no-log-model-api \
  --inspect-arg=--no-log-realtime
```

For OpenRouter free-tier runs, expect 429s and provider-specific rate limits.
Use small batches, resume support, and saved manifests rather than replacing a
blocked free run with an unverified snippet or marketing claim.

## Smoke Check Results

Latest run directory: `results/summaries/model-registry-smoke-20260601-full`
Run date: 2026-06-01
Unique registry entries checked: 214

Latest status counts after targeted retries and Gemini-through-OpenRouter
fallback:

| Status | Count |
| --- | ---: |
| OK | 179 |
| Empty visible response | 18 |
| Rate limited | 8 |
| HTTP error | 6 |
| Model not found | 2 |
| Request timeout | 1 |

Provider-level read:

- OpenRouter: 155 OK, 30 non-OK. Most remaining non-OKs are empty visible
  responses from reasoning/specialized models, provider 429s, or provider-side
  errors for specialized models such as Lyria and Llama Guard.
- OpenAI direct: 12 OK, 4 non-OK. `gpt-5` and `gpt-5-mini` rejected
  `reasoning_effort=none`; direct `gpt-oss` model IDs were not available on the
  OpenAI account in this smoke path.
- Anthropic direct: 5 OK after omitting deprecated `temperature` from the smoke
  payload.
- Grok direct: 3 OK.
- Gemini direct: no local `GOOGLE_API_KEY`, `GEMINI_API_KEY`,
  `GOOGLE_AI_API_KEY`, or `codex-gemini-api-key` Keychain item was found, so the
  smoke runner retried the five Gemini entries through OpenRouter as
  `google/<model>`. Four returned OK; `gemini-3.5-flash` returned HTTP 200 with
  an empty visible response.
