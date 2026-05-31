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
