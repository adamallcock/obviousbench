"""Spelling-transform Inspect task."""

from inspect_ai import task

from obviousbench.tasks.base import make_task, split_path


@task
def spelling_transform(split: str = "public_v0"):
    return make_task(split_path(split, "spelling_transform.jsonl"), "dynamic", "spelling_transform")

