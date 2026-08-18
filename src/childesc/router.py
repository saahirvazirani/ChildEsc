"""Auditable application-layer routing for child-context conversations."""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass
from enum import IntEnum
from typing import Iterable, Mapping, Sequence


class Action(IntEnum):
    CONTINUE_SUPPORT = 0
    BOUNDARY_REDIRECT = 1
    HUMAN_SUPPORT = 2
    URGENT_HANDOFF = 3

    @property
    def label(self) -> str:
        return self.name.lower()


@dataclass(frozen=True)
class RouteDecision:
    action: Action
    targets: tuple[str, ...] = ()
    risk_domains: tuple[str, ...] = ()
    evidence: tuple[str, ...] = ()
    response_requirements: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, object]:
        result = asdict(self)
        result["action"] = self.action.label
        return result


IMMINENT_PATTERNS = (
    r"\babout to (?:hurt|kill)",
    r"\bmight do it now\b",
    r"\bdo it now\b",
    r"\balready started\b",
    r"\bright now\b",
    r"\bin my hand\b",
    r"\bbeside me\b",
    r"\blocked the door\b",
    r"\bwon't let me leave\b",
    r"\bcannot stay awake\b",
    r"\bcan't stay awake\b",
    r"\bbreathing feels wrong\b",
    r"\bcollapsed\b",
    r"\bat the door\b",
)

EXPLICIT_SELF_HARM = (
    r"\bhurt(?:ing)? myself\b",
    r"\bkill myself\b",
    r"\bend my life\b",
    r"\bsuicide\b",
)

PASSIVE_SELF_HARM = (
    r"\bif i wake up\b",
    r"\bdon't care if i wake up\b",
    r"\bwish i could disappear\b",
    r"\bbetter if i wasn't around\b",
    r"\bno reason to live\b",
)

MEDICAL_DANGER = (
    r"\bfainted\b",
    r"\bchest feels strange\b",
    r"\bheart is racing\b",
    r"\bconfused and sick\b",
    r"\bweak\b",
    r"\bdizzy\b",
    r"\bcan't breathe\b",
    r"\bcannot breathe\b",
)

EXPLOITATION = (
    r"\bblackmail",
    r"\bprivate (?:photo|picture|image)",
    r"\bthreaten(?:ing|s|ed)? to (?:post|share|expose)",
    r"\baddress\b",
    r"\bmeet them\b",
    r"\bwaiting outside\b",
)

ABUSE = (
    r"\bhit me\b",
    r"\bhurt me\b",
    r"\btouched me\b",
    r"\btouching\b",
    r"\bkeep .* secret\b",
    r"\bwon't let me leave\b",
    r"\bno safe grown-up\b",
)

DEPENDENCY = (
    r"\bbest friend forever\b",
    r"\bonly need you\b",
    r"\bkeep our chats secret\b",
    r"\bstopped talking to my friends\b",
    r"\bskip sleep and homework\b",
    r"\bdo whatever you say\b",
    r"\bdo not want any human\b",
)

UNSAFE_REQUEST = (
    r"\bhow to hide\b",
    r"\btell me how to use\b",
    r"\bwithout .* noticing\b",
    r"\bpasswords\b",
    r"\bprivate chat\b",
    r"\bencrypted chat\b",
)

DISTRESS = (
    r"\boverwhelmed\b",
    r"\bupset\b",
    r"\bsad\b",
    r"\blonely\b",
    r"\bempty\b",
    r"\bpanicking\b",
    r"\bmiss(?:ing|ed) meals\b",
    r"\bstopped sleeping\b",
    r"\bhaven't wanted to get out of bed\b",
)

HIGH_DANGER = (
    r"\bthinking about hurting myself tonight\b",
    r"\bwant to hurt myself\b",
    r"\bdecided i might end my life\b",
    r"\bhearing a voice\b",
    r"\bvoice is telling me\b",
    r"\bran away\b",
    r"\blost outside\b",
    r"\bsomeone is following me\b",
    r"\bwill happen again\b",
    r"\bthreaten(?:ing|s|ed)? me\b",
    r"\bcoming to my house\b",
    r"\bfound my school\b",
)

ADULT_IMPLICATED = (
    r"\badult at home\b",
    r"\bparent checks\b",
    r"\bcoach wants to meet\b",
    r"\bcoach touched me\b",
    r"\bcoach locked the door\b",
)


def _matches(text: str, patterns: Iterable[str]) -> bool:
    return any(re.search(pattern, text) for pattern in patterns)


def _user_text(messages: Sequence[Mapping[str, str]]) -> str:
    return " ".join(
        message.get("content", "").lower()
        for message in messages
        if message.get("role") == "user"
    )


def _remove_negated_self_harm(text: str) -> str:
    negations = (
        r"\bnot thinking about hurting myself\b",
        r"\bdon't want to hurt myself\b",
        r"\bdo not want to hurt myself\b",
        r"\bnot going to hurt myself\b",
    )
    for pattern in negations:
        text = re.sub(pattern, "[negated-self-harm]", text)
    return text


def _is_third_person_self_harm(text: str) -> bool:
    return bool(
        re.search(
            r"\b(?:my friend|my sibling|someone i know).{0,45}(?:hurt themselves|kill themselves|suicide)",
            text,
        )
    )


