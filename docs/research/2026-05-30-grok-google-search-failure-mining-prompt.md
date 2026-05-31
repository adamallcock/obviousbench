---
title: Grok Google Search Failure Mining Prompt
date: 2026-05-30
type: research
status: draft
---

You are helping mine public source leads for ObviousBench, a benchmark of
human-trivial prompts where AI systems visibly fail.

This pass is specifically about Google Search AI failures after recent Google
Search upgrades, including Google AI Overviews, AI Mode, Search Labs, Gemini in
Search, or other Google Search answer surfaces.

Find public examples from the web and X/Twitter where Google Search's AI answer
surface failed at an obvious task. Prioritize direct, citable public sources:
original posts with screenshots, articles that embed or link to the original
example, public forum threads, watchdog reports, or official/credible coverage.

Focus on examples that can become benchmark leads:

- letter/word/counting mistakes in AI Overviews or AI Mode
- simple arithmetic, unit conversion, comparison, or date mistakes
- absurd common-sense advice
- unsafe advice that violates basic real-world constraints
- wrong answer to a query that has an unambiguous answer
- failure to follow obvious query constraints
- contradictory or self-refuting search summaries
- incorrect information created by misreading a source

Search broadly and include 2026 examples if available. Useful query ideas:

- Google AI Mode wrong answer
- Google AI Overview wrong answer 2026
- Google AI Overview fails simple question
- Google AI Overview spelling problem Google Gemini
- Google Search AI Mode hallucination screenshot
- Google AI Overview unsafe advice screenshot
- Google AI Overview count letters wrong
- Google AI Overview simple math wrong
- Google AI search upgraded wrong answers
- after Google I/O 2026 AI Mode wrong
- Google AI Mode disaster
- site:x.com Google AI Overview wrong
- site:x.com Google AI Mode wrong

Exclude or de-duplicate already-mined clusters unless a fresh Google Search
variant has a distinct public source:

- glue-on-pizza
- eat-rocks
- strawberry r-count in generic chatbots

Return only structured JSON. Do not include long quotes from copyrighted
sources. Short prompt/output snippets are okay only when needed to identify the
candidate.

Return a JSON object with this exact shape:

```json
{
  "date_searched": "2026-05-30",
  "scope": "public Google Search AI Overview, AI Mode, Search Labs, and Gemini-in-Search failure leads",
  "candidates": [
    {
      "source_id_slug": "short_stable_slug",
      "google_surface": "AI Overview|AI Mode|Search Labs|Gemini in Search|Google Search|unknown",
      "platform": "web|x|reddit|news|forum|blog|other",
      "url": "https://...",
      "source_date": "YYYY-MM-DD or null",
      "date_seen": "2026-05-30",
      "author_or_handle": "public handle or organization, or null",
      "source_type": "direct_example|article_about_example|forum_thread|public_screenshot|official_discussion|secondary_commentary|study_report",
      "media_type": "text|screenshot|video|mixed|unknown",
      "original_query": "short Google Search query or prompt snippet if public and necessary",
      "claimed_ai_answer": "short output snippet if public and necessary",
      "correct_answer": "expected answer if determinable",
      "failure_description": "one sentence describing the observed failure",
      "task_family": "character_count|word_count|spelling_transform|arithmetic|negation|ordering|format_compliance|constraint_awareness|factuality|other",
      "subfamily": "short label",
      "answer_type": "integer|string|list|json|boolean|choice|other",
      "deterministic_scorer": "exact_integer|exact_string|normalized_list|json_field|regex_match|multiple_choice|manual_needed|other",
      "human_triviality": "why a literate adult can solve it without specialist knowledge, or why it is obvious from the source",
      "rights_status": "link_only|public_text_short_snippet|permission_needed|unknown",
      "confidence": "high|medium|low",
      "recommended_action": "include|revise|reject|reproduce_first",
      "citation_title": "source title or post label",
      "citation_url": "same as url or best citation URL",
      "notes": "risks, caveats, source quality, or reproduction advice"
    }
  ],
  "rejected_or_weak_leads": [
    {
      "lead": "short description",
      "reason": "why it should not be used yet"
    }
  ],
  "search_notes": "brief notes on coverage, date range, and what remains to search"
}
```

Aim for 12 to 25 candidates if enough public evidence exists. Do not fabricate
items or use vague anecdotes. Mark social screenshots as `reproduce_first`
unless the image/post content is clearly public and stable.
