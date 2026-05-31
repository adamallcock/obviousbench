---
title: Underrepresented Archetype Expansions
date: 2026-05-30
type: research
status: draft
---

# Underrepresented Archetype Expansions

## Purpose

This pass adds source-archetype mining and generated expansions outside the
already crowded Google AI Overview spelling/counting and strawberry clusters.

The target was "another 50 or so" items by finding example types and expanding
each type into five similar generated variants.

## Artifacts

Source-archetype prompts and raw outputs:

- `docs/research/2026-05-30-grok-underrepresented-archetype-mining-prompt.md`
- `docs/research/2026-05-30-grok-underrepresented-archetype-leads.raw.json`
- `docs/research/2026-05-30-grok-underrepresented-archetype-leads.json`
- `docs/research/2026-05-30-grok-underrepresented-archetype-mining-prompt-2.md`
- `docs/research/2026-05-30-grok-underrepresented-archetype-leads-pass-2.raw.json`
- `docs/research/2026-05-30-grok-underrepresented-archetype-leads-pass-2.json`
- `docs/research/2026-05-30-openrouter-underrepresented-archetype-mining-prompt.md`
- `docs/research/2026-05-30-openrouter-underrepresented-archetype-leads.raw.json`
- `docs/research/2026-05-30-openrouter-underrepresented-archetype-leads-retry.raw.json`
- `docs/research/2026-05-30-openrouter-underrepresented-archetype-leads-narrow.raw.json`
- `docs/research/2026-05-30-openrouter-underrepresented-archetype-leads-deepseek-free.raw.json`

Normalized source candidates:

- `data/source_catalog/candidates_underrepresented_2026-05-30.jsonl`

Generated expansion items:

- `scripts/generate_underrepresented_expansions.py`
- `data/public_v0/archetype_expansions_2026-05-30.jsonl`

## Method

1. Ran two Grok passes for non-Google, non-strawberry archetypes.
2. Asked each pass for source-backed archetypes with five synthetic expansion
   ideas.
3. Ran OpenRouter with web tools as an independent pass, per request.
4. OpenRouter hosted tools failed and fell back to local tools; the default free
   Nemotron model returned unusable tool-call-shaped or empty output. A second
   free-model attempt with `deepseek/deepseek-chat-v3-0324:free` returned a 404
   from OpenRouter. These attempts are preserved as raw artifacts.
5. Normalized the 10 usable Grok archetypes into source-candidate JSONL.
6. Generated exactly five variants for each archetype using a reproducible
   script.

## Selected Archetypes

| Source candidate | Family used | Subfamily used | Generated rows |
| --- | --- | --- | --- |
| `grok_underrep_20260530_githubnext_gpt4_calc` | arithmetic | unit_conversion_and_small_calc | 5 |
| `grok_underrep_20260530_reddit_sort_numbers` | ordering | numeric_sort | 5 |
| `grok_underrep_20260530_linkedin_alphabetize_words` | ordering | alphabetical_sort | 5 |
| `grok_underrep_20260530_reddit_reverse_words` | spelling_transform | reverse_word | 5 |
| `grok_underrep_20260530_quanta_negation` | negation | not_choice | 5 |
| `grok_underrep_20260530_local_llama_json_break` | format_compliance | exact_json_schema | 5 |
| `grok_underrep_20260530_claude_word_count_fail` | word_count | sentence_word_count | 5 |
| `grok_underrep_20260530_conflicting_instructions_blog` | format_compliance | instruction_conflict | 5 |
| `grok_underrep_20260530_ai_negation_struggle` | negation | without_constraint | 5 |
| `grok_underrep_20260530_chatgpt_wordcount_community` | word_count | comma_list_count | 5 |

## Generated Distribution

Total generated rows: 50.

By family:

```text
arithmetic: 5
format_compliance: 10
negation: 10
ordering: 10
spelling_transform: 5
word_count: 10
```

These rows are generated variants, not public examples. Their `source_refs`
point to source-candidate archetypes and their `metadata.variant_of` field
records the source candidate used for expansion.

## Verification

Commands run on 2026-05-30:

```bash
.venv/bin/python scripts/generate_underrepresented_expansions.py
.venv/bin/python scripts/validate_dataset.py data/public_v0/*.jsonl data/calibration_v0/smoke_test.jsonl
```

Observed:

```text
wrote 50 items to data/public_v0/archetype_expansions_2026-05-30.jsonl
Validation passed.
```

Source candidate schema parsing also passed for:

```text
10 candidates in candidates_underrepresented_2026-05-30.jsonl
12 candidates in candidates_google_search_2026-05-30.jsonl
11 candidates in candidates_grok_2026-05-30.jsonl
```

## Caveats

- Several source candidates are social/forum leads and remain unverified beyond
  Grok's citation output.
- OpenRouter did not produce usable mined candidates in this run despite being
  given search tools.
- The 50 new benchmark rows are deliberately artificial expansions. They should
  not be described as 50 newly mined public failures.
- The expansion file is separate from the family JSONL files so it can be
  reviewed, promoted, or removed independently.
