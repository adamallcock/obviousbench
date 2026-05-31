from obviousbench.tasks.barrage import barrage
from obviousbench.tasks.character_count import character_count
from obviousbench.tasks.smoke import smoke


def test_smoke_task_instantiates_without_model_call():
    task = smoke()

    assert task.dataset
    assert task.scorer


def test_character_count_task_instantiates_without_model_call():
    task = character_count()

    assert task.dataset
    assert task.scorer


def test_barrage_task_instantiates_without_model_call():
    task = barrage(profile="balanced_8x10", seed=20260531)

    assert len(task.dataset) == 80
    assert task.scorer
    assert task.metadata["barrage_profile"] == "balanced_8x10"
