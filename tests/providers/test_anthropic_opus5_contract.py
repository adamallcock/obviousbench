from __future__ import annotations

import asyncio
import os
import subprocess
import sys
from pathlib import Path

from inspect_ai.model import GenerateConfig, get_model


def _opus5_api(monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-anthropic-key")
    import obviousbench._registry as registry

    assert registry.anthropic_opus5 is not None
    model = get_model("anthropic-opus5/claude-opus-5")
    return model.api


def test_opus5_none_uses_documented_disabled_thinking_wire_contract(monkeypatch):
    api = _opus5_api(monkeypatch)
    try:
        params, extra_body, _headers, _betas = api.completion_config(
            GenerateConfig(
                max_tokens=64,
                reasoning_effort="none",
                effort="high",
            )
        )

        assert params["model"] == "claude-opus-5"
        assert params["max_tokens"] == 64
        assert params["thinking"] == {"type": "disabled"}
        assert params["output_config"] == {"effort": "high"}
        assert extra_body == {}
    finally:
        asyncio.run(api.aclose())


def test_opus5_named_effort_uses_adaptive_thinking_wire_contract(monkeypatch):
    api = _opus5_api(monkeypatch)
    try:
        params, extra_body, _headers, _betas = api.completion_config(
            GenerateConfig(max_tokens=8264, reasoning_effort="high")
        )

        assert params["model"] == "claude-opus-5"
        assert params["thinking"] == {"type": "adaptive", "display": "summarized"}
        assert params["output_config"] == {"effort": "high"}
        assert extra_body == {}
    finally:
        asyncio.run(api.aclose())


def test_inspect_entry_point_registers_opus5_route_in_fresh_interpreter():
    script = """
import asyncio
from inspect_ai.model import get_model

model = get_model('anthropic-opus5/claude-opus-5')
assert model.api.service_model_name() == 'claude-opus-5'
asyncio.run(model.api.aclose())
"""
    repo_root = Path(__file__).resolve().parents[2]
    result = subprocess.run(
        [sys.executable, "-c", script],
        cwd=repo_root,
        env={**os.environ, "ANTHROPIC_API_KEY": "test-anthropic-key"},
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr
