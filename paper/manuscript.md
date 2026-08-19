# Who Is Safe to Involve? ChildEsc Audits Escalation and Handoff Routing in Child-Facing AI

Anonymous workshop submission draft. The submission-authoritative source is `main.tex`; this Markdown copy is provided for collaborative editing.

## Abstract

Child-facing AI must decide not only whether to escalate, but *who is safe to involve*. Action-only evaluation can therefore reward a route that selects the right urgency while directing a child toward an inappropriate recipient. We introduce ChildEsc, a works-in-progress testbed of 80 LLM-assisted synthetic conversations in 20 counterfactual families. Each item specifies one of four actions plus permitted and forbidden handoff targets. We define the *action-route gap*: exact action accuracy minus exact action-plus-target routing. A policy-exposed deterministic checksum achieves 65.0% action accuracy but 53.8% exact routing, an 11.3% gap; 9/37 action-correct handoffs violate target constraints. A frozen relational contract audit passes 36/39 assertions across 7/9 families and retains two actionable failures. We also provide a provider-neutral, cache-replayable protocol for prompted-router audits, but report no live-model comparison because frozen credentials were unavailable. ChildEsc contributes an auditable routing specification and evidence gates, not a validated benchmark: practitioner and youth validation have not occurred, and no result supports deployment.

## Main Paper

The complete main paper, references, appendices, source register, relational contract audit, representative examples, metric definitions, validation protocol, compute disclosure, ethical release notes, and NeurIPS checklist are maintained in `main.tex`. All empirical values are generated from versioned result files; `make reproduce` regenerates the testbed, metrics, error taxonomy, input-evidence ablations, orthographic checks, guard probes, contract assertions, and paper tables. The prompted-router harness supports auditable live trials and cache-only replay, but no live-model result is reported. No practitioner or youth validation has occurred; the validation materials are prospective protocols only.
