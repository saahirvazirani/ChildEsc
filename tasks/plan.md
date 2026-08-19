# Revision Plan: Four-Page ChildEsc Submission

## Overview

The Child Safety in AI workshop permits at most four content pages, excluding references, with an optional unlimited appendix. ChildEsc now uses all four content pages. The acceptance-oriented strategy was not broad expansion: preserve the narrow contribution, use the added page for the strongest technical evidence and closest-work positioning, and move reproducibility detail, error tables, ablations, validation materials, and extended limitations to the appendix.

## Confirmed Submission Constraints

- Maximum: four content pages.
- Excluded from the content count: references.
- Optional appendix: unlimited length.
- Required format: NeurIPS 2026 template with `dblblindworkshop`.
- Review: anonymous and double-blind.
- Workshop priority: technical soundness and potential to stimulate productive discussion.
- Deadline: August 29, 2026, AoE.

## Current Baseline

- The current main text occupies four pages; references begin on page five.
- The testbed contains 80 synthetic conversations in 20 counterfactual families.
- The deterministic checksum and two diagnostic baselines reproduce with 25 passing tests.
- Independent and Gemini review findings on leakage, target validity, delay, denominators, and overclaiming have been repaired.
- No practitioner or youth validation has occurred.
- Current results are policy-exposed implementation diagnostics, not evidence of generalization or deployment safety.

## Architecture Decisions

- Keep the paper a works-in-progress technical artifact rather than implying a validated benchmark.
- Keep the four-page core centered on ordinal escalation calibration and constrained human handoff.
- Treat the rule-based prototype as an auditable checksum, not a competitive model.
- Freeze the current benchmark, labels, router, and metrics before new analyses or external review.
- Separate technical integrity, practitioner construct review, and youth assessment of realism and agency.
- Do not report practitioner or youth validation unless an appropriate ethics route and completed protocol support the claim.
- Use the appendix for depth; do not rely on it to repair an unclear contribution in the main paper.

## Dependency Graph

```text
Confirmed four-page rule
    |
    +--> Freeze v0.1 evidence
    |       |
    |       +--> Error analysis and ablations
    |       +--> Independent holdout, if feasible
    |
    +--> Ethics determination
            |
            +--> Practitioner review, if permitted
            +--> Youth review, only if specifically permitted

Frozen evidence + eligible validation evidence
    |
    +--> Four-page main-paper revision
    +--> Unlimited technical/validation appendix
            |
            +--> Claim audit and final anonymous package
```

## Evidence Gates

### Gate A: Ethics Route

Document whether any practitioner or youth activity is covered by an appropriate institutional determination or approved collaborator. If youth participation is not explicitly covered, do not recruit minors before submission. Practitioner responses analyzed or quoted as study data also require the applicable determination. Scholarly feedback may improve the paper but must not be labeled empirical validation.

### Gate B: Artifact Freeze

Record hashes for the benchmark source, generated data, router, tests, metrics, and paper table before new robustness evaluation or human review. Version and disclose every post-freeze change.

### Gate C: Submission Evidence

Freeze all reported evidence by August 24. Incomplete or procedurally ambiguous human review remains a prospective protocol, not a result.

## Four-Page Budget

| Content page | Primary purpose | Non-negotiable content |
|---|---|---|
| 1 | Abstract and introduction | Problem, closest gap, three contributions, explicit evidence boundary |
| 2 | Testbed and construct | Scope, provenance, action/target schema, closest-work distinction |
| 3 | Prototype, metrics, and diagnostics | No-oracle contract, failure-oriented metrics, synchronized result table |
| 4 | Failure analysis and implications | Most informative errors, validity threats, validation status, impact, conclusion |

## Appendix Allocation

- Full schema and target taxonomy.
- Representative scenario families and content-safety notes.
- Metric equations, denominators, bootstrap method, and additional tables.
- Item-level error taxonomy and component ablations.
- Robustness transformations and any independently authored holdout protocol/results.
- Practitioner rubric, youth-participatory protocol, safeguarding plan, and analysis plan.
- Compute, LLM usage, release restrictions, and expanded limitations.
- NeurIPS checklist.

## Phase 1: Freeze and Governance

