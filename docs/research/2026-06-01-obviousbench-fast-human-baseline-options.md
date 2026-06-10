---
title: ObviousBench Fast Human Baseline Options
date: 2026-06-01
type: research
status: accepted
---

# ObviousBench Fast Human Baseline Options

## Decision Summary

Accepted v1 path: no measured human collection for the first arXiv preprint.
The strict human-baselined benchmark path remains available later after
`paper_v1` is frozen.

If `paper_v1` is still moving, do not make a measured human baseline a hard
preprint gate. A human solve baseline is valuable only after the benchmark is
frozen; otherwise every substantive item change invalidates the collected human
rows.

Recommended path:

1. For a faster arXiv preprint, remove measured-human-baseline language from
   the main claim and frame ObviousBench as a deterministic, objective,
   reviewer-adjudicated benchmark for short tasks intended to be obvious to
   humans.
2. Keep the current human-baseline machinery as an appendix/follow-up path, not
   as the publication blocker.
3. Before submission, strengthen the non-human evidence: item cards, answer
   derivations, ambiguity notes, scorer-gold tests, scorer error audit, exact
   model-run manifests, and limitations text.

This is consistent with several recent benchmark papers: many use human work
for data construction, verification, or evaluator validation rather than a full
measured human solve baseline.

## What Fast Human Collection Can Support

A 2-5 day collection can support a small no-tools validation baseline. It should
not be sold as population-level psychometrics or a stable public claim unless
the dataset is frozen.

The current local design already has the minimum shape:

- 80 `paper_v1` items.
- 5 participants.
- 80 rows per participant.
- 400 response rows total.
- answer text plus elapsed seconds.
- scorer fills `correct`; humans do not see the answer key.

With only 5 participants, item-level human-triviality should be conservative:

- core item: all 5 participants correct and median time below a predefined
  short-answer threshold.
- review item: any miss, confusion note, extreme latency, or participant
  complaint.
- exclude or revise item: ambiguity, multiple plausible answers, scorer
  mismatch, or evidence problem.

If there is budget/time for stronger evidence, use 8-10 participants and keep
5 usable participants as the minimum after exclusions.

## Fast Collection Options

| Option | Timeline | Reliability | Best use | Main risk |
| --- | ---: | --- | --- | --- |
| Internal trusted participants | 1-2 days | Medium | Fast sanity check, appendix evidence | Biased sample, weaker external credibility |
| Prolific | 1-3 days for a small study, depending on eligibility and launch | Medium-high with checks | Fast paid no-tools validation | Self-reported screening; cannot fully prevent search/AI use |
| CloudResearch Connect | 1-3 days for a small study, depending on launch | Medium-high with checks | Alternative paid panel | Same external-tool-control limits |
| Upwork/contract raters | 2-5 days | Medium-high if supervised | More controllable instructions and follow-up | Onboarding overhead, less standardized research sample |
| No measured baseline in v1 | 0 days | Strong if claims are narrowed | Fast arXiv preprint | Cannot make measured human-performance claim |

