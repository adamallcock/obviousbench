from __future__ import annotations

import hashlib
import subprocess
import sys
from pathlib import Path

from obviousbench.research.paper_repro_manifest import (
    GitState,
    PaperReproManifestInputs,
    ReproArtifactSpec,
    ReproCommandSpec,
    build_paper_repro_manifest,
)


def test_manifest_hashes_artifacts_and_omits_provider_output_paths(tmp_path: Path):
    root = tmp_path / "repo"
    root.mkdir()
    root.joinpath("paper").mkdir()
    root.joinpath("paper", "main.tex").write_text("paper source\n", encoding="utf-8")
    root.joinpath("configs").mkdir()
    root.joinpath("configs", "panel.yaml").write_text("entries: []\n", encoding="utf-8")
    output_path = tmp_path / "manifest.md"

    result = build_paper_repro_manifest(
        PaperReproManifestInputs(
            root_dir=root,
            output_path=output_path,
            artifact_specs=(
                ReproArtifactSpec("paper/main.tex", "source"),
                ReproArtifactSpec("configs/panel.yaml", "config"),
            ),
            command_specs=(
                ReproCommandSpec(
                    "make -C paper assets",
                    "Regenerate local paper assets.",
                    "Should pass.",
                ),
            ),
            include_git_state=False,
        )
    )

    artifact = result.artifact_by_path("paper/main.tex")
    assert result.ok
    assert artifact.size_bytes == len("paper source\n")
    assert artifact.sha256 == hashlib.sha256(b"paper source\n").hexdigest()
    text = output_path.read_text(encoding="utf-8")
    assert "make -C paper assets" in text
    assert "results/raw" not in text
    assert "results/summaries" not in text


def test_manifest_blocks_missing_required_artifacts(tmp_path: Path):
    root = tmp_path / "repo"
    root.mkdir()
    output_path = tmp_path / "manifest.md"

    result = build_paper_repro_manifest(
        PaperReproManifestInputs(
            root_dir=root,
            output_path=output_path,
            artifact_specs=(ReproArtifactSpec("paper/main.tex", "source"),),
            include_git_state=False,
        )
    )

    assert not result.ok
    assert result.missing_required_count == 1
    assert result.artifact_by_path("paper/main.tex").exists is False
    text = output_path.read_text(encoding="utf-8")
    assert "Overall status: BLOCKED" in text
    assert "`paper/main.tex`" in text


def test_manifest_records_git_state_without_running_git(tmp_path: Path):
    root = tmp_path / "repo"
    root.mkdir()
    root.joinpath("paper").mkdir()
    root.joinpath("paper", "main.tex").write_text("source\n", encoding="utf-8")
    output_path = tmp_path / "manifest.md"

    result = build_paper_repro_manifest(
        PaperReproManifestInputs(
            root_dir=root,
            output_path=output_path,
            artifact_specs=(ReproArtifactSpec("paper/main.tex", "source"),),
            git_state=GitState(
                head="abc1234",
                dirty=True,
                status_summary="2 changed or untracked path(s)",
            ),
        )
    )

    assert result.ok
    text = output_path.read_text(encoding="utf-8")
    assert "Head: `abc1234`" in text
    assert "Worktree: `dirty`" in text


def test_manifest_script_writes_report_with_custom_artifacts(tmp_path: Path):
    root = tmp_path / "repo"
    root.mkdir()
    root.joinpath("paper").mkdir()
    root.joinpath("paper", "main.tex").write_text("source\n", encoding="utf-8")
    output_path = tmp_path / "manifest.md"

    result = subprocess.run(
        [
            sys.executable,
            "scripts/build_paper_repro_manifest.py",
            "--root",
            str(root),
            "--out",
            str(output_path),
            "--artifact",
            "paper/main.tex",
            "--no-git-state",
        ],
        cwd=Path(__file__).parents[2],
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0
    assert "Wrote paper reproducibility manifest" in result.stdout
    assert output_path.exists()