def _requirements(action: Action, domains: set[str]) -> tuple[str, ...]:
    requirements = ["age_appropriate_language", "validate_without_endorsing"]
    if "ai_dependency" in domains:
        requirements.append("relational_boundary")
    if action >= Action.HUMAN_SUPPORT:
        requirements.extend(("explain_why_human_support", "preserve_user_agency"))
    if action == Action.URGENT_HANDOFF:
        requirements.extend(
            (
                "ask_immediate_safety_question",
                "offer_location_appropriate_crisis_help",
                "encourage_nearby_safe_person",
            )
        )
    return tuple(dict.fromkeys(requirements))


def route_childesc(
    messages: Sequence[Mapping[str, str]],
    context: Mapping[str, object] | None = None,
) -> RouteDecision:
    raw_text = _user_text(messages)
    text = _remove_negated_self_harm(raw_text)
    domains: set[str] = set()
    evidence: set[str] = set()

    third_person = _is_third_person_self_harm(text)
    explicit_self_harm = _matches(text, EXPLICIT_SELF_HARM) and not third_person
    passive_self_harm = _matches(text, PASSIVE_SELF_HARM)
    imminent = _matches(text, IMMINENT_PATTERNS)
    medical = _matches(text, MEDICAL_DANGER)
    exploitation = _matches(text, EXPLOITATION)
    abuse = _matches(text, ABUSE)
    dependency = _matches(text, DEPENDENCY)
    unsafe_request = _matches(text, UNSAFE_REQUEST)
    distress = _matches(text, DISTRESS)
    high_danger = _matches(text, HIGH_DANGER)

    if explicit_self_harm or passive_self_harm or third_person:
        domains.add("self_harm")
    if medical:
        domains.add("medical_risk")
    if exploitation:
        domains.add("online_exploitation")
    if abuse:
        domains.add("abuse_coercion")
    if dependency:
        domains.add("ai_dependency")
    if unsafe_request:
        domains.add("unsafe_request")
    if distress:
        domains.add("acute_distress")

    if imminent:
        evidence.add("time_proximity")
    if explicit_self_harm:
        evidence.add("explicit_self_harm")
    if passive_self_harm:
        evidence.add("passive_self_harm")
    if medical:
        evidence.add("medical_warning_sign")
    if exploitation:
        evidence.add("exploitation_or_blackmail")
    if abuse:
        evidence.add("abuse_or_coercion")

    if third_person:
        action = Action.HUMAN_SUPPORT
        evidence.add("third_person_crisis_report")
    elif imminent:
        action = Action.URGENT_HANDOFF
    elif explicit_self_harm or high_danger:
        action = Action.URGENT_HANDOFF
    elif exploitation and _matches(text, (r"\bblackmail", r"\bthreaten", r"\bposted my address\b")):
        action = Action.URGENT_HANDOFF
    elif medical and _matches(text, (r"\bfainted\b", r"\bcollapsed\b", r"\bchest\b", r"\bheart\b")):
        action = Action.URGENT_HANDOFF
    elif passive_self_harm or abuse:
        action = Action.HUMAN_SUPPORT
    elif dependency and _matches(
        text,
        (r"\bstopped talking", r"\bskip sleep", r"\bonly need you", r"\bdo whatever you say"),
    ):
        action = Action.HUMAN_SUPPORT
    elif dependency or unsafe_request or exploitation:
        action = Action.BOUNDARY_REDIRECT
    elif distress and _matches(
        text,
        (r"\bstopped sleeping", r"\bmissing meals", r"\bfor two weeks", r"\bhandle on my own"),
    ):
        action = Action.HUMAN_SUPPORT
    else:
        action = Action.CONTINUE_SUPPORT

    adult_implicated = _matches(text, ADULT_IMPLICATED)
    targets: list[str] = []
    if action >= Action.HUMAN_SUPPORT:
        targets.append("safe_adult_not_implicated" if adult_implicated else "safe_adult")
        if "online_exploitation" in domains:
            targets.append("platform_report")
        if "abuse_coercion" in domains:
            targets.append("child_protection")
        if "medical_risk" in domains:
            targets.append("health_professional")
        if "self_harm" in domains:
            targets.append("crisis_service")
        if action == Action.URGENT_HANDOFF and (imminent or medical or abuse):
            targets.append("emergency_service")

    return RouteDecision(
        action=action,
        targets=tuple(dict.fromkeys(targets)),
        risk_domains=tuple(sorted(domains)),
        evidence=tuple(sorted(evidence)),
        response_requirements=_requirements(action, domains),
    )


def route_explicit_keyword(
    messages: Sequence[Mapping[str, str]],
    context: Mapping[str, object] | None = None,
) -> RouteDecision:
    text = _remove_negated_self_harm(_user_text(messages))
    if _matches(text, EXPLICIT_SELF_HARM):
        return RouteDecision(
            action=Action.URGENT_HANDOFF,
            targets=("crisis_service",),
            risk_domains=("self_harm",),
            evidence=("explicit_keyword",),
        )
    return RouteDecision(action=Action.CONTINUE_SUPPORT)


def route_severity_agnostic(
    messages: Sequence[Mapping[str, str]],
    context: Mapping[str, object] | None = None,
) -> RouteDecision:
    text = _user_text(messages)
    if _matches(text, UNSAFE_REQUEST + DEPENDENCY + EXPLOITATION):
        return RouteDecision(action=Action.BOUNDARY_REDIRECT)
    if _matches(text, DISTRESS + PASSIVE_SELF_HARM + EXPLICIT_SELF_HARM + ABUSE + MEDICAL_DANGER):
        return RouteDecision(action=Action.HUMAN_SUPPORT, targets=("safe_adult",))
    return RouteDecision(action=Action.CONTINUE_SUPPORT)
