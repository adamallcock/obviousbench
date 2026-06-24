"""Normalized list scorer."""

import re

from inspect_ai.scorer import Score, Target, scorer
from inspect_ai.solver import TaskState

from obviousbench.scorers.common import (
    ScoreDecision,
    inspect_score,
    normalize_list,
    normalize_token_artifacts,
    strip_confidence_annotation,
)

SCORER_NAME = "normalized_list_v0"
_FINAL_LIST_RE = re.compile(
    r"(?:^|[\s.;,:])(?:answer|final answer|result|therefore|so answer)\s*[:=]\s*"
    r"(?P<answer>[^\n]+)$",
    re.IGNORECASE,
)
_COLON_LIST_RE = re.compile(r":\s*(?P<answer>[^\n]+)$")
_TRAILING_ANSWER_ARTIFACT_CHARS = "\\\"'`"


def score_normalized_list(output: str, target: str) -> ScoreDecision:
    cleaned_output = strip_confidence_annotation(output)
    artifact_normalized = normalize_token_artifacts(cleaned_output)
    extracted_parts = normalize_list(cleaned_output)
    target_parts = normalize_list(target)
    compact_target_parts = _compact_symbol_target_parts(target)
    if compact_target_parts is not None:
        target_parts = compact_target_parts
    compact_symbol_parts = _compact_symbol_parts(cleaned_output, compact_target_parts)
    used_compact_symbol_match = compact_symbol_parts is not None
    if compact_symbol_parts is not None:
        extracted_parts = compact_symbol_parts
    extracted = ", ".join(extracted_parts) if extracted_parts else None
    if not extracted_parts:
        return ScoreDecision(False, None, "non_answer", "No list items found.")
    if extracted_parts == target_parts:
        failure_type = (
            "verbose_noncompliance"
            if (
                cleaned_output.strip() != output.strip()
                or artifact_normalized.strip() != cleaned_output.strip()
                or _has_stray_terminal_list_punctuation(
                    cleaned_output,
                    target_parts,
                    used_compact_symbol_match=used_compact_symbol_match,
                )
            )
            else "none"
        )
        return ScoreDecision(
            True,
            ", ".join(extracted_parts),
            failure_type,
            "List matched.",
            format_correct=False if failure_type == "verbose_noncompliance" else None,
        )
    final_parts = _extract_final_list_parts(output)
    if final_parts == target_parts:
        return ScoreDecision(
            True,
            ", ".join(final_parts),
            "verbose_noncompliance",
            "Matched final list candidate.",
            format_correct=False,
        )
    leading_parts = _extract_leading_list_parts(cleaned_output, target_parts)
    if leading_parts == target_parts:
        return ScoreDecision(
            True,
            ", ".join(leading_parts),
            "verbose_noncompliance",
            "Matched leading answer line.",
            format_correct=False,
        )
    if _starts_with_target_list(output.strip(), target.strip()):
        return ScoreDecision(
            True,
            ", ".join(target_parts),
            "verbose_noncompliance",
            "Matched leading list with extra text.",
            format_correct=False,
        )
    return ScoreDecision(False, extracted, "ordering_error", "List did not match target order.")


def _compact_symbol_target_parts(target: str) -> tuple[str, ...] | None:
    raw_parts = tuple(part.strip() for part in target.split(","))
    if not raw_parts or not all(_is_single_symbol(part) for part in raw_parts):
        return None
    return tuple(part.casefold() for part in raw_parts)


def _compact_symbol_parts(
    output: str,
    target_parts: tuple[str, ...] | None,
) -> tuple[str, ...] | None:
    if not target_parts or not all(_is_single_symbol(part) for part in target_parts):
        return None
    stripped = output.strip()
    if not stripped or "," in stripped or any(char.isspace() for char in stripped):
        return None
    parts = tuple(char.casefold() for char in stripped)
    return parts if parts == target_parts else None


def _is_single_symbol(part: str) -> bool:
    return len(part) == 1 and not part.isalnum()


def _extract_final_list_parts(output: str) -> tuple[str, ...] | None:
    for pattern in (_FINAL_LIST_RE, _COLON_LIST_RE):
        match = pattern.search(output.strip())
        if match is not None:
            return normalize_list(match.group("answer"))
    return None


def _extract_leading_list_parts(
    output: str,
    target_parts: tuple[str, ...],
) -> tuple[str, ...] | None:
    stripped = output.strip()
    if not stripped:
        return None
    first_line = next(
        (line.strip() for line in stripped.splitlines() if line.strip()),
        "",
    )
    if not first_line:
        return None
    multiline = len(stripped.splitlines()) > 1
    direct_parts = normalize_list(first_line)
    if multiline and direct_parts == target_parts:
        return direct_parts
    artifact_trimmed = _strip_trailing_answer_artifacts(first_line, target_parts)
    if artifact_trimmed != first_line:
        artifact_parts = normalize_list(artifact_trimmed)
        if artifact_parts == target_parts:
            return artifact_parts
    return None


def _strip_trailing_answer_artifacts(
    value: str,
    target_parts: tuple[str, ...],
) -> str:
    artifact_chars = _TRAILING_ANSWER_ARTIFACT_CHARS
    last_target = target_parts[-1] if target_parts else ""
    if _is_single_symbol(last_target):
        artifact_chars = artifact_chars.replace(last_target, "")
    return value.rstrip().rstrip(artifact_chars).rstrip()


def _starts_with_target_list(output: str, target: str) -> bool:
    if not target or not output.startswith(target) or len(output) == len(target):
        return False
    remainder = output[len(target) :].lstrip()
    if not remainder:
        return False
    return remainder.startswith(("(", "[", "{", ":", "-"))


def _has_terminal_list_punctuation(output: str) -> bool:
    stripped = output.strip()
    return bool(stripped) and stripped[-1] in ".!?;"


def _has_stray_terminal_list_punctuation(
    output: str,
    target_parts: tuple[str, ...],
    *,
    used_compact_symbol_match: bool,
) -> bool:
    if used_compact_symbol_match or not _has_terminal_list_punctuation(output):
        return False
    last_target = target_parts[-1] if target_parts else ""
    return not (_is_single_symbol(last_target) and output.strip()[-1].casefold() == last_target)


@scorer(metrics=[])
def normalized_list_scorer():
    async def score(state: TaskState, target: Target) -> Score:
        decision = score_normalized_list(state.output.completion, target.text)
        return inspect_score(decision, SCORER_NAME)

    return score
