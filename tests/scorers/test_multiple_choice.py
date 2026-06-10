from obviousbench.scorers.multiple_choice import score_multiple_choice_letter


def test_multiple_choice_accepts_single_letter():
    decision = score_multiple_choice_letter("B", "B")

    assert decision.correct
    assert decision.extracted == "B"


def test_multiple_choice_accepts_verbose_output_as_answer_correct():
    decision = score_multiple_choice_letter("The answer is B", "B")

    assert decision.correct
    assert decision.extracted == "B"
    assert decision.failure_type == "verbose_noncompliance"


def test_multiple_choice_accepts_letter_with_option_text_as_answer_correct():
    decision = score_multiple_choice_letter("B. The bicycle", "B")

    assert decision.correct
    assert decision.extracted == "B"
    assert decision.failure_type == "verbose_noncompliance"


def test_multiple_choice_accepts_bold_letter_with_option_text_as_answer_correct():
    decision = score_multiple_choice_letter(
        "**B. Drive the car there**\n\nThe car must be at the shop.",
        "B",
    )

    assert decision.correct
    assert decision.extracted == "B"
    assert decision.failure_type == "verbose_noncompliance"
    assert not decision.resolved_format_correct


def test_multiple_choice_extracts_wrong_letter_with_option_text():
    decision = score_multiple_choice_letter("A. Walk", "B")

    assert not decision.correct
    assert decision.extracted == "A"
    assert decision.failure_type == "negation_error"
