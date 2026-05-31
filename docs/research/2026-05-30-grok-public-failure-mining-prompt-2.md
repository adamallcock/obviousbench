---
title: Grok Public Failure Mining Prompt 2
date: 2026-05-30
type: research
status: draft
---

You are helping mine public source leads for ObviousBench, a benchmark of
human-trivial prompts where modern LLMs visibly fail.

This is a second pass. Exclude these already-found clusters:

- strawberry letter-r counting
- Google AI Overview glue-on-pizza
- Google AI Overview eat-rocks

Find additional public examples from web and X/Twitter where an LLM, AI
Overview, AI assistant, chatbot, or model-backed product failed at an obvious
task. Prioritize source diversity and direct evidence.

Target families:

- character_count: examples other than strawberry
- word_count: exact word/sentence count failures
- spelling_transform: reverse a word, alphabetize letters, remove a letter
- arithmetic: simple integer arithmetic, decimal comparison, counting objects
- negation: obey "do not" or answer the negated form
- ordering: alphabetize or sort a short list
- format_compliance: output exactly N words/items/JSON fields
- constraint_awareness: obvious one-step constraints

Search broadly. Useful query ideas:

- ChatGPT how many d in google
- ChatGPT how many letters in banana wrong
- LLM 9.11 9.9 bigger wrong
- ChatGPT simple arithmetic wrong screenshot
- Claude simple counting letters wrong
- Gemini simple math wrong screenshot
- LLM cannot count words exactly
- ChatGPT fails exact word count
- ChatGPT reverse word wrong
- LLM alphabetize letters wrong
- AI chatbot cannot follow do not say
- AI Overview wrong simple answer screenshot

Return only structured data. Do not include long quotes from copyrighted
sources. Use public links and citation URLs. Mark candidates as
`reproduce_first` when public evidence is enough to inspire a benchmark item but
not enough to include as a sourced reproduced failure.

Return a JSON object with this exact shape:

```json
{
  "date_searched": "2026-05-30",
  "scope": "second-pass public web and X source leads excluding strawberry and Google pizza/rocks",
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

Aim for 10 to 20 candidates if possible. It is acceptable to return fewer if
public evidence is weak, but do not fill the list with unverifiable anecdotes.
