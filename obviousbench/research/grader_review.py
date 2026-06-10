"""Build a combined grader-review report for final benchmark failures."""

from __future__ import annotations

import csv
import html
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from obviousbench.analysis.build_failure_gallery import FailureGalleryEntry
from obviousbench.analysis.logs import load_eval_logs_with_failures
from obviousbench.analysis.metrics import EvalRecord
from obviousbench.research.final_result_artifacts import REQUIRED_MANIFEST_COLUMNS


@dataclass(frozen=True)
class SummaryTargets:
    total_samples: int
    scored_samples: int
    provider_errors: int
    timeouts: int = 0


@dataclass(frozen=True)
class LogCandidateStats:
    path: Path
    total_samples: int
    scored_samples: int
    provider_errors: int
    timeout_count: int


@dataclass(frozen=True)
class GraderReviewInputs:
    manifest_path: Path
    raw_root: Path
    csv_output_path: Path
    html_output_path: Path
    rescore: bool = True
    source: Literal["raw_logs", "summary_galleries"] = "raw_logs"


@dataclass(frozen=True)
class GraderReviewResult:
    csv_output_path: Path
    html_output_path: Path
    row_count: int
    model_count: int
    warning_count: int
    answer_wrong_count: int
    format_only_count: int


@dataclass(frozen=True)
class _ManifestEntry:
    label: str
    model: str
    summary_dir: Path

    @property
    def entry_id(self) -> str:
        return self.summary_dir.name


@dataclass(frozen=True)
class _LoadedLogCandidate:
    stats: LogCandidateStats
    records: tuple[EvalRecord, ...]
    failures: tuple[FailureGalleryEntry, ...]


@dataclass(frozen=True)
class _ReviewRow:
    review_status: str
    grader_issue: str
    notes: str
    review_kind: str
    model_label: str
    model: str
    family: str
    subfamily: str
    sample_id: str
    failure_type: str
    answer_correct: str
    format_correct: str
    strict_correct: str
    expected_answer: str
    extracted_answer: str
    raw_output: str
    question: str
    human_triviality: str
    source_type: str
    why_obvious: str
    reference: str
    log_file: str


REVIEW_FIELDS = (
    "review_status",
    "grader_issue",
    "notes",
    "review_kind",
    "model_label",
    "model",
    "family",
    "subfamily",
    "sample_id",
    "failure_type",
    "answer_correct",
    "format_correct",
    "strict_correct",
    "expected_answer",
    "extracted_answer",
    "raw_output",
    "question",
    "human_triviality",
    "source_type",
    "why_obvious",
    "reference",
    "log_file",
)


def build_grader_review(inputs: GraderReviewInputs) -> GraderReviewResult:
    """Build combined CSV and HTML review files from a final sweep manifest."""
    manifest_entries = _load_manifest(inputs.manifest_path)
    warnings: list[str] = []
    rows: list[_ReviewRow] = []

    for entry in manifest_entries:
        if inputs.source == "summary_galleries":
            summary_rows, summary_warnings = _review_rows_from_summary_gallery(entry)
            rows.extend(summary_rows)
            warnings.extend(summary_warnings)
            continue
        targets = _read_summary_targets(entry.summary_dir / "summary.csv")
        raw_dir = inputs.raw_root / entry.entry_id
        loaded_candidates = _load_log_candidates(raw_dir, rescore=inputs.rescore)
        selected_paths, selection_warnings = select_matching_log_files(
            tuple(candidate.stats for candidate in loaded_candidates),
            targets,
            entry_id=entry.entry_id,
        )
        warnings.extend(selection_warnings)
        selected_path_set = set(selected_paths)
        selected_candidates = [
            candidate
            for candidate in loaded_candidates
            if candidate.stats.path in selected_path_set
        ]
        for candidate in selected_candidates:
            rows.extend(_review_rows(entry, candidate))

    rows = sorted(
        rows,
        key=lambda row: (
            row.family,
            row.sample_id,
            0 if row.review_kind == "answer_wrong" else 1,
            row.model_label,
        ),
    )
    _write_csv(inputs.csv_output_path, rows)
    _write_html(inputs.html_output_path, rows, warnings=tuple(warnings))
    return GraderReviewResult(
        csv_output_path=inputs.csv_output_path,
        html_output_path=inputs.html_output_path,
        row_count=len(rows),
        model_count=len(manifest_entries),
        warning_count=len(warnings),
        answer_wrong_count=sum(row.review_kind == "answer_wrong" for row in rows),
        format_only_count=sum(row.review_kind == "format_only" for row in rows),
    )


