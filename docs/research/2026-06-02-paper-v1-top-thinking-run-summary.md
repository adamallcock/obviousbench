---
title: Paper V1 Top Thinking Run Summary
date: 2026-06-02
type: research
status: draft
---

# Paper V1 Top Thinking Run Summary

## Artifacts

- Full clean report: `docs/reports/2026-06-02-paper-v1-top-thinking-clean/report.html`
- Wrong-answer review: `docs/reports/2026-06-02-paper-v1-top-thinking-clean/wrong-answer-review.html`
- Clean comparison CSV: `results/summaries/paper-v1-top-thinking-clean-20260602/comparison/comparison.csv`
- Clean run manifest: `configs/paper_v1_top_thinking_clean_20260602_manifest.csv`
- Source 37-setting panel: `configs/paper_v1_top_thinking_20260602_panel.yaml`
- Smoke status: `docs/research/2026-06-02-paper-v1-top-thinking-smoke-status.md`

## Run Status

The clean full run completed with 29 model settings, all with `80/80` scored samples and `0` provider errors. The broader 37-setting smoke panel excluded 8 Grok 4.3 settings from the clean report because both direct xAI and OpenRouter Grok hit provider-side `content_filter`/provider-error behavior on the JSON `true` item. That is not a grader parsing issue.

## Immediate Read

The fear that every latest/top model would trivially score 100% is only partly true. Ten of 29 clean settings reached 100% answer accuracy, but minimal/no-thinking settings often did not. The more interesting result is effort saturation: once a model family reaches 100%, higher effort often adds tokens and cost without improving answer accuracy.

- Cheapest 100% answer run: Google: Gemini 3.1 Flash Lite medium at `$0.000214` per correct.
- Lowest-token 100% answer run: OpenAI GPT-5.5 low at `70` tokens per correct.
- 100% answer settings: 10 of 29.
- 100% strict settings: 9 of 29.

## Effort Patterns

| Model family | Accuracy and token pattern |
|---|---|
| Claude Opus 4.8 | `low` 92.5%, 5012 tokens; `medium` 92.5%, 5080 tokens; `high` 92.5%, 4951 tokens; `xhigh` 92.5%, 4987 tokens; `max` 88.8%, 5194 tokens |
| Claude Sonnet 4.6 | `low` 90.0%, 3976 tokens; `medium` 88.8%, 4017 tokens; `high` 88.8%, 4180 tokens; `max` 86.2%, 4132 tokens |
| OpenAI GPT-5.4 | `none` 86.2%, 3633 tokens; `low` 96.2%, 5026 tokens; `medium` 97.5%, 6657 tokens; `high` 97.5%, 7403 tokens; `xhigh` 98.8%, 9320 tokens |
| OpenAI GPT-5.5 | `none` 91.2%, 3681 tokens; `low` 100.0%, 5663 tokens; `medium` 100.0%, 6226 tokens; `high` 100.0%, 7049 tokens; `xhigh` 100.0%, 8155 tokens |
| Gemini 3.1 Flash Lite | `minimal` 85.0%, 3192 tokens; `low` 96.2%, 12977 tokens; `medium` 100.0%, 13870 tokens; `high` 100.0%, 19881 tokens |
| Gemini 3.1 Pro Preview Custom Tools | `low` 100.0%, 14010 tokens; `high` 100.0%, 17391 tokens |
| Gemini 3.5 Flash | `minimal` 90.0%, 3170 tokens; `low` 100.0%, 12810 tokens; `medium` 98.8%, 19075 tokens; `high` 100.0%, 19584 tokens |

## Efficiency Warnings

These rows come from `effort_curve.csv`; they compare higher efforts against the lowest effort for the same model base.

| Model base | Effort | Accuracy delta | Token delta | Cost delta | Warning |
|---|---:|---:|---:|---:|---|
| `anthropic/claude-opus-4-8` | `medium` | 0 | 68 | 0.00052 | `higher_cost_no_accuracy_gain` |
| `anthropic/claude-opus-4-8` | `xhigh` | 0 | -25 | 0.000635 | `higher_cost_no_accuracy_gain` |
| `anthropic/claude-opus-4-8` | `max` | -0.0375 | 182 | 0.00629 | `higher_tokens_lower_accuracy` |
| `anthropic/claude-sonnet-4-6` | `medium` | -0.0125 | 41 | 0.000615 | `higher_tokens_lower_accuracy` |
| `anthropic/claude-sonnet-4-6` | `high` | -0.0125 | 204 | 0.00252 | `higher_tokens_lower_accuracy` |
| `anthropic/claude-sonnet-4-6` | `max` | -0.0375 | 156 | 0.0018 | `higher_tokens_lower_accuracy` |
| `openrouter/google/gemini-3.1-pro-preview-customtools` | `high` | 0 | 3381 | 0.040962 | `higher_cost_no_accuracy_gain` |

## Interpretation For The Paper

Use this sweep as evidence for a sharper claim: ObviousBench is not simply exposing failure of small models. It also exposes that explicit reasoning controls can be economically inefficient on obvious tasks. For strong models, `low` or `medium` can be enough; higher modes frequently increase hidden/charged reasoning tokens without answer-accuracy gains. For Claude, the current adapter does not report separate reasoning tokens, so the report should avoid treating Claude `effort` as directly comparable to reported Gemini/OpenAI reasoning-token telemetry.

## Source Notes

- Google documents Gemini 3 `thinkingLevel` and dynamic/default thinking behavior: https://ai.google.dev/gemini-api/docs/thinking
- OpenRouter documents mapping `reasoning.effort` to Gemini 3 `thinkingLevel`: https://openrouter.ai/docs/guides/best-practices/reasoning-tokens
- OpenAI documents `reasoning.effort` values and adaptive reasoning: https://developers.openai.com/api/docs/guides/reasoning
- xAI documents Grok 4.3 `reasoning_effort` values and defaults: https://docs.x.ai/developers/model-capabilities/text/reasoning
- Anthropic documents Claude extended/adaptive thinking controls: https://platform.claude.com/docs/en/build-with-claude/extended-thinking
