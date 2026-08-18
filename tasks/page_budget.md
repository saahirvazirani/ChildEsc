# ChildEsc Submission Page Ledger

## Authoritative rule

Verified on 2026-08-17 from the NeurIPS 2026 Child Safety in AI workshop call:

- Up to four content pages, excluding references.
- NeurIPS 2026 template with the `dblblindworkshop` option.
- Anonymous submission.
- Optional unlimited-length appendix.

Source: https://childsafety-ai.github.io/

## Final compiled boundary (2026-08-18)

- Content pages: 1-4.
- References begin: page 5.
- Appendix begins: page 5 after the references.
- Checklist begins: page 8.
- Total compiled pages: 14.

The current paper is compliant and uses the full four-page content allowance without changing the official template.

## Revision allocation

| Page | Purpose |
|---|---|
| 1 | Abstract, problem, closest gap, contributions |
| 2 | Scope, construction, action/target specification, metrics |
| 3 | Prototype contract, diagnostic results, uncertainty |
| 4 | Source-traceable contract audit, supported use, validity, impact, conclusion |

Detailed error tables, ablations, robustness checks, protocols, and extended limitations belong in the unlimited appendix.

The fourth page is not filled with more policy-exposed score detail. Its acceptance purpose is to show: (1) the exact construct and supported claim, (2) the distinction from CAREBench, KIDBench, and the August 2026 CARE-Bench triage benchmark, (3) source-informed relational contract results, (4) validation gates required before comparative or deployment claims, and (5) the bounded, non-operational status of the proposed delegated 988 follow-up extension.

## Verification rule

After every material manuscript change:

1. Compile `paper/main.tex` with the official template.
2. Confirm `References` starts no later than page 5.
3. Render and inspect every page.
4. Reject any layout change that compresses the paper by altering template margins, type size, or spacing.
