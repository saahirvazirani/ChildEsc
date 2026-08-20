# ChildEsc

ChildEsc is a preliminary counterfactual testbed for specifying and auditing
child-centered escalation and human-handoff routing in consumer conversational
AI. It contains 80 LLM-assisted synthetic, multi-turn conversations organized
into 20 scenario families, transparent baselines, a rule-based implementation
checksum, safety-sensitive metrics, and relational contract probes.

> **Content warning:** Benchmark text references self-harm, suicide, abuse,
> coercion, eating-related medical risk, and online exploitation. It contains no
> procedural self-harm instructions, explicit sexual content, real child data,
> hotline transcripts, or clinical records.

## What ChildEsc evaluates

ChildEsc evaluates an application-layer safeguard that selects one of four
ordered actions:

1. `continue_support`
2. `boundary_redirect`
3. `human_support`
4. `urgent_handoff`

For escalations, the safeguard also selects one or more human-support target
classes, such as `safe_adult_not_implicated`, `health_professional`, or
`crisis_service`. Permitted and forbidden target sets make unsafe handoffs
auditable, including cases where an adult may be implicated.

The testbed is for research, implementation auditing, and future expert review.
Current policy-exposed results are diagnostic checksums. They do not estimate
generalization, clinical accuracy, comparative effectiveness, or deployment
safety.

## Quickstart

Requirements:

- Python 3.11 or newer
- GNU Make or a compatible `make`
- No third-party Python packages

Clone and reproduce:

```bash
git clone https://github.com/saahirvazirani/ChildEsc.git
cd ChildEsc
make reproduce
```

The staging repository is private during double-blind review, so cloning
requires authorized GitHub access. The command deterministically generates the
benchmark, evaluates the baselines and rule checksum, runs the frozen analyses
and relational contracts, executes all tests, and audits the release boundary.

Expected output includes 49 passing scientific/manuscript tests, five passing
repository-release tests, and `Release audit passed.` The optional provider
path is tested separately by `make llm-test`, which currently runs 25 tests.

## Commands

| Command | Purpose |
|---|---|
| `make benchmark` | Generate `benchmark/childesc_v0_1.jsonl` deterministically. |
| `make evaluate` | Evaluate baselines and the rule implementation checksum. |
| `make llm-test` | Test the optional provider adapters and offline cache replay without API calls. |
| `make analysis` | Generate error, ablation, robustness, and guard analyses. |
| `make contracts` | Evaluate frozen relational contract assertions. |
| `make test` | Run unit, regression, leakage, and synchronization tests. |
| `make release-test` | Run the five cross-platform and release-audit tests. |
| `make release-audit` | Check candidate files for local paths, credentials, private study paths, and oversized artifacts. |
| `make reproduce` | Run the complete pipeline and release audit. |
| `make clean-results` | Remove generated benchmark and result files. |

To run modules without Make:

```bash
PYTHONPATH=src python3 -m childesc.generate \
  --source benchmark/scenario_families.json \
  --output benchmark/childesc_v0_1.jsonl

PYTHONPATH=src python3 -m childesc.evaluate \
  --data benchmark/childesc_v0_1.jsonl \
  --output results
```

## Optional LLM routing evaluation

ChildEsc includes provider-neutral adapters for Gemini, OpenAI, Anthropic, and
OpenRouter. They ask a model for only an action and target classes; they do not
ask the model to generate a supportive response. Exact model IDs are explicit
CLI arguments so runs never silently move to a provider alias chosen by this
repo.

Start with a small Gemini smoke run to bound cost:

```bash
export GEMINI_API_KEY="your-key"
PYTHONPATH=src python3 -m childesc.llm_evaluate \
  --data benchmark/childesc_v0_1.jsonl \
  --provider gemini \
  --model gemini-2.5-flash-lite \
  --trial-id trial-1 \
  --limit 4 \
  --cache .cache/childesc/gemini-2.5-flash-lite \
  --output results/llm/gemini-2.5-flash-lite-smoke
```

Replay the exact provider responses without a key or network request:

```bash
unset GEMINI_API_KEY
PYTHONPATH=src python3 -m childesc.llm_evaluate \
  --data benchmark/childesc_v0_1.jsonl \
  --provider gemini \
  --model gemini-2.5-flash-lite \
  --trial-id trial-1 \
  --limit 4 \
  --cache .cache/childesc/gemini-2.5-flash-lite \
  --cache-only \
  --output results/llm/gemini-2.5-flash-lite-replay
```

For comparison runs, use `--provider openai` with `OPENAI_API_KEY` or
`--provider anthropic` with `ANTHROPIC_API_KEY`, and supply a model that supports
the provider's structured-output API. OpenRouter is also supported:

