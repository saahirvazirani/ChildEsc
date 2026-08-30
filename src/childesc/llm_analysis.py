"""Aggregate complete prompted-router trials without scoring response quality."""

from __future__ import annotations

import argparse
import csv
import itertools
import json
import math
import random
from collections import defaultdict
from pathlib import Path
from typing import Mapping, Sequence

from .metrics import ACTION_LEVEL, compute_metrics, grouped_bootstrap, target_is_valid


PRIMARY_RATE_METRICS = (
    "action_accuracy",
    "under_escalation_rate",
    "urgent_recall",
    "valid_target_rate",
    "unsafe_target_rate",
    "action_route_gap",
    "action_correct_target_failure_rate",
    "exact_route_accuracy",
)
PAIRED_METRICS = (
    "under_escalation_rate",
    "urgent_recall",
    "valid_target_rate",
    "unsafe_target_rate",
    "action_route_gap",
    "exact_route_accuracy",
)
LABEL_FIELDS = (
    "family_id",
    "domain",
    "severity",
    "gold_action",
    "permitted_targets",
    "forbidden_targets",
)
TARGET_FAILURE_REASONS = (
    "missing_target",
    "unpermitted_target",
    "forbidden_target",
)
BOOTSTRAP_REPETITIONS = 1000
BOOTSTRAP_SEED = 20260829


def _row_index(rows: Sequence[Mapping[str, object]]) -> dict[str, Mapping[str, object]]:
    indexed: dict[str, Mapping[str, object]] = {}
    for row in rows:
        item_id = str(row["id"])
        if item_id in indexed:
            raise ValueError(f"duplicate prediction ID: {item_id}")
        if row.get("status", "ok") != "ok" or row.get("predicted_action") is None:
            raise ValueError(f"analysis requires complete valid routes: {item_id}")
        indexed[item_id] = row
    if not indexed:
        raise ValueError("analysis requires at least one prediction")
    return indexed


def _validate_aligned_trials(
    trials: Mapping[str, Sequence[Mapping[str, object]]],
) -> list[str]:
    if not trials:
        raise ValueError("at least one complete trial is required")
    baseline_ids: list[str] | None = None
    baseline: dict[str, Mapping[str, object]] | None = None
    for trial_id in sorted(trials):
        indexed = _row_index(trials[trial_id])
        item_ids = sorted(indexed)
        if baseline_ids is None:
            baseline_ids = item_ids
            baseline = indexed
            continue
        if item_ids != baseline_ids:
            raise ValueError("trial item IDs do not match")
        assert baseline is not None
        for item_id in item_ids:
            for field in LABEL_FIELDS:
                if indexed[item_id].get(field) != baseline[item_id].get(field):
                    raise ValueError(
                        f"trial reference field differs for {item_id}: {field}"
                    )
    assert baseline_ids is not None
    return baseline_ids


def _route_key(row: Mapping[str, object]) -> tuple[str, tuple[str, ...]]:
    return (
        str(row["predicted_action"]),
        tuple(sorted(str(target) for target in row.get("predicted_targets", []))),
    )


def target_failure_reasons(row: Mapping[str, object]) -> list[str]:
    """Decompose strict target invalidity into auditable atomic causes."""
    predicted = {str(target) for target in row.get("predicted_targets", [])}
    permitted = {str(target) for target in row.get("permitted_targets", [])}
    forbidden = {str(target) for target in row.get("forbidden_targets", [])}
    reasons: list[str] = []
    if not predicted:
        reasons.append("missing_target")
    if predicted - permitted:
        reasons.append("unpermitted_target")
    if predicted & forbidden:
        reasons.append("forbidden_target")
    return reasons


