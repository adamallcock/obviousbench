# ObviousBench

[**Open the ObviousBench launch site and interactive results**](https://obviousbench.com)

The launch site is the best place to read the release essay, explore the
interactive charts, and understand the public v0.2 result story. This GitHub
repository is the source/data companion: runnable benchmark code, public example
items, model/config metadata, release aggregate CSVs, license, and citation
materials.

ObviousBench is a benchmark for visible, user-recognizable mistakes in language
models: short prompts, objective answers, and repeated reliability checks.

**Public data:** the website links back to this repository for public examples,
release metadata, and aggregate CSVs such as
[`reports/v0_2/aggregate/summary.csv`](reports/v0_2/aggregate/summary.csv).

The public repository contains the runnable benchmark code, public examples,
model metadata, scoring logic, release aggregate results, and documentation
needed to inspect the public release surface. It intentionally does not include
the private held-out prompts, raw completions, provider logs, or item-level
private outcomes used for final private evaluation.

## What Is Included

- `obviousbench/`: dataset loading, task definitions, scorers, prompt helpers,
  runner utilities, costing helpers, and public release support code.
- `data/public_examples/`: public example items for documentation, smoke tests,
  and contributor orientation.
- `configs/registries/`: public model registry and reasoning-setting metadata.
- `configs/model_panels/models_v0.example.yaml`: a small example model panel.
- `configs/model_panels/models_v0_2_public.yaml`: the public v0.2
  model/config panel used by the aggregate release surface.
- `reports/v0_2/aggregate/`: public-safe v0.2 aggregate result tables.
- `docs/reference/` and `docs/positioning/`: public benchmark reference docs.
- `scripts/`: public dataset, model-registry, runner, and release helpers.
- `tests/`: public test coverage for the package and public release artifacts.

## What Is Not Included

The v0.2 private held-out set remains private. This repository does not publish
private prompts, raw model completions, private review HTML, provider residual
details, private manifests, local cache artifacts, or per-item private outcomes.

The public aggregate result files are intended to support comparison at the
model/configuration level without exposing private benchmark items.

## Quickstart

Install dependencies:

```bash
uv sync --extra dev
```

Run the public test suite:

```bash
uv run --extra dev python -m pytest tests -q
```

Run static checks:

```bash
uv run --extra dev python -m ruff check .
uv run --extra dev python -m compileall -q obviousbench scripts
```

Audit the public bundle:

```bash
uv run --extra dev python scripts/release/check_repo_hygiene.py
```

## Public Results

The most readable public results are on the launch site:

- [https://obviousbench.com](https://obviousbench.com)

This repository is the stable public source for the files the website can cite:

- [`data/public_examples/`](data/public_examples/)
- [`configs/model_panels/models_v0_2_public.yaml`](configs/model_panels/models_v0_2_public.yaml)
- [`reports/v0_2/aggregate/summary.csv`](reports/v0_2/aggregate/summary.csv)
- [`reports/v0_2/aggregate/report.md`](reports/v0_2/aggregate/report.md)

The v0.2 public aggregate release data lives in:

- `reports/v0_2/aggregate/summary.csv`
- `reports/v0_2/aggregate/report.md`
- `docs/release/v0_2/generated/`

The headline public metric is `answer pass^3`: all three sampled attempts for an
item must contain the correct answer. Strict formatting metrics remain useful
diagnostically, but the public release emphasizes non-strict answer correctness
because product-visible failure and format adherence are different signals.

The launch site itself is not duplicated in this repository. See
[`docs/reference/website.md`](docs/reference/website.md) and
[`docs/reference/public-release-surface.md`](docs/reference/public-release-surface.md)
for the public repo / website boundary.

## Website Boundary

The website content should live in the website release lane, not as a copied
build artifact in this repository. GitHub should link prominently to
[obviousbench.com](https://obviousbench.com), and the website should link back
to this repository for the public examples, aggregate data, source code,
license, citation, and reproducibility materials.

## License

Code is licensed under Apache-2.0. Data and documentation are licensed under
CC BY 4.0 unless otherwise noted. See `LICENSE` and `LICENSE-DATA-DOCS.md`.
