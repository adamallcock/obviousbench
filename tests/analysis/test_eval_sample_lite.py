import json
from pathlib import Path
from zipfile import ZipFile

from obviousbench.analysis.eval_sample_lite import read_eval_sample_from_log_dir


def write_eval_zip(path: Path, sample_payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(path, "w") as archive:
        archive.writestr(
            "samples/sample.json",
            json.dumps(sample_payload),
        )


def sample_payload(
    sample_id: str,
    completion: str,
    *,
    stop_reason: str = "stop",
    output_tokens: int = 1,
    reasoning_tokens: int = 0,
):
    return {
        "id": sample_id,
        "error": None,
        "output": {
            "completion": completion,
            "usage": {
                "input_tokens": 7,
                "output_tokens": output_tokens,
                "total_tokens": 7 + output_tokens,
                "reasoning_tokens": reasoning_tokens,
            },
            "choices": [
                {
                    "message": {"role": "assistant", "content": completion},
                    "stop_reason": stop_reason,
                }
            ],
        },
    }


def test_read_eval_sample_from_log_dir_extracts_completion_usage_and_stop_reason(
    tmp_path: Path,
):
    log_dir = tmp_path / "logs"
    write_eval_zip(
        log_dir / "run.eval",
        sample_payload(
            "sample-1",
            "",
            stop_reason="max_tokens",
            output_tokens=4096,
            reasoning_tokens=4096,
        ),
    )

    sample = read_eval_sample_from_log_dir(log_dir, sample_id="sample-1")

    assert sample is not None
    assert sample.id == "sample-1"
    assert sample.error is None
    assert sample.output.completion == ""
    assert sample.output.stop_reason == "max_tokens"
    assert sample.output.usage.output_tokens == 4096
    assert sample.output.usage.reasoning_tokens == 4096


def test_read_eval_sample_from_log_dir_selects_matching_sample_from_list(
    tmp_path: Path,
):
    log_dir = tmp_path / "logs"
    write_eval_zip(
        log_dir / "run.eval",
        [
            sample_payload("other", "wrong"),
            sample_payload("target", "2"),
        ],
    )

    sample = read_eval_sample_from_log_dir(log_dir, sample_id="target")

    assert sample is not None
    assert sample.output.completion == "2"


def test_read_eval_sample_from_log_dir_selects_latest_duplicate_sample_id(
    tmp_path: Path,
):
    log_dir = tmp_path / "logs"
    write_eval_zip(log_dir / "2026-06-12T00-00-00.eval", sample_payload("dupe", "old"))
    write_eval_zip(log_dir / "2026-06-12T00-00-01.eval", sample_payload("dupe", "new"))

    sample = read_eval_sample_from_log_dir(log_dir, sample_id="dupe")

    assert sample is not None
    assert sample.output.completion == "new"


def test_read_eval_sample_from_log_dir_unique_mode_returns_none_for_duplicates(
    tmp_path: Path,
):
    log_dir = tmp_path / "logs"
    write_eval_zip(log_dir / "a.eval", sample_payload("dupe", "old"))
    write_eval_zip(log_dir / "b.eval", sample_payload("dupe", "new"))

    sample = read_eval_sample_from_log_dir(
        log_dir,
        sample_id="dupe",
        duplicate_policy="unique_or_none",
        require_sample=False,
    )

    assert sample is None
