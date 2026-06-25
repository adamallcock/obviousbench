"""Static benchmark report generation from comparison summaries."""

from __future__ import annotations

import csv
import html
import json
import re
from dataclasses import dataclass
from pathlib import Path

from obviousbench.analysis.statistics import wilson_interval


@dataclass(frozen=True)
class BenchmarkReportInputs:
    comparison_dir: Path
    output_dir: Path
    generated_on: str
    title: str = "ObviousBench Report"


@dataclass(frozen=True)
class BenchmarkReportPaths:
    html: Path
    leaderboard_csv: Path
    leaderboard_md: Path
    family_heatmap_csv: Path


def build_benchmark_report(inputs: BenchmarkReportInputs) -> BenchmarkReportPaths:
    """Build a dependency-free HTML report plus machine-readable tables."""
    inputs.output_dir.mkdir(parents=True, exist_ok=True)
    comparison_rows = _read_csv(inputs.comparison_dir / "comparison.csv")
    family_rows = _read_csv(inputs.comparison_dir / "family_comparison.csv")
    effort_rows = _read_optional_csv(inputs.comparison_dir / "effort_curve.csv")
    metamorphic_rows = _read_optional_csv(
        inputs.comparison_dir / "metamorphic_consistency.csv"
    )

    leaderboard = _leaderboard_rows(comparison_rows)
    family_heatmap = _family_heatmap_rows(family_rows)

    paths = BenchmarkReportPaths(
        html=inputs.output_dir / "report.html",
        leaderboard_csv=inputs.output_dir / "leaderboard.csv",
        leaderboard_md=inputs.output_dir / "leaderboard.md",
        family_heatmap_csv=inputs.output_dir / "family-heatmap.csv",
    )
    _write_csv(paths.leaderboard_csv, leaderboard)
    _write_csv(paths.family_heatmap_csv, family_heatmap)
    paths.leaderboard_md.write_text(_leaderboard_markdown(leaderboard), encoding="utf-8")
    paths.html.write_text(
        _html_report(
            title=inputs.title,
            generated_on=inputs.generated_on,
            leaderboard=leaderboard,
            family_heatmap=family_heatmap,
            effort_rows=effort_rows,
            metamorphic_rows=metamorphic_rows,
        ),
        encoding="utf-8",
    )
    return paths


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _read_optional_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    return _read_csv(path)


def _leaderboard_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    max_scored_samples = max((_int(row.get("scored_samples")) for row in rows), default=0)
    sorted_rows = sorted(
        rows,
        key=lambda row: (
            _int(row.get("scored_samples")) != max_scored_samples,
            -_float(row.get("answer_accuracy") or row.get("accuracy")),
            _int(row.get("provider_errors")),
            _float(row.get("estimated_cost_usd")),
            row.get("label", ""),
        ),
    )
    leaderboard: list[dict[str, str]] = []
    rank = 0
    for row in sorted_rows:
        comparable = (
            max_scored_samples > 0
            and _int(row.get("scored_samples")) == max_scored_samples
        )
        if comparable:
            rank += 1
            rank_value = str(rank)
        else:
            rank_value = ""
        correct = _int(row.get("answer_correct") or row.get("correct"))
        cost = _optional_float(row.get("estimated_cost_usd"))
        total_tokens = _int(row.get("total_tokens"))
        tokens_per_correct = _optional_float(row.get("tokens_per_correct"))
        if tokens_per_correct is None and correct:
            tokens_per_correct = total_tokens / correct
        cost_per_correct = _optional_float(row.get("cost_per_correct_usd"))
        if cost_per_correct is None and cost is not None and correct:
            cost_per_correct = cost / correct
        leaderboard.append(
            {
                "rank": rank_value,
                "label": row.get("label", ""),
                "display_label": _display_label(row),
                "model": row.get("model", ""),
                "thinking_level": _thinking_level(row),
                "barrage_profile": row.get("barrage_profile", ""),
                "accuracy_pct": _format_percent(
                    row.get("answer_accuracy") or row.get("accuracy")
                ),
                "accuracy_ci_95": _answer_accuracy_interval(row),
                "answer_accuracy_pct": _format_percent(
                    row.get("answer_accuracy") or row.get("accuracy")
                ),
                "format_accuracy_pct": _format_percent(
                    row.get("format_accuracy") or row.get("accuracy")
                ),
                "strict_accuracy_pct": _format_percent(
                    row.get("strict_accuracy") or row.get("accuracy")
                ),
                "obvious_failure_rate_pct": _format_percent(
                    row.get("obvious_failure_rate")
                ),
                "correct": str(correct),
                "answer_correct": str(correct),
                "format_correct": str(_int(row.get("format_correct") or row.get("correct"))),
                "strict_correct": str(_int(row.get("strict_correct") or row.get("correct"))),
                "scored_samples": str(_int(row.get("scored_samples"))),
                "provider_errors": str(_int(row.get("provider_errors"))),
                "timeouts": str(_int(row.get("timeouts"))),
                "total_tokens": str(total_tokens),
                "total_tokens_display": _format_tokens_k(total_tokens),
                "estimated_cost_usd": _format_money(cost),
                "cost_per_correct_usd": _format_money(cost_per_correct),
                "tokens_per_correct": _format_integer(tokens_per_correct),
                "overthinking_index": _format_number(
                    _optional_float(row.get("overthinking_index"))
                ),
                "reasoning_token_source": _reasoning_token_source(row),
                "cost_warnings": row.get("cost_warnings", ""),
                "summary_dir": row.get("summary_dir", ""),
            }
        )
    return leaderboard


def _family_heatmap_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    heatmap: list[dict[str, str]] = []
    for row in sorted(rows, key=lambda item: (item.get("label", ""), item.get("family", ""))):
        samples = _int(row.get("samples"))
        scored_samples = _int(row.get("scored_samples"))
        denominator = scored_samples if row.get("scored_samples", "") != "" else samples
        correct = _int(row.get("correct"))
        heatmap.append(
            {
                "label": row.get("label", ""),
                "family": row.get("family", ""),
                "accuracy_pct": (
                    f"{(correct / denominator * 100):.2f}" if denominator else ""
                ),
                "correct": str(correct),
                "samples": str(samples),
                "scored_samples": (
                    str(scored_samples) if row.get("scored_samples", "") != "" else ""
                ),
                "provider_errors": row.get("provider_errors", ""),
                "timeouts": row.get("timeouts", ""),
                "failures": str(_int(row.get("failures"))),
                "estimated_cost_usd": row.get("estimated_cost_usd", ""),
            }
        )
    return heatmap


