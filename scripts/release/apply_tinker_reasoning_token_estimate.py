#!/usr/bin/env python3
"""Apply the audited Inkling reasoning-token estimate to public aggregates.

Tinker's OpenAI-compatible response reports one billed ``completion_tokens``
total. It exposes a separate reasoning trace, but no separate reasoning-token
usage field. The private calibration used Inkling's pinned tokenizer to count
the final answer and found a four-token non-reasoning completion baseline. The
constant table below is the resulting aggregate split for the captured 432
attempts at each Inkling setting.

The transformation validates the original billed completion total, moves only
the estimated reasoning share from ``output`` to ``reasoning``, and preserves
total tokens, cost, and scores. It contains no prompts, responses, traces,
credentials, or raw logs.
"""

from __future__ import annotations

import argparse
import csv
from collections.abc import Iterable
from pathlib import Path

TINKER_MODEL = "thinkingmachines/Inkling"

# Each tuple is (provider-reported billed completion tokens,
# estimated billed reasoning tokens). The ``none`` row is reported telemetry:
# its zero reasoning count is not an estimate.
INKLING_AGGREGATE_SPLITS: dict[str, tuple[int, int]] = {
    "none": (2716, 0),
    "minimal": (21285, 18563),
    "low": (22541, 19822),
    "medium": (36640, 33921),
    "high": (42887, 40167),
    "xhigh": (51522, 44714),
}

REPORT_ESTIMATE_NOTE = (
    "- A `~` before a Tinker reasoning-token value marks an estimate reconstructed "
    "from its billed completion total and Inkling's tokenizer; it is not provider-"
    "reported reasoning telemetry."
)


def as_int(row: dict[str, str], key: str) -> int:
    return int(float(str(row.get(key) or 0)))


def apply_estimate(rows: Iterable[dict[str, str]]) -> list[dict[str, str]]:
    """Return rows with the verified Tinker completion split applied."""
    updated_rows: list[dict[str, str]] = []
    seen_efforts: set[str] = set()
    for row in rows:
        updated = dict(row)
        if updated.get("provider_model") != TINKER_MODEL:
            updated_rows.append(updated)
            continue

        effort = str(updated.get("reasoning_effort") or "").strip().lower()
        if effort not in INKLING_AGGREGATE_SPLITS:
            raise ValueError(f"unexpected Inkling effort: {effort!r}")
        if effort in seen_efforts:
            raise ValueError(f"duplicate Inkling effort: {effort}")
        seen_efforts.add(effort)

        billed_completion, estimated_reasoning = INKLING_AGGREGATE_SPLITS[effort]
        original_output = as_int(updated, "output_tokens")
        original_reasoning = as_int(updated, "reasoning_tokens")
        estimated_output = billed_completion - estimated_reasoning
        if original_output == billed_completion and original_reasoning == 0:
            updated["output_tokens"] = str(estimated_output)
            updated["reasoning_tokens"] = str(estimated_reasoning)
        elif (
            original_output == estimated_output
            and original_reasoning == estimated_reasoning
        ):
            # The release artifact already carries the audited split. Keep the
            # command safe to rerun while still rejecting any unrelated drift.
            pass
        else:
            raise ValueError(
                f"unexpected pre-estimate token split for Inkling {effort}: "
                f"output={original_output}, reasoning={original_reasoning}"
            )
        if (
            as_int(updated, "output_tokens") + as_int(updated, "reasoning_tokens")
            != billed_completion
        ):
            raise AssertionError(f"Inkling {effort} no longer reconciles to completion total")
        updated_rows.append(updated)

    if seen_efforts != set(INKLING_AGGREGATE_SPLITS):
        missing = sorted(set(INKLING_AGGREGATE_SPLITS) - seen_efforts)
        raise ValueError(f"missing Inkling aggregate rows: {missing}")
    return updated_rows


def update_report_markdown(text: str, rows: Iterable[dict[str, str]]) -> str:
    """Update only the generated Inkling table cells and transparent note."""
    by_effort = {
        str(row["reasoning_effort"]): row
        for row in rows
        if row.get("provider_model") == TINKER_MODEL
    }
    rewritten: list[str] = []
    seen_efforts: set[str] = set()
    for line in text.splitlines():
        if not line.startswith(f"| {TINKER_MODEL} |"):
            rewritten.append(line)
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) != 14:
            raise ValueError(f"unexpected Inkling report row: {line}")
        effort = cells[1]
        row = by_effort.get(effort)
        if row is None:
            raise ValueError(f"unexpected Inkling report effort: {effort}")
        if effort in seen_efforts:
            raise ValueError(f"duplicate Inkling report effort: {effort}")
        seen_efforts.add(effort)
        expected_billed, estimated_reasoning = INKLING_AGGREGATE_SPLITS[effort]
        estimated_output = expected_billed - estimated_reasoning
        estimated_display = (
            f"~{estimated_reasoning}" if estimated_reasoning else "0"
        )
        if int(cells[8]) == expected_billed and int(cells[9]) == 0:
            cells[8] = row["output_tokens"]
            cells[9] = estimated_display
        elif cells[8] == str(estimated_output) and cells[9] == estimated_display:
            pass
        else:
            raise ValueError(f"unexpected pre-estimate report row: {line}")
        rewritten.append("| " + " | ".join(cells) + " |")

    if seen_efforts != set(INKLING_AGGREGATE_SPLITS):
        missing = sorted(set(INKLING_AGGREGATE_SPLITS) - seen_efforts)
        raise ValueError(f"missing Inkling report rows: {missing}")
    if REPORT_ESTIMATE_NOTE not in rewritten:
        anchor = "- Incomplete rows are shown but should not be used for final public claims."
        try:
            index = rewritten.index(anchor)
        except ValueError as exc:
            raise ValueError("report lacks the generated-report note anchor") from exc
        rewritten.insert(index + 1, REPORT_ESTIMATE_NOTE)
    return "\n".join(rewritten).rstrip() + "\n"


def apply_files(
    *,
    summary_path: Path,
    report_path: Path,
    output_summary_path: Path,
    output_report_path: Path,
) -> dict[str, int]:
    with summary_path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = apply_estimate(reader)
        fieldnames = list(reader.fieldnames or [])

    output_summary_path.parent.mkdir(parents=True, exist_ok=True)
    with output_summary_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    output_report_path.parent.mkdir(parents=True, exist_ok=True)
    output_report_path.write_text(
        update_report_markdown(report_path.read_text(encoding="utf-8"), rows),
        encoding="utf-8",
    )
    return {
        "summary_rows": len(rows),
        "inkling_rows": len(INKLING_AGGREGATE_SPLITS),
        "estimated_reasoning_tokens": sum(
            estimate for _, estimate in INKLING_AGGREGATE_SPLITS.values()
        ),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--summary", required=True, type=Path)
    parser.add_argument("--report", required=True, type=Path)
    parser.add_argument("--output-summary", required=True, type=Path)
    parser.add_argument("--output-report", required=True, type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    print(
        apply_files(
            summary_path=args.summary,
            report_path=args.report,
            output_summary_path=args.output_summary,
            output_report_path=args.output_report,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
