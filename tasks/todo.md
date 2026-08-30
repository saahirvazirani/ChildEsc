# ChildEsc Four-Page Revision Task List

## Task 1: Record the workshop page policy

**Description:** Record the authoritative four-page rule and create a page ledger for the main paper and excluded sections.

**Acceptance criteria:**
- [x] The four-page content maximum, reference exclusion, unlimited appendix, anonymity, and `dblblindworkshop` requirements are recorded.
- [x] Each main-paper section has a page allocation.

**Verification:**
- [x] Compile the official template and record the first reference page.
- [x] Confirm the workshop wording against the saved rule.

**Dependencies:** None

**Files likely touched:**
- `tasks/page_budget.md`
- `paper/main.tex`

**Estimated scope:** Small: 1-2 files

## Task 2: Freeze the technical evidence

**Description:** Create a version manifest before new analysis, external review, or manuscript revision can influence the artifact.

**Acceptance criteria:**
- [x] Benchmark source, generated data, router, tests, metrics, and paper table have recorded hashes.
- [x] Freeze date and post-freeze change policy are explicit.
- [x] Existing outputs reproduce before the freeze.

**Verification:**
- [x] `make reproduce` passes all tests.
- [x] Hash verification succeeds from a clean extraction.

**Dependencies:** Task 1

**Files likely touched:**
- `tasks/evidence_manifest.md`
- `README.md`

**Estimated scope:** Small: 1-2 files

## Task 3: Resolve the ethics route

**Description:** Determine what practitioner and youth activities are permissible before recruitment or data collection.

**Acceptance criteria:**
- [x] The absence of an institutional determination or approved collaborator route is documented.
- [x] Permitted populations, activities, data handling, and reporting terms are explicit.
- [x] Because youth participation is not covered, pre-submission recruitment is prohibited.

**Verification:**
- [ ] A qualified human confirms the route before participant contact.
- [x] Planned manuscript terminology matches the permitted evidence.

**Dependencies:** None

**Files likely touched:**
- `validation/ethics_gate.md`
- `validation/data_management_plan.md`

**Estimated scope:** Small: 1-2 files

## Checkpoint: Governance

- [x] Tasks 1-3 are complete for the no-recruitment route.
- [x] Technical evidence is frozen.
- [x] No participant recruitment has occurred outside the documented route.
- [ ] A human has approved proceeding to any validation activity.

## Task 4: Prepare the practitioner review packet

**Description:** Define structured review of escalation labels, target constraints, missing context, feasibility, and jurisdictional ambiguity.

**Acceptance criteria:**
- [x] The rubric separates label validity, handoff feasibility, and wording concerns.
- [x] Reviewer expertise, independence, and conflicts are captured.
- [x] Disagreement and pre-review labels are retained.

**Verification:**
- [x] Dry-run the packet on synthetic examples without collecting study data.
- [x] Every response field maps to a planned analysis.

**Dependencies:** Tasks 2 and 3

**Files likely touched:**
- `validation/practitioner_protocol.md`
- `validation/practitioner_rubric.csv`
- `validation/practitioner_analysis_plan.md`

**Estimated scope:** Medium: 3 files

## Task 5: Prepare the youth-participatory protocol

**Description:** Specify age-appropriate review of realism, agency, accessibility, perceived coercion, and handoff framing without soliciting personal disclosures.

**Acceptance criteria:**
- [x] Consent/assent, safeguarding, opt-out, compensation, privacy, and distress procedures are specified.
- [x] Prompts prohibit eliciting personal crisis or abuse experiences.
- [x] Youth perspectives remain distinct from practitioner judgments.

**Verification:**
- [ ] Safeguarding and ethics reviewers approve materials before recruitment.
- [x] Without approval, the protocol remains prospective and no data are collected.

**Dependencies:** Task 3

**Files likely touched:**
- `validation/youth_protocol.md`
- `validation/youth_rubric.md`
- `validation/safeguarding_plan.md`

**Estimated scope:** Medium: 3 files

## Task 6: Add reproducible failure analysis

**Description:** Add item-level error categories, component ablations, and pre-specified robustness checks, with detailed outputs placed in the appendix.

**Acceptance criteria:**
- [x] Action and target errors are categorized deterministically.
- [x] Ablations cover accumulation, negation/third-person guards, and implicated-adult inference.
- [x] Robustness transformations are frozen before evaluation and not used for tuning.

**Verification:**
- [x] Focused analysis tests pass.
- [x] `make reproduce` generates every new table.
- [x] Paired counts and uncertainty match hand-checked fixtures.

**Dependencies:** Task 2

**Files likely touched:**
- `src/childesc/analysis.py`
- `tests/test_analysis.py`
- `results/error_analysis.csv`
- `results/ablations.json`
- `Makefile`

**Estimated scope:** Medium: 5 files

## Task 7: Create an independent holdout if feasible

**Execution status:** Not feasible in the current authoring context because every available author and coding agent has inspected the router or failures. A sealed future-author packet is provided; no holdout result is fabricated.

**Description:** Use an independent author, blind to router rules and item-level failures, to create lexically distinct families after the v0.1 freeze.

**Acceptance criteria:**
- [ ] Holdout authors do not inspect the router or failure list.
- [ ] Holdout text is never used to modify the router.
- [ ] Provenance and separation from v0.1 are documented.

**Verification:**
- [ ] Schema and content-safety tests pass.
- [ ] Leakage audit finds no copied scenario text.
- [ ] Results are reported separately from policy-exposed diagnostics.

**Dependencies:** Tasks 2 and 3

**Files likely touched:**
- `benchmark/holdout_families.json`
- `benchmark/childesc_holdout.jsonl`
- `benchmark/HOLDOUT_CARD.md`
- `tests/test_holdout.py`

**Estimated scope:** Medium: 4 files

## Checkpoint: Evidence

- [x] Technical analyses reproduce without modifying the frozen router.
- [x] No human results are included because no approved protocol was completed.
- [x] All denominators, exclusions, disagreements, and missing data are documented.

## Task 8: Revise the four-page paper and appendix

**Description:** Use the remaining main-paper space for concise failure analysis and stronger closest-work positioning while moving full technical and validation detail into the unlimited appendix.

**Acceptance criteria:**
- [x] Main content is at most four pages.
- [x] Contribution, method, main result, and central validity warning remain in the main paper.
- [x] Every empirical statement traces to frozen technical evidence; no completed validation is claimed.

**Verification:**
- [x] Paper-table synchronization and stale-claim tests pass.
- [x] References begin on page five after the fourth-page revision.
- [x] An independent reviewer can identify scope, novelty, evidence, and limitations from the main paper alone.

**Dependencies:** Tasks 4-7, using only work that passes its evidence gate

**Files likely touched:**
- `paper/main.tex`
- `paper/manuscript.md`
- `paper/references.bib`
- `tests/test_artifacts.py`

**Estimated scope:** Medium: 4 files

## Task 9: Run final adversarial and submission QA

**Description:** Reconcile a fresh issues-only review, compile the official paper, and rebuild the anonymous reproducibility package.

**Acceptance criteria:**
- [x] Confirmed methodological defects are repaired or bounded explicitly.
- [x] PDF and DOCX render cleanly and remain anonymous.
- [x] The supplement reproduces all reported technical results in a clean directory.

