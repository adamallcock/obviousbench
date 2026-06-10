#!/usr/bin/env python
"""Build the absent-substring count experiment corpus."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/experiments/2026-06-07-substring-absent-count-suite.jsonl"


def item(
    slug: str,
    collection_label: str,
    collection: list[str],
    needle: str,
    item_type: str = "absent_zero",
    lure_type: str = "lexical_absence",
    include_now: bool = True,
) -> dict[str, object]:
    matches = [value for value in collection if needle.lower() in value.lower()]
    target = len(matches)
    if item_type == "absent_zero" and target != 0:
        raise ValueError(f"{slug}: absent_zero item has matches: {matches}")
    if item_type.startswith("positive_control") and target <= 0:
        raise ValueError(f"{slug}: positive control has no matches")

    listed = ", ".join(collection)
    question = (
        f"How many of these {collection_label} contain the exact letter "
        f'sequence "{needle}": {listed}?'
    )
    why = (
        "A person can scan the explicitly listed finite set and count exact "
        "case-insensitive substring matches."
    )
    return {
        "answer_type": "integer",
        "family": "character_count",
        "human_triviality": "H0",
        "id": "pending",
        "metadata": {
            "case_sensitive": False,
            "choices": None,
            "collection": collection,
            "collection_label": collection_label,
            "collection_size": len(collection),
            "decoy_category": lure_type,
            "generated": True,
            "generator": "scripts/build_substring_absent_count_suite.py",
            "include_now": include_now,
            "item_slug": slug,
            "item_type": item_type,
            "lure_type": lure_type,
            "matching_rule": (
                "contiguous substring; case-insensitive; do not rewrite collection items"
            ),
            "matches": matches,
            "needle": needle,
            "needle_length": len(needle),
            "normalization": "case_insensitive_raw_substring",
            "positive_control": item_type.startswith("positive_control"),
            "prompt_template_id": "final_answer_only_v0",
            "question_lists_collection": True,
            "seed": 20260607,
            "strict_format": False,
            "system_prompt": None,
            "target_zero": target == 0,
            "variant_of": None,
            "why_obvious": why,
        },
        "prompt": (
            "Answer the question. Return only the final answer, with no explanation.\n\n"
            f"Question: {question}\n"
            "Answer:"
        ),
        "question": question,
        "review_status": "reviewed",
        "scorer": "exact_integer_extract_first_v0",
        "source_refs": ["src_2026_06_07_substring_absent_count_suite_hand_authored"],
        "source_type": "hand_authored",
        "split": "private_v0",
        "subfamily": "substring_absent_count",
        "target": str(target),
    }


def absent(
    slug: str, label: str, collection: list[str], needle: str, lure: str
) -> dict[str, object]:
    return item(slug, label, collection, needle, item_type="absent_zero", lure_type=lure)


def positive(
    slug: str,
    label: str,
    collection: list[str],
    needle: str,
    lure: str = "positive_control",
) -> dict[str, object]:
    return item(
        slug,
        label,
        collection,
        needle,
        item_type="positive_control",
        lure_type=lure,
    )


def build_items() -> list[dict[str, object]]:
    raw: list[dict[str, object]] = []

    raw.extend(
        [
            absent(
                "days_toe",
                "day names",
                ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
                "toe",
                "near_miss_rewrite",
            ),
            absent(
                "months_qq",
                "month names",
                [
                    "January",
                    "February",
                    "March",
                    "April",
                    "May",
                    "June",
                    "July",
                    "August",
                    "September",
                    "October",
                    "November",
                    "December",
                ],
                "qq",
                "impossible_bigram",
            ),
            absent(
                "planets_fish",
                "planet names",
                ["Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune"],
                "fish",
                "semantic_lure",
            ),
            absent(
                "rainbow_car",
                "rainbow colors",
                ["red", "orange", "yellow", "green", "blue", "indigo", "violet"],
                "car",
                "semantic_lure",
            ),
            absent(
                "seasons_box",
                "season names",
                ["spring", "summer", "autumn", "winter"],
                "box",
                "semantic_lure",
            ),
            absent(
                "numbers_cat",
                "number words from one to ten",
                ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"],
                "cat",
                "semantic_lure",
            ),
            absent(
                "directions_up",
                "cardinal directions",
                ["north", "east", "south", "west"],
                "up",
                "spatial_semantic_lure",
            ),
            absent(
                "nato_zoo",
                "NATO alphabet words",
                ["alpha", "bravo", "charlie", "delta", "echo", "foxtrot"],
                "zoo",
                "semantic_lure",
            ),
            absent(
                "shapes_dog",
                "shape names",
                ["circle", "square", "triangle", "rectangle"],
                "dog",
                "semantic_lure",
            ),
            absent(
                "elements_pizza",
                "chemical element names",
                [
                    "hydrogen",
                    "helium",
                    "lithium",
                    "beryllium",
                    "boron",
                    "carbon",
                    "nitrogen",
                    "oxygen",
                    "fluorine",
                    "neon",
                ],
                "pizza",
                "semantic_lure",
            ),
            absent(
                "vowels_z", "vowel letters", ["a", "e", "i", "o", "u"], "z", "single_letter_absence"
            ),
            absent(
                "first_letters_cat",
                "letters from a to f",
                ["a", "b", "c", "d", "e", "f"],
                "cat",
                "multi_char_absence",
            ),
            absent(
                "ordinals_dog",
                "ordinal words",
                ["first", "second", "third", "fourth", "fifth", "sixth"],
                "dog",
                "semantic_lure",
            ),
            absent(
                "primary_colors_fish",
                "primary colors",
                ["red", "yellow", "blue"],
                "fish",
                "semantic_lure",
            ),
            absent(
                "secondary_colors_cat",
                "secondary colors",
                ["orange", "green", "purple"],
                "cat",
                "semantic_lure",
            ),
            absent(
                "chess_pieces_cat",
                "chess piece names",
                ["king", "queen", "rook", "bishop", "knight", "pawn"],
                "cat",
                "semantic_lure",
            ),
            absent(
                "card_suits_fish",
                "card suit names",
                ["hearts", "diamonds", "clubs", "spades"],
                "fish",
                "semantic_lure",
            ),
            absent(
                "musical_notes_cat",
                "musical note names",
                ["A", "B", "C", "D", "E", "F", "G"],
                "cat",
                "multi_char_absence",
            ),
            absent(
                "solfege_cat",
                "solfege syllables",
                ["do", "re", "mi", "fa", "sol", "la", "ti"],
                "cat",
                "semantic_lure",
            ),
            absent(
                "si_units_fish",
                "SI base unit names",
                ["meter", "kilogram", "second", "ampere", "kelvin", "mole", "candela"],
                "fish",
                "semantic_lure",
            ),
            absent(
                "metric_prefixes_zoo",
                "metric prefix names",
                ["milli", "centi", "deci", "deka", "hecto", "kilo", "mega", "giga"],
                "zoo",
                "semantic_lure",
            ),
            absent(
                "languages_cat",
                "programming language names",
                ["Python", "Java", "Ruby", "Go", "Rust", "Swift", "Kotlin"],
                "cat",
                "semantic_lure",
            ),
            absent(
                "file_extensions_cat",
                "file extension names",
                ["txt", "csv", "json", "xml", "yaml"],
                "cat",
                "multi_char_absence",
            ),
            absent(
                "http_methods_cat",
                "HTTP method names",
                ["GET", "POST", "PUT", "PATCH", "DELETE"],
                "cat",
                "near_subsequence_lure",
            ),
            absent(
                "crud_box",
                "CRUD action names",
                ["create", "read", "update", "delete"],
                "box",
                "semantic_lure",
            ),
            absent(
                "intercardinal_up",
                "intercardinal directions",
                ["northeast", "southeast", "southwest", "northwest"],
                "up",
                "spatial_semantic_lure",
            ),
            absent(
                "coins_box",
                "US coin names",
                ["penny", "nickel", "dime", "quarter"],
                "box",
                "semantic_lure",
            ),
            absent(
                "bills_cat",
                "US bill value names",
                ["one", "five", "ten", "twenty", "fifty", "hundred"],
                "cat",
                "semantic_lure",
            ),
            absent(
                "traffic_car",
                "traffic light colors",
                ["red", "yellow", "green"],
                "car",
                "semantic_lure",
            ),
            absent(
                "body_parts_cat",
                "body part names",
                ["head", "arm", "leg", "hand", "foot"],
                "cat",
                "semantic_lure",
            ),
            absent(
                "fingers_box",
                "finger names",
                ["thumb", "index", "middle", "ring", "little"],
                "box",
                "semantic_lure",
            ),
            absent(
                "senses_dog",
                "sense names",
                ["sight", "hearing", "smell", "taste", "touch"],
                "dog",
                "semantic_lure",
            ),
            absent(
                "tastes_cat",
                "basic taste names",
                ["sweet", "sour", "salty", "bitter", "umami"],
                "cat",
                "semantic_lure",
            ),
            absent(
                "school_subjects_toe",
                "school subject names",
                ["math", "science", "history", "art", "music"],
                "toe",
                "semantic_lure",
            ),
            absent(
                "punctuation_cat",
                "punctuation mark names",
                ["comma", "period", "colon", "semicolon", "question mark", "exclamation point"],
                "cat",
                "near_subsequence_lure",
            ),
            absent(
                "greek_first_ten_dog",
                "Greek letter names",
                [
                    "alpha",
                    "beta",
                    "gamma",
                    "delta",
                    "epsilon",
                    "zeta",
                    "eta",
                    "theta",
                    "iota",
                    "kappa",
                ],
                "dog",
                "semantic_lure",
            ),
            absent(
                "roman_symbols_cat",
                "Roman numeral symbols",
                ["I", "V", "X", "L", "C", "D", "M"],
                "cat",
                "multi_char_absence",
            ),
            absent(
                "html_tags_cat",
                "HTML tag names",
                ["div", "span", "p", "a", "ul", "li"],
                "cat",
                "semantic_lure",
            ),
            absent(
                "css_units_cat",
                "CSS unit names",
                ["px", "em", "rem", "vw", "vh", "percent"],
                "cat",
                "multi_char_absence",
            ),
            absent(
                "sql_commands_box",
                "SQL command names",
                ["select", "insert", "update", "delete", "create", "drop"],
                "box",
                "semantic_lure",
            ),
            absent("boolean_words_cat", "Boolean words", ["true", "false"], "cat", "semantic_lure"),
            absent(
                "binary_digits_cat", "binary digit words", ["zero", "one"], "cat", "semantic_lure"
            ),
            absent(
                "calendar_quarters_dog",
                "calendar quarter labels",
                ["Q1", "Q2", "Q3", "Q4"],
                "dog",
                "multi_char_absence",
            ),
            absent(
                "game_results_cat",
                "game result words",
                ["win", "loss", "draw"],
                "cat",
                "semantic_lure",
            ),
            absent(
                "weather_words_car",
                "weather words",
                ["sunny", "cloudy", "rainy", "windy", "snowy"],
                "car",
                "semantic_lure",
            ),
            absent(
                "cloud_types_dog",
                "cloud type names",
                ["cirrus", "cumulus", "stratus", "nimbus"],
                "dog",
                "semantic_lure",
            ),
            absent(
                "rock_types_cat",
                "rock type names",
                ["igneous", "sedimentary", "metamorphic"],
                "cat",
                "semantic_lure",
            ),
            absent(
                "earth_layers_box",
                "Earth layer names",
                ["crust", "mantle", "outer core", "inner core"],
                "box",
                "semantic_lure",
            ),
            absent(
                "ocean_names_cat",
                "ocean names",
                ["Pacific", "Atlantic", "Indian", "Southern", "Arctic"],
                "cat",
                "near_subsequence_lure",
            ),
            absent(
                "continents_fish",
                "continent names",
                [
                    "Africa",
                    "Antarctica",
                    "Asia",
                    "Europe",
                    "North America",
                    "South America",
                    "Australia",
                ],
                "fish",
                "semantic_lure",
            ),
            absent(
                "tree_parts_dog",
                "tree part names",
                ["root", "trunk", "branch", "leaf", "bark"],
                "dog",
                "semantic_lure",
            ),
            absent(
                "flower_parts_box",
                "flower part names",
                ["petal", "sepal", "stamen", "pistil"],
                "box",
                "semantic_lure",
            ),
            absent(
                "animal_classes_pizza",
                "animal class names",
                ["mammal", "bird", "reptile", "amphibian", "fish"],
                "pizza",
                "semantic_lure",
            ),
            absent(
                "farm_animals_cat",
                "farm animal names",
                ["cow", "pig", "goat", "sheep", "horse"],
                "cat",
                "semantic_lure",
            ),
            absent(
                "vehicles_car",
                "vehicle names",
                ["bus", "train", "bicycle", "scooter", "tram"],
                "car",
                "semantic_lure",
            ),
            absent(
                "furniture_bed",
                "furniture names",
                ["chair", "table", "sofa", "desk", "shelf"],
                "bed",
                "semantic_lure",
            ),
            absent(
                "utensils_pan",
                "kitchen utensil names",
                ["fork", "spoon", "knife", "ladle", "tongs"],
                "pan",
                "semantic_lure",
            ),
            absent(
                "fruits_pie",
                "fruit names",
                ["apple", "banana", "cherry", "grape", "melon"],
                "pie",
                "semantic_lure",
            ),
            absent(
                "vegetables_cake",
                "vegetable names",
                ["carrot", "pea", "onion", "lettuce", "celery"],
                "cake",
                "semantic_lure",
            ),
            absent(
                "beverages_dog",
                "beverage names",
                ["water", "tea", "coffee", "juice", "milk"],
                "dog",
                "semantic_lure",
            ),
            absent(
                "tools_cat",
                "tool names",
                ["hammer", "saw", "wrench", "pliers", "drill"],
                "cat",
                "semantic_lure",
            ),
            absent(
                "materials_fish",
                "material names",
                ["wood", "metal", "glass", "plastic", "stone"],
                "fish",
                "semantic_lure",
            ),
            absent(
                "emotions_box",
                "emotion words",
                ["happy", "sad", "angry", "afraid", "calm"],
                "box",
                "semantic_lure",
            ),
            absent(
                "virtues_cat",
                "virtue words",
                ["honesty", "courage", "patience", "kindness", "humility"],
                "cat",
                "semantic_lure",
            ),
        ]
    )

    raw.extend(
        [
            positive(
                "days_tue",
                "day names",
                ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
                "tue",
                "positive_control_near_miss",
            ),
            positive(
                "months_jan",
                "month names",
                [
                    "January",
                    "February",
                    "March",
                    "April",
                    "May",
                    "June",
                    "July",
                    "August",
                    "September",
                    "October",
                    "November",
                    "December",
                ],
                "jan",
            ),
            positive(
                "planets_mars",
                "planet names",
                ["Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune"],
                "mars",
            ),
            positive(
                "rainbow_red",
                "rainbow colors",
                ["red", "orange", "yellow", "green", "blue", "indigo", "violet"],
                "red",
            ),
            positive(
                "seasons_mer",
                "season names",
                ["spring", "summer", "autumn", "winter"],
                "mer",
                "positive_control_sticky_domain",
            ),
            positive(
                "numbers_six",
                "number words from one to ten",
                ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"],
                "six",
            ),
            positive(
                "directions_th",
                "cardinal directions",
                ["north", "east", "south", "west"],
                "th",
                "positive_control_sticky_domain",
            ),
            positive(
                "nato_x",
                "NATO alphabet words",
                ["alpha", "bravo", "charlie", "delta", "echo", "foxtrot"],
                "x",
            ),
            positive(
                "shapes_angle",
                "shape names",
                ["circle", "square", "triangle", "rectangle"],
                "angle",
            ),
            positive(
                "elements_bor",
                "chemical element names",
                [
                    "hydrogen",
                    "helium",
                    "lithium",
                    "beryllium",
                    "boron",
                    "carbon",
                    "nitrogen",
                    "oxygen",
                    "fluorine",
                    "neon",
                ],
                "bor",
            ),
            positive(
                "greek_eta",
                "Greek letter names",
                [
                    "alpha",
                    "beta",
                    "gamma",
                    "delta",
                    "epsilon",
                    "zeta",
                    "eta",
                    "theta",
                    "iota",
                    "kappa",
                ],
                "eta",
            ),
            positive(
                "http_patch",
                "HTTP method names",
                ["GET", "POST", "PUT", "PATCH", "DELETE"],
                "patch",
            ),
            positive(
                "sql_select",
                "SQL command names",
                ["select", "insert", "update", "delete", "create", "drop"],
                "select",
            ),
            positive(
                "weather_sun",
                "weather words",
                ["sunny", "cloudy", "rainy", "windy", "snowy"],
                "sun",
            ),
            positive(
                "fruits_app", "fruit names", ["apple", "banana", "cherry", "grape", "melon"], "app"
            ),
            positive(
                "tools_saw", "tool names", ["hammer", "saw", "wrench", "pliers", "drill"], "saw"
            ),
        ]
    )

    return raw


def main() -> int:
    raw = build_items()
    if len(raw) != 80:
        raise ValueError(f"expected 80 items, got {len(raw)}")

    for index, record in enumerate(raw, start=1):
        record["id"] = f"obviousbench.char_count.en.v0.private.{100000 + index:06d}"

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(
        "\n".join(json.dumps(record, sort_keys=True, separators=(",", ":")) for record in raw)
        + "\n",
        encoding="utf-8",
    )

    zeros = sum(1 for record in raw if record["target"] == "0")
    positives = len(raw) - zeros
    print(f"Wrote {OUT}")
    print(f"items={len(raw)} absent_zero={zeros} positive_controls={positives}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