def _write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def _leaderboard_markdown(rows: list[dict[str, str]]) -> str:
    headers = [
        "Rank",
        "Model",
        "Answer Accuracy",
        "95% CI",
        "Answer",
        "Format",
        "Strict",
        "Cost",
        "Tokens",
        "Tokens / Correct",
        "Cost / Correct",
        "Overthinking",
        "Provider Errors",
    ]
    lines = [
        "# ObviousBench Leaderboard",
        "",
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    row["rank"] or "n/a",
                    row["display_label"],
                    f"{row['accuracy_pct']}%",
                    row["accuracy_ci_95"] or "n/a",
                    f"{row['answer_accuracy_pct']}%",
                    f"{row['format_accuracy_pct']}%",
                    f"{row['strict_accuracy_pct']}%",
                    _display_money(row["estimated_cost_usd"]),
                    row["total_tokens_display"],
                    row["tokens_per_correct"] or "n/a",
                    _display_money(row["cost_per_correct_usd"]),
                    row["overthinking_index"] or "n/a",
                    row["provider_errors"],
                ]
            )
            + " |"
        )
    return "\n".join(lines) + "\n"


def _html_report(
    *,
    title: str,
    generated_on: str,
    leaderboard: list[dict[str, str]],
    family_heatmap: list[dict[str, str]],
    effort_rows: list[dict[str, str]],
    metamorphic_rows: list[dict[str, str]],
) -> str:
    return "\n".join(
        [
            "<!doctype html>",
            '<html lang="en">',
            "<head>",
            '<meta charset="utf-8">',
            '<meta name="viewport" content="width=device-width, initial-scale=1">',
            f"<title>{html.escape(title)}</title>",
            "<style>",
            _css(),
            "</style>",
            "</head>",
            "<body>",
            "<main>",
            f"<h1>{html.escape(title)}</h1>",
            f'<p class="meta">Generated on {html.escape(generated_on)}</p>',
            _summary_cards(leaderboard),
            _report_controls(leaderboard),
            '<section class="chart-block" id="leaderboard">',
            '<h2 class="ob-chart-title">Leaderboard</h2>',
            _leaderboard_table(leaderboard),
            "</section>",
            _scoring_coverage_note(leaderboard),
            '<p class="note">Intervals are Wilson 95% confidence intervals over '
            "scored final attempts. Provider errors, refusals, and timeouts count "
            "as incorrect attempts after retries, while their counts remain visible "
            "as diagnostics. Close rankings should be treated as directional rather "
            "than decisive.</p>",
            _uncertainty_cautions(leaderboard),
            _effort_warnings(effort_rows),
            '<section class="chart-block" id="tokens-frontier">',
            '<h2 class="ob-chart-title">Accuracy vs tokens</h2>',
            '<p class="chart-mode">Mode: Answer</p>',
            _tokens_scatter_svg(leaderboard),
            _scatter_omission_note(leaderboard, "tokens_per_correct"),
            "</section>",
            '<section class="chart-block" id="cost-frontier">',
            '<h2 class="ob-chart-title">Answer Accuracy vs Run Cost</h2>',
            '<p class="chart-mode">Mode: Answer</p>',
            _scatter_svg(leaderboard),
            _scatter_omission_note(leaderboard, "estimated_cost_usd"),
            "</section>",
            '<section class="chart-block" id="accuracy-bars">',
            '<h2 class="ob-chart-title">Accuracy Leaderboard</h2>',
            '<p class="chart-mode">Mode: Answer</p>',
            _bar_svg(leaderboard),
            "</section>",
            '<section class="chart-block" id="family-accuracy">',
            '<h2 class="ob-chart-title">Family Accuracy Heatmap</h2>',
            _heatmap_table(family_heatmap),
            "</section>",
            '<section class="chart-block" id="metamorphic-consistency">',
            '<h2 class="ob-chart-title">Metamorphic Consistency</h2>',
            _metamorphic_consistency_table(metamorphic_rows),
            "</section>",
            '<section class="chart-block" id="provider-errors">',
            '<h2 class="ob-chart-title">Provider Errors</h2>',
            _provider_errors(leaderboard),
            "</section>",
            '<section class="chart-block" id="reading-notes">',
            '<h2 class="ob-chart-title">Reading Notes</h2>',
            "<ul>",
            "<li>Rank scored runs by accuracy, while keeping provider-error rows visible.</li>",
            "<li>Show cost, token, cost-per-correct, and overthinking tradeoffs "
            "beside accuracy.</li>",
            "<li>Thinking labels describe explicit request settings when present, "
            "or provider default when no setting was sent. Reported reasoning "
            "tokens are usage telemetry, not a configured thinking level.</li>",
            "<li>Overthinking index is reasoning tokens divided by visible output "
            "tokens. High values mean the model spent many hidden reasoning tokens "
            "per visible token. Missing reasoning tokens are provider-dependent.</li>",
            "<li>Use family slices to reveal where aggregate scores hide weak spots.</li>",
            "</ul>",
            "</section>",
            _leaderboard_json_script(leaderboard),
            _interaction_script(),
            "</main>",
            "</body>",
            "</html>",
        ]
    )


