---
title: ObviousBench Methodology
date: 2026-05-31
type: reference
status: current
---

# ObviousBench Methodology

ObviousBench v0.1 measures obvious failure rate on short, human-trivial tasks. Public examples are treated as leads and archetypes, then converted into deterministic benchmark items or generated variants.

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

This split model is parked as documentation-only guidance for now. Current code behavior still centers on `public_v0`; future implementation should add validation and file-layout support before any split is treated as enforced.

Primary metric:

```text
obvious_failure_rate = failures / scored_questions
```

Secondary metrics include accuracy, failures per 1,000, per-family failure rate, format failure rate, non-answer rate, and provider error counts.
