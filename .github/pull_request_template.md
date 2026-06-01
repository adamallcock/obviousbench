## Summary

- 

## Validation

- [ ] `.venv/bin/python -m ruff check .`
- [ ] `.venv/bin/python -m compileall obviousbench`
- [ ] `.venv/bin/python scripts/validate_dataset.py data/public_v0/*.jsonl data/calibration_v0/smoke_test.jsonl`
- [ ] `.venv/bin/python scripts/validate_dataset.py data/public_v0/*.jsonl --item-cards-dir data/item_cards --allow-extra-item-cards`
- [ ] `.venv/bin/python -m pytest tests -q`

## Safety

- [ ] No API keys, credentials, raw provider logs, private screenshots, or local result artifacts are included.
- [ ] Generated/runtime outputs remain ignored.
