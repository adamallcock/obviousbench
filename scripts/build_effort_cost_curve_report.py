"""Build the static effort-cost curve mini-report."""
# ruff: noqa: E501

from __future__ import annotations

import csv
import html
import math
import shutil
import subprocess
import tempfile
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
RELEASE_CONFIG = ROOT / "configs/release_v0_1_0.yaml"
DEFAULT_REPORT_DIR = ROOT / "docs/reports/2026-06-02-effort-cost-curves"
DEFAULT_LEADERBOARD_CSV = (
    ROOT / "docs/reports/2026-06-03-paper-v1-8x28-current-223-final/leaderboard.csv"
)
DEFAULT_POINTS_CSV = DEFAULT_REPORT_DIR / "effort-cost-curve-points.csv"
DEFAULT_MISSING_POINTS_CSV = DEFAULT_REPORT_DIR / "effort-cost-curve-missing-points.csv"
VERSION = "240-8x28-223-mini-low"
EXPECTED_BARRAGE_PROFILE = "hard_obvious_8x28_seed_20260531"
EXPECTED_SCORED_SAMPLES = 224

EFFORT_ORDER = {
    "default": -1,
    "none": 0,
    "minimal": 0,
    "low": 1,
    "medium": 2,
    "high": 3,
    "xhigh": 4,
    "max": 5,
}

DEFAULT_MODEL_COLORS = {
    "Claude Opus 4.8": "#d77250",
    "Claude Sonnet 4.6": "#216db4",
    "GPT-5.4 nano": "#d04f83",
    "GPT-5.4 mini": "#7d8b17",
    "GPT-5.4": "#1aa16f",
    "GPT-5.5": "#2075b9",
}

DEFAULT_EFFORT_STYLES = {
    "none": ("#54565a", ""),
    "low": ("#54565a", "12 10"),
    "medium": ("#54565a", "4 7"),
    "high": ("#54565a", "18 8 4 8"),
    "xhigh": ("#54565a", "2 8"),
    "max": ("#54565a", "24 8"),
}

LABEL_OFFSETS = {
    ("Claude Opus 4.8", "none"): (-72, 0),
    ("Claude Opus 4.8", "default"): (-120, 0),
    ("Claude Opus 4.8", "low"): (-72, 46),
    ("Claude Opus 4.8", "medium"): (22, 58),
    ("Claude Opus 4.8", "high"): (22, -42),
    ("Claude Opus 4.8", "xhigh"): (22, -12),
    ("Claude Opus 4.8", "max"): (22, -24),
    ("Claude Sonnet 4.6", "none"): (22, 34),
    ("Claude Sonnet 4.6", "default"): (22, 42),
    ("Claude Sonnet 4.6", "low"): (22, -52),
    ("Claude Sonnet 4.6", "medium"): (22, -10),
    ("Claude Sonnet 4.6", "high"): (22, -24),
    ("Claude Sonnet 4.6", "max"): (-94, 42),
}


def _load_yaml(path: Path) -> dict:
    if not path.exists():
        return {}
    loaded = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return loaded if isinstance(loaded, dict) else {}


def _repo_path(value: object, default: Path) -> Path:
    if value in {None, ""}:
        return default
    path = Path(str(value))
    return path if path.is_absolute() else ROOT / path


RELEASE = _load_yaml(RELEASE_CONFIG)
REPORT_DIR = _repo_path((RELEASE.get("effort_cost") or {}).get("report_dir"), DEFAULT_REPORT_DIR)
POINTS_CSV = _repo_path((RELEASE.get("effort_cost") or {}).get("points_csv"), DEFAULT_POINTS_CSV)
MISSING_POINTS_CSV = _repo_path(
    (RELEASE.get("effort_cost") or {}).get("missing_points_csv"),
    DEFAULT_MISSING_POINTS_CSV,
)
LEADERBOARD_CSV = _repo_path(
    (Path(str((RELEASE.get("snapshot") or {}).get("report_dir"))) / "leaderboard.csv")
    if (RELEASE.get("snapshot") or {}).get("report_dir")
    else None,
    DEFAULT_LEADERBOARD_CSV,
)
THEME_CONFIG = _repo_path(
    (RELEASE.get("generated") or {}).get("theme_config"),
    ROOT / "configs/release_theme_v0_1_0.yaml",
)
THEME = _load_yaml(THEME_CONFIG)
THEME_COLORS = THEME.get("colors") if isinstance(THEME.get("colors"), dict) else {}
THEME_TYPOGRAPHY = (
    THEME.get("typography") if isinstance(THEME.get("typography"), dict) else {}
)
THEME_CHART_DEFAULTS = (
    THEME.get("chart_defaults") if isinstance(THEME.get("chart_defaults"), dict) else {}
)
MODEL_COLORS = {
    **DEFAULT_MODEL_COLORS,
    **(THEME.get("models") if isinstance(THEME.get("models"), dict) else {}),
}
EFFORT_STYLES = {
    **DEFAULT_EFFORT_STYLES,
    **{
        effort: (str(payload.get("color", "#54565a")), str(payload.get("dash", "")))
        for effort, payload in (THEME.get("efforts") or {}).items()
        if isinstance(payload, dict)
    },
}
BACKGROUND_COLOR = str(THEME_COLORS.get("background", "#fbfaf7"))
FOREGROUND_COLOR = str(THEME_COLORS.get("foreground", "#1d1d1f"))
MUTED_COLOR = str(THEME_COLORS.get("muted", "#5a5d64"))
GRID_COLOR = str(THEME_COLORS.get("grid", "#ded8ce"))
WEB_FONT = str(THEME_TYPOGRAPHY.get("web_font", "Segoe UI"))
ANSWER_AXIS_LABEL = str(THEME_CHART_DEFAULTS.get("answer_metric_label", "Answer score (%)"))
COST_AXIS_LABEL = str(
    THEME_CHART_DEFAULTS.get("cost_axis_label", "Estimated total run cost, USD")
)