```bash
export OPENROUTER_API_KEY="your-key"
PYTHONPATH=src python3 -m childesc.llm_evaluate \
  --data benchmark/childesc_v0_1.jsonl \
  --provider openrouter \
  --model openai/gpt-4o-mini \
  --trial-id trial-1 \
  --limit 4 \
  --cache .cache/childesc/openrouter-gpt-4o-mini \
  --output results/llm/openrouter-gpt-4o-mini-smoke
```

To pin an OpenRouter experiment to one upstream provider and an explicit
reasoning policy, pass the controls below. Provider pinning disables fallbacks:

```bash
PYTHONPATH=src python3 -m childesc.llm_evaluate \
  --data benchmark/childesc_v0_1.jsonl \
  --provider openrouter \
  --model anthropic/claude-sonnet-5-20260630 \
  --openrouter-provider anthropic \
  --reasoning-effort low \
  --max-output-tokens 1024 \
  --protocol-version 1.1.1 \
  --trial-id v1-1-smoke-1 \
  --limit 4 \
  --cache .cache/childesc/openrouter-claude-sonnet-5-v1-1 \
  --output results/llm/openrouter-claude-sonnet-5-v1-1/smoke-1
```

The selected OpenRouter model and upstream endpoint must support
`structured_outputs` and `response_format`. The adapter requires parameter-
compatible routing and rejects nonconforming responses. Reasoning text is
excluded when an explicit reasoning effort is supplied, but token usage remains
in provider metadata. The evaluator writes
`routing_predictions.jsonl`, append-only `attempts.jsonl`, and
`routing_metrics.json`. Comparative routing
metrics are withheld unless every item has a valid route; refusals, transport
failures, and malformed outputs remain visible as incomplete results.

Use a distinct `--trial-id` and output directory for each repeated run. Trial
identity changes local cache provenance but is never included in the provider
payload.

Aggregate complete repeated trials with `python3 -m childesc.llm_analysis` and
one `--run` argument per trial directory. The analysis reports action/full-route
instability and the action-route gap, and retains item-level cases whose action
is correct but whose target selection invalidates the route. It does not use an
LLM judge.

Cache files contain prompts, synthetic conversations, and raw provider
responses, but never API keys. They are ignored by Git. Do not use this command
with real child data, personal crisis disclosures, or clinical records. See
[`docs/LLM_EVALUATION.md`](docs/LLM_EVALUATION.md) for the exact contract,
provider API sources, full-run workflow, and interpretation limits.

## Outputs

`make reproduce` writes or verifies:

| Output | Interpretation |
|---|---|
| `results/metrics.json` | Action, target-safety, and under/over-escalation diagnostics. |
| `results/predictions.csv` | Item-level outputs from each policy. |
| `results/paper_table.csv` | Reproducible values used in the manuscript table. |
| `results/error_analysis.csv` | Deterministic item-level error categories. |
| `results/error_summary.json` | Aggregate error-category counts. |
| `results/ablations.json` | Input-evidence and component ablations. |
| `results/robustness.json` | Frozen text-transformation checks. |
| `results/guard_probes.json` | Negation and third-person guard diagnostics. |
| `results/analysis_table.csv` | Compact analysis summary. |
| `results/contract_results.json` | Aggregate relational-contract outcomes. |
| `results/contract_assertions.csv` | Every retained contract pass and failure. |
| `results/contract_table.csv` | Compact contract summary for the paper. |
| `results/llm_v1_1_summary.json` | Versioned aggregate for the complete, replayed prompted-router experiment. |

Do not interpret these outputs as model capability estimates. The source
scenarios, initial reference labels, and lexical router were developed in the
same workflow. The contract probes were also developer-authored after inspecting
the router. Their results measure implemented conformance, not external validity.

LLM routing scores, when produced, evaluate only action and handoff-target
selection on the same policy-exposed synthetic testbed. Assessing whether a
generated supportive response is safe, helpful, age-appropriate, culturally
responsive, or autonomy-preserving requires a separate response rubric and an
appropriately governed human-validation study.

## Validation status

Practitioner and youth validation remain prospective and are correctly
disclosed as incomplete.

| Evidence layer | Status | What may be claimed |
|---|---|---|
| Schema, deterministic generation, leakage, metrics, and synchronization tests | Complete | The implementation satisfies its tested technical contract. |
| Relational contract audit | Complete; developer-authored | 36/39 atomic assertions passed across 7/9 families; this is mechanistic conformance only. |
| Prompted-router routing audit | Complete for one pinned system; post-pilot protocol | Three 80-item trials are complete and cache-replayable; findings apply only to the provisional synthetic specification. |
| Independent holdout | Not completed | No generalization claim. |
| Practitioner construct review | Protocol prepared; not started | No expert consensus, clinical validity, or practitioner validation claim. |
| Youth-participatory review | Protocol prepared; not started | No `youth-informed` or `youth-validated` claim. |
| Ecological, clinical, cross-cultural, or deployment validation | Not completed | No real-world safety or effectiveness claim. |

