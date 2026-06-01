"""Build Markdown failure galleries."""

import json
from dataclasses import dataclass


@dataclass(frozen=True)
class FailureGalleryEntry:
    model: str
    family: str
    sample_id: str
    question: str
    expected_answer: str
    extracted_answer: str | None
    raw_output: str
    failure_type: str
    human_triviality: str
    source_type: str
    why_obvious: str
    run: str = ""
    epoch: int | str = 1

    @property
    def reference(self) -> str:
        parts = []
        if self.run:
            parts.append(f"run={self.run}")
        parts.extend(
            [
                f"sample={self.sample_id}",
                f"epoch={self.epoch}",
                f"model={self.model}",
            ]
        )
        return " ".join(parts)


def build_failure_gallery(entries: list[FailureGalleryEntry], limit: int = 10) -> str:
    selected = entries[:limit]
    lines = ["# ObviousBench Failure Gallery", ""]
    for index, entry in enumerate(selected, start=1):
        lines.extend(
            [
                f"## Failure {index}: {entry.family}",
                "",
                f"- Model: `{entry.model}`",
                f"- Sample ID: `{entry.sample_id}`",
                f"- Reference: `{entry.reference}`",
                _copy_reference_button(entry.reference),
                f"- Question: {entry.question}",
                f"- Expected answer: `{entry.expected_answer}`",
                f"- Extracted answer: `{entry.extracted_answer}`",
                f"- Raw model answer: `{entry.raw_output}`",
                f"- Failure type: `{entry.failure_type}`",
                f"- Human triviality: `{entry.human_triviality}`",
                f"- Source type: `{entry.source_type}`",
                f"- Why humans find it obvious: {entry.why_obvious}",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def _copy_reference_button(reference: str) -> str:
    encoded = json.dumps(reference)
    return (
        f"<button type=\"button\" onclick='navigator.clipboard.writeText({encoded})'>"
        "Copy reference</button>"
    )
