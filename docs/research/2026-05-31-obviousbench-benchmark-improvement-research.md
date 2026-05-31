---
title: ObviousBench Benchmark Improvement Research
date: 2026-05-31
type: research
status: draft
---

# ObviousBench Benchmark Improvement Research

## Executive Read

ObviousBench is already pointed in a useful direction: short prompts, objective
ground truth, deterministic scoring, answer-vs-format separation, cost
tracking, and a hard-obvious panel that is not saturated. Compared with recent
"simple but revealing" benchmark work, the biggest gap is not runner plumbing.
It is benchmark science: provenance, label verification, split hygiene,
statistical confidence, item discrimination, and systematically generated
families that isolate specific failure mechanisms.

The strongest next move is to turn ObviousBench from "good local proof point"
into a benchmark with an explicit item lifecycle:

1. mined or generated item enters with a source card,
2. answer and ambiguity are reviewed,
3. scorer behavior is locked in a gold regression suite,
4. item is assigned to public/dev/private/live/canary split,
5. results are reported with answer, format, strict, cost, tokens, confidence
   intervals, and per-item discrimination.

That would make the benchmark much harder to dismiss while preserving its
basic charm: "this should have been easy."

## Papers And Benchmarks Reviewed

| Work | Relevant Design Choice | ObviousBench Takeaway |
| --- | --- | --- |
| SimpleBench | Over 200 everyday multiple-choice prompts where high-school-level humans beat frontier models; focuses on spatial, temporal, social, and trick-question robustness. Source: <https://simple-bench.com/> | Add human baseline, everyday-reasoning framing, and a smaller public "try it yourself" set, but avoid only becoming a trick-question collection. |
| SimpleQA | Short factual questions with one indisputable answer, graded correct/incorrect/not attempted; adversarially collected against GPT-4. Source: <https://arxiv.org/abs/2411.04368> | Add abstention/not-attempted handling where applicable and make "single indisputable answer" a hard acceptance criterion. |
| SimpleQA Verified | Reworks SimpleQA with de-duplication, topic balancing, source reconciliation, and improved autorater prompts. Source: <https://arxiv.org/abs/2509.07968> | Build source reconciliation, topic balance, and de-dup tooling before growing the corpus too aggressively. |
| LiveBench | Frequently updated questions, objective automatic scoring, recent sources, contamination-limited design, and monthly updates. Source: <https://arxiv.org/abs/2406.19314> | Add public/dev/private/live splits and dated refreshes. Keep scoring objective and avoid LLM judges as primary truth. |
| IFEval | Verifiable instruction constraints instead of subjective human or LLM judging. Source: <https://arxiv.org/abs/2311.07911> | Expand the format/constraint families around programmatic verifiers. |
| IFEval-FC | Tests format instructions embedded inside function schemas; fully algorithmic. Source: <https://arxiv.org/abs/2509.18420> | Add schema-style constraints and scorer contracts for exact formats, not just natural language prompts. |
| LexInstructEval | Uses a formal grammar for fine-grained lexical instruction following and transparent programmatic verification. Source: <https://arxiv.org/abs/2511.17561> | Add a small DSL for lexical/string constraints so generated items are auditable and verifiable. |
| SATA-BENCH | Select-all-that-apply tasks expose count bias and selection bias; strongest model only reaches 41.8% exact match in the paper abstract. Source: <https://arxiv.org/abs/2506.00643> | Add multi-answer obvious questions with exact and partial scoring: days containing a letter, all objects satisfying a condition, "which of these are true?" |
| LLMThinkBench / Overthinking | Dynamic simple math tasks, accuracy-token efficiency, reasoning budgets, and overthinking score. Source: <https://arxiv.org/abs/2507.04023> | Make token efficiency first-class for "obvious" tasks. A model should not spend 2k reasoning tokens to answer "drive." |
| InductionBench | Simple formal rule induction remains hard even for advanced models. Source: <https://arxiv.org/abs/2502.15823> | Add tiny pattern-induction items where the rule is visually obvious to humans and exactly checkable. |
| StructFlowBench | Multi-turn structural dependencies are distinct from single-turn constraint satisfaction. Source: <https://arxiv.org/abs/2502.14494> | Later, add a small multi-turn "obvious correction / persistence / pivot" suite. |
| tinyBenchmarks | Carefully selected tiny subsets can reproduce larger benchmark rankings cheaply. Source: <https://huggingface.co/papers/2402.14992> | Use item response/discrimination statistics to create reliable 40/80/160 item panels rather than just larger panels. |

