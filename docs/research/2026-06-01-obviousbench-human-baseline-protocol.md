---
title: ObviousBench Human Baseline Protocol
date: 2026-06-01
type: protocol
status: draft
---

# ObviousBench Human Baseline Protocol

## Purpose

The arXiv paper should not call items "human-trivial" only because they look
easy to the authors. The `paper_v1` split needs a small human baseline that
shows ordinary humans can answer the selected items accurately and quickly.

This protocol is intentionally lightweight. It is meant to support a narrow
benchmark paper, not a psychometrics study.

## Target File

Store collected rows at:

```text
data/human_baseline/paper_v1.csv
```

Generate the collection packet before recruiting participants:

```bash
make -C paper human-baseline-packet
```

This writes randomized participant assignments, participant-facing prompt
packets, a response-template CSV, and a separate local answer key. The
participant-facing assets intentionally exclude targets and item-card
derivations.

While participant rows are being filled in, audit collection completeness with:

```bash
make -C paper human-baseline-audit
```

This writes
`docs/research/2026-06-01-paper-v1-human-baseline-collection-audit.md`. It
checks participant progress, item coverage, missing answers, invalid timings,
duplicate rows, and unknown response rows before scoring. The current empty
template should remain blocked here until every preallocated row has a real
answer and parseable timing.

After participant rows are filled in, score the response template with:

```bash
make -C paper human-baseline-score
```

This writes `data/human_baseline/paper_v1_scored_draft.csv` and
`docs/research/2026-06-01-paper-v1-human-baseline-scoring-report.md`. Do not
promote the draft scored file to `data/human_baseline/paper_v1.csv` until every
row has a real answer, parseable timing, and the readiness gate can pass.

Then audit item-level thresholds with:

```bash
make -C paper human-baseline-thresholds
```

This writes `data/human_baseline/paper_v1_threshold_items.csv`,
`data/human_baseline/paper_v1_threshold_families.csv`, and
`docs/research/2026-06-01-paper-v1-human-baseline-threshold-audit.md`. The
threshold audit classifies items as `core_h0`, `borderline`, `exclude`, or
`no_data`. It does not create participant responses and should stay blocked
until real scored rows are available.

Required CSV header:

```text
item_id,participant_id,answer,seconds,correct,notes
```

Field meanings:

- `item_id`: exact ID from `data/splits/paper_v1_manifest.jsonl`.
- `participant_id`: pseudonymous local participant ID such as `p01`.
- `answer`: participant answer as typed.
- `seconds`: elapsed seconds for the item.
- `correct`: `true` or `false`, scored by deterministic target comparison or
  manual adjudication using the item card.
- `notes`: optional ambiguity, typo, or skipped-item notes.

Do not store participant names, emails, demographic details, or other personal
data in this file.

## Participant Target

Minimum useful baseline:

- 5 participants.
- 80 `paper_v1` items.
- 400 response rows total.

Stronger baseline:

- 10 participants.
- 80 `paper_v1` items.
- 800 response rows total.

## Collection Rules

- No external tools.
- No search.
- No calculator unless the item explicitly permits it.
- Show the original prompt or question text.
- Ask for answer only.
- Randomize item order per participant if practical.
- Capture response time per item.
- Let participants skip unclear items; record skipped answers as incorrect with
  a note.

## Scoring Rules

For exact-answer families, score with the same target/scorer contract used by
ObviousBench where practical.

For multiple-choice families, score the chosen letter against the target.

For any manual adjudication, use the item card's answer derivation and
ambiguity notes. If the item card does not make scoring obvious, the item is not
paper-ready.

## Human-Triviality Threshold

Predefine the threshold before looking at model results:

- Core H0 item: at least 95% human accuracy and median response time below 10
  seconds.
- Borderline item: 80% to 95% human accuracy or median response time from 10 to
  30 seconds.
- Exclude from core paper split: below 80% human accuracy, median response time
  above 30 seconds, or repeated participant confusion notes.

The paper can still discuss excluded or borderline items in an appendix, but
headline claims should use the core H0 set.

The threshold helper enforces this policy mechanically after scoring. Its
default mode writes blocked outputs without returning a failing process status,
so it can be included in cheap paper rebuilds before real participant data is
available. Use its `--strict` flag only when the collection is expected to be
complete.

## Audit Gate

The readiness gate requires the baseline file to exist, use the required
columns, contain real response rows, use parseable timings and boolean
correctness, include at least 5 participants by default, and cover every paper
manifest item:

```bash
make -C paper readiness
```
