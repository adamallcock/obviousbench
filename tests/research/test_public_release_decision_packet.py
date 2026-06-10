from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from obviousbench.research.public_release_decision_packet import (
    PublicReleaseDecisionPacketInputs,
    build_public_release_decision_packet,
)


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _metadata(*, confirmed: bool) -> str:
    if not confirmed:
        return """---
title: Metadata
status: draft
metadata_status: draft
license: "TODO(confirm license)"
repository_url: "TODO(confirm repository)"
dataset_url: "TODO(confirm dataset)"
submitter_registered_author: false
endorsement_checked: false
submitter_is_author_or_authorized_proxy: false
title_and_abstract_checked: false
---
"""
    return """---
title: Metadata
status: confirmed
metadata_status: confirmed
license: "MIT"
repository_url: "https://github.com/example/obviousbench"
dataset_url: "https://doi.org/10.0000/example"
submitter_registered_author: true
endorsement_checked: true
submitter_is_author_or_authorized_proxy: true
title_and_abstract_checked: true
---
"""


def _inputs(tmp_path: Path, *, complete: bool) -> PublicReleaseDecisionPacketInputs:
    root = tmp_path / "repo"
    metadata = root / "metadata.md"
    release_audit = root / "release-audit.md"
    _write(metadata, _metadata(confirmed=complete))
    _write(release_audit, "Overall status: PASS\n" if complete else "Overall status: BLOCKED\n")
    _write(root / "pyproject.toml", "[project]\nname='obviousbench'\n")
    if complete:
        _write(root / "LICENSE", "MIT\n")
        _write(
            root / "CITATION.cff",
            "cff-version: 1.2.0\ntitle: ObviousBench\n",
        )
        _write(root / ".zenodo.json", "{}\n")
        _write(
            root / "pyproject.toml",
            "[project]\nname='obviousbench'\nlicense='MIT'\n",
        )
    return PublicReleaseDecisionPacketInputs(
        root_dir=root,
        output_path=root / "decision-packet.md",
        metadata_path=metadata,
        release_audit_path=release_audit,
    )


def test_release_decision_packet_blocks_unconfirmed_release_decisions(tmp_path: Path):
    inputs = _inputs(tmp_path, complete=False)

    result = build_public_release_decision_packet(inputs)

    assert not result.ok
    assert result.decision_by_name("license selection").status == "needs-confirmation"
    assert result.decision_by_name("public repository and artifact URLs").status == (
        "needs-confirmation"
    )
    text = inputs.output_path.read_text(encoding="utf-8")
    assert "Overall status: BLOCKED" in text
    assert "CITATION.cff" in text
    assert not (inputs.root_dir / "LICENSE").exists()


def test_release_decision_packet_can_pass_confirmed_release_surface(tmp_path: Path):
    inputs = _inputs(tmp_path, complete=True)

    result = build_public_release_decision_packet(inputs)

    assert result.ok
    assert result.needs_confirmation_count == 0
    assert "Overall status: PASS" in inputs.output_path.read_text(encoding="utf-8")


def test_release_decision_packet_script_writes_report(tmp_path: Path):
    inputs = _inputs(tmp_path, complete=False)

    result = subprocess.run(
        [
            sys.executable,
            "scripts/build_public_release_decision_packet.py",
            "--root",
            str(inputs.root_dir),
            "--metadata",
            str(inputs.metadata_path),
            "--release-audit",
            str(inputs.release_audit_path),
            "--out",
            str(inputs.output_path),
        ],
        cwd=Path(__file__).parents[2],
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0
    assert "Wrote public release decision packet" in result.stdout
    assert inputs.output_path.exists()
