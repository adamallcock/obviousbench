"""Underrepresented archetype expansion Inspect task."""

from inspect_ai import task

from obviousbench.tasks.base import make_task, split_path


@task
def archetype_expansions(split: str = "public_v0"):
    return make_task(
        split_path(split, "archetype_expansions_2026-05-30.jsonl"),
        "dynamic",
        "archetype_expansions",
    )
