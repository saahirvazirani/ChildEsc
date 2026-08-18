import json
import tempfile
import unittest
from collections import Counter
from pathlib import Path

from childesc.generate import SEVERITY_ORDER, expand, generate


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "benchmark" / "scenario_families.json"


class GenerateTests(unittest.TestCase):
    def test_expands_to_balanced_unique_items(self) -> None:
        source = json.loads(SOURCE.read_text(encoding="utf-8"))
        items = expand(source)

        self.assertEqual(len(items), 80)
        self.assertEqual(len({item["id"] for item in items}), 80)
        self.assertEqual(
            Counter(item["severity"] for item in items),
            Counter({severity: 20 for severity in SEVERITY_ORDER}),
        )
        self.assertTrue(all(item["synthetic"] for item in items))

    def test_generation_is_deterministic(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            first = Path(directory) / "first.jsonl"
            second = Path(directory) / "second.jsonl"
            generate(SOURCE, first)
            generate(SOURCE, second)
            self.assertEqual(first.read_bytes(), second.read_bytes())

    def test_every_item_has_three_user_turns(self) -> None:
        source = json.loads(SOURCE.read_text(encoding="utf-8"))
        for item in expand(source):
            user_turns = [m for m in item["conversation"] if m["role"] == "user"]
            self.assertEqual(len(user_turns), 3, item["id"])

    def test_escalation_onset_matches_the_decisive_second_turn(self) -> None:
        source = json.loads(SOURCE.read_text(encoding="utf-8"))
        for item in expand(source):
            if item["gold_action"] in {"human_support", "urgent_handoff"}:
                self.assertEqual(item["gold_onset_user_turn"], 2, item["id"])
            else:
                self.assertIsNone(item["gold_onset_user_turn"], item["id"])

    def test_forbidden_targets_use_the_router_target_vocabulary(self) -> None:
        source = json.loads(SOURCE.read_text(encoding="utf-8"))
        target_vocabulary = {
            "safe_adult",
            "safe_adult_not_implicated",
            "school_support",
            "health_professional",
            "crisis_service",
            "emergency_service",
            "child_protection",
            "platform_report",
        }
        for item in expand(source):
            self.assertLessEqual(set(item["forbidden_targets"]), target_vocabulary)


if __name__ == "__main__":
    unittest.main()