def _report_controls(rows: list[dict[str, str]]) -> str:
    selected = _selected_row(rows)
    provider_options = [
        '<option value="all">All providers</option>',
        *[
            f'<option value="{html.escape(provider, quote=True)}">'
            f"{html.escape(provider)}</option>"
            for provider in sorted({_provider_name(row["model"]) for row in rows})
        ],
    ]
    selected_label = html.escape(selected.get("display_label", "No scored rows"))
    selected_accuracy = html.escape(selected.get("answer_accuracy_pct", "n/a"))
    selected_cost = html.escape(_display_money(selected.get("estimated_cost_usd", "")))
    selected_tokens = html.escape(selected.get("tokens_per_correct", "n/a") or "n/a")
    return (
        '<section class="report-controls" aria-label="Report controls">'
        '<div class="control-group">'
        '<span class="control-label">Metric</span>'
        '<div class="metric-toggle" role="group" aria-label="Leaderboard metric">'
        '<button type="button" data-metric="answer" aria-pressed="true">Answer</button>'
        '<button type="button" data-metric="format" aria-pressed="false">Format</button>'
        '<button type="button" data-metric="strict" aria-pressed="false">Strict</button>'
        "</div>"
        "</div>"
        '<label class="control-inline">'
        '<input type="checkbox" id="comparable-only" checked> Comparable only'
        "</label>"
        '<label class="control-select">'
        '<span class="control-label">Provider</span>'
        f'<select id="provider-filter">{"".join(provider_options)}</select>'
        "</label>"
        '<aside id="selected-model-panel" class="selected-model-panel" aria-live="polite">'
        "<span>Why this row matters</span>"
        f"<strong>{selected_label}</strong>"
        f"<p>Answer {selected_accuracy}% with {selected_cost} run cost and "
        f"{selected_tokens} tokens per correct answer.</p>"
        "</aside>"
        "</section>"
        "<noscript>"
        '<p class="note">Interactive controls are optional; the full static tables '
        "and charts are available without JavaScript.</p>"
        "</noscript>"
    )


def _selected_row(rows: list[dict[str, str]]) -> dict[str, str]:
    return next((row for row in rows if row["rank"]), rows[0] if rows else {})


def _leaderboard_json_script(rows: list[dict[str, str]]) -> str:
    data = [
        {
            **row,
            "provider": _provider_name(row["model"]),
            "comparable": bool(row["rank"]),
        }
        for row in rows
    ]
    payload = json.dumps(data, ensure_ascii=False, indent=2).replace("</", "<\\/")
    return f'<script type="application/json" id="leaderboard-data">{payload}</script>'


def _interaction_script() -> str:
    return (
        "<script>"
        "const leaderboardDataNode = document.getElementById('leaderboard-data');"
        "const leaderboard = leaderboardDataNode ? "
        "JSON.parse(leaderboardDataNode.textContent) : [];"
        "const metricButtons = document.querySelectorAll('[data-metric]');"
        "const comparableOnly = document.getElementById('comparable-only');"
        "const providerFilter = document.getElementById('provider-filter');"
        "const panel = document.getElementById('selected-model-panel');"
        "const metricDatasetKeys = {answer: 'metricAnswer', "
        "format: 'metricFormat', strict: 'metricStrict'};"
        "let activeMetric = 'answer';"
        "function setMetric(metric) {"
        "activeMetric = metric;"
        "document.body.dataset.metric = metric;"
        "metricButtons.forEach((button) => {"
        "button.setAttribute('aria-pressed', button.dataset.metric === metric ? 'true' : 'false');"
        "});"
        "document.querySelectorAll('#leaderboard-table tbody tr').forEach((row) => {"
        "const value = row.dataset[metricDatasetKeys[metric]];"
        "const target = row.querySelector('[data-metric-value]');"
        "if (target && value) target.textContent = `${value}%`;"
        "});"
        "const selected = document.querySelector("
        "'#leaderboard-table tbody tr.selected-row:not([hidden])') || "
        "document.querySelector('#leaderboard-table tbody tr:not([hidden])');"
        "if (selected) selectModel(selected.dataset.label);"
        "}"
        "function selectModel(label) {"
        "const row = leaderboard.find((item) => "
        "item.display_label === label || item.label === label);"
        "if (!row) return;"
        "document.querySelectorAll('#leaderboard-table tbody tr').forEach((tableRow) => {"
        "tableRow.classList.toggle('selected-row', tableRow.dataset.label === row.display_label);"
        "});"
        "if (!panel) return;"
        "const value = activeMetric === 'format' ? row.format_accuracy_pct : "
        "activeMetric === 'strict' ? row.strict_accuracy_pct : row.answer_accuracy_pct;"
        "panel.replaceChildren();"
        "const eyebrow = document.createElement('span');"
        "eyebrow.textContent = 'Why this row matters';"
        "const title = document.createElement('strong');"
        "title.textContent = row.display_label;"
        "const body = document.createElement('p');"
        "body.textContent = `${value}% ${activeMetric} accuracy; "
        "${row.cost_per_correct_usd ? '$' + Number(row.cost_per_correct_usd).toFixed(6) : 'n/a'} "
        "per correct answer; ${row.provider_errors} provider errors.`;"
        "panel.append(eyebrow, title, body);"
        "}"
        "function applyFilters() {"
        "const comparable = comparableOnly ? comparableOnly.checked : false;"
        "const provider = providerFilter ? providerFilter.value : 'all';"
        "document.querySelectorAll('#leaderboard-table tbody tr').forEach((row) => {"
        "const hiddenByComparable = comparable && row.dataset.comparable !== 'true';"
        "const hiddenByProvider = provider !== 'all' && row.dataset.provider !== provider;"
        "row.hidden = hiddenByComparable || hiddenByProvider;"
        "});"
        "const visible = document.querySelector('#leaderboard-table tbody tr:not([hidden])');"
        "if (visible) selectModel(visible.dataset.label);"
        "}"
        "metricButtons.forEach((button) => "
        "button.addEventListener('click', () => setMetric(button.dataset.metric)));"
        "if (comparableOnly) comparableOnly.addEventListener('change', applyFilters);"
        "if (providerFilter) providerFilter.addEventListener('change', applyFilters);"
        "document.querySelectorAll('#leaderboard-table tbody tr').forEach((row) => {"
        "row.addEventListener('click', () => selectModel(row.dataset.label));"
        "});"
        "applyFilters();"
        "setMetric('answer');"
        "</script>"
    )


