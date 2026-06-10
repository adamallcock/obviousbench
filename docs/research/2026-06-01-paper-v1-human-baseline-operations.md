---
title: Paper V1 Human Baseline Operations Packet
date: 2026-06-01
type: runbook
status: blocked
---

# Paper V1 Human Baseline Operations Packet

This packet coordinates the collection, audit, scoring, thresholding,
promotion, and readiness gates for the paper human baseline. It does
not create participant data, score blank rows, run providers, or
authorize final model arrays.

Overall status: BLOCKED

Summary: 1 passed, 5 blocked.

## Operation Matrix

| Step | Status | Evidence | Next action |
| --- | --- | --- | --- |
| collection packet | PASS | 5 participant(s); 400 response row(s). | None. |
| response collection | BLOCKED | 0/400 answer+timing rows complete; 400 missing answer(s); 400 invalid timing(s). | Collect real answers and non-negative elapsed seconds in `data/human_baseline/paper_v1_response_template.csv`, then rerun `make -C paper human-baseline-audit`. |
| scoring | BLOCKED | 0/400 rows scored; 800 issue(s). | Run `make -C paper human-baseline-score` only after collection audit passes. |
| threshold classification | BLOCKED | 0 core H0 item(s); 80 no-data item(s); 400 ignored scored row(s). | Run `make -C paper human-baseline-thresholds` after scoring passes and use only `core_h0` items for headline claims. |
| paper readiness | BLOCKED | Readiness audit is not passing; current blocker is human-baseline evidence. | Promote only audited scored rows to `data/human_baseline/paper_v1.csv`, then rerun `make -C paper readiness`. |
| promotion target | BLOCKED | data/human_baseline/paper_v1.csv has 0 response row(s). | Copy checked scored baseline rows into `data/human_baseline/paper_v1.csv` only after collection, scoring, and threshold audits pass. |

## Command Ladder

```bash
make -C paper human-baseline-packet
make -C paper human-baseline-audit
# Fill every answer and seconds field in the response template.
make -C paper human-baseline-audit
make -C paper human-baseline-score
make -C paper human-baseline-thresholds
# Promote checked rows to data/human_baseline/paper_v1.csv only after audits pass.
make -C paper assets
make -C paper readiness
make -C paper sweep-plan
```

## Stop Rules

- Do not show `data/human_baseline/paper_v1_answer_key.csv` to participants.
- Do not store participant names, emails, demographics, payment details, or notes outside pseudonymous IDs.
- Do not run final model arrays until `make -C paper readiness` passes and the sweep handoff says `Run allowed: YES`.
