---
title: ObviousBench v0.1 Implementation Plan
date: 2026-05-30
type: plan
status: conditional
---

# ObviousBench v0.1 Implementation Plan

> **Audit correction:** The local infrastructure modules are implemented, but
> the full plan is not complete across all milestones. The current authoritative
> completion audit is
> `docs/status/2026-05-30-plan-completeness-audit.md`.

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** Build ObviousBench v0.1 as a small, credible Inspect AI benchmark for short, human-trivial, public-facing model failures, with local JSONL datasets, deterministic scorers, reproducible runs, summaries, and a failure gallery.

**Architecture:** Inspect AI owns execution, provider integration, and eval logs; ObviousBench owns the dataset contract, deterministic scoring policy, dataset generation, validation, and reporting. The first implementation should prove one end-to-end path with a smoke dataset before broadening to all v0 task families.

**Tech Stack:** Python 3.11+, Inspect AI, Pydantic, pytest, ruff, local JSONL, YAML run configs, CSV/Markdown reporting.

---

## Deep Reading Summary

The source plan is not asking for a benchmark platform. It asks for a clean v0.1 repo that can be cloned, run locally with Inspect AI, and used to produce obvious failure rates, per-family summaries, raw logs, and a failure gallery.

The implementation should optimize for trust:

- Keep v0 narrow: native provider mode, no explicit system prompt, local JSONL, deterministic scorers, no leaderboard, no Hugging Face, no OpenAI Evals adapter.
- Treat viral examples as source leads and archetypes, not unquestioned benchmark items.
- Make curation and review metadata part of the data model from the beginning.
- Keep scorer behavior transparent enough that a skeptical reader can inspect false positives and false negatives.
- Make the failure gallery a first-class output, not a later marketing task.

## Verified Inspect Assumptions

Checked against the current Inspect documentation on 2026-05-30:

- Inspect tasks are defined as a dataset plus solver plus scorer returned by an `@task` function.
- JSON/JSONL datasets can be mapped with `FieldSpec`, including sample `id`, `input`, `target`, and `metadata`.
- Custom scorers should return `Score` objects and should include extracted `answer` plus `explanation` when practical, because this makes log review and scorer debugging much better.
- Inspect logs are usable both through `inspect view` and programmatic log APIs; ObviousBench reporting should build on those logs instead of inventing a parallel run format.

Primary docs:

- https://inspect.aisi.org.uk/tasks.html
- https://inspect.aisi.org.uk/datasets.html
- https://inspect.aisi.org.uk/scorers.html
- https://inspect.aisi.org.uk/log-viewer.html
- https://inspect.aisi.org.uk/eval-logs.html

## Implementation Principles

1. Build the benchmark around contracts before volume.
2. Make every generated example reproducible from generator metadata.
3. Keep extraction and strict-format scoring separate.
4. Store failure typing in scorer metadata, not only in downstream analysis.
5. Make validation cheap enough to run before every benchmark run.
6. Do not commit raw model outputs or generated results until `.gitignore` and result policy are in place.
7. Prefer package entry points and documented CLI commands over hidden scripts.

## Product Requirements

### PR-001: Public Benchmark Identity

ObviousBench must present itself as a reliability and preflight benchmark for public-facing AI systems, not as a shame or gotcha project.

**Functional requirements:**

- README, benchmark card, methodology, source policy, and failure-gallery prose must use the name `ObviousBench`.
- Public-facing docs must include the thesis: `Catch obvious AI mistakes before users do.`
- Public-facing docs must say the benchmark covers short, human-trivial tasks such as character counting, spelling transforms, simple arithmetic, list counting, ordering, format compliance, negation, and simple constraint awareness.
- Public-facing docs must state that ObviousBench does not measure general intelligence, safety, long-context ability, RAG quality, tool use, or expert knowledge.

**Acceptance criteria:**

- `rg -n "shame|humiliation|dumb AI|gotcha" README.md docs obviousbench` returns no public-facing framing unless the phrase appears in a "do not use" guidance section.
- README opening includes the constructive preflight thesis and the Inspect/local JSONL/deterministic scorer architecture in the first 250 words.
- `docs/benchmark_card.md` includes "What this measures" and "What this does not measure" sections.
- A reviewer can read README plus `docs/methodology.md` and explain why the benchmark is narrow, deterministic, and constructive.

### PR-002: V0.1 Scope Boundary

The first implementation must prove a credible local benchmark, not a hosted benchmark platform.

**Functional requirements:**

- V0.1 must support local JSONL datasets.
- V0.1 must support Inspect AI as the only runner.
- V0.1 must support native provider mode with no explicit system prompt.
- V0.1 must support deterministic scorers only.
- V0.1 must support local raw logs, summary CSV, and failure-gallery Markdown.
- V0.1 must not include a hosted leaderboard, user accounts, a web dashboard, Hugging Face hosting, OpenAI Evals compatibility, LLM-as-judge scoring, multi-turn evals, RAG evals, tool-use evals, or long-context evals.

**Acceptance criteria:**

- No package imports or docs require a web server, database, cloud storage bucket, hosted queue, browser automation, or external dashboard.
- `pyproject.toml` dependencies remain limited to Inspect/runtime support, schema validation, YAML parsing, test tools, and lint tools unless a new dependency is justified in this plan.
- There is no code path that calls another LLM to score model outputs.
- The documented smoke path runs from local files and writes local logs only.

### PR-003: User Workflows

V0.1 must support four core local workflows: validate, evaluate, summarize, and inspect failures.

**Functional requirements:**

- A user can validate one or more JSONL datasets before running an eval.
- A user can run an Inspect task over the smoke dataset.
- A user can summarize Inspect logs into obvious failure rate, accuracy, failures per 1,000, and per-family breakdowns.
- A user can build a failure-gallery Markdown artifact from Inspect logs.
- A user can inspect scorer decisions for individual samples without reading provider-specific log internals.

**Acceptance criteria:**

- `python scripts/validate_dataset.py data/calibration_v0/smoke_test.jsonl` exits `0` for a valid smoke dataset and prints `Validation passed.`
- The same validation command exits nonzero and prints file path, line number, field name, and reason for an invalid JSONL fixture.
- `inspect eval obviousbench/smoke --model <provider/model> --log-dir results/raw` is documented and does not require code edits.
- `obviousbench summarize --logs results/raw --out results/summaries` writes a CSV summary and a Markdown failure gallery when given a supported Inspect log fixture.
- Unit tests cover the CLI paths without making model calls.

## Functional Requirements

### FR-001: Installable Python Package

ObviousBench must be installable in editable mode and expose package modules, scripts, and Inspect task registration.

**Requirements:**

- Package name: `obviousbench`.
- Python version: `>=3.11`.
- Runtime dependencies: `inspect-ai`, `pydantic`, `pyyaml`.
- Dev dependencies: `pytest`, `ruff`.
- Console entry point: `obviousbench = obviousbench.cli:main`.
- Inspect entry point: `obviousbench = obviousbench._registry`.

**Acceptance criteria:**

- `python -m pip install -e ".[dev]"` succeeds in a clean virtual environment.
- `python -c "import obviousbench; print(obviousbench.__version__)"` prints `0.1.0`.
- `python -m compileall obviousbench` succeeds.
- `python -m ruff check .` succeeds.
- `python -m pytest` succeeds without provider credentials.

