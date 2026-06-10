---
title: ObviousBench Related Work Positioning Matrix
date: 2026-06-01
type: research
status: ready
---

# ObviousBench Related Work Positioning Matrix

This matrix tracks nearby benchmark papers and the evidence standard
each one contributes to the ObviousBench arXiv manuscript. It does not
make result claims or run model providers.

Overall status: PASS

Summary: 11 passed, 0 blocked.

Required comparators: 11

Selection policy:
- Prefer recent arXiv benchmark reports with objective scoring, data curation, or contamination controls.
- Include opposite-difficulty comparators so the paper is clear about what ObviousBench does not measure.
- Include close non-arXiv comparators only when they materially shape positioning.
- Treat this matrix as related-work scaffolding, not evidence for ObviousBench result claims.

## Positioning Matrix

| Comparator | Cluster | Role | Evidence standard to borrow | ObviousBench stance | Coverage |
| --- | --- | --- | --- | --- | --- |
| [SimpleQA (2024)](https://arxiv.org/abs/2411.04368) `wei2024simpleqa` | short-answer factuality | Short-answer benchmark with explicit grading categories and answer criteria. | Unambiguous answer criteria, calibration, and grading transparency. | Borrow answer-criteria discipline while targeting visible micro-failures rather than factuality. | PASS: bib, cited |
| [IFEval (2023)](https://arxiv.org/abs/2311.07911) `zhou2023ifeval` | instruction following | Instruction-following benchmark built around verifiable constraints. | Constraint-level automated evaluation and concise benchmark-paper structure. | Borrow objective constraint verification while separating answer correctness from format compliance. | PASS: bib, cited |
| [FollowBench (2024)](https://arxiv.org/abs/2310.20410) `jiang2024followbench` | instruction following | Fine-grained constraint-following benchmark with level and category analysis. | Taxonomy-driven reporting by constraint type and difficulty level. | Borrow taxonomy reporting while keeping items short, public-facing, and deterministically scored. | PASS: bib, cited |
| [LiveBench (2025)](https://arxiv.org/abs/2406.19314) `white2025livebench` | live and contamination-limited benchmarks | Benchmark designed around recent, automatically scored questions and contamination controls. | Fresh data, objective scoring, update policy, limitations, and reproducibility reporting. | Borrow contamination and update discipline without claiming the current paper split is live. | PASS: bib, cited |
| [LiveCodeBench (2024)](https://arxiv.org/abs/2403.07974) `jain2024livecodebench` | live and contamination-limited benchmarks | Platform-derived coding benchmark with contamination-aware construction and holistic evaluation. | Source-vintage reporting, setup details, and contamination analysis. | Borrow source-vintage and audit framing, while excluding coding-specific claims. | PASS: bib, cited |
| [GSM-Symbolic (2025)](https://arxiv.org/abs/2410.05229) `mirzadeh2025gsmsymbolic` | symbolic and metamorphic robustness | Symbolic variants test whether apparent reasoning survives superficial changes. | Template families, controlled variants, and robustness analysis beyond a single headline score. | Borrow variant and metamorphic framing for short obvious prompts. | PASS: bib, cited |
| [MMLU-Pro (2024)](https://arxiv.org/abs/2406.01574) `wang2024mmlupro` | broad capability benchmarks | Harder broad knowledge and reasoning benchmark. | Benchmark construction pipeline, setup detail, results, error analysis, and limitations. | Position ObviousBench as complementary rather than harder or broader. | PASS: bib, cited |
| [GPQA (2023)](https://arxiv.org/abs/2311.12022) `rein2023gpqa` | broad capability benchmarks | Expert-level Google-proof question-answering benchmark. | Question objectivity, data collection, baselines, and limitations. | Use as an opposite-difficulty comparator: human-trivial reliability is not expert reasoning. | PASS: bib, cited |
| [Humanity's Last Exam (2026)](https://arxiv.org/abs/2501.14249) `phan2026hle` | broad capability benchmarks | High-difficulty benchmark release with modern model-evaluation framing. | Dataset review, evaluation setup, quantitative reporting, and discussion. | Use as a high-visibility opposite-difficulty comparator. | PASS: bib, cited |
| [When Benchmarks Age (2025)](https://arxiv.org/abs/2510.07238) `jiang2025benchmarkaging` | benchmark aging and freshness | Recent factuality-benchmark study of temporal misalignment and benchmark aging. | Explicit vintage, refresh, and temporal-misalignment discussion. | Use to justify reporting split vintage and avoiding overclaims about public seed freshness. | PASS: bib, cited |
| [SimpleBench (2025)](https://simple-bench.com/) `simplebench` | everyday simple benchmarks | Close positioning comparator for everyday reasoning failures. | Human-easy framing and public-facing simplicity. | Differentiate on deterministic scorer contracts, source cards, split hygiene, and regression use. | PASS: bib, cited |

## Manuscript Use

| Comparator | Manuscript use |
| --- | --- |
| SimpleQA | Data quality and grading-policy comparator. |
| IFEval | Scoring and format-compliance comparator. |
| FollowBench | Task-family and constraint-taxonomy comparator. |
| LiveBench | Freshness, contamination, and update-policy comparator. |
| LiveCodeBench | Data-source and contamination-framing comparator. |
| GSM-Symbolic | Metamorphic robustness comparator. |
| MMLU-Pro | Opposite-scope broad-capability comparator. |
| GPQA | Opposite-difficulty comparator. |
| Humanity's Last Exam | Modern benchmark-release style comparator. |
| When Benchmarks Age | Freshness and benchmark-aging caveat. |
| SimpleBench | Closest product-positioning comparator. |
