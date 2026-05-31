"""Simple constraint-awareness Inspect task."""

from inspect_ai import task

from obviousbench.tasks.base import make_task, split_path


@task
def constraint_awareness(split: str = "public_v0"):
    return make_task(
        split_path(split, "constraint_awareness.jsonl"),
        "dynamic",
        "constraint_awareness",
    )

