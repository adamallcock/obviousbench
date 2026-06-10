ROOT := ..
PY ?= $(ROOT)/.venv/bin/python
PAPER := main
RELEASE_CONFIG ?= configs/release_v0_1_0.yaml
RELEASE_MK ?= release.mk
-include $(RELEASE_MK)
EVIDENCE_MANIFEST ?= results/summaries/paper-v1-8x28-current-223-final-20260603/manifest.csv
EVIDENCE_COMPARISON_DIR ?= results/summaries/paper-v1-8x28-current-223-final-20260603/comparison
EVIDENCE_REPORT_DIR ?= docs/reports/2026-06-03-paper-v1-8x28-current-223-final
EVIDENCE_WRONG_REVIEW ?= $(EVIDENCE_REPORT_DIR)/wrong-answer-review.csv
EVIDENCE_EXPECTED_MODELS ?= 223

.PHONY: assets effort-curves release-assets release-check release-package readiness readiness-preprint related-work human-baseline-packet human-baseline-audit human-baseline-collection-handoff human-baseline-score human-baseline-thresholds human-baseline-promotion human-baseline-ops result-artifacts release-audit release-packet claims claim-ledger source-audit pdf-audit pdf-handoff pdf clean arxiv-package arxiv-audit metadata preflight submission-handoff internal-review sweep-plan analysis-plan manuscript-completeness report-tracker blocker-dashboard completion-roadmap repro-manifest

assets:
	cd $(ROOT) && .venv/bin/python scripts/build_paper_assets.py \
		--manifest data/splits/paper_v1_manifest.jsonl \
		--human-baseline data/human_baseline/paper_v1.csv \
		--model-panel $(EVIDENCE_MANIFEST) \
		--final-results-dir $(EVIDENCE_COMPARISON_DIR) \
		--wrong-answer-review $(EVIDENCE_WRONG_REVIEW) \
		--figure-renderer chrome-svg \
		--out paper/tables

readiness:
	cd $(ROOT) && .venv/bin/python scripts/audit_arxiv_readiness.py \
		--human-baseline data/human_baseline/paper_v1.csv \
		--paper-manifest data/splits/paper_v1_manifest.jsonl \
		--manifest-scope

readiness-preprint:
	cd $(ROOT) && .venv/bin/python scripts/audit_arxiv_readiness.py \
		--human-baseline data/human_baseline/paper_v1.csv \
		--paper-manifest data/splits/paper_v1_manifest.jsonl \
		--manifest-scope \
		--readiness-profile preprint \
		--out docs/research/2026-06-01-obviousbench-arxiv-readiness-audit-preprint.md

related-work:
	cd $(ROOT) && .venv/bin/python scripts/build_related_work_matrix.py

human-baseline-packet:
	cd $(ROOT) && .venv/bin/python scripts/build_human_baseline_packet.py

human-baseline-audit:
	cd $(ROOT) && .venv/bin/python scripts/audit_human_baseline_collection.py

human-baseline-collection-handoff: human-baseline-packet human-baseline-audit
	cd $(ROOT) && .venv/bin/python scripts/build_human_baseline_collection_handoff.py

human-baseline-score:
	cd $(ROOT) && .venv/bin/python scripts/score_human_baseline.py

human-baseline-thresholds: human-baseline-score
	cd $(ROOT) && .venv/bin/python scripts/audit_human_baseline_thresholds.py

human-baseline-promotion: human-baseline-thresholds
	cd $(ROOT) && .venv/bin/python scripts/promote_human_baseline.py

human-baseline-ops: human-baseline-collection-handoff human-baseline-score human-baseline-thresholds human-baseline-promotion
	cd $(ROOT) && .venv/bin/python scripts/build_human_baseline_operations.py

result-artifacts:
	cd $(ROOT) && .venv/bin/python scripts/audit_final_result_artifacts.py \
		--manifest $(EVIDENCE_MANIFEST) \
		--comparison-dir $(EVIDENCE_COMPARISON_DIR) \
		--report-dir $(EVIDENCE_REPORT_DIR) \
		--expected-models $(EVIDENCE_EXPECTED_MODELS) \
		--out docs/release/generated/final-result-artifact-audit.md \
		--strict

effort-curves:
	cd $(ROOT) && .venv/bin/python scripts/build_effort_cost_curve_report.py

release-assets: effort-curves
	cd $(ROOT) && .venv/bin/python scripts/build_release_assets.py \
		--config $(RELEASE_CONFIG)
	$(MAKE) assets

