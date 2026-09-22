"""Hybrid synthesis runner.

Deterministic extraction is always performed.  If `--llm` is enabled and a
reachable model is configured, a richer draft may be produced as an additional
PROPOSED candidate.  All outputs remain PROPOSED pending human Accept.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .config import EngineConfig
from .db import LivingStore, MessageRow
from .extract import CandidateExtract, DeterministicExtractor
from .llm_client import LLMClient


@dataclass(frozen=True)
class SynthesisResult:
    proposed_ids: list[str]
    deterministic_count: int
    llm_drafted: bool
    llm_error: str | None
    warnings: list[str]


class HybridSynthesisEngine:
    def __init__(self, store: LivingStore, config: EngineConfig):
        self.store = store
        self.config = config
        self.extractor = DeterministicExtractor(min_message_length=config.min_message_length)
        self.llm_client = LLMClient(config)

    def synthesize_conversation(self, external_id: str) -> SynthesisResult:
        conv = self.store.get_conversation_by_external_id(external_id)
        if conv is None:
            return SynthesisResult(
                proposed_ids=[],
                deterministic_count=0,
                llm_drafted=False,
                llm_error=None,
                warnings=[f"Conversation {external_id!r} not found."],
            )

        messages = self.store.get_messages(conv.id)
        if not messages:
            return SynthesisResult(
                proposed_ids=[],
                deterministic_count=0,
                llm_drafted=False,
                llm_error=None,
                warnings=[f"Conversation {external_id!r} has no messages."],
            )

        proposed_ids: list[str] = []
        warnings: list[str] = []

        # Deterministic path: always run.
        extracts = self.extractor.extract(messages)
        for extract in extracts:
            body = self._format_body(extract)
            provenance = self._format_provenance(conv, extract)
            if self.config.dry_run:
                proposed_ids.append(f"dry_run:{extract.kind}:{extract.label[:20]}")
            else:
                doc_id = self.store.insert_proposed_document(
                    title=extract.label,
                    body=body,
                    provenance=provenance,
                    source_message_ids=extract.source_message_ids,
                    engine="deterministic",
                )
                proposed_ids.append(doc_id)

        # Optional LLM path: only if enabled.
        llm_drafted = False
        llm_error: str | None = None
        if not self.config.deterministic_only:
            existing_titles = [d["title"] for d in self.store.list_working_documents()]
            draft = self.llm_client.draft_synthesis(messages, existing_titles)
            if draft.success:
                provenance = (
                    f"Synthesis drafted by optional LLM (model={self.config.llm_model}) "
                    f"from conversation {conv.external_id} ({conv.title or 'untitled'}). "
                    "All source turn IDs are linked via provenance_link."
                )
                if self.config.dry_run:
                    proposed_ids.append("dry_run:llm:draft")
                else:
                    doc_id = self.store.insert_proposed_document(
                        title=draft.title,
                        body=draft.body,
                        provenance=provenance,
                        source_message_ids=[m.id for m in messages],
                        engine="llm",
                    )
                    proposed_ids.append(doc_id)
                llm_drafted = True
            else:
                llm_error = draft.error
                warnings.append(f"LLM draft failed closed: {draft.error}")

        return SynthesisResult(
            proposed_ids=proposed_ids,
            deterministic_count=len(extracts),
            llm_drafted=llm_drafted,
            llm_error=llm_error,
            warnings=warnings,
        )

    def _format_body(self, extract: CandidateExtract) -> str:
        parts = [
            f"**Source:** {extract.source_text[:300]}{'...' if len(extract.source_text) > 300 else ''}",
            f"**Interpretation:** {extract.interpretation}",
            f"**Proposal ({extract.kind}):** {extract.label}",
        ]
        if extract.discussion_topic:
            parts.append(f"**Discussion topic:** {extract.discussion_topic}")
        parts.append(f"**Confidence:** {extract.confidence}")
        parts.append(
            "**Epistemic label:** This is a Working proposal, not accepted Codex content. "
            "Requires explicit human Accept to become WORKING."
        )
        return "\n\n".join(parts)

    def _format_provenance(self, conv: Any, extract: CandidateExtract) -> str:
        ids = ", ".join(extract.source_message_ids)
        return (
            f"Extracted deterministically from conversation {conv.external_id} "
            f"({conv.title or 'untitled'}). Source message IDs: {ids}."
        )
