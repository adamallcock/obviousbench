from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from obviousbench.research.human_baseline_form import (
    HumanBaselineFormInputs,
    build_human_baseline_form,
)
from tests.datasets.test_schemas import valid_record


def _write_jsonl(path: Path, rows: list[dict]) -> None:
    path.write_text("\n".join(json.dumps(row) for row in rows) + "\n", encoding="utf-8")


def test_build_human_baseline_form_writes_markdown_and_csv_template(tmp_path: Path):
    dataset_path = tmp_path / "items.jsonl"
    manifest_path = tmp_path / "paper_v1_manifest.jsonl"
    form_path = tmp_path / "form.md"
    csv_path = tmp_path / "paper_v1.csv"
    item = valid_record()
    _write_jsonl(dataset_path, [item])
    _write_jsonl(manifest_path, [{"item_id": item["id"]}])

    result = build_human_baseline_form(
        HumanBaselineFormInputs(
            manifest_path=manifest_path,
            dataset_paths=[dataset_path],
            form_path=form_path,
            csv_path=csv_path,
        )
    )

    form_text = form_path.read_text(encoding="utf-8")
    assert result.item_count == 1
    assert item["id"] in form_text
    assert item["question"] in form_text
    assert item["target"] not in form_text
    assert csv_path.read_text(encoding="utf-8") == (
        "item_id,participant_id,answer,seconds,correct,notes\n"
    )


def test_build_human_baseline_form_script_writes_outputs(tmp_path: Path):
    dataset_path = tmp_path / "items.jsonl"
    manifest_path = tmp_path / "paper_v1_manifest.jsonl"
    form_path = tmp_path / "form.md"
    csv_path = tmp_path / "paper_v1.csv"
    item = valid_record()
    _write_jsonl(dataset_path, [item])
    _write_jsonl(manifest_path, [{"item_id": item["id"]}])

    result = subprocess.run(
        [
            sys.executable,
            "scripts/build_human_baseline_form.py",
            "--manifest",
            str(manifest_path),
            "--dataset",
            str(dataset_path),
            "--form-out",
            str(form_path),
            "--csv-out",
            str(csv_path),
        ],
        cwd=Path(__file__).parents[2],
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0
    assert "Wrote 1 human-baseline form item" in result.stdout
    assert form_path.exists()
    assert csv_path.exists()
