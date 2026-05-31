---
title: ObviousBench Shareable Benchmark Card
date: 2026-05-31
type: benchmark-card
status: shareable
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

Current local dataset version: `public_v0`, generated on 2026-05-30.

The current `public_v0` dataset is generated seed data inspired by source
archetypes. It is suitable for a proof point, not a public leaderboard claim.

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
- Semantic constraint-awareness items require stricter human review than character-counting items.
- Small-panel results are useful conversation evidence, not a statistically
  representative benchmark of all model behavior.

## Latest Comparison Snapshot

Generated on: 2026-05-31

- gpt-4.1: 80.0% accuracy, 20.0% obvious failure rate, estimated cost $0.008474.
- gpt-4o: 73.8% accuracy, 26.2% obvious failure rate, estimated cost $0.011052.
- gpt-5.5 none: 91.2% accuracy, 8.8% obvious failure rate, estimated cost $0.032245.

## Failure Hotspots

- character_count: 13 failures
- constraint_awareness: 14 failures
- format_compliance: 3 failures
- negation: 7 failures
- spelling_transform: 7 failures
