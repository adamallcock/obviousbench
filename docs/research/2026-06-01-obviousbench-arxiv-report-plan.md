---
title: ObviousBench arXiv Report Plan
date: 2026-06-01
type: research
status: draft
---

# ObviousBench arXiv Report Plan

## Executive Read

This document treats "aarvix" as arXiv.

ObviousBench can plausibly become an arXiv-style benchmark report, but the
current public positioning should be tightened before submission. The repo
already has a credible proof point: a narrow benchmark, deterministic scorers,
answer correctness as the primary score, strict/format compliance diagnostics,
confidence intervals, cost and token reporting, hard-obvious panels, and
shareable artifacts. The largest gap is not
paper formatting. It is that the current `public_v0` dataset is explicitly
generated seed data suitable for a proof point, not yet a strong public
leaderboard claim.

The correct arXiv paper posture is:

> ObviousBench is a focused reliability benchmark for short, human-trivial
> language-model tasks where failures are visibly disproportionate to task
> difficulty.

Editorial direction after the SimpleBench-style review: keep the main report
plain and short. Lead with the benchmark idea and visible results, describe the
run protocol in compact language, and move detailed evidence machinery into
generated tables, appendices, and repo docs. The paper should feel closer to a
clear benchmark technical note than to a broad survey or speculative model
mechanism essay.

The paper should be a benchmark paper, not a product launch, not a model
solution paper, and not a gotcha essay. It should spend most of its space on
benchmark definition, item curation, scorer validity, contamination controls,
model results, uncertainty, and failure analysis. Hypotheses about why models
fail should be clearly labeled as analysis. Remediation ideas should be short
and secondary.

Recommended submission gate:

- Do not submit a paper that only reports the current `public_v0` proof-point
  data.
- Submit after there is a paper-frozen split with reviewed item cards,
  documented answer derivations, ambiguity notes, scorer gold fixtures, exact
  model configs, and a reproducible model sweep.
- For the first preprint, do not collect a measured human baseline. Remove
  empirical human-performance language and treat human-triviality as a design
  target until a strict benchmark version freezes the item set.
- Use arXiv first as a preprint archive for a serious technical report; if the
  goal is conference submission later, format and anonymity constraints should
  be handled separately.

## Foundation Progress

Current local foundation state as of 2026-06-01:

- `data/splits/paper_v1_manifest.jsonl` contains the 80-item paper candidate
  split, balanced across 8 families.
- All 80 paper candidate item cards are reviewed and placeholder-free.
- The manifest-scoped readiness gate passes dataset validation, item-card
  review, scorer-gold coverage, and paper-manifest checks.
- `docs/research/2026-06-01-paper-v1-human-baseline-form.md` and
  `data/human_baseline/paper_v1.csv` exist for future human-baseline
  collection, but measured collection is deferred for the fast preprint.
- `docs/research/2026-06-01-paper-v1-human-baseline-collection-packet.md`,
  participant packets, randomized assignments, a response template, and a
  local answer key now exist for a possible later 5-participant, 400-row
  baseline collection.
- `docs/research/2026-06-01-paper-v1-human-baseline-collection-audit.md`
  now tracks collection completeness before scoring. It currently reports
  400/400 response rows present and 0/400 answer+timing rows complete, with no
  duplicate or unknown response-row issues.
- `docs/research/2026-06-01-paper-v1-human-baseline-collection-handoff.md`
  now gives the operator-facing runbook for collecting the 400 real
  answer/timing rows while preserving participant-facing packet boundaries,
  answer-key privacy, data-entry contracts, and stop rules before scoring.
- `docs/research/2026-06-01-paper-v1-human-baseline-scoring-report.md` and
  `data/human_baseline/paper_v1_scored_draft.csv` now provide the scoring
  handoff for filled participant responses. They are intentionally blocked
  while the response template is empty.
- `data/human_baseline/paper_v1_threshold_items.csv`,
  `data/human_baseline/paper_v1_threshold_families.csv`, and
  `docs/research/2026-06-01-paper-v1-human-baseline-threshold-audit.md`
  now provide the post-scoring threshold audit. The current audit is blocked
  with 80 `no_data` items because no real participant responses exist.
- `docs/research/2026-06-01-paper-v1-human-baseline-operations.md`
  now coordinates collection, audit, scoring, thresholding, promotion, and
  strict-readiness into one operational gate. It is future-validation
  infrastructure, not a v1 preprint blocker.
- `configs/paper_v1_related_work.yaml`,
  `docs/research/2026-06-01-obviousbench-related-work-positioning.md`, and
  `paper/tables/related_work_positioning.tex` now define and render a
  citation-checked comparator matrix for the related-work section. The current
  matrix reports 11 passed comparators and 0 blocked coverage checks.
- `configs/paper_v1_model_panel.yaml` freezes a 12-model planned panel without
  launching expensive provider calls.
- `docs/research/2026-06-01-paper-v1-final-result-artifact-audit.md` defines
  and checks the final sweep output contract: per-model summaries, comparison
  CSVs, generated report files, and the promotion rule for replacing result
  placeholders.
- `docs/research/2026-06-01-paper-v1-model-panel-cost-estimates.md` contains
  dry-run cost estimates for that panel.
- `paper/tables/human_baseline_summary.tex` and `paper/tables/model_panel.tex`
  are generated paper assets.
- `paper/tables/main_results.tex`, `paper/tables/family_results.tex`,
  `paper/tables/thinking_group_results.tex`,
  `paper/tables/model_family_results.tex`,
  `paper/tables/failure_type_summary.tex`, and
  `paper/tables/provider_exclusions.tex` now render the
  `docs/shareable/2026-05-31-obviousbench-proof-point` result bundle as a
  clearly labeled draft-only placeholder until the final sweep exists.
  The main result tables rank by answer correctness, expose Wilson 95%
  confidence intervals and answer-level obvious failure rate, and keep strict
  accuracy as a secondary compliance diagnostic. Grouping tables separate
  thinking-mode and model-family views for hypothesis generation.
