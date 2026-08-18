import csv
import json
import unittest
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def paper_number(value: float) -> str:
    rounded = Decimal(str(value)).quantize(Decimal("0.001"), rounding=ROUND_HALF_UP)
    return f"{rounded:.3f}".removeprefix("0")


class ArtifactSynchronizationTests(unittest.TestCase):
    def test_manuscript_reports_current_test_count(self) -> None:
        test_count = unittest.defaultTestLoader.discover(ROOT / "tests").countTestCases()
        manuscript = (ROOT / "paper" / "main.tex").read_text(encoding="utf-8")
        self.assertIn(f"{test_count} tests", manuscript)

    def test_latex_table_matches_versioned_metrics(self) -> None:
        systems = json.loads(
            (ROOT / "results" / "metrics.json").read_text(encoding="utf-8")
        )["systems"]
        manuscript = (ROOT / "paper" / "main.tex").read_text(encoding="utf-8")
        labels = {
            "explicit_keyword": "Keyword",
            "severity_agnostic": "Agnostic",
            "childesc_rules": "ChildEsc-Rules",
        }
        fields = (
            "macro_f1",
            "urgent_recall",
            "under_escalation_rate",
            "severe_under_escalation_rate",
            "counterfactual_sensitivity",
            "valid_target_rate",
            "exact_route_accuracy",
        )
        for system, label in labels.items():
            point = systems[system]["point"]
            expected = " & ".join(
                [label, *(paper_number(float(point[field])) for field in fields)]
            )
            self.assertIn(expected, manuscript)

    def test_manuscript_labels_results_as_policy_exposed_diagnostics(self) -> None:
        manuscript = (ROOT / "paper" / "main.tex").read_text(encoding="utf-8").lower()
        self.assertIn("policy-exposed", manuscript)
        self.assertIn("diagnostic checksum", manuscript)
        self.assertNotIn("mean escalation delay", manuscript)
        self.assertNotIn("reduces dangerous under-escalation", manuscript)

    def test_latex_analysis_table_matches_versioned_results(self) -> None:
        with (ROOT / "results" / "analysis_table.csv").open(
            encoding="utf-8", newline=""
        ) as stream:
            rows = {row["analysis"]: row for row in csv.DictReader(stream)}
        manuscript = (ROOT / "paper" / "main.tex").read_text(encoding="utf-8")
        labels = {
            "full": "Full conversation",
            "latest_user_turn_only": "Latest turn only",
            "adult_implication_disabled": "Adult inference off",
            "uppercase": "Uppercase",
            "extra_spaces": "Extra spaces",
            "expanded_contractions": "Expanded contractions",
        }
        fields = (
            "action_agreement",
            "urgent_recall",
            "under_escalation_rate",
            "valid_target_rate",
            "unsafe_target_rate",
            "exact_route_accuracy",
        )
        for analysis, label in labels.items():
            expected = " & ".join(
                [label, *(paper_number(float(rows[analysis][field])) for field in fields)]
            )
            self.assertIn(expected, manuscript)

    def test_manuscript_preserves_human_validation_boundary(self) -> None:
        manuscript = (ROOT / "paper" / "main.tex").read_text(encoding="utf-8").lower()
        self.assertIn("no practitioner or youth validation has occurred", manuscript)
        self.assertIn("7/12", manuscript)
        self.assertIn("45.0\\%", manuscript)

    def test_manuscript_reports_frozen_contract_audit(self) -> None:
        summary = json.loads(
            (ROOT / "results" / "contract_results.json").read_text(encoding="utf-8")
        )["summary"]
        manuscript = (ROOT / "paper" / "main.tex").read_text(encoding="utf-8")
        self.assertIn(
            f"{summary['passed_families']}/{summary['families']} families",
            manuscript,
        )
        self.assertIn(
            f"{summary['passed_assertions']}/{summary['assertions']} assertions",
            manuscript,
        )
        self.assertIn("not held-out", manuscript)

    def test_manuscript_distinguishes_recent_triage_benchmark(self) -> None:
        manuscript = (ROOT / "paper" / "main.tex").read_text(encoding="utf-8")
        bibliography = (ROOT / "paper" / "references.bib").read_text(encoding="utf-8")
        self.assertIn("CARE-Bench", manuscript)
        self.assertIn("hua2026caretriage", bibliography)

    def test_delegated_followup_extension_defaults_to_no_action(self) -> None:
        extension = json.loads(
            (ROOT / "validation" / "delegated_followup_extension.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(extension["status"], "prospective_only_not_implemented")
        self.assertFalse(extension["current_behavior"]["transmit_contact_data"])
        self.assertFalse(extension["current_behavior"]["initiate_outreach"])
        self.assertFalse(extension["eligibility"]["model_score_alone_can_trigger"])
        self.assertFalse(
            extension["consent_contract"]["bundled_terms_of_service_is_sufficient"]
        )

    def test_manuscript_bounds_delegated_followup_claims(self) -> None:
        manuscript = (ROOT / "paper" / "main.tex").read_text(encoding="utf-8")
        self.assertIn("not an established 988 policy", manuscript)
        self.assertIn("no cutoff is validated", manuscript)
        self.assertIn(
            "must not collect PII, schedule follow-up, transmit data, or initiate contact",
            manuscript,
        )
        self.assertIn("Imminent danger is excluded from a delayed queue", manuscript)


if __name__ == "__main__":
    unittest.main()
