---
title: OpenRouter Underrepresented Archetype Mining Prompt
date: 2026-05-30
type: research
status: draft
---

You are an independent second-pass miner for ObviousBench source archetypes.

You have context from prior Grok searches. Use web search tools to find
additional public source leads or to corroborate/replace weak leads. Focus on
underrepresented benchmark categories, not Google AI Overview spelling/counting
and not strawberry letter counting.

Target output: source-backed archetypes that can each produce five generated
benchmark variants.

Prioritize gaps:

- format compliance: strict JSON, exact bullets, only one token, no explanation
- word count: exact word count generation and counting
- arithmetic: decimal comparison, small calculations, date/time arithmetic
- ordering: alphabetic/numeric sorting
- negation: not/except/without
- constraint awareness: object-present and physical-action constraints
- instruction conflict: ignore/disregard/cancel/stop/conflicting instructions

Return only JSON with this shape:

```json
{
  "date_searched": "2026-05-30",
  "model_role": "openrouter independent web-search pass",
  "archetypes": [
    {
      "source_id_slug": "short_stable_slug",
      "platform": "web|x|reddit|news|forum|blog|paper|repo|other",
      "url": "https://...",
      "source_date": "YYYY-MM-DD or null",
      "date_seen": "2026-05-30",
      "author_or_handle": "public handle, organization, or null",
      "source_type": "direct_example|article_about_example|forum_thread|public_screenshot|official_discussion|study_report|benchmark_repo|paper",
      "media_type": "text|screenshot|video|article|paper|repo|mixed|unknown",
      "original_prompt": "short public prompt/query snippet if available",
      "claimed_model": "model/product if stated, else null",
      "claimed_output": "short public output snippet if available",
      "correct_answer": "expected answer if determinable",
      "failure_description": "one sentence describing the observed failure or benchmarked weakness",
      "task_family": "character_count|word_count|spelling_transform|arithmetic|negation|ordering|format_compliance|constraint_awareness|other",
      "subfamily": "short label",
      "answer_type": "integer|string|list|json|boolean|choice|decimal|other",
      "deterministic_scorer": "exact_integer|exact_string|normalized_list|json_field|regex_match|multiple_choice|word_count|manual_needed|other",
      "confidence": "high|medium|low",
      "recommended_action": "include|revise|reject|reproduce_first",
      "citation_title": "source title or post label",
      "citation_url": "same as url or best citation URL",
      "synthetic_expansion_ideas": [
        {
          "question": "generated variant question",
          "target": "target answer",
          "answer_type": "integer|string|list|json|boolean|choice|decimal|other",
          "scorer": "exact_integer|exact_string|normalized_list|json_field|regex_match|multiple_choice|word_count|manual_needed|other"
        }
      ],
      "notes": "risks, caveats, or reproduction advice"
    }
  ],
  "duplicates_or_rejected": [
    {
      "lead": "short description",
      "reason": "duplicate, weak, unverifiable, or unsuitable"
    }
  ],
  "search_notes": "coverage and remaining gaps"
}
```

Return 5 to 8 archetypes. Each archetype must have exactly five synthetic
expansion ideas. Do not fabricate URLs or pad with vague anecdotes.
