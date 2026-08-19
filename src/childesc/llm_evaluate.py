"""Evaluate cached or live LLM routing decisions, never response quality."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
from typing import Mapping

from .llm import (
    PROMPT_VERSION,
    ROUTE_SCHEMA,
    SYSTEM_PROMPT,
    CacheMissError,
    CachedRoutingClient,
    ResponseCache,
    UrllibJsonTransport,
    get_adapter,
)
from .metrics import ACTION_LEVEL, SEVERITY_LEVEL, compute_metrics, grouped_bootstrap


INTERVAL_METRICS = (
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


def _sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _defined_interval_metrics(
    rows: list[dict[str, object]],
) -> tuple[str, ...]:
    """Select conditional metrics that the requested benchmark slice defines."""
    has_urgent = any(row["gold_action"] == "urgent_handoff" for row in rows)
    has_escalation = any(
        ACTION_LEVEL[str(row["gold_action"])] >= 2 for row in rows
    )
    has_target = any(
        ACTION_LEVEL[str(row["gold_action"])] >= 2
        and bool(row["permitted_targets"])
        for row in rows
    )
    has_forbidden = any(bool(row["forbidden_targets"]) for row in rows)
    by_family: dict[str, list[dict[str, object]]] = {}
    for row in rows:
        by_family.setdefault(str(row["family_id"]), []).append(row)
    has_gold_transition = False
    for family_rows in by_family.values():
        ordered = sorted(
            family_rows,
            key=lambda row: SEVERITY_LEVEL[str(row["severity"])],
        )
        if any(
            ACTION_LEVEL[str(current["gold_action"])]
            > ACTION_LEVEL[str(previous["gold_action"])]
            for previous, current in zip(ordered, ordered[1:])
        ):
            has_gold_transition = True
            break
    conditional = {
        "urgent_recall": has_urgent,
        "under_escalation_rate": has_escalation,
        "severe_under_escalation_rate": has_escalation,
        "counterfactual_sensitivity": has_gold_transition,
        "valid_target_rate": has_target,
        "unsafe_target_rate": has_forbidden,
    }
    return tuple(
        metric for metric in INTERVAL_METRICS if conditional.get(metric, True)
    )


def evaluate_item(
    item: Mapping[str, object], client: CachedRoutingClient
) -> dict[str, object]:
    """Send only the conversation to a model and attach labels afterward."""
    conversation = item["conversation"]
    if not isinstance(conversation, list):
        raise ValueError("benchmark conversation must be a list")
    attempt = client.classify(conversation)
    decision = attempt.decision
    return {
        "id": item["id"],
        "family_id": item["family_id"],
        "domain": item["domain"],
        "severity": item["severity"],
        "gold_action": item["gold_action"],
        "predicted_action": decision.action.label if decision else None,
        "permitted_targets": item.get("permitted_targets", []),
        "forbidden_targets": item.get("forbidden_targets", []),
        "predicted_targets": list(decision.targets) if decision else [],
        "status": attempt.status,
        "cache_hit": attempt.cache_hit,
        "request_hash": attempt.request_hash,
        "error": attempt.error,
        "provider_metadata": attempt.provider_metadata or {},
    }


def run(
    data_path: Path,
    output_dir: Path,
    client: CachedRoutingClient,
    *,
    limit: int | None = None,
) -> dict[str, object]:
    """Evaluate one provider/model and write auditable routing-only outputs."""
    data_text = data_path.read_text(encoding="utf-8")
    items = [
        json.loads(line)
        for line in data_text.splitlines()
        if line.strip()
    ]
    if limit is not None:
        if limit < 1:
            raise ValueError("limit must be positive")
        items = items[:limit]
    if not items:
        raise ValueError("evaluation requires at least one benchmark item")

    rows = [evaluate_item(item, client) for item in items]
    output_dir.mkdir(parents=True, exist_ok=True)
    predictions_path = output_dir / "routing_predictions.jsonl"
    predictions_path.write_text(
        "".join(json.dumps(row, sort_keys=True) + "\n" for row in rows),
        encoding="utf-8",
    )

    valid_rows = [row for row in rows if row["status"] == "ok"]
    complete = len(valid_rows) == len(rows)
    point_metrics = compute_metrics(valid_rows) if complete else None
    family_count = len({str(row["family_id"]) for row in rows})
    intervals = None
    if complete and family_count < len(rows):
        intervals = grouped_bootstrap(
            valid_rows, _defined_interval_metrics(valid_rows)
        )

    cache_hits = sum(bool(row["cache_hit"]) for row in rows)
    result: dict[str, object] = {
        "benchmark": "ChildEsc",
        "benchmark_version": "0.1.0",
        "scope": "routing_decisions_only",
        "supportive_response_quality_evaluated": False,
        "supportive_response_validation_required": (
            "separate rubric and human-validation study"
        ),
        "provider": client.adapter.name,
        "model": client.model,
        "api_contract": client.adapter.api_contract,
        "data_sha256": _sha256_text(data_text),
        "evaluated_item_ids_sha256": _sha256_text(
            json.dumps([row["id"] for row in rows], separators=(",", ":"))
        ),
        "requested_limit": limit,
        "prompt_version": PROMPT_VERSION,
        "prompt_sha256": _sha256_text(SYSTEM_PROMPT),
        "schema_sha256": _sha256_text(
            json.dumps(ROUTE_SCHEMA, separators=(",", ":"), sort_keys=True)
        ),
        "temperature": client.temperature,
        "max_output_tokens": client.max_output_tokens,
        "cache_only": client.cache_only,
        "items": len(rows),
        "complete": complete,
        "valid_responses": len(valid_rows),
        "invalid_responses": sum(
            row["status"] == "invalid_response" for row in rows
        ),
        "provider_errors": sum(row["status"] == "provider_error" for row in rows),
        "cache_hits": cache_hits,
        "cache_misses": len(rows) - cache_hits,
        "cache_hit_rate": cache_hits / len(rows),
        "routing_metrics": point_metrics,
        "ci95_grouped_bootstrap": intervals,
        "comparative_metrics_policy": (
            "reported only when every benchmark item has a valid route"
        ),
    }
    (output_dir / "routing_metrics.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return result


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Evaluate ChildEsc routing actions and targets with an LLM. "
            "This command does not generate or assess supportive responses."
        )
    )
    parser.add_argument("--data", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--provider",
        choices=("gemini", "openai", "anthropic", "openrouter"),
        required=True,
    )
    parser.add_argument("--model", required=True)
    parser.add_argument(
        "--cache", type=Path, default=Path(".cache/childesc/llm-responses")
    )
    parser.add_argument("--cache-only", action="store_true")
    parser.add_argument("--limit", type=int)
    parser.add_argument("--timeout", type=float, default=60.0)
    parser.add_argument("--max-output-tokens", type=int, default=256)
    parser.add_argument("--temperature", type=float)
    args = parser.parse_args()

    adapter = get_adapter(args.provider)
    api_key = None if args.cache_only else os.environ.get(adapter.api_key_env)
    if not args.cache_only and not api_key:
        parser.error(
            f"{adapter.api_key_env} is required unless --cache-only is used"
        )
    client = CachedRoutingClient(
        adapter=adapter,
        model=args.model,
        cache=ResponseCache(args.cache),
        transport=UrllibJsonTransport(),
        api_key=api_key,
        cache_only=args.cache_only,
        timeout=args.timeout,
        max_output_tokens=args.max_output_tokens,
        temperature=args.temperature,
    )
    try:
        result = run(args.data, args.output, client, limit=args.limit)
    except CacheMissError as error:
        parser.error(str(error))
    print(json.dumps(result, indent=2, sort_keys=True))
    if not result["complete"]:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
