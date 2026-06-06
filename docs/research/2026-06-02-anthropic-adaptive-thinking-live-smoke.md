---
title: Anthropic Adaptive Thinking Live Smoke
date: 2026-06-02
type: research
status: draft
---

# Anthropic Adaptive Thinking Live Smoke

> **Superseded / refined by
> [`2026-06-03-opus-4-8-adaptive-thinking-diagnosis.md`](2026-06-03-opus-4-8-adaptive-thinking-diagnosis.md).**
> This note's conclusion ("points away from the benchmark parser") was only
> partly right: the zero-thinking on trivial prompts is expected provider
> behavior, but the benchmark's `reasoning_tokens` (summary length, not billed
> thinking) and an Opus-specific cost-undercharge bug were also material. See the
> diagnosis for the full root cause and the applied fixes.

Purpose: verify whether the unusual Opus 4.8 reasoning-token curve is caused by
our benchmark stack or by direct Anthropic API behavior.

Source docs checked:

- <https://platform.claude.com/docs/en/build-with-claude/adaptive-thinking>
- <https://platform.claude.com/docs/en/build-with-claude/effort>

The direct smoke used the Keychain-backed `ANTHROPIC_API_KEY` without printing
the raw key. Prompt:

```text
What is 9 + 14 - 1? Reply with just the final answer.
```

Request shape:

```json
{
  "max_tokens": 16000,
  "thinking": {"type": "adaptive"},
  "output_config": {"effort": "max"}
}
```

Observed direct API behavior:

| Model | Status | Content block types | Thinking tokens | Output tokens | Text |
| --- | ---: | --- | ---: | ---: | --- |
| claude-opus-4-8 | 200 | text | 0 | 3 | 22 |
| claude-sonnet-4-6 | 200 | thinking, text | 26 | 32 | 22 |

Variant with `thinking: {"type": "adaptive", "display": "summarized"}` on
`claude-opus-4-8` also returned only a text block and `thinking_tokens: 0`.

Conclusion: the Opus 4.8 max/low-thinking anomaly reproduces below Inspect and
below ObviousBench on this simple prompt. The current evidence points away from
the benchmark parser as the primary cause. It may be Anthropic API behavior for
very simple prompts, a docs-vs-runtime mismatch, or a provider-side issue with
Opus 4.8 adaptive `max`.
