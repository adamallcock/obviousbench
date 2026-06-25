from obviousbench.scorers.word_count import score_word_count


def test_word_count_accepts_integer():
    decision = score_word_count("5", "5")

    assert decision.correct


def test_word_count_rejects_wrong_integer():
    decision = score_word_count("4", "5")

    assert not decision.correct
    assert decision.failure_type == "list_count_error"

