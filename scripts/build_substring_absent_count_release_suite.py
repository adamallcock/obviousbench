#!/usr/bin/env python
"""Build the 160-item release-candidate absent-substring count corpus."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from build_substring_absent_count_expanded_suite import (
    append_unique,
    item_fingerprint,
    pasted_answer_candidates,
)
from build_substring_absent_count_suite import absent, build_items, positive

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/experiments/2026-06-07-substring-absent-count-release-160.jsonl"
SUITE_ID = "substring_absent_count_release_160_v0"
ID_BASE = 260700

PUBLIC_SEED_SLUGS = {"days_toe"}
CALIBRATION_SLUGS = {
    "days_toe",
    "months_qq",
    "planets_fish",
    "rainbow_car",
    "seasons_box",
    "numbers_cat",
    "days_tue",
    "months_jan",
    "planets_mars",
    "rainbow_red",
}
CHALLENGE_SLUGS = {
    "first_letters_cat",
    "secondary_colors_cat",
    "bills_cat",
    "punctuation_cat",
    "boolean_words_cat",
    "cloud_types_dog",
    "seasons_mer",
    "nato_x",
    "shapes_angle",
    "greek_eta",
    "tools_saw",
    "days_moon",
    "months_mars",
    "planets_pluto",
    "planets_sun",
    "shapes_hexagon",
    "elements_gold",
    "chess_castle",
    "dna_bases_uracil",
    "rna_bases_thymine",
    "arithmetic_ops_plus",
    "temperature_scales_rankine",
    "languages_snake",
    "metric_prefixes_micro",
    "months_ber",
    "months_ary",
    "elements_ium",
    "continents_america",
    "taxonomic_ranks_dom",
    "arithmetic_ops_tion",
}


def release_topoff_candidates() -> list[dict[str, object]]:
    return [
        absent(
            "blood_types_cat", "blood type labels", ["A", "B", "AB", "O"], "cat", "lexical_absence"
        ),
        absent(
            "blood_types_dog", "blood type labels", ["A", "B", "AB", "O"], "dog", "lexical_absence"
        ),
        absent(
            "taxonomic_ranks_dog",
            "taxonomic rank names",
            ["domain", "kingdom", "phylum", "class", "order", "family", "genus", "species"],
            "dog",
            "semantic_lure",
        ),
        absent(
            "taxonomic_ranks_cat",
            "taxonomic rank names",
            ["domain", "kingdom", "phylum", "class", "order", "family", "genus", "species"],
            "cat",
            "semantic_lure",
        ),
        absent(
            "unix_permissions_cat",
            "Unix permission names",
            ["read", "write", "execute"],
            "cat",
            "lexical_absence",
        ),
        absent(
            "unix_permissions_dog",
            "Unix permission names",
            ["read", "write", "execute"],
            "dog",
            "lexical_absence",
        ),
        absent(
            "compass_rose_dog",
            "compass rose direction names",
            ["north", "northeast", "east", "southeast", "south", "southwest", "west", "northwest"],
            "dog",
            "spatial_semantic_lure",
        ),
        absent(
            "compass_rose_left",
            "compass rose direction names",
            ["north", "northeast", "east", "southeast", "south", "southwest", "west", "northwest"],
            "left",
            "spatial_semantic_lure",
        ),
        absent(
            "continents_zz",
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
            "zz",
            "impossible_bigram",
        ),
        absent(
            "oceans_zz",
            "ocean names",
            ["Pacific", "Atlantic", "Indian", "Southern", "Arctic"],
            "zz",
            "impossible_bigram",
        ),
        absent(
            "planets_star",
            "planet names",
            ["Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune"],
            "star",
            "semantic_lure",
        ),
        absent(
            "seasons_snow",
            "season names",
            ["spring", "summer", "autumn", "winter"],
            "snow",
            "semantic_lure",
        ),
        positive(
            "weekdays_sun",
            "day names",
            ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
            "sun",
            "positive_control_single",
        ),
        positive(
            "taxonomic_ranks_dom",
            "taxonomic rank names",
            ["domain", "kingdom", "phylum", "class", "order", "family", "genus", "species"],
            "dom",
            "positive_control_single",
        ),
        positive(
            "arithmetic_ops_tion",
            "arithmetic operation names",
            ["addition", "subtraction", "multiplication", "division"],
            "tion",
            "positive_control_multi",
        ),
    ]


def build_release_items() -> list[dict[str, object]]:
    records = build_items()
    if len(records) != 80:
        raise ValueError(f"expected 80 core items, got {len(records)}")

    added_pasted, skipped_pasted = append_unique(records, pasted_answer_candidates())
    if added_pasted != 65 or skipped_pasted != 0:
        raise ValueError(
            "expected pasted-answer expansion to add 65 unique items, "
            f"got added={added_pasted} skipped={skipped_pasted}"
        )

    added_topoff, skipped_topoff = append_unique(records, release_topoff_candidates())
    if added_topoff != 15 or skipped_topoff != 0:
        raise ValueError(
            "expected release topoff to add 15 unique items, "
            f"got added={added_topoff} skipped={skipped_topoff}"
        )
    if len(records) != 160:
        raise ValueError(f"expected 160 release items, got {len(records)}")

    fingerprints = [item_fingerprint(record) for record in records]
    if len(fingerprints) != len(set(fingerprints)):
        raise ValueError("release suite contains duplicate collection/needle fingerprints")

    for record in records:
        slug = str(record["metadata"]["item_slug"])
        metadata = record["metadata"]
        if not isinstance(metadata, dict):
            raise TypeError("metadata must be a dict")

        if slug in CALIBRATION_SLUGS:
            suite_split = "dev_calibration"
            record["split"] = "calibration_v0"
            record["source_type"] = "calibration"
        elif slug in CHALLENGE_SLUGS:
            suite_split = "challenge"
            record["split"] = "private_v0"
            record["source_type"] = "hand_authored"
        else:
            suite_split = "main_eval"
            record["split"] = "private_v0"
            record["source_type"] = "hand_authored"

        public_seed = slug in PUBLIC_SEED_SLUGS
        metadata.update(
            {
                "dev_calibration_only": suite_split == "dev_calibration",
                "derived_from_generators": [
                    "scripts/build_substring_absent_count_suite.py",
                    "scripts/build_substring_absent_count_expanded_suite.py",
                ],
                "generator": "scripts/build_substring_absent_count_release_suite.py",
                "known_public_seed_example": public_seed,
                "release_candidate": True,
                "suite_id": SUITE_ID,
                "suite_split": suite_split,
            }
        )

        if public_seed:
            metadata.update(
                {
                    "public_seed_rights_status": "user_provided_screenshot_do_not_republish",
                    "public_seed_urls": [
                        "https://techcrunch.com/2026/05/27/why-googles-ai-cant-spell-google-or-anything-else/",
                        "https://x.com/mersomas/status/2059633208300290276",
                    ],
                }
            )
            record["source_refs"] = [
                "src_2026_05_27_techcrunch_google_ai_toe_days",
                "src_2026_06_07_x_mersomas_toe_days_screenshot",
                *record["source_refs"],
            ]

    split_counts = Counter(str(record["metadata"]["suite_split"]) for record in records)
    expected_splits = {"dev_calibration": 10, "main_eval": 120, "challenge": 30}
    if dict(split_counts) != expected_splits:
        raise ValueError(f"unexpected suite split counts: {dict(split_counts)}")

    return records


def write_jsonl(path: Path, records: list[dict[str, object]]) -> None:
    split_indexes: Counter[str] = Counter()
    split_short = {"calibration_v0": "calibration", "private_v0": "private"}
    for record in records:
        split = str(record["split"])
        split_indexes[split] += 1
        record["id"] = (
            "obviousbench.char_count.en.v0."
            f"{split_short[split]}.{ID_BASE + split_indexes[split]:06d}"
        )

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "\n".join(json.dumps(record, sort_keys=True, separators=(",", ":")) for record in records)
        + "\n",
        encoding="utf-8",
    )


def summary(records: list[dict[str, object]]) -> str:
    targets = Counter(record["target"] for record in records)
    item_types = Counter(str(record["metadata"]["item_type"]) for record in records)
    suite_splits = Counter(str(record["metadata"]["suite_split"]) for record in records)
    return (
        f"items={len(records)} targets={dict(targets)} "
        f"item_type={dict(item_types)} suite_split={dict(suite_splits)}"
    )


def main() -> int:
    records = build_release_items()
    write_jsonl(OUT, records)
    print(f"Wrote {OUT}")
    print(summary(records))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
