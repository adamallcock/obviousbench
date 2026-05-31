"""Balanced barrage Inspect task."""

from pathlib import Path

from inspect_ai import Task, task
from inspect_ai.solver import generate

from obviousbench.barrage import BarrageProfile, build_barrage, load_split_items
from obviousbench.datasets.load import load_benchmark_jsonl, to_samples
from obviousbench.scorers.dynamic import dynamic_metadata_scorer


@task
def barrage(
    profile: str = "balanced_8x10",
    split: str = "public_v0",
    seed: int = 20260531,
    dataset: str | None = None,
):
    """Run a deterministic balanced barrage."""
    if dataset is not None:
        items = load_benchmark_jsonl(Path(dataset))
        profile_name = Path(dataset).stem
    else:
        parsed_profile = BarrageProfile.parse(profile)
        items = build_barrage(load_split_items(split), parsed_profile, seed=seed)
        profile_name = parsed_profile.name

    return Task(
        dataset=to_samples(items),
        solver=generate(),
        scorer=dynamic_metadata_scorer(),
        name="barrage",
        metadata={
            "prompt_policy": "native_provider_no_system_prompt_v0",
            "scoring_policy": "deterministic_v0",
            "barrage_profile": profile_name,
            "barrage_seed": seed,
        },
    )
