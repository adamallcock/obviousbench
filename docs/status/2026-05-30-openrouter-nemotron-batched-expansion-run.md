---
title: OpenRouter Nemotron Batched Expansion Run
date: 2026-05-30
type: status
status: draft
---

# OpenRouter Nemotron Batched Expansion Run

> Snapshot note: this is a draft run log for one OpenRouter batching experiment.
> Use `docs/runbook.md` for current runner guidance and treat the commands below
> as historical evidence, not the canonical workflow.

## Run

Model:

```text
openrouter/nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free
```

Command:

```bash
.venv/bin/python scripts/run_openrouter_batches.py \
  --task obviousbench/tasks/archetype_expansions.py \
  --dataset data/public_v0/archetype_expansions_2026-05-30.jsonl \
  --batch-size 2 \
  --inspect-max-retries 1 \
  --timeout 90 \
  --attempt-timeout 45 \
  --max-batch-retries 3 \
  --log-dir results/raw/openrouter-nemotron-batched-2026-05-30-small
```

The initial `batch-size 8`, `inspect-max-retries 6`, `timeout 900` attempt was
stopped because Inspect stayed inside provider retry/backoff too long for one
batch to be operationally useful.

The completed small-batch run intentionally used `attempt-timeout 45`, which is
where the per-sample `AttemptTimeoutError` rows came from. That value is too low
for this reasoning-heavy free model if complete coverage is the priority.

## Outputs

Raw logs:

```text
results/raw/openrouter-nemotron-batched-2026-05-30-small/
```

Summary:

```text
results/summaries/openrouter-nemotron-batched-2026-05-30-small/summary.csv
results/summaries/openrouter-nemotron-batched-2026-05-30-small/failure_gallery.md
```

## Metrics

```text
total samples: 50
scored samples: 37
correct scored samples: 34
scored failures: 3
provider errors: 13
accuracy over scored samples: 0.918918918918919
obvious failure rate over scored samples: 0.08108108108108109
```

Failure type counts:

```text
none: 34
provider-error/non-answer equivalent: 13
ordering_error: 1
wrong_letter_or_substring: 1
non_answer: 1
```

Provider errors by family:

```text
arithmetic: 1
format_compliance: 2
negation: 1
ordering: 1
spelling_transform: 2
word_count: 6
```

## Scored Failures

1. `obviousbench.ordering.en.v0.public.000047`
   - Question: sort `3.1, 3.01, 3.2`
   - Expected: `3.01, 3.1, 3.2`
   - Output: `[3.01,3.1, 3.2]`
   - Interpretation: model answer is semantically correct. Follow-up fixed the
     list scorer so bracketed list notation is normalized going forward.

2. `obviousbench.spell.en.v0.public.000033`
   - Question: spell `cabinet` backwards
   - Expected: `tenibac`
   - Output: `tneicab`
   - Interpretation: true model failure.

3. `obviousbench.spell.en.v0.public.000034`
   - Question: spell `bicycle` backwards
   - Expected: `elcycib`
   - Output: empty
   - Interpretation: confirmed in the raw `.eval`: no provider error, no time
     limit, stop reason `stop`, and empty assistant text after a reasoning
     chunk. This is a true non-answer / generation issue.

## Operational Notes

- No hard process-level 429 stopped the run.
- Because the wrapper currently runs Inspect with `--score-on-error`, late-run
  sample-level `RateLimitError`s were logged as provider errors rather than
  causing a batch retry.
- This mode is useful for collecting partial benchmark signal under free-model
  limits.
- If the goal is complete coverage with no provider-error rows, the wrapper
  should support a strict mode that omits `--score-on-error` and lets 429s fail
  the batch so the outer `X-RateLimit-Reset` sleep/retry logic can handle them.

Follow-up implemented:

- Default wrapper `--attempt-timeout` is now `180`.
- `--independent-batches` writes each batch into a separate `batch-XXXX`
  directory and appends status to `batch-manifest.jsonl`.
- `--resume` skips prior successful batches.
- `--strict-batch-errors` omits `--score-on-error` / `--no-fail-on-error` so
  provider failures can fail the batch and be retried externally.
- `--continue-after-batch-error` records failed batches but continues later
  batches, returning a non-zero exit code at the end if any batch failed.

Recommended rerun shape for better coverage:

```bash
.venv/bin/python scripts/run_openrouter_batches.py \
  --task obviousbench/tasks/archetype_expansions.py \
  --dataset data/public_v0/archetype_expansions_2026-05-30.jsonl \
  --batch-size 4 \
  --inspect-max-retries 6 \
  --timeout 900 \
  --attempt-timeout 180 \
  --independent-batches \
  --resume \
  --continue-after-batch-error
```
