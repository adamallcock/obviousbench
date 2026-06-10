"""Config-driven local release asset and snapshot checks."""

from __future__ import annotations

import csv
import glob
import hashlib
import html
import json
import subprocess
import sys
from collections import Counter
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Literal

import yaml

from obviousbench.datasets.item_cards import ItemCard, load_item_cards
from obviousbench.datasets.load import load_benchmark_jsonl
from obviousbench.datasets.schemas import BenchmarkItem

CheckStatus = Literal["pass", "warn", "fail"]

REQUIRED_SNAPSHOT_STATUS_LABELS = (
    "current",
    "stale",
    "exploratory",
    "proofpoint",
    "release_snapshot",
)

EVIDENCE_CHART_FILENAMES = (
    "snapshot-status.svg",
    "evidence-readiness.svg",
    "model-accuracy.svg",
)


@dataclass(frozen=True)
class ReleaseSnapshotInputs:
    config_path: Path
    output_path: Path | None = None
    include_public: bool = False
    generated_on: str = "2026-06-03"


@dataclass(frozen=True)
class ReleaseCheck:
    name: str
    status: CheckStatus
    evidence: str
    next_action: str


@dataclass(frozen=True)
class ReleaseSnapshotResult:
    output_path: Path | None
    checks: tuple[ReleaseCheck, ...]
    config: dict[str, Any]

    @property
    def ok(self) -> bool:
        return all(check.status != "fail" for check in self.checks)

    @property
    def failed_count(self) -> int:
        return sum(check.status == "fail" for check in self.checks)

    @property
    def warning_count(self) -> int:
        return sum(check.status == "warn" for check in self.checks)

    @property
    def passed_count(self) -> int:
        return sum(check.status == "pass" for check in self.checks)

    def check_by_name(self, name: str) -> ReleaseCheck:
        for check in self.checks:
            if check.name == name:
                return check
        raise KeyError(name)


def load_release_config(path: Path) -> dict[str, Any]:
    """Load and minimally validate a release config file."""
    if not path.exists():
        raise FileNotFoundError(path)
    loaded = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(loaded, dict):
        raise ValueError(f"release config must be a mapping: {path}")
    for section in ("release", "snapshot", "generated"):
        if not isinstance(loaded.get(section), dict):
            raise ValueError(f"release config missing mapping section: {section}")
    return loaded


def audit_release_snapshot(inputs: ReleaseSnapshotInputs) -> ReleaseSnapshotResult:
    """Audit the local, non-publishing release snapshot contract."""
    config = load_release_config(inputs.config_path)
    checks: list[ReleaseCheck] = [
        _required_path_check("release config", inputs.config_path),
        *_snapshot_path_checks(config),
        _manifest_count_check(config),
        _comparison_contract_check(config),
        _report_contract_check(config),
        _effort_cost_contract_check(config),
        _stale_reference_check(config),
        _evidence_bundle_contract_check(config),
    ]
    if inputs.include_public:
        checks.append(_public_links_check(config))
    result = ReleaseSnapshotResult(
        output_path=inputs.output_path,
        checks=tuple(checks),
        config=config,
    )
    if inputs.output_path is not None:
        inputs.output_path.parent.mkdir(parents=True, exist_ok=True)
        inputs.output_path.write_text(_render_snapshot_audit(result, inputs), encoding="utf-8")
    return result


