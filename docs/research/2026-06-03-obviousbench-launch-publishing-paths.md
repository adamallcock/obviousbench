---
title: ObviousBench Launch Publishing Paths
date: 2026-06-03
type: research
status: draft
---

# ObviousBench Launch Publishing Paths

Live web research performed on 2026-06-03. This note compares launch and
publishing paths for ObviousBench as alternatives to, or complements of, a
formal arXiv paper. It is grounded in the current repo's paper-readiness
artifacts and does not change benchmark code.

## Repo Evidence Snapshot

Relevant local artifacts inspected:

- `docs/research/2026-06-01-obviousbench-arxiv-readiness-decision.md`
- `docs/research/2026-06-01-obviousbench-arxiv-completion-roadmap.md`
- `docs/research/2026-06-01-obviousbench-arxiv-blocker-dashboard.md`
- `docs/research/2026-06-01-obviousbench-arxiv-submission-checklist.md`
- `docs/research/2026-06-01-obviousbench-arxiv-submission-handoff.md`
- `docs/research/2026-06-01-obviousbench-public-release-artifact-audit.md`
- `docs/research/2026-06-01-obviousbench-public-release-decision-packet.md`
- `docs/research/2026-06-01-obviousbench-arxiv-submission-metadata.md`
- `docs/research/2026-06-03-opus-4-8-adaptive-thinking-diagnosis.md`
- `docs/research/2026-06-03-paper-v1-cost-integrity-audit.md`
- `paper/Makefile`
- `paper/main.pdf`
- `paper/arxiv-src.tar.gz`
- `docs/reports/2026-06-03-paper-v1-8x28-current-223-final/leaderboard.csv`

Current repo posture:

- The arXiv path is unusually mature: LaTeX source, PDF, source bundle,
  release metadata files, paper audits, and preflight machinery exist.
- Existing arXiv blockers are mostly release/identity/metadata decisions:
  final public links, author/title/abstract confirmation, and endorsement
  confirmation.
- `paper/Makefile` still points at the older
  `paper_v1_combined_234_overline_attempt_scored_20260602` evidence manifest,
  while the newest visible report path is
  `docs/reports/2026-06-03-paper-v1-8x28-current-223-final/`.
- The newest leaderboard file has 224 CSV lines including the header, which is
  223 model rows. Separate config text refers to a "224-question" effort-cost
  shape. Treat "224" carefully in launch copy: verify whether it refers to item
  count, model-row count, or rerun scope before public claims.
- The Opus 4.8 adaptive-thinking diagnosis says the old thinking/cost curves
  should not be published without repricing/reinstrumentation; any launch should
  avoid Anthropic reasoning-token claims unless the fixed regenerated artifacts
  are the selected release snapshot.

## Recommendation

Use a layered launch, not a single channel.

Best near-term path:

1. Publish a technical report and artifact release first: public GitHub repo,
   project page, Hugging Face dataset card, GitHub release, Zenodo DOI, and a
   concise launch essay. This gives credible, citable, inspectable artifacts
   even if arXiv endorsement or moderation takes longer than expected.
2. Submit arXiv as soon as the release URLs are live and metadata is confirmed.
   arXiv should become the canonical scholarly paper once accepted/announced,
   but it should not be the only launch dependency.
3. After the arXiv ID exists, link the paper into Hugging Face Paper Pages and
   Papers with Code. Papers with Code explicitly requires a preprint,
   conference paper, or journal paper for benchmark results, so arXiv unlocks
   that path.
4. Defer a public submission leaderboard until the governance story is stronger:
   hidden/test split policy, model submission rules, refresh cadence, anti-
   overfitting posture, and provider-cost handling. A static "paper snapshot"
   leaderboard is safe now; a live submission leaderboard is v0.2+.

This sequence gives ObviousBench credibility in three layers:

- artifact credibility: code/data/reports are visible and versioned;
- scholarly credibility: arXiv paper and, later, workshop/OpenReview review;
- ecosystem credibility: Hugging Face/Papers with Code/leaderboard surfaces.

## Channel Comparison