- `paper/figures/leaderboard.pdf`, `paper/figures/family_heatmap.pdf`,
  `paper/figures/answer_format_gap.pdf`, and `paper/figures/cost_frontier.pdf`
  now render draft placeholder plots from that proof-point bundle so the source
  bundle shape and results-section visual design can be reviewed before
  provider calls. The family heatmap is generated at a page-shaped size with
  larger row labels and cell text for manuscript review readability.
- The LaTeX manuscript has been simplified toward the SimpleBench-style spine:
  plain title and abstract, direct positioning, short benchmark/scoring
  sections, result figures near the front of the empirical section, and a
  compact limitations/reproducibility close. The detailed related-work matrix
  plus scorer/model-panel machinery are now appendix material rather than early
  main-body narrative.
- `docs/research/2026-06-01-obviousbench-draft-result-placeholders.md`
  records the source, allowed uses, disallowed claims, and replacement rule for
  those reused proof-point results.
- `docs/research/2026-06-01-paper-claim-blocker-audit.md` tracks unresolved
  claim blockers.
- `docs/research/2026-06-01-obviousbench-arxiv-completion-roadmap.md`
  converts the current readiness, threshold, sweep, internal-review,
  section-tracker, checklist, and metadata evidence into an ordered path to
  final arXiv submission.
- `docs/research/2026-06-01-obviousbench-arxiv-blocker-dashboard.md`
  consolidates the current audit blockers into one dependency-grouped action
  dashboard. It currently reports 0 passing gates, 10 blocked gates, and 1
  waiting gate.
- `docs/research/2026-06-01-obviousbench-manuscript-completeness-audit.md`
  verifies that the LaTeX source has every expected arXiv report component,
  required citations, generated tables, and generated figures. It currently
  reports 3 passing components, 8 blocked components, and 0 missing components.
- `docs/research/2026-06-01-obviousbench-public-release-artifact-audit.md`
  defines the release-side gate for public documentation, frozen paper data,
  license/citation/archive metadata, public code/data URLs, and final metadata
  confirmation.
- `docs/research/2026-06-01-obviousbench-public-release-decision-packet.md`
  turns those release blockers into explicit decisions and draft templates for
  `LICENSE`, `CITATION.cff`, `.zenodo.json`, `pyproject.toml`, and final
  public URLs without choosing a license or creating release files.
- `docs/research/2026-06-01-obviousbench-arxiv-source-bundle-audit.md` checks
  the draft source tarball for obvious packaging mistakes.
- `docs/research/2026-06-01-obviousbench-arxiv-submission-handoff.md`
  provides the upload-facing handoff. It currently says upload readiness is
  `NO` and should stay blocked until the source bundle, PDF audit, preflight,
  release audit, metadata audit, and blocker dashboard all pass.
- `docs/research/2026-06-01-obviousbench-paper-pdf-build-audit.md` records the
  current PDF build state. It is blocked until a LaTeX toolchain exists, static
  source markers are resolved, `paper/main.pdf` is built, and `paper/main.log`
  is clean enough for inspection.
- `docs/research/2026-06-01-obviousbench-pdf-build-handoff.md` records the
  off-the-shelf PDF toolchain options, local command availability, build
  ladder, inspection checklist, and stop rules for getting from the current
  LaTeX source to an inspected final PDF.
- The current preprint posture uses `make -C paper readiness-preprint`.
  `make -C paper readiness` remains the stricter gate for a later paper that
  reports empirical human-baseline evidence.

Do not run final model arrays until `make -C paper readiness-preprint` passes,
the model panel is explicitly approved, and expected cost is accepted.

## Primary Sources Used

arXiv process and format:

- arXiv submission overview: <https://info.arxiv.org/help/submit/index.html>
- arXiv endorsement: <https://info.arxiv.org/help/endorsement.html>
- arXiv moderation: <https://info.arxiv.org/help/moderation/index.html>
- arXiv availability and announcement schedule:
  <https://info.arxiv.org/help/availability.html>
- arXiv file preparation:
  <https://info.arxiv.org/help/submit_tex.html>
- arXiv accepted formats:
  <https://info.arxiv.org/help/submit_formats.html>
- arXiv AI policy for authorship and disclosure:
  <https://info.arxiv.org/help/submit/index.html#artificial-intelligence-ai-policy>

Benchmark-paper comparators:

- SimpleQA: <https://arxiv.org/abs/2411.04368>
- IFEval: <https://arxiv.org/abs/2311.07911>
- FollowBench: <https://arxiv.org/abs/2310.20410>
- LiveBench: <https://arxiv.org/abs/2406.19314>
- LiveCodeBench: <https://arxiv.org/abs/2403.07974>
- GSM-Symbolic: <https://arxiv.org/abs/2410.05229>
- MMLU-Pro: <https://arxiv.org/abs/2406.01574>
- GPQA: <https://arxiv.org/abs/2311.12022>
- Humanity's Last Exam: <https://arxiv.org/abs/2501.14249>
- When Benchmarks Age:
  <https://arxiv.org/abs/2510.07238>
- SimpleBench, non-arXiv but close in positioning:
  <https://simple-bench.com/>

Local ObviousBench sources:

- [README.md](../../README.md)
- [docs/benchmark_card.md](../benchmark_card.md)
- [docs/methodology.md](../methodology.md)
- [docs/scoring_policy.md](../scoring_policy.md)
- [docs/source_policy.md](../source_policy.md)
- [docs/status/2026-05-31-rescore-and-hard-obvious.md](../status/2026-05-31-rescore-and-hard-obvious.md)
- [docs/reports/2026-05-31-mega-model-sweep-rescored-v2/leaderboard.md](../reports/2026-05-31-mega-model-sweep-rescored-v2/leaderboard.md)

## How arXiv Works

arXiv is an open scholarly preprint archive. It is not a peer-reviewed
conference or journal, and appearance on arXiv is not the same thing as
acceptance by an academic venue. The practical acceptance standard is:

1. the paper fits an arXiv subject area,
2. the submitter has the right account/endorsement status,
3. the source files and metadata pass technical checks,
4. moderators judge that the submission is appropriate scholarly content for
   the selected category.

