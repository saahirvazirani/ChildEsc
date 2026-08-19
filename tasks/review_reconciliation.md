# Cross-Model Review Reconciliation

Reviews compared:

- Fresh-context adversarial reviewer.
- Gemini CLI 0.55.1 in read-only plan mode.

The reviews are evidence, not verdicts. Findings were checked against source, generated data, and metrics before classification.

## Confirmed validity defects

1. **Policy exposure and circularity.** Scenario cues, initial labels, and lexical rules were drafted in the same workflow. Exact phrase overlap makes the current run in-sample. The paper now calls it a policy-exposed diagnostic checksum, removes superiority claims, and requires a separately authored lexical holdout before comparison.
2. **Oracle adult-implication leakage.** Evaluation passed `adult_implicated` directly to routers. The evaluator now passes conversation text only; the diagnostic router infers implication from text, and a spy-router regression test enforces this boundary.
3. **Vacuous forbidden targets.** Source labels used `caregiver` and `coach`, which no policy could emit. Forbidden labels now use the emittable `safe_adult` class, while implicated cases may permit `safe_adult_not_implicated`.
4. **Permissive exact-route scoring.** The previous metric allowed extra unpermitted targets and any target on no-handoff cases. Strict validity now requires a nonempty predicted set to be a subset of permitted targets and disjoint from forbidden targets; targetless actions must emit no target.
5. **Invalid delay claim.** Onset was mechanically derived from severity and non-detections were treated as a finite mean despite being described as censored. Version 0.1 now records the actual fixed decisive cue turn, removes delay evaluation, and states that this construction cannot support latency claims.
6. **Under-escalation presentation.** The prior severe-miss rate used all 80 items as denominator and did not foreground urgent-to-human misses. The artifact now reports any and severe under-escalation among the 58 escalation-required items, plus urgent recall.
7. **Missing result synchronization.** A regression test now derives the expected LaTeX rows from `results/metrics.json`; the suite increased from 17 to 25 tests.

## Plausible reviewer concerns

1. **Stagnation is not a monotonicity violation, but it is unsafe non-responsiveness.** The original monotonicity definition was mathematically correct. A separate counterfactual-sensitivity metric now measures upward prediction changes when reference action rises.
2. **Closest-work overlap was understated.** CAREBench and KIDBench already cover crisis referral, de-escalation, boundaries, and trusted-adult redirection. The novelty claim is narrowed to an ordinal application-layer router with severity-matched counterfactuals and explicit permitted/forbidden target sets.
3. **Twenty selected families cannot support population claims.** Bootstrap intervals are retained only as selected-family variation diagnostics; the paper explicitly disclaims population uncertainty and protection from tuning bias.
4. **Child-centeredness is not measured.** The paper now identifies it as a design objective rather than an established property and separates route conformance from language, agency, coercion, access, and successful handoff.

## Optional improvements deferred

1. Add misspellings, paraphrases, longer third-person reports, multilingual cases, and adversarial obfuscation only in a separately authored holdout. Adding them post hoc to the exposed set would deepen tuning leakage.
2. Expand the family count after practitioner and youth review rather than generating more unvalidated synthetic volume.
3. Evaluate handoff wording, consent, perceived coercion, localization, and successful connection in the human validation study.
4. Replace or supplement the deterministic checksum with model-based policies only after the specification and held-out set are frozen.

## Residual trade-offs

- The current router remains deliberately brittle and should not be deployed.
- `safe_adult_not_implicated` is a proposed abstraction, not proof that a safe person is available.
- Reference labels remain provisional and the schema field `gold_action` is retained only for compatibility.
- The repaired artifact is suitable as a works-in-progress specification and reproducibility package, not as a validated benchmark result.

## Revision review, 2026-08-17

A second fresh-context, read-only review identified five confirmed defects. All were verified against the workspace rather than accepted automatically:

1. **Stale named PDF and supplement:** confirmed. The final build and supplement are regenerated only after all review repairs and clean-room checks.
2. **Reproduction ordering:** confirmed. `make reproduce` now regenerates the benchmark, predictions, metrics, and analyses before running synchronization tests.
3. **Target-error precedence:** confirmed. Forbidden-target intersections now take precedence even when the permitted set is empty, with a regression test.
4. **Undefined conditional bootstrap draws:** confirmed. Draws with no eligible rows are excluded from that metric's interval rather than encoded as zero, with a regression test.
5. **Narrative test-count drift:** confirmed. The manuscript reports 36 tests, and a synchronization test derives the current discovered count.

The reviewer also raised plausible concerns about independently unverifiable pre-specification, incomplete future-study details, unvalidated ordinal and target-sufficiency constructs, and an incomplete Agnostic description. The paper now uses the narrower phrase “developer-specified before execution,” calls human review a prospective protocol, preserves the construct-validity limitation, and describes all Agnostic boundary branches. No practitioner, youth, or independent-holdout evidence is claimed.

## Fourth-page and delegated-follow-up review, 2026-08-18

### Confirmed validity defects repaired

