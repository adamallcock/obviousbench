---
title: ObviousBench Methodology
date: 2026-06-18
type: reference
status: current
---

# ObviousBench Methodology

ObviousBench measures obvious failure risk on short, human-trivial tasks. Public
examples are treated as leads and archetypes, then converted into deterministic
benchmark items, generated variants, or held-out split candidates.

Dataset lifecycle:

1. Source discovery records public examples and prior art.
2. Reproduction checks whether an archetype is still observable.
3. Generalization creates clean variants that avoid overfitting to famous prompts.
4. Review checks ambiguity, human-triviality, scorer reliability, and source safety.
5. Inclusion requires a stable ID, target, scorer, family, prompt template, source reference, and reviewed status.

Item-card lifecycle:

1. Generated or mined item receives a draft card.
2. Reviewer fills answer derivation, ambiguity notes, and scorer contract.
3. Trusted splits require reviewed cards.
4. Runtime JSONL stays compact; cards preserve provenance and review evidence.

Split policy:

- Public splits are small, inspectable example sets for docs, demos, and failure galleries. They are useful for transparency, but public exposure makes them unsuitable for headline leaderboard claims.
- Dev splits support local iteration and regression checks. Results on dev data should be treated as engineering feedback, not external benchmark evidence.
- Private splits are held-out evaluation data for stronger model comparisons. Claims from private data must state the split name, procedure, and data vintage.
- Live splits are dated refreshes from recent sources. Claims from live data must name the frozen refresh date or vintage, such as `live_v2026_06`.
- Canary splits are leakage and overfitting diagnostics only. Canary items should stay out of shareable bundles and should not be used as leaderboard evidence.

For v0.2, the headline evidence comes from a private held-out pass^3 snapshot.
Public examples are transparency and demo materials, not the private benchmark
itself. Public release surfaces may include aggregate private results and public
example questions, but must not include private held-out prompts, raw private
completions, item-level private outcomes, private review HTML, or raw attempt
logs.

The public website is the narrative and interactive chart surface. The public
repository is the code/data/reproducibility companion: public examples, scoring
code, model metadata, aggregate CSVs, release metadata, license, and citation
files.

Primary metric:

```text
answer_pass3 = item/model/config cells where all 3 attempts are answer-correct
```

For v0.2 public interpretation, use non-strict answer pass^3 as the headline
metric. Strict correctness and format correctness remain diagnostics.

Secondary metrics include strict pass^3, any^3, answer accuracy, format
accuracy, failures per 1,000, per-family failure rate, non-answer rate, token
usage, estimated cost, and provider error counts.

Provider-route failures, unavailable models, and blank-final-output routes
should be tracked as operational caveats rather than silently converted into
model-quality failures.
