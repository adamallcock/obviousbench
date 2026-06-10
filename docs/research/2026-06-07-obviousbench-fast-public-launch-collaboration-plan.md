---
title: ObviousBench Fast Public Launch Collaboration Plan
date: 2026-06-07
type: plan
status: draft
---

# ObviousBench Fast Public Launch Collaboration Plan

## Executive Take

Recommendation: launch ObviousBench through a non-arXiv-first route.

The fastest credible path is:

1. Public GitHub repository with code, data policy, scorer policy, tests, static
   report, and release notes.
2. Project website as the canonical reader entry point.
3. Human-authored launch essay and X/Twitter thread pointing to the website and
   GitHub release.
4. Hugging Face dataset card and Zenodo DOI if they can be completed without
   slowing the first public announcement.
5. arXiv as a second-wave scholarly anchor after public URLs, endorsement, and
   metadata are confirmed.

This preserves the seriousness of the paper while avoiding arXiv as the launch
gate. The repo is already stronger than a casual blog-post project: it has a
frozen snapshot, deterministic scoring, paper source, generated reports, release
metadata scaffolding, and audits. The missing layer is not more benchmark code.
It is a clean public story, final public URLs, and a natural authorial voice.

## Evidence Boundary

This note is grounded in local repo artifacts inspected on 2026-06-07. It did
not refresh external publishing-platform requirements live. The prior launch
research note from 2026-06-03 contains source links for arXiv, GitHub, Zenodo,
Hugging Face, Papers with Code, and related channels; refresh those primary
sources before performing final publishing operations.

Local evidence inspected:

- `README.md`
- `docs/branding.md`
- `docs/benchmark_card.md`
- `docs/methodology.md`
- `docs/scoring_policy.md`
- `docs/source_policy.md`
- `docs/prompt_policy.md`
- `configs/release_v0_1_0.yaml`
- `configs/release_surfaces_v0_1_0.yaml`
- `docs/release/generated/*`
- `docs/research/2026-06-03-obviousbench-launch-publishing-paths.md`
- `docs/research/2026-06-03-obviousbench-layered-release-plan.md`
- `docs/research/2026-06-01-obviousbench-arxiv-readiness-decision.md`
- `docs/research/2026-06-01-obviousbench-arxiv-submission-metadata.md`
- `paper/main.tex`
- `paper/sections/*.tex`
- `docs/reports/2026-06-03-paper-v1-8x28-current-223-final/*`
- `results/summaries/paper-v1-8x28-current-223-final-20260603/comparison/*`

Lightweight local checks run:

```bash
.venv/bin/python scripts/audit_release_snapshot.py --config configs/release_v0_1_0.yaml --strict
```

Result: PASS, 15 passed, 0 warnings, 0 failures.

```bash
.venv/bin/python scripts/audit_public_release_artifacts.py --strict
```

Result: BLOCKED, 4 passed, 2 failed. The failures are public release URLs and
metadata confirmation, specifically the dataset URL and endorsement/metadata
confirmation.

```bash
.venv/bin/python scripts/audit_paper_claims.py --paper-dir paper
```

Result: 0 unresolved `claimblocked` or `obtodo` markers.

```bash
.venv/bin/python scripts/audit_cost_integrity.py \
  --comparison results/summaries/paper-v1-8x28-current-223-final-20260603/comparison/comparison.csv \
  --strict
```

Result: PASS, 0 findings across 223 comparison rows.

## Repo Evaluation

### What Is Strong

The ethos is unusually clear. ObviousBench is not positioned as a dunk machine
or a global intelligence contest. The repo consistently frames it as reliability
preflight for public-facing AI systems: short prompts, obvious expected answers,
deterministic scorers, and failure examples a product team can understand.

The benchmark scope is legible. The core families are character counting,
spelling transforms, small arithmetic, word/list counting, ordering, negation,
format compliance, and constraint awareness. These are not exotic tasks, which
is exactly why the project works. The result is socially intuitive: when a model
misses these, users notice.

The scoring posture is healthy. The primary score is answer correctness, while
format accuracy and strict correctness remain visible secondary diagnostics.
That prevents the benchmark from over-punishing a model that solved the task but
wrapped the answer in prose, while still preserving product-interface failures.

