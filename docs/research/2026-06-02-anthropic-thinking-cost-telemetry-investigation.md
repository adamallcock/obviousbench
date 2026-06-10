---
title: Anthropic Thinking Cost Telemetry Investigation
date: 2026-06-02
type: research
status: draft
---

# Anthropic Thinking Cost Telemetry Investigation

## Executive Summary

The current Anthropic "thinking" rows are not reliable evidence of billed adaptive-thinking cost. The local evidence indicates that the benchmark did pass Anthropic `output_config.effort` through Inspect, but did not enable Anthropic adaptive thinking with `thinking: {"type": "adaptive"}`. As a result, the runs likely exercised Claude's effort parameter without extended thinking enabled.

This explains why every direct Anthropic effort row reports `reasoning_tokens=0`: no visible or summarized thinking blocks were returned, and Inspect's Anthropic adapter only derives `ModelUsage.reasoning_tokens` by counting returned `ThinkingBlock` text. The raw sample logs also contain only `input_tokens`, `output_tokens`, cache token fields, and text content blocks. The cost ledgers then price only the normalized visible input/output usage provided to runcost.

Most likely root causes:

1. **Primary config-path issue:** `provider_request_settings.thinking.type=adaptive` exists in the panel metadata, but the runner passes only `generation_settings` to Inspect. The saved GenerateConfig files contain `effort`, `max_tokens`, and `seed`, not `thinking`.
2. **Telemetry parser gap if adaptive thinking is later enabled:** Anthropic documents `usage.output_tokens_details.thinking_tokens` as the read-only breakdown for billed internal reasoning. The installed Inspect adapter currently derives `reasoning_tokens` by counting returned `ThinkingBlock` text, not by reading `output_tokens_details.thinking_tokens`.
3. **Cost-accounting consequence:** runcost receives `normalized.usage` from ObviousBench with `reasoning_tokens=0`, so cost ledgers contain only input and output text components. If hidden thinking was enabled but omitted from parsed usage, costs would be undercounted; for the current runs, the stronger evidence is that adaptive thinking was not enabled in the first place.

## Evidence Table

