from obviousbench.scorers.exact_string import score_exact_string_trim


def test_exact_string_accepts_trimmed_match():
    decision = score_exact_string_trim("  yrrebwarts\n", "yrrebwarts")

    assert decision.correct
    assert decision.extracted == "yrrebwarts"
    assert decision.failure_type == "none"


def test_exact_string_accepts_case_only_difference_as_exact_match():
    decision = score_exact_string_trim("Circle", "circle")

    assert decision.correct
    assert decision.extracted == "Circle"
    assert decision.failure_type == "none"
    assert decision.resolved_format_correct


def test_exact_string_accepts_terminal_punctuation_as_wrong_format():
    decision = score_exact_string_trim("yrrebwarts.", "yrrebwarts")

    assert decision.correct
    assert decision.extracted == "yrrebwarts"
    assert decision.failure_type == "verbose_noncompliance"
    assert not decision.resolved_format_correct


def test_exact_string_accepts_byte_token_artifacts_as_wrong_format():
    decision = score_exact_string_trim("\u010a\u010aplum", "plum")

    assert decision.correct
    assert decision.extracted == "plum"
    assert decision.failure_type == "verbose_noncompliance"
    assert not decision.resolved_format_correct


def test_exact_string_accepts_explicit_alternate_target():
    decision = score_exact_string_trim(
        "Mars",
        "plant",
        accepted_targets=("mars", "pluto"),
    )

    assert decision.correct
    assert decision.extracted == "Mars"
    assert decision.failure_type == "none"
    assert decision.resolved_format_correct


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
    assert decision.failure_type == "verbose_noncompliance"
    assert not decision.resolved_format_correct


def test_exact_string_accepts_quoted_value_after_equals():
    decision = score_exact_string_trim(
        'committee without the letter e = "committ"',
        "committ",
    )

    assert decision.correct
    assert decision.extracted == "committ"
    assert decision.failure_type == "verbose_noncompliance"
    assert not decision.resolved_format_correct


def test_exact_string_accepts_leading_answer_with_explanation_as_wrong_format():
    decision = score_exact_string_trim(
        "paper (The answer is paper, since the others are metal.)",
        "paper",
    )

    assert decision.correct
    assert decision.extracted == "paper"
    assert decision.failure_type == "verbose_noncompliance"
    assert not decision.resolved_format_correct


def test_exact_string_accepts_leading_answer_sentence_as_wrong_format():
    decision = score_exact_string_trim("Paper is not made of metal.", "paper")

    assert decision.correct
    assert decision.extracted == "paper"
    assert decision.failure_type == "verbose_noncompliance"
    assert not decision.resolved_format_correct


def test_exact_string_accepts_first_line_answer_with_explanation_as_wrong_format():
    decision = score_exact_string_trim(
        "paper \n\nThe question asks for the item that is not metal.",
        "paper",
    )

    assert decision.correct
    assert decision.extracted == "paper"
    assert decision.failure_type == "verbose_noncompliance"
    assert not decision.resolved_format_correct


def test_exact_string_accepts_final_line_answer_after_self_correction_as_wrong_format():
    decision = score_exact_string_trim(
        (
            "committx\n\n"
            "Wait: comittx\n\n"
            "Removing e's from committee gives a different result.\n\n"
            "**committ**"
        ),
        "committ",
    )

    assert decision.correct
    assert decision.extracted == "committ"
    assert decision.failure_type == "verbose_noncompliance"
    assert not decision.resolved_format_correct


def test_exact_string_accepts_markdown_wrapped_answer_as_wrong_format():
    decision = score_exact_string_trim("**paralll**", "paralll")

    assert decision.correct
    assert decision.extracted == "paralll"
    assert decision.failure_type == "verbose_noncompliance"
    assert not decision.resolved_format_correct


def test_exact_string_accepts_repeated_letter_with_separators_as_wrong_format():
    decision = score_exact_string_trim("e, e", "ee")

    assert decision.correct
    assert decision.extracted == "e, e"
    assert decision.failure_type == "verbose_noncompliance"
    assert not decision.resolved_format_correct


def test_exact_string_accepts_replacement_spacing_as_wrong_format():
    decision = score_exact_string_trim("+oo+ h", "+oo+h")

    assert decision.correct
    assert decision.extracted == "+oo+ h"
    assert decision.failure_type == "verbose_noncompliance"
    assert not decision.resolved_format_correct


