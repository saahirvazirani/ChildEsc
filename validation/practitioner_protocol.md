# Prospective Practitioner Construct-Review Protocol

Status: protocol only; recruitment and data collection are not authorized

## Objective

Assess whether ChildEsc's proposed action ordering and handoff-target constraints are understandable, defensible, and sufficiently contextualized for child-safety escalation research. This review would test construct and content validity, not clinical effectiveness or deployment safety.

## Reviewer groups

Subject to institutional approval, recruit 8-12 adults across at least three roles:

- Youth-facing mental-health or crisis-support practitioners.
- Child-protection or safeguarding practitioners.
- Digital-safety, online-exploitation, or platform-trust practitioners.

Collect role and broad experience band only as needed for analysis. Do not collect client information or ask reviewers to disclose identifiable cases.

## Sampling

- Freeze ChildEsc v0.1 before recruitment.
- Use all 80 synthetic items in a balanced incomplete-block design.
- Assign approximately 30 items per reviewer so every item receives at least three independent ratings where sample size permits.
- Balance each packet across domain, severity, age band, and implicated-adult status.
- Randomize item order within packet with a recorded seed.
- Do not show router predictions during independent labeling.

## Review procedure

1. Provide content warning, scope, target definitions, and the right to skip any item.
2. Obtain consent under the approved protocol.
3. Present synthetic conversations without reference action, target labels, or router output.
4. Collect the structured rubric in `practitioner_rubric.csv`.
5. Ask for optional concise rationale without requesting real-case details.
6. Show no aggregate results until independent ratings are locked.
7. Offer a debrief and researcher-wellness resources defined by the approved protocol.

## Primary constructs

- Ordinal escalation action.
- Permitted and forbidden target classes.
- Whether material context is missing.
- Whether the route could be coercive or unsafe.
- Whether the item is too ambiguous to label responsibly.
- Jurisdictional or cultural dependence.

## Analysis boundary

- Report distributions and disagreement, not one forced consensus label.
- Use ordinal weighted agreement for actions only if its assumptions fit the final design.
- Report pairwise Jaccard agreement and per-target prevalence for set-valued targets.
- Stratify descriptively by practitioner role; do not make underpowered group-effect claims.
- Preserve the original labels and all pre-adjudication ratings.
- Route contested urgent or child-protection cases to qualified adjudication, but retain the disagreement record.

## Revision policy

Review findings create a new benchmark version. They do not overwrite v0.1. A revision log must record each changed action, target, scenario, or definition and the evidence motivating it. Router rules may not be tuned on the practitioner-reviewed evaluation set and then reported as held-out performance.

## Excluded claims

Completion would not establish therapeutic benefit, crisis-triage accuracy, legal compliance, cultural universality, successful handoff, or safe autonomous deployment.