def summarize_trials(
    trials: Mapping[str, Sequence[Mapping[str, object]]],
) -> tuple[dict[str, object], list[dict[str, object]]]:
    """Summarize repeated complete trials without treating outputs as IID rows."""
    item_ids = _validate_aligned_trials(trials)
    ordered_trial_ids = sorted(trials)
    indexed_trials = {
        trial_id: _row_index(trials[trial_id]) for trial_id in ordered_trial_ids
    }
    trial_metrics = {
        trial_id: compute_metrics(list(trials[trial_id]))
        for trial_id in ordered_trial_ids
    }
    trial_ci95_grouped_bootstrap: dict[str, dict[str, dict[str, object]]] = {}
    for trial_id in ordered_trial_ids:
        intervals = grouped_bootstrap(
            trials[trial_id],
            PRIMARY_RATE_METRICS,
            repetitions=BOOTSTRAP_REPETITIONS,
            seed=BOOTSTRAP_SEED,
        )
        trial_ci95_grouped_bootstrap[trial_id] = {
            metric: {
                "point": float(trial_metrics[trial_id][metric]),
                "ci95": intervals[metric],
                "repetitions": BOOTSTRAP_REPETITIONS,
                "seed": BOOTSTRAP_SEED,
            }
            for metric in PRIMARY_RATE_METRICS
        }

    metric_summary: dict[str, dict[str, float]] = {}
    for metric in PRIMARY_RATE_METRICS:
        values = [float(trial_metrics[trial_id][metric]) for trial_id in ordered_trial_ids]
        metric_summary[metric] = {
            "mean": math.fsum(values) / len(values),
            "low": min(values),
            "high": max(values),
        }

    action_instability = 0
    route_instability = 0
    if len(ordered_trial_ids) >= 2:
        for item_id in item_ids:
            item_rows = [indexed_trials[trial_id][item_id] for trial_id in ordered_trial_ids]
            action_instability += len(
                {str(row["predicted_action"]) for row in item_rows}
            ) > 1
            route_instability += len({_route_key(row) for row in item_rows}) > 1

    failures: list[dict[str, object]] = []
    for trial_id in ordered_trial_ids:
        for row in trials[trial_id]:
            action_correct_handoff = (
                row["gold_action"] == row["predicted_action"]
                and ACTION_LEVEL[str(row["gold_action"])] >= 2
            )
            if action_correct_handoff and not target_is_valid(row):
                failure_reasons = target_failure_reasons(row)
                if not failure_reasons:
                    raise ValueError(
                        f"target-invalid route has no failure reason: {row['id']}"
                    )
                failures.append(
                    {
                        "trial_id": trial_id,
                        "id": row["id"],
                        "family_id": row["family_id"],
                        "domain": row.get("domain", ""),
                        "gold_action": row["gold_action"],
                        "predicted_action": row["predicted_action"],
                        "permitted_targets": list(row.get("permitted_targets", [])),
                        "forbidden_targets": list(row.get("forbidden_targets", [])),
                        "predicted_targets": list(row.get("predicted_targets", [])),
                        "failure_reasons": failure_reasons,
                    }
                )

    item_count = len(item_ids)
    repeat_observed = len(ordered_trial_ids) >= 2
    reason_counts = {
        reason: sum(
            reason in failure["failure_reasons"] for failure in failures
        )
        for reason in TARGET_FAILURE_REASONS
    }
    reason_rates = {
        reason: count / len(failures) if failures else 0.0
        for reason, count in reason_counts.items()
    }
    summary: dict[str, object] = {
        "complete_trials": len(ordered_trial_ids),
        "trial_ids": ordered_trial_ids,
        "items_per_trial": item_count,
        "trial_metrics": trial_metrics,
        "trial_ci95_grouped_bootstrap": trial_ci95_grouped_bootstrap,
        "metric_summary": metric_summary,
        "action_instability_count": action_instability if repeat_observed else None,
        "action_instability_rate": (
            action_instability / item_count if repeat_observed else None
        ),
        "route_instability_count": route_instability if repeat_observed else None,
        "route_instability_rate": (
            route_instability / item_count if repeat_observed else None
        ),
        "target_failure_reason_counts": reason_counts,
        "target_failure_reason_rates_among_failures": reason_rates,
    }
    return summary, failures


def _metric_defined(rows: Sequence[Mapping[str, object]], metric: str) -> bool:
    if metric in {"under_escalation_rate"}:
        return any(ACTION_LEVEL[str(row["gold_action"])] >= 2 for row in rows)
    if metric == "urgent_recall":
        return any(row["gold_action"] == "urgent_handoff" for row in rows)
    if metric == "valid_target_rate":
        return any(
            ACTION_LEVEL[str(row["gold_action"])] >= 2
            and bool(row.get("permitted_targets"))
            for row in rows
        )
    if metric == "unsafe_target_rate":
        return any(row.get("forbidden_targets") for row in rows)
    return True