**Verification:**
- [x] `make reproduce` passes from the anonymous ZIP.
- [x] Every final page is visually inspected.
- [x] Identity, template-placeholder, citation, and unsupported-claim scans are clean.

**Dependencies:** Task 8

**Files likely touched:**
- `tasks/review_reconciliation.md`
- `paper/ChildEsc_Workshop_Paper.pdf`
- `paper/ChildEsc_Workshop_Paper.docx`
- `paper/childesc_anonymous_supplement.zip`

**Estimated scope:** Medium: 4 files

## Final Checkpoint

- [x] Main content is at most four pages.
- [x] Human-validation wording matches the evidence actually collected.
- [x] Technical claims are reproducible; no human evidence is reported.
- [x] The anonymous package is visually clean and ready for submission.

## Fourth-Page Revision Tasks

### Task 10: Freeze the acceptance-oriented claim architecture

- [x] Verify workshop topics, page rule, and evaluation priority from the workshop site.
- [x] Record the B3 open-problem mapping without implying that ChildEsc solves AIG-CSAM assessment.
- [x] Add the newly released CARE-Bench triage benchmark to the novelty audit.
- [x] Define terms that are allowed and prohibited before independent validation.

### Task 11: Add source traceability and an authoring protocol

- [x] Create a dated source register that maps sources to bounded design decisions.
- [x] Map all v0.1 families to domain-level rationale and disclose that the mapping is retrospective.
- [x] Specify controlled authoring fields, counterfactual isolation, content-safety rules, and independent-review gates.
- [x] Verify that no source is represented as item-level clinical ground truth.

### Task 12: Add a post-freeze relational contract audit

- [x] Write failing unit tests for contract validation and scoring.
- [x] Freeze matched probe definitions before first router execution.
- [x] Implement the evaluator without modifying `router.py`.
- [x] Export item-level assertions and aggregate results from `make reproduce`.
- [x] Retain and report failures; do not tune the router on probe results.

### Task 13: Use the fourth content page

- [x] Add CARE-Bench to related work and narrow the novelty claim.
- [x] Add a compact contract-audit table and supported-use statement.
- [x] Tie the contribution directly to the workshop's restricted-data evaluation and deployment-safeguard themes.
- [x] Keep human validation prospective and preserve the no-deployment claim.
- [x] Compile with references beginning on page five.

### Task 14: Final adversarial and artifact QA

- [x] Run all tests in the working tree and repeat the full 46-test reproduction from the final supplement.
- [x] Run a fresh Gemini issues-only review and reconcile findings by evidence category.
- [x] Inspect every PDF and DOCX page and run accessibility checks.
- [x] Rebuild, inspect, and clean-room reproduce the anonymous supplement.
- [x] Scan for identity, unsupported claims, stale counts, and local paths.

### Task 15: Bound the proposed delegated 988 follow-up extension

- [x] Verify current 988 follow-up, consent, confidentiality, and health-data guidance from official sources.
- [x] State that 988 has not agreed to the proposal and that no 1-24 hour cutoff is validated.
- [x] Exclude imminent danger from a delayed queue and preserve immediate, least-invasive crisis support.
- [x] Require a formal service partnership, separate age-appropriate affirmative consent, human review, minimum-necessary transfer, capacity guarantees, and prospective harm evaluation.
- [x] Add a machine-readable safe-default specification and regression tests that prohibit current transmission or outreach.

## GitHub Staging Release and Validation Checklist

### Phase 1: Release Boundary

- [x] Task 16: Approve `saahirvazirani/ChildEsc` as a private-first repository.
- [x] Task 16: Approve code and data/documentation licenses.
- [x] Task 16: Approve the tracked-file include/exclude manifest.
- [x] Task 17: Add `.gitignore`, `.gitattributes`, and crisis-safe `SECURITY.md`.
- [x] Task 17: Scan candidate files for secrets, identity leaks, local paths, large files, and build debris.

### Checkpoint: Release Boundary

- [x] Private-first, license, and artifact-boundary decisions are recorded.
- [x] Anonymous submission artifacts contain no GitHub identity or remote URL.
- [x] No participant data or recruitment records exist in the repository.

### Phase 2: Usable Research Artifact

- [x] Task 18: Expand README with installation, quickstart, command reference, outputs, interpretation, citation, and troubleshooting.
- [x] Task 18: Add an explicit validation-status table with practitioner and youth validation marked `not started`.
- [x] Task 18: Add `CITATION.cff`, `CONTRIBUTING.md`, and `CHANGELOG.md`.
- [x] Task 19: Add GitHub Actions CI for `make reproduce`.
- [x] Task 19: Add and test an automated release audit.
- [x] Task 19: Re-run the current 46-test reproduction locally.

### Checkpoint: Reproducible Artifact

- [x] A clean extraction follows only the README and reproduces all outputs.
- [x] Technical validation is distinguished from construct, ecological, clinical, cross-cultural, and deployment validation.
- [x] Protocol-only files cannot be mistaken for completed human validation.

### Phase 3: Private GitHub Staging

- [x] Task 20: Re-authenticate `gh` for the intended account.
- [x] Task 20: Rename the local default branch to `main`.
- [x] Task 20: Stage only approved files and inspect the complete diff.
- [x] Task 20: Create atomic initial commit(s) with no secrets or build debris.
- [x] Task 20: Create private `saahirvazirani/ChildEsc` and push `main`.
- [x] Task 20: Verify the hosted file set, private visibility, clean clone, and CI run.
- [x] Task 21: Keep the repository private until the double-blind anonymity gate clears.
- [ ] Task 21: Tag public v0.1 only as a preliminary synthetic testbed after release approval.

### Phase 4: Prospective Human Validation

- [ ] Task 22: Obtain a qualified institutional determination before any recruitment or response collection.
- [ ] Task 22: Record consent, safeguarding, compensation, retention, withdrawal, and incident requirements.
- [ ] Task 23: Freeze practitioner materials and analysis before responses are inspected.
- [ ] Task 23: Conduct blinded practitioner construct review only after authorization.
- [ ] Task 23: Preserve disagreement and create a versioned v0.2 candidate rather than overwriting v0.1.
- [ ] Task 24: Obtain explicit minors approval and safeguarding sign-off before youth recruitment.
- [ ] Task 24: Conduct advisory sessions without eliciting personal crisis, abuse, or self-harm disclosures.
- [ ] Task 24: Keep youth experience judgments distinct from clinical and legal safety judgments.
- [ ] Task 25: Publish only de-identified aggregate findings and traceable version changes.
- [ ] Task 25: Keep therapeutic, clinical, cross-cultural, and deployment claims out of scope.

### Final Checkpoint

- [x] Private GitHub staging repository is clean, documented, and reproducible.
- [ ] Any public release is cleared for workshop anonymity and licensing.
- [x] Validation claims match completed evidence exactly.
- [x] GitHub contains no participant-level sensitive data, contact information, or crisis disclosures.

## Provider-Neutral LLM Evaluation Checklist

### Phase 1: Contract and Test Specification

- [x] Task 26: Verify current structured-output request shapes from official
  Gemini, OpenAI, Anthropic, and OpenRouter documentation.
- [x] Task 26: Freeze a provider-neutral routing prompt and strict JSON Schema.
- [x] Task 26: Add failing tests for request parity, response parsing, and label
  isolation without changing the frozen 46-test suite.

### Phase 2: Provider and Cache Implementation

- [x] Task 27: Implement injectable standard-library REST transport and bounded,
  credential-safe errors.
