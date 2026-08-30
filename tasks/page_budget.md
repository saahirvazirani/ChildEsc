# ChildEsc Submission Page Ledger

## Authoritative rule

Verified on 2026-08-17 from the NeurIPS 2026 Child Safety in AI workshop call:

- Up to four content pages, excluding references.
- NeurIPS 2026 template with the `dblblindworkshop` option.
- Anonymous submission.
- Optional unlimited-length appendix.

Source: https://childsafety-ai.github.io/

## Final acceptance build boundary (verified 2026-08-29)

- Content pages: 1-4.
- References begin: page 5.
- Appendix begins: page 5 after the references.
- NeurIPS checklist: not included.
- Total compiled pages: 8.

The acceptance-focused paper is compliant and uses the full four-page content
allowance without changing the official template. The completed prompted-router
diagnostic, its post-pilot validity boundary, and prospective validation outputs
occupy the fourth page. Unsupported automatic contact, disclosure, dispatch,
and timed-outreach proposals are excluded from all submission sources.

The final render was inspected at 160 DPI. The formal route-validity predicate,
three-system result table, and failure-decomposition table are legible; no
content spills onto page 5, and visible hyperlink boxes are suppressed without
changing template geometry.

## Revision allocation

| Page | Purpose |
|---|---|
| 1 | Abstract, problem, closest gap, contributions |
| 2 | Scope, construction, action/target specification, metrics |
| 3 | Prototype contract, diagnostic results, uncertainty |
| 4 | Source-traceable contract audit, supported use, validity, impact, conclusion |

Detailed error tables, ablations, robustness checks, protocols, and extended limitations belong in the unlimited appendix.

The fourth page is not filled with more policy-exposed score detail. Its acceptance purpose is to show: (1) the exact construct and supported claim, (2) the distinction from CAREBench, KIDBench, and the August 2026 CARE-Bench triage benchmark, (3) the review-form-informed need for explicit action semantics and an abstain/clarify state, (4) validation gates required before comparative or deployment claims, and (5) a bounded conclusion stating what recipient-constrained routing adds.

## Acceptance revision allocation, 2026-08-19

If at least one complete prompted-model audit is available, the main paper will
replace checksum breadth rather than add another table:

| Page | Acceptance job | Main content |
|---|---|---|
| 1 | Make the paper memorable | Safe-recipient question, closest-work gap, narrow contributions |
| 2 | Make the construct credible | Scope, matched families, actions, target constraints, provenance, primary metrics |
| 3 | Prove technical utility | Frozen model protocol, model-plus-checksum table, action-route gap, one target failure |
| 4 | Earn workshop fit | Validity boundary, practical use, evidence gates, and bounded conclusion |

Keyword and severity-agnostic rows, full intervals, stress tests, the complete
contract audit, and procedural validation detail move to the appendix. The
reported audit contains eight complete replayable trials across three prompted
systems; one additional GPT trial failed at 79/80 and remains unscored without
retry. The checksum remains an independent mechanistic diagnostic rather than
the headline result.

## Verification rule

After every material manuscript change:

1. Compile `paper/main.tex` with the official template.
2. Confirm `References` starts no later than page 5.
3. Render and inspect every page.
4. Reject any layout change that compresses the paper by altering template margins, type size, or spacing.
