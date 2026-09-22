"""Optional LLM draft assistant.

Uses an OpenAI-compatible chat-completions endpoint (default Ollama), with a
fallback to Ollama's native ``/api/chat``.  The LLM may only create/update
``proposal`` rows (status PROPOSED).

If the LLM is unavailable, the engine FAILS CLOSED: returns no proposals
rather than inventing empty success.  If the LLM returns substantial text that
cannot be parsed as JSON, the engine wraps that text as a PROPOSED body behind
an epistemic fence.

All prompts are fenced as Working synthesis / interpretation, never
unfenced essence or doctrine.
"""

from __future__ import annotations

import json
import os
import re
import urllib.error
import urllib.request
from dataclasses import dataclass

from .config import EngineConfig
from .db import MessageRow


@dataclass(frozen=True)
class LLMDraftResult:
    success: bool
    title: str = ""
    body: str = ""
    interpretation: str = ""
    discussion_topic: str = ""
    error: str = ""


class LLMClient:
    """OpenAI-compatible chat completion client with fail-closed behaviour."""

    def __init__(self, config: EngineConfig):
        self.config = config

    def draft_synthesis(
        self, messages: list[MessageRow], existing_titles: list[str] | None = None
    ) -> LLMDraftResult:
        """Ask the LLM for a single rich PROPOSED synthesis body."""
        if self.config.deterministic_only:
            return LLMDraftResult(
                success=False,
                error="LLM mode disabled (deterministic_only=True). Use --llm to enable.",
            )

        # Deterministic mock path for CI / smoke tests.
        if os.getenv("SOLBIAN_LLM_MOCK", "").lower() in ("1", "true", "yes"):
            return self._mock_draft(messages)

        prompt = self._build_prompt(messages, existing_titles or [])
        try:
            response = self._chat_completion(prompt)
        except urllib.error.URLError as exc:
            return LLMDraftResult(
                success=False,
                error=f"LLM endpoint unreachable ({self.config.llm_base}): {exc.reason}",
            )
        except Exception as exc:  # pragma: no cover - broad network/parsing safety
            return LLMDraftResult(success=False, error=f"LLM call failed: {exc}")

        parsed = self._parse_json_response(response)
        body = parsed.get("body", "")

        if len(body.strip()) < self.config.min_llm_body_chars:
            raw = response.strip()
            if len(raw) >= self.config.min_llm_body_chars:
                body = self._wrap_unparseable_text(raw)
                parsed["body"] = body
            else:
                return LLMDraftResult(
                    success=False,
                    error=(
                        f"LLM returned empty or too-short synthesis body "
                        f"({len(body.strip())} chars, minimum {self.config.min_llm_body_chars})."
                    ),
                )

        body = body[: self.config.max_llm_body_chars]
        return LLMDraftResult(
            success=True,
            title=parsed.get("title", "LLM-drafted synthesis"),
            body=body,
            interpretation=parsed.get(
                "interpretation",
                "Working interpretation drafted by optional LLM; requires human review.",
            ),
            discussion_topic=parsed.get("discussion_topic", ""),
        )

    def _build_prompt(
        self, messages: list[MessageRow], existing_titles: list[str]
    ) -> str:
        transcript = "\n\n".join(
            f"[{m.role}] {m.content.strip()}" for m in messages if m.content.strip()
        )
        existing = "\n".join(f"- {t}" for t in existing_titles) or "(none)"
        return (
            "You are an optional draft assistant for the Codex Solbian project.\n"
            "Your output must be a single JSON object. Do not include commentary outside the JSON object.\n"
            "You must propose content in a PROPOSED state only; you are not allowed to declare anything CANONICAL or accepted.\n"
            "Label your output as Working synthesis, not unfenced doctrine.\n"
            "Do not invent authority, polity, governance, or integrity boards.\n"
            "Preserve plurality; do not merge law or protocol catalogues.\n"
            "Return exactly ONE proposed synthesis document, not a list of dozens.\n"
            f"The body must be non-empty and substantial (minimum approximately {self.config.min_llm_body_chars} characters).\n"
            "If evidence is insufficient, produce a well-formed discussion_topic instead of a strong claim.\n\n"
            "Return JSON with these keys:\n"
            "  title: a short title for the proposed Codex document\n"
            "  body: 2-6 paragraphs of proposed synthesis, each tied to source turns, epistemically honest\n"
            "  interpretation: one-sentence note that this is a Working interpretation/proposal\n"
            "  discussion_topic: a prompt for a future JD↔Solace turn where the material is unresolved\n\n"
            f"Existing WORKING document titles:\n{existing}\n\n"
            f"Transcript (Journey, read-only source):\n{transcript}\n"
        )

    def _chat_completion(self, user_prompt: str) -> str:
        """Try OpenAI-compatible endpoint first, then Ollama native fallback."""
        try:
            return self._openai_chat_completion(user_prompt)
        except urllib.error.HTTPError as exc:
            if exc.code in (404, 405):
                return self._ollama_native_chat_completion(user_prompt)
            raise
        except urllib.error.URLError:
            # Endpoint may still expose /api/chat even if /v1 is absent.
            return self._ollama_native_chat_completion(user_prompt)

    def _openai_chat_completion(self, user_prompt: str) -> str:
        url = f"{self.config.llm_base.rstrip('/')}/chat/completions"
        payload = {
            "model": self.config.llm_model,
            "messages": [
                {
                    "role": "system",
                    "content": "You are a careful synthesis assistant. Always return valid JSON only.",
                },
                {"role": "user", "content": user_prompt},
            ],
            "temperature": 0.4,
            "max_tokens": 2048,
        }
        data = json.dumps(payload).encode()
        headers = {"Content-Type": "application/json"}
        if self.config.llm_api_key:
            headers["Authorization"] = f"Bearer {self.config.llm_api_key}"

        req = urllib.request.Request(url, data=data, headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=self.config.llm_timeout) as resp:
            result = json.loads(resp.read().decode())

        return self._extract_content(result)

    def _ollama_native_chat_completion(self, user_prompt: str) -> str:
        url = f"{self.config.llm_base.rstrip('/')}/api/chat"
        payload = {
            "model": self.config.llm_model,
            "messages": [
                {
                    "role": "system",
                    "content": "You are a careful synthesis assistant. Always return valid JSON only.",
                },
                {"role": "user", "content": user_prompt},
            ],
            "stream": False,
            "options": {"temperature": 0.4},
        }
        data = json.dumps(payload).encode()
        headers = {"Content-Type": "application/json"}
        if self.config.llm_api_key:
            headers["Authorization"] = f"Bearer {self.config.llm_api_key}"

        req = urllib.request.Request(url, data=data, headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=self.config.llm_timeout) as resp:
            result = json.loads(resp.read().decode())

        return self._extract_content(result)

    @staticmethod
    def _extract_content(result: dict) -> str:
        """Extract assistant content from either OpenAI or Ollama-native response shape."""
        if "message" in result and isinstance(result["message"], dict):
            return str(result["message"].get("content", "")).strip()
        choices = result.get("choices", [])
        if choices and isinstance(choices[0], dict):
            msg = choices[0].get("message", {})
            return str(msg.get("content", "")).strip()
        return str(result.get("content", "")).strip()

    def _parse_json_response(self, text: str) -> dict:
        text = self._strip_markdown_fences(text)
        data: dict | None = None
        try:
            data = json.loads(text)
        except json.JSONDecodeError:
            # Try to extract the first JSON object if extra text leaked in.
            start = text.find("{")
            end = text.rfind("}")
            if start != -1 and end != -1 and end > start:
                try:
                    data = json.loads(text[start : end + 1])
                except json.JSONDecodeError:
                    data = None
        if not isinstance(data, dict):
            return {}

        # Flatten a nested "synthesis" wrapper.
        if "synthesis" in data and isinstance(data["synthesis"], dict):
            nested = data.pop("synthesis")
            for key, value in nested.items():
                data.setdefault(key, value)

        # Accept common aliases for the body key.
        body = (
            data.get("body")
            or data.get("content")
            or data.get("text")
            or data.get("synthesis")
        )
        if body is not None:
            data["body"] = str(body)

        return data

    @staticmethod
    def _strip_markdown_fences(text: str) -> str:
        text = text.strip()
        if text.startswith("```json"):
            text = text[7:]
        elif text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
        return text.strip()

    def _wrap_unparseable_text(self, text: str) -> str:
        text = self._strip_markdown_fences(text)
        text = re.sub(r"\n{3,}", "\n\n", text)
        return (
            "**LLM raw-text fallback (PROPOSED only):**\n\n"
            f"{text[:self.config.max_llm_body_chars]}\n\n"
            "**Epistemic fence:** This body was produced by the optional LLM in a format "
            "the engine could not parse as the expected JSON object. It has been wrapped "
            "as a PROPOSED candidate and must be reviewed before any Accept step."
        )

    def _mock_draft(self, messages: list[MessageRow]) -> LLMDraftResult:
        """Deterministic mock draft for smoke tests."""
        transcript = "\n\n".join(
            f"[{m.role}] {m.content.strip()}" for m in messages if m.content.strip()
        )
        body = (
            "**Mock LLM draft (PROPOSED only)**\n\n"
            "This is a deterministic stand-in for an optional LLM synthesis. It exists to "
            "verify that the hybrid engine can produce a single, non-empty, hybrid:llm "
            "PROPOSED document when the LLM path is enabled.\n\n"
            "**Interpretation:** Working interpretation produced by mock LLM client; requires human review.\n\n"
            f"**Source turn summary:** {transcript[:800]}{'...' if len(transcript) > 800 else ''}\n\n"
            "**Discussion topic:** What should the real LLM draft emphasize once the endpoint is reachable?"
        )
        return LLMDraftResult(
            success=True,
            title="Mock LLM-drafted synthesis",
            body=body,
            interpretation="Working interpretation produced by mock LLM client; requires human review.",
            discussion_topic="What should the real LLM draft emphasize once the endpoint is reachable?",
        )
