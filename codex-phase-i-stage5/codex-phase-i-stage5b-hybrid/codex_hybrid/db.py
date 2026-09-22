"""Living-store database helpers (dual schema).

Supports:
1) Fixture schema used by smoke_hybrid.py (content / external_id / simplified tables)
2) Phase I Stage 3–7 living store (body / conversation.id / proposal + provenance_link)

Never writes CANONICAL.
"""

from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from .config import EngineConfig


@dataclass(frozen=True)
class MessageRow:
    id: str
    role: str
    content: str
    created_at: str | None = None


@dataclass(frozen=True)
class ConversationRow:
    id: str
    external_id: str
    title: str | None


class LivingStore:
    """Minimal wrapper around a SQLite living store."""

    def __init__(self, db_path: str | Path):
        self.db_path = Path(db_path)
        self._con: sqlite3.Connection | None = None
        self._mode: str | None = None  # "fixture" | "phase_i"
        self._safety_warnings: list[str] = []

    def connect(self) -> "LivingStore":
        self._con = sqlite3.connect(str(self.db_path), check_same_thread=False)
        self._con.row_factory = sqlite3.Row
        self._mode = self._detect_mode()
        self._safety_warnings = self._check_safety()
        return self

    def close(self) -> None:
        if self._con:
            self._con.close()
            self._con = None

    def __enter__(self) -> "LivingStore":
        return self.connect()

    def __exit__(self, exc_type: Any, exc: Any, tb: Any) -> None:
        self.close()

    @property
    def safety_warnings(self) -> list[str]:
        return list(self._safety_warnings)

    def _detect_mode(self) -> str:
        cols = {r[1] for r in self._con.execute("PRAGMA table_info(message)")}
        if "body" in cols:
            return "phase_i"
        return "fixture"

    def _columns(self, table: str) -> set[str]:
        return {r[1] for r in self._con.execute(f"PRAGMA table_info({table})")}

    def _list_tables(self) -> set[str]:
        return {
            r[0]
            for r in self._con.execute("SELECT name FROM sqlite_master WHERE type='table'")
        }

    @staticmethod
    def is_historical_corpus(db_path: str | Path) -> bool:
        """Return True if the path is inside the historical read-only corpus tree.

        Uses exact Path.relative_to matching so ``codex-phase-i-*`` paths are
        not false-positives for ``.../solbian/codex``.
        """
        path = Path(db_path).resolve()
        for root in EngineConfig.historical_corpus_roots():
            try:
                root = root.resolve()
            except FileNotFoundError:
                root = root
            try:
                path.relative_to(root)
                return True
            except ValueError:
                continue
        return False

    def looks_like_stage3_sot(self) -> bool:
        """Return True if the connected DB resembles a Stage 3 SoT read-only corpus."""
        if self._con is None:
            raise RuntimeError("not connected")
        tables = self._list_tables()
        has_codex_document = "codex_document" in tables
        has_proposal = "proposal" in tables
        has_revision = "revision" in tables
        has_conversation = "conversation" in tables
        has_message = "message" in tables
        if has_codex_document and not (has_proposal or has_revision):
            # Fixture mode also has conversation/message; a true Stage-3 SoT lacks
            # both the living-loop tables and the proposal/revision machinery.
            if not (has_conversation and has_message):
                return True
        return False

    def _check_safety(self) -> list[str]:
        warnings: list[str] = []
        if self.looks_like_stage3_sot():
            warnings.append(
                "Database looks like a Stage 3 SoT read-only corpus. "
                "Writes should target the Stage 4/7 living store, not the historical corpus."
            )
        return warnings

    def _write_guard(self) -> None:
        """Refuse to write the historical corpus; Stage-3 SoT is warn-only."""
        if self.is_historical_corpus(self.db_path):
            raise RuntimeError(
                f"Refusing to write historical corpus: {self.db_path}. "
                "Target the Stage 4/7 living store instead."
            )
        # Stage-3 SoT resemblance is advisory only (printed at connect).

    def get_conversation_by_external_id(self, external_id: str) -> ConversationRow | None:
        cols = self._columns("conversation")
        if "external_id" in cols:
            cur = self._con.execute(
                "SELECT id, external_id, title FROM conversation WHERE external_id = ?",
                (external_id,),
            )
            row = cur.fetchone()
            if row is None:
                return None
            return ConversationRow(id=row["id"], external_id=row["external_id"], title=row["title"])
        # Phase I: conversation.id IS the public conversation id
        cur = self._con.execute(
            "SELECT id, title FROM conversation WHERE id = ?",
            (external_id,),
        )
        row = cur.fetchone()
        if row is None:
            return None
        return ConversationRow(id=row["id"], external_id=row["id"], title=row["title"])

    def get_messages(self, conversation_id: str) -> list[MessageRow]:
        cols = self._columns("message")
        if "body" in cols:
            cur = self._con.execute(
                "SELECT id, role, body AS content, created_at FROM message "
                "WHERE conversation_id = ? ORDER BY seq, created_at, id",
                (conversation_id,),
            )
        else:
            cur = self._con.execute(
                "SELECT id, role, content, created_at FROM message "
                "WHERE conversation_id = ? ORDER BY created_at, id",
                (conversation_id,),
            )
        return [
            MessageRow(
                id=row["id"],
                role=row["role"],
                content=(row["content"] or ""),
                created_at=row["created_at"],
            )
            for row in cur.fetchall()
        ]

    def list_working_documents(self) -> list[dict[str, Any]]:
        if self._mode == "phase_i":
            # Prefer WORKING codex_document; also surface accepted proposals
            cur = self._con.execute(
                "SELECT id, title, body, status FROM codex_document WHERE status = 'WORKING'"
            )
            return [dict(row) for row in cur.fetchall()]
        cur = self._con.execute(
            "SELECT id, title, body, status, attribution FROM codex_document WHERE status = 'WORKING'"
        )
        return [dict(row) for row in cur.fetchall()]

    def list_proposed_documents(
        self,
        hybrid_only: bool = True,
        include_themes: bool = False,
        limit: int | None = None,
        verbose: bool = False,
    ) -> list[dict[str, Any]]:
        """List PROPOSED rows.

        Defaults are intentionally quiet:
          * Only rows whose attribution looks like ``hybrid:*`` (or equivalent) are shown.
          * ``Theme:*`` titles are suppressed unless ``include_themes`` or ``verbose``.
          * Newest first.
        """
        cap = -1 if limit is None or verbose else limit
        if self._mode == "phase_i":
            cur = self._con.execute(
                """
                SELECT id, summary AS title, body, status, attribution AS provenance,
                       attribution, created_at
                FROM proposal
                WHERE status = 'PROPOSED'
                  AND (? = 0 OR attribution LIKE 'hybrid:%')
                  AND (? = 1 OR summary NOT LIKE 'Theme:%')
                ORDER BY created_at DESC
                LIMIT ?
                """,
                (1 if hybrid_only else 0, 1 if include_themes else 0, cap),
            )
            rows = [dict(row) for row in cur.fetchall()]
            for r in rows:
                r.setdefault("engine", None)
            return rows

        # Fixture mode: prefer attribution, fall back to engine for hybrid detection.
        has_attr = "attribution" in self._columns("codex_document")
        hybrid_expr = (
            "attribution LIKE 'hybrid:%'" if has_attr else "engine IN ('deterministic', 'llm')"
        )
        cur = self._con.execute(
            f"""
            SELECT id, title, body, status, engine, provenance, attribution, created_at
            FROM codex_document
            WHERE status = 'PROPOSED'
              AND (? = 0 OR {hybrid_expr})
              AND (? = 1 OR title NOT LIKE 'Theme:%')
            ORDER BY created_at DESC
            LIMIT ?
            """,
            (1 if hybrid_only else 0, 1 if include_themes else 0, cap),
        )
        return [dict(row) for row in cur.fetchall()]

    def count_proposed(
        self,
        hybrid_only: bool = True,
        include_themes: bool = False,
    ) -> int:
        """Return the number of rows matching the same default filters."""
        if self._mode == "phase_i":
            cur = self._con.execute(
                """
                SELECT COUNT(*) AS n
                FROM proposal
                WHERE status = 'PROPOSED'
                  AND (? = 0 OR attribution LIKE 'hybrid:%')
                  AND (? = 1 OR summary NOT LIKE 'Theme:%')
                """,
                (1 if hybrid_only else 0, 1 if include_themes else 0),
            )
        else:
            has_attr = "attribution" in self._columns("codex_document")
            hybrid_expr = (
                "attribution LIKE 'hybrid:%'" if has_attr else "engine IN ('deterministic', 'llm')"
            )
            cur = self._con.execute(
                f"""
                SELECT COUNT(*) AS n
                FROM codex_document
                WHERE status = 'PROPOSED'
                  AND (? = 0 OR {hybrid_expr})
                  AND (? = 1 OR title NOT LIKE 'Theme:%')
                """,
                (1 if hybrid_only else 0, 1 if include_themes else 0),
            )
        return cur.fetchone()["n"]

    def insert_proposed_document(
        self,
        title: str,
        body: str,
        provenance: str,
        source_message_ids: Iterable[str],
        engine: str = "deterministic",
    ) -> str:
        """Write a PROPOSED row + provenance links. Returns id."""
        self._write_guard()
        now = self._now()
        msg_ids = list(set(source_message_ids))
        attr = f"hybrid:{engine}"
        if self._mode == "phase_i":
            prop_id = self._generate_id("prop")
            based = json.dumps({"message_ids": msg_ids, "engine": engine, "note": provenance})
            self._con.execute(
                """
                INSERT INTO proposal (id, summary, body, based_on_json, status, attribution, created_at, updated_at)
                VALUES (?, ?, ?, ?, 'PROPOSED', ?, ?, ?)
                """,
                (prop_id, title[:500], body, based, attr, now, now),
            )
            for msg_id in msg_ids:
                self._con.execute(
                    """
                    INSERT INTO provenance_link
                      (id, subject_kind, subject_id, source_kind, source_id, note, confidence, status, created_at, updated_at)
                    VALUES (?, 'proposal', ?, 'message', ?, ?, 'SYNTHESIS', 'PROPOSED', ?, ?)
                    """,
                    (self._generate_id("plink"), prop_id, msg_id, provenance[:400], now, now),
                )
            self._con.commit()
            return prop_id

        doc_id = self._generate_id("doc")
        self._con.execute(
            """
            INSERT INTO codex_document (id, title, body, status, provenance, engine, attribution, created_at, updated_at)
            VALUES (?, ?, ?, 'PROPOSED', ?, ?, ?, ?, ?)
            """,
            (doc_id, title, body, provenance, engine, attr, now, now),
        )
        for msg_id in msg_ids:
            self._con.execute(
                """
                INSERT INTO provenance_link (id, document_id, source_type, source_id, source_role, created_at)
                VALUES (?, ?, 'message', ?, 'source', ?)
                """,
                (self._generate_id("link"), doc_id, msg_id, now),
            )
        self._con.commit()
        return doc_id

    def accept_document(self, doc_id: str) -> None:
        """Explicit human Accept: PROPOSED -> WORKING (fixture or Phase I)."""
        self._write_guard()
        now = self._now()
        if self._mode == "phase_i":
            # Accept proposal -> WORKING codex_document + revision + provenance copy
            prop = self._con.execute(
                "SELECT id, summary, body, status FROM proposal WHERE id = ?", (doc_id,)
            ).fetchone()
            if prop is None:
                raise ValueError(f"proposal not found: {doc_id}")
            if prop["status"] != "PROPOSED":
                # idempotent if already accepted
                return
            doc_new = self._generate_id("cdoc")
            self._con.execute(
                """
                INSERT INTO codex_document
                  (id, kind, title, body, source_document_id, status, version, attribution, created_at, updated_at)
                VALUES (?, 'section', ?, ?, NULL, 'WORKING', 1, 'hybrid:accept', ?, ?)
                """,
                (doc_new, prop["summary"], prop["body"], now, now),
            )
            rev_id = self._generate_id("rev")
            self._con.execute(
                """
                INSERT INTO revision
                  (id, target_kind, target_id, proposal_id, prev_version, next_version, diff_summary, status, reversible, created_at, updated_at)
                VALUES (?, 'codex_document', ?, ?, NULL, 1, 'hybrid Accept PROPOSED->WORKING', 'REVISION', 1, ?, ?)
                """,
                (rev_id, doc_new, doc_id, now, now),
            )
            # copy provenance onto document and revision
            links = self._con.execute(
                "SELECT source_kind, source_id, note, confidence FROM provenance_link WHERE subject_kind='proposal' AND subject_id=?",
                (doc_id,),
            ).fetchall()
            for lk in links:
                for subject_kind, subject_id in (("codex_document", doc_new), ("revision", rev_id)):
                    self._con.execute(
                        """
                        INSERT INTO provenance_link
                          (id, subject_kind, subject_id, source_kind, source_id, note, confidence, status, created_at, updated_at)
                        VALUES (?, ?, ?, ?, ?, ?, ?, 'WORKING', ?, ?)
                        """,
                        (
                            self._generate_id("plink"),
                            subject_kind,
                            subject_id,
                            lk["source_kind"],
                            lk["source_id"],
                            lk["note"],
                            lk["confidence"] or "SYNTHESIS",
                            now,
                            now,
                        ),
                    )
            self._con.execute(
                "UPDATE proposal SET status='WORKING', updated_at=? WHERE id=?",
                (now, doc_id),
            )
            self._con.commit()
            return

        self._con.execute(
            "UPDATE codex_document SET status = 'WORKING', updated_at = ? WHERE id = ? AND status = 'PROPOSED'",
            (now, doc_id),
        )
        self._con.commit()

    def ensure_core_schema(self) -> None:
        """Create the minimal fixture tables assumed by smoke tests."""
        self._con.executescript(
            """
            CREATE TABLE IF NOT EXISTS conversation (
                id TEXT PRIMARY KEY,
                external_id TEXT UNIQUE,
                title TEXT,
                created_at TEXT
            );
            CREATE TABLE IF NOT EXISTS message (
                id TEXT PRIMARY KEY,
                conversation_id TEXT NOT NULL,
                role TEXT,
                content TEXT,
                created_at TEXT
            );
            CREATE INDEX IF NOT EXISTS idx_message_conversation ON message(conversation_id);
            CREATE TABLE IF NOT EXISTS codex_document (
                id TEXT PRIMARY KEY,
                title TEXT,
                body TEXT,
                status TEXT,
                provenance TEXT,
                engine TEXT,
                attribution TEXT,
                created_at TEXT,
                updated_at TEXT
            );
            CREATE INDEX IF NOT EXISTS idx_doc_status ON codex_document(status);
            CREATE TABLE IF NOT EXISTS provenance_link (
                id TEXT PRIMARY KEY,
                document_id TEXT NOT NULL,
                source_type TEXT,
                source_id TEXT,
                source_role TEXT,
                created_at TEXT
            );
            CREATE INDEX IF NOT EXISTS idx_link_doc ON provenance_link(document_id);
            """
        )
        self._con.commit()
        self._mode = "fixture"

    def load_fixture_conversation(
        self, external_id: str, title: str, messages: list[tuple[str, str, str]]
    ) -> None:
        """Insert a fixture conversation for smoke tests."""
        conv_id = self._generate_id("conv")
        now = self._now()
        self._con.execute(
            "INSERT INTO conversation (id, external_id, title, created_at) VALUES (?, ?, ?, ?)",
            (conv_id, external_id, title, now),
        )
        for role, content, ts in messages:
            msg_id = self._generate_id("msg")
            self._con.execute(
                "INSERT INTO message (id, conversation_id, role, content, created_at) VALUES (?, ?, ?, ?, ?)",
                (msg_id, conv_id, role, content, ts),
            )
        self._con.commit()

    @staticmethod
    def _generate_id(prefix: str) -> str:
        return f"{prefix}_{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S%f')}"

    @staticmethod
    def _now() -> str:
        return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
