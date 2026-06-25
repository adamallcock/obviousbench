from obviousbench.scorers.json_field import score_json_exact_field


def test_json_field_accepts_exact_answer_field():
    decision = score_json_exact_field('{"answer": "3"}', "3")

    assert decision.correct
    assert decision.extracted == "3"


def test_json_field_accepts_json_boolean_literal():
    decision = score_json_exact_field('{"answer": true}', "true")

    assert decision.correct
    assert decision.extracted == "true"
    assert decision.failure_type == "none"


def test_json_field_accepts_byte_token_artifacts_as_wrong_format():
    decision = score_json_exact_field('\u010a\u010a{"answer":\u0120true}', "true")

    assert decision.correct
    assert decision.extracted == "true"
    assert decision.failure_type == "verbose_noncompliance"
    assert not decision.resolved_format_correct


def test_json_field_rejects_malformed_json():
    decision = score_json_exact_field("{answer: 3}", "3")

    assert not decision.correct
    assert decision.failure_type == "json_malformed"


def test_json_field_accepts_fenced_json_block():
    decision = score_json_exact_field('```json\n{"answer": "north"}\n```', "north")

    assert decision.correct
    assert decision.extracted == "north"
    assert decision.failure_type == "verbose_noncompliance"
