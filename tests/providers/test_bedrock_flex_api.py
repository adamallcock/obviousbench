from __future__ import annotations

import asyncio
import json

import httpx
import pytest
from botocore.credentials import ReadOnlyCredentials
from inspect_ai.model import GenerateConfig
from inspect_ai.model._chat_message import ChatMessageUser
from inspect_ai.model._providers.bedrock import (
    ConverseClientConverseRequest,
    ConverseInferenceConfig,
)

from obviousbench.providers.bedrock_flex import (
    BEDROCK_FLEX_SERVICE_TIER,
    BedrockFlexAPI,
    BedrockStandardAPI,
    bearer_flex_converse_request,
    flex_converse_payload,
    flex_service_tier_from_response,
    resolve_bedrock_bearer_token,
    resolve_bedrock_region,
    signed_flex_converse_request,
    standard_converse_payload,
    standard_service_tier_from_response,
    validate_flex_model,
    validate_standard_model,
)


def _credentials() -> ReadOnlyCredentials:
    return ReadOnlyCredentials(
        access_key="AKIDEXAMPLE",
        secret_key="unit-test-secret",
        token="unit-test-session-token",
    )


def _response(*, service_tier: str | None = "flex") -> dict[str, object]:
    response: dict[str, object] = {
        "output": {
            "message": {
                "role": "assistant",
                "content": [{"text": "OK"}],
            }
        },
        "stopReason": "end_turn",
        "usage": {"inputTokens": 3, "outputTokens": 1, "totalTokens": 4},
        "metrics": {"latencyMs": 1},
    }
    if service_tier is not None:
        response["serviceTier"] = {"type": service_tier}
    return response


def test_flex_payload_moves_model_id_to_uri_and_keeps_service_tier_top_level():
    model_id, payload = flex_converse_payload(
        ConverseClientConverseRequest(
            modelId="us.amazon.nova-2-lite-v1:0",
            messages=[],
            inferenceConfig=ConverseInferenceConfig(maxTokens=64),
        )
    )

    assert model_id == "us.amazon.nova-2-lite-v1:0"
    assert "modelId" not in payload
    assert payload["serviceTier"] == BEDROCK_FLEX_SERVICE_TIER
    assert "serviceTier" not in payload.get("additionalModelRequestFields", {})


def test_standard_payload_omits_service_tier_to_request_bedrock_default():
    model_id, payload = standard_converse_payload(
        ConverseClientConverseRequest(
            modelId="us.amazon.nova-micro-v1:0",
            messages=[],
            inferenceConfig=ConverseInferenceConfig(maxTokens=64),
        )
    )

    assert model_id == "us.amazon.nova-micro-v1:0"
    assert "serviceTier" not in payload


def test_signed_flex_converse_request_preserves_profile_id_and_uses_bedrock_sigv4():
    url, headers, body = signed_flex_converse_request(
        endpoint="https://bedrock-runtime.us-east-1.amazonaws.com",
        region_name="us-east-1",
        model_id="us.amazon.nova-2-lite-v1:0",
        payload={"serviceTier": {"type": "flex"}, "messages": []},
        credentials=_credentials(),
    )

    assert url.endswith("/model/us.amazon.nova-2-lite-v1%3A0/converse")
    assert headers["Authorization"].startswith(
        "AWS4-HMAC-SHA256 Credential=AKIDEXAMPLE/"
    )
    assert headers["X-Amz-Security-Token"] == "unit-test-session-token"
    assert json.loads(body) == {
        "serviceTier": {"type": "flex"},
        "messages": [],
    }


def test_bearer_flex_converse_request_uses_bedrock_api_key_without_sigv4():
    url, headers, body = bearer_flex_converse_request(
        endpoint="https://bedrock-runtime.us-east-1.amazonaws.com",
        model_id="us.amazon.nova-pro-v1:0",
        payload={"serviceTier": {"type": "flex"}, "messages": []},
        bearer_token="unit-bedrock-api-key",
    )

    assert url.endswith("/model/us.amazon.nova-pro-v1%3A0/converse")
    assert headers == {
        "Accept": "application/json",
        "Authorization": "Bearer unit-bedrock-api-key",
        "Content-Type": "application/json",
    }
    assert json.loads(body)["serviceTier"] == {"type": "flex"}


def test_bedrock_bearer_resolution_prefers_official_variable(monkeypatch):
    monkeypatch.setenv("BEDROCK_API_KEY", "local-alias")
    monkeypatch.setenv("AWS_BEARER_TOKEN_BEDROCK", "official")

    assert resolve_bedrock_bearer_token() == "official"
    assert resolve_bedrock_bearer_token("explicit") == "explicit"


