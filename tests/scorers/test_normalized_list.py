from obviousbench.scorers.normalized_list import score_normalized_list


def test_normalized_list_accepts_comma_separated_answer():
    decision = score_normalized_list("3, 9, 12", "3, 9, 12")

    assert decision.correct
    assert decision.extracted == "3, 9, 12"


def test_normalized_list_accepts_bracketed_array_answer():
    decision = score_normalized_list("[3.01,3.1, 3.2]", "3.01, 3.1, 3.2")

    assert decision.correct
    assert decision.extracted == "3.01, 3.1, 3.2"


def test_normalized_list_accepts_quoted_array_answer():
    decision = score_normalized_list('["a", "b", "c"]', "a, b, c")

    assert decision.correct
    assert decision.extracted == "a, b, c"


def test_normalized_list_accepts_confidence_macro_as_wrong_format():
    decision = score_normalized_list(
        r"apple, banana, pear \confidence{95}",
        "apple, banana, pear",
    )

    assert decision.correct
    assert decision.extracted == "apple, banana, pear"
    assert decision.failure_type == "verbose_noncompliance"
    assert not decision.resolved_format_correct


def test_normalized_list_accepts_leading_list_with_explanation_as_wrong_format():
    decision = score_normalized_list(
        "3.01, 3.1, 3.2 (the numbers sorted from smallest to largest.)",
        "3.01, 3.1, 3.2",
    )

    assert decision.correct
    assert decision.extracted == "3.01, 3.1, 3.2"
    assert decision.failure_type == "verbose_noncompliance"
    assert not decision.resolved_format_correct


def test_normalized_list_accepts_colon_prefixed_sorted_list_as_wrong_format():
    decision = score_normalized_list(
        "The items sorted alphabetically: cap, car, cat",
        "cap, car, cat",
    )

    assert decision.correct
    assert decision.extracted == "cap, car, cat"
    assert decision.failure_type == "verbose_noncompliance"
    assert not decision.resolved_format_correct


def test_normalized_list_accepts_terminal_period_as_wrong_format():
    decision = score_normalized_list("Blue, green, red.", "blue, green, red")

    assert decision.correct
    assert decision.extracted == "blue, green, red"
    assert decision.failure_type == "verbose_noncompliance"
    assert not decision.resolved_format_correct


def test_normalized_list_accepts_numeric_colon_prefixed_list_as_wrong_format():
    decision = score_normalized_list(
        "The numbers sorted from smallest to largest is: 5.05, 5.15, 5.5",
        "5.05, 5.15, 5.5",
    )

    assert decision.correct
    assert decision.extracted == "5.05, 5.15, 5.5"
    assert decision.failure_type == "verbose_noncompliance"
    assert not decision.resolved_format_correct


def test_normalized_list_rejects_wrong_order():
    decision = score_normalized_list("9, 3, 12", "3, 9, 12")

    assert not decision.correct
    assert decision.failure_type == "ordering_error"
