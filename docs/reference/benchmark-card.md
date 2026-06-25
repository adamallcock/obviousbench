---
title: ObviousBench Benchmark Card
date: 2026-06-18
type: reference
status: current
---

# ObviousBench Benchmark Card

ObviousBench is a lightweight reliability benchmark for public-facing AI
systems. It focuses on short questions where the expected answer is obvious to
a person and embarrassing when a model misses it.

The current intended publication-prep snapshot is v0.2. The private v0.2
headline evidence is aggregate-only: 144 held-out items, 293 complete
model/config rows, 126,576 scored attempts, and non-strict answer pass^3 as the
primary metric. Private prompts, raw private completions, provider logs,
item-level private outcomes, and private review HTML remain out of public
materials.

## What This Measures

ObviousBench measures short, human-trivial tasks that are reputationally visible
when failed: character counting, spelling transforms, simple arithmetic,
word/list counting, ordering, format compliance, negation, and simple constraint
awareness.

## What This Does Not Measure

It does not measure general intelligence, safety, factuality, RAG quality, tool
use, long-context ability, expert knowledge, or multi-turn agent behavior.

## Current Evidence Version

Current intended publication-prep version: `v0.2`.

Current private evidence shape:

- 144 private held-out items.
- 293 complete model/config rows.
- 126,576 attempted item/config/pass cells.
- 126,576 scored attempts.
- Estimated measured run cost: about $131.00.
- Primary headline metric: non-strict answer pass^3.

The strongest v0.2 model/config rows saturate or near-saturate the benchmark.
That is a positive signal: the questions are solvable with enough capability or
test-time compute. The benchmark signal is the spread below that ceiling, where
smaller, cheaper, no-thinking, or lower-compute rows still make visible obvious
mistakes.

Public examples remain a transparency and demo surface. Public examples alone
should not be treated as leaderboard-grade held-out evidence. Any public claim
must name the exact split, evidence vintage, metric, and public/private boundary.

## Runner

Inspect AI with local JSONL datasets, native provider model calls, no explicit
system prompt, and deterministic Python scorers.

## Shareable Proof Point

The shareable public surface is aggregate-only. It contains:

- [https://obviousbench.com](https://obviousbench.com) for the canonical public
  narrative and interactive charts.
- `data/public_examples/` for public example questions and contributor
  orientation.
- `configs/model_panels/models_v0_2_public.yaml` for the public v0.2
  model/config panel.
- `reports/v0_2/aggregate/summary.csv` for the public-safe aggregate result
  table.
- `reports/v0_2/aggregate/report.md` for the public-safe aggregate evidence
  summary.
- `docs/release/v0_2/generated/` for generated release notes, metadata, and
  dataset-card drafts.

Raw Inspect logs and provider payloads remain local and ignored by git.

## Known Risks

- Famous prompts may be contaminated.
- Generated variants are only as good as their review process.
- Public seed data can be inspected and copied, so public-only results should
  not be presented as leaderboard-grade held-out evidence.
- Semantic constraint-awareness items require stricter human review than character-counting items.
- Small-panel results are useful conversation evidence, not a statistically
  representative benchmark of all model behavior.
- v0.2 should not be described as a global model ranking, a measured human
  baseline, or a permanent statement about provider behavior.