For paid panels, use a short form, fair pay, explicit no-tools attestation,
instruction/comprehension checks, simple canary items, duplicate/rephrased
items, per-item timing, and a predeclared exclusion policy. Prolific's official
researcher guidance supports [demographic prescreening](https://researcher-help.prolific.com/en/article/412c0a),
[attention/comprehension checks](https://researcher-help.prolific.com/en/article/fb63bb),
and [authenticity checks](https://researcher-help.prolific.com/en/articles/445144-what-is-an-authenticity-check).
CloudResearch Connect presents itself as a [research recruitment platform](https://www.cloudresearch.com/products/connect-for-researchers-archive/)
with participant-quality tooling.

## Precedent From Similar Benchmarks

| Benchmark | Human work pattern | Implication for ObviousBench |
| --- | --- | --- |
| SimpleQA | Human trainers created Q/A pairs; another trainer independently answered; items were kept only on agreement; a third-trainer audit estimated about a 3% benchmark error rate. Source: [SimpleQA PDF](https://cdn.openai.com/papers/simpleqa.pdf). | Strong precedent for human verification and error-rate estimation without a human performance baseline. |
| GPQA | Domain experts wrote questions; PhD-level experts and skilled non-experts were measured, with non-experts spending over 30 minutes with web access. Source: [arXiv:2311.12022](https://arxiv.org/abs/2311.12022). | Strong methodology, but too heavy for a few-day ObviousBench preprint. |
| MMLU-Pro | Uses expert review for answer correctness and distractor validity, including human expert review of suspected false-negative options. Source: [NeurIPS paper PDF](https://proceedings.neurips.cc/paper_files/paper/2024/file/ad236edc564f3e3156e1b2feafb99a24-Paper-Datasets_and_Benchmarks_Track.pdf). | Good precedent for item-level expert/reviewer quality control rather than a solve baseline. |
| IFEval | Avoids slow and non-reproducible human evaluation by using verifiable instructions and deterministic checks. Source: [arXiv:2311.07911](https://arxiv.org/abs/2311.07911). | Strong precedent for leaning into objective scoring when tasks are checkable. |
| LiveBench | Uses recent sources and objective ground-truth answers, enabling automatic scoring without LLM judges. Source: [LiveBench GitHub](https://github.com/livebench/livebench). | Strong precedent for objective scoring and contamination-aware refreshes without a human solve baseline. |
| LiveCodeBench | Collects fresh contest problems and relies on executable/objective coding evaluation. Source: [LiveCodeBench GitHub](https://github.com/livecodebench/livecodebench). | Precedent for external-source objective validity rather than collecting new human answers. |
| FollowBench | Validates model-based evaluation against 3 expert human labelers on a sampled set, reporting agreement with human labels. Source: [arXiv PDF](https://arxiv.org/pdf/2310.20410). | Good precedent for validating the evaluator/scorer on a sample instead of human-solving every benchmark item. |
| GSM-Symbolic | Generates symbolic variants, applies automated checks, manually reviews 10 random samples per template, and re-reviews items not answered by at least two models. Source: [arXiv PDF](https://arxiv.org/pdf/2410.05229). | Precedent for template/data-generation audits and targeted manual review. |
| Humanity's Last Exam | Expert-created questions, audits, community bug bounty, author/reviewer consensus, and reported expert disagreement rates. Source: [arXiv:2501.14249](https://arxiv.org/abs/2501.14249). | Precedent for acknowledging expert disagreement and using post-release repair workflows. |

The common pattern: if human baselines are central to the claim, they are slow
and carefully designed. If the benchmark has objective answers, papers often
prefer verifiable scoring, item validation, and limited human audits.

## If We Remove Human Collection From V1

The paper can still be credible, but the claims must change.

Allowed wording:

- "ObviousBench targets short, objectively scored tasks designed to be trivial
  for unassisted humans."
- "We provide item cards, answer derivations, ambiguity notes, and scorer-gold
  tests to support item validity."
- "A measured human baseline is deferred until the benchmark split is frozen."

Avoid wording:

- "Humans score 95%+."
- "Human-triviality is empirically established."
- "The benchmark measures the gap between models and humans."
- "ObviousBench is a leaderboard-grade public split."

Required substitutions for the missing baseline:

- Complete reviewed item cards for every `paper_v1` item.
- Freeze the exact `paper_v1` manifest before final model runs.
- Add answer derivation and ambiguity notes for each item.
- Expand scorer-gold examples for every scorer used in the paper.
- Manually inspect a sample of model outputs marked correct and incorrect to
  estimate scorer false positives/false negatives.
- Report model aliases, provider, date, decoding parameters, retries, failures,
  cost, tokens, and cache policy.
- Add limitations text saying that measured human performance is future work
  and that changing the benchmark invalidates any future human baseline.
- Update readiness gates so the fast-preprint path does not require
  `data/human_baseline/paper_v1.csv`.

## If We Still Want A 2-5 Day Baseline

Use this protocol only after `paper_v1` is frozen.

Day 0:

- Freeze item set and answer key.
- Run the scorer-gold suite.
- Build a short form from participant packets.
- Pilot 10 items with 1 trusted participant.
- Fix confusing instructions or form errors, not item answers.

Day 1:

- Recruit 7-10 participants for 5 usable completions.
- Use Prolific, CloudResearch Connect, trusted internal participants, or
  supervised contractors.
- Block mobile if the form makes timing or copy/paste unreliable.
- Require no search, no calculators, no AI/model assistance, and no external
  tools.

Day 2:

- Collect responses.
- Monitor completion rate and obvious bad data.
- Launch backup participants if needed.

Day 3:

- Score with the existing scoring helper.
- Run collection, scoring, and threshold audits.
- Review every item with a human miss or scorer mismatch.

Days 4-5:

- Freeze a human-baseline report.
- Add aggregate accuracy, family-level accuracy, item-level flags, median
  timing, and exclusion rules to the appendix.
- Keep limitations explicit: small no-tools convenience sample, not a
  representative estimate of the general population.

## Implementation Plan

For the fast arXiv preprint, use the no-measured-baseline path now. Keep the
human collection packet, but do not block the preprint on it. The current work
package is the "fast preprint mode" patch:

- update the readiness decision/gates to make human baseline optional under
  fast-preprint mode;
- revise manuscript claims to avoid measured-human language;
- strengthen item-card, scorer-gold, scorer-audit, and limitation sections;
- keep a clearly named future-work section for a frozen-split human baseline.

Acceptance criteria:

- `make -C paper readiness-preprint` treats the header-only
  `data/human_baseline/paper_v1.csv` as acceptable.
- `make -C paper readiness` still blocks without real human rows.
- `make -C paper sweep-plan` uses the preprint readiness profile by default.
- The paper and planning docs contain no claim that human accuracy, timing, or
  model-versus-human gaps have been measured.
- The strict human-baseline path remains documented as future validation.
