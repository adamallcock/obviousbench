#!/usr/bin/env python3
"""Build the ObviousBench v0.2 launch site from the canonical aggregate CSV.

The builder deliberately treats summary.csv as the numerical source of truth.
Row-level presentation metadata (family labels, public-surface and narrative
inclusion, reasoning-state labels, etc.) is stored separately in
row-metadata.json so a previous generated page can never silently override
current benchmark values.
"""

from __future__ import annotations

import argparse
import base64
import csv
import hashlib
import json
import math
import re
import shutil
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parents[4]
DEFAULT_CONFIG = REPO_ROOT / "configs" / "releases" / "release_v0_2_0.yaml"


PROVIDER_LABELS = {
    "anthropic": "Anthropic",
    "deepseek": "DeepSeek",
    "google": "Google",
    "meta-llama": "Meta",
    "minimax": "MiniMax",
    "mistralai": "Mistral",
    "moonshotai": "Kimi",
    "nvidia": "NVIDIA",
    "openai": "OpenAI",
    "qwen": "Qwen",
    "x-ai": "xAI",
    "z-ai": "Z.ai",
}

EFFORT_ORDER = {
    "none": 0,
    "disabled": 0,
    "minimal": 1,
    "low": 2,
    "medium": 3,
    "high": 4,
    "xhigh": 5,
    "max": 6,
    "reasoning": 2,
}

REQUIRED_STORY_ROWS = {
    "gpt5_nano_minimal": "old-1-openai-gpt-5-nano-minimal",
    "gpt5_nano_low": "old-188-openai-gpt-5-nano-low",
    "gpt5_nano_medium": "old-190-openai-gpt-5-nano-medium",
    "gpt5_nano_high": "manual-20260612-openai-gpt-5-nano-high",
    "gemma4_31b_low": "manual-20260612-google-gemma-4-31b-it-low",
    "gemma4_31b_medium": "manual-20260612-google-gemma-4-31b-it-medium",
    "gemma4_31b_high": "manual-20260612-google-gemma-4-31b-it-high",
    "gemini35_minimal": "old-220-google-gemini-3-5-flash-minimal",
    "gemini35_low": "old-221-google-gemini-3-5-flash-low",
    "gemini35_medium": "old-222-google-gemini-3-5-flash-medium",
    "gemini35_high": "old-223-google-gemini-3-5-flash-high",
    "o1_high": "manual-20260612-openai-o1-high",
    "o3_medium": "manual-20260612-openai-o3-medium",
    "grok43_disabled": "manual-20260612-x-ai-grok-4-3-disabled",
    "grok43_high": "manual-20260612-x-ai-grok-4-3-high",
    "grok420_disabled": "manual-20260612-x-ai-grok-4-20-disabled",
    "grok420_high": "manual-20260612-x-ai-grok-4-20-high",
}


def json_safe(value: Any) -> Any:
    if value is None:
        return None
    if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
        return None
    if hasattr(value, "item"):
        value = value.item()
    return value


def normalized_effort(raw: str, reasoning_tokens: int) -> str:
    raw = (raw or "none").strip().lower()
    if raw.startswith("low"):
        return "low"
    if raw.startswith("medium"):
        return "medium"
    if raw.startswith("high"):
        return "high"
    if raw.startswith("xhigh"):
        return "xhigh"
    if raw in {"none", "disabled"}:
        return "none"
    if raw == "minimal":
        return "minimal"
    if raw == "max":
        return "max"
    if raw in {"dynamic", "thinking"}:
        return "reasoning"
    if raw == "default":
        return "reasoning" if reasoning_tokens > 0 else "none"
    return "reasoning" if reasoning_tokens > 0 else "none"


def title_from_model(model: str) -> str:
    stem = model.split("/", 1)[-1]
    tokens = re.split(r"[-_]", stem)
    special = {"gpt": "GPT", "vl": "VL", "it": "IT", "ai": "AI", "oss": "OSS"}
    parts = []
    for token in tokens:
        if not token:
            continue
        lower = token.lower()
        if lower in special:
            parts.append(special[lower])
        elif re.fullmatch(r"\d+b", lower):
            parts.append(lower[:-1] + "B")
        else:
            parts.append(token.capitalize())
    return " ".join(parts)


