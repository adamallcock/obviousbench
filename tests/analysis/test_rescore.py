from types import SimpleNamespace

from obviousbench.analysis.logs import load_eval_logs, load_eval_logs_with_failures, score_sample
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


def test_rescore_output_accepts_item_level_alternate_targets():
    decision = rescore_output(
        scorer_name="normalized_list_v0",
        output=".@#?!",
        target="@, #, ?, !",
        accepted_targets=["., @, #, ?, !"],
    )

    assert decision.correct
    assert decision.extracted == "., @, #, ?, !"
    assert decision.failure_type == "none"


def test_score_sample_applies_planet_item_accepted_answer_override():
    sample = SimpleNamespace(
        id="obviousbench.spell.en.v0.public.000014",
        metadata={"scorer": "exact_string_trim_v0"},
        output=SimpleNamespace(completion="Mars"),
        target="plant",
        scores={},
    )

    decision = score_sample(sample, provider_error=False, rescore=True)

    assert decision.correct
    assert decision.extracted == "Mars"
    assert decision.failure_type == "none"
    assert decision.answer_correct
    assert decision.format_correct
    assert decision.strict_correct


def test_score_sample_rescore_uses_benchmark_metadata_accepted_targets():
    sample = SimpleNamespace(
        metadata={
            "scorer": "normalized_list_v0",
            "benchmark_metadata": {"accepted_targets": ["., @, #, ?, !"]},
        },
        output=SimpleNamespace(completion=".@#?!"),
        target="@, #, ?, !",
        scores={},
    )

    decision = score_sample(sample, provider_error=False, rescore=True)

    assert decision.correct
    assert decision.extracted == "., @, #, ?, !"
    assert decision.strict_correct


def test_score_sample_rescore_accepts_correct_multiple_choice_option_text_as_strict():
    sample = SimpleNamespace(
        id="obviousbench.constraint.en.v0.public.000013",
        metadata={
            "scorer": "multiple_choice_letter_v0",
            "benchmark_metadata": {
                "choices": [
                    "Take the boat there",
                    "Walk down the dock",
                    "Bring only a rope",
                    "It is impossible",
                ],
            },
        },
        output=SimpleNamespace(completion="Take the boat there"),
        target="A",
        scores={},
    )

    decision = score_sample(sample, provider_error=False, rescore=True)

    assert decision.correct
    assert decision.extracted == "A"
    assert decision.failure_type == "none"
    assert decision.answer_correct
    assert decision.format_correct
    assert decision.strict_correct


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
                    "barrage_profile": "balanced_8x5_seed_20260531",
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
    assert records[0].barrage_profile == "balanced_8x5_seed_20260531"
    assert records[0].barrage_seed == 20260531


def test_load_eval_logs_deduplicates_retry_logs_and_prefers_success(
    tmp_path,
    monkeypatch,
):
    log_dir = tmp_path / "results" / "raw" / "repair-run"
    log_dir.mkdir(parents=True)
    (log_dir / "001-full.eval").write_text("placeholder", encoding="utf-8")
    (log_dir / "002-retry.eval").write_text("placeholder", encoding="utf-8")

    def fake_read_eval_log(path):
        completion = (
            "Content violates usage guidelines. Failed check: SAFETY_CHECK_TYPE_BIO"
            if path.name == "001-full.eval"
            else '{"answer": true}'
        )
        stop_reason = "content_filter" if path.name == "001-full.eval" else "stop"
        score = (
            SimpleNamespace(
                value="I",
                answer=None,
                metadata={"failure_type": "json_malformed"},
            )
            if path.name == "001-full.eval"
            else SimpleNamespace(
                value="C",
                answer="true",
                metadata={"failure_type": "none"},
            )
        )
        return SimpleNamespace(
            eval=SimpleNamespace(
                model="provider/model",
                task_args={},
                metadata={},
                model_generate_config=SimpleNamespace(
                    reasoning_effort=None,
                    reasoning_summary=None,
                ),
            ),
            samples=[
                SimpleNamespace(
                    id="obviousbench.format.en.v0.public.000050",
                    epoch=1,
                    input="Question: Return JSON.\nAnswer:",
                    target="true",
                    output=SimpleNamespace(
                        completion=completion,
                        stop_reason=stop_reason,
                    ),
                    metadata={"family": "format_compliance", "subfamily": "json"},
                    scores={"score": score},
                    error=None,
                    limit=None,
                    model_usage={},
                )
            ],
        )

    monkeypatch.setattr("obviousbench.analysis.logs.read_eval_log", fake_read_eval_log)

    records = load_eval_logs(log_dir)

    assert len(records) == 1
    assert records[0].sample_id == "obviousbench.format.en.v0.public.000050"
    assert records[0].correct
    assert not records[0].provider_error