### FR-002: Dataset Item Validation

Every benchmark item must be validated before use.

**Requirements:**

- Each line of a dataset file is one complete JSON object.
- Required top-level fields: `id`, `family`, `subfamily`, `prompt`, `question`, `target`, `answer_type`, `scorer`, `split`, `source_type`, `source_refs`, `human_triviality`, `review_status`, `metadata`.
- Required metadata fields: `prompt_template_id` and `system_prompt`.
- `system_prompt` must be `null` for v0 unless a provider requires a system field at execution time; provider-required defaults must be recorded in run metadata, not embedded in dataset items.
- Dataset validation must reject invalid JSON, missing fields, unknown enum values, duplicate IDs, unreviewed public items, `H3` items, unknown scorer names, and unknown prompt template IDs.

**Acceptance criteria:**

- A complete sample matching `obviousbench.char_count.en.v0.public.000001` parses successfully.
- A sample missing `metadata.prompt_template_id` fails with a precise validation issue.
- A sample with `human_triviality: "H3"` in `public_v0` fails validation.
- Duplicate IDs across two dataset paths fail validation and identify both locations.
- Validation never silently drops invalid rows.

### FR-003: Source Catalog Validation

Public examples must be treated as leads and archetypes, with enough metadata to preserve provenance without republishing sensitive or copyrighted material.

**Requirements:**

- Source catalog records must include `source_id`, `platform`, `url`, `date_seen`, `original_prompt`, `claimed_model`, `claimed_output`, `failure_description`, `engagement_signal`, `media_type`, `rights_status`, and `notes`.
- `rights_status` must distinguish link-only, paraphrase-only, permissioned, public-domain, and internal-only sources.
- Source records must not require private author names or handles.
- Dataset items may reference source IDs through `source_refs`.
- Source validation must report broken JSON, missing source IDs, duplicate source IDs, invalid URLs, invalid dates, and unsupported rights statuses.

**Acceptance criteria:**

- `data/source_catalog/sources_v0.jsonl` validates with at least 25 records before public v0 publication.
- `docs/source_archetypes_v0.md` summarizes source archetypes without embedding screenshots.
- Public dataset records reference source IDs that exist in `sources_v0.jsonl`.
- No validation fixture or committed source catalog record contains credentials, private account IDs, private email addresses, or copied screenshot text beyond short prompt/output snippets needed for reproducibility.

### FR-004: Prompt Rendering

Prompt rendering must be centralized so prompt-policy drift is visible and testable.

**Requirements:**

- `final_answer_only_v0` must render exactly:

```text
Answer the question. Return only the final answer, with no explanation.

Question: {question}
Answer:
```

- `multiple_choice_letter_v0` must render exactly:

```text
Answer the question. Return only the letter of the correct option.

Question: {question}

A. {choice_a}
B. {choice_b}
C. {choice_c}
D. {choice_d}

Answer:
```

- V0 prompt renderers must not add a system prompt, chain-of-thought instruction, "be careful" language, or hints that the question is tricky.
- Rendered prompts must be deterministic for the same item.

**Acceptance criteria:**

- Prompt tests compare full strings, including blank lines.
- Unknown prompt template IDs raise a clear exception and fail validation.
- Multiple-choice prompt rendering rejects fewer than four choices, more than four choices, blank choices, and non-string choices.
- A dataset item's stored `prompt` matches re-rendering from `question`, `metadata.prompt_template_id`, and `metadata.choices` when choices are present.

### FR-005: Inspect Sample Conversion

Dataset items must convert into Inspect samples without losing benchmark metadata.

**Requirements:**

- Inspect sample `id` must equal benchmark item `id`.
- Inspect sample `input` must equal benchmark item `prompt`.
- Inspect sample `target` must equal benchmark item `target`.
- Inspect sample `metadata` must include `family`, `subfamily`, `answer_type`, `scorer`, `split`, `source_type`, `source_refs`, `human_triviality`, `review_status`, and the nested benchmark `metadata`.

**Acceptance criteria:**

- Loader tests assert exact sample `id`, `input`, `target`, and representative metadata values.
- Loading preserves item order from JSONL.
- Loading a missing file fails with a path-specific error.
- Loading an empty file fails unless the caller explicitly requests empty-file tolerance for tests.

### FR-006: Deterministic Scorer Registry

Every scorer referenced by a dataset item must resolve through one local registry.

**Requirements:**

- Registry function: `get_scorer(name: str) -> inspect_ai.scorer.Scorer`.
- Supported v0 scorer names:
  - `exact_integer_extract_first_v0`
  - `exact_string_trim_v0`
  - `normalized_string_v0`
  - `normalized_list_v0`
  - `multiple_choice_letter_v0`
  - `regex_match_v0`
  - `json_exact_field_v0`
  - `word_count_v0`
- Unknown scorer names must fail fast before an Inspect eval starts.

**Acceptance criteria:**

- Validation rejects every unknown scorer name.
- `get_scorer()` returns callable Inspect scorers for every supported scorer name.
- Registry tests assert that all scorer names in schema enums resolve.
- No scorer calls an LLM, network API, browser, or subprocess.

### FR-007: Scorer Output Contract

Scorers must return enough structured information for debugging and reporting.

**Requirements:**

- Each scorer returns Inspect `Score` with correct/incorrect value.
- Each scorer sets `answer` to the extracted answer or `None`.
- Each scorer sets `explanation` to a short human-readable description that includes the raw model output or a summarized parse error.
- Each scorer sets metadata with at least `failure_type`, `scorer_name`, and `strict_format`.
- Failure types must be drawn from the stable taxonomy in this plan.

**Acceptance criteria:**

- Correct answers produce `failure_type: null` or `failure_type: "none"`, consistently across all scorers.
- Incorrect count answers produce `incorrect_count`.
- Verbose outputs in strict format tasks produce `verbose_noncompliance`.
- Empty outputs produce `non_answer`.
- Malformed JSON for `json_exact_field_v0` produces `json_malformed`.
- Ambiguous outputs with multiple conflicting candidate answers produce `ambiguous_output`.

### FR-008: Inspect Task Definitions

Tasks must be thin wrappers over local datasets and local scorer selection.

**Requirements:**

- Shared task factory accepts dataset path, task name, and scorer selection.
- Each task uses `generate()` as solver.
- Tasks do not define a system prompt.
- Task modules exist for all v0 families.
- A smoke task loads `data/calibration_v0/smoke_test.jsonl`.

**Acceptance criteria:**

- Task construction tests instantiate each task without provider credentials.
- The smoke task loads 10-20 samples.
- Each family task points at the matching `data/public_v0/<family>.jsonl` path by default.
- A missing dataset path fails before any model call.

### FR-009: Dataset Generation

Generated variants must be reproducible, reviewable, and traceable.

**Requirements:**

- Generators must be deterministic for the same generator version, seed, and source inputs.
- Generated items must include `metadata.generated: true`, `metadata.generator`, `metadata.seed`, and `metadata.variant_of` when applicable.
- Hand-authored seed items must include `metadata.generated: false`.
- Generated item IDs must be stable and monotonically numbered within family/split.
- Generators must avoid ambiguous examples and must not produce duplicate questions within a split.

**Acceptance criteria:**

