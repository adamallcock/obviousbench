from __future__ import annotations

import tomllib
from pathlib import Path
from typing import Any

import yaml

PANEL_PATH = Path("configs/paper_v1_model_panel.yaml")
OUTPUT_SAFETY_MAX_TOKENS = 10_000


def _panel() -> dict[str, Any]:
    return yaml.safe_load(PANEL_PATH.read_text(encoding="utf-8"))


def test_paper_v1_model_panel_is_frozen_and_balanced():
    panel = _panel()
    entries = panel["entries"]
    route_counts: dict[str, int] = {}
    ids = [entry["id"] for entry in entries]
    gates = " ".join(panel["selection_policy"]["do_not_run_until"]).lower()

    assert panel["schema_version"] == "paper-model-panel-v1"
    assert panel["dataset_manifest"] == "data/splits/paper_v1_manifest.jsonl"
    assert panel["run_status"] == "planned_not_run"
    assert 8 <= len(entries) <= 14
    assert len(set(ids)) == len(ids)

    for entry in entries:
        route_counts[entry["provider_route"]] = route_counts.get(entry["provider_route"], 0) + 1

    assert route_counts["openrouter"] >= 3
    assert {"openai", "anthropic", "gemini", "grok"}.issubset(route_counts)
    assert "human-baseline" not in gates
    assert "readiness-preprint" in gates
    assert panel["selection_policy"]["strict_release_requirements"][
        "human_baseline"
    ].startswith("required")


def test_paper_v1_model_panel_entries_are_documented_and_non_secret():
    panel = _panel()
    forbidden_key_parts = ("api_key", "apikey", "password", "secret")
    forbidden_value_parts = ("sk-", "xai-", "AIza", "anthropic_api_key")
    required = {
        "id",
        "label",
        "provider_route",
        "inspect_model",
        "role",
        "temperature",
        "max_tokens",
        "pricing_source",
        "run_status",
        "selection_rationale",
    }

    def walk(value: Any):
        if isinstance(value, dict):
            for key, child in value.items():
                assert not any(part in str(key).lower() for part in forbidden_key_parts)
                yield from walk(child)
        elif isinstance(value, list):
            for child in value:
                yield from walk(child)
        elif isinstance(value, str):
            yield value

    for entry in panel["entries"]:
        assert required.issubset(entry)
        assert entry["run_status"] == "planned"
        assert entry["temperature"] == 0
        assert entry["max_tokens"] == OUTPUT_SAFETY_MAX_TOKENS
        assert entry["selection_rationale"]

    for text in walk(panel):
        lowered = text.lower()
        assert not any(part.lower() in lowered for part in forbidden_value_parts)


def test_paper_v1_provider_routes_have_runtime_dependencies():
    panel = _panel()
    pyproject = tomllib.loads(Path("pyproject.toml").read_text(encoding="utf-8"))
    dependencies = " ".join(pyproject["project"]["dependencies"]).lower()
    provider_routes = {entry["provider_route"] for entry in panel["entries"]}

    assert "anthropic" not in provider_routes or "anthropic" in dependencies
    assert "openai" not in provider_routes or "openai" in dependencies
    assert "grok" not in provider_routes or "xai_sdk" in dependencies
    assert "gemini" not in provider_routes or "google-genai" in dependencies