@dataclass(frozen=True)
class Point:
    provider: str
    curve: str
    model: str
    effort: str
    label: str
    accuracy_pct: float
    strict_accuracy_pct: float
    answer_failures: int
    format_only_failures: int
    estimated_cost_usd: float
    total_tokens: int
    reasoning_tokens: int
    scored_samples: int
    summary_dir: str


@dataclass(frozen=True)
class PointSpec:
    provider: str
    curve: str
    model: str
    effort: str
    label: str
    summary_suffix: str
    note: str = ""


POINT_SPECS = [
    PointSpec(
        "Anthropic",
        "Claude Opus 4.8",
        "anthropic/claude-opus-4-8",
        "default",
        "Claude Opus 4.8 default",
        "expand222-next-084-registry-anthropic-claude-opus-4-8",
        "224 panel has provider default, not explicit no-thinking.",
    ),
    PointSpec(
        "Anthropic",
        "Claude Opus 4.8",
        "anthropic/claude-opus-4-8",
        "low",
        "Claude Opus 4.8 low",
        "expand222-top-thinking-011-anthropic-claude-opus-4-8-low",
    ),
    PointSpec(
        "Anthropic",
        "Claude Opus 4.8",
        "anthropic/claude-opus-4-8",
        "medium",
        "Claude Opus 4.8 medium",
        "expand222-top-thinking-012-anthropic-claude-opus-4-8-medium",
    ),
    PointSpec(
        "Anthropic",
        "Claude Opus 4.8",
        "anthropic/claude-opus-4-8",
        "high",
        "Claude Opus 4.8 high",
        "expand222-top-thinking-013-anthropic-claude-opus-4-8-high",
    ),
    PointSpec(
        "Anthropic",
        "Claude Opus 4.8",
        "anthropic/claude-opus-4-8",
        "xhigh",
        "Claude Opus 4.8 xhigh",
        "expand222-top-thinking-014-anthropic-claude-opus-4-8-xhigh",
    ),
    PointSpec(
        "Anthropic",
        "Claude Opus 4.8",
        "anthropic/claude-opus-4-8",
        "max",
        "Claude Opus 4.8 max",
        "expand222-top-thinking-015-anthropic-claude-opus-4-8-max",
    ),
    PointSpec(
        "Anthropic",
        "Claude Sonnet 4.6",
        "anthropic/claude-sonnet-4-6",
        "default",
        "Claude Sonnet 4.6 default",
        "expand222-paper-anthropic-claude-sonnet-4-6",
        "224 panel has provider default, not explicit no-thinking.",
    ),
    PointSpec(
        "Anthropic",
        "Claude Sonnet 4.6",
        "anthropic/claude-sonnet-4-6",
        "low",
        "Claude Sonnet 4.6 low",
        "expand222-top-thinking-016-anthropic-claude-sonnet-4-6-low",
    ),
    PointSpec(
        "Anthropic",
        "Claude Sonnet 4.6",
        "anthropic/claude-sonnet-4-6",
        "medium",
        "Claude Sonnet 4.6 medium",
        "expand222-top-thinking-017-anthropic-claude-sonnet-4-6-medium",
    ),
    PointSpec(
        "Anthropic",
        "Claude Sonnet 4.6",
        "anthropic/claude-sonnet-4-6",
        "high",
        "Claude Sonnet 4.6 high",
        "expand222-top-thinking-018-anthropic-claude-sonnet-4-6-high",
    ),
    PointSpec(
        "Anthropic",
        "Claude Sonnet 4.6",
        "anthropic/claude-sonnet-4-6",
        "max",
        "Claude Sonnet 4.6 max",
        "expand222-top-thinking-019-anthropic-claude-sonnet-4-6-max",
    ),
    PointSpec("OpenAI", "GPT-5.4", "openai/gpt-5.4", "none", "OpenAI GPT-5.4 none", "expand222-top-thinking-006-openai-gpt-5-4-none"),
    PointSpec("OpenAI", "GPT-5.4", "openai/gpt-5.4", "low", "OpenAI GPT-5.4 low", "expand222-top-thinking-007-openai-gpt-5-4-low"),
    PointSpec("OpenAI", "GPT-5.4", "openai/gpt-5.4", "medium", "OpenAI GPT-5.4 medium", "expand222-top-thinking-008-openai-gpt-5-4-medium"),
    PointSpec("OpenAI", "GPT-5.4", "openai/gpt-5.4", "high", "OpenAI GPT-5.4 high", "expand222-top-thinking-009-openai-gpt-5-4-high"),
    PointSpec("OpenAI", "GPT-5.4", "openai/gpt-5.4", "xhigh", "OpenAI GPT-5.4 xhigh", "expand222-top-thinking-010-openai-gpt-5-4-xhigh"),
    PointSpec("OpenAI", "GPT-5.4 mini", "openai/gpt-5.4-mini", "none", "OpenAI GPT-5.4 mini no thinking", "expand222-next-070-registry-openai-gpt-5-4-mini-none"),
    PointSpec(
        "OpenAI",
        "GPT-5.4 mini",
        "openai/gpt-5.4-mini",
        "low",
        "OpenAI GPT-5.4 mini low",
        "expand222-fill-openai-gpt-5-4-mini-low",
    ),
    PointSpec("OpenAI", "GPT-5.4 mini", "openai/gpt-5.4-mini", "medium", "OpenAI GPT-5.4 mini medium", "expand222-overline-004-openai-gpt-5-4-mini-medium"),
    PointSpec("OpenAI", "GPT-5.4 mini", "openai/gpt-5.4-mini", "high", "OpenAI GPT-5.4 mini high", "expand222-overline-005-openai-gpt-5-4-mini-high"),
    PointSpec("OpenAI", "GPT-5.4 mini", "openai/gpt-5.4-mini", "xhigh", "OpenAI GPT-5.4 mini xhigh", "expand222-overline-007-openai-gpt-5-4-mini-xhigh"),
    PointSpec("OpenAI", "GPT-5.4 nano", "openai/gpt-5.4-nano", "none", "OpenAI GPT-5.4 nano no thinking", "expand222-next-037-registry-openai-gpt-5-4-nano-none"),
    PointSpec("OpenAI", "GPT-5.4 nano", "openai/gpt-5.4-nano", "low", "OpenAI GPT-5.4 nano low", "expand222-next-099-thinking-openai-gpt-5-4-nano-low"),
    PointSpec("OpenAI", "GPT-5.4 nano", "openai/gpt-5.4-nano", "medium", "OpenAI GPT-5.4 nano medium", "expand222-overline-002-openai-gpt-5-4-nano-medium"),
    PointSpec("OpenAI", "GPT-5.4 nano", "openai/gpt-5.4-nano", "high", "OpenAI GPT-5.4 nano high", "expand222-overline-003-openai-gpt-5-4-nano-high"),
    PointSpec("OpenAI", "GPT-5.4 nano", "openai/gpt-5.4-nano", "xhigh", "OpenAI GPT-5.4 nano xhigh", "expand222-overline-006-openai-gpt-5-4-nano-xhigh"),
    PointSpec("OpenAI", "GPT-5.5", "openai/gpt-5.5", "none", "OpenAI GPT-5.5 none", "expand222-top-thinking-001-openai-gpt-5-5-none"),
    PointSpec("OpenAI", "GPT-5.5", "openai/gpt-5.5", "low", "OpenAI GPT-5.5 low", "expand222-top-thinking-002-openai-gpt-5-5-low"),
    PointSpec("OpenAI", "GPT-5.5", "openai/gpt-5.5", "medium", "OpenAI GPT-5.5 medium", "expand222-top-thinking-003-openai-gpt-5-5-medium"),
    PointSpec("OpenAI", "GPT-5.5", "openai/gpt-5.5", "high", "OpenAI GPT-5.5 high", "expand222-top-thinking-004-openai-gpt-5-5-high"),
    PointSpec("OpenAI", "GPT-5.5", "openai/gpt-5.5", "xhigh", "OpenAI GPT-5.5 xhigh", "expand222-top-thinking-005-openai-gpt-5-5-xhigh"),
]


