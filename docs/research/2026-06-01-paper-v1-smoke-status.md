---
title: Paper V1 Smoke Status
date: 2026-06-01
type: research
status: ready
---

# Paper V1 Smoke Status

This records the exact one-sample live smoke attempted before the larger
ObviousBench paper sweep. The current accepted smoke is the 10k safety-cap
rerun after the 64-token cap investigation.

## Result

Status: passed.

The Keychain-backed 10k-cap smoke attempted all 12 paper-panel entries against
the frozen paper dataset and sample `obviousbench.char_count.en.v0.public.000040`,
with Inspect cache disabled. All 12 entries returned at least one scored answer.
No smoke log stopped because of `max_tokens`.

Earlier smoke attempts exposed two free-route failure modes:

- `qwen/qwen3-next-80b-a3b-instruct:free` returned an OpenRouter provider
  spend-limit error.
- `openai/gpt-oss-20b:free` returned an OpenRouter rate-limit error.
- `poolside/laguna-xs.2:free` later rate-limited during the full sweep after
  logging only 20 of 80 samples.

The paper panel now uses paid OpenRouter siblings for Qwen Next, GPT-OSS 20B,
and Nemotron 3 Nano, and replaced Poolside with the paid Xiaomi MiMo-V2-Flash
route. The panel also carries an Inspect API timeout and disables Inspect-level
retries by default so a single provider route cannot stall the larger sweep.
The output cap is now a high safety cap (`max_tokens=10000`). This is explicit
instead of provider-defaulted so final runs remain reproducible across provider
default changes.

## Command

```bash
export OPENAI_API_KEY="$(security find-generic-password -s OPENAI_API_KEY -w)"
export ANTHROPIC_API_KEY="$(security find-generic-password -s ANTHROPIC_API_KEY -w)"
export OPENROUTER_API_KEY="$(security find-generic-password -s OPENROUTER_API_KEY -w)"
export XAI_API_KEY="$(security find-generic-password -s codex-xai-api-key -w)"
export GOOGLE_API_KEY="$(security find-generic-password -s GOOGLE_AI_STUDIO_API_KEY -w)"

.venv/bin/python scripts/run_model_panel.py \
  --panel configs/paper_v1_model_panel.yaml \
  --dataset data/barrages/hard_obvious_8x10_seed_20260531.jsonl \
  --raw-root results/raw/paper-v1-smoke-10k-cap \
  --summary-root results/summaries/paper-v1-smoke-10k-cap \
  --manifest-out configs/paper_v1_smoke_manifest.csv \
  --status-out results/summaries/paper-v1-smoke-10k-cap/status.jsonl \
  --mode smoke \
  --sample-id obviousbench.char_count.en.v0.public.000040 \
  --no-cache \
  --no-skip-completed \
  --cost none
```

Exit code: `0`.

## Artifacts

- Status ledger: `results/summaries/paper-v1-smoke-10k-cap/status.jsonl`
- Run manifest: `configs/paper_v1_smoke_manifest.csv`
- Raw smoke root: `results/raw/paper-v1-smoke-10k-cap`
- Summary smoke root: `results/summaries/paper-v1-smoke-10k-cap`

## Status Summary

| Status | Entries | Meaning |
| --- | ---: | --- |
| `passed` | 12 | Entry has at least one valid scored smoke response. |

| Stop reason | Entries | Meaning |
| --- | ---: | --- |
| `stop` | 12 | No high-cap smoke entry was truncated by `max_tokens`. |

| Provider route | Entries | Current blocker |
| --- | ---: | --- |
| `openai` | 3 | Passed using `OPENAI_API_KEY` from Keychain. |
| `anthropic` | 2 | Passed using `ANTHROPIC_API_KEY` from Keychain. |
| `gemini` | 2 | Passed using `GOOGLE_AI_STUDIO_API_KEY` loaded as `GOOGLE_API_KEY`. |
| `grok` | 1 | Passed using `codex-xai-api-key` loaded as `XAI_API_KEY`. |
| `openrouter` | 4 | Passed using `OPENROUTER_API_KEY` from Keychain. |

## Passed Entries

- `paper-openai-gpt-5-nano-minimal`
- `paper-openai-gpt-4-1`
- `paper-openai-gpt-4-1-mini`
- `paper-anthropic-claude-sonnet-4-6`
- `paper-anthropic-claude-haiku-4-5`
- `paper-gemini-3-5-flash`
- `paper-gemini-2-5-flash-lite`
- `paper-grok-4-3`
- `paper-openrouter-xiaomi-mimo-v2-flash`
- `paper-openrouter-nemotron-3-nano`
- `paper-openrouter-gpt-oss-20b`
- `paper-openrouter-qwen3-next`

## Runner Fixes From Smoke

- Added a resumable model-panel runner: `scripts/run_model_panel.py`.
- Threaded smoke `sample_ids` through the existing Inspect runner instead of
  using a separate execution path.
- Passed dataset paths to Inspect as absolute paths.
- Added summary validation so a smoke pass requires at least one scored sample.
- Added `google-genai` to project dependencies because the paper panel includes
  direct Gemini routes.
- Replaced fragile free OpenRouter Qwen, GPT-OSS, Nemotron, and Poolside routes
  with paid siblings or paid alternatives.
- Added default generation settings to the paper panel:
  - `--timeout=60`
  - `--max-retries=0`
- Replaced the old `max_tokens=64` short-answer cap with a high safety cap:
  - `max_tokens=10000` for current panel entries
  - future entries are clamped lower only when a provider advertises a positive
    completion ceiling below 10000

## Next Action

The 10k-cap smoke gate is clear for the 12-entry paper panel. Before the
larger run, accept the updated cost estimate, freeze a fresh output root, and
expect any remaining free OpenRouter routes in broader configs to require
retry/resume handling.
