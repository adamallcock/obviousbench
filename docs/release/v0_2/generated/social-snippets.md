# ObviousBench v0.2 Social Snippets

## Generated Artifact Notice

- Source config: `configs/releases/release_v0_2_0.yaml`
- Generator: `uv run --extra dev python scripts/release/build_v0_2_release_assets.py --config configs/releases/release_v0_2_0.yaml`
- Release date: `2026-06-18`
- Status: `local-publication-prep`
- Public/private boundary: excludes private held-out prompts, raw outputs,
  item-level private outcomes, private review HTML, and attempt-level outcomes.


Status: draft local copy only.

1. ObviousBench v0.2 is designed to be saturatable at the top end: the
best model/config rows can reach 100% answer pass^3. The signal is how
quickly that falls apart when models are smaller or thinking is off.

2. Simple tasks are not trivial for deployment. Literal counting,
ordering, spelling transforms, negation, and format constraints still
separate model families and thinking settings.

3. The v0.2 public bundle will publish aggregate private results and
public examples, while keeping the private held-out prompts and raw
model outputs private.

4. This is not a model shame board. It is a preflight check for the
kind of obvious mistake users remember.

5. The practical question is not only which model is best. It is how
much visible failure risk you accept when you choose a cheaper,
faster, smaller, or lower-thinking configuration.
