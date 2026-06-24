---
title: Scoring Policy
date: 2026-05-31
type: policy
status: current
---

# Scoring Policy

ObviousBench uses deterministic Python scorers only. No model output is scored
by another LLM.

Non-format tasks may accept reasonable wrappers when a single compatible answer
is recoverable. For example, `There are 3.` can be correct when the target is
`3`, and `3 items` is correct when the target is `3`.

Integer-count tasks extract digit numerals and simple English number words from
zero through twenty. For example, `four days` is scored as extracted answer `4`.
Signed digit integers such as `-2` are accepted, but signed number words such as
`minus two` are extracted as the unsigned value `2`.

Numeric exact-string tasks accept a single matching numeric value with unit text.
For example, `4.827 km` is correct for target `4.827`. Outputs with multiple
numeric values, such as `4.827 km from 3 miles`, are ambiguous and incorrect.
Decimal-equivalent forms such as `.5 liters` for target `0.5` and `0.50 kg` for
target `0.5` are accepted.

Exact string tasks treat terminal final-answer cues as answer-correct only when
they identify one compatible answer. Examples include `Answer: blue`,
`result=blue`, and quoted equals forms such as `word = "blue"`. These wrappers
are verbose noncompliance, so they are not strict-correct. A leading exact answer
followed by a parenthetical explanation is also answer-correct but not strict.
Prompt rewrites or whole-prompt echoes are rejected even if they contain the
target string, such as `Replace every @ in necess@ry with @.` for target
`necess@ry`.

Normalized list tasks accept comma-separated lists, whitespace-separated lists
when there are no commas, case differences, quoted items, and enclosing `[]`,
`()`, or `{}` wrappers. Bracketed arrays such as `[3.01,3.1, 3.2]` are correct
for target `3.01, 3.1, 3.2`. A leading matching list followed by explanation or
a trailing confidence annotation is answer-correct but not strict. Wrong order,
missing items, extra items, semicolon-separated text, and punctuation attached
to list items are rejected.

Multiple-choice tasks are strict when the output is only a letter. Verbose
wrappers such as `The answer is B`, `B. option text`, and `final answer: B` can
be answer-correct, but they are not strict-correct. Natural-language option text
alone, parenthesized letters, slash-combined choices, and unsupported wrappers
such as `I choose B.` are format failures under the current scorer.

JSON exact-field tasks require a top-level object with an `answer` field. Extra
fields are allowed, and fenced JSON blocks are answer-correct when the field
matches, but fences are verbose noncompliance. Prose around JSON, malformed JSON,
arrays at the top level, and missing `answer` fields are rejected.

Regex tasks trim outer whitespace and then require `re.fullmatch`. Verbose
prefixes, trailing punctuation, case mismatches, and extra digits are format
failures unless the target pattern explicitly permits them.

Format-compliance tasks are strict. If the instruction says to return only a number, `There are 3.` is a format failure.

Ambiguous outputs are rejected when they include multiple incompatible candidate
answers. Examples include `2 or 3` for target `3`, `4.827 km from 3 miles` for
target `4.827`, and `4 or 5` for target `5`. Repeating the same value in two
forms, such as `3 or three`, is not ambiguous under the integer extractor.

Provider safety or policy strings returned as assistant text, for example
`SAFETY_CHECK_TYPE_*`, are treated as provider errors by log summarization rather
than as ordinary model reasoning failures. After configured retries, final
provider errors, refusals, and timeouts remain in the scored denominator as
incorrect attempts. Their counts are reported separately so readers can
distinguish wrong answers from provider-side refusals or infrastructure issues.

Scorer gold examples live in `tests/fixtures/scorer_gold/` and are exercised
through `obviousbench.analysis.rescore.rescore_output`. Scorer changes that
alter these decisions must update the fixture expectations and this policy in
the same change.

Supported scorer names:

- `exact_integer_extract_first_v0`
- `exact_string_trim_v0`
- `normalized_string_v0`
- `normalized_list_v0`
- `multiple_choice_letter_v0`
- `regex_match_v0`
- `json_exact_field_v0`
- `word_count_v0`

Every scorer returns a correctness value, extracted answer, explanation, scorer name, strict-format flag, and failure type.