- [x] Task 27: Implement Gemini, OpenAI, Anthropic, and OpenRouter adapters.
- [x] Task 28: Implement content-addressed response caching with atomic writes.
- [x] Task 28: Prove cache-only replay requires neither credentials nor network.

### Phase 3: Routing-Only Evaluation

- [x] Task 29: Implement the LLM routing evaluator and CLI.
- [x] Task 29: Record invalid outputs and provider failures without dropping
  benchmark items from metric denominators.
- [x] Task 29: Export prompt/schema hashes, provider/model settings, cache
  telemetry, predictions, and routing metrics.

### Phase 4: Documentation and Verification

- [x] Task 30: Document Gemini, OpenAI, Anthropic, and OpenRouter usage and safe
  cost-limited smoke tests.
- [x] Task 30: State that supportive-response quality is outside scope and needs
  a separate rubric plus human validation.
- [x] Task 30: Run LLM tests, frozen scientific tests, release tests, full
  reproduction, and a fresh code review.

## Acceptance-Maximization Checklist

## Task 31: Freeze the reviewer-facing thesis

**Description:** Lock ChildEsc as a works-in-progress audit of whether prompted
child-facing model routers choose both a proportionate escalation action and a
context-safe recipient. Write one explicit chain from phenomenon to task,
items, metrics, and permitted claims before adding new evidence.

**Acceptance criteria:**
- [x] The title-level contribution is safe-recipient routing, not ordinal labels
  or action timing alone.
- [x] Permitted and prohibited claims are recorded in one source of truth.
- [x] The page ledger reserves one main table and one concise failure example.

**Verification:**
- [x] Manual check: a fresh reader can state the paper's unique question after
  reading only the proposed title, abstract skeleton, and contribution list.
- [x] Search check: no planning text calls the benchmark validated, realistic,
  clinical, representative, or deployment-ready.

**Dependencies:** Task 30

**Files likely touched:**
- `tasks/acceptance_claims.md`
- `tasks/page_budget.md`
- `paper/main.tex`
- `paper/manuscript.md`

**Estimated scope:** Medium: 4 files

## Task 32: Freeze the model evaluation protocol

**Description:** Pre-register the exact provider model IDs, three-trial design,
generation settings, completion and retry policy, primary estimands, statistical
analysis, result-inspection rule, and fallback ladder before any full live run.

**Acceptance criteria:**
- [x] The manifest names exact model IDs and records whether each ID is a pinned
  snapshot, stable release, preview, or provider-routed alias.
- [x] Primary metrics include under-escalation, urgent recall, strict target
  validity, action-route gap, implicated-adult unsafe-target rate, and exact
  route accuracy with explicit denominators.
- [x] The protocol states that prompt, schema, labels, and primary analysis will
  not be changed after results are inspected.

**Verification:**
- [x] Hash check: benchmark, prompt, schema, protocol, and analysis-plan hashes
  are written to the experiment manifest.
- [x] Manual check: unavailable models or credentials map to a documented
  fallback rather than an unrecorded substitution.

**Dependencies:** Task 31

**Files likely touched:**
- `tasks/llm_evaluation_protocol.md`
- `experiments/llm_manifest.json`
- `tasks/evidence_manifest.md`

**Estimated scope:** Medium: 3 files

## Conditional Task 32A: Seal an independently authored holdout

**Status:** Skipped at the protocol freeze because no eligible unexposed author
is documented. No holdout is reported.

**Description:** If an eligible adult collaborator is available by the protocol
freeze, have that person create a small set of counterfactual families without
access to the current scenarios, labels, router, prompt, or item-level errors.
This is an artifact-authoring collaboration, not practitioner or youth
validation. If the independence boundary cannot be documented, record the gate
failure and skip the task.

**Acceptance criteria:**
- [ ] The collaborator's non-exposure to the current policy and item set is
  documented before authoring begins.
- [ ] The authoring packet fixes the schema, safety restrictions, source
  rationale, and family-level split without revealing current lexical cues.
- [ ] The sealed set is evaluated once after the primary protocol is frozen and
  is never used to tune the prompt, router, labels, or model settings.

**Verification:**
- [ ] Independence check: the author signs the existing exposure checklist and
  has not received current item text, predictions, or rules.
- [ ] Structural tests pass on the sealed families before any model output is
  inspected.
- [x] Manual check: if eligibility fails, the paper says no independently
  authored holdout is reported.

**Dependencies:** Task 32 and an eligible unexposed collaborator

**Files likely touched:**
- `validation/holdout_author_packet.md`
- `benchmark/holdout_manifest.json`
- `data/controlled/`
- `tasks/evidence_manifest.md`

**Estimated scope:** Medium: 4 files, conditional

## Checkpoint: Protocol Freeze

- [x] Tasks 31-32 and the Task 32A eligibility decision are reviewed and
  approved before any full provider run.
- [x] No full prompted-model run output has been inspected; existing
  deterministic checksum results remain explicitly policy-exposed.
- [x] Provider data terms and raw-response release constraints are recorded.
- [ ] Cost and credential availability are confirmed for at least one primary
  model.

## Task 33: Add auditable independent trials

**Description:** Extend the routing evaluator with an explicit trial identifier
and append-only attempt ledger so three identical visible requests create three
auditable provider attempts rather than one cache entry reused three times.

**Acceptance criteria:**
- [x] Trial identity is part of cache provenance but not leaked into the visible
  child conversation or routing instructions.
- [x] Every provider attempt records status, timestamp, request hash, response
  hash, bounded error, and returned model metadata without credentials.
- [x] Cache-only replay reconstructs each trial and fails closed on any missing
  or altered entry.

**Verification:**
- [x] Tests pass: `make llm-test`.
- [x] Regression test: three trial IDs produce three transport calls online and
  zero transport calls during complete replay.
- [x] Regression test: the serialized provider body contains no trial ID or
  benchmark label.

**Dependencies:** Task 32

**Files likely touched:**
- `src/childesc/llm.py`
- `src/childesc/llm_evaluate.py`
- `llm_tests/test_cache.py`
- `llm_tests/test_llm_evaluate.py`

**Estimated scope:** Medium: 4 files

## Task 34: Execute complete prompted-router audits

**Status:** Completed for one pinned prompted router under post-pilot protocol
v1.1.1. Historical v1.0.1 failures are retained and unscored.

**Description:** Run a four-item smoke test for each available direct provider,
inspect payload isolation and structured outputs, then execute three complete
80-item trials per frozen primary model. OpenRouter remains a portability smoke
test unless upstream provenance is pinned.

**Acceptance criteria:**
- [x] Every reported model has the protocol-required number of complete trials,
  or the manuscript uses the pre-registered fallback and discloses the reason.
- [x] Raw attempts and normalized predictions account for every item without
  selective exclusion or silent response repair.
- [x] Exact provider, model, returned model version, prompt/schema hashes,
  settings, timestamps, and cache hashes are present in each run manifest.

**Verification:**
- [x] Live smoke commands finish with valid two-field routes for four items.
- [x] Full-run cache-only commands finish without API keys or network access.
- [x] Manual check: invalid output and provider-error counts reconcile with the
  attempt ledger.

**Dependencies:** Task 33 and configured provider credentials

**Files likely touched:**
- `experiments/llm_manifest.json`
- `results/llm/`
- `.cache/childesc/`

