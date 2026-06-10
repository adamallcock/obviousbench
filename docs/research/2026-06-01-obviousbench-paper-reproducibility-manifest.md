---
title: ObviousBench Paper Reproducibility Manifest
date: 2026-06-01
type: research
status: ready
---

# ObviousBench Paper Reproducibility Manifest

This manifest records the local paper artifacts, hashes, and cheap
rebuild commands needed to reproduce the current arXiv manuscript
workspace. It is intentionally limited to source, configs, frozen
paper data, generated paper assets, audit reports, and the draft
source bundle. Provider logs and post-sweep summary directories are
outside this manifest's scope.

Overall status: PASS

Required artifacts: 55/55 present

Missing required artifacts: 0

## Git State

- Head: `6c8ef48`
- Worktree: `dirty`
- Status summary: 245 changed or untracked path(s)

## Artifact Inventory

| Category | Path | Required | Status | Bytes | SHA-256 |
| --- | --- | --- | --- | ---: | --- |
| analysis plan | `configs/paper_v1_analysis_plan.yaml` | yes | present | 6992 | `66dcd8e8d8d07439398f53233c7959df8ed55d2978d5b8f4cdcb46620a0aa443` |
| analysis plan | `docs/research/2026-06-01-obviousbench-paper-analysis-plan.md` | yes | present | 5801 | `5c3416a4861576ea98a379ac3873dfd21f4bacaa178f5a03af876b17e463f4b4` |
| article source | `paper/main.tex` | yes | present | 2215 | `5ae5e84af77ede6030e42b978af840b86b9d97b1274713f844a0d30df5727603` |
| article source | `paper/references.bib` | yes | present | 4040 | `9ad836522d7a1c896bb5f197f4d0e8d1525f645f21f2951e354c145309f46220` |
| article source | `paper/sections/01_introduction.tex` | yes | present | 1603 | `c90e6030d17713a0b0202b618151ed9abd2f904953555f141f49789f510465c5` |
| article source | `paper/sections/02_related_work.tex` | yes | present | 1510 | `4e8996f9671c55063973025178aa0f6159583435527b7f495e0baf29c51dc0b5` |
| article source | `paper/sections/03_benchmark.tex` | yes | present | 1640 | `1959e00505539bf4bbd287eb1793649af4cf10bd92b9b2306dc8eb4335e8e941` |
| article source | `paper/sections/04_data_review.tex` | yes | present | 1286 | `89edbc82995981bd9b86bb2a294848f6f0a02c886073b17a19fa9862a545e11b` |
| article source | `paper/sections/05_scoring_protocol.tex` | yes | present | 2417 | `113f1d4c649eab1c2097283d9b4d39058c82341f2b8e1d89077b27c3f4143e16` |
| article source | `paper/sections/06_results.tex` | yes | present | 2973 | `ce875b2d2f5bb1650678885f5e3a04e2af77bb1d5ecf782eb66c69d8238bf17f` |
| article source | `paper/sections/07_analysis.tex` | yes | present | 2910 | `50a5030e5322b22fa86e3fa4d20a6ca0904a5105ea1965c3da68352651634e11` |
| article source | `paper/sections/08_discussion.tex` | yes | present | 1473 | `269692ed3a1830cacee5d261d9c7019a0630f5d653a953058c2b0f76574e6e15` |
| article source | `paper/sections/09_limitations_ethics_reproducibility.tex` | yes | present | 2189 | `51edff2a04420309890e1d5726ea785d3d74ff6ac9ee8acc22b671b0f4792ec3` |
| article source | `paper/sections/appendix.tex` | yes | present | 2569 | `1dd38a47a230aa2eb2333d7e94d9db7b12d85014b330f9dbbd0ad885ccc95abe` |
| arxiv source bundle | `paper/arxiv-src.tar.gz` | yes | present | 227889 | `d921cc18859068f57f5d717f385bbf4337563d656c38d37bee27bd30544a9581` |
| audit report | `docs/research/2026-06-01-obviousbench-arxiv-internal-review.md` | yes | present | 993 | `3ca3678b98d74c2f18489912aa5005c665b348aa072cbdda1bb166eda68655c5` |
| audit report | `docs/research/2026-06-01-obviousbench-arxiv-submission-checklist.md` | yes | present | 1848 | `b01420a023b5b695449ef0c1fb6cf84ca821bbb0c23c0b672b379f0670280ff2` |
| audit report | `docs/research/2026-06-01-obviousbench-arxiv-submission-handoff.md` | yes | present | 2154 | `3e2543516b437c0005542bc65dbe7282ff59b5d5506f2c4f5966e88a18463a72` |
| audit report | `docs/research/2026-06-01-obviousbench-manuscript-completeness-audit.md` | yes | present | 3509 | `d1e7f0e7bc6dc498760bb5e5a03b240b185d0439e3737dc9135b38d0ec35622b` |
| audit report | `docs/research/2026-06-01-obviousbench-paper-claim-evidence-ledger.md` | yes | present | 4087 | `9b805ad214b006c8cb4508967c330a6416509db0d5bac8f0eaf6f4e64520ee03` |
| audit report | `docs/research/2026-06-01-obviousbench-paper-pdf-build-audit.md` | yes | present | 1050 | `1d0fd29bba0cbb66f62e915e360c4b0a7521fac4764b2b39d58690a424171a8f` |
| audit report | `docs/research/2026-06-01-obviousbench-paper-source-audit.md` | yes | present | 780 | `019315d22b45e66643845873c4232822f4b0b158ac0aa2e55b51f2e92abf2b33` |
| audit report | `docs/research/2026-06-01-obviousbench-pdf-build-handoff.md` | yes | present | 3044 | `1d3d172a3dbebed3a18db548bcd53dffe69c02edbc1f29297cb1a10b88426011` |
| audit report | `docs/research/2026-06-01-obviousbench-public-release-artifact-audit.md` | yes | present | 1450 | `312e85d47ee039dd69936abb45da25e7d643b8ca1b2ba705f8f932d311ead46c` |
| audit report | `docs/research/2026-06-01-obviousbench-public-release-decision-packet.md` | yes | present | 3298 | `53ea4e7eb756e2e211bf8acda0371b17efe6820b9165d7207515a9b16d2ee313` |
| deferred human baseline | `data/human_baseline/paper_v1.csv` | no | present | 53 | `1124031fea4efd68811567aab4b487eedface0743980a447be440bfabd35fee2` |
| deferred human baseline | `data/human_baseline/paper_v1_answer_key.csv` | no | present | 8984 | `2dc17994ede529ac6779dddc8ee61097545f9639aa8a98cc6c8df836bf573ed5` |
| deferred human baseline | `data/human_baseline/paper_v1_assignments.csv` | no | present | 112846 | `4a5eb5c04b868451097da86db9c930e8c8d31943ad634f96a88a65cd8c6717cd` |
| deferred human baseline | `data/human_baseline/paper_v1_response_template.csv` | no | present | 20353 | `135fa391b4e78cb6e6fa77172b3fd03cdb355724f3e827105d211baa94c6e773` |
| deferred human baseline | `data/human_baseline/paper_v1_scored_draft.csv` | no | present | 33190 | `0786ba8e0ae2b600defee5c2ee475850484381013e794c0f7ce85ff960f61183` |
| deferred human baseline | `data/human_baseline/paper_v1_threshold_families.csv` | no | present | 374 | `e6d08e7caed492067dff4d75eafeb5c3ff6462f365d4d0d527013d05a0456011` |
| deferred human baseline | `data/human_baseline/paper_v1_threshold_items.csv` | no | present | 12819 | `5fe1a6bfd6320876a657b7ee9eb8673e74d9d7a0f8cfedbe6675b9a4b4874807` |
| deferred human baseline | `docs/research/2026-06-01-paper-v1-human-baseline-collection-audit.md` | no | present | 1815 | `1ea70dc03631498110248c21fe80ca2a1aaa09a1c25708c97e7056c68332c461` |
| deferred human baseline | `docs/research/2026-06-01-paper-v1-human-baseline-collection-handoff.md` | no | present | 3737 | `1768568f96c38a820b52be030e72c9ad6034ee58acab6f549d0357098b15aa2d` |
| deferred human baseline | `docs/research/2026-06-01-paper-v1-human-baseline-collection-packet.md` | no | present | 1856 | `7a883b12a519afaf104a96546afcfdb02a1554281608dff35d6836284de48bba` |
| deferred human baseline | `docs/research/2026-06-01-paper-v1-human-baseline-operations.md` | no | present | 2443 | `df02734f0de577d495cab44c655141080a7d8ce879cc4c67227e2c41796260fc` |
| deferred human baseline | `docs/research/2026-06-01-paper-v1-human-baseline-participant-packets.md` | no | present | 120531 | `20702119b82b288d58f99a7d5f58229cc5d8693cc85ce6e92447ee87a5979007` |
| deferred human baseline | `docs/research/2026-06-01-paper-v1-human-baseline-promotion-report.md` | no | missing |  |  |
| deferred human baseline | `docs/research/2026-06-01-paper-v1-human-baseline-scoring-report.md` | no | present | 2243 | `7f7b0ecf78a3e1fafc24f0b3ab9bfa59cc06803262f8a2ee9f9fb57608d8cd7a` |
| deferred human baseline | `docs/research/2026-06-01-paper-v1-human-baseline-threshold-audit.md` | no | present | 3957 | `788e6dc629afde4aece1c77103df81500c46dd20abe2f4f23634b19e6fe00186` |
| editorial tracker | `docs/research/2026-06-01-obviousbench-arxiv-blocker-dashboard.md` | yes | present | 3757 | `6655165dd83fc2c11ac4a694a1c347119c4a1c9d2e8137ebbcf8ddf68ba7d22b` |
| editorial tracker | `docs/research/2026-06-01-obviousbench-arxiv-completion-roadmap.md` | yes | present | 10681 | `b449e618102ad382bf13a807dc450a2dc48af43243847620ba52c7146318237b` |
| editorial tracker | `docs/research/2026-06-01-obviousbench-report-section-tracker.md` | yes | present | 3216 | `16dd70a0b3efc2086a828d6e607ed5c783348fbc15873a660a5692ac265f2502` |
| evidence-run comparison | `results/summaries/paper-v1-combined-234-overline-attempt-scored-20260602/comparison/comparison.csv` | yes | present | 113829 | `18ca56187cc81ede4c39347539c72f82d06bc27ddb8fee1bf0dd7e2a952dd817` |
| evidence-run manifest | `configs/paper_v1_combined_234_overline_attempt_scored_20260602_manifest.csv` | yes | present | 43596 | `429cefa1535cba916df7f15536609d3206d930533b6123254dbad38c6571e0c2` |
| evidence-run report | `docs/reports/2026-06-02-paper-v1-combined-234-overline/report.html` | yes | present | 528729 | `0c99b555c5d1cb0320a930cf2d4034dbf54a6fb5e12f09510a53c48a32c52f68` |
| frozen paper data | `data/barrages/hard_obvious_8x10_seed_20260531.jsonl` | yes | present | 92258 | `8babbc22ea470c10b210983cbbf10e0459cc760eafb8f0a1ac0325fe07378533` |
| frozen paper data | `data/splits/paper_v1_manifest.jsonl` | yes | present | 39818 | `a2a95ab2db2046e2a76d475d1dfd2063e96d5406fe1a991212ebcdffb967ced2` |
| generated paper assets | `paper/figures/answer_format_gap.pdf` | yes | present | 41656 | `e5acc8e6b4628d7aee7c680340b3c1ea292fe5e2a83445c6571638a52a003e4f` |
| generated paper assets | `paper/figures/cost_frontier.pdf` | yes | present | 68779 | `a4f3a59f6c1d05dfecc1a91eb49aaf7eecb00f1068171ed008972a3382874154` |
| generated paper assets | `paper/figures/family_heatmap.pdf` | yes | present | 80951 | `381ea7c07c56dc2db211f57e0c9d4edd17a33db31e2aed61025efa2a14c9f660` |
| generated paper assets | `paper/figures/leaderboard.pdf` | yes | present | 67486 | `68116a4b9b30415164bc8f3800836e899c5def7a326980c19264001b9864009e` |
| generated paper assets | `paper/tables/dataset_composition.tex` | yes | present | 720 | `a8a347bf884337cbad730d0c8bddd04a993abe029417b1634685638760bb8d43` |
| generated paper assets | `paper/tables/failure_type_summary.tex` | yes | present | 1032 | `38e78fbf51bba13404a5a17527c465fb83abbfca593dee87103f7dcc8250494a` |
| generated paper assets | `paper/tables/family_results.tex` | yes | present | 1009 | `6eac8447727a8fbe841b39f43c7ef7eea0e7f96b1fa531c90fcd54dcbbf65a19` |
| generated paper assets | `paper/tables/human_baseline_summary.tex` | yes | present | 191 | `5b054828d85c5a5c2310d63b726f4f6b0f3b48db35e7cd496d3fb167494fd97d` |
| generated paper assets | `paper/tables/main_results.tex` | yes | present | 1724 | `3d0dbe188b5f3a6a9b69182375e03a52de2b5162edd7a7a8347e4285a04318ce` |
| generated paper assets | `paper/tables/model_family_results.tex` | yes | present | 840 | `39c612488b4c39fd2d4693a2f1eefb83efd70b846d408de11cfd1c2feb02ecb6` |
| generated paper assets | `paper/tables/model_panel.tex` | yes | present | 895 | `80360fb007356f900ae59020314b4d34eb265abf0399b4741ebf4ca3bc6522f9` |
| generated paper assets | `paper/tables/provider_exclusions.tex` | yes | present | 1368 | `e5e0420c8c5c19132eaf5f3c061352586fe5766fb2b534719ab4cb892b5ca381` |
| generated paper assets | `paper/tables/readiness_gates.tex` | yes | present | 642 | `c7a5cba345af09e0a3d19e775198b5ec5518622001d903cd8efd03cb96d73529` |
| generated paper assets | `paper/tables/related_work_positioning.tex` | yes | present | 2654 | `4e5d22ae1a0ba403a9c817dea6a94f6cf90f9aa73fd8767318d0c7b253497f39` |
| generated paper assets | `paper/tables/scorer_gold_coverage.tex` | yes | present | 406 | `3edbd06988d84de9b3b283856c023fa241c13ae3a9568f4541c4a0fc767cb6cb` |
| generated paper assets | `paper/tables/thinking_group_results.tex` | yes | present | 811 | `300cac01c66fb8c16ea9be0a82458acc22fc9be16c9b9ef7e320af02d4347e6f` |
| item evidence | `data/item_cards/public_v0/cards.yaml` | yes | present | 464971 | `2999a790f09d47a70c1fa8e5aff4ff1a72c51de76a8f1163f7aa52828a67541e` |
| model panel | `configs/paper_v1_model_panel.yaml` | yes | present | 7755 | `94ba43c1438e4d99465ae61210ffde20d755e9d879e79df99cc1a661ed1b0351` |
| related work | `configs/paper_v1_related_work.yaml` | yes | present | 7329 | `baff2b364a106bfe20d08ef042372633d5bf98ec574e5f1d34fb700aea870d85` |
| related work | `docs/research/2026-06-01-obviousbench-related-work-positioning.md` | yes | present | 5772 | `9284e0ac33a02b4cc2c412168680cc8378e2aff6722adf1c99fe3bd488608840` |
| run handoff | `docs/research/2026-06-01-paper-v1-final-result-artifact-audit.md` | yes | present | 297749 | `5fa51913bd665f3663368c005082a7e1331b0ce58ffa493faf6a37e86ae778a6` |
| run handoff | `docs/research/2026-06-01-paper-v1-final-sweep-plan.md` | yes | present | 14164 | `31623f170bea921b7f3074c97445268422a1b98b138486c290f08e557c0391fc` |

