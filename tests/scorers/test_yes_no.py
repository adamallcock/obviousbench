from obviousbench.scorers.yes_no import score_yes_no


def test_yes_no_accepts_exact_answer_and_format():
    decision = score_yes_no("Yes", "yes")

    assert decision.correct
    assert decision.extracted == "Yes"
    assert decision.failure_type == "none"
    assert decision.resolved_format_correct


def test_yes_no_wrong_exact_answer_keeps_format_correct():
    decision = score_yes_no("No", "yes")

    assert not decision.correct
    assert decision.extracted == "No"
    assert decision.failure_type == "wrong_letter_or_substring"
    assert decision.resolved_format_correct


def test_yes_no_wrong_lowercase_exact_answer_keeps_format_correct():
    decision = score_yes_no("no", "yes")

    assert not decision.correct
    assert decision.extracted == "no"
    assert decision.failure_type == "wrong_letter_or_substring"
    assert decision.resolved_format_correct


def test_yes_no_answer_prefix_is_answer_correct_but_wrong_format():
    decision = score_yes_no("Answer: yes", "yes")

    assert decision.correct
    assert decision.extracted == "yes"
    assert decision.failure_type == "verbose_noncompliance"
    assert not decision.resolved_format_correct


def test_yes_no_terminal_punctuation_is_answer_correct_but_wrong_format():
    decision = score_yes_no("Yes.", "yes")

    assert decision.correct
    assert decision.extracted == "Yes"
    assert decision.failure_type == "verbose_noncompliance"
    assert not decision.resolved_format_correct


def test_yes_no_verbose_leading_answer_is_answer_correct_but_wrong_format():
    decision = score_yes_no("Yes, because trailing zeros do not change value.", "yes")

    assert decision.correct
    assert decision.extracted == "Yes"
    assert decision.failure_type == "verbose_noncompliance"
    assert not decision.resolved_format_correct


def test_yes_no_leading_answer_line_allows_opposite_word_in_explanation():
    decision = score_yes_no(
        (
            "yes\n\n"
            "The decimals are equal because trailing zeros after the decimal point "
            "do not alter the value, so no additional hundredths contribution exists."
        ),
        "yes",
    )

    assert decision.correct
    assert decision.extracted == "yes"
    assert decision.failure_type == "verbose_noncompliance"
    assert not decision.resolved_format_correct


def test_yes_no_leading_answer_line_allows_no_as_non_answer_modifier():
    decision = score_yes_no(
        "yes\n\nNo additional value is added by the trailing zero.",
        "yes",
    )

    assert decision.correct
    assert decision.extracted == "yes"
    assert decision.failure_type == "verbose_noncompliance"
    assert not decision.resolved_format_correct


def test_yes_no_leading_answer_line_rejects_later_conflicting_answer_cue():
    decision = score_yes_no(
        "yes\n\nNo, the correct answer is no.",
        "yes",
    )

    assert not decision.correct
    assert decision.extracted == "yes"
    assert decision.failure_type == "ambiguous_output"
    assert not decision.resolved_format_correct


def test_yes_no_wrong_verbose_leading_answer_is_wrong_format():
    decision = score_yes_no("No, because trailing zeros do not matter.", "yes")

    assert not decision.correct
    assert decision.extracted == "No"
    assert decision.failure_type == "wrong_letter_or_substring"
    assert not decision.resolved_format_correct


def test_yes_no_conflicting_tokens_are_ambiguous():
    decision = score_yes_no("yes. no.", "yes")

    assert not decision.correct
    assert decision.failure_type == "ambiguous_output"
    assert not decision.resolved_format_correct


def test_yes_no_final_answer_cue_can_supersede_reasoning_tokens():
    decision = score_yes_no("At first this looks like no.\nFinal answer: yes", "yes")

    assert decision.correct
    assert decision.extracted == "yes"
    assert decision.failure_type == "verbose_noncompliance"
    assert not decision.resolved_format_correct


def test_yes_no_rejects_synonym():
    decision = score_yes_no("yeah", "yes")

    assert not decision.correct
    assert decision.extracted is None
    assert decision.failure_type == "format_noncompliance"
    assert not decision.resolved_format_correct


def test_yes_no_empty_output_is_not_format_correct():
    decision = score_yes_no("", "yes")

    assert not decision.correct
    assert decision.extracted is None
    assert decision.failure_type == "non_answer"
    assert not decision.resolved_format_correct
