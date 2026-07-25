"""Public aggregate reasoning-token invariants for the v0.2 release."""

from __future__ import annotations

import csv
from pathlib import Path

from scripts.release.audit_v0_2_public_bundle import validate_aggregate_reasoning_telemetry

ROOT = Path(__file__).resolve().parents[2]
SUMMARY_PATH = ROOT / "reports/v0_2/aggregate/summary.csv"


def _rows_by_entry_id() -> dict[str, dict[str, str]]:
    with SUMMARY_PATH.open(newline="", encoding="utf-8") as handle:
        return {row["model_entry_id"]: row for row in csv.DictReader(handle)}


def test_public_v0_2_aggregate_keeps_reasoning_telemetry_separate_from_billing() -> None:
    assert validate_aggregate_reasoning_telemetry(SUMMARY_PATH) == []

    rows = _rows_by_entry_id()
    assert all(
        row["reasoning_token_source"]
        not in {
            "aggregate_completion_contract",
            "aggregate_usage_only",
            "thinking_disabled_contract",
        }
        for row in rows.values()
    )


def test_public_opus_celeris_and_sonar_rows_publish_their_actual_reasoning_state() -> None:
    rows = _rows_by_entry_id()

    expected_opus = {
        "anthropic-claude-opus-5-none": ("0", "reported_zero", "not_applicable_contract"),
        "anthropic-claude-opus-5-low": ("11807", "reported_mixed", "adaptive_no_thinking_block"),
        "anthropic-claude-opus-5-medium": ("13147", "reported_mixed", "adaptive_no_thinking_block"),
        "anthropic-claude-opus-5-high": ("16704", "reported_mixed", "adaptive_no_thinking_block"),
        "anthropic-claude-opus-5-xhigh": ("17876", "reported_mixed", "adaptive_no_thinking_block"),
        "anthropic-claude-opus-5-max": ("19136", "reported_mixed", "adaptive_no_thinking_block"),
    }
    for entry_id, expected in expected_opus.items():
        row = rows[entry_id]
        assert (
            row["reasoning_tokens"],
            row["reasoning_token_status"],
            row["reasoning_token_source"],
        ) == expected

    assert (
        rows["celeris-celeris-1-provider-default"]["reasoning_tokens"],
        rows["celeris-celeris-1-provider-default"]["reasoning_token_status"],
        rows["celeris-celeris-1-provider-default"]["reasoning_token_source"],
    ) == ("0", "reported_zero", "not_applicable_contract")
    assert rows["celeris-celeris-1-provider-default"]["reasoning_effort"] == "Default"

    for entry_id in (
        "perplexity-sonar-provider-default",
        "perplexity-sonar-pro-provider-default",
    ):
        assert (
            rows[entry_id]["reasoning_tokens"],
            rows[entry_id]["reasoning_token_status"],
            rows[entry_id]["reasoning_token_source"],
        ) == ("0", "reported_zero", "not_applicable_contract")

    assert (
        rows["perplexity-sonar-reasoning-pro-provider-default"]["reasoning_tokens"],
        rows["perplexity-sonar-reasoning-pro-provider-default"]["reasoning_token_status"],
        rows["perplexity-sonar-reasoning-pro-provider-default"]["reasoning_token_source"],
    ) == ("", "not_separately_reported", "not_separately_reported")
