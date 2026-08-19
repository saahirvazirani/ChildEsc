import json
import tempfile
import unittest
from pathlib import Path

from childesc.llm import (
    CacheError,
    CacheMissError,
    CachedRoutingClient,
    GeminiAdapter,
    JsonTransport,
    ResponseCache,
)
from childesc.router import Action


class RecordingTransport(JsonTransport):
    def __init__(self) -> None:
        self.calls: list[object] = []

    def post_json(self, request, timeout):
        self.calls.append(request)
        route = json.dumps(
            {"action": "urgent_handoff", "targets": ["crisis_service"]}
        )
        return {
            "responseId": "gemini-response",
            "candidates": [{"content": {"parts": [{"text": route}]}}],
            "usageMetadata": {"promptTokenCount": 10, "candidatesTokenCount": 8},
        }


class FailingTransport(JsonTransport):
    def post_json(self, request, timeout):
        raise AssertionError("cache replay attempted network access")


class CacheTests(unittest.TestCase):
    def test_cached_replay_needs_neither_api_key_nor_transport(self) -> None:
        messages = [{"role": "user", "content": "I might hurt myself tonight."}]
        with tempfile.TemporaryDirectory() as directory:
            cache = ResponseCache(Path(directory))
            transport = RecordingTransport()
            online = CachedRoutingClient(
                adapter=GeminiAdapter(),
                model="test-model",
                cache=cache,
                transport=transport,
                api_key="top-secret",
            )

            first = online.classify(messages)
            offline = CachedRoutingClient(
                adapter=GeminiAdapter(),
                model="test-model",
                cache=cache,
                transport=FailingTransport(),
                cache_only=True,
            )
            second = offline.classify(messages)

            self.assertFalse(first.cache_hit)
            self.assertTrue(second.cache_hit)
            self.assertEqual(second.decision.action, Action.URGENT_HANDOFF)
            self.assertEqual(len(transport.calls), 1)
            cache_text = next(Path(directory).glob("*.json")).read_text()
            self.assertNotIn("top-secret", cache_text)

    def test_cache_key_changes_with_model_or_conversation_not_api_key(self) -> None:
        messages = [{"role": "user", "content": "I feel lonely."}]
        with tempfile.TemporaryDirectory() as directory:
            cache = ResponseCache(Path(directory))
            first = CachedRoutingClient(
                GeminiAdapter(), "model-a", cache, RecordingTransport(), api_key="one"
            )
            same = CachedRoutingClient(
                GeminiAdapter(), "model-a", cache, RecordingTransport(), api_key="two"
            )
            other_model = CachedRoutingClient(
                GeminiAdapter(), "model-b", cache, RecordingTransport(), api_key="one"
            )

            self.assertEqual(first.request_hash(messages), same.request_hash(messages))
            self.assertNotEqual(
                first.request_hash(messages), other_model.request_hash(messages)
            )
            self.assertNotEqual(
                first.request_hash(messages),
                first.request_hash(
                    [{"role": "user", "content": "I feel very lonely."}]
                ),
            )

    def test_cache_only_miss_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            client = CachedRoutingClient(
                adapter=GeminiAdapter(),
                model="test-model",
                cache=ResponseCache(Path(directory)),
                transport=FailingTransport(),
                cache_only=True,
            )
            with self.assertRaises(CacheMissError):
                client.classify([{"role": "user", "content": "Hello"}])

    def test_tampered_cache_entry_is_rejected(self) -> None:
        messages = [{"role": "user", "content": "I feel lonely."}]
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            cache = ResponseCache(root)
            online = CachedRoutingClient(
                GeminiAdapter(), "test-model", cache, RecordingTransport(), api_key="key"
            )
            request_hash = online.request_hash(messages)
            online.classify(messages)
            entry_path = cache.path_for(request_hash)
            entry = json.loads(entry_path.read_text(encoding="utf-8"))
            changed_route = json.dumps(
                {"action": "continue_support", "targets": []}
            )
            entry["response"]["candidates"][0]["content"]["parts"][0][
                "text"
            ] = changed_route
            entry_path.write_text(json.dumps(entry), encoding="utf-8")

            with self.assertRaises(CacheError):
                online.classify(messages)


if __name__ == "__main__":
    unittest.main()
