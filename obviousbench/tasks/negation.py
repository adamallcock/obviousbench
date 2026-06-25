"""Negation/exclusion Inspect task."""

from inspect_ai import task

from obviousbench.tasks.base import make_task, split_path


@task
def negation(split: str = "public_v0"):
    return make_task(split_path(split, "negation.jsonl"), "dynamic", "negation")

