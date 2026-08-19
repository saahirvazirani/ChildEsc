"""Run ChildEsc baselines and export reproducible evaluation artifacts."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Callable, Mapping, Sequence

from .metrics import compute_metrics, grouped_bootstrap
from .router import (
    RouteDecision,
    route_childesc,
    route_explicit_keyword,
    route_severity_agnostic,
)


Router = Callable[
    [Sequence[Mapping[str, str]], Mapping[str, object] | None], RouteDecision
]

ROUTERS: dict[str, Router] = {
    "explicit_keyword": route_explicit_keyword,
    "severity_agnostic": route_severity_agnostic,
    "childesc_rules": route_childesc,
}


def evaluate_item(item: Mapping[str, object], router: Router) -> dict[str, object]:
    conversation = item["conversation"]
    assert isinstance(conversation, list)
    decision = router(conversation, None)
    return {
        "id": item["id"],
        "family_id": item["family_id"],
        "domain": item["domain"],
        "severity": item["severity"],
        "gold_action": item["gold_action"],
        "predicted_action": decision.action.label,
        "permitted_targets": item.get("permitted_targets", []),
        "forbidden_targets": item.get("forbidden_targets", []),
        "predicted_targets": list(decision.targets),
        "risk_domains": list(decision.risk_domains),
        "evidence": list(decision.evidence),
    }


def run(data_path: Path, output_dir: Path) -> dict[str, object]:
    items = [json.loads(line) for line in data_path.read_text(encoding="utf-8").splitlines()]
    output_dir.mkdir(parents=True, exist_ok=True)
    all_metrics: dict[str, object] = {
        "benchmark": "ChildEsc",
        "version": "0.1.0",
        "items": len(items),
        "bootstrap_repetitions": 1000,
        "systems": {},
    }
    prediction_rows: list[dict[str, object]] = []

    interval_metrics = (
        "action_accuracy",
        "action_route_gap",
        "action_correct_target_failure_rate",
        "macro_f1",
        "under_escalation_rate",
        "severe_under_escalation_rate",
        "over_escalation_rate",
        "urgent_recall",
        "counterfactual_sensitivity",
        "valid_target_rate",
        "unsafe_target_rate",
        "exact_route_accuracy",
    )
    for name, router in ROUTERS.items():
        rows = [evaluate_item(item, router) for item in items]
        for row in rows:
            prediction_rows.append({"system": name, **row})
        all_metrics["systems"][name] = {
            "point": compute_metrics(rows),
            "ci95_grouped_bootstrap": grouped_bootstrap(rows, interval_metrics),
        }

    metrics_path = output_dir / "metrics.json"
    metrics_path.write_text(
        json.dumps(all_metrics, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    predictions_path = output_dir / "predictions.csv"
    fieldnames = list(prediction_rows[0])
    with predictions_path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in prediction_rows:
            writer.writerow(
                {
                    key: json.dumps(value) if isinstance(value, list) else value
                    for key, value in row.items()
                }
            )

    table_path = output_dir / "paper_table.csv"
    table_fields = [
        "system",
        "action_accuracy",
        "action_route_gap",
        "action_correct_handoff_n",
        "action_correct_target_failures",
        "action_correct_target_failure_rate",
        "macro_f1",
        "urgent_recall",
        "under_escalation_rate",
        "severe_under_escalation_rate",
        "over_escalation_rate",
        "monotonicity_violation_rate",
        "counterfactual_sensitivity",
        "valid_target_rate",
        "unsafe_target_rate",
        "exact_route_accuracy",
    ]
    with table_path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=table_fields, lineterminator="\n")
        writer.writeheader()
        for name, result in all_metrics["systems"].items():
            point = result["point"]
            writer.writerow({"system": name, **{field: point[field] for field in table_fields[1:]}})

    return all_metrics


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    metrics = run(args.data, args.output)
    print(json.dumps(metrics["systems"], indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