- [ ] Record the workshop page-limit source and page-counting rule.
- [ ] Create a version manifest for every technical artifact supporting a claim.
- [ ] Document the applicable ethics route before participant contact.
- [ ] Prepare separate practitioner and youth protocols, with protocol-only fallback.

### Checkpoint: Permission and Freeze

- [ ] Current outputs reproduce before the freeze is declared.
- [ ] Permitted populations and activities are explicit.
- [ ] No participant recruitment occurs outside the documented route.
- [ ] If approval is absent, the paper continues to say no practitioner or youth validation has occurred.

## Phase 2: Technical Strengthening

- [ ] Produce a deterministic item-level taxonomy of action and target errors.
- [ ] Run pre-specified ablations for conversation accumulation, negation/third-person guards, and implicated-adult inference.
- [ ] Add robustness stress tests without tuning the frozen router on inspected failures.
- [ ] Create a lexically held-out family set only if an independent author can remain blind to rules and item-level errors.

### Checkpoint: Technical Evidence

- [ ] Every new number is generated from a versioned artifact.
- [ ] Paired counts, denominators, uncertainty, and exclusions are explicit.
- [ ] No post-hoc rule change is described as held-out performance.
- [ ] `make reproduce` regenerates every reported technical result.

## Phase 3: Validation Path

- [ ] Practitioner review, if authorized, evaluates label validity, target constraints, missing context, feasibility, and jurisdictional ambiguity.
- [ ] Youth review, only if authorized, evaluates realism, agency, accessibility, perceived coercion, and handoff framing without eliciting personal disclosures.
- [ ] Retain disagreement and pre-review labels rather than forcing consensus.
- [ ] Report `practitioner-reviewed`, `youth-informed`, or `youth-validated` only when the completed evidence supports that exact term.

## Phase 4: Manuscript and Appendix Revision

- [ ] Use the fourth content page for concise error analysis and stronger closest-work comparison.
- [ ] Keep the result table and core validity warning in the main text.
- [ ] Move procedural detail and secondary analyses to the appendix with explicit cross-references.
- [ ] Present human-validation results only if Gate A and the relevant protocol are complete.
- [ ] Revise the abstract last, after the evidence and claim audits.

### Checkpoint: Reviewer Read

- [ ] The first page states the narrow gap and does not imply clinical or child-centered validation.
- [ ] The main paper is self-contained despite using the appendix for detail.
- [ ] The strongest technical and validity evidence fits within four content pages.
- [ ] References begin no later than page five.

## Phase 5: Final Verification

- [ ] Run a fresh issues-only review on construct validity, statistics, ethics, novelty, and overclaiming.
- [ ] Reconcile findings as confirmed defects, plausible concerns, or optional improvements.
- [ ] Compile in anonymous `dblblindworkshop` mode and inspect every PDF and DOCX page.
- [ ] Rebuild and clean-room test the anonymous supplement.
- [ ] Scan all artifacts for identity, local paths, placeholders, and stale claims.

## Schedule

| Date | Milestone |
|---|---|
| Aug 18 | Page policy recorded; ethics route decided |
| Aug 20 | Artifact and analysis plan frozen |
| Aug 22 | Technical analyses complete; validation status checkpoint |
| Aug 24 | Submission evidence frozen |
| Aug 26 | Four-page manuscript and appendix feature-complete |
| Aug 27 | Independent review and methodological repairs complete |
| Aug 28 | Final render, anonymity scan, and clean-room reproduction |
| Aug 29 | Submission buffer; no new experiments |

## Risks and Mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| Main text exceeds four pages | Critical | Maintain a page ledger and compile after every material revision. |
| Youth research is rushed | Critical | Do not recruit without explicit approval and safeguards; submit the protocol instead. |
| Appendix becomes a dumping ground | High | Keep contribution, method, main result, and core limitations in the four-page paper. |
| Human feedback causes post-hoc tuning | High | Freeze v0.1 and version all later changes. |
| Added analyses dilute the narrow claim | High | Include only analyses that test escalation calibration or target safety. |
| Validation cannot finish by August 24 | Medium | Retain honest protocol-only framing and prioritize reproducible technical evidence. |

## Definition of Done