The release pipeline is more mature than the public copy. The repo already has:

- frozen release config: `configs/release_v0_1_0.yaml`;
- release tag target: `v0.1.0-paper-v1`;
- snapshot: 224 questions, 223 model/settings rows;
- report: `docs/reports/2026-06-03-paper-v1-8x28-current-223-final`;
- generated release surfaces under `docs/release/generated`;
- `CITATION.cff`, `.zenodo.json`, `LICENSE`, and `LICENSE-DATA-DOCS.md`;
- paper source and arXiv bundle machinery;
- audit scripts for release snapshots, public artifacts, costs, paper claims,
  paper sources, and arXiv bundles.

The result story is strong enough for launch. The frozen snapshot has 223
model/settings rows over 224 scored questions each. Three rows reached 100%
answer correctness, 80 rows reached at least 95%, and 40 rows scored below 80%.
The hardest aggregate families were character counting at about 62.4% answer
correctness and spelling transforms at about 68.1%, while word count, ordering,
negation, and format-compliance answer correctness were much higher.

The public claim guardrails are already written. The repo repeatedly says not to
claim general intelligence, global model ranking, measured human performance,
contamination resistance, or internal reasoning-cause explanations.

### What Is Risky

The worktree is extremely mixed. `git status` shows many modified and untracked
files across source, tests, configs, data, paper, reports, and release docs.
Before publishing or staging, this needs a deliberate public-release scrub and
logical commit plan. Do not treat the current checkout as automatically safe to
make public.

The public release audit is still blocked. The local release snapshot is ready,
but public metadata is not. The current blockers are live dataset URL
confirmation and final metadata/endorsement confirmation. Those are not cosmetic
fields; they decide what readers can cite and what arXiv metadata can truthfully
say.

The generated launch copy is too thin. Files like
`docs/release/generated/launch-essay-draft.md`,
`docs/release/generated/project-page.md`, and
`docs/release/generated/social-snippets.md` are useful scaffolds, but they do
not yet explain why ObviousBench exists or what surprised the author. They need
a human-authored layer.

The paper and launch can drift if counts are mixed. Older notes mention 234-row
or 80-item states, while the release config now points at 224 questions and 223
model/settings rows. Public copy should repeat one frozen statement everywhere:

> ObviousBench v0.1 uses a frozen `paper_v1` snapshot with 224 questions and
> 223 model/settings rows, evaluated in the 2026-06-03 evidence run.

The human-baseline caveat must remain explicit. The paper says human-triviality
is a design target supported by reviewed item cards, answer derivations, and
scorer-gold artifacts. It does not report measured human accuracy or response
time. That is acceptable for a fast launch, but it must be stated plainly.

Cost and thinking claims need restraint. The cost integrity audit passes for the
selected comparison, but Anthropic reasoning-token and thinking-budget language
has known caveats in prior notes. Launch copy should say cost/token burden is
reported for the frozen run, not that reported reasoning telemetry always equals
billed hidden thinking.

## What The arXiv Paper Says In Plain English

Use this as the factual skeleton for your own writing.

### Abstract

ObviousBench is a compact benchmark for short questions that a careful human
should find easy but that language models can still visibly fail. The paper uses
a frozen `paper_v1` split with 224 questions across eight task families. It
reports a 2026-06-03 evidence snapshot covering 223 model/settings rows and 178
unique model identifiers. It does not claim a measured human baseline.

### Introduction

The motivating idea is simple: some AI failures are instantly legible. A model
counts letters wrong, removes the wrong character, ignores a format instruction,
or misses a plain constraint. The paper argues that these failures are worth
tracking because they are visible to users and cheap to score objectively.

### Positioning

The paper places ObviousBench near everyday-reasoning and instruction-following
benchmarks, but with a narrower regression-testing posture. It is not trying to
be MMLU-Pro, GPQA, Humanity's Last Exam, or a broad capability exam. It is a
deterministic preflight check for short, objective mistakes.

### Benchmark

