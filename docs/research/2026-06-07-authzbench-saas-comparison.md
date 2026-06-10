---
title: AuthZBench-SaaS Comparison For ObviousBench
date: 2026-06-07
type: research
status: draft
---

# AuthZBench-SaaS Comparison For ObviousBench

## Executive Summary

I inspected ObviousBench locally and compared it with
[`bmendonca3/authzbench-saas`](https://github.com/bmendonca3/authzbench-saas),
cloned at commit `53d953e726e6bea74c9abd5288e7bc8df32345f4`
(`Record current Qwen validation evidence`, committed 2026-06-07 11:53:52
UTC-07:00).

Verdict: AuthZBench-SaaS is worth borrowing from, but mostly at the benchmark
governance, public-evidence, and reviewer-packaging layer. ObviousBench is
already stronger on broad model-panel execution, Inspect integration, pricing
and cost telemetry, paper/release automation, and deterministic short-answer
scoring. AuthZBench-SaaS is sharper at making benchmark claims auditable for an
outside reader: what each artifact proves, what it does not prove, which runs
are current or stale, which rows are leaderboard-eligible, and what reviewers
should inspect.

The highest-value inspiration for ObviousBench is:

1. Add a reader-facing `docs/evidence-and-claims.md` claim matrix.
2. Add a machine-readable run/snapshot registry that labels current, stale,
   exploratory, proof-point, and release-snapshot artifacts.
3. Add benchmark fingerprints or comparability keys to summaries, comparisons,
   and release reports.
4. Generate an internal-only item review matrix from dataset rows and item
   cards.
5. Package a small external review packet and review registry.
6. Create one public artifact validation wrapper with stable expected outputs.

Do not copy AuthZBench-SaaS's domain-specific live HTTP target machinery,
authorization replay schemas, or private-holdout leaderboard rules directly.
Those make sense for an agentic AppSec benchmark; ObviousBench should adapt the
underlying evidence discipline to short, human-trivial model reliability tasks.

## Sources Inspected

### ObviousBench Local Sources

Primary local files inspected:

- `README.md`
- `docs/benchmark_card.md`
- `docs/methodology.md`
- `docs/scoring_policy.md`
- `docs/source_policy.md`
- `docs/prompt_policy.md`
- `docs/runbook.md`
- `docs/architecture/2026-05-31-current-architecture.md`
- `paper/README.md`
- `paper/Makefile`
- `configs/release_v0_1_0.yaml`
- `docs/research/2026-06-03-obviousbench-launch-publishing-paths.md`
- `docs/research/2026-06-03-obviousbench-layered-release-plan.md`
- `obviousbench/datasets/schemas.py`
- `obviousbench/datasets/validation.py`
- `obviousbench/scorers/common.py`
- `obviousbench/scorers/accepted_answers.py`
- `obviousbench/analysis/metrics.py`
- `obviousbench/analysis/comparison.py`
- `obviousbench/analysis/benchmark_report.py`
- `obviousbench/research/release_snapshot.py`
- `obviousbench/research/public_release_audit.py`
- `obviousbench/research/cost_integrity.py`
- `obviousbench/research/final_result_artifacts.py`

Important local caveat: this checkout was already heavily dirty before this
research pass. I did not modify existing source or generated artifacts.

### AuthZBench-SaaS Sources

External repo inspected from `/tmp/authzbench-saas`:

- `README.md`
- `ROADMAP.md`
- `artifact/README.md`
- `artifact/install.md`
- `artifact/run-bundle.md`
- `artifact/expected-output/v1-readiness-public-view.json`
- `docs/benchmark-card.md`
- `docs/evidence-and-claims.md`
- `docs/methodology.md`
- `docs/score-policy.md`
- `docs/score-stability-policy.md`
- `docs/result-schema.md`
- `docs/leaderboard-schema.md`
- `docs/baseline-credibility.md`
- `docs/holdout-and-contamination.md`
- `docs/holdout-rotation-protocol.md`
- `docs/task-quality-rubric.md`
- `docs/task-quality-matrix.md`
- `docs/v0-release-plan.md`
- `docs/v1-community-submission-governance.md`
- `docs/publish-checklist.md`
- `docs/release-evidence.json`
- `docs/reviews/README.md`
- `docs/reviews/external-review-packet.md`
- `docs/reviews/external-review-summary.md`
- `baselines/baseline-registry.json`
- `authzbench/core.py`
- `authzbench/score.py`
- `authzbench/run.py`
- `authzbench/validate_manifests.py`
- `scripts/validate_public.py`
- `scripts/validate_baseline_registry.py`
- `scripts/validate_v0_release.py`
- `scripts/validate_leaderboard_submission.py`
- `scripts/generate_task_quality_matrix.py`
- representative task and submission files under `tasks/` and `examples/`.

Validation run:

```bash
python3 -m venv /tmp/authzbench-saas/.venv
/tmp/authzbench-saas/.venv/bin/python -m pip install -e /tmp/authzbench-saas
/tmp/authzbench-saas/.venv/bin/python scripts/validate_public.py --include-scripted-baseline
```

Result after fetching full history: passed. The run included 190 unit tests,
54 public manifest validation, baseline registry validation, redacted protected
private evidence validation, release/v1 readiness status reporting, generated
task quality matrix and chart diff checks, leaderboard example validation,
compileall, privacy scan, and a deterministic scripted 54-task baseline.

Validation caveat: the first attempt from a depth-1 clone failed only because
`validate_v1_readiness.py --public-view --expected-output ...` added
`benchmark_source_sha must exist as a commit` when the historical SHA was not
present in the shallow clone. After `git fetch --unshallow`, the expected
fixture matched and the public validation wrapper passed. This is a useful
warning if we add historical-SHA checks to ObviousBench public validation.

## Side-By-Side Read

### ObviousBench Strengths

ObviousBench is already mature in areas AuthZBench-SaaS does not try to solve:

- Native Inspect AI integration for provider execution.
- Broad model and thinking-setting panel machinery.
- Dry-run cost estimation through `runcost` and saved usage history.
- Cost integrity audits that block successful rows with missing telemetry.
- Answer, format, and strict accuracy split into distinct metrics.
- Wilson intervals, paired deltas, effort/cost curves, metamorphic consistency,
  and static report generation.
- Item-card validation as provenance and review scaffolding.
- Release snapshot config, generated release surfaces, paper Makefile gates,
  arXiv source-bundle audits, and public-release artifact audits.
- A clear prompt policy: native provider mode, no explicit system prompt, no
  tools, no browsing, no chain-of-thought request.

AuthZBench-SaaS should not cause us to doubt the technical core of ObviousBench.
The stronger lesson is presentation and governance, not replacing the runner.

### AuthZBench-SaaS Strengths

AuthZBench-SaaS is especially good at saying exactly what stage it is in:
released v0.0 artifact, not hosted leaderboard, not community benchmark, current
v1-prep public split, stale historical baselines, protected private evidence,
and future v1 governance. That language appears repeatedly in README, benchmark
card, evidence docs, release notes, and readiness gates.

The strongest reusable patterns are:

- `docs/evidence-and-claims.md`: a matrix with `Evidence`, `What It Proves`,
  and `What It Does Not Prove`.
- `baselines/baseline-registry.json`: each run is a harness check, model
  baseline, or tool-agent baseline; each row is current, stale, legacy, or a
  release snapshot.
- `benchmark_fingerprint`: a hash/count contract over tasks and scoring policy.
- `comparability_key`: a validation rule that prevents superficially similar
  rows from being compared when split, scoring, or fingerprint differ.
- `docs/task-quality-rubric.md` and generated `docs/task-quality-matrix.md`:
  public-safe task audit artifacts that summarize structure without leaking
  private details.
- `docs/reviews/external-review-packet.md`: a ready-to-send reviewer packet
  with lanes, questions, evidence paths, and acceptance criteria.
- `artifact/README.md`: a compact reproducibility packet separate from the
  main README.
- `scripts/validate_public.py`: one wrapper that expresses what a public
  checkout should be able to prove.
- `docs/release-evidence.json`: a truth table for whether release evidence
  exists, including local validation, fresh clone validation, remote CI, Docker
  smoke, privacy scan, and protected holdout execution.

### AuthZBench-SaaS Weak Spots

These are not reasons to ignore the repo, but they matter for what we borrow:

- The depth-1 clone validation path can fail because a historical commit check
  expects full Git history. If ObviousBench adopts historical evidence checks,
  it should either fetch the required commit or make the public expected fixture
  independent of clone depth.
- The repo has many overlapping status labels: v0.0 release, v1-prep, current
  public split, frozen release snapshot, public readiness, private readiness,
  hosted readiness. They are honestly documented, but cognitively heavy.
  ObviousBench should borrow the precision without overmultiplying labels.
- Many AuthZBench-SaaS mechanics are domain-specific: Docker target apps,
  target request logs, backend replay, tool-agent artifacts, private route
  variants, and host path denial. They are not a natural fit for short-answer
  model reliability.
- The docs are very extensive. Useful for audit, but a first-time reader can
  drown unless there is one canonical "read this first" path.

## Recommendation Backlog

### 1. Add An Evidence And Claims Matrix

Recommendation: create `docs/evidence-and-claims.md`.

Purpose: give readers a single truth table for ObviousBench claims, especially
around public seed data, paper-v1 snapshot, repeated/pass-k studies, cost
telemetry, human-baseline status, and future leaderboard plans.

Suggested rows:

| Evidence | What It Proves | What It Does Not Prove |
| --- | --- | --- |
| `public_v0` 401-item seed dataset | ObviousBench has runnable public seed data across 8 families | leaderboard-grade hidden-set model ranking |
| `paper_v1` 224-question / 223 model-settings snapshot | a frozen release-prep result set exists | permanent model-family ranking or current provider behavior |
| item-card draft layer | provenance/review scaffolding exists | every seed item has completed trusted human review |
| deterministic scorer gold fixtures | scorer behavior is regression-tested | task ambiguity is solved for every item |
| cost integrity audit | selected report rows are not silently missing usage/cost telemetry | provider pricing cannot drift after release |
| pass-k/repeated runs | selected models have reliability diagnostics | pass-k should replace the frozen leaderboard metric |
| human-baseline packet | future collection workflow exists | measured human baseline exists today |
| static report | reader can inspect one frozen snapshot | hosted leaderboard or live submissions are available |

Acceptance criteria:

- The doc uses explicit "use" and "avoid" public framing.
- README and benchmark card link to it.
- It names exact snapshot paths and dates.
- It is updated when a new release snapshot is selected.

### 2. Add A Snapshot Or Baseline Registry

Recommendation: add a machine-readable registry, likely under
`docs/release/snapshot-registry.json` or `results/summaries/registry.json`, with
a small validator.

Purpose: prevent the 222/223/234-row and 80/224-question confusion from
reappearing in public copy.

Useful fields:

- `id`
- `kind`: `proof_point`, `paper_snapshot`, `exploratory_reliability`,
  `historical_snapshot`, `release_candidate`
- `status`: `current_release_candidate`, `current_exploratory`, `stale`,
  `legacy_snapshot`, `deprecated`
- `dataset_split`
- `item_count`
- `model_setting_count`
- `manifest`
- `comparison_dir`
- `report_dir`
- `generated_on`
- `claim_allowed`
- `claim_disallowed`
- `requires_rerun_before_current_comparison`
- `source_commands`

Acceptance criteria:

- Validator checks referenced manifests, comparison CSVs, report dirs, and row
  counts.
- Release config and paper Makefile either consume this registry or agree with
  it.
- Historical rows remain visible but are clearly non-current.

### 3. Add Benchmark Fingerprints Or Comparability Keys

Recommendation: compute a public-safe fingerprint for summaries and comparison
directories.

For ObviousBench, the fingerprint should hash:

- dataset item IDs in the scored split or barrage
- item targets or target hashes, depending on public/private split policy
- scorer names and scorer policy version
- prompt policy version or prompt template IDs
- split name and data vintage
- barrage profile and seed
- generation settings that materially affect results
- comparison builder version, if needed

Why it matters: two rows with the same sample count are not necessarily
comparable if one uses a different scorer policy, different prompt template,
or a repaired result artifact. This would make report and pass-k work less
fragile.

Acceptance criteria:

- `obviousbench summarize` or `build-comparison` emits the fingerprint.
- `build-report` displays or links the fingerprint.
- A validator can reject mixed-fingerprint comparison manifests unless explicitly
  allowed.

### 4. Generate An Internal Item Review Matrix

Recommendation: add an internal-only generator analogous to AuthZBench-SaaS's
task quality matrix, but based on ObviousBench item rows and item cards.

Suggested columns:

- item ID
- family and subfamily
- split
- source type
- review status
- human triviality label
- scorer
- answer type
- prompt template ID
- `strict_format`
- source-ref count
- item-card status
- answer-derivation present
- ambiguity notes present
- accepted-answer override present
- metamorphic group ID present
- quality flags

Public-safety rule: for public splits, targets are already visible in JSONL; for
future private/trusted splits, matrix output should use hashes/counts rather
than raw targets.

Acceptance criteria:

- Generator writes both JSON and Markdown.
- Validation can fail if required review signals are missing for a trusted or
  release split.
- README or benchmark card links the matrix as a review aid, not as proof of
  leaderboard readiness.

### 5. Create An External Review Packet

Recommendation: add `docs/reviews/` with a small packet and registry.

Suggested lanes:

- Benchmark/evals methodology: split policy, leakage risk, statistics, ranking
  interpretation.
- Scoring and prompt policy: deterministic scorers, format-vs-answer policy,
  accepted-answer overrides, provider-error handling.
- Paper/results review: figures, tables, claim boundaries, release snapshot
  consistency.
- Dataset review: item ambiguity, human triviality, source safety, item-card
  sufficiency.

Acceptance criteria:

- Packet lists exact artifacts to send.
- Packet lists questions for reviewers.
- Summary distinguishes packet-ready from review-complete.
- No external review is claimed until real findings or explicit no-finding
  dispositions are recorded.

### 6. Add A Public Artifact Validation Wrapper

Recommendation: create a single public-safe wrapper, perhaps
`scripts/validate_public_artifact.py`.

Suggested default checks:

- dataset validation for public/release data
- item-card validation appropriate to release status
- selected targeted tests for scorers, report builder, release snapshot, and
  cost integrity
- compileall or package import smoke
- release snapshot registry validation
- generated internal item review matrix clean-diff check
- generated report contract check
- privacy/path scan for tracked public artifact files
- optional fresh-clone check

Important caveat from AuthZBench-SaaS: avoid clone-depth-sensitive expected
fixtures unless the wrapper fetches the required history or treats the missing
historical commit as an expected public-clone condition.

### 7. Add Release Evidence JSON

Recommendation: add a truth-source file similar to `docs/release-evidence.json`
once the public release path is finalized.

Useful fields:

- `release.version_label`
- `release.tag`
- `release.snapshot_registry_id`
- `required_for_v0_1.local_validation_passed`
- `fresh_clone_validation_passed`
- `remote_ci_passed`
- `privacy_scan_passed`
- `public_urls_confirmed`
- `dataset_card_published`
- `zenodo_doi_minted`
- `arxiv_metadata_confirmed`
- `claim_matrix_updated`

This should not be hand-waved into truth. The file should stay blocked until
the evidence exists.

## What Not To Borrow

Do not borrow:

- Backend replay transcripts.
- Live target request-log correlation.
- Dockerized synthetic app families.
- Tool-agent submission schemas.
- Private route/decoy variant mechanics.
- False-positive leaderboard thresholds as written.

Those are correct for an authorization-agent benchmark. ObviousBench should
instead express analogous ideas in its own terms:

- answer derivation, ambiguity, and scorer-contract evidence
- prompt/scorer/split fingerprints
- provider-error and telemetry integrity gates
- held-out or trusted split governance
- static paper leaderboard now, hosted/live leaderboard later

## Suggested Implementation Order

### Phase 1: Docs-Only Governance

1. Add `docs/evidence-and-claims.md`.
2. Add `docs/reviews/external-review-packet.md` and
   `docs/reviews/external-review-summary.md`.
3. Link both from README and benchmark card.

This gives immediate public-communication value with low source-code risk.

### Phase 2: Snapshot Registry

1. Add a registry JSON for proof-point, paper-v1, pass-k, and historical
   snapshots.
2. Add a validator that checks paths, row counts, and current/stale labels.
3. Wire release config and public docs to the registry where practical.

This directly addresses the release-copy risk already visible in this repo.

### Phase 3: Fingerprints And Internal Item Review

1. Add comparison/report fingerprints.
2. Add an internal item review matrix generator.
3. Add tests for both.

This is more invasive but high-value for future private/trusted splits and
leaderboard governance.

### Phase 4: Public Artifact Wrapper

1. Add the validation wrapper.
2. Add expected output fixtures only where they are clone-depth safe.
3. Run it in CI or release preflight.

## Bottom Line

AuthZBench-SaaS is not a better version of ObviousBench; it is solving a
different benchmark problem. But it is a useful example of public benchmark
honesty. The most important idea to copy is not any one file. It is the habit of
turning claims into a validated evidence map, and treating stale/current,
public/private, diagnostic/leaderboard, and proof/claim boundaries as first
class release surfaces.
