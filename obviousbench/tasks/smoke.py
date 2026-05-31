"""Smoke Inspect task."""

from inspect_ai import task

from obviousbench.tasks.base import make_task, split_path


@task
def smoke(split: str = "calibration_v0"):
    return make_task(
        split_path(split, "smoke_test.jsonl"),
        "exact_integer_extract_first_v0",
        "smoke",
    )