def test_bedrock_region_resolution_honors_both_documented_environment_spellings(
    monkeypatch,
):
    monkeypatch.delenv("AWS_DEFAULT_REGION", raising=False)
    monkeypatch.setenv("AWS_REGION", "us-west-2")
    assert resolve_bedrock_region() == "us-west-2"

    monkeypatch.setenv("AWS_DEFAULT_REGION", "us-east-1")
    assert resolve_bedrock_region() == "us-east-1"


@pytest.mark.parametrize(
    ("model_id", "config", "message"),
    [
        (
            "us.amazon.nova-micro-v1:0",
            GenerateConfig(),
            "Standard-only",
        ),
        (
            "us.amazon.nova-lite-v1:0",
            GenerateConfig(),
            "Standard-only",
        ),
        (
            "us.amazon.nova-pro-v1:0",
            GenerateConfig(reasoning_effort="low"),
            "no documented selectable",
        ),
        (
            "us.amazon.nova-premier-v1:0",
            GenerateConfig(reasoning_effort="low"),
            "no documented selectable",
        ),
        (
            "us.amazon.nova-2-lite-v1:0",
            GenerateConfig(reasoning_effort="none"),
            "only Nova 2 Lite reasoning_effort values",
        ),
        (
            "us.amazon.nova-2-lite-v1:0",
            GenerateConfig(reasoning_effort="high", temperature=0),
            "requires these controls to be unset",
        ),
    ],
)
def test_flex_model_capability_guards(model_id, config, message):
    with pytest.raises(ValueError, match=message):
        validate_flex_model(model_id, config)


@pytest.mark.parametrize(
    ("model_id", "config", "message"),
    [
        (
            "us.amazon.nova-pro-v1:0",
            GenerateConfig(),
            "Standard-only Nova Micro and Nova Lite",
        ),
        (
            "us.amazon.nova-micro-v1:0",
            GenerateConfig(reasoning_effort="low"),
            "no documented selectable",
        ),
    ],
)
def test_standard_model_capability_guards(model_id, config, message):
    with pytest.raises(ValueError, match=message):
        validate_standard_model(model_id, config)


@pytest.mark.parametrize("effort", (None, "low", "medium", "high"))
def test_nova_2_lite_accepts_only_its_documented_efforts(effort):
    validate_flex_model(
        "us.amazon.nova-2-lite-v1:0", GenerateConfig(reasoning_effort=effort)
    )


@pytest.mark.parametrize("effort", (None, "low", "medium", "high"))
def test_nova_2_lite_does_not_receive_or_send_an_output_cap(effort):
    api = BedrockFlexAPI(
        "us.amazon.nova-2-lite-v1:0",
        region_name="us-east-1",
        api_key="unit-bedrock-api-key",
    )
    try:
        config = GenerateConfig(reasoning_effort=effort, max_tokens=10_000)
        assert api.max_tokens_for_config(config) is None
        assert api.max_tokens() is None
        request = asyncio.run(api._converse_request([], [], "none", config))
        assert request.inferenceConfig.maxTokens is None
    finally:
        asyncio.run(api.aclose())


def test_flex_response_requires_explicit_served_tier_attestation():
    assert flex_service_tier_from_response(_response()) == "flex"
    with pytest.raises(ValueError, match="omitted serviceTier.type"):
        flex_service_tier_from_response({})


def test_standard_response_preserves_an_absent_tier_as_unreported_default():
    assert standard_service_tier_from_response(_response(service_tier=None)) == (
        "unreported_default"
    )
    assert standard_service_tier_from_response(_response(service_tier="default")) == (
        "default"
    )
    with pytest.raises(ValueError, match="non-Standard tier"):
        standard_service_tier_from_response(_response(service_tier="flex"))


