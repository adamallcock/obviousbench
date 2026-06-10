#!/usr/bin/env python
"""Run compact provider smoke checks for entries in configs/model_registry_v1.yaml."""

from __future__ import annotations

import argparse
import csv
import json
import multiprocessing
import os
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import yaml

DEFAULT_REGISTRY = Path("configs/model_registry_v1.yaml")
DEFAULT_PROMPT = "Reply with exactly OK."
DEFAULT_MAX_TOKENS = 64
DEFAULT_TIMEOUT_SECONDS = 45
DEFAULT_BATCH_SIZE = 8
DEFAULT_MAX_WORKERS = 2
DEFAULT_BATCH_SLEEP_SECONDS = 2

KEY_SOURCES = {
    "openrouter": (
        ("OPENROUTER_API_KEY",),
        ("OPENROUTER_API_KEY", "codex-openrouter-api-key"),
    ),
    "openai": (
        ("OPENAI_API_KEY",),
        ("OPENAI_API_KEY", "codex-openai-api-key"),
    ),
    "anthropic": (
        ("ANTHROPIC_API_KEY",),
        ("ANTHROPIC_API_KEY", "codex-anthropic-api-key"),
    ),
    "gemini": (
        ("GOOGLE_API_KEY", "GEMINI_API_KEY", "GOOGLE_AI_API_KEY"),
        ("GOOGLE_API_KEY", "GEMINI_API_KEY", "GOOGLE_AI_API_KEY", "codex-gemini-api-key"),
    ),
    "grok": (
        ("XAI_API_KEY",),
        ("XAI_API_KEY", "codex-xai-api-key"),
    ),
}


@dataclass(frozen=True)
class Secret:
    value: str
    source: str


@dataclass(frozen=True)
class RequestSpec:
    url: str
    headers: dict[str, str]
    payload: dict[str, Any]


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY)
    parser.add_argument(
        "--out-dir",
        type=Path,
        help="Defaults to results/summaries/model-registry-smoke-<timestamp>.",
    )
    parser.add_argument("--provider-route", action="append", default=[])
    parser.add_argument("--tag", action="append", default=[])
    parser.add_argument("--entry-id", action="append", default=[])
    parser.add_argument("--limit", type=int)
    parser.add_argument("--offset", type=int, default=0)
    parser.add_argument("--batch-size", type=int, default=DEFAULT_BATCH_SIZE)
    parser.add_argument("--max-workers", type=int, default=DEFAULT_MAX_WORKERS)
    parser.add_argument("--batch-sleep", type=float, default=DEFAULT_BATCH_SLEEP_SECONDS)
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT_SECONDS)
    parser.add_argument("--max-tokens", type=int, default=DEFAULT_MAX_TOKENS)
    parser.add_argument("--max-retries", type=int, default=1)
    parser.add_argument("--retry-sleep-cap", type=int, default=20)
    parser.add_argument("--prompt", default=DEFAULT_PROMPT)
    parser.add_argument(
        "--resume",
        action="store_true",
        help="Skip entries already present in results.jsonl in --out-dir.",
    )
    parser.add_argument(
        "--retry-status",
        action="append",
        default=[],
        help=(
            "With --resume, retry entries whose previous status matches this value. "
            "May be repeated, e.g. --retry-status rate_limited."
        ),
    )
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--gemini-openrouter-fallback",
        action="store_true",
        help=(
            "If a direct Gemini key is unavailable, try the same Gemini model ID "
            "through OpenRouter as google/<model>."
        ),
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    registry = load_registry(args.registry)
    entries = select_entries(
        registry["entries"],
        provider_routes=set(args.provider_route),
        tags=set(args.tag),
        entry_ids=set(args.entry_id),
        offset=args.offset,
        limit=args.limit,
    )
    out_dir = args.out_dir or default_output_dir()
    out_dir.mkdir(parents=True, exist_ok=True)
    existing = load_existing_results(out_dir / "results.jsonl") if args.resume else {}
    retry_statuses = set(args.retry_status)
    pending = [
        entry
        for entry in entries
        if entry["id"] not in existing
        or existing[entry["id"]].get("status") in retry_statuses
    ]
    pending_ids = {entry["id"] for entry in pending}

    write_run_metadata(out_dir, args, registry, entries, pending)
    if args.dry_run:
        write_dry_run(out_dir, pending)
        write_summaries(out_dir, list(existing.values()))
        print(f"Dry run selected {len(pending)} pending entries under {out_dir}")
        return 0

    results = [
        row for entry_id, row in existing.items() if entry_id not in pending_ids
    ]
    results_path = out_dir / "results.jsonl"
    for batch_index, batch in enumerate(chunks(pending, args.batch_size), 1):
        print(
            f"batch {batch_index}: {len(batch)} entries "
            f"({batch[0]['id']}..{batch[-1]['id']})",
            flush=True,
        )
        batch_results = run_batch(batch, args)
        append_jsonl(results_path, batch_results)
        results.extend(batch_results)
        write_summaries(out_dir, results)
        if args.batch_sleep and batch_index * args.batch_size < len(pending):
            time.sleep(args.batch_sleep)

    print(f"Wrote {len(results)} total result rows under {out_dir}")
    print(format_status_counts(results))
    return 0


