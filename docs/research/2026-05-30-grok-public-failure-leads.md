---
title: Grok Public Failure Leads
date: 2026-05-30
type: research
status: draft
---

# Grok Public Failure Leads

## Purpose

This note records a Grok-assisted public-source mining pass for ObviousBench.
The goal was to find public, citable leads for human-trivial LLM failures
without promoting model-generated research output directly into the canonical
benchmark corpus.

Raw outputs:

- `docs/research/2026-05-30-grok-public-failure-leads.raw.json`
- `docs/research/2026-05-30-grok-public-failure-leads.json`
- `docs/research/2026-05-30-grok-public-failure-leads-pass-2.raw.json`
- `docs/research/2026-05-30-grok-public-failure-leads-pass-2.json`

Normalized candidate catalog:

- `data/source_catalog/candidates_grok_2026-05-30.jsonl`

Prompts:

- `docs/research/2026-05-30-grok-public-failure-mining-prompt.md`
- `docs/research/2026-05-30-grok-public-failure-mining-prompt-2.md`

## Method

I ran two Grok searches using hosted web and X search:

1. A broad pass for obvious LLM failure examples.
2. A second pass excluding the already-dominant strawberry and Google
   glue/pizza/rocks clusters.

Grok was instructed to return JSON with source URL, prompt/output snippets,
task family, scorer fit, confidence, rights status, and recommended action.
I then normalized the candidates into JSONL and added a local verification
status based on whether I could independently open or search-confirm the source
on 2026-05-30.

## Results

Grok returned 11 candidate rows:

- 6 character-count leads
- 2 arithmetic leads
- 2 constraint-awareness leads
- 1 word-count lead

Verification status:

- 6 `independently_opened_2026_05_30`
- 2 `search_unconfirmed_2026_05_30`
- 1 `source_blocked_by_robots_2026_05_30`
- 1 `source_paywalled_2026_05_30`
- 1 `x_shell_opened_no_content_2026_05_30`

## Candidate Summary

| Candidate | Family | Grok action | Local status | Source |
| --- | --- | --- | --- | --- |
| `grok_20260530_openai_strawberry_r_count_2024` | character_count | include | independently opened | https://community.openai.com/t/incorrect-count-of-r-characters-in-the-word-strawberry/829618 |
| `grok_20260530_techcrunch_strawberry_tokenization_2024` | character_count | include | independently opened | https://techcrunch.com/2024/08/27/why-ai-cant-spell-strawberry/ |
| `grok_20260530_hn_strawberry_all_models_2024` | character_count | include | independently opened | https://news.ycombinator.com/item?id=41058318 |
| `grok_20260530_carry_forward_r_count` | character_count | include | independently opened | https://generativeai.pub/how-many-rs-in-carry-forward-chatgpt-claude-and-copilot-all-fail-a-simple-letter-counting-test-1d74d5719fc6 |
| `grok_20260530_9_11_vs_9_9_comparison` | arithmetic | include | independently opened | https://community.openai.com/t/why-9-11-is-larger-than-9-9-incredible/869824 |
| `grok_20260530_chatgpt_word_count_fail` | word_count | include | independently opened | https://community.openai.com/t/chatgpt-cannot-count-words-or-produce-word-count-limited-text/47380 |
| `grok_20260530_bbc_google_ai_glue_pizza_2024` | constraint_awareness | include | source blocked by robots | https://www.bbc.com/news/articles/cd11gzejgz4o |
| `grok_20260530_forbes_google_ai_glue_rocks_2024` | constraint_awareness | include | source paywalled | https://www.forbes.com/sites/jackkelly/2024/05/31/google-ai-glue-to-pizza-viral-blunders/ |
| `grok_20260530_google_ai_overview_p_in_google` | character_count | include | search unconfirmed | https://www.wionews.com/trending/after-disregard-google-ai-overview-has-a-spelling-problem-p-in-google-and-2-m-in-gemini-1779967800785 |
| `grok_20260530_ai_overview_gemini_m_count` | character_count | include | search unconfirmed | https://www.wionews.com/trending/after-disregard-google-ai-overview-has-a-spelling-problem-p-in-google-and-2-m-in-gemini-1779967800785 |
| `grok_20260530_gemini_arithmetic_fail_x` | arithmetic | reproduce_first | X shell opened, no content | https://x.com/Gdthainakub/status/2025039495767490841 |

## Promotion Guidance

Do not append these rows directly to `data/source_catalog/sources_v0.jsonl`
without review. Grok output is a research lead, not source truth.

Recommended next promotion path:

1. Promote the 6 independently opened rows into canonical source records after
   a source-policy review.
2. Treat the BBC and Forbes rows as link-only secondary sources unless a direct
   screenshot/post source is recovered.
3. Treat the WION rows as unconfirmed until the exact article is independently
   reachable or corroborated by another source.
4. Treat the X arithmetic row as `reproduce_first` unless the post content can
   be retrieved through an authenticated browser or another public mirror.
5. Add no benchmark item solely because Grok recommended `include`; every item
   still needs deterministic target/scorer review and ideally a current model
   reproduction attempt.

## Gaps

This pass still over-indexes on character counting. We still need better public
leads for:

- negation failures
- ordering/sorting failures
- exact JSON or format-compliance failures
- non-character spelling transforms
- direct public examples that are not screenshots behind a social login

The current candidate set is useful for replacing vague source placeholders
with real public leads, but it is not yet the full source-mined corpus promised
by the v0.1 plan.