Moderation is not a full review. Moderators do not normally provide detailed
review feedback, and they are evaluating topical fit, scholarly character,
minimum quality, and policy compliance rather than deciding whether the result
is important or correct. arXiv can reclassify, hold, reject, or request changes.

### Account And Endorsement

Authors submit from a registered arXiv account. New submitters, or submitters
entering a new subject area, may need endorsement from an established arXiv
author in that category. For ObviousBench, the likely primary category is
`cs.CL` if the paper emphasizes language-model evaluation, with possible
cross-listing to `cs.AI` or `cs.LG` if the final framing warrants it.

If the user has not previously submitted to `cs.CL`, plan for endorsement early
instead of treating it as a final-week administrative step.

### Announcement Timing

arXiv has daily submission deadlines and announcement windows. As of the
current arXiv availability page, submissions received before the weekday cutoff
are generally announced after moderation and processing on the next announcement
cycle, while weekends and holidays delay announcement. The operational takeaway:
do not promise a same-day public paper link. Submit after all PDFs, metadata,
source, abstract, authorship, code/data links, and license decisions are final.

### File Formats

The normal technical expectation is a PDF generated from TeX/LaTeX source.
arXiv accepts several formats, but if the paper was produced from TeX, the TeX
source should be submitted rather than only the generated PDF. Figure files,
bibliography files, style files that are not standard, and any necessary source
assets should be bundled cleanly.

For this project, the correct structure is likely:

```text
paper/
  main.tex
  references.bib
  figures/
    taxonomy.pdf
    data-lifecycle.pdf
    leaderboard.pdf
    family-heatmap.pdf
    answer-format-gap.pdf
    cost-frontier.pdf
  tables/
    dataset-composition.tex
    model-panel.tex
    main-results.tex
    ablations.tex
```

Keep heavy raw results, raw provider logs, and private/canary data out of the
arXiv source bundle. Link to a GitHub release, Zenodo archive, Hugging Face
dataset, or project page for larger artifacts.

### AI Authorship And Disclosure

arXiv's AI policy does not allow generative AI systems to be listed as authors.
If AI tools materially assisted the writing, code, data generation, or analysis,
disclose that in an acknowledgments or author-contributions style note, using
plain language.

### What arXiv Moderation Will Care About For ObviousBench

The paper should look like a research article:

- a clear technical contribution,
- a defined benchmark,
- reproducible methods,
- data curation and review criteria,
- model results with uncertainty,
- limitations and ethical considerations,
- references to related benchmarks.

The paper should not look like:

- a README pasted into PDF form,
- a product announcement,
- a benchmark leaderboard with weak data provenance,
- an opinion essay about "LLMs are bad",
- a proposal for a future benchmark without enough current evidence.

## Benchmark-Paper Corpus

I downloaded and inspected the current arXiv PDFs for the following papers on
2026-06-01. The page counts below are local PDF counts, useful only as practical
format evidence.

| Work | Pages | Main-body Shape | Why It Matters For ObviousBench |
| --- | ---: | --- | --- |
| SimpleQA | 13 | Intro, data collection, grading/metrics, model evaluation, calibration, related work, appendix | Very close shape for short-answer tasks: single-answer criteria, data quality, grading policy, and calibration are central. |
| IFEval | 43 | Short main paper, large prompt/result appendix | Best nearby example for deterministic/verifiable instruction-following constraints. Shows that a small main paper can carry a large artifact appendix. |
| FollowBench | 22 | Related work, benchmark construction, protocol, experiments, analysis | Good template for constraint taxonomy and level/category analysis. |
| LiveBench | 37 | Benchmark description by category, update plan, experiments, correlation analyses, limitations, reproducibility, ethics | Strong template for contamination-limited, objective-scored, frequently refreshed benchmark reports. |
| LiveCodeBench | 46 | Holistic evaluation, curation, platform-specific construction, setup, results, contamination analysis | Useful for data-source curation and contamination framing, even though coding is outside ObviousBench scope. |
| GSM-Symbolic | 24 | Template generation, experimental setup, results, analysis, conclusion | Very relevant for metamorphic/symbolic variants that test whether models rely on shallow pattern matching. |
| MMLU-Pro | 24 | Benchmark pipeline, setup, results, error analysis, comparison with prior benchmark, limitations | Useful for a "we improve on a saturated benchmark style" narrative. |
| GPQA | 28 | Data collection, dataset splits, dataset analysis, baselines, limitations | Strong template for question objectivity, expert/human validation, and split reporting. |
| Humanity's Last Exam | 28 | Dataset collection/review, evaluation setup, quantitative results, discussion | Useful as a modern high-visibility benchmark release style, even though its difficulty regime is the opposite of ObviousBench. |

Practical length norm from this corpus:

- Main paper before references: often 6 to 14 pages.
- Total arXiv PDF with references and appendix: commonly 13 to 46 pages.
- Benchmark papers often push examples, prompts, per-category tables, extended
  model results, and review instructions into appendices.
- arXiv itself does not impose a standard ML conference page limit; the apparent
  standard comes from conference styles and reader expectations, not arXiv.

## Comparator Analysis

### SimpleQA

SimpleQA is a benchmark for short factual questions with unambiguous answers.
Its relevant choices are:

- define an answerability criterion tightly,
- collect questions adversarially enough to expose frontier model gaps,
- grade into correct, incorrect, and not-attempted,
- report calibration and abstention behavior, not only accuracy.

ObviousBench takeaway:

- Require a "single obvious target" contract for each item.
- Add "not attempted" or non-answer accounting where relevant.
- Keep answer derivation and ambiguity review visible.
- If using an automated grader for any future family, make it auditable and
  secondary to deterministic scoring where possible.

### IFEval

IFEval's key idea is that instruction-following can be evaluated through
verifiable constraints rather than subjective judgments. It uses prompts with
checkable instructions and metrics that distinguish prompt-level and
instruction-level success.

ObviousBench takeaway:

