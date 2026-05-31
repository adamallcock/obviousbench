# Scoring Policy

ObviousBench v0.1 uses deterministic Python scorers only. No model output is scored by another LLM.

Non-format tasks may accept reasonable wrappers. For example, `There are 3.` can be correct when the target is `3`.

Integer-count tasks extract digit numerals and simple English number words from
zero through twenty. For example, `four days` is scored as extracted answer `4`.

Numeric exact-string tasks accept a single matching numeric value with unit text.
For example, `4.827 km` is correct for target `4.827`. Outputs with multiple
numeric values, such as `4.827 km from 3 miles`, are ambiguous and incorrect.

Format-compliance tasks are strict. If the instruction says to return only a number, `There are 3.` is a format failure.

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
