---
title: ObviousBench Benchmark Card
date: 2026-05-31
type: reference
status: current
---

# ObviousBench Benchmark Card

ObviousBench is a lightweight reliability benchmark for public-facing AI
systems. It focuses on short questions where the expected answer is obvious to
a person and embarrassing when a model misses it.

## What This Measures

ObviousBench measures short, human-trivial tasks that are reputationally visible
when failed: character counting, spelling transforms, simple arithmetic,
word/list counting, ordering, format compliance, negation, and simple constraint
awareness.

## What This Does Not Measure

It does not measure general intelligence, safety, factuality, RAG quality, tool
use, long-context ability, expert knowledge, or multi-turn agent behavior.

## Dataset Version

Current local dataset version: `public_v0`, with generated seed data and
metadata updates through 2026-05-31.

Current local `public_v0` composition:

- 401 total items.
- 399 generated variants.
- 2 public archetype items.
- 8 task families.
- 3 items with metamorphic group metadata.

The current `public_v0` dataset is generated seed data inspired by source
archetypes. It is suitable for a proof point, not a public leaderboard claim.

Any current or future claim must name the exact split and data vintage used.
Until stronger held-out or live splits are implemented and documented,
`public_v0` results should be described as proof-point seed-data evidence only.

## Runner

Inspect AI with local JSONL datasets, native provider model calls, no explicit
system prompt, and deterministic Python scorers.

## Shareable Proof Point

The promoted snapshot uses an 80-sample balanced barrage with 10 samples from
each of 8 task families. The tracked shareable bundle contains:

- `benchmark-card.md` for scope, headline metrics, and caveats.
- `failure-gallery.md` for readable examples of observed misses.
- `model-comparison.csv` and `family-comparison.csv` for compact metrics.
- `model-matrix.yaml` for exact Inspect model strings.

Raw Inspect logs and provider payloads remain local and ignored by git.

## Known Risks

- Famous prompts may be contaminated.
- Generated variants are only as good as their review process.
- Public seed data can be inspected and copied, so public-only results should
  not be presented as leaderboard-grade held-out evidence.
- Semantic constraint-awareness items require stricter human review than character-counting items.
- Small-panel results are useful conversation evidence, not a statistically
  representative benchmark of all model behavior.
