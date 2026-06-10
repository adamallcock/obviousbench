from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

PANEL_PATH = Path("configs/paper_v1_8x28_current_222_20260602_panel.yaml")


def _panel() -> dict[str, Any]:
    return yaml.safe_load(PANEL_PATH.read_text(encoding="utf-8"))


def test_anthropic_effort_entries_preserve_adaptive_control_style():
    panel = _panel()
    missing = []
    for entry in panel["entries"]:
        inspect_model = str(entry.get("inspect_model") or "")
        generation_settings = entry.get("generation_settings") or {}
        if (
            inspect_model.startswith("anthropic/")
            and isinstance(generation_settings, dict)
            and generation_settings.get("effort") is not None
            and entry.get("control_style") != "anthropic_adaptive_thinking_effort"
        ):
            missing.append(entry["id"])

    assert missing == []
