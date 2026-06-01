from obviousbench.analysis.efficiency import (
    cost_per_correct_usd,
    overthinking_index,
    safe_ratio,
    tokens_per_correct,
)


def test_safe_ratio_returns_none_for_zero_denominator():
    assert safe_ratio(10, 0) is None


def test_safe_ratio_returns_none_for_missing_values():
    assert safe_ratio(None, 2) is None
    assert safe_ratio(10, None) is None


def test_tokens_per_correct_uses_total_tokens_and_correct_count():
    assert tokens_per_correct(total_tokens=120, correct=3) == 40.0


def test_cost_per_correct_uses_estimated_cost_and_correct_count():
    assert cost_per_correct_usd(estimated_cost_usd=0.24, correct=3) == 0.08


def test_overthinking_index_uses_one_for_zero_output_tokens():
    assert overthinking_index(reasoning_tokens=6, output_tokens=0) == 6.0
