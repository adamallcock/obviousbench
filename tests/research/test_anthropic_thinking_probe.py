from __future__ import annotations

import csv
from pathlib import Path

import yaml

from obviousbench.research.anthropic_thinking_probe import build_probe_rows


def _write_panel(path: Path) -> None:
    path.write_text(
        yaml.safe_dump(
            {
                "defaults": {"generation_settings": {"seed": 20260531}},
                "entries": [
                    {
                        "id": "opus-max",
                        "label": "Claude Opus 4.8 max",
                        "provider_route": "anthropic",
                        "inspect_model": "anthropic/claude-opus-4-8",
                        "control_style": "anthropic_adaptive_thinking_effort",
                        "configured_reasoning_tokens_per_sample": 32700,
                        "generation_settings": {
                            "max_tokens": 328_000,
                            "effort": "max",
                        },
                        "estimated_usage": {
                            "reasoning_tokens_per_sample": 384,
                            "output_tokens_billed": 800,
                            "sample_count": 4,
                        },
                    },
                    {
                        "id": "sonnet-max",
                        "label": "Claude Sonnet 4.6 max",
                        "provider_route": "anthropic",
                        "inspect_model": "anthropic/claude-sonnet-4-6",
                        "control_style": "anthropic_adaptive_thinking_effort",
                        "configured_reasoning_tokens_per_sample": 30_000,
                        "generation_settings": {
                            "max_tokens": 30_000,
                            "effort": "max",
                        },
                        "estimated_usage": {
                            "reasoning_tokens_per_sample": 50,
                            "output_tokens_billed": 2_000,
                            "sample_count": 4,
                        },
                    },
                ],
            },
            sort_keys=False,
        ),
        encoding="utf-8",
    )


def _write_summary(summary_dir: Path, *, reasoning_values: list[int]) -> None:
    summary_dir.mkdir(parents=True)
    total_reasoning = sum(reasoning_values)
    sample_count = len(reasoning_values)
    (summary_dir / "summary.csv").write_text(
        (
            "model,reasoning_effort,total_samples,scored_samples,answer_accuracy,"
            "strict_accuracy,input_tokens,output_tokens,reasoning_tokens,total_tokens,"
            "estimated_cost_usd,reasoning_token_source\n"
            f"anthropic/test,max,{sample_count},{sample_count},1,1,100,200,"
            f"{total_reasoning},{300 + total_reasoning},0.01,reported\n"
        ),
        encoding="utf-8",
    )
    with (summary_dir / "usage_by_sample.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["sample_id", "reasoning_tokens", "output_tokens"],
            lineterminator="\n",
        )
        writer.writeheader()
        for index, reasoning_tokens in enumerate(reasoning_values):
            writer.writerow(
                {
                    "sample_id": f"sample-{index}",
                    "reasoning_tokens": reasoning_tokens,
                    "output_tokens": 10 + reasoning_tokens,
                }
            )


def test_build_probe_rows_reports_request_shape_and_usage_flags(tmp_path: Path):
    panel_path = tmp_path / "panel.yaml"
    summary_root = tmp_path / "summaries"
    _write_panel(panel_path)
    _write_summary(summary_root / "opus-max", reasoning_values=[0, 0, 10, 0])
    _write_summary(summary_root / "sonnet-max", reasoning_values=[50, 60, 70, 70])

    rows = build_probe_rows(panel_path=panel_path, summary_root=summary_root)

    assert [row.entry_id for row in rows] == ["opus-max", "sonnet-max"]
    assert rows[0].generation_settings["reasoning_effort"] == "max"
    assert rows[0].request_thinking_type == "adaptive"
    assert rows[0].request_thinking_display == "summarized"
    assert rows[0].request_output_effort == "max"
    assert rows[0].observed_reasoning_tokens_per_sample == 2.5
    assert rows[0].reasoning_nonzero_samples == 1
    # Effort warnings are now baselined on billed output tokens, not on the
    # summary-length reasoning axis.
    assert rows[0].observed_output_tokens_per_sample == 12.5
    assert rows[0].estimated_output_tokens_per_sample == 200.0
    assert rows[0].observed_to_estimated_output_ratio == 0.0625
    assert "observed_output_below_estimate" in rows[0].warnings
    assert "thinking_blocks_sparse" in rows[0].warnings
    assert rows[1].observed_reasoning_tokens_per_sample == 62.5
    assert rows[1].reasoning_nonzero_samples == 4
    assert rows[1].observed_output_tokens_per_sample == 72.5
    assert rows[1].warnings == ()
