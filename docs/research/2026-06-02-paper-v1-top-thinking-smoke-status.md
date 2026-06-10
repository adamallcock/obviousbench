---
title: Paper V1 Top Thinking Smoke Status
date: 2026-06-02
type: research
status: draft
---

# Paper V1 Top Thinking Smoke Status

- Source panel: `configs/paper_v1_top_thinking_20260602_panel.yaml`
- Clean full-run panel: `configs/paper_v1_top_thinking_clean_20260602_panel.yaml`
- Smoke status: `results/summaries/paper-v1-top-thinking-smoke-20260602/status.jsonl`
- Passed: 29
- Excluded after smoke: 8

## Excluded After Smoke

| Entry | Model | Status | Reason |
|---|---|---|---|
| `top-thinking-020-grok-grok-4-3-none` | `grok/grok-4.3` | `failed_inspect` | content_filter/provider refusal during smoke |
| `top-thinking-021-grok-grok-4-3-low` | `grok/grok-4.3` | `failed_inspect` | content_filter/provider refusal during smoke |
| `top-thinking-022-grok-grok-4-3-medium` | `grok/grok-4.3` | `failed_inspect` | content_filter/provider refusal during smoke |
| `top-thinking-023-grok-grok-4-3-high` | `grok/grok-4.3` | `failed_inspect` | content_filter/provider refusal during smoke |
| `top-thinking-024-openrouter-x-ai-grok-4-3-none` | `openrouter/x-ai/grok-4.3` | `failed_summary_validation` | summary has total_samples=3 and scored_samples=2; expected 3 total samples and expected 3 scored samples; provider_errors=1 |
| `top-thinking-025-openrouter-x-ai-grok-4-3-low` | `openrouter/x-ai/grok-4.3` | `failed_summary_validation` | summary has total_samples=3 and scored_samples=2; expected 3 total samples and expected 3 scored samples; provider_errors=1 |
| `top-thinking-026-openrouter-x-ai-grok-4-3-medium` | `openrouter/x-ai/grok-4.3` | `failed_summary_validation` | summary has total_samples=3 and scored_samples=2; expected 3 total samples and expected 3 scored samples; provider_errors=1 |
| `top-thinking-027-openrouter-x-ai-grok-4-3-high` | `openrouter/x-ai/grok-4.3` | `failed_summary_validation` | summary has total_samples=3 and scored_samples=2; expected 3 total samples and expected 3 scored samples; provider_errors=1 |

The Grok failures were investigated in the raw smoke logs and are provider-side `content_filter`/provider-error behavior on the JSON `true` sample, not a deterministic grader parsing issue.
