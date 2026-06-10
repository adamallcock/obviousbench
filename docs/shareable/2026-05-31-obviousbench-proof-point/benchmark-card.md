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

## Latest Comparison Snapshot

Generated on: 2026-05-31

- GPT-5 Nano minimal: 77.5% accuracy, 22.5% obvious failure rate, estimated cost $0.000897.
- GPT-4.1 none: 82.5% accuracy, 17.5% obvious failure rate, estimated cost $0.008474.
- GPT-4o none: 88.8% accuracy, 11.2% obvious failure rate, estimated cost $0.011052.
- GPT-5.2 none: 87.5% accuracy, 12.5% obvious failure rate, estimated cost $0.013134.
- GPT-5 low: 98.8% accuracy, 1.2% obvious failure rate, estimated cost $0.067441.
- GPT-5.4 none: 87.5% accuracy, 12.5% obvious failure rate, estimated cost $0.016063.
- GPT-5.4 low: 97.5% accuracy, 2.5% obvious failure rate, estimated cost $0.040587.
- GPT-5.4 medium: 97.5% accuracy, 2.5% obvious failure rate, estimated cost $0.059353.
- GPT-5.4 high: 98.8% accuracy, 1.2% obvious failure rate, estimated cost $0.071712.
- GPT-5.5 none: 91.2% accuracy, 8.8% obvious failure rate, estimated cost $0.032245.
- GPT-5.5 medium: 100.0% accuracy, 0.0% obvious failure rate, estimated cost $0.110635.
- GPT-5.5 high: 100.0% accuracy, 0.0% obvious failure rate, estimated cost $0.139195.
- Claude Haiku 4.5: 82.5% accuracy, 17.5% obvious failure rate, estimated cost $0.006536.
- Claude Sonnet 4.6: 77.5% accuracy, 22.5% obvious failure rate, estimated cost $0.021108.
- Claude Opus 4.6 low: 91.2% accuracy, 8.8% obvious failure rate, estimated cost $0.033505.
- Claude Opus 4.6 medium: 96.2% accuracy, 3.8% obvious failure rate, estimated cost $0.033880.
- Claude Opus 4.6 high: 95.0% accuracy, 5.0% obvious failure rate, estimated cost $0.044155.
- Claude Opus 4.7 low: 91.2% accuracy, 8.8% obvious failure rate, estimated cost $0.040605.
- Claude Opus 4.7 medium: 93.8% accuracy, 6.2% obvious failure rate, estimated cost $0.040605.
- Claude Opus 4.7 high: 92.5% accuracy, 7.5% obvious failure rate, estimated cost $0.040605.
- Claude Opus 4.8 low: 92.5% accuracy, 7.5% obvious failure rate, estimated cost $0.033630.
- Claude Opus 4.8 medium: 93.8% accuracy, 6.2% obvious failure rate, estimated cost $0.033630.
- Claude Opus 4.8 high: 93.8% accuracy, 6.2% obvious failure rate, estimated cost $0.033630.
- Gemini 3.1 Flash Lite OR: 81.2% accuracy, 18.8% obvious failure rate, estimated cost $0.001098.
- Gemini 3 Flash Preview OR: 87.5% accuracy, 12.5% obvious failure rate, estimated cost $0.002180.
- Gemini 3.1 Pro Preview OR: 100.0% accuracy, 0.0% obvious failure rate, estimated cost $0.182912.
- Gemini 3.5 Flash OR: 100.0% accuracy, 0.0% obvious failure rate, estimated cost $0.149019.
- Grok 4.3 xAI: 87.5% accuracy, 12.5% obvious failure rate, estimated cost $0.064638.
- Grok 4.20 xAI: 57.5% accuracy, 42.5% obvious failure rate, estimated cost $0.149072.

## Failure Hotspots

- arithmetic: 8 failures
- character_count: 86 failures
- constraint_awareness: 28 failures
- format_compliance: 5 failures
- negation: 14 failures
- ordering: 15 failures
- spelling_transform: 63 failures
- word_count: 4 failures