def _summary_cards(rows: list[dict[str, str]]) -> str:
    scored = [row for row in rows if row["rank"]]
    best = scored[0] if scored else {}
    cheapest_correct = min(
        scored,
        key=lambda row: _optional_float(row["cost_per_correct_usd"]) or float("inf"),
        default={},
    )
    fewest_tokens_correct = min(
        scored,
        key=lambda row: _optional_float(row["tokens_per_correct"]) or float("inf"),
        default={},
    )
    best_label = html.escape(best.get("display_label", "n/a"))
    cheapest_label = html.escape(cheapest_correct.get("display_label", "n/a"))
    fewest_tokens_label = html.escape(
        fewest_tokens_correct.get("display_label", "n/a")
    )
    cost_per_correct = html.escape(
        _display_money(cheapest_correct.get("cost_per_correct_usd", ""))
    )
    tokens_per_correct = html.escape(
        fewest_tokens_correct.get("tokens_per_correct", "n/a")
    )
    return (
        '<section class="cards">'
        f"<div><span>Best Answer Accuracy</span><strong>{best_label}</strong>"
        f'<em>{html.escape(best.get("accuracy_pct", ""))}%</em></div>'
        f"<div><span>Lowest Cost / Correct</span><strong>{cheapest_label}</strong>"
        f"<em>{cost_per_correct}</em></div>"
        f"<div><span>Lowest Tokens / Correct</span><strong>{fewest_tokens_label}</strong>"
        f"<em>{tokens_per_correct}</em></div>"
        f"<div><span>Runs</span><strong>{len(rows)}</strong><em>{len(scored)} comparable</em></div>"
        "</section>"
    )


def _leaderboard_table(rows: list[dict[str, str]]) -> str:
    headers = [
        "Rank",
        "Model",
        "Answer Accuracy",
        "95% CI",
        "Answer",
        "Format",
        "Strict",
        "Correct",
        "Run Cost",
        "Cost / Correct",
        "Tokens / Correct",
        "Overthinking index",
        "Tokens",
        "Provider Errors",
    ]
    body = []
    selected = _selected_row(rows)
    for row in rows:
        provider = _provider_name(row["model"])
        selected_class = (
            ' class="selected-row"'
            if row.get("display_label") == selected.get("display_label")
            else ""
        )
        row_attrs = (
            selected_class
            + f' data-label="{html.escape(row["display_label"], quote=True)}"'
            + f' data-provider="{html.escape(provider, quote=True)}"'
            + f' data-comparable="{str(bool(row["rank"])).lower()}"'
            + f' data-metric-answer="{html.escape(row["answer_accuracy_pct"], quote=True)}"'
            + f' data-metric-format="{html.escape(row["format_accuracy_pct"], quote=True)}"'
            + f' data-metric-strict="{html.escape(row["strict_accuracy_pct"], quote=True)}"'
        )
        body.append(
            f"<tr{row_attrs}>"
            f"<td>{html.escape(row['rank'] or 'n/a')}</td>"
            f"<td>{html.escape(row['display_label'])}<br><code>{html.escape(row['model'])}</code></td>"
            f'<td data-metric-value>{html.escape(row["answer_accuracy_pct"])}%</td>'
            f"<td>{html.escape(row['accuracy_ci_95'] or 'n/a')}</td>"
            f"<td>{html.escape(row['answer_accuracy_pct'])}%</td>"
            f"<td>{html.escape(row['format_accuracy_pct'])}%</td>"
            f"<td>{html.escape(row['strict_accuracy_pct'])}%</td>"
            f"<td>{html.escape(row['correct'])}/{html.escape(row['scored_samples'])}</td>"
            f"<td>{html.escape(_display_money(row['estimated_cost_usd']))}</td>"
            f"<td>{html.escape(_display_money(row['cost_per_correct_usd']))}</td>"
            f"<td>{html.escape(row['tokens_per_correct'] or 'n/a')}</td>"
            f"<td>{html.escape(row['overthinking_index'] or 'n/a')}</td>"
            f"<td>{html.escape(row['total_tokens_display'])}</td>"
            f"<td>{html.escape(row['provider_errors'])}</td>"
            "</tr>"
        )
    return _table(headers, body).replace(
        "<table>",
        '<table id="leaderboard-table" class="leaderboard-table">',
        1,
    )


def _scoring_coverage_note(rows: list[dict[str, str]]) -> str:
    scored_counts = [_int(row.get("scored_samples")) for row in rows]
    max_scored = max(scored_counts, default=0)
    comparable = sum(count == max_scored and count > 0 for count in scored_counts)
    partial = sum(0 < count < max_scored for count in scored_counts)
    zero = sum(count == 0 for count in scored_counts)
    return (
        '<p class="note">Scoring coverage: '
        f"{comparable} runs completed the full {max_scored}-question attempted set, "
        f"{partial} runs completed a partial set, and {zero} runs completed zero "
        "scored final attempts. Only full-set rows receive ranks.</p>"
    )


def _uncertainty_cautions(rows: list[dict[str, str]]) -> str:
    scored = [row for row in rows if row["rank"]]
    warnings = []
    for left, right in zip(scored, scored[1:], strict=False):
        left_accuracy = (_optional_float(left["accuracy_pct"]) or 0.0) / 100
        right_accuracy = (_optional_float(right["accuracy_pct"]) or 0.0) / 100
        max_half_width = max(_ci_half_width(left), _ci_half_width(right))
        if max_half_width > 0 and abs(left_accuracy - right_accuracy) < max_half_width:
            warnings.append(
                f"{left['label']} and {right['label']} are closer than the larger "
                "accuracy interval half-width."
            )
    if not warnings:
        return ""
    items = "".join(f"<li>{html.escape(warning)}</li>" for warning in warnings)
    return (
        '<section class="note"><strong>Accuracy interval cautions</strong><ul>'
        + items
        + "</ul></section>"
    )


def _ci_half_width(row: dict[str, str]) -> float:
    interval = row.get("accuracy_ci_95", "")
    normalized = interval.replace(" ", "").replace("%", "")
    if "-" not in normalized:
        return 0.0
    low_raw, high_raw = normalized.split("-", maxsplit=1)
    low = (_optional_float(low_raw) or 0.0) / 100
    high = (_optional_float(high_raw) or 0.0) / 100
    accuracy = (_optional_float(row.get("accuracy_pct")) or 0.0) / 100
    return max(abs(accuracy - low), abs(high - accuracy))


