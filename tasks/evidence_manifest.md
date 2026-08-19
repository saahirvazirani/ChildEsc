# ChildEsc v0.1 Evidence Freeze

Freeze date: 2026-08-17

Status: frozen policy-exposed diagnostic artifact

## Reproduction check

`make reproduce` completed successfully immediately before hashing:

- 25 tests passed.
- 80 items regenerated.
- All three policies reevaluated.
- Metrics, predictions, and paper table regenerated.

## SHA-256 manifest

```text
c0fa16508bb0e5ff61d08c35f8f172e6bc5a7d6291a1978cf37aa173f0eafb6e  benchmark/scenario_families.json
2acae4d6b88b5651454e9b07fafa9163d91c9e612794df8382443110300cba44  benchmark/childesc_v0_1.jsonl
d38f4f23fd972e585b63195f6ae32ee4b35e3e0630ce3af4e569a5d3a81ee0fe  src/childesc/router.py
2ac4a77c9d8d2a1b595facda4f9402967cef4756e27bba3520fba8a81be90c1a  src/childesc/generate.py
e76f24ceab2a7f49eaf0f089645df4e2b508711585bbc71d315e61b4100837e2  src/childesc/metrics.py
19faa3921056d4e8a3f125d99b15d074ea2e6a594a5c41924687fa4601cc3c58  src/childesc/evaluate.py
893f04fea572c954b445b414a3a36076a09915834048d63f28ccf17ee916fad5  tests/test_router.py
45e78ebdb8cc66fac2febe6eaea593d27d59b9f4a01663a59aaef61404fd5db5  tests/test_generate.py
7ed67406258e1338f0c2702611ce37942882525afb0a2b39fe510b051c463787  tests/test_metrics.py
963a39de83bdd6709ee9195f66704a87732eeb207f00d1d94e9705ddd2827365  tests/test_evaluate.py
0c0e96ba528a690567fb58f46b0ac5b832892b8f7b2498d87c5b601cbf116324  tests/test_artifacts.py
b9a9a7ae52afdae4ee41ad829357c25d9252c7c6d9e712720a1cb6ebfffb088d  results/metrics.json
6b8669fd02c874098de372d82c9b94e004949386a8f9cc3ce7835b4816bf0dec  results/predictions.csv
dacd8db1d065366bd4e110abfdd78adc410cb06b35bf5ebdd7ee648ce74265aa  results/paper_table.csv
cff8a774db9e8665204ce8160c75984741b0bf7e8696feb25a3729d6c8e5b211  paper/main.tex
0a002cd6da5e03b1c92725780cef507e55a8006f2b0e472aeba4a84ea012e714  paper/references.bib
```

## Post-freeze policy

- New analysis code and outputs may be added without changing the frozen router or labels.
- The router, source families, or labels may change only under a new version.
- No inspected robustness case or human-review response may be used to tune v0.1 and then reported as held-out evidence.
- Any independently authored holdout must be created by a contributor who has not inspected router rules or item-level failures.
- Manuscript revisions must distinguish frozen v0.1 results from any later evidence.

## Repository-history limitation

The workspace files are currently untracked in Git. This hash manifest provides artifact integrity but does not establish a historical pre-registration or independently timestamped freeze. The paper must not claim otherwise.

## Final reproduction run

After adding diagnostic-analysis and manuscript-synchronization tests, `make reproduce` passed all 36 tests and regenerated the 80 benchmark items, policy predictions, aggregate metrics, error taxonomy, ablations, robustness checks, guard probes, and both paper tables. The original 25-test entry above records the pre-analysis freeze point rather than the final suite size.

The final anonymous supplement was extracted into a new temporary directory and reproduced from that clean copy. All ten generated benchmark/result files matched the workspace byte-for-byte by SHA-256.

## Fourth-page and governance extension, 2026-08-18

`make reproduce` passes 46 tests. The frozen router hash remains unchanged. The post-freeze source register, contract suite, contract evaluator, retained contract results, and non-operational delegated follow-up specification are:

```text
ff700e02cf558c8829182ec7e595a38f477631a52b70168f4ad264d35ddad0a6  benchmark/source_register.json
f1dfa0369b27272c37d5dfd41c42dceba7c899c82056872285fcaf67d9644602  benchmark/contract_probes.json
8ffd188e4d26a3e9d24bd6789cc621cd20464214a5dcee33eeb9af48291adc59  validation/delegated_followup_extension.json
d38f4f23fd972e585b63195f6ae32ee4b35e3e0630ce3af4e569a5d3a81ee0fe  src/childesc/router.py
ca06d0e6bf695ed8086385d50eff5ab134817cedb73dc0218c0103c9615a741f  src/childesc/contracts.py
0671d10468e4fb44c3b3c879935d37cba6e77d45fc23062bdbe0df72aa29993e  results/contract_results.json
f7d8c99d51793d94d5b5d3bed1a1b3f803baebd065a98fec6650d6e288ef53de  paper/main.tex
4790585edd7ccd2e5e5b6d6ee5afea79981727c8eec06782fe948f4711bc304c  paper/references.bib
b953a7edbbbce8768f83357e6792ab0a25595f0ecd0c639fce7e663693d5512b  tests/test_artifacts.py
da5fcdb3a68f7e27accfe0db7b673866f4d6a1b15798e82ae0d0bc8b8a217f66  tests/test_contracts.py
```

