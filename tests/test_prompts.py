import pytest

from obviousbench.prompts import render_prompt


def test_final_answer_only_prompt_matches_policy_exactly():
    assert render_prompt(
        "final_answer_only_v0",
        "How many r's are in strawberry?",
    ) == (
        "Answer the question. Return only the final answer, with no explanation.\n\n"
        "Question: How many r's are in strawberry?\n"
        "Answer:"
    )


def test_multiple_choice_prompt_matches_policy_exactly():
    assert render_prompt(
        "multiple_choice_letter_v0",
        "Which word contains the letter e?",
        ["cat", "dog", "tree", "sun"],
    ) == (
        "Answer the question. Return only the letter of the correct option.\n\n"
        "Question: Which word contains the letter e?\n\n"
        "A. cat\n"
        "B. dog\n"
        "C. tree\n"
        "D. sun\n\n"
        "Answer:"
    )


@pytest.mark.parametrize("choices", [[], ["A"], ["A", "B", "C"], ["A", "B", "C", "D", "E"]])
def test_multiple_choice_requires_exactly_four_choices(choices):
    with pytest.raises(ValueError, match="exactly four"):
        render_prompt("multiple_choice_letter_v0", "Question?", choices)


def test_unknown_prompt_template_fails_clearly():
    with pytest.raises(ValueError, match="Unknown prompt template"):
        render_prompt("unknown_v0", "Question?")

