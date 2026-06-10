from __future__ import annotations

import subprocess
import sys
import tarfile
from pathlib import Path

from obviousbench.research.arxiv_source_bundle import (
    ArxivBundleAuditInputs,
    audit_arxiv_source_bundle,
)


def _write_tar(path: Path, root: Path, names: list[str]) -> None:
    with tarfile.open(path, "w:gz") as archive:
        for name in names:
            file_path = root / name
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text("content\n", encoding="utf-8")
            archive.add(file_path, arcname=name)


def test_audit_arxiv_source_bundle_passes_core_source_bundle(tmp_path: Path):
    bundle = tmp_path / "arxiv-src.tar.gz"
    _write_tar(
        bundle,
        tmp_path / "src",
        [
            "main.tex",
            "references.bib",
            "sections/01_introduction.tex",
            "tables/main_results.tex",
            "figures/leaderboard.pdf",
        ],
    )
    output_path = tmp_path / "audit.md"

    result = audit_arxiv_source_bundle(
        ArxivBundleAuditInputs(bundle_path=bundle, output_path=output_path)
    )

    assert result.ok
    assert result.issue_count == 0
    assert "Overall status: PASS" in output_path.read_text(encoding="utf-8")


def test_audit_arxiv_source_bundle_blocks_forbidden_paths(tmp_path: Path):
    bundle = tmp_path / "arxiv-src.tar.gz"
    _write_tar(
        bundle,
        tmp_path / "src",
        [
            "main.tex",
            "references.bib",
            "sections/01_introduction.tex",
            "results/raw/provider.log",
        ],
    )

    result = audit_arxiv_source_bundle(
        ArxivBundleAuditInputs(
            bundle_path=bundle,
            output_path=tmp_path / "audit.md",
        )
    )

    assert not result.ok
    assert any("results/raw/provider.log" in issue for issue in result.issues)


def test_audit_arxiv_source_bundle_script_writes_report(tmp_path: Path):
    bundle = tmp_path / "arxiv-src.tar.gz"
    output_path = tmp_path / "audit.md"
    _write_tar(
        bundle,
        tmp_path / "src",
        [
            "main.tex",
            "references.bib",
            "sections/01_introduction.tex",
        ],
    )

    result = subprocess.run(
        [
            sys.executable,
            "scripts/audit_arxiv_source_bundle.py",
            "--bundle",
            str(bundle),
            "--out",
            str(output_path),
        ],
        cwd=Path(__file__).parents[2],
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0
    assert "0 issue(s)" in result.stdout
    assert output_path.exists()
