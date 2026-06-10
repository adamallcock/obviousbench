from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from obviousbench.research.pdf_build_handoff import (
    PdfBuildHandoffInputs,
    build_pdf_build_handoff,
)


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def test_pdf_build_handoff_blocks_current_missing_toolchain_and_pdf(tmp_path: Path):
    pdf_audit = tmp_path / "pdf-audit.md"
    source_audit = tmp_path / "source-audit.md"
    output = tmp_path / "handoff.md"
    _write(
        pdf_audit,
        "Overall status: BLOCKED\n"
        "Summary: 0 passed, 4 failed.\n"
        "| PDF artifact | FAIL | Missing file: paper/main.pdf |\n"
        "| LaTeX build log | FAIL | Missing file: paper/main.log |\n",
    )
    _write(
        source_audit,
        "Overall status: BLOCKED\n"
        "Summary: 5 passed, 1 failed.\n"
        "| submission markers | FAIL | main.tex contains claimblocked |\n",
    )

    result = build_pdf_build_handoff(
        PdfBuildHandoffInputs(
            output_path=output,
            pdf_audit_path=pdf_audit,
            source_audit_path=source_audit,
            available_commands=("brew",),
        )
    )

    assert not result.ok
    assert result.status == "blocked"
    assert any(
        blocker.startswith("No LaTeX build command is available")
        for blocker in result.blockers
    )
    text = output.read_text(encoding="utf-8")
    assert "brew install tectonic" in text
    assert "brew install --cask mactex" in text
    assert "make -C paper sweep-plan" not in text


def test_pdf_build_handoff_passes_when_audits_and_toolchain_pass(tmp_path: Path):
    pdf_audit = tmp_path / "pdf-audit.md"
    source_audit = tmp_path / "source-audit.md"
    output = tmp_path / "handoff.md"
    _write(pdf_audit, "Overall status: PASS\nSummary: 4 passed, 0 failed.\n")
    _write(source_audit, "Overall status: PASS\nSummary: 6 passed, 0 failed.\n")

    result = build_pdf_build_handoff(
        PdfBuildHandoffInputs(
            output_path=output,
            pdf_audit_path=pdf_audit,
            source_audit_path=source_audit,
            available_commands=("latexmk", "brew"),
        )
    )

    assert result.ok
    assert result.blockers == ()
    text = output.read_text(encoding="utf-8")
    assert "Overall status: PASS" in text
    assert "Available LaTeX commands: `latexmk`" in text


def test_pdf_build_handoff_script_can_fail_strictly(tmp_path: Path):
    pdf_audit = tmp_path / "pdf-audit.md"
    source_audit = tmp_path / "source-audit.md"
    output = tmp_path / "handoff.md"
    _write(pdf_audit, "Overall status: BLOCKED\nSummary: 0 passed, 4 failed.\n")
    _write(source_audit, "Overall status: PASS\nSummary: 6 passed, 0 failed.\n")

    result = subprocess.run(
        [
            sys.executable,
            "scripts/build_pdf_build_handoff.py",
            "--pdf-audit",
            str(pdf_audit),
            "--source-audit",
            str(source_audit),
            "--out",
            str(output),
            "--available-command",
            "brew",
            "--strict",
        ],
        cwd=Path(__file__).parents[2],
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 1
    assert "Wrote PDF build handoff" in result.stdout
    assert output.exists()
