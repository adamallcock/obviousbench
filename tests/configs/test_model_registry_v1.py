from collections import Counter
from pathlib import Path
from typing import Any

import yaml

REGISTRY_PATH = Path("configs/registries/model_registry_v1.yaml")
OUTPUT_SAFETY_MAX_TOKENS = 10_000
UNCAPPED_PROVIDER_DEFAULT_ENTRY_IDS = {
    "openrouter-requested-2026-07-21-nousresearch-hermes-3-llama-3-1-70b",
    "openrouter-requested-2026-07-21-rekaai-reka-flash-3",
}
NOVA_2_LITE_UNCAPPED_ENTRY_IDS = {
    "bedrock-flex-us-amazon-nova-2-lite-v1-0-none-omitted",
    "bedrock-flex-us-amazon-nova-2-lite-v1-0-low",
    "bedrock-flex-us-amazon-nova-2-lite-v1-0-medium",
    "bedrock-flex-us-amazon-nova-2-lite-v1-0-high",
}


def _registry() -> dict[str, Any]:
    return yaml.safe_load(REGISTRY_PATH.read_text(encoding="utf-8"))


def _entries() -> list[dict[str, Any]]:
    return _registry()["entries"]


def test_model_registry_v1_has_comprehensive_coverage():
    registry = _registry()
    entries = registry["entries"]
    route_counts = Counter(entry["provider_route"] for entry in entries)

    assert registry["schema_version"] == "model-registry-v1"
    assert registry["defaults"]["profile"] == "hard_obvious_8x10"
    assert registry["defaults"]["seed"] == 20260531
    assert len(entries) == 326
    assert route_counts["openrouter"] >= 220
    assert {
        "openrouter",
        "openai",
        "anthropic",
        "gemini",
        "gemini-flex",
        "grok",
        "tinker",
        "aion",
        "longcat",
        "bedrock-standard",
        "bedrock-flex",
        "perplexity",
        "zai",
        "cohere",
    }.issubset(route_counts)
    assert sum("free" in entry["tags"] for entry in entries) >= 15
    assert sum(
        "small" in entry["tags"] or "open-weight" in entry["tags"]
        for entry in entries
    ) >= 200


