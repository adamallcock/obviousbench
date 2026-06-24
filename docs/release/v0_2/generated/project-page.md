# ObviousBench v0.2 Project Page Draft

## Generated Artifact Notice

- Source config: `configs/releases/release_v0_2_0.yaml`
- Generator: `uv run --extra dev python scripts/release/build_v0_2_release_assets.py --config configs/releases/release_v0_2_0.yaml`
- Release date: `2026-06-18`
- Status: `local-publication-prep`
- Public/private boundary: excludes private held-out prompts, raw outputs,
  item-level private outcomes, private review HTML, and attempt-level outcomes.


ObviousBench catches obvious AI mistakes before users do.

It asks models questions that look too simple to miss: literal
counting, spelling transforms, ordering, negation, formatting,
arithmetic, word counting, and basic constraint awareness.

The v0.2 private pass^3 run shows the desired shape. The strongest
models and highest test-time-compute settings can saturate the
benchmark, which is evidence that the questions are solvable rather
than broken. Lower-compute, smaller, or no-thinking rows still fail
often enough to expose the practical risk: a model can look capable
and still make obvious mistakes.

## Why This Exists

Modern models can summarize long documents, write code, and operate
tools, yet still stumble on small literal tasks users instantly
recognize. These failures are not always catastrophic, but they are
embarrassing, trust-eroding, and often avoidable with the right
model/configuration tradeoff.

ObviousBench turns that failure mode into a small, reproducible
preflight check.

## How Product Teams Should Use It

- Compare candidate models and thinking settings before launch.
- Track regressions when changing providers, prompts, or routing.
- Inspect failure examples to decide whether a cheap/small model is
  acceptable for a workflow.
- Keep answer correctness separate from format compliance so product
  teams can see both reasoning failures and interface failures.

## Top Saturated Rows

| Model | Effort | Answer pass^3 | Strict pass^3 | Cost | Reasoning tok |
|---|---|---|---|---|---|
| google/gemma-4-31b-it | high | 100.0% | 100.0% | $0.03 | 43350 |
| google/gemma-4-31b-it | low | 100.0% | 100.0% | $0.03 | 44722 |
| qwen/qwen3.5-27b | default | 100.0% | 100.0% | $0.27 | 160625 |
| openai/o3 | medium | 100.0% | 100.0% | $0.54 | 46428 |
| openai/o3 | high | 100.0% | 100.0% | $0.62 | 56094 |
| openai/gpt-5 | medium | 100.0% | 100.0% | $0.71 | 51584 |
| openai/gpt-5.5 | medium | 100.0% | 100.0% | $0.74 | 17991 |
| google/gemini-3.5-flash | high | 100.0% | 100.0% | $1.00 | 106673 |

## High Failure-Risk Rows

| Model | Effort | Answer pass^3 | Strict pass^3 | Cost | Reasoning tok |
|---|---|---|---|---|---|
| openai/gpt-3.5-turbo-instruct | none | 17.4% | 13.2% | $0.04 | 0 |
| meta-llama/llama-3.1-8b-instruct | none | 20.8% | 18.1% | $0.00 | 0 |
| meta-llama/llama-3.2-11b-vision-instruct | none | 23.6% | 22.2% | $0.01 | 0 |
| meta-llama/llama-3.2-1b-instruct | none | 24.3% | 24.3% | $0.00 | 0 |
| mistralai/ministral-3b-2512 | default | 25.0% | 25.0% | $0.00 | 0 |
| mistralai/mistral-small-24b-instruct-2501 | default | 31.9% | 28.5% | $0.01 | 0 |
| google/gemma-3-4b-it | none | 36.1% | 36.1% | $0.00 | 0 |
| openai/gpt-5.4-nano | none | 36.8% | 36.1% | $0.01 | 0 |

## Public Boundary

The project page can show aggregate private results and public example
questions. It must not show private held-out questions, raw private
outputs, item-level private outcomes, or private review HTML.

## What Not To Claim

Do not use ObviousBench as a global ranking, a general intelligence
measure, a human-baseline claim, or a permanent statement about a
provider. It is a frozen reliability snapshot for a deliberately
narrow class of visible mistakes.
