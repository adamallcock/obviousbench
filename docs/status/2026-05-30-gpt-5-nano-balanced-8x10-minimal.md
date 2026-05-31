---
title: GPT-5 Nano Balanced 8x10 Minimal Run
date: 2026-05-30
type: status
status: complete
---

# GPT-5 Nano Balanced 8x10 Minimal Run

## Command

```bash
OPENAI_API_KEY="$(security find-generic-password -s OPENAI_API_KEY -w)" \
  .venv/bin/inspect eval obviousbench/tasks/barrage.py \
  --model openai/gpt-5-nano \
  --log-dir results/raw/gpt-5-nano-balanced-8x10-minimal-20260530-210720 \
  -T profile=balanced_8x10 \
  -T seed=20260531 \
  --reasoning-effort minimal \
  --reasoning-summary none \
  --max-connections 4 \
  --max-retries 3 \
  --timeout 240 \
  --attempt-timeout 120 \
  --no-log-realtime \
  --no-log-model-api \
  --no-fail-on-error \
  --continue-on-fail \
  --score-on-error
```

The shell wrapper attempted to assign to zsh's read-only `status` variable after
Inspect finished, so the wrapper exited non-zero. The Inspect eval itself
completed successfully and produced a valid `.eval` log.

## Artifacts

- Raw log directory:
  `results/raw/gpt-5-nano-balanced-8x10-minimal-20260530-210720`
- Summary directory:
  `results/summaries/gpt-5-nano-balanced-8x10-minimal-20260530-210720`
- Summary CSV:
  `results/summaries/gpt-5-nano-balanced-8x10-minimal-20260530-210720/summary.csv`
- Failure gallery:
  `results/summaries/gpt-5-nano-balanced-8x10-minimal-20260530-210720/failure_gallery.md`
- Costed summary directory:
  `results/summaries/gpt-5-nano-balanced-8x10-minimal-20260530-210720-costed`

## Summary

```text
model: openai/gpt-5-nano
profile: balanced_8x10
seed: 20260531
samples: 80
scored_samples: 80
correct: 60
failures: 20
accuracy: 0.75
obvious_failure_rate: 0.25
failures_per_1000: 250
provider_errors: 0
timeouts: 0
reasoning_effort: minimal
reasoning_summary: none
reasoning_tokens: 0
input_tokens: 3281
output_tokens: 1833
total_tokens: 5114
estimated_cost_usd: 0.00089725
```

## Per-Family Breakdown

| Family | Correct | Total | Accuracy |
| --- | ---: | ---: | ---: |
| arithmetic | 9 | 10 | 90% |
| character_count | 2 | 10 | 20% |
| constraint_awareness | 9 | 10 | 90% |
| format_compliance | 10 | 10 | 100% |
| negation | 10 | 10 | 100% |
| ordering | 8 | 10 | 80% |
| spelling_transform | 3 | 10 | 30% |
| word_count | 9 | 10 | 90% |

## Notable Failures

- Arithmetic: `obviousbench.arith.en.v0.public.000021` answered `9.11` for
  "Which is larger, 9.9 or 9.11?" Expected `9.9`.
- Character count: 8 of 10 failed, including raspberry, responsiveness,
  alphabetical, coconut, bookkeeping, and accessibility variants.
- Constraint awareness: `obviousbench.constraint.en.v0.public.000004` chose
  `Walk` for the car wash prompt. Expected `Drive`.
- Ordering: two alphabetical/numeric ordering failures.
- Spelling transform: 7 of 10 failed, including remove-letter, replace-letter,
  and reverse-word prompts.
