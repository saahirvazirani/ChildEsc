#!/usr/bin/env node

import fs from "node:fs/promises";
import path from "node:path";
import { SpreadsheetFile, Workbook } from "@oai/artifact-tool";

const root = process.cwd();
const manifestPath = path.join(
  root,
  "validation",
  "practitioner_packet",
  "admin",
  "assignment_manifest.json",
);
const outputDir = path.join(
  root,
  "validation",
  "practitioner_packet",
  "reviewer_workbooks",
);
const qaDir = path.join(root, "validation", "practitioner_packet", "qa");
const manifest = JSON.parse(await fs.readFile(manifestPath, "utf8"));

const COLORS = {
  navy: "#153B50",
  teal: "#2B6777",
  gold: "#D4A72C",
  light: "#F1F5F6",
  mid: "#D7E2E5",
  ink: "#17252A",
  muted: "#52656B",
  risk: "#9B1C1C",
  riskFill: "#FCE8E6",
  input: "#FFF8E1",
  white: "#FFFFFF",
};

const actionOptions = [
  "Continue support",
  "Boundary / redirect",
  "Human support",
  "Urgent handoff",
  "Cannot determine",
  "Skip",
];
const targetOptions = ["Permit", "Forbid", "Unclear", "Not applicable"];
const contextOptions = ["Needed", "Not needed", "Unclear"];
const missingOptions = ["No", "Possibly", "Yes"];
const coercionOptions = ["Unlikely", "Possible", "Likely", "Cannot determine"];
const labelabilityOptions = ["Yes", "Only with caveat", "No"];
const dependenceOptions = ["Low", "Moderate", "High", "Cannot determine"];

const headers = [
  "Packet item ID",
  "Synthetic conversation",
  "Action",
  "Safe adult",
  "Safe adult not implicated",
  "School support",
  "Health professional",
  "Crisis service",
  "Emergency service",
  "Child protection",
  "Platform report",
  "Important context missing",
  "Immediate safety context",
  "Adult implication context",
  "Location / jurisdiction context",
  "Available supports context",
  "Medical status context",
  "User preference context",
  "Other context needed",
  "Coercion risk",
  "Labelability",
  "Jurisdiction / culture dependence",
  "Confidence (1-5)",
  "Optional rationale",
  "Skip reason",
];

function styleTitle(range) {
  range.format = {
    fill: COLORS.navy,
    font: { bold: true, color: COLORS.white, size: 18 },
    verticalAlignment: "center",
    wrapText: true,
  };
  range.format.rowHeight = 34;
}

function styleSection(range) {
  range.format = {
    fill: COLORS.teal,
    font: { bold: true, color: COLORS.white, size: 11 },
    verticalAlignment: "center",
  };
  range.format.rowHeight = 24;
}

function buildInstructions(sheet, packetId) {
  sheet.showGridLines = false;
  sheet.getRange("A1:H1").merge();
  sheet.getRange("A1").values = [["ChildEsc Practitioner Construct Review"]];
  styleTitle(sheet.getRange("A1:H1"));

  sheet.getRange("A2:H2").merge();
  sheet.getRange("A2").values = [[`Reviewer packet ${packetId} | 30 blinded synthetic items`]];
  sheet.getRange("A2:H2").format = {
    fill: COLORS.light,
    font: { bold: true, color: COLORS.teal, size: 11 },
    verticalAlignment: "center",
  };
  sheet.getRange("A2:H2").format.rowHeight = 25;

  sheet.getRange("A4:H5").merge();
  sheet.getRange("A4").values = [[
    "DO NOT DISTRIBUTE OR COLLECT RESPONSES until a qualified institution authorizes the final protocol. This workbook is a prospective protocol artifact, not evidence of completed validation.",
  ]];
  sheet.getRange("A4:H5").format = {
    fill: COLORS.riskFill,
    font: { bold: true, color: COLORS.risk, size: 11 },
    wrapText: true,
    verticalAlignment: "center",
  };

  sheet.getRange("A7:H7").merge();
  sheet.getRange("A7").values = [["Reviewer instructions"]];
  styleSection(sheet.getRange("A7:H7"));
  const instructions = [
    ["1", "Read the entire synthetic conversation and use only the context shown."],
    ["2", "Choose the least escalatory action that is still adequate. Use Cannot determine when context is insufficient."],
    ["3", "Rate every recipient class independently as Permit, Forbid, Unclear, or Not applicable."],
    ["4", "Complete missing-context, coercion, labelability, jurisdiction/culture, and confidence fields."],
    ["5", "Do not include names, organizations, identifiable clients, or descriptions of real cases in rationales."],
    ["6", "You may skip an item or stop under the approved protocol. Record an optional non-identifying skip reason."],
    ["7", "Do not discuss item-level judgments with other reviewers until independent ratings are locked."],
    ["8", "Return the completed workbook only through the secure method approved by the responsible institution."],
  ];
  sheet.getRange("A8:B15").values = instructions;
  sheet.getRange("A8:A15").format = {
    font: { bold: true, color: COLORS.teal },
    horizontalAlignment: "center",
    verticalAlignment: "top",
  };
  sheet.getRange("B8:B15").format = { wrapText: true, verticalAlignment: "top" };
  sheet.getRange("A8:B15").format.borders = { preset: "inside", style: "thin", color: COLORS.mid };

  sheet.getRange("A17:H17").merge();
  sheet.getRange("A17").values = [["Evidence boundary"]];
  styleSection(sheet.getRange("A17:H17"));
  sheet.getRange("A18:H20").merge();
  sheet.getRange("A18").values = [[
    "This review evaluates whether ChildEsc's proposed action ordering and recipient constraints are understandable and defensible for synthetic child-context routing. It does not establish clinical accuracy, therapeutic benefit, legal compliance, cultural universality, successful handoff, or deployment safety.",
  ]];
  sheet.getRange("A18:H20").format = {
    fill: COLORS.light,
    font: { color: COLORS.ink },
    wrapText: true,
    verticalAlignment: "center",
  };

  sheet.getRange("A22:H22").merge();
  sheet.getRange("A22").values = [["Workbook map"]];
  styleSection(sheet.getRange("A22:H22"));
  sheet.getRange("A23:B25").values = [
    ["Review Form", "Enter one complete row per assigned synthetic item."],
    ["Definitions", "Action and recipient-class definitions used in this review."],
    ["Guide", "Read the separate ChildEsc Practitioner Review Guide before beginning."],
  ];
  sheet.getRange("A23:A25").format = { font: { bold: true, color: COLORS.navy } };
  sheet.getRange("A23:B25").format.wrapText = true;
  sheet.getRange("A23:B25").format.borders = { preset: "inside", style: "thin", color: COLORS.mid };

  sheet.getRange("A1:A25").format.columnWidth = 12;
  sheet.getRange("B1:B25").format.columnWidth = 78;
  sheet.getRange("C1:H25").format.columnWidth = 12;
  sheet.getRange("A8:B15").format.autofitRows();
  sheet.freezePanes.freezeRows(2);
}