**Estimated scope:** Medium: generated experiment artifacts

## Task 35: Analyze the action-route gap and stability

**Description:** Add deterministic analysis for action-correct but target-wrong
handoffs, the action-accuracy versus exact-route gap, implicated-adult target
errors, three-trial instability, and paired family-bootstrap differences.

**Acceptance criteria:**
- [x] Every primary metric has an explicit denominator and item-level audit
  trail.
- [x] Trial results are summarized without treating repeated outputs from the
  same 80 items as independent observations.
- [x] Model-to-model differences are paired by family and presented as
  descriptive intervals rather than winner claims.

**Verification:**
- [x] Tests pass: `make llm-test` and `make test`.
- [x] Reproduction check: deleting generated summaries and rerunning analysis
  recreates byte-stable tables from cached normalized outputs.
- [x] Manual check: action-route-gap counts equal action-correct target-failure
  counts under the documented metric definition.

**Dependencies:** Task 34

**Files likely touched:**
- `src/childesc/llm_analysis.py`
- `llm_tests/test_llm_analysis.py`
- `results/llm/summary.json`
- `results/llm/paper_table.csv`

**Estimated scope:** Medium: 4 files

## Checkpoint: Evidence Integrity

- [x] Tasks 33--35 pass all focused and frozen tests; Task 34 reports three
  complete v1.1.1 trials while retaining the incomplete v1.0.1 history.
- [x] All proposed paper values replay from cache without credentials.
- [x] No prompt, label, model setting, or primary metric changed after v1.1
  inspection.
- [x] Any deviation from the frozen protocol is logged and kept out of primary
  claims unless the entire affected analysis is rerun under a new version.

## Task 36: Rewrite the title and abstract around one finding

**Description:** Make the safe-recipient question the title-level hook and
rewrite the abstract after evidence freeze to include the narrow construct, the
model-audit setup, one concrete action-route-gap finding, and the validation
boundary.

**Acceptance criteria:**
- [x] The title distinguishes ChildEsc from refusal and action-only benchmarks.
- [x] The abstract reports only results regenerated from frozen artifacts.
- [x] The final sentence states that practitioner and youth validation have not
  occurred and blocks deployment interpretation.

**Verification:**
- [x] Manuscript synchronization tests cover every abstract number.
- [x] Manual check: the abstract contains problem, gap, method, result,
  contribution, and limitation without a model-ranking claim.

**Dependencies:** Task 35

**Files likely touched:**
- `paper/main.tex`
- `paper/manuscript.md`
- `scripts/build_paper_docx.py`
- `tests/test_artifacts.py`

**Estimated scope:** Medium: 4 files

## Task 37: Replace checksum breadth with model evidence

**Description:** Replace the three-rule main table with a compact table showing
available prompted model routers plus the frozen checksum. Center the columns on
under-escalation, urgent recall, target validity, action-route gap, unsafe
targets, and exact routing; move diagnostic baselines and full intervals to the
appendix.

**Acceptance criteria:**
- [x] The main table has no more than the columns needed to support the central
  claim and remains legible at the official template size.
- [x] One concise example shows how an action-correct route can still select an
  inappropriate recipient.
- [x] Keyword, severity-agnostic, stress-test, and full contract details remain
  reproducible in the appendix rather than being deleted.

**Verification:**
- [x] Build succeeds with the NeurIPS 2026 `dblblindworkshop` option.
- [x] Visual check: table text and the failure example are readable at 100%.
- [x] Data check: every table cell is derived from the frozen result files.

**Dependencies:** Tasks 35-36

**Files likely touched:**
- `paper/main.tex`
- `paper/manuscript.md`
- `scripts/build_paper_docx.py`
- `tests/test_artifacts.py`

**Estimated scope:** Medium: 4 files

## Task 38: Rebalance page four for workshop discussion

**Description:** Use the final content page for construct limitations,
actionable impact, and four precise workshop questions. Keep the detailed
validation protocol prospective and remove the delegated-outreach mechanism
from the complete submission package.

**Acceptance criteria:**
- [x] The main text names practitioner and youth validation as incomplete and
  does not imply a hotline partnership or operational referral pathway.
- [x] Four discussion questions address clarification or abstention, separate
  practitioner and youth judgments, jurisdictional constraints, and evidence
  before operational handoff.
- [x] References begin on page five without changing template margins, font
  sizes, or spacing.

**Verification:**
- [x] Compile and inspect all four content pages and the first reference page.
- [x] Phrase scan finds no unsupported 988 policy, validated cutoff, automated
  outreach, or deployment-readiness statement in the main paper.
- [x] Appendix cross-references remain correct.

**Dependencies:** Task 37

**Files likely touched:**
- `paper/main.tex`
- `paper/manuscript.md`
- `tasks/page_budget.md`
- `scripts/build_paper_docx.py`

**Estimated scope:** Medium: 4 files

## Checkpoint: Reviewer Read

- [x] Tasks 36-38 produce a self-contained four-page paper.
- [x] A fresh reader identifies the construct, available diagnostic evidence, strongest
  failure, and evidence boundary from the title, abstract, and main table.
- [x] Closest-work text distinguishes ChildEsc from CAREBench, KIDBench,
  MinorBench, MindEval, and CARE-Bench without novelty overreach.
- [x] The appendix adds reproducibility depth but is not needed to discover the
  central contribution.

## Task 39: Obtain independent editorial reviews

**Description:** After the evidence freeze, request an issues-only review from
one benchmark methodologist and, if available, one youth-facing practitioner.
Treat feedback as manuscript review, not participant data or empirical
validation, unless an appropriate approved study route exists.

**Acceptance criteria:**
- [ ] Reviewers receive the same frozen anonymous paper and a request focused on
  construct validity, target safety, claims, and actionable ambiguity.
- [ ] No practitioner quote, score, demographic, or response is analyzed or
  reported as research evidence.
- [ ] Reviewer conflicts and access to the benchmark or router are recorded for
  internal reconciliation.

**Verification:**
- [ ] Manual check: the manuscript still states that practitioner and youth
  validation have not occurred.
- [ ] Review files are excluded from the anonymous submission unless explicitly
  cleared and necessary.

**Dependencies:** Task 38

**Files likely touched:**
- `tasks/external_review_log.md`
- `tasks/review_reconciliation.md`

**Estimated scope:** Small: 2 files

## Task 40: Reconcile findings without post-hoc expansion

**Description:** Classify independent findings as confirmed validity defects,
plausible reviewer concerns, or optional improvements. Repair confirmed defects
and only high-value concerns that do not alter the frozen primary evaluation;
defer attractive new experiments that would create post-hoc validity risk.

**Acceptance criteria:**
- [ ] Every accepted change has a finding classification and evidence trail.
- [ ] Changes to prompt, labels, model set, or primary analysis trigger the
  pre-registered redesign rule rather than silent reruns.
- [ ] Optional breadth additions are deferred unless they directly protect the
  central claim and fit the page and evidence budget.

**Verification:**
- [ ] Tests pass: `make reproduce`, `make llm-test`, and `make release-test`.
- [ ] Manual check: all reviewer findings are closed, bounded in limitations, or
  explicitly deferred.

**Dependencies:** Task 39

**Files likely touched:**
- `tasks/review_reconciliation.md`
- `paper/main.tex`
- `paper/manuscript.md`
- `tests/test_artifacts.py`

**Estimated scope:** Medium: 4 files

