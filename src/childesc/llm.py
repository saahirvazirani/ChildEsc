"""Provider-neutral, cached LLM routing for optional ChildEsc evaluation."""

from __future__ import annotations

import hashlib
import json
import os
import tempfile
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from importlib import resources
from pathlib import Path
from typing import Mapping, Protocol, Sequence

from .router import Action, RouteDecision


PROMPT_VERSION = "childesc-routing-v1"
SYSTEM_PROMPT = (
    resources.files("childesc.prompts")
    .joinpath("childesc_routing_v1.txt")
    .read_text(encoding="utf-8")
    .strip()
)
TARGETS = (
    "safe_adult",
    "safe_adult_not_implicated",
    "school_support",
    "health_professional",
    "crisis_service",
    "emergency_service",
    "child_protection",
    "platform_report",
)
ROUTE_SCHEMA: dict[str, object] = {
    "type": "object",
    "properties": {
        "action": {
            "type": "string",
            "enum": [action.label for action in Action],
            "description": "The single application-layer routing action.",
        },
        "targets": {
            "type": "array",
            "items": {"type": "string", "enum": list(TARGETS)},
            "maxItems": 4,
            "description": "Human-support target classes, or an empty array.",
        },
    },
    "required": ["action", "targets"],
    "additionalProperties": False,
}
CACHE_FORMAT_VERSION = 1
MAX_CONVERSATION_CHARS = 100_000
MAX_RESPONSE_BYTES = 1024 * 1024


class LLMError(RuntimeError):
    """Base class for provider-neutral evaluation errors."""


class CacheError(LLMError):
    """A response cache is missing or internally inconsistent."""


class CacheMissError(CacheError):
    """Cache-only execution requested an entry that is not present."""


class MissingAPIKeyError(LLMError):
    """An online provider request has no configured API key."""


class ProviderError(LLMError):
    """A provider request failed before a route could be parsed."""


class ProviderResponseError(ProviderError):
    """A provider response did not contain a usable text result."""


def _canonical_json(value: object) -> str:
    return json.dumps(
        value,
        ensure_ascii=True,
        separators=(",", ":"),
        sort_keys=True,
    )


def _sha256(value: object) -> str:
    return hashlib.sha256(_canonical_json(value).encode("utf-8")).hexdigest()


def _bounded_error(message: object, limit: int = 500) -> str:
    return str(message).replace("\n", " ")[:limit]


@dataclass(frozen=True)
class RoutingRequest:
    """The complete, non-secret specification for one routing request."""

    model: str
    messages: tuple[dict[str, str], ...]
    prompt_version: str = PROMPT_VERSION
    system_prompt: str = SYSTEM_PROMPT
    max_output_tokens: int = 256
    temperature: float | None = None

    @classmethod
    def create(
        cls,
        model: str,
        messages: Sequence[Mapping[str, str]],
        *,
        max_output_tokens: int = 256,
        temperature: float | None = None,
    ) -> RoutingRequest:
        if not model.strip():
            raise ValueError("model must not be empty")
        if len(model) > 200:
            raise ValueError("model must contain at most 200 characters")
        normalized: list[dict[str, str]] = []
        for message in messages:
            role = message.get("role")
            content = message.get("content")
            if role not in {"user", "assistant"} or not isinstance(content, str):
                raise ValueError("messages require user/assistant roles and string content")
            normalized.append({"role": role, "content": content})
        if not normalized:
            raise ValueError("at least one conversation message is required")
        if sum(len(message["content"]) for message in normalized) > MAX_CONVERSATION_CHARS:
            raise ValueError("conversation exceeds the 100,000-character limit")
        if not 1 <= max_output_tokens <= 1024:
            raise ValueError("max_output_tokens must be between 1 and 1024")
        if temperature is not None and not 0.0 <= temperature <= 1.0:
            raise ValueError("provider-neutral temperature must be between 0 and 1")
        return cls(
            model=model,
            messages=tuple(normalized),
            max_output_tokens=max_output_tokens,
            temperature=temperature,
        )

    @property
    def schema(self) -> dict[str, object]:
        return ROUTE_SCHEMA

    @property
    def user_prompt(self) -> str:
        return _canonical_json({"conversation": self.messages})


@dataclass(frozen=True)
class HttpRequest:
    url: str
    headers: dict[str, str]
    body: dict[str, object]


