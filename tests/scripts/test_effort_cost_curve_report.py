from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]


def _load_effort_report_module():
    path = ROOT / "scripts" / "build_effort_cost_curve_report.py"
    spec = importlib.util.spec_from_file_location("build_effort_cost_curve_report", path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_effort_cost_report_reads_release_paths_and_theme():
    module = _load_effort_report_module()
    release = yaml.safe_load((ROOT / "configs/release_v0_1_0.yaml").read_text())
    theme = yaml.safe_load((ROOT / "configs/release_theme_v0_1_0.yaml").read_text())

    assert ROOT / release["effort_cost"]["report_dir"] == module.REPORT_DIR
    assert ROOT / release["effort_cost"]["points_csv"] == module.POINTS_CSV
    assert ROOT / release["snapshot"]["report_dir"] / "leaderboard.csv" == module.LEADERBOARD_CSV
    assert module.MODEL_COLORS["GPT-5.4 mini"] == theme["models"]["GPT-5.4 mini"]
    assert module.EFFORT_STYLES["low"] == (
        theme["efforts"]["low"]["color"],
        theme["efforts"]["low"]["dash"],
    )
    assert theme["chart_defaults"]["answer_metric_label"] == module.ANSWER_AXIS_LABEL
