"""Format-compliance Inspect task."""

from inspect_ai import task

from obviousbench.tasks.base import make_task, split_path


@task
def format_compliance(split: str = "public_v0"):
    return make_task(split_path(split, "format_compliance.jsonl"), "dynamic", "format_compliance")

