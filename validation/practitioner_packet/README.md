# ChildEsc Practitioner Review Packet

Status: prospective protocol material; distribution and response collection are
not authorized in this workspace.

## Contents

- `ChildEsc_Practitioner_Review_Guide.docx`: administrator and reviewer guide.
- `reviewer_workbooks/`: eight blinded workbooks, one per reviewer packet.
- `reviewer_bundles/`: eight reviewer-ready ZIPs containing the guide and one workbook each.
- `admin/assignment_manifest.json`: reviewer-facing rows and frozen design metadata.
- `admin/administrator_assignment_map.csv`: administrator-only source-item map.
- `qa/`: local render and inspection outputs; not for distribution.

## Frozen base design

- Eight reviewer packets.
- Thirty items per reviewer.
- All 80 synthetic source items.
- Exactly three independent ratings per source item.
- Every packet contains all eight domains and 7-8 items at each severity.
- Across packets, domain and implicated-adult category counts vary by at most
  one item, while age-band category counts vary by at most three items.
- Reference actions, target labels, router outputs, and source item IDs are
  absent from reviewer workbooks.

The assignment seed is `childesc-practitioner-packet-v1`. If an approved study
uses 9-12 reviewers, create and freeze a new assignment manifest before any
workbook is distributed.

## Optional all-80 workbook

Run `node scripts/build_practitioner_all_80_workbook.mjs` to create one blinded
workbook containing each of the 80 scenarios exactly once. It is written to
`outputs/childesc-practitioner-all-80/` and uses stable shuffle seed
`childesc-practitioner-all-80-v1`. This convenience artifact does not replace
the frozen eight-reviewer assignment or change the pre-specified analysis plan.

## Build and verify

1. Run `python scripts/build_practitioner_packet.py` with the bundled document
   runtime to create the guide, manifest, and administrator map.
2. Run `node scripts/build_practitioner_workbooks.mjs` with
   `@oai/artifact-tool` available to create the reviewer workbooks.
3. Run `make packet-test`.
4. Visually inspect the guide and every workbook before distribution.
5. Run `python scripts/package_practitioner_review.py` to audit and package the
   reviewer and administrator bundles.

## Distribution boundary

After institutional authorization, give each reviewer:

- the guide; and
- exactly one workbook matching their reviewer code.

The generated ZIP in `reviewer_bundles/` already contains that pair.

Never distribute the `admin/` directory. Do not collect names, contact details,
or identifiable real-case information in reviewer workbooks. Returned responses
belong only in the approved private data location, never in GitHub.
