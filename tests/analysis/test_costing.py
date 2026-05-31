import json
import subprocess
from pathlib import Path

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
    bridge = Path("scripts/price_usage_with_runcost.mjs")
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