## What ObviousBench Should Improve

### 1. Add Source Cards And Item Cards

Every item should have a durable card, separate from the prompt JSONL, that
answers:

- Where did the archetype come from?
- Is the item mined, generated variant, synthetic control, or live canary?
- What is the exact expected answer and derivation?
- What ambiguity did reviewers consider?
- Which scorer is authoritative?
- Which alternative outputs are acceptable?
- Which outputs are answer-correct but format-wrong?
- Which split is it allowed to appear in?
- Is the source public, private, generated, or screenshot-derived?

Acceptance criteria:

- No item enters `public_v1` without a source card.
- Each source card has at least one source ref or a generated-control rationale.
- Each card includes `ambiguity_notes`, `answer_derivation`, `review_status`,
  `scorer_contract`, and `split_policy`.
- Validation rejects items with missing cards, missing derivations, or unresolved
  ambiguity notes.

This is the SimpleQA Verified lesson: label quality and de-duplication matter
more than raw item count.

### 2. Create A Scorer Gold Suite

The scorer is now important enough to be treated like product code. We should
maintain a gold corpus of raw model outputs and expected score decisions:

- correct exact answer,
- correct answer with verbose noncompliance,
- correct answer inside JSON/fenced code,
- wrong answer with matching format,
- multi-answer partial match,
- invalid array/list wrapper,
- refusal/non-answer,
- unit variants,
- punctuation/case variants,
- "answer appears in reasoning but final answer is wrong" cases.

Acceptance criteria:

- Each scorer has at least 20 gold examples.
- Gold examples cover answer-correct/format-wrong and answer-wrong/format-right.
- `obviousbench rescore` is tested against stale logs from older scorer
  behavior.
- Failure galleries show raw output, extracted answer, answer correctness,
  format correctness, strict correctness, and failure type.

This protects us from the exact problem we just saw: the benchmark can be right
while the scorer makes the published number misleading.

### 3. Add Human Baseline And Human Triviality Evidence

We currently label human triviality (`H0`, etc.) but do not prove it. SimpleBench
is persuasive partly because it explicitly frames non-specialist human
performance.

Recommended lightweight protocol:

- 5 to 10 human participants,
- 100 item calibration panel,
- no external tools,
- response time captured,
- answer only, no explanation,
- report human accuracy and median time by family.

Acceptance criteria:

- `human_baseline_v0.csv` contains per-item human accuracy and median seconds.
- `human_triviality` is computed from evidence, not only assigned by intuition.
- H0 means at least 95% human accuracy and median answer time under 10 seconds.
- Items below threshold are either revised, moved to H1/H2, or removed from the
  "obvious" core.

This would materially strengthen the claim that failures are embarrassing rather
than merely adversarial.

### 4. Add Public, Dev, Private, Live, And Canary Splits

ObviousBench should not have one monolithic public set if it is intended to
remain useful.

Recommended split model:

- `public_v1`: small inspectable set for credibility and examples.
- `dev_v1`: local iteration set; may overlap archetypes but not exact items.
- `private_v1`: evaluation set not committed publicly.
- `live_vYYYY_MM`: dated refresh mined from recent public examples.
- `canary_v1`: synthetic controls used to detect contamination or overfitting.

Acceptance criteria:

- Validation rejects ID/source overlap across protected splits.
- Reports state the split and data vintage.
- Public leaderboard claims use private or live split results, not only public
  examples.
- Each live release freezes the exact item set and source cards.

This is the LiveBench lesson: freshness and contamination control are part of
the benchmark, not a footnote.

### 5. Add Statistical Reporting

The current reports are useful but too point-estimate-heavy. We should add:

- Wilson confidence intervals for accuracy,
- bootstrap intervals by model and family,
- paired model deltas on the same sample IDs,
- per-item difficulty and discrimination,
- reliability of 40/80/160 sample panels against larger runs.

Acceptance criteria:

- `comparison.csv` includes confidence interval columns.
- `delta.csv` includes paired deltas and uncertainty.
- Report explicitly flags when two models are not meaningfully separated.
- A `panel_reliability.csv` shows how well each short barrage predicts the
  larger evaluation pool.