The follow-up specification is not part of the v0.1 empirical result. It defaults to no PII collection, no transfer, no scheduling, no outreach, and no claim of 988 participation.

The final 57-file anonymous supplement was extracted into `/private/tmp/childesc_supplement_reviewed_20260818` and `make reproduce` passed all 46 tests. The generated benchmark and all 12 result artifacts, including the three contract-audit outputs, matched the workspace byte-for-byte by SHA-256.

## Prompted-router protocol freeze, 2026-08-19

The acceptance-oriented model protocol was frozen before any full live
prompted-model result. Provider credentials were absent, and no eligible
independent holdout author was documented. The current author and coding agents
remain ineligible to create a claimed independent holdout.

```text
2acae4d6b88b5651454e9b07fafa9163d91c9e612794df8382443110300cba44  benchmark/childesc_v0_1.jsonl
186e9e055eb71599866c89d1eef1eb6cdd44b861a214cd94bbb0b8077ba35ec3  src/childesc/prompts/childesc_routing_v1.txt
bdda4a89ac8353aa487cf0dd60dc854e8d5b4e3c1f53cb9ddf28fc4842dbd2c7  canonical ROUTE_SCHEMA JSON
bc7e83ab1fe42b6a153aea3b21a2b72a366ed0533c3e6df7d4e14084527b7f5c  tasks/llm_evaluation_protocol.md
6e6b37f7ace4be68d730d309259583d612d0750c4a710e9503204895378cbf9c  tasks/acceptance_claims.md
987d4ecacf94756916b7260590547b022639dc21  git commit before protocol files
```

The protocol fixes three trials per available direct-provider model, one call
per item per trial, no hidden retries, complete-run gating, family-level
resampling, deterministic route scoring, and the action-route gap as the central
target analysis. No prompted-model score may be added to the paper until its
full run replays from verified cache entries.

## Acceptance-focused execution, 2026-08-19

No provider credential became available after the protocol freeze. The
pre-registered checksum fallback was therefore used without a smoke request,
partial model run, model substitution, or prompted-model score. The final
artifact reports this limitation in the abstract, technical protocol, appendix,
and experiment manifest.

`make reproduce` passed 48 frozen scientific/manuscript tests and 5 release
tests; `make llm-test` passed 22 provider-path tests. Tectonic compiled the
official `dblblindworkshop` source to 14 pages: content pages 1--4, references
beginning on page 5, followed by the optional appendix and checklist. All four
content pages and the first reference page were rendered and visually inspected.
The collaboration DOCX was independently rendered to five pages and inspected.

```text
2a758ea9a0e9449c57e187d9902b01ee007a42b57175432e002db6cb2c06cdab  src/childesc/metrics.py
912f6c4edaf89563df7096aa8245af24489f7af4cc1343d6b849915686ccf16c  src/childesc/llm.py
22eace55c259d91187bf026d46b0a286421e66737c8d51e8513f955c7ff44817  src/childesc/llm_evaluate.py
70c47506e9db8b98e13bfa7b294d39bec0de2136719a574b6de368216a6d704b  src/childesc/llm_analysis.py
8a3b44e01e28400155eeb0d5461a5f460d0978f06c89c4f33f08ab0eaf923539  results/metrics.json
5558834e02206e86c04d97bd81ce137a5903dddeb964abda7f8ab7a88a4b3974  results/paper_table.csv
aa1efdb76142ed7c6bbccbf72ee128d37502e4b4b49b356f7c0219ebe339c99c  paper/main.tex
98f63314d09c54ed33f7715247a219b6949f21b0563f8ef13d856f2a78ab33b0  paper/manuscript.md
430df645fd7b8ff88bd330837c239017b4b9e10f84c8c4b0650cd286a04ead13  scripts/build_paper_docx.py
2087d5ec6b9cc3fb7005580c61ba2ddcefd3a1593deff3d71d1eec41bd037028  tests/test_artifacts.py
bae59495ad1d8d9cea21a4e1ff4df704015d87395907b3e971d03fd65c362ee1  llm_tests/test_llm_analysis.py
5148fb94c432b82ec75d2fe61102d2989e10910e25d3f1e7802df5ae3db41d05  experiments/llm_manifest.json
```
