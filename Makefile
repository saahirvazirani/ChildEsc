PYTHON ?= python3
export PYTHONPATH := src

.PHONY: test release-test benchmark evaluate analysis contracts release-audit reproduce clean-results

test:
	$(PYTHON) -m unittest discover -s tests -v

release-test:
	$(PYTHON) -m unittest discover -s release_tests -v

benchmark:
	$(PYTHON) -m childesc.generate --source benchmark/scenario_families.json --output benchmark/childesc_v0_1.jsonl

evaluate: benchmark
	$(PYTHON) -m childesc.evaluate --data benchmark/childesc_v0_1.jsonl --output results

analysis: evaluate
	$(PYTHON) -m childesc.analysis --data benchmark/childesc_v0_1.jsonl --predictions results/predictions.csv --output results

contracts:
	$(PYTHON) -m childesc.contracts --suite benchmark/contract_probes.json --sources benchmark/source_register.json --output results

release-audit:
	$(PYTHON) scripts/release_audit.py --root .

reproduce: analysis contracts test release-test release-audit

clean-results:
	rm -f benchmark/childesc_v0_1.jsonl results/metrics.json results/predictions.csv results/paper_table.csv results/error_analysis.csv results/error_summary.json results/ablations.json results/robustness.json results/guard_probes.json results/analysis_table.csv results/contract_results.json results/contract_assertions.csv results/contract_table.csv
