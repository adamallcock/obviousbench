---
title: Balanced 8x10 No Thinking Model Comparison
date: 2026-05-30
type: status
status: complete
---

# Balanced 8x10 No Thinking Model Comparison

> Snapshot note: this is a point-in-time 2026-05-30 run record. Use later
> rescored comparison outputs and generated reports for current benchmark
> claims; keep this file as provenance for the original no-thinking panel.

## Scope

Profile: `balanced_8x10`  
Seed: `20260531`  
Samples: 80 per model  
Costing: `runcost` over normalized Inspect usage  

Runs:

- `openai/gpt-4.1`
- `openai/gpt-4o`
- `openai/gpt-5.5` with `--reasoning-effort none --reasoning-summary none`

## Summary

| Model | Correct | Accuracy | Failures | Failure Rate | Tokens | Estimated Cost |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `openai/gpt-5.5` | 73 / 80 | 91.25% | 7 | 8.75% | 3,809 | $0.03224500 |
| `openai/gpt-4.1` | 64 / 80 | 80.00% | 16 | 20.00% | 3,580 | $0.00847400 |
| `openai/gpt-4o` | 59 / 80 | 73.75% | 21 | 26.25% | 3,626 | $0.01105250 |

## Per-Family Correct

| Family | GPT-4.1 | GPT-4o | GPT-5.5 none |
| --- | ---: | ---: | ---: |
| arithmetic | 10 / 10 | 10 / 10 | 10 / 10 |
| character_count | 5 / 10 | 7 / 10 | 5 / 10 |
| constraint_awareness | 5 / 10 | 1 / 10 | 10 / 10 |
| format_compliance | 10 / 10 | 7 / 10 | 10 / 10 |
| negation | 8 / 10 | 5 / 10 | 10 / 10 |
| ordering | 10 / 10 | 10 / 10 | 10 / 10 |
| spelling_transform | 6 / 10 | 9 / 10 | 8 / 10 |
| word_count | 10 / 10 | 10 / 10 | 10 / 10 |

## Worst Sections

| Model | Section | Correct | Failures | Estimated Cost |
| --- | --- | ---: | ---: | ---: |
| `openai/gpt-4o` | `constraint_awareness/object_must_be_present` | 1 / 10 | 9 | $0.00191000 |
| `openai/gpt-4.1` | `character_count/single_letter_count` | 5 / 10 | 5 | $0.00074400 |
| `openai/gpt-4.1` | `constraint_awareness/object_must_be_present` | 5 / 10 | 5 | $0.00136800 |
| `openai/gpt-5.5` | `character_count/single_letter_count` | 5 / 10 | 5 | $0.00311000 |
| `openai/gpt-4o` | `negation/not_choice` | 1 / 5 | 4 | $0.00072750 |

## Artifacts

Aggregate comparison:

- `results/summaries/model-comparison-balanced-8x10-nothinking-20260530-2136/comparison.csv`
- `results/summaries/model-comparison-balanced-8x10-nothinking-20260530-2136/family_comparison.csv`
- `results/summaries/model-comparison-balanced-8x10-nothinking-20260530-2136/section_comparison.csv`

Per-run summaries:

- `results/summaries/gpt-4-1-balanced-8x10-nothinking-20260530-213526`
- `results/summaries/gpt-4o-balanced-8x10-nothinking-20260530-213550`
- `results/summaries/gpt-5-5-balanced-8x10-nothinking-20260530-213600`

Raw logs:

- `results/raw/gpt-4-1-balanced-8x10-nothinking-20260530-213526`
- `results/raw/gpt-4o-balanced-8x10-nothinking-20260530-213550`
- `results/raw/gpt-5-5-balanced-8x10-nothinking-20260530-213600`

## Notes

- `gpt-5.5` accepted `reasoning_effort=none` and reported zero reasoning
  tokens.
- `gpt-4.1` and `gpt-4o` were run without reasoning flags, since they are not
  reasoning-mode runs in this setup.
- The biggest recurring weakness is still character counting. Even `gpt-5.5`
  only scored 5 / 10 on `single_letter_count`.
- The most surprising section failure was `gpt-4o` on
  `object_must_be_present`, where it scored 1 / 10.
