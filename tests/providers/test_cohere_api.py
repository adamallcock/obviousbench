from __future__ import annotations

import asyncio
import json

import httpx
import pytest
from inspect_ai._util.content import ContentReasoning, ContentText
from inspect_ai._util.error import PrerequisiteError
from inspect_ai.model import GenerateConfig, get_model
from inspect_ai.model._chat_message import ChatMessageSystem, ChatMessageUser

from obviousbench.providers.cohere import (
    COHERE_API_KEY_VARS,
    COHERE_BASE_URL_VARS,
    COHERE_BENCHMARK_THINKING_TOKEN_BUDGETS,
    DEFAULT_COHERE_BASE_URL,
    CohereAPI,
    cohere_chat_headers,
    cohere_chat_request,
    cohere_model_output,
    cohere_thinking_disabled,
    cohere_thinking_enabled,
    normalize_cohere_thinking,
    resolve_cohere_api_key,
    resolve_cohere_base_url,
)


def _clear_cohere_env(monkeypatch: pytest.MonkeyPatch) -> None:
    for env_var in (*COHERE_API_KEY_VARS, *COHERE_BASE_URL_VARS):
        monkeypatch.delenv(env_var, raising=False)


def _response_body() -> dict[str, object]:
    return {
        "id": "cohere-response-unit",
        "finish_reason": "COMPLETE",
        "message": {
            "role": "assistant",
            "content": [
                {"type": "thinking", "thinking": "Check the arithmetic."},
                {"type": "text", "text": "Four."},
            ],
        },
        "usage": {
            "tokens": {"input_tokens": 17, "output_tokens": 12},
            "billed_units": {"input_tokens": 9, "output_tokens": 12},
        },
    }


def test_cohere_adapter_uses_native_v2_defaults(monkeypatch):
    _clear_cohere_env(monkeypatch)
    monkeypatch.setenv("COHERE_API_KEY", "test-cohere-key")

    api = CohereAPI("cohere/command-a-reasoning-08-2025")
    try:
        assert api.service_model_name() == "command-a-reasoning-08-2025"
        assert api.canonical_name() == "cohere/command-a-reasoning-08-2025"
        assert api.base_url == DEFAULT_COHERE_BASE_URL
        assert api.api_key == "test-cohere-key"
    finally:
        asyncio.run(api.aclose())


def test_cohere_route_resolves_to_obviousbenchs_native_v2_adapter(monkeypatch):
    _clear_cohere_env(monkeypatch)
    monkeypatch.setenv("COHERE_API_KEY", "test-cohere-key")

    model = get_model("cohere/command-r7b-12-2024", memoize=False)
    try:
        assert type(model.api).__module__ == "obviousbench.providers.cohere"
        assert type(model.api).__name__ == "CohereAPI"
    finally:
        asyncio.run(model.api.aclose())


def test_cohere_key_and_base_url_resolution_are_explicit(monkeypatch):
    _clear_cohere_env(monkeypatch)
    monkeypatch.setenv("COHERE_API_KEY", "test-cohere-key")
    monkeypatch.setenv("COHERE_BASE_URL", "https://unit.example/v2/")

    assert resolve_cohere_api_key() == ("test-cohere-key", "COHERE_API_KEY")
    assert resolve_cohere_base_url() == "https://unit.example/v2"


def test_cohere_production_key_is_preferred_when_both_are_present(monkeypatch):
    _clear_cohere_env(monkeypatch)
    monkeypatch.setenv("COHERE_API_KEY", "fallback-key")
    monkeypatch.setenv("COHEREPROD_API_KEY", "production-key")

    assert resolve_cohere_api_key() == ("production-key", "COHEREPROD_API_KEY")


def test_cohere_key_is_required(monkeypatch):
    _clear_cohere_env(monkeypatch)

    with pytest.raises(PrerequisiteError) as exc_info:
        resolve_cohere_api_key()

    assert "COHERE_API_KEY" in str(exc_info.value)


def test_cohere_native_disabled_thinking_shape_is_explicit():
    assert cohere_thinking_disabled() == {"type": "disabled"}
    assert normalize_cohere_thinking({"type": "disabled"}) == {
        "type": "disabled"
    }


@pytest.mark.parametrize("token_budget", COHERE_BENCHMARK_THINKING_TOKEN_BUDGETS)
def test_cohere_native_enabled_thinking_budgets_are_schema_complete(token_budget):
    thinking = cohere_thinking_enabled(token_budget)
    request = cohere_chat_request(
        model_name="cohere/command-a-reasoning-08-2025",
        input=[ChatMessageUser(content="What is 2 + 2?")],
        tools=[],
        tool_choice="none",
        config=GenerateConfig(extra_body={"thinking": thinking}),
    )

    assert thinking == {"type": "enabled", "token_budget": token_budget}
    assert request["thinking"] == thinking
    assert request["stream"] is False