- ObviousBench's answer-vs-format-vs-strict split is directionally right.
- The paper should define answer correctness and format compliance as separate
  measurement targets, not an implementation detail.
- Add a table of verifier contracts by family, similar to IFEval's constraint
  classes.

### FollowBench

FollowBench organizes instruction following by constraint type and difficulty
level, then reports level-categorized and constraint-categorized results.

ObviousBench takeaway:

- Report by family and by constraint type.
- Include a difficulty ladder only if it is evidenced by item statistics,
  reviewed item criteria, or a later measured human baseline.
- Avoid calling a task "easy" solely by intuition.

### LiveBench

LiveBench is positioned around contamination resistance, frequent updates,
objective automatic scoring, and category diversity.

ObviousBench takeaway:

- Add dated live splits before making strong claims about current models.
- State exactly which split and data vintage every result uses.
- Keep automatic objective scoring as a core differentiator.
- Include a maintenance plan: what gets refreshed, who reviews it, and when
  old items retire or move to public examples.

### Benchmark Aging

When Benchmarks Age studies temporal misalignment in factuality benchmarks and
is useful for one specific ObviousBench caveat: even if many current
ObviousBench answers are intended to be stable, source examples, model
behavior, and public expectations still have a vintage. The paper should report
the exact split date and avoid implying that a static public seed is a live or
permanently contamination-resistant benchmark.

ObviousBench takeaway:

- Report split vintage wherever results are reported.
- Treat public examples as dated source leads.
- Keep refresh policy separate from paper-v1 result claims.

### LiveCodeBench

LiveCodeBench focuses on recent, platform-derived programming tasks and
scenario-specific evaluation. Its useful lesson for ObviousBench is not coding;
it is data-source hygiene.

ObviousBench takeaway:

- Public examples are source leads, not ground truth.
- Each source type needs a curation rule.
- If examples are generated from archetypes, the paper must separate mined
  examples, generated variants, synthetic controls, private items, and live
  refreshes.

### GSM-Symbolic

GSM-Symbolic uses symbolic template variants to test whether mathematical
reasoning performance is robust to superficial changes. It is especially close
to ObviousBench's metamorphic-variant direction.

ObviousBench takeaway:

- Paired/metamorphic variants should be a named contribution.
- Report how often a model passes one variant but fails an equivalent variant.
- Use variants to support hypotheses about brittle string handling, counting,
  instruction parsing, or reasoning shortcuts.

### MMLU-Pro

MMLU-Pro reframes an existing benchmark family by making it harder, less
saturated, and more reasoning-oriented.

ObviousBench takeaway:

- The paper can position ObviousBench as complementary to broad benchmarks:
  high MMLU/GPQA-style scores do not guarantee reliability on tiny public-facing
  tasks.
- A "not a replacement" paragraph should be explicit.

### GPQA And Humanity's Last Exam

GPQA and HLE are opposite-difficulty comparators. They focus on very hard
questions and expert validation, but their paper conventions are useful:

- clear dataset collection pipeline,
- review and validation steps,
- split policy,
- baseline/model evaluation,
- limitations.

ObviousBench takeaway:

- ObviousBench should borrow their dataset-governance rigor while preserving a
  deliberately simple task surface.
- For the fast preprint, human-triviality must be phrased as a design target
  supported by reviewed item evidence. If the paper later makes empirical
  human-performance claims, a measured baseline becomes essential.

### SimpleBench

SimpleBench is not an arXiv benchmark paper in the same way as the others, but
it is very close in public positioning: everyday tasks where unspecialized
humans outperform frontier models. It is useful as a product/communication
comparator.

ObviousBench takeaway:

- The public hook can be accessible and vivid.
- The arXiv paper still needs stricter methodology than a website leaderboard:
  item provenance, scorer contracts, split hygiene, confidence intervals, and
  reproducibility.

## Expected Components Of An ObviousBench Report

### 1. Title

Recommended title:

```text
ObviousBench: Measuring Human-Trivial Failure Modes in Public-Facing Language Models
```

Alternate titles:

- `ObviousBench: A Reliability Benchmark for Human-Trivial Language-Model Tasks`
- `ObviousBench: Benchmarking the Short Tasks Users Expect Models to Never Miss`
- `ObviousBench: Objective Evaluation of Visible, Human-Trivial LLM Failures`

Avoid titles that use "embarrassing", "dumb", "gotcha", or "strawberry" as the
main scholarly frame.

### 2. Abstract

Target: 150 to 220 words.

Must include:

- the gap: broad benchmarks can miss short visible reliability failures,
- what ObviousBench is,
- task families,
- scorer/evaluation design,
- dataset size and split vintage,
- model panel size,
- headline result pattern,
- release/reproducibility note,
- limitation that the benchmark is narrow.

### 3. Introduction

Target: 1.5 to 2 pages.

The introduction should answer:

- Why should anyone care about human-trivial tasks?
- Why are these failures different from hard reasoning failures?
- Why are existing benchmarks insufficient?
- What does ObviousBench contribute?

Proposed contribution list:

1. A benchmark taxonomy for short, human-trivial, public-facing failure modes.
2. A curated dataset with reviewed item cards, source lineage, and split policy.
3. Deterministic scorer contracts that rank answer correctness while reporting
   format compliance and strict correctness as secondary diagnostics.
4. A model sweep across frontier, efficient, and weaker systems with confidence
   intervals, cost, and token-efficiency reporting.
5. Failure analyses including family hotspots, answer/format gaps,
   metamorphic-variant instability, and overthinking on obvious tasks.

### 4. Related Work

Target: 1 to 1.5 pages.

Group related work by role:

- broad knowledge/reasoning benchmarks: MMLU-Pro, GPQA, HLE,
- contamination/live benchmarks: LiveBench, LiveCodeBench,
- short-answer factuality: SimpleQA,
- instruction/format following: IFEval, FollowBench,
- symbolic/metamorphic robustness: GSM-Symbolic,
- everyday simple challenge framing: SimpleBench.

The narrative should be "complementary niche", not "all prior benchmarks are
wrong."