1. **Source-identity mismatch.** The source register incorrectly linked the Cha et al. practitioner study to the K-AI Trust DOI and used the wrong MindEval arXiv identifier. The register now points to `2608.07902` and `2511.18491`, matching the bibliography.
2. **Unverified 988 capability.** The proposed text stated that 988 would receive chatbot-company data and contact users within 1-24 hours. No agreement or official policy supports that claim. The paper now labels it a prospective extension and explicitly states that it is not an established 988 policy.
3. **Bundled consent and mandatory identifiers.** Requiring phone/email and placing disclosure permission in general terms would not establish meaningful authorization. The extension now requires separate, affirmative, revocable, age-appropriate consent and cannot condition account access.
4. **Delayed handling of imminent danger.** A 1-24 hour queue could be unsafe for attempts in progress or imminent danger. Those states now bypass delayed scheduling and remain subject to immediate, least-invasive support under a qualified human protocol.
5. **Unvalidated cutoff formula.** No committee has researched, calibrated, or implemented the proposed formula. The specification leaves it unimplemented and requires independent prospective calibration, pre-registration, monotonicity, uncertainty-aware abstention, subgroup audits, and multidisciplinary ownership.

### Plausible reviewer concerns retained

1. Even a consent-based pathway may chill help-seeking, create wrong-person disclosures, or burden crisis-service capacity. These are pre-specified outcomes and activation gates, not assumed mitigations.
2. The extension may distract from ChildEsc's primary benchmark contribution. It is confined to one impact paragraph and the appendix, with current behavior unchanged.
3. A user may lack a safe private device or contact channel. Human review and safe-channel confirmation are required before any prospective transfer.

### Optional improvements deferred

1. Do not choose numerical cutoff coefficients before a formal partner committee and prospective outcome definition exist.
2. Do not implement OAuth, PII storage, or 988 APIs in the research artifact; doing so would imply operational readiness and create unnecessary security risk.
3. Add a separate participatory study of consent comprehension and chilling effects only after institutional and safeguarding approval.

### External review status

Gemini CLI was run in read-only plan mode. After repeated provider `503` and quota retries, the fallback model produced eight findings. The two router failures were confirmed but were already retained and reported; circularity, construct validity, novelty, and the 988 pathway remained plausible concerns already bounded in the paper. One new confirmed framework defect was repaired: the contract harness now accepts interleaved user/assistant turns instead of rejecting every non-user message, with a regression test. The optional B3 analogy was removed from the main paper to keep workshop fit focused. The artifact then passed 46 tests, page-boundary scans, visual renders, anonymity scans, and a zero-finding DOCX accessibility audit.

## OpenRouter smoke review, 2026-08-19

### Confirmed validity defect repaired

1. **Ambiguous prompt-hash semantics.** The frozen manifest hashed the prompt file bytes, including its trailing newline, while evaluator run records hashed the stripped text actually sent to providers. Protocol 1.0.1 now records both hashes explicitly. This is a metadata-only repair; the transmitted prompt and all experimental settings are unchanged.

### Plausible reviewer concern retained

1. **Reasoning-token exhaustion.** A frozen four-item OpenRouter smoke of `google/gemini-3.1-pro-preview` produced two valid routes and two length-truncated outputs because provider-default reasoning consumed nearly all of the 256-token completion allowance. The trial remains incomplete, receives no metrics, and will not be silently retried or repaired.

### Optional improvement deferred

1. A future protocol version may pre-specify a larger output budget or an explicit reasoning setting. Making that change after seeing this smoke would define a new experiment, so protocol 1.0.1 keeps the frozen 256-token budget and default reasoning behavior.

### Full-trial execution outcome

Three 80-item OpenRouter trial attempts were retained but are incomplete. The account exhausted its available credits after 66 valid responses and three length-truncated responses across the trials; the other 171 calls returned HTTP 402. Valid calls also reported two AWS upstream labels. No recovery call was made, and no score from these incomplete v1.0.1 attempts is added to the paper. A future execution must use new trial IDs and retain these failures. If it changes the token budget, reasoning setting, or upstream routing policy, it must be declared as a new protocol version rather than a repair to these trials.

## Post-pilot v1.1.1 review, 2026-08-19

### Confirmed validity defects repaired

1. **The failed pilot could not be silently resumed.** The v1.0.1 runs remain
   incomplete and unscored. The 1,024-token allowance, low reasoning policy,
   Anthropic-only routing, and new trial IDs are explicitly versioned as v1.1.
2. **Returned model identity required an auditable gate.** The v1.1 smoke
   returned OpenRouter's short alias despite a dated requested slug. Before any
   full trial, amendment v1.1.1 accepted that alias only with provider
   `Anthropic` and a frozen public alias-to-canonical snapshot. The amendment
   changed metadata validation only, not the prompt, labels, settings, metrics,
   or correctness criteria.

### Plausible reviewer concerns retained

1. **The configuration is post-pilot.** It was pre-specified only after failed
   operational pilots, so the paper says this directly and avoids a stronger
   preregistration claim.
2. **The evaluation covers one prompted router on the exposed v0.1 labels.**
   Three trials measure repeatability, not cross-model superiority or external
   generalization.
3. **High urgent recall does not establish safe routing.** Exact routes remain
   only 51.7% accurate because missing and extra unpermitted recipients count as
   failures even when the action is correct.

### Optional improvements deferred

1. Add a separately authored holdout only through the documented contributor
   eligibility and freeze process; the current author and coding agents are not
   eligible holdout authors.
2. Add a direct-provider or multi-model panel only under a new frozen protocol;
   it is not needed to support the current construct-level finding.
3. Evaluate supportive-response quality only with a separate rubric and
   appropriately governed practitioner and youth study.

### Verified outcome

All three v1.1.1 trials completed with 80/80 valid routes and replayed from
content-addressed caches without credentials. Across trials, mean action
accuracy was 80.8%, exact route accuracy was 51.7%, and the action-route gap was
29.2 points. Only 1/80 items varied in action, while 18/80 varied in full route.
These values are routing-specification diagnostics, not clinical or deployment
evidence.
