"""Simple arithmetic item generation."""

from obviousbench.datasets.schemas import BenchmarkItem
from obviousbench.generators.ids import make_id
from obviousbench.prompts import FINAL_ANSWER_ONLY_V0, render_prompt

CASES = [
    ("What is 17 + 8 - 3?", "22", "integer", "arithmetic_error"),
    ("Which is larger, 9.9 or 9.11?", "9.9", "decimal", "numeric_comparison_error"),
    ("What is 6 * 7?", "42", "integer", "arithmetic_error"),
    ("What is half of 42?", "21", "integer", "arithmetic_error"),
    ("What is 12 + 3?", "15", "integer", "arithmetic_error"),
]


def generate_arithmetic_items(
    split: str = "public_v0",
    start_index: int = 1,
) -> list[BenchmarkItem]:
    items: list[BenchmarkItem] = []
    for offset, (question, target, answer_type, _failure_type) in enumerate(CASES):
        items.append(
            BenchmarkItem.model_validate(
                {
                    "id": make_id("arithmetic", split, start_index + offset),
                    "family": "arithmetic",
                    "subfamily": "simple_arithmetic",
                    "prompt": render_prompt(FINAL_ANSWER_ONLY_V0, question),
                    "question": question,
                    "target": target,
                    "answer_type": answer_type,
                    "scorer": "exact_integer_extract_first_v0"
                    if answer_type == "integer"
                    else "exact_string_trim_v0",
                    "split": split,
                    "source_type": "generated_variant",
                    "source_refs": ["src_easy_problems_prior_art"],
                    "human_triviality": "H0",
                    "review_status": "reviewed",
                    "metadata": {
                        "generated": True,
                        "variant_of": None,
                        "generator": "arithmetic_generator_v0",
                        "seed": None,
                        "prompt_template_id": FINAL_ANSWER_ONLY_V0,
                        "system_prompt": None,
                        "why_obvious": "The arithmetic is small enough to compute mentally.",
                    },
                }
            )
        )
    return items
