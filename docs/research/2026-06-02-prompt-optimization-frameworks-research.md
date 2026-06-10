---
title: Prompt Optimization Frameworks Research
date: 2026-06-02
type: research
status: draft
---

# Prompt Optimization Frameworks Research

## Question

Should the prompt-evolution system be a submodule inside ObviousBench, or a reusable standalone system imported by ObviousBench? Which existing prompt optimization harnesses or frameworks should be used off the shelf?

## Short Answer

Spin this out into a separate reusable Python package/repo, then integrate it into ObviousBench through a thin adapter. Do not build a prompt optimizer from scratch.

The best fit is a thin orchestration package around GEPA as the primary optimizer backend, with Promptolution as a secondary algorithm-zoo backend and Promptfoo as an optional eval/export harness. ObviousBench should remain the source of truth for benchmark items, scoring, cache behavior, cost estimates, and statistical promotion gates.

Confidence level: medium-high, not final. GEPA is the leading backend candidate because it matches the missing optimizer kernel. It still needs a small adapter spike before being treated as the committed dependency.

## Evaluation Criteria

The desired system needs to:

- Optimize plain system prompts, not only a framework-specific LLM program.
- Support a strong teacher/reflection model and a weaker student/target model.
- Run many candidate prompts and hypotheses in parallel.
- Accept deterministic benchmark scorers and preserve per-item outputs.
- Store prompt lineage, hypotheses, failures, and promotion decisions.
- Use holdout splits and paired confidence intervals before promotion.
- Reuse ObviousBench barrage generation, scoring, cache, pricing, and reporting where possible.
- Be generic enough to reuse outside ObviousBench.

## Primary Recommendation

Use GEPA as the primary optimization engine.

Why:

- GEPA explicitly optimizes textual parameters such as prompts, code, agent architectures, and configs against arbitrary metrics.
- Its direct `gepa.optimize(...)` path accepts a seed candidate dictionary, train/validation sets, a target model, a reflection model, custom adapters/evaluators, metric-call budgets, callbacks, run directories, caching, and validation policies.
- Its README describes an adapter interface that implements `evaluate` and `make_reflective_dataset`, which maps well to an ObviousBench adapter.
- It is current and active: GitHub API snapshot on 2026-06-02 showed `gepa-ai/gepa` at 4,913 stars, 412 forks, MIT license, and `pushed_at=2026-06-02T00:23:57Z`.
- PyPI snapshot on 2026-06-02 showed `gepa==0.1.1`, uploaded 2026-03-16.
- Local package smoke passed: `uv run --no-project --with gepa python -c ...` imported `gepa`; `gepa.optimize` exists; `gepa.optimize_anything` is available as a module exposing the generic optimization primitives.

Decision: wrap/use.

## GEPA vs Promptfoo vs Custom

This decision should be framed by layer:

- GEPA is an optimizer backend.
- Promptfoo is primarily an evaluation, regression, CI, red-team, and comparison harness with an optimizer command.
- Custom code should cover orchestration, adapters, storage, and statistical promotion gates, not the evolutionary optimizer itself.

### Why GEPA First

GEPA is closest to the exact missing component: reflective evolutionary search over text artifacts. Its README and local API smoke both support the fit:

- It optimizes textual parameters such as system prompts against arbitrary evaluation metrics.
- The README example optimizes a `system_prompt` with `trainset`, `valset`, `task_lm`, `reflection_lm`, and `max_metric_calls`.
- It uses actionable side information from traces and failures, which is important for ObviousBench because scalar scores alone are weak teacher feedback.
- It exposes adapter seams: implement `evaluate` and `make_reflective_dataset`.
- Local smoke confirmed `gepa.optimize(...)` exists and accepts custom adapter/evaluator, reflection model, validation set, metric-call budget, callbacks, run directory, caching, and seed.

The main GEPA risk is maturity/API churn. The PyPI package is young, so we should prove the adapter before depending on it.

### Why Not Promptfoo As The Core Optimizer

Promptfoo is excellent infrastructure, but it solves a different layer first. Its prompt optimization docs state that `promptfoo optimize` improves one configured prompt against one configured provider, then evaluates generated candidates against the tests in the config. The same docs explicitly say optimization targets one resolved prompt/provider pair and recommend tuning one pair at a time.

That makes Promptfoo attractive for:

- Exporting an eval matrix.
- Running CI checks.
- Reviewing prompt variants in a UI.
- Comparing models/providers against a fixed prompt.
- Possibly doing one-off prompt improvements.

It is weaker as the core ObviousBench prompt-evolution engine because:

- ObviousBench already has deterministic item scoring, cached Inspect runs, model settings, cost estimates, and paired statistics.
- Translating ObviousBench into Promptfoo assertions risks duplicating or drifting from the benchmark scorer.
- The desired workflow needs many hypotheses, many candidates per hypothesis, lineage, repeated holdouts, paired confidence intervals, and promote/continue/drop decisions.
- Promptfoo's optimizer command is intentionally narrow; the surrounding eval harness is stronger than the optimizer abstraction for this use case.

