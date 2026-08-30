# Reviewer Statement Reconciliation

Date: 2026-08-29

This record reconciles the external review against the submission source,
official style file, frozen protocols, analysis code, and distributed artifact.
It is an internal validity record, not part of the anonymous supplement.

| Review statement | Assessment | Evidence and action |
|---|---|---|
| The paper is a strong workshop fit but acceptance cannot be guaranteed. | Valid. | The contribution matches restricted-data evaluation and deployment safeguards, but reviewer assignment and competition are unknowable. No acceptance guarantee is made. |
| The workshop template may be misconfigured because the PDF has a generic footer. | Not a defect. | `paper/main.tex` already uses `dblblindworkshop` and defines `\workshoptitle{Child Safety in AI}` without `final`. The official `neurips_2026.sty` emits the generic conference footer for anonymous non-final submissions; the workshop title is used in final mode. Regression tests now preserve the required source configuration. |
| The checklist contradicts API compute, broader impacts, and interval reporting. | Obsolete as a checklist issue; the underlying disclosure concerns are valid. | The checklist was already removed as requested and is excluded from the supplement. API cost remains disclosed in Appendix L; a broader-impacts paragraph was added; computed family-bootstrap intervals are now exported and shown in the appendix. |
| The main result primarily measures extra unpermitted classes, not demonstrated unsafe recipients. | Confirmed validity defect in interpretation. | All 247 target-invalid, action-correct handoffs contain an extra unpermitted class; only two also intersect a forbidden class. The paper now calls the metric `TgtFail` and explicitly frames it as over-broad provisional recipient sets and specification conformance, not demonstrated real-world harm. |
| The four actions should not all be described as handoff obligations. | Confirmed terminology defect. | The revised definition distinguishes boundary-setting without human handoff from non-urgent and urgent human pathways, while allowing supportive language with every action. |
| Protocol v1.1 and v1.2 differences and the claim gate are unclear. | Confirmed presentation defect. | The paper now states that v1.2 changed no benchmark item, label, prompt, schema, request setting, score, or retry rule, and explains the frozen system identities, inclusion/spend rules, and zero/one/both positive-gap claim language. |
| Reviewer-facing cache replay is overstated. | Confirmed presentation defect. | Internal replay used retained caches, but raw responses and caches are excluded from the anonymous supplement. The paper and supplement now distinguish internal replay from reviewer-verifiable hashes and deterministic analyses. |
| KORA should be discussed. | Plausible reviewer concern. | KORA is now cited as a related multi-turn child-safety benchmark; ChildEsc is distinguished by application-layer action-plus-recipient constraint conformance rather than generated-response grading. |
| Grouped intervals and instability definitions are promised but not surfaced. | Confirmed aggregation and presentation defect. | The analysis now preserves per-trial family-bootstrap intervals in the aggregate JSON and exports a 64-row interval CSV. The appendix reports central intervals and formally defines action instability and RouteVar. Counterfactual and monotonicity diagnostics are explicitly labeled artifact computations. |
| Bibliography capitalization and model identity need polish. | Valid optional improvement. | Acronyms are brace-protected, recent arXiv URLs are included, `Gemini 3.1 Pro Preview` is used consistently, and exact provider slugs plus dated endpoint snapshots are documented. |
| The four workshop questions should be retained. | Reasonable but superseded by a stronger editorial choice. | A previous revision intentionally removed the four-question block to avoid making the paper read as under-specified. The conclusion now retains one focused workshop question about missing context, disagreement, and provisional routes. |
| “Who Is Safe to Involve?” may imply validated safety. | Valid reviewer-perception risk. | The title is now “Who Gets Involved?”, preserving the hook without implying validated recipient ground truth. |

The unresolved root risk remains substantive target validity. Practitioner and
youth validation are prospective and explicitly disclosed as incomplete; no
current result establishes child-centeredness, clinical validity, recipient
safety, or deployment readiness.
