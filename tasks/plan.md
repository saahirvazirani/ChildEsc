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
conversation text and a versioned routing prompt to Gemini, OpenAI, Anthropic,
or OpenRouter. Provider responses are normalized to the existing `RouteDecision`
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

- Implement injectable Gemini, OpenAI, Anthropic, and OpenRouter REST adapters
  against their official structured-output APIs.
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

- All four providers produce the same normalized routing contract in tests.
- A cached run completes with no API key and no transport invocation.
- No benchmark label or authoring field is sent to a provider.
- Every invalid or failed provider result remains visible in output telemetry.
- Frozen scientific tests, release tests, LLM adapter tests, and the full
  reproduction pipeline pass.

## Execution Outcome (2026-08-19)

Implemented a two-field routing contract and standard-library REST adapters for
Gemini, OpenAI, Anthropic, and OpenRouter. Content-addressed cache entries
verify both the complete non-secret request and raw provider response, while cache-only mode
fails closed before network access. The evaluator withholds comparative metrics
unless every requested item has a valid route and omits conditional bootstrap
intervals that a smoke-test slice cannot define. Fifteen no-network LLM tests,
the frozen 46-test scientific suite, five release tests, full reproduction, and
the release audit pass. No paid or live model evaluation was run. An attempted
read-only Gemini CLI review was stopped after repeated quota-exhaustion errors;
the confirmed smoke-slice bootstrap defect found during manual review was fixed
and regression-tested.

# Acceptance-Maximization Plan: Child Safety in AI Workshop

## Overview

The highest-probability submission shape is a works-in-progress technical paper
that asks one memorable question: when a child-facing conversational model
escalates, does it identify a context-appropriate person or service rather than
defaulting to a potentially implicated adult? The current artifact already
specifies this construct and discloses its validity limits unusually well. Its
largest remaining acceptance weakness is empirical: all reported scores come
from policy-exposed lexical policies, even though the repository now has a
provider-neutral, leakage-tested LLM evaluation path. The acceptance-oriented
revision should replace some checksum detail with a small, frozen, multi-model
routing audit and use the resulting action-versus-target gap to demonstrate why
ChildEsc adds information beyond action-only scoring.

The goal is not to claim a validated benchmark or identify a winning model.
The goal is to establish technical utility, expose a concrete child-safety
failure mode, and give the workshop a precise construct and validation pathway
to debate.

## Evidence Basis

- The official workshop explicitly welcomes synthetic benchmarks, evaluation
  protocols, deployment safeguards, hotline collaboration, and child-centered
  design. It prioritizes productive workshop discussion alongside technical
  soundness: <https://childsafety-ai.github.io/>.
- MinorBench, accepted at the ICLR 2025 AI for Children workshop, combined a
  child-specific taxonomy with 299 prompts, six model evaluations, and system
  prompt comparisons: <https://openreview.net/forum?id=SmZcXcPBAU>.
- CAREBench evaluates 500 prompts on seven frontier models with three replicate
  generations and has parent, clinician, and safety-practitioner input. ChildEsc
  should not compete on breadth; it should isolate the distinct safe-recipient
  construct: <https://arxiv.org/abs/2606.29685>.
- MindEval validates both simulated-patient realism and automated judgment
  against expert judgments before making response-quality claims. This supports
  keeping generated supportive-response quality outside the current paper:
  <https://arxiv.org/abs/2511.18491>.
- CounselBench finds that LLM judges can overlook safety concerns identified by
  mental-health professionals. ChildEsc should retain deterministic route
  scoring and not add an unvalidated LLM judge:
  <https://arxiv.org/abs/2506.08584>.
- NeurIPS benchmark-validity guidance recommends an explicit chain from
  phenomenon to task, items, metrics, and claims, plus uncertainty and error
  analysis. ChildEsc should make that chain visible in the four-page paper:
  <https://proceedings.neurips.cc/paper_files/paper/2025/file/1967e0fc3aa6cbbace562f5cb8e3954e-Paper-Datasets_and_Benchmarks_Track.pdf>.

## Reviewer-Centered Diagnosis

| Dimension | Current state | Acceptance implication | Required action |
|---|---|---|---|
| Workshop fit | Strong alignment with synthetic evaluation and safeguards | Preserve and state directly | Frame as a discussion-ready works-in-progress audit |
| Novelty | Narrow but defensible: ordinal routing plus permitted and forbidden recipients | Make the recipient constraint the title-level hook | Stop presenting ordered actions as the novelty |
| Technical evidence | Reproducible but limited to policy-exposed rule checks | Largest remaining weakness | Add frozen prompted-model routing runs |
| Construct validity | Transparently incomplete | Acceptable for WIP if claims remain narrow | Keep practitioner and youth validation prospective |
| Statistical evidence | Grouped bootstrap exists for 20 families | Adequate for descriptive uncertainty, not ranking | Add paired family-level deltas and replicate instability |
| Practical impact | Clear developer use, but 988 extension is speculative | Main-text distraction and governance risk | Keep operational follow-up out of the four-page thesis |
| Reproducibility | Strong local artifact, cache, and leakage tests | Competitive advantage | Release anonymous cached outputs and exact run manifests |
| Discussion value | Present but diffuse | Workshop explicitly rewards it | End with three concrete questions for participants |

