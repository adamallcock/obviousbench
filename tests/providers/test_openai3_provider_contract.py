from __future__ import annotations

import asyncio
import json
import tomllib
from importlib.metadata import version
from pathlib import Path

import httpx2
import pytest
from inspect_ai.model import GenerateConfig, ModelOutput
from inspect_ai.model._chat_message import ChatMessageUser
from inspect_ai.model._providers.openai import OpenAIAPI
from inspect_ai.model._providers.openai_compatible import OpenAICompatibleAPI
from openai import AsyncOpenAI
from packaging.version import Version
from xai_sdk.chat import chat_pb2


def test_provider_stack_versions_match_the_qualified_bounds():
    assert Version("0.3.259") <= Version(version("inspect-ai")) < Version("0.3.260")
    assert Version("3.1") <= Version(version("openai")) < Version("4")
    assert Version("0.28") <= Version(version("httpx")) < Version("1")
    assert Version("2.7") <= Version(version("httpx2")) < Version("3")


def test_pyproject_declares_the_qualified_provider_bounds_exactly():
    project = tomllib.loads(
        (Path(__file__).resolve().parents[2] / "pyproject.toml").read_text(
            encoding="utf-8"
        )
    )
    declared_dependencies = set(project["project"]["dependencies"])

    assert {
        "inspect-ai>=0.3.259,<0.3.260",
        "openai>=3.1,<4",
        "httpx>=0.28,<1",
        "xai_sdk>=1.18,<2",
    } <= declared_dependencies


@pytest.mark.parametrize(
    ("api_class", "model_name", "service"),
    [
        (OpenAIAPI, "gpt-5.6-sol", None),
        (OpenAICompatibleAPI, "test-service/test-model", "test-service"),
    ],
)
def test_inspect_openai_providers_default_to_httpx2_without_network(
    api_class: type[OpenAIAPI | OpenAICompatibleAPI],
    model_name: str,
    service: str | None,
):
    kwargs: dict[str, object] = {
        "api_key": "test-key",
        "base_url": "https://example.invalid/v1",
    }
    if service is not None:
        kwargs["service"] = service

    api = api_class(model_name, **kwargs)
    try:
        assert isinstance(api.client, AsyncOpenAI)
        assert isinstance(api.http_client, httpx2.AsyncClient)
    finally:
        asyncio.run(api.aclose())


def test_openai_compatible_generate_posts_chat_completion_over_mocked_httpx2():
    captured: dict[str, object] = {}

    async def run() -> None:
        async def handler(request: httpx2.Request) -> httpx2.Response:
            captured["method"] = request.method
            captured["url"] = str(request.url)
            captured["body"] = json.loads(request.content)
            return httpx2.Response(
                200,
                json={
                    "id": "chatcmpl-unit",
                    "object": "chat.completion",
                    "created": 1_710_000_000,
                    "model": "test-model",
                    "choices": [
                        {
                            "index": 0,
                            "message": {"role": "assistant", "content": "Four."},
                            "logprobs": None,
                            "finish_reason": "stop",
                        }
                    ],
                    "usage": {
                        "prompt_tokens": 3,
                        "completion_tokens": 1,
                        "total_tokens": 4,
                    },
                },
                request=request,
            )

        client = httpx2.AsyncClient(transport=httpx2.MockTransport(handler))
        api = OpenAICompatibleAPI(
            "test-service/test-model",
            base_url="https://example.invalid/v1",
            api_key="test-key",
            service="test-service",
            http_client=client,
        )
        try:
            output, call = await api.generate(
                [ChatMessageUser(content="What is 2 + 2?")],
                [],
                "none",
                GenerateConfig(max_tokens=16, temperature=0),
            )
            assert isinstance(output, ModelOutput)
            assert output.completion == "Four."
            assert output.stop_reason == "stop"
            assert call.error is None
        finally:
            await api.aclose()
            await client.aclose()

    asyncio.run(run())

    assert captured == {
        "method": "POST",
        "url": "https://example.invalid/v1/chat/completions",
        "body": {
            "messages": [{"role": "user", "content": "What is 2 + 2?"}],
            "model": "test-model",
            "max_tokens": 16,
            "temperature": 0.0,
        },
    }


def test_xai_sdk_118_exposes_grok_xhigh_reasoning_effort_without_network():
    assert Version("1.18") <= Version(version("xai-sdk")) < Version("2")
    assert hasattr(chat_pb2.ReasoningEffort, "EFFORT_XHIGH")
