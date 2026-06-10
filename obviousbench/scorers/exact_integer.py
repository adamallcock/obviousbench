"""Integer extraction scorer."""

import re

from inspect_ai.scorer import Score, Target, scorer
from inspect_ai.solver import TaskState

from obviousbench.scorers.common import (
    ScoreDecision,
    extract_integer_candidates,
    extract_single_integer,
    inspect_score,
    is_non_answer,
    normalize_token_artifacts,
)

SCORER_NAME = "exact_integer_extract_first_v0"
_FINAL_INTEGER_CUE_RE = re.compile(
    r"\b(?:answer|final answer|result)\s*(?:is|=|:)\s*"
    r"(?P<answer>(?:\*\*|__|`)?[A-Za-z0-9-]+(?:\*\*|__|`)?)"
    r"[\s.!?]*$",
    re.IGNORECASE,
)


def score_exact_integer_extract_first(output: str, target: str) -> ScoreDecision:
    if is_non_answer(output):
        return ScoreDecision(False, None, "non_answer", "Output was empty.")
    candidates = extract_integer_candidates(output)
    normalized_target = str(target)
    if len(set(candidates)) > 1 and candidates[0] == normalized_target:
        return ScoreDecision(
            True,
            candidates[0],
            "verbose_noncompliance",
            f"Leading integer matched {normalized_target}.",
        )
    extracted, ambiguous = extract_single_integer(output)
    if ambiguous:
        final_answer = _extract_final_integer_answer(output)
        if final_answer == normalized_target:
            return ScoreDecision(
                True,
                final_answer,
                "verbose_noncompliance",
                f"Final answer cue matched {normalized_target}.",
            )
        return ScoreDecision(False, None, "ambiguous_output", f"Ambiguous output: {output}")
    if extracted is None:
        return ScoreDecision(False, None, "non_answer", f"No integer found: {output}")
    if extracted == normalized_target:
        return ScoreDecision(True, extracted, "none", f"Extracted {extracted}.")
    return ScoreDecision(False, extracted, "incorrect_count", f"Extracted {extracted}.")


def _extract_final_integer_answer(output: str) -> str | None:
    normalized = normalize_token_artifacts(output).strip()
    match = _FINAL_INTEGER_CUE_RE.search(normalized)
    if match is None:
        return None
    candidate = match.group("answer").strip()
    for wrapper in ("**", "__", "`"):
        if candidate.startswith(wrapper) and candidate.endswith(wrapper):
            candidate = candidate[len(wrapper) : -len(wrapper)].strip()
    candidates = extract_integer_candidates(candidate)
    if len(set(candidates)) != 1:
        return None
    return candidates[0]


@scorer(metrics=[])
def exact_integer_extract_first():
    async def score(state: TaskState, target: Target) -> Score:
        decision = score_exact_integer_extract_first(state.output.completion, target.text)
        return inspect_score(decision, SCORER_NAME)

    return score
