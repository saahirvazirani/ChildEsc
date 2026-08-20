"""Deterministic balanced assignments for prospective practitioner review."""

from __future__ import annotations

import hashlib
from collections import Counter
from typing import Iterable


SEVERITY_ORDER = ("low", "moderate", "high", "imminent")
REVIEWER_COUNT = 8
RATINGS_PER_ITEM = 3
ITEMS_PER_REVIEWER = 30
ASSIGNMENT_SEED = "childesc-practitioner-packet-v1"
BALANCE_SPREAD_LIMITS = {
    "domain": 1,
    "adult_implicated": 1,
    "age_band": 3,
}


def _stable_key(value: str) -> str:
    return hashlib.sha256(f"{ASSIGNMENT_SEED}:{value}".encode()).hexdigest()


def build_assignments(items: Iterable[dict]) -> list[list[dict]]:
    """Assign all 80 items to eight balanced, blinded reviewer packets."""
    item_list = list(items)
    if len(item_list) != 80:
        raise ValueError("the v1 practitioner packet requires exactly 80 items")
    if len({item["id"] for item in item_list}) != len(item_list):
        raise ValueError("item IDs must be unique")

    by_severity = {
        severity: sorted(
            (item for item in item_list if item["severity"] == severity),
            key=lambda item: (item["domain"], item["family_id"], item["id"]),
        )
        for severity in SEVERITY_ORDER
    }
    if any(len(group) != 20 for group in by_severity.values()):
        raise ValueError("the v1 packet expects 20 items at each severity")

    packets: list[list[dict]] = [[] for _ in range(REVIEWER_COUNT)]
    offsets = (0, 2, 5)
    severity_starts = (0, 2, 4, 6)
    for severity_index, severity in enumerate(SEVERITY_ORDER):
        for item_index, item in enumerate(by_severity[severity]):
            for offset in offsets:
                reviewer = (
                    item_index + severity_starts[severity_index] + offset
                ) % REVIEWER_COUNT
                packets[reviewer].append(item)

    for reviewer_index, packet in enumerate(packets):
        packet.sort(key=lambda item: _stable_key(f"{reviewer_index}:{item['id']}"))

    _validate_assignments(packets, item_list)
    return packets


def _validate_assignments(packets: list[list[dict]], items: list[dict]) -> None:
    if len(packets) != REVIEWER_COUNT:
        raise ValueError("expected eight reviewer packets")
    if any(len(packet) != ITEMS_PER_REVIEWER for packet in packets):
        raise ValueError("each reviewer packet must contain 30 items")

    ratings = Counter(item["id"] for packet in packets for item in packet)
    if set(ratings) != {item["id"] for item in items}:
        raise ValueError("packet assignment does not cover every source item")
    if set(ratings.values()) != {RATINGS_PER_ITEM}:
        raise ValueError("every source item must receive exactly three ratings")

    all_domains = {item["domain"] for item in items}
    for packet in packets:
        severity_counts = Counter(item["severity"] for item in packet)
        if set(severity_counts) != set(SEVERITY_ORDER):
            raise ValueError("every packet must contain every severity")
        if any(count not in {7, 8} for count in severity_counts.values()):
            raise ValueError("each severity must appear seven or eight times")
        if {item["domain"] for item in packet} != all_domains:
            raise ValueError("every packet must contain every domain")

    for field, spread_limit in BALANCE_SPREAD_LIMITS.items():
        categories = {item[field] for item in items}
        for category in categories:
            counts = [
                sum(item[field] == category for item in packet) for packet in packets
            ]
            if max(counts) - min(counts) > spread_limit:
                raise ValueError(
                    f"{field}={category!r} exceeds the packet balance spread "
                    f"limit of {spread_limit}"
                )


def public_packet_rows(packet: list[dict], reviewer_number: int) -> list[dict]:
    """Return blinded reviewer rows without source IDs, labels, or model output."""
    rows = []
    for index, item in enumerate(packet, start=1):
        turns = [
            f"{message['role'].title()}: {message['content']}"
            for message in item["conversation"]
        ]
        rows.append(
            {
                "packet_item_id": f"R{reviewer_number:02d}-{index:03d}",
                "conversation": "\n".join(turns),
            }
        )
    return rows
