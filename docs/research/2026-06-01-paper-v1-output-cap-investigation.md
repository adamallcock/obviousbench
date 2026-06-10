---
title: Paper V1 Output Cap Investigation
date: 2026-06-01
type: research
status: draft
---

# Paper V1 Output Cap Investigation

## Summary

The 2026-06-01 `paper-v1-final` sweep used `max_tokens=64`. This was intended
as a short-answer safety bound, but it materially contaminated the final result
artifacts. The cap truncates some models before their final answer is emitted,
turning generation-limit artifacts into apparent answer or format failures.

The current final-sweep result artifacts should not be used for paper claims
until the model panel is rerun with the updated high output safety cap.

## Trigger Example

Reference:

```text
run=paper-v1-final sample=obviousbench.arith.en.v0.public.000020 epoch=1 model=openrouter/nvidia/nemotron-3-nano-30b-a3b
```

Original final-sweep configuration:

```json
{"max_tokens":64,"temperature":0}
```

Original logged output:

```text
The user asks: "Answer the question. Return only the final answer, with no explanation.

Question: What is 22 + 27 - 2?
Answer:"

We need to compute 22 + 27 - 2 = 49 - 2? Wait 22+
```

Inspect recorded:

- `stop_reason=max_tokens`
- `output_tokens=64`
- target: `47`
- rescored failure type: `ambiguous_output`

The scorer behavior is reasonable for the truncated text. The bug is the run
configuration, not the grader.

## Controlled Probe

A one-sample no-cache rerun used the same model and sample with only the output
cap changed to `max_tokens=20000`.

Probe output:

```text
47
```

Probe metadata:

- `stop_reason=stop`
- `input_tokens=47`
- `output_tokens=38`
- `reasoning_tokens=25`
- rescored result: correct

This directly supports the hypothesis that the 64-token cap caused the cited
failure.

## Prevalence In Final Sweep

The prevalence check used the final manifest and excluded provider errors using
the same provider-error detector used by the analysis loader.

| Model | Scored | Strict failures | Capped scored | Capped failures | Share of failures capped |
| --- | ---: | ---: | ---: | ---: | ---: |
| OpenAI GPT-5 nano minimal | 80 | 18 | 2 | 2 | 11.1% |
| OpenAI GPT-4.1 | 80 | 20 | 0 | 0 | 0.0% |
| OpenAI GPT-4.1 mini | 80 | 9 | 0 | 0 | 0.0% |
| Anthropic Claude Sonnet 4.6 | 80 | 13 | 1 | 1 | 7.7% |
| Anthropic Claude Haiku 4.5 | 80 | 22 | 1 | 1 | 4.5% |
| Gemini 3.5 Flash | 80 | 47 | 62 | 44 | 93.6% |
| Gemini 2.5 Flash-Lite | 80 | 24 | 0 | 0 | 0.0% |
| Grok 4.3 | 70 | 31 | 4 | 4 | 12.9% |
| Xiaomi MiMo-V2-Flash | 80 | 11 | 0 | 0 | 0.0% |
| NVIDIA Nemotron 3 Nano 30B A3B | 80 | 69 | 77 | 69 | 100.0% |
| OpenAI GPT-OSS 20B | 80 | 50 | 51 | 50 | 100.0% |
| Qwen3 Next 80B A3B Instruct | 80 | 19 | 0 | 0 | 0.0% |
| Total | 950 | 333 | 198 | 171 | 51.4% |

The most affected models are Nemotron, GPT-OSS 20B, and Gemini 3.5 Flash.

## Action Taken

The model-panel policy now treats output length as a high safety cap rather than
a behavioral constraint:

- Default paper-panel output cap: `max_tokens=10000`.
- Provider-specific clamp: if a provider advertises a lower positive completion
  ceiling, use that ceiling.
- Current paper panel: all entries use `max_tokens=10000`; future entries are
  clamped lower only when a provider advertises a positive completion ceiling
  below 10000.

Updated artifacts:

- `configs/paper_v1_model_panel.yaml`
- `configs/model_registry_v1.yaml`
- `scripts/build_model_registry.mjs`
- `docs/research/2026-06-01-paper-v1-final-sweep-plan.md`
- `docs/research/2026-06-01-paper-v1-model-panel-cost-estimates.md`
- `docs/research/2026-06-01-paper-v1-model-panel-cost-estimates.csv`

## Recommendation

Do not patch the old final results in place. Rerun the 12-model paper sweep under
a fresh raw/summary root with the updated cap, then regenerate comparison,
figures, report HTML, wrong-answer review, and paper tables from that new root.
