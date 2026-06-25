#!/usr/bin/env python3
"""Audit a v0.2 public-local bundle for private held-out leaks."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DATA_DIR = ROOT / "data"
DEFAULT_BUNDLE_DIR = ROOT / "dist/obviousbench-v0.2-public-local"

TEXT_SUFFIXES = {
    ".csv",
    ".html",
    ".json",
    ".jsonl",
    ".md",
    ".txt",
    ".yaml",
    ".yml",
}

FORBIDDEN_PATH_PARTS = {
    "private_heldout",
    "private_heldout_v0_2",
    "question_failure_review_assets",
    "raw",
}

FORBIDDEN_FILENAMES = {
    "attempt_detail_cache_v0_2_review.jsonl",
    "attempts.csv",
    "blank_provider_faults.csv",
    "items.csv",
    "question_failure_review.html",
    "wrong_answer_review.html",
}

FORBIDDEN_TEXT_SNIPPETS = {
    ".codex/worktrees",
    "/Users/",
    "data/private_heldout",
    "data/benchmark/private_heldout/v0_2",
    "question_failure_review_assets",
    "reports/private_pass3",
    "reports/v0_2/private_pass3",
    "results/manifests/v0_2_private",
    "attempt_detail_cache_v0_2_review.jsonl",
    "wrong_answer_review.html",
    "question_failure_review.html",
    "blank_provider_faults.csv",
}

REQUIRED_GENERATED_MARKDOWN_SNIPPETS = {
    "## Generated Artifact Notice",
    "Source config:",
    "Generator:",
    "Status:",
    "Public/private boundary:",
}

COMMON_MULTIPLE_CHOICE_STRINGS = {
    "it is impossible",
    "none of the above",
    "all of the above",
}

IGNORED_BUNDLE_FILENAMES = {
    ".DS_Store",
}

IGNORED_BUNDLE_PATH_PARTS = {
    "__MACOSX",
}


@dataclass(frozen=True)
class AuditIssue:
    code: str
    message: str
    path: str | None = None
    line: int | None = None
    label: str | None = None

    def as_dict(self) -> dict[str, Any]:
        row: dict[str, Any] = {"code": self.code, "message": self.message}
        if self.path is not None:
            row["path"] = self.path
        if self.line is not None:
            row["line"] = self.line
        if self.label is not None:
            row["label"] = self.label
        return row


def rel(path: Path, *, root: Path = ROOT) -> str:
    try:
        return str(path.resolve().relative_to(root))
    except ValueError:
        return str(path)


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def private_manifest_rows(data_dir: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    rows.extend(
        read_jsonl(
            data_dir
            / "manifests/candidate_pools/candidate_pool_v0_2_private_heldout_draft_manifest.jsonl"
        )
    )
    rows.extend(
        read_jsonl(
            data_dir / "splits/candidate_pool_v0_2_private_heldout_draft_manifest.jsonl"
        )
    )
    for private_runtime_dir in (
        data_dir / "benchmark/private_heldout/v0_2",
        data_dir / "private_heldout_v0_2",
    ):
        if private_runtime_dir.exists():
            for path in sorted(private_runtime_dir.glob("*.jsonl")):
                rows.extend(read_jsonl(path))
    return rows


def private_leak_terms(rows: list[dict[str, Any]]) -> dict[str, str]:
    terms: dict[str, str] = {}
    for row in rows:
        metadata = row.get("metadata") if isinstance(row.get("metadata"), dict) else {}
        answer_type = str(row.get("answer_type") or "")
        row_id = str(row.get("id") or row.get("pool_id") or row.get("candidate_id") or "")
        question = str(row.get("question") or "")
        prompt = str(row.get("prompt") or "")
        target = str(row.get("target") or "")
        choices = row.get("choices") or metadata.get("choices")
        pool_id = str(row.get("pool_id") or metadata.get("pool_id") or "")
        candidate_id = str(row.get("candidate_id") or metadata.get("candidate_id") or "")

        if len(question.strip()) >= 12:
            terms[question] = f"{row_id}:question"
        if len(prompt.strip()) >= 12:
            terms[prompt] = f"{row_id}:prompt"
        if is_distinctive_private_text(target, answer_type=answer_type):
            terms[target] = f"{row_id}:target"
        if len(pool_id.strip()) >= 6:
            terms[pool_id] = f"{row_id}:pool_id"
        if len(candidate_id.strip()) >= 6:
            terms[candidate_id] = f"{row_id}:candidate_id"
        if row.get("id") and len(str(row["id"])) >= 10:
            terms[str(row["id"])] = f"{row_id}:runtime_id"

        if isinstance(choices, list):
            for index, choice in enumerate(choices, start=1):
                choice_text = str(choice)
                if is_distinctive_private_choice(choice_text):
                    terms[choice_text] = f"{row_id}:choice_{index}"
        elif isinstance(choices, str) and is_distinctive_private_choice(choices):
            terms[choices] = f"{row_id}:choices"
    return terms


def is_distinctive_private_text(text: str, *, answer_type: str = "") -> bool:
    value = text.strip()
    if len(value) < 8:
        return False
    if answer_type == "multiple_choice" and len(value) == 1:
        return False
    if value.lower() in COMMON_MULTIPLE_CHOICE_STRINGS:
        return False
    if len(value) >= 18:
        return True
    return any(char in value for char in ("_", "-", "|", ";", ",", " "))


def is_distinctive_private_choice(text: str) -> bool:
    value = text.strip()
    if value.lower() in COMMON_MULTIPLE_CHOICE_STRINGS:
        return False
    return len(value) >= 28


def is_ignored_bundle_file(path: Path) -> bool:
    return path.name in IGNORED_BUNDLE_FILENAMES or bool(
        set(path.parts) & IGNORED_BUNDLE_PATH_PARTS
    )


def bundle_files(bundle_dir: Path) -> list[Path]:
    return sorted(
        path
        for path in bundle_dir.rglob("*")
        if path.is_file() and not is_ignored_bundle_file(path.relative_to(bundle_dir))
    )


def text_files(bundle_dir: Path) -> list[Path]:
    return sorted(
        path
        for path in bundle_files(bundle_dir)
        if path.suffix.lower() in TEXT_SUFFIXES
    )


def validate_bundle_paths(bundle_dir: Path) -> list[AuditIssue]:
    issues: list[AuditIssue] = []
    for path in bundle_files(bundle_dir):
        relative = path.relative_to(bundle_dir)
        parts = set(relative.parts)
        forbidden_parts = sorted(parts & FORBIDDEN_PATH_PARTS)
        if forbidden_parts:
            issues.append(
                AuditIssue(
                    code="forbidden_private_path",
                    message="Public bundle contains a forbidden private/raw path component.",
                    path=rel(path),
                    label=",".join(forbidden_parts),
                )
            )
        if path.name in FORBIDDEN_FILENAMES:
            issues.append(
                AuditIssue(
                    code="forbidden_private_file",
                    message="Public bundle contains a forbidden private report/review file.",
                    path=rel(path),
                    label=path.name,
                )
            )
    return issues


def scan_private_terms(*, bundle_dir: Path, leak_terms: dict[str, str]) -> list[AuditIssue]:
    issues: list[AuditIssue] = []
    for path in text_files(bundle_dir):
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except UnicodeDecodeError:
            continue
        for line_number, line in enumerate(lines, start=1):
            for snippet in FORBIDDEN_TEXT_SNIPPETS:
                if snippet in line:
                    issues.append(
                        AuditIssue(
                            code="forbidden_private_reference",
                            message="Public bundle references a private raw/review artifact.",
                            path=rel(path),
                            line=line_number,
                            label=snippet,
                        )
                    )
            for term, label in leak_terms.items():
                if term and term in line:
                    issues.append(
                        AuditIssue(
                            code="private_term_leak",
                            message="Public bundle contains private split text or identifier.",
                            path=rel(path),
                            line=line_number,
                            label=label,
                        )
                    )
    return issues


def validate_generated_markdown_provenance(bundle_dir: Path) -> list[AuditIssue]:
    issues: list[AuditIssue] = []
    generated_root = bundle_dir / "docs/release/v0_2/generated"
    if not generated_root.exists():
        return issues
    for path in sorted(generated_root.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        missing = sorted(
            snippet for snippet in REQUIRED_GENERATED_MARKDOWN_SNIPPETS if snippet not in text
        )
        if missing:
            issues.append(
                AuditIssue(
                    code="missing_generated_provenance",
                    message="Generated public markdown is missing required provenance text.",
                    path=rel(path),
                    label=",".join(missing),
                )
            )
    return issues


def validate_bundle_manifest(bundle_dir: Path) -> list[AuditIssue]:
    manifest_path = bundle_dir / "bundle_manifest.json"
    if not manifest_path.exists():
        return [
            AuditIssue(
                code="missing_bundle_manifest",
                message="Public bundle is missing bundle_manifest.json.",
                path=rel(manifest_path),
            )
        ]
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [
            AuditIssue(
                code="invalid_bundle_manifest",
                message=f"Public bundle manifest is invalid JSON: {exc}",
                path=rel(manifest_path),
            )
        ]
    declared = sorted(str(item) for item in manifest.get("included_files", []))
    actual = sorted(str(path.relative_to(bundle_dir)) for path in bundle_files(bundle_dir))
    if declared != actual:
        return [
            AuditIssue(
                code="bundle_manifest_mismatch",
                message="bundle_manifest.json included_files does not match actual files.",
                path=rel(manifest_path),
                label=f"declared={len(declared)} actual={len(actual)}",
            )
        ]
    return []


def audit_public_bundle(
    *,
    bundle_dir: Path = DEFAULT_BUNDLE_DIR,
    data_dir: Path = DEFAULT_DATA_DIR,
) -> dict[str, Any]:
    issues: list[AuditIssue] = []
    if not bundle_dir.exists():
        issues.append(
            AuditIssue(
                code="missing_bundle",
                message="Public bundle directory does not exist.",
                path=rel(bundle_dir),
            )
        )
        return {
            "ok": False,
            "issue_count": len(issues),
            "issues": [issue.as_dict() for issue in issues],
            "bundle_dir": rel(bundle_dir),
            "data_dir": rel(data_dir),
            "private_rows_loaded": 0,
            "private_terms_scanned": 0,
        }

    rows = private_manifest_rows(data_dir)
    terms = private_leak_terms(rows)
    issues.extend(validate_bundle_paths(bundle_dir))
    issues.extend(validate_bundle_manifest(bundle_dir))
    issues.extend(validate_generated_markdown_provenance(bundle_dir))
    issues.extend(scan_private_terms(bundle_dir=bundle_dir, leak_terms=terms))
    return {
        "ok": not issues,
        "issue_count": len(issues),
        "issues": [issue.as_dict() for issue in issues],
        "bundle_dir": rel(bundle_dir),
        "data_dir": rel(data_dir),
        "private_rows_loaded": len(rows),
        "private_terms_scanned": len(terms),
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("bundle_dir", nargs="?", type=Path, default=DEFAULT_BUNDLE_DIR)
    parser.add_argument("--data-dir", type=Path, default=DEFAULT_DATA_DIR)
    parser.add_argument("--out", type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    report = audit_public_bundle(bundle_dir=args.bundle_dir, data_dir=args.data_dir)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(f"Wrote {rel(args.out)}")
    print(f"ok={report['ok']} issues={report['issue_count']}")
    for issue in report["issues"]:
        print(f"{issue['code']}: {issue['message']} {issue.get('path', '')}", file=sys.stderr)
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
