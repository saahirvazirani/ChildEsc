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

OpenRouter credentials became available after the original freeze. Protocol
v1.0.1 was executed without silent repair: a Gemini smoke was incomplete because
reasoning exhausted the 256-token allowance, and three Claude attempts remained
incomplete after credit exhaustion. They receive no comparative score.

A new v1.1 configuration was specified after those failed pilots but before any
v1.1 call. It pinned the dated Claude Sonnet 5 slug to OpenRouter's first-party
Anthropic endpoint, disabled fallbacks, set low reasoning with reasoning text
excluded, raised the output cap to 1,024 tokens, and retained one attempt per
item with no response repair. The four-item smoke returned OpenRouter's short
model alias. Before any full v1.1 trial, amendment 1.1.1 defined a metadata-only
identity gate using a frozen public alias-to-canonical snapshot; no prompt,
label, metric, generation setting, or correctness-dependent rule changed.

Three sequential 80-item v1.1.1 trials then completed with 240/240 valid routes,
no provider errors, and first-party provider label `Anthropic`. Credential-free
cache replay reproduced each normalized decision hash. The paper reports trial
means and ranges, not pooled pseudo-replication: action accuracy 80.8%, exact
route accuracy 51.7%, a 29.2-point action-route gap, and 40.7--43.6% target
failure among action-correct handoffs. This is a routing-only diagnostic against
the same provisional synthetic specification, not a model comparison, holdout,
clinical result, or deployment claim.

```text
759bca00b868059589124f323c04fe86e5e56ea2ff8f75bbbf63825f3325863d  tasks/llm_evaluation_protocol_v1_1.md
b31166cf3f977d512519e79513e557c6d0cadfb05639a7fb121d7e618ce60562  experiments/openrouter_claude_sonnet_5_snapshot_2026-08-19.json
88826b7e21d660066de0b17814fc793a306da498c156fc53a2866c621406ca3c  results/llm_v1_1_summary.json
30630d7cc83b8302b74cfddf31f1cf8936c403656cdb8e4adb6ccea80415cce0  normalized replay v1-1-trial-1
117e194d46ddf8d06fa10cf7689a45f66f988b8ec1c00eed04b93c2a1c035d8d  normalized replay v1-1-trial-2
12b8fd755e781c1c7b960a47dab0680a2c2eb8c1058ba86430b93c04c1899257  normalized replay v1-1-trial-3
```

## Cross-system routing extension, 2026-08-29

Protocol v1.2.0 was committed before any v1.2 model call. It preserved the
benchmark, prompt, schema, labels, metrics, and existing Claude outputs while
freezing first-party OpenRouter endpoints for the Gemini and GPT families named
in the original manifest. Provider fallbacks were disabled, strict structured
outputs were required, reasoning was set to low and excluded, and no output
repair or hidden retry was allowed.

Both four-item smokes qualified on completeness, endpoint identity, schema, and
offline replay. All three Gemini 80-item trials completed. Two GPT 80-item
trials completed; the third returned one provider error and remains retained at
79/80 valid outputs without a score or retry. Every scored trial replays from
content-addressed cache with matching normalized decision hashes.

New spend, including smokes and the incomplete GPT trial, was USD 1.999982:

- Gemini: 244/244 valid calls, USD 0.644322.
- GPT: 243/244 valid calls, one provider error, USD 1.355660.

The result-dependent claim gate permits a bounded statement that the
action-route gap recurs across three prompted systems on ChildEsc v0.1. It does
not permit model ranking or external, clinical, validated-benchmark, response-
quality, or deployment claims.

```text
44271373927c9f777e8f928231c05f8c629b3c0fb6548d271b23e2bea4cc9daf  tasks/llm_evaluation_protocol_v1_2.md
f0cb4e8c228fc298de7a656e4ae489bb19e94acbeea14562a3f6ba78751fb93c  experiments/openrouter_gemini_snapshot_2026-08-29.json
37e8e088362b3fea138e2551594826c58e45ba39f5bf6cbcb67dba8ed48159bd  experiments/openrouter_gpt_snapshot_2026-08-29.json
0b1594d1e4d12f015fad5bbb2bcb2468eb7e891458b347252c9e7698c35652df  results/llm_v1_2_summary.json
d750dc24d8dcba7debfa322c52a8351b9688e10e5a4f443e31a73c4feadabc2f  results/llm_v1_2_paper_table.csv
650438e4aac81a5bb65930baaba5e6604467540c6e96f9ac0acee3c9cfe28816  results/llm_v1_2_target_failures.csv
ea03cb4b072ea0f33cdbbaa5f738b537c1226d43e2e17462a96bfb7d51ea4798  normalized Gemini trial 1 and replay
897243daa2b23b0d98c6e04e2147d21fe6c7f228fc95fbd3e1f84cacf1a181cc  normalized Gemini trial 2 and replay
f5c077b6842706266cd99077b1cb902f5aa019ee555728c6bfa5d518217b0e12  normalized Gemini trial 3 and replay
cd6996a69baba733e100f9cc146797dea1207f5a5b2ead49c345299f599a2fef  normalized GPT trial 1 and replay
24d72adfbdd453a2b14e7c5b70c1867804bd8a8d60f160a8ec7e4cfe62b4aff8  normalized GPT trial 2 and replay
```