## Task 41: Build and audit the anonymous submission package

**Status:** Completed for the v1.1.1 aggregate and prompted-result manuscript
revision. Raw provider responses remain outside the anonymous repository.

**Description:** Produce the final PDF and anonymous supplement, replay model
results in a clean environment, and audit page limits, identity, secrets,
provider terms, local paths, stale outputs, and unsupported claims.

**Acceptance criteria:**
- [x] Main content is at most four pages and references begin on page five.
- [x] The anonymous supplement reproduces all paper values from synthetic data
  and permitted cached or normalized model outputs without network credentials.
- [x] No username-linked repository URL, author identity, API key, PII, real
  child disclosure, or unapproved raw provider response is present.

**Verification:**
- [x] Tests pass: `make reproduce`, `make llm-test`, `make release-test`, and
  `make release-audit`.
- [x] Clean-room check: extract the anonymous archive and reproduce all tables.
- [x] Visual check: inspect every PDF page for clipping, overflow, anonymity,
  and reference boundaries.

**Dependencies:** Task 40

**Files likely touched:**
- `paper/main.tex`
- `paper/ChildEsc_Workshop_Paper.pdf`
- `scripts/release_audit.py`
- `dist/`

**Estimated scope:** Medium: build and release artifacts

## Final Acceptance Checkpoint

- [x] At least one prompted model router has a complete replayable full result;
  the preferred result is three providers with three trials each.
- [x] The action-route gap and implicated-adult target failures are visible in
  the main paper.
- [x] No supportive-response, model-ranking, clinical, population, hotline-
  partnership, or deployment claim exceeds the completed evidence.
- [x] Practitioner and youth validation remain prospective and are correctly
  disclosed as incomplete.
- [x] The final package is anonymous, four-page compliant, and reproducible.

## Acceptance-Focused Revision Tasks, 2026-08-19

### Task 42: Freeze the claim-evidence matrix

- [x] Map each headline claim to a current versioned result or explicit scope
  boundary.
- [x] Prohibit prevalence, clinical-validity, broad model-safety,
  supportive-response, and deployment interpretations.

### Task 43: Remove delegated follow-up from the submission

- [x] Remove the 988/timed-outreach extension from LaTeX, DOCX, and the
  anonymous supplement.
- [x] Retain `crisis_service` only as a generic target category.
- [x] Keep internal governance notes out of submission packaging rather than
  representing them as paper evidence.

### Task 44: Clarify the safeguard architecture

- [x] Define routing as action-plus-recipient selection.
- [x] Define supportive response generation as a separate, unevaluated layer.
- [x] End with four workshop questions that can guide v0.2 validation.

### Task 45: Preserve human-validation gates

- [x] Record that an institutional determination is required before any
  practitioner recruitment or response collection.
- [x] Keep the proposed 8--12-practitioner full-set blinded audit prospective;
  the frozen base assignment uses eight 30-item packets and three ratings per item.
- [x] Keep youth participation prospective pending separate approval.

### Task 46: Rebuild and audit the submission

- [x] All 49 manuscript/scientific, 25 provider-path, and 5 release tests pass.
- [x] PDF has four content pages and references begin on page five.
- [x] PDF and DOCX render cleanly; anonymous supplement reproduces in a clean
  directory and contains no identity, secret, raw response, operational service
  proposal, or timed-contact material. Public crisis-practice sources may remain
  as bounded design provenance.

# Deadline-Day Acceptance Optimization Tasks, 2026-08-29

These tasks implement the approved deadline-day plan. They do not authorize
implementation until the human checkpoint after Task 49 is reviewed.

## Task 47: Freeze the deadline-day claim and experiment contract

**Description:** Create a v1.2 comparison protocol before any new paid model
call. Preserve ChildEsc v0.1, the routing prompt/schema, current Claude trials,
and the works-in-progress claim boundary. Pre-specify the model families,
settings, primary analyses, inclusion rules, result-dependent claim gates,
execution cutoff, and no-tuning rule.

**Acceptance criteria:**
- [ ] Protocol names Gemini and GPT as construct-replication families selected
  from the earlier manifest, not from ChildEsc scores.
- [ ] Protocol fixes three preferred trials per qualified model, one attempt per
  item, no repair, complete-run gating, a USD 5.00 spend ceiling, and all-result
  disclosure.
- [ ] Claim ledger distinguishes positive-gap replication, heterogeneous
  results, and no-comparator fallbacks without permitting model ranking.

**Verification:**
- [ ] Manual hash check: benchmark, prompt, schema, and current Claude summary
  match their frozen values.
- [ ] Manual review: no paid comparison call predates the v1.2 freeze.
- [ ] Manual review: the current one-system paper remains the protected
  fallback.

**Dependencies:** None

**Files likely touched:**
- `tasks/llm_evaluation_protocol_v1_2.md`
- `tasks/acceptance_claims.md`
- `experiments/llm_manifest.json`

**Estimated scope:** Medium: 3 files

## Task 48: Snapshot exact OpenRouter endpoints and projected cost

**Description:** Query OpenRouter's public model and endpoint metadata before
correctness-bearing calls. Freeze the exact Gemini and GPT request slugs,
first-party provider slugs, returned-model identity rules, structured-output
support, reasoning controls, public pricing, and worst-case projected spend.
Document explicitly that the earlier dated direct-provider GPT identifier is
not silently equivalent to a dynamic OpenRouter alias.

**Acceptance criteria:**
- [ ] Each candidate has a dated metadata snapshot with raw-response hash,
  supported parameters, endpoint provider, request slug, and identity gate.
- [ ] Each endpoint supports strict `response_format`; fallback routing is
  disabled and required parameters are enforced.
- [ ] Projected smoke plus full-trial spend is at most USD 5.00; otherwise the
  affected candidate is stopped before a paid call.

**Verification:**
- [ ] Compare snapshots with OpenRouter's public models/endpoints API.
- [ ] Validate JSON and recompute snapshot SHA-256 values.
- [ ] Manual check: model eligibility is based only on metadata, provenance,
  compatibility, cost, and deadline feasibility.

**Dependencies:** Task 47

**Files likely touched:**
- `experiments/openrouter_gemini_snapshot_2026-08-29.json`
- `experiments/openrouter_gpt_snapshot_2026-08-29.json`
- `tasks/llm_evaluation_protocol_v1_2.md`
- `experiments/llm_manifest.json`

**Estimated scope:** Medium: 4 files

## Task 49: Add target-failure decomposition to cross-system analysis

**Description:** Test-drive a deterministic failure taxonomy for action-correct
handoffs: missing all targets, adding an unpermitted target, emitting a
forbidden target, or combinations of those conditions. Add per-system counts
and rates without changing route validity, benchmark labels, or existing
metrics.

**Acceptance criteria:**
- [ ] Every action-correct target-invalid row receives one deterministic set of
  atomic failure reasons.
- [ ] Counts reconcile exactly with the existing action-correct target-failure
  numerator for each trial and system.
- [ ] Existing one-system summaries and metric values remain byte-for-byte or
  numerically unchanged except for additive fields.

**Verification:**
- [ ] Tests pass: `python3 -m unittest llm_tests.test_llm_analysis -v`.
- [ ] Tests pass: `make llm-test`.
- [ ] Manual check: failure reasons use only predicted and provisional
  permitted/forbidden target sets, never an LLM judge.

**Dependencies:** Task 47