def _scatter_svg(rows: list[dict[str, str]]) -> str:
    points = _scatter_points(rows, "estimated_cost_usd")
    if not points:
        return "<p>No costed scored runs available.</p>"
    return _scatter_plot_svg(
        points=points,
        aria_label="Answer accuracy versus total estimated run cost scatter plot",
        x_label="Estimated total run cost, USD (80-question scored set)",
        x_formatter=_display_money,
        title_formatter=lambda row: _display_money(row["estimated_cost_usd"]),
    )


def _tokens_scatter_svg(rows: list[dict[str, str]]) -> str:
    points = _scatter_points(rows, "tokens_per_correct")
    if not points:
        return "<p>No token efficiency values available.</p>"
    return _scatter_plot_svg(
        points=points,
        aria_label="Answer accuracy versus tokens per correct answer scatter plot",
        x_label="Tokens per correct answer",
        x_formatter=_format_integer,
        title_formatter=lambda row: f"{row['tokens_per_correct']} tokens/correct",
    )


def _scatter_points(
    rows: list[dict[str, str]], x_key: str
) -> list[tuple[dict[str, str], float, float]]:
    return [
        (row, x_value, accuracy)
        for row in rows
        if row["rank"]
        for x_value in [_optional_float(row[x_key])]
        for accuracy in [_optional_float(row["accuracy_pct"])]
        if x_value is not None and accuracy is not None
    ]


def _scatter_plot_svg(
    *,
    points: list[tuple[dict[str, str], float, float]],
    aria_label: str,
    x_label: str,
    x_formatter,
    title_formatter,
) -> str:
    max_x = max(x_value for _, x_value, _ in points) or 1
    width, height = 860, 400
    left_pad, right_pad, top_pad, bottom_pad = 76, 168, 42, 68
    plot_width = width - left_pad - right_pad
    plot_height = height - top_pad - bottom_pad
    frontier_indexes = _pareto_frontier_indexes(points)
    positioned = []
    for index, (row, x_value, accuracy) in enumerate(points):
        x = left_pad + (x_value / max_x) * plot_width
        y = top_pad + (1 - accuracy / 100) * plot_height
        positioned.append((index, row, x_value, accuracy, x, y))
    frontier_line = _frontier_line_svg(
        [(x, y) for index, _, _, _, x, y in positioned if index in frontier_indexes]
    )
    marks = []
    label_boxes: list[tuple[float, float, float, float]] = []
    for index, row, _, _, x, y in positioned:
        raw_label = row.get("display_label") or row["label"]
        label = html.escape(raw_label)
        short_label = html.escape(_short_label(raw_label))
        provider = html.escape(_provider_class(row["model"]))
        point_class = f"point {provider}"
        if index in frontier_indexes:
            point_class += " frontier"
        label_x = x + 9
        label_y = y + 4
        label_width = min(len(_short_label(raw_label)), 28) * 6.5
        label_box = (label_x, label_y - 12, label_x + label_width, label_y + 4)
        label_collides = any(
            _boxes_overlap(label_box, previous_box) for previous_box in label_boxes
        )
        if not label_collides:
            label_boxes.append(label_box)
            label_text = (
                f'<text class="point-label" x="{label_x:.1f}" y="{label_y:.1f}">'
                f"{short_label}</text>"
            )
        else:
            label_text = (
                f'<title>{label} label hidden to avoid overlap</title>'
                '<text class="label-suppressed" aria-hidden="true"></text>'
            )
        marks.append(
            f'<circle class="{point_class}" data-provider="{provider.removeprefix("provider-")}" '
            f'cx="{x:.1f}" cy="{y:.1f}" r="6"><title>{label}: '
            f'{html.escape(_point_accuracy_label(row))}% answer accuracy at '
            f'{html.escape(title_formatter(row))}</title>'
            "</circle>"
            + label_text
        )
    return (
        f'<svg class="ob-report-chart ob-frontier-chart" viewBox="0 0 {width} {height}" role="img" '
        f'aria-label="{aria_label}">'
        + _scatter_axes_svg(
            width=width,
            height=height,
            left_pad=left_pad,
            right_pad=right_pad,
            top_pad=top_pad,
            bottom_pad=bottom_pad,
            max_x=max_x,
            x_label=x_label,
            x_formatter=x_formatter,
        )
        + frontier_line
        + '<g class="ob-direct-label">'
        + "".join(marks)
        + "</g>"
        + "</svg>"
    )


def _scatter_axes_svg(
    *,
    width: int,
    height: int,
    left_pad: int,
    right_pad: int,
    top_pad: int,
    bottom_pad: int,
    max_x: float,
    x_label: str,
    x_formatter,
) -> str:
    x_axis_y = height - bottom_pad
    y_axis_x = left_pad
    plot_width = width - left_pad - right_pad
    plot_height = height - top_pad - bottom_pad
    x_ticks = _nice_ticks(max_x, count=5)
    y_ticks = [50.0, 62.5, 75.0, 87.5, 100.0]
    parts = [
        f'<line x1="{left_pad}" y1="{x_axis_y}" x2="{width-right_pad}" y2="{x_axis_y}" />',
        f'<line x1="{y_axis_x}" y1="{top_pad}" x2="{y_axis_x}" y2="{x_axis_y}" />',
    ]
    for tick in x_ticks:
        x = left_pad + (tick / max_x) * plot_width if max_x else left_pad
        parts.append(
            f'<line class="grid-line" x1="{x:.1f}" y1="{top_pad}" '
            f'x2="{x:.1f}" y2="{x_axis_y}" />'
        )
        parts.append(f'<line x1="{x:.1f}" y1="{x_axis_y}" x2="{x:.1f}" y2="{x_axis_y + 5}" />')
        parts.append(
            f'<text class="tick-label" x="{x:.1f}" y="{x_axis_y + 20}" '
            f'text-anchor="middle">{html.escape(x_formatter(tick))}</text>'
        )
    for tick in y_ticks:
        y = top_pad + (1 - tick / 100) * plot_height
        parts.append(
            f'<line class="grid-line" x1="{y_axis_x}" y1="{y:.1f}" '
            f'x2="{width - right_pad}" y2="{y:.1f}" />'
        )
        parts.append(f'<line x1="{y_axis_x - 5}" y1="{y:.1f}" x2="{y_axis_x}" y2="{y:.1f}" />')
        parts.append(
            f'<text class="tick-label" x="{y_axis_x - 9}" y="{y + 4:.1f}" '
            f'text-anchor="end">{tick:.0f}%</text>'
        )
    parts.extend(
        [
            f'<text class="axis-label" x="{left_pad + plot_width / 2:.1f}" '
            f'y="{height - 10}" text-anchor="middle">{html.escape(x_label)}</text>',
            '<text class="axis-label" x="14" y="24">Answer accuracy</text>',
        ]
    )
    return "".join(parts)


