import csv
from types import SimpleNamespace

from obviousbench.analysis.logs import load_eval_logs
from obviousbench.analysis.metamorphic import (
    compute_metamorphic_consistency,
    export_metamorphic_consistency_csv,
)
from obviousbench.analysis.metrics import EvalRecord
from obviousbench.analysis.summarize_results import summarize_results


def test_equivalent_group_consistency_requires_same_correctness():
    rows = compute_metamorphic_consistency(
        [
            EvalRecord(
                model="m",
                sample_id="a",
                family="spelling_transform",
                correct=True,
                failure_type="none",
                provider_error=False,
                timeout=False,
                metamorphic_group_id="g1",
                metamorphic_relation="equivalent",
            ),
            EvalRecord(
                model="m",
                sample_id="b",
                family="spelling_transform",
                correct=False,
                failure_type="string_transform_error",
                provider_error=False,
                timeout=False,
                metamorphic_group_id="g1",
                metamorphic_relation="equivalent",
            ),
        ]
    )

    assert len(rows) == 1
    assert rows[0].samples == 2
    assert rows[0].scored_samples == 2
    assert rows[0].all_correct is False
    assert rows[0].all_incorrect is False
    assert rows[0].mixed_outcomes is True
    assert rows[0].consistent is False


def test_provider_errors_are_unscored_for_group_consistency():
    rows = compute_metamorphic_consistency(
        [
            EvalRecord(
                model="m",
                sample_id="a",
                family="spelling_transform",
                correct=True,
                failure_type="none",
                provider_error=False,
                timeout=False,
                metamorphic_group_id="g1",
                metamorphic_relation="equivalent",
            ),
            EvalRecord(
                model="m",
                sample_id="b",
                family="spelling_transform",
                correct=False,
                failure_type="provider_error",
                provider_error=True,
                timeout=False,
                metamorphic_group_id="g1",
                metamorphic_relation="equivalent",
            ),
            EvalRecord(
                model="m",
                sample_id="c",
                family="spelling_transform",
                correct=False,
                failure_type="timeout",
                provider_error=False,
                timeout=True,
                metamorphic_group_id="g1",
                metamorphic_relation="equivalent",
            ),
        ]
    )

    assert rows[0].samples == 3
    assert rows[0].scored_samples == 1
    assert rows[0].assessable is False
    assert rows[0].all_correct is True
    assert rows[0].consistent is False


def test_single_scored_group_is_not_assessable_or_consistent():
    rows = compute_metamorphic_consistency(
        [
            EvalRecord(
                model="m",
                sample_id="a",
                family="spelling_transform",
                correct=True,
                failure_type="none",
                provider_error=False,
                timeout=False,
                metamorphic_group_id="g1",
                metamorphic_relation="equivalent",
            )
        ]
    )

    assert rows[0].scored_samples == 1
    assert rows[0].assessable is False
    assert rows[0].consistent is False


def test_metamorphic_consistency_groups_by_run_variant_model_family_and_relation():
    rows = compute_metamorphic_consistency(
        [
            EvalRecord(
                model="m",
                sample_id="a",
                family="spelling_transform",
                correct=True,
                failure_type="none",
                provider_error=False,
                timeout=False,
                barrage_profile="balanced_8x10",
                barrage_seed=1,
                metamorphic_group_id="g1",
                metamorphic_relation="equivalent",
            ),
            EvalRecord(
                model="m",
                sample_id="b",
                family="spelling_transform",
                correct=True,
                failure_type="none",
                provider_error=False,
                timeout=False,
                barrage_profile="balanced_8x10",
                barrage_seed=2,
                metamorphic_group_id="g1",
                metamorphic_relation="equivalent",
            ),
        ]
    )

    assert len(rows) == 2
    assert {row.run_variant for row in rows} == {
        (
            "m|profile=balanced_8x10|seed=1|reasoning_effort=|"
            "reasoning_summary="
        ),
        (
            "m|profile=balanced_8x10|seed=2|reasoning_effort=|"
            "reasoning_summary="
        ),
    }


def test_export_metamorphic_consistency_csv(tmp_path):
    path = tmp_path / "metamorphic_consistency.csv"
    rows = compute_metamorphic_consistency(
        [
            EvalRecord(
                model="m",
                sample_id="a",
                family="spelling_transform",
                correct=True,
                failure_type="none",
                provider_error=False,
                timeout=False,
                metamorphic_group_id="g1",
                metamorphic_relation="equivalent",
            )
        ]
    )

    export_metamorphic_consistency_csv(rows, path)

    [row] = list(csv.DictReader(path.open(encoding="utf-8")))
    assert row["metamorphic_group_id"] == "g1"
    assert row["samples"] == "1"
    assert row["scored_samples"] == "1"
    assert row["assessable"] == "False"


