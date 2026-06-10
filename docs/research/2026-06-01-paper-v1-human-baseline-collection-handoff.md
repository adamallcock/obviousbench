---
title: Paper V1 Human Baseline Collection Handoff
date: 2026-06-01
type: runbook
status: blocked
---

# Paper V1 Human Baseline Collection Handoff

This generated handoff is the operator runbook for collecting the real
human-baseline answer and timing rows. It does not create participant
data, reveal answer keys to participants, score responses, or run model
providers.

Overall status: BLOCKED

- Participants: 5
- Assignment rows: 400
- Response rows: 400
- Completed answer+timing rows: 0
- Missing answers: 400
- Invalid seconds: 400
- Collection packet ready: yes
- Participant packets present: yes
- Local answer key present: yes

## Files

- Participant packets: `docs/research/2026-06-01-paper-v1-human-baseline-participant-packets.md`
- Assignment CSV: `data/human_baseline/paper_v1_assignments.csv`
- Response template CSV: `data/human_baseline/paper_v1_response_template.csv`
- Local answer key: `data/human_baseline/paper_v1_answer_key.csv`
- Collection audit: `docs/research/2026-06-01-paper-v1-human-baseline-collection-audit.md`

Only participant packets and assignment rows are participant-facing. The
answer key is local scoring material and must not be shown to
participants.

## Participant Progress

| Participant | Expected rows | Present rows | Complete rows | Missing answers | Invalid seconds |
| --- | ---: | ---: | ---: | ---: | ---: |
| `p01` | 80 | 80 | 0 | 80 | 80 |
| `p02` | 80 | 80 | 0 | 80 | 80 |
| `p03` | 80 | 80 | 0 | 80 | 80 |
| `p04` | 80 | 80 | 0 | 80 | 80 |
| `p05` | 80 | 80 | 0 | 80 | 80 |

## Operator Checklist

- [ ] Assign one pseudonymous participant ID per participant.
- [ ] Give each participant only their own packet section.
- [ ] Confirm participants answer without search, calculators, model
      assistance, or external tools.
- [ ] Time each item or have participants record elapsed seconds per item.
- [ ] Enter answer text exactly as given into the response template.
- [ ] Enter non-negative elapsed seconds for every row.
- [ ] Leave `correct` blank until scorer-based grading is run.
- [ ] Store no names, emails, demographics, payment details, or free-form
      personal data in repository files.
- [ ] Rerun `make -C paper human-baseline-audit` after every collection
      batch.

## Participant Instructions

Use this neutral instruction block when distributing each packet:

```text
Please answer each item without search, calculators, AI/model help, or
other external tools. Answer as quickly and accurately as you can.
Record the elapsed seconds for each item. If an item is unclear, enter
your best answer or leave it blank; skipped or blank items are treated
as incorrect for the baseline.
```

## Completion Contract

The collection stage is ready for scoring only when:

- every preallocated response row is present,
- every `answer` cell is non-empty,
- every `seconds` cell is parseable and non-negative,
- each participant has the expected number of complete rows,
- the collection audit reports `Ready for scoring: yes`.

## Command Ladder

```bash
make -C paper human-baseline-packet
make -C paper human-baseline-collection-handoff
# Fill answer and seconds cells in data/human_baseline/paper_v1_response_template.csv
make -C paper human-baseline-audit
make -C paper human-baseline-score
make -C paper human-baseline-thresholds
make -C paper human-baseline-ops
```

## Stop Rules

- Do not show `data/human_baseline/paper_v1_answer_key.csv` to participants.
- Do not infer missing answers or timings.
- Do not mark `correct` by hand before the scoring helper runs.
- Do not promote rows to `data/human_baseline/paper_v1.csv` until
  collection, scoring, and threshold audits are reviewed.
- Do not run final model arrays while this handoff is blocked.