- Running `python scripts/generate_public_v0.py --seed 98231 --dry-run` twice produces byte-identical output.
- Generator tests assert exact targets for `strawberry`, `mississippi`, `bookkeeper`, representative spelling transforms, representative arithmetic examples, and representative ordering examples.
- Generated public datasets validate with the same validator used for hand-authored items.
- Generator output never overwrites existing dataset files unless `--write` is provided.

### FR-010: Analysis And Metrics

Analysis must turn Inspect logs into stable metrics aligned with the benchmark thesis.

**Requirements:**

- Primary metric: `obvious_failure_rate = failures / scored_questions`.
- Secondary metrics: accuracy, failures per 1,000, per-family failure rate, format failure count/rate, refusal/non-answer count/rate, verbose noncompliance count/rate, public-archetype versus generated-variant failure rate.
- Provider errors and timeouts must be counted separately from scored failures.
- Analysis must preserve model/provider string exactly as recorded in the Inspect log.
- Analysis must preserve sample IDs so failures can be traced back to dataset rows.

**Acceptance criteria:**

- A fixture with 8 scored samples and 2 failures reports `obvious_failure_rate = 0.25` and `failures_per_1000 = 250`.
- Provider errors do not inflate accuracy or obvious failure rate denominators unless a documented `--count-provider-errors` mode is explicitly selected.
- Per-family metrics sum to the global scored sample count.
- Summary CSV includes columns: `model`, `total_samples`, `scored_samples`, `correct`, `failures`, `obvious_failure_rate`, `accuracy`, `failures_per_1000`, `provider_errors`, `timeouts`, `non_answers`, `format_failures`.

### FR-011: Failure Gallery

The failure gallery must be a shareable, reviewable artifact that explains why failures matter.

**Requirements:**

- Gallery entries must include model, task family, sample ID, question, expected answer, extracted answer, raw model answer, failure type, human-triviality label, source type, and why humans find it obvious.
- Gallery generation must support a `limit` parameter.
- Gallery ordering must prioritize high-legibility failures, then H0 samples, then stable sample ID order.
- Gallery output must be Markdown.

**Acceptance criteria:**

- A fixture log with two failures produces exactly two gallery entries when `limit=10`.
- A fixture log with two failures produces exactly one gallery entry when `limit=1`.
- Gallery entries do not include hidden chain-of-thought, API keys, environment variables, or provider request headers.
- Gallery tests compare stable Markdown output against expected text.

### FR-012: Documentation

Documentation must make reproduction possible without reading the source plan.

**Requirements:**

- README must include install, validate, smoke run, summarize, and inspect-log commands.
- `docs/methodology.md` must describe dataset lifecycle, review, generated variants, and metric definitions.
- `docs/prompt_policy.md` must state native provider mode, no explicit system prompt, temperature `0` or provider equivalent, no tool use, and no web browsing.
- `docs/scoring_policy.md` must describe strict versus lenient scoring and every scorer in the registry.
- `docs/source_policy.md` must describe source discovery, rights handling, privacy, screenshots, and attribution.
- `docs/benchmark_card.md` must summarize intended use, limitations, dataset version, task families, and known risks.

**Acceptance criteria:**

- Every command in README either runs locally without credentials or is clearly marked as requiring provider credentials.
- Docs use exact dates for versioned benchmark claims.
- Docs avoid naming exact current flagship model names unless copied from a concrete run artifact.
- Docs include a concise "v0 non-goals" section.

### FR-013: Privacy And Result Safety

The repository must protect local secrets, raw provider logs, and sensitive source material.

**Requirements:**

- `.gitignore` must exclude local env files, raw result logs, summaries, failure-gallery outputs, Python caches, and build artifacts.
- Committed source records must not include raw credentials, auth codes, private email addresses, private account IDs, or private balances.
- Public docs must not include copied screenshots unless permission and licensing are recorded.
- Failure-gallery generation must not write files outside the requested output directory.

**Acceptance criteria:**

- `git check-ignore -v .env results/raw/example.eval results/summaries/example.csv results/failure_gallery/example.md` confirms all representative generated/private outputs are ignored.
- Tests cover output path normalization for analysis and gallery writing.
- A pre-publication review checklist in `docs/source_policy.md` includes secrets, screenshots, private handles, and raw provider logs.

## Technical Requirements

### TR-001: Code Organization

**Requirements:**

- Keep modules small and responsibility-focused.
- Dataset schema and validation live under `obviousbench/datasets/`.
- Scorers live under `obviousbench/scorers/`.
- Inspect tasks live under `obviousbench/tasks/`.
- Generators live under `obviousbench/generators/`.
- Analysis lives under `obviousbench/analysis/`.
- Source-catalog utilities live under `obviousbench/sources/`.
- CLI orchestration lives in `obviousbench/cli.py`.

**Acceptance criteria:**

- No single Python module exceeds 450 lines before tests unless reviewed and split is explicitly rejected in the plan.
- Task modules contain task wiring only; scorer logic is not duplicated in task modules.
- Generator modules do not import Inspect.
- Scorer modules do not import dataset generators.

### TR-002: Determinism

**Requirements:**

- Dataset generation must use local seeded random instances rather than global random state.
- Output ordering must be stable.
- JSONL writing must use UTF-8 and deterministic key ordering.
- Summary CSV ordering must be stable by model then task family or explicit sort key.

**Acceptance criteria:**

- Running generator tests twice produces identical expected outputs.
- Running analysis over the same fixture twice produces byte-identical CSV and Markdown.
- No implementation uses current wall-clock time in generated IDs or metric outputs, except docs and manually versioned files.

### TR-003: Error Handling

**Requirements:**

- Validation errors must be structured and include file path, line number when available, field path when available, code, and message.
- CLI errors must be concise and actionable.
- Library functions must raise typed exceptions or return structured reports; they must not print during normal operation.
- Scripts and CLI commands must set nonzero exit codes on failed validation, missing input files, unsupported scorer names, malformed configs, and unsupported log formats.

**Acceptance criteria:**

- Tests assert nonzero exit for invalid validation fixtures.
- Tests assert the error message includes the invalid field name.
- Library tests assert validation functions can be called without writing to stdout.

### TR-004: Testing Boundaries

**Requirements:**

- Unit tests must not call model providers.
- Unit tests must not require network access.
- Tests must cover validators, prompt rendering, scorer edge cases, task construction, generator determinism, analysis metrics, failure-gallery output, and CLI failure paths.
- Any integration test that calls a provider must be opt-in and skipped by default.

**Acceptance criteria:**

- `python -m pytest` passes without provider credentials and without network access.
- Provider-backed tests are marked with a dedicated pytest marker such as `provider`.
- `pytest.ini` or `pyproject.toml` registers any custom markers.

### TR-005: Configuration

**Requirements:**

- Example model config must use placeholder categories, not stale claims about current flagship models.
- Run config must capture dataset split, task family list, log directory, summary output directory, prompt policy ID, and scoring policy version.
- Config parsing must reject unknown top-level keys.

**Acceptance criteria:**

- `configs/models_v0.example.yaml` can be copied to a local config without editing source code.
- Config tests reject an unknown key such as `leaderboard_url`.
- Docs explain that exact model strings belong to run configs and run artifacts, not the benchmark spec.

### TR-006: Performance And Scale

