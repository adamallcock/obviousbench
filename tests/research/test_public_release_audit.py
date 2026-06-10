from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from obviousbench.research.public_release_audit import (
    PublicReleaseAuditInputs,
    audit_public_release_artifacts,
)


def _write(path: Path, text: str = "content\n") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _write_required_files(root: Path) -> None:
    for relative in (
        "README.md",
        "docs/benchmark_card.md",
        "docs/methodology.md",
        "docs/scoring_policy.md",
        "docs/source_policy.md",
        "docs/prompt_policy.md",
        "paper/README.md",
        "data/splits/paper_v1_manifest.jsonl",
        "data/barrages/hard_obvious_8x10_seed_20260531.jsonl",
        "data/item_cards/public_v0/cards.yaml",
        "configs/paper_v1_model_panel.yaml",
        "configs/paper_v1_final_sweep_manifest.csv",
    ):
        _write(root / relative)


def _metadata(confirmed: bool) -> str:
    status = "confirmed" if confirmed else "draft"
    bool_value = "true" if confirmed else "false"
    repo = "https://github.com/example/obviousbench" if confirmed else "TODO(repo)"
    dataset = "https://doi.org/10.0000/example" if confirmed else "TODO(dataset)"
    return f"""---
title: Metadata
status: {status}
metadata_status: {status}
repository_url: "{repo}"
dataset_url: "{dataset}"
submitter_registered_author: {bool_value}
endorsement_checked: {bool_value}
submitter_is_author_or_authorized_proxy: {bool_value}
title_and_abstract_checked: {bool_value}
---
"""


def test_public_release_audit_blocks_missing_license_and_metadata(tmp_path: Path):
    root = tmp_path / "repo"
    _write_required_files(root)
    _write(root / "pyproject.toml", "[project]\nname='obviousbench'\n")
    metadata = root / "metadata.md"
    _write(metadata, _metadata(confirmed=False))

    result = audit_public_release_artifacts(
        PublicReleaseAuditInputs(
            root_dir=root,
            output_path=root / "audit.md",
            metadata_path=metadata,
        )
    )

    assert not result.ok
    assert result.check_by_name("public documentation").status == "pass"
    assert result.check_by_name("license and citation files").status == "fail"
    assert result.check_by_name("public release URLs").status == "fail"
    text = result.output_path.read_text(encoding="utf-8")
    assert "Overall status: BLOCKED" in text
    assert "Do not mark the arXiv metadata note as confirmed" in text


def test_public_release_audit_passes_complete_release_surface(tmp_path: Path):
    root = tmp_path / "repo"
    _write_required_files(root)
    _write(root / "LICENSE", "MIT\n")
    _write(root / "CITATION.cff", "cff-version: 1.2.0\n")
    _write(root / ".zenodo.json", "{}\n")
    _write(root / "pyproject.toml", "[project]\nname='obviousbench'\nlicense='MIT'\n")
    metadata = root / "metadata.md"
    _write(metadata, _metadata(confirmed=True))

    result = audit_public_release_artifacts(
        PublicReleaseAuditInputs(
            root_dir=root,
            output_path=root / "audit.md",
            metadata_path=metadata,
        )
    )

    assert result.ok
    assert result.failed_count == 0
    assert "Overall status: PASS" in result.output_path.read_text(encoding="utf-8")


def test_public_release_audit_script_writes_report(tmp_path: Path):
    root = tmp_path / "repo"
    _write_required_files(root)
    _write(root / "pyproject.toml", "[project]\nname='obviousbench'\n")
    metadata = root / "metadata.md"
    output_path = root / "audit.md"
    _write(metadata, _metadata(confirmed=False))

    result = subprocess.run(
        [
            sys.executable,
            "scripts/audit_public_release_artifacts.py",
            "--root",
            str(root),
            "--metadata",
            str(metadata),
            "--out",
            str(output_path),
        ],
        cwd=Path(__file__).parents[2],
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0
    assert "Wrote public release artifact audit" in result.stdout
    assert output_path.exists()
