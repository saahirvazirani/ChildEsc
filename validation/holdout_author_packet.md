# Prospective Independent Holdout Author Packet

Status: no independent holdout has been authored

## Independence requirement

The holdout author must not inspect:

- `src/childesc/router.py`
- Existing item-level predictions or error analysis.
- The lexical robustness results.
- The exact phrases in `benchmark/scenario_families.json` beyond the abstract schema needed to avoid duplication.

The current project author and coding agents are not eligible to claim an independently authored holdout because they have inspected all of those materials.

## Assignment

Create 8-12 new scenario families spanning at least six ChildEsc domains. Each family should contain four naturally distinct severity variants and use the frozen action/target definitions. Write new wording from the construct definitions rather than paraphrasing existing items.

## Safety constraints

- Use fictional, non-procedural text only.
- Do not use real child conversations, hotline transcripts, clinical records, or explicit abuse material.
- Do not include self-harm methods, grooming tactics, or evasion instructions.
- Mark any scenario that requires specialist safety review before inclusion.

## Materials the author may receive

- Scope and action definitions from `tasks/spec.md`.
- Target taxonomy and schema fields.
- Content-safety and provenance requirements.
- A blank family JSON template with no existing scenario text.

## Sealing procedure

1. Freeze the analysis plan before receiving holdout text.
2. Record authorship, date, and source-file hash.
3. Run schema and prohibited-content checks without changing wording for router compatibility.
4. Evaluate the frozen router once.
5. Do not tune the router on holdout failures.
6. Report holdout results separately from v0.1 policy-exposed diagnostics.

## Current submission language

Because no eligible independent author has completed this process, the paper must not claim held-out performance. This packet documents the required next step only.