def main() -> int:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    rows, missing = build_224_points()
    write_missing_points(missing)
    if missing:
        missing_labels = ", ".join(
            f"{row['label']} ({row['expected_summary_suffix']})" for row in missing
        )
        raise RuntimeError(f"missing requested 224-question effort-cost point(s): {missing_labels}")
    write_points(rows)
    points = [point_from_row(row) for row in rows]
    build_all_charts(points)
    write_index()
    return 0


def build_224_points() -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    leaderboard = leaderboard_rows_by_summary_suffix()
    points: list[dict[str, str]] = []
    missing: list[dict[str, str]] = []
    for spec in POINT_SPECS:
        leaderboard_row = leaderboard.get(spec.summary_suffix)
        if leaderboard_row is None:
            missing.append(
                {
                    "provider": spec.provider,
                    "curve": spec.curve,
                    "model": spec.model,
                    "effort": spec.effort,
                    "label": spec.label,
                    "expected_summary_suffix": spec.summary_suffix,
                    "note": spec.note,
                }
            )
            continue
        points.append(point_row_from_summary(spec, leaderboard_row["summary_dir"]))
    return points, missing


def leaderboard_rows_by_summary_suffix() -> dict[str, dict[str, str]]:
    with LEADERBOARD_CSV.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    by_suffix: dict[str, dict[str, str]] = {}
    for row in rows:
        suffix = Path(row["summary_dir"]).name
        by_suffix.setdefault(suffix, row)
    return by_suffix


