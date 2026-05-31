from obviousbench.scorers.exact_string import score_exact_string_trim


def test_exact_string_accepts_trimmed_match():
    decision = score_exact_string_trim("  yrrebwarts\n", "yrrebwarts")

    assert decision.correct
    assert decision.extracted == "yrrebwarts"
    assert decision.failure_type == "none"


def test_exact_string_rejects_punctuation():
    decision = score_exact_string_trim("yrrebwarts.", "yrrebwarts")

    assert not decision.correct
    assert decision.extracted == "yrrebwarts."
    assert decision.failure_type == "wrong_letter_or_substring"


def test_exact_string_accepts_final_answer_cue_at_end():
    decision = score_exact_string_trim(
        (
            "If removing e from strawberry, the result is strawbrry. "
            "So answer: strawbrry."
        ),
        "strawbrry",
    )

    assert decision.correct
    assert decision.extracted == "strawbrry"
    assert decision.failure_type == "none"


def test_exact_string_accepts_quoted_value_after_equals():
    decision = score_exact_string_trim(
        'committee without the letter e = "committ"',
        "committ",
    )

    assert decision.correct
    assert decision.extracted == "committ"
    assert decision.failure_type == "none"


def test_exact_string_rejects_prompt_rewrite_with_target_inside():
    decision = score_exact_string_trim(
        "Replace every @ in necess@ry with @.",
        "necess@ry",
    )

    assert not decision.correct
    assert decision.extracted == "Replace every @ in necess@ry with @."
    assert decision.failure_type == "wrong_letter_or_substring"


def test_exact_string_accepts_decimal_with_unit_suffix():
    decision = score_exact_string_trim("4.827 km", "4.827")

    assert decision.correct
    assert decision.extracted == "4.827"
    assert decision.failure_type == "none"


def test_exact_string_rejects_numeric_output_with_conflicting_extra_number():
    decision = score_exact_string_trim("4.827 km from 3 miles", "4.827")

    assert not decision.correct
    assert decision.extracted == "4.827 km from 3 miles"
    assert decision.failure_type == "ambiguous_output"


def test_exact_string_empty_is_non_answer():
    decision = score_exact_string_trim("", "yrrebwarts")

    assert not decision.correct
    assert decision.extracted is None
    assert decision.failure_type == "non_answer"
