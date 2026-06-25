"""Per-sample scorer dispatch for mixed-family datasets."""

from collections.abc import Iterable

from inspect_ai.scorer import Score, Target, scorer
from inspect_ai.solver import TaskState

from obviousbench.scorers.accepted_answers import accepted_answers_for_sample
from obviousbench.scorers.common import inspect_score
from obviousbench.scorers.exact_integer import score_exact_integer_extract_first
from obviousbench.scorers.exact_string import score_exact_string_trim
from obviousbench.scorers.json_field import score_json_exact_field
from obviousbench.scorers.multiple_choice import score_multiple_choice_letter
from obviousbench.scorers.normalized_list import score_normalized_list
from obviousbench.scorers.regex_match import score_regex_match
from obviousbench.scorers.word_count import score_word_count
from obviousbench.scorers.yes_no import score_yes_no

SCORER_NAME = "dynamic_metadata_scorer_v0"


def score_by_name(
    scorer_name: str,
    output: str,
    target: str,
    *,
    accepted_targets: Iterable[str] | None = (),
):
    if scorer_name in {"exact_string_trim_v0", "normalized_string_v0"}:
        return score_exact_string_trim(
            output,
            target,
            accepted_targets=accepted_targets,
        )
    if scorer_name == "multiple_choice_letter_v0":
        return score_multiple_choice_letter(
            output,
            target,
            accepted_targets=accepted_targets,
        )
    scorers = {
        "exact_integer_extract_first_v0": score_exact_integer_extract_first,
        "normalized_list_v0": score_normalized_list,
        "regex_match_v0": score_regex_match,
        "json_exact_field_v0": score_json_exact_field,
        "word_count_v0": score_word_count,
        "yes_no_v0": score_yes_no,
    }
    try:
        scorer_fn = scorers[scorer_name]
    except KeyError as exc:
        raise ValueError(f"Unknown scorer: {scorer_name}") from exc
    decisions = [
        scorer_fn(output, candidate_target)
        for candidate_target in target_candidates(target, accepted_targets)
    ]
    for decision in decisions:
        if decision.correct:
            return decision
    return decisions[0]


def target_candidates(
    target: str,
    accepted_targets: Iterable[str] | None,
) -> list[str]:
    candidates: list[str] = []
    for index, candidate in enumerate((target, *(accepted_targets or ()))):
        text = str(candidate)
        if (index == 0 or text) and text not in candidates:
            candidates.append(text)
    return candidates


@scorer(metrics=[])
def dynamic_metadata_scorer():
    async def score(state: TaskState, target: Target) -> Score:
        scorer_name = state.metadata.get("scorer", "exact_string_trim_v0")
        decision = score_by_name(
            scorer_name,
            state.output.completion,
            target.text,
            accepted_targets=accepted_answers_for_sample(
                metadata=state.metadata,
                target=target.text,
                scorer_name=str(scorer_name),
            ),
        )
        strict = scorer_name in {
            "exact_string_trim_v0",
            "multiple_choice_letter_v0",
            "regex_match_v0",
            "json_exact_field_v0",
            "yes_no_v0",
        }
        return inspect_score(decision, scorer_name, strict_format=strict)

    return score
