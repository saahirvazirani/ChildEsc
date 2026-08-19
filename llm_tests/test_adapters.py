import json
import unittest

from childesc.llm import (
    AnthropicAdapter,
    GeminiAdapter,
    OpenAIAdapter,
    OpenRouterAdapter,
    ProviderResponseError,
    RoutingRequest,
    parse_route,
)
from childesc.router import Action


MESSAGES = (
    {"role": "user", "content": "I have felt overwhelmed for two weeks."},
)


class AdapterTests(unittest.TestCase):
    def setUp(self) -> None:
        self.request = RoutingRequest.create(model="test-model", messages=MESSAGES)

    def test_gemini_uses_current_structured_output_shape(self) -> None:
        http_request = GeminiAdapter().build_http_request(self.request, "secret")

        self.assertIn("models/test-model:generateContent", http_request.url)
        self.assertEqual(http_request.headers["x-goog-api-key"], "secret")
        text_format = http_request.body["generationConfig"]["responseFormat"]["text"]
        self.assertEqual(text_format["mimeType"], "APPLICATION_JSON")
        self.assertEqual(text_format["schema"], self.request.schema)

    def test_openai_uses_responses_json_schema(self) -> None:
        http_request = OpenAIAdapter().build_http_request(self.request, "secret")

        self.assertEqual(http_request.url, "https://api.openai.com/v1/responses")
        self.assertEqual(http_request.headers["Authorization"], "Bearer secret")
        output_format = http_request.body["text"]["format"]
        self.assertEqual(output_format["type"], "json_schema")
        self.assertTrue(output_format["strict"])
        self.assertEqual(output_format["schema"], self.request.schema)

    def test_anthropic_uses_messages_output_config(self) -> None:
        http_request = AnthropicAdapter().build_http_request(self.request, "secret")

        self.assertEqual(http_request.url, "https://api.anthropic.com/v1/messages")
        self.assertEqual(http_request.headers["x-api-key"], "secret")
        self.assertEqual(http_request.headers["anthropic-version"], "2023-06-01")
        output_format = http_request.body["output_config"]["format"]
        self.assertEqual(output_format["type"], "json_schema")
        self.assertEqual(output_format["schema"], self.request.schema)

    def test_openrouter_requires_structured_output_capable_routing(self) -> None:
        http_request = OpenRouterAdapter().build_http_request(self.request, "secret")

        self.assertEqual(
            http_request.url, "https://openrouter.ai/api/v1/chat/completions"
        )
        self.assertEqual(http_request.headers["Authorization"], "Bearer secret")
        output_format = http_request.body["response_format"]
        self.assertEqual(output_format["type"], "json_schema")
        self.assertTrue(output_format["json_schema"]["strict"])
        self.assertEqual(
            output_format["json_schema"]["schema"], self.request.schema
        )
        self.assertEqual(
            http_request.body["provider"], {"require_parameters": True}
        )

    def test_openrouter_can_pin_provider_and_reasoning_policy(self) -> None:
        request = RoutingRequest.create(
            model="anthropic/claude-sonnet-5-20260630",
            messages=MESSAGES,
            max_output_tokens=1024,
        )
        adapter = OpenRouterAdapter(
            provider_slug="anthropic",
            reasoning_effort="low",
        )

        http_request = adapter.build_http_request(request, "secret")

        self.assertEqual(http_request.body["max_tokens"], 1024)
        self.assertEqual(
            http_request.body["provider"],
            {
                "allow_fallbacks": False,
                "only": ["anthropic"],
                "require_parameters": True,
            },
        )
        self.assertEqual(
            http_request.body["reasoning"],
            {"effort": "low", "exclude": True},
        )
        self.assertEqual(
            adapter.execution_config(),
            {
                "openrouter_provider": "anthropic",
                "provider_fallbacks": False,
                "reasoning_effort": "low",
                "reasoning_excluded": True,
            },
        )

    def test_openrouter_rejects_invalid_policy_values(self) -> None:
        with self.assertRaises(ValueError):
            OpenRouterAdapter(provider_slug="Anthropic provider")
        with self.assertRaises(ValueError):
            OpenRouterAdapter(reasoning_effort="automatic")

    def test_all_adapters_extract_the_same_route_json(self) -> None:
        route = json.dumps(
            {"action": "human_support", "targets": ["safe_adult"]}
        )
        responses = (
            (
                GeminiAdapter(),
                {"candidates": [{"content": {"parts": [{"text": route}]}}]},
            ),
            (
                OpenAIAdapter(),
                {
                    "output": [
                        {
                            "type": "message",
                            "content": [{"type": "output_text", "text": route}],
                        }
                    ]
                },
            ),
            (
                AnthropicAdapter(),
                {"content": [{"type": "text", "text": route}]},
            ),
            (
                OpenRouterAdapter(),
                {
                    "choices": [
                        {
                            "finish_reason": "stop",
                            "message": {"role": "assistant", "content": route},
                        }
                    ]
                },
            ),
        )

        for adapter, response in responses:
            with self.subTest(provider=adapter.name):
                decision = parse_route(adapter.extract_text(response))
                self.assertEqual(decision.action, Action.HUMAN_SUPPORT)
                self.assertEqual(decision.targets, ("safe_adult",))

    def test_refusal_or_missing_text_is_not_coerced_to_a_route(self) -> None:
        with self.assertRaises(ProviderResponseError):
            OpenAIAdapter().extract_text(
                {
                    "output": [
                        {
                            "type": "message",
                            "content": [{"type": "refusal", "refusal": "No."}],
                        }
                    ]
                }
            )
        with self.assertRaises(ProviderResponseError):
            AnthropicAdapter().extract_text({"content": [], "stop_reason": "refusal"})
        with self.assertRaises(ProviderResponseError):
            OpenRouterAdapter().extract_text(
                {
                    "choices": [
                        {
                            "finish_reason": "content_filter",
                            "message": {"role": "assistant", "content": None},
                        }
                    ]
                }
            )

    def test_route_parser_rejects_extra_fields_and_unknown_targets(self) -> None:
        with self.assertRaises(ValueError):
            parse_route(
                json.dumps(
                    {
                        "action": "urgent_handoff",
                        "targets": ["police"],
                        "supportive_response": "You should...",
                    }
                )
            )


if __name__ == "__main__":
    unittest.main()