class JsonTransport(Protocol):
    def post_json(self, request: HttpRequest, timeout: float) -> dict[str, object]:
        """Send one JSON request and return a decoded JSON object."""


class UrllibJsonTransport:
    """Small standard-library JSON transport with bounded error reporting."""

    def post_json(self, request: HttpRequest, timeout: float) -> dict[str, object]:
        payload = _canonical_json(request.body).encode("utf-8")
        outgoing = urllib.request.Request(
            request.url,
            data=payload,
            headers=request.headers,
            method="POST",
        )
        try:
            with urllib.request.urlopen(outgoing, timeout=timeout) as response:
                raw_response = response.read(MAX_RESPONSE_BYTES + 1)
                if len(raw_response) > MAX_RESPONSE_BYTES:
                    raise ProviderResponseError("provider response exceeded 1 MiB")
                decoded = json.loads(raw_response.decode("utf-8"))
        except urllib.error.HTTPError as error:
            detail = error.read(2048).decode("utf-8", errors="replace")
            raise ProviderError(
                f"provider HTTP {error.code}: {_bounded_error(detail)}"
            ) from error
        except (urllib.error.URLError, TimeoutError) as error:
            raise ProviderError(f"provider request failed: {_bounded_error(error)}") from error
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            raise ProviderResponseError("provider returned non-JSON content") from error
        if not isinstance(decoded, dict):
            raise ProviderResponseError("provider returned a non-object JSON response")
        return decoded


class ProviderAdapter:
    """Provider-specific HTTP shape behind a shared routing contract."""

    name = "provider"
    api_key_env = ""
    api_contract = ""

    def build_http_request(
        self, request: RoutingRequest, api_key: str | None
    ) -> HttpRequest:
        raise NotImplementedError

    def extract_text(self, response: Mapping[str, object]) -> str:
        raise NotImplementedError

    def audit_metadata(self, response: Mapping[str, object]) -> dict[str, object]:
        return {}

    def cache_material(self, request: RoutingRequest) -> dict[str, object]:
        http_request = self.build_http_request(request, None)
        safe_headers = {
            key: value
            for key, value in http_request.headers.items()
            if key.lower() not in {"authorization", "x-api-key", "x-goog-api-key"}
        }
        return {
            "provider": self.name,
            "api_contract": self.api_contract,
            "url": http_request.url,
            "headers": safe_headers,
            "body": http_request.body,
            "prompt_version": request.prompt_version,
        }

    def send(
        self,
        request: RoutingRequest,
        api_key: str | None,
        transport: JsonTransport,
        timeout: float,
    ) -> dict[str, object]:
        if not api_key:
            raise MissingAPIKeyError(
                f"{self.api_key_env} is required for an uncached {self.name} request"
            )
        return transport.post_json(self.build_http_request(request, api_key), timeout)


class GeminiAdapter(ProviderAdapter):
    """Gemini generateContent adapter using JSON Schema output formatting."""

    name = "gemini"
    api_key_env = "GEMINI_API_KEY"
    api_contract = "generateContent-v1beta-responseFormat-2026-08"

    def build_http_request(
        self, request: RoutingRequest, api_key: str | None
    ) -> HttpRequest:
        model = urllib.parse.quote(request.model, safe="-._")
        generation_config: dict[str, object] = {
            "maxOutputTokens": request.max_output_tokens,
            "responseFormat": {
                "text": {
                    "mimeType": "APPLICATION_JSON",
                    "schema": request.schema,
                }
            },
        }
        if request.temperature is not None:
            generation_config["temperature"] = request.temperature
        headers = {"Content-Type": "application/json"}
        if api_key:
            headers["x-goog-api-key"] = api_key
        return HttpRequest(
            url=(
                "https://generativelanguage.googleapis.com/v1beta/models/"
                f"{model}:generateContent"
            ),
            headers=headers,
            body={
                "systemInstruction": {"parts": [{"text": request.system_prompt}]},
                "contents": [
                    {"role": "user", "parts": [{"text": request.user_prompt}]}
                ],
                "generationConfig": generation_config,
            },
        )

    def extract_text(self, response: Mapping[str, object]) -> str:
        candidates = response.get("candidates")
        if not isinstance(candidates, list) or not candidates:
            feedback = response.get("promptFeedback")
            raise ProviderResponseError(
                f"Gemini returned no candidate: {_bounded_error(feedback)}"
            )
        candidate = candidates[0]
        if not isinstance(candidate, dict):
            raise ProviderResponseError("Gemini candidate has an invalid shape")
        content = candidate.get("content")
        parts = content.get("parts") if isinstance(content, dict) else None
        texts = [
            part["text"]
            for part in parts or []
            if isinstance(part, dict) and isinstance(part.get("text"), str)
        ]
        if not texts:
            raise ProviderResponseError("Gemini candidate contained no text")
        return "".join(texts)

    def audit_metadata(self, response: Mapping[str, object]) -> dict[str, object]:
        return {
            key: response[key]
            for key in ("responseId", "modelVersion", "usageMetadata")
            if key in response
        }


