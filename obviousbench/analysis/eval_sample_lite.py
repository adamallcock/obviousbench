"""Lightweight Inspect ``.eval`` sample extraction for report builders."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from zipfile import ZipFile


@dataclass(frozen=True)
class LiteUsage:
    input_tokens: int = 0
    output_tokens: int = 0
    total_tokens: int = 0
    input_tokens_cache_read: int = 0
    input_tokens_cache_write: int = 0
    reasoning_tokens: int = 0


@dataclass(frozen=True)
class LiteOutput:
    completion: str
    stop_reason: str
    usage: LiteUsage
    model: str = ""


@dataclass(frozen=True)
class LiteSample:
    id: str
    output: LiteOutput
    error: Any = None


def read_eval_sample_from_log_dir(
    log_dir: Path | str,
    *,
    sample_id: str = "",
    require_sample: bool = True,
    duplicate_policy: str = "latest",
) -> LiteSample | None:
    """Read one sample from Inspect ``.eval`` zips without hydrating full logs."""

    if sample_id:
        samples_by_id = read_eval_samples_from_log_dir(
            log_dir,
            sample_ids={sample_id},
            require_samples=require_sample,
            duplicate_policy=duplicate_policy,
        )
        return samples_by_id.get(sample_id)

    log_files = sorted(Path(log_dir).glob("*.eval"))
    if not log_files:
        if require_sample:
            raise FileNotFoundError(f"no .eval file in {log_dir}")
        return None

    samples: list[LiteSample] = []
    for log_file in log_files:
        samples.extend(read_eval_samples(log_file))

    if sample_id:
        matches = [sample for sample in samples if str(sample.id) == sample_id]
        if not matches:
            if require_sample:
                raise ValueError(
                    f"expected at least one sample_id={sample_id!r} in {log_dir}, "
                    f"found {len(matches)}"
                )
            return None
        if duplicate_policy == "unique_or_none" and len(matches) != 1:
            return None
        return matches[-1]

    if len(samples) != 1:
        if require_sample:
            raise ValueError(f"expected one sample in {log_dir}, found {len(samples)}")
        return None
    return samples[0]


def read_eval_samples_from_log_dir(
    log_dir: Path | str,
    *,
    sample_ids: set[str],
    require_samples: bool = True,
    duplicate_policy: str = "latest",
) -> dict[str, LiteSample | None]:
    """Read selected samples from Inspect ``.eval`` zips.

    Inspect stores samples as ``samples/{sample_id}_epoch_1.json`` in the common
    case. Use that filename index first so batched logs do not require parsing
    every sample payload repeatedly.
    """

    requested = {sample_id for sample_id in sample_ids if sample_id}
    if not requested:
        return {}

    log_files = sorted(Path(log_dir).glob("*.eval"))
    if not log_files:
        if require_samples:
            raise FileNotFoundError(f"no .eval file in {log_dir}")
        return {sample_id: None for sample_id in requested}

    matches: dict[str, list[LiteSample]] = {sample_id: [] for sample_id in requested}
    for log_file in log_files:
        read_matching_eval_samples(log_file, requested=requested, matches=matches)

    result: dict[str, LiteSample | None] = {}
    for requested_id, requested_matches in matches.items():
        if not requested_matches:
            if require_samples:
                raise ValueError(
                    f"expected at least one sample_id={requested_id!r} in {log_dir}, "
                    f"found {len(requested_matches)}"
                )
            result[requested_id] = None
            continue
        if duplicate_policy == "unique_or_none" and len(requested_matches) != 1:
            result[requested_id] = None
            continue
        result[requested_id] = requested_matches[-1]
    return result


def read_eval_samples(path: Path | str) -> list[LiteSample]:
    samples: list[LiteSample] = []
    with ZipFile(path) as archive:
        sample_names = sorted(
            name
            for name in archive.namelist()
            if name.startswith("samples/") and name.endswith(".json")
        )
        for name in sample_names:
            payload = json.loads(archive.read(name))
            raw_samples = payload if isinstance(payload, list) else [payload]
            samples.extend(
                sample
                for raw_sample in raw_samples
                if (sample := lite_sample_from_payload(raw_sample)) is not None
            )
    return samples


def read_matching_eval_samples(
    path: Path | str,
    *,
    requested: set[str],
    matches: dict[str, list[LiteSample]],
) -> None:
    with ZipFile(path) as archive:
        sample_names = [
            name
            for name in archive.namelist()
            if name.startswith("samples/") and name.endswith(".json")
        ]
        fallback_names: list[str] = []
        direct_match_count_before = sum(len(sample_matches) for sample_matches in matches.values())
        for name in sample_names:
            name_sample_id = sample_id_from_sample_path(name)
            if name_sample_id in requested:
                add_matching_payload_samples(
                    archive.read(name),
                    requested=requested,
                    matches=matches,
                )
            else:
                fallback_names.append(name)

        remaining = requested - {
            sample.id for sample_matches in matches.values() for sample in sample_matches
        }
        direct_match_count_after = sum(len(sample_matches) for sample_matches in matches.values())
        archive_had_direct_match = direct_match_count_after > direct_match_count_before
        if not remaining and archive_had_direct_match:
            return
        fallback_requested = remaining if remaining else requested
        for name in fallback_names:
            add_matching_payload_samples(
                archive.read(name),
                requested=fallback_requested,
                matches=matches,
            )
            remaining = fallback_requested - {
                sample.id for sample_matches in matches.values() for sample in sample_matches
            }
            if not remaining:
                break


def add_matching_payload_samples(
    payload_bytes: bytes,
    *,
    requested: set[str],
    matches: dict[str, list[LiteSample]],
) -> None:
    payload = json.loads(payload_bytes)
    raw_samples = payload if isinstance(payload, list) else [payload]
    for raw_sample in raw_samples:
        sample = lite_sample_from_payload(raw_sample)
        if sample is not None and sample.id in requested:
            matches[sample.id].append(sample)


def sample_id_from_sample_path(name: str) -> str:
    if not name.startswith("samples/") or not name.endswith(".json"):
        return ""
    filename = name.removeprefix("samples/").removesuffix(".json")
    sample_id, epoch_separator, epoch = filename.rpartition("_epoch_")
    if epoch_separator and epoch.isdigit():
        return sample_id
    return filename


def lite_sample_from_payload(payload: Any) -> LiteSample | None:
    if not isinstance(payload, dict):
        return None
    output_payload = payload.get("output") or {}
    if not isinstance(output_payload, dict):
        output_payload = {}
    usage_payload = output_payload.get("usage") or {}
    if not isinstance(usage_payload, dict):
        usage_payload = {}
    usage = LiteUsage(
        input_tokens=int_value(usage_payload.get("input_tokens")),
        output_tokens=int_value(usage_payload.get("output_tokens")),
        total_tokens=int_value(usage_payload.get("total_tokens")),
        input_tokens_cache_read=int_value(
            usage_payload.get("input_tokens_cache_read")
        ),
        input_tokens_cache_write=int_value(
            usage_payload.get("input_tokens_cache_write")
        ),
        reasoning_tokens=int_value(usage_payload.get("reasoning_tokens")),
    )
    completion = output_payload.get("completion")
    output = LiteOutput(
        completion="" if completion is None else str(completion),
        stop_reason=stop_reason_from_output(output_payload),
        usage=usage,
        model=str(output_payload.get("model") or ""),
    )
    return LiteSample(
        id=str(payload.get("id") or ""),
        output=output,
        error=payload.get("error"),
    )


def stop_reason_from_output(output_payload: dict[str, Any]) -> str:
    direct = output_payload.get("stop_reason")
    if direct:
        return str(direct)
    choices = output_payload.get("choices")
    if isinstance(choices, list):
        for choice in choices:
            if isinstance(choice, dict) and choice.get("stop_reason"):
                return str(choice["stop_reason"])
    return ""


def int_value(value: Any) -> int:
    if value in {None, ""}:
        return 0
    return int(float(str(value)))
