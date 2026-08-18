# Prospective Delegated Follow-Up Protocol

Status: design specification only; no data transfer, outreach, partnership, or formula is authorized or implemented

## Proposal retained for future evaluation

The candidate intervention is an optional pathway in which a participating crisis service may contact an opted-in user by a user-selected channel within a governed 1-24 hour window. A higher independently validated concern score would map monotonically to a shorter deadline. This is a research hypothesis, not a current 988 service, ChildEsc output, legal entitlement, or deployment recommendation.

## Why the original formulation cannot be implemented as written

- ChildEsc has no agreement with the 988 Lifeline Administrator or a participating crisis center.
- No evidence establishes a safe 1-24 hour cutoff formula, and delayed follow-up is not an appropriate substitute for immediate support when an attempt is in progress or danger is imminent.
- A general account-creation requirement and bundled terms clause would not establish meaningful, age-appropriate permission to disclose sensitive mental-health information.
- Model-derived concern scores and ChildEsc labels are not clinically validated and cannot independently trigger disclosure or outreach.
- The paper cannot promise legal protection to participating chatbot companies.

## Required workflow

1. The chatbot offers immediate, user-initiated crisis support when appropriate and never delays an imminent-risk pathway to place a case in a scheduled queue.
2. For non-imminent significant concern, the system may explain a prospective follow-up option only after every activation gate in `delegated_followup_extension.json` is satisfied.
3. Consent is separate, affirmative, plain-language, age-appropriate, revocable, and specific about recipient, purpose, data, channel, expiry, retention, and limits of confidentiality. Declining cannot block account access.
4. A qualified crisis professional reviews the underlying evidence, uncertainty, safe contact channel, coercion risk, and implicated-adult context before any disclosure.
5. The payload is minimum necessary. It excludes a transcript and precise location by default and is encrypted, access-logged, purpose-limited, and deleted on a predeclared schedule.
6. The receiving service accepts the case under a written capacity and service-level agreement. Queue failure, unreachable users, revocation, wrong-person contact, and unsafe-device concerns have explicit fallback procedures.

## Deadline-function requirements

An independent multidisciplinary committee, including 988/crisis-service operations, child safety, clinical, privacy, disability, cultural, and youth representatives, must research, pre-register, validate, and own any function. The function must be monotone, calibrated on independent prospective outcomes, uncertainty-aware, capable of abstaining, and separately audited across protected and access-relevant groups. The proposed 1-24 hour range remains provisional until that process is complete.

## Evaluation before deployment

Primary safety outcomes include missed imminent cases, false alerts, time to successful voluntary contact, user revocation, wrong-person disclosure, coercion, chilling effects on help-seeking, accessibility, disparities, and service-capacity failures. The protocol must compare the extension with user-initiated referral and other least-invasive alternatives. No model-only endpoint, contact attempt, or legal-compliance checklist is sufficient evidence of benefit.

## Current ChildEsc boundary

The current router may recommend or offer a `crisis_service` target. It does not collect contact details, transmit conversations or scores, schedule follow-up, contact 988, or authorize emergency action.
