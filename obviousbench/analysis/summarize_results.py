"""Summary command helpers."""

from pathlib import Path

from obviousbench.analysis.build_failure_gallery import build_failure_gallery
from obviousbench.analysis.costing import price_records_with_runcost
from obviousbench.analysis.export_csv import export_summary_csv
from obviousbench.analysis.logs import load_eval_logs_with_failures
from obviousbench.analysis.metamorphic import (
    compute_metamorphic_consistency,
    export_metamorphic_consistency_csv,
)
from obviousbench.analysis.metrics import compute_summary
from obviousbench.analysis.usage import (
    compute_usage_by_family,
    compute_usage_by_question,
    compute_usage_by_section,
    export_usage_by_family_csv,
    export_usage_by_question_csv,
    export_usage_by_sample_csv,
    export_usage_by_section_csv,
    write_cost_ledger,
)


def summarize_results(
    logs: Path,
    out: Path,
    *,
    cost_mode: str = "none",
    rescore: bool = False,
) -> tuple[Path, ...]:
    records, failures = load_eval_logs_with_failures(logs, rescore=rescore)
    cost_ledger = None
    if cost_mode == "runcost":
        records, cost_ledger = price_records_with_runcost(records)
    elif cost_mode != "none":
        raise ValueError(f"Unknown cost mode: {cost_mode}")

    rows = compute_summary(records)
    out.mkdir(parents=True, exist_ok=True)
    summary_path = out / "summary.csv"
    gallery_path = out / "failure_gallery.md"
    sample_usage_path = out / "usage_by_sample.csv"
    family_usage_path = out / "usage_by_family.csv"
    section_usage_path = out / "usage_by_section.csv"
    question_usage_path = out / "usage_by_question.csv"
    metamorphic_consistency_path = out / "metamorphic_consistency.csv"
    export_summary_csv(rows, summary_path)
    export_usage_by_sample_csv(records, sample_usage_path)
    export_usage_by_family_csv(compute_usage_by_family(records), family_usage_path)
    export_usage_by_section_csv(compute_usage_by_section(records), section_usage_path)
    export_usage_by_question_csv(compute_usage_by_question(records), question_usage_path)
    gallery_path.write_text(build_failure_gallery(failures, limit=25), encoding="utf-8")
    paths = [
        summary_path,
        gallery_path,
        sample_usage_path,
        family_usage_path,
        section_usage_path,
        question_usage_path,
    ]
    metamorphic_rows = compute_metamorphic_consistency(records)
    if metamorphic_rows:
        export_metamorphic_consistency_csv(
            metamorphic_rows,
            metamorphic_consistency_path,
        )
        paths.append(metamorphic_consistency_path)
    if cost_ledger is not None:
        cost_ledger_path = out / "cost_ledger.json"
        write_cost_ledger(cost_ledger, cost_ledger_path)
        paths.append(cost_ledger_path)
    return tuple(paths)