def test_exact_string_rejects_plain_word_spacing_difference():
    decision = score_exact_string_trim("blue and red", "blueandred")

    assert not decision.correct
    assert decision.extracted == "blue and red"
    assert decision.failure_type == "wrong_letter_or_substring"


def test_exact_string_rejects_wrong_repeated_letter_count_with_separators():
    decision = score_exact_string_trim("e e e", "ee")

    assert not decision.correct
    assert decision.extracted == "e e e"
    assert decision.failure_type == "wrong_letter_or_substring"


def test_exact_string_accepts_colon_suffix_answer_as_wrong_format():
    decision = score_exact_string_trim(
        "strawberry without the letter e: strawbrry",
        "strawbrry",
    )

    assert decision.correct
    assert decision.extracted == "strawbrry"
    assert decision.failure_type == "verbose_noncompliance"
    assert not decision.resolved_format_correct


def test_exact_string_accepts_arrow_suffix_answer_as_wrong_format():
    decision = score_exact_string_trim("coconut -> ccnut", "ccnut")

    assert decision.correct
    assert decision.extracted == "ccnut"
    assert decision.failure_type == "verbose_noncompliance"
    assert not decision.resolved_format_correct


def test_exact_string_accepts_unicode_arrow_suffix_answer_as_wrong_format():
    decision = score_exact_string_trim("coconut → ccnut", "ccnut")

    assert decision.correct
    assert decision.extracted == "ccnut"
    assert decision.failure_type == "verbose_noncompliance"
    assert not decision.resolved_format_correct


def test_exact_string_accepts_becomes_suffix_answer_as_wrong_format():
    decision = score_exact_string_trim("freezer becomes fr33z3r", "fr33z3r")

    assert decision.correct
    assert decision.extracted == "fr33z3r"
    assert decision.failure_type == "verbose_noncompliance"
    assert not decision.resolved_format_correct


def test_exact_string_rejects_broad_becomes_sentence():
    decision = score_exact_string_trim("the word becomes fr33z3r", "fr33z3r")

    assert not decision.correct
    assert decision.extracted == "the word becomes fr33z3r"
    assert decision.failure_type == "wrong_letter_or_substring"


def test_exact_string_accepts_remove_letter_explanation_as_wrong_format():
    decision = score_exact_string_trim("umbrea without the letter l", "umbrea")

    assert decision.correct
    assert decision.extracted == "umbrea"
    assert decision.failure_type == "verbose_noncompliance"
    assert not decision.resolved_format_correct


def test_exact_string_rejects_wrong_leading_remove_letter_explanation():
    decision = score_exact_string_trim("eahhell without the letter s", "eahell")

    assert not decision.correct
    assert decision.extracted == "eahhell without the letter s"
    assert decision.failure_type == "wrong_letter_or_substring"


def test_exact_string_accepts_terminal_copula_answer_as_wrong_format():
    decision = score_exact_string_trim(
        "The number that is not greater than 10 is 9.",
        "9",
    )

    assert decision.correct
    assert decision.extracted == "9"
    assert decision.failure_type == "verbose_noncompliance"
    assert not decision.resolved_format_correct


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


def test_exact_string_accepts_numeric_equation_rhs_as_wrong_format():
    decision = score_exact_string_trim("3 * 1.609 = 4.827 km", "4.827")

    assert decision.correct
    assert decision.extracted == "4.827"
    assert decision.failure_type == "verbose_noncompliance"
    assert not decision.resolved_format_correct


def test_exact_string_rejects_prompt_specific_rounding_miss():
    decision = score_exact_string_trim("4.828 kilometers", "4.827")

    assert not decision.correct
    assert decision.extracted == "4.828 kilometers"
    assert decision.failure_type == "wrong_letter_or_substring"


def test_exact_string_accepts_confidence_macro_as_wrong_format():
    decision = score_exact_string_trim(r"7.2 \confidence{100}", "7.2")

    assert decision.correct
    assert decision.extracted == "7.2"
    assert decision.failure_type == "verbose_noncompliance"
    assert not decision.resolved_format_correct


def test_exact_string_accepts_leading_numeric_with_parenthetical_explanation():
    decision = score_exact_string_trim(
        "9.9 (The answer is 9.9, as 9.9 = 9.90 > 9.11.)",
        "9.9",
    )

    assert decision.correct
    assert decision.extracted == "9.9"
    assert decision.failure_type == "verbose_noncompliance"
    assert not decision.resolved_format_correct


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
