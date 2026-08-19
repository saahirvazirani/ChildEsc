import json
import tempfile
import unittest
from pathlib import Path

from childesc.llm_analysis import (
    paired_family_bootstrap_difference,
    run_analysis,
    summarize_trials,
)
from childesc.metrics import compute_metrics


def prediction(
    item_id: str,
    family_id: str,
    severity: str,
    gold_action: str,
    predicted_action: str,
    permitted_targets: list[str],
    predicted_targets: list[str],
    forbidden_targets: list[str] | None = None,
) -> dict[str, object]:
    return {
        "id": item_id,
        "family_id": family_id,
        "domain": "abuse_coercion",
        "severity": severity,
        "gold_action": gold_action,
        "predicted_action": predicted_action,
        "permitted_targets": permitted_targets,
        "predicted_targets": predicted_targets,
        "forbidden_targets": forbidden_targets or [],
        "status": "ok",
    }


class LLMAnalysisTests(unittest.TestCase):
    def setUp(self) -> None:
        self.trial_1 = [
            prediction(
                "a",
                "family-a",
                "moderate",
                "human_support",
                "human_support",
                ["safe_adult_not_implicated"],
                ["safe_adult_not_implicated"],
                ["safe_adult"],
            ),
            prediction(
                "b",
                "family-b",
                "high",
                "urgent_handoff",
                "urgent_handoff",
                ["crisis_service"],
                ["crisis_service"],
            ),
        ]
        self.trial_2 = [
            prediction(
                "a",
                "family-a",
                "moderate",
                "human_support",
                "human_support",
                ["safe_adult_not_implicated"],
                ["safe_adult"],
                ["safe_adult"],
            ),
            prediction(
                "b",
                "family-b",
                "high",
                "urgent_handoff",
                "human_support",
                ["crisis_service"],
                ["crisis_service"],
            ),
        ]

    def test_summary_reports_gap_failures_and_trial_instability(self) -> None:
        summary, failures = summarize_trials(
            {"trial-1": self.trial_1, "trial-2": self.trial_2}
        )

        self.assertEqual(summary["complete_trials"], 2)
        self.assertEqual(summary["action_instability_count"], 1)
        self.assertEqual(summary["action_instability_rate"], 0.5)
        self.assertEqual(summary["route_instability_count"], 2)
        self.assertEqual(summary["route_instability_rate"], 1.0)
        self.assertEqual(summary["metric_summary"]["action_route_gap"]["mean"], 0.25)
        self.assertEqual(summary["metric_summary"]["action_route_gap"]["low"], 0.0)
        self.assertEqual(summary["metric_summary"]["action_route_gap"]["high"], 0.5)
        self.assertEqual(len(failures), 1)
        self.assertEqual(failures[0]["trial_id"], "trial-2")
        self.assertEqual(failures[0]["id"], "a")

    def test_action_route_gap_exposes_action_correct_target_failures(self) -> None:
        rows = [
            prediction(
                "a",
                "family-a",
                "moderate",
                "human_support",
                "human_support",
                ["safe_adult_not_implicated"],
                ["safe_adult"],
                ["safe_adult"],
            ),
            prediction(
                "b",
                "family-b",
                "high",
                "urgent_handoff",
                "urgent_handoff",
                ["crisis_service"],
                ["crisis_service"],
            ),
            prediction(
                "c",
                "family-c",
                "low",
                "continue_support",
                "boundary_redirect",
                [],
                [],
            ),
        ]

        metrics = compute_metrics(rows)

        self.assertAlmostEqual(metrics["action_accuracy"], 2 / 3)
        self.assertAlmostEqual(metrics["exact_route_accuracy"], 1 / 3)
        self.assertAlmostEqual(metrics["action_route_gap"], 1 / 3)
        self.assertEqual(metrics["action_correct_handoff_n"], 2)
        self.assertEqual(metrics["action_correct_target_failures"], 1)
        self.assertEqual(metrics["action_correct_target_failure_rate"], 0.5)

    def test_paired_bootstrap_keeps_families_aligned(self) -> None:
        difference = paired_family_bootstrap_difference(
            self.trial_1,
            self.trial_2,
            "exact_route_accuracy",
            repetitions=200,
            seed=5,
        )

        self.assertEqual(difference["candidate_minus_reference"], -1.0)
        self.assertLessEqual(difference["ci95"]["low"], -1.0)
        self.assertGreaterEqual(difference["ci95"]["high"], -1.0)

    def test_run_analysis_writes_stable_audit_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            run_dirs = []
            for trial_id, rows in (
                ("trial-1", self.trial_1),
                ("trial-2", self.trial_2),
            ):
                run_dir = root / trial_id
                run_dir.mkdir()
                (run_dir / "routing_predictions.jsonl").write_text(
                    "".join(json.dumps(row, sort_keys=True) + "\n" for row in rows),
                    encoding="utf-8",
                )
                (run_dir / "routing_metrics.json").write_text(
                    json.dumps(
                        {
                            "complete": True,
                            "provider": "gemini",
                            "model": "test-model",
                            "trial_id": trial_id,
                            "prompt_sha256": "prompt-hash",
                            "schema_sha256": "schema-hash",
                            "data_sha256": "data-hash",
                        }
                    )
                    + "\n",
                    encoding="utf-8",
                )
                run_dirs.append(run_dir)

            output = root / "analysis"
            first = run_analysis(run_dirs, output)
            first_summary = (output / "summary.json").read_bytes()
            first_table = (output / "paper_table.csv").read_bytes()
            first_failures = (output / "action_correct_target_failures.csv").read_bytes()
            second = run_analysis(run_dirs, output)

            self.assertEqual(first, second)
            self.assertEqual(first_summary, (output / "summary.json").read_bytes())
            self.assertEqual(first_table, (output / "paper_table.csv").read_bytes())
            self.assertEqual(
                first_failures,
                (output / "action_correct_target_failures.csv").read_bytes(),
            )
            self.assertEqual(first["systems"]["gemini/test-model"]["complete_trials"], 2)


if __name__ == "__main__":
    unittest.main()
