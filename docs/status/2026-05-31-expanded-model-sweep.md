---
title: Expanded Model Sweep
date: 2026-05-31
type: status
status: complete
---

# Expanded Model Sweep

> Snapshot note: this is a point-in-time expanded sweep. The later mega sweep
> and rescored V2 report supersede it for current model-comparison claims, while
> this file remains useful for provider-limit and cost-history context.

Run date: 2026-05-31  
Primary profile: `balanced_8x10`  
Free-model profile: `balanced_8x2`  
Summary directory: `results/summaries/expanded-model-sweep-20260531-0028`

## Headline Results

| Model | Profile | Correct | Accuracy | Provider Errors | Tokens | Est. Cost |
|---|---:|---:|---:|---:|---:|---:|
| GPT-5 Nano minimal | 8x10 | 60/80 | 75.00% | 0 | 5,114 | $0.00089725 |
| GPT-4.1 none | 8x10 | 64/80 | 80.00% | 0 | 3,580 | $0.008474 |
| GPT-4o none | 8x10 | 59/80 | 73.75% | 0 | 3,626 | $0.0110525 |
| GPT-5.5 none | 8x10 | 73/80 | 91.25% | 0 | 3,809 | $0.032245 |
| GPT-5.2 none | 8x10 | 70/80 | 87.50% | 0 | 3,809 | $0.01313375 |
| GPT-5 low | 8x10 | 79/80 | 98.75% | 0 | 9,615 | $0.0280475 |
| GPT-5.5 medium | 8x10 | 80/80 | 100.00% | 0 | 6,422 | $0.110635 |
| Claude Haiku 4.5 | 8x10 | 61/80 | 76.25% | 0 | 4,172 | $0.006536 |
| Claude Sonnet 4.6 | 8x10 | 62/80 | 77.50% | 0 | 4,272 | $0.021108 |
| Gemini 3.5 Flash via OpenRouter | 8x10 | 78/80 | 97.50% | 0 | 17,560 | $0.135555 |
| Gemini 2.5 Flash via OpenRouter | 8x10 | 65/80 | 81.25% | 0 | 3,236 | $0.0014944 |
| OpenRouter free DeepSeek V4 Flash | 8x2 | 0/0 | n/a | 16 | 0 | $0.00 |
| OpenRouter free GPT-OSS 120B | 8x2 | 16/16 | 100.00% | 0 | 2,123 | $0.00 |

## Notes

- Costing is now the default summary behavior via the local `runcost` bridge.
- The previously run GPT-5 Nano full `balanced_8x10` estimate is `$0.00089725`.
- Anthropic required the `anthropic` Python package, now added to project
  dependencies.
- OpenRouter Gemini runs require an explicit `--max-tokens` cap; without it,
  Inspect requested a 65k output reservation and OpenRouter returned 402s.
- The OpenRouter free bucket was rate-limited during the sweep. One free model
  completed cleanly after waiting for reset; the broader free sweep should be
  treated as provider-limited, not benchmark-limited.