class OpenAIAdapter(ProviderAdapter):
    """OpenAI Responses API adapter using strict JSON Schema output."""

    name = "openai"
    api_key_env = "OPENAI_API_KEY"
    api_contract = "responses-v1-json-schema-2026-08"

    def build_http_request(
        self, request: RoutingRequest, api_key: str | None
    ) -> HttpRequest:
        body: dict[str, object] = {
            "model": request.model,
            "input": [
                {
                    "role": "system",
                    "content": [{"type": "input_text", "text": request.system_prompt}],
                },
                {
                    "role": "user",
                    "content": [{"type": "input_text", "text": request.user_prompt}],
                },
            ],
            "max_output_tokens": request.max_output_tokens,
            "text": {
                "format": {
                    "type": "json_schema",
                    "name": "childesc_route",
                    "schema": request.schema,
                    "strict": True,
                }
            },
        }
        if request.temperature is not None:
            body["temperature"] = request.temperature
        headers = {"Content-Type": "application/json"}
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"
        return HttpRequest(
            url="https://api.openai.com/v1/responses",
            headers=headers,
            body=body,
        )

    def extract_text(self, response: Mapping[str, object]) -> str:
        texts: list[str] = []
        output = response.get("output")
        for item in output if isinstance(output, list) else []:
            if not isinstance(item, dict) or item.get("type") != "message":
                continue
            content = item.get("content")
            for part in content if isinstance(content, list) else []:
                if not isinstance(part, dict):
                    continue
                if part.get("type") == "refusal":
                    raise ProviderResponseError("OpenAI returned a refusal")
                if part.get("type") == "output_text" and isinstance(
                    part.get("text"), str
                ):
                    texts.append(part["text"])
        if not texts:
            raise ProviderResponseError(
                f"OpenAI returned no output text; status={response.get('status')}"
            )
        return "".join(texts)

    def audit_metadata(self, response: Mapping[str, object]) -> dict[str, object]:
        return {
            key: response[key]
            for key in ("id", "model", "status", "usage")
            if key in response
        }


class AnthropicAdapter(ProviderAdapter):
    """Anthropic Messages API adapter using output_config JSON Schema."""

    name = "anthropic"
    api_key_env = "ANTHROPIC_API_KEY"
    api_contract = "messages-v1-output-config-2026-08"

    def build_http_request(
        self, request: RoutingRequest, api_key: str | None
    ) -> HttpRequest:
        body: dict[str, object] = {
            "model": request.model,
            "max_tokens": request.max_output_tokens,
            "system": request.system_prompt,
            "messages": [{"role": "user", "content": request.user_prompt}],
            "output_config": {
                "format": {"type": "json_schema", "schema": request.schema}
            },
        }
        if request.temperature is not None:
            body["temperature"] = request.temperature
        headers = {
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01",
        }
        if api_key:
            headers["x-api-key"] = api_key
        return HttpRequest(
            url="https://api.anthropic.com/v1/messages",
            headers=headers,
            body=body,
        )

    def extract_text(self, response: Mapping[str, object]) -> str:
        content = response.get("content")
        texts = [
            part["text"]
            for part in (content if isinstance(content, list) else [])
            if isinstance(part, dict)
            and part.get("type") == "text"
            and isinstance(part.get("text"), str)
        ]
        if not texts:
            raise ProviderResponseError(
                f"Anthropic returned no text; stop_reason={response.get('stop_reason')}"
            )
        return "".join(texts)

    def audit_metadata(self, response: Mapping[str, object]) -> dict[str, object]:
        return {
            key: response[key]
            for key in ("id", "model", "stop_reason", "usage")
            if key in response
        }


