---
title: Paper V1 Top Thinking Cost Estimates
date: 2026-06-02
type: research
status: draft
---

# Paper V1 Top Thinking Cost Estimates

This is a focused flagship/top-model sweep designed to test whether explicit higher thinking levels add measurable ObviousBench accuracy on `paper_v1`, or mainly add tokens/cost once models are already near 100% answer accuracy.

- Panel: `configs/paper_v1_top_thinking_20260602_panel.yaml`
- Settings: 37
- Estimated full-run cost: `$6.65` before cache effects
- Budget target: `<$10`
- Output cap policy: preserve source thinking controls, but raise any `max_tokens < 2000` to `2000` to reduce truncation artefacts.
- Temperature policy: no sweep-level `temperature=0`; provider/model defaults are used unless an entry already defines temperature.

## Provider Routes

| Route | Settings |
|---|---:|
| `anthropic` | 9 |
| `grok` | 4 |
| `openai` | 10 |
| `openrouter` | 14 |

## Thinking Depths

| Depth | Settings |
|---|---:|
| `high` | 9 |
| `low` | 9 |
| `max` | 2 |
| `medium` | 8 |
| `minimal` | 2 |
| `none` | 4 |
| `xhigh` | 3 |

Detailed CSV: `docs/research/2026-06-02-paper-v1-top-thinking-cost-estimates.csv`
