"""Deterministic extraction of candidate synthesis from a Journey.

Each candidate carries epistemic tags:
  SOURCE        - verbatim turn text
  INTERPRETATION - what the engine thinks this turn expresses
  PROPOSAL       - a candidate codex body in PROPOSED state
  DISCUSSION_TOPIC - a prompt for a future JD↔Solace turn

No candidate is auto-accepted.  Status stays PROPOSED.
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from typing import Iterable

from .db import MessageRow


@dataclass(frozen=True)
class CandidateExtract:
    kind: str  # claim, question, principle, concept, discussion_topic
    label: str
    source_text: str
    source_message_ids: tuple[str, ...]
    interpretation: str
    discussion_topic: str | None = None
    confidence: str = "low"  # low | medium | high


class DeterministicExtractor:
    """Rule/heuristic extractor tuned for Solace philosophical dialogue."""

    def __init__(self, min_message_length: int = 10):
        self.min_message_length = min_message_length

    def extract(self, messages: list[MessageRow]) -> list[CandidateExtract]:
        candidates: list[CandidateExtract] = []
        for i, msg in enumerate(messages):
            if len(msg.content.strip()) < self.min_message_length:
                continue
            candidates.extend(self._extract_from_message(messages, msg, i))
        candidates = self._deduplicate(candidates)
        return candidates

    def _extract_from_message(self, messages: list[MessageRow], msg: MessageRow, index: int) -> list[CandidateExtract]:
        text = msg.content.strip()
        out: list[CandidateExtract] = []

        # Skip very short or purely affirmative turns.
        if len(text) < 30:
            return out

        # Questions that seem durable.
        if "?" in text:
            q = self._first_sentence(text)
            if self._looks_durable_question(q):
                out.append(
                    CandidateExtract(
                        kind="question",
                        label=self._short_label(q, 60),
                        source_text=q,
                        source_message_ids=(msg.id,),
                        interpretation="A durable question surfaced in dialogue that may deserve a Codex discussion topic or eventual answer.",
                        discussion_topic=f"Return to this question in a future JD↔Solace turn: {q}",
                        confidence="medium",
                    )
                )

        # Definition / concept markers.
        if re.search(r"\bis\b.*\b(a kind of|the|an?|defined as|means)\b", text, re.I):
            label = self._extract_definition_label(text)
            if label and not self._label_is_junk(label):
                out.append(
                    CandidateExtract(
                        kind="concept",
                        label=label,
                        source_text=text,
                        source_message_ids=(msg.id,),
                        interpretation="A possible concept or working definition that could be clarified in Codex.",
                        discussion_topic="Is this definition stable enough to record, or does it need refinement?",
                        confidence="low",
                    )
                )

        # Principle / claim markers.
        if re.search(r"\b(we (should|must|can|need to)|it is (important|necessary)|our (goal|aim|purpose)|the (point|reason|purpose)|I believe|we believe)\b", text, re.I):
            claim = self._first_sentence(text)
            if len(claim) > 30:
                out.append(
                    CandidateExtract(
                        kind="claim",
                        label=self._short_label(claim, 70),
                        source_text=claim,
                        source_message_ids=(msg.id,),
                        interpretation="A normative claim or working principle that could become a PROPOSED Codex entry.",
                        discussion_topic="Does this claim hold across the project's working fences?",
                        confidence="low",
                    )
                )

        # Theme / repetition candidates (repeated 2+ word phrases across this and next message).
        next_msg = messages[index + 1] if index + 1 < len(messages) else None
        themes = self._shared_themes(text, next_msg.content if next_msg else "")
        for theme in themes:
            if not self._theme_is_junk(theme):
                out.append(
                    CandidateExtract(
                        kind="theme",
                        label=f"Theme: {theme}",
                        source_text=text,
                        source_message_ids=(msg.id,) + ((next_msg.id,) if next_msg else ()),
                        interpretation=f"The theme '{theme}' appears in adjacent turns and may link multiple turns in a synthesis.",
                        discussion_topic=f"Should '{theme}' be tracked as a recurring Codex theme?",
                        confidence="low",
                    )
                )

        return out

    def _looks_durable_question(self, q: str) -> bool:
        q = q.lower()
        durable_stems = [
            "who are we", "what are we", "what is", "why do we", "how do we",
            "what does it mean", "what is the", "should we", "could we",
            "what would", "where do we",
        ]
        return any(stem in q for stem in durable_stems)

    def _first_sentence(self, text: str) -> str:
        # Naive first sentence split on . ? !, capped at 200 chars.
        m = re.split(r"(?<=[.?!])\s+", text.strip(), maxsplit=1)
        sent = m[0] if m else text
        return sent[:200].strip()

    def _short_label(self, text: str, max_len: int = 60) -> str:
        cleaned = re.sub(r"\s+", " ", text.strip()).replace("\n", " ")
        if len(cleaned) <= max_len:
            return cleaned
        return cleaned[: max_len - 3].rstrip() + "..."

    def _extract_definition_label(self, text: str) -> str | None:
        m = re.search(r"([A-Z][a-zA-Z\s]{2,25})(?:\s+(?:is|are|means|refer))", text)
        if m:
            return f"Concept: {m.group(1).strip()}"
        m = re.search(r"\b([a-z]+(?:\s+[a-z]+){0,4})\s+is\s+(?:a|the|an)\b", text, re.I)
        if m:
            return f"Concept: {m.group(1).strip()}"
        return None

    def _shared_themes(self, a: str, b: str) -> list[str]:
        a_words = set(re.findall(r"[a-zA-Z]{4,}", a.lower()))
        b_words = set(re.findall(r"[a-zA-Z]{4,}", b.lower()))
        # Filter out very common words.
        stop = {
            "this", "that", "with", "from", "have", "been", "were", "they",
            "about", "would", "there", "their", "what", "when", "where",
            "which", "while", "those", "these", "because", "something",
        }
        shared = (a_words & b_words) - stop
        return sorted(shared)[:3]

    def _label_is_junk(self, label: str) -> bool:
        # Reject concept labels that are just sentence starters or pronouns.
        junk = {
            "so", "that", "this", "it", "there", "then", "and", "but", "or",
            "a possible answer", "a good", "the fact", "what",
        }
        lower = label.lower().replace("concept: ", "")
        return any(lower.startswith(j) for j in junk) or len(lower.split()) > 6

    def _theme_is_junk(self, theme: str) -> bool:
        stop_themes = {
            "that", "this", "there", "then", "they", "them", "agreed", "every",
            "claim", "turn", "source", "something", "anything", "someone",
            "because", "would", "could", "should", "about", "think", "people",
        }
        return theme.lower() in stop_themes

    def _deduplicate(self, candidates: list[CandidateExtract]) -> list[CandidateExtract]:
        seen: set[str] = set()
        out: list[CandidateExtract] = []
        for c in candidates:
            key = hashlib.sha256(
                (c.kind + "|" + c.label + "|" + "|".join(c.source_message_ids)).encode()
            ).hexdigest()[:16]
            if key not in seen:
                seen.add(key)
                out.append(c)
        return out
