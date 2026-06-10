import importlib.util
import sys
from pathlib import Path


def _module():
    spec = importlib.util.spec_from_file_location(
        "smoke_model_registry",
        Path("scripts/smoke_model_registry.py"),
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _entry(provider_route="openrouter", **overrides):
    entry = {
        "id": "entry-1",
        "label": "Entry 1",
        "provider_route": provider_route,
        "inspect_model": f"{provider_route}/model-1",
        "model_id": "vendor/model-1" if provider_route == "openrouter" else "model-1",
        "generation_settings": {"temperature": 0, "max_tokens": 64},
        "tags": ["small"],
    }
    entry.update(overrides)
    return entry


def test_select_entries_filters_by_provider_tag_and_limit():
    smoke = _module()
    entries = [
        _entry("openrouter", id="a", tags=["free", "small"]),
        _entry("openai", id="b", tags=["small"]),
        _entry("openrouter", id="c", tags=["open-weight"]),
    ]

    selected = smoke.select_entries(
        entries,
        provider_routes={"openrouter"},
        tags={"free"},
        entry_ids=set(),
        offset=0,
        limit=1,
    )

    assert [entry["id"] for entry in selected] == ["a"]


def test_build_openrouter_request_uses_model_id_not_inspect_prefix():
    smoke = _module()
    request = smoke.build_request(
        _entry("openrouter", model_id="qwen/qwen3:free"),
        "test-key",
        "Reply OK",
        16,
    )

    assert request.url == "https://openrouter.ai/api/v1/chat/completions"
    assert request.payload["model"] == "qwen/qwen3:free"
    assert request.payload["max_tokens"] == 16
    assert request.headers["authorization"] == "Bearer test-key"


def test_build_openai_request_maps_reasoning_effort_to_responses_api():
    smoke = _module()
    request = smoke.build_request(
        _entry(
            "openai",
            model_id="gpt-5.5",
            generation_settings={
                "temperature": 0,
                "max_tokens": 64,
                "reasoning_effort": "none",
            },
        ),
        "test-key",
        "Reply OK",
        8,
    )

    assert request.url == "https://api.openai.com/v1/responses"
    assert request.payload == {
        "model": "gpt-5.5",
        "input": "Reply OK",
        "max_output_tokens": 8,
        "reasoning": {"effort": "none"},
    }


def test_extract_text_handles_provider_response_shapes():
    smoke = _module()

    assert (
        smoke.extract_text(
            "openrouter",
            {"choices": [{"message": {"content": "OK"}}]},
        )
        == "OK"
    )
    assert smoke.extract_text("openai", {"output_text": "OK"}) == "OK"
    assert (
        smoke.extract_text("anthropic", {"content": [{"type": "text", "text": "OK"}]})
        == "OK"
    )
    assert (
        smoke.extract_text(
            "gemini",
            {"candidates": [{"content": {"parts": [{"text": "OK"}]}}]},
        )
        == "OK"
    )


def test_write_summaries_creates_one_compact_summary_set(tmp_path):
    smoke = _module()
    rows = [
        {"provider_route": "openrouter", "status": "ok", "answer_exact_ok": True},
        {"provider_route": "openai", "status": "auth_error", "answer_exact_ok": False},
    ]

    smoke.write_summaries(tmp_path, rows)

    assert (tmp_path / "summary.csv").exists()
    assert (tmp_path / "summary.md").exists()
    assert "openrouter" in (tmp_path / "summary.md").read_text()
