# ObviousBench Methodology

ObviousBench v0.1 measures obvious failure rate on short, human-trivial tasks. Public examples are treated as leads and archetypes, then converted into deterministic benchmark items or generated variants.

Dataset lifecycle:

1. Source discovery records public examples and prior art.
2. Reproduction checks whether an archetype is still observable.
3. Generalization creates clean variants that avoid overfitting to famous prompts.
4. Review checks ambiguity, human-triviality, scorer reliability, and source safety.
5. Inclusion requires a stable ID, target, scorer, family, prompt template, source reference, and reviewed status.

Primary metric:

```text
obvious_failure_rate = failures / scored_questions
```

Secondary metrics include accuracy, failures per 1,000, per-family failure rate, format failure rate, non-answer rate, and provider error counts.

