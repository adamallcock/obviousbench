"""Tests for the public-repository hygiene guardrail."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from scripts.release.check_repo_hygiene import (
    REQUIRED_IGNORE_PATTERNS,
    REQUIRED_REPO_FILES,
    check_repo_hygiene,
    tracked_path_issues,
)


def _write(root: Path, relative: str, text: str = "ok\n") -> None:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _write_minimal_public_repo(root: Path) -> None:
    _write(root, ".gitignore", "\n".join(REQUIRED_IGNORE_PATTERNS) + "\n")
    for relative in REQUIRED_REPO_FILES:
        _write(root, relative)


def _issue_checks(paths: list[str]) -> set[str]:
    return {issue.check for issue in tracked_path_issues(paths)}


def test_public_hygiene_accepts_public_release_lanes(tmp_path: Path) -> None:
    _write_minimal_public_repo(tmp_path)
    _write(tmp_path, "scripts/release/build_v0_2_public_release_bundle.py")

    issues = check_repo_hygiene(
        tmp_path,
        tracked_paths=[
            "README.md",
            "data/public_examples/arithmetic.jsonl",
            "docs/release/v0_2/generated/README.md",
            "reports/v0_2/aggregate/summary.csv",
            "configs/registries/model_registry_v1.yaml",
            "scripts/release/build_v0_2_public_release_bundle.py",
        ],
        check_repository_files=True,
    )

    assert issues == []


def test_public_hygiene_rejects_private_and_generated_lanes() -> None:
    checks = _issue_checks(
        [
            ".DS_Store",
            "obviousbench/__pycache__/x.pyc",
            "data/private_heldout_v0_2/arithmetic.jsonl",
            "data/benchmark/private_heldout/v0_2/arithmetic.jsonl",
            "data/manifests/candidate_pools/candidate_pool_v0_2_all.jsonl",
            "data/manifests/splits/draft_v0_1/private_heldout_manifest.jsonl",
            "reports/v0_2/private_pass3/report.md",
            "reports/v0_1/private_pass3/report.md",
            "results/manifests/private.jsonl",
            "dist/public-bundle.zip",
        ]
    )

    assert "tracked-local-junk" in checks
    assert "tracked-private-data" in checks
    assert "tracked-private-candidate-pool" in checks
    assert "tracked-private-manifest" in checks
    assert "tracked-private-or-generated-report" in checks
    assert "tracked-nonaggregate-report" in checks
    assert "tracked-generated-output" in checks


def test_public_hygiene_rejects_legacy_data_and_private_doc_lanes() -> None:
    checks = _issue_checks(
        [
            "data/public_v0/arithmetic.jsonl",
            "data/dev_regression_v0_1/arithmetic.jsonl",
            "docs/internal/release-note.md",
            "docs/release/v0_1/generated/README.md",
            "docs/superpowers/plans/2026-06-10-plan.md",
        ]
    )

    assert "tracked-legacy-data-path" in checks
    assert "tracked-disallowed-doc-path" in checks


def test_public_hygiene_rejects_stale_active_doc_references(tmp_path: Path) -> None:
    _write_minimal_public_repo(tmp_path)
    _write(
        tmp_path,
        "README.md",
        "Do not link wrong_answer_review.html from public docs.\n",
    )

    issues = check_repo_hygiene(
        tmp_path,
        tracked_paths=["README.md"],
        check_repository_files=True,
    )

    assert [issue.check for issue in issues] == ["banned-active-text-reference"]


def test_public_hygiene_rejects_forbidden_private_imports(tmp_path: Path) -> None:
    _write_minimal_public_repo(tmp_path)
    _write(
        tmp_path,
        "obviousbench/release/bad.py",
        "from obviousbench.research.paper_assets import build\n",
    )

    issues = check_repo_hygiene(
        tmp_path,
        tracked_paths=["obviousbench/release/bad.py"],
        check_repository_files=False,
    )

    assert [issue.check for issue in issues] == ["forbidden-private-code-import"]


def test_public_hygiene_script_passes_current_checkout() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/release/check_repo_hygiene.py"],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert "Repo hygiene check passed." in result.stdout
