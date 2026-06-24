from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import Any

import yaml

PANEL_PATH = Path("configs/registries/model_thinking_settings_v1.yaml")


def _panel() -> dict[str, Any]:
    return yaml.safe_load(PANEL_PATH.read_text(encoding="utf-8"))


def _entries() -> list[dict[str, Any]]:
    return _panel()["entries"]


def test_thinking_settings_panel_has_frontier_coverage():
    panel = _panel()
    entries = panel["entries"]
    route_counts = Counter(entry["provider_route"] for entry in entries)
    depth_counts = Counter(entry["thinking_depth"] for entry in entries)

    assert panel["schema_version"] == "model-thinking-settings-v1"
    assert panel["run_status"] == "planned_not_run"
    assert panel["defaults"]["profile"] == "balanced_8x5"
    assert panel["defaults"]["seed"] == 20260531
    assert 200 <= len(entries) <= 260
    assert {"openai", "anthropic", "gemini", "grok", "openrouter"}.issubset(
        route_counts
    )
    assert route_counts["openrouter"] >= 100
    assert route_counts["openai"] >= 30
    assert route_counts["anthropic"] >= 20
    assert route_counts["gemini"] >= 20
    assert route_counts["grok"] >= 8
    assert {"minimal", "low", "medium", "high", "xhigh", "max"}.issubset(
        depth_counts
    )


def test_thinking_settings_entries_are_unique_priced_and_runnable():
    panel = _panel()
    entries = panel["entries"]
    ids = [entry["id"] for entry in entries]

    assert len(set(ids)) == len(ids)
    assert panel["totals"]["entry_count"] == len(entries)
    assert panel["totals"]["priced_entry_count"] == len(entries)
    assert panel["totals"]["estimated_full_panel_cost_usd"] > 0
    assert panel["totals"]["estimated_full_panel_cost_usd"] < 150
    assert panel["sources"]["runcost_default_price_cards"]["card_count"] >= 7000
    assert panel["sources"]["openrouter_models_api"]["selected_model_count"] >= 30
    assert panel["sources"]["usage_calibration"]["basis"] == (
        "measured_usage_with_conservative_buffer"
    )

    for entry in entries:
        usage = entry["estimated_usage"]
        settings = entry["generation_settings"]

        assert entry["profile"] == "balanced_8x5"
        assert entry["seed"] == 20260531
        assert entry["run_status"] == "planned"
        assert entry["inspect_model"].count("/") >= 1
        assert isinstance(settings["max_tokens"], int)
        assert settings["max_tokens"] >= 64
        assert entry["configured_reasoning_tokens_per_sample"] >= 0
        assert entry["configured_reasoning_tokens_per_sample"] >= usage[
            "reasoning_tokens_per_sample"
        ]
        assert usage["sample_count"] == 80
        assert usage["reasoning_tokens_per_sample"] >= 0
        assert usage["calibration_source"].startswith(
            "measured_usage_with_conservative_buffer:"
        )
        assert usage["output_tokens_billed"] == (
            usage["visible_output_tokens"] + usage["reasoning_tokens"]
        )
        assert entry["estimated_cost_usd"] is not None
        assert entry["estimated_cost_usd"] >= 0
        assert entry["pricing_source"] in {
            "openrouter_models_api",
            "openrouter_models_api_proxy_price",
            "runcost_default_price_cards",
        }


def test_gpt_5_0_thinking_panel_excludes_unsupported_none_reasoning():
    direct_gpt_5_0_ids = {"gpt-5", "gpt-5-mini", "gpt-5-nano"}

    for entry in _entries():
        if entry["provider_route"] == "openai" and entry["model_id"] in direct_gpt_5_0_ids:
            assert entry["thinking_depth"] != "none"
            assert entry["generation_settings"].get("reasoning_effort") != "none"
        if (
            entry["provider_route"] == "openrouter"
            and entry["model_id"].startswith("openai/gpt-5")
            and not any(suffix in entry["model_id"] for suffix in (".2", ".4", ".5"))
        ):
            assert entry["thinking_depth"] != "none"
            assert entry["generation_settings"].get("reasoning_effort") != "none"


def test_thinking_settings_include_required_frontier_examples():
    ids = {entry["id"] for entry in _entries()}
    required_ids = {
        "openai-gpt-5-minimal",
        "openai-gpt-5-mini-minimal",
        "anthropic-claude-opus-4-8-high",
        "anthropic-claude-sonnet-4-6-high",
        "gemini-gemini-2-5-pro-high",
        "grok-grok-4-20-multi-agent-xhigh",
    }

    assert required_ids.issubset(ids)
    assert any(entry_id.startswith("openrouter-deepseek-deepseek-r1") for entry_id in ids)
    assert sum(entry_id.startswith("openrouter-minimax-minimax-m3") for entry_id in ids) >= 3
    assert any(entry_id.startswith("openrouter-qwen-qwen3") for entry_id in ids)


def test_thinking_settings_exclude_expensive_research_system_variants():
    excluded_model_ids = {
        "gpt-5-pro",
        "gpt-5.5-pro",
        "gpt-5.4-pro",
        "gpt-5.2-pro",
        "openai/gpt-5-pro",
        "openai/gpt-5.5-pro",
        "openai/gpt-5.4-pro",
        "openai/gpt-5.2-pro",
        "anthropic/claude-opus-4.8-fast",
        "anthropic/claude-opus-4.7-fast",
        "anthropic/claude-opus-4.6-fast",
    }

    for entry in _entries():
        assert entry["model_id"] not in excluded_model_ids
        assert entry["inspect_model"].removeprefix("openrouter/") not in excluded_model_ids


def test_thinking_settings_does_not_store_secrets():
    forbidden_key_parts = ("api_key", "apikey", "password", "secret")
    forbidden_value_parts = ("sk-", "xai-", "AIza", "anthropic_api_key")

    def walk(value: Any):
        if isinstance(value, dict):
            for key, child in value.items():
                lowered_key = str(key).lower()
                assert not any(part in lowered_key for part in forbidden_key_parts)
                yield from walk(child)
        elif isinstance(value, list):
            for child in value:
                yield from walk(child)
        elif isinstance(value, str):
            yield value

    for text in walk(_panel()):
        lowered = text.lower()
        assert not any(part.lower() in lowered for part in forbidden_value_parts)
