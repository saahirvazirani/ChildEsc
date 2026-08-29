# Provider-Neutral LLM Routing Evaluation

## Scope

The optional LLM path evaluates exactly two outputs:

1. one of `continue_support`, `boundary_redirect`, `human_support`, or
   `urgent_handoff`; and
2. zero or more permitted handoff target classes from the frozen ChildEsc
   vocabulary.

It does not generate, score, or retain a proposed supportive response. Routing
performance is not evidence that a model's language is safe, helpful,
developmentally appropriate, culturally responsive, clinically sound, or
acceptable to young people. Those claims require a separately pre-specified
response rubric and appropriately governed practitioner and youth validation.

## Leakage Boundary

`childesc.llm_evaluate.evaluate_item` passes only `item["conversation"]` to the
model client. The provider request does not contain the item ID, family, domain,
severity, gold action, permitted targets, forbidden targets,
`adult_implicated`, or onset annotation. Labels are attached only after the
cached or live route is returned. Regression tests inspect the serialized HTTP
body for those fields.

The exact system prompt is versioned at
`src/childesc/prompts/childesc_routing_v1.txt`. Every run records the prompt and
schema SHA-256 hashes.

## Provider Contract

All adapters use the same strict JSON Schema:

```json
{
  "action": "human_support",
  "targets": ["safe_adult_not_implicated"]
}
```

Extra fields, prose, code fences, unknown labels, duplicate targets, targets on
non-handoff actions, and targetless human handoffs are rejected rather than
coerced. The current REST shapes were checked against official documentation on
2026-08-19:

- Gemini `models.generateContent` and structured outputs:
  <https://ai.google.dev/api/generate-content> and
  <https://ai.google.dev/gemini-api/docs/structured-output?lang=rest>
- OpenAI Responses and structured outputs:
  <https://platform.openai.com/docs/api-reference/responses/create> and
  <https://platform.openai.com/docs/guides/structured-outputs?api-mode=responses>
- Anthropic Messages and structured outputs:
  <https://platform.claude.com/docs/en/api/messages/create> and
  <https://platform.claude.com/docs/en/build-with-claude/structured-outputs>
- OpenRouter Chat Completions and structured outputs:
  <https://openrouter.ai/docs/api_reference/overview> and
  <https://openrouter.ai/docs/guides/features/structured-outputs>

The adapters use only the Python standard library. No provider SDK is required.
The API contract identifier is part of each cache key, so a future endpoint
migration cannot silently reuse old responses.

## Live Run

First run the no-network adapter tests:

```bash
make llm-test
```

Then make a small paid/provider-account smoke run. The reported v1.1.1 study
used OpenRouter with a dated model slug, the first-party Anthropic endpoint,
fallbacks disabled, low reasoning effort, and a 1,024-token output cap:

```bash
export OPENROUTER_API_KEY="your-key"
PYTHONPATH=src python3 -m childesc.llm_evaluate \
  --data benchmark/childesc_v0_1.jsonl \
  --provider openrouter \
  --model anthropic/claude-sonnet-5-20260630 \
  --openrouter-provider anthropic \
  --reasoning-effort low \
  --max-output-tokens 1024 \
  --protocol-version 1.1.1 \
  --trial-id v1-1-smoke-1 \
  --limit 4 \
  --cache .cache/childesc/openrouter-claude-sonnet-5-v1-1 \
  --output results/llm/openrouter-claude-sonnet-5-v1-1/smoke-1
```

Inspect `routing_predictions.jsonl` before removing `--limit`. A full run uses
the same command without that flag. Use separate cache and output directories
for every provider/model/settings combination, even though cache hashes already
prevent collisions.

For a pre-registered repeated evaluation, run each trial under an explicit
identifier such as `trial-1`, `trial-2`, and `trial-3`. Trial identity is local
cache provenance: it creates an independent provider attempt but is never sent
in the prompt or request body. Keep one output directory per trial for primary
experiments. The evaluator also appends one non-secret row per item to
`attempts.jsonl`, including request and response hashes, provider metadata,
status, and cache use.

Comparison adapters use the same workflow:

```bash
export OPENAI_API_KEY="your-key"
PYTHONPATH=src python3 -m childesc.llm_evaluate \
  --data benchmark/childesc_v0_1.jsonl \
  --provider openai \
  --model MODEL_ID \
  --trial-id trial-1 \
  --cache .cache/childesc/openai-model \
  --output results/llm/openai-model

export ANTHROPIC_API_KEY="your-key"
PYTHONPATH=src python3 -m childesc.llm_evaluate \
  --data benchmark/childesc_v0_1.jsonl \
  --provider anthropic \
  --model MODEL_ID \
  --trial-id trial-1 \
  --cache .cache/childesc/anthropic-model \
  --output results/llm/anthropic-model

export OPENROUTER_API_KEY="your-key"
PYTHONPATH=src python3 -m childesc.llm_evaluate \
  --data benchmark/childesc_v0_1.jsonl \
  --provider openrouter \
  --model openai/gpt-4o-mini \
  --trial-id trial-1 \
  --cache .cache/childesc/openrouter-gpt-4o-mini \
  --output results/llm/openrouter-gpt-4o-mini
```

OpenRouter structured-output support is endpoint-dependent. Before selecting a
model, confirm that its model/provider page advertises `structured_outputs` and
`response_format`. The adapter sends `provider.require_parameters=true` so
OpenRouter routes only to an endpoint that accepts the requested parameters.
OpenRouter notes that strict enforcement can still vary by upstream provider,
so ChildEsc independently applies the same strict parser and incomplete-run
policy used for direct providers. Response-healing plugins are deliberately not
enabled because they would introduce a provider-specific transformation between
the model output and the evaluated route.