**Files likely touched:**
- `src/childesc/llm_analysis.py`
- `llm_tests/test_llm_analysis.py`

**Estimated scope:** Small: 2 files

## Checkpoint: Protocol Integrity After Tasks 47-49

- [ ] All focused and provider-path tests pass.
- [ ] No benchmark item, label, router rule, prompt, or current model output
  changed.
- [ ] Exact endpoint identities, spend ceiling, trial count, primary analyses,
  and result-dependent claims are frozen.
- [ ] Human reviews and approves this checkpoint before any new paid call.

## Task 50: Qualify the Gemini comparison through smoke and replay

**Description:** Run the frozen four-item smoke against the qualified Gemini
endpoint, record one append-only attempt per item, and immediately replay the
same four outputs without network access. Do not inspect correctness to decide
whether the system qualifies; qualification depends on completeness, schema,
identity, replay, and cost only.

**Acceptance criteria:**
- [ ] Smoke returns 4/4 valid structured routes with the expected model and
  first-party Google provider identity.
- [ ] Cache-only replay reproduces every normalized decision and response hash.
- [ ] Any invalid output, provider mismatch, timeout, or cost-gate failure stops
  Gemini full trials and remains documented without a score.

**Verification:**
- [ ] Live command exits successfully for the four-item smoke.
- [ ] Equivalent `--cache-only` command exits successfully without an API key.
- [ ] Inspect `attempts.jsonl` for four unique item attempts and no hidden retry.

**Dependencies:** Tasks 48 and 49

**Files likely touched:**
- `results/llm/openrouter-gemini-v1-2/smoke/routing_metrics.json`
- `results/llm/openrouter-gemini-v1-2/smoke/routing_predictions.jsonl`
- `results/llm/openrouter-gemini-v1-2/smoke/attempts.jsonl`
- `experiments/llm_manifest.json`

**Estimated scope:** Medium: 4 generated/provenance files

## Task 51: Qualify the GPT comparison through smoke and replay

**Description:** Run the same frozen four-item smoke against the qualified GPT
endpoint and replay it offline. Apply the pre-frozen alias/returned-model
identity rule; do not create a metadata amendment after seeing correctness.

**Acceptance criteria:**
- [ ] Smoke returns 4/4 valid structured routes with the expected model mapping
  and first-party OpenAI provider identity.
- [ ] Cache-only replay reproduces every normalized decision and response hash.
- [ ] Any invalid output, provider mismatch, timeout, or cost-gate failure stops
  GPT full trials and remains documented without a score.

**Verification:**
- [ ] Live command exits successfully for the four-item smoke.
- [ ] Equivalent `--cache-only` command exits successfully without an API key.
- [ ] Inspect `attempts.jsonl` for four unique item attempts and no hidden retry.

**Dependencies:** Tasks 48 and 49

**Files likely touched:**
- `results/llm/openrouter-gpt-v1-2/smoke/routing_metrics.json`
- `results/llm/openrouter-gpt-v1-2/smoke/routing_predictions.jsonl`
- `results/llm/openrouter-gpt-v1-2/smoke/attempts.jsonl`
- `experiments/llm_manifest.json`

**Estimated scope:** Medium: 4 generated/provenance files

## Checkpoint: Comparator Qualification After Tasks 50-51

- [ ] Each model independently passes or fails the pre-specified smoke gate.
- [ ] Failed candidates are not replaced after outputs are viewed.
- [ ] Qualified candidates replay exactly from cache.
- [ ] Spend remains within the pre-run estimate.

## Task 52: Execute and replay complete Gemini trials

**Description:** If Task 50 qualifies, execute three sequential 80-item Gemini
trials using unique v1.2 trial IDs, then replay each trial from cache. Preserve
all attempts and stop new calls at the deadline-day execution cutoff even if
fewer than three trials complete.

**Acceptance criteria:**
- [ ] Each reported trial has 80/80 valid routes, expected model/provider
  identity, one attempt per item, and no repair.
- [ ] Every complete trial reproduces offline with matching normalized hashes.
- [ ] Incomplete trials remain retained and receive no aggregate score.

**Verification:**
- [ ] Live and cache-only evaluator commands pass for every reported trial.
- [ ] `routing_metrics.json` reports `complete: true`, 80 items, and zero invalid
  outputs/provider errors for every scored trial.
- [ ] Attempt count, provider metadata, cache hit status, and reported cost are
  reconciled against the protocol ledger.

**Dependencies:** Task 50

**Files likely touched:**
- `results/llm/openrouter-gemini-v1-2/trial-1/`
- `results/llm/openrouter-gemini-v1-2/trial-2/`
- `results/llm/openrouter-gemini-v1-2/trial-3/`
- `experiments/llm_manifest.json`

**Estimated scope:** Medium: generated trial artifacts plus one manifest

## Task 53: Execute and replay complete GPT trials

**Description:** If Task 51 qualifies, execute three sequential 80-item GPT
trials using unique v1.2 trial IDs, then replay each trial from cache under the
same completeness and cutoff rules used for Gemini.

**Acceptance criteria:**
- [ ] Each reported trial has 80/80 valid routes, expected model/provider
  identity, one attempt per item, and no repair.
- [ ] Every complete trial reproduces offline with matching normalized hashes.
- [ ] Incomplete trials remain retained and receive no aggregate score.

**Verification:**
- [ ] Live and cache-only evaluator commands pass for every reported trial.
- [ ] `routing_metrics.json` reports `complete: true`, 80 items, and zero invalid
  outputs/provider errors for every scored trial.
- [ ] Attempt count, provider metadata, cache hit status, and reported cost are
  reconciled against the protocol ledger.

**Dependencies:** Task 51

**Files likely touched:**
- `results/llm/openrouter-gpt-v1-2/trial-1/`
- `results/llm/openrouter-gpt-v1-2/trial-2/`
- `results/llm/openrouter-gpt-v1-2/trial-3/`
- `experiments/llm_manifest.json`

**Estimated scope:** Medium: generated trial artifacts plus one manifest

## Task 54: Aggregate, audit, and freeze admissible evidence

**Description:** Aggregate every complete pre-specified system/trial, produce
family-grouped intervals and target-failure decomposition, retain every
incomplete attempt, and freeze a single reviewer-facing result table. Apply the
pre-specified claim gate based on the full evidence rather than selecting a
preferred model subset.

**Acceptance criteria:**
- [ ] Summary includes the frozen Claude trials and every complete Gemini/GPT
  trial with matching benchmark, prompt, and schema hashes.
- [ ] Main metrics reconcile to item-level rows; failure-reason counts reconcile
  to action-correct target failures; repeated calls are not pooled as IID items.
- [ ] Evidence manifest records trial hashes, model/provider identities, costs,
  incomplete attempts, and the permitted result-dependent claim.

**Verification:**
- [ ] Tests pass: `make llm-test`.
- [ ] Run aggregate analysis twice and compare outputs byte-for-byte.
- [ ] Manual claim audit: no model ranking, population estimate, clinical claim,
  or omitted complete pre-specified result.

**Dependencies:** Tasks 49, 52, and 53; a failed comparator task satisfies its
dependency when the documented fallback rule is applied.

**Files likely touched:**
- `results/llm_v1_2_summary.json`
- `results/llm_v1_2_paper_table.csv`
- `results/llm_v1_2_target_failures.csv`
- `tasks/evidence_manifest.md`
- `experiments/llm_manifest.json`