def point_row_from_summary(spec: PointSpec, summary_dir: str) -> dict[str, str]:
    summary = read_summary(ROOT / summary_dir / "summary.csv")
    validate_summary_for_spec(spec, summary, summary_dir)
    scored = int(float(summary["scored_samples"]))
    answer_correct = int(float(summary["answer_correct"]))
    strict_correct = int(float(summary["strict_correct"]))
    return {
        "provider": spec.provider,
        "curve": spec.curve,
        "model": spec.model,
        "effort": spec.effort,
        "label": spec.label,
        "accuracy_pct": pct(summary["answer_accuracy"]),
        "strict_accuracy_pct": pct(summary["strict_accuracy"]),
        "answer_failures": str(scored - answer_correct),
        "format_only_failures": str(max(0, answer_correct - strict_correct)),
        "estimated_cost_usd": trim(summary["estimated_cost_usd"]),
        "total_tokens": str(int(float(summary["total_tokens"]))),
        "reasoning_tokens": str(int(float(summary["reasoning_tokens"]))),
        "scored_samples": str(scored),
        "summary_dir": summary_dir,
    }


def read_summary(path: Path) -> dict[str, str]:
    if not path.exists():
        raise FileNotFoundError(path)
    with path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) != 1:
        raise ValueError(f"expected one summary row in {path}, found {len(rows)}")
    return rows[0]


def validate_summary_for_spec(
    spec: PointSpec, summary: dict[str, str], summary_dir: str
) -> None:
    model = summary.get("model", "")
    if model != spec.model:
        raise ValueError(
            f"{spec.label}: summary model {model!r} does not match expected {spec.model!r} in {summary_dir}"
        )
    profile = summary.get("barrage_profile", "")
    if profile != EXPECTED_BARRAGE_PROFILE:
        raise ValueError(
            f"{spec.label}: summary barrage_profile {profile!r} does not match {EXPECTED_BARRAGE_PROFILE!r} in {summary_dir}"
        )
    total_samples = int(float(summary.get("total_samples") or 0))
    scored_samples = int(float(summary.get("scored_samples") or 0))
    if total_samples != EXPECTED_SCORED_SAMPLES or scored_samples != EXPECTED_SCORED_SAMPLES:
        raise ValueError(
            f"{spec.label}: summary has total_samples={total_samples}, scored_samples={scored_samples}; expected {EXPECTED_SCORED_SAMPLES}/{EXPECTED_SCORED_SAMPLES} in {summary_dir}"
        )
    if spec.effort == "default":
        return
    effort = summary.get("reasoning_effort", "")
    if effort != spec.effort:
        raise ValueError(
            f"{spec.label}: summary reasoning_effort {effort!r} does not match expected {spec.effort!r} in {summary_dir}"
        )


def write_points(rows: list[dict[str, str]]) -> None:
    fieldnames = [
        "provider",
        "curve",
        "model",
        "effort",
        "label",
        "accuracy_pct",
        "strict_accuracy_pct",
        "answer_failures",
        "format_only_failures",
        "estimated_cost_usd",
        "total_tokens",
        "reasoning_tokens",
        "scored_samples",
        "summary_dir",
    ]
    with POINTS_CSV.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_missing_points(rows: list[dict[str, str]]) -> None:
    fieldnames = [
        "provider",
        "curve",
        "model",
        "effort",
        "label",
        "expected_summary_suffix",
        "note",
    ]
    with MISSING_POINTS_CSV.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def point_from_row(row: dict[str, str]) -> Point:
    return Point(
        provider=row["provider"],
        curve=row["curve"],
        model=row["model"],
        effort=row["effort"],
        label=row["label"],
        accuracy_pct=float(row["accuracy_pct"]),
        strict_accuracy_pct=float(row["strict_accuracy_pct"]),
        answer_failures=int(row["answer_failures"]),
        format_only_failures=int(row["format_only_failures"]),
        estimated_cost_usd=float(row["estimated_cost_usd"]),
        total_tokens=int(row["total_tokens"]),
        reasoning_tokens=int(row["reasoning_tokens"]),
        scored_samples=int(row["scored_samples"]),
        summary_dir=row["summary_dir"],
    )


