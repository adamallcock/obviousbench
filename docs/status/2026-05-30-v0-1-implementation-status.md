---
title: ObviousBench V0.1 Implementation Status
date: 2026-05-30
type: status
status: conditional
---

# ObviousBench V0.1 Implementation Status

> Correction: this status describes runnable v0.1 infrastructure plus generated
> seed data. It should not be read as completion of every milestone in the
> implementation plan. See `docs/status/2026-05-30-plan-completeness-audit.md`
> for the current audit.

Implemented locally on branch `implement-obviousbench-v0-1`.

## Implemented

- Python package scaffold with editable install support.
- Inspect AI task registration and task modules for all eight v0 families.
- Local JSONL dataset schema, loading, and validation.
- Deterministic prompt rendering for final-answer and multiple-choice templates.
- Deterministic scorer registry and per-sample dynamic scorer dispatch.
- Scorers for integer extraction, exact strings, normalized lists, multiple choice, regex, JSON field, and word/list count.
- Deterministic generator script for public v0 datasets and source catalog.
- Public v0 generated seed dataset with 318 items across eight families.
- Calibration smoke dataset.
- Source catalog with 25 validated source records.
- Grok-assisted public-source candidate mining pass with 11 candidate leads in
  `data/source_catalog/candidates_grok_2026-05-30.jsonl`.
- Google Search-focused public-source mining pass with 12 AI Overview / AI Mode
  candidate leads in
  `data/source_catalog/candidates_google_search_2026-05-30.jsonl`.
- Underrepresented-category source-archetype mining with 10 candidate archetypes
  in `data/source_catalog/candidates_underrepresented_2026-05-30.jsonl`.
- Reproducible generated expansion file with 50 additional generated variants
  in `data/public_v0/archetype_expansions_2026-05-30.jsonl`.
- Inspect smoke eval path using `mockllm/model`.
- OpenAI smoke eval path using Keychain-provided `OPENAI_API_KEY` and `openai/gpt-4.1`.
- OpenRouter smoke/partial eval path using the OpenAI-compatible endpoint and
  Keychain-provided `OPENROUTER_API_KEY`.
- Analysis CLI that parses Inspect `.eval` logs and writes summary CSV plus failure-gallery Markdown.
- README, methodology, prompt policy, scoring policy, source policy, benchmark card, branding, and source archetype docs.
- Run/model example configs.

## Verification Evidence

Commands run successfully on 2026-05-30:

```bash
.venv/bin/python -m pytest tests -q
.venv/bin/python -m ruff check .
.venv/bin/python -m compileall obviousbench
.venv/bin/python scripts/validate_dataset.py data/public_v0/*.jsonl data/calibration_v0/smoke_test.jsonl
.venv/bin/inspect eval obviousbench/tasks/smoke.py --model mockllm/model --log-dir results/raw --limit 3 --no-log-realtime
.venv/bin/inspect eval obviousbench/tasks/smoke.py --model openai/gpt-4.1 --log-dir results/raw --limit 3 --max-connections 1 --max-retries 1 --timeout 90 --no-log-realtime
.venv/bin/obviousbench summarize --logs results/raw --out results/summaries
git check-ignore -v .env results/raw/example.eval results/summaries/example.csv results/failure_gallery/example.md
```

Observed results:

- Tests: 53 passed.
- Ruff: all checks passed.
- Dataset validation: passed.
- Source catalog validation: 25 records parsed.
- Grok public-source mining: 11 candidate leads preserved separately from the
  canonical source catalog; 6 were independently opened on 2026-05-30.
- Google Search mining: 12 candidate leads preserved separately from the
  canonical source catalog; 10 were independently opened on 2026-05-30.
- Underrepresented expansion mining: 10 candidate archetypes normalized; 50
  generated expansion items validated.
- OpenRouter web-tool attempts were preserved as raw research artifacts but did
  not return usable archetype candidates in this run.
- Public dataset: 318 items.
- Inspect smoke eval: completed with `mockllm/model`.
- OpenAI smoke eval: completed with `openai/gpt-4.1`; 3 samples, 3 correct, 0 failures.
- OpenRouter smoke eval: completed with
  `openai/nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free`; 3 samples, 3
  correct, 0 failures.
- OpenRouter character-count subset: completed with 10 samples, 10 correct, 0
  failures.
- OpenRouter archetype-expansion subset: partially completed before free-model
  rate limiting; 17 scored samples, 15 correct, 2 scored failures, 2 provider
  errors. The two scored failures were numerically correct answers with unit
  suffixes, indicating scorer/prompt strictness rather than arithmetic failure.
- Summary and failure gallery: written under ignored `results/summaries/`.
- Private/generated output ignore checks: passed.

## Dataset Counts

```text
arithmetic.jsonl: 23
character_count.jsonl: 76
constraint_awareness.jsonl: 15
format_compliance.jsonl: 45
negation.jsonl: 25
ordering.jsonl: 45
spelling_transform.jsonl: 29
word_count.jsonl: 60
```

Total public v0 items: 318.

## Remaining Work For Full Public Results

- Run against the full desired 5-8 model panel once selected.
- Manually inspect a sample of real model failures for scorer false positives and false negatives.
- Decide whether to promote selected summary and failure-gallery artifacts out of ignored `results/` paths for public reporting.
- Expand generators if the target distribution needs to be closer to the original 400-item allocation.
- Review the Grok-mined candidates in
  `docs/research/2026-05-30-grok-public-failure-leads.md` and promote only
  verified records into `data/source_catalog/sources_v0.jsonl`.
- Review the Google Search-focused candidates in
  `docs/research/2026-05-30-google-search-failure-leads.md` and deduplicate
  overlapping TechCrunch / India Today / PC Gamer spelling-count clusters before
  promotion.
- Review the underrepresented-category expansion summary in
  `docs/research/2026-05-30-underrepresented-archetype-expansions.md`; keep
  these rows labeled as generated variants unless independently reproduced.
