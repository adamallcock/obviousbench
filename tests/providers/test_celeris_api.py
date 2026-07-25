from __future__ import annotations

import asyncio
import os
import subprocess
import sys
from pathlib import Path

import pytest
from inspect_ai._util.error import PrerequisiteError
from inspect_ai.model import GenerateConfig, get_model

from obviousbench.providers.celeris import (
    CELERIS_API_KEY_VARS,
    CELERIS_BASE_URL_VARS,
    CELERIS_MAX_CONTEXT_TOKENS,
    DEFAULT_CELERIS_BASE_URL,
    CelerisAPI,
    resolve_celeris_api_key,
    resolve_celeris_base_url,
)


def _clear_celeris_env(monkeypatch: pytest.MonkeyPatch) -> None:
    for env_var in (*CELERIS_API_KEY_VARS, *CELERIS_BASE_URL_VARS):
        monkeypatch.delenv(env_var, raising=False)


def test_celeris_adapter_uses_documented_openai_compatible_endpoint(monkeypatch):
    _clear_celeris_env(monkeypatch)
    monkeypatch.setenv("CELERIS_API_KEY", "test-celeris-key")

    api = CelerisAPI("celeris-1")
    try:
        assert api.service_model_name() == "celeris-1"
        assert api.base_url == DEFAULT_CELERIS_BASE_URL
        assert api.api_key == "test-celeris-key"
        assert api.responses_api is False
    finally:
        asyncio.run(api.aclose())


def test_celeris_registered_route_resolves_model(monkeypatch):
    _clear_celeris_env(monkeypatch)
    monkeypatch.setenv("CELERIS_API_KEY", "test-celeris-key")
    import obviousbench._registry as registry

    assert registry.celeris is not None
    model = get_model("celeris/celeris-1")
    try:
        assert model.api.service_model_name() == "celeris-1"
    finally:
        asyncio.run(model.api.aclose())


def test_inspect_entry_point_registers_celeris_route_in_fresh_interpreter():
    script = """
import asyncio
from inspect_ai.model import get_model

model = get_model('celeris/celeris-1')
assert model.api.service_model_name() == 'celeris-1'
asyncio.run(model.api.aclose())
"""
    repo_root = Path(__file__).resolve().parents[2]
    result = subprocess.run(
        [sys.executable, "-c", script],
        cwd=repo_root,
        env={**os.environ, "CELERIS_API_KEY": "test-celeris-key"},
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr


def test_celeris_adapter_accepts_documented_output_cap(monkeypatch):
    _clear_celeris_env(monkeypatch)
    monkeypatch.setenv("CELERIS_API_KEY", "test-celeris-key")
    api = CelerisAPI("celeris-1")
    try:
        assert api.completion_params(GenerateConfig(max_tokens=2048), tools=False) == {
            "model": "celeris-1",
            "max_tokens": 2048,
        }
    finally:
        asyncio.run(api.aclose())


@pytest.mark.parametrize("max_tokens", [0, 1, 255, 257, 1025, True])
def test_celeris_adapter_rejects_invalid_output_caps(monkeypatch, max_tokens):
    _clear_celeris_env(monkeypatch)
    monkeypatch.setenv("CELERIS_API_KEY", "test-celeris-key")
    api = CelerisAPI("celeris-1")
    try:
        with pytest.raises(ValueError, match="positive integer multiple"):
            api.completion_params(GenerateConfig(max_tokens=max_tokens), tools=False)
    finally:
        asyncio.run(api.aclose())


def test_celeris_adapter_rejects_output_cap_larger_than_context(monkeypatch):
    _clear_celeris_env(monkeypatch)
    monkeypatch.setenv("CELERIS_API_KEY", "test-celeris-key")
    api = CelerisAPI("celeris-1")
    try:
        with pytest.raises(ValueError, match=str(CELERIS_MAX_CONTEXT_TOKENS)):
            api.completion_params(
                GenerateConfig(max_tokens=CELERIS_MAX_CONTEXT_TOKENS + 256),
                tools=False,
            )
    finally:
        asyncio.run(api.aclose())


def test_celeris_adapter_accepts_base_url_override(monkeypatch):
    _clear_celeris_env(monkeypatch)
    monkeypatch.setenv("CELERIS_OPENAI_BASE_URL", "https://unit.example/celeris/v1/")

    assert resolve_celeris_base_url() == "https://unit.example/celeris/v1"


def test_celeris_adapter_reports_required_api_key(monkeypatch):
    _clear_celeris_env(monkeypatch)

    with pytest.raises(PrerequisiteError) as exc_info:
        resolve_celeris_api_key()

    assert "CELERIS_API_KEY" in str(exc_info.value)
