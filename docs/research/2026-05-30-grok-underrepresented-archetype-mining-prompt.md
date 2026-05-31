---
title: Grok Underrepresented Archetype Mining Prompt
date: 2026-05-30
type: research
status: draft
---

You are helping mine public source leads for ObviousBench, a benchmark of
human-trivial prompts where AI systems visibly fail.

This pass should avoid over-indexing on Google AI Overview spelling/counting and
the strawberry letter-count meme. Find source-backed example types across other
categories that can each be artificially expanded into five similar generated
benchmark items.

Target categories:

- arithmetic: decimal comparison, simple calculations, unit/counting mistakes
- word_count: exact word counts, exact sentence/paragraph length
- spelling_transform: reverse word, remove letters, replace letters, spell out
- ordering: alphabetize/sort short lists, order numbers/dates
- format_compliance: exact JSON, exact number of bullet points, only one token
- negation: "not", "except", "do not", "which does not"
- constraint_awareness: object must be present, physical/action constraints
- instruction_conflict: ignore/disregard/cancel treated incorrectly

Good source types:

- original public posts/screenshots
- public forums such as OpenAI Community, Hacker News, Reddit, or issue threads
- articles that embed or describe a specific public example
- benchmark/prior-art repos or papers that include concrete examples

Return source leads, not final benchmark rows. For each lead, identify the
archetype and give five synthetic expansion ideas that are similar in character
but not copied from the public source.

Do not invent URLs. Do not include long quotes from copyrighted sources. Use
short prompt/output snippets only when needed to identify the lead.

Return a JSON object with this exact shape:

```json
{
  "date_searched": "2026-05-30",
  "scope": "public source leads for non-Google/non-strawberry ObviousBench archetypes",
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

Aim for 10 to 14 archetypes. Prefer diversity over many duplicate letter-count
examples. Each archetype should have exactly five synthetic expansion ideas.
