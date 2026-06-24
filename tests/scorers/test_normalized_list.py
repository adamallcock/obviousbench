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


def test_normalized_list_accepts_leading_list_then_explanation_as_wrong_format():
    decision = score_normalized_list(
        "canoe, leaf, twig, drum \n\n"
        "The words sorted by their ending letters in alphabetical order "
        "(e, f, g, m) are canoe (e), leaf (f), twig (g), drum (m).",
        "canoe, leaf, twig, drum",
    )

    assert decision.correct
    assert decision.extracted == "canoe, leaf, twig, drum"
    assert decision.failure_type == "verbose_noncompliance"
    assert not decision.resolved_format_correct


def test_normalized_list_accepts_exact_list_with_trailing_escape_artifact():
    decision = score_normalized_list(
        "-0.4, -0.04, 0.04, 0.4\n\\",
        "-0.4, -0.04, 0.04, 0.4",
    )

    assert decision.correct
    assert decision.extracted == "-0.4, -0.04, 0.04, 0.4"
    assert decision.failure_type == "verbose_noncompliance"
    assert not decision.resolved_format_correct


def test_normalized_list_accepts_exact_list_with_same_line_escape_artifact():
    decision = score_normalized_list(
        '-0.4, -0.04, 0.04, 0.4\\"',
        "-0.4, -0.04, 0.04, 0.4",
    )

    assert decision.correct
    assert decision.extracted == "-0.4, -0.04, 0.04, 0.4"
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


def test_normalized_list_rejects_wrong_leading_list_that_mentions_target_later():
    decision = score_normalized_list(
        "leaf, canoe, twig, drum\n\n"
        "The correct order would have been canoe, leaf, twig, drum.",
        "canoe, leaf, twig, drum",
    )

    assert not decision.correct
    assert decision.failure_type == "ordering_error"


def test_normalized_list_rejects_target_prefix_inside_longer_item():
    decision = score_normalized_list("1, 23\nextra text", "1, 2")

    assert not decision.correct
    assert decision.failure_type == "ordering_error"


def test_normalized_list_accepts_compact_punctuation_symbol_sequence():
    decision = score_normalized_list("@#?!", "@, #, ?, !")

    assert decision.correct
    assert decision.extracted == "@, #, ?, !"


def test_normalized_list_accepts_comma_separated_punctuation_symbols():
    decision = score_normalized_list("@, #, ?, !", "@, #, ?, !")

    assert decision.correct
    assert decision.extracted == "@, #, ?, !"
    assert decision.failure_type == "none"
    assert decision.strict_correct


def test_normalized_list_accepts_comma_separated_punctuation_symbol_alternate():
    decision = score_normalized_list("., @, #, ?, !", "., @, #, ?, !")

    assert decision.correct
    assert decision.extracted == "., @, #, ?, !"
    assert decision.failure_type == "none"
    assert decision.strict_correct


def test_normalized_list_does_not_compact_alphanumeric_sequence():
    decision = score_normalized_list("abc", "a, b, c")

    assert not decision.correct
    assert decision.failure_type == "ordering_error"
