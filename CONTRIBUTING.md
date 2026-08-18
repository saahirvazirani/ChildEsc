# Contributing to ChildEsc

ChildEsc welcomes reproducibility fixes, construct critiques, safer synthetic
counterexamples, documentation improvements, and independently authored test
families. Contributions must preserve the project's evidence boundaries.

## Before opening an issue

- Read `README.md`, `benchmark/DATASET_CARD.md`, and `validation/README.md`.
- Use synthetic examples only.
- Do not post personal crisis disclosures, identifying child data, clinical
  records, recruitment information, or participant responses.
- Use the private route in `SECURITY.md` for software vulnerabilities.

## Development workflow

1. Create a short-lived branch from `main`.
2. Make one focused change and add or update tests.
3. Run `make reproduce`.
4. Run `make release-audit`.
5. Describe the construct assumption, expected impact, and evidence boundary in
   the pull request.

## Benchmark changes

ChildEsc v0.1 is immutable. Proposed scenario or label changes must target a new
candidate version and include:

- the original and proposed value;
- a source-informed or reviewer-supported rationale;
- whether the proposer inspected the router or existing failures;
- any effect on action, target, timing, or contract metrics; and
- retained disagreement rather than a fabricated consensus.

Router rules must not be tuned on a set and then evaluated on that same set as
if it were held out.

## Human validation

Protocol files are not invitations to recruit participants. Do not contact
practitioners or youth, collect responses, or upload study data through GitHub.
Human work requires the gates in `validation/ethics_gate.md`. Youth participation
requires the additional minors-specific and safeguarding approvals.

## Style

- Use Python 3.11 or newer and the standard library unless a dependency is
  justified explicitly.
- Keep generated artifacts deterministic.
- Prefer precise terms such as `synthetic`, `source-informed`, and
  `policy-exposed diagnostic` over unsupported validity claims.
