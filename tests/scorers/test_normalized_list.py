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


def test_normalized_list_rejects_wrong_order():
    decision = score_normalized_list("9, 3, 12", "3, 9, 12")

    assert not decision.correct
    assert decision.failure_type == "ordering_error"