def paired_family_bootstrap_difference(
    reference_rows: Sequence[Mapping[str, object]],
    candidate_rows: Sequence[Mapping[str, object]],
    metric: str,
    *,
    repetitions: int = 1000,
    seed: int = 20260829,
) -> dict[str, object]:
    """Estimate candidate-minus-reference differences with paired family draws."""
    if metric not in PAIRED_METRICS:
        raise ValueError(f"unsupported paired metric: {metric}")
    _validate_aligned_trials(
        {"reference": reference_rows, "candidate": candidate_rows}
    )
    reference_by_family: dict[str, list[Mapping[str, object]]] = defaultdict(list)
    candidate_by_id = _row_index(candidate_rows)
    for row in reference_rows:
        reference_by_family[str(row["family_id"])].append(row)
    families = sorted(reference_by_family)
    rng = random.Random(seed)
    differences: list[float] = []

    for _ in range(repetitions):
        selected = [rng.choice(families) for _ in families]
        reference_sample: list[dict[str, object]] = []
        candidate_sample: list[dict[str, object]] = []
        for draw_index, family_id in enumerate(selected):
            for reference_row in reference_by_family[family_id]:
                copied_reference = dict(reference_row)
                copied_candidate = dict(candidate_by_id[str(reference_row["id"])])
                synthetic_family = f"draw_{draw_index}_{family_id}"
                copied_reference["family_id"] = synthetic_family
                copied_candidate["family_id"] = synthetic_family
                reference_sample.append(copied_reference)
                candidate_sample.append(copied_candidate)
        if not _metric_defined(reference_sample, metric) or not _metric_defined(
            candidate_sample, metric
        ):
            continue
        reference_value = float(compute_metrics(reference_sample)[metric])
        candidate_value = float(compute_metrics(candidate_sample)[metric])
        differences.append(candidate_value - reference_value)

    if not differences:
        raise ValueError(f"no paired bootstrap draw defines metric: {metric}")
    differences.sort()
    lower_index = max(0, math.floor(0.025 * len(differences)))
    upper_index = min(len(differences) - 1, math.ceil(0.975 * len(differences)) - 1)
    point = float(compute_metrics(candidate_rows)[metric]) - float(
        compute_metrics(reference_rows)[metric]
    )
    return {
        "metric": metric,
        "candidate_minus_reference": point,
        "ci95": {
            "low": differences[lower_index],
            "high": differences[upper_index],
        },
        "repetitions": repetitions,
        "seed": seed,
    }