### 5. Benchmark Definition

Target: 2 pages.

Define exactly what counts as an ObviousBench item:

- short single-turn prompt,
- answer can be determined without tools,
- target is unambiguous to a careful human,
- expected human performance is intended to be near ceiling but not measured in
  the fast preprint,
- deterministic scorer exists,
- task is public-facing or screenshot-risk-relevant,
- item is narrow enough that failure is meaningful.

Core families:

- character counting,
- spelling transforms,
- simple arithmetic or numeric comparison,
- word/list counting,
- ordering,
- negation,
- format compliance,
- constraint/object presence.

Each family should have:

- one clean example,
- target answer,
- scorer,
- possible failure types,
- why the task is human-trivial.

### 6. Dataset Construction And Review

Target: 2 to 3 pages.

This is where ObviousBench currently needs the most strengthening before arXiv.

Required components:

- source discovery policy,
- mined vs generated vs synthetic item labels,
- item-card schema,
- reviewer protocol,
- ambiguity criteria,
- duplicate and near-duplicate checks,
- source safety and privacy policy,
- human-triviality design criteria and deferred-validation policy,
- split policy: public/dev/private/live/canary,
- contamination risk handling.

Minimum paper-ready dataset gate:

- every reported item has a completed item card,
- every item has answer derivation and ambiguity notes,
- every scorer has gold examples,
- every public example has either a source URL or generated-control rationale,
- no private or canary item leaks into shareable artifacts,
- measured human-baseline claims are absent from the fast preprint,
- paper reports exact data vintage and commit hash.

### 7. Evaluation Protocol

Target: 1.5 to 2 pages.

Must specify:

- runner: Inspect AI,
- model access path and dates,
- exact model names/aliases,
- prompt format,
- system prompt policy,
- decoding parameters,
- caching policy,
- provider error handling,
- scoring denominators,
- answer/format/strict definitions,
- confidence interval method,
- cost and token estimation method,
- exclusion policy for failed provider runs.

The current repo's separation of answer, format, and strict correctness is a
real contribution. In the paper, it should be presented as a measurement
decision, not just a CSV column.

### 8. Results

Target: 3 to 4 pages.

Expected result tables and figures:

- main leaderboard on the frozen paper split,
- confidence intervals,
- family heatmap,
- answer-vs-format-vs-strict gap plot,
- cost/accuracy or token/accuracy frontier,
- hard-obvious vs balanced split comparison,
- deferred human-validation note,
- provider-error and excluded-run table,
- top failure examples.

The results should report facts first. Do not over-interpret until the analysis
section.

### 9. Analysis

Target: 2 to 3 pages.

Recommended analyses:

- Which families remain hardest after rescoring?
- Which failures are answer failures vs format failures?
- Which models overthink cheap obvious tasks?
- Do reasoning-effort settings help or hurt?
- Do metamorphic variants expose brittleness?
- Are failures concentrated in a small set of archetypes?
- Are public examples easier than private/live variants?

This is where hypotheses belong. Phrase them carefully:

- "These results suggest..."
- "One plausible explanation is..."
- "This is consistent with..."
- "We do not claim this isolates the underlying mechanism."

### 10. Discussion And Implications

Target: 0.75 to 1.25 pages.

This should not become a solutions paper. Suggested implication categories:

- benchmark as a preflight/regression check,
- value of deterministic verifiers,
- need for held-out/live refreshes,
- product risk from small visible failures,
- difference between broad capability and reliability on tiny tasks.

Keep remediation concrete but short:

- add deterministic unit-test-style checks for high-risk UX surfaces,
- separate answer correctness from format compliance in eval dashboards,
- track cost/token burden on simple tasks,
- refresh obvious-failure panels over time.

### 11. Limitations, Ethics, And Reproducibility

Target: 1 page main body plus appendix details.

Must include:

- narrow task scope,
- not a general intelligence benchmark,
- generated variants can still be biased or flawed,
- public data is contamination-prone,
- human-triviality claims depend on the tested population,
- model/provider aliases drift,
- pricing can change,
- deterministic scoring can be too strict or too forgiving,
- risk of overfitting once examples are public,
- source privacy and screenshot handling.

Reproducibility should include:

- code link,
- dataset release policy,
- model configs,
- exact commands,
- commit hash,
- paper split manifest,
- scorer-gold tests,
- generated reports.

## Reporting Results Vs Hypotheses Vs Solutions

For an ObviousBench arXiv report, the main body should roughly allocate space
like this:

| Component | Share Of Main Paper | Purpose |
| --- | ---: | --- |
| Motivation, positioning, related work | 15-20% | Explain the gap and why this benchmark exists. |
| Benchmark definition, data, review, scoring | 30-35% | Prove the benchmark is legitimate and not just a prompt collection. |
| Evaluation protocol and results | 30-40% | Report model behavior, uncertainty, costs, and failure rates. |
| Analysis and hypotheses | 10-15% | Explain patterns without pretending to prove mechanisms. |
| Solutions/implications | 5% or less | Offer practical next steps without making the paper about remediation. |

For ObviousBench specifically:

- results should dominate hypotheses,
- benchmark construction should be at least as important as leaderboard
  results,
- solution proposals should stay lightweight,
- failure examples should illustrate measured categories, not carry the paper by
  anecdote.

## Recommended Paper Outline

Target main body: 12 to 14 pages before references.

Target total arXiv PDF: 25 to 40 pages with appendices.