def pct(value: str) -> str:
    return trim(float(value) * 100)


def trim(value: str | float) -> str:
    number = float(value)
    text = f"{number:.8f}".rstrip("0").rstrip(".")
    return text or "0"


def build_all_charts(points: list[Point]) -> None:
    openai = [p for p in points if p.provider == "OpenAI"]
    anthropic = [p for p in points if p.provider == "Anthropic"]
    chart_model_curves(
        openai,
        REPORT_DIR / "openai-effort-cost-curves.svg",
        "OpenAI Effort Cost Curves",
        "224-question panel; answer score (%) vs reported run cost",
        log_x=False,
    )
    chart_model_curves(
        openai,
        REPORT_DIR / "openai-effort-cost-curves-log.svg",
        "OpenAI Effort Cost Curves",
        "224-question panel; log-scaled reported run cost",
        log_x=True,
    )
    chart_model_curves(
        anthropic,
        REPORT_DIR / "anthropic-effort-cost-curves.svg",
        "Anthropic Adaptive Thinking",
        "224-question panel; default rows are provider default, not explicit no-thinking",
        log_x=False,
        y_min=84,
        y_max=101,
    )
    chart_model_curves(
        points,
        REPORT_DIR / "combined-effort-cost-curves-log.svg",
        "Combined Effort Cost Curves",
        "224-question panel; OpenAI plus Anthropic adaptive-thinking rows",
        log_x=True,
    )
    chart_effort_setting_curves(
        openai,
        REPORT_DIR / "openai-effort-setting-curves-log.svg",
        efforts=("none", "low", "medium", "high", "xhigh"),
        title="OpenAI Grouped By Thinking Setting",
        subtitle="224-question panel; curves are settings; points progress nano to full-size",
    )
    chart_effort_setting_curves(
        openai,
        REPORT_DIR / "openai-none-low-size-curves-log.svg",
        efforts=("none", "low"),
        title="OpenAI size curve: no thinking vs low effort",
        subtitle="224-question panel; none and low points are present for current OpenAI sizes",
    )
    chart_effort_setting_curves(
        openai,
        REPORT_DIR / "openai-none-low-setting-curves-model-colors-log.svg",
        efforts=("none", "low"),
        title="OpenAI None Vs Low",
        subtitle="Curves are settings; colors are models",
    )
    rasterize_svgs(REPORT_DIR.glob("*.svg"))


def chart_model_curves(
    points: list[Point],
    out: Path,
    title: str,
    subtitle: str,
    *,
    log_x: bool,
    y_min: float = 77,
    y_max: float = 101,
) -> None:
    series = []
    for curve in sorted({p.curve for p in points}, key=model_order):
        curve_points = sorted(
            [p for p in points if p.curve == curve],
            key=lambda p: EFFORT_ORDER.get(p.effort, 99),
        )
        series.append((curve, curve_points))
    chart = SvgChart(
        title=title,
        subtitle=subtitle,
        x_label=(
            f"{COST_AXIS_LABEL} (log scale)"
            if log_x
            else f"{COST_AXIS_LABEL} (224 questions)"
        ),
        y_label=ANSWER_AXIS_LABEL,
        points=points,
        log_x=log_x,
        y_min=y_min,
        y_max=y_max,
    )
    chart.start()
    for curve, curve_points in series:
        color = MODEL_COLORS.get(curve, "#7b6f62")
        chart.line(curve_points, color=color, width=5)
        for point in curve_points:
            chart.point(point, color=color, label=point.effort)
    chart.legend([(curve, MODEL_COLORS.get(curve, "#7b6f62"), "") for curve, _ in series])
    chart.footnote(source_text(points))
    out.write_text(chart.finish(), encoding="utf-8")