`require_parameters` constrains capability but does not itself select one
upstream vendor. Use `--openrouter-provider PROVIDER_SLUG` to send an `only`
allowlist and disable provider fallbacks. Record both the requested model and
the returned model/provider metadata. Protocol v1.1.1 accepts OpenRouter's
short returned alias only through the dated public identity snapshot in
`experiments/openrouter_claude_sonnet_5_snapshot_2026-08-19.json`; do not infer
missing provenance for a different run.

`temperature` is omitted by default because model support differs. If a study
sets `--temperature`, use the same supported value across comparison runs and
report it. The evaluator performs one request per cache miss and does not hide
automatic retries. A provider error therefore remains an incomplete item.

## Offline Replay

After a successful live run, remove the API key and add `--cache-only` while
keeping provider, model, prompt, schema, generation settings, data, and item
limit identical. Any missing entry aborts immediately. A successful replay
therefore proves that no provider call was needed for the reported outputs.

Cache entries are content-addressed by the complete non-secret request:

- provider and API contract version;
- endpoint and non-secret headers;
- exact model ID and generation settings;
- local trial identifier, which is excluded from the provider payload;
- system prompt and response schema; and
- canonical synthetic conversation payload.

Entries contain that request material and the raw provider JSON response. API
keys are used only in HTTP headers and are excluded from both hashes and files.
Writes are atomic. Cache verification fails if the stored request, request hash,
raw response, or response hash is modified.

Trial-aware evaluation uses cache format version 2. Caches created before trial
identity was introduced are intentionally not reused because they cannot prove
which independent attempt produced a response. The run record also stores the
protocol version and non-secret request policy. Protocol version is not provider
payload material, which preserves exact replay of legacy provider requests.

## Output and Reporting Rules

`routing_predictions.jsonl` records every benchmark item, route or null route,
status, cache hit, request hash, bounded error, and limited provider metadata.
`routing_metrics.json` records the provider/model/settings, prompt/schema hashes,
API contract, dataset and evaluated-item hashes, completion counts, and routing
metrics. `attempts.jsonl` is append-only and records every observed attempt,
including incomplete trials. Use a fresh output directory for each primary
trial so its predictions and metrics cannot overwrite another trial.

Standard comparative metrics and grouped bootstrap intervals are reported only
when every requested item yields a valid route. If any response is refused,
malformed, or lost to a provider error, `complete` is false and
`routing_metrics` is null. This prevents selective exclusion from improving a
model's score. The item-level failure record is still written for diagnosis.

Do not compare a four-item smoke run with a full 80-item run. Do not compare live
results collected under different prompt/schema hashes as if they were the same
evaluation. Provider/model names and cache files are experiment provenance, not
evidence of clinical validity or deployment safety.

## Reported v1.2 Cross-System Audit

After incomplete v1.0 pilots exposed reasoning-budget and credit failures,
protocol v1.1 fixed the Claude configuration and yielded three complete trials.
Protocol v1.2 then froze two comparison model families, first-party endpoint
requirements, hashes, inclusion rules, and a result-dependent claim gate before
the comparison calls. This remains a post-pilot study, not a preregistration,
independent holdout, or leaderboard.

Eight complete 80-item trials across Claude Sonnet 5, Gemini 3.1 Pro Preview,
and GPT-5.5 replayed without credentials. Mean action accuracy spans
80.0--83.1%, while exact route accuracy spans 33.8--51.7%, producing
29.2--49.4-point action-route gaps. Among action-correct handoffs,
42.7--71.2% violate target constraints. Every one of the 247 such failures
includes an extra unpermitted target; two Gemini trial-items also include a
forbidden target. One additional GPT trial ended at 79/80 after a provider
error and remains incomplete and unscored without retry. These are diagnostics
against the same provisional, policy-exposed synthetic labels; they do not
establish generalization, clinical validity, model superiority, or real-world
safety. The checked-in aggregate is `results/llm_v1_2_summary.json`; raw
responses remain excluded from Git.

## Repeated-Trial Analysis

After complete trials have replayed from cache, aggregate their routing
decisions without treating repeated outputs as independent benchmark items:

```bash
PYTHONPATH=src python3 -m childesc.llm_analysis \
  --run results/llm/openrouter-gemini/trial-1 \
  --run results/llm/openrouter-gemini/trial-2 \
  --run results/llm/openrouter-gemini/trial-3 \
  --output results/llm/analysis
```

The analyzer rejects incomplete runs, mismatched prompt/schema/data hashes,
duplicate trial IDs, and inconsistent reference fields. It writes:

- `summary.json` with per-trial metrics, trial means and ranges, and action/full-
  route instability;
- `paper_table.csv` with deterministic reporting fields;
- `action_correct_target_failures.csv` for cases where the action is correct but
  targets invalidate the route; and
- `paired_differences.json` with family-paired bootstrap differences for systems
  sharing trial IDs.

The action-route gap is exact action accuracy minus exact route accuracy. It
quantifies how much action-only scoring would overstate conformance because of
missing, unpermitted, forbidden, or spurious targets. It is not a clinical risk
score.

## Data and Safety

The checked-in benchmark is synthetic and contains sensitive themes. Provider
processing is still subject to the selected account, contract, region, and data
retention terms. Review those terms before a live run. Never send real child
data, hotline transcripts, personal crisis disclosures, participant responses,
clinical records, contact information, or identifiers through this evaluator.

Local caches are intentionally excluded from Git. Treat them as research data:
restrict access, set a retention period, and delete them when no longer needed.
