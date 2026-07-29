---
title: ObviousBench Background And Rhetoric
date: 2026-06-16
type: positioning
status: draft
---

# ObviousBench Background And Rhetoric

This is the hand-authored source for durable ObviousBench v0.2 positioning. It
promotes the reusable language from earlier v0.1 launch drafts, the paused
paper lane, the root build plan, and the generated v0.2 release surfaces while
dropping stale v0.1 counts and paper-specific claims.

Generated release surfaces may adapt this language, but this file is the source
to edit when the public story changes.

## Branding And Tone

Primary tagline:

```text
Catch obvious AI mistakes before users do.
```

Use language around reliability, preflight checks, regression testing, user
trust, public-facing QA, and human-trivial tasks.

Avoid shame language, humiliation language, and claims that a model is generally
bad because it failed one obvious task.

## Core Frame

ObviousBench catches obvious AI mistakes before users do.

It is a compact reliability benchmark for short tasks that people expect a
public-facing AI system to answer correctly every time: letter counts, spelling
transforms, small arithmetic, word and list counting, ordering, negation, format
compliance, and simple constraint awareness.

The benchmark is intentionally narrow. It is not a global model ranking, not a
general intelligence test, and not a shame board. It is a preflight surface for
visible mistakes that are embarrassing, trust-eroding, and often avoidable.

## Why Obvious Tasks Matter

Modern models can summarize long documents, write code, use tools, and reason
across domains. Yet the same systems can still miss a literal letter count, a
required output format, or the object that must be present for a simple
real-world task.

These failures are not always catastrophic. They are worse in a different way:
they are instantly legible to users. A person may forgive uncertainty on an
expert problem, but obvious misses create the feeling that the system is
careless.

ObviousBench turns that product risk into something model and product teams can
measure before launch.

## v0.2 Interpretation

The v0.2 private pass^3 evidence has the desired shape. The strongest
model/config rows saturate or nearly saturate the benchmark, which is evidence
that the questions are solvable rather than broken. The useful signal is the
spread below that ceiling.

Smaller, cheaper, no-thinking, or lower-test-time-compute rows still fail often
enough to expose obvious-mistake risk. That makes the benchmark useful for
model selection, routing, prompt/interface QA, and regression testing.

The product question is practical:

> How much visible obvious-mistake risk are you accepting when you choose a
> cheaper, faster, smaller, or lower-compute route?

Sometimes that tradeoff is worth it. ObviousBench helps make the tradeoff
explicit.

## Metrics Language

Use non-strict answer pass^3 as the v0.2 headline metric. It asks whether all
three attempts for an item/model/config are answer-correct, independent of
strict formatting.

Keep strict correctness and format correctness available as diagnostics:

- answer correctness: did the response contain the right answer?
- format correctness: did the response obey the requested output form?
- strict correctness: were both answer and format correct?

This distinction matters because product teams may treat a wrong answer and a
right answer in the wrong wrapper differently.

## Claims To Make

- ObviousBench is a narrow reliability benchmark for visible, human-trivial
  mistakes.
- v0.2 top-end saturation is a positive sign: the benchmark is solvable with
  enough capability or test-time compute.
- The spread across lower-compute and smaller-model rows is the product signal.
- The benchmark helps compare model/configuration tradeoffs before users see
  avoidable mistakes.
- Deterministic scorers and frozen snapshots make results reproducible and
  auditable.

## Claims To Avoid

- Do not claim ObviousBench ranks all models globally.
- Do not claim a measured human baseline unless one has actually been collected.
- Do not treat provider-route failures as model-quality failures.
- Do not publish private held-out prompts, raw private completions, item-level
  private outcomes, or private review HTML.
- Do not imply that one visible miss proves a model is generally bad.
- Do not explain all failures as one mechanistic cause.

## Public Boundary

The v0.2 public story may include aggregate private results and public example
questions. It must not include private held-out prompts, raw private outputs,
item-level private outcomes, private review HTML, or raw attempt logs.

Until public repository, dataset, and project URLs exist and the public bundle
has been rebuilt and audited with those URLs, all v0.2 release copy remains
local publication prep.