def chart_effort_setting_curves(
    points: list[Point],
    out: Path,
    *,
    efforts: tuple[str, ...],
    title: str,
    subtitle: str,
) -> None:
    filtered = [p for p in points if p.effort in efforts]
    chart = SvgChart(
        title=title,
        subtitle=subtitle,
        x_label=f"{COST_AXIS_LABEL} (log scale)",
        y_label=ANSWER_AXIS_LABEL,
        points=filtered,
        log_x=True,
        y_min=77,
        y_max=101,
        right=520,
    )
    chart.start()
    for effort in efforts:
        effort_points = sorted(
            [p for p in filtered if p.effort == effort],
            key=lambda p: model_order(p.curve),
        )
        color, dash = EFFORT_STYLES.get(effort, ("#54565a", ""))
        chart.line(effort_points, color=color, width=5, dash=dash)
        for point in effort_points:
            chart.point(point, color=MODEL_COLORS.get(point.curve, "#7b6f62"), label=short_model(point.curve))
    chart.legend(
        [(effort, EFFORT_STYLES[effort][0], EFFORT_STYLES[effort][1]) for effort in efforts],
        title="Curves",
        x=1450,
        y=205,
    )
    chart.legend(
        [(curve, MODEL_COLORS.get(curve, "#7b6f62"), "") for curve in sorted({p.curve for p in filtered}, key=model_order)],
        title="Models",
        x=1450,
        y=365,
        as_points=True,
    )
    chart.footnote(source_text(points))
    out.write_text(chart.finish(), encoding="utf-8")


class SvgChart:
    def __init__(
        self,
        *,
        title: str,
        subtitle: str,
        x_label: str,
        y_label: str,
        points: list[Point],
        log_x: bool,
        y_min: float,
        y_max: float,
        width: int = 1900,
        height: int = 1120,
        left: int = 170,
        right: int = 430,
        top: int = 190,
        bottom: int = 170,
    ) -> None:
        self.title = title
        self.subtitle = subtitle
        self.x_label = x_label
        self.y_label = y_label
        self.points = points
        self.log_x = log_x
        self.y_min = y_min
        self.y_max = y_max
        self.width = width
        self.height = height
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom
        self.plot_w = width - left - right
        self.plot_h = height - top - bottom
        costs = [p.estimated_cost_usd for p in points if p.estimated_cost_usd > 0]
        self.x_min = min(costs)
        self.x_max = max(costs)
        if log_x:
            self.x_min = 10 ** (math.floor(math.log10(self.x_min * 0.85)))
            self.x_max = 10 ** (math.ceil(math.log10(self.x_max * 1.15)))
        else:
            pad = (self.x_max - self.x_min) * 0.08 or self.x_max * 0.1
            self.x_min = max(0, self.x_min - pad)
            self.x_max += pad
        self.parts: list[str] = []

    def start(self) -> None:
        self.parts.extend(
            [
                f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.width}" height="{self.height}" viewBox="0 0 {self.width} {self.height}">',
                "<style>",
                f"text{{font-family:-apple-system,BlinkMacSystemFont,'{esc(WEB_FONT)}',sans-serif;fill:{FOREGROUND_COLOR}}}",
                f".title{{font-size:54px;font-weight:800}}.subtitle{{font-size:30px;fill:{MUTED_COLOR}}}",
                f".axis{{font-size:30px;font-weight:700}}.tick{{font-size:24px;fill:{MUTED_COLOR}}}",
                f".label{{font-size:26px;font-weight:700}}.foot{{font-size:21px;fill:{MUTED_COLOR}}}",
                "</style>",
                f'<rect width="100%" height="100%" fill="{BACKGROUND_COLOR}"/>',
                f'<text class="title" x="{centered_text_x(self.title, 54, self.width / 2, bold=True):.1f}" y="78">{esc(self.title)}</text>',
                f'<text class="subtitle" x="{centered_text_x(self.subtitle, 30, self.width / 2):.1f}" y="124">{esc(self.subtitle)}</text>',
            ]
        )
        self.grid()

    def grid(self) -> None:
        for tick in self.y_ticks():
            y = self.y(tick)
            label = f"{tick:.0f}%"
            self.parts.append(
                f'<line x1="{self.left}" y1="{y:.1f}" x2="{self.width - self.right}" y2="{y:.1f}" stroke="{GRID_COLOR}" stroke-width="2"/>'
            )
            self.parts.append(
                f'<text class="tick" x="{self.left - 24 - approx_text_width(label, 24):.1f}" y="{y + 8:.1f}">{label}</text>'
            )
        for tick in self.x_ticks():
            x = self.x(tick)
            label = format_cost(tick)
            self.parts.append(
                f'<line x1="{x:.1f}" y1="{self.top}" x2="{x:.1f}" y2="{self.height - self.bottom}" stroke="{GRID_COLOR}" stroke-width="2"/>'
            )
            self.parts.append(
                f'<text class="tick" x="{centered_text_x(label, 24, x):.1f}" y="{self.height - self.bottom + 46}">{esc(label)}</text>'
            )
        self.parts.append(
            f'<line x1="{self.left}" y1="{self.height - self.bottom}" x2="{self.width - self.right}" y2="{self.height - self.bottom}" stroke="{FOREGROUND_COLOR}" stroke-width="4"/>'
        )
        self.parts.append(
            f'<line x1="{self.left}" y1="{self.top}" x2="{self.left}" y2="{self.height - self.bottom}" stroke="{FOREGROUND_COLOR}" stroke-width="4"/>'
        )
        self.parts.append(
            f'<text class="axis" x="{self.left}" y="{self.top - 32}">{esc(self.y_label)}</text>'
        )
        self.parts.append(
            f'<text class="axis" x="{centered_text_x(self.x_label, 30, self.left + self.plot_w / 2, bold=True):.1f}" y="{self.height - 65}">{esc(self.x_label)}</text>'
        )

    def line(
        self,
        points: list[Point],
        *,
        color: str,
        width: int,
        dash: str = "",
    ) -> None:
        if len(points) < 2:
            return
        coords = " ".join(f"{self.x(p.estimated_cost_usd):.1f},{self.y(p.accuracy_pct):.1f}" for p in points)
        dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
        self.parts.append(
            f'<polyline points="{coords}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round"{dash_attr}/>'
        )

    def point(self, point: Point, *, color: str, label: str) -> None:
        x = self.x(point.estimated_cost_usd)
        y = self.y(point.accuracy_pct)
        dx, dy = LABEL_OFFSETS.get((point.curve, point.effort), (14, -15))
        self.parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="13" fill="{color}" stroke="{BACKGROUND_COLOR}" stroke-width="4"/>')
        self.parts.append(
            f'<text class="label" x="{x + dx:.1f}" y="{y + dy:.1f}">{esc(label)}</text>'
        )

    def legend(
        self,
        entries: list[tuple[str, str, str]],
        *,
        title: str = "",
        x: int | None = None,
        y: int | None = None,
        as_points: bool = False,
    ) -> None:
        x = x if x is not None else self.width - self.right + 70
        y = y if y is not None else self.top + 15
        if title:
            self.parts.append(f'<text class="label" x="{x}" y="{y}">{esc(title)}</text>')
            y += 45
        for index, (name, color, dash) in enumerate(entries):
            yy = y + index * 45
            if as_points:
                self.parts.append(f'<circle cx="{x + 15}" cy="{yy - 8}" r="10" fill="{color}"/>')
            else:
                dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
                self.parts.append(
                    f'<line x1="{x}" y1="{yy - 8}" x2="{x + 70}" y2="{yy - 8}" stroke="{color}" stroke-width="7"{dash_attr}/>'
                )
            self.parts.append(f'<text class="tick" x="{x + 86}" y="{yy}">{esc(name)}</text>')

    def footnote(self, text: str) -> None:
        self.parts.append(f'<text class="foot" x="{self.left}" y="{self.height - 22}">{esc(text)}</text>')

    def finish(self) -> str:
        self.parts.append("</svg>")
        return "\n".join(self.parts) + "\n"

    def x(self, value: float) -> float:
        if self.log_x:
            start = math.log10(self.x_min)
            end = math.log10(self.x_max)
            frac = (math.log10(value) - start) / (end - start)
        else:
            frac = (value - self.x_min) / (self.x_max - self.x_min)
        return self.left + frac * self.plot_w

    def y(self, value: float) -> float:
        frac = (value - self.y_min) / (self.y_max - self.y_min)
        return self.height - self.bottom - frac * self.plot_h

    def x_ticks(self) -> list[float]:
        if self.log_x:
            candidates = [
                0.001,
                0.002,
                0.003,
                0.005,
                0.01,
                0.02,
                0.05,
                0.1,
                0.2,
                0.5,
                1.0,
            ]
            return [tick for tick in candidates if self.x_min <= tick <= self.x_max]
        step = (self.x_max - self.x_min) / 5
        return [self.x_min + step * index for index in range(6)]

    def y_ticks(self) -> list[float]:
        start = math.ceil(self.y_min / 5) * 5
        end = math.floor(self.y_max / 5) * 5
        return [float(tick) for tick in range(int(start), int(end) + 1, 5)]


