---
title: ObviousBench arXiv Readiness Decision
date: 2026-06-01
type: decision-record
status: accepted
---

# ObviousBench arXiv Readiness Decision

## Decision

Do not submit an ObviousBench arXiv paper from the current `public_v0`
proof-point dataset, and do not block the first preprint on measured human
collection.

Proceed toward a faster arXiv preprint by creating a paper-specific evidence
layer:

- primary category target: `cs.CL`,
- paper split: `paper_v1`, seeded as an 80-item candidate manifest,
- paper posture: benchmark methodology and model-evaluation report,
- result claim scope: narrow tasks designed to be obvious to unassisted humans
  and scored deterministically,
- excluded claim scope: measured human performance, model-versus-human gaps,
  global model ranking, or general intelligence.

Measured human-baseline collection is deferred until the item set is frozen for
a strict benchmark version. Any future human baseline must be rerun after
substantive item, answer-key, scorer, or instruction changes.

## Rationale

The current repo has real foundations:

- Inspect AI runner.
- Local JSONL datasets.
- Deterministic scorers.
- Answer, format, and strict scoring.
- Scorer-gold fixtures.
- Cost and token reporting.
- Confidence intervals.
- Shareable model-comparison reports.

The current repo also has paper blockers:

- `public_v0` is documented as generated seed data suitable for proof points,
  not as a durable leaderboard split.
- Item cards are present but still draft placeholders.
- The `paper_v1` split manifest is only a candidate seeded from the
  hard-obvious panel; item cards, answer derivations, ambiguity notes,
  scorer-gold coverage, and final model artifacts still need to make it
  paper-ready.
- Public-only examples are contamination-prone.

arXiv moderation is not peer review, but the paper still needs to read as a
scholarly benchmark report. The current artifacts are strong enough to justify
continued investment, but not strong enough to freeze as paper evidence.
Removing human collection from v1 is acceptable only if the manuscript removes
empirical human-performance language and treats "human-trivial" as a design
target supported by review artifacts.

## Accepted Paper Claims

These claims are allowed once `paper_v1` exists and passes the preprint
readiness audit:

- ObviousBench targets a narrow class of short, objectively scored tasks
  designed to be trivial for careful unassisted humans.
- Deterministic scorer contracts can separate answer correctness, format
  compliance, and strict correctness.
- Frontier and production-relevant models can still make visible mistakes on
  selected obvious tasks.
- Failure rates differ by task family.
- Cost and token burden differ materially across models even on short tasks.
- A live or private refresh is needed for leaderboard-grade claims.

## Disallowed Paper Claims

These claims should not appear in the paper:

- ObviousBench measures general intelligence.
- ObviousBench proves one model is globally best.
- `public_v0` results are contamination-resistant.
- Generated seed data alone supports public leaderboard claims.
- A model failure on ObviousBench proves a specific internal reasoning defect.
- The benchmark is comprehensive across factuality, safety, tool use,
  long-context behavior, RAG, or agents.
- Humans achieve a specific accuracy or response-time distribution on
  `paper_v1`.
- ObviousBench measures a quantified gap between humans and models.

## Evidence Gate

The fast-preprint paper can move from planning to drafting when all of these
pass:

- `make -C paper readiness-preprint` passes for the paper dataset.
- The paper split manifest exists at `data/splits/paper_v1_manifest.jsonl`.
- Each `paper_v1` item has a reviewed item card with no placeholder text.
- Each used scorer has at least 20 scorer-gold examples.
- The model sweep has exact model aliases, run dates, run parameters, and
  provider-error handling.
- Results include answer accuracy, format accuracy, strict accuracy,
  confidence intervals, cost, tokens, and sample counts.
- The manuscript contains no measured human-baseline claims, no human response
  time claims, and no model-versus-human claims.

The strict benchmark gate remains available later. It additionally requires
`data/human_baseline/paper_v1.csv`, collection/scoring/threshold audits, and
predeclared human-triviality thresholds before any empirical human claims.

## Immediate Work Packages

### 1. Paper Split Manifest

Status: seeded.

`data/splits/paper_v1_manifest.jsonl` now contains a small first subset rather
than all 401 items:

- 80 items total.
- 10 items from each of 8 families.
- Seeded from the existing `hard_obvious_8x10` panel.
- Exclude items whose answer derivation is hard to explain cleanly.
- Include only items that can be reviewed without external private evidence.

### 2. Item-Card Review

Review only the selected `paper_v1` items first.

Each reviewed card must include:

- source summary,
- answer derivation,
- ambiguity notes,
- scorer contract,
- split-policy rationale,
- reviewer and review date,
- no `TODO(review)` placeholders.

### 3. Human Baseline

Status: deferred for the fast preprint.

Do not collect the measured baseline until the exact item set, instructions,
answer key, and scorers are frozen. The current participant packets and scoring
helpers remain useful future infrastructure, but they are not blockers for the
v1 preprint.

If the strict path is chosen later, create
`data/human_baseline/paper_v1.csv` with this minimal schema:

```text
item_id,participant_id,answer,seconds,correct,notes
```

Target protocol:

- 5 to 10 participants.
- No external tools.
- Answer-only interface.
- Capture response time.
- Predefine the H0 threshold before looking at model comparisons.

### 4. Paper Sweep

After the preprint readiness audit passes:

- run a frozen model panel,
- summarize logs,
- build comparison reports,
- build figures and tables,
- freeze claim text.

## Consequences

This decision speeds the first arXiv draft while narrowing its claim surface.
It prevents the paper from wasting a human collection pass on a moving
benchmark split, and it avoids pretending that a small unfrozen baseline can
carry more evidential weight than it really has.

The next milestone is a passing `make -C paper readiness-preprint` audit for a
small reviewed `paper_v1` split, followed by an explicitly approved final
model sweep. The strict human-baselined version remains a future validation or
revision path.