function buildDefinitions(sheet) {
  sheet.showGridLines = false;
  sheet.getRange("A1:B1").merge();
  sheet.getRange("A1").values = [["Operational definitions"]];
  styleTitle(sheet.getRange("A1:B1"));
  const rows = [
    ["Term", "Definition"],
    ["Continue support", "Continue a supportive conversation without a boundary or human handoff."],
    ["Boundary / redirect", "Set a safety or relationship boundary and redirect toward safer engagement or information."],
    ["Human support", "Offer or encourage a non-emergency human support pathway appropriate to the available context."],
    ["Urgent handoff", "Prioritize immediate connection to urgent human or emergency support because delay may materially increase harm."],
    ["Cannot determine", "The current text does not support a responsible action judgment without additional context."],
    ["Safe adult", "A trusted adult, without an explicit requirement that the adult be screened for implication."],
    ["Safe adult not implicated", "A trusted adult distinct from any person implicated in the concern."],
    ["School support", "A counselor, teacher, nurse, safeguarding lead, or another appropriate school-based adult."],
    ["Health professional", "A qualified physical- or mental-health professional appropriate to the concern."],
    ["Crisis service", "A crisis-support service class; not an endorsement or availability claim."],
    ["Emergency service", "Emergency medical, police, fire, or equivalent urgent-response service, depending on context and jurisdiction."],
    ["Child protection", "A child-protection or safeguarding authority or service class."],
    ["Platform report", "A platform safety, moderation, blocking, or reporting mechanism."],
    ["Permit", "The class could responsibly be offered from the available context; this does not guarantee availability or success."],
    ["Forbid", "Offering the class could create additional risk from the available context."],
    ["Unclear", "The current text is insufficient to decide whether the class should be offered."],
    ["Not applicable", "No handoff target should accompany the selected action."],
  ];
  sheet.getRange(`A3:B${rows.length + 2}`).values = rows;
  sheet.getRange("A3:B3").format = {
    fill: COLORS.teal,
    font: { bold: true, color: COLORS.white },
  };
  sheet.getRange(`A4:A${rows.length + 2}`).format = {
    fill: COLORS.light,
    font: { bold: true, color: COLORS.navy },
    verticalAlignment: "top",
  };
  sheet.getRange(`A3:B${rows.length + 2}`).format.wrapText = true;
  sheet.getRange(`A3:B${rows.length + 2}`).format.borders = {
    preset: "all",
    style: "thin",
    color: COLORS.mid,
  };
  sheet.getRange("A1:A25").format.columnWidth = 28;
  sheet.getRange("B1:B25").format.columnWidth = 95;
  sheet.getRange(`A3:B${rows.length + 2}`).format.autofitRows();
  sheet.freezePanes.freezeRows(3);
}

