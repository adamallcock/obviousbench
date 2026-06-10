"""Inspect log parsing for ObviousBench analysis."""

from pathlib import Path

from inspect_ai.log import read_eval_log

from obviousbench.analysis.build_failure_gallery import FailureGalleryEntry
from obviousbench.analysis.metrics import EvalRecord
from obviousbench.analysis.rescore import rescore_output
from obviousbench.provider_errors import is_provider_transient_output
from obviousbench.scorers.accepted_answers import accepted_answers_for_sample
from obviousbench.scorers.common import FORMAT_FAILURE_TYPES, ScoreDecision


def load_eval_logs(path: Path) -> list[EvalRecord]:
    records, _entries = load_eval_logs_with_failures(path)
    return records


def load_eval_logs_with_failures(
    path: Path,
    *,
    rescore: bool = False,
) -> tuple[list[EvalRecord], list[FailureGalleryEntry]]:
    if not path.exists():
        raise FileNotFoundError(f"Log path does not exist: {path}")

    log_files = [path] if path.is_file() else sorted(path.rglob("*.eval"))
    records_by_key: dict[tuple[str, str], EvalRecord] = {}
    entries_by_key: dict[tuple[str, str], FailureGalleryEntry] = {}

    for log_file in log_files:
        eval_log = read_eval_log(log_file)
        model = str(eval_log.eval.model)
        task_args = eval_log.eval.task_args or {}
        eval_metadata = eval_log.eval.metadata or {}
        generate_config = eval_log.eval.model_generate_config
        for sample in eval_log.samples or []:
            provider_error = _sample_provider_error(sample)
            timeout = bool(sample.limit and getattr(sample.limit, "type", None) == "time")
            score_result = score_sample(sample, provider_error=provider_error, rescore=rescore)
            family = str(sample.metadata.get("family", "unknown"))
            subfamily = str(sample.metadata.get("subfamily", ""))
            sample_id = str(sample.id)
            usage = _sample_usage(sample.model_usage or {}, model)
            metamorphic_metadata = _metamorphic_metadata(sample.metadata or {})
            record = (
                EvalRecord(
                    model=model,
                    sample_id=sample_id,
                    family=family,
                    subfamily=subfamily,
                    question=_question_from_input(str(sample.input)),
                    correct=score_result.correct,
                    failure_type=score_result.failure_type,
                    provider_error=provider_error,
                    timeout=timeout,
                    answer_correct=score_result.answer_correct,
                    format_correct=score_result.format_correct,
                    strict_correct=score_result.strict_correct,
                    barrage_profile=str(
                        eval_metadata.get("barrage_profile")
                        or task_args.get("profile")
                        or ""
                    ),
                    barrage_seed=_optional_int(
                        eval_metadata.get("barrage_seed") or task_args.get("seed")
                    ),
                    reasoning_effort=str(
                        getattr(generate_config, "reasoning_effort", None) or ""
                    ),
                    reasoning_summary=str(
                        getattr(generate_config, "reasoning_summary", None) or ""
                    ),
                    input_tokens=_usage_int(usage, "input_tokens"),
                    output_tokens=_usage_int(usage, "output_tokens"),
                    reasoning_tokens=_usage_int(usage, "reasoning_tokens"),
                    cache_read_tokens=_usage_int(usage, "input_tokens_cache_read"),
                    cache_write_tokens=_usage_int(usage, "input_tokens_cache_write"),
                    total_tokens=_usage_int(usage, "total_tokens"),
                    metamorphic_group_id=metamorphic_metadata["metamorphic_group_id"],
                    metamorphic_role=metamorphic_metadata["metamorphic_role"],
                    metamorphic_relation=metamorphic_metadata["metamorphic_relation"],
                )
            )
            key = (record.run_variant, record.sample_id)
            if not score_result.strict_correct and not provider_error and not timeout:
                entry = (
                    FailureGalleryEntry(
                        model=model,
                        family=family,
                        sample_id=sample_id,
                        question=_question_from_input(str(sample.input)),
                        expected_answer=str(sample.target),
                        extracted_answer=score_result.extracted,
                        raw_output=sample.output.completion,
                        failure_type=score_result.failure_type,
                        human_triviality=str(sample.metadata.get("human_triviality", "")),
                        source_type=str(sample.metadata.get("source_type", "")),
                        why_obvious=str(
                            sample.metadata.get("benchmark_metadata", {}).get(
                                "why_obvious",
                                "A human can answer this by direct inspection "
                                "or simple mental work.",
                            )
                        ),
                        run=_run_reference(log_file),
                        epoch=getattr(sample, "epoch", 1) or 1,
                    )
                )
            else:
                entry = None
            previous = records_by_key.get(key)
            if previous is None or _dedupe_rank(record) >= _dedupe_rank(previous):
                records_by_key[key] = record
                if entry is None:
                    entries_by_key.pop(key, None)
                else:
                    entries_by_key[key] = entry
    return list(records_by_key.values()), list(entries_by_key.values())


