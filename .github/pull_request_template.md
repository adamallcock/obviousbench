## Summary

- 

## Validation

- [ ] `python -m ruff check .`
- [ ] `python -m compileall obviousbench`
- [ ] `python scripts/validate_dataset.py data/public_v0/*.jsonl data/calibration_v0/smoke_test.jsonl`
- [ ] `python -m pytest tests -q`

## Safety

- [ ] No API keys, credentials, raw provider logs, private screenshots, or local result artifacts are included.
- [ ] Generated/runtime outputs remain ignored.
