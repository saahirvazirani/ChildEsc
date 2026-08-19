# Changelog

All notable changes to ChildEsc will be recorded here. Benchmark versions are
immutable after release; corrections create a new candidate version.

## Unreleased

- Added provider-neutral routing adapters for Gemini, OpenAI, Anthropic, and
  OpenRouter using structured-output REST APIs.
- Added content-addressed raw-response caching and credential-free offline
  replay with cache-integrity checks.
- Added a routing-only evaluator that withholds comparative metrics when any
  requested item lacks a valid route.
- Added 15 isolated adapter, cache, leakage, and evaluator tests without
  changing the frozen 46-test scientific suite.

Supportive-response quality remains outside scope and requires a separate
rubric and human-validation study.

## 0.1.0-draft - 2026-08-18

- Added 80 LLM-assisted synthetic conversations across 20 counterfactual
  scenario families.
- Added four-level action routing and permitted/forbidden handoff-target labels.
- Added deterministic baselines, a transparent rule implementation checksum,
  safety-sensitive metrics, ablations, robustness probes, and relational
  contract checks.
- Added 46 unit and artifact-synchronization tests.
- Added prospective practitioner and youth-participatory validation protocols.

Validation status: technical checks complete; independent holdout, practitioner,
youth, clinical, ecological, cross-cultural, and deployment validation not
completed.