def model_order(name: str) -> tuple[int, str]:
    order = {
        "GPT-5.4 nano": 0,
        "GPT-5.4 mini": 1,
        "GPT-5.4": 2,
        "GPT-5.5": 3,
        "Claude Sonnet 4.6": 10,
        "Claude Opus 4.8": 11,
    }
    return (order.get(name, 99), name)


def short_model(name: str) -> str:
    return (
        name.replace("GPT-5.4 nano", "nano")
        .replace("GPT-5.4 mini", "mini")
        .replace("GPT-5.4", "5.4")
        .replace("GPT-5.5", "5.5")
    )


def format_cost(value: float) -> str:
    if value < 0.01:
        return f"${value:.3f}"
    if value < 0.1:
        return f"${value:.2f}"
    return f"${value:.2f}"


def centered_text_x(text: str, font_size: float, center_x: float, *, bold: bool = False) -> float:
    return center_x - approx_text_width(text, font_size, bold=bold) / 2


def approx_text_width(text: str, font_size: float, *, bold: bool = False) -> float:
    # qlmanage ignores SVG text-anchor in generated PNGs, so use explicit positions.
    width = 0.0
    for char in text:
        if char in "ilI.,:;|!":
            width += 0.26
        elif char in "mwMW@#%":
            width += 0.86
        elif char == " ":
            width += 0.32
        else:
            width += 0.56
    if bold:
        width *= 1.08
    return width * font_size