def _review_rows_from_summary_gallery(
    entry: _ManifestEntry,
) -> tuple[list[_ReviewRow], tuple[str, ...]]:
    gallery_path = entry.summary_dir / "failure_gallery.md"
    usage_path = entry.summary_dir / "usage_by_sample.csv"
    warnings: list[str] = []
    if not gallery_path.exists():
        return [], (f"{entry.entry_id}: no failure_gallery.md found",)
    if not usage_path.exists():
        return [], (f"{entry.entry_id}: no usage_by_sample.csv found",)

    usage_by_sample = {
        row.get("sample_id", ""): row for row in _read_csv_dicts(usage_path)
    }
    rows: list[_ReviewRow] = []
    for failure in _parse_failure_gallery(gallery_path):
        sample_id = failure.get("Sample ID", "")
        usage = usage_by_sample.get(sample_id, {})
        if not usage:
            warnings.append(f"{entry.entry_id}: no usage row for {sample_id}")
        answer_correct = _truthy(usage.get("answer_correct"))
        format_correct = _truthy(usage.get("format_correct"))
        strict_correct = _truthy(usage.get("strict_correct"))
        review_kind = "format_only" if answer_correct and not format_correct else "answer_wrong"
        rows.append(
            _ReviewRow(
                review_status="",
                grader_issue="",
                notes="",
                review_kind=review_kind,
                model_label=entry.label,
                model=entry.model,
                family=failure.get("family", usage.get("family", "")),
                subfamily=usage.get("subfamily", ""),
                sample_id=sample_id,
                failure_type=failure.get("Failure type", ""),
                answer_correct=str(answer_correct).lower(),
                format_correct=str(format_correct).lower(),
                strict_correct=str(strict_correct).lower(),
                expected_answer=failure.get("Expected answer", ""),
                extracted_answer=failure.get("Extracted answer", ""),
                raw_output=failure.get("Raw model answer", ""),
                question=failure.get("Question", usage.get("question", "")),
                human_triviality=failure.get("Human triviality", ""),
                source_type=failure.get("Source type", ""),
                why_obvious=failure.get("Why humans find it obvious", ""),
                reference=failure.get("Reference", ""),
                log_file=str(gallery_path),
            )
        )
    return rows, tuple(warnings)


def select_matching_log_files(
    candidates: tuple[LogCandidateStats, ...],
    targets: SummaryTargets,
    *,
    entry_id: str,
) -> tuple[tuple[Path, ...], tuple[str, ...]]:
    """Select raw log files whose counts match the final summary contract."""
    if not candidates:
        return (), (f"{entry_id}: no raw eval logs found",)

    matching = tuple(
        candidate.path
        for candidate in candidates
        if (
            candidate.total_samples == targets.total_samples
            and candidate.scored_samples == targets.scored_samples
            and candidate.provider_errors == targets.provider_errors
            and candidate.timeout_count == targets.timeouts
        )
    )
    if len(matching) == 1:
        return matching, ()
    if len(matching) > 1:
        return matching, (f"{entry_id}: {len(matching)} raw logs matched summary counts",)
    if len(candidates) == 1:
        candidate = candidates[0]
        return (
            (candidate.path,),
            (
                f"{entry_id}: raw log counts did not match summary counts; "
                "using the only available log",
            ),
        )
    warning = (
        f"{entry_id}: no single raw log matched summary counts; "
        f"using all {len(candidates)} logs"
    )
    return (tuple(candidate.path for candidate in candidates), (warning,))