Promptfoo is therefore a good optional harness, not the first core optimizer.

### Why Not Custom First

Building the optimizer ourselves would let us match the product exactly, but it would immediately recreate solved hard parts:

- Candidate mutation and reflection loops.
- Exploration/exploitation and Pareto/frontier selection.
- Trace-to-feedback conversion.
- Candidate ancestry and merging.
- Metric-call budgets and stopping behavior.
- Avoiding overfit during prompt search.

Custom code is still necessary, but it should be the reusable shell around existing optimizers:

- `BenchmarkAdapter`.
- ObviousBench adapter.
- Prompt candidate and hypothesis storage.
- Cost/rate-limit planning.
- Statistical promotion gates.
- Teacher memory and run commentary.
- CLI/reporting.

### Kill/Confirm Gates

Treat GEPA as the default only if a tiny spike confirms:

- It can run baseline plus at least 3 candidate prompts through an ObviousBench slice.
- It can receive useful per-item side information, not just average score.
- It preserves enough candidate lineage for a run report.
- It can operate within our desired metric-call budget and concurrency model.
- Its best candidate can be independently validated on a holdout split using ObviousBench paired statistics.

If GEPA fails those, test Promptolution next. If both fail at the adapter or lineage layer, then build a minimal custom optimizer, but reuse the same adapter/storage/statistics shell.

## Candidate Matrix