**Requirements:**

- Validation and analysis must run in linear time over rows/samples.
- JSONL loading should stream records for validation; task loading may materialize lists for Inspect sample creation.
- Scorer functions must avoid expensive regex backtracking and unbounded parsing.
- V0 public dataset size target is 300-500 items; implementation should comfortably validate and analyze 2,000 items for v1 planning.

**Acceptance criteria:**

- Validation of a generated 2,000-line local fixture completes in under 2 seconds on a normal laptop when run outside CI noise.
- Scorer unit tests include a long malformed string fixture and complete quickly.
- Analysis over a 2,000-sample fixture completes without excessive memory growth or network calls.

### TR-007: Dependency Discipline

**Requirements:**

- Do not add a dependency when the standard library is sufficient for a simple, stable need.
- New runtime dependencies must be justified by a requirement in this plan.
- Test-only dependencies must live under the dev extra.
- No dependency may require a local database, browser, GUI, or hosted service for v0.1.

**Acceptance criteria:**

- `pyproject.toml` dependency list remains reviewable on one screen.
- Any added dependency has a comment or plan update explaining which requirement it satisfies.

## Data Contract Requirements

### Dataset Item Canonical Shape

Every dataset record must follow this shape:

```json
{
  "id": "obviousbench.char_count.en.v0.public.000001",
  "family": "character_count",
  "subfamily": "single_letter_count",
  "prompt": "Answer the question. Return only the final answer, with no explanation.\n\nQuestion: How many r's are in strawberry?\nAnswer:",
  "question": "How many r's are in strawberry?",
  "target": "3",
  "answer_type": "integer",
  "scorer": "exact_integer_extract_first_v0",
  "split": "public_v0",
  "source_type": "public_archetype",
  "source_refs": ["src_strawberry_public_discussion"],
  "human_triviality": "H0",
  "review_status": "reviewed",
  "metadata": {
    "word": "strawberry",
    "character": "r",
    "case_sensitive": false,
    "generated": false,
    "variant_of": null,
    "prompt_template_id": "final_answer_only_v0",
    "system_prompt": null
  }
}
```

**Acceptance criteria:**

- A fixture with this exact shape validates.
- A fixture where `target` is numeric instead of string fails with a field-type issue.
- A fixture where `source_refs` is an empty list fails for public splits.
- A fixture where `review_status` is not `reviewed` fails for public splits.

### Stable ID Format

IDs must follow:

```text
obviousbench.<family_short>.en.v0.<split_short>.<six_digit_index>
```

**Requirements:**

- `family_short` must be stable and documented for every family.
- `split_short` must distinguish public, calibration, private, and retired if those splits are introduced.
- Numeric suffix must be zero-padded to six digits.
- IDs must never be reused for semantically different items.

**Acceptance criteria:**

- ID parser tests accept `obviousbench.char_count.en.v0.public.000001`.
- ID parser tests reject missing prefix, unknown family short name, non-English language code for v0, non-v0 version, unknown split short name, and non-six-digit suffix.
- If an item is retired, its ID remains in a retired manifest rather than being reused.

### Human-Triviality Labels

Labels must be constrained to:

```text
H0 = near-universal human-trivial task
H1 = easy but attention-sensitive
H2 = trick-prone or ambiguity-prone
H3 = exclude from benchmark
```

**Acceptance criteria:**

- Public v0 headline datasets contain only `H0` and carefully reviewed `H1` items.
- `H2` items are allowed only in calibration or experimental splits unless a plan update approves them.
- `H3` items fail validation for benchmark splits.

## Scoring Requirements

### Scorer Behavior Matrix

| Scorer | Accepted output example | Rejected output example | Primary failure type |
| --- | --- | --- | --- |
| `exact_integer_extract_first_v0` | `There are 3.` for target `3` | `There are 2.` | `incorrect_count` |
| `exact_string_trim_v0` | `yrrebwarts` for target `yrrebwarts` | `yrrebwarts.` | `wrong_letter_or_substring` |
| `normalized_string_v0` | `Apple` for target `apple` when case-insensitive metadata is set | `apples` | `wrong_letter_or_substring` |
| `normalized_list_v0` | `3, 9, 12` for target `3, 9, 12` | `9, 3, 12` | `ordering_error` |
| `multiple_choice_letter_v0` | `B` for target `B` | `The answer is B` when strict format is required | `format_noncompliance` |
| `regex_match_v0` | `YES` for regex `^(YES|NO)$` | `Yes.` | `format_noncompliance` |
| `json_exact_field_v0` | `{"answer": "3"}` | `{answer: 3}` | `json_malformed` |
| `word_count_v0` | `5` for target `5` | `four` | `list_count_error` |

**Acceptance criteria:**

- Each scorer has tests for accepted output, rejected output, empty output, verbose output, and malformed output when relevant.
- Strict format tasks reject wrappers that lenient answer tasks accept.
- Scorer tests assert both correctness and failure type.

### Failure Type Taxonomy

Supported failure types:

```text
incorrect_count
incorrect_character_position
wrong_letter_or_substring
string_transform_error
arithmetic_error
numeric_comparison_error
list_count_error
ordering_error
negation_error
format_noncompliance
json_malformed
verbose_noncompliance
refusal_or_safety_overtrigger
non_answer
ambiguous_output
provider_error
timeout
```

**Acceptance criteria:**

- Failure type enum contains exactly these values plus a consistent no-failure sentinel.
- Analysis groups unknown failure types under a validation error rather than silently reporting them as `other`.
- Failure gallery can render every failure type without crashing.

## Milestone Acceptance Criteria

### Milestone 0: Repository Skeleton

Milestone 0 is accepted only when:

- Package installs in editable mode.
- `.gitignore` protects raw logs, summaries, gallery output, env files, and caches.
- One smoke dataset file exists and validates.
- One Inspect task can be constructed without provider credentials.
- One deterministic scorer has passing tests.
- README includes the smoke-run command.

### Milestone 1: Seed Catalog

Milestone 1 is accepted only when:

- `data/source_catalog/sources_v0.jsonl` contains at least 25 validated source records.
- Each source record has a source category and rights status.
- `docs/source_archetypes_v0.md` identifies at least 5 archetypes worth converting into benchmark families.
- Public docs state that sources are leads, not ground truth.

### Milestone 2: V0 Dataset

Milestone 2 is accepted only when:

- Public v0 contains 300-500 validated items.
- Public v0 covers at least 5 task families.
- Every public item has a deterministic scorer.
- Every public item has `review_status: "reviewed"`.
- No public item has an empty `source_refs` list.
- Dataset validation passes across all public files in one command.

### Milestone 3: Model Run

Milestone 3 is accepted only when:

- V0 runs against 5-8 configured models or records a documented blocker for unavailable provider credentials.
- Raw Inspect logs are written under `results/raw`.
- Summary CSV is generated under `results/summaries`.
- Per-family breakdown is generated.
- Failure gallery is generated.
- At least one real model output is manually inspected against the scorer decision to check log parsing.

### Milestone 4: Public Prototype

Milestone 4 is accepted only when:

- README, methodology, prompt policy, scoring policy, source policy, and benchmark card are current.
- A new developer can follow docs from clone to validation to smoke run without editing source files.
- The public prototype includes v0 results or clearly labels results as pending if provider runs are blocked.
- Public prose is constructive and avoids shame framing.