def test_cohere_request_maps_native_generation_fields_and_auth_headers():
    request = cohere_chat_request(
        model_name="command-a-reasoning-08-2025",
        input=[
            ChatMessageSystem(content="Reply with one word."),
            ChatMessageUser(content="What is 2 + 2?"),
        ],
        tools=[],
        tool_choice="none",
        config=GenerateConfig(
            max_tokens=64,
            temperature=0,
            top_p=0.8,
            top_k=50,
            stop_seqs=["END"],
            extra_body={"thinking": {"type": "disabled"}},
        ),
    )

    assert request == {
        "model": "command-a-reasoning-08-2025",
        "messages": [
            {"role": "system", "content": "Reply with one word."},
            {"role": "user", "content": "What is 2 + 2?"},
        ],
        "stream": False,
        "max_tokens": 64,
        "stop_sequences": ["END"],
        "temperature": 0,
        "k": 50,
        "p": 0.8,
        "thinking": {"type": "disabled"},
    }
    assert cohere_chat_headers("test-cohere-key", {"X-Request-ID": "unit"}) == {
        "X-Request-ID": "unit",
        "Accept": "application/json",
        "Authorization": "Bearer test-cohere-key",
        "Content-Type": "application/json",
    }


@pytest.mark.parametrize(
    "thinking",
    [
        {},
        {"type": "medium"},
        {"type": "disabled", "token_budget": 512},
        {"type": "enabled", "token_budget": 0},
        {"type": "enabled", "token_budget": True},
        {"type": "enabled", "token_budget": 512, "named_level": "high"},
    ],
)
def test_cohere_rejects_invalid_native_thinking_shapes(thinking):
    with pytest.raises(ValueError):
        normalize_cohere_thinking(thinking)


def test_cohere_rejects_generic_named_reasoning_controls():
    with pytest.raises(ValueError, match="does not accept Inspect reasoning_effort"):
        cohere_chat_request(
            model_name="command-a-reasoning-08-2025",
            input=[ChatMessageUser(content="hi")],
            tools=[],
            tool_choice="none",
            config=GenerateConfig(reasoning_effort="high"),
        )


def test_cohere_parses_native_response_content_and_usage():
    output = cohere_model_output(
        _response_body(),
        model_name="command-a-reasoning-08-2025",
        tools=[],
    )

    assert output.completion == "Four."
    assert output.stop_reason == "stop"
    assert isinstance(output.message.content, list)
    assert isinstance(output.message.content[0], ContentReasoning)
    assert output.message.content[0].reasoning == "Check the arithmetic."
    assert isinstance(output.message.content[1], ContentText)
    assert output.message.content[1].text == "Four."
    assert output.usage is not None
    assert output.usage.model_dump() == {
        "input_tokens": 17,
        "output_tokens": 12,
        "total_tokens": 29,
        "input_tokens_cache_write": None,
        "input_tokens_cache_read": None,
        "reasoning_tokens": None,
        "total_cost": None,
    }
    assert output.metadata == {
        "cohere_response_id": "cohere-response-unit",
        "cohere_billed_units": {"input_tokens": 9, "output_tokens": 12},
    }


def test_cohere_generate_posts_only_to_native_v2_chat(monkeypatch):
    _clear_cohere_env(monkeypatch)
    captured: dict[str, object] = {}

    async def run() -> None:
        async def handler(request: httpx.Request) -> httpx.Response:
            captured["method"] = request.method
            captured["url"] = str(request.url)
            captured["headers"] = dict(request.headers)
            captured["body"] = json.loads(request.content)
            return httpx.Response(200, json=_response_body())

        client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
        api = CohereAPI(
            "command-a-reasoning-08-2025",
            api_key="test-cohere-key",
            http_client=client,
        )
        try:
            output, call = await api.generate(
                [ChatMessageUser(content="What is 2 + 2?")],
                [],
                "none",
                GenerateConfig(
                    extra_body={"thinking": cohere_thinking_enabled(2048)}
                ),
            )
            assert not isinstance(output, Exception)
            assert output.completion == "Four."
            assert call.error is None
            assert call.response == _response_body()
        finally:
            await api.aclose()
            await client.aclose()

    asyncio.run(run())

    assert captured["method"] == "POST"
    assert captured["url"] == "https://api.cohere.ai/v2/chat"
    assert captured["headers"]["authorization"] == "Bearer test-cohere-key"
    assert captured["headers"]["content-type"] == "application/json"
    assert captured["body"] == {
        "model": "command-a-reasoning-08-2025",
        "messages": [{"role": "user", "content": "What is 2 + 2?"}],
        "stream": False,
        "thinking": {"type": "enabled", "token_budget": 2048},
    }


def test_cohere_generate_returns_native_http_auth_errors_without_network():
    async def run() -> None:
        async def handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(401, json={"message": "invalid token"})

        client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
        api = CohereAPI(
            "command-a-reasoning-08-2025",
            api_key="test-cohere-key",
            http_client=client,
        )
        try:
            output, call = await api.generate(
                [ChatMessageUser(content="hi")], [], "none", GenerateConfig()
            )
            assert isinstance(output, httpx.HTTPStatusError)
            assert api.is_auth_failure(output)
            assert call.error is True
            assert call.response == {"message": "invalid token"}
        finally:
            await api.aclose()
            await client.aclose()

    asyncio.run(run())