def _nice_ticks(max_x: float, *, count: int) -> list[float]:
    if max_x <= 0 or count <= 1:
        return [0.0, max_x]
    return [max_x * index / (count - 1) for index in range(count)]


def _pareto_frontier_indexes(
    points: list[tuple[dict[str, str], float, float]]
) -> set[int]:
    best_accuracy = -1.0
    frontier_indexes: set[int] = set()
    for index, (_, _x_value, accuracy) in sorted(
        enumerate(points), key=lambda item: (item[1][1], -item[1][2])
    ):
        if accuracy > best_accuracy:
            frontier_indexes.add(index)
            best_accuracy = accuracy
    return frontier_indexes


def _frontier_line_svg(points: list[tuple[float, float]]) -> str:
    if len(points) < 2:
        return ""
    ordered = sorted(points)
    point_list = " ".join(f"{x:.1f},{y:.1f}" for x, y in ordered)
    return f'<polyline class="frontier-line" points="{point_list}" />'


def _provider_class(model: str) -> str:
    provider = model.split("/", maxsplit=1)[0] if model else "unknown"
    safe = "".join(character if character.isalnum() else "-" for character in provider)
    return f"provider-{safe.lower() or 'unknown'}"


def _provider_name(model: str) -> str:
    provider = model.split("/", maxsplit=1)[0] if model else "unknown"
    safe = "".join(character if character.isalnum() else "-" for character in provider)
    return safe.lower() or "unknown"


def _boxes_overlap(
    left: tuple[float, float, float, float], right: tuple[float, float, float, float]
) -> bool:
    return not (
        left[2] < right[0]
        or right[2] < left[0]
        or left[3] < right[1]
        or right[3] < left[1]
    )


def _scatter_omission_note(rows: list[dict[str, str]], x_key: str) -> str:
    omitted = [
        row
        for row in rows
        if not row["rank"] or _optional_float(row.get(x_key)) is None
    ]
    if not omitted:
        return ""
    return (
        '<p class="chart-note">Scatter charts omit '
        f"{len(omitted)} run{'s' if len(omitted) != 1 else ''} "
        "with incomplete samples or missing chart values.</p>"
    )


def _short_label(value: str, max_length: int = 28) -> str:
    if len(value) <= max_length:
        return value
    return value[: max_length - 1] + "..."


def _point_accuracy_label(row: dict[str, str]) -> str:
    return row.get("answer_accuracy_pct") or row.get("accuracy_pct", "")


def _bar_svg(rows: list[dict[str, str]]) -> str:
    scored = [row for row in rows if row["rank"]][:12]
    width = 920
    row_height = 34
    height = 36 + len(scored) * row_height
    bars = []
    for index, row in enumerate(scored):
        y = 24 + index * row_height
        value = _optional_float(row["accuracy_pct"]) or 0
        bar_width = value / 100 * 430
        bars.append(
            f'<text x="0" y="{y + 15}">{html.escape(_short_label(row["display_label"], 46))}</text>'
            f'<rect x="370" y="{y}" width="{bar_width:.1f}" height="18" />'
            f'<text x="{378 + bar_width:.1f}" y="{y + 14}">{value:.1f}%</text>'
        )
    return (
        f'<svg class="ob-report-chart ob-range-bar" viewBox="0 0 {width} {height}" role="img" '
        'aria-label="Accuracy leaderboard bar chart">'
        + "".join(bars)
        + "</svg>"
    )


def _heatmap_table(rows: list[dict[str, str]]) -> str:
    headers = ["Model", "Family", "Accuracy", "Failures", "Samples"]
    body = []
    for row in rows:
        accuracy = _optional_float(row["accuracy_pct"])
        shade = _heat_color(accuracy)
        body.append(
            "<tr>"
            f"<td>{html.escape(row['label'])}</td>"
            f"<td>{html.escape(row['family'])}</td>"
            f'<td style="background:{shade}">{html.escape(row["accuracy_pct"])}%</td>'
            f"<td>{html.escape(row['failures'])}</td>"
            f"<td>{html.escape(row['samples'])}</td>"
            "</tr>"
        )
    return '<div class="ob-segmented-bar">' + _table(headers, body) + "</div>"


def _provider_errors(rows: list[dict[str, str]]) -> str:
    error_rows = [
        row
        for row in rows
        if _int(row["provider_errors"]) or row.get("cost_warnings")
    ]
    if not error_rows:
        return "<p>No provider errors or cost warnings in this comparison.</p>"
    items = []
    for row in error_rows:
        details = row.get("cost_warnings") or "provider request errors"
        items.append(
            f"<li><strong>{html.escape(row['label'])}</strong>: "
            f"{html.escape(row['provider_errors'])} provider errors; "
            f"{html.escape(details)}</li>"
        )
    return "<ul>" + "".join(items) + "</ul>"