def test_load_eval_logs_treats_provider_safety_text_as_provider_error(
    tmp_path,
    monkeypatch,
):
    log_dir = tmp_path / "results" / "raw" / "hard-obvious-grok"
    log_dir.mkdir(parents=True)
    (log_dir / "run.eval").write_text("placeholder", encoding="utf-8")

    def fake_read_eval_log(path):
        assert path.name == "run.eval"
        return SimpleNamespace(
            eval=SimpleNamespace(
                model="grok/grok-4.3",
                task_args={},
                metadata={},
                model_generate_config=SimpleNamespace(
                    reasoning_effort=None,
                    reasoning_summary=None,
                ),
            ),
            samples=[
                SimpleNamespace(
                    id="obviousbench.format.en.v0.public.000050",
                    epoch=1,
                    input="Question: Return JSON.\nAnswer:",
                    target="true",
                    output=SimpleNamespace(
                        completion=(
                            "Content violates usage guidelines. "
                            "Failed check: SAFETY_CHECK_TYPE_BIO"
                        )
                    ),
                    metadata={"family": "format_compliance", "subfamily": "json"},
                    scores={
                        "score": SimpleNamespace(
                            value="I",
                            answer=None,
                            metadata={"failure_type": "json_malformed"},
                        )
                    },
                    error=None,
                    limit=None,
                    model_usage={},
                )
            ],
        )

    monkeypatch.setattr("obviousbench.analysis.logs.read_eval_log", fake_read_eval_log)

    records, failures = load_eval_logs_with_failures(log_dir)

    assert records[0].provider_error
    assert records[0].failure_type == "provider_error"
    assert records[0].correct is False
    assert failures == []


def test_load_eval_logs_treats_content_filter_stop_as_provider_error(
    tmp_path,
    monkeypatch,
):
    log_dir = tmp_path / "results" / "raw" / "content-filter-stop"
    log_dir.mkdir(parents=True)
    (log_dir / "run.eval").write_text("placeholder", encoding="utf-8")

    def fake_read_eval_log(path):
        assert path.name == "run.eval"
        return SimpleNamespace(
            eval=SimpleNamespace(
                model="openai/gpt-5-nano",
                task_args={},
                metadata={},
                model_generate_config=SimpleNamespace(
                    reasoning_effort=None,
                    reasoning_summary=None,
                ),
            ),
            samples=[
                SimpleNamespace(
                    id="obviousbench.spell.en.v0.public.000022",
                    epoch=1,
                    input="Question: Rewrite the word.\nAnswer:",
                    target="paralll",
                    output=SimpleNamespace(
                        completion=(
                            "Invalid prompt: your prompt was flagged as potentially "
                            "violating our usage policy."
                        ),
                        stop_reason="content_filter",
                    ),
                    metadata={"family": "spelling_transform", "subfamily": "replace"},
                    scores={
                        "score": SimpleNamespace(
                            value="I",
                            answer=None,
                            metadata={"failure_type": "wrong_letter_or_substring"},
                        )
                    },
                    error=None,
                    limit=None,
                    model_usage={},
                )
            ],
        )

    monkeypatch.setattr("obviousbench.analysis.logs.read_eval_log", fake_read_eval_log)

    records, failures = load_eval_logs_with_failures(log_dir, rescore=True)

    assert records[0].provider_error
    assert records[0].failure_type == "provider_error"
    assert records[0].answer_correct is False
    assert failures == []


def test_load_eval_logs_includes_format_noncompliance_in_failure_gallery(
    tmp_path,
    monkeypatch,
):
    log_dir = tmp_path / "results" / "raw" / "strict-run"
    log_dir.mkdir(parents=True)
    (log_dir / "run.eval").write_text("placeholder", encoding="utf-8")

    def fake_read_eval_log(path):
        assert path.name == "run.eval"
        return SimpleNamespace(
            eval=SimpleNamespace(
                model="provider/model-a",
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
                    epoch=1,
                    input="Question: Choose the item.\nAnswer:",
                    target="paper",
                    output=SimpleNamespace(completion="paper (because it is not metal)"),
                    metadata={"family": "negation", "subfamily": "not_metal"},
                    scores={
                        "score": SimpleNamespace(
                            value="C",
                            answer="paper",
                            explanation="Matched with extra text.",
                            metadata={
                                "failure_type": "verbose_noncompliance",
                                "answer_correct": True,
                                "format_correct": False,
                                "strict_correct": False,
                            },
                        )
                    },
                    error=None,
                    limit=None,
                    model_usage={},
                )
            ],
        )

    monkeypatch.setattr("obviousbench.analysis.logs.read_eval_log", fake_read_eval_log)

    records, failures = load_eval_logs_with_failures(log_dir)

    assert records[0].correct
    assert records[0].answer_ok
    assert not records[0].format_ok
    assert not records[0].strict_ok
    assert failures[0].sample_id == "sample-1"
    assert failures[0].reference == "run=strict-run sample=sample-1 epoch=1 model=provider/model-a"
