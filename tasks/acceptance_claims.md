# ChildEsc Acceptance Claim Ledger

Freeze date: 2026-08-19

Submission shape: works-in-progress technical paper

## Reviewer-facing thesis

ChildEsc tests whether a prompted application-layer router selects both a
proportionate escalation action and a context-appropriate human-handoff target
for synthetic child-context conversations. Its distinctive question is not only
whether to escalate, but who is safe to involve when an adult or setting may be
implicated.

Proposed title after model evidence is frozen:

> Who Is Safe to Involve? ChildEsc Audits Escalation and Handoff Routing in
> Child-Facing LLMs

## Construct chain

| Stage | Frozen definition |
|---|---|
| Phenomenon | Conformance to a proposed child-specific escalation and context-safe recipient specification |
| Task | Map a synthetic multi-turn conversation to one of four actions and zero or more target classes |
| Items | 80 policy-exposed synthetic conversations in 20 matched counterfactual families |
| Metrics | Under-escalation, urgent recall, strict target validity, unsafe-target rate, action-route gap, and exact route accuracy |
| Claims | Diagnostic behavior of prompted routers on this provisional synthetic specification |

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
- Practitioner review, youth review, independent holdout evaluation, or a 988
  partnership has occurred.

## Main-paper evidence hierarchy

1. Prompted-model routing evidence, if a complete frozen run exists.
2. The frozen ChildEsc-Rules checksum as policy-exposed implementation evidence.
3. One action-correct but target-invalid example supporting the central thesis.
4. Construct limits and three workshop discussion questions.

Keyword and severity-agnostic baselines, full contract probes, stress tests,
complete intervals, and the non-operational delegated-follow-up proposal belong
in the appendix.

## Validation status

Practitioner and youth validation have not occurred. Informal manuscript review,
if obtained, is editorial feedback only and cannot be reported as empirical
validation. No independently authored holdout exists because the current author
and coding agents have inspected the router, scenarios, and item-level errors.

