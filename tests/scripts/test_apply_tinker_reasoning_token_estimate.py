import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
SCRIPT_PATH = ROOT / "scripts/release/apply_tinker_reasoning_token_estimate.py"
SPEC = importlib.util.spec_from_file_location("apply_tinker_reasoning_estimate", SCRIPT_PATH)
assert SPEC is not None
assert SPEC.loader is not None
estimate_script = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(estimate_script)


def inkling_rows() -> list[dict[str, str]]:
    return [
        {
            "provider_model": estimate_script.TINKER_MODEL,
            "reasoning_effort": effort,
            "output_tokens": str(completion),
            "reasoning_tokens": "0",
            "total_tokens": str(22000 + completion),
        }
        for effort, (completion, _) in estimate_script.INKLING_AGGREGATE_SPLITS.items()
    ]


def test_apply_estimate_preserves_billed_completion_and_marks_only_enabled_efforts():
    rows = inkling_rows()
    updated = estimate_script.apply_estimate(rows)

    for row in updated:
        completion, estimate = estimate_script.INKLING_AGGREGATE_SPLITS[
            row["reasoning_effort"]
        ]
        assert int(row["output_tokens"]) + int(row["reasoning_tokens"]) == completion
        assert row["reasoning_tokens"] == str(estimate)


def test_apply_estimate_rejects_unexpected_billed_completion_total():
    rows = inkling_rows()
    rows[0]["output_tokens"] = "1"

    with pytest.raises(ValueError, match="unexpected pre-estimate token split"):
        estimate_script.apply_estimate(rows)


def test_apply_estimate_is_idempotent_for_a_verified_release_split():
    once = estimate_script.apply_estimate(inkling_rows())
    assert estimate_script.apply_estimate(once) == once


def test_report_marks_estimates_without_changing_the_none_row():
    rows = estimate_script.apply_estimate(inkling_rows())
    lines = [
        "# Report",
        "",
        "- Incomplete rows are shown but should not be used for final public claims.",
        "",
    ]
    for row in inkling_rows():
        lines.append(
            "| {provider_model} | {reasoning_effort} | 144/144 | 432 | 1 | 1 | 1 | "
            "22000 | {output_tokens} | {reasoning_tokens} | {total_tokens} | 0.1 | 0 | 0 |".format(
                **row
            )
        )

    report = estimate_script.update_report_markdown("\n".join(lines), rows)

    assert estimate_script.REPORT_ESTIMATE_NOTE in report
    assert (
        "| thinkingmachines/Inkling | none | 144/144 | 432 | 1 | 1 | 1 | 22000 | 2716 | 0 |"
        in report
    )
    assert (
        "| thinkingmachines/Inkling | high | 144/144 | 432 | 1 | 1 | 1 | 22000 | 2720 | ~40167 |"
        in report
    )
