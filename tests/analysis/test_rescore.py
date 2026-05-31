from types import SimpleNamespace

from obviousbench.analysis.logs import load_eval_logs, score_sample
from obviousbench.analysis.rescore import rescore_output


def test_rescore_output_uses_current_dynamic_scorer():
    decision = rescore_output(
        scorer_name="multiple_choice_letter_v0",
        output="B. The bicycle",
        target="B",
    )

    assert decision.correct
    assert decision.extracted == "B"
    assert decision.failure_type == "verbose_noncompliance"
    assert decision.answer_correct
    assert not decision.resolved_format_correct
    assert not decision.strict_correct


def test_score_sample_can_rescore_stale_logged_score():
    sample = SimpleNamespace(
        metadata={"scorer": "json_exact_field_v0"},
        output=SimpleNamespace(completion='```json\n{"answer": "north"}\n```'),
        target="north",
        scores={
            "old": SimpleNamespace(
                value="I",
                answer=None,
                metadata={"failure_type": "json_malformed"},
            )
        },
    )

    decision = score_sample(sample, provider_error=False, rescore=True)

    assert decision.correct
    assert decision.extracted == "north"
    assert decision.failure_type == "verbose_noncompliance"
    assert decision.answer_correct
    assert not decision.format_correct
    assert not decision.strict_correct


def test_score_sample_uses_existing_score_without_rescore():
    sample = SimpleNamespace(
        metadata={"scorer": "json_exact_field_v0"},
        output=SimpleNamespace(completion='```json\n{"answer": "north"}\n```'),
        target="north",
        scores={
            "old": SimpleNamespace(
                value="I",
                answer=None,
                metadata={"failure_type": "json_malformed"},
            )
        },
    )

    decision = score_sample(sample, provider_error=False, rescore=False)

    assert not decision.correct
    assert decision.extracted is None
    assert decision.failure_type == "json_malformed"
    assert not decision.answer_correct
    assert not decision.format_correct
    assert not decision.strict_correct


def test_load_eval_logs_discovers_nested_batch_logs(tmp_path, monkeypatch):
    log_dir = tmp_path / "logs" / "batch-0001"
    log_dir.mkdir(parents=True)
    (log_dir / "run.eval").write_text("placeholder", encoding="utf-8")

    def fake_read_eval_log(path):
        assert path.name == "run.eval"
        return SimpleNamespace(
            eval=SimpleNamespace(
                model="openrouter/model",
                task_args={"profile": "balanced_8x10", "seed": 1},
                metadata={
                    "barrage_profile": "hard_obvious_8x10_seed_20260531",
                    "barrage_seed": 20260531,
                },
                model_generate_config=SimpleNamespace(
                    reasoning_effort=None,
                    reasoning_summary=None,
                ),
            ),
            samples=[
                SimpleNamespace(
                    id="sample-1",
                    input="Question: What is 1+1?\nAnswer:",
                    target="2",
                    output=SimpleNamespace(completion="2"),
                    metadata={"family": "arithmetic", "subfamily": "addition"},
                    scores={
                        "score": SimpleNamespace(
                            value="C",
                            answer="2",
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

    records = load_eval_logs(tmp_path / "logs")

    assert len(records) == 1
    assert records[0].sample_id == "sample-1"
    assert records[0].barrage_profile == "hard_obvious_8x10_seed_20260531"
    assert records[0].barrage_seed == 20260531
