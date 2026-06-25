import pytest

from obviousbench.scorers.exact_integer import score_exact_integer_extract_first


@pytest.mark.parametrize(
    ("output", "target", "correct", "extracted", "failure_type"),
    [
        ("3", "3", True, "3", "none"),
        ("There are 3.", "3", True, "3", "none"),
        ("5,000 milliliters", "5000", True, "5000", "none"),
        ("There are 2 r's.", "3", False, "2", "incorrect_count"),
        ("There are two.", "3", False, "2", "incorrect_count"),
        ("four days", "6", False, "4", "incorrect_count"),
        ("", "3", False, None, "non_answer"),
        ("three", "3", True, "3", "none"),
        ("3\n\nPositions 1, 7, and 8 contain r.", "3", True, "3", "verbose_noncompliance"),
        ("210\n\n\\confidence{90}", "210", True, "210", "verbose_noncompliance"),
        (
            "0 g's\n\nThere is 1 g in rearrangement.\n\nThe answer is **1**.",
            "1",
            True,
            "1",
            "verbose_noncompliance",
        ),
        ("2 or 3", "3", False, None, "ambiguous_output"),
        ("one d in four days", "6", False, None, "ambiguous_output"),
    ],
)
def test_exact_integer_extraction(output, target, correct, extracted, failure_type):
    decision = score_exact_integer_extract_first(output, target)

    assert decision.correct is correct
    assert decision.extracted == extracted
    assert decision.failure_type == failure_type
