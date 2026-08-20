import json
import unittest
from collections import Counter
from pathlib import Path

from childesc.practitioner_packet import (
    BALANCE_SPREAD_LIMITS,
    ITEMS_PER_REVIEWER,
    RATINGS_PER_ITEM,
    REVIEWER_COUNT,
    build_assignments,
    public_packet_rows,
)


ROOT = Path(__file__).resolve().parents[1]


class PractitionerPacketTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.items = [
            json.loads(line)
            for line in (ROOT / "benchmark" / "childesc_v0_1.jsonl")
            .read_text(encoding="utf-8")
            .splitlines()
            if line.strip()
        ]
        cls.packets = build_assignments(cls.items)

    def test_balanced_incomplete_block_covers_every_item_three_times(self) -> None:
        self.assertEqual(len(self.packets), REVIEWER_COUNT)
        self.assertTrue(
            all(len(packet) == ITEMS_PER_REVIEWER for packet in self.packets)
        )
        counts = Counter(item["id"] for packet in self.packets for item in packet)
        self.assertEqual(set(counts), {item["id"] for item in self.items})
        self.assertEqual(set(counts.values()), {RATINGS_PER_ITEM})

    def test_each_packet_balances_severity_and_covers_every_domain(self) -> None:
        domains = {item["domain"] for item in self.items}
        for packet in self.packets:
            severity = Counter(item["severity"] for item in packet)
            self.assertEqual(set(severity.values()), {7, 8})
            self.assertEqual({item["domain"] for item in packet}, domains)

    def test_cross_packet_balance_is_bounded(self) -> None:
        for field, spread_limit in BALANCE_SPREAD_LIMITS.items():
            categories = {item[field] for item in self.items}
            for category in categories:
                counts = [
                    sum(item[field] == category for item in packet)
                    for packet in self.packets
                ]
                self.assertLessEqual(max(counts) - min(counts), spread_limit)

    def test_public_rows_do_not_expose_reference_or_source_fields(self) -> None:
        prohibited = {
            "id",
            "source_id",
            "gold_action",
            "gold_onset_user_turn",
            "permitted_targets",
            "forbidden_targets",
            "adult_implicated",
            "severity",
            "domain",
            "family_id",
        }
        rows = public_packet_rows(self.packets[0], 1)
        self.assertEqual(set(rows[0]), {"packet_item_id", "conversation"})
        self.assertFalse(prohibited.intersection(rows[0]))

    def test_assignment_is_deterministic(self) -> None:
        repeated = build_assignments(reversed(self.items))
        self.assertEqual(
            [[item["id"] for item in packet] for packet in self.packets],
            [[item["id"] for item in packet] for packet in repeated],
        )


if __name__ == "__main__":
    unittest.main()
