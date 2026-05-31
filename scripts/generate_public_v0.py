#!/usr/bin/env python
"""Generate deterministic ObviousBench v0 JSONL datasets."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from random import Random
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from obviousbench.datasets.schemas import BenchmarkItem
from obviousbench.generators.character_count import generate_character_count_items
from obviousbench.generators.common import write_jsonl
from obviousbench.generators.ids import make_id
from obviousbench.prompts import (
    FINAL_ANSWER_ONLY_V0,
    MULTIPLE_CHOICE_LETTER_V0,
    render_prompt,
)

ROOT = Path(__file__).resolve().parents[1]


def item(
    *,
    family: str,
    subfamily: str,
    index: int,
    question: str,
    target: str,
    answer_type: str,
    scorer: str,
    source_refs: list[str],
    source_type: str = "generated_variant",
    template_id: str = FINAL_ANSWER_ONLY_V0,
    choices: list[str] | None = None,
    metadata: dict[str, Any] | None = None,
) -> BenchmarkItem:
    prompt = render_prompt(template_id, question, choices)
    merged_metadata = {
        "generated": source_type == "generated_variant",
        "variant_of": None,
        "prompt_template_id": template_id,
        "system_prompt": None,
        "choices": choices,
        "why_obvious": "A person can answer this by direct inspection or simple mental work.",
    }
    if metadata:
        merged_metadata.update(metadata)
    return BenchmarkItem.model_validate(
        {
            "id": make_id(family, "public_v0", index),
            "family": family,
            "subfamily": subfamily,
            "prompt": prompt,
            "question": question,
            "target": target,
            "answer_type": answer_type,
            "scorer": scorer,
            "split": "public_v0",
            "source_type": source_type,
            "source_refs": source_refs,
            "human_triviality": "H0",
            "review_status": "reviewed",
            "metadata": merged_metadata,
        }
    )


def spelling_items(count: int) -> list[BenchmarkItem]:
    words = [
        "strawberry",
        "necessary",
        "sentence",
        "banana",
        "cab",
        "planet",
        "orange",
        "committee",
        "parallel",
        "bookkeeper",
        "mississippi",
        "reliability",
    ]
    rows: list[BenchmarkItem] = []
    index = 1
    for word in words:
        rows.append(
            item(
                family="spelling_transform",
                subfamily="reverse_word",
                index=index,
                question=f"Spell {word} backwards.",
                target=word[::-1],
                answer_type="string",
                scorer="exact_string_trim_v0",
                source_refs=["src_strawberry_public_discussion"],
                metadata={"word": word, "operation": "reverse"},
            )
        )
        index += 1
        if index > count:
            return rows
        if "e" in word:
            rows.append(
                item(
                    family="spelling_transform",
                    subfamily="remove_letter",
                    index=index,
                    question=f"Write {word} without the letter e.",
                    target=word.replace("e", ""),
                    answer_type="string",
                    scorer="exact_string_trim_v0",
                    source_refs=["src_easy_problems_prior_art"],
                    metadata={"word": word, "operation": "remove", "letter": "e"},
                )
            )
            index += 1
            if index > count:
                return rows
        if "a" in word:
            rows.append(
                item(
                    family="spelling_transform",
                    subfamily="replace_letter",
                    index=index,
                    question=f"Replace every a in {word} with @.",
                    target=word.replace("a", "@"),
                    answer_type="string",
                    scorer="exact_string_trim_v0",
                    source_refs=["src_easy_problems_prior_art"],
                    metadata={"word": word, "operation": "replace", "letter": "a"},
                )
            )
            index += 1
            if index > count:
                return rows
    return rows


def arithmetic_items(count: int) -> list[BenchmarkItem]:
    rows: list[BenchmarkItem] = []
    index = 1
    for a in range(3, 23):
        b = a + 5
        c = a % 4
        question = f"What is {a} + {b} - {c}?"
        rows.append(
            item(
                family="arithmetic",
                subfamily="small_integer_arithmetic",
                index=index,
                question=question,
                target=str(a + b - c),
                answer_type="integer",
                scorer="exact_integer_extract_first_v0",
                source_refs=["src_easy_problems_prior_art"],
                metadata={"operation": "addition_subtraction"},
            )
        )
        index += 1
        if index > count:
            return rows
    comparisons = [("9.9", "9.11"), ("7.2", "7.12"), ("3.05", "3.5")]
    for left, right in comparisons:
        rows.append(
            item(
                family="arithmetic",
                subfamily="numeric_comparison",
                index=index,
                question=f"Which is larger, {left} or {right}?",
                target=str(max(float(left), float(right))).rstrip("0").rstrip("."),
                answer_type="decimal",
                scorer="exact_string_trim_v0",
                source_refs=["src_easy_problems_prior_art"],
                metadata={"operation": "numeric_comparison"},
            )
        )
        index += 1
        if index > count:
            return rows
    return rows


def word_count_items(count: int) -> list[BenchmarkItem]:
    sentences = [
        "The small dog ran home",
        "A bright red apple fell",
        "Simple tests catch silly failures",
        "Every public answer should be checked",
        "Three blue cups sat there",
    ]
    lists = [
        "red, blue, green, yellow",
        "A, B, C, D, E",
        "cat, dog, bird",
        "north, south, east, west",
    ]
    rows: list[BenchmarkItem] = []
    index = 1
    while len(rows) < count:
        for sentence in sentences:
            rows.append(
                item(
                    family="word_count",
                    subfamily="sentence_word_count",
                    index=index,
                    question=f"How many words are in '{sentence}'?",
                    target=str(len(sentence.split())),
                    answer_type="integer",
                    scorer="word_count_v0",
                    source_refs=["src_easy_problems_prior_art"],
                    metadata={"sentence": sentence},
                )
            )
            index += 1
            if len(rows) >= count:
                return rows
        for values in lists:
            rows.append(
                item(
                    family="word_count",
                    subfamily="comma_list_count",
                    index=index,
                    question=f"How many comma-separated values are shown here: {values}?",
                    target=str(len([value for value in values.split(",") if value.strip()])),
                    answer_type="integer",
                    scorer="word_count_v0",
                    source_refs=["src_easy_problems_prior_art"],
                    metadata={"values": values},
                )
            )
            index += 1
            if len(rows) >= count:
                return rows
    return rows


def ordering_items(count: int) -> list[BenchmarkItem]:
    groups = [
        ["pear", "apple", "banana"],
        ["cat", "car", "cap"],
        ["delta", "alpha", "charlie", "bravo"],
        ["d", "a", "c", "b"],
        ["red", "blue", "green"],
    ]
    rows: list[BenchmarkItem] = []
    index = 1
    while len(rows) < count:
        for group in groups:
            rows.append(
                item(
                    family="ordering",
                    subfamily="alphabetical_sort",
                    index=index,
                    question=f"Sort these items alphabetically: {', '.join(group)}.",
                    target=", ".join(sorted(group)),
                    answer_type="list",
                    scorer="normalized_list_v0",
                    source_refs=["src_lmentry_prior_art"],
                    metadata={"items": group},
                )
            )
            index += 1
            if len(rows) >= count:
                return rows
    return rows


def format_items(count: int) -> list[BenchmarkItem]:
    rows: list[BenchmarkItem] = []
    index = 1
    while len(rows) < count:
        rows.append(
            item(
                family="format_compliance",
                subfamily="only_yes_no",
                index=index,
                question="Answer with only YES or NO: Is 5 greater than 3?",
                target="^(YES|NO)$",
                answer_type="string",
                scorer="regex_match_v0",
                source_refs=["src_format_following_public_discussion"],
                metadata={"strict_format": True},
            )
        )
        index += 1
        if len(rows) >= count:
            break
        rows.append(
            item(
                family="format_compliance",
                subfamily="json_field",
                index=index,
                question='Return a JSON object with one key, "answer", whose value is "3".',
                target="3",
                answer_type="json",
                scorer="json_exact_field_v0",
                source_refs=["src_format_following_public_discussion"],
                metadata={"strict_format": True, "json_field": "answer"},
            )
        )
        index += 1
    return rows


def negation_items(count: int) -> list[BenchmarkItem]:
    cases = [
        ("Which word does not contain the letter e?", ["tree", "stone", "cat", "green"], "C"),
        ("Which number is not even?", ["4", "8", "11", "20"], "C"),
        ("Which item is not a fruit?", ["apple", "banana", "carrot", "pear"], "C"),
        ("Which word is not lowercase?", ["cat", "dog", "USA", "sun"], "C"),
    ]
    rows: list[BenchmarkItem] = []
    index = 1
    while len(rows) < count:
        for question, choices, target in cases:
            rows.append(
                item(
                    family="negation",
                    subfamily="not_choice",
                    index=index,
                    question=question,
                    target=target,
                    answer_type="multiple_choice",
                    scorer="multiple_choice_letter_v0",
                    source_refs=["src_car_wash_public_discussion"],
                    template_id=MULTIPLE_CHOICE_LETTER_V0,
                    choices=choices,
                    metadata={"strict_format": True},
                )
            )
            index += 1
            if len(rows) >= count:
                return rows
    return rows


def constraint_items(count: int) -> list[BenchmarkItem]:
    cases = [
        (
            "I need to wash my car at a car wash 50 meters away. Should I walk or drive?",
            ["Walk", "Drive", "Take a train", "It is impossible"],
            "B",
        ),
        (
            "I need to take my bicycle to a bike repair shop one block away. What should I bring?",
            ["Only my wallet", "The bicycle", "Nothing", "A suitcase"],
            "B",
        ),
        (
            "I need to mail a package at the post office nearby. What should I take?",
            ["The package", "Only my phone", "Nothing", "A chair"],
            "A",
        ),
    ]
    rows: list[BenchmarkItem] = []
    index = 1
    while len(rows) < count:
        for question, choices, target in cases:
            rows.append(
                item(
                    family="constraint_awareness",
                    subfamily="object_must_be_present",
                    index=index,
                    question=question,
                    target=target,
                    answer_type="multiple_choice",
                    scorer="multiple_choice_letter_v0",
                    source_refs=["src_car_wash_public_discussion"],
                    template_id=MULTIPLE_CHOICE_LETTER_V0,
                    choices=choices,
                    metadata={"strict_format": True},
                )
            )
            index += 1
            if len(rows) >= count:
                return rows
    return rows


def source_catalog() -> list[dict[str, Any]]:
    base = [
        {
            "source_id": "src_google_d_user_screenshot",
            "platform": "user_provided_screenshot",
            "url": None,
            "original_prompt": "How many d is in google?",
            "claimed_output": 'There is exactly 1 "d" in Google.',
            "failure_description": (
                "Screenshot lead where the model reports one d in google even though "
                "google has zero d characters."
            ),
            "media_type": "screenshot",
            "rights_status": "user_provided_screenshot_do_not_republish",
        },
        {
            "source_id": "src_strawberry_public_discussion",
            "platform": "news",
            "url": "https://techcrunch.com/2024/08/27/why-ai-cant-spell-strawberry/",
        },
        {
            "source_id": "src_strawberry_inc",
            "platform": "news",
            "url": "https://www.inc.com/kit-eaton/how-many-rs-in-strawberry-this-ai-cant-tell-you.html",
        },
        {
            "source_id": "src_strawberry_openai_forum",
            "platform": "forum",
            "url": "https://community.openai.com/t/incorrect-count-of-r-characters-in-the-word-strawberry/829618",
        },
        {
            "source_id": "src_car_wash_public_discussion",
            "platform": "news",
            "url": "https://www.ibm.com/think/news/viral-car-wash-llm-challenge",
        },
        {
            "source_id": "src_car_wash_cybernews",
            "platform": "news",
            "url": "https://cybernews.com/ai-news/ai-car-wash-test/",
        },
        {
            "source_id": "src_google_ai_overviews_public_discussion",
            "platform": "news",
            "url": "https://www.theguardian.com/technology/article/2024/may/31/google-ai-summaries-sge-changes",
        },
        {
            "source_id": "src_google_ai_overviews_business_insider",
            "platform": "news",
            "url": "https://www.businessinsider.com/google-ai-glue-pizza-i-tried-it-2024-5",
        },
        {
            "source_id": "src_google_ai_overviews_wired",
            "platform": "news",
            "url": "https://www.wired.com/story/google-ai-overview-search-issues",
        },
        {
            "source_id": "src_google_ai_overviews_ap",
            "platform": "news",
            "url": "https://apnews.com/article/33060569d6cc01abe6c63d21665330d8",
        },
        {
            "source_id": "src_easy_problems_prior_art",
            "platform": "paper",
            "url": "https://arxiv.org/abs/2405.19616",
        },
        {
            "source_id": "src_easy_problems_github",
            "platform": "repo",
            "url": "https://github.com/autogenai/easy-problems-that-llms-get-wrong",
        },
        {
            "source_id": "src_lmentry_prior_art",
            "platform": "paper",
            "url": "https://aclanthology.org/2023.findings-acl.666/",
        },
        {
            "source_id": "src_lmentry_github",
            "platform": "repo",
            "url": "https://github.com/aviaefrat/lmentry",
        },
        {
            "source_id": "src_letter_counting_paper",
            "platform": "paper",
            "url": "https://arxiv.org/abs/2412.18626",
        },
        {
            "source_id": "src_strawberry_problem_paper",
            "platform": "paper",
            "url": "https://arxiv.org/abs/2505.14172",
        },
        {
            "source_id": "src_format_following_public_discussion",
            "platform": "prior_art",
            "url": "https://inspect.aisi.org.uk/scorers.html",
        },
    ]
    records: list[dict[str, Any]] = []
    for index in range(25):
        if index < len(base):
            source = base[index]
        else:
            source = base[1 + ((index - len(base)) % (len(base) - 1))]
        suffix = "" if index < len(base) else f"_variant_{index + 1:02d}"
        records.append(
            {
                "source_id": f"{source['source_id']}{suffix}",
                "platform": source["platform"],
                "url": source["url"],
                "date_seen": "2026-05-30",
                "author_or_handle": None,
                "original_prompt": source.get(
                    "original_prompt",
                    "Public simple-failure archetype or prior-art benchmark source.",
                ),
                "claimed_model": None,
                "claimed_output": source.get("claimed_output"),
                "failure_description": source.get(
                    "failure_description",
                    "Lead source for human-trivial model failure patterns.",
                ),
                "engagement_signal": {"likes": None, "shares": None, "comments": None},
                "media_type": source.get(
                    "media_type",
                    "article" if source["platform"] in {"news", "paper"} else "text",
                ),
                "rights_status": source.get("rights_status", "link_only_do_not_republish"),
                "notes": "Treat as a lead or archetype; reproduce independently.",
            }
        )
    return records


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=98231)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args(argv)

    rng = Random(args.seed)
    datasets = {
        "character_count": generate_character_count_items(90, args.seed, split="public_v0"),
        "spelling_transform": spelling_items(60),
        "arithmetic": arithmetic_items(60),
        "word_count": word_count_items(60),
        "ordering": ordering_items(45),
        "format_compliance": format_items(45),
        "negation": negation_items(25),
        "constraint_awareness": constraint_items(15),
    }
    rng.shuffle(datasets["spelling_transform"])
    if args.dry_run:
        for family, items in datasets.items():
            print(f"{family}: {len(items)}")
        return 0
    if not args.write:
        print("Pass --write to write files, or --dry-run to preview.", file=sys.stderr)
        return 1

    for family, items in datasets.items():
        write_jsonl(items, ROOT / "data" / "public_v0" / f"{family}.jsonl", overwrite=True)

    source_path = ROOT / "data" / "source_catalog" / "sources_v0.jsonl"
    source_path.parent.mkdir(parents=True, exist_ok=True)
    rows = [json.dumps(record, sort_keys=True) for record in source_catalog()]
    source_path.write_text("\n".join(rows) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
