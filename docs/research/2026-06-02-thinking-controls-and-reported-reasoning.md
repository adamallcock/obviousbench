---
title: Thinking Controls And Reported Reasoning
date: 2026-06-02
type: research
status: draft
---

# Thinking Controls And Reported Reasoning

## Decision

ObviousBench reports must separate request-time thinking controls from response-time token telemetry.

- **Thinking setting**: the explicit generation setting requested for the run, such as Gemini `thinkingLevel`, Gemini `thinkingBudget`, OpenAI `reasoning.effort`, Anthropic `thinking.budget_tokens`, xAI `reasoning_effort`, or OpenRouter `reasoning`.
- **Provider default**: no explicit thinking control was sent. The provider/model may still use adaptive or default internal reasoning.
- **Reported reasoning tokens**: usage telemetry returned by the provider or adapter after generation. This is not a thinking setting.
- **Thought summaries / reasoning details**: optional returned summaries or reasoning blocks. These are not the same as the raw hidden reasoning budget.

The report should not use `reported reasoning` as a model thinking label. It should show the configured setting when available, otherwise `provider default`, while keeping `reasoning_token_source=reported` as a separate accounting field.

## Provider controls

### Google Gemini

Google's thinking guide says Gemini 3 and 2.5 models use an internal thinking process and can be run without additional request fields. Gemini models dynamically adjust reasoning by default.

For Gemini 3 and later, the recommended control is `thinkingConfig.thinkingLevel`. The current table includes:

- Gemini 3.5 Flash: `minimal`, `low`, `medium` default, `high` dynamic.
- Gemini 3.1 Flash-Lite: `minimal` default, `low`, `medium`, `high` dynamic.
- Gemini 3 Flash: `minimal`, `low`, `medium`, `high` default/dynamic.
- Gemini 3.1 Pro: `low`, `medium`, `high` default/dynamic; `minimal` is not supported.

For Gemini 2.5, the control is `thinkingConfig.thinkingBudget`. Google documents `thinkingBudget = 0` to disable thinking where supported, `-1` for dynamic thinking, and positive numeric budgets within model-specific ranges.

Sources:

- https://ai.google.dev/gemini-api/docs/thinking

### OpenRouter

OpenRouter normalizes reasoning controls behind a `reasoning` request object. The docs say `reasoning.max_tokens` is passed through as Gemini `thinkingBudget` for Google routes, and `reasoning.effort` maps to Google `thinkingLevel` values. OpenRouter can also return reasoning content/details and has separate options for excluding returned reasoning from the response.

Source:

- https://openrouter.ai/docs/guides/best-practices/reasoning-tokens

### OpenAI

OpenAI reasoning models use `reasoning.effort`. Supported values are model-dependent and can include `none`, `minimal`, `low`, `medium`, `high`, and `xhigh`. Defaults are also model-dependent, so a missing effort value is a provider/model default, not necessarily "no thinking."

Source:

- https://developers.openai.com/api/docs/guides/reasoning

### Anthropic Claude

Claude extended thinking uses a `thinking` request object. The manual form uses `type: "enabled"` and a `budget_tokens` value, while recent Claude 4.6 documentation recommends `type: "adaptive"` for Claude Opus 4.6 and Claude Sonnet 4.6. Anthropic describes the budget as the maximum internal reasoning tokens, not the summarized output.

Source:

- https://platform.claude.com/docs/en/build-with-claude/extended-thinking

### xAI Grok

xAI documents `reasoning_effort` for `grok-4.3`, with `none`, `low`, `medium`, and `high`; if unspecified, the default is `low`. xAI also exposes `reasoning_tokens` in usage metrics for reasoning models.

Source:

- https://docs.x.ai/developers/model-capabilities/text/reasoning

## Current ObviousBench interpretation

The current report pipeline computes:

- `reasoning_tokens`: observed token usage from logs.
- `reasoning_token_source`: `reported` when nonzero reasoning tokens are present, otherwise `not_reported_or_zero`.
- `overthinking_index`: `reasoning_tokens / max(output_tokens, 1)`.

Those are telemetry and efficiency metrics. They do not prove which thinking level was requested.

Current generated configs show:

- `paper-gemini-3-5-flash`: `{"max_tokens":10000,"temperature":0}`. This is provider default thinking, with reasoning tokens later reported.
- `next-089-thinking-gemini-gemini-2-5-flash-lite-low`: `{"max_tokens":10000,"reasoning_tokens":1024,"temperature":0}`. This is intended as a numeric Gemini 2.5 thinking budget run.
- `next-097-thinking-gemini-gemini-2-5-flash-lite-medium`: `{"max_tokens":10000,"reasoning_tokens":8192,"temperature":0}`. This is intended as a larger numeric Gemini 2.5 thinking budget run.
- `next-093-thinking-gemini-gemini-3-1-flash-lite-minimal`: `{"max_tokens":10000,"temperature":0}`. Despite the label, no explicit Gemini 3 `thinkingLevel` was present in the generated config, so this should be treated as provider default unless we rerun with an explicit Gemini 3 control.
- OpenRouter Gemini rows with `reasoning_effort="minimal"` are intended as OpenRouter-normalized thinking-level runs, but should be smoke-tested because OpenRouter support can drift.

## Required report language

Use these terms:

- **Configured thinking setting** for explicit request knobs.
- **Provider default** when no explicit knob was set.
- **Reported reasoning tokens** for usage accounting.
- **Overthinking index** for the ratio of reported reasoning tokens to visible output tokens.

Avoid:

- Calling a run `reported reasoning` as its thinking level.
- Comparing default Gemini rows against explicit budget rows as if both had known discrete levels.
- Treating nonzero reported reasoning tokens as proof that a specific requested thinking depth was used.

## Next implementation work

1. Add first-class `thinking_setting` metadata to comparison rows by carrying panel `generation_settings`, `thinking_depth`, and `control_style` through the manifest or a sidecar run-metadata file.
2. For Gemini 3 direct-provider runs, use an explicit provider field for `thinkingLevel` if Inspect supports it, or route through a provider-specific runner if Inspect only exposes generic `reasoning_tokens`.
3. For Gemini 2.5 direct-provider runs, verify that Inspect's `reasoning_tokens` maps to Google `thinkingBudget`; if not, use `extra_body` or a direct-provider runner.
4. Keep `reasoning_token_source` and `overthinking_index` as telemetry columns only.