- Main content is at most four pages, with references beginning afterward.
- No human-validation claim exceeds the ethically reportable evidence.
- Every technical claim traces to a versioned, reproducible artifact.
- The appendix contains sufficient detail for reproduction and future validation.
- The anonymous PDF, DOCX, and supplement pass visual, integrity, accessibility, and identity checks.

## Execution Outcome

Completed on 2026-08-17 for the protocol-only submission route. The paper uses three content pages before references, the anonymous supplement clean-room reproduces all outputs with 36 passing tests, and final PDF/DOCX visual, accessibility, metadata, identity, and claim scans pass. Practitioner/youth recruitment and independent-holdout evaluation were deliberately not executed because the required ethics authorization and unexposed holdout author are unavailable; the paper reports those limits directly and includes prospective materials only.

## Fourth-Page Acceptance Revision (2026-08-18)

### Decision

Use the available fourth content page for evidence architecture rather than more scenarios or broader performance claims. Keep the 80-item v0.1 testbed and router frozen. Add a separately identified, post-freeze contract audit that checks source-informed relational requirements without serving as a held-out set or a realism estimate.

### Workshop fit

- Primary fit: safe data, evaluation, and benchmarking under restricted-access conditions.
- Secondary fit: auditable deployment safeguards and child-centered human handoff.
- Discussion value: when a child-facing system should preserve engagement, set a relational boundary, seek context, or surface human support, and how to prevent an implicated adult from becoming the default handoff target.
- Open-problem mapping: standardized safety assessments (B3), with the explicit caveat that the cited open-problem page is scoped to AIG-CSAM while ChildEsc addresses a broader workshop topic.

### Closest-work correction

CARE-Bench for patient-facing medical triage appeared on 2026-08-04 and also uses a four-label sequential current-action task. ChildEsc must not claim that ordinal routing or action timing is itself new. The remaining distinction is child-specific and narrower: matched severity trajectories plus machine-checkable permitted and forbidden human-handoff targets, including implicated-adult constraints. CAREBench and KIDBench remain the closest child-safety comparisons.

### Source hierarchy

1. Normative child-rights and crisis guidance defines design requirements, not item-level ground truth.
2. Peer-reviewed and preprint benchmarks inform task structure, controlled prompt construction, and reporting practice.
3. Developer-authored synthetic text instantiates those requirements but is not called representative, realistic, clinical, or validated.
4. Practitioner review and youth-participatory review remain prospective and require the documented ethics route.

### Technical slice

- Add a dated source register with the exact design decision supported by each source.
- Add a family rationale map covering all 20 v0.1 families while stating that the mapping is retrospective and domain-level.
- Add matched contract probes for temporal immediacy, resolved or negated risk, first- versus third-person risk, implicated-adult routing, AI dependency, coercive secrecy, online threat escalation, and medical deterioration.
- Score atomic assertions over action order, target inclusion/exclusion, risk domains, and response requirements.
- Freeze probe definitions before first execution and do not modify the router in response to probe failures.
- Report pass counts as mechanistic conformance only; retain every failed assertion.

### Claim gates

- `source-informed`: permitted when a traceable public source supports the design rationale.
- `source-grounded`: reserved for an individual case whose content and label are auditable to a source action or trigger; v0.1 does not meet this bar.
- `held-out`: prohibited for the new probes because their author has inspected the router and existing errors.
- `validated`, `realistic`, `child-centered`, `clinically appropriate`, or `effective`: prohibited as empirical claims until the relevant independent human study is completed.

### Acceptance checks

- The abstract states the supported claim and evidence boundary in the same paragraph.
- The main paper explicitly distinguishes ChildEsc from both CAREBench and CARE-Bench.
- References begin on page five, with no template compression.
- Every new number is generated by `make reproduce` and synchronized by tests.
- The anonymous supplement includes the source register, authoring protocol, probes, evaluator, and outputs.
- A fresh issues-only review checks novelty, construct validity, child rights, crisis policy, statistics, and overclaiming.

## Delegated Follow-Up Integration (2026-08-18)

