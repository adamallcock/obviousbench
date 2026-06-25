"""Character-count Inspect task."""

from inspect_ai import task

from obviousbench.tasks.base import make_task, split_path


@task
def character_count(split: str = "public_v0"):
    return make_task(
        split_path(split, "character_count.jsonl"),
        "exact_integer_extract_first_v0",
        "character_count",
    )

