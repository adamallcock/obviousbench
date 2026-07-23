from __future__ import annotations

import asyncio
from types import SimpleNamespace

import pytest
from inspect_ai._util.error import PrerequisiteError
from inspect_ai.model import GenerateConfig, get_model
from inspect_ai.model._providers.google import GoogleGenAIAPI

from obviousbench.providers.gemini_flex import (
    GEMINI_API_KEY_ENV_VAR,
    GEMINI_FLEX_MODEL_IDS,
    GEMINI_FLEX_REASONING_EFFORTS,
    GEMINI_FLEX_SERVICE_TIER,
    GeminiFlexAPI,
    gemini_flex_request_body,
    normalize_gemini_flex_model_name,
    resolve_gemini_api_key,
    validate_gemini_flex_config,
)


def _clear_gemini_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv(GEMINI_API_KEY_ENV_VAR, raising=False)


def test_gemini_flex_adapter_uses_direct_developer_api_key(monkeypatch):
    _clear_gemini_env(monkeypatch)
    monkeypatch.setenv(GEMINI_API_KEY_ENV_VAR, "test-gemini-key")

    api = GeminiFlexAPI("gemini-3.6-flash")
    try:
        assert not api.is_vertex()
        assert api.service_model_name() == "gemini-3.6-flash"
        assert api.execution_mode == GEMINI_FLEX_SERVICE_TIER
        assert api.api_key == "test-gemini-key"
    finally:
        asyncio.run(api.aclose())


def test_gemini_flex_registered_route_resolves_through_inspect(monkeypatch):
    _clear_gemini_env(monkeypatch)
    monkeypatch.setenv(GEMINI_API_KEY_ENV_VAR, "test-gemini-key")

    model = get_model("gemini-flex/gemini-3.5-flash-lite", memoize=False)
    try:
        assert type(model.api).__name__ == "GeminiFlexAPI"
        assert model.api.service_model_name() == "gemini-3.5-flash-lite"
        assert model.api.execution_mode == GEMINI_FLEX_SERVICE_TIER
    finally:
        asyncio.run(model.api.aclose())


@pytest.mark.parametrize(
    ("model_name", "effort", "expected_level"),
    [
        (model_name, effort, expected_level)
        for model_name in sorted(GEMINI_FLEX_MODEL_IDS)
        for effort, expected_level in (
            ("minimal", "MINIMAL"),
            ("low", "LOW"),
            ("medium", "MEDIUM"),
            ("high", "HIGH"),
        )
    ],
)
def test_gemini_flex_maps_each_documented_thinking_level(
    model_name, effort, expected_level
):
    api = GeminiFlexAPI(model_name, api_key="test-gemini-key")
    try:
        thinking = api.chat_thinking_config(GenerateConfig(reasoning_effort=effort))
        assert thinking is not None
        assert thinking.include_thoughts is True
        assert thinking.thinking_level.name == expected_level
    finally:
        asyncio.run(api.aclose())


@pytest.mark.parametrize(
    "config",
    [
        GenerateConfig(reasoning_effort="none"),
        GenerateConfig(reasoning_effort="xhigh"),
        GenerateConfig(reasoning_tokens=0),
        GenerateConfig(batch=True),
        GenerateConfig(extra_body={"serviceTier": "standard"}),
    ],
)
def test_gemini_flex_rejects_unsupported_or_misleading_controls(config):
    with pytest.raises(ValueError):
        validate_gemini_flex_config(config)


@pytest.mark.parametrize("effort", sorted(GEMINI_FLEX_REASONING_EFFORTS))
def test_gemini_flex_accepts_only_documented_named_levels(effort):
    validate_gemini_flex_config(GenerateConfig(reasoning_effort=effort))


def test_gemini_flex_model_and_key_guards(monkeypatch):
    _clear_gemini_env(monkeypatch)

    with pytest.raises(PrerequisiteError) as exc_info:
        resolve_gemini_api_key()
    assert GEMINI_API_KEY_ENV_VAR in str(exc_info.value)
    assert resolve_gemini_api_key("explicit-key") == "explicit-key"
    assert normalize_gemini_flex_model_name("gemini-flex/gemini-3.6-flash") == (
        "gemini-3.6-flash"
    )
    with pytest.raises(ValueError, match="verified released models"):
        normalize_gemini_flex_model_name("gemini-3.6-pro")
    with pytest.raises(ValueError, match="Flex tier"):
        GeminiFlexAPI(
            "gemini-3.6-flash",
            api_key="test-gemini-key",
            execution_mode="standard",
        )


def test_gemini_flex_injects_top_level_tier_only_for_generation_paths():
    body = {"contents": [], "generationConfig": {"thinkingConfig": {}}}
    configured = gemini_flex_request_body(
        "models/gemini-3.6-flash:generateContent", body
    )

    assert configured == {
        "contents": [],
        "generationConfig": {"thinkingConfig": {}},
        "serviceTier": "flex",
    }
    assert body == {"contents": [], "generationConfig": {"thinkingConfig": {}}}
    assert gemini_flex_request_body("models/gemini-3.6-flash:countTokens", body) is body
    with pytest.raises(ValueError, match="non-Flex serviceTier"):
        gemini_flex_request_body(
            "models/gemini-3.6-flash:streamGenerateContent",
            {"serviceTier": "standard"},
        )


def test_gemini_flex_decorates_regular_and_streaming_sdk_requests(monkeypatch):
    captured: list[tuple[str, str, dict[str, object]]] = []

    class FakeAPIClient:
        async def async_request(self, method, path, body, http_options=None):
            captured.append((method, path, body))
            return "regular"

        async def async_request_streamed(self, method, path, body, http_options=None):
            captured.append((method, path, body))
            return "stream"

    fake_client = SimpleNamespace(_api_client=FakeAPIClient())

    def fake_model_client(self, http_options=None):
        return fake_client

    monkeypatch.setattr(GoogleGenAIAPI, "model_client", fake_model_client)
    api = GeminiFlexAPI("gemini-3.6-flash", api_key="test-gemini-key")

    async def exercise() -> None:
        client = api.model_client()
        assert await client._api_client.async_request(
            "post", "models/gemini-3.6-flash:generateContent", {"contents": []}
        ) == "regular"
        assert await client._api_client.async_request_streamed(
            "post",
            "models/gemini-3.6-flash:streamGenerateContent?alt=sse",
            {"contents": []},
        ) == "stream"
        assert await client._api_client.async_request(
            "post", "models/gemini-3.6-flash:countTokens", {"contents": []}
        ) == "regular"

    try:
        asyncio.run(exercise())
    finally:
        asyncio.run(api.aclose())

    assert captured == [
        (
            "post",
            "models/gemini-3.6-flash:generateContent",
            {"contents": [], "serviceTier": "flex"},
        ),
        (
            "post",
            "models/gemini-3.6-flash:streamGenerateContent?alt=sse",
            {"contents": [], "serviceTier": "flex"},
        ),
        ("post", "models/gemini-3.6-flash:countTokens", {"contents": []}),
    ]
