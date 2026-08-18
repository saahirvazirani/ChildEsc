import json
import csv
import tempfile
import unittest
from pathlib import Path

from childesc.analysis import (
    action_error_category,
    apply_transformation,
    latest_user_turn_only,
    redact_adult_implication,
    run,
    target_error_category,
)
from childesc.router import ADULT_IMPLICATED


ROOT = Path(__file__).resolve().parents[1]


class AnalysisTests(unittest.TestCase):
    def test_action_error_categories_distinguish_severe_misses(self) -> None:
        self.assertEqual(action_error_category("human_support", "human_support"), "correct")
        self.assertEqual(
            action_error_category("urgent_handoff", "human_support"),
            "under_escalation",
        )
        self.assertEqual(
            action_error_category("urgent_handoff", "boundary_redirect"),
            "severe_under_escalation",
        )
        self.assertEqual(
            action_error_category("continue_support", "human_support"),
            "over_escalation",
        )

    def test_target_error_categories_are_strict_and_deterministic(self) -> None:
        self.assertEqual(target_error_category([], [], []), "not_required_valid")
        self.assertEqual(
            target_error_category([], [], ["safe_adult"]),
            "not_required_spurious",
        )
        self.assertEqual(
            target_error_category([], ["safe_adult"], ["safe_adult"]),
            "forbidden",
        )
        self.assertEqual(
            target_error_category(["safe_adult"], [], ["safe_adult"]),
            "valid",
        )
        self.assertEqual(target_error_category(["safe_adult"], [], []), "missing")
        self.assertEqual(
            target_error_category(
                ["safe_adult_not_implicated"],
                ["safe_adult"],
                ["safe_adult"],
            ),
            "forbidden",
        )
        self.assertEqual(
            target_error_category(
                ["safe_adult"],
                [],
                ["safe_adult", "crisis_service"],
            ),
            "extra_unpermitted",
        )

    def test_latest_turn_ablation_keeps_only_the_last_user_message(self) -> None:
        messages = [
            {"role": "user", "content": "context"},
            {"role": "assistant", "content": "question"},
            {"role": "user", "content": "decisive cue"},
            {"role": "assistant", "content": "acknowledgment"},
            {"role": "user", "content": "follow up"},
        ]
        self.assertEqual(
            latest_user_turn_only(messages),
            [{"role": "user", "content": "follow up"}],
        )

    def test_adult_implication_redaction_changes_only_user_text(self) -> None:
        messages = [
            {"role": "user", "content": "A parent checks every message I send."},
            {"role": "assistant", "content": "Does the parent check?"},
        ]
        redacted = redact_adult_implication(messages)
        self.assertNotIn("parent checks", redacted[0]["content"].lower())
        self.assertEqual(redacted[1], messages[1])

    def test_pre_specified_transformations_preserve_roles(self) -> None:
        messages = [
            {"role": "user", "content": "I'm upset and can't sleep."},
            {"role": "assistant", "content": "I am listening."},
        ]
        upper = apply_transformation(messages, "uppercase")
        spaced = apply_transformation(messages, "extra_spaces")
        expanded = apply_transformation(messages, "expanded_contractions")
        self.assertEqual(upper[0]["content"], "I'M UPSET AND CAN'T SLEEP.")
        self.assertEqual(upper[1], messages[1])
        self.assertIn("  ", spaced[0]["content"])
        self.assertIn("I am", expanded[0]["content"])
        self.assertIn("cannot", expanded[0]["content"])

    def test_unknown_transformation_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            apply_transformation([{"role": "user", "content": "hello"}], "unknown")

    def test_run_exports_complete_frozen_router_diagnostics(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            output = Path(temporary_directory)
            result = run(
                ROOT / "benchmark" / "childesc_v0_1.jsonl",
                ROOT / "results" / "predictions.csv",
                output,
            )

            self.assertEqual(result["error_summary"]["total_rows"], 240)
            self.assertEqual(
                sum(
                    result["error_summary"]["systems"]["childesc_rules"]["action"].values()
                ),
                80,
            )
            self.assertEqual(
                result["ablations"]["full"]["point"]["n"],
                80,
            )
            self.assertEqual(result["ablations"]["implicated_subset_n"], 12)
            self.assertEqual(
                result["ablations"]["adult_implication_disabled"]["action_agreement"],
                1.0,
            )
            self.assertNotIn("adult_implication_redacted", result["ablations"])
            self.assertEqual(
                ADULT_IMPLICATED,
                (
                    r"\badult at home\b",
                    r"\bparent checks\b",
                    r"\bcoach wants to meet\b",
                    r"\bcoach touched me\b",
                    r"\bcoach locked the door\b",
                ),
            )
            self.assertEqual(
                set(result["robustness"]),
                {"uppercase", "extra_spaces", "expanded_contractions"},
            )
            self.assertTrue(
                all(probe["passes_expected"] for probe in result["guard_probes"])
            )
            for filename in (
                "error_analysis.csv",
                "error_summary.json",
                "ablations.json",
                "robustness.json",
                "guard_probes.json",
                "analysis_table.csv",
            ):
                self.assertTrue((output / filename).is_file(), filename)

            with (output / "analysis_table.csv").open(
                encoding="utf-8", newline=""
            ) as stream:
                table_rows = list(csv.DictReader(stream))
            self.assertEqual(len(table_rows), 6)
            self.assertEqual(
                {row["analysis"] for row in table_rows},
                {
                    "full",
                    "latest_user_turn_only",
                    "adult_implication_disabled",
                    "uppercase",
                    "extra_spaces",
                    "expanded_contractions",
                },
            )

            full_metrics = result["ablations"]["full"]["point"]
            frozen_metrics = json.loads(
                (ROOT / "results" / "metrics.json").read_text(encoding="utf-8")
            )["systems"]["childesc_rules"]["point"]
            self.assertEqual(full_metrics, frozen_metrics)


if __name__ == "__main__":
    unittest.main()