| Finding | Evidence | Interpretation |
|---|---|---|
| Current combined report rows show zero reasoning tokens for all direct Anthropic effort rows. | `results/summaries/paper-v1-combined-237-overline-attempt-scored-20260602/comparison/comparison.csv:212-220` has Opus/Sonnet low/medium/high/xhigh/max with `reasoning_tokens=0` and `reasoning_token_source=not_reported_or_zero`. | The plotted cost curves are using visible input/output token costs only. |
| No-thinking fill rows also have zero reasoning tokens. | `results/summaries/paper-v1-combined-237-overline-attempt-scored-20260602/comparison/comparison.csv:237-238` has `Claude Opus 4.8 none` and `Claude Sonnet 4.6 none` with `reasoning_tokens=0`. | The fill confirms zero reasoning is not unique to effort rows. |
| The top-thinking panel intended adaptive thinking. | `configs/paper_v1_top_thinking_clean_20260602_panel.yaml:797-806` shows Opus high `generation_settings: {max_tokens, effort}` and separate `provider_request_settings: {thinking: {type: adaptive, display: omitted}, output_config: {effort}}`. Similar Anthropic registry entries appear in `configs/model_thinking_settings_v1.yaml:2063-2305` and `configs/model_thinking_settings_v1.yaml:2348-2580`. | The benchmark design captured the intended provider request shape, but only part of it was executable by the current runner. |
| The no-thinking fill panel intentionally omits thinking and effort. | `configs/paper_v1_anthropic_no_thinking_fill_20260602_panel.yaml:24-27` and `:38-41` use `control_style: anthropic_no_thinking` and only `generation_settings.max_tokens`. | This gives a local control surface for comparing raw configs and summary costs. |
| The runner passes only `generation_settings` to Inspect. | `obviousbench/research/model_panel_runner.py:250-255` constructs `InspectEvalConfig(... generation_settings=_generation_settings(...))`; `_generation_settings` merges defaults and entry `generation_settings` at `obviousbench/research/model_panel_runner.py:261-274`. | `provider_request_settings` is inert metadata for this runner unless copied into `generation_settings` or translated elsewhere. |
| Inspect command uses `--generate-config` only. | `obviousbench/runners/inspect_eval.py:65-70` adds `--generate-config <path>` when `config.generation_settings` is non-empty. | Only the generated JSON reaches Inspect. |
| Raw saved configs for effort rows contain `effort` but no `thinking`. | `results/raw/paper-v1-top-thinking-clean-20260602/top-thinking-016-anthropic-claude-sonnet-4-6-low/_generate_config_8174923c0053.json:1` is `{"effort":"low","max_tokens":2000,"seed":20260531}`. `results/raw/paper-v1-top-thinking-clean-20260602/top-thinking-019-anthropic-claude-sonnet-4-6-max/_generate_config_7ba99886a45b.json:1` is `{"effort":"max","max_tokens":32840,"seed":20260531}`. | The actual Inspect GenerateConfig did not include `thinking`. |
| Raw saved config for no-thinking fill contains no `effort` or `thinking`. | `results/raw/paper-v1-fill-anthropic-no-thinking-20260602/fill-anthropic-claude-sonnet-4-6-none/_generate_config_f71117a048dd.json:1` is `{"max_tokens":2000,"seed":20260531}`. | The direct difference between fill and effort configs is `effort`, not enabled thinking. |
| Installed Inspect supports `GenerateConfig.effort`. | `.venv/lib/python3.14/site-packages/inspect_ai/model/_generate_config.py:277-280` defines `effort` and describes it as an Anthropic Claude Opus 4.5+ parameter. | `effort` is not being silently rejected as an unknown GenerateConfig field. |
| Inspect's Anthropic adapter maps `effort` to `output_config.effort`. | `.venv/lib/python3.14/site-packages/inspect_ai/model/_providers/anthropic.py:833-841` appends `effort-2025-11-24` and sets `params["output_config"] = OutputConfigParam(effort=effort)`. | The saved `effort` likely reached the provider as `output_config.effort`. |
| Inspect only sets `thinking` when `reasoning_effort` or `reasoning_tokens` is used. | `.venv/lib/python3.14/site-packages/inspect_ai/model/_providers/anthropic.py:843-868` sets `params["thinking"]` inside `if self.is_using_thinking(config)`. `is_using_thinking` at `.venv/lib/python3.14/site-packages/inspect_ai/model/_providers/anthropic.py:962-966` depends on bridged `reasoning_tokens` or `reasoning_effort`, not `effort`. | Current `generation_settings.effort` did not enable adaptive thinking in Inspect. |
| Inspect can map `reasoning_effort` to adaptive thinking for Claude frontier models. | `.venv/lib/python3.14/site-packages/inspect_ai/model/_providers/anthropic.py:1559-1578` maps `reasoning_effort` values to Anthropic effort values; `.venv/lib/python3.14/site-packages/inspect_ai/model/_providers/anthropic.py:845-849` then sets `thinking={type: adaptive, display: summarized}` and `output_config.effort`. | A likely low-risk runner/config fix is to use `reasoning_effort` for Anthropic adaptive-thinking rows instead of bare `effort`. |
| Raw sample logs expose no reasoning usage fields. | Example sampled records from `results/raw/paper-v1-top-thinking-clean-20260602/top-thinking-019-anthropic-claude-sonnet-4-6-max/*.eval` show `output.usage` with `input_tokens`, `output_tokens`, `total_tokens`, `input_tokens_cache_write`, and `input_tokens_cache_read`; assistant content block types are only `text`. | The saved Inspect output has no `thinking_tokens`, no visible `ThinkingBlock`, and no metadata carrying hidden billed reasoning. |
| Inspect derives Anthropic `reasoning_tokens` from returned thinking text. | `.venv/lib/python3.14/site-packages/inspect_ai/model/_providers/anthropic.py:2337-2344` counts tokens for each `ThinkingBlock`; `.venv/lib/python3.14/site-packages/inspect_ai/model/_providers/anthropic.py:2427-2434` stores that count as `ModelUsage.reasoning_tokens` only if positive. | With omitted or absent thinking blocks, `reasoning_tokens` becomes `None`/0 even if a provider usage breakdown exists elsewhere. |
| ObviousBench feeds runcost normalized usage only. | `obviousbench/analysis/usage.py:360-379` builds cost input with `input_tokens`, `output_tokens`, `reasoning_tokens`, cache tokens, and `total_tokens` from `EvalRecord`. | If `EvalRecord.reasoning_tokens` is zero, runcost cannot infer hidden thinking tokens. |
| Cost ledgers contain visible input/output components only. | `results/summaries/paper-v1-top-thinking-clean-20260602/top-thinking-019-anthropic-claude-sonnet-4-6-max/cost_ledger.json` records components such as `input_uncached_tokens` and `output_text_tokens`; sampled records have no reasoning component. | Current summary costs are visible-token runcost prices, not calibrated thinking estimates. |
| Anthropic official docs say effort alone is not the same as adaptive thinking. | Anthropic's effort docs say effort can be used without thinking and affects all token spend; the adaptive-thinking docs say Opus 4.8 thinking is off unless `thinking: {type: "adaptive"}` is explicitly set, and adaptive+effort examples include both `thinking` and `output_config`. See [Effort](https://platform.claude.com/docs/en/build-with-claude/effort) and [Adaptive thinking](https://platform.claude.com/docs/en/build-with-claude/adaptive-thinking). | The local request shape is consistent with effort-only runs, not enabled adaptive-thinking runs. |
| Anthropic official docs identify the expected hidden-thinking telemetry field. | Anthropic's adaptive-thinking docs say billed output includes internal thinking and expose `usage.output_tokens_details.thinking_tokens` as the read-only breakdown. See [Adaptive thinking pricing](https://platform.claude.com/docs/en/build-with-claude/adaptive-thinking). | The parser should eventually read this provider usage field when available. |

