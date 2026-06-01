from obviousbench.analysis.statistics import (
    bootstrap_mean_interval,
    paired_boolean_delta,
    wilson_interval,
)


def test_wilson_interval_empty_count():
    assert wilson_interval(0, 0) == (0.0, 0.0)


def test_wilson_interval_bounds_are_valid():
    low, high = wilson_interval(8, 10)
    assert 0.0 <= low <= 0.8 <= high <= 1.0


def test_paired_boolean_delta_counts_wins_losses_and_ties():
    result = paired_boolean_delta(
        baseline={"a": True, "b": False, "c": True},
        comparison={"a": True, "b": True, "c": False},
    )

    assert result.matched_samples == 3
    assert result.wins == 1
    assert result.losses == 1
    assert result.ties == 1
    assert result.delta == 0.0


def test_paired_boolean_delta_bootstrap_is_deterministic():
    result = paired_boolean_delta(
        baseline={"a": False, "b": False, "c": True, "d": True},
        comparison={"a": True, "b": False, "c": True, "d": False},
    )

    assert result.ci_low <= result.delta <= result.ci_high
    assert result == paired_boolean_delta(
        baseline={"a": False, "b": False, "c": True, "d": True},
        comparison={"a": True, "b": False, "c": True, "d": False},
    )


def test_bootstrap_mean_interval_uses_explicit_95_percentile_cutoffs():
    assert bootstrap_mean_interval([-1, 0, 1, 1], seed=123, resamples=40) == (
        -0.5,
        1.0,
    )