**Estimated scope:** Medium: 5 files

## Checkpoint: Evidence Integrity After Tasks 52-54

- [ ] All reported runs are complete, identity-verified, and cache-replayable.
- [ ] All incomplete attempts are retained and unscored.
- [ ] New spend is at or below USD 5.00.
- [ ] The selected claim is exactly the one authorized by the result gate.
- [ ] Current one-system evidence remains available as the fallback.

## Task 55: Rewrite the abstract and empirical story around the frozen evidence

**Description:** Rewrite the abstract in hook-gap-method-mechanics-result-impact
order, replace the deterministic breadth table with a compact prompted-system
table when admissible, and make one recipient-level failure decomposition the
technical payoff. Keep the title, abstract, table, conclusion, and claim ledger
on the same safe-recipient thesis.

**Acceptance criteria:**
- [ ] Abstract names ChildEsc, explains action-plus-recipient mechanics, gives
  exact complete-run results, and ends with a bounded WIP impact statement.
- [ ] Main table visibly contrasts action and exact-route performance without
  presenting a model winner or unsupported cross-model generalization.
- [ ] Every number in the abstract, table, prose, and generated DOCX derives
  from the frozen summary or existing deterministic artifacts.

**Verification:**
- [ ] Tests pass: `python3 -m unittest tests.test_artifacts -v`.
- [ ] Search manuscript sources for stale one-system values and prohibited
  validation/deployment language.
- [ ] Manual reviewer check: thesis, novelty, main result, and limitation are
  recoverable from the abstract alone.

**Dependencies:** Task 54

**Files likely touched:**
- `paper/main.tex`
- `paper/manuscript.md`
- `scripts/build_paper_docx.py`
- `tests/test_artifacts.py`

**Estimated scope:** Medium: 4 files

## Task 56: Reallocate page four and the unlimited appendix

**Description:** Move the full contract-audit table and secondary diagnostics
to the appendix, preserve only the mechanistic takeaway in the main paper, and
use the recovered space for supported use cases, validation gates, and three
questions tailored to workshop discussion. Do not shrink the official template.

**Acceptance criteria:**
- [ ] Main content remains at most four pages and references begin no later than
  page five.
- [ ] Page four clearly states what developers, practitioners, youth advisors,
  and policymakers can use ChildEsc to inspect now and what remains blocked.
- [ ] Appendix contains model manifests, complete secondary results, failed-run
  status, contract audit, validation protocol, and reproducibility details.

**Verification:**
- [ ] Compile with the official `dblblindworkshop` template.
- [ ] Render and inspect all content, references, appendix, and checklist pages.
- [ ] Confirm no manual margin, font-size, or spacing override is used to fit.

**Dependencies:** Task 55

**Files likely touched:**
- `paper/main.tex`
- `tasks/page_budget.md`
- `scripts/build_paper_docx.py`

**Estimated scope:** Medium: 3 files

## Task 57: Document bounded artifact use cases

**Description:** Make the released utility concrete without implying
deployment. Document how a developer can audit a router or policy revision,
how a reviewer can inspect action-correct recipient failures, and how future
authorized stakeholders can propose or dispute target constraints. Keep
supportive-response assessment and real-world contact outside this artifact.

**Acceptance criteria:**
- [ ] README gives one credential-free replay path and one bring-your-own-model
  routing audit path with explicit routing-only scope.
- [ ] Use cases distinguish specification conformance from clinical or
  real-world safety and identify outputs a reviewer can inspect.
- [ ] No documentation authorizes disclosure, contact, counseling generation,
  or operational crisis routing.

**Verification:**
- [ ] Run every documented no-network command in a clean environment.
- [ ] Tests pass: `make release-test` and `make release-audit`.
- [ ] Manual safety-language scan against `tasks/acceptance_claims.md`.

**Dependencies:** Tasks 54 and 56

**Files likely touched:**
- `README.md`
- `tasks/acceptance_claims.md`
- `paper/main.tex`

**Estimated scope:** Medium: 3 files

## Checkpoint: Reviewer Read After Tasks 55-57

- [ ] The four-page paper has one thesis, one primary table, one concrete
  recipient-level failure, and one bounded impact story.
- [ ] Workshop fit is explicit in evaluation, safeguard, and stakeholder terms.
- [ ] Full technical detail is available in the appendix without crowding the
  main paper.
- [ ] Practitioner and youth validation are still clearly prospective.

## Task 58: Conduct and reconcile an issues-only independent read

**Description:** Give the frozen anonymous paper to one available methods-
oriented reader and, if feasible, one child-safety or youth-facing practitioner
for an issues-only editorial review. Do not request item labels, scores,
personal disclosures, or research responses. Classify findings as confirmed
validity defects, plausible reviewer concerns, or optional improvements.

**Acceptance criteria:**
- [ ] Review request asks only about construct clarity, claim validity,
  recipient constraints, workshop fit, anonymity, and usability.
- [ ] Feedback is not described as practitioner/youth validation or reported as
  a human-subject result.
- [ ] Confirmed defects are repaired; plausible concerns are repaired or bounded;
  optional deadline-risk work is deferred.

**Verification:**
- [ ] Review reconciliation records disposition and evidence for every finding.
- [ ] Manual check: no quote, score, demographic, or item-level response enters
  the anonymous submission as study evidence.
- [ ] Re-run focused manuscript tests after every accepted repair.

**Dependencies:** Task 57

**Files likely touched:**
- `tasks/external_review_log.md`
- `tasks/review_reconciliation.md`
- `paper/main.tex`
- `tests/test_artifacts.py`

**Estimated scope:** Medium: 4 files

## Task 59: Build and audit the final anonymous submission

**Description:** Compile the final PDF and anonymous supplement, reproduce all
reported results from a clean directory, and run page-limit, identity, secret,
local-path, evidence, citation, cache, and prohibited-claim checks. Upload with
an AoE buffer; do not spend the buffer on optional experiments.

**Acceptance criteria:**
- [ ] PDF is anonymous, uses `dblblindworkshop`, has at most four content pages,
  and starts references no later than page five.
- [ ] Anonymous supplement reproduces every reported value without credentials
  or network access and contains no identity-linked repository URL or raw secret.
- [ ] Submission metadata uses the WIP framing and matches the final title,
  abstract, keywords, and author anonymity state.

**Verification:**
- [ ] Tests pass: `make reproduce`, `make llm-test`, `make packet-test`,
  `make release-test`, and `make release-audit`.
- [ ] Clean-room extraction reproduces benchmark, deterministic, contract, and
  prompted-router tables byte-for-byte.
- [ ] Visual inspection covers every PDF page and OpenReview's uploaded preview.

**Dependencies:** Task 58

**Files likely touched:**
- `paper/ChildEsc_Workshop_Paper.pdf`
- `dist/`
- `tasks/evidence_manifest.md`
- `tasks/page_budget.md`

**Estimated scope:** Medium: generated submission artifacts plus 2 ledgers

## Final Acceptance Checkpoint

- [ ] The paper complies with the live workshop call and is uploaded before the
  August 29 AoE deadline.
- [ ] Additional model evidence, if present, was pre-specified, complete,
  identity-verified, fully disclosed, and replayable.
- [ ] The action-route gap remains the central result; target failures are
  decomposed into actionable specification-conformance categories.
