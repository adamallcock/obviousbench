from __future__ import annotations

import asyncio
import os
import subprocess
import sys
from pathlib import Path

import pytest
from inspect_ai._util.error import PrerequisiteError
from inspect_ai.model import GenerateConfig, get_model

from obviousbench.providers.aion import (
    AION_2_0_REASONING_EFFORTS,
    AION_API_KEY_VARS,
    AION_BASE_URL_VARS,
    DEFAULT_AION_BASE_URL,
    AionAPI,
    resolve_aion_api_key,
    resolve_aion_base_url,
)


def _clear_aion_env(monkeypatch: pytest.MonkeyPatch) -> None:
    for env_var in (*AION_API_KEY_VARS, *AION_BASE_URL_VARS):
        monkeypatch.delenv(env_var, raising=False)


def test_aion_adapter_uses_documented_openai_compatible_endpoint(monkeypatch):
    _clear_aion_env(monkeypatch)
    monkeypatch.setenv("AIONLABS_API_KEY", "test-aion-key")

    api = AionAPI("aion-labs/aion-2.0")
    try:
        assert api.service_model_name() == "aion-labs/aion-2.0"
        assert api.base_url == DEFAULT_AION_BASE_URL
        assert api.api_key == "test-aion-key"
        assert api.responses_api is False
    finally:
        asyncio.run(api.aclose())


def test_aion_registered_route_preserves_model_namespace(monkeypatch):
    _clear_aion_env(monkeypatch)
    monkeypatch.setenv("AIONLABS_API_KEY", "test-aion-key")
    import obviousbench._registry as registry

    assert registry.aion is not None
    model = get_model("aion/aion-labs/aion-2.0")
    try:
        assert model.api.service_model_name() == "aion-labs/aion-2.0"
    finally:
        asyncio.run(model.api.aclose())


def test_inspect_entry_point_registers_aion_route_in_fresh_interpreter():
    script = """
import asyncio
from inspect_ai.model import get_model

model = get_model('aion/aion-labs/aion-2.0')
assert model.api.service_model_name() == 'aion-labs/aion-2.0'
asyncio.run(model.api.aclose())
"""
    repo_root = Path(__file__).resolve().parents[2]
    result = subprocess.run(
        [sys.executable, "-c", script],
        cwd=repo_root,
        env={**os.environ, "AIONLABS_API_KEY": "test-aion-key"},
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr


@pytest.mark.parametrize("effort", sorted(AION_2_0_REASONING_EFFORTS))
def test_aion_2_0_adapter_allows_documented_reasoning_efforts(monkeypatch, effort):
    _clear_aion_env(monkeypatch)
    monkeypatch.setenv("AIONLABS_API_KEY", "test-aion-key")
    api = AionAPI("aion-labs/aion-2.0")
    try:
        assert api.completion_params(
            GenerateConfig(max_tokens=64, reasoning_effort=effort), tools=False
        ) == {
            "model": "aion-labs/aion-2.0",
            "max_tokens": 64,
            "reasoning_effort": effort,
        }
    finally:
        asyncio.run(api.aclose())


def test_aion_other_models_remain_provider_default_only(monkeypatch):
    _clear_aion_env(monkeypatch)
    monkeypatch.setenv("AIONLABS_API_KEY", "test-aion-key")
    api = AionAPI("aion-labs/aion-3.0")
    try:
        assert api.completion_params(GenerateConfig(max_tokens=64), tools=False) == {
            "model": "aion-labs/aion-3.0",
            "max_tokens": 64,
        }
        with pytest.raises(ValueError, match="no documented selectable"):
            api.completion_params(
                GenerateConfig(max_tokens=64, reasoning_effort="high"),
                tools=False,
            )
    finally:
        asyncio.run(api.aclose())


def test_aion_adapter_accepts_key_and_base_url_aliases(monkeypatch):
    _clear_aion_env(monkeypatch)
    monkeypatch.setenv("AION_API_KEY", "test-aion-key")
    monkeypatch.setenv("AION_BASE_URL", "https://unit.example/v1/")

    assert resolve_aion_api_key() == ("test-aion-key", "AION_API_KEY")
    assert resolve_aion_base_url() == "https://unit.example/v1"


def test_aion_adapter_reports_required_api_key(monkeypatch):
    _clear_aion_env(monkeypatch)

    with pytest.raises(PrerequisiteError) as exc_info:
        resolve_aion_api_key()

    message = str(exc_info.value)
    assert "AIONLABS_API_KEY" in message
    assert "AION_API_KEY" in message
