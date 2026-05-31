"""Per-sample scorer dispatch for mixed-family datasets."""

from inspect_ai.scorer import Score, Target, scorer
from inspect_ai.solver import TaskState

from obviousbench.scorers.common import inspect_score
from obviousbench.scorers.exact_integer import score_exact_integer_extract_first
from obviousbench.scorers.exact_string import score_exact_string_trim
from obviousbench.scorers.json_field import score_json_exact_field
from obviousbench.scorers.multiple_choice import score_multiple_choice_letter
from obviousbench.scorers.normalized_list import score_normalized_list
from obviousbench.scorers.regex_match import score_regex_match
from obviousbench.scorers.word_count import score_word_count

SCORER_NAME = "dynamic_metadata_scorer_v0"


def score_by_name(scorer_name: str, output: str, target: str):
    scorers = {
        "exact_integer_extract_first_v0": score_exact_integer_extract_first,
        "exact_string_trim_v0": score_exact_string_trim,
        "normalized_string_v0": score_exact_string_trim,
        "normalized_list_v0": score_normalized_list,
        "multiple_choice_letter_v0": score_multiple_choice_letter,
        "regex_match_v0": score_regex_match,
        "json_exact_field_v0": score_json_exact_field,
        "word_count_v0": score_word_count,
    }
    try:
        return scorers[scorer_name](output, target)
    except KeyError as exc:
        raise ValueError(f"Unknown scorer: {scorer_name}") from exc


@scorer(metrics=[])
def dynamic_metadata_scorer():
    async def score(state: TaskState, target: Target) -> Score:
        scorer_name = state.metadata.get("scorer", "exact_string_trim_v0")
        decision = score_by_name(scorer_name, state.output.completion, target.text)
        strict = scorer_name in {
            "exact_string_trim_v0",
            "multiple_choice_letter_v0",
            "regex_match_v0",
            "json_exact_field_v0",
        }
        return inspect_score(decision, scorer_name, strict_format=strict)

    return score