def _load_manifest(path: Path) -> tuple[_ManifestEntry, ...]:
    if not path.exists():
        raise FileNotFoundError(f"Manifest does not exist: {path}")
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        missing = sorted(set(REQUIRED_MANIFEST_COLUMNS) - set(reader.fieldnames or ()))
        if missing:
            raise ValueError(f"{path} missing columns: {', '.join(missing)}")
        entries = []
        for index, row in enumerate(reader, start=2):
            label = (row.get("label") or "").strip()
            model = (row.get("model") or "").strip()
            summary_dir = (row.get("summary_dir") or "").strip()
            if not label or not model or not summary_dir:
                raise ValueError(f"{path}:{index} has a blank label, model, or summary_dir")
            entries.append(_ManifestEntry(label=label, model=model, summary_dir=Path(summary_dir)))
    return tuple(entries)


def _read_summary_targets(path: Path) -> SummaryTargets:
    if not path.exists():
        raise FileNotFoundError(f"Summary CSV does not exist: {path}")
    with path.open(encoding="utf-8", newline="") as handle:
        row = next(csv.DictReader(handle), None)
    if row is None:
        raise ValueError(f"Summary CSV has no data row: {path}")
    return SummaryTargets(
        total_samples=_csv_int(row, "total_samples"),
        scored_samples=_csv_int(row, "scored_samples"),
        provider_errors=_csv_int(row, "provider_errors"),
        timeouts=_csv_int(row, "timeouts"),
    )


def _load_log_candidates(raw_dir: Path, *, rescore: bool) -> tuple[_LoadedLogCandidate, ...]:
    if not raw_dir.exists():
        return ()
    candidates: list[_LoadedLogCandidate] = []
    for log_file in sorted(raw_dir.glob("*.eval")):
        records, failures = load_eval_logs_with_failures(log_file, rescore=rescore)
        stats = LogCandidateStats(
            path=log_file,
            total_samples=len(records),
            scored_samples=len(records),
            provider_errors=sum(record.provider_error for record in records),
            timeout_count=sum(record.timeout for record in records),
        )
        candidates.append(
            _LoadedLogCandidate(
                stats=stats,
                records=tuple(records),
                failures=tuple(failures),
            )
        )
    return tuple(candidates)


def _parse_failure_gallery(path: Path) -> list[dict[str, str]]:
    text = path.read_text(encoding="utf-8")
    failures: list[dict[str, str]] = []
    current: dict[str, str] | None = None
    current_key: str | None = None
    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        if line.startswith("## Failure "):
            if current is not None:
                failures.append(_clean_gallery_fields(current))
            current = {"family": line.split(":", 1)[1].strip() if ":" in line else ""}
            current_key = None
            continue
        if current is None:
            continue
        if line.startswith("<button "):
            continue
        if line.startswith("- ") and ":" in line:
            key, value = line[2:].split(":", 1)
            current_key = key.strip()
            current[current_key] = _strip_markdown_value(value.strip())
            continue
        if current_key and line:
            current[current_key] = (
                current[current_key] + "\n" + _strip_markdown_value(line)
            ).strip()
    if current is not None:
        failures.append(_clean_gallery_fields(current))
    return failures


def _clean_gallery_fields(fields: dict[str, str]) -> dict[str, str]:
    return {key: value.strip() for key, value in fields.items()}


def _strip_markdown_value(value: str) -> str:
    if value.startswith("`") and value.endswith("`") and len(value) >= 2:
        return value[1:-1]
    return value


def _read_csv_dicts(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def _truthy(value: str | None) -> bool:
    return str(value or "").strip().casefold() in {"true", "1", "yes"}


def _review_rows(entry: _ManifestEntry, candidate: _LoadedLogCandidate) -> list[_ReviewRow]:
    record_by_sample = {record.sample_id: record for record in candidate.records}
    rows: list[_ReviewRow] = []
    for failure in candidate.failures:
        record = record_by_sample.get(failure.sample_id)
        answer_correct = bool(record.answer_ok) if record else False
        format_correct = bool(record.format_ok) if record else False
        strict_correct = bool(record.strict_ok) if record else False
        review_kind = "format_only" if answer_correct and not format_correct else "answer_wrong"
        rows.append(
            _ReviewRow(
                review_status="",
                grader_issue="",
                notes="",
                review_kind=review_kind,
                model_label=entry.label,
                model=entry.model,
                family=failure.family,
                subfamily=record.subfamily if record else "",
                sample_id=failure.sample_id,
                failure_type=failure.failure_type,
                answer_correct=str(answer_correct).lower(),
                format_correct=str(format_correct).lower(),
                strict_correct=str(strict_correct).lower(),
                expected_answer=failure.expected_answer,
                extracted_answer=failure.extracted_answer or "",
                raw_output=failure.raw_output,
                question=failure.question,
                human_triviality=failure.human_triviality,
                source_type=failure.source_type,
                why_obvious=failure.why_obvious,
                reference=failure.reference,
                log_file=str(candidate.stats.path),
            )
        )
    return rows


def _write_csv(path: Path, rows: list[_ReviewRow]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=REVIEW_FIELDS)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: getattr(row, field) for field in REVIEW_FIELDS})


