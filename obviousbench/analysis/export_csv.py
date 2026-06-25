"""CSV export helpers."""

import csv
from pathlib import Path

from obviousbench.analysis.metrics import SummaryRow


def export_summary_csv(rows: list[SummaryRow], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(SummaryRow.__dataclass_fields__.keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow(row.__dict__)
