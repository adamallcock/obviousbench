---
title: Paper V1 Human Baseline Collection Audit
date: 2026-06-01
type: research
status: blocked
---

# Paper V1 Human Baseline Collection Audit

This audit checks collection completeness before scorer-based grading.
It does not create participant data, score answers, or run model providers.

Overall status: BLOCKED

- Assignments: `data/human_baseline/paper_v1_assignments.csv`
- Responses: `data/human_baseline/paper_v1_response_template.csv`
- Answer key: `data/human_baseline/paper_v1_answer_key.csv`
- Expected response rows: 400
- Response rows present: 400
- Completed answer+timing rows: 0
- Participants: 5
- Items: 80
- Missing response rows: 0
- Missing answers: 400
- Invalid timings: 400
- Duplicate assignment rows: 0
- Duplicate response rows: 0
- Unknown response rows: 0
- Structural issues: 0
- Ready for scoring: no

## Participant Progress

| Participant | Expected | Present | Complete | Missing response | Missing answer | Invalid seconds |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| p01 | 80 | 80 | 0 | 0 | 80 | 80 |
| p02 | 80 | 80 | 0 | 0 | 80 | 80 |
| p03 | 80 | 80 | 0 | 0 | 80 | 80 |
| p04 | 80 | 80 | 0 | 0 | 80 | 80 |
| p05 | 80 | 80 | 0 | 0 | 80 | 80 |

## Family Progress

| Family | Expected | Complete | Missing answer | Invalid seconds |
| --- | ---: | ---: | ---: | ---: |
| arithmetic | 50 | 0 | 50 | 50 |
| character_count | 50 | 0 | 50 | 50 |
| constraint_awareness | 50 | 0 | 50 | 50 |
| format_compliance | 50 | 0 | 50 | 50 |
| negation | 50 | 0 | 50 | 50 |
| ordering | 50 | 0 | 50 | 50 |
| spelling_transform | 50 | 0 | 50 | 50 |
| word_count | 50 | 0 | 50 | 50 |

## Next Step Rule

Run scoring only after this audit passes. After scoring, run the
threshold audit and promote checked rows to
`data/human_baseline/paper_v1.csv` only when readiness can pass.