def test_bedrock_flex_adapter_posts_signed_top_level_tier_and_records_metadata():
    captured: dict[str, object] = {}

    async def run() -> None:
        async def handler(request: httpx.Request) -> httpx.Response:
            captured["method"] = request.method
            captured["url"] = str(request.url)
            captured["headers"] = dict(request.headers)
            captured["body"] = json.loads(request.content)
            return httpx.Response(200, json=_response())

        client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
        api = BedrockFlexAPI(
            "us.amazon.nova-2-lite-v1:0",
            base_url="https://bedrock.unit.example",
            region_name="us-east-1",
            credentials_resolver=_credentials,
            http_client=client,
        )
        try:
            output, call = await api.generate(
                [ChatMessageUser(content="Reply with exactly OK.")],
                [],
                "none",
                GenerateConfig(reasoning_effort="low"),
            )
            assert not isinstance(output, Exception)
            assert output.completion == "OK"
            assert call.error is None
            assert output.metadata == {
                "bedrock_flex": {
                    "auth_mode": "aws_sigv4",
                    "model_id": "us.amazon.nova-2-lite-v1:0",
                    "region": "us-east-1",
                    "requested_service_tier": "flex",
                    "served_service_tier": "flex",
                }
            }
        finally:
            await api.aclose()
            await client.aclose()

    asyncio.run(run())

    assert captured["method"] == "POST"
    assert captured["url"] == (
        "https://bedrock.unit.example/model/us.amazon.nova-2-lite-v1%3A0/converse"
    )
    assert captured["headers"]["authorization"].startswith(
        "AWS4-HMAC-SHA256 Credential=AKIDEXAMPLE/"
    )
    assert captured["body"] == {
        "messages": [
            {"role": "user", "content": [{"text": "Reply with exactly OK."}]}
        ],
        "additionalModelRequestFields": {
            "reasoningConfig": {
                "type": "enabled",
                "maxReasoningEffort": "low",
            }
        },
        "serviceTier": {"type": "flex"},
    }


def test_bedrock_flex_adapter_uses_api_key_bearer_auth_when_available():
    captured: dict[str, object] = {}

    async def run() -> None:
        async def handler(request: httpx.Request) -> httpx.Response:
            captured["headers"] = dict(request.headers)
            return httpx.Response(200, json=_response())

        client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
        api = BedrockFlexAPI(
            "us.amazon.nova-pro-v1:0",
            base_url="https://bedrock.unit.example",
            region_name="us-east-1",
            api_key="unit-bedrock-api-key",
            http_client=client,
        )
        try:
            output, call = await api.generate(
                [ChatMessageUser(content="Reply with exactly OK.")],
                [],
                "none",
                GenerateConfig(),
            )
            assert not isinstance(output, Exception)
            assert call.error is None
            assert output.metadata["bedrock_flex"]["auth_mode"] == "bedrock_api_key"
        finally:
            await api.aclose()
            await client.aclose()

    asyncio.run(run())
    assert captured["headers"]["authorization"] == "Bearer unit-bedrock-api-key"


def test_bedrock_standard_adapter_uses_bearer_auth_and_omits_service_tier():
    captured: dict[str, object] = {}

    async def run() -> None:
        async def handler(request: httpx.Request) -> httpx.Response:
            captured["headers"] = dict(request.headers)
            captured["body"] = json.loads(request.content)
            return httpx.Response(200, json=_response(service_tier=None))

        client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
        api = BedrockStandardAPI(
            "us.amazon.nova-micro-v1:0",
            base_url="https://bedrock.unit.example",
            region_name="us-east-1",
            api_key="unit-bedrock-api-key",
            http_client=client,
        )
        try:
            output, call = await api.generate(
                [ChatMessageUser(content="Reply with exactly OK.")],
                [],
                "none",
                GenerateConfig(),
            )
            assert not isinstance(output, Exception)
            assert call.error is None
            assert output.metadata == {
                "bedrock_standard": {
                    "auth_mode": "bedrock_api_key",
                    "model_id": "us.amazon.nova-micro-v1:0",
                    "region": "us-east-1",
                    "requested_service_tier": "standard",
                    "wire_service_tier": "omitted",
                    "served_service_tier": "unreported_default",
                }
            }
        finally:
            await api.aclose()
            await client.aclose()

    asyncio.run(run())
    assert captured["headers"]["authorization"] == "Bearer unit-bedrock-api-key"
    assert "serviceTier" not in captured["body"]


def test_bedrock_flex_fails_if_bedrock_reports_standard_tier():
    async def run() -> None:
        async def handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(200, json=_response(service_tier="default"))

        client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
        api = BedrockFlexAPI(
            "us.amazon.nova-pro-v1:0",
            base_url="https://bedrock.unit.example",
            region_name="us-east-1",
            credentials_resolver=_credentials,
            http_client=client,
        )
        try:
            output, call = await api.generate(
                [ChatMessageUser(content="Reply with exactly OK.")],
                [],
                "none",
                GenerateConfig(),
            )
            assert isinstance(output, ValueError)
            assert "non-Flex tier" in str(output)
            assert call.error is True
        finally:
            await api.aclose()
            await client.aclose()

    asyncio.run(run())
