"""Word-count Inspect task."""

from inspect_ai import task

from obviousbench.tasks.base import make_task, split_path


@task
def word_count(split: str = "public_v0"):
    return make_task(split_path(split, "word_count.jsonl"), "dynamic", "word_count")