### Milestone 5: V1 Planning

Milestone 5 is accepted only when:

- There is a written decision record for private holdout, human validation, public leaderboard, Hugging Face hosting, and Inspect Evals registration.
- Each decision cites evidence from v0 runs, scorer behavior, source quality, or user feedback.
- V1 scope does not expand into hosted infrastructure without a clear adoption signal.

## Definition Of Done For Any Module

A module is done only when:

- Its tests are written before or alongside implementation.
- Its public interfaces match this plan.
- Its edge cases are represented in tests.
- It has no provider calls in unit tests.
- Its docs or README references are updated when user-facing behavior changes.
- `python -m pytest` passes.
- `python -m ruff check .` passes.
- `python -m compileall obviousbench` passes after code exists.
- New generated outputs are either ignored or intentionally promoted with a note explaining why.

## Module Completion Tracker

Updated on 2026-05-30 after implementation and local verification.

| Module | Status | Evidence |
| --- | --- | --- |
| Module 0: Repository Foundation | Complete | `pyproject.toml`, `.gitignore`, `README.md`, package import, pytest, ruff, compileall |
| Module 1: Dataset Contract And Validation | Complete | `obviousbench/datasets/`, `scripts/validate_dataset.py`, dataset validation passing |
| Module 2: Prompt Policy And Sample Conversion | Complete | `obviousbench/prompts.py`, `obviousbench/datasets/load.py`, prompt/sample tests passing |
| Module 3: Deterministic Scoring Kernel | Complete | `obviousbench/scorers/`, scorer tests passing, dynamic metadata scorer |
| Module 4: Inspect Task Integration | Complete | `obviousbench/tasks/`, mock Inspect smoke eval passing |
| Module 5: Seed Data And Generators | Complete | `scripts/generate_public_v0.py`, 318 public items, 10-item smoke dataset |
| Module 6: Source Catalog And Review Workflow | Complete | `data/source_catalog/sources_v0.jsonl`, source policy docs, 25 source records validated |
| Module 7: Run Configuration And CLI | Complete | `configs/`, `obviousbench validate`, `obviousbench summarize` |
| Module 8: Analysis And Reporting | Complete | Inspect log parsing, summary CSV, failure-gallery Markdown generation |
| Module 9: Public Docs And Release Readiness | Complete | README, methodology, prompt/scoring/source policies, benchmark card, branding docs |

## Module Map

### Module 0: Repository Foundation

**Purpose:** Establish a Python package that can be installed, tested, linted, and run through Inspect without bespoke local state.

**Owns:**

- Packaging metadata.
- Dependency groups.
- Ignore rules.
- Basic CLI/script entrypoints.
- Minimal docs scaffold.

**Files:**

- Create: `.gitignore`
- Create: `pyproject.toml`
- Create: `README.md`
- Create: `obviousbench/__init__.py`
- Create: `obviousbench/_registry.py`
- Create: `tests/conftest.py`
- Create: `docs/methodology.md`
- Create: `docs/prompt_policy.md`
- Create: `docs/scoring_policy.md`
- Create: `docs/source_policy.md`

**Quality gates:**

- `python -m pip install -e ".[dev]"`
- `python -m pytest`
- `python -m ruff check .`
- `python -m compileall obviousbench`

### Module 1: Dataset Contract And Validation

**Purpose:** Convert the plan's JSONL shape into a strict local contract so every sample has a stable ID, target, scorer, family, prompt template, review status, and metadata.

**Owns:**

- Benchmark item model.
- Source catalog record model.
- Prompt template identifiers.
- Dataset validation command.
- Duplicate ID checks.
- Family/scorer compatibility checks.

**Files:**

- Create: `obviousbench/datasets/__init__.py`
- Create: `obviousbench/datasets/schemas.py`
- Create: `obviousbench/datasets/load.py`
- Create: `obviousbench/datasets/validation.py`
- Create: `scripts/validate_dataset.py`
- Create: `tests/datasets/test_schemas.py`
- Create: `tests/datasets/test_validation.py`

**Interfaces:**

- `BenchmarkItem.from_record(record: dict[str, Any]) -> BenchmarkItem`
- `BenchmarkItem.to_inspect_sample() -> inspect_ai.dataset.Sample`
- `validate_dataset_paths(paths: Sequence[Path]) -> ValidationReport`
- `load_benchmark_jsonl(path: Path) -> list[BenchmarkItem]`

**Quality gates:**

- Reject missing `id`, `family`, `prompt`, `question`, `target`, `answer_type`, `scorer`, `split`, `review_status`, or `metadata.prompt_template_id`.
- Reject duplicate IDs across all provided files.
- Reject unreviewed samples in `public_v0`.
- Reject unknown scorer names.
- Reject `H3` samples from benchmark splits.

### Module 2: Prompt Policy And Sample Conversion

**Purpose:** Keep prompt rendering reproducible and prevent prompt-policy drift from creeping into individual datasets.

**Owns:**

- Canonical final-answer-only prompt.
- Multiple-choice prompt.
- Prompt template registry.
- Sample conversion into Inspect `Sample` objects.

**Files:**

- Create: `obviousbench/prompts.py`
- Modify: `obviousbench/datasets/schemas.py`
- Modify: `obviousbench/datasets/load.py`
- Create: `tests/test_prompts.py`
- Create: `tests/datasets/test_load.py`

**Interfaces:**

- `render_prompt(template_id: str, question: str, choices: list[str] | None = None) -> str`
- `to_sample(item: BenchmarkItem) -> inspect_ai.dataset.Sample`

**Quality gates:**

- `final_answer_only_v0` renders exactly the prompt policy in the source plan.
- `multiple_choice_letter_v0` renders choices as `A.` through `D.` and targets as capital letters.
- No v0 prompt renderer inserts a system prompt, chain-of-thought instruction, or "be careful" language.

### Module 3: Deterministic Scoring Kernel

**Purpose:** Implement the benchmark's credibility layer: deterministic extraction, comparison, format strictness, and failure typing.

**Owns:**

- Normalization helpers.
- Extractors.
- Strict versus lenient scorer behavior.
- Inspect scorer wrappers.
- Failure type assignment.

**Files:**

- Create: `obviousbench/scorers/__init__.py`
- Create: `obviousbench/scorers/common.py`
- Create: `obviousbench/scorers/exact_integer.py`
- Create: `obviousbench/scorers/exact_string.py`
- Create: `obviousbench/scorers/normalized_list.py`
- Create: `obviousbench/scorers/multiple_choice.py`
- Create: `obviousbench/scorers/regex_match.py`
- Create: `obviousbench/scorers/json_field.py`
- Create: `obviousbench/scorers/word_count.py`
- Create: `obviousbench/scorers/failure_types.py`
- Create: `tests/scorers/test_exact_integer.py`
- Create: `tests/scorers/test_exact_string.py`
- Create: `tests/scorers/test_normalized_list.py`
- Create: `tests/scorers/test_multiple_choice.py`
- Create: `tests/scorers/test_regex_match.py`
- Create: `tests/scorers/test_json_field.py`
- Create: `tests/scorers/test_word_count.py`

**Interfaces:**

