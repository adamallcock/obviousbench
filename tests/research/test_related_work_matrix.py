from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import yaml

from obviousbench.research.related_work_matrix import (
    RelatedWorkMatrixInputs,
    build_related_work_matrix,
)


def _write_fixture(tmp_path: Path, *, cite: bool = True) -> dict[str, Path]:
    config_path = tmp_path / "related.yaml"
    paper_dir = tmp_path / "paper"
    bib_path = paper_dir / "references.bib"
    markdown_path = tmp_path / "related.md"
    tex_path = paper_dir / "tables" / "related_work_positioning.tex"
    (paper_dir / "sections").mkdir(parents=True)
    (paper_dir / "tables").mkdir()
    config_path.write_text(
        yaml.safe_dump(
            {
                "schema_version": "paper-related-work-v1",
                "selection_policy": {"rules": ["Prefer objective scoring."]},
                "entries": [
                    {
                        "id": "unitbench",
                        "citation_key": "unit2026bench",
                        "title": "UnitBench",
                        "year": 2026,
                        "source_url": "https://arxiv.org/abs/2601.00001",
                        "cluster": "unit tests",
                        "comparator_role": "Fixture comparator.",
                        "evidence_standard": "Objective scorer contracts.",
                        "obviousbench_stance": "Borrow scorer discipline.",
                        "manuscript_use": "Unit-test comparator.",
                        "required": True,
                    }
                ],
            },
            sort_keys=False,
        ),
        encoding="utf-8",
    )
    bib_path.write_text("@misc{unit2026bench,\n  title = {UnitBench}\n}\n", encoding="utf-8")
    related_text = "\\citep{unit2026bench}\n" if cite else "No citation yet.\n"
    (paper_dir / "sections" / "02_related_work.tex").write_text(
        related_text,
        encoding="utf-8",
    )
    return {
        "config": config_path,
        "paper_dir": paper_dir,
        "bib": bib_path,
        "markdown": markdown_path,
        "tex": tex_path,
    }


def test_related_work_matrix_writes_markdown_and_tex(tmp_path: Path):
    paths = _write_fixture(tmp_path)

    result = build_related_work_matrix(
        RelatedWorkMatrixInputs(
            config_path=paths["config"],
            paper_dir=paths["paper_dir"],
            bib_path=paths["bib"],
            markdown_path=paths["markdown"],
            tex_path=paths["tex"],
        )
    )

    assert result.ok
    assert result.entry_by_id("unitbench").bib_present
    assert result.entry_by_id("unitbench").cited_in_related_work
    markdown = paths["markdown"].read_text(encoding="utf-8")
    tex = paths["tex"].read_text(encoding="utf-8")
    assert "Overall status: PASS" in markdown
    assert "[UnitBench (2026)]" in markdown
    assert "\\citep{unit2026bench}" in tex


def test_related_work_matrix_blocks_missing_related_work_citation(tmp_path: Path):
    paths = _write_fixture(tmp_path, cite=False)

    result = build_related_work_matrix(
        RelatedWorkMatrixInputs(
            config_path=paths["config"],
            paper_dir=paths["paper_dir"],
            bib_path=paths["bib"],
            markdown_path=paths["markdown"],
            tex_path=paths["tex"],
        )
    )

    assert not result.ok
    entry = result.entry_by_id("unitbench")
    assert entry.bib_present
    assert not entry.cited_in_related_work
    assert "missing cite" in paths["markdown"].read_text(encoding="utf-8")


def test_related_work_matrix_script_writes_outputs(tmp_path: Path):
    paths = _write_fixture(tmp_path)

    result = subprocess.run(
        [
            sys.executable,
            "scripts/build_related_work_matrix.py",
            "--config",
            str(paths["config"]),
            "--paper-dir",
            str(paths["paper_dir"]),
            "--bib",
            str(paths["bib"]),
            "--markdown-out",
            str(paths["markdown"]),
            "--tex-out",
            str(paths["tex"]),
            "--strict",
        ],
        cwd=Path(__file__).parents[2],
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0
    assert "Wrote related-work matrix" in result.stdout
    assert paths["markdown"].exists()
    assert paths["tex"].exists()