release-check: release-assets result-artifacts claims source-audit pdf-audit arxiv-audit
	cd $(ROOT) && .venv/bin/python scripts/audit_release_snapshot.py \
		--config $(RELEASE_CONFIG) \
		--strict
	cd $(ROOT) && .venv/bin/python scripts/audit_cost_integrity.py \
		--comparison $(EVIDENCE_COMPARISON_DIR)/comparison.csv \
		--out docs/release/generated/cost-integrity-audit.md \
		--strict

release-package: release-assets arxiv-package arxiv-audit

release-audit:
	cd $(ROOT) && .venv/bin/python scripts/audit_public_release_artifacts.py

release-packet: release-audit
	cd $(ROOT) && .venv/bin/python scripts/build_public_release_decision_packet.py

claims:
	cd $(ROOT) && .venv/bin/python scripts/audit_paper_claims.py \
		--paper-dir paper \
		--out docs/research/2026-06-01-paper-claim-blocker-audit.md

claim-ledger:
	cd $(ROOT) && .venv/bin/python scripts/build_paper_claim_ledger.py \
		--paper-dir paper \
		--out docs/research/2026-06-01-obviousbench-paper-claim-evidence-ledger.md

source-audit: assets related-work
	cd $(ROOT) && .venv/bin/python scripts/audit_paper_source.py \
		--paper-dir paper \
		--out docs/research/2026-06-01-obviousbench-paper-source-audit.md

pdf-audit:
	cd $(ROOT) && .venv/bin/python scripts/audit_paper_pdf.py

pdf-handoff: pdf-audit
	cd $(ROOT) && .venv/bin/python scripts/build_pdf_build_handoff.py

pdf: assets
	@if command -v latexmk >/dev/null 2>&1; then \
		latexmk -pdf -interaction=nonstopmode $(PAPER).tex; \
	elif command -v pdflatex >/dev/null 2>&1; then \
		pdflatex -interaction=nonstopmode $(PAPER).tex; \
		bibtex $(PAPER) || true; \
		pdflatex -interaction=nonstopmode $(PAPER).tex; \
		pdflatex -interaction=nonstopmode $(PAPER).tex; \
	elif command -v tectonic >/dev/null 2>&1; then \
		tectonic --keep-logs $(PAPER).tex; \
	else \
		echo "No LaTeX compiler found. Install latexmk/pdflatex or tectonic."; \
		exit 2; \
	fi

clean:
	rm -f *.aux *.bbl *.bcf *.blg *.fdb_latexmk *.fls *.log *.out *.run.xml *.toc

arxiv-package: assets related-work
	tar --exclude='main.pdf' --exclude='*.aux' --exclude='*.log' \
		-czf arxiv-src.tar.gz \
		main.tex references.bib sections tables figures

arxiv-audit: arxiv-package
	cd $(ROOT) && .venv/bin/python scripts/audit_arxiv_source_bundle.py \
		--bundle paper/arxiv-src.tar.gz \
		--out docs/research/2026-06-01-obviousbench-arxiv-source-bundle-audit.md

metadata:
	cd $(ROOT) && test -f docs/research/2026-06-01-obviousbench-arxiv-submission-metadata.md || \
		.venv/bin/python scripts/build_arxiv_submission_metadata.py

preflight: arxiv-audit
	cd $(ROOT) && .venv/bin/python scripts/build_arxiv_submission_checklist.py

submission-handoff:
	cd $(ROOT) && .venv/bin/python scripts/build_arxiv_submission_handoff.py

internal-review: arxiv-audit
	cd $(ROOT) && .venv/bin/python scripts/audit_internal_research_review.py

sweep-plan:
	cd $(ROOT) && .venv/bin/python scripts/build_final_sweep_plan.py \
		--readiness-profile preprint

analysis-plan:
	cd $(ROOT) && .venv/bin/python scripts/build_paper_analysis_plan.py

manuscript-completeness:
	cd $(ROOT) && .venv/bin/python scripts/audit_manuscript_completeness.py

report-tracker:
	cd $(ROOT) && .venv/bin/python scripts/build_report_section_tracker.py

blocker-dashboard: manuscript-completeness
	cd $(ROOT) && .venv/bin/python scripts/build_paper_blocker_dashboard.py

completion-roadmap:
	cd $(ROOT) && .venv/bin/python scripts/build_paper_completion_roadmap.py

repro-manifest:
	cd $(ROOT) && .venv/bin/python scripts/build_paper_repro_manifest.py