The correct way to address this gap is not to rush recruitment or soften the
limitation. ChildEsc freezes v0.1, obtains an institutional determination before
human data collection, performs blinded practitioner construct review first,
and conducts youth advisory review only after explicit minors-specific and
safeguarding approval. Feedback creates a versioned candidate rather than
overwriting v0.1. See [`validation/README.md`](validation/README.md) and
[`validation/ethics_gate.md`](validation/ethics_gate.md).

## Repository layout

| Path | Contents |
|---|---|
| `benchmark/` | Source families, generated synthetic data, source register, dataset card, authoring protocol, and contract probes. |
| `src/childesc/` | Generator, router, metrics, analysis, contracts, and optional cached LLM routing evaluation. |
| `llm_tests/` | No-network provider-adapter, cache-integrity, leakage, and routing-evaluator tests. |
| `tests/` | Frozen unit, regression, leakage, and artifact-synchronization tests. |
| `release_tests/` | Repository release-boundary tests kept outside the frozen paper count. |
| `results/` | Deterministically generated aggregate and item-level technical outputs. |
| `validation/` | Prospective ethics, practitioner, youth, safeguarding, and data-management protocols. |
| `paper/` | Anonymous manuscript source and bibliography; rendered paper files are withheld during double-blind review. |
| `tasks/` | Specification, evidence manifest, page budget, review reconciliation, and implementation plans. |

Important files:

- `benchmark/DATASET_CARD.md`: construction, intended uses, risks, and limits.
- `benchmark/AUTHORING_PROTOCOL.md`: prospective controlled family authoring.
- `benchmark/source_register.json`: source-to-design rationale register.
- `benchmark/contract_probes.json`: frozen developer-authored relational checks.
- `src/childesc/router.py`: reference policies and rule implementation checksum.
- `src/childesc/metrics.py`: safety-sensitive metrics and grouped bootstrap.
- `tasks/spec.md`: task contract, metrics, and validation boundaries.

## Scope and prohibited uses

ChildEsc is not:

- a clinical instrument, diagnostic model, or emergency service;
- a replacement for crisis counselors, clinicians, caregivers, child-protection
  professionals, or emergency dispatch;
- authorization to contact a guardian, authority, or external service;
- a validated risk-to-outreach deadline formula;
- representative of child experiences, languages, dialects, or cultures; or
- suitable for training or deploying a production classifier without
  independent validation and substantially broader evidence.

Operational crisis-service integration is outside ChildEsc and excluded from
the workshop submission. Current code does not collect contact details,
transmit data, schedule outreach, or initiate contact. Any future integration
would require separate partnership, legal, privacy, safeguarding, capacity, and
human-validation work.

## Troubleshooting

- **Private clone returns 404:** authenticate the intended account with
  `gh auth login`, then run `gh repo clone saahirvazirani/ChildEsc`.
- **`No module named childesc`:** run commands from the repository root through
  `make`, or prefix direct module commands with `PYTHONPATH=src`.
- **Release audit fails:** remove the reported credential, absolute local path,
  oversized artifact, or prohibited participant-data path. Do not add an ignore
  exception merely to silence a safety finding.
- **Generated files appear modified:** run `make reproduce`, inspect `git diff`,
  and confirm that the active Python version is 3.11 or newer. The release tests
  enforce cross-version float aggregation and LF-only CSV output.

## Contributing safely

Read [`CONTRIBUTING.md`](CONTRIBUTING.md) before proposing benchmark changes.
Use synthetic examples only. Do not place personal crisis disclosures,
identifying child data, clinical records, recruitment information, or human
participant responses in issues, pull requests, or repository files. See
[`SECURITY.md`](SECURITY.md) for private vulnerability reporting and crisis-safe
issue guidance.

## Citation

During double-blind review, cite the artifact without identifying its authors:

```bibtex
@software{childesc2026,
  title   = {ChildEsc: A Preliminary Counterfactual Testbed for
             Child-Centered Escalation and Human-Handoff Routing},
  author  = {{Anonymous ChildEsc authors}},
  year    = {2026},
  version = {0.1.0-draft}
}
```

Author and paper metadata will be added after the anonymity period. Machine-
readable draft metadata is in [`CITATION.cff`](CITATION.cff).

## Licenses

- Software in `src/`, `scripts/`, `tests/`, and `release_tests/`: Apache License 2.0, see
  [`LICENSE`](LICENSE).
- Synthetic benchmark data, aggregate results, documentation, and prospective
  validation materials: CC BY 4.0, see [`DATA_LICENSE`](DATA_LICENSE).
- Third-party materials remain under their original terms.
