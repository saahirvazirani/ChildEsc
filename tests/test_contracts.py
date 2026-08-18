import csv
import json
import tempfile
import unittest
from pathlib import Path

from childesc.contracts import (
    evaluate_case_assertions,
    evaluate_relation,
    run,
    validate_contract_suite,
)
from childesc.router import Action, RouteDecision


ROOT = Path(__file__).resolve().parents[1]


class ContractAuditTests(unittest.TestCase):
    def test_case_assertions_report_each_atomic_requirement(self) -> None:
        decision = RouteDecision(
            action=Action.URGENT_HANDOFF,
            targets=("crisis_service",),
            risk_domains=("self_harm",),
            response_requirements=("preserve_user_agency",),
        )
        expected = {
            "action_in": ["urgent_handoff"],
            "action_not_in": ["continue_support"],
            "targets_include": ["crisis_service"],
            "targets_exclude": ["safe_adult"],
            "domains_include": ["self_harm"],
            "requirements_include": ["preserve_user_agency"],
        }

        assertions = evaluate_case_assertions("probe", "variant", decision, expected)

        self.assertEqual(len(assertions), 6)
        self.assertTrue(all(assertion["passes"] for assertion in assertions))

    def test_relation_evaluation_uses_action_order(self) -> None:
        low = RouteDecision(action=Action.CONTINUE_SUPPORT)
        high = RouteDecision(action=Action.URGENT_HANDOFF)

        self.assertTrue(evaluate_relation("probe", low, high, "increase")["passes"])
        self.assertTrue(evaluate_relation("probe", high, low, "decrease")["passes"])
        self.assertFalse(evaluate_relation("probe", low, high, "same")["passes"])

    def test_suite_validation_rejects_unknown_source(self) -> None:
        suite = {
            "families": [
                {
                    "id": "one",
                    "factor": "factor",
                    "source_basis": ["missing"],
                    "base": {"messages": [{"role": "user", "content": "a"}], "expected": {}},
                    "variant": {"messages": [{"role": "user", "content": "b"}], "expected": {}},
                    "relation": {"action": "same"},
                }
            ]
        }
        with self.assertRaisesRegex(ValueError, "unknown source"):
            validate_contract_suite(suite, {"known"})

    def test_suite_validation_accepts_multi_turn_conversations(self) -> None:
        messages = [
            {"role": "user", "content": "I am having a hard night."},
            {"role": "assistant", "content": "What is happening right now?"},
            {"role": "user", "content": "I am safe, but I need support."},
        ]
        suite = {
            "families": [
                {
                    "id": "multi_turn",
                    "factor": "information state",
                    "source_basis": ["known"],
                    "base": {"messages": messages, "expected": {}},
                    "variant": {"messages": messages, "expected": {}},
                    "relation": {"action": "same"},
                }
            ]
        }

        validate_contract_suite(suite, {"known"})

    def test_repository_traceability_is_complete(self) -> None:
        source_register = json.loads(
            (ROOT / "benchmark" / "source_register.json").read_text(encoding="utf-8")
        )
        source_ids = {source["id"] for source in source_register["sources"]}
        contracts = json.loads(
            (ROOT / "benchmark" / "contract_probes.json").read_text(encoding="utf-8")
        )
        validate_contract_suite(contracts, source_ids)
        self.assertEqual(len(contracts["families"]), 9)

        family_source = json.loads(
            (ROOT / "benchmark" / "scenario_families.json").read_text(encoding="utf-8")
        )
        rationale = json.loads(
            (ROOT / "benchmark" / "family_rationale.json").read_text(encoding="utf-8")
        )
        self.assertEqual(
            {family["id"] for family in family_source["families"]},
            set(rationale["families"]),
        )
        for mapping in rationale["families"].values():
            self.assertTrue(set(mapping["rationale_sources"]).issubset(source_ids))

    def test_run_exports_complete_contract_audit(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            output = Path(temporary_directory)
            result = run(
                ROOT / "benchmark" / "contract_probes.json",
                ROOT / "benchmark" / "source_register.json",
                output,
            )

            self.assertEqual(result["summary"]["families"], 9)
            self.assertGreater(result["summary"]["assertions"], 9)
            for filename in (
                "contract_results.json",
                "contract_assertions.csv",
                "contract_table.csv",
            ):
                self.assertTrue((output / filename).is_file(), filename)

            with (output / "contract_table.csv").open(
                encoding="utf-8", newline=""
            ) as stream:
                rows = list(csv.DictReader(stream))
            self.assertEqual(len(rows), 9)


if __name__ == "__main__":
    unittest.main()
