from obviousbench.generators.arithmetic import generate_arithmetic_items


def test_arithmetic_generator_has_exact_targets():
    items = generate_arithmetic_items()
    by_question = {item.question: item for item in items}

    assert by_question["What is 17 + 8 - 3?"].target == "22"
    assert by_question["Which is larger, 9.9 or 9.11?"].target == "9.9"
    assert by_question["What is half of 42?"].target == "21"