def test_summarize_results_writes_metamorphic_consistency_when_groups_exist(
    monkeypatch,
    tmp_path,
):
    def fake_load_eval_logs_with_failures(logs, *, rescore=False):
        return (
            [
                EvalRecord(
                    model="m",
                    sample_id="a",
                    family="spelling_transform",
                    correct=True,
                    failure_type="none",
                    provider_error=False,
                    timeout=False,
                    metamorphic_group_id="g1",
                    metamorphic_relation="equivalent",
                )
            ],
            [],
        )

    monkeypatch.setattr(
        "obviousbench.analysis.summarize_results.load_eval_logs_with_failures",
        fake_load_eval_logs_with_failures,
    )

    paths = summarize_results(tmp_path / "logs", tmp_path / "summary", cost_mode="none")

    metamorphic_path = tmp_path / "summary" / "metamorphic_consistency.csv"
    assert metamorphic_path in paths
    assert metamorphic_path.exists()


def test_load_eval_logs_preserves_nested_metamorphic_metadata(tmp_path, monkeypatch):
    log_path = tmp_path / "run.eval"
    log_path.write_text("placeholder", encoding="utf-8")

    def fake_read_eval_log(path):
        assert path == log_path
        return SimpleNamespace(
            eval=SimpleNamespace(
                model="m",
                task_args={},
                metadata={},
                model_generate_config=SimpleNamespace(
                    reasoning_effort=None,
                    reasoning_summary=None,
                ),
            ),
            samples=[
                SimpleNamespace(
                    id="sample-1",
                    input="Question: Reverse abc.\nAnswer:",
                    target="cba",
                    output=SimpleNamespace(completion="cba"),
                    metadata={
                        "family": "spelling_transform",
                        "subfamily": "reverse_word",
                        "benchmark_metadata": {
                            "metamorphic_group_id": "spell.reverse.001",
                            "metamorphic_role": "base",
                            "metamorphic_relation": "equivalent",
                        },
                    },
                    scores={
                        "score": SimpleNamespace(
                            value="C",
                            answer="cba",
                            metadata={"failure_type": "none"},
                        )
                    },
                    error=None,
                    limit=None,
                    model_usage={},
                )
            ],
        )

    monkeypatch.setattr("obviousbench.analysis.logs.read_eval_log", fake_read_eval_log)

    [record] = load_eval_logs(log_path)

    assert record.metamorphic_group_id == "spell.reverse.001"
    assert record.metamorphic_role == "base"
    assert record.metamorphic_relation == "equivalent"


def test_load_eval_logs_strips_blank_metamorphic_metadata(tmp_path, monkeypatch):
    log_path = tmp_path / "run.eval"
    log_path.write_text("placeholder", encoding="utf-8")

    def fake_read_eval_log(path):
        assert path == log_path
        return SimpleNamespace(
            eval=SimpleNamespace(
                model="m",
                task_args={},
                metadata={},
                model_generate_config=SimpleNamespace(
                    reasoning_effort=None,
                    reasoning_summary=None,
                ),
            ),
            samples=[
                SimpleNamespace(
                    id="sample-1",
                    input="Question: Reverse abc.\nAnswer:",
                    target="cba",
                    output=SimpleNamespace(completion="cba"),
                    metadata={
                        "family": "spelling_transform",
                        "subfamily": "reverse_word",
                        "benchmark_metadata": {
                            "metamorphic_group_id": "   ",
                            "metamorphic_role": "\t",
                            "metamorphic_relation": " equivalent ",
                        },
                    },
                    scores={
                        "score": SimpleNamespace(
                            value="C",
                            answer="cba",
                            metadata={"failure_type": "none"},
                        )
                    },
                    error=None,
                    limit=None,
                    model_usage={},
                )
            ],
        )

    monkeypatch.setattr("obviousbench.analysis.logs.read_eval_log", fake_read_eval_log)

    [record] = load_eval_logs(log_path)

    assert record.metamorphic_group_id == ""
    assert record.metamorphic_role == ""
    assert record.metamorphic_relation == "equivalent"
