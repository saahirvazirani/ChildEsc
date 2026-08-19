# ChildEsc Anonymous Supplement

This supplement accompanies the anonymous workshop submission, "Who Is Safe
to Involve? ChildEsc Audits Escalation and Handoff Routing in Child-Facing AI."

Run the deterministic artifact pipeline from the supplement root:

```bash
make reproduce
make llm-test
```

The first command regenerates the 80-item synthetic testbed, deterministic
diagnostics, relational contract audit, and synchronization checks without
network access. The second runs the provider-adapter, cache-integrity, leakage,
and prompted-routing analysis tests without making API calls.

The reported prompted-router aggregate is in
`results/llm_v1_1_summary.json`. Raw provider responses are intentionally not
included. Their normalized decisions were replayed from content-addressed
caches before packaging; the replay hashes and protocol are recorded in
`experiments/llm_manifest.json` and
`tasks/llm_evaluation_protocol_v1_1.md`.

All conversations are synthetic. Do not use the artifact with real child data,
personal crisis disclosures, hotline transcripts, clinical records, or contact
information. Practitioner and youth validation have not occurred, and the
artifact is not suitable for clinical or deployment use.