def score_sample(sample, *, provider_error: bool, rescore: bool) -> ScoreDecision:
    if provider_error:
        return ScoreDecision(
            False,
            None,
            "provider_error",
            "Provider error.",
            format_correct=False,
        )
    if rescore:
        scorer_name = str(sample.metadata.get("scorer", "exact_string_trim_v0"))
        decision = rescore_output(
            scorer_name=scorer_name,
            output=sample.output.completion,
            target=str(sample.target),
            accepted_targets=accepted_answers_for_sample(
                sample_id=str(getattr(sample, "id", "") or ""),
                metadata=sample.metadata or {},
            ),
        )
        return ScoreDecision(
            decision.correct,
            decision.extracted,
            decision.failure_type,
            decision.explanation,
            format_correct=decision.resolved_format_correct,
        )

    score = next(iter((sample.scores or {}).values()), None)
    if score is None:
        return ScoreDecision(False, None, "non_answer", "No score was logged.")

    metadata = score.metadata or {}
    correct = score.value == "C"
    failure_type = str(metadata.get("failure_type", "none" if correct else "non_answer"))
    answer_correct = _metadata_bool(metadata.get("answer_correct"), default=correct)
    format_correct = _metadata_bool(
        metadata.get("format_correct"),
        default=failure_type not in FORMAT_FAILURE_TYPES,
    )
    return ScoreDecision(
        answer_correct,
        score.answer,
        failure_type,
        str(getattr(score, "explanation", "") or ""),
        format_correct=format_correct,
    )


def _sample_provider_error(sample) -> bool:
    if sample.error is not None:
        return True
    if _sample_stop_reason(sample) == "content_filter":
        return True
    output = getattr(sample, "output", None)
    completion = getattr(output, "completion", None)
    return is_provider_transient_output(completion)


def _dedupe_rank(record: EvalRecord) -> int:
    if not record.provider_error and not record.timeout:
        return 2
    if record.timeout:
        return 1
    return 0


def _sample_stop_reason(sample) -> str:
    output = getattr(sample, "output", None)
    if output is None:
        return ""
    try:
        return str(getattr(output, "stop_reason", "") or "")
    except (AttributeError, IndexError):
        return ""


def _sample_usage(model_usage: dict, model: str):
    if model in model_usage:
        return model_usage[model]
    return next(iter(model_usage.values()), None) if model_usage else None


def _metadata_bool(value, *, default: bool) -> bool:
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().casefold() in {"1", "true", "yes"}
    return bool(value)


def _usage_int(usage, field: str) -> int:
    if usage is None:
        return 0
    value = getattr(usage, field, None)
    return int(value or 0)


def _optional_int(value) -> int | None:
    if value in {None, ""}:
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _metamorphic_metadata(metadata: dict) -> dict[str, str]:
    benchmark_metadata = metadata.get("benchmark_metadata") or {}
    if not isinstance(benchmark_metadata, dict):
        benchmark_metadata = {}
    values: dict[str, str] = {}
    for field in (
        "metamorphic_group_id",
        "metamorphic_role",
        "metamorphic_relation",
    ):
        values[field] = str(
            benchmark_metadata.get(field) or metadata.get(field) or ""
        ).strip()
    return values


def _question_from_input(prompt: str) -> str:
    marker = "Question: "
    if marker not in prompt:
        return prompt
    question = prompt.split(marker, 1)[1]
    return question.split("\nAnswer:", 1)[0].strip()


def _run_reference(log_file: Path) -> str:
    parts = log_file.parts
    if "raw" in parts and "results" in parts:
        raw_index = parts.index("raw")
        if raw_index + 1 < len(parts) - 1:
            return parts[raw_index + 1]
        return log_file.stem
    parent = log_file.parent.name
    return parent if parent else log_file.stem