def load_registry(path: Path) -> dict[str, Any]:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def select_entries(
    entries: list[dict[str, Any]],
    *,
    provider_routes: set[str],
    tags: set[str],
    entry_ids: set[str],
    offset: int,
    limit: int | None,
) -> list[dict[str, Any]]:
    selected = []
    for entry in entries:
        if provider_routes and entry["provider_route"] not in provider_routes:
            continue
        if tags and not tags.issubset(set(entry.get("tags", []))):
            continue
        if entry_ids and entry["id"] not in entry_ids:
            continue
        selected.append(entry)
    selected = selected[offset:]
    return selected[:limit] if limit is not None else selected


def default_output_dir() -> Path:
    stamp = datetime.now(UTC).strftime("%Y%m%d-%H%M%S")
    return Path("results/summaries") / f"model-registry-smoke-{stamp}"


def load_existing_results(path: Path) -> dict[str, dict[str, Any]]:
    if not path.exists():
        return {}
    rows = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        rows[row["entry_id"]] = row
    return rows


def write_run_metadata(
    out_dir: Path,
    args: argparse.Namespace,
    registry: dict[str, Any],
    selected: list[dict[str, Any]],
    pending: list[dict[str, Any]],
) -> None:
    metadata = {
        "created_at": datetime.now(UTC).isoformat(),
        "registry_path": str(args.registry),
        "registry_generated_at": registry.get("generated_at"),
        "selected_entries": len(selected),
        "pending_entries": len(pending),
        "prompt": args.prompt,
        "max_tokens": args.max_tokens,
        "batch_size": args.batch_size,
        "max_workers": args.max_workers,
        "provider_routes": args.provider_route,
        "tags": args.tag,
        "entry_ids": args.entry_id,
        "retry_status": args.retry_status,
        "gemini_openrouter_fallback": args.gemini_openrouter_fallback,
    }
    (out_dir / "run.json").write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def write_dry_run(out_dir: Path, entries: list[dict[str, Any]]) -> None:
    rows = [
        {
            "entry_id": entry["id"],
            "provider_route": entry["provider_route"],
            "inspect_model": entry["inspect_model"],
            "model_id": entry["model_id"],
        }
        for entry in entries
    ]
    (out_dir / "dry_run.json").write_text(
        json.dumps(rows, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def run_batch(entries: list[dict[str, Any]], args: argparse.Namespace) -> list[dict[str, Any]]:
    results = []
    with ThreadPoolExecutor(max_workers=max(args.max_workers, 1)) as executor:
        futures = [executor.submit(run_entry, entry, args) for entry in entries]
        for future in as_completed(futures):
            results.append(future.result())
    return sorted(results, key=lambda row: row["registry_index"])


def run_entry(entry: dict[str, Any], args: argparse.Namespace) -> dict[str, Any]:
    started = datetime.now(UTC)
    base = {
        "registry_index": entry.get("_registry_index", -1),
        "entry_id": entry["id"],
        "label": entry["label"],
        "provider_route": entry["provider_route"],
        "inspect_model": entry["inspect_model"],
        "model_id": entry["model_id"],
        "execution_route": entry["provider_route"],
        "started_at": started.isoformat(),
    }
    secret = resolve_secret(entry["provider_route"])
    request_entry = entry
    execution_route = entry["provider_route"]
    if secret is None and entry["provider_route"] == "gemini" and args.gemini_openrouter_fallback:
        secret = resolve_secret("openrouter")
        execution_route = "openrouter_fallback"
        request_entry = {
            **entry,
            "provider_route": "openrouter",
            "model_id": f"google/{entry['model_id']}",
        }
    if secret is None:
        return {
            **base,
            "finished_at": datetime.now(UTC).isoformat(),
            "status": "missing_credential",
            "http_status": None,
            "latency_ms": 0,
            "credential_source": None,
            "answer_exact_ok": False,
            "content_preview": "",
            "error_code": "missing_credential",
            "error_message": f"No credential found for {entry['provider_route']}.",
        }

    request = build_request(request_entry, secret.value, args.prompt, args.max_tokens)
    status, http_status, body, error = request_with_retries(
        request,
        timeout=args.timeout,
        max_retries=args.max_retries,
        retry_sleep_cap=args.retry_sleep_cap,
    )
    finished = datetime.now(UTC)
    text = extract_text(request_entry["provider_route"], body) if body else ""
    answer_exact_ok = normalize_answer(text) == "ok"
    if status == "ok" and not text:
        status = "empty_response"
    return {
        **base,
        "finished_at": finished.isoformat(),
        "status": status,
        "http_status": http_status,
        "latency_ms": round((finished - started).total_seconds() * 1000),
        "execution_route": execution_route,
        "credential_source": secret.source,
        "answer_exact_ok": answer_exact_ok,
        "content_preview": text[:200],
        "error_code": error.get("code") if error else "",
        "error_message": error.get("message")[:500] if error else "",
    }


def resolve_secret(provider_route: str) -> Secret | None:
    env_names, keychain_services = KEY_SOURCES.get(provider_route, ((), ()))
    for name in env_names:
        value = os.environ.get(name)
        if value:
            return Secret(value=value, source=f"env:{name}")
    for service in keychain_services:
        value = read_keychain_service(service)
        if value:
            return Secret(value=value, source=f"keychain:{service}")
    return None


def read_keychain_service(service: str) -> str | None:
    try:
        result = subprocess.run(
            ["security", "find-generic-password", "-s", service, "-w"],
            check=False,
            capture_output=True,
            text=True,
        )
    except OSError:
        return None
    if result.returncode != 0:
        return None
    return result.stdout.strip() or None


def build_request(
    entry: dict[str, Any],
    api_key: str,
    prompt: str,
    smoke_max_tokens: int,
) -> RequestSpec:
    route = entry["provider_route"]
    configured_max_tokens = int(
        entry["generation_settings"].get("max_tokens", smoke_max_tokens)
    )
    max_tokens = min(configured_max_tokens, smoke_max_tokens)
    if route == "openrouter":
        return chat_completion_request(
            "https://openrouter.ai/api/v1/chat/completions",
            api_key,
            entry["model_id"],
            prompt,
            max_tokens,
            extra_payload={
                "include_reasoning": False,
                "reasoning": {"exclude": True},
            },
        )
    if route == "grok":
        return chat_completion_request(
            "https://api.x.ai/v1/chat/completions",
            api_key,
            entry["model_id"],
            prompt,
            max_tokens,
        )
    if route == "openai":
        payload: dict[str, Any] = {
            "model": entry["model_id"],
            "input": prompt,
            "max_output_tokens": max_tokens,
        }
        reasoning_effort = entry["generation_settings"].get("reasoning_effort")
        if reasoning_effort:
            payload["reasoning"] = {"effort": reasoning_effort}
        return RequestSpec(
            url="https://api.openai.com/v1/responses",
            headers=auth_headers(api_key),
            payload=payload,
        )
    if route == "anthropic":
        return RequestSpec(
            url="https://api.anthropic.com/v1/messages",
            headers={
                "content-type": "application/json",
                "x-api-key": api_key,
                "anthropic-version": "2023-06-01",
            },
            payload={
                "model": entry["model_id"],
                "max_tokens": max_tokens,
                "messages": [{"role": "user", "content": prompt}],
            },
        )
    if route == "gemini":
        model = urllib.parse.quote(entry["model_id"], safe="")
        return RequestSpec(
            url=(
                "https://generativelanguage.googleapis.com/v1beta/models/"
                f"{model}:generateContent?key={api_key}"
            ),
            headers={"content-type": "application/json"},
            payload={
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {
                    "temperature": 0,
                    "maxOutputTokens": max_tokens,
                },
            },
        )
    raise ValueError(f"Unsupported provider_route: {route}")


def chat_completion_request(
    url: str,
    api_key: str,
    model: str,
    prompt: str,
    max_tokens: int,
    *,
    extra_payload: dict[str, Any] | None = None,
) -> RequestSpec:
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0,
        "max_tokens": max_tokens,
    }
    if extra_payload:
        payload.update(extra_payload)
    return RequestSpec(
        url=url,
        headers=auth_headers(api_key),
        payload=payload,
    )


def auth_headers(api_key: str) -> dict[str, str]:
    return {
        "authorization": f"Bearer {api_key}",
        "content-type": "application/json",
    }


def request_with_retries(
    request: RequestSpec,
    *,
    timeout: int,
    max_retries: int,
    retry_sleep_cap: int,
) -> tuple[str, int | None, dict[str, Any] | None, dict[str, str] | None]:
    for attempt in range(max_retries + 1):
        status, http_status, body, error, retry_after = post_json(request, timeout=timeout)
        if status == "ok" or attempt >= max_retries or http_status not in {429, 500, 502, 503, 504}:
            return status, http_status, body, error
        time.sleep(min(retry_after or (2**attempt), retry_sleep_cap))
    return (
        "request_error",
        None,
        None,
        {"code": "retry_exhausted", "message": "Retry loop exhausted."},
    )


def post_json(
    request: RequestSpec,
    *,
    timeout: int,
) -> tuple[str, int | None, dict[str, Any] | None, dict[str, str] | None, int | None]:
    ctx = multiprocessing.get_context("spawn")
    queue = ctx.Queue()
    process = ctx.Process(target=_post_json_child, args=(request, timeout, queue))
    process.start()
    process.join(timeout + 2)
    if process.is_alive():
        process.terminate()
        process.join(2)
        if process.is_alive():
            process.kill()
            process.join(1)
        return (
            "request_timeout",
            None,
            None,
            {
                "code": "request_timeout",
                "message": f"Provider request exceeded hard timeout of {timeout}s.",
            },
            None,
        )
    if queue.empty():
        return (
            "request_error",
            None,
            None,
            {
                "code": "child_process_error",
                "message": f"Provider request worker exited with {process.exitcode}.",
            },
            None,
        )
    return queue.get()


def _post_json_child(request: RequestSpec, timeout: int, queue) -> None:
    queue.put(post_json_once(request, timeout=timeout))


def post_json_once(
    request: RequestSpec,
    *,
    timeout: int,
) -> tuple[str, int | None, dict[str, Any] | None, dict[str, str] | None, int | None]:
    data = json.dumps(request.payload).encode("utf-8")
    http_request = urllib.request.Request(
        request.url,
        data=data,
        headers=request.headers,
        method="POST",
    )
    try:
        with urllib.request.urlopen(http_request, timeout=timeout) as response:
            body = json.loads(response.read().decode("utf-8") or "{}")
            return "ok", response.status, body, None, None
    except urllib.error.HTTPError as exc:
        retry_after = parse_retry_after(exc.headers.get("retry-after"))
        body_text = exc.read().decode("utf-8", errors="replace")
        error = parse_error(body_text)
        return status_for_http(exc.code), exc.code, None, error, retry_after
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        return (
            "request_error",
            None,
            None,
            {"code": type(exc).__name__, "message": str(exc)},
            None,
        )


def parse_retry_after(value: str | None) -> int | None:
    if not value:
        return None
    try:
        return max(int(float(value)), 0)
    except ValueError:
        return None


def parse_error(body_text: str) -> dict[str, str]:
    try:
        body = json.loads(body_text)
    except json.JSONDecodeError:
        return {"code": "http_error", "message": body_text[:500]}
    error = body.get("error", body)
    if isinstance(error, dict):
        return {
            "code": str(error.get("code") or error.get("type") or "http_error"),
            "message": str(error.get("message") or body_text)[:500],
        }
    return {"code": "http_error", "message": str(error)[:500]}


def status_for_http(status: int) -> str:
    if status == 401:
        return "auth_error"
    if status == 402:
        return "credit_error"
    if status == 404:
        return "model_not_found"
    if status == 429:
        return "rate_limited"
    return "http_error"


def extract_text(provider_route: str, body: dict[str, Any]) -> str:
    if provider_route in {"openrouter", "grok"}:
        return str(
            body.get("choices", [{}])[0]
            .get("message", {})
            .get("content")
            or ""
        ).strip()
    if provider_route == "openai":
        if body.get("output_text"):
            return str(body["output_text"]).strip()
        parts = []
        for item in body.get("output", []):
            for content in item.get("content", []):
                if content.get("type") in {"output_text", "text"}:
                    parts.append(str(content.get("text", "")))
        return "\n".join(parts).strip()
    if provider_route == "anthropic":
        return "\n".join(
            str(part.get("text", ""))
            for part in body.get("content", [])
            if part.get("type") == "text"
        ).strip()
    if provider_route == "gemini":
        parts = body.get("candidates", [{}])[0].get("content", {}).get("parts", [])
        return "\n".join(str(part.get("text", "")) for part in parts).strip()
    return ""


def normalize_answer(text: str) -> str:
    return text.strip().strip(".").lower()


def chunks(values: list[dict[str, Any]], size: int):
    if size < 1:
        raise ValueError("batch size must be positive")
    for index in range(0, len(values), size):
        batch = values[index : index + size]
        for offset, entry in enumerate(batch):
            entry["_registry_index"] = index + offset
        yield batch


def append_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("a", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, sort_keys=True) + "\n")