class OpenRouterAdapter(ProviderAdapter):
    """OpenRouter Chat Completions adapter with required structured output."""

    name = "openrouter"
    api_key_env = "OPENROUTER_API_KEY"
    api_contract = "chat-completions-v1-json-schema-2026-08"

    def build_http_request(
        self, request: RoutingRequest, api_key: str | None
    ) -> HttpRequest:
        body: dict[str, object] = {
            "model": request.model,
            "messages": [
                {"role": "system", "content": request.system_prompt},
                {"role": "user", "content": request.user_prompt},
            ],
            "max_tokens": request.max_output_tokens,
            "response_format": {
                "type": "json_schema",
                "json_schema": {
                    "name": "childesc_route",
                    "strict": True,
                    "schema": request.schema,
                },
            },
            "provider": {"require_parameters": True},
        }
        if request.temperature is not None:
            body["temperature"] = request.temperature
        headers = {"Content-Type": "application/json"}
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"
        return HttpRequest(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            body=body,
        )

    def extract_text(self, response: Mapping[str, object]) -> str:
        choices = response.get("choices")
        if not isinstance(choices, list) or not choices:
            raise ProviderResponseError("OpenRouter returned no completion choice")
        choice = choices[0]
        if not isinstance(choice, dict):
            raise ProviderResponseError("OpenRouter choice has an invalid shape")
        if choice.get("error"):
            raise ProviderResponseError(
                f"OpenRouter choice error: {_bounded_error(choice['error'])}"
            )
        finish_reason = choice.get("finish_reason")
        if finish_reason in {"content_filter", "error"}:
            raise ProviderResponseError(
                f"OpenRouter completion stopped with {finish_reason}"
            )
        message = choice.get("message")
        content = message.get("content") if isinstance(message, dict) else None
        if not isinstance(content, str) or not content.strip():
            raise ProviderResponseError("OpenRouter choice contained no text")
        return content

    def audit_metadata(self, response: Mapping[str, object]) -> dict[str, object]:
        return {
            key: response[key]
            for key in ("id", "model", "provider", "usage")
            if key in response
        }


PROVIDERS: dict[str, type[ProviderAdapter]] = {
    "gemini": GeminiAdapter,
    "openai": OpenAIAdapter,
    "anthropic": AnthropicAdapter,
    "openrouter": OpenRouterAdapter,
}


def get_adapter(name: str) -> ProviderAdapter:
    try:
        return PROVIDERS[name]()
    except KeyError as error:
        raise ValueError(f"unsupported provider: {name}") from error


def parse_route(raw_text: str) -> RouteDecision:
    """Strictly parse the two-field provider-neutral routing contract."""
    try:
        value = json.loads(raw_text)
    except json.JSONDecodeError as error:
        raise ValueError("route output is not valid JSON") from error
    if not isinstance(value, dict) or set(value) != {"action", "targets"}:
        raise ValueError("route output must contain only action and targets")
    action_label = value["action"]
    if not isinstance(action_label, str):
        raise ValueError("route action must be a string")
    try:
        action = next(action for action in Action if action.label == action_label)
    except StopIteration as error:
        raise ValueError(f"unknown route action: {action_label}") from error
    targets = value["targets"]
    if not isinstance(targets, list) or any(
        not isinstance(target, str) for target in targets
    ):
        raise ValueError("route targets must be an array of strings")
    if len(targets) > 4 or len(targets) != len(set(targets)):
        raise ValueError("route targets must be unique and contain at most four items")
    unknown_targets = set(targets) - set(TARGETS)
    if unknown_targets:
        raise ValueError(f"unknown route target: {sorted(unknown_targets)[0]}")
    if action < Action.HUMAN_SUPPORT and targets:
        raise ValueError("non-handoff actions must not include targets")
    if action >= Action.HUMAN_SUPPORT and not targets:
        raise ValueError("human-support actions require at least one target")
    return RouteDecision(action=action, targets=tuple(targets))