The proposed chatbot-to-988 follow-up mechanism is included only as a prospective governance extension. Official SAMHSA guidance supports governed follow-up and requires documented informed consent for contact-PII sharing in referral or case-management contexts; it does not establish unsolicited chatbot referrals or a risk-to-deadline formula. HHS/FTC guidance also weighs against burying health-data disclosure in a general Terms of Use clause.

The accepted technical shape therefore preserves the candidate 1-24 hour monotonic deadline as a research hypothesis while blocking implementation. A formal 988/center partnership, child-safeguarding and legal review, separate revocable and age-appropriate consent, human crisis-professional approval, minimum-necessary transfer, receiving-service capacity agreement, independently calibrated committee-owned formula, and prospective harm evaluation are all mandatory gates. Imminent danger is excluded from delayed scheduling. The current router only recommends or offers a `crisis_service` target and never collects PII, transfers data, schedules outreach, or claims 988 participation.

## Fourth-Page Execution Outcome (2026-08-18)

The official PDF now uses four content pages, with references beginning on page five. The fourth page contains the frozen relational contract audit, retained failures, construct-validity limits, evidence gates, and the bounded delegated-follow-up extension. `make reproduce` passes 46 tests and reports 36/39 atomic contract assertions across 7/9 families without modifying the frozen router. The DOCX renders in five clean pages and its OOXML accessibility audit reports zero findings.

# Implementation Plan: GitHub Staging Release and Prospective Validation

## Overview

Publish ChildEsc as a private GitHub staging repository with a clean, reproducible public-facing structure and a README that explains installation, execution, outputs, safety limits, and validation status. The initial repository must not imply that practitioner or youth validation has occurred. Instead, it will expose the pre-specified protocols, ethics gates, and versioning path needed to perform that work defensibly. A public release remains a separate gate because a username-linked repository could compromise the workshop's double-blind review and because the current dataset card requires independent review before public release.

## Architecture Decisions

- Use the existing local Git repository and rename its default branch from `master` to `main`; do not create a second nested repository.
- Create `saahirvazirani/ChildEsc` as a private staging repository first. Public visibility is deferred until the workshop anonymity policy and release-readiness gate are satisfied.
- Keep ChildEsc v0.1 immutable. Practitioner or youth feedback creates a versioned v0.2 candidate with a change log; it never silently overwrites v0.1.
- Treat the rule router as an implementation checksum, not a validated classifier. Public documentation must distinguish technical verification from construct, ecological, clinical, and deployment validity.
- Publish only synthetic benchmark data, code, aggregate generated results, protocols, and selected paper artifacts. Exclude local templates, build logs, render directories, caches, and future participant-level data.
- Keep validation sequential: qualified institutional determination first, practitioner construct review second, and youth-participatory review only after minors-specific approval and safeguarding sign-off.

## Dependency Graph

```text
Release boundary and human decisions
    |
    +-- Repository hygiene and licensing
    |       |
    |       +-- README and governance files
    |       |       |
    |       |       +-- Clean-room reproduction and release audit
    |       |               |
    |       |               +-- Initial private commit and GitHub push
    |       |
    |       +-- Workshop anonymity gate --> Optional public release
    |
    +-- Institutional ethics determination
            |
            +-- Practitioner construct review --> Versioned v0.2 candidate
                    |
                    +-- Minors-specific approval and safeguarding review
                            |
                            +-- Youth-participatory review --> Validation report
```

## Phase 1: Release Boundary

### Task 16: Lock repository visibility, license, and artifact boundary

**Description:** Record the human decisions that have legal or double-blind-review consequences before staging any commit.

**Acceptance criteria:**
- [x] Repository owner, name, and private-first visibility are approved.
- [x] Code, data/documentation, and paper licenses are selected explicitly.
- [x] The include/exclude manifest preserves anonymity and excludes participant data and local build debris.

**Verification:**
- [x] Manual check: compare the manifest against every top-level file and directory.
- [x] Manual check: confirm that no public repository is created before the anonymity decision.

**Dependencies:** None

**Files likely touched:**
- `tasks/plan.md`
- `tasks/todo.md`
- `LICENSE`
- `DATA_LICENSE`

**Estimated scope:** Small: 4 files

### Task 17: Add repository hygiene and safety controls

