# ChildEsc Acceptance Claim Ledger

Freeze date: 2026-08-19

Submission shape: works-in-progress technical paper

## Reviewer-facing thesis

ChildEsc tests whether a prompted application-layer router selects both a
proportionate escalation action and a context-appropriate human-handoff target
for synthetic child-context conversations. Its distinctive question is not only
whether to escalate, but who is safe to involve when an adult or setting may be
implicated.

Submission title:

> Who Gets Involved? ChildEsc Audits Escalation and Handoff Routing in
> Child-Facing AI

## Construct chain

| Stage | Frozen definition |
|---|---|
| Phenomenon | Conformance to a proposed child-specific escalation and context-safe recipient specification |
| Task | Map a synthetic multi-turn conversation to one of four actions and zero or more target classes |
| Items | 80 policy-exposed synthetic conversations in 20 matched counterfactual families |
| Metrics | Under-escalation, urgent recall, strict target validity, unsafe-target rate, action-route gap, and exact route accuracy |
| Claims | Diagnostic behavior of prompted routers on this provisional synthetic specification |

## Claim-evidence matrix

| Submission claim | Evidence | Boundary |
|---|---|---|
| Action-only scoring can conceal recipient-constraint failures | Eight complete trials across three prompted systems: 80.0--83.1% mean action accuracy versus 33.8--51.7% exact routing; 29.2--49.4-point gaps | Provisional, policy-exposed synthetic labels; no model ranking or external generalization |
| Recipient choice is a distinct and less stable routing decision | 42.7--71.2% target failure among action-correct handoffs; 1.3--6.3% action instability versus 22.5--51.3% full-route instability | Primarily over-broad recipient sets and specification conformance, not observed real-world harm |
| ChildEsc makes action-plus-recipient constraints auditable | Versioned permitted/forbidden targets, strict deterministic scoring, item-level audit trails, grouped intervals, and hash-documented internal replay | Proposed measurement construct, not clinical or developmental validation; caches are not distributed |
| Practitioner and youth input is required before stronger claims | Prospective blinded practitioner and youth protocols with disagreement retention | No recruitment, review data, or validation statistic exists |
| Supportive-response quality remains a separate layer | Evaluator emits and scores only action and recipient targets | No therapeutic-helpfulness, language-safety, or response-quality claim |

## Permitted claims

- ChildEsc executes an auditable routing-only evaluation with strict structured
  outputs and deterministic target scoring.
- Prompted systems produce the reported action and target errors on the frozen,
  policy-exposed ChildEsc v0.1 set.
- The action-route gap identifies action-correct cases with missing,
  unpermitted, forbidden, or otherwise nonconforming target decisions.
- Retained caches enabled internal offline replay without new provider calls, while the anonymous
  supplement distributes normalized hashes, aggregates, and deterministic
  analysis code rather than raw provider responses or caches.
- The artifact supplies a concrete object for practitioner, youth, policy, and
  technical discussion about child-specific escalation.

## Prohibited claims

- ChildEsc is a validated, representative, realistic, clinical, or
  deployment-ready benchmark.
- A reported model is safer, clinically better, or generally superior to
  another model.
- The reported rates estimate real-world child-safety performance or population
  error.
- Correct routing implies a safe, helpful, age-appropriate, culturally
  responsive, or autonomy-preserving generated response.
- A target label establishes that a person or service is available, accessible,
  consensual, or successful.
- Practitioner review, youth review, independent holdout evaluation, or an
  operational service partnership has occurred.

## Main-paper evidence hierarchy

1. The complete cross-system prompted-router diagnostic.
2. The frozen ChildEsc-Rules checksum as policy-exposed implementation evidence.
3. One action-correct but target-invalid example supporting the central thesis.
4. Construct limits, broader impacts, and one focused workshop question.

Keyword and severity-agnostic baselines, full contract probes, stress tests,
and complete intervals belong in the appendix. Operational crisis-service
integration is separate governance research and is excluded from the
submission package.

## Validation status

Practitioner and youth validation have not occurred. Informal manuscript review,
if obtained, is editorial feedback only and cannot be reported as empirical
validation. No independently authored holdout exists because the current author
and coding agents have inspected the router, scenarios, and item-level errors.

Before any practitioner recruitment or response collection, the project must
obtain a written institutional determination. If authorized, the proposed audit
uses 8--12 qualified adult practitioners blinded to existing labels, rules, and
model outputs. The frozen base assignment uses eight 30-item packets over all
80 items, yielding three ratings per item. It retains label distributions,
missing-context judgments, revisions, and unresolved disagreement rather than
manufacturing one consensus gold label. Youth participation remains prospective
pending separate minors-specific ethics and safeguarding approval.

## Deadline-day comparison extension, 2026-08-29

Protocol v1.2 extends the same frozen routing-only task to the Gemini and GPT
families named in the original model manifest. These systems are construct
replications, not competitors. Every complete pre-specified run must be
disclosed, and the main claim is selected by the frozen result gate rather than
by favorable scores.

The incomplete informal review form remains editorial feedback only. Its
action choices and rationales exposed three useful manuscript risks without
validating any label: supportive conversation can be interpreted as compatible
with referral, missing immediacy/medical context can make forced actions
ambiguous, and target choices can depend on jurisdiction. The submission must
therefore define actions by intervention and routing obligations, treat abstention/clarification
as a v0.2 question, and preserve target uncertainty and disagreement in future
validation. Suggestions of automatic reporting, dispatch, or 988 involvement
are not evidence and remain outside ChildEsc.

Additional permitted claims depend on complete v1.2 evidence:

- positive gaps in both comparison systems permit a bounded statement that the
  action-route gap recurs across three prompted systems on ChildEsc v0.1;
- one completed positive comparison permits a statement that the gap appears in
  more than one prompted system; and
- heterogeneous or near-zero gaps permit only the statement that action-only
  accuracy incompletely characterizes routing and the discrepancy is
  system-dependent.

No comparison outcome permits a model winner, external generalization,
validated-benchmark, clinical, response-quality, or deployment claim.
