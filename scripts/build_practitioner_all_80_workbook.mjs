#!/usr/bin/env node

import { createHash } from "node:crypto";
import fs from "node:fs/promises";
import path from "node:path";

import { buildWorkbook } from "./build_practitioner_workbooks.mjs";


const root = process.cwd();
const sourcePath = path.join(root, "benchmark", "childesc_v0_1.jsonl");
const outputDir = path.join(root, "outputs", "childesc-practitioner-all-80");
const outputPath = path.join(outputDir, "ChildEsc_Practitioner_Review_All_80.xlsx");
const qaDir = path.join(root, "validation", "practitioner_packet", "qa", "all_80");
const shuffleSeed = "childesc-practitioner-all-80-v1";

function stableKey(itemId) {
  return createHash("sha256").update(`${shuffleSeed}:${itemId}`).digest("hex");
}

function conversationText(item) {
  return item.conversation
    .map((message) => {
      const role = message.role.charAt(0).toUpperCase() + message.role.slice(1);
      return `${role}: ${message.content}`;
    })
    .join("\n");
}

const sourceText = await fs.readFile(sourcePath, "utf8");
const sourceItems = sourceText
  .split(/\r?\n/)
  .filter(Boolean)
  .map((line) => JSON.parse(line));

if (sourceItems.length !== 80) {
  throw new Error(`expected 80 source scenarios, found ${sourceItems.length}`);
}
if (new Set(sourceItems.map((item) => item.id)).size !== 80) {
  throw new Error("source scenario IDs must be unique");
}

const items = [...sourceItems]
  .sort((left, right) => stableKey(left.id).localeCompare(stableKey(right.id)))
  .map((item, index) => ({
    packet_item_id: `ALL-${String(index + 1).padStart(3, "0")}`,
    conversation: conversationText(item),
  }));

if (new Set(items.map((item) => item.conversation)).size !== 80) {
  throw new Error("the full-set workbook must contain 80 unique conversations");
}

const packet = { reviewer_packet: "ALL80", items };
const workbook = await buildWorkbook(packet, {
  outputPath,
  qaDir,
  qaPrefix: "ALL80",
});

const finalRows = await workbook.inspect({
  kind: "table",
  range: "Review Form!A77:Y81",
  include: "values,formulas",
  tableMaxRows: 5,
  tableMaxCols: 25,
  maxChars: 12000,
});
await fs.writeFile(path.join(qaDir, "ALL80_final_rows.ndjson"), finalRows.ndjson);

const errors = await workbook.inspect({
  kind: "match",
  searchTerm: "#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A",
  options: { useRegex: true, maxResults: 300 },
  summary: "all-80 workbook formula error scan",
});
if (
  errors.ndjson.includes('"matchCount":') &&
  !errors.ndjson.includes('"matchCount":0')
) {
  throw new Error("formula error found in the all-80 workbook");
}

console.log(`wrote one blinded 80-scenario workbook to ${outputPath}`);
