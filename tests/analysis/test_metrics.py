from obviousbench.analysis.metrics import EvalRecord, compute_summary


def test_compute_summary_reports_obvious_failure_rate():
    records = [
        EvalRecord("openai/gpt-5-nano", "id1", "character_count", True, "none", False, False),
        EvalRecord("openai/gpt-5-nano", "id2", "character_count", True, "none", False, False),
        EvalRecord(
            "openai/gpt-5-nano",
            "id3",
            "character_count",
            False,
            "incorrect_count",
            False,
            False,
        ),
        EvalRecord(
            "openai/gpt-5-nano",
            "id4",
            "format_compliance",
            True,
            "verbose_noncompliance",
            False,
            False,
        ),
        EvalRecord("openai/gpt-5-nano", "id5", "format_compliance", True, "none", False, False),
        EvalRecord("openai/gpt-5-nano", "id6", "word_count", True, "none", False, False),
        EvalRecord("openai/gpt-5-nano", "id7", "word_count", True, "none", False, False),
        EvalRecord("openai/gpt-5-nano", "id8", "ordering", True, "none", False, False),
        EvalRecord("openai/gpt-5-nano", "id9", "ordering", False, "provider_error", True, False),
    ]

    summary = compute_summary(records)[0]

    assert summary.model == "openai/gpt-5-nano"
    assert summary.scored_samples == 8
    assert summary.failures == 1
    assert summary.obvious_failure_rate == 0.125
    assert summary.accuracy_ci_low <= summary.accuracy <= summary.accuracy_ci_high
    assert (
        summary.answer_accuracy_ci_low
        <= summary.answer_accuracy
        <= summary.answer_accuracy_ci_high
    )
    assert (
        summary.strict_accuracy_ci_low
        <= summary.strict_accuracy
        <= summary.strict_accuracy_ci_high
    )
    assert summary.failures_per_1000 == 125
    assert summary.answer_correct == 7
    assert summary.format_correct == 7
    assert summary.strict_correct == 6
    assert summary.answer_accuracy == 0.875
    assert summary.format_accuracy == 0.875
    assert summary.strict_accuracy == 0.75
    assert summary.provider_errors == 1
    assert summary.format_failures == 1


def test_compute_summary_rolls_up_usage_and_cost_by_variant():
    records = [
        EvalRecord(
            "openai/gpt-5-nano",
            "id1",
            "character_count",
            True,
            "none",
            False,
            False,
            barrage_profile="balanced_8x10",
            barrage_seed=20260531,
            reasoning_effort="minimal",
            reasoning_summary="none",
            input_tokens=10,
            output_tokens=3,
            reasoning_tokens=1,
            total_tokens=14,
            estimated_cost_usd=0.00001,
            cost_source="runcost",
        ),
        EvalRecord(
            "openai/gpt-5-nano",
            "id2",
            "character_count",
            False,
            "incorrect_count",
            False,
            False,
            barrage_profile="balanced_8x10",
            barrage_seed=20260531,
            reasoning_effort="minimal",
            reasoning_summary="none",
            input_tokens=20,
            output_tokens=4,
            reasoning_tokens=2,
            total_tokens=26,
            estimated_cost_usd=0.00002,
            cost_source="runcost",
            cost_warnings="No cached-token price.",
        ),
    ]

    summary = compute_summary(records)[0]

    assert summary.run_variant == (
        "openai/gpt-5-nano|profile=balanced_8x10|seed=20260531|"
        "reasoning_effort=minimal|reasoning_summary=none"
    )
    assert summary.input_tokens == 30
    assert summary.output_tokens == 7
    assert summary.reasoning_tokens == 3
    assert summary.total_tokens == 40
    assert summary.estimated_cost_usd == 0.00003
    assert summary.cost_source == "runcost"
    assert summary.cost_warnings == "No cached-token price."


def test_compute_summary_adds_efficiency_metrics():
    records = [
        EvalRecord(
            "openai/gpt-5-nano",
            "id1",
            "character_count",
            True,
            "none",
            False,
            False,
            output_tokens=10,
            reasoning_tokens=30,
            total_tokens=50,
            estimated_cost_usd=0.2,
        ),
        EvalRecord(
            "openai/gpt-5-nano",
            "id2",
            "character_count",
            False,
            "incorrect_count",
            False,
            False,
            output_tokens=10,
            reasoning_tokens=30,
            total_tokens=50,
            estimated_cost_usd=0.2,
        ),
    ]

    summary = compute_summary(records)[0]

    assert summary.tokens_per_scored_sample == 50.0
    assert summary.output_tokens_per_scored_sample == 10.0
    assert summary.reasoning_tokens_per_scored_sample == 30.0
    assert summary.tokens_per_correct == 100.0
    assert summary.cost_per_correct_usd == 0.4
    assert summary.reasoning_token_share == 0.6
    assert summary.overthinking_index == 3.0
    assert summary.reasoning_token_source == "reported"
