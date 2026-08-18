# Prospective Practitioner Analysis Plan

Status: pre-specified protocol; no data collected

## Units

- Item: one synthetic conversation.
- Rating: one reviewer's complete rubric response for one item.
- Family: four severity variants sharing a scenario context.

## Primary summaries

1. Action-label distribution per item and overall.
2. Ordinal distance between v0.1 action and each practitioner action.
3. Pairwise Jaccard similarity for permitted-target sets.
4. Per-target selection and prohibition prevalence.
5. Proportion of ratings marking missing context, coercion risk, or inadequate labelability.

## Agreement

- Report raw exact action agreement and adjacent-action agreement.
- If design and sample support it, report an ordinal agreement coefficient with a bootstrap interval grouped by family.
- Do not summarize set-valued targets with exact match alone; include pairwise Jaccard and per-target agreement.
- Report contested items and role-specific distributions descriptively.

## Missingness

- A skipped item is missing, not a negative response.
- Report skip rate by domain and severity.
- Do not impute action or target labels.
- Retain `cannot_determine` as a substantive response.

## Revision flags

Flag, but do not automatically relabel, an item when any condition holds:

- Fewer than half of reviewers select the v0.1 action.
- At least one-third select an action two or more levels away.
- At least one-third prohibit a v0.1 permitted target.
- At least half mark important context missing.
- At least one-third mark the item not responsibly labelable.

Qualified adjudicators review every flag. Publish pre-review labels, distributions, adjudication rationale, and the resulting version change.

## Prohibited analyses

- No claim of clinical accuracy against practitioner plurality.
- No significance fishing across small reviewer-role groups.
- No tuning and evaluation on the same practitioner-reviewed items without explicit in-sample labeling.