def write_summaries(out_dir: Path, results: list[dict[str, Any]]) -> None:
    write_latest_jsonl(out_dir / "latest_results.jsonl", results)
    write_summary_csv(out_dir / "summary.csv", results)
    write_summary_md(out_dir / "summary.md", results)


def write_latest_jsonl(path: Path, results: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for row in sorted(results, key=lambda item: item.get("entry_id", "")):
            handle.write(json.dumps(row, sort_keys=True) + "\n")


def write_summary_csv(path: Path, results: list[dict[str, Any]]) -> None:
    fieldnames = [
        "provider_route",
        "status",
        "count",
        "answer_exact_ok",
    ]
    counts = Counter(
        (
            row["provider_route"],
            row["status"],
            "yes" if row.get("answer_exact_ok") else "no",
        )
        for row in results
    )
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for (provider_route, status, answer_exact_ok), count in sorted(counts.items()):
            writer.writerow(
                {
                    "provider_route": provider_route,
                    "status": status,
                    "count": count,
                    "answer_exact_ok": answer_exact_ok,
                }
            )


def write_summary_md(path: Path, results: list[dict[str, Any]]) -> None:
    status_counts = Counter(row["status"] for row in results)
    lines = [
        "# Model Registry Smoke Summary",
        "",
        f"Updated: {datetime.now(UTC).isoformat()}",
        f"Unique entries summarized: {len(results)}",
        f"OK entries: {status_counts.get('ok', 0)}",
        f"Non-OK entries: {len(results) - status_counts.get('ok', 0)}",
        "",
        format_status_counts(results),
        "",
        "## Provider Status Counts",
        "",
        "| Provider | Status | Count |",
        "| --- | --- | ---: |",
    ]
    counts = Counter((row["provider_route"], row["status"]) for row in results)
    for (provider_route, status), count in sorted(counts.items()):
        lines.append(f"| {provider_route} | {status} | {count} |")
    non_ok = [row for row in results if row["status"] != "ok"]
    if non_ok:
        lines.extend(
            [
                "",
                "## Remaining Non-OK Entries",
                "",
                "| Entry | Provider | Model | Status | HTTP | Error |",
                "| --- | --- | --- | --- | ---: | --- |",
            ]
        )
        for row in sorted(
            non_ok,
            key=lambda item: (item["status"], item.get("entry_id", "")),
        ):
            error = (row.get("error_message") or row.get("error_code") or "").replace(
                "|", "\\|"
            )
            lines.append(
                "| "
                f"{row.get('entry_id', '')} | "
                f"{row['provider_route']} | "
                f"{row.get('model_id', '')} | "
                f"{row['status']} | "
                f"{row.get('http_status') or ''} | "
                f"{error[:160]} |"
            )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def format_status_counts(results: list[dict[str, Any]]) -> str:
    counts = Counter(row["status"] for row in results)
    return "status counts: " + ", ".join(
        f"{status}={count}" for status, count in sorted(counts.items())
    )


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
