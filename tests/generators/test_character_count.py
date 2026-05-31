from obviousbench.generators.character_count import generate_character_count_items


def test_character_count_generator_is_deterministic():
    first = generate_character_count_items(5, seed=98231)
    second = generate_character_count_items(5, seed=98231)

    assert [item.model_dump(mode="json") for item in first] == [
        item.model_dump(mode="json") for item in second
    ]


def test_character_count_targets_representative_words():
    items = generate_character_count_items(10, seed=98231)
    by_word = {item.metadata.extra["word"]: item for item in items}

    assert by_word["strawberry"].target == "3"
    assert by_word["mississippi"].target == "4"
    assert by_word["bookkeeper"].target == "3"

