---
title: ObviousBench Pro Consult Context
date: 2026-06-07
type: brief
status: draft
---

# ObviousBench Pro Consult Context

This packet is for a ChatGPT Pro consultation on the ObviousBench launch essay.
The goal is not fact verification of model results. Detailed result files are
intentionally omitted from this consult. Treat result-specific claims in the
draft as placeholders or locally verified claims that will be checked in a
later pass.

## Consult Ask

Please critique the attached first-pass essay and project context. Recommend:

1. the strongest positioning for the launch essay;
2. better tagline/naming language than "obvious mistakes" if appropriate;
3. what the essay should include or remove;
4. where the tone risks sounding like model shaming rather than reliability
   preflight;
5. how to explain public/private split limitations without losing readers;
6. what claims should stay in the paper versus the essay;
7. a suggested outline for the next essay revision;
8. specific line-level or paragraph-level edits where useful.

Be critical and practical. The audience is AI builders, model/product teams,
researchers, and technical readers on X/Twitter who may click through to the
website/GitHub repo.

## Project Summary

ObviousBench is a benchmark for short, high-visibility language-model failures:
letter counting, spelling transforms, small arithmetic, ordering, negation,
format compliance, word counting, and simple constraint awareness.

The original tagline was:

> Catch obvious AI mistakes before users do.

The working concern is that "obvious" may be the wrong center of gravity. The
real product risk may be better described as embarrassment exposure,
high-visibility failure, user-visible brittleness, or mistakes users can
recognize immediately.

The benchmark is intentionally narrow:

- single-turn prompts;
- objective expected answers;
- deterministic Python scorers;
- no LLM-as-judge scoring for primary results;
- answer correctness separated from format correctness;
- public examples treated as source leads, not ground truth.

The desired launch path is website + GitHub + static report + launch essay /
X thread first, with arXiv later as a scholarly anchor.

## Current Data/Split Sanity

Current local data counts:

| Surface | Count | Meaning |
| --- | ---: | --- |
| `data/public_v0/*.jsonl` | 401 | reviewed unique public items |
| `data/splits/paper_v1_manifest.jsonl` | 80 | current manifest file, 10 per family |
| `data/barrages/hard_obvious_8x28_seed_20260531.jsonl` | 224 | release-run question set, 28 per family |
| release comparison | 223 rows | model/settings rows in the current local evidence snapshot |

Important caveat: the release copy currently speaks about a 224-question
snapshot, but the checked `paper_v1_manifest` file still contains 80 items.
Before public launch, the repo should either promote the 224-item barrage into
the actual paper/release manifest or avoid saying that the `paper_v1_manifest`
itself contains 224 questions.

Family counts in the full reviewed public corpus:

| Family | Public items | In 80-item manifest | Unused after 80-item manifest |
| --- | ---: | ---: | ---: |
| character_count | 76 | 10 | 66 |
| word_count | 70 | 10 | 60 |
| ordering | 55 | 10 | 45 |
| format_compliance | 55 | 10 | 45 |
| constraint_awareness | 48 | 10 | 38 |
| negation | 35 | 10 | 25 |
| spelling_transform | 34 | 10 | 24 |
| arithmetic | 28 | 10 | 18 |

There does not appear to be a true private split on disk. A private split could
be created, but to be contamination-resistant it should not be published in the
public GitHub/Hugging Face release.

## Result Handling For This Consult

Do not rely on detailed result claims in the draft. They are included for shape,
but the consultant should focus on essay structure, positioning, claim hygiene,
and reader trust.

Placeholders allowed:

- `[RESULT: headline score distribution]`
- `[RESULT: hardest task families]`
- `[RESULT: thinking/cost tradeoff]`
- `[RESULT: example visible failure]`

## Files Sent With This Consult

Primary writing files:

- `docs/release/2026-06-07-obviousbench-launch-essay-first-pass.md`
- `docs/release/2026-06-07-obviousbench-launch-essay-working-draft.md`
- `docs/release/2026-06-07-obviousbench-pro-consult-context.md`

Project context files:

- `README.md`
- `docs/branding.md`
- `docs/benchmark_card.md`
- `docs/methodology.md`
- `docs/scoring_policy.md`
- `docs/source_policy.md`
- `docs/prompt_policy.md`
- `paper/sections/01_introduction.tex`
- `paper/sections/03_benchmark.tex`
- `paper/sections/04_data_review.tex`
- `paper/sections/05_scoring_protocol.tex`
- `paper/sections/08_discussion.tex`
- `paper/sections/09_limitations_ethics_reproducibility.tex`