def clean_model_family_label(label: str) -> str:
    cleaned = label.strip()
    cleaned = cleaned.replace("Gemma 4.31B IT", "Gemma 4 31B IT")
    cleaned = re.sub(
        r"\b(\d+)b\b",
        lambda match: f"{match.group(1)}B",
        cleaned,
        flags=re.IGNORECASE,
    )
    name_words = {
        "opus": "Opus",
        "sonnet": "Sonnet",
        "haiku": "Haiku",
        "flash": "Flash",
        "mini": "mini",
        "nano": "nano",
    }
    tokens = []
    for token in cleaned.split():
        key = token.lower()
        tokens.append(name_words.get(key, token))
    return " ".join(tokens)


def route_label(inspect_model: str) -> str:
    if not inspect_model:
        return "Unknown route"
    first = inspect_model.split("/", 1)[0]
    labels = {
        "openrouter": "OpenRouter",
        "anthropic": "Anthropic API",
        "google": "Google API",
        "openai": "OpenAI API",
    }
    return labels.get(first, first.replace("-", " ").title())


def load_json(path: Path, fallback: Any) -> Any:
    if not path.exists():
        return fallback
    return json.loads(path.read_text(encoding="utf-8"))


def read_release_config(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(path)
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def resolve_summary_path(root: Path, config: dict[str, Any], requested: Path | None) -> Path:
    if requested is not None:
        return requested.resolve()
    report_summary = REPO_ROOT / config.get("snapshot", {}).get("summary_csv", "")
    if report_summary.exists():
        return report_summary
    return (root / "data" / "summary.csv").resolve()


def build_rows(
    summary_path: Path,
    metadata_path: Path,
    release_date: str = "2026-07-01",
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    with summary_path.open("r", encoding="utf-8-sig", newline="") as handle:
        records = list(csv.DictReader(handle))
    metadata = load_json(metadata_path, {})

    seen_ids: set[str] = set()
    dupes: list[str] = []
    for record in records:
        row_id = str(record.get("model_entry_id") or "")
        if row_id in seen_ids:
            dupes.append(row_id)
        seen_ids.add(row_id)
    if dupes:
        raise ValueError(f"Duplicate model_entry_id values in summary CSV: {dupes[:10]}")

    rows: list[dict[str, Any]] = []
    for record in records:
        row_id = str(record["model_entry_id"])
        meta = metadata.get(row_id, {})
        provider_model = str(record["provider_model"])
        provider = str(meta.get("provider") or provider_model.split("/", 1)[0])
        reasoning_tokens = int(record.get("reasoning_tokens") or 0)
        raw_effort = str(record.get("reasoning_effort") or "")
        effort = str(
            meta.get("effort") or normalized_effort(raw_effort, reasoning_tokens)
        )
        configured_effort = str(record.get("reasoning_effort") or "none")

        thinking_state = meta.get("thinking_state")
        thinking_state_label = meta.get("thinking_state_label")
        if not thinking_state:
            if effort == "minimal" and reasoning_tokens == 0:
                thinking_state = "minimal_no_reasoning"
                thinking_state_label = "Minimal / no reasoning reported"
            elif reasoning_tokens > 0:
                thinking_state = "thinking_reported"
                thinking_state_label = "Reasoning reported"
            else:
                thinking_state = "no_reported_reasoning"
                thinking_state_label = "No reported reasoning"

        availability = str(meta.get("availability") or "unclassified")
        availability_label = str(meta.get("availability_label") or "Not reviewed")
        if provider == "openai" and row_id == "requested-004-openai-gpt-3-5-turbo-instruct-default":
            availability = "proprietary"
            availability_label = "Proprietary"

        model_family = str(meta.get("model_family") or provider_model)
        model_family_label = clean_model_family_label(
            str(meta.get("model_family_label") or title_from_model(model_family))
        )
        size_class = str(meta.get("size_class") or "undisclosed")
        size_label = str(
            meta.get("size_label")
            or ("Undisclosed" if size_class == "undisclosed" else size_class.title())
        )
        parameter_b = json_safe(meta.get("parameter_b"))

        surface_included = bool(meta.get("surface_included", True))
        narrative_included = bool(meta.get("narrative_included", True))
        surface_note = str(
            meta.get("surface_note")
            or ("Included headline row" if surface_included else "Diagnostic row")
        )

        items = int(record.get("items") or 0)
        complete_items = int(record.get("complete_items") or 0)
        if items and complete_items != items:
            surface_note = f"{surface_note} Incomplete aggregate: {complete_items}/{items} items."

        row = {
            "row_id": row_id,
            "label": str(record.get("label") or provider_model),
            "model": provider_model,
            "model_family": model_family,
            "model_family_label": model_family_label,
            "provider": provider,
            "provider_label": PROVIDER_LABELS.get(provider, provider.replace("-", " ").title()),
            "inspect_model": str(record.get("inspect_model") or ""),
            "route_label": route_label(str(record.get("inspect_model") or "")),
            "configured_effort": configured_effort,
            "effort": effort,
            "effort_order": int(
                meta.get("effort_order")
                if meta.get("effort_order") is not None
                else EFFORT_ORDER.get(effort, 2)
            ),
            "answer": float(record.get("answer_pass3_accuracy") or 0) * 100,
            "strict": float(record.get("strict_pass3_accuracy") or 0) * 100,
            "format": float(record.get("format_pass3_accuracy") or 0) * 100,
            "strict_attempt": float(record.get("strict_attempt_accuracy") or 0) * 100,
            "strict_any3": float(record.get("strict_any3_accuracy") or 0) * 100,
            "answer_items": int(record.get("answer_pass3_items") or 0),
            "strict_items": int(record.get("strict_pass3_items") or 0),
            "items": items,
            "complete_items": complete_items,
            "valid_attempts": int(record.get("valid_attempts") or 0),
            "cost": float(record.get("estimated_cost_usd") or 0),
            "input_tokens": int(record.get("input_tokens") or 0),
            "output_tokens": int(record.get("output_tokens") or 0),
            "reasoning_tokens": reasoning_tokens,
            "cache_read_tokens": int(record.get("cache_read_tokens") or 0),
            "cache_write_tokens": int(record.get("cache_write_tokens") or 0),
            "total_tokens": int(record.get("total_tokens") or 0),
            "provider_errors": int(record.get("provider_errors") or 0),
            "timeouts": int(record.get("timeouts") or 0),
            "strict_ci_low": float(record.get("strict_pass3_ci_low") or 0) * 100,
            "strict_ci_high": float(record.get("strict_pass3_ci_high") or 0) * 100,
            "availability": availability,
            "availability_label": availability_label,
            "size_class": size_class,
            "size_label": size_label,
            "parameter_b": parameter_b,
            "size_evidence": str(
                meta.get("size_evidence")
                or "Not reviewed in the supplied classification artifact"
            ),
            "surface_included": surface_included,
            "narrative_included": narrative_included,
            "surface_note": surface_note,
            "thinking_state": thinking_state,
            "thinking_state_label": str(thinking_state_label),
            "thinking_evidence": str(
                meta.get("thinking_evidence")
                or f"setting={configured_effort}; reasoning_tokens={reasoning_tokens:,}"
            ),
        }
        rows.append(row)

    row_by_id = {row["row_id"]: row for row in rows}
    missing = {
        name: row_id
        for name, row_id in REQUIRED_STORY_ROWS.items()
        if row_id not in row_by_id
    }
    if missing:
        raise ValueError(f"Required narrative rows are missing: {missing}")
    non_narrative = {
        name: row_id
        for name, row_id in REQUIRED_STORY_ROWS.items()
        if row_by_id[row_id].get("narrative_included") is False
    }
    if non_narrative:
        raise ValueError(
            "Required narrative rows were excluded from narrative surfaces: "
            f"{non_narrative}"
        )

    item_counts = {row["items"] for row in rows if row["items"]}
    if len(item_counts) != 1:
        raise ValueError(f"Expected one benchmark item count, found: {sorted(item_counts)}")

    rows.sort(
        key=lambda row: (
            row["provider_label"],
            row["model_family_label"],
            row["effort_order"],
            row["cost"],
            row["row_id"],
        )
    )
    source_bytes = summary_path.read_bytes()
    build = {
        "generated_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "source_csv": summary_path.name,
        "source_sha256": hashlib.sha256(source_bytes).hexdigest(),
        "row_count": len(rows),
        "surface_row_count": sum(1 for row in rows if row["surface_included"]),
        "narrative_row_count": sum(1 for row in rows if row["narrative_included"]),
        "narrative_surface_row_count": sum(
            1 for row in rows if row["surface_included"] and row["narrative_included"]
        ),
        "diagnostic_row_count": sum(1 for row in rows if not row["surface_included"]),
        "item_count": next(iter(item_counts)),
        "attempts_per_item": 3,
        "failure_family_count": 8,
        "release_date": release_date,
        "status": "local-publication-prep",
    }
    return rows, build


def write_js(path: Path, assignment: str, payload: Any) -> None:
    encoded = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f"window.{assignment}={encoded};\n", encoding="utf-8")


def inline_script(text: str) -> str:
    return text.replace("</script", "<\\/script")


def data_uri(payload: bytes, mime_type: str) -> str:
    encoded = base64.b64encode(payload).decode("ascii")
    return f"data:{mime_type};base64,{encoded}"


def asset_data_uri(root: Path, relative_path: str, mime_type: str) -> str:
    return data_uri((root / relative_path).read_bytes(), mime_type)


def standalone_manifest_uri(root: Path) -> str:
    manifest = json.loads((root / "assets" / "site.webmanifest").read_text(encoding="utf-8"))
    for icon in manifest.get("icons", []):
        icon["src"] = asset_data_uri(root, f"assets/{icon['src']}", "image/png")
    payload = json.dumps(manifest, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    return data_uri(payload, "application/manifest+json")


def make_standalone(root: Path) -> Path:
    html = (root / "index.html").read_text(encoding="utf-8")
    css = (root / "styles.css").read_text(encoding="utf-8")
    vendor = (root / "vendor" / "echarts.min.js").read_text(encoding="utf-8")
    icons = (root / "data" / "provider-icons.js").read_text(encoding="utf-8")
    results = (root / "data" / "results.js").read_text(encoding="utf-8")
    build_js = (root / "data" / "build.js").read_text(encoding="utf-8")
    app = (root / "app.js").read_text(encoding="utf-8")

    asset_replacements = {
        "assets/obviousbench-mark.png": asset_data_uri(
            root,
            "assets/obviousbench-mark.png",
            "image/png",
        ),
        "assets/favicon-32x32.png": asset_data_uri(
            root,
            "assets/favicon-32x32.png",
            "image/png",
        ),
        "assets/favicon-16x16.png": asset_data_uri(
            root,
            "assets/favicon-16x16.png",
            "image/png",
        ),
        "assets/apple-touch-icon.png": asset_data_uri(
            root,
            "assets/apple-touch-icon.png",
            "image/png",
        ),
    }
    for relative_path, uri in asset_replacements.items():
        html = html.replace(f'href="{relative_path}"', f'href="{uri}"')
        html = html.replace(f'src="{relative_path}"', f'src="{uri}"')
    html = html.replace(
        'href="assets/site.webmanifest"',
        f'href="{standalone_manifest_uri(root)}"',
    )

    html = html.replace(
        '<link rel="stylesheet" href="styles.css">',
        f"<style>\n{css}\n</style>",
    )
    html = html.replace(
        '<script src="vendor/echarts.min.js"></script>',
        f"<script>\n{inline_script(vendor)}\n</script>",
    )
    html = html.replace(
        '<script src="data/provider-icons.js"></script>',
        f"<script>\n{inline_script(icons)}\n</script>",
    )
    html = html.replace(
        '<script src="data/results.js"></script>',
        f"<script>\n{inline_script(results)}\n</script>",
    )
    html = html.replace(
        '<script src="data/build.js"></script>',
        f"<script>\n{inline_script(build_js)}\n</script>",
    )
    html = html.replace(
        '<script src="app.js"></script>',
        f"<script>\n{inline_script(app)}\n</script>",
    )
    output = root / "dist" / "obviousbench-v0.2-launch.html"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(html, encoding="utf-8")
    return output


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--summary", type=Path, default=None)
    parser.add_argument("--metadata", type=Path, default=None)
    args = parser.parse_args()

    root = args.root.resolve()
    config = read_release_config((args.config or DEFAULT_CONFIG).resolve())
    summary = resolve_summary_path(root, config, args.summary)
    metadata = (args.metadata or root / "data" / "row-metadata.json").resolve()
    if not summary.exists():
        raise FileNotFoundError(summary)

    rows, build = build_rows(
        summary,
        metadata,
        release_date=str(config["release"]["date"]),
    )
    public_rows = [row for row in rows if row["surface_included"]]
    write_js(root / "data" / "results.js", "OBVIOUSBENCH_ROWS", public_rows)
    write_js(root / "data" / "build.js", "OBVIOUSBENCH_BUILD", build)
    write_js(
        root / "data" / "provider-icons.js",
        "OBVIOUSBENCH_PROVIDER_ICONS",
        load_json(root / "data" / "provider-icons.json", {}),
    )
    summary_copy = (root / "data" / "summary.csv").resolve()
    if summary != summary_copy:
        shutil.copy2(summary, summary_copy)
    standalone = make_standalone(root)
    print(
        json.dumps(
            {
                "rows": len(public_rows),
                "surface_rows": build["surface_row_count"],
                "narrative_surface_rows": build["narrative_surface_row_count"],
                "standalone": str(standalone),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
