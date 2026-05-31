from obviousbench.scorers.json_field import score_json_exact_field


def test_json_field_accepts_exact_answer_field():
    decision = score_json_exact_field('{"answer": "3"}', "3")

    assert decision.correct
    assert decision.extracted == "3"


def test_json_field_rejects_malformed_json():
    decision = score_json_exact_field("{answer: 3}", "3")

    assert not decision.correct
    assert decision.failure_type == "json_malformed"


def test_json_field_accepts_fenced_json_block():
    decision = score_json_exact_field('```json\n{"answer": "north"}\n```', "north")

    assert decision.correct
    assert decision.extracted == "north"
    assert decision.failure_type == "verbose_noncompliance"