def _effort_warnings(rows: list[dict[str, str]]) -> str:
    warning_rows = [row for row in rows if row.get("efficiency_warning")]
    if not warning_rows:
        return ""
    items = []
    for row in warning_rows:
        label = row.get("model_base") or row.get("model") or "model"
        effort = row.get("reasoning_effort") or "unknown effort"
        warning = row.get("efficiency_warning", "")
        accuracy_delta = row.get("accuracy_delta_from_min_effort", "")
        token_delta = row.get("token_delta_from_min_effort", "")
        cost_delta = row.get("cost_delta_from_min_effort", "")
        details = (
            f"{warning}; effort={effort}; accuracy delta={accuracy_delta}; "
            f"token delta={token_delta}; cost delta={cost_delta}"
        )
        items.append(
            f"<li><strong>{html.escape(label)}</strong>: {html.escape(details)}</li>"
        )
    return (
        '<section class="note"><strong>Efficiency warnings</strong><ul>'
        + "".join(items)
        + "</ul></section>"
    )


def _metamorphic_consistency_table(rows: list[dict[str, str]]) -> str:
    if not rows:
        return "<p>No metamorphic groups were present in this comparison.</p>"
    headers = [
        "Model",
        "Family",
        "Groups",
        "Assessable",
        "Unassessable",
        "Consistency",
        "Mixed Outcomes",
        "Mixed Group IDs",
    ]
    body = []
    for row in rows:
        mixed_group_ids = row.get("mixed_group_ids", "")
        body.append(
            "<tr>"
            f"<td>{html.escape(row.get('label', ''))}</td>"
            f"<td>{html.escape(row.get('family', ''))}</td>"
            f"<td>{html.escape(row.get('groups', ''))}</td>"
            f"<td>{html.escape(row.get('assessable_groups', ''))}</td>"
            f"<td>{html.escape(row.get('unassessable_groups', ''))}</td>"
            f"<td>{html.escape(_display_percent(row.get('consistency_rate')))}</td>"
            f"<td>{html.escape(row.get('mixed_outcome_groups', ''))}</td>"
            f"<td>{html.escape(mixed_group_ids or 'n/a')}</td>"
            "</tr>"
        )
    return _table(headers, body)


def _table(headers: list[str], body_rows: list[str]) -> str:
    header = "".join(f"<th>{html.escape(value)}</th>" for value in headers)
    return (
        "<table><thead><tr>"
        + header
        + "</tr></thead><tbody>"
        + "".join(body_rows)
        + "</tbody></table>"
    )


def _css() -> str:
    return "\n".join(
        [
            ":root { --ink: #171b1f; --muted: #5e6673; --line: #d7dde5; "
            "--paper: #ffffff; --wash: #f4f2ed; --accent: #106a63; "
            "--accent-2: #c25a2a; --gold: #e7b84b; --rose: #b4475f; }",
            "body { margin: 0; font-family: Inter, ui-sans-serif, system-ui, "
            "sans-serif; color: var(--ink); background: var(--wash); }",
            "main { max-width: 1200px; margin: 0 auto; padding: 36px 24px 72px; }",
            "h1 { margin: 0 0 4px; font-size: 36px; line-height: 1.05; }",
            "h2 { margin: 0; font-size: 20px; line-height: 1.2; }",
            ".meta { color: var(--muted); margin-top: 0; }",
            ".cards { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); "
            "gap: 12px; margin: 24px 0; }",
            ".cards div { background: var(--paper); border: 1px solid var(--line); "
            "border-radius: 8px; padding: 14px 16px; box-shadow: 0 1px 0 #ebe7dd; }",
            ".cards span, .control-label, .selected-model-panel span { display: block; "
            "color: var(--muted); font-size: 12px; font-weight: 650; }",
            ".cards strong { display: block; margin-top: 6px; line-height: 1.25; }",
            ".cards em { display: block; margin-top: 4px; color: var(--muted); "
            "font-style: normal; }",
            ".report-controls { display: grid; grid-template-columns: minmax(220px, 1fr) "
            "minmax(170px, auto) minmax(180px, auto) minmax(260px, 1.1fr); gap: 12px; "
            "align-items: stretch; margin: 28px 0; }",
            ".control-group, .control-inline, .control-select, .selected-model-panel { "
            "background: var(--paper); border: 1px solid var(--line); border-radius: 8px; "
            "padding: 12px; }",
            ".metric-toggle { display: inline-grid; grid-template-columns: repeat(3, 1fr); "
            "gap: 4px; margin-top: 8px; width: 100%; }",
            ".metric-toggle button { appearance: none; border: 1px solid var(--line); "
            "background: #f9faf8; border-radius: 6px; color: var(--ink); cursor: pointer; "
            "font: inherit; font-size: 13px; padding: 7px 8px; }",
            ".metric-toggle button[aria-pressed='true'] { background: var(--accent); "
            "border-color: var(--accent); color: #fff; }",
            ".control-inline { display: flex; align-items: center; gap: 8px; "
            "font-size: 13px; font-weight: 650; }",
            ".control-select select { width: 100%; margin-top: 8px; border: 1px solid "
            "var(--line); border-radius: 6px; background: #fff; color: var(--ink); "
            "font: inherit; padding: 7px 8px; }",
            ".selected-model-panel strong { display: block; margin-top: 5px; line-height: 1.25; }",
            ".selected-model-panel p { margin: 6px 0 0; color: var(--muted); font-size: 13px; }",
            ".chart-block { margin-top: 26px; padding-top: 18px; border-top: 1px solid "
            "#ddd4c7; }",
            ".ob-chart-title { margin-bottom: 10px; }",
            ".chart-mode { display: inline-block; margin: 0 0 10px; color: var(--muted); "
            "font-size: 12px; font-weight: 650; }",
            "table { width: 100%; border-collapse: collapse; background: var(--paper); "
            "border: 1px solid var(--line); border-radius: 8px; overflow: hidden; }",
            "th, td { padding: 9px 10px; border-bottom: 1px solid #e8ebef; "
            "text-align: left; vertical-align: top; font-size: 13px; }",
            "th { background: #ece7dd; font-weight: 650; }",
            "tr.selected-row { background: #fff8df; box-shadow: inset 3px 0 0 var(--gold); }",
            "tr[hidden] { display: none; }",
            "code { color: var(--muted); font-size: 12px; }",
            "svg { width: 100%; height: auto; background: var(--paper); "
            "border: 1px solid var(--line); border-radius: 8px; padding: 12px; "
            "box-sizing: border-box; }",
            "svg rect { fill: var(--accent); }",
            "svg.ob-range-bar rect:nth-of-type(2n) { fill: var(--accent-2); }",
            "svg circle { fill: var(--muted); stroke: #fff; stroke-width: 1.5; }",
            "svg .provider-openai { fill: #1874a5; }",
            "svg .provider-anthropic { fill: #8b5e3c; }",
            "svg .provider-google { fill: #278656; }",
            "svg .provider-openrouter { fill: #c25a2a; }",
            "svg .provider-grok { fill: #b4475f; }",
            "svg .frontier { stroke: #111827; stroke-width: 2; }",
            "svg .frontier-line { fill: none; stroke: #111827; stroke-width: 2; "
            "stroke-dasharray: 5 4; }",
            "svg .grid-line { stroke: #e4e7ec; stroke-width: 1; }",
            "svg line { stroke: #98a2b3; stroke-width: 1; }",
            "svg text { fill: #344054; font-size: 12px; }",
            "svg .point-label { font-size: 11px; }",
            ".ob-segmented-bar table td:nth-child(3) { font-weight: 650; }",
            ".chart-note, .note { color: var(--muted); font-size: 13px; margin-top: 8px; }",
            "@media (max-width: 900px) { .cards, .report-controls { grid-template-columns: 1fr; } "
            "table { display: block; overflow-x: auto; } h1 { font-size: 30px; } }",
        ]
    )


