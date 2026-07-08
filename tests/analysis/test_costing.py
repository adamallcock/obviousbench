import json
import subprocess
from pathlib import Path

import pytest

from obviousbench.analysis.costing import apply_cost_ledger
from obviousbench.analysis.metrics import EvalRecord


def test_apply_cost_ledger_adds_sample_costs_and_warnings():
    records = [
        EvalRecord("openai/gpt-5-nano", "id1", "family", True, "none", False, False),
        EvalRecord("openai/gpt-5-nano", "id2", "family", True, "none", False, False),
    ]
    ledger = {
        "records": [
            {
                "sample_id": "id1",
                "estimated_cost_usd": 0.01,
                "cost_source": "runcost",
                "warnings": [],
            },
            {
                "sample_id": "id2",
                "estimated_cost_usd": 0.02,
                "cost_source": "runcost",
                "warnings": [{"message": "No exact price card."}],
            },
        ]
    }

    priced = apply_cost_ledger(records, ledger)

    assert priced[0].estimated_cost_usd == 0.01
    assert priced[0].cost_source == "runcost"
    assert priced[0].cost_warnings == ""
    assert priced[1].estimated_cost_usd == 0.02
    assert priced[1].cost_warnings == "No exact price card."


def test_runcost_bridge_handles_scientific_notation_price_cards():
    bridge = Path("scripts/runners/price_usage_with_runcost.mjs")
    payload = {
        "records": [
            {
                "sample_id": "id1",
                "provider": "anthropic",
                "model": "anthropic/claude-sonnet-4-6",
                "usage": {
                    "input_tokens": 100,
                    "output_tokens": 10,
                    "reasoning_tokens": 0,
                },
            }
        ]
    }

    completed = subprocess.run(
        ["node", str(bridge)],
        input=json.dumps(payload),
        text=True,
        capture_output=True,
        check=True,
    )
    ledger = json.loads(completed.stdout)

    record = ledger["records"][0]
    assert record["estimated_cost_usd"] is not None
    assert "Cannot convert" not in json.dumps(record["warnings"])


def test_runcost_bridge_prices_direct_gemini_reasoning_tokens():
    bridge = Path("scripts/runners/price_usage_with_runcost.mjs")
    payload = {
        "records": [
            {
                "sample_id": "gemini",
                "provider": "google",
                "model": "google/gemini-3.5-flash",
                "usage": {
                    "input_tokens": 32,
                    "output_tokens": 1,
                    "reasoning_tokens": 1000,
                },
            }
        ]
    }

    completed = subprocess.run(
        ["node", str(bridge)],
        input=json.dumps(payload),
        text=True,
        capture_output=True,
        check=True,
    )
    ledger = json.loads(completed.stdout)

    record = ledger["records"][0]
    components = {entry["name"]: entry for entry in record["ledger"]["components"]}
    assert record["estimated_cost_usd"] == 0.009057
    assert components["output_reasoning_tokens"]["quantity"] == "1000"
    assert components["output_reasoning_tokens"]["cost"] == "0.009"
    assert components["output_reasoning_tokens"]["metadata"] == {
        "pricing_policy": "gemini_thinking_tokens_priced_as_output_tokens",
        "priced_as_component": "output_text_tokens",
    }


def test_runcost_bridge_prices_openai_flex_at_standard_public_rate():
    bridge = Path("scripts/runners/price_usage_with_runcost.mjs")
    standard_record = {
        "sample_id": "standard",
        "provider": "openai",
        "model": "openai/gpt-5-mini",
        "usage": {
            "input_tokens": 100,
            "output_tokens": 20,
            "reasoning_tokens": 0,
        },
    }
    payload = {
        "records": [
            standard_record,
            {
                **standard_record,
                "sample_id": "flex",
                "service_tier": "flex",
            },
        ]
    }

    completed = subprocess.run(
        ["node", str(bridge)],
        input=json.dumps(payload),
        text=True,
        capture_output=True,
        check=True,
    )
    records = {
        record["sample_id"]: record for record in json.loads(completed.stdout)["records"]
    }

    assert records["flex"]["cost_source"] == "runcost"
    assert records["flex"]["estimated_cost_usd"] == records["standard"][
        "estimated_cost_usd"
    ]
    assert "pricing_adjustment" not in records["flex"]["ledger"]


def test_runcost_bridge_prices_free_nemotron_nano_at_paid_equivalent_rate():
    bridge = Path("scripts/runners/price_usage_with_runcost.mjs")
    payload = {
        "records": [
            {
                "sample_id": "nano",
                "provider": "openrouter",
                "model": (
                    "openrouter/nvidia/"
                    "nemotron-3-nano-omni-30b-a3b-reasoning:free"
                ),
                "usage": {
                    "input_tokens": 100,
                    "output_tokens": 25,
                    "reasoning_tokens": 0,
                },
            }
        ]
    }

    completed = subprocess.run(
        ["node", str(bridge)],
        input=json.dumps(payload),
        text=True,
        capture_output=True,
        check=True,
    )
    record = json.loads(completed.stdout)["records"][0]

    assert record["cost_source"] == "user_paid_equivalent_override_2026_06_17"
    assert record["estimated_cost_usd"] == pytest.approx(0.00001)


def test_runcost_bridge_prices_direct_grok_4_5_at_xai_docs_rate():
    bridge = Path("scripts/runners/price_usage_with_runcost.mjs")
    payload = {
        "records": [
            {
                "sample_id": "grok-4-5",
                "provider": "grok",
                "model": "grok/grok-4.5",
                "usage": {
                    "input_tokens": 100,
                    "output_tokens": 25,
                    "reasoning_tokens": 20,
                    "cache_read_tokens": 10,
                },
            }
        ]
    }

    completed = subprocess.run(
        ["node", str(bridge)],
        input=json.dumps(payload),
        text=True,
        capture_output=True,
        check=True,
    )
    record = json.loads(completed.stdout)["records"][0]

    expected_cost = 90 * 0.000002 + 10 * 0.0000005 + (25 + 20) * 0.000006
    assert record["cost_source"] == "xai_grok_4_5_docs_2026_07_08"
    assert record["estimated_cost_usd"] == pytest.approx(expected_cost)
