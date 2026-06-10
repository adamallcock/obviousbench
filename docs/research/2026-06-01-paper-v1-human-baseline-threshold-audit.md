---
title: Paper V1 Human Baseline Threshold Audit
date: 2026-06-01
type: research
status: blocked
---

# Paper V1 Human Baseline Threshold Audit

This report classifies scored human-baseline rows against the
predeclared ObviousBench paper thresholds. It does not collect
participant data, adjudicate ambiguous answers, or run model providers.

Overall status: BLOCKED

- Scored responses: `data/human_baseline/paper_v1_scored_draft.csv`
- Answer key: `data/human_baseline/paper_v1_answer_key.csv`
- Item output: `data/human_baseline/paper_v1_threshold_items.csv`
- Family output: `data/human_baseline/paper_v1_threshold_families.csv`
- Items: 80
- Scored response rows used: 0
- Ignored scored rows: 400
- Unknown-item rows: 0
- Core H0 items: 0
- Borderline items: 0
- Excluded items: 0
- Items with no scored data: 80
- Structural issues: 0

## Threshold Rules

- `core_h0`: accuracy at or above 95% and median time below 10 seconds.
- `borderline`: at least 80% accuracy and no exclusion trigger, but not core H0.
- `exclude`: accuracy below 80%, median time above 30 seconds, or repeated confusion or ambiguity notes.
- `no_data`: no scored human response rows are available for the item.

## Family Summary

| Family | Items | Core H0 | Borderline | Exclude | No Data | Responses | Median Accuracy | Median Seconds |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| arithmetic | 10 | 0 | 0 | 0 | 10 | 0 |  |  |
| character_count | 10 | 0 | 0 | 0 | 10 | 0 |  |  |
| constraint_awareness | 10 | 0 | 0 | 0 | 10 | 0 |  |  |
| format_compliance | 10 | 0 | 0 | 0 | 10 | 0 |  |  |
| negation | 10 | 0 | 0 | 0 | 10 | 0 |  |  |
| ordering | 10 | 0 | 0 | 0 | 10 | 0 |  |  |
| spelling_transform | 10 | 0 | 0 | 0 | 10 | 0 |  |  |
| word_count | 10 | 0 | 0 | 0 | 10 | 0 |  |  |

## No-Data Items

- `obviousbench.char_count.en.v0.public.000040`
- `obviousbench.spell.en.v0.public.000002`
- `obviousbench.arith.en.v0.public.000023`
- `obviousbench.word_count.en.v0.public.000045`
- `obviousbench.ordering.en.v0.public.000048`
- `obviousbench.format.en.v0.public.000047`
- `obviousbench.negation.en.v0.public.000034`
- `obviousbench.constraint.en.v0.public.000040`
- `obviousbench.char_count.en.v0.public.000030`
- `obviousbench.spell.en.v0.public.000005`
- `obviousbench.arith.en.v0.public.000021`
- `obviousbench.word_count.en.v0.public.000033`
- `obviousbench.ordering.en.v0.public.000049`
- `obviousbench.format.en.v0.public.000048`
- `obviousbench.negation.en.v0.public.000033`
- `obviousbench.constraint.en.v0.public.000003`
- `obviousbench.char_count.en.v0.public.000029`
- `obviousbench.spell.en.v0.public.000020`
- `obviousbench.arith.en.v0.public.000022`
- `obviousbench.word_count.en.v0.public.000070`
- `obviousbench.ordering.en.v0.public.000046`
- `obviousbench.format.en.v0.public.000049`
- `obviousbench.negation.en.v0.public.000031`
- `obviousbench.constraint.en.v0.public.000038`
- `obviousbench.char_count.en.v0.public.000017`
- `obviousbench.spell.en.v0.public.000022`
- `obviousbench.arith.en.v0.public.000024`
- `obviousbench.word_count.en.v0.public.000015`
- `obviousbench.ordering.en.v0.public.000050`
- `obviousbench.format.en.v0.public.000046`
- `obviousbench.negation.en.v0.public.000035`
- `obviousbench.constraint.en.v0.public.000036`
- `obviousbench.char_count.en.v0.public.000046`
- `obviousbench.spell.en.v0.public.000008`
- `obviousbench.arith.en.v0.public.000025`
- `obviousbench.word_count.en.v0.public.000051`
- `obviousbench.ordering.en.v0.public.000047`
- `obviousbench.format.en.v0.public.000050`
- `obviousbench.negation.en.v0.public.000032`
- `obviousbench.constraint.en.v0.public.000032`
- 40 additional item(s) omitted.

## Use In Paper

Use only `core_h0` rows for headline human-trivial claims. Keep
`borderline` and `exclude` rows out of headline claims unless the
paper explicitly labels them as appendix or diagnostic material.
Do not promote this audit to final evidence while `no_data` rows
remain.