## Architecture Decisions

- Keep the submission category and claims consistent with a works-in-progress
  paper. Do not relabel ChildEsc as validated, representative, clinical, or
  deployment-ready.
- Define the measured phenomenon as route conformance under the ChildEsc
  specification, not general child safety, mental-health support quality, crisis
  prediction, or real-world handoff success.
- Freeze `benchmark/childesc_v0_1.jsonl`, its labels, the routing prompt, schema,
  primary metrics, model set, and analysis plan before the first full model run.
- If a genuinely unexposed adult collaborator is available by August 20,
  prioritize a small sealed set of independently authored counterfactual
  families over adding the third provider. The collaborator must not inspect
  the current scenarios, labels, router, prompt, or item-level errors before
  authoring. If that boundary cannot be maintained, skip the holdout and report
  none rather than generating more same-workflow data.
- Evaluate three prompted model routers from different providers, using exact
  provider model identifiers and identical visible task instructions. Candidate
  models are Gemini `gemini-3.1-pro-preview`, OpenAI
  `gpt-5.5-2026-04-23`, and Anthropic `claude-sonnet-5`, subject to a
  documented API capability preflight immediately before freezing.
- Prefer direct-provider results in the paper. Use OpenRouter for portability
  testing or a fallback only; do not treat an OpenRouter slug as a controlled
  provider comparison unless the upstream endpoint and returned model version
  are pinned and recorded.
- Run three independently cached trials per model because provider outputs can
  vary even for classification. Record every attempt and do not silently replace
  malformed responses or provider failures.
- Do not add an LLM judge. The model returns only the two-field route, and all
  reported scoring remains deterministic against the provisional reference
  action and target constraints.
- Make the primary technical result the action-route gap: the number and rate of
  cases whose action is correct but whose handoff target is missing,
  unpermitted, or forbidden. This directly tests the paper's unique thesis.
- Keep the current checksum as an auditable reference implementation. Move the
  Keyword and Agnostic rows, stress tests, full contract table, and secondary
  metrics to the appendix if space is needed.
- Remove the prospective 1--24 hour 988 mechanism from the four-page main text.
  The appendix may retain it as explicitly non-operational governance work, but
  it is not evidence for ChildEsc and should not compete with the central claim.

## Pre-Registered Evaluation Contract

### Systems

| Role | System | Reporting rule |
|---|---|---|
| Primary | Three direct-provider prompted model routers | Three complete cached trials per model |
| Checksum | Frozen `ChildEsc-Rules` | One deterministic run, labeled policy-exposed |
| Appendix baselines | Keyword and severity-agnostic rules | Diagnostic only |
| Portability | OpenRouter adapter | Smoke result only unless endpoint provenance is pinned |

### Primary Estimands

| Estimand | Denominator | Reason |
|---|---|---|
| Under-escalation rate | Items requiring human or urgent support | Captures missed escalation without dilution by low-risk items |
| Urgent recall | Urgent-reference items | Makes urgent-to-human downgrades visible |
| Strict target validity | Items requiring a target | Measures whether every emitted recipient is permitted and none forbidden |
| Action-route gap | All items, with paired count among action-correct handoffs | Shows what action-only evaluation misses |
| Unsafe implicated-adult rate | Items with a forbidden recipient | Tests the paper's child-specific handoff constraint |
| Exact route accuracy | All items | Requires both action and recipient conformance |

Macro F1, counterfactual sensitivity, monotonicity violations, family/domain
breakdowns, malformed-output counts, and target-error categories remain
secondary. No aggregate safety score is created.

### Inference and Stability

- Keep the four variants of each family together in all resampling.
- Report point estimates and 95% family-bootstrap intervals for each model.
- Report paired family-bootstrap intervals for model-to-model differences only
  in the appendix; do not declare a winner from overlapping point estimates.
- Report the proportion of items with action or target disagreement across the
  three trials. Summarize primary metrics across trials without pooling 240
  correlated outputs as if they were independent items.
- Treat invalid structured outputs and provider failures as observable system
  failures. A primary table row requires a complete, auditable run policy; all
  failed attempts remain in the run ledger.

### Claim Boundary