An item is eligible only if it is understandable without external context, has
an objective answer, can be solved without tools, can be scored
deterministically, and would be visible if failed in a public-facing AI product.
The families are concrete: counting, spelling edits, arithmetic, ordering,
negation, format compliance, word counting, and constraint awareness.

### Item Review

Public examples are treated as leads, not ground truth. The benchmark item must
stand on its own, with an answer derivation, ambiguity notes, scorer contract,
split policy, leakage risk, review status, reviewer, and review date.

### Scoring

The primary score is answer correctness. Format correctness and strict
correctness are secondary diagnostics. Provider errors, refusals, and timeouts
remain counted after retries but are separately visible so readers can tell
wrong answers apart from provider/infrastructure issues.

### Results

The frozen run has 223 model/settings rows and 224 scored attempts per row.
Three rows answered all 224 questions correctly. Eighty rows reached at least
95% answer correctness. Forty rows scored below 80%. The paper treats this as
first-draft benchmark evidence, not a universal model ranking.

### Analysis

The strongest failure concentration is in character counting and spelling
transforms. Format failures reveal a different product issue: sometimes the
answer is semantically right but the model violates the requested response
interface. Thinking/cost analysis should be read together with accuracy, not as
a standalone leaderboard.

### Discussion

The paper's best line of argument is that the narrowness is the point. Short,
objective prompts make deterministic scoring, cheap repeated runs, and readable
failure galleries practical. The right use is regression monitoring and product
quality work, not crowning one universal model winner.

### Limitations

The limitations are important and should stay visible: no general intelligence
claim, no measured human baseline, public-data contamination risk, generated
variant risk, model/provider/pricing drift, and no claim that failures reveal a
specific internal reasoning defect.

## Recommended Collaboration Model

Best collaboration pattern: keep the paper evidence-locked and create a
separate human-authored launch essay canvas.

The paper should remain compact, cautious, and artifact-backed. Your natural
voice belongs in the launch essay, website intro, README opening, and social
thread. That is where you can explain why you built this, what felt surprising,
what you do and do not want people to conclude, and how this fits your broader
view of model reliability.

### Working Files

Use two layers:

1. Evidence layer: existing paper, report, release config, benchmark card, and
   generated release metadata.
2. Voice layer: a new human-authored draft, preferably:
   `docs/release/2026-06-07-obviousbench-launch-essay-working-draft.md`.

Keep the voice layer hand-authored. It can cite generated facts, but it should
not be generated by `scripts/build_release_assets.py`.

If you want inline comments, freewriting from a phone, or a less-code-shaped
writing surface, a Google Doc can be useful as the temporary drafting surface.
For final release provenance, bring the accepted version back into the repo as
Markdown.

### Collaboration Loop

1. I prepare a plain-English paper digest and a launch essay scaffold.
2. You freewrite rough notes under prompts without worrying about polish.
3. I preserve your phrasing where it has voice, tighten structure where needed,
   and mark every factual claim as supported, needs-check, or remove.
4. We split the final writing into four outputs:
   - website landing copy;
   - launch essay;
   - README opening section;
   - X/Twitter thread.
5. Before publishing, I run a claim pass against the frozen snapshot, then a
   link/public-metadata pass against the live public surfaces.

### Prompts For Your Voice Pass

Write rough bullets or paragraphs under these. Do not try to sound academic.

- What made you want to build a benchmark for "obvious" failures?
- What examples made the problem feel real rather than abstract?
- What surprised you in the 224-question / 223-row snapshot?
- What result did you expect but did not see?
- What do you wish more model/product teams tested before launch?
- What is the difference between "this model failed a task" and "this model is
  bad"?
- Why is deterministic scoring important to you here?
- What should readers not overclaim from this release?
- How should someone use ObviousBench next Monday in an actual product workflow?
- What would make v0.2 feel meaningfully stronger?

### Claim Guardrail Labels

When editing your draft, mark claims this way:

- `SUPPORTED`: directly backed by the frozen report, paper, or config.
- `AUTHOR_VIEW`: your interpretation or motivation, allowed if clearly framed.
- `NEEDS_CHECK`: likely true but requires a current source or fresh local audit.
- `REMOVE_OR_SOFTEN`: too broad, unsupported, or likely to invite misreading.

