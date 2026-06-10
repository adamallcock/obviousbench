---
title: Paper V1 Grader Policy Investigation
date: 2026-06-01
type: research
status: ready
---

# Paper V1 Grader Policy Investigation

This note records the grader and generation-policy decisions from reviewing
specific `paper-v1-final` wrong-answer rows. The old `paper-v1-final` run is
still invalid for paper claims because it used `max_tokens=64`; the findings
below are for scorer policy and the rerun plan.

## Generation Policy

Use explicit benchmark settings rather than provider defaults:

- `max_tokens=10000` as a high safety cap, not as a short-answer constraint.
- Clamp lower only when a provider advertises a positive completion ceiling
  below 10000.
- `temperature=0` where supported, because the paper run should be as
  repeatable as each provider allows. Some reasoning routes ignore temperature;
  keep the setting explicit and record provider behavior rather than switching
  to hidden defaults.

Provider defaults are not recommended for claim-bearing sweeps because they can
change without a model alias change and differ across providers. A benchmark
should make the generation contract visible.

## Prompt Policy

Do not add a special system prompt to rescue messy models after inspecting
results. The paper v1 prompt policy uses the same user-facing final-answer
instruction across models. If we want to test a stronger instruction wrapper,
that should be a new frozen prompt-policy variant and all models should be
rerun under it.

This matters for Nemotron and Grok: both can emit correct answers with poor
format discipline. The benchmark should report that as answer correctness plus
format noncompliance, not tune one provider route until it behaves.

## Case Review

| Case | Old behavior | Finding | Policy decision |
| --- | --- | --- | --- |
| `grok/grok-4.3`, `obviousbench.negation.en.v0.public.000032` | Answer marked wrong. | Output started with `paper` then explanation; old run also stopped at `max_tokens=64`. | Rescore as answer-correct, format-wrong when the first non-empty line is exactly the target. |
| `anthropic/claude-haiku-4-5`, `obviousbench.negation.en.v0.public.000033` | `Circle` marked wrong for target `circle`. | Case is not semantically meaningful for these string-answer tasks. | Case-only string differences are strict-correct. |
| `anthropic/claude-sonnet-4-6`, `obviousbench.spell.en.v0.public.000022` | Messy repeated answer marked wrong. | First line was the correct transformed string `paralll`; later text was explanation. | Rescore as answer-correct, format-wrong. Markdown-wrapped exact answers are also answer-correct, format-wrong. |
| `anthropic/claude-sonnet-4-6`, `obviousbench.constraint.en.v0.public.000008` | `**B. Drive the car there**` marked format noncompliance and answer-wrong. | Leading multiple-choice letter is recoverable despite markdown. | Rescore as answer-correct, format-wrong. |
| `google/gemini-3.5-flash`, `obviousbench.format.en.v0.public.000046` | Malformed JSON from output `{"`. | Raw log stopped at `max_tokens=64`; 10k no-cache probe returned `{"answer": "blue"}` and scored strict-correct. | Do not repair malformed JSON in the grader. The fix is the 10k safety-cap rerun. |
| `openai/gpt-5-nano`, `obviousbench.spell.en.v0.public.000022` | Provider safety text was scored as a wrong answer after the 10k rerun. | Inspect recorded structured stop reason `content_filter`. | Treat structured `content_filter` stops as provider errors and exclude them from scored-sample denominators. |

## Implemented Scorer Changes

- `exact_string_trim_v0` accepts case-only differences as exact matches.
- `exact_string_trim_v0` accepts a target on the first non-empty line followed
  by explanation as answer-correct and format-wrong.
- `exact_string_trim_v0` accepts a markdown-wrapped exact answer as
  answer-correct and format-wrong.
- `multiple_choice_letter_v0` extracts leading choices through common markdown
  wrappers such as `**B. ...**`.
- `json_exact_field_v0` remains strict: malformed or truncated JSON is not
  guessed or repaired.
- Analysis treats structured `content_filter` stop reasons as provider errors,
  matching provider refusal text handling.

## Verification

- Targeted scorer tests cover the rescued cases.
- The named samples were rescored directly from raw logs with the updated
  scorer implementation.
- A fresh 12-model smoke with `max_tokens=10000` completed with `stop` for all
  12 entries.
- A Gemini 3.5 Flash no-cache JSON probe for
  `obviousbench.format.en.v0.public.000046` returned valid JSON and scored
  strict-correct.
- Targeted analysis tests cover provider refusal text and structured
  `content_filter` stop reasons.

## Rerun Rule

Do not patch the old leaderboard in place. Run the full paper panel into
`results/raw/paper-v1-final-high-cap` and
`results/summaries/paper-v1-final-high-cap`, then regenerate comparison
artifacts, wrong-answer review, figures, and paper tables from that fresh run.
