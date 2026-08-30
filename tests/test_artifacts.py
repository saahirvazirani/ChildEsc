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
        self.assertIn("53 tests for the frozen scientific and manuscript path", manuscript)
        self.assertIn("26 provider-path tests", manuscript)

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

    def test_latex_table_and_claims_match_cross_system_summary(self) -> None:
        result = json.loads(
            (ROOT / "results" / "llm_v1_2_summary.json").read_text(
                encoding="utf-8"
            )
        )
        manuscript = self.manuscript()
        labels = {
            "openrouter/anthropic/claude-sonnet-5-20260630": "Claude Sonnet 5",
            "openrouter/google/gemini-3.1-pro-preview": "Gemini 3.1 Pro Preview",
            "openrouter/openai/gpt-5.5": "GPT-5.5",
        }
        fields = (
            "action_accuracy",
            "exact_route_accuracy",
            "action_route_gap",
            "action_correct_target_failure_rate",
        )
        for system_key, label in labels.items():
            system = result["systems"][system_key]
            expected = " & ".join(
                [
                    label,
                    str(system["complete_trials"]),
                    *(
                        paper_number(float(system["metric_summary"][field]["mean"]))
                        for field in fields
                    ),
                    paper_number(float(system["route_instability_rate"])),
                ]
            )
            self.assertIn(expected, manuscript)
        self.assertIn("29.2--49.4-point action-route gaps", manuscript)
        self.assertIn("42.7--71.2\\%", manuscript)
        self.assertIn("one GPT trial failed at 79/80", manuscript)
        self.assertIn("pre-specified after a failed pilot", manuscript)

    def test_main_paper_formalizes_and_decomposes_route_failures(self) -> None:
        manuscript = self.main_content()

        self.assertIn("V_i", manuscript)
        self.assertIn("T_i\\subseteq P_i", manuscript)
        self.assertIn("Failure decomposition across complete trials", manuscript)
        self.assertIn("Claude Sonnet 5 & 164 & 70 & 70 & 0 & 0", manuscript)
        self.assertIn("Gemini 3.1 Pro Preview & 160 & 98 & 98 & 0 & 2", manuscript)
        self.assertIn("GPT-5.5 & 111 & 79 & 79 & 0 & 0", manuscript)

    def test_title_and_abstract_center_safe_recipient_gap(self) -> None:
        systems = json.loads(
            (ROOT / "results" / "metrics.json").read_text(encoding="utf-8")
        )["systems"]
        point = systems["childesc_rules"]["point"]
        manuscript = self.manuscript()

        self.assertIn("Who Gets Involved?", manuscript)
        self.assertIn("\\usepackage[dblblindworkshop]{neurips_2026}", manuscript)
        self.assertIn("\\workshoptitle{Child Safety in AI}", manuscript)
        self.assertNotIn("\\usepackage[final]", manuscript)
        self.assertIn("action-route gap", manuscript)
        self.assertIn(
            f"{point['action_correct_target_failures']}/"
            f"{point['action_correct_handoff_n']}",
            manuscript,
        )
        self.assertIn("11.3\\%", manuscript)
        self.assertIn("practitioner and youth validation have not occurred", manuscript)

    def test_abstract_has_workshop_argument_structure(self) -> None:
        manuscript = self.manuscript()
        docx_builder = (ROOT / "scripts" / "build_paper_docx.py").read_text(
            encoding="utf-8"
        )
        abstract = manuscript.split("\\begin{abstract}", 1)[1].split(
            "\\end{abstract}", 1
        )[0]

        self.assertIn("increasingly mediates emotional support", abstract)
        self.assertIn("Yet action-only evaluations", abstract)
        self.assertIn("We introduce ChildEsc", abstract)
        self.assertIn("80 LLM-assisted synthetic conversations", abstract)
        self.assertIn("80.0--83.1\\% mean action accuracy", abstract)
        self.assertIn("33.8--51.7\\% exact routing", abstract)
        self.assertIn("29.2--49.4-point gaps", abstract)
        self.assertIn("three prompted systems", abstract)
        self.assertIn("specification-conformance diagnostics", abstract)
        for phrase in (
            "increasingly mediates emotional support",
            "Yet action-only evaluations",
            "We introduce",
            "ChildEsc, a works-in-progress testbed",
            "mean action accuracy ranges from 80.0% to 83.1%",
            "exact routing ranges from 33.8% to 51.7%",
            "29.2- to 49.4-point",
            "three prompted systems",
            "specification-conformance",
        ):
            self.assertIn(phrase, docx_builder)

    def test_action_semantics_and_editorial_feedback_boundary_are_explicit(self) -> None:
        manuscript = self.manuscript()

        self.assertIn("intervention and routing obligation rather than complete response style", manuscript)
        self.assertIn("boundary-setting without human handoff", manuscript)
        self.assertIn("does not authorize autonomous contact", manuscript)
        self.assertIn("incomplete informal editorial read", manuscript)
        self.assertIn("but is not validation", manuscript)
        self.assertIn("dual interpretation", manuscript)
        self.assertIn("abstain or clarify", manuscript)
        self.assertIn("No practitioner or youth validation has occurred", manuscript)

    def test_main_content_ends_with_defensible_contribution_not_open_questions(self) -> None:
        main_content = self.main_content()
        manuscript = self.manuscript()

        self.assertNotIn("Questions for the workshop", main_content)
        self.assertIn("Conclusion", main_content)
        self.assertIn("recipient-constrained routing", main_content)
        self.assertIn("machine-checkable object", main_content)
        self.assertIn("abstain or clarify", main_content)
        self.assertIn("practitioner and youth", main_content)
        self.assertNotIn("\\input{checklist}", manuscript)
        self.assertIn("\\author{Anonymous Author(s)}", manuscript)
        self.assertNotIn("The author had inspected", manuscript)

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
        self.assertIn("KORA", manuscript)
        self.assertIn("kora2026benchmark", bibliography)

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

    def test_supplement_points_to_frozen_cross_system_evidence(self) -> None:
        supplement = (ROOT / "paper" / "SUPPLEMENT_README.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("results/llm_v1_2_summary.json", supplement)
        self.assertIn("results/llm_v1_2_target_failures.csv", supplement)
        self.assertIn("results/llm_v1_2_bootstrap_intervals.csv", supplement)
        self.assertTrue((ROOT / "results" / "llm_v1_2_bootstrap_intervals.csv").is_file())
        self.assertIn("all eight scored trials", supplement.lower())
        self.assertIn("incomplete 79/80 GPT trial", supplement)
        self.assertIn("tasks/llm_evaluation_protocol_v1_2.md", supplement)
        self.assertIn(
            "raw provider responses and caches are excluded", self.manuscript().lower()
        )
        self.assertIn("cannot replay provider calls", supplement.lower())

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
