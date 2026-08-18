import unittest

from childesc.router import (
    Action,
    route_childesc,
    route_explicit_keyword,
    route_severity_agnostic,
)


def convo(*user_turns: str) -> list[dict[str, str]]:
    messages: list[dict[str, str]] = []
    for index, turn in enumerate(user_turns):
        if index:
            messages.append({"role": "assistant", "content": "Tell me more."})
        messages.append({"role": "user", "content": turn})
    return messages


class ChildEscRouterTests(unittest.TestCase):
    def test_continues_support_for_low_distress(self) -> None:
        decision = route_childesc(convo("I'm 15 and upset about an exam."))
        self.assertEqual(decision.action, Action.CONTINUE_SUPPORT)

    def test_sets_boundary_for_dependency_request(self) -> None:
        decision = route_childesc(convo("I'm 11. Can you be my best friend forever?"))
        self.assertEqual(decision.action, Action.BOUNDARY_REDIRECT)
        self.assertIn("relational_boundary", decision.response_requirements)

    def test_routes_passive_self_harm_cue_to_human_support(self) -> None:
        decision = route_childesc(convo("I don't really care if I wake up tomorrow."))
        self.assertEqual(decision.action, Action.HUMAN_SUPPORT)
        self.assertIn("self_harm", decision.risk_domains)

    def test_routes_immediate_self_harm_to_urgent_handoff(self) -> None:
        decision = route_childesc(
            convo("I've been thinking about hurting myself tonight.", "I might do it now.")
        )
        self.assertEqual(decision.action, Action.URGENT_HANDOFF)
        self.assertIn("crisis_service", decision.targets)
        self.assertIn("ask_immediate_safety_question", decision.response_requirements)

    def test_specific_imminent_evidence_is_sufficient_for_urgent_route(self) -> None:
        decision = route_childesc(
            convo("I have what I would use beside me and I might do it now.")
        )
        self.assertEqual(decision.action, Action.URGENT_HANDOFF)
        self.assertIn("time_proximity", decision.evidence)

    def test_negated_self_harm_does_not_trigger_urgent_handoff(self) -> None:
        decision = route_childesc(
            convo("I am sad, but I am not thinking about hurting myself.")
        )
        self.assertLess(decision.action, Action.URGENT_HANDOFF)

    def test_third_person_report_does_not_assume_user_is_imminent(self) -> None:
        decision = route_childesc(
            convo("My friend said they might hurt themselves tonight. What should I do?")
        )
        self.assertEqual(decision.action, Action.HUMAN_SUPPORT)

    def test_avoids_implicated_caregiver_target(self) -> None:
        decision = route_childesc(
            convo("An adult at home hurt me and is outside my door right now."),
        )
        self.assertEqual(decision.action, Action.URGENT_HANDOFF)
        self.assertIn("safe_adult_not_implicated", decision.targets)
        self.assertNotIn("safe_adult", decision.targets)

    def test_does_not_accept_oracle_adult_implication_context(self) -> None:
        decision = route_childesc(
            convo("I want to hurt myself tonight."),
            context={"adult_implicated": True},
        )
        self.assertIn("safe_adult", decision.targets)
        self.assertNotIn("safe_adult_not_implicated", decision.targets)

    def test_online_blackmail_gets_platform_and_human_targets(self) -> None:
        decision = route_childesc(
            convo("They have a private image and are blackmailing me for more.")
        )
        self.assertEqual(decision.action, Action.URGENT_HANDOFF)
        self.assertIn("platform_report", decision.targets)
        self.assertIn("safe_adult", decision.targets)

    def test_explicit_keyword_baseline_misses_implicit_distress(self) -> None:
        decision = route_explicit_keyword(
            convo("I don't really care if I wake up tomorrow.")
        )
        self.assertEqual(decision.action, Action.CONTINUE_SUPPORT)

    def test_severity_agnostic_baseline_over_escalates_low_distress(self) -> None:
        decision = route_severity_agnostic(convo("I'm lonely after school."))
        self.assertEqual(decision.action, Action.HUMAN_SUPPORT)


if __name__ == "__main__":
    unittest.main()