## Root-Cause Assessment

### 1. Are Anthropic adaptive thinking settings actually passed in a supported way?

Partially. The effort setting is passed in a supported way; adaptive thinking is not.

The panel rows contain both executable `generation_settings` and non-executable `provider_request_settings`. The saved raw GenerateConfig files prove that only `effort`, `max_tokens`, and `seed` reached Inspect for the effort rows. Inspect's Anthropic provider maps `GenerateConfig.effort` to Anthropic `output_config.effort`, so the effort parameter likely reached the API.

However, the official Anthropic docs and Inspect provider code both indicate that adaptive thinking requires a `thinking` configuration. In this installed Inspect version, `thinking` is emitted only when `reasoning_effort` or `reasoning_tokens` is present. Current rows use `effort`, not `reasoning_effort`, so they do not enter Inspect's `is_using_thinking` path.

Therefore the labels `low/medium/high/xhigh/max` are valid as Anthropic effort settings, but not valid as "adaptive thinking enabled" settings.

### 2. Should Anthropic usage telemetry expose thinking/reasoning tokens?

If adaptive thinking is actually enabled and the provider emits the documented response shape, yes: Anthropic documents `usage.output_tokens_details.thinking_tokens` as the breakdown for internal reasoning, while `usage.output_tokens` remains the inclusive billed output total.

The saved raw Inspect sample JSONs do not include `output_tokens_details` or any thinking block content. For the current run, that is consistent with adaptive thinking not being enabled. It also means the current artifacts cannot recover hidden thinking tokens after the fact.

There is also a future parser gap: Inspect's Anthropic adapter derives `ModelUsage.reasoning_tokens` by token-counting visible `ThinkingBlock` text. That is fragile for adaptive thinking with `display: "omitted"` and does not use Anthropic's documented `usage.output_tokens_details.thinking_tokens` field.

