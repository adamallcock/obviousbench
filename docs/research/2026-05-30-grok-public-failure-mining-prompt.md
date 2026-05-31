---
title: Grok Public Failure Mining Prompt
date: 2026-05-30
type: research
status: draft
---

You are helping mine public source leads for ObviousBench, a benchmark of
human-trivial prompts where modern LLMs visibly fail.

Find public examples from the web and X/Twitter where an LLM, AI Overview, AI
assistant, chatbot, or model-backed product failed at an "obvious" task such as:

- counting letters or words
- simple spelling/transformation questions
- elementary arithmetic
- negation or instruction following
- ordering or sorting
- format compliance
- constraint awareness
- trivial common-sense or "read the prompt carefully" tasks

Prioritize direct, citable public sources over commentary. Good source types
include original posts, public screenshots with stable URLs, articles that embed
or quote the original example, public issue/forum discussions, blog posts, or
official pages discussing the failure. Do not invent URLs. If a candidate cannot
be verified from a public citation, mark it as low confidence or reject.

Use both web and X search if available. Search broadly, including queries such
as:

- ChatGPT strawberry r
- LLM cannot count letters
- AI car wash test LLM
- Google AI Overview glue pizza rocks
- ChatGPT simple math fail
- Gemini simple question fail
- Claude letter counting fail
- LLM failed simple spelling
- AI says how many letters in word
- chatbot fails obvious question

Return only structured data. Do not include long quotes from copyrighted
sources. Short prompt/output snippets are okay only when needed to identify the
candidate.

Return a JSON object with this shape:

```json
{
  "date_searched": "2026-05-30",
  "scope": "public web and X source leads for obvious LLM failures",
  "candidates": [
    {
      "source_id_slug": "short_stable_slug",
      "platform": "web|x|reddit|news|forum|blog|other",
      "url": "https://...",
      "source_date": "YYYY-MM-DD or null",
      "date_seen": "2026-05-30",
      "author_or_handle": "public handle or organization, or null",
      "source_type": "direct_example|article_about_example|forum_thread|public_screenshot|official_discussion|secondary_commentary",
      "media_type": "text|screenshot|video|mixed|unknown",
      "claimed_model": "model/product name if stated, else null",
      "original_prompt": "short prompt snippet if public and necessary",
      "claimed_output": "short output snippet if public and necessary",
      "correct_answer": "expected answer if determinable",
      "failure_description": "one sentence describing the observed failure",
      "task_family": "character_count|word_count|spelling_transform|arithmetic|negation|ordering|format_compliance|constraint_awareness|other",
      "subfamily": "short label",
      "answer_type": "integer|string|list|json|boolean|choice|other",
      "deterministic_scorer": "exact_integer|exact_string|normalized_list|json_field|regex_match|multiple_choice|manual_needed|other",
      "human_triviality": "why a literate adult can solve it without specialist knowledge",
      "rights_status": "link_only|public_text_short_snippet|permission_needed|unknown",
      "confidence": "high|medium|low",
      "recommended_action": "include|revise|reject|reproduce_first",
      "citation_title": "source title or post label",
      "citation_url": "same as url or best citation URL",
      "notes": "risks, caveats, or reproduction advice"
    }
  ],
  "rejected_or_weak_leads": [
    {
      "lead": "short description",
      "reason": "why it should not be used yet"
    }
  ],
  "search_notes": "brief notes on coverage and what remains to search"
}
```

Return 15 to 25 candidates if enough public evidence exists. Separate
"benchmark-ready" candidates from mere leads by using `recommended_action`.
Favor `reproduce_first` when the source is public but the observed failure
should be verified against current models before inclusion.
