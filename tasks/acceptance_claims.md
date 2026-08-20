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

> Who Is Safe to Involve? ChildEsc Audits Escalation and Handoff Routing in
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
| Action-only scoring can conceal recipient-selection failures | Three complete trials: 80.8% mean action accuracy versus 51.7% exact routing; 29.2-point gap | One pinned prompted router on provisional, policy-exposed synthetic labels |
| Recipient choice is a distinct and less stable routing decision | 40.7--43.6% target failure among action-correct handoffs; 1/80 action instability versus 18/80 full-route instability | Specification conformance, not observed real-world harm |
| ChildEsc makes action-plus-recipient constraints auditable | Versioned permitted/forbidden targets, strict deterministic scoring, item-level audit trails, and cache replay | Proposed measurement construct, not clinical or developmental validation |
| Practitioner and youth input is required before stronger claims | Prospective blinded practitioner and youth protocols with disagreement retention | No recruitment, review data, or validation statistic exists |
| Supportive-response quality remains a separate layer | Evaluator emits and scores only action and recipient targets | No therapeutic-helpfulness, language-safety, or response-quality claim |

## Permitted claims

- ChildEsc executes an auditable routing-only evaluation with strict structured
  outputs and deterministic target scoring.
- Prompted systems produce the reported action and target errors on the frozen,
  policy-exposed ChildEsc v0.1 set.
- The action-route gap identifies action-correct cases with missing,
  unpermitted, forbidden, or otherwise nonconforming target decisions.
- Cached outputs and exact manifests make reported provider runs replayable
  without credentials or network access.
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

1. The complete, replayable one-system prompted-router case study.
2. The frozen ChildEsc-Rules checksum as policy-exposed implementation evidence.
3. One action-correct but target-invalid example supporting the central thesis.
4. Construct limits and four workshop discussion questions.

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
uses 3--5 qualified adult practitioners blinded to existing labels, rules, and
model outputs on a stratified 24--32-item subset. It retains label distributions,
missing-context judgments, revisions, and unresolved disagreement rather than
manufacturing one consensus gold label. Youth participation remains prospective
pending separate minors-specific ethics and safeguarding approval.