- `extract_first_integer(output: str) -> str | None`
- `normalize_string(value: str) -> str`
- `normalize_list(value: str) -> tuple[str, ...]`
- `score_value(extracted: str | None, target: str, mode: ScoringMode) -> ScoreDecision`
- `get_scorer(name: str) -> inspect_ai.scorer.Scorer`

**Quality gates:**

- Non-format tasks accept reasonable wrappers such as `There are 3.` when the target is `3`.
- Format-compliance tasks can mark the same output incorrect when the instruction says to return only the number.
- Every scorer returns extracted `answer`, the raw output as `explanation`, and metadata with `failure_type`.
- Unit tests cover correct, incorrect, malformed, empty, verbose, and ambiguous outputs.

### Module 4: Inspect Task Integration

**Purpose:** Provide stable Inspect task entrypoints that load local JSONL datasets and attach the correct scorer per task family.

**Owns:**

- Task definitions.
- Shared task factory.
- Inspect package registration.
- Smoke task.

**Files:**

- Create: `obviousbench/tasks/__init__.py`
- Create: `obviousbench/tasks/base.py`
- Create: `obviousbench/tasks/character_count.py`
- Create: `obviousbench/tasks/spelling_transform.py`
- Create: `obviousbench/tasks/arithmetic.py`
- Create: `obviousbench/tasks/word_count.py`
- Create: `obviousbench/tasks/ordering.py`
- Create: `obviousbench/tasks/format_compliance.py`
- Create: `obviousbench/tasks/negation.py`
- Create: `obviousbench/tasks/constraint_awareness.py`
- Modify: `obviousbench/_registry.py`
- Create: `tests/tasks/test_task_definitions.py`

**Interfaces:**

- `make_task(dataset_path: Path, scorer_name: str, name: str) -> inspect_ai.Task`
- `character_count(split: str = "public_v0") -> inspect_ai.Task`
- `smoke(split: str = "calibration_v0") -> inspect_ai.Task`

**Quality gates:**

- Every task has a default `generate()` solver and no system prompt.
- Task parameters allow alternate split paths without changing code.
- `inspect list tasks` can discover package tasks after editable install.
- Smoke tests can instantiate tasks without making model calls.

### Module 5: Seed Data And Generators

**Purpose:** Produce trustworthy initial examples from deterministic generators and a small hand-reviewed seed set.

**Owns:**

- Generator logic.
- Stable item IDs.
- Metadata provenance.
- Calibration/smoke datasets.
- Public v0 dataset files.

**Files:**

- Create: `obviousbench/generators/__init__.py`
- Create: `obviousbench/generators/ids.py`
- Create: `obviousbench/generators/common.py`
- Create: `obviousbench/generators/character_count.py`
- Create: `obviousbench/generators/spelling_transform.py`
- Create: `obviousbench/generators/arithmetic.py`
- Create: `obviousbench/generators/ordering.py`
- Create: `obviousbench/generators/word_count.py`
- Create: `obviousbench/generators/format_compliance.py`
- Create: `scripts/generate_public_v0.py`
- Create: `data/source_catalog/sources_v0.jsonl`
- Create: `data/calibration_v0/smoke_test.jsonl`
- Create: `data/public_v0/character_count.jsonl`
- Create: `data/public_v0/spelling_transform.jsonl`
- Create: `data/public_v0/arithmetic.jsonl`
- Create: `data/public_v0/word_count.jsonl`
- Create: `data/public_v0/ordering.jsonl`
- Create: `data/public_v0/format_compliance.jsonl`
- Create: `data/public_v0/negation.jsonl`
- Create: `data/public_v0/constraint_awareness.jsonl`
- Create: `tests/generators/test_character_count.py`
- Create: `tests/generators/test_arithmetic.py`
- Create: `tests/generators/test_ids.py`

**Interfaces:**

- `make_id(family: str, split: str, index: int) -> str`
- `generate_character_count_items(count: int, seed: int) -> list[BenchmarkItem]`
- `write_jsonl(items: Iterable[BenchmarkItem], path: Path) -> None`

**Quality gates:**

- Generated IDs are stable for the same generator version, seed, and input list.
- Every generated item validates through Module 1.
- Generator tests assert exact expected targets for representative cases.
- Smoke dataset contains 10-20 samples across at least 3 families.

### Module 6: Source Catalog And Review Workflow

**Purpose:** Preserve the benchmark's evidence trail without copying private or copyrighted social content into the repo.

**Owns:**

- Source record schema.
- Inclusion checklist.
- Review status transitions.
- Source summary artifact.

**Files:**

- Modify: `obviousbench/datasets/schemas.py`
- Create: `obviousbench/sources/__init__.py`
- Create: `obviousbench/sources/validation.py`
- Create: `scripts/summarize_sources.py`
- Create: `docs/source_archetypes_v0.md`
- Create: `tests/sources/test_source_validation.py`

**Interfaces:**

- `SourceRecord.from_record(record: dict[str, Any]) -> SourceRecord`
- `validate_source_catalog(path: Path) -> ValidationReport`
- `summarize_source_catalog(path: Path) -> SourceSummary`

**Quality gates:**

- Source records distinguish public links, paraphrase-only content, and non-republishable screenshots.
- Public dataset items can reference source IDs without embedding screenshot content.
- The source summary lists archetypes, not private author details.

### Module 7: Run Configuration And CLI

**Purpose:** Make local runs boring and reproducible while avoiding stale hard-coded model names in the spec.

**Owns:**

- Model config examples.
- Run config examples.
- Thin CLI helpers for validation, generation, and analysis.
- Result directory policy.

**Files:**

- Create: `configs/models_v0.example.yaml`
- Create: `configs/run_v0.yaml`
- Create: `obviousbench/cli.py`
- Modify: `pyproject.toml`
- Create: `tests/test_cli.py`

**Interfaces:**

- `obviousbench validate data/public_v0 data/calibration_v0`
- `obviousbench generate --split public_v0 --seed 98231`
- `obviousbench summarize --logs results/raw --out results/summaries`

**Quality gates:**

- Example config never claims exact current flagship names.
- CLI commands fail with actionable messages when Inspect logs or datasets are missing.
- `.gitignore` excludes raw run logs and generated result artifacts unless explicitly promoted.

### Module 8: Analysis And Reporting

**Purpose:** Turn Inspect logs into the benchmark outputs promised by the plan.

**Owns:**

- Obvious failure rate.
- Accuracy and failures per 1,000.
- Per-family breakdown.
- Format failure rate.
- Refusal/non-answer rate.
- Public archetype versus generated-variant comparison.
- Failure gallery Markdown.
- Summary CSV.

**Files:**

- Create: `obviousbench/analysis/__init__.py`
- Create: `obviousbench/analysis/logs.py`
- Create: `obviousbench/analysis/metrics.py`
- Create: `obviousbench/analysis/summarize_results.py`
- Create: `obviousbench/analysis/build_failure_gallery.py`
- Create: `obviousbench/analysis/export_csv.py`
- Create: `tests/analysis/test_metrics.py`
- Create: `tests/analysis/test_failure_gallery.py`
- Create: `tests/fixtures/inspect_log_minimal.json`

**Interfaces:**

- `load_eval_logs(path: Path) -> list[EvalRun]`
- `compute_summary(runs: Sequence[EvalRun]) -> SummaryTable`
- `build_failure_gallery(runs: Sequence[EvalRun], limit: int) -> str`
- `export_summary_csv(summary: SummaryTable, path: Path) -> None`