| Candidate | Layer | Evidence checked 2026-06-02 | Strengths | Gaps | Decision |
| --- | --- | --- | --- | --- | --- |
| [GEPA](https://github.com/gepa-ai/gepa) | Reflective evolutionary optimizer | GitHub, PyPI, local import/API smoke | Direct system-prompt optimization, arbitrary metrics, reflection model, candidate lineage, metric-call budgets, adapters | Needs an ObviousBench adapter and promotion-stat layer | Primary backend |
| [Promptolution](https://github.com/automl/promptolution) | Prompt-optimization algorithm zoo | GitHub, PyPI, local import/API smoke, EACL paper | CAPO, EvoPromptDE, EvoPromptGA, OPRO; caching; parallel inference; token usage tracking; research-benchmark orientation | Much smaller ecosystem; top-level API is less obvious; needs adapter inspection | Secondary backend to test |
| [Promptfoo](https://www.promptfoo.dev/docs/usage/prompt-optimization/) | Eval/regression harness plus optimizer | Docs, NPM metadata, GitHub API; NPM `promptfoo==0.121.14`, modified 2026-06-02 | Mature CLI/config/CI eval harness; `promptfoo optimize`; validation split; assertions; UI | Optimizes one prompt/provider pair at a time; would duplicate ObviousBench scoring unless carefully wrapped | Optional harness/export |
| [MLflow prompt optimization](https://mlflow.org/docs/latest/genai/prompt-registry/optimize-prompts/) | Registry/eval/platform | Docs, PyPI, GitHub API | Prompt registry, lineage, `GepaPromptOptimizer`, `MetaPromptOptimizer`, custom scorers, multi-prompt optimization | Heavy platform dependency for the initial experiment | Later registry option |
| [DeepEval prompt optimization](https://deepeval.com/docs/prompt-optimization-introduction) | Eval framework plus optimizer replicas | Docs, PyPI, GitHub API | Simple `model_callback`; GEPA/MIPROv2 style algorithms; metrics ecosystem | Evaluation layer would compete with ObviousBench deterministic scorers | Optional app-eval layer |
| [DSPy](https://github.com/stanfordnlp/dspy/blob/main/docs/docs/api/optimizers/MIPROv2.md) | LLM programming framework | Docs, PyPI, GitHub API | Very active; GEPA/MIPROv2; custom metrics; strong for optimizing DSPy modules | Invasive for plain provider system prompts; optimized artifacts are DSPy programs | Use only when target is a DSPy program |
| [PromptWizard](https://github.com/microsoft/PromptWizard) | Discrete prompt optimizer | GitHub, PyPI, paper | Popular, MIT, self-refining prompt/examples, custom dataset path | Older PyPI release; single optimizer; more bespoke dataset conventions | Reference/possible backend |
| [SAMMO](https://github.com/microsoft/sammo) | Structured prompt program search | GitHub, PyPI | Prompt components, mutators, beam search, rate limiting, structured prompt editing | Better for prompt programs than raw system-prompt evolution | Reference/backend for structured prompts |
| [TextGrad](https://github.com/zou-group/textgrad) | Textual-gradient optimizer | GitHub, PyPI | Strong research pedigree; arbitrary text variables; prompt optimization examples | Requires wrapping prompts/losses into TextGrad abstractions; less direct for benchmark-scale prompt tournaments | Reference only |
| [DSPyground](https://github.com/karthikscale3/dspyground) | TypeScript GEPA harness/UI | GitHub | Agentic prompt optimization UI; powered by GEPA; AI SDK portability | Narrower stack; no release found; license metadata unclear via API | Watch, do not depend yet |
| [OpenAI Prompt Optimizer](https://developers.openai.com/api/docs/guides/prompt-optimizer/) | Dashboard optimizer | Official docs | Uses datasets, annotations, grader results, and output feedback | Dashboard-oriented, not a reusable code harness for hundreds of concurrent benchmark trials | Manual baseline/input source |

## Proposed Standalone Package

Working name: `promptlab` or `prompt-forge`.

Keep the reusable package generic and let ObviousBench provide an adapter:

```text
promptlab/
  core/
    candidate.py        # CandidatePrompt, Hypothesis, Trial, TrialResult
    benchmark.py        # BenchmarkAdapter protocol
    decisions.py        # promote/continue/drop decision model
  optimizers/
    gepa_backend.py
    promptolution_backend.py
    teacher_proposer.py
    random_search.py
  stats/
    paired_bootstrap.py
    wilson.py
    sequential_gates.py
  storage/
    sqlite_store.py
    jsonl_artifacts.py
  cli.py
```

ObviousBench integration should live in ObviousBench:

```text
obviousbench/promptlab_adapter.py
```

That adapter should expose:

- `load_items(split)`.
- `run_candidate(candidate_prompt, model, generation_config)`.
- `score_outputs(outputs)` using existing ObviousBench scorers.
- `compare_candidate(candidate, baseline)` using existing paired statistics.
- `estimate_cost(plan)` using existing registry/pricing/cost tools.

This keeps the evolutionary framework reusable while avoiding a generic package that imports the whole benchmark by default.

## Suggested First Proof

Build the smallest real proof around GEPA:

1. Create a standalone package skeleton in a new repo.
2. Add a local ObviousBench adapter that can run a tiny barrage slice through existing Inspect/runner/scorer code.
3. Seed with the current baseline system prompt and 2-3 deliberately different candidate prompts.
4. Run one cheap student model on a small train split and a held-out validation split.
5. Store every prompt, hypothesis, parent, score, item output, and decision in JSONL plus a SQLite index.
6. Emit a promotion report that requires a paired improvement threshold and confidence interval before replacing the baseline.

Success criteria:

- One command runs baseline plus candidates.
- GEPA receives useful per-item failure traces or side information, not only scalar scores.
- The final report can say `promote`, `continue`, or `drop` with a statistical reason.
- No ObviousBench scorer, item, cache, or pricing code is forked.

## Build-vs-Buy Decision

Decision: wrap, then build only the missing glue.

Use:

- GEPA for reflective/evolutionary prompt search.
- ObviousBench for scoring, item generation, cache, pricing, and benchmark reporting.
- Existing paired/Wilson statistics already in ObviousBench for promotion gates.

Explore:

- Promptolution as a second optimizer backend for CAPO/EvoPrompt/OPRO comparison.
- Promptfoo as an export/CI/UI format if its config and result artifacts are useful.
- MLflow only if prompt registry and lineage become more valuable than a lightweight local store.

Do not build yet:

- Custom evolutionary operators.
- A new eval framework.
- A new prompt registry.
- A bespoke observability platform.

## Open Risks

- GEPA side-information quality may matter more than raw score. The adapter should return concise failure diagnostics: expected answer, extracted answer, scorer family, output format failure, and any refusal/provider error.
- High parallelism needs rate-limit control at the benchmark runner layer, not only the optimizer layer.
- Optimizing against one fixed split can overfit. The first proof should use train/validation split and the later system should support repeated random seeds or successive holdouts.
- A generic package should not depend on private ObviousBench data or generated reports.
- Promptolution imports cleanly, but its exact custom-task adapter surface still needs a small code-level proof before being selected as a peer backend.

## Source Links

- GEPA: <https://github.com/gepa-ai/gepa>
- Promptolution: <https://github.com/automl/promptolution>
- Promptolution EACL demo paper: <https://aclanthology.org/2026.eacl-demo.21.pdf>
- Promptfoo prompt optimization: <https://www.promptfoo.dev/docs/usage/prompt-optimization/>
- MLflow prompt optimization: <https://mlflow.org/docs/latest/genai/prompt-registry/optimize-prompts/>
- DeepEval prompt optimization: <https://deepeval.com/docs/prompt-optimization-introduction>
- DSPy MIPROv2 docs: <https://github.com/stanfordnlp/dspy/blob/main/docs/docs/api/optimizers/MIPROv2.md>
- PromptWizard: <https://github.com/microsoft/PromptWizard>
- SAMMO: <https://github.com/microsoft/sammo>
- TextGrad: <https://github.com/zou-group/textgrad>
- OpenAI Prompt Optimizer: <https://developers.openai.com/api/docs/guides/prompt-optimizer/>
