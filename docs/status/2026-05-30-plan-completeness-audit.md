---
title: ObviousBench Plan Completeness Audit
date: 2026-05-30
type: review
status: conditional
---

# ObviousBench Plan Completeness Audit

> Snapshot note: this audit reflects the 2026-05-30 worktree. Dataset counts,
> implemented modules, and report capabilities have changed since then. Use
> `docs/architecture/2026-05-31-current-architecture.md` for the current system
> map and this file for historical plan-completion evidence.

This audit compares the current worktree against
`docs/superpowers/plans/2026-05-30-obviousbench-v0-1-implementation.md`.

## Bottom Line

The codebase has a working local ObviousBench v0.1 infrastructure slice:

- installable package
- local JSONL datasets
- validators
- deterministic scorers
- Inspect task wiring
- generated v0 seed dataset
- mock and OpenAI smoke eval paths
- summary CSV and failure-gallery generation
- core docs

It does **not** yet have a fully researched, item-by-item online-sourced
benchmark corpus, a 5-8 model run, human validation, or v1 decision records.

## How To Run It

Use `docs/runbook.md`.

## Plan Alignment

| Area | Status | Evidence | Gap |
| --- | --- | --- | --- |
| Product identity | Complete | `README.md`, `docs/benchmark_card.md`, `docs/branding.md` | None found |
| Scope boundary | Complete | No hosted app, no dashboard, no LLM judge | None found |
| Installable package | Complete | `pyproject.toml`, import, tests | None found |
| Dataset schema/loading/validation | Complete | `obviousbench/datasets/`, validation passing | Source catalog validation is schema-only |
| Prompt rendering | Complete | `obviousbench/prompts.py`, tests | None found |
| Scorer registry/kernel | Mostly complete | `obviousbench/scorers/`, tests | Some scorer behaviors remain minimally tested |
| Inspect task definitions | Complete for v0 families | `obviousbench/tasks/`, mock/OpenAI smoke evals | Full-family eval not yet run |
| Dataset generation | Partial | `scripts/generate_public_v0.py`, 318 items | Dataset is generated variants, not mined examples |
| Source catalog | Partial | 25 records in `data/source_catalog/sources_v0.jsonl`; 11 Grok-mined candidates in `data/source_catalog/candidates_grok_2026-05-30.jsonl` | Canonical records are still leads/archetypes; Grok candidates need promotion review |
| Analysis/reporting | Partial | CLI writes summary CSV and failure gallery | Per-family CSV/table export is not rich; failure ranking is basic |
| Run config/CLI | Partial | `obviousbench validate`, `obviousbench summarize`, configs | Config parsing/unknown-key rejection not implemented |
| Public docs | Partial | README and docs exist | Needed a runbook; added in this audit |
| Privacy/result safety | Mostly complete | `.gitignore`, `git check-ignore` evidence | Path traversal hardening for gallery output is not explicitly tested |
| Milestone 0 | Complete | package, smoke dataset, scorer, docs, tests | None found |
| Milestone 1 | Partial | 25 source records | Source research depth is weak |
| Milestone 2 | Partial | 318 validated items across 8 families | Review labels are programmatic, not human review |
| Milestone 3 | Partial | mock + `openai/gpt-4.1` smoke run | Not 5-8 models |
| Milestone 4 | Partial | docs and local reproduction path | Public result artifact not promoted |
| Milestone 5 | Not complete | No decision records | v1 planning not done |

## Verification Evidence

Commands run successfully in the current worktree:

```bash
.venv/bin/python -m pytest tests -q
.venv/bin/python -m ruff check .
.venv/bin/python -m compileall obviousbench
.venv/bin/python scripts/validate_dataset.py data/public_v0/*.jsonl data/calibration_v0/smoke_test.jsonl
.venv/bin/inspect eval obviousbench/tasks/smoke.py --model mockllm/model --log-dir results/raw --limit 3 --no-log-realtime
.venv/bin/obviousbench summarize --logs results/raw --out results/summaries
```

Observed:

```text
53 tests passed
ruff passed
compileall passed
dataset validation passed
mock smoke eval passed
summary/failure gallery generated
```

The worktree also contains a prior OpenAI smoke log:

```text
model: openai/gpt-4.1
task: smoke
samples: 3
status: success
scores: 3 correct, 0 failures
```

## Dataset Provenance Audit

Current public v0 data:

```text
318 total rows
316 generated_variant
2 public_archetype
```

The source catalog records archetype leads. It should not be represented as
318 independent online findings.

Additional mining performed on 2026-05-30:

```text
11 Grok-mined candidate rows
6 independently opened
2 search unconfirmed
1 source blocked by robots
1 source paywalled
1 X shell opened with no content
```

Research artifact:

```text
docs/research/2026-05-30-grok-public-failure-leads.md
```

## Issues Found

### High: Previous completion claim overstated the dataset maturity

The implementation created a generated seed dataset. It did not mine and review
318 real online examples.

Recommendation: describe this as "generated v0 seed data inspired by source
archetypes" until a source-mining/review workflow exists.

### Medium: Plan checklist was marked complete too broadly

Module code exists, but milestone-level acceptance criteria remain partial.

Recommendation: use this audit as the authoritative completion state instead of
the checkbox section alone.

### Medium: Config parsing requirements are not implemented

The plan says config parsing should reject unknown top-level keys. The repo has
example YAML configs, but no parser/validator for them.

Recommendation: either implement config parsing or downgrade that requirement.

### Medium: Source catalog validation is incomplete

`SourceRecord` parses records, but there is no dedicated
`obviousbench/sources/validation.py` implementation or CLI command.

Recommendation: add source validation before calling Milestone 1 complete.

### Medium: Grok-mined leads are useful but not canonical evidence

Grok found 11 structured public-source leads, but the search pass surfaced
blocked, paywalled, duplicate, and unconfirmed links. These are now preserved as
candidate records, not appended directly to the canonical catalog.

Recommendation: independently verify and reproduce each promoted source before
adding it to `sources_v0.jsonl` or using it as proof for a benchmark item.

### Low: Analysis is useful but not full public reporting

The summary CSV is global by model. Per-family tables and gallery ranking are
basic.

Recommendation: expand analysis before public prototype release.

## Verdict

Conditional pass for runnable v0.1 infrastructure.

Fail for "entire plan complete" if that means all milestones, full curation,
full model panel, and v1 planning.
