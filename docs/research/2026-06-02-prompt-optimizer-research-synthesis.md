---
title: Prompt Optimizer Research Synthesis
date: 2026-06-02
type: research
status: draft
---

# Prompt Optimizer Research Synthesis

## Source

This note synthesizes the user-provided external research in `/Users/adamallcock/.codex/attachments/40179e59-b34e-4132-8dc4-4878852d8c21/pasted-text.txt` against the existing ObviousBench prompt-optimization research notes.

## Decision Update

The external research strengthens the prior recommendation:

- Wrap GEPA as the primary optimizer backend.
- Keep Promptolution as the first algorithm-zoo backup spike.
- Add Evidently's prompt optimizer as a simple-backend candidate worth investigating.
- Use Promptfoo as optional eval/export/CI/UI infrastructure, not as the core optimizer.
- Build a reusable custom shell around those backends: benchmark adapters, storage, lineage, teacher memory, cost/rate scheduling, statistics, and reports.

Confidence remains medium-high rather than final. The decision should still be gated by a small GEPA adapter spike.

## What Changed From The First Pass

The external research added several useful details:

1. GEPA is still the strongest fit, but should be pinned and isolated behind a backend interface because it is young and has some API rough edges.
2. GEPA's backend artifacts are richer than the first pass captured: `candidate_tree.html`, `candidates.json`, `gepa_state.bin`, run logs, and validation best-output artifacts.
3. A GEPA fake-adapter smoke reportedly observed candidate lineage, validation subscores, run artifacts, and a possible metric-call budget overshoot by a batch.
4. GEPA may require a small adapter workaround when using custom candidate proposers: an adapter may need `propose_new_texts = None`.
5. Promptolution remains interesting, but its declared package metadata is a compatibility concern: PyPI and package metadata for `promptolution==2.2.3` say `Requires-Python: >=3.10,<3.13`.
6. A local `uv` smoke can still install/import Promptolution under Python 3.14, but that is unsupported by its declared metadata and should not be treated as deployment-safe.
7. Evidently's prompt optimizer may be a useful low-complexity backup/simple baseline because it reportedly supports arbitrary scoring functions, train/validation/test discipline, mistake-driven improvement, and early stopping.
8. Promptfoo's best role is clearer: export locked prompts and frozen eval slices for CI/UI/regression, but do not let it become the source of truth for benchmark scoring or prompt evolution.
9. A simple custom metaprompt baseline should exist as a sanity check: teacher sees failure clusters, proposes `N` variants, ObviousBench evaluates and gates them.

## Current Build-Vs-Buy Call

| Layer | Decision | Reason |
| --- | --- | --- |
| Optimizer kernel | Wrap GEPA first | Best match for arbitrary text parameters, reflection model, adapter-based evaluation, traces, train/val, and candidate ancestry. |
| Backup optimizer | Spike Promptolution second | Algorithmically diverse, but more framework-shaped and declared Python support is `<3.13`. |
| Simple baseline | Build small custom baseline | Needed to prove GEPA's complexity is justified. |
| Eval/CI/UI harness | Optional Promptfoo export | Strong harness, but optimizer targets one resolved prompt/provider pair and would duplicate ObviousBench source-of-truth logic as core. |
| Registry/tracking | Defer MLflow | Useful later if prompt registry becomes strategic; too heavy as first architecture. |
| Benchmark/scoring/stats | Keep ObviousBench | Existing deterministic scoring, cache, pricing, and paired statistics should not be replaced. |
| Storage/lineage/memory | Build custom | No candidate gives the exact hypothesis, prompt, score, CI, cost, trace, and decision memory schema needed. |

## GEPA Spike Gates

GEPA should become the primary backend only if a small spike passes all of these gates:

- Adapter fit: an ObviousBench adapter can call existing benchmark/scoring/cache paths without reimplementing them.
- Trace fit: per-item failure diagnostics can be turned into useful GEPA reflection inputs.
- Artifact fit: GEPA candidates, parents, validation subscores, and run artifacts can be mapped into stable local records.
- Budget fit: metric-call and model-call counts stay within an externally planned budget, allowing for possible batch overshoot.
- Holdout fit: train/validation can be used by the optimizer while sealed holdout remains external and untouched.
- Outcome fit: on a tiny slice, GEPA either improves validation performance or produces informative negative evidence.

If adapter fit, trace fit, or budget fit fails, demote GEPA and spike Promptolution, Evidently, and the custom metaprompt baseline.

## Promptolution Compatibility Note

Verified on 2026-06-02:

- PyPI reports `promptolution==2.2.3` with `requires_python=<3.13,>=3.10`.
- Local metadata from `uv run --no-project --with promptolution` also reports `Requires-Python: >=3.10,<3.13`.
- The package can still import under the local Python 3.14 smoke, but this should be treated as unsupported behavior.

Decision impact: Promptolution remains a backup spike, not the primary backend, unless the standalone package targets Python 3.12 or Promptolution updates its declared compatibility.

## First Implementation Shape

The standalone package should use a backend interface:

```text
prompt_evolver/
  core/
    models.py
    ids.py
    splits.py
  adapters/
    base.py
    obviousbench.py
  optimizers/
    base.py
    gepa_backend.py
    promptolution_backend.py
    evidently_backend.py
    custom_baselines.py
  orchestration/
    scheduler.py
    budget.py
    retries.py
  gates/
    statistics.py
    promotion.py
  storage/
    artifact_store.py
    sqlite_store.py
    file_store.py
  memory/
    teacher_memory.py
    failure_patterns.py
  export/
    promptfoo.py
    mlflow.py
  reports/
    markdown.py
    html.py
  cli.py
```

ObviousBench should remain the source of truth through a `BenchmarkAdapter`:

```python
class BenchmarkAdapter(Protocol):
    def get_items(self, split: str, families: list[str] | None = None) -> list[BenchmarkItem]:
        ...

    async def evaluate(
        self,
        *,
        prompt: PromptArtifact,
        items: list[BenchmarkItem],
        model_settings: dict,
        capture_traces: bool,
    ) -> list[ItemResult]:
        ...

    def summarize(self, item_results: list[ItemResult]) -> ScoreSummary:
        ...
```

GEPA should sit behind `OptimizerBackend`, not leak through the product API.

## Recommended Next Step

Do not start with a paid optimization run. Start with no-cost proof artifacts:

1. Reproduce the GEPA import/API smoke in a repo-local script.
2. Write a fake GEPA adapter with deterministic scores and traces.
3. Confirm GEPA lineage, validation subscores, run artifacts, budget behavior, and adapter workaround requirements.
4. Build a stable artifact mapper from GEPA outputs to local `PromptArtifact`, `Candidate`, `ItemResult`, `ScoreSummary`, and `Decision`.
5. Only then connect a tiny cached/mock ObviousBench adapter.

This turns the GEPA recommendation from "promising" into an engineering decision.
