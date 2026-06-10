---
title: Paper V1 Human Baseline Scoring Report
date: 2026-06-01
type: research
status: blocked
---

# Paper V1 Human Baseline Scoring Report

This report scores collected human-baseline response rows with the same
deterministic scorer contracts used by ObviousBench. It does not create
participant data and does not run model providers.

Overall status: BLOCKED

- Input responses: `data/human_baseline/paper_v1_response_template.csv`
- Answer key: `data/human_baseline/paper_v1_answer_key.csv`
- Scored CSV: `data/human_baseline/paper_v1_scored_draft.csv`
- Response rows: 400
- Scored rows: 0
- Correct rows: 0
- Participants: 5
- Items with rows: 80
- Issues: 800

## Family Row Counts

| Family | Rows |
| --- | ---: |
| `arithmetic` | 50 |
| `character_count` | 50 |
| `constraint_awareness` | 50 |
| `format_compliance` | 50 |
| `negation` | 50 |
| `ordering` | 50 |
| `spelling_transform` | 50 |
| `word_count` | 50 |

## Issues

- row 2: missing answer
- row 2: invalid seconds ''
- row 3: missing answer
- row 3: invalid seconds ''
- row 4: missing answer
- row 4: invalid seconds ''
- row 5: missing answer
- row 5: invalid seconds ''
- row 6: missing answer
- row 6: invalid seconds ''
- row 7: missing answer
- row 7: invalid seconds ''
- row 8: missing answer
- row 8: invalid seconds ''
- row 9: missing answer
- row 9: invalid seconds ''
- row 10: missing answer
- row 10: invalid seconds ''
- row 11: missing answer
- row 11: invalid seconds ''
- row 12: missing answer
- row 12: invalid seconds ''
- row 13: missing answer
- row 13: invalid seconds ''
- row 14: missing answer
- row 14: invalid seconds ''
- row 15: missing answer
- row 15: invalid seconds ''
- row 16: missing answer
- row 16: invalid seconds ''
- row 17: missing answer
- row 17: invalid seconds ''
- row 18: missing answer
- row 18: invalid seconds ''
- row 19: missing answer
- row 19: invalid seconds ''
- row 20: missing answer
- row 20: invalid seconds ''
- row 21: missing answer
- row 21: invalid seconds ''
- 760 additional issue(s) omitted.

## Promotion Rule

Do not copy this scored CSV to `data/human_baseline/paper_v1.csv`
until all response rows have real answers, parseable timings, and
`make -C paper readiness` can pass after promotion.
