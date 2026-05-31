# ObviousBench Benchmark Card

## What This Measures

ObviousBench measures short, human-trivial tasks that are reputationally visible when failed: character counting, spelling transforms, simple arithmetic, word/list counting, ordering, format compliance, negation, and simple constraint awareness.

## What This Does Not Measure

It does not measure general intelligence, safety, factuality, RAG quality, tool use, long-context ability, expert knowledge, or multi-turn agent behavior.

## Dataset Version

Current local dataset version: `public_v0`, generated on 2026-05-30.

## Runner

Inspect AI with local JSONL datasets and deterministic Python scorers.

## Known Risks

- Famous prompts may be contaminated.
- Generated variants are only as good as their review process.
- Semantic constraint-awareness items require stricter human review than character-counting items.

