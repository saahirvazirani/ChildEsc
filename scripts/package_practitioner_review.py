#!/usr/bin/env python3
"""Audit and package prospective practitioner-review deliverables."""

from __future__ import annotations

import csv
import json
import zipfile
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKET_ROOT = ROOT / "validation" / "practitioner_packet"
GUIDE = PACKET_ROOT / "ChildEsc_Practitioner_Review_Guide.docx"
WORKBOOKS = PACKET_ROOT / "reviewer_workbooks"
BUNDLES = PACKET_ROOT / "reviewer_bundles"
ADMIN = PACKET_ROOT / "admin"
ADMIN_BUNDLE = PACKET_ROOT / "ChildEsc_Practitioner_Review_Admin_Bundle.zip"


def audit_manifest() -> None:
    manifest = json.loads((ADMIN / "assignment_manifest.json").read_text())
    if manifest["status"] != "prospective_only_not_authorized":
        raise ValueError("manifest must remain prospective and unauthorized")
    if len(manifest["packets"]) != 8:
        raise ValueError("expected eight reviewer packets")
    if any(len(packet["items"]) != 30 for packet in manifest["packets"]):
        raise ValueError("each reviewer packet must contain 30 items")
    if manifest.get("balance_spread_limits") != {
        "domain": 1,
        "adult_implicated": 1,
        "age_band": 3,
    }:
        raise ValueError("manifest balance limits do not match the frozen design")

    assignment_map = ADMIN / "administrator_assignment_map.csv"
    if b"\r\n" in assignment_map.read_bytes():
        raise ValueError("administrator map must use LF line endings")
    with assignment_map.open(newline="") as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) != 240:
        raise ValueError("administrator map must contain 240 assignments")
    source_counts = Counter(row["source_item_id"] for row in rows)
    if len(source_counts) != 80 or set(source_counts.values()) != {3}:
        raise ValueError("each source item must appear exactly three times")
    reviewer_counts = Counter(row["reviewer_packet"] for row in rows)
    if len(reviewer_counts) != 8 or set(reviewer_counts.values()) != {30}:
        raise ValueError("each reviewer must receive exactly 30 assignments")

    for field, spread_limit in (("domain", 1), ("adult_implicated", 1), ("age_band", 3)):
        categories = {row[field] for row in rows}
        for category in categories:
            counts = [
                sum(
                    row[field] == category and row["reviewer_packet"] == reviewer
                    for row in rows
                )
                for reviewer in sorted(reviewer_counts)
            ]
            if max(counts) - min(counts) > spread_limit:
                raise ValueError(f"{field}={category!r} is not balanced across packets")


def audit_workbook(path: Path, source_ids: set[str]) -> None:
    if not path.exists():
        raise FileNotFoundError(path)
    with zipfile.ZipFile(path) as archive:
        names = set(archive.namelist())
        worksheet_names = {
            name for name in names if name.startswith("xl/worksheets/sheet") and name.endswith(".xml")
        }
        if len(worksheet_names) != 3:
            raise ValueError(f"{path.name} must contain exactly three worksheets")
        xml_text = "\n".join(
            archive.read(name).decode("utf-8", errors="ignore")
            for name in names
            if name.endswith(".xml")
        )
    lowered = xml_text.lower()
    for phrase in (
        "gold_action",
        "gold_onset",
        "permitted_targets",
        "forbidden_targets",
        "adult_implicated",
        "family_id",
        "router output",
    ):
        if phrase in lowered:
            raise ValueError(f"{phrase!r} leaked into {path.name}")
    if any(source_id in xml_text for source_id in source_ids):
        raise ValueError(f"source item ID leaked into {path.name}")
    if "dataValidations" not in xml_text:
        raise ValueError(f"dropdown validation missing from {path.name}")


def build_bundles() -> None:
    with (ADMIN / "administrator_assignment_map.csv").open(newline="") as handle:
        source_ids = {row["source_item_id"] for row in csv.DictReader(handle)}
    BUNDLES.mkdir(parents=True, exist_ok=True)
    reviewer_bundle_paths = []
    for reviewer_number in range(1, 9):
        reviewer = f"R{reviewer_number:02d}"
        workbook = WORKBOOKS / f"ChildEsc_Practitioner_Review_{reviewer}.xlsx"
        audit_workbook(workbook, source_ids)
        bundle = BUNDLES / f"ChildEsc_Reviewer_Packet_{reviewer}.zip"
        with zipfile.ZipFile(bundle, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            archive.write(GUIDE, GUIDE.name)
            archive.write(workbook, workbook.name)
        with zipfile.ZipFile(bundle) as archive:
            expected = {GUIDE.name, workbook.name}
            if set(archive.namelist()) != expected:
                raise ValueError(f"unexpected reviewer bundle contents for {reviewer}")
        reviewer_bundle_paths.append(bundle)

    with zipfile.ZipFile(ADMIN_BUNDLE, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.write(PACKET_ROOT / "README.md", "README.md")
        archive.write(GUIDE, GUIDE.name)
        archive.write(ADMIN / "assignment_manifest.json", "admin/assignment_manifest.json")
        archive.write(
            ADMIN / "administrator_assignment_map.csv",
            "admin/administrator_assignment_map.csv",
        )
        for bundle in reviewer_bundle_paths:
            archive.write(bundle, f"reviewer_bundles/{bundle.name}")


def main() -> None:
    audit_manifest()
    build_bundles()
    print(f"audited and wrote eight reviewer bundles to {BUNDLES}")
    print(f"wrote administrator bundle to {ADMIN_BUNDLE}")


if __name__ == "__main__":
    main()