def _heat_color(value: float | None) -> str:
    if value is None:
        return "#f2f4f7"
    if value >= 95:
        return "#c7f0d8"
    if value >= 85:
        return "#dff3b8"
    if value >= 70:
        return "#fff0a6"
    return "#ffd0c2"


def _display_money(value: str) -> str:
    if value == "":
        return "n/a"
    try:
        return f"${float(value):.6f}"
    except ValueError:
        return value


def _display_percent(value: str | None) -> str:
    if value in (None, ""):
        return "n/a"
    return f"{_format_percent(value)}%"


def _format_percent(value: str | None) -> str:
    return f"{_float(value) * 100:.1f}"


def _format_interval(low: str | None, high: str | None) -> str:
    if low in (None, "") or high in (None, ""):
        return ""
    return f"{_float(low) * 100:.1f}-{_float(high) * 100:.1f}%"


def _accuracy_interval(row: dict[str, str]) -> str:
    explicit = _format_interval(row.get("accuracy_ci_low"), row.get("accuracy_ci_high"))
    if explicit:
        return explicit
    scored_samples = _int(row.get("scored_samples"))
    if scored_samples <= 0:
        return ""
    low, high = wilson_interval(_int(row.get("correct")), scored_samples)
    return f"{low * 100:.1f}-{high * 100:.1f}%"


def _answer_accuracy_interval(row: dict[str, str]) -> str:
    explicit = _format_interval(
        row.get("answer_accuracy_ci_low"),
        row.get("answer_accuracy_ci_high"),
    )
    if explicit:
        return explicit
    return _accuracy_interval(row)


def _format_money(value: float | None) -> str:
    return "" if value is None else f"{value:.8f}".rstrip("0").rstrip(".")


def _format_number(value: float | None) -> str:
    return "" if value is None else f"{value:.2f}"


def _format_integer(value: float | None) -> str:
    return "" if value is None else f"{value:.0f}"


def _format_tokens_k(value: int) -> str:
    return f"{value / 1000:.2f}k"


def _display_label(row: dict[str, str]) -> str:
    label = row.get("label", "")
    thinking = _thinking_level(row)
    return f"{label} ({thinking})" if thinking else label


def _thinking_level(row: dict[str, str]) -> str:
    effort = row.get("reasoning_effort", "")
    summary = row.get("reasoning_summary", "")
    if effort and summary:
        return f"thinking={effort}/{summary}"
    if effort:
        return f"thinking={effort}"
    if summary:
        return f"thinking-summary={summary}"
    label = row.get("label", "")
    label_lower = label.lower()
    budget_match = re.search(
        r"\b(none|minimal|low|medium|high|xhigh|max)_budget_(\d+)\b",
        label_lower,
    )
    if budget_match:
        if _direct_gemini_3_model(row):
            return "provider default"
        depth, budget = budget_match.groups()
        return f"thinking={depth} budget={budget}"
    if re.search(r"\b(no thinking|non-thinking|non thinking)\b", label_lower):
        return "thinking=none"
    suffix_match = re.search(
        r"\b(none|minimal|low|medium|high|xhigh|max)\b$",
        label_lower,
    )
    if suffix_match and _likely_explicit_thinking_label(row):
        return f"thinking={suffix_match.group(1)}"
    if "thinking" in label_lower:
        return "model-named thinking"
    return "provider default"


def _reasoning_token_source(row: dict[str, str]) -> str:
    explicit = row.get("reasoning_token_source", "")
    if explicit:
        return explicit
    return "reported" if _int(row.get("reasoning_tokens")) > 0 else "not_reported_or_zero"


def _direct_gemini_3_model(row: dict[str, str]) -> bool:
    model = row.get("model", "").lower()
    return model.startswith("google/gemini-3")


def _likely_explicit_thinking_label(row: dict[str, str]) -> bool:
    label = row.get("label", "").lower()
    model = row.get("model", "").lower()
    summary_dir = row.get("summary_dir", "").lower()
    if "thinking" in label or "thinking" in summary_dir:
        return True
    return model.startswith(
        (
            "openai/gpt-5",
            "grok/",
            "google/gemini",
            "openrouter/google/gemini",
            "openrouter/openai/gpt-5",
            "openrouter/x-ai/grok",
        )
    )


def _optional_float(value: str | None) -> float | None:
    if value in (None, ""):
        return None
    try:
        return float(value)
    except ValueError:
        return None


def _float(value: str | None) -> float:
    return _optional_float(value) or 0.0


def _int(value: str | None) -> int:
    try:
        return int(float(value or 0))
    except ValueError:
        return 0
