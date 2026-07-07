from collections import Counter
from pathlib import Path
from typing import Any

import yaml

REGISTRY_PATH = Path("configs/registries/model_registry_v1.yaml")
OUTPUT_SAFETY_MAX_TOKENS = 10_000


def _registry() -> dict[str, Any]:
    return yaml.safe_load(REGISTRY_PATH.read_text(encoding="utf-8"))


def _entries() -> list[dict[str, Any]]:
    return _registry()["entries"]


def test_model_registry_v1_has_comprehensive_coverage():
    registry = _registry()
    entries = registry["entries"]
    route_counts = Counter(entry["provider_route"] for entry in entries)

    assert registry["schema_version"] == "model-registry-v1"
    assert registry["defaults"]["profile"] == "balanced_8x5"
    assert registry["defaults"]["seed"] == 20260531
    assert 190 <= len(entries) <= 230
    assert route_counts["openrouter"] >= 180
    assert {"openrouter", "openai", "anthropic", "gemini", "grok"}.issubset(
        route_counts
    )
    assert sum("free" in entry["tags"] for entry in entries) >= 20
    assert sum(
        "small" in entry["tags"] or "open-weight" in entry["tags"]
        for entry in entries
    ) >= 100


def test_model_registry_entries_are_unique_and_runnable():
    entries = _entries()
    ids = [entry["id"] for entry in entries]
    inspect_models = [entry["inspect_model"] for entry in entries]

    assert len(set(ids)) == len(ids)
    assert all("<" not in model and ">" not in model for model in inspect_models)

    for entry in entries:
        settings = entry["generation_settings"]
        assert entry["profile"] == "balanced_8x5"
        assert entry["seed"] == 20260531
        assert entry["inspect_model"].count("/") >= 1
        assert settings["temperature"] == 0
        assert isinstance(settings["max_tokens"], int)
        advertised_max = int(entry.get("max_output_tokens") or 0)
        expected_max = (
            advertised_max
            if 0 < advertised_max < OUTPUT_SAFETY_MAX_TOKENS
            else OUTPUT_SAFETY_MAX_TOKENS
        )
        assert settings["max_tokens"] == expected_max
        assert entry["pricing_source"] in {
            "openrouter_models_api",
            "runcost_default_price_cards",
            "manual_lookup_required",
        }
        assert isinstance(entry["tags"], list)
        assert entry["tags"]


def test_gpt_5_0_aliases_do_not_request_unsupported_none_reasoning():
    for entry in _entries():
        if entry["provider_route"] != "openai":
            continue
        if entry["model_id"] not in {"gpt-5", "gpt-5-mini", "gpt-5-nano"}:
            continue

        settings = entry["generation_settings"]
        assert settings.get("reasoning_effort") != "none"
        assert settings.get("reasoning_effort") in {"minimal", "low", "medium", "high"}


def test_model_registry_price_metadata_is_explicit():
    entries = _entries()
    registry = _registry()

    assert registry["sources"]["runcost_default_price_cards"]["card_count"] >= 7000
    assert registry["sources"]["openrouter_models_api"]["selected_count"] >= 180

    for entry in entries:
        missing_price = (
            entry.get("input_price_per_mtok_usd") is None
            or entry.get("output_price_per_mtok_usd") is None
        )
        if missing_price:
            assert entry["pricing_source"] == "manual_lookup_required"
            assert entry["runcost_price_card_id"] is None
        else:
            assert entry["input_price_per_mtok_usd"] >= 0
            assert entry["output_price_per_mtok_usd"] >= 0


def test_tencent_hy3_release_route_is_pinned_with_paid_equivalent_pricing():
    entries = _entries()
    [hy3] = [
        entry
        for entry in entries
        if entry["id"] == "openrouter-pinned-tencent-hy3-free"
    ]

    assert hy3["provider_route"] == "openrouter"
    assert hy3["upstream_provider"] == "tencent"
    assert hy3["inspect_model"] == "openrouter/tencent/hy3:free"
    assert hy3["model_id"] == "tencent/hy3:free"
    assert hy3["priced_as_model_id"] == "tencent/hy3"
    assert hy3["input_price_per_mtok_usd"] == 0.2
    assert hy3["output_price_per_mtok_usd"] == 0.8
    assert hy3["cache_read_price_per_mtok_usd"] == 0.5
    assert hy3["pricing_source"] == "openrouter_models_api"
    assert "free-endpoint" in hy3["tags"]
    assert "paid-equivalent-pricing" in hy3["tags"]


def test_model_registry_does_not_store_secrets():
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

    for text in walk(_registry()):
        lowered = text.lower()
        assert not any(part.lower() in lowered for part in forbidden_value_parts)
