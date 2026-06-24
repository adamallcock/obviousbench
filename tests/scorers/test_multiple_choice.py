from obviousbench.scorers.multiple_choice import score_multiple_choice_letter


def test_multiple_choice_accepts_single_letter():
    decision = score_multiple_choice_letter("B", "B")

    assert decision.correct
    assert decision.extracted == "B"


def test_multiple_choice_accepts_bare_letter_with_period_as_strict_correct():
    decision = score_multiple_choice_letter("A.", "A")

    assert decision.correct
    assert decision.extracted == "A"
    assert decision.failure_type == "none"
    assert decision.strict_correct


def test_multiple_choice_accepts_verbose_output_as_answer_correct():
    decision = score_multiple_choice_letter("The answer is B", "B")

    assert decision.correct
    assert decision.extracted == "B"
    assert decision.failure_type == "verbose_noncompliance"


def test_multiple_choice_accepts_letter_with_option_text_as_strict_correct():
    decision = score_multiple_choice_letter(
        "B. The bicycle",
        "B",
        accepted_targets=("The bicycle",),
    )

    assert decision.correct
    assert decision.extracted == "B"
    assert decision.failure_type == "none"
    assert decision.strict_correct


def test_multiple_choice_accepts_letter_with_accepted_option_text_as_strict_correct():
    decision = score_multiple_choice_letter(
        "A: Take the boat there",
        "A",
        accepted_targets=("Take the boat there",),
    )

    assert decision.correct
    assert decision.extracted == "A"
    assert decision.failure_type == "none"
    assert decision.strict_correct


def test_multiple_choice_accepts_correct_option_text_as_strict_correct():
    decision = score_multiple_choice_letter(
        "Take the boat there",
        "A",
        accepted_targets=("Take the boat there",),
    )

    assert decision.correct
    assert decision.extracted == "A"
    assert decision.failure_type == "none"
    assert decision.strict_correct


def test_multiple_choice_accepts_case_insensitive_option_text_as_strict_correct():
    decision = score_multiple_choice_letter(
        "take the boat there",
        "A",
        accepted_targets=("Take the boat there",),
    )

    assert decision.correct
    assert decision.extracted == "A"
    assert decision.failure_type == "none"
    assert decision.strict_correct


def test_multiple_choice_accepts_option_text_with_terminal_period_as_strict_correct():
    decision = score_multiple_choice_letter(
        "Take the boat there.",
        "A",
        accepted_targets=("Take the boat there",),
    )

    assert decision.correct
    assert decision.extracted == "A"
    assert decision.failure_type == "none"
    assert decision.strict_correct


def test_multiple_choice_accepts_answer_phrase_with_correct_option_text_as_strict_correct():
    decision = score_multiple_choice_letter(
        "The answer is Take the boat there.",
        "A",
        accepted_targets=("Take the boat there",),
    )

    assert decision.correct
    assert decision.extracted == "A"
    assert decision.failure_type == "none"
    assert decision.strict_correct


def test_multiple_choice_rejects_option_text_without_accepted_target_context():
    decision = score_multiple_choice_letter("Take the boat there", "A")

    assert not decision.correct
    assert decision.failure_type == "format_noncompliance"


def test_multiple_choice_rejects_wrong_option_text():
    decision = score_multiple_choice_letter(
        "Walk down the dock",
        "A",
        accepted_targets=("Take the boat there",),
    )

    assert not decision.correct
    assert decision.failure_type == "format_noncompliance"


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


def test_multiple_choice_accepts_correct_answer_phrase_as_answer_correct():
    decision = score_multiple_choice_letter(
        "Thus, the correct answer is:\n\n**B. Ride the motorcycle there**",
        "B",
    )

    assert decision.correct
    assert decision.extracted == "B"
    assert decision.failure_type == "verbose_noncompliance"
    assert not decision.resolved_format_correct


def test_multiple_choice_accepts_final_standalone_letter_as_answer_correct():
    decision = score_multiple_choice_letter(
        "The mechanic needs the motorcycle at the shop.\n\nB",
        "B",
    )

    assert decision.correct
    assert decision.extracted == "B"
    assert decision.failure_type == "verbose_noncompliance"
    assert not decision.resolved_format_correct


def test_multiple_choice_accepts_boxed_letter_as_answer_correct():
    decision = score_multiple_choice_letter(
        "The motorcycle should be ridden there.\n\n$$\n\\boxed{B}\n$$",
        "B",
    )

    assert decision.correct
    assert decision.extracted == "B"
    assert decision.failure_type == "verbose_noncompliance"
    assert not decision.resolved_format_correct
