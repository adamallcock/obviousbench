#!/usr/bin/env python
"""Build the expanded absent-substring count experiment corpus."""

from __future__ import annotations

import json
from pathlib import Path

from build_substring_absent_count_suite import absent, build_items, positive

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/experiments/2026-06-07-substring-absent-count-suite-expanded.jsonl"


def item_fingerprint(record: dict[str, object]) -> tuple[str, tuple[str, ...], str]:
    metadata = record["metadata"]
    if not isinstance(metadata, dict):
        raise TypeError("metadata must be a dict")
    collection = metadata["collection"]
    if not isinstance(collection, list):
        raise TypeError("metadata.collection must be a list")
    return (
        str(metadata["collection_label"]).casefold(),
        tuple(str(value).casefold() for value in collection),
        str(metadata["needle"]).casefold(),
    )


def append_unique(
    records: list[dict[str, object]],
    candidates: list[dict[str, object]],
) -> tuple[int, int]:
    seen = {item_fingerprint(record) for record in records}
    slugs = {
        str(record["metadata"]["item_slug"])
        for record in records
        if isinstance(record.get("metadata"), dict)
    }
    added = 0
    skipped = 0
    for candidate in candidates:
        slug = str(candidate["metadata"]["item_slug"])
        fingerprint = item_fingerprint(candidate)
        if slug in slugs or fingerprint in seen:
            skipped += 1
            continue
        records.append(candidate)
        slugs.add(slug)
        seen.add(fingerprint)
        added += 1
    return added, skipped