def _write_html(path: Path, rows: list[_ReviewRow], *, warnings: tuple[str, ...]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(_render_html(rows, warnings=warnings), encoding="utf-8")


def _render_html(rows: list[_ReviewRow], *, warnings: tuple[str, ...]) -> str:
    models = sorted({row.model_label for row in rows})
    families = sorted({row.family for row in rows})
    failure_types = sorted({row.failure_type for row in rows})
    answer_wrong_count = sum(row.review_kind == "answer_wrong" for row in rows)
    format_only_count = sum(row.review_kind == "format_only" for row in rows)
    body_rows = "\n".join(_render_row(row) for row in rows)
    warning_html = _render_warnings(warnings)
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>ObviousBench Wrong Answer Review</title>
  <style>
    :root {{
      color-scheme: light;
      --ink: #17202a;
      --muted: #5e6874;
      --line: #d8dee6;
      --panel: #f7f9fb;
      --blue: #145a9e;
      --red: #a4312a;
      --amber: #8a5a00;
      --green: #236b3d;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: Inter, ui-sans-serif, system-ui, -apple-system,
        BlinkMacSystemFont, "Segoe UI", sans-serif;
      color: var(--ink);
      background: #fff;
      line-height: 1.45;
    }}
    header {{
      padding: 28px 32px 20px;
      border-bottom: 1px solid var(--line);
      background: linear-gradient(180deg, #fff 0%, #f8fafc 100%);
    }}
    h1 {{
      margin: 0 0 8px;
      font-size: 28px;
      letter-spacing: 0;
    }}
    .lede {{
      max-width: 1000px;
      margin: 0;
      color: var(--muted);
      font-size: 14px;
    }}
    main {{ padding: 22px 32px 40px; }}
    .cards {{
      display: grid;
      grid-template-columns: repeat(5, minmax(130px, 1fr));
      gap: 10px;
      max-width: 1100px;
      margin-bottom: 18px;
    }}
    .metric {{
      border: 1px solid var(--line);
      background: var(--panel);
      border-radius: 6px;
      padding: 10px 12px;
    }}
    .metric strong {{
      display: block;
      font-size: 22px;
      line-height: 1.1;
    }}
    .metric span {{
      color: var(--muted);
      font-size: 12px;
    }}
    .controls {{
      display: grid;
      grid-template-columns: minmax(220px, 1.7fr) repeat(4, minmax(150px, 1fr));
      gap: 10px;
      align-items: end;
      margin: 0 0 14px;
      max-width: 1350px;
    }}
    label {{
      display: grid;
      gap: 4px;
      color: var(--muted);
      font-size: 12px;
      font-weight: 650;
    }}
    input, select {{
      width: 100%;
      min-height: 36px;
      border: 1px solid var(--line);
      border-radius: 5px;
      padding: 7px 9px;
      color: var(--ink);
      background: #fff;
      font: inherit;
      font-size: 13px;
    }}
    .visible-count {{
      margin: 0 0 12px;
      color: var(--muted);
      font-size: 13px;
    }}
    .warnings {{
      max-width: 1100px;
      margin: 0 0 16px;
      padding: 10px 12px;
      border-left: 4px solid var(--amber);
      background: #fff8e8;
      color: #563b04;
      font-size: 13px;
    }}
    .table-wrap {{
      width: 100%;
      overflow-x: auto;
      border: 1px solid var(--line);
      border-radius: 7px;
    }}
    table {{
      width: 100%;
      min-width: 1180px;
      border-collapse: collapse;
      font-size: 13px;
    }}
    th {{
      position: sticky;
      top: 0;
      z-index: 1;
      text-align: left;
      color: #334155;
      background: #eef3f8;
      border-bottom: 1px solid var(--line);
      padding: 9px 10px;
      font-size: 12px;
    }}
    td {{
      vertical-align: top;
      border-bottom: 1px solid #e9edf2;
      padding: 10px;
    }}
    tr:last-child td {{ border-bottom: 0; }}
    tr[data-kind="answer_wrong"] .kind {{ color: var(--red); }}
    tr[data-kind="format_only"] .kind {{ color: var(--amber); }}
    .kind, .mono {{
      font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
      font-size: 12px;
    }}
    .model {{ min-width: 190px; font-weight: 650; }}
    .sample {{ max-width: 260px; overflow-wrap: anywhere; }}
    .answer-cell {{ min-width: 330px; }}
    .answer-grid {{
      display: grid;
      grid-template-columns: 78px 1fr;
      gap: 4px 8px;
      margin-bottom: 8px;
    }}
    .answer-grid span {{
      color: var(--muted);
      font-size: 12px;
    }}
    code {{
      white-space: pre-wrap;
      overflow-wrap: anywhere;
      color: #0f172a;
      background: #f1f5f9;
      border-radius: 4px;
      padding: 1px 4px;
    }}
    details {{
      margin-top: 8px;
      max-width: 760px;
    }}
    summary {{
      cursor: pointer;
      color: var(--blue);
      font-weight: 650;
    }}
    pre {{
      max-height: 360px;
      overflow: auto;
      white-space: pre-wrap;
      overflow-wrap: anywhere;
      border: 1px solid var(--line);
      border-radius: 5px;
      background: #fbfdff;
      padding: 10px;
      font-size: 12px;
    }}
    button {{
      min-height: 30px;
      border: 1px solid var(--line);
      border-radius: 5px;
      background: #fff;
      color: var(--blue);
      font-weight: 650;
      cursor: pointer;
    }}
    button:hover {{ border-color: var(--blue); }}
    @media (max-width: 960px) {{
      header, main {{ padding-left: 18px; padding-right: 18px; }}
      .cards {{ grid-template-columns: repeat(2, minmax(130px, 1fr)); }}
      .controls {{ grid-template-columns: 1fr; }}
    }}
  </style>
</head>
<body>
  <header>
    <h1>ObviousBench Wrong Answer Review</h1>
    <p class="lede">
      Combined review queue for final-sweep scored failures. Rows include answer-wrong and
      format-only strict failures; provider errors are excluded because there is no model answer
      to grade.
    </p>
  </header>
  <main>
    <section class="cards" aria-label="Summary metrics">
      <div class="metric"><strong>{len(rows)}</strong><span>review rows</span></div>
      <div class="metric"><strong>{answer_wrong_count}</strong><span>answer-wrong rows</span></div>
      <div class="metric"><strong>{format_only_count}</strong><span>format-only rows</span></div>
      <div class="metric"><strong>{len(models)}</strong><span>models</span></div>
      <div class="metric"><strong>{len(families)}</strong><span>families</span></div>
    </section>
    {warning_html}
    <section class="controls" aria-label="Filters">
      <label>Search
        <input id="search" type="search" placeholder="model, sample, answer, question, raw output">
      </label>
      <label>Model
        <select id="modelFilter">{_options(models)}</select>
      </label>
      <label>Family
        <select id="familyFilter">{_options(families)}</select>
      </label>
      <label>Failure Type
        <select id="failureFilter">{_options(failure_types)}</select>
      </label>
      <label>Review Kind
        <select id="kindFilter">
          <option value="">All</option>
          <option value="answer_wrong">Answer wrong</option>
          <option value="format_only">Format only</option>
        </select>
      </label>
    </section>
    <p class="visible-count"><span id="visibleCount">{len(rows)}</span> visible row(s)</p>
    <div class="table-wrap">
      <table>
        <thead>
          <tr>
            <th>Model</th>
            <th>Kind</th>
            <th>Family</th>
            <th>Sample</th>
            <th>Answer / Evidence</th>
            <th>Reference</th>
          </tr>
        </thead>
        <tbody>
          {body_rows}
        </tbody>
      </table>
    </div>
  </main>
  <script>
    const rows = Array.from(document.querySelectorAll("tbody tr"));
    const search = document.getElementById("search");
    const modelFilter = document.getElementById("modelFilter");
    const familyFilter = document.getElementById("familyFilter");
    const failureFilter = document.getElementById("failureFilter");
    const kindFilter = document.getElementById("kindFilter");
    const visibleCount = document.getElementById("visibleCount");

    function applyFilters() {{
      const q = search.value.trim().toLowerCase();
      const model = modelFilter.value;
      const family = familyFilter.value;
      const failure = failureFilter.value;
      const kind = kindFilter.value;
      let visible = 0;
      rows.forEach((row) => {{
        const show =
          (!q || row.dataset.search.includes(q)) &&
          (!model || row.dataset.model === model) &&
          (!family || row.dataset.family === family) &&
          (!failure || row.dataset.failure === failure) &&
          (!kind || row.dataset.kind === kind);
        row.hidden = !show;
        if (show) visible += 1;
      }});
      visibleCount.textContent = visible.toString();
    }}

    function copyReference(button) {{
      navigator.clipboard.writeText(button.dataset.reference);
      const previous = button.textContent;
      button.textContent = "Copied";
      setTimeout(() => {{ button.textContent = previous; }}, 900);
    }}

    [search, modelFilter, familyFilter, failureFilter, kindFilter].forEach((control) => {{
      control.addEventListener("input", applyFilters);
      control.addEventListener("change", applyFilters);
    }});
  </script>
</body>
</html>
"""


def _render_row(row: _ReviewRow) -> str:
    searchable = " ".join(
        (
            row.model_label,
            row.model,
            row.family,
            row.subfamily,
            row.sample_id,
            row.failure_type,
            row.expected_answer,
            row.extracted_answer,
            row.raw_output,
            row.question,
            row.why_obvious,
        )
    ).casefold()
    return f"""<tr
  data-model="{_attr(row.model_label)}"
  data-family="{_attr(row.family)}"
  data-failure="{_attr(row.failure_type)}"
  data-kind="{_attr(row.review_kind)}"
  data-search="{_attr(searchable)}">
  <td class="model">
    {_text(row.model_label)}<br><span class="mono">{_text(row.model)}</span>
  </td>
  <td>
    <span class="kind">{_text(row.review_kind)}</span><br>
    <span class="mono">{_text(row.failure_type)}</span>
  </td>
  <td>{_text(row.family)}<br><span class="mono">{_text(row.subfamily)}</span></td>
  <td class="sample mono">{_text(row.sample_id)}</td>
  <td class="answer-cell">
    <div class="answer-grid">
      <span>Expected</span><code>{_text(row.expected_answer)}</code>
      <span>Extracted</span><code>{_text(row.extracted_answer)}</code>
      <span>Flags</span>
      <code>
        answer={_text(row.answer_correct)}
        format={_text(row.format_correct)}
        strict={_text(row.strict_correct)}
      </code>
    </div>
    <details>
      <summary>Question and raw output</summary>
      <p>{_text(row.question)}</p>
      <pre>{_text(row.raw_output)}</pre>
      <p><strong>Why obvious:</strong> {_text(row.why_obvious)}</p>
    </details>
  </td>
  <td>
    <button
      type="button"
      data-reference="{_attr(row.reference)}"
      onclick="copyReference(this)">
      Copy reference
    </button>
    <pre>{_text(row.reference)}</pre>
    <span class="mono">{_text(row.log_file)}</span>
  </td>
</tr>"""


def _render_warnings(warnings: tuple[str, ...]) -> str:
    if not warnings:
        return ""
    items = "".join(f"<li>{_text(warning)}</li>" for warning in warnings)
    return (
        '<section class="warnings"><strong>Log selection warnings</strong>'
        f"<ul>{items}</ul></section>"
    )


def _options(values: list[str]) -> str:
    options = ['<option value="">All</option>']
    options.extend(f'<option value="{_attr(value)}">{_text(value)}</option>' for value in values)
    return "\n".join(options)


def _csv_int(row: dict[str, str], field: str) -> int:
    value = (row.get(field) or "0").strip()
    return int(float(value)) if value else 0


def _text(value: str) -> str:
    return html.escape(value, quote=False)


def _attr(value: str) -> str:
    return html.escape(value, quote=True)
