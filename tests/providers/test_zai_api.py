from __future__ import annotations

import asyncio
import os
import subprocess
import sys

import pytest
from inspect_ai._util.error import PrerequisiteError
from inspect_ai.model import GenerateConfig, get_model

from obviousbench.providers.zai import (
    DEFAULT_ZAI_BASE_URL,
    ZAI_REASONING_EFFORTS,
    ZAIAPI,
    resolve_zai_api_key,
    resolve_zai_base_url,
)


def _clear_zai_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("ZAI_API_KEY", raising=False)
    monkeypatch.delenv("ZAI_BASE_URL", raising=False)


def test_zai_adapter_uses_documented_openai_compatible_endpoint(monkeypatch):
    _clear_zai_env(monkeypatch)
    monkeypatch.setenv("ZAI_API_KEY", "test-zai-key")

    api = ZAIAPI("glm-5.2")
    try:
        assert api.service_model_name() == "glm-5.2"
        assert api.base_url == DEFAULT_ZAI_BASE_URL
        assert api.api_key == "test-zai-key"
    finally:
        asyncio.run(api.aclose())


def test_zai_registered_route_resolves_through_inspect(monkeypatch):
    _clear_zai_env(monkeypatch)
    monkeypatch.setenv("ZAI_API_KEY", "test-zai-key")
    import obviousbench._registry as registry

    assert registry.zai is not None
    model = get_model("zai/glm-5.2", memoize=False)
    try:
        assert type(model.api).__name__ == "ZAIAPI"
        assert model.api.service_model_name() == "glm-5.2"
    finally:
        asyncio.run(model.api.aclose())


def test_inspect_entry_point_registers_zai_route_in_fresh_interpreter():
    command = [
        sys.executable,
        "-c",
        "import obviousbench._registry; from inspect_ai.model import get_model; "
        "model = get_model('zai/glm-5.2'); "
        "assert model.api.service_model_name() == 'glm-5.2'",
    ]
    result = subprocess.run(
        command,
        env={**os.environ, "ZAI_API_KEY": "test-zai-key"},
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr


@pytest.mark.parametrize("effort", ["high", "xhigh"])
def test_zai_adapter_allows_requested_distinct_thinking_efforts(monkeypatch, effort):
    _clear_zai_env(monkeypatch)
    monkeypatch.setenv("ZAI_API_KEY", "test-zai-key")
    api = ZAIAPI("glm-5.2")
    try:
        assert api.completion_params(
            GenerateConfig(
                max_tokens=64,
                reasoning_effort=effort,
                extra_body={"thinking": {"type": "enabled"}},
            ),
            tools=False,
        ) == {
            "model": "glm-5.2",
            "max_tokens": 64,
            "reasoning_effort": effort,
            "extra_body": {"thinking": {"type": "enabled"}},
        }
    finally:
        asyncio.run(api.aclose())


def test_zai_adapter_allows_explicitly_disabled_thinking(monkeypatch):
    _clear_zai_env(monkeypatch)
    monkeypatch.setenv("ZAI_API_KEY", "test-zai-key")
    api = ZAIAPI("glm-5.2")
    try:
        assert api.completion_params(
            GenerateConfig(
                max_tokens=64,
                extra_body={"thinking": {"type": "disabled"}},
            ),
            tools=False,
        ) == {
            "model": "glm-5.2",
            "max_tokens": 64,
            "extra_body": {"thinking": {"type": "disabled"}},
        }
    finally:
        asyncio.run(api.aclose())


@pytest.mark.parametrize("effort", sorted(ZAI_REASONING_EFFORTS))
def test_zai_adapter_accepts_every_documented_effort_when_thinking_is_enabled(
    monkeypatch, effort
):
    _clear_zai_env(monkeypatch)
    monkeypatch.setenv("ZAI_API_KEY", "test-zai-key")
    api = ZAIAPI("glm-5.2")
    try:
        params = api.completion_params(
            GenerateConfig(
                reasoning_effort=effort,
                extra_body={"thinking": {"type": "enabled"}},
            ),
            tools=False,
        )
        assert params["reasoning_effort"] == effort
    finally:
        asyncio.run(api.aclose())


def test_zai_adapter_rejects_ambiguous_or_undocumented_thinking(monkeypatch):
    _clear_zai_env(monkeypatch)
    monkeypatch.setenv("ZAI_API_KEY", "test-zai-key")
    api = ZAIAPI("glm-5.2")
    try:
        with pytest.raises(ValueError, match="requires explicit"):
            api.completion_params(GenerateConfig(reasoning_effort="high"), tools=False)
        with pytest.raises(ValueError, match="cannot be combined"):
            api.completion_params(
                GenerateConfig(
                    reasoning_effort="high",
                    extra_body={"thinking": {"type": "disabled"}},
                ),
                tools=False,
            )
        with pytest.raises(ValueError, match="disabled, enabled"):
            api.completion_params(
                GenerateConfig(extra_body={"thinking": {"type": "maybe"}}),
                tools=False,
            )
    finally:
        asyncio.run(api.aclose())


def test_zai_adapter_accepts_base_url_override_and_requires_key(monkeypatch):
    _clear_zai_env(monkeypatch)
    monkeypatch.setenv("ZAI_BASE_URL", "https://unit.example/v4/")

    assert resolve_zai_base_url() == "https://unit.example/v4"
    with pytest.raises(PrerequisiteError) as exc_info:
        resolve_zai_api_key()
    assert "ZAI_API_KEY" in str(exc_info.value)
