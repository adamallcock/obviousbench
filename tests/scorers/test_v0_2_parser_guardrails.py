"""Guardrail fixtures for parser behavior used by v0.2 rebalance analysis."""

from obviousbench.scorers.exact_string import score_exact_string_trim
from obviousbench.scorers.multiple_choice import score_multiple_choice_letter
from obviousbench.scorers.normalized_list import score_normalized_list
from obviousbench.scorers.yes_no import score_yes_no_target


def _strict_format(decision) -> bool:
    return decision.format_correct is not False


def test_yes_no_accepts_bare_answers_case_insensitively() -> None:
    decision = score_yes_no_target("Yes", "yes")
    assert decision.correct is True
    assert _strict_format(decision)
    assert decision.failure_type == "none"


def test_yes_no_wrong_answer_can_still_have_valid_format() -> None:
    for output in ("No", "no"):
        decision = score_yes_no_target(output, "yes")
        assert decision.correct is False
        assert decision.format_correct is True
        assert decision.failure_type == "wrong_letter_or_substring"


def test_yes_no_answer_cue_is_correct_but_not_strict_format() -> None:
    decision = score_yes_no_target("Answer: yes", "yes")
    assert decision.correct is True
    assert decision.format_correct is False
    assert decision.failure_type == "verbose_noncompliance"


def test_yes_no_leading_answer_survives_explanatory_opposite_word() -> None:
    decision = score_yes_no_target(
        "yes\nThe answer is not no because 12.30 equals 12.3.",
        "yes",
    )
    assert decision.correct is True
    assert decision.format_correct is False
    assert decision.failure_type == "verbose_noncompliance"


def test_yes_no_later_answer_cue_conflict_is_ambiguous() -> None:
    decision = score_yes_no_target(
        "yes\nActually, the answer is no.",
        "yes",
    )
    assert decision.correct is False
    assert decision.failure_type == "ambiguous_output"
    assert decision.format_correct is False


def test_multiple_choice_accepts_punctuated_letter_as_strict_format() -> None:
    decision = score_multiple_choice_letter("A.", "A")
    assert decision.correct is True
    assert _strict_format(decision)
    assert decision.failure_type == "none"


def test_multiple_choice_accepts_correct_option_text_as_strict_format() -> None:
    decision = score_multiple_choice_letter(
        "Take the boat there.",
        "A",
        accepted_targets=("Take the boat there",),
    )
    assert decision.correct is True
    assert _strict_format(decision)
    assert decision.failure_type == "none"


def test_multiple_choice_accepts_letter_plus_correct_option_text_as_strict_format() -> None:
    decision = score_multiple_choice_letter(
        "A: Take the boat there",
        "A",
        accepted_targets=("Take the boat there",),
    )
    assert decision.correct is True
    assert _strict_format(decision)
    assert decision.failure_type == "none"


def test_multiple_choice_rejects_wrong_option_text() -> None:
    decision = score_multiple_choice_letter(
        "Walk there instead.",
        "A",
        accepted_targets=("Take the boat there",),
    )
    assert decision.correct is False
    assert decision.failure_type == "format_noncompliance"


def test_normalized_list_accepts_compact_symbol_answer() -> None:
    decision = score_normalized_list("@#?!", "@, #, ?, !")
    assert decision.correct is True
    assert _strict_format(decision)
    assert decision.failure_type == "none"


def test_normalized_list_accepts_leading_list_with_trailing_artifact_as_non_strict() -> None:
    decision = score_normalized_list(
        '-0.4, -0.04, 0.04, 0.4\n"',
        "-0.4, -0.04, 0.04, 0.4",
    )
    assert decision.correct is True
    assert decision.format_correct is False
    assert decision.failure_type == "verbose_noncompliance"


def test_normalized_list_accepts_leading_list_before_explanation_as_non_strict() -> None:
    decision = score_normalized_list(
        "canoe, leaf, twig, drum\n\nSorted by ending letters.",
        "canoe, leaf, twig, drum",
    )
    assert decision.correct is True
    assert decision.format_correct is False
    assert decision.failure_type == "verbose_noncompliance"


def test_exact_string_accepts_repeated_letters_with_separators_as_non_strict() -> None:
    decision = score_exact_string_trim("e, e", "ee")
    assert decision.correct is True
    assert decision.format_correct is False
    assert decision.failure_type == "verbose_noncompliance"


def test_exact_string_rejects_wrong_repeated_letter_count() -> None:
    decision = score_exact_string_trim("e e e", "ee")
    assert decision.correct is False
    assert decision.failure_type == "wrong_letter_or_substring"


def test_exact_string_accepts_remove_letter_explanation_as_non_strict() -> None:
    decision = score_exact_string_trim("ccnut without the letter o", "ccnut")
    assert decision.correct is True
    assert decision.format_correct is False
    assert decision.failure_type == "verbose_noncompliance"


def test_exact_string_accepts_explicit_terminal_period_alternate_as_strict() -> None:
    decision = score_exact_string_trim(
        "END",
        "END.",
        accepted_targets=("END",),
    )
    assert decision.correct is True
    assert _strict_format(decision)
    assert decision.failure_type == "none"