**Quality gates:**

- Metrics use failures divided by scored questions as the primary public value.
- Provider errors and timeouts are counted separately from incorrect answers.
- Failure gallery entries include model, family, question, expected answer, model answer, failure type, and why the item is obvious.
- Analysis tests use fixtures and do not call external models.

### Module 9: Public Docs And Release Readiness

**Purpose:** Make the repo understandable to a skeptical user who wants to reproduce the benchmark.

**Owns:**

- README.
- Benchmark card.
- Methodology.
- Prompt policy.
- Scoring policy.
- Source policy.
- Result reproduction instructions.

**Files:**

- Modify: `README.md`
- Create: `docs/benchmark_card.md`
- Modify: `docs/methodology.md`
- Modify: `docs/prompt_policy.md`
- Modify: `docs/scoring_policy.md`
- Modify: `docs/source_policy.md`
- Create: `docs/branding.md`

**Quality gates:**

- Public wording says reliability, preflight, regression, and user trust.
- Public wording avoids shame/gotcha framing.
- Docs state v0 non-goals plainly.
- Docs include exact commands for validation, smoke run, summarization, and viewing logs.

## Build Order

1. Module 0: repository foundation.
2. Module 1: dataset contract and validation.
3. Module 3: deterministic scoring kernel.
4. Module 2: prompt rendering and Inspect sample conversion.
5. Module 4: Inspect smoke task.
6. Module 5: smoke dataset and first generators.
7. Module 8: analysis over fixture logs.
8. Module 7: CLI and run configs.
9. Module 6: source catalog workflow.
10. Module 9: public docs and release readiness.

This order deliberately proves the smallest end-to-end loop before adding dataset volume:

```text
validated JSONL -> Inspect Sample -> generate() -> deterministic scorer -> Inspect log -> summary/failure gallery
```

## Implementation Tasks

### Task 1: Repository Foundation

**Files:**

- Create: `.gitignore`
- Create: `pyproject.toml`
- Create: `README.md`
- Create: `obviousbench/__init__.py`
- Create: `obviousbench/_registry.py`
- Create: `tests/conftest.py`

- [x] **Step 1: Add Python and Inspect packaging**

Create `pyproject.toml` with package metadata, Inspect AI, PyYAML, pytest, ruff, and an Inspect entry point:

```toml
[build-system]
requires = ["setuptools>=69", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "obviousbench"
version = "0.1.0"
description = "A lightweight Inspect AI benchmark for obvious public-facing LLM failures."
readme = "README.md"
requires-python = ">=3.11"
dependencies = [
  "inspect-ai>=0.3",
  "pydantic>=2.7",
  "pyyaml>=6.0",
]

[project.optional-dependencies]
dev = [
  "pytest>=8.0",
  "ruff>=0.5",
]

[project.scripts]
obviousbench = "obviousbench.cli:main"

[project.entry-points.inspect_ai]
obviousbench = "obviousbench._registry"

[tool.setuptools.packages.find]
include = ["obviousbench*"]

[tool.ruff]
line-length = 100
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "I", "UP", "B", "SIM"]
```

- [x] **Step 2: Add initial package registry**

Create `obviousbench/__init__.py`:

```python
"""ObviousBench: deterministic checks for obvious public-facing LLM failures."""

__all__ = ["__version__"]

__version__ = "0.1.0"
```

Create `obviousbench/_registry.py`:

```python
"""Inspect AI task registration imports."""

# Task imports are added as task modules are implemented.
```

- [x] **Step 3: Add result-safe ignore rules**

Create `.gitignore`:

```gitignore
.DS_Store
__pycache__/
*.py[cod]
.pytest_cache/
.ruff_cache/
.mypy_cache/
.venv/
venv/
dist/
build/
*.egg-info/
logs/
results/raw/
results/summaries/
results/failure_gallery/
*.eval
.env
.env.*
!.env.example
```

- [x] **Step 4: Run foundation checks**

Run:

```bash
python -m pip install -e ".[dev]"
python -m pytest
python -m ruff check .
python -m compileall obviousbench
```

Expected:

```text
pytest finds no tests or passes existing tests.
ruff reports no lint failures.
compileall successfully compiles obviousbench.
```

### Task 2: Dataset Schema And Validation

**Files:**

- Create: `obviousbench/datasets/__init__.py`
- Create: `obviousbench/datasets/schemas.py`
- Create: `obviousbench/datasets/validation.py`
- Create: `scripts/validate_dataset.py`
- Create: `tests/datasets/test_schemas.py`
- Create: `tests/datasets/test_validation.py`

- [x] **Step 1: Write schema tests first**

Create tests that assert:

- A complete `BenchmarkItem` parses.
- Missing required fields fail validation.
- Unknown scorer names fail validation.
- Duplicate IDs across two JSONL files fail validation.
- `H3` samples fail public split validation.

- [x] **Step 2: Implement schema models**

Create Pydantic models for:

- `BenchmarkItem`
- `BenchmarkMetadata`
- `SourceRecord`
- `ValidationIssue`
- `ValidationReport`

Use literal enums for known families, answer types, scorer names, review statuses, human-triviality labels, source types, and failure types.

- [x] **Step 3: Implement JSONL validation**

Implement:

```python
def validate_dataset_paths(paths: Sequence[Path]) -> ValidationReport:
    """Validate benchmark JSONL files and return structured issues."""
```

Validation must check required fields, duplicate IDs, public split review status, scorer name, family name, prompt template ID, and exclusion of `H3`.

- [x] **Step 4: Add script wrapper**

Create `scripts/validate_dataset.py` as a thin wrapper around `validate_dataset_paths()` that exits nonzero when `report.ok` is false.

- [x] **Step 5: Run validation tests**

Run:

```bash
python -m pytest tests/datasets -v
```

Expected:

```text
All schema and validation tests pass.
```

### Task 3: Scorer Kernel

**Files:**

- Create: `obviousbench/scorers/common.py`
- Create: `obviousbench/scorers/exact_integer.py`
- Create: `obviousbench/scorers/exact_string.py`
- Create: `obviousbench/scorers/failure_types.py`
- Create: `tests/scorers/test_exact_integer.py`
- Create: `tests/scorers/test_exact_string.py`

- [x] **Step 1: Write exact integer tests**

Cover these cases:

```python
("3", "3", True, "3")
("There are 3.", "3", True, "3")
("There are 2 r's.", "3", False, "2")
("", "3", False, None)
("three", "3", False, None)
```

- [x] **Step 2: Write exact string tests**

Cover trimmed exact matches, case-sensitive mismatches, verbose outputs, and empty outputs.

- [x] **Step 3: Implement common score decision model**

Implement a small internal type that records:

- `correct`
- `extracted`
- `failure_type`
- `explanation`

- [x] **Step 4: Implement Inspect scorer wrappers**

Each wrapper should return an Inspect `Score` with:

- `value=CORRECT` or `value=INCORRECT`
- `answer=decision.extracted`
- `explanation=state.output.completion`
- `metadata={"failure_type": decision.failure_type}`

- [x] **Step 5: Run scorer tests**

Run:

```bash
python -m pytest tests/scorers -v
```