**Description:** Prevent generated files, local templates, credentials, participant data, and sensitive disclosures from entering the repository accidentally.

**Acceptance criteria:**
- [x] `.gitignore` excludes Python caches, LaTeX intermediates, rendered pages, local templates, temporary files, and private validation data paths.
- [x] `SECURITY.md` tells users not to submit crisis disclosures or identifying child data through issues and provides a private vulnerability-reporting route.
- [x] The tracked-file allowlist contains only intended research artifacts.

**Verification:**
- [x] `git status --short --ignored` matches the approved boundary.
- [x] Secret, identity, absolute-path, and large-file scans return no unexplained findings.

**Dependencies:** Task 16

**Files likely touched:**
- `.gitignore`
- `.gitattributes`
- `SECURITY.md`

**Estimated scope:** Medium: 3 files

## Checkpoint: Release Boundary

- [x] The private-first strategy, license, and tracked-file boundary are approved.
- [x] No public identity or remote URL has been introduced into the anonymous submission package.
- [x] No recruitment or participant-data collection has begun.

## Phase 2: Usable Research Artifact

### Task 18: Rewrite the README as the canonical user guide

**Description:** Make the root README sufficient for a new researcher to understand scope, install ChildEsc, reproduce results, interpret outputs, and avoid unsupported uses.

**Acceptance criteria:**
- [x] README includes scope, content warning, requirements, quickstart, command reference, repository map, output interpretation, citation, and troubleshooting.
- [x] A validation-status table marks technical checks complete and practitioner, youth, ecological, clinical, cross-cultural, and deployment validation incomplete.
- [x] Claims consistently describe `child-centered` as a design objective and v0.1 results as policy-exposed diagnostics.

**Verification:**
- [x] A clean clone can follow only the README to run `make reproduce`.
- [x] A terminology scan finds no unsupported `validated`, `effective`, `clinically appropriate`, or `youth-informed` claims.

**Dependencies:** Tasks 16-17

**Files likely touched:**
- `README.md`
- `CITATION.cff`
- `CONTRIBUTING.md`
- `CHANGELOG.md`

**Estimated scope:** Medium: 4 files

### Task 19: Add reproducibility CI and release checks

**Description:** Re-run the existing standard-library testbed on GitHub and make release-boundary failures visible before merge or publication.

**Acceptance criteria:**
- [x] CI runs `make reproduce` on supported Python versions without network dependencies.
- [x] Generated benchmark and result synchronization remains covered by the existing tests.
- [x] Release checks detect credentials, local absolute paths, and prohibited participant-data directories.

**Verification:**
- [x] `make reproduce` passes locally with 46 scientific tests and five release tests.
- [x] The corrected GitHub Actions run passes on Python 3.11 and 3.12 in the private repository.

**Dependencies:** Tasks 17-18

**Files likely touched:**
- `.github/workflows/ci.yml`
- `scripts/release_audit.py`
- `tests/test_release_audit.py`
- `Makefile`

**Estimated scope:** Medium: 4 files

## Checkpoint: Reproducible Artifact

- [x] A clean local extraction reproduces benchmark outputs and all tests.
- [x] README commands and generated paths are accurate.
- [x] Validation-status wording matches `validation/ethics_gate.md` exactly.

## Phase 3: Private GitHub Staging

### Task 20: Create an atomic initial history and push the private repository

**Description:** Authenticate the GitHub CLI, create a clean initial commit on `main`, create the private remote, and verify the hosted artifact.

**Acceptance criteria:**
- [x] `gh auth status` succeeds for the intended GitHub account.
- [x] The initial commit contains only approved files and has no secrets, identities in anonymous artifacts, or oversized build debris.
- [x] `saahirvazirani/ChildEsc` exists privately with `main` tracking `origin/main`.

**Verification:**
- [x] `git status --short --branch` is clean after push.
- [x] `gh repo view saahirvazirani/ChildEsc` confirms private visibility and the expected default branch.
- [x] A fresh clone passes `make reproduce` and the hosted CI run succeeds.

**Dependencies:** Tasks 16-19

**Files likely touched:**
- Repository metadata and Git history only

**Estimated scope:** Small: repository operation

### Task 21: Gate any later public release

