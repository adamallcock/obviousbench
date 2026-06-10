from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

import yaml

from obviousbench.research.model_panel_costs import (
    ModelPanelCostInputs,
    estimate_model_panel_costs,
)


def test_estimate_model_panel_costs_writes_csv_and_markdown(tmp_path: Path):
    panel_path = tmp_path / "panel.yaml"
    csv_path = tmp_path / "costs.csv"
    markdown_path = tmp_path / "costs.md"
    panel_path.write_text(
        yaml.safe_dump(
            {
                "schema_version": "paper-model-panel-v1",
                "profile": "hard_obvious_8x10",
                "seed": 20260531,
                "defaults": {
                    "temperature": 0,
                    "inspect_args": [
                        "--no-log-model-api",
                        "--attempt-timeout",
                        "180",
                    ],
                },
                "entries": [
                    {
                        "id": "unit-model",
                        "label": "Unit Model",
                        "provider_route": "openai",
                        "inspect_model": "openai/unit",
                        "generation_settings": {
                            "max_tokens": 64,
                        },
                        "run_status": "planned",
                    }
                ],
            },
            sort_keys=False,
        ),
        encoding="utf-8",
    )
    calls = []

    def fake_estimator(inputs):
        calls.append(inputs)
        return SimpleNamespace(
            model=inputs.model,
            total_samples=80,
            billable_samples=80,
            cache_hits=0,
            estimated_billable_cost_usd=0.1234,
            pricing_source="unit-prices",
            warnings=("unit warning",),
        )

    result = estimate_model_panel_costs(
        ModelPanelCostInputs(
            panel_path=panel_path,
            csv_path=csv_path,
            markdown_path=markdown_path,
            cache=None,
            cache_dir=None,
            estimator=fake_estimator,
        )
    )

    assert result.row_count == 1
    assert calls[0].model == "openai/unit"
    assert calls[0].settings == {
        "temperature": "0",
        "attempt_timeout": "180",
        "max_tokens": "64",
    }
    assert calls[0].cache is None
    assert calls[0].cache_dir is None
    csv_text = csv_path.read_text(encoding="utf-8")
    markdown_text = markdown_path.read_text(encoding="utf-8")
    assert "unit-model" in csv_text
    assert "0.123400" in csv_text
    assert "| Unit Model | openai/unit | 80 | 80 | $0.123400 | unit-prices |" in markdown_text
    assert "unit warning" in markdown_text


def test_estimate_model_panel_costs_falls_back_to_panel_price_metadata(
    tmp_path: Path,
):
    panel_path = tmp_path / "panel.yaml"
    csv_path = tmp_path / "costs.csv"
    markdown_path = tmp_path / "costs.md"
    panel_path.write_text(
        yaml.safe_dump(
            {
                "schema_version": "paper-model-panel-v1",
                "profile": "hard_obvious_8x10",
                "seed": 20260531,
                "entries": [
                    {
                        "id": "unit-grok",
                        "label": "Unit Grok",
                        "provider_route": "grok",
                        "inspect_model": "grok/unit",
                        "temperature": 0,
                        "max_tokens": 64,
                        "input_price_per_mtok_usd": 1.25,
                        "output_price_per_mtok_usd": 2.5,
                        "run_status": "planned",
                    }
                ],
            },
            sort_keys=False,
        ),
        encoding="utf-8",
    )

    def fake_estimator(inputs):
        return SimpleNamespace(
            model=inputs.model,
            total_samples=1,
            billable_samples=1,
            cache_hits=0,
            estimated_billable_cost_usd=0.0,
            pricing_source="runcost",
            warnings=("No price card found for provider grok.",),
            rows=(
                SimpleNamespace(
                    cache_hit=False,
                    input_tokens=100,
                    output_tokens=20,
                    reasoning_tokens=10,
                ),
            ),
        )

    estimate_model_panel_costs(
        ModelPanelCostInputs(
            panel_path=panel_path,
            csv_path=csv_path,
            markdown_path=markdown_path,
            estimator=fake_estimator,
        )
    )

    csv_text = csv_path.read_text(encoding="utf-8")
    markdown_text = markdown_path.read_text(encoding="utf-8")
    assert "0.000200" in csv_text
    assert "panel_price_metadata" in csv_text
    assert "runcost price card missing; used panel price metadata" in markdown_text
