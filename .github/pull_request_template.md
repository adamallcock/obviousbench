## Summary

- 

## Validation

- [ ] `uv run --extra dev python -m pytest tests -q`
- [ ] `uv run --extra dev python -m ruff check .`
- [ ] `uv run --extra dev python -m compileall -q obviousbench scripts`
- [ ] `uv run --extra dev python scripts/datasets/validate_dataset.py data/public_examples/*.jsonl`
- [ ] `uv run --extra dev python scripts/release/check_repo_hygiene.py`
- [ ] `node --check scripts/runners/price_usage_with_runcost.mjs`

## Safety

- [ ] No API keys, credentials, raw provider logs, private prompts, private review HTML, or item-level private outcomes are included.
- [ ] Generated/runtime outputs remain ignored unless explicitly part of the public v0.2 aggregate release surface.