| Channel | Use for ObviousBench | Readiness | Requirements / evidence | Risks | Recommendation |
| --- | --- | --- | --- | --- | --- |
| arXiv preprint | Scholarly anchor for benchmark methodology and results. | High, but blocked on metadata and release confirmation. | arXiv wants registered authors, topical/refereeable scientific work, license grant, accepted formats, metadata, and moderation. TeX is preferred, figures must be included, and first/new-category submissions may need endorsement. Sources: [submission overview](https://info.arxiv.org/help/submit/index.html), [availability schedule](https://info.arxiv.org/help/availability.html), [endorsement](https://info.arxiv.org/help/endorsement.html), [metadata](https://info.arxiv.org/help/prep.html), [licenses](https://info.arxiv.org/help/license/index.html), [category taxonomy](https://arxiv.org/category_taxonomy). | Endorsement delay; moderation delay; current artifact-count mismatch; stale paper Makefile evidence target. | Do it, but do not make it the only launch route. |
| Technical report on project site / GitHub | Fastest credible public narrative, with full artifacts. | High. | GitHub Pages can host a project site directly from a repository and publish static HTML/CSS/JS. Source: [GitHub Pages docs](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages). | Less scholarly than arXiv; needs careful citation/claim framing. | Launch this first or same day as arXiv submission. |
| GitHub release | Versioned code/data snapshot and release notes. | High. | GitHub releases are based on tags and package software for public use; GitHub auto-includes source archives. Source: [GitHub Releases docs](https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases). | Public repo scrub must be real; release asset sprawl can confuse readers. | Required for first launch. Use a clean `v0.1.0-paper-v1` release. |
| Zenodo DOI | Citable archival snapshot. | High once public release exists. | GitHub says Zenodo can archive public repositories and issue DOIs; Zenodo says connected GitHub releases are ingested and archived, and `.zenodo.json` can provide release metadata. Sources: [GitHub citation docs](https://docs.github.com/articles/referencing-and-citing-content), [Zenodo enable repository](https://help.zenodo.org/docs/github/enable-repository/), [Zenodo archive release](https://help.zenodo.org/docs/github/archive-software/github-upload/), [Zenodo JSON](https://help.zenodo.org/docs/github/describe-software/zenodo-json/). | DOI appears after release processing; `.zenodo.json` overrides `CITATION.cff` metadata. | Required. Mint after GitHub release, then add DOI to site/arXiv comments if timing allows. |
| Hugging Face dataset repo | Dataset distribution, discoverability, viewer, dataset card. | High. | Dataset repos render `README.md` as a dataset card; YAML metadata controls license/tags/discovery; dataset cards should document contents, biases, and use context. Source: [Hugging Face Dataset Cards](https://huggingface.co/docs/hub/datasets-cards). | Dataset-card quality matters; private/generated source leakage risk; license scope must be explicit. | Required for AI-benchmark launch. Publish reviewed `paper_v1` data and, if appropriate, separate public/proof splits. |
| Hugging Face Paper Page | Connect paper, dataset, and discussion once arXiv ID exists. | Medium before arXiv, high after arXiv. | HF Paper Pages link artifacts to papers; if repo cards include an HF/arXiv paper link, Hub extracts the arXiv ID; authors can claim authorship. Source: [HF Paper Pages](https://huggingface.co/docs/hub/en/paper-pages). | Mostly arXiv-dependent; indexing can lag. | Do immediately after arXiv ID is public. |
| Papers with Code | Benchmark/task/dataset listing and result table. | Medium; arXiv is gating. | PWC says anyone can contribute via edit buttons, but benchmark results require the paper to be published as a preprint, conference paper, or journal paper; code is encouraged but not required. Source: [Papers with Code About](https://paperswithcode.com/about). | Taxonomy fit may be awkward; edits monitored; weak if only a technical report exists. | Add after arXiv announcement. Use as ecosystem indexing, not primary launch. |
| Blog post / essay | Accessible launch story, examples, lessons, and caveats. | High. | No formal gate. Should link to the release, dataset card, report, and eventual arXiv ID. | Easy to overclaim; not archival. | Strong complement. Publish same day as artifacts, then update with arXiv ID. |
| Benchmark leaderboard site | Static leaderboard now; live submission leaderboard later. | Static: high. Live: medium/low. | HF leaderboard templates use a frontend Space, request dataset, results dataset, and optional backend Space; HF Spaces host apps; EvalAI supports hosted challenge submissions/leaderboards; Kaggle competitions provide hosted real-time leaderboards/scoring. Sources: [HF Leaderboards](https://huggingface.co/docs/leaderboards/main/leaderboards/building_page), [HF Spaces](https://huggingface.co/docs/hub/main/spaces), [EvalAI host challenge](https://evalai-develop-copy.readthedocs.io/en/latest/host_challenge.html), [Kaggle host competitions](https://www.kaggle.com/c/about/host). | Live leaderboard invites gaming and hidden-set governance problems; provider API cost and model-version drift need policy. | Ship static paper leaderboard first. Design live submissions as a separate v0.2 project. |
| OpenReview / workshop | Peer-review signal and feedback loop. | Low for immediate launch; medium as follow-up. | OpenReview is venue-driven; current public OpenReview page lists open venues and deadlines, and docs show venue-specific submission/revision/public-reader controls. Sources: [OpenReview venues](https://openreview.net/), [submission revision stage](https://docs.openreview.net/reference/stages/submission-revision-stage), [making submissions available](https://docs.openreview.net/how-to-guides/workflow/how-to-make-submissions-available-before-the-submission-deadline). | Deadlines, anonymity, prior-publication, and formatting vary by workshop/conference. arXiv-before-workshop can be fine for many venues but must be checked per venue. | Treat as a second wave after public artifacts. Target benchmark/dataset/evaluation workshops. |
| Social launch | Distribution and recruiting signal. | High once artifacts are live. | No formal gate; should link to stable artifacts and avoid unsupported claims. | Social posts amplify mistakes; need one canonical URL and caveat discipline. | Use after public repo/HF/report are live; amplify again after arXiv ID. |
| Semantic Scholar / Google Scholar indexing | Passive discovery. | Low-control. | Usually follows arXiv/DOI/web indexing. | Cannot be forced reliably on launch day. | Do not plan around it. |
| Kaggle benchmark / competition | Community competition or benchmark surface. | Medium as future channel. | Kaggle advertises data hosting, real-time leaderboards, preloaded metrics, forums, automated scoring, and notebooks for hosted competitions. Source: [Kaggle host page](https://www.kaggle.com/c/about/host). | ObviousBench may not fit classic predictive competition format; public/private split design needed. | Consider only after a hidden or private eval split exists. |

## arXiv Route Timeline From Current Repo State

Assumptions:

- No new model reruns are intentionally started for the first public release.
- The selected public snapshot is either the older 234-row `paper/Makefile`
  evidence target or the newer 223-row/224-question rerun context, but not a
  vague mixture of both.
- Anthropic cost/thinking fixes are reflected in whichever snapshot is chosen.
- The submitter already has a registered arXiv account; endorsement status is
  unknown because repo metadata still has `endorsement_checked: false`.

### Fast Path: 2 to 5 calendar days to announcement

This is realistic only if endorsement is not required or is already satisfied.

Day 0.5: choose and freeze the release snapshot.

- Decide whether the arXiv paper uses the older 234-row evidence run or the
  newer 223-row/224-question rerun context.
- Update `paper/Makefile`, metadata abstract, tables, figures, report links,
  and release notes to match exactly one snapshot.
- Explicitly drop or caveat Anthropic reasoning-token curves unless fixed
  telemetry supports them.

Day 0.5 to 1.5: public artifact release.

- Scrub repo for private/generated/provider-sensitive material.
- Publish public GitHub repo.
- Publish Hugging Face dataset repo and dataset card.
- Create GitHub release and Zenodo archive/DOI.
- Confirm `CITATION.cff`, `.zenodo.json`, license files, README, benchmark card,
  dataset card, and report links.

Day 1 to 2: final paper package.

- Regenerate paper assets from the frozen snapshot.
- Rerun repo gates already represented by:
  `make -C paper readiness-preprint`, `result-artifacts`, `assets`, `claims`,
  `manuscript-completeness`, `report-tracker`, `blocker-dashboard`,
  `arxiv-package`, `arxiv-audit`, `release-audit`, `submission-handoff`,
  `preflight`, `internal-review`, and `repro-manifest`.
- Visually inspect `paper/main.pdf`.
- Confirm title, abstract, authors, category, license, release links, and
  AI-tool disclosure.

Day 2: submit before 14:00 US Eastern if possible.

- arXiv says submissions before the weekday 14:00 Eastern cutoff are generally
  announced at 20:00 Eastern on the corresponding announcement day, but QA and
  moderation can take one to four days or longer.
- arXiv IDs are assigned at announcement, not in advance.

Day 2 to 5: announcement and follow-through.

- When arXiv is public, update README/site/HF dataset card with the arXiv ID.
- Index or claim the Hugging Face Paper Page.
- Add Papers with Code task/dataset/result pages.
- Publish the social launch and/or short essay.

### Endorsement / Moderation Path: 1 to 3 weeks

If arXiv requires endorsement for `cs.CL` or the selected category:

- Start a new submission and select the category to trigger the endorsement
  flow.
- Use arXiv's endorsement process to identify a knowledgeable endorser from
  related recent papers or personal network.
- Send the intended manuscript plus public artifact links.
- Expect the critical path to be human response time, not repo work.

If moderation asks for changes:

- Preserve the frozen artifact snapshot.
- Revise claims/category/format as needed.
- Resubmit before announcement if the paper is still incomplete; otherwise
  submit a new version after announcement.

### Main Blockers To Clear

1. Evidence snapshot mismatch.

   The paper Makefile targets 234 rows from 2026-06-02, while the latest visible
   report is 223 rows from 2026-06-03 and nearby config mentions a 224-question
   shape. A launch can be credible with either snapshot, but not with copy that
   mixes them.

2. Anthropic telemetry and cost language.

   The Opus 4.8 diagnosis says old Anthropic reasoning-token telemetry is not
   publishable as billed thinking, and old Opus cost was underpriced. Final
   public copy should use corrected cost artifacts and avoid unfixed reasoning
   curves.

3. Public release confirmation.

   Existing release audits are blocked only on confirmation fields, but those
   fields represent real work: live GitHub/HF/Zenodo URLs and final metadata
   consistency.

4. Endorsement status.

   Current metadata still has `endorsement_checked: false`. If endorsement is
   required, it dominates elapsed time.

5. Claim discipline.

   The accepted local arXiv readiness decision disallows broad claims: no global
   model ranking, no measured human baseline, no model-versus-human gap, no
   contamination-resistance claim for generated public data, and no causal claim
   about internal reasoning defects.

## Launch Pack Definition

Minimum credible launch pack:

- public GitHub repo with code, tests, benchmark card, methodology, scoring
  policy, source policy, and reproduction commands;
- `v0.1.0-paper-v1` GitHub release;
- Zenodo DOI for that release;
- Hugging Face dataset repo with dataset card, license metadata, task tags,
  intended-use limits, and exact split/version names;
- static project page or GitHub Pages site with report, failure gallery,
  leaderboard snapshot, caveats, and citation block;
- arXiv PDF/source bundle when ready;
- short launch essay/post pointing to the canonical project page;
- after arXiv announcement: HF Paper Page and Papers with Code entries.

Definition of done before public launch:

- one frozen snapshot selected and named consistently everywhere;
- no private provider logs, secrets, account IDs, or non-public source material
  in public release;
- public URLs verified live;
- release DOI minted or DOI creation explicitly noted as pending;
- paper/site/blog use the same title, abstract-ish summary, row counts, item
  counts, and claim limits;
- arXiv preflight either passes or is not represented as submitted-ready.

## Practical Order Of Operations

1. Freeze the chosen evidence snapshot and write a one-paragraph release claim.
2. Update the paper/report metadata to that snapshot.
3. Run local paper/release gates.
4. Publish GitHub + HF dataset + project page.
5. Create GitHub release and Zenodo DOI.
6. Submit arXiv.
7. When arXiv is announced, update links and index HF Paper Page / Papers with
   Code.
8. Publish social launch and blog/essay.
9. Scope the live leaderboard as a v0.2 project only after hidden-set and
   submission governance are written.
