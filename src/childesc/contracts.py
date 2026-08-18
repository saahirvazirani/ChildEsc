"""Evaluate post-freeze relational contracts against the diagnostic router."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any, Iterable

from childesc.router import RouteDecision, route_childesc


VALID_RELATIONS = {"same", "increase", "decrease", "nondecreasing"}
EXPECTED_FIELDS = {
    "action_in",
    "action_not_in",
    "targets_include",
    "targets_exclude",
    "domains_include",
    "requirements_include",
}


def _json_value(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def validate_contract_suite(suite: dict[str, Any], source_ids: set[str]) -> None:
    families = suite.get("families", [])
    if not families:
        raise ValueError("contract suite needs at least one family")
    ids = [family.get("id") for family in families]
    if len(ids) != len(set(ids)):
        raise ValueError("contract family IDs must be unique")

    for family in families:
        family_id = family.get("id", "<missing>")
        unknown_sources = set(family.get("source_basis", [])) - source_ids
        if unknown_sources:
            raise ValueError(
                f"{family_id}: unknown source {sorted(unknown_sources)}"
            )
        relation = family.get("relation", {}).get("action")
        if relation not in VALID_RELATIONS:
            raise ValueError(f"{family_id}: invalid action relation {relation!r}")
        for case_name in ("base", "variant"):
            case = family.get(case_name, {})
            messages = case.get("messages", [])
            roles = {message.get("role") for message in messages}
            if not messages or not roles.issubset({"user", "assistant"}) or "user" not in roles:
                raise ValueError(
                    f"{family_id}/{case_name}: user/assistant messages with at least "
                    "one user turn required"
                )
            unknown_fields = set(case.get("expected", {})) - EXPECTED_FIELDS
            if unknown_fields:
                raise ValueError(
                    f"{family_id}/{case_name}: unknown expected fields "
                    f"{sorted(unknown_fields)}"
                )


def _assertion(
    family_id: str,
    case_name: str,
    assertion: str,
    expected: object,
    observed: object,
    passes: bool,
) -> dict[str, object]:
    return {
        "family_id": family_id,
        "case": case_name,
        "assertion": assertion,
        "expected": _json_value(expected),
        "observed": _json_value(observed),
        "passes": passes,
    }


def evaluate_case_assertions(
    family_id: str,
    case_name: str,
    decision: RouteDecision,
    expected: dict[str, list[str]],
) -> list[dict[str, object]]:
    checks: list[dict[str, object]] = []
    action = decision.action.label
    targets = set(decision.targets)
    domains = set(decision.risk_domains)
    requirements = set(decision.response_requirements)

    if "action_in" in expected:
        allowed = expected["action_in"]
        checks.append(
            _assertion(
                family_id, case_name, "action_in", allowed, action, action in allowed
            )
        )
    if "action_not_in" in expected:
        forbidden = expected["action_not_in"]
        checks.append(
            _assertion(
                family_id,
                case_name,
                "action_not_in",
                forbidden,
                action,
                action not in forbidden,
            )
        )

    set_checks: Iterable[tuple[str, set[str], bool]] = (
        ("targets_include", targets, True),
        ("targets_exclude", targets, False),
        ("domains_include", domains, True),
        ("requirements_include", requirements, True),
    )
    for field, observed_set, should_include in set_checks:
        if field not in expected:
            continue
        expected_set = set(expected[field])
        passes = (
            expected_set.issubset(observed_set)
            if should_include
            else expected_set.isdisjoint(observed_set)
        )
        checks.append(
            _assertion(
                family_id,
                case_name,
                field,
                sorted(expected_set),
                sorted(observed_set),
                passes,
            )
        )
    return checks


def evaluate_relation(
    family_id: str,
    base: RouteDecision,
    variant: RouteDecision,
    relation: str,
) -> dict[str, object]:
    base_value = int(base.action)
    variant_value = int(variant.action)
    passes = {
        "same": variant_value == base_value,
        "increase": variant_value > base_value,
        "decrease": variant_value < base_value,
        "nondecreasing": variant_value >= base_value,
    }[relation]
    return _assertion(
        family_id,
        "relation",
        f"action_{relation}",
        relation,
        {"base": base.action.label, "variant": variant.action.label},
        passes,
    )


def _write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"cannot write empty table: {path.name}")
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def run(
    suite_path: Path,
    source_register_path: Path,
    output_dir: Path,
) -> dict[str, Any]:
    suite = json.loads(suite_path.read_text(encoding="utf-8"))
    source_register = json.loads(source_register_path.read_text(encoding="utf-8"))
    source_ids = {source["id"] for source in source_register["sources"]}
    validate_contract_suite(suite, source_ids)

    assertion_rows: list[dict[str, object]] = []
    family_rows: list[dict[str, object]] = []
    detailed_families: list[dict[str, object]] = []

    for family in suite["families"]:
        decisions: dict[str, RouteDecision] = {}
        family_assertions: list[dict[str, object]] = []
        for case_name in ("base", "variant"):
            case = family[case_name]
            decision = route_childesc(case["messages"])
            decisions[case_name] = decision
            family_assertions.extend(
                evaluate_case_assertions(
                    family["id"], case_name, decision, case.get("expected", {})
                )
            )
        family_assertions.append(
            evaluate_relation(
                family["id"],
                decisions["base"],
                decisions["variant"],
                family["relation"]["action"],
            )
        )
        assertion_rows.extend(family_assertions)
        passed = sum(bool(assertion["passes"]) for assertion in family_assertions)
        family_passes = passed == len(family_assertions)
        family_rows.append(
            {
                "family_id": family["id"],
                "factor": family["factor"],
                "base_action": decisions["base"].action.label,
                "variant_action": decisions["variant"].action.label,
                "relation": family["relation"]["action"],
                "passed_assertions": passed,
                "assertions": len(family_assertions),
                "family_passes": family_passes,
            }
        )
        detailed_families.append(
            {
                "id": family["id"],
                "factor": family["factor"],
                "source_basis": family["source_basis"],
                "base_decision": decisions["base"].to_dict(),
                "variant_decision": decisions["variant"].to_dict(),
                "assertions": family_assertions,
                "family_passes": family_passes,
            }
        )

    passed_assertions = sum(bool(row["passes"]) for row in assertion_rows)
    passed_families = sum(bool(row["family_passes"]) for row in family_rows)
    result = {
        "artifact": suite["artifact"],
        "version": suite["version"],
        "status": suite["status"],
        "frozen_on": suite["frozen_on"],
        "summary": {
            "families": len(family_rows),
            "passed_families": passed_families,
            "assertions": len(assertion_rows),
            "passed_assertions": passed_assertions,
            "family_pass_rate": passed_families / len(family_rows),
            "assertion_pass_rate": passed_assertions / len(assertion_rows),
        },
        "families": detailed_families,
    }

    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "contract_results.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    _write_csv(output_dir / "contract_assertions.csv", assertion_rows)
    _write_csv(output_dir / "contract_table.csv", family_rows)
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--suite", type=Path, required=True)
    parser.add_argument("--sources", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run(args.suite, args.sources, args.output)
    summary = result["summary"]
    print(
        "contract audit: "
        f"{summary['passed_families']}/{summary['families']} families, "
        f"{summary['passed_assertions']}/{summary['assertions']} assertions"
    )


if __name__ == "__main__":
    main()
