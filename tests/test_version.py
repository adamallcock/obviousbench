"""Release/package version consistency checks."""

from __future__ import annotations

import tomllib
from pathlib import Path

import yaml

import obviousbench

ROOT = Path(__file__).resolve().parents[1]


def test_package_version_matches_release_config() -> None:
    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    release = yaml.safe_load(
        (ROOT / "configs/releases/release_v0_2_0.yaml").read_text(encoding="utf-8")
    )

    version = str(release["release"]["version"])

    assert pyproject["project"]["version"] == version
    assert obviousbench.__version__ == version