## Rebuild And Check Commands

| Command | Purpose | Expected status |
| --- | --- | --- |
| `make -C paper assets` | Regenerate paper tables and figures from the current evidence run. | Should pass without provider calls. |
| `make -C paper readiness` | Run the strict manifest-scoped paper-readiness gate. | Expected to fail until real human-baseline rows exist. |
| `make -C paper readiness-preprint` | Run the fast-preprint paper-readiness gate. | Should pass without human-baseline rows when measured-human claims are omitted. |
| `make -C paper related-work` | Regenerate the related-work positioning matrix and LaTeX table. | Should pass when required comparator citations are present. |
| `make -C paper human-baseline-packet` | Regenerate participant assignments and response templates. | Should pass without provider calls. |
| `make -C paper human-baseline-audit` | Audit human-baseline response collection completeness before scoring. | Should pass and report blockers until real responses and timings are present. |
| `make -C paper human-baseline-collection-handoff` | Regenerate the human-baseline collection execution handoff. | Should pass and report blockers until every response row is complete. |
| `make -C paper human-baseline-score` | Score filled human-baseline responses against the local answer key. | Should pass and report blockers until real responses are present. |
| `make -C paper human-baseline-thresholds` | Classify scored human-baseline rows against predeclared paper thresholds. | Should pass and report no-data blockers until real responses are present. |
| `make -C paper human-baseline-promotion` | Audit whether scored human-baseline rows can be promoted into paper_v1.csv. | Should pass and report blockers until collection, scoring, and thresholds pass. |
| `make -C paper human-baseline-ops` | Regenerate the human-baseline collection and promotion operations handoff. | Should pass and report blockers until collection, scoring, thresholds, and readiness pass. |
| `make -C paper result-artifacts` | Audit expected final paper-sweep summaries, comparison CSVs, and reports. | Should pass and report missing artifacts until the final sweep has run. |
| `make -C paper release-audit` | Audit public release, license, citation, and metadata-link artifacts. | Should pass and report blockers until public release decisions are confirmed. |
| `make -C paper release-packet` | Build the public-release decision packet and draft metadata templates. | Should pass and report confirmation blockers until release decisions are final. |
| `make -C paper claims` | Audit unresolved manuscript claim markers. | Expected to fail while claimblocked or obtodo markers remain. |
| `make -C paper claim-ledger` | Map unresolved claim markers to required replacement evidence. | Expected to fail while markers remain, after writing the ledger. |
| `make -C paper source-audit` | Check TeX inputs, figures, bibliography, citations, and upload markers. | Expected to fail while submission markers remain. |
| `make -C paper pdf-audit` | Audit the current PDF build environment, artifact, source, and log state. | Expected to fail until a LaTeX toolchain, PDF, clean log, and clean source exist. |
| `make -C paper pdf-handoff` | Regenerate the PDF toolchain and inspection handoff. | Should pass and report blockers until the PDF audit is clean. |
| `make -C paper arxiv-audit` | Build and audit the draft arXiv source bundle. | Should pass when the local source bundle contains only allowed files. |
| `make -C paper preflight` | Aggregate final arXiv submission blockers. | Expected to fail until PDF, metadata, release links, and claims are final. |
| `make -C paper submission-handoff` | Regenerate the upload-facing arXiv submission handoff. | Should pass and report blocked upload readiness until final checks pass. |
| `make -C paper internal-review` | Run the local research-review gate. | Expected to fail until final result evidence and claim replacements exist. |
| `make -C paper sweep-plan` | Generate the dry-run final-sweep handoff without running providers. | Should pass; Run allowed may be YES after preprint readiness and cost artifacts pass, but provider execution still needs approval. |
| `make -C paper analysis-plan` | Regenerate the frozen paper reporting and statistics plan. | Should pass without provider calls. |
| `make -C paper manuscript-completeness` | Audit expected arXiv manuscript components, assets, citations, and markers. | Should pass and report blockers until final evidence-backed prose exists. |
| `make -C paper report-tracker` | Regenerate the manuscript section-status dashboard. | Should pass without provider calls. |
| `make -C paper blocker-dashboard` | Regenerate the consolidated blocker dashboard from current paper audits. | Should pass and report blocked/waiting rows until final evidence exists. |
| `make -C paper completion-roadmap` | Regenerate the ordered roadmap from current paper audits to arXiv submission. | Should pass and report blocked/waiting phases until final evidence exists. |
| `make -C paper repro-manifest` | Regenerate this reproducibility manifest. | Should pass once required local artifacts exist. |