def test_model_registry_entries_are_unique_and_runnable():
    entries = _entries()
    ids = [entry["id"] for entry in entries]
    inspect_models = [entry["inspect_model"] for entry in entries]

    assert len(set(ids)) == len(ids)
    assert all("<" not in model and ">" not in model for model in inspect_models)

    for entry in entries:
        settings = entry["generation_settings"]
        assert entry["profile"] == "hard_obvious_8x10"
        assert entry["seed"] == 20260531
        assert entry["inspect_model"].count("/") >= 1
        uncapped = entry["id"] in (
            UNCAPPED_PROVIDER_DEFAULT_ENTRY_IDS | NOVA_2_LITE_UNCAPPED_ENTRY_IDS
        )
        if "temperature" in settings:
            assert settings["temperature"] == 0
        else:
            assert entry["id"] in {
                "kimi-k3-max",
                "bedrock-flex-us-amazon-nova-2-lite-v1-0-high",
            }
        if uncapped:
            assert "max_tokens" not in settings
            assert "max_tokens" in entry["omit_generation_settings"]
        else:
            assert isinstance(settings["max_tokens"], int)
        advertised_max = int(entry.get("max_output_tokens") or 0)
        expected_max = (
            advertised_max
            if 0 < advertised_max < OUTPUT_SAFETY_MAX_TOKENS
            else OUTPUT_SAFETY_MAX_TOKENS
        )
        if not uncapped:
            assert settings["max_tokens"] == expected_max
        assert entry["pricing_source"] in {
            "openrouter_models_api",
            "runcost_external_price_resolution",
            "xai_grok_4_5_docs_2026_07_08",
            "meta_model_api_blog_2026_07_09",
            "openai_standard_short_context_2026_07_09",
            "deepseek_v4_pricing_2026_07_14",
            "tinker_inkling_undiscounted_pricing_2026_07_15",
            "kimi_k3_standard_pricing_2026_07_16",
            "vertex_gemini_standard_pricing_2026_07_21",
            "gemini_api_standard_pricing_2026_07_21",
            "longcat_normal_pricing_2026_07_21",
            "aionlabs_direct_pricing_2026_07_21",
            "cohere_direct_public_pricing_2026_07_21",
            "cohere_user_supplied_standard_equivalent_pricing_2026_07_21",
            "cohere_north_mini_code_public_free_pricing_2026_07_21",
            "bedrock_nova_us_geo_standard_pricing_2026_07_21",
            "perplexity_sonar_standard_pricing_2026_07_21",
            "zai_glm_5_2_standard_pricing_2026_07_21",
            "nvidia_nim_free_endpoint_pricing_2026_07_21",
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

    assert registry["sources"]["runcost_external_price_resolution"]["card_count"] >= 1000
    assert registry["sources"]["openrouter_models_api"]["selected_count"] >= 220

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


def test_tencent_hy3_catalog_route_uses_current_openrouter_pricing():
    entries = _entries()
    [hy3] = [
        entry
        for entry in entries
        if entry["id"] == "openrouter-098-tencent-hy3"
    ]

    assert hy3["provider_route"] == "openrouter"
    assert hy3["upstream_provider"] == "tencent"
    assert hy3["inspect_model"] == "openrouter/tencent/hy3"
    assert hy3["model_id"] == "tencent/hy3"
    assert hy3["input_price_per_mtok_usd"] == 0.14
    assert hy3["output_price_per_mtok_usd"] == 0.58
    assert hy3["pricing_source"] == "openrouter_models_api"
    assert "open-weight" in hy3["tags"]
    assert "cheap" in hy3["tags"]


def test_model_registry_includes_grok_4_5_with_manual_xai_price():
    entries = _entries()
    rows = [entry for entry in entries if entry["id"] == "grok-4-5"]

    assert len(rows) == 1
    row = rows[0]
    assert row["label"] == "Grok 4.5"
    assert row["inspect_model"] == "grok/grok-4.5"
    assert row["model_id"] == "grok-4.5"
    assert row["provider_route"] == "grok"
    assert row["upstream_provider"] == "xai"
    assert row["input_price_per_mtok_usd"] == 2.0
    assert row["output_price_per_mtok_usd"] == 6.0
    assert row["pricing_source"] == "xai_grok_4_5_docs_2026_07_08"


def test_model_registry_includes_gpt_5_6_defaults_with_standard_prices():
    rows = {
        entry["model_id"]: entry
        for entry in _entries()
        if entry["id"].startswith("openai-gpt-5-6-")
    }

    assert set(rows) == {"gpt-5.6-sol", "gpt-5.6-terra", "gpt-5.6-luna"}
    assert {
        model_id: (
            row["input_price_per_mtok_usd"],
            row["output_price_per_mtok_usd"],
        )
        for model_id, row in rows.items()
    } == {
        "gpt-5.6-sol": (5, 30),
        "gpt-5.6-terra": (2.5, 15),
        "gpt-5.6-luna": (1, 6),
    }
    for row in rows.values():
        assert row["provider_route"] == "openai"
        assert row["generation_settings"]["reasoning_effort"] == "medium"
        assert row["generation_settings"]["extra_body"] == {"service_tier": "flex"}
        assert row["pricing_source"] == "openai_standard_short_context_2026_07_09"


def test_model_registry_includes_tinker_inkling_effort_rows_at_undiscounted_prices():
    rows = {
        entry["id"]: entry
        for entry in _entries()
        if entry["provider_route"] == "tinker"
    }

    assert set(rows) == {
        "tinker-inkling-none",
        "tinker-inkling-minimal",
        "tinker-inkling-low",
        "tinker-inkling-medium",
        "tinker-inkling-high",
        "tinker-inkling-xhigh",
    }
    assert {row["generation_settings"].get("reasoning_effort") for row in rows.values()} == {
        "none",
        "minimal",
        "low",
        "medium",
        "high",
        "xhigh",
    }
    assert all(
        row["inspect_model"] == "tinker/thinkingmachines/Inkling"
        and row["model_id"] == "thinkingmachines/Inkling"
        and row["provider_api"] == "tinker_openai_compatible"
        and row["pricing_source"] == "tinker_inkling_undiscounted_pricing_2026_07_15"
        and row["input_price_per_mtok_usd"] == 3.74
        and row["cached_input_price_per_mtok_usd"] == 0.748
        and row["output_price_per_mtok_usd"] == 9.36
        for row in rows.values()
    )


def test_provider_expansion_routes_preserve_documented_controls_and_standard_prices():
    entries = {entry["id"]: entry for entry in _entries()}

    aion = entries["aion-aion-labs-aion-3-0-provider-default"]
    assert (aion["input_price_per_mtok_usd"], aion["output_price_per_mtok_usd"]) == (3, 6)
    assert aion["inspect_model"] == "aion/aion-labs/aion-3.0"

    for entry_id in (
        "longcat-longcat-2-0-thinking-disabled",
        "longcat-longcat-2-0-thinking-enabled",
    ):
        row = entries[entry_id]
        assert row["inspect_model"] == "longcat/LongCat-2.0"
        assert (row["input_price_per_mtok_usd"], row["output_price_per_mtok_usd"]) == (
            0.75,
            2.95,
        )

    nova = entries["bedrock-flex-us-amazon-nova-2-lite-v1-0-high"]
    assert nova["execution_service_tier"] == "flex"
    assert nova["public_pricing_service_tier"] == "standard"
    assert nova["omit_generation_settings"] == ["max_tokens", "temperature", "top_p", "top_k"]
    assert "max_tokens" not in nova["generation_settings"]

    gemini = entries["gemini-flex-gemini-3-6-flash-medium"]
    assert gemini["execution_service_tier"] == "flex"
    assert gemini["public_pricing_service_tier"] == "standard"
    assert (gemini["input_price_per_mtok_usd"], gemini["output_price_per_mtok_usd"]) == (
        1.5,
        7.5,
    )

    glm = entries["zai-glm-5-2-xhigh"]
    assert glm["generation_settings"]["reasoning_effort"] == "xhigh"
    assert glm["generation_settings"]["extra_body"] == {"thinking": {"type": "enabled"}}

    sonar = entries["perplexity-sonar-reasoning-pro-provider-default"]
    assert (sonar["input_price_per_mtok_usd"], sonar["output_price_per_mtok_usd"]) == (2, 8)
    assert sonar["request_fee_usd_per_1k"] == 6


def test_provider_expansion_weight_statuses_are_source_backed():
    entries = {entry["id"]: entry for entry in _entries()}
    expected = {
        "longcat-longcat-2-0-thinking-disabled": (
            "open_weights",
            "https://huggingface.co/meituan-longcat/LongCat-2.0",
        ),
        "longcat-longcat-2-0-thinking-enabled": (
            "open_weights",
            "https://huggingface.co/meituan-longcat/LongCat-2.0",
        ),
        "aion-aion-labs-aion-rp-llama-3-1-8b-provider-default": (
            "open_weights",
            "https://huggingface.co/aion-labs/Aion-RP-Llama-3.1-8B",
        ),
        "zai-glm-5-2-high": (
            "open_weights",
            "https://huggingface.co/zai-org/GLM-5.2",
        ),
        "openrouter-requested-2026-07-21-deepcogito-cogito-v2-1-671b": (
            "open_weights",
            "https://huggingface.co/blog/deepcogito/cogito-v2-1",
        ),
        "openrouter-requested-2026-07-21-inclusionai-ling-2-6-1t": (
            "open_weights",
            "https://huggingface.co/inclusionAI/Ling-2.6-1T",
        ),
        "openrouter-requested-2026-07-21-inclusionai-ling-2-6-flash": (
            "open_weights",
            "https://huggingface.co/inclusionAI/Ling-2.6-flash",
        ),
        "openrouter-requested-2026-07-21-inclusionai-ring-2-6-1t": (
            "open_weights",
            "https://huggingface.co/inclusionAI/Ring-2.6-1T",
        ),
        "openrouter-147-moonshotai-kimi-k3": (
            "proprietary",
            "https://platform.kimi.ai/docs/guide/kimi-k3-quickstart",
        ),
    }
    for entry_id, (status, source) in expected.items():
        entry = entries[entry_id]
        assert entry["weight_status"] == status
        assert entry["weight_status_source_refs"] == [source]


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