**Description:** Convert the private staging repository to public only after double-blind anonymity, licensing, artifact, and validation-disclosure checks pass.

**Acceptance criteria:**
- [ ] The workshop policy or review phase permits a username-linked public artifact.
- [ ] The release notes state exactly which human validation remains incomplete.
- [ ] Public v0.1 is tagged as a preliminary synthetic testbed, not a deployment-ready benchmark.

**Verification:**
- [ ] Manual check: anonymous submission files contain no GitHub identity or repository URL unless explicitly permitted.
- [ ] `gh repo view` confirms the intended visibility only after approval.

**Dependencies:** Task 20 and workshop anonymity clearance

**Files likely touched:**
- `README.md`
- `CHANGELOG.md`

**Estimated scope:** Small: 2 files plus repository settings

## Phase 4: Prospective Human Validation

### Task 22: Obtain and record the institutional determination

**Description:** Before any recruitment, a qualified institution or authorized partner determines the applicable human-subjects, safeguarding, consent, data-management, compensation, and reporting requirements.

**Acceptance criteria:**
- [ ] A qualified human records the determination, approving body, scope, date, and protocol version.
- [ ] Recruitment, consent, data handling, withdrawal, compensation, and incident procedures match that determination.
- [ ] If no route is approved, all human validation remains protocol-only and the public status remains `not started`.

**Verification:**
- [ ] Manual sign-off by the responsible institutional and safeguarding contacts.
- [ ] No recruitment record predates the approval or determination.

**Dependencies:** None; blocks Tasks 23-24

**Files likely touched:**
- `validation/ethics_gate.md`
- `validation/data_management_plan.md`
- `validation/safeguarding_plan.md`

**Estimated scope:** Medium: 3 files plus external review

### Task 23: Run practitioner construct review without contaminating evaluation

**Description:** After authorization, conduct the frozen balanced incomplete-block review with 8-12 practitioners across youth mental health or crisis support, child protection, and digital safety.

**Acceptance criteria:**
- [ ] Router predictions and reference labels remain hidden during independent ratings, with at least three ratings per item where feasible.
- [ ] Analysis reports action disagreement, target-set agreement, missing context, unsafe routing, ambiguity, and role-stratified descriptive results without forcing consensus.
- [ ] All changes produce a versioned v0.2 candidate and change log; the router is not tuned and evaluated on the same reviewed items.

**Verification:**
- [ ] Assignment seeds, protocol version, exclusions, missingness, and pre-adjudication ratings are auditable.
- [ ] Aggregate results reproduce from a de-identified analysis export.

**Dependencies:** Task 22 and frozen v0.1

**Files likely touched:**
- `validation/practitioner_protocol.md`
- `validation/practitioner_analysis_plan.md`
- `validation/practitioner_rubric.csv`
- `CHANGELOG.md`

**Estimated scope:** Medium: 4 files plus approved data collection

### Task 24: Run youth-participatory review under the stronger minors gate

**Description:** Only after explicit minors approval and safeguarding sign-off, conduct a formative advisory review of comprehensibility, agency, plausibility, coercion, and handoff wording without eliciting personal crisis experiences.

**Acceptance criteria:**
- [ ] Guardian consent and youth assent, or an institutionally authorized alternative, are documented with skip, stop, compensation, privacy, and deletion rights.
- [ ] Sessions never ask whether a vignette happened to the participant and keep youth preference separate from clinical or legal safety judgments.
- [ ] Reporting preserves contradictory perspectives and uses `youth-informed` only for specifically documented design changes; `youth-validated` is not used by default.

**Verification:**
- [ ] Safeguarding lead, materials, escalation process, and debrief resources are approved before the first session.
- [ ] Published outputs contain no participant-level sensitive data or identifying quotations.

**Dependencies:** Tasks 22-23 and minors-specific approval

**Files likely touched:**
- `validation/youth_protocol.md`
- `validation/youth_rubric.md`
- `validation/safeguarding_plan.md`
- `CHANGELOG.md`

**Estimated scope:** Medium: 4 files plus approved data collection

### Task 25: Publish a validation report and versioned benchmark candidate

**Description:** Synthesize practitioner and youth findings without collapsing distinct constructs, then release a traceable candidate version for independent evaluation.

