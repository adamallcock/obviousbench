"""Inspect log parsing for ObviousBench analysis."""

from pathlib import Path

from inspect_ai.log import read_eval_log

from obviousbench.analysis.build_failure_gallery import FailureGalleryEntry
from obviousbench.analysis.metrics import EvalRecord


def load_eval_logs(path: Path) -> list[EvalRecord]:
    records, _entries = load_eval_logs_with_failures(path)
    return records


def load_eval_logs_with_failures(path: Path) -> tuple[list[EvalRecord], list[FailureGalleryEntry]]:
    if not path.exists():
        raise FileNotFoundError(f"Log path does not exist: {path}")

    log_files = [path] if path.is_file() else sorted(path.glob("*.eval"))
    records: list[EvalRecord] = []
    entries: list[FailureGalleryEntry] = []

    for log_file in log_files:
        eval_log = read_eval_log(log_file)
        model = str(eval_log.eval.model)
        task_args = eval_log.eval.task_args or {}
        generate_config = eval_log.eval.model_generate_config
        for sample in eval_log.samples or []:
            provider_error = sample.error is not None
            timeout = bool(sample.limit and getattr(sample.limit, "type", None) == "time")
            score = next(iter((sample.scores or {}).values()), None)
            failure_type = "provider_error" if provider_error else "non_answer"
            correct = False
            extracted = None
            if score is not None:
                correct = score.value == "C"
                extracted = score.answer
                failure_type = str((score.metadata or {}).get("failure_type", failure_type))
            family = str(sample.metadata.get("family", "unknown"))
            subfamily = str(sample.metadata.get("subfamily", ""))
            sample_id = str(sample.id)
            usage = _sample_usage(sample.model_usage or {}, model)
            records.append(
                EvalRecord(
                    model=model,
                    sample_id=sample_id,
                    family=family,
                    subfamily=subfamily,
                    question=_question_from_input(str(sample.input)),
                    correct=correct,
                    failure_type=failure_type,
                    provider_error=provider_error,
                    timeout=timeout,
                    barrage_profile=str(task_args.get("profile") or ""),
                    barrage_seed=_optional_int(task_args.get("seed")),
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
                )
            )
            if not correct and not provider_error and not timeout:
                entries.append(
                    FailureGalleryEntry(
                        model=model,
                        family=family,
                        sample_id=sample_id,
                        question=_question_from_input(str(sample.input)),
                        expected_answer=str(sample.target),
                        extracted_answer=extracted,
                        raw_output=sample.output.completion,
                        failure_type=failure_type,
                        human_triviality=str(sample.metadata.get("human_triviality", "")),
                        source_type=str(sample.metadata.get("source_type", "")),
                        why_obvious=str(
                            sample.metadata.get("benchmark_metadata", {}).get(
                                "why_obvious",
                                "A human can answer this by direct inspection "
                                "or simple mental work.",
                            )
                        ),
                    )
                )
    return records, entries


def _sample_usage(model_usage: dict, model: str):
    if model in model_usage:
        return model_usage[model]
    return next(iter(model_usage.values()), None) if model_usage else None


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


def _question_from_input(prompt: str) -> str:
    marker = "Question: "
    if marker not in prompt:
        return prompt
    question = prompt.split(marker, 1)[1]
    return question.split("\nAnswer:", 1)[0].strip()