Expected:

```text
All scorer tests pass without model calls.
```

### Task 4: Prompt Rendering And Inspect Samples

**Files:**

- Create: `obviousbench/prompts.py`
- Create: `obviousbench/datasets/load.py`
- Create: `tests/test_prompts.py`
- Create: `tests/datasets/test_load.py`

- [x] **Step 1: Write prompt tests**

Assert that `final_answer_only_v0` renders:

```text
Answer the question. Return only the final answer, with no explanation.

Question: How many r's are in strawberry?
Answer:
```

Assert that `multiple_choice_letter_v0` renders only the letter-answer instruction and choices `A.` through `D.`.

- [x] **Step 2: Implement prompt registry**

Implement `render_prompt()` with explicit supported template IDs and a clear exception for unknown template IDs.

- [x] **Step 3: Implement JSONL loading**

Implement `load_benchmark_jsonl()` and `to_sample()` so Inspect receives:

- `id=item.id`
- `input=item.prompt`
- `target=item.target`
- `metadata` containing family, subfamily, scorer, answer type, source type, source refs, human triviality, review status, and item metadata.

- [x] **Step 4: Run prompt and loader tests**

Run:

```bash
python -m pytest tests/test_prompts.py tests/datasets/test_load.py -v
```

Expected:

```text
Prompt renderers match the source policy exactly.
Loaded samples preserve IDs, targets, and metadata.
```

### Task 5: First Inspect Smoke Task

**Files:**

- Create: `obviousbench/tasks/base.py`
- Create: `obviousbench/tasks/character_count.py`
- Create: `obviousbench/tasks/__init__.py`
- Modify: `obviousbench/_registry.py`
- Create: `data/calibration_v0/smoke_test.jsonl`
- Create: `tests/tasks/test_task_definitions.py`

- [x] **Step 1: Create a 10-item smoke dataset**

Include reviewed examples for character counting, spelling transform, and arithmetic. Every record must pass Module 1 validation.

- [x] **Step 2: Implement shared task factory**

Implement `make_task()` to load samples and attach the named scorer.

- [x] **Step 3: Register smoke and character-count tasks**

Expose:

- `smoke(split: str = "calibration_v0")`
- `character_count(split: str = "public_v0")`

- [x] **Step 4: Test task construction without model calls**

Run:

```bash
python -m pytest tests/tasks/test_task_definitions.py -v
```

Expected:

```text
Tasks instantiate, load datasets, and expose default generate solvers without calling any model provider.
```

### Task 6: End-To-End Smoke Run

**Files:**

- Create: `configs/models_v0.example.yaml`
- Create: `configs/run_v0.yaml`
- Update: `README.md`

- [x] **Step 1: Add run docs with one local or cheap provider target**

Document the command shape:

```bash
inspect eval obviousbench/smoke --model <provider/model> --log-dir results/raw
```

- [x] **Step 2: Run validation before eval**

Run:

```bash
python scripts/validate_dataset.py data/calibration_v0/smoke_test.jsonl
```

Expected:

```text
Validation passed.
```

- [x] **Step 3: Run one smoke eval only after credentials/model access are available**

Run:

```bash
inspect eval obviousbench/smoke --model <provider/model> --log-dir results/raw
```

Expected:

```text
Inspect writes an eval log under results/raw and reports scorer metrics.
```

### Task 7: Analysis Over Fixture Logs

**Files:**

- Create: `tests/fixtures/inspect_log_minimal.json`
- Create: `obviousbench/analysis/metrics.py`
- Create: `obviousbench/analysis/build_failure_gallery.py`
- Create: `obviousbench/analysis/export_csv.py`
- Create: `tests/analysis/test_metrics.py`
- Create: `tests/analysis/test_failure_gallery.py`

- [x] **Step 1: Build a tiny fixture log**

The fixture should include at least one correct sample, one incorrect obvious failure, one format noncompliance, and one provider error or timeout representation.

- [x] **Step 2: Implement metric computations**

Compute:

- Obvious failure rate.
- Accuracy.
- Failures per 1,000.
- Per-family failure rate.
- Format failure count.
- Non-answer/refusal count.

- [x] **Step 3: Implement failure gallery Markdown**

Each entry must include model, task family, question, expected answer, model answer, failure type, and why humans find it obvious.

- [x] **Step 4: Run analysis tests**

Run:

```bash
python -m pytest tests/analysis -v
```

Expected:

```text
Summary metrics and failure gallery match fixture expectations exactly.
```

## Deferred V0 Work Packages

These modules are part of v0.1, but they should start after the smoke loop is proven:

- Full scorer set: normalized list, multiple choice, regex, JSON field, word count.
- Full task family set: spelling transform, arithmetic, word count, ordering, format compliance, negation, constraint awareness.
- Public v0 generators and 300-500 reviewed items.
- Source catalog expansion to 25+ public leads.
- Full docs set and benchmark card.
- Multi-model run configs and summary publication workflow.

## Critical Audits Before Calling V0.1 Done

Before declaring v0.1 complete, run skeptical passes for:

- Plan completeness: every source-plan v0 requirement maps to code, docs, tests, or an explicit non-goal.
- Code quality: validators and scorers are typed, tested, and easy to inspect.
- Test/docs alignment: README commands work, smoke dataset validates, scorer examples match docs.
- Performance: dataset validation and analysis are linear over samples and do not load avoidable large artifacts.
- Privacy/source policy: no screenshots, private handles, secrets, raw API keys, or sensitive source material are committed.

## Open Decisions To Resolve During Implementation

These are not blockers for the smoke loop:

- Whether to use Pydantic-only validation or also emit JSON Schema for external reviewers.
- Whether `results/summaries/` should remain ignored until explicit promotion.
- Which provider/model to use for the first real smoke run.
- Whether public v0 should include constraint-awareness items or defer them until human review is stronger.
- Whether to create a GitHub remote immediately or only after the smoke loop and ignore rules are in place.

## Self-Review Against Source Plan

- v0 scope preserved: Inspect AI, local JSONL, native provider mode, no explicit system prompt, deterministic scoring.
- Public framing preserved: reliability and preflight language, no shame/gotcha language.
- Dataset lifecycle represented: source, reproduction, generalization, review, inclusion.
- Core task families represented: modules include all v0 families and prioritize a smoke subset.
- Output promises represented: raw logs, summaries, obvious failure rate, per-family breakdown, failure gallery.
- Non-goals preserved: no hosted leaderboard, user accounts, web dashboard, adapters, LLM-as-judge, tool-use, RAG, long context, or multi-turn evals.
- Highest-risk areas elevated early: schemas, validation, scorers, prompt policy, and result policy come before volume.
- Product requirements now define public identity, scope boundaries, and the four core local workflows.
- Functional requirements now define acceptance criteria for package installability, validation, prompt rendering, Inspect sample conversion, scorer registry behavior, generation, analysis, gallery output, docs, and privacy.
- Technical requirements now define module boundaries, determinism, error handling, test isolation, config behavior, performance expectations, and dependency discipline.
- Data and scoring contracts now define canonical JSONL shape, stable IDs, human-triviality labels, scorer behavior, and failure taxonomy.
- Milestone criteria now define observable completion gates for repository skeleton, source catalog, v0 dataset, model run, public prototype, and v1 planning.