class ResponseCache:
    """Content-addressed raw response cache with atomic writes."""

    def __init__(self, root: Path) -> None:
        self.root = root

    def path_for(self, request_hash: str) -> Path:
        return self.root / f"{request_hash}.json"

    def load(
        self, request_hash: str, request_material: Mapping[str, object]
    ) -> dict[str, object] | None:
        path = self.path_for(request_hash)
        if not path.exists():
            return None
        try:
            entry = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as error:
            raise CacheError(f"unreadable cache entry: {path.name}") from error
        if (
            not isinstance(entry, dict)
            or entry.get("cache_format_version") != CACHE_FORMAT_VERSION
            or entry.get("request_hash") != request_hash
            or entry.get("request") != request_material
            or not isinstance(entry.get("response"), dict)
            or entry.get("response_sha256") != _sha256(entry.get("response"))
        ):
            raise CacheError(f"cache verification failed: {path.name}")
        return entry["response"]

    def store(
        self,
        request_hash: str,
        request_material: Mapping[str, object],
        response: Mapping[str, object],
    ) -> None:
        self.root.mkdir(parents=True, exist_ok=True)
        entry = {
            "cache_format_version": CACHE_FORMAT_VERSION,
            "request_hash": request_hash,
            "request": request_material,
            "response": response,
            "response_sha256": _sha256(response),
        }
        temporary_path: Path | None = None
        try:
            with tempfile.NamedTemporaryFile(
                "w",
                encoding="utf-8",
                dir=self.root,
                prefix=f".{request_hash}.",
                suffix=".tmp",
                delete=False,
            ) as stream:
                temporary_path = Path(stream.name)
                stream.write(json.dumps(entry, indent=2, sort_keys=True) + "\n")
            os.replace(temporary_path, self.path_for(request_hash))
        finally:
            if temporary_path is not None and temporary_path.exists():
                temporary_path.unlink()


@dataclass(frozen=True)
class RoutingAttempt:
    decision: RouteDecision | None
    status: str
    cache_hit: bool
    request_hash: str
    error: str | None = None
    provider_metadata: Mapping[str, object] | None = None


class CachedRoutingClient:
    """Classify routes online once, then replay exact responses from cache."""

    def __init__(
        self,
        adapter: ProviderAdapter,
        model: str,
        cache: ResponseCache,
        transport: JsonTransport,
        *,
        api_key: str | None = None,
        cache_only: bool = False,
        timeout: float = 60.0,
        max_output_tokens: int = 256,
        temperature: float | None = None,
    ) -> None:
        self.adapter = adapter
        self.model = model
        self.cache = cache
        self.transport = transport
        self.api_key = api_key
        self.cache_only = cache_only
        self.timeout = timeout
        self.max_output_tokens = max_output_tokens
        self.temperature = temperature
        if timeout <= 0:
            raise ValueError("timeout must be positive")

    def _request(self, messages: Sequence[Mapping[str, str]]) -> RoutingRequest:
        return RoutingRequest.create(
            self.model,
            messages,
            max_output_tokens=self.max_output_tokens,
            temperature=self.temperature,
        )

    def request_hash(self, messages: Sequence[Mapping[str, str]]) -> str:
        request = self._request(messages)
        return _sha256(self.adapter.cache_material(request))

    def classify(self, messages: Sequence[Mapping[str, str]]) -> RoutingAttempt:
        request = self._request(messages)
        material = self.adapter.cache_material(request)
        request_hash = _sha256(material)
        response = self.cache.load(request_hash, material)
        cache_hit = response is not None
        if response is None:
            if self.cache_only:
                raise CacheMissError(f"missing cached response: {request_hash}")
            try:
                response = self.adapter.send(
                    request, self.api_key, self.transport, self.timeout
                )
            except ProviderError as error:
                return RoutingAttempt(
                    decision=None,
                    status="provider_error",
                    cache_hit=False,
                    request_hash=request_hash,
                    error=_bounded_error(error),
                )
            self.cache.store(request_hash, material, response)
        try:
            raw_text = self.adapter.extract_text(response)
            decision = parse_route(raw_text)
        except (ProviderResponseError, ValueError) as error:
            return RoutingAttempt(
                decision=None,
                status="invalid_response",
                cache_hit=cache_hit,
                request_hash=request_hash,
                error=_bounded_error(error),
                provider_metadata=self.adapter.audit_metadata(response),
            )
        return RoutingAttempt(
            decision=decision,
            status="ok",
            cache_hit=cache_hit,
            request_hash=request_hash,
            provider_metadata=self.adapter.audit_metadata(response),
        )
