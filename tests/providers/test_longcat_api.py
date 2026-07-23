from __future__ import annotations

import asyncio
import os
import subprocess
import sys
from pathlib import Path

import pytest
from inspect_ai._util.error import PrerequisiteError
from inspect_ai.model import GenerateConfig, get_model

from obviousbench.providers.longcat import (
    DEFAULT_LONGCAT_BASE_URL,
    LONGCAT_API_KEY_VARS,
    LONGCAT_BASE_URL_VARS,
    LongCatAPI,
    resolve_longcat_api_key,
    resolve_longcat_base_url,
)


def _clear_longcat_env(monkeypatch: pytest.MonkeyPatch) -> None:
    for env_var in (*LONGCAT_API_KEY_VARS, *LONGCAT_BASE_URL_VARS):
        monkeypatch.delenv(env_var, raising=False)


def test_longcat_adapter_uses_documented_openai_compatible_endpoint(monkeypatch):
    _clear_longcat_env(monkeypatch)
    monkeypatch.setenv("LONGCAT_API_KEY", "test-longcat-key")

    api = LongCatAPI("LongCat-2.0")
    try:
        assert api.service_model_name() == "LongCat-2.0"
        assert api.base_url == DEFAULT_LONGCAT_BASE_URL
        assert api.api_key == "test-longcat-key"
        assert api.responses_api is False
    finally:
        asyncio.run(api.aclose())


def test_longcat_registered_route_resolves_model(monkeypatch):
    _clear_longcat_env(monkeypatch)
    monkeypatch.setenv("LONGCAT_API_KEY", "test-longcat-key")
    import obviousbench._registry as registry

    assert registry.longcat is not None
    model = get_model("longcat/LongCat-2.0")
    try:
        assert model.api.service_model_name() == "LongCat-2.0"
    finally:
        asyncio.run(model.api.aclose())


def test_inspect_entry_point_registers_longcat_route_in_fresh_interpreter():
    script = """
import asyncio
from inspect_ai.model import get_model

model = get_model('longcat/LongCat-2.0')
assert model.api.service_model_name() == 'LongCat-2.0'
asyncio.run(model.api.aclose())
"""
    repo_root = Path(__file__).resolve().parents[2]
    result = subprocess.run(
        [sys.executable, "-c", script],
        cwd=repo_root,
        env={**os.environ, "LONGCAT_API_KEY": "test-longcat-key"},
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr


@pytest.mark.parametrize("thinking_type", ["disabled", "enabled"])
def test_longcat_adapter_preserves_documented_thinking_types(monkeypatch, thinking_type):
    _clear_longcat_env(monkeypatch)
    monkeypatch.setenv("LONGCAT_API_KEY", "test-longcat-key")
    api = LongCatAPI("LongCat-2.0")
    try:
        assert api.completion_params(
            GenerateConfig(
                max_tokens=64,
                extra_body={"thinking": {"type": thinking_type}},
            ),
            tools=False,
        ) == {
            "model": "LongCat-2.0",
            "max_tokens": 64,
            "extra_body": {"thinking": {"type": thinking_type}},
        }
    finally:
        asyncio.run(api.aclose())


def test_longcat_adapter_rejects_an_undocumented_thinking_type(monkeypatch):
    _clear_longcat_env(monkeypatch)
    monkeypatch.setenv("LONGCAT_API_KEY", "test-longcat-key")
    api = LongCatAPI("LongCat-2.0")
    try:
        with pytest.raises(ValueError, match="disabled, enabled"):
            api.completion_params(
                GenerateConfig(extra_body={"thinking": {"type": "medium"}}),
                tools=False,
            )
    finally:
        asyncio.run(api.aclose())


def test_longcat_adapter_accepts_base_url_override(monkeypatch):
    _clear_longcat_env(monkeypatch)
    monkeypatch.setenv("LONGCAT_OPENAI_BASE_URL", "https://unit.example/openai/v1/")

    assert resolve_longcat_base_url() == "https://unit.example/openai/v1"


def test_longcat_adapter_reports_required_api_key(monkeypatch):
    _clear_longcat_env(monkeypatch)

    with pytest.raises(PrerequisiteError) as exc_info:
        resolve_longcat_api_key()

    assert "LONGCAT_API_KEY" in str(exc_info.value)
