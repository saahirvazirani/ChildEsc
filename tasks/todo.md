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
  Gemini, OpenAI, and Anthropic documentation.
- [x] Task 26: Freeze a provider-neutral routing prompt and strict JSON Schema.
- [x] Task 26: Add failing tests for request parity, response parsing, and label
  isolation without changing the frozen 46-test suite.

### Phase 2: Provider and Cache Implementation

- [x] Task 27: Implement injectable standard-library REST transport and bounded,
  credential-safe errors.
- [x] Task 27: Implement Gemini, OpenAI, and Anthropic adapters.
- [x] Task 28: Implement content-addressed response caching with atomic writes.
- [x] Task 28: Prove cache-only replay requires neither credentials nor network.

### Phase 3: Routing-Only Evaluation

- [x] Task 29: Implement the LLM routing evaluator and CLI.
- [x] Task 29: Record invalid outputs and provider failures without dropping
  benchmark items from metric denominators.
- [x] Task 29: Export prompt/schema hashes, provider/model settings, cache
  telemetry, predictions, and routing metrics.

### Phase 4: Documentation and Verification

- [x] Task 30: Document Gemini, OpenAI, and Anthropic usage and safe cost-limited
  smoke tests.
- [x] Task 30: State that supportive-response quality is outside scope and needs
  a separate rubric plus human validation.
- [x] Task 30: Run LLM tests, frozen scientific tests, release tests, full
  reproduction, and a fresh code review.
