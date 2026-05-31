#!/usr/bin/env python
"""Generate source-archetype expansion items for underrepresented families."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from obviousbench.datasets.schemas import BenchmarkItem, parse_item_id
from obviousbench.generators.ids import make_id
from obviousbench.prompts import (
    FINAL_ANSWER_ONLY_V0,
    MULTIPLE_CHOICE_LETTER_V0,
    render_prompt,
)

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "public_v0" / "archetype_expansions_2026-05-30.jsonl"


Case = dict[str, Any]


CASES: list[Case] = [
    {
        "family": "arithmetic",
        "subfamily": "unit_conversion_and_small_calc",
        "source_ref": "grok_underrep_20260530_githubnext_gpt4_calc",
        "variants": [
            (
                "Convert 3 miles to kilometers using 1 mile = 1.609 km.",
                "4.827",
                "decimal",
                "exact_string_trim_v0",
            ),
            (
                "How many minutes are in 3.5 hours?",
                "210",
                "integer",
                "exact_integer_extract_first_v0",
            ),
            ("What is 18 multiplied by 7?", "126", "integer", "exact_integer_extract_first_v0"),
            ("Convert 750 grams to kilograms.", "0.75", "decimal", "exact_string_trim_v0"),
            ("What is 42 + 29 - 11?", "60", "integer", "exact_integer_extract_first_v0"),
        ],
    },
    {
        "family": "ordering",
        "subfamily": "numeric_sort",
        "source_ref": "grok_underrep_20260530_reddit_sort_numbers",
        "variants": [
            ("Sort these numbers from smallest to largest: 7, 2, 10, 1.", "1, 2, 7, 10"),
            ("Sort these numbers from smallest to largest: 3.1, 3.01, 3.2.", "3.01, 3.1, 3.2"),
            ("Sort these numbers from smallest to largest: -1, 4, 0, -3.", "-3, -1, 0, 4"),
            ("Sort these numbers from smallest to largest: 12, 2, 21, 1.", "1, 2, 12, 21"),
            ("Sort these numbers from smallest to largest: 5.5, 5.05, 5.15.", "5.05, 5.15, 5.5"),
        ],
        "answer_type": "list",
        "scorer": "normalized_list_v0",
    },
    {
        "family": "ordering",
        "subfamily": "alphabetical_sort",
        "source_ref": "grok_underrep_20260530_linkedin_alphabetize_words",
        "variants": [
            (
                "Sort these words alphabetically: plum, apple, pear, banana.",
                "apple, banana, pear, plum",
            ),
            ("Sort these words alphabetically: cab, car, cat, cap.", "cab, cap, car, cat"),
            (
                "Sort these words alphabetically: delta, alpha, charlie, bravo.",
                "alpha, bravo, charlie, delta",
            ),
            (
                "Sort these words alphabetically: mango, melon, mint, maple.",
                "mango, maple, melon, mint",
            ),
            (
                "Sort these words alphabetically: blue, black, brown, beige.",
                "beige, black, blue, brown",
            ),
        ],
        "answer_type": "list",
        "scorer": "normalized_list_v0",
    },
    {
        "family": "spelling_transform",
        "subfamily": "reverse_word",
        "source_ref": "grok_underrep_20260530_reddit_reverse_words",
        "variants": [
            ("Spell planet backwards.", "tenalp"),
            ("Spell orange backwards.", "egnaro"),
            ("Spell window backwards.", "wodniw"),
            ("Spell cabinet backwards.", "tenibac"),
            ("Spell bicycle backwards.", "elcycib"),
        ],
    },
    {
        "family": "negation",
        "subfamily": "not_choice",
        "source_ref": "grok_underrep_20260530_quanta_negation",
        "template_id": MULTIPLE_CHOICE_LETTER_V0,
        "variants": [
            (
                "Which word does not contain the letter a?",
                ["apple", "chair", "stone", "table"],
                "C",
            ),
            ("Which number is not odd?", ["3", "7", "10", "15"], "C"),
            ("Which item is not a color?", ["blue", "green", "circle", "red"], "C"),
            ("Which word is not lowercase?", ["river", "cloud", "NASA", "paper"], "C"),
            ("Which animal does not have legs?", ["dog", "horse", "snake", "cat"], "C"),
        ],
        "answer_type": "multiple_choice",
        "scorer": "multiple_choice_letter_v0",
    },
    {
        "family": "format_compliance",
        "subfamily": "exact_json_schema",
        "source_ref": "grok_underrep_20260530_local_llama_json_break",
        "variants": [
            ('Return a JSON object with exactly one key, "answer", whose value is "blue".', "blue"),
            ('Return a JSON object with exactly one key, "answer", whose value is "17".', "17"),
            ('Return a JSON object with exactly one key, "answer", whose value is "cat".', "cat"),
            (
                'Return a JSON object with exactly one key, "answer", whose value is "north".',
                "north",
            ),
            ('Return a JSON object with exactly one key, "answer", whose value is "true".', "true"),
        ],
        "answer_type": "json",
        "scorer": "json_exact_field_v0",
        "metadata": {"strict_format": True, "json_field": "answer"},
    },
    {
        "family": "word_count",
        "subfamily": "sentence_word_count",
        "source_ref": "grok_underrep_20260530_claude_word_count_fail",
        "variants": [
            ("How many words are in 'A red kite flew above the hill'?", "7"),
            ("How many words are in 'Simple tests often reveal stubborn mistakes'?", "6"),
            ("How many words are in 'The quiet library closes at nine tonight'?", "7"),
            ("How many words are in 'Every small detail still matters here'?", "6"),
            ("How many words are in 'Three blue cups sat beside four plates'?", "7"),
        ],
        "answer_type": "integer",
        "scorer": "word_count_v0",
    },
    {
        "family": "format_compliance",
        "subfamily": "instruction_conflict",
        "source_ref": "grok_underrep_20260530_conflicting_instructions_blog",
        "variants": [
            (
                "The first instruction says output BLUE. "
                "The final instruction says output RED. "
                "Output only the final requested color.",
                "RED",
            ),
            (
                "The first instruction says output CAT. "
                "The final instruction says output DOG. "
                "Output only the final requested animal.",
                "DOG",
            ),
            (
                "The first instruction says output 12. "
                "The final instruction says output 21. "
                "Output only the final requested number.",
                "21",
            ),
            (
                "The first instruction says output NORTH. "
                "The final instruction says output SOUTH. "
                "Output only the final requested direction.",
                "SOUTH",
            ),
            (
                "The first instruction says output TRUE. "
                "The final instruction says output FALSE. "
                "Output only the final requested boolean.",
                "FALSE",
            ),
        ],
        "answer_type": "string",
        "scorer": "exact_string_trim_v0",
        "metadata": {"strict_format": True},
    },
    {
        "family": "negation",
        "subfamily": "without_constraint",
        "source_ref": "grok_underrep_20260530_ai_negation_struggle",
        "variants": [
            ("Choose the word without the letter e: peach, melon, plum, cherry.", "plum"),
            ("Choose the item that is not made of metal: spoon, nail, paper, coin.", "paper"),
            (
                "Choose the shape that does not have corners: square, triangle, circle, rectangle.",
                "circle",
            ),
            (
                "Choose the month that is not in winter in the northern hemisphere: "
                "January, July, February, December.",
                "July",
            ),
            ("Choose the number that is not greater than 10: 14, 22, 9, 18.", "9"),
        ],
    },
    {
        "family": "word_count",
        "subfamily": "comma_list_count",
        "source_ref": "grok_underrep_20260530_chatgpt_wordcount_community",
        "variants": [
            (
                "How many comma-separated values are shown here: red, blue, green, yellow, purple?",
                "5",
            ),
            ("How many comma-separated values are shown here: alpha, beta, gamma?", "3"),
            ("How many comma-separated values are shown here: north, south, east, west?", "4"),
            (
                "How many comma-separated values are shown here: "
                "tea, coffee, water, juice, milk, soda?",
                "6",
            ),
            (
                "How many comma-separated values are shown here: "
                "Monday, Tuesday, Wednesday, Thursday?",
                "4",
            ),
        ],
        "answer_type": "integer",
        "scorer": "word_count_v0",
    },
]


def current_max_indexes() -> dict[str, int]:
    max_by_family: dict[str, int] = {}
    for path in sorted((ROOT / "data" / "public_v0").glob("*.jsonl")):
        if path == OUTPUT:
            continue
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            record = json.loads(line)
            parsed = parse_item_id(record["id"])
            family = record["family"]
            max_by_family[family] = max(max_by_family.get(family, 0), parsed.index)
    return max_by_family


def make_item(case: Case, variant: Any, index: int) -> BenchmarkItem:
    template_id = case.get("template_id", FINAL_ANSWER_ONLY_V0)
    metadata = {
        "generated": True,
        "variant_of": case["source_ref"],
        "prompt_template_id": template_id,
        "system_prompt": None,
        "choices": None,
        "generator": "scripts/generate_underrepresented_expansions.py",
        "strict_format": bool(case.get("metadata", {}).get("strict_format", False)),
        "why_obvious": "A person can answer this by direct inspection or simple mental work.",
    }
    metadata.update(case.get("metadata", {}))

    if template_id == MULTIPLE_CHOICE_LETTER_V0:
        question, choices, target = variant
        metadata["choices"] = choices
        prompt = render_prompt(template_id, question, choices)
        answer_type = case["answer_type"]
        scorer = case["scorer"]
    else:
        question = variant[0]
        target = variant[1]
        prompt = render_prompt(template_id, question, None)
        answer_type = variant[2] if len(variant) > 2 else case.get("answer_type", "string")
        scorer = variant[3] if len(variant) > 3 else case.get("scorer", "exact_string_trim_v0")

    return BenchmarkItem.model_validate(
        {
            "id": make_id(case["family"], "public_v0", index),
            "family": case["family"],
            "subfamily": case["subfamily"],
            "prompt": prompt,
            "question": question,
            "target": target,
            "answer_type": answer_type,
            "scorer": scorer,
            "split": "public_v0",
            "source_type": "generated_variant",
            "source_refs": [case["source_ref"]],
            "human_triviality": "H0",
            "review_status": "reviewed",
            "metadata": metadata,
        }
    )


def main() -> int:
    indexes = current_max_indexes()
    rows: list[BenchmarkItem] = []
    for case in CASES:
        family = case["family"]
        next_index = indexes.get(family, 0) + 1
        for variant in case["variants"]:
            rows.append(make_item(case, variant, next_index))
            next_index += 1
        indexes[family] = next_index - 1

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(
        "\n".join(json.dumps(row.model_dump(mode="json"), sort_keys=True) for row in rows) + "\n",
        encoding="utf-8",
    )
    print(f"wrote {len(rows)} items to {OUTPUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