**Acceptance criteria:**
- [ ] The report separates practitioner construct judgments, youth experience judgments, disagreements, exclusions, and remaining evidence gaps.
- [ ] Every changed item or label traces to a documented rationale while v0.1 remains available and immutable.
- [ ] Claims remain bounded: completion does not establish therapeutic benefit, crisis-triage accuracy, cultural universality, or safe autonomous deployment.

**Verification:**
- [ ] Reproduction succeeds from the versioned aggregate artifacts.
- [ ] An independent reviewer verifies claim-to-evidence traceability before release.

**Dependencies:** Tasks 23-24

**Files likely touched:**
- `validation/VALIDATION_REPORT.md`
- `benchmark/DATASET_CARD.md`
- `benchmark/childesc_v0_2_candidate.jsonl`
- `CHANGELOG.md`

**Estimated scope:** Medium: 4 files

## Final Checkpoint

- [ ] Private GitHub staging repository is clean, reproducible, and correctly documented.
- [ ] Any public release has passed the workshop anonymity and artifact-release gates.
- [ ] Validation status is represented as technical-only, practitioner-reviewed, youth-informed, or independently evaluated only when the corresponding evidence exists.
- [ ] No participant-level sensitive data, contact information, or crisis disclosure is stored in GitHub.

## Risks and Mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| Public repository deanonymizes the double-blind submission | Critical | Use a private staging repository and preserve the anonymous ZIP until policy clearance. |
| GitHub issues receive real crisis disclosures | Critical | Add a prominent non-emergency notice, disable inappropriate issue paths, and direct vulnerability reports privately. |
| Protocol files are mistaken for completed validation | High | Use a validation-status table and repeat `protocol only; not started` in README, dataset card, and validation index. |
| Rushed youth recruitment creates ethical or safeguarding harm | Critical | Keep the gate closed until explicit minors approval and trained safeguarding coverage exist. |
| Human review contaminates benchmark evaluation | High | Freeze v0.1, preserve raw disagreement, version changes, and require a separate independent holdout for capability claims. |
| License choice unintentionally permits or blocks intended reuse | Medium | Require explicit code and data/documentation license approval before the first commit. |
| Invalid GitHub credentials block publication | Medium | Re-authenticate `gh` only after the plan and repository decisions are approved. |
| Generated and binary artifacts bloat history | Medium | Use an explicit tracked-file boundary and ignore build/render intermediates before the initial commit. |

## Open Questions Requiring Human Approval

- Approve the recommended private-first repository `saahirvazirani/ChildEsc`, or explicitly accept the double-blind risk of an immediate public repository.
- Select licenses. Recommended default: Apache-2.0 for code and CC BY 4.0 for synthetic data and documentation, subject to author and venue requirements.
- Decide whether the final workshop PDF belongs in the private staging repository now or should be added only after the anonymity period.

## GitHub Staging Execution Outcome (2026-08-18)

The approved private-first release is live at `https://github.com/saahirvazirani/ChildEsc` with `main` tracking `origin/main`. The repository contains source, synthetic data, aggregate diagnostics, anonymous manuscript source, prospective validation protocols, Apache-2.0 and CC BY 4.0 licensing, safety guidance, and a complete README. Rendered papers, Word files, supplement archives, templates, caches, local paths, credentials, and future participant-data paths are excluded.

Local and clean-clone reproduction pass 46 frozen scientific-artifact tests, five separate release tests, and the release audit. The initial hosted run exposed Python-version floating-point and CSV newline drift; commit `769fb21` repaired both with high-precision aggregation, explicit LF output, and regression coverage. GitHub Actions run `32183952057` then passed on Python 3.11 and 3.12. Public visibility remains blocked by the workshop anonymity gate. Practitioner and youth validation remain protocol-only and are correctly reported as not started.

# Implementation Plan: Provider-Neutral LLM Routing Evaluation

## Overview

Add an optional, dependency-free evaluation path that sends only synthetic
conversation text and a versioned routing prompt to Gemini, OpenAI, or
Anthropic. Provider responses are normalized to the existing `RouteDecision`
contract, stored in a content-addressed local cache, and replayable without
network access or credentials. This path evaluates routing actions and handoff
targets only. It does not generate or assess a supportive response.