This is where tinyBenchmarks is useful: small can be rigorous if item selection
is evidence-driven.

### 6. Add Item Response And Panel Builder Logic

The current `hard_obvious_8x10` is a good start. It should become data-driven.

Recommended item metrics:

- difficulty: model failure rate,
- discrimination: ability to separate top/mid/weak models,
- format fragility: strict minus answer gap,
- cost sensitivity: tokens spent by reasoning models,
- instability: variance across prompt paraphrases or repeated runs.

Acceptance criteria:

- Each summarized run updates an item statistics table.
- `make-barrage --profile hard_obvious_8x10` can select by empirical
  discrimination, not only hardcoded subfamily preference.
- The panel builder supports constraints: family balance, source balance,
  no near-duplicate prompts, and max variants per archetype.

This turns our current intuition into a reproducible selection policy.

### 7. Add Overthinking And Efficiency Metrics

For obvious questions, excessive reasoning is itself a failure mode. The hard
panel already shows reasoning-token gaps. We should formalize it.

Metrics:

- answer accuracy,
- strict accuracy,
- median output tokens,
- median reasoning tokens,
- cost per correct,
- tokens per correct,
- overthinking score: harmonic-style combination of accuracy and token
  efficiency,
- budget sensitivity: none/minimal/low/medium/high curves.

Acceptance criteria:

- Reports include an "accuracy vs token efficiency" chart.
- Reasoning models are evaluated across effort settings for a fixed panel.
- The report flags "no accuracy gain, higher token spend" cases.
- Per-family token waste is visible.

This imports the LLMThinkBench lesson directly into ObviousBench.

### 8. Add Multi-Answer "Select All" Obvious Questions

The "how many days have d" example is a perfect warning: models often miss that
every weekday contains `day`. We should add a multi-answer family rather than
only scalar answers.

Candidate subfamilies:

- select all weekdays/months/items containing a character,
- select all options satisfying a simple condition,
- select all statements that are true,
- count plus list consistency,
- "none/all of the above" traps.

Scoring:

- exact set match,
- partial precision/recall/F1,
- count accuracy,
- selection bias diagnostics by option position.

Acceptance criteria:

- Add `select_all_v0` scorer.
- Add exact and partial metrics, with strict exact match as the main score.
- Report count-bias and option-position bias.
- Include examples where the correct answer is all options, no options, and a
  non-contiguous subset.

This is the SATA-BENCH lesson, but in an ObviousBench-native style.

### 9. Separate String Manipulation Into A First-Class Category

String manipulation is currently spread across spelling/character tasks. It
deserves its own explicit category because it catches several distinct failure
modes.

Subfamilies:

- remove character from target token only,
- replace character in target token only,
- replace character in whole quoted string,
- reverse word,
- reverse list order,
- preserve capitalization,
- count overlapping substrings,
- apply operation once vs every occurrence,
- operate on answer choices vs prompt text.

Acceptance criteria:

- Add a `string_manipulation` family or rename/split the existing spelling
  family with migration notes.
- Each item specifies operation scope: `target_token`, `quoted_span`,
  `entire_string`, or `choice_text`.
- Scorers preserve exact-string checking but allow documented whitespace/case
  normalization only when intended.
- Include regression items for "model replaced text in the whole prompt" style
  failures.

This directly addresses the observed failure where the model interpreted a
replacement instruction as operating over too much context.

### 10. Improve Object Presence As Its Own Category

The car-wash family should not be buried in generic constraint awareness. It is
a recognizable "object must be present at destination" primitive.

Recommended category name:

- `object_presence`
- or `task_object_transport`

Good item shape:

- "The car wash is 100m away. Should I walk or drive?" -> drive.
- "The dry cleaner is next door. Do I need the coat?" -> yes / bring the coat.
- "The key cutter is across the street. Do I need the key?" -> yes.
- "The recycling bin is outside. Do I need the bottles?" -> yes.

Avoid weak items:

- cases where "bring myself only" sounds unnatural,
- cases where walking while carrying the item is equally valid,
- cases where the object is optional or the service can be done remotely.

Acceptance criteria:

- Add a standalone category only after the user-led #4 iteration produces at
  least 30 high-quality items.