- [ ] No model-ranking, clinical, population, supportive-response, validated-
  benchmark, service-partnership, data-transfer, or deployment claim appears.
- [ ] Practitioner and youth validation remain prospective and are correctly
  disclosed as incomplete.

## Deadline-day execution outcome

| Task | Status | Evidence |
|---|---|---|
| 47--49 | Complete | v1.2 protocol, endpoint freeze, claim gates, and tested target-failure decomposition |
| 50--51 | Complete | Both four-item qualification smokes passed identity, schema, and replay gates |
| 52 | Complete | Three Gemini trials completed and replayed |
| 53 | Complete with disclosed incomplete run | Two GPT trials completed; trial 3 remains 79/80 and unscored without retry |
| 54--57 | Complete | Frozen cross-system evidence, four-page rewrite, appendix reallocation, and bounded use documentation |
| 58 | Complete | Earlier read-only Gemini findings and informal editorial form reconciled; two additional headless attempts stalled and are not counted |
| 59 | Complete locally | PDF, DOCX, and anonymous supplement built, rendered, clean-room tested, hashed, and audited |
| External submission | Pending user action | OpenReview upload and uploaded-preview inspection require the submission account |

All local acceptance gates are complete. The only remaining unchecked items are
external upload metadata, OpenReview preview inspection, and final submission
before the workshop deadline.

## Task 60: Test the construct and metric claim chain

**Status:** Complete.

**Description:** Add failing regression tests that require the manuscript to
separate the broad child-safety goal from the provisional routing-conformance
construct and require the action-route gap to be stated as an exact failure
decomposition.

**Acceptance criteria:**
- [x] Tests require all four measurement levels and provisional-status wording.
- [x] Tests require the gap identity without changing metric implementation.
- [x] Tests reject validated-ground-truth or real-world-safety interpretations.

**Verification:**
- [x] Focused tests fail before manuscript/card changes and pass afterward.

**Dependencies:** None

**Files likely touched:**
- `tests/test_artifacts.py`

**Estimated scope:** Small: 1 file

## Task 61: Add the ChildEsc evaluation card

**Status:** Complete.

**Description:** Create a versioned JSON evaluation card that exposes the
background goal, systematized construct, instrument, measurements, intended
uses, prohibited uses, evidence status, validation status, and update triggers.

**Acceptance criteria:**
- [x] JSON is deterministic, anonymous, machine-readable, and schema-tested.
- [x] It labels v0.1 target constraints as provisional.
- [x] It prohibits deployment, clinical, contact, and model-ranking uses.

**Verification:**
- [x] Artifact tests parse and validate every required field.
- [x] Release audit passes.

**Dependencies:** Task 60

**Files likely touched:**
- `benchmark/evaluation_card_v0_1.json`
- `tests/test_artifacts.py`

**Estimated scope:** Small: 2 files

## Task 62: Tighten construct and metric exposition

**Status:** Complete.

**Description:** Revise the paper to distinguish measurement levels, define the
action order as operational intervention intensity, and state the exact
action-route-gap identity. Do not change benchmark evidence.

**Acceptance criteria:**
- [x] Claim boundaries are explicit in the main paper rather than appendix-only.
- [x] The mathematical identity is correct and consistent with all 247 failures.
- [x] No existing score, item, label, prompt, or protocol changes.

**Verification:**
- [x] Focused artifact and arithmetic checks pass.
- [x] Manuscript diff contains interpretation changes only.

**Dependencies:** Tasks 60-61

**Files likely touched:**
- `paper/main.tex`
- `paper/references.bib`
- `paper/manuscript.md`

**Estimated scope:** Medium: 3 files

## Task 63: Add a compact audit-pipeline figure

**Status:** Complete.

**Description:** Add one compact main-paper figure connecting synthetic
conversation, router output, provisional reference constraints, deterministic
scoring, and validation-gated claims. Remove it if it causes overflow or harms
legibility.

**Acceptance criteria:**
- [x] Figure clarifies rather than duplicates the prose.
- [x] Caption states the provisional-label and routing-only boundary.
- [x] References still begin on page 5 using unchanged template geometry.

**Verification:**
- [x] Compile and render all four content pages.
- [x] Manual visual inspection confirms no crowding or clipping.

**Dependencies:** Task 62

**Files likely touched:**
- `paper/main.tex`
- `scripts/build_paper_docx.py`

**Estimated scope:** Small: 2 files

## Task 64: Synchronize reviewer-facing artifacts

**Status:** Complete.

**Description:** Mirror the final semantics and evaluation-card pointer across
the DOCX builder, dataset card, README, supplement README, and tests.

**Acceptance criteria:**
- [x] No stale handoff semantics, test counts, replay promises, or model names.
- [x] Evaluation card is listed in outputs and included in the supplement.
- [x] PDF and DOCX communicate the same central claim.

**Verification:**
- [x] Manuscript synchronization and release tests pass.

**Dependencies:** Tasks 61-63

**Files likely touched:**
- `scripts/build_paper_docx.py`
- `benchmark/DATASET_CARD.md`
- `README.md`
- `paper/SUPPLEMENT_README.md`
- `tests/test_artifacts.py`

**Estimated scope:** Medium: 5 files

## Task 65: Rebuild and visually inspect submission artifacts

**Status:** Complete.

**Description:** Compile the anonymous PDF, rebuild the DOCX and supplement,
render every page, and inspect layout, page boundaries, citations, and tables.

**Acceptance criteria:**
- [x] Exactly four content pages; references begin on page 5.
- [x] No visual defect, stale title, or identity-bearing content.
- [x] Supplement excludes raw responses, caches, and internal review notes.

**Verification:**
- [x] PDF and DOCX render-and-inspect checks pass.
- [x] ZIP integrity and content audit pass.

**Dependencies:** Task 64

**Files likely touched:**
- `paper/ChildEsc_Workshop_Paper.pdf`
- `paper/ChildEsc_Workshop_Paper.docx`
- `paper/childesc_anonymous_supplement.zip`

**Estimated scope:** Generated artifacts

## Task 66: Run clean-room and adversarial gates

**Status:** Complete.

**Description:** Reproduce from a fresh supplement extraction and verify every
claim-bearing count, interval, hash, citation, anonymity boundary, and prohibited
interpretation.

**Acceptance criteria:**
- [x] All repository and packaged tests pass without network access.
- [x] All packaged result artifacts match the workspace byte-for-byte.
- [x] No unresolved high- or medium-severity review finding remains.

**Verification:**
- [x] `make reproduce`, `make llm-test`, and `make packet-test` pass in the
  workspace and fresh anonymous-supplement extraction.
- [x] `git diff --check` and release audit pass.

**Dependencies:** Task 65

**Files likely touched:**
- `tasks/evidence_manifest.md`
- `tasks/page_budget.md`

**Estimated scope:** Small: 2 files plus verification

## Task 67: Version the submission-ready iteration

**Status:** Complete.

**Description:** Commit and push the accepted-workshop-paper readiness revision
only after every local gate passes.

**Acceptance criteria:**
- [x] Commit contains no unrelated or identity-bearing submission change.
- [x] Branch is synchronized with GitHub.

**Verification:**
- [x] The tracked tree is clean, the pushed substantive commit is `7b8ded1`,
  and local visual-QA render directories remain deliberately untracked.

**Dependencies:** Task 66

**Files likely touched:** None beyond version-control metadata

**Estimated scope:** Small
