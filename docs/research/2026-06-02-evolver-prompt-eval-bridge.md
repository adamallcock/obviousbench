---
title: Evolver Prompt Eval Bridge
date: 2026-06-02
type: decision-record
status: draft
---

# Evolver Prompt Eval Bridge

## Decision

ObviousBench now exposes a narrow `prompt-eval` command for Evolver's external
benchmark adapter:

```bash
obviousbench prompt-eval --request <request.json> --response <response.json>
```

The current command is a no-cost bridge. It reads Evolver's prompt-eval request
shape, scores mock completions with ObviousBench's deterministic scorers, and
writes Evolver-compatible `ItemResult` rows. It does not make student-model
provider calls.

An explicit model-backed mode is available for future paid or cache-backed
student-model runs:

```bash
obviousbench prompt-eval \
  --mode openai \
  --model openai/gpt-5.4-mini \
  --generation-setting reasoning_effort=none \
  --generation-setting max_output_tokens=64 \
  --max-provider-requests 1 \
  --max-total-cost-usd 0.01 \
  --input-price-per-million <input-price> \
  --output-price-per-million <output-price> \
  --reasoning-price-per-million <reasoning-price> \
  --request <request.json> \
  --response <response.json>
```

This mode uses the OpenAI Responses API through an injectable provider, records
provider token usage in `token_usage`, and stores the response id as `trace_uri`
when the SDK returns one. `cost_usd` is left null unless a provider supplies cost
or explicit token prices are provided; when explicit prices are supplied, the
bridge computes and enforces the requested total-cost cap. OpenAI mode requires
`--max-provider-requests`, so a paid smoke has a hard request cap before any
provider call is made.

ObviousBench also exports real benchmark rows into Evolver's external item
manifest shape:

```bash
obviousbench export-evolver-manifest \
  --dataset data/public_v0/format_compliance.jsonl \
  --out /tmp/obviousbench-evolver-format-manifest.jsonl \
  --train-count 4 \
  --validation-count 4
```

## Request Requirements

Each item must provide:

- `id`
- `family`
- `input`
- `expected`
- `metadata.split`, one of `train`, `validation`, or `holdout`
- `metadata.scorer`, such as `exact_integer_extract_first_v0`

For mock scoring, each item must also provide either:

- `metadata.mock_completion`, or
- `metadata.required_prompt_hint` plus `passing_completion` and
  `failing_completion`

The prompt-conditioned form is what lets a zero-cost GEPA smoke prove that
prompt edits flow through ObviousBench scorer decisions.

## Response Shape

The command writes:

```json
{
  "results": [
    {
      "item_id": "train_math",
      "family": "arithmetic",
      "split": "train",
      "prompt_id": "prompt_gepa_1",
      "score": 1.0,
      "parsed_answer": "5",
      "objective_scores": {
        "accuracy": 1.0
      },
      "failure_type": "none",
      "scorer_diagnostics": {
        "scorer": "exact_integer_extract_first_v0",
        "required_hint": "integer only",
        "answer_correct": true,
        "format_correct": true,
        "strict_correct": true
      },
      "token_usage": {
        "input_tokens": 0,
        "output_tokens": 0
      },
      "cost_usd": 0.0
    }
  ]
}
```

## Verified Cross-Repo Smoke

From the Evolver repo, this command shape has been verified against a hand-built
temporary manifest:

```bash
uv run --project . evolver external-gepa-evolve \
  --items-path /tmp/evolver-obviousbench.4SRgIp/items.jsonl \
  --eval-command "/Users/adamallcock/Documents/Coding/benchmark-obviousbench/.venv/bin/obviousbench prompt-eval --request {request} --response {response}" \
  --artifact-dir runs/verify-obviousbench-prompt-eval \
  --max-metric-calls 48
```

Observed result:

```text
backend: gepa_benchmark
best_prompt_id: prompt_gepa_4
best_score: 1.000
num_candidates: 5
total_metric_calls: 52
model_calls: 0
```

The stronger smoke uses an exported manifest from real ObviousBench rows:

```bash
uv run --project . evolver external-gepa-evolve \
  --items-path /tmp/obviousbench-evolver-format-manifest.jsonl \
  --eval-command "/Users/adamallcock/Documents/Coding/benchmark-obviousbench/.venv/bin/obviousbench prompt-eval --request {request} --response {response}" \
  --artifact-dir runs/verify-obviousbench-exported-format \
  --max-metric-calls 48
```

Observed result:

```text
backend: gepa_benchmark
best_prompt_id: prompt_gepa_2
best_score: 1.000
num_candidates: 3
total_metric_calls: 52
model_calls: 0
```

## Remaining Paid-Run Gate

Before a paid evolution run, run a tiny OpenAI-mode smoke with `--max-provider-requests 1`
and explicit token prices or provider-reported cost. The current provider-backed
path preserves the response shape, token usage, response ids, request caps, and
explicit-price cost accounting. The remaining risk is empirical: the paid smoke
has not been run in this thread.
