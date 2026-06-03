#!/usr/bin/env python
"""Tiny diagnostic: billed thinking vs summary length for Claude 4.x thinking.

Demonstrates that for Claude 4.x ``usage.output_tokens_details.thinking_tokens``
(billed thinking) diverges from the re-tokenized ThinkingBlock *summary* that
Inspect historically counted as ``reasoning_tokens`` -- the summary can exceed the
billed thinking and even ``output_tokens``. Also shows that adaptive thinking +
``effort=max`` still produces zero thinking on trivial prompts (effort is soft
guidance, not a floor).

Supports the diagnosis in
docs/research/2026-06-03-opus-4-8-adaptive-thinking-diagnosis.md.

Reads the API key from $ANTHROPIC_API_KEY (never prints it). On macOS:

    ANTHROPIC_API_KEY="$(security find-generic-password -s ANTHROPIC_API_KEY -w)" \\
        .venv/bin/python scripts/smoke_anthropic_thinking.py

Cost is tiny (max_tokens capped; prompts are short).
"""

from __future__ import annotations

import os

import anthropic

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

PROMPTS = {
    "trivial": "What is 9 + 14 - 1? Reply with just the final answer.",
    "harder": (
        "Three switches outside a room control three bulbs inside it; you may "
        "flip switches freely but enter the room only once. Explain how to "
        "determine which switch controls which bulb. Be concise."
    ),
}
MODELS = ["claude-opus-4-8", "claude-sonnet-4-6"]


def count_tokens(model: str, text: str) -> object:
    if not text:
        return 0
    try:
        r = client.messages.count_tokens(
            model=model, messages=[{"role": "user", "content": text}]
        )
        return r.input_tokens
    except Exception as exc:  # noqa: BLE001
        return f"count_err:{type(exc).__name__}"


def main() -> int:
    header = (
        f"{'model':<20} {'prompt':<8} {'blocks':<16} {'out_tok':>7} "
        f"{'think_tok':>9} {'sum_len_tok':>11} {'stop':<10}"
    )
    print(header)
    print("-" * len(header))
    for model in MODELS:
        for label, prompt in PROMPTS.items():
            try:
                resp = client.messages.create(
                    model=model,
                    max_tokens=1500,
                    thinking={"type": "adaptive", "display": "summarized"},
                    extra_body={"output_config": {"effort": "max"}},
                    messages=[{"role": "user", "content": prompt}],
                )
            except Exception as exc:  # noqa: BLE001
                print(f"{model:<20} {label:<8} ERROR {type(exc).__name__}: {str(exc)[:70]}")
                continue
            types = [b.type for b in resp.content]
            thinking_text = "".join(
                getattr(b, "thinking", "") or ""
                for b in resp.content
                if b.type == "thinking"
            )
            usage = resp.usage.model_dump()
            otd = usage.get("output_tokens_details") or {}
            think_tok = otd.get("thinking_tokens")
            summary_len = count_tokens(model, thinking_text)
            print(
                f"{model:<20} {label:<8} {','.join(types):<16} "
                f"{usage.get('output_tokens'):>7} {str(think_tok):>9} "
                f"{str(summary_len):>11} {resp.stop_reason:<10}"
            )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
