from obviousbench.scorers.regex_match import score_regex_match


def test_yes_no_regex_accepts_terminal_punctuation_as_wrong_format():
    decision = score_regex_match("Yes.", "(?i)yes")

    assert decision.correct
    assert decision.extracted == "Yes"
    assert decision.failure_type == "verbose_noncompliance"
    assert not decision.resolved_format_correct


def test_yes_no_regex_treats_wrong_yes_no_answer_as_valid_format():
    decision = score_regex_match("No", "(?i)yes")

    assert not decision.correct
    assert decision.extracted == "No"
    assert decision.failure_type == "wrong_letter_or_substring"
    assert decision.resolved_format_correct


def test_yes_no_regex_treats_lowercase_wrong_answer_as_valid_format():
    decision = score_regex_match("no", "(?i)yes")

    assert not decision.correct
    assert decision.extracted == "no"
    assert decision.failure_type == "wrong_letter_or_substring"
    assert decision.resolved_format_correct


def test_yes_no_regex_accepts_answer_prefix_as_wrong_format():
    decision = score_regex_match("Answer: yes", "(?i)yes")

    assert decision.correct
    assert decision.extracted == "yes"
    assert decision.failure_type == "verbose_noncompliance"
    assert not decision.resolved_format_correct


def test_yes_no_regex_empty_output_is_not_format_correct():
    decision = score_regex_match("", "(?i)yes")

    assert not decision.correct
    assert decision.extracted is None
    assert decision.failure_type == "non_answer"
    assert not decision.resolved_format_correct


def test_regex_match_accepts_leading_matching_answer_as_wrong_format():
    decision = score_regex_match(
        "yes\n\n12.30 and 12.3 are equal because trailing zeros do not change value.",
        "(?i)yes",
    )

    assert decision.correct
    assert decision.extracted == "yes"
    assert decision.failure_type == "verbose_noncompliance"
    assert not decision.resolved_format_correct


def test_regex_match_rejects_wrong_leading_answer_that_mentions_target_later():
    decision = score_regex_match(
        "no\n\nThe correct response would have been yes.",
        "(?i)yes",
    )

    assert not decision.correct
    assert decision.extracted == "no"
    assert decision.failure_type == "ambiguous_output"
