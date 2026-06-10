---
title: Paper V1 Human Baseline Collection Packet
date: 2026-06-01
type: research
status: ready
---

# Paper V1 Human Baseline Collection Packet

This packet prepares human-baseline collection for the paper split. It
does not contain real participant responses and does not make model
provider calls.

Overall status: PASS

- Participants: 5
- Paper items: 80
- Assignment rows: 400
- Preallocated response rows: 400
- Assignments per item: 5 to 5
- Randomization seed: 20260601

## Generated Files

- Assignment CSV: `data/human_baseline/paper_v1_assignments.csv`
- Response template CSV: `data/human_baseline/paper_v1_response_template.csv`
- Local answer key CSV: `data/human_baseline/paper_v1_answer_key.csv`
- Participant packets: `docs/research/2026-06-01-paper-v1-human-baseline-participant-packets.md`

The assignment CSV and participant packets are participant-facing and do
not include targets. The answer key is local scoring material and should
not be shown to participants.

## Family Coverage

| Family | Items | Assignment rows |
| --- | ---: | ---: |
| `arithmetic` | 10 | 50 |
| `character_count` | 10 | 50 |
| `constraint_awareness` | 10 | 50 |
| `format_compliance` | 10 | 50 |
| `negation` | 10 | 50 |
| `ordering` | 10 | 50 |
| `spelling_transform` | 10 | 50 |
| `word_count` | 10 | 50 |

## Collection Procedure

1. Give each participant only their section from the participant packet.
2. Record answer text and elapsed seconds for every assigned item.
3. Copy completed rows into `data/human_baseline/paper_v1.csv`.
4. Score `correct` with the target/scorer contract and item cards.
5. Run `make -C paper readiness` before any final model sweep.

## Privacy Boundary

Use pseudonymous participant IDs only. Do not store participant names,
emails, demographics, payment details, or other personal data in the
paper baseline files.
