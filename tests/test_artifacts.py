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
    def manuscript(self) -> str:
        return (ROOT / "paper" / "main.tex").read_text(encoding="utf-8")

    def main_content(self) -> str:
        return self.manuscript().split("\\clearpage\n\\bibliographystyle", 1)[0]

    def test_manuscript_reports_current_test_count(self) -> None:
        manuscript = (ROOT / "paper" / "main.tex").read_text(encoding="utf-8")
        self.assertIn("49 tests for the frozen scientific and manuscript path", manuscript)
        self.assertIn("25 provider-path tests", manuscript)

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
            "action_accuracy",
            "urgent_recall",
            "under_escalation_rate",
            "valid_target_rate",
            "action_route_gap",
            "exact_route_accuracy",
        )
        for system, label in labels.items():
            point = systems[system]["point"]
            expected = " & ".join(
                [label, *(paper_number(float(point[field])) for field in fields)]
            )
            self.assertIn(expected, manuscript)

    def test_latex_table_and_claims_match_prompted_router_summary(self) -> None:
        result = json.loads(
            (ROOT / "results" / "llm_v1_1_summary.json").read_text(
                encoding="utf-8"
            )
        )
        metrics = result["metrics"]
        manuscript = self.manuscript()
        fields = (
            "action_accuracy",
            "urgent_recall",
            "under_escalation_rate",
            "valid_target_rate",
            "action_route_gap",
            "exact_route_accuracy",
        )
        expected = " & ".join(
            [
                "Prompted router$^{\\dagger}$",
                *(paper_number(float(metrics[field]["mean"])) for field in fields),
            ]
        )
        self.assertIn(expected, manuscript)
        self.assertIn("29.2-point action-route gap", manuscript)
        self.assertIn("22.5\\% of items varied in full route", manuscript)
        self.assertIn("1.3\\% varied in action", manuscript)
        self.assertIn("pre-specified after a failed pilot", manuscript)

    def test_title_and_abstract_center_safe_recipient_gap(self) -> None:
        systems = json.loads(
            (ROOT / "results" / "metrics.json").read_text(encoding="utf-8")
        )["systems"]
        point = systems["childesc_rules"]["point"]
        manuscript = self.manuscript()

        self.assertIn("Who Is Safe to Involve?", manuscript)
        self.assertIn("action-route gap", manuscript)
        self.assertIn(
            f"{point['action_correct_target_failures']}/"
            f"{point['action_correct_handoff_n']}",
            manuscript,
        )
        self.assertIn("11.3\\%", manuscript)
        self.assertIn("practitioner and youth validation have not occurred", manuscript)

    def test_main_content_asks_four_actionable_workshop_questions(self) -> None:
        main_content = self.main_content()
        self.assertIn("Questions for the workshop", main_content)
        self.assertIn("clarify", main_content)
        self.assertIn("practitioner", main_content)
        self.assertIn("universal", main_content)
        self.assertIn("jurisdiction-specific", main_content)
        self.assertIn("becomes operational", main_content)

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

    def test_submission_sources_exclude_delegated_followup_and_988(self) -> None:
        submission_sources = (
            ROOT / "paper" / "main.tex",
            ROOT / "paper" / "references.bib",
            ROOT / "scripts" / "build_paper_docx.py",
            ROOT / "paper" / "SUPPLEMENT_README.md",
        )
        prohibited = ("988", "delegated follow", "1--24", "1-24 hour")
        for path in submission_sources:
            content = path.read_text(encoding="utf-8").lower()
            for phrase in prohibited:
                self.assertNotIn(phrase, content, f"{phrase!r} found in {path}")
        manuscript = (ROOT / "paper" / "main.tex").read_text(encoding="utf-8").lower()
        for phrase in ("ground truth", "ground-truth", "clinically valid", "model safety"):
            self.assertNotIn(phrase, manuscript)

    def test_manuscript_explains_two_layer_safeguard_scope(self) -> None:
        manuscript = (ROOT / "paper" / "main.tex").read_text(encoding="utf-8")
        self.assertIn("Layer 1", manuscript)
        self.assertIn("action and recipient", manuscript)
        self.assertIn("Layer 2", manuscript)
        self.assertIn("supportive language", manuscript)
        self.assertIn("separate rubric", manuscript)
        self.assertIn("human validation", manuscript)


if __name__ == "__main__":
    unittest.main()
