#!/usr/bin/env node

import { FileBlob, SpreadsheetFile } from "@oai/artifact-tool";

const source =
  "validation/practitioner_packet/reviewer_workbooks/ChildEsc_Practitioner_Review_R01.xlsx";
const output = "/private/tmp/ChildEsc_Practitioner_Review_R01_dry_run.xlsx";
const workbook = await SpreadsheetFile.importXlsx(await FileBlob.load(source));
const sheet = workbook.worksheets.getItem("Review Form");

sheet.getRange("C2:Y2").values = [[
  "Human support",
  "Unclear",
  "Permit",
  "Permit",
  "Not applicable",
  "Unclear",
  "Forbid",
  "Unclear",
  "Permit",
  "Yes",
  "Needed",
  "Needed",
  "Unclear",
  "Needed",
  "Not needed",
  "Needed",
  "Whether a non-implicated adult is available",
  "Possible",
  "Only with caveat",
  "High",
  3,
  "Training dry run only; not reviewer data.",
  null,
]];

const check = await workbook.inspect({
  kind: "table",
  range: "Review Form!A1:Y2",
  include: "values,formulas",
  tableMaxRows: 2,
  tableMaxCols: 25,
  maxChars: 12000,
});
if (!check.ndjson.includes("Training dry run only; not reviewer data.")) {
  throw new Error("dry-run response did not round-trip through the workbook");
}
const errors = await workbook.inspect({
  kind: "match",
  searchTerm: "#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A",
  options: { useRegex: true, maxResults: 100 },
  summary: "dry-run formula error scan",
});
if (errors.ndjson.includes('"matchCount":') && !errors.ndjson.includes('"matchCount":0')) {
  throw new Error("formula error found during packet dry run");
}

const exported = await SpreadsheetFile.exportXlsx(workbook);
await exported.save(output);
console.log(`dry run passed and wrote ${output}`);
