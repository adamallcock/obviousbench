import json

from obviousbench.datasets.validation import validate_dataset_paths
from tests.datasets.test_schemas import valid_record


def write_jsonl(path, rows):
    path.write_text("\n".join(json.dumps(row) for row in rows) + "\n", encoding="utf-8")


def test_valid_dataset_passes(tmp_path):
    path = tmp_path / "character_count.jsonl"
    write_jsonl(path, [valid_record()])

    report = validate_dataset_paths([path])

    assert report.ok
    assert report.issues == []


def test_duplicate_ids_fail_with_both_locations(tmp_path):
    first = tmp_path / "first.jsonl"
    second = tmp_path / "second.jsonl"
    write_jsonl(first, [valid_record()])
    write_jsonl(second, [valid_record()])

    report = validate_dataset_paths([first, second])

    assert not report.ok
    assert report.issues[0].code == "duplicate_id"
    assert "first.jsonl:1" in report.issues[0].message
    assert "second.jsonl:1" in report.issues[0].message


def test_h3_public_item_fails(tmp_path):
    path = tmp_path / "bad.jsonl"
    write_jsonl(path, [valid_record(human_triviality="H3")])

    report = validate_dataset_paths([path])

    assert not report.ok
    assert any(issue.code == "excluded_human_triviality" for issue in report.issues)


def test_unreviewed_public_item_fails(tmp_path):
    path = tmp_path / "bad.jsonl"
    write_jsonl(path, [valid_record(review_status="draft")])

    report = validate_dataset_paths([path])

    assert not report.ok
    assert any(issue.code == "unreviewed_public_item" for issue in report.issues)