def pasted_answer_candidates() -> list[dict[str, object]]:
    return [
        absent(
            "days_axe",
            "day names",
            ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
            "axe",
            "lexical_absence",
        ),
        absent(
            "days_moon",
            "day names",
            ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
            "moon",
            "near_miss_lure",
        ),
        absent(
            "months_mars",
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
            "mars",
            "near_miss_lure",
        ),
        absent(
            "months_toe",
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
            "toe",
            "lexical_absence",
        ),
        absent(
            "months_cat",
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
            "cat",
            "lexical_absence",
        ),
        absent(
            "planets_pluto",
            "planet names",
            ["Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune"],
            "pluto",
            "semantic_lure",
        ),
        absent(
            "planets_sun",
            "planet names",
            ["Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune"],
            "sun",
            "semantic_lure",
        ),
        absent(
            "rainbow_black",
            "rainbow colors",
            ["red", "orange", "yellow", "green", "blue", "indigo", "violet"],
            "black",
            "semantic_lure",
        ),
        absent(
            "rainbow_zz",
            "rainbow colors",
            ["red", "orange", "yellow", "green", "blue", "indigo", "violet"],
            "zz",
            "impossible_bigram",
        ),
        absent(
            "seasons_qq",
            "season names",
            ["spring", "summer", "autumn", "winter"],
            "qq",
            "impossible_bigram",
        ),
        absent(
            "seasons_cat",
            "season names",
            ["spring", "summer", "autumn", "winter"],
            "cat",
            "lexical_absence",
        ),
        absent(
            "numbers_zero",
            "number words from one to ten",
            ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"],
            "zero",
            "semantic_lure",
        ),
        absent(
            "numbers_dog",
            "number words from one to ten",
            ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"],
            "dog",
            "lexical_absence",
        ),
        absent(
            "directions_left",
            "cardinal directions",
            ["north", "east", "south", "west"],
            "left",
            "spatial_semantic_lure",
        ),
        absent(
            "directions_zz",
            "cardinal directions",
            ["north", "east", "south", "west"],
            "zz",
            "impossible_bigram",
        ),
        absent(
            "nato_golf",
            "NATO alphabet words",
            ["alpha", "bravo", "charlie", "delta", "echo", "foxtrot"],
            "golf",
            "semantic_lure",
        ),
        absent(
            "nato_ship",
            "NATO alphabet words",
            ["alpha", "bravo", "charlie", "delta", "echo", "foxtrot"],
            "ship",
            "lexical_absence",
        ),
        absent(
            "shapes_hexagon",
            "shape names",
            ["circle", "square", "triangle", "rectangle"],
            "hexagon",
            "semantic_lure",
        ),
        absent(
            "shapes_star",
            "shape names",
            ["circle", "square", "triangle", "rectangle"],
            "star",
            "semantic_lure",
        ),
        absent(
            "elements_gold",
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
            "gold",
            "semantic_lure",
        ),
        absent(
            "elements_sodium",
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
            "sodium",
            "semantic_lure",
        ),
        absent(
            "chess_castle",
            "chess piece names",
            ["king", "queen", "rook", "bishop", "knight", "pawn"],
            "castle",
            "semantic_lure",
        ),
        absent(
            "card_suits_crown",
            "card suit names",
            ["hearts", "diamonds", "clubs", "spades"],
            "crown",
            "semantic_lure",
        ),
        absent(
            "coins_dollar",
            "US coin names",
            ["penny", "nickel", "dime", "quarter"],
            "dollar",
            "semantic_lure",
        ),
        absent(
            "coins_cat",
            "US coin names",
            ["penny", "nickel", "dime", "quarter"],
            "cat",
            "lexical_absence",
        ),
        absent(
            "animals_zoo",
            "animal names",
            ["ant", "bee", "cat", "dog", "eel", "fox"],
            "zoo",
            "semantic_lure",
        ),
        absent(
            "animals_bird",
            "animal names",
            ["ant", "bee", "cat", "dog", "eel", "fox"],
            "bird",
            "semantic_lure",
        ),
        absent(
            "fruits_toe",
            "fruit names",
            [
                "apple",
                "banana",
                "cherry",
                "grape",
                "lemon",
                "mango",
                "orange",
                "peach",
                "pear",
                "plum",
            ],
            "toe",
            "lexical_absence",
        ),
        absent(
            "fruits_car",
            "fruit names",
            [
                "apple",
                "banana",
                "cherry",
                "grape",
                "lemon",
                "mango",
                "orange",
                "peach",
                "pear",
                "plum",
            ],
            "car",
            "lexical_absence",
        ),
        absent(
            "vegetables_fish",
            "vegetable names",
            [
                "carrot",
                "broccoli",
                "celery",
                "corn",
                "cucumber",
                "lettuce",
                "onion",
                "spinach",
                "tomato",
                "zucchini",
            ],
            "fish",
            "semantic_lure",
        ),
        absent(
            "vegetables_pizza",
            "vegetable names",
            [
                "carrot",
                "broccoli",
                "celery",
                "corn",
                "cucumber",
                "lettuce",
                "onion",
                "spinach",
                "tomato",
                "zucchini",
            ],
            "pizza",
            "semantic_lure",
        ),
        absent(
            "greek_first_ten_fish",
            "Greek letter names",
            ["alpha", "beta", "gamma", "delta", "epsilon", "zeta", "eta", "theta", "iota", "kappa"],
            "fish",
            "semantic_lure",
        ),
        absent(
            "roman_one_to_ten_cat",
            "Roman numerals from one to ten",
            ["i", "ii", "iii", "iv", "v", "vi", "vii", "viii", "ix", "x"],
            "cat",
            "lexical_absence",
        ),
        absent(
            "roman_one_to_ten_zero",
            "Roman numerals from one to ten",
            ["i", "ii", "iii", "iv", "v", "vi", "vii", "viii", "ix", "x"],
            "zero",
            "semantic_lure",
        ),
        absent(
            "file_extensions_long_cat",
            "file extension names",
            ["txt", "pdf", "docx", "xlsx", "pptx", "csv", "json", "xml", "html", "md"],
            "cat",
            "lexical_absence",
        ),
        absent(
            "programming_keywords_pizza",
            "programming keywords",
            ["if", "else", "for", "while", "return", "class", "import", "from", "def"],
            "pizza",
            "semantic_lure",
        ),
        absent(
            "metric_prefixes_cat",
            "metric prefix names",
            ["milli", "centi", "deci", "deka", "hecto", "kilo", "mega", "giga"],
            "cat",
            "lexical_absence",
        ),
        absent(
            "si_units_cat",
            "SI base unit names",
            ["meter", "kilogram", "second", "ampere", "kelvin", "mole", "candela"],
            "cat",
            "lexical_absence",
        ),
        absent(
            "dna_bases_uracil",
            "DNA base names",
            ["adenine", "cytosine", "guanine", "thymine"],
            "uracil",
            "semantic_lure",
        ),
        absent(
            "rna_bases_thymine",
            "RNA base names",
            ["adenine", "cytosine", "guanine", "uracil"],
            "thymine",
            "semantic_lure",
        ),
        absent(
            "continents_moon",
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
            "moon",
            "lexical_absence",
        ),
        absent(
            "oceans_moon",
            "ocean names",
            ["Pacific", "Atlantic", "Indian", "Southern", "Arctic"],
            "moon",
            "lexical_absence",
        ),
        absent(
            "great_lakes_cat",
            "Great Lakes names",
            ["Superior", "Michigan", "Huron", "Erie", "Ontario"],
            "cat",
            "lexical_absence",
        ),
        absent(
            "arithmetic_ops_square",
            "arithmetic operation names",
            ["addition", "subtraction", "multiplication", "division"],
            "square",
            "semantic_lure",
        ),
        absent(
            "arithmetic_ops_plus",
            "arithmetic operation names",
            ["addition", "subtraction", "multiplication", "division"],
            "plus",
            "semantic_lure",
        ),
        absent(
            "temperature_scales_rankine",
            "temperature scale names",
            ["Celsius", "Fahrenheit", "Kelvin"],
            "rankine",
            "semantic_lure",
        ),
        absent(
            "web_browsers_whale",
            "web browser names",
            ["Chrome", "Firefox", "Safari", "Edge", "Opera"],
            "whale",
            "semantic_lure",
        ),
        absent(
            "web_browsers_net",
            "web browser names",
            ["Chrome", "Firefox", "Safari", "Edge", "Opera"],
            "net",
            "lexical_absence",
        ),
        absent(
            "languages_snake",
            "programming language names",
            ["Python", "Java", "JavaScript", "Ruby", "Go", "Rust", "Swift", "Kotlin"],
            "snake",
            "semantic_lure",
        ),
        absent(
            "si_units_pound",
            "SI base unit names",
            ["meter", "kilogram", "second", "ampere", "kelvin", "mole", "candela"],
            "pound",
            "semantic_lure",
        ),
        absent(
            "metric_prefixes_micro",
            "metric prefix names",
            ["milli", "centi", "deci", "deka", "hecto", "kilo", "mega", "giga"],
            "micro",
            "semantic_lure",
        ),
        positive(
            "months_ber",
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
            "ber",
            "positive_control_many",
        ),
        positive(
            "months_ary",
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
            "ary",
            "positive_control_multi",
        ),
        positive(
            "days_ur",
            "day names",
            ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
            "ur",
            "positive_control_multi",
        ),
        positive(
            "planets_ur",
            "planet names",
            ["Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune"],
            "ur",
            "positive_control_multi",
        ),
        positive(
            "numbers_en",
            "number words from one to ten",
            ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"],
            "en",
            "positive_control_multi",
        ),
        positive(
            "elements_ium",
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
            "ium",
            "positive_control_multi",
        ),
        positive(
            "chess_kn",
            "chess piece names",
            ["king", "queen", "rook", "bishop", "knight", "pawn"],
            "kn",
            "positive_control_single",
        ),
        positive(
            "rainbow_or",
            "rainbow colors",
            ["red", "orange", "yellow", "green", "blue", "indigo", "violet"],
            "or",
            "positive_control_single",
        ),
        positive(
            "months_mar",
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
            "mar",
            "positive_control_single",
        ),
        positive(
            "rainbow_in",
            "rainbow colors",
            ["red", "orange", "yellow", "green", "blue", "indigo", "violet"],
            "in",
            "positive_control_single",
        ),
        positive(
            "card_suits_dia",
            "card suit names",
            ["hearts", "diamonds", "clubs", "spades"],
            "dia",
            "positive_control_single",
        ),
        positive(
            "coins_nick",
            "US coin names",
            ["penny", "nickel", "dime", "quarter"],
            "nick",
            "positive_control_single",
        ),
        positive(
            "fruits_an",
            "fruit names",
            [
                "apple",
                "banana",
                "cherry",
                "grape",
                "lemon",
                "mango",
                "orange",
                "peach",
                "pear",
                "plum",
            ],
            "an",
            "positive_control_multi",
        ),
        positive(
            "continents_america",
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
            "america",
            "positive_control_multi",
        ),
    ]


def write_jsonl(path: Path, records: list[dict[str, object]]) -> None:
    for index, record in enumerate(records, start=1):
        record["id"] = f"obviousbench.char_count.en.v0.private.{100000 + index:06d}"

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "\n".join(json.dumps(record, sort_keys=True, separators=(",", ":")) for record in records)
        + "\n",
        encoding="utf-8",
    )


def summary(records: list[dict[str, object]]) -> str:
    zeros = sum(1 for record in records if record["target"] == "0")
    positives = len(records) - zeros
    return f"items={len(records)} absent_zero={zeros} positive_controls={positives}"


def main() -> int:
    raw = build_items()
    if len(raw) != 80:
        raise ValueError(f"expected 80 core items, got {len(raw)}")

    added, skipped = append_unique(raw, pasted_answer_candidates())
    if added == 0:
        raise ValueError("expanded suite did not add any items")

    write_jsonl(OUT, raw)
    print(f"Wrote {OUT}")
    print(f"{summary(raw)} added={added} skipped_duplicates={skipped}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
