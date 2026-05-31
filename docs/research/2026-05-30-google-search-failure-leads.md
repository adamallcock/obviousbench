---
title: Google Search Failure Leads
date: 2026-05-30
type: research
status: draft
---

# Google Search Failure Leads

## Purpose

This note records a focused public-source mining pass for Google Search AI
failures, especially AI Overviews and AI Mode after Google I/O 2026 Search
upgrades.

Artifacts:

- `docs/research/2026-05-30-grok-google-search-failure-mining-prompt.md`
- `docs/research/2026-05-30-grok-google-search-failure-leads.raw.json`
- `docs/research/2026-05-30-grok-google-search-failure-leads.json`
- `data/source_catalog/candidates_google_search_2026-05-30.jsonl`

## Method

I ran a structured Grok web/X search for Google Search AI failures, then
spot-checked and supplemented the results with direct web verification on
2026-05-30.

The resulting JSONL file keeps these leads separate from the canonical source
catalog. They should be reviewed before promotion into `sources_v0.jsonl` or
conversion into benchmark items.

## Results

The pass produced 12 Google Search-specific candidate rows.

By surface:

- 11 AI Overview candidates
- 1 AI Mode candidate

By task family:

- 8 character-count candidates
- 2 constraint-awareness/query-intent candidates
- 1 ordering/spell-out candidate
- 1 factuality/date candidate

By verification status:

- 10 independently opened on 2026-05-30
- 1 source-open failed
- 1 social/login-gated unverified

## Candidate Summary

| Candidate | Surface | Family | Local status | Source |
| --- | --- | --- | --- | --- |
| `grok_google_20260530_indiatoday_google_ps_2026` | AI Overview | character_count | independently opened | https://www.indiatoday.in/technology/news/story/google-ai-cannot-spell-google-it-is-not-a-joke-2918502-2026-05-28 |
| `grok_google_20260530_indiatoday_gemini_ms_2026` | AI Overview | character_count | independently opened | https://www.indiatoday.in/technology/news/story/google-ai-cannot-spell-google-it-is-not-a-joke-2918502-2026-05-28 |
| `grok_google_20260530_indiatoday_journalism_ds_2026` | AI Overview | character_count | independently opened | https://www.indiatoday.in/technology/news/story/google-ai-cannot-spell-google-it-is-not-a-joke-2918502-2026-05-28 |
| `web_google_20260530_techcrunch_google_p_count` | AI Overview | character_count | independently opened | https://techcrunch.com/2026/05/27/why-googles-ai-cant-spell-google-or-anything-else/ |
| `web_google_20260530_techcrunch_poop_r_count` | AI Overview | character_count | independently opened | https://techcrunch.com/2026/05/27/why-googles-ai-cant-spell-google-or-anything-else/ |
| `web_google_20260530_techcrunch_journalism_d_count` | AI Overview | character_count | independently opened | https://techcrunch.com/2026/05/27/why-googles-ai-cant-spell-google-or-anything-else/ |
| `web_google_20260530_techcrunch_trump_p_position` | AI Overview | ordering | independently opened | https://techcrunch.com/2026/05/27/why-googles-ai-cant-spell-google-or-anything-else/ |
| `web_google_20260530_pcgamer_enigmatic_r_count` | AI Overview | character_count | independently opened | https://www.pcgamer.com/software/ai/there-are-two-ps-in-the-word-google-says-the-companys-upgraded-ai-overview-as-an-old-llm-issue-rears-its-ugly-head/ |
| `web_google_20260530_tomsguide_disregard_definition` | AI Overview | constraint_awareness | independently opened | https://www.tomsguide.com/computing/search-engines/dont-search-disregard-googles-new-ai-experience-is-breaking-search |
| `web_google_20260530_tomsguide_stop_cancel_aimode` | AI Mode | constraint_awareness | independently opened | https://www.tomsguide.com/computing/search-engines/dont-search-disregard-googles-new-ai-experience-is-breaking-search |
| `grok_google_20260530_mashable_astronomical_spelling_2026` | AI Overview | character_count | source-open failed | https://mashable.com/tech/google-ai-overview-spelling |
| `grok_google_20260530_linkedin_2027_next_year_2026` | AI Overview | factuality | social/login-gated unverified | https://www.linkedin.com/posts/analytics-india-magazine_google-ai-overviews-is-back-in-the-spotlight-activity-7414625788429258753-iGbM |

## Strongest Promotion Candidates

These look strongest for benchmark-item derivation because they have direct
article evidence and deterministic targets:

- `web_google_20260530_techcrunch_google_p_count`
- `web_google_20260530_techcrunch_poop_r_count`
- `web_google_20260530_techcrunch_journalism_d_count`
- `web_google_20260530_pcgamer_enigmatic_r_count`
- `grok_google_20260530_indiatoday_google_ps_2026`
- `grok_google_20260530_indiatoday_gemini_ms_2026`
- `grok_google_20260530_indiatoday_journalism_ds_2026`

The `disregard`, `cancel`, and `stop` examples are important for Google Search
specifically, but they likely need manual scoring or a separate query-intent
subfamily rather than simple exact-answer scoring.

## Caveats

- Several candidates are different reports of the same late-May 2026 Google AI
  Overview spelling/counting cluster.
- Some examples may have been patched or account/device gated by the time of
  reproduction.
- Screenshots and article text should be treated as link-only evidence unless
  permission is obtained.
- No candidate has been promoted into the canonical source catalog yet.

## Next Steps

1. Promote only independently opened, non-duplicative rows into
   `data/source_catalog/sources_v0.jsonl`.
2. Generate benchmark items for the deterministic count cases first.
3. Add a `query_intent_misclassification` subfamily before using the
   `disregard`, `cancel`, and `stop` examples.
4. Run current Google Search reproduction only if the project decides that
   live-product repros are in scope; these may vary by account, location, and
   rollout bucket.