This lets your essay sound human without accidentally weakening the benchmark's
credibility.

## Non-arXiv-First Launch Plan

### Phase 1: Freeze The Public Story

Goal: one sentence, one snapshot, one claim surface.

Canonical sentence:

> ObviousBench v0.1 is a frozen 224-question benchmark snapshot for short,
> human-trivial tasks where public-facing language models can still make
> visible mistakes.

Acceptance criteria:

- All launch copy distinguishes 224 questions from 223 model/settings rows.
- No public copy says measured human baseline.
- No public copy says global model ranking.
- No public copy equates reasoning-token telemetry with billed hidden thinking.
- The website, README, release notes, and social post all link to the same
  canonical report.

### Phase 2: Prepare The Public Repo

Goal: make GitHub safe and useful before social traffic arrives.

Acceptance criteria:

- Private/generated/provider-sensitive files are excluded.
- `README.md`, benchmark card, methodology, scoring policy, source policy, and
  prompt policy are present.
- Repro commands use the frozen snapshot or clearly identify dev-only commands.
- `LICENSE`, `LICENSE-DATA-DOCS.md`, `CITATION.cff`, and `.zenodo.json` are
  present and consistent.
- The public repo URL in `configs/release_v0_1_0.yaml` resolves live.

### Phase 3: Ship The Website

Goal: make the website the easiest entry point.

Recommended first viewport:

- Name: ObviousBench.
- One-line promise: "Catch obvious AI mistakes before users do."
- Short explanation: frozen 224-question reliability snapshot for visible
  public-facing model failures.
- Primary links: GitHub, report, dataset/card if ready, release notes.
- Immediate caveat: static snapshot, not a permanent global ranking.

Acceptance criteria:

- Website links resolve in a clean browser.
- Report path or hosted equivalent is accessible.
- Leaderboard and failure examples are easy to find.
- Caveats are visible without sounding defensive.

### Phase 4: Publish The Human Essay And Social Thread

Goal: make the launch understandable and worth sharing.

Essay structure:

1. The problem: some AI failures are small but highly visible.
2. The benchmark: short prompts, objective answers, deterministic scorers.
3. The result: three perfect rows, many near-perfect rows, and a long tail of
   visible failures.
4. The surprise: character counting and spelling transforms remain hard across
   many rows.
5. The use case: preflight and regression testing for product teams.
6. The caveats: static snapshot, no human baseline, no global ranking.
7. The invitation: run it, inspect failures, contribute better splits.

Thread structure:

1. "I built ObviousBench to test obvious AI mistakes before users find them."
2. "v0.1 is a frozen 224-question snapshot across 223 model/settings rows."
3. "Three rows got everything right; 40 scored below 80%."
4. "The hardest families were not exotic: character counting and spelling
   transforms."
5. "It uses deterministic scorers, not an LLM judge."
6. "The goal is not to shame models or declare a universal winner."
7. "It is a preflight/regression tool for public-facing AI products."
8. "Links: website, GitHub, report, dataset/card if live."

### Phase 5: arXiv Later

Goal: keep arXiv serious without letting it block launch.

Use arXiv after:

- public repository URL is live;
- dataset URL is live or intentionally removed from metadata;
- Zenodo DOI is minted or explicitly pending;
- endorsement status is resolved;
- metadata note is changed from draft to confirmed;
- final PDF has been visually inspected;
- public artifact audit passes.

This lets arXiv become the canonical scholarly record instead of the first
public proof that the project exists.

## Immediate Next Actions

1. Create `docs/release/2026-06-07-obviousbench-launch-essay-working-draft.md`
   with the voice prompts above and a fact sidebar.
2. Confirm whether the first public launch requires Hugging Face and Zenodo on
   day one, or whether GitHub plus website plus static report is enough.
3. Run a public-repo scrub pass before any publish or push.
4. Replace the skeletal generated social snippets with hand-authored launch
   copy derived from the essay.
5. After public URLs are live, rerun:

```bash
.venv/bin/python scripts/audit_public_release_artifacts.py --strict
```

6. Only then decide whether to submit arXiv immediately or hold it for the
   second wave.
