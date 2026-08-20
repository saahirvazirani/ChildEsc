# Validation Status

Every file in this directory is prospective unless it explicitly records a
completed, authorized activity. As of 2026-08-18, no practitioner or youth
recruitment, response collection, validation statistic, or participant quotation
exists for ChildEsc.

## Current state

| Evidence layer | Status | Supported interpretation |
|---|---|---|
| Structural and deterministic tests | Complete | The artifact satisfies its implemented schema and reproducibility checks. |
| Relational contract audit | Complete, developer-authored | The frozen router passed 36/39 assertions; this is mechanistic conformance, not external validity. |
| Independent holdout | Not completed | No generalization claim is supported. |
| Practitioner construct review | Protocol prepared; not started | No expert agreement or clinical-validity claim is supported. |
| Youth-participatory review | Protocol prepared; not started | `Youth-informed` and `youth-validated` are not supported. |
| Ecological, cross-cultural, clinical, or deployment validation | Not completed | No real-world safety or effectiveness claim is supported. |

## Required sequence

1. Obtain and record a qualified institutional determination.
2. Freeze practitioner materials and the analysis plan.
3. Conduct blinded practitioner construct review, if authorized.
4. Create a versioned candidate rather than overwriting v0.1.
5. Obtain explicit minors-specific approval and safeguarding sign-off.
6. Conduct youth advisory review without eliciting personal disclosures.
7. Publish only de-identified aggregate findings with disagreements retained.

Protocol preparation does not satisfy any of these evidence gates. See
`ethics_gate.md` for the controlling status and claim vocabulary.

The prospective distribution materials are under `practitioner_packet/`.
The base design contains eight blinded 30-item workbooks and gives each of the
80 synthetic items exactly three independent ratings. These artifacts must not
be distributed before the first gate is satisfied.
