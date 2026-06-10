---
title: Substring Absent Count Expanded Suite
date: 2026-06-07
type: research
status: draft
---

# Substring Absent Count Expanded Suite

## Summary

The original 80-item `substring_absent_count` suite is preserved unchanged because
the completed GPT-5.4 nano pass^3 report is provenance-tied to that exact corpus.
The new pasted-answer candidates were reviewed, deduped, and added to a sibling
expanded corpus for future benchmark runs.

- Core corpus: `data/experiments/2026-06-07-substring-absent-count-suite.jsonl`
- Expanded corpus: `data/experiments/2026-06-07-substring-absent-count-suite-expanded.jsonl`
- Builder: `scripts/build_substring_absent_count_expanded_suite.py`
- Expanded size: 145 items
- Added from pasted answer: 65 items
- Target mix: 115 zero-target absent-substring traps and 30 positive controls

## Dedupe Policy

Candidates were skipped if they repeated either:

- an existing `metadata.item_slug`
- the same `(collection_label, collection, needle)` fingerprint after casefolding

The generated expanded suite has `duplicate_fingerprints=0`.

## Included Candidate Classes

Included candidates emphasize low-ambiguity public knowledge lists where the
exact collection is finite in the prompt and the answer can be mechanically
checked:

- weekday and month traps such as absent `axe`, `moon`, `mars`, `toe`, and `cat`
- semantic lures over planets, rainbow colors, shapes, coins, chess pieces, card
  suits, continents, oceans, Great Lakes, temperature scales, DNA/RNA bases, and
  SI units
- impossible or near-impossible lexical probes such as `zz` and `qq`
- positive controls such as month `ber`, month `ary`, day `ur`, planet `ur`,
  element `ium`, chess `kn`, and continent `america`

## Held-Out Candidate Classes

Some pasted-answer ideas were intentionally not added because they add ambiguity
or policy drift risk without improving this first expanded corpus:

- alias-sensitive items, such as season `fall`
- spelling-variant items, such as SI `metre` versus `meter`
- high-cardinality or partially specified sets, such as zodiac signs, music
  note naming systems, and broad programming language lists
- overly self-referential or prompt-format-sensitive probes, such as asking for
  `day` in weekday names

## Validation

Commands run:

```bash
.venv/bin/python -m py_compile scripts/build_substring_absent_count_expanded_suite.py
.venv/bin/python scripts/build_substring_absent_count_expanded_suite.py
.venv/bin/python scripts/validate_dataset.py data/experiments/2026-06-07-substring-absent-count-suite-expanded.jsonl
```

Observed validation result:

```text
Validation passed.
items 145
targets {'0': 115, '1': 19, '2': 6, '4': 2, '3': 3}
item_type {'absent_zero': 115, 'positive_control': 30}
duplicate_fingerprints 0
```