Permitted claims are that ChildEsc can execute a reproducible routing audit,
that prompted systems exhibit particular errors on this policy-exposed
synthetic set, and that target constraints reveal failures hidden by action-only
scoring. Prohibited claims include model safety rankings, clinical accuracy,
population error rates, realistic child behavior, successful crisis referral,
or safe supportive responses.

## Dependency Graph

```text
Acceptance thesis and claim freeze
    |
    +--> Evaluation manifest and primary estimands
    |       |
    |       +--> Conditional independent holdout decision
    |       |
    |       +--> Replicate-aware cache and attempt ledger
    |               |
    |               +--> Provider capability smoke tests
    |                       |
    |                       +--> Three complete model audits
    |                               |
    |                               +--> Paired analysis and error cases
    |
    +--> Four-page page ledger
            |
            +--> Main-table replacement and narrative rewrite

Model evidence + four-page rewrite
    |
    +--> Methodologist review
    +--> Practitioner editorial review, if available
            |
            +--> Claim reconciliation, anonymity audit, final package
```

## Task List

### Phase 1: Freeze the Acceptance Thesis

- [ ] Task 31: Freeze the paper as a works-in-progress audit of escalation and
  context-safe recipients, with a one-sentence phenomenon/task/metric/claim
  chain.
- [ ] Task 32: Pre-register exact model IDs, trial count, settings, primary
  estimands, retry policy, exclusions, and fallback rules before live runs.
- [ ] Conditional Task 32A: If an eligible unexposed collaborator is available,
  seal a small independently authored family set before model evaluation;
  otherwise record the failed eligibility gate and do not create a holdout.

### Checkpoint: Protocol Freeze

- [ ] Benchmark, labels, prompt, schema, model manifest, and analysis plan have
  hashes and timestamps.
- [ ] No live prompted-model result has been inspected before the protocol
  freeze; the already reported deterministic checksum remains explicitly
  policy-exposed.
- [ ] Provider credentials and cost approval are available for at least one
  primary model; unavailable providers trigger a disclosed fallback, not a
  silent model substitution.

### Phase 2: Produce Model Evidence

- [ ] Task 33: Add replicate-aware run identity, append-only attempt logging,
  and deterministic aggregation tests without changing the frozen benchmark.
- [ ] Task 34: Run four-item provider smoke tests, inspect request isolation and
  structured outputs, then execute three complete trials for each available
  primary model.
- [ ] Task 35: Add action-route-gap, action-correct target-failure, replicate
  instability, and paired family-bootstrap analyses.

### Checkpoint: Evidence Integrity

- [ ] Every primary result replays from cache without credentials or network.
- [ ] Every attempted item is accounted for, including malformed responses and
  provider errors.
- [ ] Exact prompts, schemas, model versions, timestamps, settings, hashes, and
  provider metadata accompany the results.
- [ ] A frozen analysis script regenerates every number proposed for the paper.

### Phase 3: Rewrite the Four-Page Paper

- [ ] Task 36: Replace the generic title and checksum-centered abstract with the
  safe-recipient question, a concrete model-audit finding, and the validation
  boundary.
- [ ] Task 37: Replace the current three-rule table with one compact model-plus-
  checksum table and a paired action-versus-route failure visualization or
  concise error table.
- [ ] Task 38: Rebalance page four around limitations, actionable impact, and
  three workshop questions; move the delegated 988 mechanism and procedural
  validation detail to the appendix.

### Checkpoint: Reviewer Read

- [ ] A reviewer can identify the new construct, technical method, strongest
  result, and evidence boundary from the title, abstract, and one table.
- [ ] The main text directly distinguishes ChildEsc from CAREBench, KIDBench,
  MinorBench, and CARE-Bench without claiming ordered routing as novel.
- [ ] References start on page five without template compression.

### Phase 4: Independent Review and Submission QA

- [ ] Task 39: Obtain one benchmark-methodology review and, if available, one
  youth-facing practitioner editorial review after the model analysis is frozen.
- [ ] Task 40: Reconcile reviews as confirmed defects, plausible concerns, or
  optional improvements; repair only confirmed defects and high-value concerns.
- [ ] Task 41: Build the anonymous supplement, run clean-room cache replay and
  artifact tests, inspect every PDF page, and scan all files for identity or
  provider-secret leakage.

### Final Checkpoint

- [ ] The four-page submission is technically self-contained and discussion-
  ready even if the appendix is not read.
- [ ] Practitioner and youth validation are still described as not completed.
- [ ] Editorial feedback is not reported as empirical validation or participant
  data.
- [ ] The anonymous artifact contains reproducible synthetic data, cached model
  outputs permitted for release, and no credentials, PII, or real disclosures.
- [ ] The final manuscript contains no model-ranking, clinical, 988-partnership,
  or deployment-readiness claim.

## Four-Page Revision Budget

