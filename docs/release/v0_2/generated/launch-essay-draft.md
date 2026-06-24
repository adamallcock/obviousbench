# ObviousBench v0.2 Launch Essay Draft

## Generated Artifact Notice

- Source config: `configs/releases/release_v0_2_0.yaml`
- Generator: `uv run --extra dev python scripts/release/build_v0_2_release_assets.py --config configs/releases/release_v0_2_0.yaml`
- Release date: `2026-06-18`
- Status: `local-publication-prep`
- Public/private boundary: excludes private held-out prompts, raw outputs,
  item-level private outcomes, private review HTML, and attempt-level outcomes.


Large language models can do work that would have sounded impossible
a few years ago. They can summarize thousands of pages, write code,
use tools, and carry a conversation across domains.

And then, sometimes, they miss something a careful person would catch
immediately: a letter count, a spelling transform, a reversed list,
or the exact format the user asked for.

That gap is what ObviousBench is for.

The point is not that simple questions are hard for everyone. The
point is that simple questions are still an excellent way to see
where capability, model size, and test-time compute stop protecting
a system from looking foolish.

In v0.2, the top end saturates: the strongest configurations can reach
100% non-strict answer pass^3 across the private set. That is good. A
benchmark of obvious tasks should be solvable by sufficiently capable
systems. The useful signal is what happens below that ceiling.

The lower rows still miss literal spelling, counting, ordering, and
format constraints. The benchmark therefore gives a concrete way to
compare how much obvious-mistake risk remains when you reduce model
size, disable thinking, or lower test-time compute.

This is the useful product question: how much risk are you accepting
when you choose a cheaper, faster, smaller, or lower-compute route?
Sometimes that tradeoff is worth it. ObviousBench helps make the
tradeoff explicit.

It is not a shame board. It is not a claim that one visible miss makes
a model bad. It is not a replacement for broad evaluations. It is a
small, deterministic preflight for a class of failures users notice
immediately.

This draft is not public copy yet. Before launch, replace local paths
with public repository, dataset, and project URLs and rerun the
public-bundle audit.