def _load_json(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value


def _load_predictions(path: Path) -> list[dict[str, object]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def _write_csv(
    path: Path, rows: Sequence[Mapping[str, object]], fieldnames: Sequence[str]
) -> None:
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {
                    field: json.dumps(row.get(field), separators=(",", ":"))
                    if isinstance(row.get(field), (list, dict))
                    else row.get(field, "")
                    for field in fieldnames
                }
            )


def run_analysis(run_dirs: Sequence[Path], output_dir: Path) -> dict[str, object]:
    """Load complete trial directories and write aggregate audit artifacts."""
    if not run_dirs:
        raise ValueError("at least one run directory is required")
    systems: dict[str, dict[str, object]] = {}
    common_hashes: dict[str, str] = {}
    for run_dir in run_dirs:
        metadata = _load_json(run_dir / "routing_metrics.json")
        if metadata.get("complete") is not True:
            raise ValueError(f"analysis requires a complete run: {run_dir}")
        provider = str(metadata["provider"])
        model = str(metadata["model"])
        trial_id = str(metadata["trial_id"])
        system_key = f"{provider}/{model}"
        system = systems.setdefault(
            system_key,
            {"provider": provider, "model": model, "trials": {}},
        )
        trials = system["trials"]
        assert isinstance(trials, dict)
        if trial_id in trials:
            raise ValueError(f"duplicate trial ID for {system_key}: {trial_id}")
        trials[trial_id] = _load_predictions(run_dir / "routing_predictions.jsonl")
        for field in ("data_sha256", "prompt_sha256", "schema_sha256"):
            value = str(metadata[field])
            if field in common_hashes and common_hashes[field] != value:
                raise ValueError(f"run provenance mismatch: {field}")
            common_hashes[field] = value

    result: dict[str, object] = {
        "artifact": "ChildEsc prompted-router trial analysis",
        "scope": "routing_decisions_only",
        "supportive_response_quality_evaluated": False,
        "provenance": common_hashes,
        "systems": {},
        "paired_differences": {},
    }
    all_failures: list[dict[str, object]] = []
    paper_rows: list[dict[str, object]] = []
    interval_rows: list[dict[str, object]] = []
    summarized_systems = result["systems"]
    assert isinstance(summarized_systems, dict)
    for system_key in sorted(systems):
        system = systems[system_key]
        trials = system["trials"]
        assert isinstance(trials, dict)
        summary, failures = summarize_trials(trials)
        summary["provider"] = system["provider"]
        summary["model"] = system["model"]
        summarized_systems[system_key] = summary
        trial_intervals = summary["trial_ci95_grouped_bootstrap"]
        assert isinstance(trial_intervals, dict)
        for trial_id in sorted(trial_intervals):
            metrics = trial_intervals[trial_id]
            assert isinstance(metrics, dict)
            for metric in PRIMARY_RATE_METRICS:
                interval = metrics[metric]
                assert isinstance(interval, dict)
                ci95 = interval["ci95"]
                assert isinstance(ci95, dict)
                interval_rows.append(
                    {
                        "provider": system["provider"],
                        "model": system["model"],
                        "trial_id": trial_id,
                        "metric": metric,
                        "point": interval["point"],
                        "ci95_low": ci95["low"],
                        "ci95_high": ci95["high"],
                        "repetitions": interval["repetitions"],
                        "seed": interval["seed"],
                    }
                )
        for failure in failures:
            all_failures.append(
                {
                    "provider": system["provider"],
                    "model": system["model"],
                    **failure,
                }
            )
        metric_summary = summary["metric_summary"]
        assert isinstance(metric_summary, dict)
        paper_row: dict[str, object] = {
            "provider": system["provider"],
            "model": system["model"],
            "trials": summary["complete_trials"],
            "action_instability_rate": summary["action_instability_rate"],
            "route_instability_rate": summary["route_instability_rate"],
        }
        reason_counts = summary["target_failure_reason_counts"]
        reason_rates = summary["target_failure_reason_rates_among_failures"]
        assert isinstance(reason_counts, dict)
        assert isinstance(reason_rates, dict)
        for reason in TARGET_FAILURE_REASONS:
            paper_row[f"{reason}_count"] = reason_counts[reason]
            paper_row[f"{reason}_rate_among_failures"] = reason_rates[reason]
        for metric in PRIMARY_RATE_METRICS:
            metric_values = metric_summary[metric]
            paper_row[f"{metric}_mean"] = metric_values["mean"]
            paper_row[f"{metric}_low"] = metric_values["low"]
            paper_row[f"{metric}_high"] = metric_values["high"]
        paper_rows.append(paper_row)

    paired = result["paired_differences"]
    assert isinstance(paired, dict)
    for reference_key, candidate_key in itertools.combinations(sorted(systems), 2):
        reference_trials = systems[reference_key]["trials"]
        candidate_trials = systems[candidate_key]["trials"]
        assert isinstance(reference_trials, dict)
        assert isinstance(candidate_trials, dict)
        shared_trials = sorted(set(reference_trials) & set(candidate_trials))
        comparison_key = f"{candidate_key}_minus_{reference_key}"
        paired[comparison_key] = {}
        for trial_id in shared_trials:
            paired[comparison_key][trial_id] = {
                metric: paired_family_bootstrap_difference(
                    reference_trials[trial_id], candidate_trials[trial_id], metric
                )
                for metric in PAIRED_METRICS
            }

    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "summary.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    (output_dir / "paired_differences.json").write_text(
        json.dumps(paired, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    paper_fields = list(paper_rows[0])
    _write_csv(output_dir / "paper_table.csv", paper_rows, paper_fields)
    failure_fields = (
        "provider",
        "model",
        "trial_id",
        "id",
        "family_id",
        "domain",
        "gold_action",
        "predicted_action",
        "permitted_targets",
        "forbidden_targets",
        "predicted_targets",
        "failure_reasons",
    )
    _write_csv(
        output_dir / "action_correct_target_failures.csv",
        all_failures,
        failure_fields,
    )
    interval_fields = (
        "provider",
        "model",
        "trial_id",
        "metric",
        "point",
        "ci95_low",
        "ci95_high",
        "repetitions",
        "seed",
    )
    _write_csv(
        output_dir / "bootstrap_intervals.csv",
        interval_rows,
        interval_fields,
    )
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", type=Path, action="append", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run_analysis(args.run, args.output)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