| Page | Acceptance job | Content to preserve or add | Content to move |
|---|---|---|---|
| 1 | Make the paper memorable | Safe-recipient hook, closest-work gap, narrow contributions | Long benchmark catalog |
| 2 | Make the construct credible | Scope, matched families, actions and target constraints, provenance | Full taxonomy and equations |
| 3 | Prove technical utility | Model protocol, primary metrics, model-plus-checksum table, action-route gap | Keyword/Agnostic detail and full CIs |
| 4 | Earn workshop fit | Failure example, validity boundary, impact path, three discussion questions | 988 timing mechanism and full validation gates |

## Workshop Discussion Questions

The final paper should end with questions that the reported artifact makes
concrete rather than generic future work:

1. When context is incomplete, should a child-safety router abstain, ask a
   question, or offer multiple consent-preserving routes?
2. How should practitioner risk judgments and young people's judgments of
   agency, plausibility, and coercion be kept distinct when validating handoff
   targets?
3. What evidence and governance gates are required before a target label such
   as `crisis_service` can become an operational referral pathway?

## Fallback Ladder

| Trigger | Submission fallback |
|---|---|
| Three providers complete by August 23 | Report all three with replicate stability |
| Two providers complete | Report two plus checksum; avoid broad cross-provider claims |
| Only Gemini completes | Report one prompted-router case study plus checksum and emphasize evaluation infrastructure |
| No live run completes | Keep the current checksum paper, remove any claim that model evaluation has occurred, and emphasize the released protocol |
| Independent practitioner or holdout author is unavailable | Preserve protocol-only validation and do not recruit or generate a same-workflow holdout |

## Explicit Stop-List

- Do not rush youth recruitment or collect personal disclosures before an
  appropriate institutional and safeguarding route is documented.
- Do not describe informal practitioner comments as validation, expert labels,
  or study evidence.
- Do not tune the prompt, labels, or model settings after inspecting primary
  results unless the affected run is clearly redesignated as development-only.
- Do not add more LLM-authored families from the same policy-exposed workflow to
  create the appearance of scale.
- Do not score supportive-response quality, empathy, clinical appropriateness,
  or cultural responsiveness in this paper.
- Do not use an LLM-as-a-judge for target correctness when the current target
  schema supports deterministic scoring.
- Do not make the proposed 988 data-transfer and 1--24 hour follow-up mechanism
  a main-paper contribution or imply a service partnership.
- Do not publish the identity-linked GitHub repository before the double-blind
  policy permits it.

## Schedule

| Date | Deliverable |
|---|---|
| August 19 | Acceptance thesis, model set, estimands, and fallback policy frozen |
| August 20 | Holdout eligibility decided; replicate and attempt-ledger support complete and tested |
| August 21 | Provider smoke tests and capability manifest complete |
| August 22--23 | Full model runs, cache replay, and primary analysis complete |
| August 24 | Evidence freeze and four-page table selected |
| August 25 | Main paper and appendix rewritten |
| August 26 | Independent methodology and practitioner editorial reviews |
| August 27 | Confirmed defects repaired; no new exploratory experiments |
| August 28 | Final page, anonymity, clean-room, and submission checks |
| August 29 | Submission buffer |

## Risks and Mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| Model results look like rankings on an unvalidated set | Critical | Call them prompted-router diagnostics and foreground the policy-exposed set |
| Provider drift or aliases undermine reproducibility | High | Use pinned IDs where available, record returned versions, and release cache replay |
| Repeated runs are silently deduplicated by the cache | High | Add an explicit trial identifier to cache provenance and test independent attempts |
| Transient errors disappear during reruns | High | Use an append-only attempt ledger and pre-specified completion policy |
| The model table crowds out the construct | High | Replace checksum detail rather than adding a second large table |
| Target scoring appears arbitrary | High | Show the phenomenon-to-claim chain and one implicated-adult counterexample |
| A rushed holdout repeats circular authoring | High | Require an unexposed independent author or report no holdout |
| Validation language outruns completed evidence | Critical | Preserve protocol-only wording and run a phrase-level claim audit |
| The 988 extension dominates reviewer attention | High | Remove it from main-text contributions and keep it non-operational in the appendix |
| Provider terms prohibit releasing raw responses | Medium | Review terms before the run and release normalized outputs plus hashes if raw cache release is not permitted |

## Definition of Done

- The title, abstract, and main result all center the same safe-recipient thesis.
- At least one prompted model router has a complete, replayable full evaluation;
  the preferred outcome is three models with three trials each.
- Primary results include the action-route gap and implicated-adult target errors,
  not only macro F1 or exact accuracy.
- All empirical claims are bounded to the policy-exposed synthetic testbed.
- The fourth page creates concrete workshop discussion rather than adding an
  operational policy proposal.
- The submission remains at most four content pages, anonymous, reproducible,
  and free of unsupported practitioner, youth, clinical, or service claims.