### 3. Is runcost/summary accounting missing a hidden-thinking billing component?

For the current artifacts, runcost is not independently missing a known field; it is pricing exactly what ObviousBench gives it. ObviousBench passes normalized usage with `reasoning_tokens=0`, and the cost ledgers show input/output text token components only.

If a future corrected adaptive-thinking run returns `output_tokens` inclusive of thinking and `output_tokens_details.thinking_tokens`, then the cost policy should avoid double-counting. Anthropic says `output_tokens` is authoritative and inclusive. In that case:

- Total Anthropic cost should be computed from `input_tokens` plus inclusive `output_tokens`.
- `reasoning_tokens` should be stored for observability and charts.
- If `output_tokens` is already inclusive, cost code should not add `reasoning_tokens` on top for Anthropic rows.

The existing comparison fallback in `obviousbench/analysis/comparison.py:702-709` adds `output_tokens + reasoning_tokens` for manual price-registry fallback. That is appropriate for providers where output excludes reasoning, but it would overcount Anthropic if `output_tokens` is inclusive and `reasoning_tokens` is a breakdown.

## Comparison: No-Thinking vs Effort Rows

Fresh no-thinking fill:

- `Claude Sonnet 4.6 none`: `input_tokens=3629`, `output_tokens=707`, `reasoning_tokens=0`, `estimated_cost_usd=0.021492`.
- `Claude Opus 4.8 none`: `input_tokens=4692`, `output_tokens=430`, `reasoning_tokens=0`, `estimated_cost_usd=0.03421`.

Effort rows:

- `Claude Sonnet 4.6 low`: `input_tokens=3465`, `output_tokens=511`, `reasoning_tokens=0`, `estimated_cost_usd=0.01806`.
- `Claude Sonnet 4.6 max`: `input_tokens=3510`, `output_tokens=622`, `reasoning_tokens=0`, `estimated_cost_usd=0.01986`.
- `Claude Opus 4.8 low`: `input_tokens=4598`, `output_tokens=414`, `reasoning_tokens=0`, `estimated_cost_usd=0.03334`.
- `Claude Opus 4.8 max`: `input_tokens=4511`, `output_tokens=683`, `reasoning_tokens=0`, `estimated_cost_usd=0.03963`.

The effort rows do show behavior and visible-output differences, so `output_config.effort` may have affected response style and verbosity. They do not show evidence of adaptive-thinking billing telemetry.

## Recommended Fixes and Tests

### Fix 1: Make Anthropic adaptive-thinking rows executable

Use Inspect's supported `reasoning_effort` path for Anthropic adaptive-thinking entries, or add a runner translation layer that converts `control_style: anthropic_adaptive_thinking_effort` into:

```yaml
generation_settings:
  max_tokens: <cap>
  reasoning_effort: low|medium|high|xhigh|max
```

Inspect's current Anthropic adapter should then emit:

- `thinking: {"type": "adaptive", "display": "summarized"}`
- `output_config: {"effort": <mapped effort>}`

For Opus 4.8, consider whether `display: "omitted"` is required for latency/privacy. If yes, verify Inspect can pass that exact display mode, or use `extra_headers`/provider support if available. For telemetry validation, `display: "summarized"` is useful because it should produce a visible `ThinkingBlock`, but it may not match the intended production display mode.

### Fix 2: Add a runner/panel test for Anthropic adaptive settings

Add a unit test that builds an `InspectEvalConfig` for a representative `anthropic_adaptive_thinking_effort` entry and asserts the generated config contains `reasoning_effort` or another field that Inspect maps to `thinking`, not just `effort`.

Suggested assertions:

- Existing effort-only rows are labeled as effort-only, not thinking-enabled.
- Adaptive-thinking rows include a setting that enters Inspect's `is_using_thinking` path.
- No-thinking fill rows omit both `effort` and thinking controls.

### Fix 3: Add a no-paid-call request-shape smoke

