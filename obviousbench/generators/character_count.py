"""Character-count variant generation."""

from __future__ import annotations

from random import Random

from obviousbench.datasets.schemas import BenchmarkItem
from obviousbench.generators.ids import make_id
from obviousbench.prompts import FINAL_ANSWER_ONLY_V0, render_prompt

BASE_CASES = [
    ("strawberry", "r", "src_strawberry_public_discussion", False),
    ("mississippi", "s", "src_strawberry_public_discussion", True),
    ("bookkeeper", "e", "src_strawberry_public_discussion", True),
    ("google", "d", "src_google_d_user_screenshot", False),
    ("google", "o", "src_google_d_user_screenshot", True),
    ("google", "g", "src_google_d_user_screenshot", True),
    ("google", "l", "src_google_d_user_screenshot", True),
    ("banana", "a", "src_strawberry_public_discussion", True),
    ("parallel", "l", "src_strawberry_public_discussion", True),
    ("committee", "t", "src_strawberry_public_discussion", True),
    ("cranberry", "r", "src_strawberry_public_discussion", True),
    ("raspberry", "r", "src_strawberry_public_discussion", True),
    ("necessary", "s", "src_strawberry_public_discussion", True),
    ("letterpress", "t", "src_strawberry_public_discussion", True),
]


def generate_character_count_items(
    count: int,
    seed: int,
    split: str = "public_v0",
) -> list[BenchmarkItem]:
    rng = Random(seed)
    cases = list(BASE_CASES)
    if count > len(cases):
        extra_words = [
            "accessibility",
            "bookkeeping",
            "rearrangement",
            "successes",
            "assesses",
            "pepper",
            "terracotta",
            "coconut",
            "alphabetical",
            "responsiveness",
        ]
        letters = "abcdefghijklmnopqrstuvwxyz"
        for word in extra_words:
            for letter in letters:
                if letter in word:
                    cases.append((word, letter, "src_strawberry_public_discussion", True))
    selected = cases[:3] + rng.sample(cases[3:], k=max(0, min(count, len(cases)) - 3))
    selected = selected[:count]

    items: list[BenchmarkItem] = []
    for index, (word, character, source_ref, generated) in enumerate(selected, start=1):
        question = f"How many {character}'s are in {word}?"
        prompt = render_prompt(FINAL_ANSWER_ONLY_V0, question)
        items.append(
            BenchmarkItem.model_validate(
                {
                    "id": make_id("character_count", split, index),
                    "family": "character_count",
                    "subfamily": "single_letter_count",
                    "prompt": prompt,
                    "question": question,
                    "target": str(word.count(character)),
                    "answer_type": "integer",
                    "scorer": "exact_integer_extract_first_v0",
                    "split": split,
                    "source_type": "generated_variant" if generated else "public_archetype",
                    "source_refs": [source_ref],
                    "human_triviality": "H0",
                    "review_status": "reviewed",
                    "metadata": {
                        "word": word,
                        "character": character,
                        "case_sensitive": False,
                        "generated": generated,
                        "variant_of": (
                            None
                            if not generated
                            else make_id("character_count", split, 1)
                        ),
                        "generator": "character_count_generator_v0" if generated else None,
                        "seed": seed if generated else None,
                        "prompt_template_id": FINAL_ANSWER_ONLY_V0,
                        "system_prompt": None,
                        "why_obvious": "Humans can count the visible letters directly.",
                    },
                }
            )
        )
    return items