def build_local_release_assets(config_path: Path) -> tuple[Path, ...]:
    """Write local release metadata, Makefile include, and draft public surfaces."""
    config = load_release_config(config_path)
    generated = _mapping(config, "generated")
    output_dir = Path(str(generated.get("output_dir", "docs/release/generated")))
    output_dir.mkdir(parents=True, exist_ok=True)

    release_metadata = _release_metadata(config)
    metadata_path = Path(
        str(generated.get("release_metadata", output_dir / "release-metadata.json"))
    )
    metadata_path.parent.mkdir(parents=True, exist_ok=True)
    metadata_path.write_text(
        json.dumps(release_metadata, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    makefile_path = Path(str(generated.get("paper_release_makefile", "paper/release.mk")))
    makefile_path.parent.mkdir(parents=True, exist_ok=True)
    makefile_path.write_text(_paper_release_makefile(config), encoding="utf-8")

    surface_paths = _write_surface_drafts(config)
    evidence_bundle_paths = _write_evidence_bundle(config_path, config)
    provenance_path = Path(str(generated.get("provenance", output_dir / "provenance.json")))
    provenance_path.parent.mkdir(parents=True, exist_ok=True)
    output_paths = [metadata_path, makefile_path, *surface_paths, *evidence_bundle_paths]
    provenance_path.write_text(
        json.dumps(_provenance(config_path, config, output_paths), indent=2, sort_keys=True)
        + "\n",
        encoding="utf-8",
    )

    index_path = Path(str(generated.get("release_index", output_dir / "README.md")))
    index_path.parent.mkdir(parents=True, exist_ok=True)
    all_paths = [
        metadata_path,
        makefile_path,
        *surface_paths,
        *evidence_bundle_paths,
        provenance_path,
    ]
    index_path.write_text(_release_index(config, all_paths), encoding="utf-8")
    return tuple(
        [
            index_path,
            metadata_path,
            makefile_path,
            *surface_paths,
            *evidence_bundle_paths,
            provenance_path,
        ]
    )


def _snapshot_path_checks(config: dict[str, Any]) -> tuple[ReleaseCheck, ...]:
    snapshot = _mapping(config, "snapshot")
    effort = _mapping(config, "effort_cost", required=False)
    generated = _mapping(config, "generated")
    paths = [
        ("snapshot manifest", snapshot.get("manifest")),
        ("snapshot comparison directory", snapshot.get("comparison_dir")),
        ("snapshot report directory", snapshot.get("report_dir")),
        ("paper manifest", snapshot.get("paper_manifest")),
        ("theme config", generated.get("theme_config")),
        ("surfaces config", generated.get("surfaces_config")),
    ]
    if effort:
        paths.extend(
            [
                ("effort cost report directory", effort.get("report_dir")),
                ("effort cost points CSV", effort.get("points_csv")),
                ("effort cost missing points CSV", effort.get("missing_points_csv")),
            ]
        )
    return tuple(_required_path_check(name, value) for name, value in paths)


def _required_path_check(name: str, value: object) -> ReleaseCheck:
    if not isinstance(value, (str, Path)) or not str(value):
        return ReleaseCheck(name, "fail", "path is not configured", "Configure this path.")
    path = Path(value)
    if not path.exists():
        return ReleaseCheck(name, "fail", f"missing: {path}", "Create or regenerate it.")
    if path.is_file() and path.stat().st_size == 0:
        return ReleaseCheck(name, "fail", f"empty file: {path}", "Regenerate it.")
    return ReleaseCheck(name, "pass", f"present: {path}", "None.")


def _manifest_count_check(config: dict[str, Any]) -> ReleaseCheck:
    snapshot = _mapping(config, "snapshot")
    manifest_path = Path(str(snapshot.get("manifest", "")))
    expected = _int(snapshot.get("expected_model_settings"))
    if not manifest_path.exists():
        return ReleaseCheck(
            "manifest row count",
            "fail",
            f"missing: {manifest_path}",
            "Create manifest.",
        )
    rows = _read_csv(manifest_path)
    if len(rows) != expected:
        return ReleaseCheck(
            "manifest row count",
            "fail",
            f"expected {expected} model/settings rows, found {len(rows)}",
            "Regenerate or correct the release manifest.",
        )
    return ReleaseCheck(
        "manifest row count",
        "pass",
        f"{len(rows)} model/settings rows match expected count",
        "None.",
    )


def _comparison_contract_check(config: dict[str, Any]) -> ReleaseCheck:
    snapshot = _mapping(config, "snapshot")
    comparison_path = Path(str(snapshot.get("comparison_dir", ""))) / "comparison.csv"
    expected_rows = _int(snapshot.get("expected_model_settings"))
    expected_samples = _int(snapshot.get("expected_scored_samples"))
    expected_profile = str(snapshot.get("barrage_profile", ""))
    if not comparison_path.exists():
        return ReleaseCheck(
            "comparison contract",
            "fail",
            f"missing: {comparison_path}",
            "Build comparison.",
        )
    rows = _read_csv(comparison_path)
    issues: list[str] = []
    if len(rows) != expected_rows:
        issues.append(f"expected {expected_rows} rows, found {len(rows)}")
    sample_values = sorted({row.get("scored_samples", "") for row in rows})
    if sample_values != [str(expected_samples)]:
        issues.append(f"scored_samples values are {sample_values}, expected {expected_samples}")
    profile_values = sorted({row.get("barrage_profile", "") for row in rows})
    if profile_values != [expected_profile]:
        issues.append(f"barrage_profile values are {profile_values}, expected {expected_profile}")
    if issues:
        return ReleaseCheck(
            "comparison contract",
            "fail",
            "; ".join(issues),
            "Regenerate comparison artifacts from the frozen snapshot.",
        )
    return ReleaseCheck(
        "comparison contract",
        "pass",
        f"{len(rows)} rows, {expected_samples} samples, profile {expected_profile}",
        "None.",
    )


def _report_contract_check(config: dict[str, Any]) -> ReleaseCheck:
    snapshot = _mapping(config, "snapshot")
    report_dir = Path(str(snapshot.get("report_dir", "")))
    expected_rows = _int(snapshot.get("expected_model_settings"))
    expected_samples = _int(snapshot.get("expected_scored_samples"))
    required = (
        "report.html",
        "leaderboard.csv",
        "leaderboard.md",
        "family-heatmap.csv",
        "wrong-answer-review.csv",
        "wrong-answer-review.html",
    )
    missing = [name for name in required if not (report_dir / name).is_file()]
    if missing:
        return ReleaseCheck(
            "report contract",
            "fail",
            "missing: " + ", ".join(str(report_dir / name) for name in missing),
            "Regenerate the static report.",
        )
    leaderboard = _read_csv(report_dir / "leaderboard.csv")
    issues: list[str] = []
    if len(leaderboard) != expected_rows:
        issues.append(f"leaderboard expected {expected_rows} rows, found {len(leaderboard)}")
    sample_values = sorted({row.get("scored_samples", "") for row in leaderboard})
    if sample_values != [str(expected_samples)]:
        issues.append(f"leaderboard scored_samples values are {sample_values}")
    if issues:
        return ReleaseCheck("report contract", "fail", "; ".join(issues), "Regenerate report.")
    return ReleaseCheck(
        "report contract",
        "pass",
        f"report files present; leaderboard has {len(leaderboard)} rows",
        "None.",
    )


def _effort_cost_contract_check(config: dict[str, Any]) -> ReleaseCheck:
    effort = _mapping(config, "effort_cost", required=False)
    if not effort:
        return ReleaseCheck(
            "effort cost contract",
            "warn",
            "effort_cost section absent",
            "Add it if needed.",
        )
    points_path = Path(str(effort.get("points_csv", "")))
    missing_path = Path(str(effort.get("missing_points_csv", "")))
    expected_samples = _int(effort.get("expected_scored_samples"))
    if not points_path.exists() or not missing_path.exists():
        return ReleaseCheck(
            "effort cost contract",
            "fail",
            f"missing points CSV or missing-points CSV under {points_path.parent}",
            "Regenerate effort cost curves.",
        )
    points = _read_csv(points_path)
    missing_rows = _read_csv(missing_path)
    issues: list[str] = []
    if missing_rows:
        issues.append(f"{len(missing_rows)} missing requested effort point(s)")
    sample_values = sorted({row.get("scored_samples", "") for row in points})
    if sample_values != [str(expected_samples)]:
        issues.append(f"point scored_samples values are {sample_values}")
    point_keys = {
        (row.get("model", ""), row.get("effort", ""), row.get("label", "")) for row in points
    }
    for required in effort.get("required_points", []) or []:
        if not isinstance(required, dict):
            issues.append(f"invalid required point: {required!r}")
            continue
        key = (
            str(required.get("model", "")),
            str(required.get("effort", "")),
            str(required.get("label", "")),
        )
        if key not in point_keys:
            issues.append(f"missing required effort point: {key[2]} ({key[0]} {key[1]})")
    if issues:
        return ReleaseCheck(
            "effort cost contract",
            "fail",
            "; ".join(issues),
            "Regenerate or repair effort-cost curve inputs.",
        )
    return ReleaseCheck(
        "effort cost contract",
        "pass",
        f"{len(points)} effort points present; no missing requested points",
        "None.",
    )


def _stale_reference_check(config: dict[str, Any]) -> ReleaseCheck:
    audit = _mapping(config, "audit", required=False)
    if not audit:
        return ReleaseCheck(
            "stale release references",
            "warn",
            "audit section absent",
            "Add stale checks.",
        )
    paths = [Path(str(path)) for path in audit.get("stale_reference_paths", []) or []]
    forbidden = [str(value) for value in audit.get("forbidden_release_strings", []) or []]
    hits: list[str] = []
    for base in paths:
        if not base.exists():
            continue
        files = [base] if base.is_file() else [path for path in base.rglob("*") if path.is_file()]
        for path in files:
            if path.name in {"provenance.json", "release-snapshot-audit.md"}:
                continue
            if path.name == "snapshot-registry.json":
                continue
            if path.suffix in {".pdf", ".png", ".jpg", ".jpeg", ".gz", ".zip"}:
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            for needle in forbidden:
                if needle and needle in text:
                    hits.append(f"{path}: {needle}")
    if hits:
        preview = "; ".join(hits[:8])
        suffix = "" if len(hits) <= 8 else f"; plus {len(hits) - 8} more"
        return ReleaseCheck(
            "stale release references",
            "fail",
            preview + suffix,
            "Regenerate or edit stale release surfaces to the frozen snapshot.",
        )
    return ReleaseCheck(
        "stale release references",
        "pass",
        f"checked {len(paths)} path(s) for {len(forbidden)} forbidden string(s)",
        "None.",
    )


def _public_links_check(config: dict[str, Any]) -> ReleaseCheck:
    links = _mapping(config, "public_links", required=False)
    if not links:
        return ReleaseCheck(
            "public links",
            "fail",
            "public_links section absent",
            "Add public URLs.",
        )
    incomplete: list[str] = []
    for name, payload in links.items():
        if not isinstance(payload, dict):
            incomplete.append(name)
            continue
        value = str(payload.get("value") or "").strip()
        status = str(payload.get("status") or "").strip()
        if not value or status not in {"live", "confirmed"}:
            incomplete.append(name)
    if incomplete:
        return ReleaseCheck(
            "public links",
            "fail",
            "not live/confirmed: " + ", ".join(incomplete),
            "Complete public publishing steps.",
        )
    return ReleaseCheck("public links", "pass", "all public links confirmed", "None.")


def _evidence_bundle_contract_check(config: dict[str, Any]) -> ReleaseCheck:
    bundle = _mapping(config, "evidence_bundle", required=False)
    if not bundle:
        return ReleaseCheck(
            "evidence bundle contract",
            "warn",
            "evidence_bundle section absent",
            "Add snapshot registry, item review matrix, and chart outputs.",
        )

    visibility_issues = _item_review_matrix_visibility_issues(config, bundle)
    if visibility_issues:
        return ReleaseCheck(
            "evidence bundle contract",
            "fail",
            "; ".join(visibility_issues),
            "Keep item review matrix outputs internal-only.",
        )

    required = _evidence_bundle_output_paths(bundle)
    missing = [path for path in required if not path.is_file()]
    if missing:
        return ReleaseCheck(
            "evidence bundle contract",
            "fail",
            "missing: " + ", ".join(str(path) for path in missing),
            "Run scripts/build_release_assets.py to regenerate release evidence.",
        )

    registry_path = Path(str(bundle["snapshot_registry"]))
    matrix_path = Path(str(bundle["item_review_matrix_json"]))
    issues: list[str] = []
    try:
        registry = json.loads(registry_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        issues.append(f"{registry_path} is invalid JSON: {exc}")
        registry = {}
    try:
        matrix = json.loads(matrix_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        issues.append(f"{matrix_path} is invalid JSON: {exc}")
        matrix = {}

    labels = {
        str(artifact.get("status_label", ""))
        for artifact in registry.get("artifacts", [])
        if isinstance(artifact, dict)
    }
    missing_labels = sorted(set(REQUIRED_SNAPSHOT_STATUS_LABELS) - labels)
    if missing_labels:
        issues.append("registry missing status label(s): " + ", ".join(missing_labels))
    registry_missing_paths = [
        str(path_payload.get("path", ""))
        for artifact in registry.get("artifacts", [])
        if isinstance(artifact, dict)
        for path_payload in artifact.get("paths", [])
        if isinstance(path_payload, dict) and not path_payload.get("exists")
    ]
    if registry_missing_paths:
        issues.append("registry references missing path(s): " + ", ".join(registry_missing_paths))
    item_count = _int(_mapping(config, "snapshot").get("item_count"))
    matrix_count = _int((matrix.get("summary") or {}).get("item_count"))
    if matrix_count != item_count:
        issues.append(f"matrix item count {matrix_count} does not match snapshot {item_count}")

    if issues:
        return ReleaseCheck(
            "evidence bundle contract",
            "fail",
            "; ".join(issues),
            "Regenerate or repair release evidence bundle outputs.",
        )
    return ReleaseCheck(
        "evidence bundle contract",
        "pass",
        (
            f"{len(required)} generated evidence files present; "
            f"{len(labels)} status labels; {matrix_count} matrix rows"
        ),
        "None.",
    )


def _evidence_bundle_output_paths(bundle: dict[str, Any]) -> list[Path]:
    paths = [
        Path(str(bundle.get("snapshot_registry", ""))),
        Path(str(bundle.get("item_review_matrix_json", ""))),
        Path(str(bundle.get("item_review_matrix_md", ""))),
        Path(str(bundle.get("evidence_and_claims", ""))),
    ]
    for key in ("release_evidence_json", "external_review_packet"):
        if bundle.get(key):
            paths.append(Path(str(bundle[key])))
    charts_dir = Path(str(bundle.get("charts_dir", "")))
    paths.extend(charts_dir / filename for filename in EVIDENCE_CHART_FILENAMES)
    return paths


def _write_evidence_bundle(config_path: Path, config: dict[str, Any]) -> list[Path]:
    bundle = _mapping(config, "evidence_bundle", required=False)
    if not bundle:
        return []

    registry_path = Path(str(bundle["snapshot_registry"]))
    release_evidence_path = _optional_bundle_path(bundle, "release_evidence_json")
    matrix_json_path = Path(str(bundle["item_review_matrix_json"]))
    matrix_md_path = Path(str(bundle["item_review_matrix_md"]))
    review_packet_path = _optional_bundle_path(bundle, "external_review_packet")
    evidence_doc_path = Path(str(bundle["evidence_and_claims"]))
    charts_dir = Path(str(bundle["charts_dir"]))

    registry = _snapshot_registry_payload(config_path, config)
    registry_path.parent.mkdir(parents=True, exist_ok=True)
    registry_path.write_text(
        json.dumps(registry, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    matrix = _item_review_matrix_payload(config)
    matrix_json_path.parent.mkdir(parents=True, exist_ok=True)
    matrix_json_path.write_text(
        json.dumps(matrix, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    matrix_md_path.parent.mkdir(parents=True, exist_ok=True)
    matrix_md_path.write_text(_item_review_matrix_markdown(matrix, config), encoding="utf-8")

    charts_dir.mkdir(parents=True, exist_ok=True)
    chart_paths = _write_evidence_charts(charts_dir, registry, matrix, config)

    written_paths = [registry_path]
    if release_evidence_path is not None:
        release_evidence_path.parent.mkdir(parents=True, exist_ok=True)
        release_evidence_path.write_text(
            json.dumps(
                _release_evidence_payload(registry, matrix, chart_paths, config),
                indent=2,
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
        )
        written_paths.append(release_evidence_path)
    written_paths.extend([matrix_json_path, matrix_md_path])

    if review_packet_path is not None:
        review_packet_path.parent.mkdir(parents=True, exist_ok=True)
        review_packet_path.write_text(
            _external_review_packet_markdown(registry, matrix, chart_paths, config),
            encoding="utf-8",
        )
        written_paths.append(review_packet_path)

    evidence_doc_path.parent.mkdir(parents=True, exist_ok=True)
    evidence_doc_path.write_text(
        _evidence_and_claims_markdown(registry, matrix, config),
        encoding="utf-8",
    )
    written_paths.append(evidence_doc_path)

    return [*written_paths, *chart_paths]


def _optional_bundle_path(bundle: dict[str, Any], key: str) -> Path | None:
    value = bundle.get(key)
    return Path(str(value)) if value else None


def _item_review_matrix_visibility_issues(
    config: dict[str, Any],
    bundle: dict[str, Any],
) -> list[str]:
    issues: list[str] = []
    matrix_paths: set[str] = set()
    for key in ("item_review_matrix_json", "item_review_matrix_md"):
        path = Path(str(bundle.get(key, "")))
        matrix_paths.add(str(path))
        if "internal" not in path.parts:
            issues.append(f"item review matrix must be under an internal path: {path}")
    surfaces = _load_optional_yaml(Path(str(_mapping(config, "generated").get("surfaces_config"))))
    surface_map = surfaces.get("surfaces", {}) if isinstance(surfaces, dict) else {}
    for name, payload in surface_map.items():
        if not isinstance(payload, dict) or str(payload.get("path", "")) not in matrix_paths:
            continue
        if payload.get("public") is not False:
            issues.append(f"item review matrix surface must be public: false: {name}")
    return issues


def _snapshot_registry_payload(config_path: Path, config: dict[str, Any]) -> dict[str, Any]:
    release = _mapping(config, "release")
    snapshot = _mapping(config, "snapshot")
    bundle = _mapping(config, "evidence_bundle")
    artifacts = []
    for raw_entry in bundle.get("artifact_registry", []) or []:
        if not isinstance(raw_entry, dict):
            continue
        artifact = _artifact_registry_entry(raw_entry, config)
        artifacts.append(artifact)

    label_counts = Counter(str(artifact["status_label"]) for artifact in artifacts)
    missing_labels = sorted(set(REQUIRED_SNAPSHOT_STATUS_LABELS) - set(label_counts))
    return {
        "schema_version": 1,
        "generated_by": "scripts/build_release_assets.py",
        "config_path": str(config_path),
        "release_id": str(release.get("id", "")),
        "release_version": str(release.get("version", "")),
        "release_date": str(release.get("date", "")),
        "snapshot_name": str(snapshot.get("name", "")),
        "dataset_split": str(snapshot.get("dataset_split", "")),
        "item_count": _int(snapshot.get("item_count")),
        "model_setting_count": _int(snapshot.get("expected_model_settings")),
        "scored_samples_per_model_setting": _int(snapshot.get("expected_scored_samples")),
        "barrage_profile": str(snapshot.get("barrage_profile", "")),
        "required_status_labels": list(REQUIRED_SNAPSHOT_STATUS_LABELS),
        "status_label_counts": dict(sorted(label_counts.items())),
        "missing_required_status_labels": missing_labels,
        "artifacts": sorted(artifacts, key=lambda item: (item["status_label"], item["id"])),
    }


def _artifact_registry_entry(raw_entry: dict[str, Any], config: dict[str, Any]) -> dict[str, Any]:
    paths = [_path_evidence(Path(str(path))) for path in raw_entry.get("paths", []) or []]
    present_count = sum(1 for path in paths if path["exists"])
    payload = {
        "id": str(raw_entry.get("id", "")),
        "status_label": str(raw_entry.get("status_label", "")),
        "claim_allowed": str(raw_entry.get("claim_allowed", "")),
        "claim_disallowed": str(raw_entry.get("claim_disallowed", "")),
        "comparability_key": _comparability_key(config),
        "paths": paths,
        "path_count": len(paths),
        "present_path_count": present_count,
        "all_paths_present": present_count == len(paths),
    }
    payload["benchmark_fingerprint"] = _artifact_fingerprint(payload)
    return payload


def _comparability_key(config: dict[str, Any]) -> str:
    snapshot = _mapping(config, "snapshot")
    parts = [
        str(snapshot.get("dataset_split", "")),
        str(snapshot.get("item_count", "")),
        str(snapshot.get("barrage_profile", "")),
        str(snapshot.get("expected_scored_samples", "")),
        str(snapshot.get("expected_model_settings", "")),
    ]
    return "|".join(parts)


def _artifact_fingerprint(payload: dict[str, Any]) -> str:
    digest = hashlib.sha256()
    for key in ("id", "status_label", "claim_allowed", "claim_disallowed", "comparability_key"):
        digest.update(str(payload.get(key, "")).encode("utf-8"))
        digest.update(b"\0")
    for path_payload in payload.get("paths", []):
        digest.update(str(path_payload.get("path", "")).encode("utf-8"))
        digest.update(str(path_payload.get("sha256", "")).encode("utf-8"))
        digest.update(str(path_payload.get("exists", "")).encode("utf-8"))
        digest.update(b"\0")
    return digest.hexdigest()


def _path_evidence(path: Path) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "path": str(path),
        "exists": path.exists(),
        "kind": "missing",
    }
    if path.is_file():
        payload.update(
            {
                "kind": "file",
                "sha256": _sha256(path),
                "bytes": path.stat().st_size,
            }
        )
    elif path.is_dir():
        digest, file_count, byte_count = _directory_sha256(path)
        payload.update(
            {
                "kind": "directory",
                "sha256": digest,
                "file_count": file_count,
                "bytes": byte_count,
            }
        )
    return payload


def _directory_sha256(path: Path) -> tuple[str, int, int]:
    digest = hashlib.sha256()
    file_count = 0
    byte_count = 0
    for child in sorted(candidate for candidate in path.rglob("*") if candidate.is_file()):
        file_count += 1
        byte_count += child.stat().st_size
        digest.update(child.relative_to(path).as_posix().encode("utf-8"))
        digest.update(b"\0")
        with child.open("rb") as handle:
            for chunk in iter(lambda: handle.read(65536), b""):
                digest.update(chunk)
        digest.update(b"\0")
    return digest.hexdigest(), file_count, byte_count


def _item_review_matrix_payload(config: dict[str, Any]) -> dict[str, Any]:
    release = _mapping(config, "release")
    snapshot = _mapping(config, "snapshot")
    bundle = _mapping(config, "evidence_bundle")
    dataset_by_id = _load_release_dataset_items(bundle)
    matrix_source_items = _load_matrix_source_items(bundle)
    dataset_by_id.update({item.id: item for item in matrix_source_items})
    manifest_by_id = _load_paper_manifest_rows(Path(str(snapshot.get("paper_manifest", ""))))
    selected_ids = (
        [item.id for item in matrix_source_items]
        or list(manifest_by_id)
        or sorted(dataset_by_id)
    )
    cards = _load_cards_by_id(Path(str(bundle.get("item_cards_dir", ""))))
    rows = [
        _item_review_row(item_id, dataset_by_id.get(item_id), manifest_by_id.get(item_id), cards)
        for item_id in selected_ids
    ]
    return {
        "schema_version": 1,
        "generated_by": "scripts/build_release_assets.py",
        "release_id": str(release.get("id", "")),
        "snapshot_name": str(snapshot.get("name", "")),
        "dataset_split": str(snapshot.get("dataset_split", "")),
        "summary": _item_review_summary(rows),
        "items": rows,
    }


def _load_release_dataset_items(bundle: dict[str, Any]) -> dict[str, BenchmarkItem]:
    items: dict[str, BenchmarkItem] = {}
    for path in _expand_paths(bundle.get("dataset_files", []) or []):
        for item in load_benchmark_jsonl(path):
            items[item.id] = item
    return items


def _load_matrix_source_items(bundle: dict[str, Any]) -> list[BenchmarkItem]:
    items: list[BenchmarkItem] = []
    item_review_source_files = bundle.get("item_review_source_files", [])
    for path in _expand_paths(item_review_source_files or []):
        items.extend(load_benchmark_jsonl(path))
    return items


def _expand_paths(raw_paths: list[Any]) -> list[Path]:
    paths: list[Path] = []
    for raw_path in raw_paths:
        text = str(raw_path)
        matches = sorted(Path(match) for match in glob.glob(text))
        paths.extend(matches or [Path(text)])
    return paths


def _load_paper_manifest_rows(path: Path) -> dict[str, dict[str, Any]]:
    if not path.exists():
        return {}
    rows: dict[str, dict[str, Any]] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        payload = json.loads(line)
        if isinstance(payload, dict) and payload.get("item_id"):
            rows[str(payload["item_id"])] = payload
    return rows


def _load_cards_by_id(cards_dir: Path) -> dict[str, ItemCard]:
    if not cards_dir.exists():
        return {}
    return load_item_cards(cards_dir).by_item_id


def _item_review_row(
    item_id: str,
    item: BenchmarkItem | None,
    manifest_row: dict[str, Any] | None,
    cards: dict[str, ItemCard],
) -> dict[str, Any]:
    card = cards.get(item_id)
    metadata = item.metadata if item else None
    scorer_contract = card.scorer_contract if card else None
    split_policy = card.split_policy if card else None
    review = card.review if card else None
    family = str(item.family) if item else str((manifest_row or {}).get("family", ""))
    subfamily = item.subfamily if item else str((manifest_row or {}).get("subfamily", ""))
    scorer = str(item.scorer) if item else str((manifest_row or {}).get("scorer", ""))
    answer_type = str(item.answer_type) if item else ""
    strict_format = (
        bool(scorer_contract.strict_format)
        if scorer_contract is not None
        else bool(metadata.strict_format)
        if metadata is not None
        else False
    )
    return {
        "item_id": item_id,
        "family": family,
        "subfamily": subfamily,
        "scorer": str(scorer_contract.scorer) if scorer_contract else scorer,
        "answer_type": str(scorer_contract.answer_type) if scorer_contract else answer_type,
        "human_triviality": (
            str(item.human_triviality)
            if item
            else str((manifest_row or {}).get("human_triviality", ""))
        ),
        "source_type": card.source_type if card else str(item.source_type) if item else "",
        "source_ref_count": len(card.source_refs) if card else len(item.source_refs) if item else 0,
        "dataset_review_status": str(item.review_status) if item else "",
        "card_present": card is not None,
        "card_review_status": review.status if review else "missing",
        "card_reviewer": review.reviewer if review else "",
        "card_reviewed_on": review.reviewed_on if review else "",
        "strict_format": strict_format,
        "publishable": bool(split_policy.publishable) if split_policy else False,
        "leakage_risk": split_policy.leakage_risk if split_policy else "",
        "acceptable_output_count": (
            len(scorer_contract.acceptable_outputs) if scorer_contract is not None else 0
        ),
        "ambiguity_notes": list(card.ambiguity_notes) if card else [],
        "metamorphic_group_id": metadata.metamorphic_group_id if metadata is not None else None,
        "metamorphic_role": metadata.metamorphic_role if metadata is not None else None,
        "selection_rationale": str((manifest_row or {}).get("selection_rationale", "")),
    }


def _item_review_summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "item_count": len(rows),
        "family_counts": _counter_dict(row["family"] for row in rows),
        "source_type_counts": _counter_dict(row["source_type"] for row in rows),
        "scorer_counts": _counter_dict(row["scorer"] for row in rows),
        "review_status_counts": _counter_dict(row["card_review_status"] for row in rows),
        "human_triviality_counts": _counter_dict(row["human_triviality"] for row in rows),
        "leakage_risk_counts": _counter_dict(row["leakage_risk"] for row in rows),
        "strict_format_count": sum(1 for row in rows if row["strict_format"]),
        "publishable_count": sum(1 for row in rows if row["publishable"]),
        "card_present_count": sum(1 for row in rows if row["card_present"]),
        "missing_card_count": sum(1 for row in rows if not row["card_present"]),
        "metamorphic_item_count": sum(1 for row in rows if row["metamorphic_group_id"]),
    }


def _counter_dict(values: Any) -> dict[str, int]:
    return dict(sorted(Counter(str(value) for value in values if str(value)).items()))


def _item_review_matrix_markdown(matrix: dict[str, Any], config: dict[str, Any]) -> str:
    snapshot = _mapping(config, "snapshot")
    summary = matrix["summary"]
    lines = _generated_header("configs/release_v0_1_0.yaml") + [
        "# ObviousBench Item Review Matrix",
        "",
        (
            f"Snapshot `{snapshot['name']}` item review summary: "
            f"{summary['item_count']} items; "
            f"strict format items: {summary['strict_format_count']}; "
            f"missing item cards: {summary['missing_card_count']}."
        ),
        "",
        "## Family Counts",
        "",
        _inline_counts(summary["family_counts"]),
        "",
        "## Item Matrix",
        "",
        "| Item | Family | Subfamily | Scorer | Source | Review | Strict | Publishable |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in matrix["items"]:
        lines.append(
            "| "
            + " | ".join(
                _md_cell(value)
                for value in (
                    row["item_id"],
                    row["family"],
                    row["subfamily"],
                    row["scorer"],
                    row["source_type"],
                    row["card_review_status"],
                    "yes" if row["strict_format"] else "no",
                    "yes" if row["publishable"] else "no",
                )
            )
            + " |"
        )
    lines.append("")
    return "\n".join(lines)


def _inline_counts(counts: dict[str, int]) -> str:
    if not counts:
        return "None."
    return ", ".join(f"`{key}`: {value}" for key, value in counts.items())


def _write_evidence_charts(
    charts_dir: Path,
    registry: dict[str, Any],
    matrix: dict[str, Any],
    config: dict[str, Any],
) -> list[Path]:
    paths = [
        charts_dir / "snapshot-status.svg",
        charts_dir / "evidence-readiness.svg",
        charts_dir / "model-accuracy.svg",
    ]
    paths[0].write_text(_snapshot_status_svg(registry), encoding="utf-8")
    paths[1].write_text(_evidence_readiness_svg(registry, matrix, config), encoding="utf-8")
    paths[2].write_text(_model_accuracy_svg(config), encoding="utf-8")
    return paths


def _snapshot_status_svg(registry: dict[str, Any]) -> str:
    counts = registry.get("status_label_counts", {})
    bars = [
        (label.replace("_", " "), float(counts.get(label, 0)))
        for label in REQUIRED_SNAPSHOT_STATUS_LABELS
    ]
    return _bar_chart_svg(
        title="Snapshot artifact status",
        subtitle="Machine-readable registry labels for public release artifacts",
        bars=bars,
        unit="artifact",
        footnote="Generated from snapshot-registry.json.",
    )


def _evidence_readiness_svg(
    registry: dict[str, Any],
    matrix: dict[str, Any],
    config: dict[str, Any],
) -> str:
    snapshot = _mapping(config, "snapshot")
    registry_paths = [
        path
        for artifact in registry.get("artifacts", [])
        if isinstance(artifact, dict)
        for path in artifact.get("paths", [])
        if isinstance(path, dict)
    ]
    present_paths = sum(1 for path in registry_paths if path.get("exists"))
    matrix_summary = matrix.get("summary", {})
    item_count = max(1, _int(matrix_summary.get("item_count")))
    comparison_rows = _read_csv(Path(str(snapshot.get("comparison_dir", ""))) / "comparison.csv")
    complete_rows = sum(
        1
        for row in comparison_rows
        if row.get("scored_samples") == str(snapshot.get("expected_scored_samples"))
    )
    expected_rows = max(1, _int(snapshot.get("expected_model_settings")))
    bars = [
        ("registry paths present", _percent(present_paths, len(registry_paths))),
        (
            "item cards present",
            _percent(_int(matrix_summary.get("card_present_count")), item_count),
        ),
        (
            "items reviewed",
            _percent(
                _int(matrix_summary.get("review_status_counts", {}).get("reviewed")),
                item_count,
            ),
        ),
        ("items publishable", _percent(_int(matrix_summary.get("publishable_count")), item_count)),
        ("model rows complete", _percent(complete_rows, expected_rows)),
    ]
    return _bar_chart_svg(
        title="Evidence readiness",
        subtitle="Release evidence coverage checks derived from the frozen snapshot",
        bars=bars,
        unit="percent",
        footnote="Generated from snapshot registry, item review matrix, and comparison CSV.",
        x_max=100.0,
    )


def _model_accuracy_svg(config: dict[str, Any]) -> str:
    snapshot = _mapping(config, "snapshot")
    rows = _model_accuracy_points(snapshot)
    bars: list[tuple[str, float]] = []
    for row in rows[:8]:
        bars.append((f"{row['label']} answer", row["answer"]))
        bars.append((f"{row['label']} strict", row["strict"]))
    return _bar_chart_svg(
        title="Model answer vs strict accuracy",
        subtitle="Top model/settings rows in the frozen release report",
        bars=bars,
        unit="percent",
        footnote="Generated from leaderboard.csv or comparison.csv.",
        x_max=100.0,
        width=1040,
    )


def _model_accuracy_points(snapshot: dict[str, Any]) -> list[dict[str, Any]]:
    leaderboard_path = Path(str(snapshot.get("report_dir", ""))) / "leaderboard.csv"
    comparison_path = Path(str(snapshot.get("comparison_dir", ""))) / "comparison.csv"
    rows = _read_csv(leaderboard_path) if leaderboard_path.exists() else _read_csv(comparison_path)
    points: list[dict[str, Any]] = []
    for row in rows:
        label = row.get("display_label") or row.get("label") or row.get("model") or "model"
        answer = _accuracy_percent(row, "answer_accuracy_pct", "answer_accuracy")
        strict = _accuracy_percent(row, "strict_accuracy_pct", "strict_accuracy")
        if answer is None:
            continue
        points.append(
            {
                "label": _short_label(label),
                "answer": answer,
                "strict": strict if strict is not None else answer,
            }
        )
    return sorted(points, key=lambda row: (-row["answer"], -row["strict"], row["label"]))


def _accuracy_percent(row: dict[str, str], pct_key: str, fraction_key: str) -> float | None:
    raw_pct = str(row.get(pct_key, "")).strip().rstrip("%")
    if raw_pct:
        return _float_or_none(raw_pct)
    raw_fraction = str(row.get(fraction_key, "")).strip()
    value = _float_or_none(raw_fraction)
    if value is None:
        return None
    return value * 100 if value <= 1.0 else value


def _float_or_none(value: str) -> float | None:
    try:
        return float(value)
    except ValueError:
        return None


def _short_label(label: str, *, max_chars: int = 44) -> str:
    compact = " ".join(label.split())
    return compact if len(compact) <= max_chars else compact[: max_chars - 1] + "..."


def _bar_chart_svg(
    *,
    title: str,
    subtitle: str,
    bars: list[tuple[str, float]],
    unit: str,
    footnote: str,
    x_max: float | None = None,
    width: int = 960,
) -> str:
    bars = bars or [("no data", 0.0)]
    max_value = x_max if x_max is not None else max(value for _, value in bars) or 1.0
    left = 260
    right = 120
    top = 82
    row_height = 30
    height = top + row_height * len(bars) + 66
    chart_width = width - left - right
    parts = [
        (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
            f'viewBox="0 0 {width} {height}" role="img" '
            f'aria-labelledby="{_svg_id(title)}-title {_svg_id(title)}-desc">'
        ),
        f'<title id="{_svg_id(title)}-title">{_svg_text(title)}</title>',
        (
            f'<desc id="{_svg_id(title)}-desc">{_svg_text(subtitle)}. '
            "Generated from source release artifacts.</desc>"
        ),
        '<rect width="100%" height="100%" fill="#fbfaf7" />',
        (
            '<text x="24" y="34" font-size="22" font-weight="700" fill="#1f2023">'
            f"{_svg_text(title)}</text>"
        ),
        f'<text x="24" y="58" font-size="13" fill="#5f6368">{_svg_text(subtitle)}</text>',
    ]
    for index, (label, value) in enumerate(bars):
        y = top + index * row_height
        bar_width = (
            0 if max_value <= 0 else chart_width * max(0.0, min(value, max_value)) / max_value
        )
        color = "#216db4" if index % 2 == 0 else "#d77250"
        value_text = f"{value:.1f}%" if unit == "percent" else f"{value:.0f}"
        if unit == "artifact":
            value_text = f"{value:.0f}"
        parts.extend(
            [
                (
                    f'<text x="24" y="{y + 19}" font-size="12" fill="#344054">'
                    f"{_svg_text(label)}</text>"
                ),
                (
                    f'<rect x="{left}" y="{y + 4}" width="{chart_width}" '
                    'height="18" fill="#ebe5db" />'
                ),
                (
                    f'<rect x="{left}" y="{y + 4}" width="{bar_width:.2f}" '
                    f'height="18" fill="{color}" />'
                ),
                (
                    f'<text x="{left + chart_width + 12}" y="{y + 19}" '
                    f'font-size="12" fill="#344054">{value_text}</text>'
                ),
            ]
        )
    parts.extend(
        [
            (
                f'<text x="24" y="{height - 24}" font-size="12" fill="#5f6368">'
                f"Generated from {_svg_text(footnote)}</text>"
            ),
            "</svg>",
        ]
    )
    return "\n".join(parts)


def _svg_id(value: str) -> str:
    return "".join(char.lower() if char.isalnum() else "-" for char in value).strip("-")


def _svg_text(value: object) -> str:
    return html.escape(str(value), quote=True)


def _percent(value: int, total: int) -> float:
    return 0.0 if total <= 0 else 100.0 * value / total


def _release_evidence_payload(
    registry: dict[str, Any],
    matrix: dict[str, Any],
    chart_paths: list[Path],
    config: dict[str, Any],
) -> dict[str, Any]:
    release = _mapping(config, "release")
    snapshot = _mapping(config, "snapshot")
    bundle = _mapping(config, "evidence_bundle")
    return {
        "schema_version": 1,
        "generated_by": "scripts/build_release_assets.py",
        "release": {
            "id": str(release.get("id", "")),
            "version": str(release.get("version", "")),
            "tag": str(release.get("tag", "")),
            "date": str(release.get("date", "")),
        },
        "snapshot": {
            "name": str(snapshot.get("name", "")),
            "dataset_split": str(snapshot.get("dataset_split", "")),
            "item_count": _int(snapshot.get("item_count")),
            "model_setting_count": _int(snapshot.get("expected_model_settings")),
            "scored_samples_per_model_setting": _int(
                snapshot.get("expected_scored_samples")
            ),
            "barrage_profile": str(snapshot.get("barrage_profile", "")),
        },
        "registry": {
            "path": str(bundle.get("snapshot_registry", "")),
            "required_status_labels": registry.get("required_status_labels", []),
            "status_label_counts": registry.get("status_label_counts", {}),
            "missing_required_status_labels": registry.get(
                "missing_required_status_labels", []
            ),
        },
        "item_review_matrix": {
            "path": str(bundle.get("item_review_matrix_json", "")),
            "visibility": "internal-only",
            **matrix.get("summary", {}),
        },
        "charts": [str(path) for path in chart_paths],
        "documents": {
            "evidence_and_claims": str(bundle.get("evidence_and_claims", "")),
            "external_review_packet": str(bundle.get("external_review_packet", "")),
        },
        "claim_limits": config.get("claim_limits", {}),
    }


def _external_review_packet_markdown(
    registry: dict[str, Any],
    matrix: dict[str, Any],
    chart_paths: list[Path],
    config: dict[str, Any],
) -> str:
    release = _mapping(config, "release")
    snapshot = _mapping(config, "snapshot")
    bundle = _mapping(config, "evidence_bundle", required=False)
    snapshot_registry = str(
        bundle.get(
            "snapshot_registry",
            "docs/internal/release/generated/snapshot-registry.json",
        )
    )
    item_review_matrix = str(
        bundle.get(
            "item_review_matrix_md",
            "docs/internal/release/generated/item-review-matrix.md",
        )
    )
    release_evidence = str(
        bundle.get(
            "release_evidence_json",
            "docs/internal/release/generated/release-evidence.json",
        )
    )
    lines = [
        "---",
        "title: ObviousBench External Review Packet",
        f"date: {release.get('date', '2026-06-03')}",
        "type: review",
        "status: generated",
        "---",
        "",
        *_generated_header("configs/release_v0_1_0.yaml"),
        "# ObviousBench External Review Packet",
        "",
        (
            f"This packet orients reviewers to snapshot `{snapshot['name']}` "
            f"({snapshot['item_count']} items, "
            f"{snapshot['expected_model_settings']} model/settings rows)."
        ),
        "",
        "## Review Materials",
        "",
        "- Evidence and claims doc: `docs/evidence-and-claims.md`",
        f"- Snapshot registry: `{snapshot_registry}`",
        f"- Item review matrix: `{item_review_matrix}`",
        f"- Release evidence JSON: `{release_evidence}`",
        *[f"- Chart: `{path}`" for path in chart_paths],
        "",
        "## Reviewer Questions",
        "",
        "- Are the `current`, `stale`, `exploratory`, `proofpoint`, and "
        "`release_snapshot` labels understandable without private context?",
        "- Does the item review matrix expose enough scorer, source, review, "
        "ambiguity, and split-policy information to audit the benchmark items?",
        "- Do the allowed and disallowed claims prevent confusing proofpoint or "
        "stale artifacts with the frozen release snapshot?",
        "- Are any draft item-card rows unacceptable for the public release claim?",
        "",
        "## Artifact Registry",
        "",
        "| Artifact | Label | Allowed | Disallowed |",
        "| --- | --- | --- | --- |",
    ]
    for artifact in registry["artifacts"]:
        lines.append(
            "| "
            + " | ".join(
                _md_cell(value)
                for value in (
                    f"`{artifact['id']}`",
                    artifact["status_label"],
                    artifact["claim_allowed"],
                    artifact["claim_disallowed"],
                )
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Item Review Summary",
            "",
            f"- Items: {matrix['summary']['item_count']}",
            (
                "- Reviewed item cards: "
                f"{matrix['summary']['review_status_counts'].get('reviewed', 0)}"
            ),
            f"- Draft item cards: {matrix['summary']['review_status_counts'].get('draft', 0)}",
            f"- Missing item cards: {matrix['summary']['missing_card_count']}",
            f"- Strict-format items: {matrix['summary']['strict_format_count']}",
            "",
        ]
    )
    return "\n".join(lines)


def _evidence_and_claims_markdown(
    registry: dict[str, Any],
    matrix: dict[str, Any],
    config: dict[str, Any],
) -> str:
    release = _mapping(config, "release")
    snapshot = _mapping(config, "snapshot")
    claim_limits = _mapping(config, "claim_limits", required=False)
    lines = [
        "---",
        "title: ObviousBench Evidence And Claims",
        f"date: {release.get('date', '2026-06-03')}",
        "type: reference",
        "status: generated",
        "---",
        "",
        *_generated_header("configs/release_v0_1_0.yaml"),
        "# ObviousBench Evidence And Claims",
        "",
        str(claim_limits.get("summary", "")),
        "",
        "## Canonical Evidence",
        "",
        f"- Static report: `{snapshot['report_dir']}/report.html`",
        f"- Leaderboard CSV: `{snapshot['report_dir']}/leaderboard.csv`",
        "- Release config: `configs/release_v0_1_0.yaml`",
        "",
        (
            "Internal release-governance artifacts are generated under `docs/internal/` "
            "and are not public release surfaces."
        ),
        "",
        "## Allowed Claims",
        "",
        "| Artifact | Label | Allowed | Disallowed | Fingerprint |",
        "| --- | --- | --- | --- | --- |",
    ]
    for artifact in registry["artifacts"]:
        lines.append(
            "| "
            + " | ".join(
                _md_cell(value)
                for value in (
                    f"`{artifact['id']}`",
                    artifact["status_label"],
                    artifact["claim_allowed"],
                    artifact["claim_disallowed"],
                    artifact["benchmark_fingerprint"][:12],
                )
            )
            + " |"
        )
    caveats = [str(value) for value in claim_limits.get("caveats", []) or []]
    lines.extend(
        [
            "",
            "## Claim Boundaries",
            "",
            *(f"- {caveat}" for caveat in caveats),
            "",
        ]
    )
    return "\n".join(lines)


def _render_snapshot_audit(
    result: ReleaseSnapshotResult,
    inputs: ReleaseSnapshotInputs,
) -> str:
    status = "PASS" if result.ok else "BLOCKED"
    lines = [
        "---",
        "title: ObviousBench Release Snapshot Audit",
        f"date: {inputs.generated_on}",
        "type: audit",
        f"status: {'pass' if result.ok else 'blocked'}",
        "---",
        "",
        "# ObviousBench Release Snapshot Audit",
        "",
        f"Config: `{inputs.config_path}`",
        f"Overall status: {status}",
        "",
        f"Passed: {result.passed_count}",
        f"Warnings: {result.warning_count}",
        f"Failures: {result.failed_count}",
        "",
        "| Check | Status | Evidence | Next action |",
        "| --- | --- | --- | --- |",
    ]
    for check in result.checks:
        lines.append(
            "| "
            + " | ".join(
                _md_cell(value)
                for value in (
                    check.name,
                    check.status.upper(),
                    check.evidence,
                    check.next_action,
                )
            )
            + " |"
        )
    lines.append("")
    return "\n".join(lines)


def _release_metadata(config: dict[str, Any]) -> dict[str, Any]:
    snapshot = _mapping(config, "snapshot")
    release = _mapping(config, "release")
    return {
        "release": release,
        "snapshot": snapshot,
        "authors": config.get("authors", []),
        "licenses": config.get("licenses", {}),
        "claim_limits": config.get("claim_limits", {}),
        "public_links": config.get("public_links", {}),
    }


def _paper_release_makefile(config: dict[str, Any]) -> str:
    snapshot = _mapping(config, "snapshot")
    return "\n".join(
        [
            "# Generated by scripts/build_release_assets.py. Do not hand-edit.",
            "RELEASE_CONFIG := configs/release_v0_1_0.yaml",
            f"EVIDENCE_MANIFEST := {snapshot['manifest']}",
            f"EVIDENCE_COMPARISON_DIR := {snapshot['comparison_dir']}",
            f"EVIDENCE_REPORT_DIR := {snapshot['report_dir']}",
            f"EVIDENCE_WRONG_REVIEW := {snapshot['wrong_answer_review']}",
            f"EVIDENCE_EXPECTED_MODELS := {snapshot['expected_model_settings']}",
            "",
        ]
    )


def _write_surface_drafts(config: dict[str, Any]) -> list[Path]:
    surfaces_config = _load_optional_yaml(
        Path(str(_mapping(config, "generated").get("surfaces_config")))
    )
    surfaces = surfaces_config.get("surfaces", {}) if isinstance(surfaces_config, dict) else {}
    writers = {
        "github_release_notes": _github_release_notes,
        "dataset_card": _dataset_card,
        "project_page_draft": _project_page_draft,
        "launch_essay_draft": _launch_essay_draft,
        "social_snippets": _social_snippets,
        "arxiv_metadata_draft": _arxiv_metadata_draft,
        "citation_cff": _citation_cff,
        "zenodo_metadata": _zenodo_metadata,
    }
    written: list[Path] = []
    for key, writer in writers.items():
        payload = surfaces.get(key, {})
        if not isinstance(payload, dict) or not payload.get("path"):
            continue
        path = Path(str(payload["path"]))
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(writer(config), encoding="utf-8")
        written.append(path)
    return written


def _generated_header(source: str) -> list[str]:
    return [
        "<!-- Generated by scripts/build_release_assets.py. Do not hand-edit. -->",
        f"<!-- Source: {source} -->",
        "",
    ]


def _github_release_notes(config: dict[str, Any]) -> str:
    release = _mapping(config, "release")
    snapshot = _mapping(config, "snapshot")
    caveats = _caveat_lines(config)
    lines = _generated_header("configs/release_v0_1_0.yaml") + [
        f"# {release['tag']}",
        "",
        f"{release['title']}",
        "",
        "## Snapshot",
        "",
        f"- Dataset split: `{snapshot['dataset_split']}`",
        f"- Questions: {snapshot['item_count']}",
        f"- Model/settings rows: {snapshot['expected_model_settings']}",
        f"- Scored samples per row: {snapshot['expected_scored_samples']}",
        f"- Static report: `{snapshot['report_dir']}`",
        "",
        "## Caveats",
        "",
        *caveats,
        "",
        "## Local Verification",
        "",
        "- Run `make release-check` before publishing this release.",
        "",
    ]
    return "\n".join(lines)


def _dataset_card(config: dict[str, Any]) -> str:
    release = _mapping(config, "release")
    snapshot = _mapping(config, "snapshot")
    caveats = _caveat_lines(config)
    lines = _generated_header("configs/release_v0_1_0.yaml") + [
        "---",
        "license: cc-by-4.0",
        "task_categories:",
        "  - text-generation",
        "tags:",
        "  - benchmark",
        "  - evaluation",
        "  - llm",
        "pretty_name: ObviousBench",
        "---",
        "",
        f"# {release['short_name']} Dataset Card",
        "",
        "This card is a draft generated for the v0.1 release package.",
        "",
        "## Snapshot",
        "",
        f"- Split: `{snapshot['dataset_split']}`",
        f"- Questions: {snapshot['item_count']}",
        f"- Model/settings rows in the paper snapshot: {snapshot['expected_model_settings']}",
        "",
        "## Intended Use",
        "",
        "Use this dataset to inspect a frozen obvious-question benchmark snapshot,",
        "scoring policy, and static model/settings results.",
        "",
        "## Limitations",
        "",
        *caveats,
        "",
    ]
    return "\n".join(lines)


def _project_page_draft(config: dict[str, Any]) -> str:
    release = _mapping(config, "release")
    snapshot = _mapping(config, "snapshot")
    return "\n".join(
        _generated_header("configs/release_v0_1_0.yaml")
        + [
            f"# {release['short_name']}",
            "",
            str(_mapping(config, "claim_limits").get("summary", "")),
            "",
            "## Explore",
            "",
            f"- Static report: `{snapshot['report_dir']}/report.html`",
            f"- Leaderboard CSV: `{snapshot['report_dir']}/leaderboard.csv`",
            "- Effort/cost curves: `docs/reports/2026-06-02-effort-cost-curves/index.html`",
            "",
            "## Citation",
            "",
            "Use `CITATION.cff` after public release metadata is confirmed.",
            "",
        ]
    )


def _launch_essay_draft(config: dict[str, Any]) -> str:
    release = _mapping(config, "release")
    caveats = _caveat_lines(config)
    return "\n".join(
        _generated_header("configs/release_v0_1_0.yaml")
        + [
            f"# Launch Draft: {release['title']}",
            "",
            "ObviousBench v0.1 is a frozen benchmark snapshot for questions that",
            "should be easy but still expose brittle behavior in model settings.",
            "",
            "The launch should point readers to the canonical project page, static",
            "report, dataset card, GitHub release, DOI, and arXiv paper once live.",
            "",
            "## Caveats",
            "",
            *caveats,
            "",
        ]
    )


def _social_snippets(config: dict[str, Any]) -> str:
    release = _mapping(config, "release")
    snapshot = _mapping(config, "snapshot")
    return "\n".join(
        _generated_header("configs/release_v0_1_0.yaml")
        + [
            "# Social Snippets",
            "",
            "## Short",
            "",
            (
                f"{release['short_name']} v0.1 is a frozen {snapshot['item_count']}-question "
                f"benchmark snapshot across {snapshot['expected_model_settings']} "
                "model/settings rows. Static results, data, and reproducibility "
                "artifacts are prepared for release."
            ),
            "",
            "## Caveat",
            "",
            "Snapshot scores are dated artifacts, not permanent model-family rankings.",
            "",
        ]
    )


def _arxiv_metadata_draft(config: dict[str, Any]) -> str:
    release = _mapping(config, "release")
    snapshot = _mapping(config, "snapshot")
    return "\n".join(
        _generated_header("configs/release_v0_1_0.yaml")
        + [
            f"# arXiv Metadata Draft: {release['title']}",
            "",
            f"Title: {release['title']}",
            "",
            "Abstract seed:",
            "",
            (
                f"ObviousBench is a benchmark for short prompts that should be "
                f"easy for careful humans but still expose visible failures in "
                f"language-model settings. The v0.1 `{snapshot['dataset_split']}` "
                f"snapshot contains {snapshot['item_count']} questions and reports "
                f"{snapshot['expected_model_settings']} model/settings rows."
            ),
            "",
            "Public URLs must be regenerated into this draft after artifact publishing.",
            "",
        ]
    )


def _citation_cff(config: dict[str, Any]) -> str:
    release = _mapping(config, "release")
    links = _mapping(config, "public_links", required=False)
    licenses = _mapping(config, "licenses", required=False)
    authors = _authors(config)
    lines = [
        "# Generated by scripts/build_release_assets.py. Do not hand-edit.",
        "cff-version: 1.2.0",
        'message: "If you use ObviousBench, please cite the paper and archived release."',
        f'title: "{release["title"]}"',
        f'version: "{release["version"]}"',
        f'date-released: "{release["date"]}"',
        "authors:",
    ]
    for author in authors:
        lines.extend(
            [
                f'  - family-names: "{author["family_names"]}"',
                f'    given-names: "{author["given_names"]}"',
            ]
        )
    repository_url = _public_link_value(links, "repository_url")
    dataset_url = _public_link_value(links, "dataset_url")
    if repository_url:
        lines.append(f'repository-code: "{repository_url}"')
    if dataset_url:
        lines.append(f'url: "{dataset_url}"')
    lines.extend(
        [
            f'license: "{licenses.get("code", "Apache-2.0")}"',
            "abstract: >-",
            "  ObviousBench is a compact benchmark for short prompts that should be easy for",
            "  a careful human but still produce visible failures in public-facing language",
            "  models.",
            "keywords:",
            "  - language-model-evaluation",
            "  - benchmark",
            "  - reliability",
            "  - arxiv",
            "",
        ]
    )
    return "\n".join(lines)


def _zenodo_metadata(config: dict[str, Any]) -> str:
    release = _mapping(config, "release")
    links = _mapping(config, "public_links", required=False)
    licenses = _mapping(config, "licenses", required=False)
    related_identifiers = []
    repository_url = _public_link_value(links, "repository_url")
    dataset_url = _public_link_value(links, "dataset_url")
    if repository_url:
        related_identifiers.append(
            {
                "identifier": repository_url,
                "relation": "isSupplementTo",
                "resource_type": "software",
            }
        )
    if dataset_url:
        related_identifiers.append(
            {
                "identifier": dataset_url,
                "relation": "isSupplementedBy",
                "resource_type": "dataset",
            }
        )
    payload = {
        "title": release["title"],
        "upload_type": "software",
        "description": (
            "A compact benchmark for short prompts that should be easy for a careful "
            "human but still produce visible failures in public-facing language models."
        ),
        "creators": [
            {
                "name": author["name"],
                "affiliation": author.get("affiliation", ""),
            }
            for author in _authors(config)
        ],
        "license": licenses.get("code", "Apache-2.0"),
        "keywords": [
            "language-model-evaluation",
            "benchmark",
            "reliability",
        ],
        "related_identifiers": related_identifiers,
    }
    return json.dumps(payload, indent=2, sort_keys=False) + "\n"


def _release_index(config: dict[str, Any], paths: list[Path]) -> str:
    release = _mapping(config, "release")
    snapshot = _mapping(config, "snapshot")
    rows = [
        "| Path | SHA256 |",
        "| --- | --- |",
    ]
    for path in paths:
        rows.append(f"| `{path}` | `{_sha256(path)}` |")
    return "\n".join(
        _generated_header("configs/release_v0_1_0.yaml")
        + [
            f"# {release['short_name']} Local Release Assets",
            "",
            f"Release tag: `{release['tag']}`",
            f"Snapshot: `{snapshot['name']}`",
            f"Questions: {snapshot['item_count']}",
            f"Model/settings rows: {snapshot['expected_model_settings']}",
            "",
            "These files are generated local release-prep artifacts. Publishing",
            "steps still require live public URL confirmation.",
            "",
            "## Generated Files",
            "",
            *rows,
            "",
        ]
    )


def _provenance(
    config_path: Path, config: dict[str, Any], output_paths: list[Path]
) -> dict[str, Any]:
    return {
        "generated_at": datetime.now(tz=UTC).isoformat(),
        "generator": "scripts/build_release_assets.py",
        "config_path": str(config_path),
        "config_sha256": _sha256(config_path),
        "git": _git_state(),
        "python_environment": _python_environment(),
        "inputs": _provenance_inputs(config_path, config),
        "outputs": [
            {
                "path": str(path),
                "sha256": _sha256(path),
                "bytes": path.stat().st_size,
            }
            for path in output_paths
            if path.exists()
        ],
    }


def _provenance_inputs(config_path: Path, config: dict[str, Any]) -> list[dict[str, Any]]:
    generated = _mapping(config, "generated")
    snapshot = _mapping(config, "snapshot")
    effort = _mapping(config, "effort_cost", required=False)
    bundle = _mapping(config, "evidence_bundle", required=False)
    candidates: list[tuple[str, object]] = [
        ("release config", config_path),
        ("theme config", generated.get("theme_config")),
        ("surfaces config", generated.get("surfaces_config")),
        ("snapshot manifest", snapshot.get("manifest")),
        ("comparison CSV", Path(str(snapshot.get("comparison_dir", ""))) / "comparison.csv"),
        ("report HTML", Path(str(snapshot.get("report_dir", ""))) / "report.html"),
        ("leaderboard CSV", Path(str(snapshot.get("report_dir", ""))) / "leaderboard.csv"),
        ("family heatmap CSV", Path(str(snapshot.get("report_dir", ""))) / "family-heatmap.csv"),
        ("wrong-answer review", snapshot.get("wrong_answer_review")),
        ("paper manifest", snapshot.get("paper_manifest")),
        ("human baseline", snapshot.get("human_baseline")),
    ]
    if effort:
        candidates.extend(
            [
                ("effort cost points", effort.get("points_csv")),
                ("effort cost missing points", effort.get("missing_points_csv")),
            ]
        )
    if bundle:
        candidates.append(("item cards directory", bundle.get("item_cards_dir")))
        candidates.extend(
            ("release dataset file", path)
            for path in _expand_paths(bundle.get("dataset_files", []) or [])
        )
        item_review_source_files = bundle.get("item_review_source_files", [])
        candidates.extend(
            ("item review source file", path)
            for path in _expand_paths(item_review_source_files or [])
        )

    inputs: list[dict[str, Any]] = []
    seen: set[tuple[str, str]] = set()
    for role, raw_path in candidates:
        if raw_path in {None, ""}:
            continue
        path = Path(str(raw_path))
        key = str(path)
        seen_key = (role, key)
        if seen_key in seen:
            continue
        seen.add(seen_key)
        payload: dict[str, Any] = {
            "role": role,
            "path": key,
            "exists": path.exists(),
        }
        if path.is_file():
            payload["sha256"] = _sha256(path)
            payload["bytes"] = path.stat().st_size
        elif path.is_dir():
            digest, file_count, byte_count = _directory_sha256(path)
            payload["sha256"] = digest
            payload["file_count"] = file_count
            payload["bytes"] = byte_count
        inputs.append(payload)
    return inputs


def _python_environment() -> dict[str, Any]:
    dependency_candidates = [
        Path("pyproject.toml"),
        Path("uv.lock"),
        Path("poetry.lock"),
        *sorted(Path(".").glob("requirements*.txt")),
        *sorted(Path(".").glob("requirements*.in")),
    ]
    dependency_files = [
        {
            "path": str(path),
            "sha256": _sha256(path),
            "bytes": path.stat().st_size,
        }
        for path in dependency_candidates
        if path.is_file()
    ]
    lockfiles = [
        payload
        for payload in dependency_files
        if Path(str(payload["path"])).name in {"uv.lock", "poetry.lock"}
    ]
    return {
        "python_version": sys.version.split()[0],
        "dependency_files": dependency_files,
        "lockfiles_present": bool(lockfiles),
    }


def _git_state() -> dict[str, str]:
    def run(args: list[str]) -> str:
        try:
            result = subprocess.run(args, text=True, capture_output=True, check=False)
        except OSError:
            return ""
        return result.stdout.strip()

    status_lines = [
        line for line in run(["git", "status", "--short"]).splitlines() if line.strip()
    ]
    return {
        "commit": run(["git", "rev-parse", "HEAD"]),
        "dirty": "true" if status_lines else "false",
        "status_entry_count": str(len(status_lines)),
    }


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _load_optional_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    loaded = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return loaded if isinstance(loaded, dict) else {}


def _mapping(config: dict[str, Any], section: str, *, required: bool = True) -> dict[str, Any]:
    value = config.get(section)
    if not isinstance(value, dict):
        if required:
            raise ValueError(f"release config missing mapping section: {section}")
        return {}
    return value


def _int(value: object) -> int:
    if value in {None, ""}:
        return 0
    return int(value)


def _caveat_lines(config: dict[str, Any]) -> list[str]:
    claim_limits = _mapping(config, "claim_limits", required=False)
    caveats = claim_limits.get("caveats", []) if claim_limits else []
    return [f"- {value}" for value in caveats]


def _authors(config: dict[str, Any]) -> list[dict[str, str]]:
    authors = config.get("authors")
    if not isinstance(authors, list) or not authors:
        return [
            {
                "family_names": "Allcock",
                "given_names": "Adam",
                "name": "Allcock, Adam",
                "affiliation": "Independent Researcher",
            }
        ]
    return [
        {
            "family_names": str(author.get("family_names", "")),
            "given_names": str(author.get("given_names", "")),
            "name": str(author.get("name", "")),
            "affiliation": str(author.get("affiliation", "")),
        }
        for author in authors
        if isinstance(author, dict)
    ]


def _public_link_value(links: dict[str, Any], key: str) -> str:
    payload = links.get(key)
    if not isinstance(payload, dict):
        return ""
    return str(payload.get("value") or "").strip()


def _md_cell(value: str) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")
