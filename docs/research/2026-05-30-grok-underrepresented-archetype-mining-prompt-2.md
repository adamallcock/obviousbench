---
title: Grok Underrepresented Archetype Mining Prompt 2
date: 2026-05-30
type: research
status: draft
---

You are helping mine additional public source leads for ObviousBench.

This is a second pass. Exclude these already-found archetype clusters:

- GPT-4 with Calc arithmetic/unit conversions
- Reddit short number sorting
- LinkedIn alphabetizing words
- Reddit reverse-spelling bot tests
- Quanta/simple negation
- Google AI Overview spelling/counting
- strawberry letter counting

Find source-backed archetypes in these categories:

- format_compliance: exact JSON, exactly N bullet points, single-token answer,
  XML/YAML/table formatting, "do not explain"
- word_count: exact word counts, exactly N words/sentences, count words in a
  sentence/list
- arithmetic: decimal comparison and small numeric comparison, not broad calc
- constraint_awareness: physical action/object-present failures, classic car
  wash/bike/shop style constraints
- instruction_conflict: queries or prompts with ignore/disregard/cancel/stop,
  or conflicting instructions
- negation: except/not/without, preferably concrete examples

Return source leads that can each be expanded into exactly five generated
benchmark variants. Prefer direct public examples, forum threads, papers/repos
with concrete examples, or articles describing specific examples.

Return only structured JSON in this exact shape:

```json
{
  "date_searched": "2026-05-30",
  "scope": "second-pass public source leads for underrepresented ObviousBench archetypes",
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
      "human_triviality": "why a literate adult can solve it without specialist knowledge",
      "rights_status": "link_only|public_text_short_snippet|permission_needed|unknown",
      "confidence": "high|medium|low",
      "recommended_action": "include|revise|reject|reproduce_first",
      "citation_title": "source title or post label",
      "citation_url": "same as url or best citation URL",
      "expansion_pattern": "how to create five similar generated variants without copying the public item",
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
  "rejected_or_weak_leads": [
    {
      "lead": "short description",
      "reason": "why it should not be used yet"
    }
  ],
  "search_notes": "brief notes on coverage and what remains"
}
```

Aim for 5 to 8 archetypes. Each archetype must have exactly five synthetic
expansion ideas. Do not pad with unverifiable anecdotes.