def source_text(points: Iterable[Point]) -> str:
    if any(p.provider == "Anthropic" and p.effort == "default" for p in points):
        return "Source: 223-row merged 224-question 8x28 leaderboard. Anthropic default is provider default; costs use reported telemetry, not hidden-thinking billing."
    return "Source: 223-row merged 224-question 8x28 leaderboard. Y uses answer correctness."


def esc(text: str) -> str:
    return html.escape(text, quote=True)


def rasterize_svgs(paths: Iterable[Path]) -> None:
    svg_paths = list(paths)
    if rasterize_svgs_with_cairosvg(svg_paths):
        return
    qlmanage = shutil.which("qlmanage")
    if not qlmanage:
        return
    for svg in svg_paths:
        with tempfile.TemporaryDirectory() as tmpdir:
            subprocess.run(
                [qlmanage, "-t", "-s", "1900", "-o", tmpdir, str(svg)],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            png = Path(tmpdir) / f"{svg.name}.png"
            if not png.exists():
                raise FileNotFoundError(png)
            shutil.copyfile(png, svg.with_suffix(".svg.png"))
            shutil.copyfile(png, svg.with_suffix(".png"))


def rasterize_svgs_with_cairosvg(paths: Iterable[Path]) -> bool:
    try:
        import cairosvg
    except ImportError:
        return False

    for svg in paths:
        png = svg.with_suffix(".png")
        cairosvg.svg2png(url=str(svg), write_to=str(png), output_width=1900)
        shutil.copyfile(png, svg.with_suffix(".svg.png"))
    return True


def write_index() -> None:
    source = (
        "Generated from the 223-row merged hard_obvious_8x28 leaderboard and "
        "per-run summary CSVs. X axis is reported run cost for 224 questions; y "
        "axis is answer correctness. Anthropic default points are provider-default "
        "rows, not explicit no-thinking controls. Anthropic costs use reported "
        "telemetry and should not be read as billed hidden-thinking measurements. Strict correctness and "
        "format-only failure counts are included in the point CSV. Requested "
        "curve points are validated as 224-sample hard_obvious_8x28 summaries."
    )
    html_text = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Effort Cost Curves</title>
<style>
body{{font-family:-apple-system,BlinkMacSystemFont,"{esc(WEB_FONT)}",sans-serif;margin:32px;background:{BACKGROUND_COLOR};color:{FOREGROUND_COLOR}}}
main{{max-width:1540px;margin:auto}}
img{{display:block;width:100%;height:auto;margin:24px 0 44px;border:1px solid {GRID_COLOR};background:{BACKGROUND_COLOR}}}
code{{font-size:.95em}}
p{{line-height:1.45}}
</style>
</head>
<body>
<main>
<h1>Effort Cost Curves</h1>
<p>{esc(source)}</p>
<h2>OpenAI None Vs Low By Model Size</h2>
<img id="openai-none-low" src="openai-none-low-size-curves-log.svg?v={VERSION}" alt="OpenAI none and low thinking curves by model size with log cost axis">
<h2>OpenAI None Vs Low By Thinking Setting</h2>
<img src="openai-none-low-setting-curves-model-colors-log.svg?v={VERSION}" alt="OpenAI none and low thinking curves grouped by setting with model colors">
<h2>OpenAI Grouped By Thinking Setting</h2>
<img src="openai-effort-setting-curves-log.svg?v={VERSION}" alt="OpenAI curves grouped by thinking setting with log cost axis">
<h2>OpenAI Log Cost</h2>
<img src="openai-effort-cost-curves-log.svg?v={VERSION}" alt="OpenAI effort cost curves with log cost axis">
<h2>OpenAI Linear Cost</h2>
<img src="openai-effort-cost-curves.svg?v={VERSION}" alt="OpenAI effort cost curves">
<h2>Anthropic</h2>
<img src="anthropic-effort-cost-curves.svg?v={VERSION}" alt="Anthropic adaptive thinking effort cost curves">
<h2>Combined</h2>
<img src="combined-effort-cost-curves-log.svg?v={VERSION}" alt="Combined effort cost curves with log cost axis">
<p>Data: <a href="effort-cost-curve-points.csv?v={VERSION}">effort-cost-curve-points.csv</a></p>
<p>Missing-point guardrail CSV (expected empty): <a href="effort-cost-curve-missing-points.csv?v={VERSION}">effort-cost-curve-missing-points.csv</a></p>
</main>
</body>
</html>
"""
    (REPORT_DIR / "index.html").write_text(html_text, encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
