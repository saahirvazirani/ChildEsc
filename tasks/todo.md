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
- [ ] Dry-run the packet on synthetic examples without collecting study data.
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

**Description:** Run a four-item smoke test for each available direct provider,
inspect payload isolation and structured outputs, then execute three complete
80-item trials per frozen primary model. OpenRouter remains a portability smoke
test unless upstream provenance is pinned.

**Acceptance criteria:**
- [ ] Every reported model has the protocol-required number of complete trials,
  or the manuscript uses the pre-registered fallback and discloses the reason.
- [ ] Raw attempts and normalized predictions account for every item without
  selective exclusion or silent response repair.
- [ ] Exact provider, model, returned model version, prompt/schema hashes,
  settings, timestamps, and cache hashes are present in each run manifest.

**Verification:**
- [ ] Live smoke commands finish with valid two-field routes for four items.
- [ ] Full-run cache-only commands finish without API keys or network access.
- [ ] Manual check: invalid output and provider-error counts reconcile with the
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
- [ ] Every primary metric has an explicit denominator and item-level audit
  trail.
- [ ] Trial results are summarized without treating repeated outputs from the
  same 80 items as independent observations.
- [ ] Model-to-model differences are paired by family and presented as
  descriptive intervals rather than winner claims.

**Verification:**
- [ ] Tests pass: `make llm-test` and `make test`.
- [ ] Reproduction check: deleting generated summaries and rerunning analysis
  recreates byte-stable tables from cached normalized outputs.
- [ ] Manual check: action-route-gap counts equal action-correct target-failure
  counts under the documented metric definition.

**Dependencies:** Task 34

**Files likely touched:**
- `src/childesc/llm_analysis.py`
- `llm_tests/test_llm_analysis.py`
- `results/llm/summary.json`
- `results/llm/paper_table.csv`

**Estimated scope:** Medium: 4 files

## Checkpoint: Evidence Integrity

- [ ] Tasks 33-35 pass all focused and frozen tests.
- [ ] All proposed paper values replay from cache without credentials.
- [ ] No prompt, label, model setting, or primary metric changed after result
  inspection.
- [ ] Any deviation from the frozen protocol is logged and kept out of primary
  claims unless the entire affected analysis is rerun under a new version.

## Task 36: Rewrite the title and abstract around one finding

**Description:** Make the safe-recipient question the title-level hook and
rewrite the abstract after evidence freeze to include the narrow construct, the
model-audit setup, one concrete action-route-gap finding, and the validation
boundary.

**Acceptance criteria:**
- [ ] The title distinguishes ChildEsc from refusal and action-only benchmarks.
- [ ] The abstract reports only results regenerated from frozen artifacts.
- [ ] The final sentence states that practitioner and youth validation have not
  occurred and blocks deployment interpretation.

**Verification:**
- [ ] Manuscript synchronization tests cover every abstract number.
- [ ] Manual check: the abstract contains problem, gap, method, result,
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
- [ ] The main table has no more than the columns needed to support the central
  claim and remains legible at the official template size.
- [ ] One concise example shows how an action-correct route can still select an
  inappropriate recipient.
- [ ] Keyword, severity-agnostic, stress-test, and full contract details remain
  reproducible in the appendix rather than being deleted.

**Verification:**
- [ ] Build succeeds with the NeurIPS 2026 `dblblindworkshop` option.
- [ ] Visual check: table text and the failure example are readable at 100%.
- [ ] Data check: every table cell is derived from the frozen result files.

**Dependencies:** Tasks 35-36

**Files likely touched:**
- `paper/main.tex`
- `paper/manuscript.md`
- `scripts/build_paper_docx.py`
- `tests/test_artifacts.py`

**Estimated scope:** Medium: 4 files

## Task 38: Rebalance page four for workshop discussion

**Description:** Use the final content page for construct limitations,
actionable impact, and three precise workshop questions. Move the prospective
1--24 hour 988 mechanism and detailed validation protocol to the appendix so
they do not dilute or destabilize the core paper.

**Acceptance criteria:**
- [ ] The main text names practitioner and youth validation as incomplete and
  does not imply a hotline partnership or operational referral pathway.
- [ ] Three discussion questions address abstention or clarification, separate
  practitioner and youth judgments, and governance before operational handoff.
- [ ] References begin on page five without changing template margins, font
  sizes, or spacing.

**Verification:**
- [ ] Compile and inspect all four content pages and the first reference page.
- [ ] Phrase scan finds no unsupported 988 policy, validated cutoff, automated
  outreach, or deployment-readiness statement in the main paper.
- [ ] Appendix cross-references remain correct.

**Dependencies:** Task 37

**Files likely touched:**
- `paper/main.tex`
- `paper/manuscript.md`
- `tasks/page_budget.md`
- `scripts/build_paper_docx.py`

**Estimated scope:** Medium: 4 files

## Checkpoint: Reviewer Read

- [ ] Tasks 36-38 produce a self-contained four-page paper.
- [ ] A fresh reader identifies the construct, model evidence, strongest
  failure, and evidence boundary from the title, abstract, and main table.
- [ ] Closest-work text distinguishes ChildEsc from CAREBench, KIDBench,
  MinorBench, MindEval, and CARE-Bench without novelty overreach.
- [ ] The appendix adds reproducibility depth but is not needed to discover the
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

**Description:** Produce the final PDF and anonymous supplement, replay model
results in a clean environment, and audit page limits, identity, secrets,
provider terms, local paths, stale outputs, and unsupported claims.

**Acceptance criteria:**
- [ ] Main content is at most four pages and references begin on page five.
- [ ] The anonymous supplement reproduces all paper values from synthetic data
  and permitted cached or normalized model outputs without network credentials.
- [ ] No username-linked repository URL, author identity, API key, PII, real
  child disclosure, or unapproved raw provider response is present.

**Verification:**
- [ ] Tests pass: `make reproduce`, `make llm-test`, `make release-test`, and
  `make release-audit`.
- [ ] Clean-room check: extract the anonymous archive and reproduce all tables.
- [ ] Visual check: inspect every PDF page for clipping, overflow, anonymity,
  and reference boundaries.

**Dependencies:** Task 40

**Files likely touched:**
- `paper/main.tex`
- `paper/ChildEsc_Workshop_Paper.pdf`
- `scripts/release_audit.py`
- `dist/`

**Estimated scope:** Medium: build and release artifacts

## Final Acceptance Checkpoint

- [ ] At least one prompted model router has a complete replayable full result;
  the preferred result is three providers with three trials each.
- [ ] The action-route gap and implicated-adult target failures are visible in
  the main paper.
- [ ] No supportive-response, model-ranking, clinical, population, hotline-
  partnership, or deployment claim exceeds the completed evidence.
- [ ] Practitioner and youth validation remain prospective and are correctly
  disclosed as incomplete.
- [ ] The final package is anonymous, four-page compliant, and reproducible.
