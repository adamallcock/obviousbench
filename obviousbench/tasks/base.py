"""Shared Inspect task factory."""

from pathlib import Path

from inspect_ai import Task
from inspect_ai.solver import generate

from obviousbench.datasets.load import load_benchmark_jsonl, to_samples
from obviousbench.scorers.dynamic import dynamic_metadata_scorer

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def make_task(dataset_path: Path, scorer_name: str, name: str) -> Task:
    items = load_benchmark_jsonl(dataset_path)
    return Task(
        dataset=to_samples(items),
        solver=generate(),
        scorer=dynamic_metadata_scorer(),
        name=name,
        metadata={
            "prompt_policy": "native_provider_no_system_prompt_v0",
            "scoring_policy": "deterministic_v0",
        },
    )


def split_path(split: str, family_file: str) -> Path:
    if split == "calibration_v0":
        return PROJECT_ROOT / "data" / split / family_file
    return PROJECT_ROOT / "data" / split / family_file
