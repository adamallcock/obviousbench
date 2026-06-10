---
title: Prompt Optimizer Research Agent Prompt
date: 2026-06-02
type: research
status: draft
---

# Prompt Optimizer Research Agent Prompt

Use the prompt below with a high-reasoning research agent. It is designed to be standalone: the agent should not need this chat transcript.

## Copy-Ready Prompt

```text
You are a GPT-5.5 Pro research agent. Your job is to perform a decision-quality technical and market research pass for a proposed reusable prompt-optimization system.

Current date: 2026-06-02.

You must browse the web, inspect GitHub repositories, read official documentation, inspect package registries, and separate verified facts from assumptions. Prefer primary sources: official docs, GitHub source, package registries, release notes, papers, examples, tests, and issue discussions. Treat README and marketing claims as hypotheses until checked against docs, code, examples, tests, package activity, or a live smoke if your environment supports one.

Do not produce a generic list of tools. Produce a decision-ready recommendation about whether we should use GEPA, Promptfoo, Promptolution, some other existing framework, or custom code for the core optimizer.

## Project Context

We have a benchmark project called ObviousBench. It evaluates LLMs on "obvious" tasks where mistakes are easy to score. The current benchmark already has:

- Deterministic scoring for item families.
- Inspect-based benchmark running.
- Cached model runs.
- Model/provider/generation settings.
- Cost estimation and pricing integration.
- Wilson intervals and paired/bootstrap-style comparison logic.
- Reports and run summaries.
- A model registry and thinking/non-thinking setting panels.

The new idea is a reusable prompt-evolution system. The purpose is to test many hypotheses about how system prompt changes can improve a weak or mid-performing student model on a benchmark.

Desired high-level flow:

1. A strong teacher/orchestrator model proposes hypotheses about prompt changes that may improve a weaker student model.
2. The teacher, or a prompt-writing agent, writes candidate system prompts for each hypothesis.
3. The benchmark runner evaluates candidate prompts against the student model.
4. Deterministic scoring evaluates results.
5. Statistical gates decide whether candidates are promoted, continued, or dropped.
6. Results and commentary are stored so future teacher iterations know what was already tried.
7. Many hypotheses and candidate prompts should be testable concurrently.

This system might be used many times outside ObviousBench, so we are considering spinning it out into a standalone reusable repo/package and importing or adapting it into ObviousBench.

## Current Working Hypothesis

The current tentative recommendation is:

- Use GEPA as the primary optimizer backend.
- Use Promptolution as a secondary backend worth testing.
- Use Promptfoo as an optional eval/export/CI/UI harness, but probably not the core optimizer.
- Keep ObviousBench as the source of truth for item generation, scoring, cache behavior, cost estimation, and statistical promotion.
- Build only the reusable shell: benchmark adapters, prompt/hypothesis storage, lineage, rate/cost planning, decision gates, reports, and teacher memory.

This is not final. Your job is to pressure-test it.

## Key Question

Are we sure GEPA is the right primary backend, rather than Promptfoo, Promptolution, another framework, or custom code?

Answer this as a build-vs-buy decision:

- Stop: an existing tool already solves the real need directly.
- Use: adopt an existing tool directly.
- Wrap: build a thin adapter/orchestration layer around an existing tool.
- Contribute: a strong project is missing only a small feature.
- Fork: a close project is directionally blocked but salvageable.
- Build: custom implementation is justified because existing tools do not fit.

## Must-Have Capabilities

Evaluate each candidate against these requirements:

1. Optimizes plain system prompts or arbitrary text artifacts, not only a framework-specific LLM program.
2. Supports a strong teacher/reflection model and a weak student/target model.
3. Accepts deterministic benchmark scores from external code.
4. Can use per-item failure traces or side information, not only scalar aggregate scores.
5. Supports train/validation or holdout splits.
6. Supports many hypotheses and many prompt candidates per hypothesis.
7. Supports high throughput or can be wrapped with external concurrency/rate-limit control.
8. Preserves prompt lineage, candidate ancestry, and run artifacts.
9. Allows metric-call budgets, stopping rules, retries, and cost controls.
10. Can integrate with local scoring/caching without duplicating benchmark logic.
11. Can produce artifacts suitable for later teacher memory: tested hypothesis, candidate prompt, parent prompt, scores, confidence intervals, failure patterns, and final decision.
12. Is reusable beyond ObviousBench.

## Candidate Tools To Investigate

At minimum, investigate:

- GEPA: https://github.com/gepa-ai/gepa
- Promptfoo: https://github.com/promptfoo/promptfoo and https://www.promptfoo.dev/docs/usage/prompt-optimization/
- Promptolution: https://github.com/automl/promptolution
- MLflow prompt optimization: https://mlflow.org/docs/latest/genai/prompt-registry/optimize-prompts/
- DeepEval prompt optimization: https://deepeval.com/docs/prompt-optimization-introduction
- DSPy GEPA/MIPROv2: https://github.com/stanfordnlp/dspy
- PromptWizard: https://github.com/microsoft/PromptWizard
- SAMMO: https://github.com/microsoft/sammo
- TextGrad: https://github.com/zou-group/textgrad
- OpenAI Prompt Optimizer: https://developers.openai.com/api/docs/guides/prompt-optimizer/

Also search GitHub and the web for newer or better alternatives using queries like:

- "automatic prompt optimization framework GitHub"
- "GEPA prompt optimization arbitrary metric"
- "prompt optimizer deterministic scorer custom evaluator"
- "evolutionary prompt optimization framework"
- "LLM prompt optimization train validation custom metric"
- "prompt optimization benchmark harness"
- "system prompt optimizer GitHub"

Include any strong candidates you find, even if they are not on the list.

## Specific Research Tasks

For each serious candidate, verify:

1. What layer it primarily solves: optimizer, eval harness, prompt registry, observability platform, agent framework, or algorithm research code.
2. Whether it can optimize a plain system prompt with an arbitrary external scorer.
3. Whether it supports a separate teacher/reflection model and student/task model.
4. Whether it captures or accepts per-example failure traces.
5. Whether it supports holdouts, train/validation splits, or anti-overfit mechanisms.
6. Whether it supports candidate lineage and artifacts.
7. Whether it supports custom concurrency/rate-limit/cost controls, or can be externally wrapped.
8. Whether its API is stable enough to depend on.
9. Its package/repo health: stars, forks, commit recency, release recency, license, package version, docs quality, tests/examples, issue/PR activity.
10. Its integration cost with an existing Python benchmark that already has scoring, caching, and stats.

If you can run code, do small local smokes for the top 2-3 candidates:

- Install/import the package in an isolated environment.
- Print package version if available.
- Inspect the main optimization function signatures.
- Confirm whether custom evaluator/adapter paths exist.
- Do not spend money on model calls unless explicitly permitted. API-free import/API smokes are enough.

## Current Evidence To Verify Or Falsify

Known preliminary evidence from an earlier pass:

- GEPA appeared to expose `gepa.optimize(...)`.
- `gepa.optimize(...)` appeared to accept seed candidates, trainset, valset, adapter/evaluator, task model, reflection model, metric-call budget, callbacks, run directory, caching, seed, and validation policy.
- GEPA documentation appeared to describe arbitrary text parameter optimization and an adapter interface.
- Promptfoo documentation appeared to say `promptfoo optimize` improves one configured prompt against one configured provider, and that optimization targets exactly one resolved prompt/provider pair.
- Promptfoo appeared very mature as an eval/CI/red-team harness.
- Promptolution imported locally and exposed optimizer modules such as CAPO, EvoPromptDE, EvoPromptGA, and OPRO, but its exact adapter fit was not yet proven.

Verify these points live. If they are wrong, say so.

## Required Output

Produce a structured report with these sections:

1. Executive Decision

State the recommendation in one paragraph:

- primary choice,
- backup choice,
- what to build custom,
- what not to build,
- confidence level,
- what evidence would change the decision.

2. Capability Matrix

Provide a table with rows for each candidate and columns:

- Candidate
- Primary layer
- Plain system prompt optimization
- External deterministic scorer support
- Teacher/student model separation
- Per-item trace/side-info support
- Holdout/anti-overfit support
- Lineage/artifacts
- Concurrency/cost controls
- Integration cost with ObviousBench-like benchmark
- Repo/package health
- Decision: use, wrap, optional, reject, or investigate

3. GEPA Deep Dive

Answer:

- What exactly does GEPA solve?
- What API would we likely use?
- What adapter would we need to write?
- What artifacts does GEPA preserve?
- How would it receive ObviousBench failure traces?
- Where could GEPA fail us?
- What is the smallest spike that proves or kills GEPA?

4. Promptfoo Deep Dive

Answer:

- What exactly does Promptfoo solve?
- Is `promptfoo optimize` strong enough for multi-hypothesis prompt evolution?
- What would be gained by using Promptfoo directly?
- What would be lost or duplicated compared with keeping ObviousBench scoring?
- Is Promptfoo better as a core optimizer, secondary harness, CI/export tool, or not useful?

5. Custom Build Analysis

Explain what we should build custom and what we should avoid building custom.

Separate:

- optimizer kernel,
- benchmark adapter,
- storage,
- statistics,
- teacher memory,
- reporting,
- concurrency/rate control,
- prompt registry.

6. Architecture Recommendation

Propose a concrete architecture for a standalone reusable package.

Include:

- package/module layout,
- core data models,
- optimizer backend interface,
- benchmark adapter interface,
- storage/artifact format,
- integration path with ObviousBench,
- how to support multiple optimizer backends,
- how to run many candidates concurrently,
- how to preserve train/validation/holdout discipline,
- how to promote/drop/continue candidates.

7. Spike Plan

Design a 1-2 day proof that can settle the decision.

Include:

- exact experiments,
- no/low-cost smokes,
- minimum benchmark slice,
- pass/fail criteria,
- artifacts to inspect,
- expected commands or pseudocode,
- decision gates for GEPA, Promptfoo, Promptolution, and custom.

8. Source Ledger

List sources with links and one-line notes:

- official docs,
- GitHub repos,
- package registry pages,
- papers,
- code examples,
- relevant issues/PRs.

For each key claim in the report, indicate whether it is:

- verified from primary source,
- verified by local smoke,
- inferred from docs,
- untested,
- model judgment.

## Decision Bias

Prefer existing frameworks and thin wrappers over custom implementation, but do not force adoption if the tool does not fit the actual workflow.

Do not recommend Promptfoo merely because it is more mature if its optimizer layer is too narrow.

Do not recommend GEPA merely because it is fashionable or promising if its API, lineage, artifacts, or adapter surface do not fit.

Do not recommend custom unless you can name the exact unsolved requirements and show that wrapping existing tools would be more expensive or fragile.

The final answer should be clear enough that an engineer can start the spike without another research pass.
```