## Architecture Decisions

- Preserve `evaluate_item` as the label-isolation boundary; an LLM never receives
  gold actions, target sets, severity labels, family identifiers, or authoring
  metadata.
- Use provider REST APIs through the Python standard library so the benchmark
  does not acquire provider SDK dependencies.
- Use one versioned system prompt, one canonical conversation serialization,
  and one JSON Schema across providers.
- Key cache entries by the complete non-secret request specification, including
  provider, model, endpoint mode, prompt, schema, generation settings, and
  conversation.
- Never cache credentials. Keep response caches ignored by Git because they may
  contain conversation text and provider metadata.
- Treat API errors, refusals, and schema-invalid outputs as recorded routing
  failures. Do not exclude them from denominators or silently retry them into a
  successful result.
- Keep LLM tests outside `tests/` so the manuscript's frozen 46-test scientific
  suite remains unchanged.

## Dependency Graph

```text
Versioned routing prompt + strict schema
    |
    +--> Provider request/response adapters
    |       |
    |       +--> Content-addressed response cache
    |               |
    |               +--> Cache-only replay
    |
    +--> Normalized route parser
            |
            +--> Routing-only evaluator and metrics
                    |
                    +--> CLI, documentation, and audit tests
```

## Phases

### Phase 1: Contract and Tests

- Specify the allowed action, target, risk-domain, and response-requirement
  vocabulary in one strict JSON Schema.
- Add tests for provider request shapes, response extraction, strict parsing,
  API-key omission from cache keys, cache hits, and cache-only misses.
- Add an end-to-end cached evaluation test proving that labels are not present
  in provider requests and no network transport is called during replay.

### Phase 2: Adapters and Cache

- Implement injectable Gemini, OpenAI, and Anthropic REST adapters against their
  official structured-output APIs.
- Implement atomic, content-addressed JSON cache writes and request-fingerprint
  verification on reads.
- Normalize valid outputs to `RouteDecision` and retain bounded provider
  metadata needed for auditability.

### Phase 3: Evaluation and Documentation

- Add a CLI with explicit provider/model selection, cache directory, cache-only
  mode, item limit, timeout, and output directory.
- Export routing predictions, standard ChildEsc metrics, invalid-result counts,
  cache telemetry, prompt/schema hashes, and run configuration.
- Document credentials, cost controls, reproducibility, limitations, and the
  separate human-validation study required to evaluate supportive responses.

## Risks and Mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| Gold-label leakage through request context | Critical | Build requests only from `conversation`; test sent payloads for forbidden benchmark fields. |
| Provider drift changes results | High | Record provider/model and cache exact raw responses; replay cached runs for analysis. |
| Invalid outputs inflate metrics if excluded | High | Record them as failures and include them in all-item denominators. |
| API keys or sensitive content enter Git | Critical | Exclude secrets from cache material, ignore cache directories, and retain release-audit checks. |
| Routing scores are misread as response quality | High | Name outputs routing-only and state the exclusion in CLI help, README, and run metadata. |

## Definition of Done

- All three providers produce the same normalized routing contract in tests.
- A cached run completes with no API key and no transport invocation.
- No benchmark label or authoring field is sent to a provider.
- Every invalid or failed provider result remains visible in output telemetry.
- Frozen scientific tests, release tests, LLM adapter tests, and the full
  reproduction pipeline pass.

## Execution Outcome (2026-08-19)

Implemented a two-field routing contract and standard-library REST adapters for
Gemini, OpenAI, and Anthropic. Content-addressed cache entries verify both the
complete non-secret request and raw provider response, while cache-only mode
fails closed before network access. The evaluator withholds comparative metrics
unless every requested item has a valid route and omits conditional bootstrap
intervals that a smoke-test slice cannot define. Thirteen no-network LLM tests,
the frozen 46-test scientific suite, five release tests, full reproduction, and
the release audit pass. No paid or live model evaluation was run. An attempted
read-only Gemini CLI review was stopped after repeated quota-exhaustion errors;
the confirmed smoke-slice bootstrap defect found during manual review was fixed
and regression-tested.
