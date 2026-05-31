from obviousbench.scorers.multiple_choice import score_multiple_choice_letter


def test_multiple_choice_accepts_single_letter():
    decision = score_multiple_choice_letter("B", "B")

    assert decision.correct
    assert decision.extracted == "B"


def test_multiple_choice_rejects_verbose_output():
    decision = score_multiple_choice_letter("The answer is B", "B")

    assert not decision.correct
    assert decision.failure_type == "verbose_noncompliance"

