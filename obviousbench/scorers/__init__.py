"""Deterministic scorer registry."""

from inspect_ai.scorer import Scorer

from obviousbench.scorers.dynamic import dynamic_metadata_scorer
from obviousbench.scorers.exact_integer import exact_integer_extract_first
from obviousbench.scorers.exact_string import exact_string_trim
from obviousbench.scorers.json_field import json_exact_field
from obviousbench.scorers.multiple_choice import multiple_choice_letter
from obviousbench.scorers.normalized_list import normalized_list_scorer
from obviousbench.scorers.regex_match import regex_match_scorer
from obviousbench.scorers.word_count import word_count_scorer


def get_scorer(name: str) -> Scorer:
    registry = {
        "dynamic_metadata_scorer_v0": dynamic_metadata_scorer,
        "exact_integer_extract_first_v0": exact_integer_extract_first,
        "exact_string_trim_v0": exact_string_trim,
        "normalized_string_v0": exact_string_trim,
        "normalized_list_v0": normalized_list_scorer,
        "multiple_choice_letter_v0": multiple_choice_letter,
        "regex_match_v0": regex_match_scorer,
        "json_exact_field_v0": json_exact_field,
        "word_count_v0": word_count_scorer,
    }
    try:
        return registry[name]()
    except KeyError as exc:
        raise ValueError(f"Unknown scorer: {name}") from exc


__all__ = ["get_scorer"]