- Each item includes a rationale for why the object is necessary.
- Each item has an ambiguity note explaining why the alternate answer is not
  reasonable.
- Include controls where walking is correct because the object is portable.

This category is currently one of the best separators in the hard panel.

### 11. Add Paired And Metamorphic Variants

Many obvious failures are not about one prompt. They are about inconsistency
under trivial transformations.

Variant types:

- paraphrase same question,
- swap order of answer choices,
- change irrelevant distances/names,
- invert a negation,
- ask for count vs list,
- ask "which" vs "how many",
- same answer with strict JSON vs free text.

Acceptance criteria:

- Items can declare `metamorphic_group_id`.
- Reports include group consistency.
- A model can be penalized for answering equivalent items inconsistently.
- Panel builder avoids overloading public samples with too many siblings from
  one group unless the profile asks for robustness stress.

This would make ObviousBench less anecdotal and more diagnostic.

### 12. Add Small Induction Tasks

InductionBench suggests a nice expansion: simple pattern inference that is easy
for humans but exact to score.

Examples:

- `A -> B, B -> C, C -> D; what is F -> ?`
- sequence with a simple string rewrite rule,
- classify examples under a visible rule,
- infer "remove first letter" from 3 examples and apply once.

Acceptance criteria:

- Rules are finite-state/simple string functions, not open-ended puzzles.
- Each item has training examples and one test example.
- Scorer checks exact output.
- Difficulty tags record rule type and number of examples.

This adds a new failure primitive without drifting into expert math.

### 13. Add Multi-Turn Only After Single-Turn Is Strong

StructFlowBench is relevant, but multi-turn should be a second-track suite, not
a distraction from the core benchmark.

Useful ObviousBench-native multi-turn flows:

- correction: user corrects a false assumption, model must update answer,
- persistence: user adds irrelevant detail, answer should stay the same,
- refinement: user narrows a previous instruction,
- pivot: new question supersedes previous context,
- contradiction: user gives impossible constraints; model should ask/flag.

Acceptance criteria:

- Multi-turn examples have deterministic final-state answers.
- Flow relationships are labeled.
- Scoring checks the final response and optionally intermediate compliance.
- Multi-turn results are reported separately from single-turn ObviousBench.

This should wait until the item-card and scorer infrastructure is solid.

## Suggested Implementation Order

### Phase 1: Credibility Foundation

1. Add source-card/item-card schema and validation.
2. Add scorer gold suite with answer/format/strict expected outcomes.
3. Add human baseline protocol and first 100-item calibration.
4. Add confidence intervals and paired deltas to comparison reports.

### Phase 2: New High-Signal Families

1. Add `select_all` family and scorer.
2. Split or formalize `string_manipulation`.
3. Promote object presence after the user-led generation pass.
4. Add paired/metamorphic group reporting.

### Phase 3: Benchmark Longevity

1. Add public/dev/private/live/canary split policy.
2. Add monthly or ad hoc live refresh pipeline.
3. Add item discrimination and data-driven barrage builder.
4. Add token-efficiency and overthinking score charts.

### Phase 4: Optional Expansion

1. Add small induction tasks.
2. Add multi-turn structural obviousness.
3. Add multilingual variants only after English quality is stable.
4. Consider visual/screenshot tasks only if the benchmark explicitly expands to
   multimodal systems.

## Concrete Next Backlog

Recommended immediate issues:

1. `item-cards-v1`: create `data/item_cards/*.yaml`, validator, and migration
   for existing public items.
2. `scorer-gold-v1`: create gold raw-output fixtures for every scorer and make
   `rescore` tests consume them.
3. `select-all-v0`: add answer type, scorer, metrics, and 30 seed items.
4. `string-scope-v0`: add operation-scope metadata and examples for
   token-only vs quoted-span vs whole-string operations.
5. `report-ci-v0`: add Wilson intervals and paired deltas.
6. `overthinking-v0`: add token-efficiency metrics and effort-curve reports.
7. `panel-irt-v0`: compute item difficulty/discrimination from existing sweep
   results and use it in `hard_obvious_XxY`.

My recommendation: do `item-cards-v1` and `scorer-gold-v1` first. Those are not
the flashiest changes, but they make every later dataset expansion easier to
trust.