Use a monkeypatched or fake Inspect Anthropic API object to call `completion_config()` with representative GenerateConfig values and assert request fields:

- `GenerateConfig(effort="max")` produces `output_config.effort` but no `thinking`.
- `GenerateConfig(reasoning_effort="max")` produces both `thinking.type=adaptive` and `output_config.effort=max`.

This can be done entirely locally without provider calls.

### Fix 4: Parse Anthropic thinking telemetry when available

Inspect currently does not expose `output_tokens_details.thinking_tokens` through `ModelUsage.reasoning_tokens` in the inspected local code path. Options:

1. Upstream/follow Inspect: file or check for an Inspect release that maps Anthropic `usage.output_tokens_details.thinking_tokens` into `ModelUsage.reasoning_tokens`.
2. Local post-processing fallback: when raw model API logging is enabled in a controlled smoke, read `output.usage.output_tokens_details.thinking_tokens` if present and store it as `reasoning_tokens`.
3. Avoid logging raw responses in full benchmark runs unless needed; API responses may include sensitive prompt/output content.

### Fix 5: Fix cost semantics before adding Anthropic reasoning tokens

For Anthropic, treat `output_tokens` as inclusive billed output and `reasoning_tokens` as a breakdown. Do not compute cost as `output_tokens + reasoning_tokens` when the provider docs say `output_tokens` already includes thinking.

Add tests for both semantics:

- Provider where output excludes reasoning: cost uses `output_tokens + reasoning_tokens`.
- Anthropic adaptive thinking: cost uses `output_tokens` only, while `reasoning_tokens` is reported separately for plots.

### Fix 6: Report/chart guardrail

Until rerun with verified adaptive-thinking request shape and telemetry, annotate the effort-cost report:

- Direct Anthropic low/medium/high/xhigh/max rows are `effort-only, thinking not confirmed`.
- Reasoning-token and cost curves should not imply hidden thinking billing for these rows.
- The no-thinking fill rows are a useful control but do not validate adaptive-thinking cost.

## Proposed Live Probe, Not Run

No new paid provider calls were run for this investigation.

If a live probe becomes necessary, keep it to one or two low-cost samples:

```bash
.venv/bin/inspect eval obviousbench.tasks.paper_v1 \
  --model anthropic/claude-sonnet-4-6 \
  --log-dir tmp/anthropic-adaptive-thinking-probe \
  --sample-id obviousbench.arith.en.v0.public.000007 \
  --generate-config tmp/anthropic-adaptive-thinking-probe/generate_config.json \
  -T dataset=$(pwd)/data/barrages/hard_obvious_8x10_seed_20260531.jsonl \
  --no-log-realtime \
  --timeout=180 \
  --max-retries=0
```

Where `generate_config.json` is:

```json
{"reasoning_effort":"low","max_tokens":2000,"seed":20260531}
```

Expected budget: one Anthropic Sonnet 4.6 request on a short ObviousBench sample, likely well under one cent. Expected evidence: request includes adaptive thinking and output usage either includes `output_tokens_details.thinking_tokens` or at least inclusive output token growth.

## Open Questions

1. Does the current Inspect release intentionally require `reasoning_effort` rather than `effort` to enable Anthropic adaptive thinking, or is `effort`-without-thinking the expected API behavior? Local code and Anthropic docs both support this interpretation, but an Inspect changelog or maintainer confirmation would be useful.
2. Can Inspect pass `thinking.display="omitted"` for adaptive thinking through GenerateConfig today, or would that require provider-specific support?
3. Does Anthropic always include `usage.output_tokens_details.thinking_tokens` for adaptive thinking, including when `display="omitted"` and when the model skips thinking? The docs imply the field is the intended observability surface, but local logs cannot confirm because current runs did not enable thinking.
4. Should the paper report compare Anthropic `effort` as a separate control from `adaptive thinking`, since Anthropic documents effort as useful even without thinking?
5. Should the report use configured/calibrated expected thinking tokens for planned-cost estimates, while keeping observed run costs separate until telemetry is verified?