```text
Abstract

1. Introduction
   1.1 Motivation: visible human-trivial failures
   1.2 Why existing benchmarks leave this gap
   1.3 Contributions

2. Related Work
   2.1 Broad capability benchmarks
   2.2 Short-answer factuality and instruction following
   2.3 Live, contamination-limited, and metamorphic benchmarks

3. ObviousBench
   3.1 Benchmark scope and item acceptance criteria
   3.2 Task families and examples
   3.3 Dataset construction and review
   3.4 Splits and contamination policy

4. Scoring And Evaluation Protocol
   4.1 Deterministic scorer contracts
   4.2 Answer, format, and strict correctness
   4.3 Model panel and run configuration
   4.4 Confidence intervals, cost, and token metrics

5. Results
   5.1 Main model comparison
   5.2 Family-level results
   5.3 Answer-vs-format gaps
   5.4 Cost and token-efficiency frontier
   5.5 Deferred human-validation note

6. Analysis
   6.1 Failure taxonomy
   6.2 Metamorphic variant instability
   6.3 Overthinking on obvious tasks
   6.4 Public vs private/live split behavior

7. Discussion
   7.1 What ObviousBench measures
   7.2 What it does not measure
   7.3 Implications for public-facing AI QA

8. Limitations, Ethics, And Reproducibility

References

Appendix A. Dataset card and item-card schema
Appendix B. Full task family examples
Appendix C. Scorer gold examples
Appendix D. Model configs and prompts
Appendix E. Full leaderboard and family tables
Appendix F. Future human baseline protocol
Appendix G. Additional failure gallery
```

## Figures And Tables To Prepare

Required main figures:

1. `taxonomy`: one figure showing task families and example item forms.
2. `data_lifecycle`: source lead -> item card -> review -> split -> eval.
3. `main_leaderboard`: answer correctness with confidence intervals.
4. `family_heatmap`: model x family answer-correctness rate.
5. `answer_format_gap`: answer correctness vs strict compliance.
6. `cost_frontier`: answer correctness vs estimated cost or tokens per correct.
7. `metamorphic_delta`: paired variant pass/fail inconsistency.

Required main tables:

1. Dataset composition by family, source type, split, and review status.
2. Model panel with provider, alias, run date, parameters, and sample count.
3. Main results with answer correctness, confidence interval, format, strict,
   cost, tokens, and provider errors.
4. Failure taxonomy with example, scorer, and observed count.

Appendix tables:

- full per-model leaderboard,
- per-family results,
- item-level statistics,
- scorer gold examples,
- excluded or failed provider runs,
- future human baseline protocol and exclusion policy.

## Detailed Plan To Write The ObviousBench arXiv Report

### Phase 0: Decide The Submission Standard

Deliverable: a decision record at
`docs/research/2026-06-01-obviousbench-arxiv-readiness-decision.md`.

Decision criteria:

- Is this a preprint-only technical report or a conference-targeted paper?
- Is the primary category `cs.CL`?
- Will the paper include only public data, or a private/live split?
- Is the strict human-baseline path deferred, as currently selected?
- Is the current repo public or private at submission time?
- What code/data artifacts can be linked publicly?

Recommended decision:

- arXiv preprint first,
- primary category `cs.CL`,
- public code plus public example split,
- paper results from a frozen `paper_v1` split that is not identical to the
  already-public proof-point bundle,
- no measured human baseline in the first preprint,
- no claims of leaderboard-grade general model ranking unless private/live data
  exists.

### Phase 1: Freeze The Paper Claims

Deliverables:

- `docs/research/2026-06-01-paper-claim-freeze.md`
- `data/splits/paper_v1_manifest.jsonl`
- `results/paper_v1/manifest.csv`

Steps:

1. Choose the exact benchmark claim.
2. List the task families included.
3. List excluded families and why.
4. Freeze the item pool and split names.
5. Freeze the model panel.
6. Freeze the scoring version.
7. Freeze the cost/pricing vintage.
8. Record the git commit hash.

Claims to allow:

- ObviousBench measures a narrow class of human-trivial failures.
- Deterministic scoring can expose answer and format failures separately.
- Frontier models still exhibit nonzero failure rates on selected obvious
  tasks.
- Some failures are concentrated in family-specific patterns.
- Cost and token burden vary meaningfully even when accuracy is similar.

Claims to avoid:

- ObviousBench proves one model is globally best.
- Public `public_v0` results are contamination-resistant.
- ObviousBench measures general intelligence.
- Model failures prove lack of reasoning.
- Generated seed data alone is sufficient for a durable public leaderboard.

### Phase 2: Make The Dataset Paper-Ready

Deliverables:

- reviewed item cards for the paper split,
- source-card coverage report,
- duplicate/near-duplicate report,
- deferred human-validation policy,
- split policy enforcement.

Required checks:

```bash
.venv/bin/python scripts/validate_dataset.py data/public_v0/*.jsonl data/calibration_v0/smoke_test.jsonl
.venv/bin/python -m pytest tests -q
.venv/bin/python -m ruff check .
```

Additional paper-readiness checks to add if missing:

- every paper item has a completed item card,
- every paper item has answer derivation,
- every paper item has ambiguity notes,
- every paper item names a scorer contract,
- every family has at least one scorer-gold fixture group,
- every source URL is public or replaced by a generated-control rationale,
- no private/canary item is exported into public artifacts.

Future strict human-baseline minimum:

- collect only after the item set, instructions, answer key, and scorer
  contracts are frozen,
- 5 usable participants minimum, 8 to 10 if feasible,
- no tools,
- answer-only interface,
- record per-item accuracy and median response time,
- predefine thresholds before inspecting model comparisons.

### Phase 3: Run The Model Sweep

Deliverables:

- raw Inspect logs in ignored results storage,
- summarized paper results,
- model comparison CSV,
- family comparison CSV,
- delta/paired comparison CSV,
- report HTML/Markdown for inspection.

Recommended model panel:

- strongest available frontier models,
- strong cheaper models,
- one or two small/cheap models,
- known weak or mock control only for plumbing, not headline ranking,
- reasoning-effort variants where a provider exposes them.

Run policy:

- use the same prompt format across models,
- use no explicit system prompt unless the paper argues otherwise,
- record all decoding parameters,
- avoid max-token caps unless needed and documented,
- separate provider failures from model wrong answers,
- do not compare short smoke runs against full runs in headline ranks.

Current repo commands to adapt:

```bash
.venv/bin/obviousbench make-barrage \
  --profile hard_obvious_8x10 \
  --seed 20260531 \
  --out data/barrages/hard_obvious_8x10_seed_20260531.jsonl

.venv/bin/python scripts/run_inspect_eval.py \
  --task obviousbench/tasks/barrage.py \
  --model <provider/model> \
  --log-dir results/raw \
  -T profile=hard_obvious_8x10 \
  -T seed=20260531 \
  --inspect-arg=--no-log-model-api

.venv/bin/obviousbench summarize \
  --logs results/raw \
  --out results/summaries/<paper-run> \
  --cost auto

.venv/bin/obviousbench build-comparison \
  --manifest results/summaries/<paper-run>/manifest.csv \
  --out results/summaries/<paper-run>-comparison

.venv/bin/obviousbench build-report \
  --comparison-dir results/summaries/<paper-run>-comparison \
  --out docs/reports/<paper-report> \
  --generated-on 2026-06-01 \
  --title "ObviousBench Paper Sweep"
```

### Phase 4: Build Analysis Artifacts

Deliverables:

- `paper/figures/*.pdf`
- `paper/tables/*.tex`
- `docs/research/<date>-paper-analysis-notes.md`

Analysis artifacts:

- main answer-correctness leaderboard with Wilson confidence intervals,
- family answer-correctness heatmap,
- answer-vs-strict compliance gap,
- cost/tokens per correct,
- metamorphic pair inconsistency,
- human vs model comparison,
- failure gallery with source-safe snippets,
- top ambiguous or removed items,
- provider failures and excluded runs.

Quality rule:

- Every main-body claim must point to a table, figure, or appendix artifact.
- Every anecdotal failure must map to an aggregate category.
- Every model comparison must name the split and sample count.

### Phase 5: Write The LaTeX Paper

Deliverables:

- `paper/main.tex`
- `paper/references.bib`
- `paper/README.md`
- compiled `paper/obviousbench.pdf`

Writing order:

1. Write the abstract last.
2. Write the benchmark definition first.
3. Write data construction and scorer contracts next.
4. Write results from frozen tables only.
5. Write analysis after results.
6. Write introduction after the contribution list is stable.
7. Write related work from the source corpus above.
8. Write limitations and reproducibility before polishing.

Voice rules:

- Use "we introduce", "we evaluate", "we report", "we find".
- Avoid marketing claims.
- Avoid dunking on specific providers.
- Avoid implying that easy prompts are a complete measure of intelligence.
- Say "human-trivial" only as a design target supported by item criteria unless
  a measured baseline is collected later.
- Say "failure mode" rather than "embarrassing failure" in the main paper.
- Reserve "public-facing" and "visible reliability" for product relevance.

### Phase 6: Internal Review

Deliverables:

- code-quality review notes,
- benchmark-methodology review notes,
- paper-readability review notes,
- privacy/source-safety review notes.

Review questions:

- Can another researcher reproduce the reported numbers?
- Are private or source-sensitive materials excluded?
- Are generated variants clearly labeled?
- Are public-only results overclaimed?
- Are confidence intervals and sample sizes visible?
- Does the paper distinguish answer correctness from strict format compliance?
- Are failure examples representative rather than cherry-picked?
- Does the related-work section cite the nearest obvious comparators?
- Does the conclusion stay within the evidence?

### Phase 7: Release And Submit

Deliverables:

- final PDF,
- arXiv source bundle,
- public code or release tag,
- dataset or public split release,
- model run manifest,
- project page or README update.

arXiv submission checklist:

- Confirm arXiv account and endorsement status.
- Choose primary category, likely `cs.CL`.
- Choose cross-lists only if the paper truly fits them.
- Compile from clean TeX source.
- Confirm no raw private logs, keys, private prompts, or provider headers are in
  source or appendix.
- Add AI-tool disclosure if applicable.
- Add code/data links.
- Add license decision.
- Submit only after the PDF, source, metadata, abstract, and author list are
  final.

## Readiness Checklist

ObviousBench is arXiv-ready when all of these are true:

- [ ] The paper has a frozen split that is not described as proof-point-only.
- [ ] Every paper item has an item card.
- [ ] Every paper item has answer derivation and ambiguity notes.
- [ ] Every scorer has gold examples.
- [ ] The manuscript contains no measured human-baseline, human-timing, or
      model-versus-human claims.
- [ ] Results include answer correctness, confidence intervals, format, strict,
      cost, and token metrics.
- [ ] Results name exact model aliases, run dates, and run parameters.
- [ ] Provider errors and excluded runs are reported separately.
- [ ] Public/private/live/canary split policy is documented.
- [ ] Related work covers SimpleQA, IFEval, FollowBench, LiveBench,
      LiveCodeBench, GSM-Symbolic, MMLU-Pro, GPQA/HLE, benchmark aging, and
      SimpleBench.
- [ ] Limitations explicitly say ObviousBench is narrow and not a general
      intelligence benchmark.
- [ ] The repo has a public-safe release artifact or project page.
- [ ] The arXiv source bundle contains only paper source assets.

## Recommended Next Action

The next concrete step is no longer to open a blank LaTeX file or design a
paper skeleton. Those foundations now exist. The remaining sequence is:

1. keep the reviewed `paper_v1` split frozen unless a specific item defect is
   found,
2. keep human collection deferred for v1 and remove measured-human language,
3. confirm the frozen model panel and frozen analysis plan,
4. run the final model panel only after `make -C paper readiness-preprint`
   passes and the cost ceiling is accepted,
5. generate final figures and tables,
6. replace claim blockers in the LaTeX paper from fixed evidence,
7. build and inspect the final PDF and rerun the PDF build audit,
8. confirm metadata and upload the clean arXiv source bundle.

That sequence gives the paper a research contribution instead of making it a
polished version of the existing proof-point bundle.

## Foundation Progress

Current foundation artifacts:

- [2026-06-01-obviousbench-arxiv-readiness-decision.md](2026-06-01-obviousbench-arxiv-readiness-decision.md)
  records the accepted submission posture and evidence gate.