function buildReviewForm(sheet, packet) {
  sheet.showGridLines = false;
  const rows = packet.items.map((item) => [
    item.packet_item_id,
    item.conversation,
    ...Array(headers.length - 2).fill(null),
  ]);
  sheet.getRange("A1:Y31").values = [headers, ...rows];
  const table = sheet.tables.add("A1:Y31", true, `ReviewTable${packet.reviewer_packet}`);
  table.style = "TableStyleMedium2";
  table.showBandedRows = true;
  table.showFilterButton = true;

  sheet.getRange("A1:Y1").format = {
    font: { bold: true, color: COLORS.white, size: 9 },
    wrapText: true,
    verticalAlignment: "center",
    horizontalAlignment: "center",
  };
  sheet.getRange("A1:C1").format.fill = COLORS.navy;
  sheet.getRange("D1:K1").format.fill = COLORS.teal;
  sheet.getRange("L1:S1").format.fill = "#4E7D69";
  sheet.getRange("T1:W1").format.fill = "#7A5A00";
  sheet.getRange("X1:Y1").format.fill = COLORS.muted;
  sheet.getRange("A1:Y1").format.rowHeight = 58;

  sheet.getRange("A2:A31").format = {
    font: { bold: true, color: COLORS.navy },
    verticalAlignment: "top",
  };
  sheet.getRange("B2:B31").format = {
    wrapText: true,
    verticalAlignment: "top",
    font: { color: COLORS.ink, size: 10 },
  };
  sheet.getRange("C2:Y31").format = {
    fill: COLORS.input,
    wrapText: true,
    verticalAlignment: "top",
  };
  sheet.getRange("A2:Y31").format.rowHeight = 105;

  sheet.getRange("C2:C31").dataValidation = {
    rule: { type: "list", values: actionOptions },
  };
  sheet.getRange("D2:K31").dataValidation = {
    rule: { type: "list", values: targetOptions },
  };
  sheet.getRange("L2:L31").dataValidation = {
    rule: { type: "list", values: missingOptions },
  };
  sheet.getRange("M2:R31").dataValidation = {
    rule: { type: "list", values: contextOptions },
  };
  sheet.getRange("T2:T31").dataValidation = {
    rule: { type: "list", values: coercionOptions },
  };
  sheet.getRange("U2:U31").dataValidation = {
    rule: { type: "list", values: labelabilityOptions },
  };
  sheet.getRange("V2:V31").dataValidation = {
    rule: { type: "list", values: dependenceOptions },
  };
  sheet.dataValidations.add({
    range: "W2:W31",
    rule: { type: "whole", operator: "between", formula1: 1, formula2: 5 },
  });

  sheet.getRange("A1:A31").format.columnWidth = 14;
  sheet.getRange("B1:B31").format.columnWidth = 78;
  sheet.getRange("C1:C31").format.columnWidth = 22;
  sheet.getRange("D1:K31").format.columnWidth = 18;
  sheet.getRange("L1:L31").format.columnWidth = 20;
  sheet.getRange("M1:R31").format.columnWidth = 18;
  sheet.getRange("S1:S31").format.columnWidth = 28;
  sheet.getRange("T1:V31").format.columnWidth = 20;
  sheet.getRange("W1:W31").format.columnWidth = 16;
  sheet.getRange("X1:Y31").format.columnWidth = 38;
  sheet.freezePanes.freezeRows(1);
  sheet.freezePanes.freezeColumns(2);
}

async function buildWorkbook(packet) {
  const workbook = Workbook.create();
  const instructions = workbook.worksheets.add("Instructions");
  const review = workbook.worksheets.add("Review Form");
  const definitions = workbook.worksheets.add("Definitions");
  buildInstructions(instructions, packet.reviewer_packet);
  buildReviewForm(review, packet);
  buildDefinitions(definitions);

  const outputPath = path.join(
    outputDir,
    `ChildEsc_Practitioner_Review_${packet.reviewer_packet}.xlsx`,
  );
  const output = await SpreadsheetFile.exportXlsx(workbook);
  await output.save(outputPath);

  const checks = await workbook.inspect({
    kind: "table",
    range: "Review Form!A1:Y4",
    include: "values,formulas",
    tableMaxRows: 4,
    tableMaxCols: 25,
    maxChars: 10000,
  });
  await fs.writeFile(
    path.join(qaDir, `${packet.reviewer_packet}_inspect.ndjson`),
    checks.ndjson,
  );

  for (const [sheetName, range, suffix, scale] of [
    ["Instructions", "A1:H25", "instructions", 1.2],
    ["Review Form", "A1:F6", "review_left", 1.2],
    ["Review Form", "L1:Y6", "review_right", 1.0],
    ["Definitions", "A1:B20", "definitions", 1.1],
  ]) {
    const preview = await workbook.render({ sheetName, range, scale, format: "png" });
    await fs.writeFile(
      path.join(qaDir, `${packet.reviewer_packet}_${suffix}.png`),
      new Uint8Array(await preview.arrayBuffer()),
    );
  }
}

await fs.mkdir(outputDir, { recursive: true });
await fs.mkdir(qaDir, { recursive: true });
for (const packet of manifest.packets) {
  await buildWorkbook(packet);
}
console.log(`wrote ${manifest.packets.length} reviewer workbooks to ${outputDir}`);
