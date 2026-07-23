from __future__ import annotations

import asyncio

import pytest
from inspect_ai.model import get_model


@pytest.mark.parametrize(
    "model_name",
    [
        "bedrock-standard/us.amazon.nova-micro-v1:0",
        "bedrock-standard/us.amazon.nova-lite-v1:0",
    ],
)
def test_bedrock_standard_nova_routes_use_bearer_capable_adapter(model_name):
    """Resolve Standard-only Nova without requiring ambient AWS credentials."""
    model = get_model(model_name)
    try:
        assert type(model.api).__module__ == "obviousbench.providers.bedrock_flex"
        assert type(model.api).__name__ == "BedrockStandardAPI"
        assert model.api.service_model_name() == model_name.removeprefix(
            "bedrock-standard/"
        )
    finally:
        asyncio.run(model.api.aclose())


@pytest.mark.parametrize(
    "model_name",
    [
        "perplexity/sonar",
        "perplexity/sonar-pro",
        "perplexity/sonar-reasoning-pro",
    ],
)
def test_perplexity_sonar_routes_use_inspects_native_provider(monkeypatch, model_name):
    """Construct the native route only; the supplied key is deliberately fake."""
    monkeypatch.setenv("PERPLEXITY_API_KEY", "unit-test-key")
    model = get_model(model_name)
    try:
        assert type(model.api).__module__ == "inspect_ai.model._providers.perplexity"
        assert model.api.service_model_name() == model_name.removeprefix("perplexity/")
    finally:
        asyncio.run(model.api.aclose())