- [2026-06-01-obviousbench-arxiv-readiness-audit.md](2026-06-01-obviousbench-arxiv-readiness-audit.md)
  records the strict audit. The fast-preprint audit is
  [2026-06-01-obviousbench-arxiv-readiness-audit-preprint.md](2026-06-01-obviousbench-arxiv-readiness-audit-preprint.md),
  where missing human-baseline evidence is deferred rather than blocking v1.
- [2026-06-01-obviousbench-human-baseline-protocol.md](2026-06-01-obviousbench-human-baseline-protocol.md)
  defines the baseline schema and collection threshold.
- [2026-06-01-paper-v1-human-baseline-collection-packet.md](2026-06-01-paper-v1-human-baseline-collection-packet.md)
  assigns all 80 paper items to 5 pseudonymous participants and prepares 400
  response rows without exposing targets in participant-facing packets.
- [2026-06-01-paper-v1-human-baseline-collection-audit.md](2026-06-01-paper-v1-human-baseline-collection-audit.md)
  tracks answer/timing completion, participant progress, family progress,
  duplicate rows, unknown rows, and collection readiness before scoring.
- [2026-06-01-paper-v1-human-baseline-collection-handoff.md](2026-06-01-paper-v1-human-baseline-collection-handoff.md)
  gives the operator checklist, participant instruction block, command ladder,
  privacy boundary, and completion contract for real response collection.
- [2026-06-01-paper-v1-human-baseline-scoring-report.md](2026-06-01-paper-v1-human-baseline-scoring-report.md)
  scores filled baseline responses through the benchmark scorer contracts and
  records why the current empty template cannot support paper-ready claims.
- [2026-06-01-paper-v1-human-baseline-threshold-audit.md](2026-06-01-paper-v1-human-baseline-threshold-audit.md)
  classifies scored baseline rows into strict-path threshold states for later
  validation or revision gating.
- [2026-06-01-paper-v1-human-baseline-operations.md](2026-06-01-paper-v1-human-baseline-operations.md)
  consolidates the human-baseline command ladder, stop rules, promotion target,
  and strict-readiness blockers into one future response-collection handoff.
- [2026-06-01-obviousbench-related-work-positioning.md](2026-06-01-obviousbench-related-work-positioning.md)
  records the comparator matrix used by the related-work section and checks
  that each required citation is present in both the bibliography and
  manuscript.
- [2026-06-01-obviousbench-paper-authoring-toolchain.md](2026-06-01-obviousbench-paper-authoring-toolchain.md)
  records the LaTeX-first authoring decision and explains why R Markdown,
  Quarto, and Pandoc are support options rather than the source of record.
- [2026-06-01-obviousbench-paper-analysis-plan.md](2026-06-01-obviousbench-paper-analysis-plan.md)
  freezes primary metrics, secondary metrics, confidence intervals, exclusions,
  tables, figures, and claim-language policy before final model results exist.
- [2026-06-01-obviousbench-report-section-tracker.md](2026-06-01-obviousbench-report-section-tracker.md)
  tracks manuscript sections, unresolved claim markers, placeholder mentions,
  generated assets, and remaining evidence dependencies.
- [2026-06-01-obviousbench-arxiv-blocker-dashboard.md](2026-06-01-obviousbench-arxiv-blocker-dashboard.md)
  aggregates the current blocker state across deferred human validation,
  model-sweep, claim/prose, PDF/source, preflight, internal review, release,
  and metadata gates.
- [2026-06-01-obviousbench-manuscript-completeness-audit.md](2026-06-01-obviousbench-manuscript-completeness-audit.md)
  audits the current LaTeX manuscript against the expected arXiv report
  components and makes remaining evidence-backed prose work explicit.
- [2026-06-01-obviousbench-arxiv-submission-handoff.md](2026-06-01-obviousbench-arxiv-submission-handoff.md)
  summarizes the upload packet and marks arXiv upload readiness as a hard
  yes/no gate before submission.
- [2026-06-01-obviousbench-paper-pdf-build-audit.md](2026-06-01-obviousbench-paper-pdf-build-audit.md)
  records PDF build-toolchain, PDF artifact, LaTeX log, and static source-audit
  status before final source-bundle upload.
- [2026-06-01-obviousbench-pdf-build-handoff.md](2026-06-01-obviousbench-pdf-build-handoff.md)
  records the recommended Tectonic/MacTeX toolchain path and the exact final
  PDF inspection ladder.
- [2026-06-01-obviousbench-public-release-decision-packet.md](2026-06-01-obviousbench-public-release-decision-packet.md)
  records the remaining release decisions and exact templates to fill after
  license, citation, archive, URL, and submitter choices are confirmed.
- [2026-06-01-obviousbench-paper-reproducibility-manifest.md](2026-06-01-obviousbench-paper-reproducibility-manifest.md)
  records SHA-256 hashes, byte sizes, and cheap rebuild/check commands for the
  current paper artifact set.
- [../status/2026-06-01-obviousbench-arxiv-paper-progress.md](../status/2026-06-01-obviousbench-arxiv-paper-progress.md)
  is the live progress ledger for context recovery.
- [../superpowers/plans/2026-06-01-obviousbench-arxiv-article-completion.md](../superpowers/plans/2026-06-01-obviousbench-arxiv-article-completion.md)
  is the task-by-task completion plan from current state to arXiv submission.
- `data/splits/paper_v1_manifest.jsonl` seeds an 80-item candidate paper split
  from the existing hard-obvious panel.
- [2026-06-01-paper-v1-item-review-queue.md](2026-06-01-paper-v1-item-review-queue.md)
  lists the 80 paper candidates grouped by family; the current queue has no
  blocked items after item-card promotion.
- `scripts/audit_arxiv_readiness.py` provides the repeatable readiness gate
  that should pass before the LaTeX drafting phase begins.
- `configs/paper_v1_analysis_plan.yaml` is the machine-audited source for the
  frozen paper analysis policy.
- `paper/main.tex` and `paper/sections/*.tex` now lay out the full report
  scaffold with blocked claims marked explicitly.
- `scripts/build_paper_assets.py` generates cheap LaTeX tables under
  `paper/tables/` without running model arrays.
