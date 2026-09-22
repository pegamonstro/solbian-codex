#!/usr/bin/env python3
"""Codex Solbian Phase I — Stage 4/7 two-surface prototype server + living loop.

Three surfaces over **one living SQLite store** (Python stdlib only; no
frameworks):

* **Solace**  — list / create conversations and append messages.  Appending a
  message also runs the Stage 5 *durable* analyzer against the living store, so
  new PROPOSED proposals appear without a separate command.
* **Codex Solbian** — browse ``source_document`` (HISTORICAL, read-only) *and*
  the consolidated ``codex_document`` rows (WORKING, read-only here).  Optional
  read-only text preview of files under a registered corpus root.
* **Engine** — inspect PROPOSED proposals and their provenance, **Run living
  loop** (runs the Stage 5 engine against the living store, in place), and
  **Accept → WORKING** for a single PROPOSED proposal (controlled
  consolidation).  A dry-run button is kept for compatibility.  The Solace
  conversation view also offers **Synthesize dialogue** (Stage 5b hybrid
  deterministic path, the default) and **Draft with LLM** (explicit confirm;
  fails closed), both of which only ever create PROPOSED candidates.

Living store (Stage 7)
----------------------
The living store is ``data/codex_phase_i.sqlite`` in this directory (Stage 4),
i.e. the working copy of the Stage 3 source-of-truth store.  The Stage 5 engine
tables are seeded into it **once** (``living_store.migrate``) and Stage 5 is
never written again.  ``living_store.py`` implements the policy + consolidation.

Consolidation rules
-------------------
* ``proposal`` (PROPOSED) -> ``codex_document`` status **WORKING**
  + ``revision`` (``proposal_id`` set) + copied ``provenance_link`` rows.
* The accepted ``proposal`` is marked ``WORKING`` ("accepted-into-working").
* ``CANONICAL`` is not representable and is never offered or emitted.
* Consolidation needs an explicit API/UI action — nothing auto-accepts.

Safety
------
* ``source_document`` is never inserted, updated or deleted by this server.
* The historical corpus ``/Users/archcore/solbian/codex`` is only ever opened
  read-only, and only for a capped text preview (200 KB) of a regular file that
  resolves inside a registered corpus root.
* Read-only browse surfaces open SQLite with ``mode=ro``.  The only writers are
  Solace append, the explicit engine run, and explicit consolidation.

Run
---
    python3 app.py                 # -> http://127.0.0.1:8787
    python3 app.py --port 9000
    python3 app.py --db /path/to/codex_phase_i.sqlite
    python3 app.py --engine-db /path/to/living.sqlite   # defaults to --db
"""

from __future__ import annotations

import argparse
import hashlib
import json
import mimetypes
import os
import pathlib
import re
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import uuid
from contextlib import closing
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, unquote, urlparse

# Stage 7 living-store core.  After `apply_to_stage4.sh` it lives next to this
# file; while staging it lives in the Stage 7 directory.
try:
    import living_store
except ImportError:  # pragma: no cover - staging fallback
    sys.path.insert(0, os.environ.get(
        "SOLBIAN_STAGE7_DIR", "/Users/archcore/solbian/codex-phase-i-stage7"))
    import living_store

HERE = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(HERE, "static")
DEFAULT_DB = os.path.join(HERE, "data", "codex_phase_i.sqlite")
STAGE3_DB = "/Users/archcore/solbian/codex-phase-i-stage3/codex_phase_i.sqlite"
DEFAULT_INVENTORY = os.path.join(HERE, "baseline_inventory_full.json")

# Stage 5 engine CLI (read-only): used by the living loop and the dry-run.
STAGE5_DIR = "/Users/archcore/solbian/codex-phase-i-stage5"
# The living store IS the engine store now: default the engine surface to it.
DEFAULT_ENGINE_DB = os.environ.get(
    "SOLBIAN_LIVING_DB", os.environ.get("SOLBIAN_ENGINE_DB", DEFAULT_DB))
DEFAULT_ENGINE_PY = os.environ.get(
    "SOLBIAN_ENGINE_PY", os.path.join(STAGE5_DIR, "engine.py"))
ENGINE_TIMEOUT = 240

# Stage 5b hybrid synthesis engine: explicit deterministic (default) or optional
# LLM dialogue synthesis into PROPOSED candidates.  Never auto-Accepts.
HYBRID_DIR = "/Users/archcore/solbian/codex-phase-i-stage5/codex-phase-i-stage5b-hybrid"
DEFAULT_HYBRID_PY = os.environ.get(
    "SOLBIAN_HYBRID_PY", os.path.join(HYBRID_DIR, "engine.py"))
HYBRID_TIMEOUT = 240

# Engine kinds the "Run living loop" button runs.  The Solace append path runs
# only the fast `durable` analyzer.
LIVING_LOOP_KINDS = ("plurality", "duplicates", "underdeveloped", "durable",
                     "discussion")
SOLACE_KINDS = ("durable",)

PREVIEW_CAP = 200 * 1024  # 200 KB
MAX_BODY = 1 * 1024 * 1024
MAX_MESSAGE_LEN = 100_000

# Text surfaces we are willing to preview (read-only). Anything else is metadata-only.
TEXT_EXTS = {
    ".md", ".markdown", ".txt", ".text", ".json", ".ndjson", ".jsonl", ".sum",
    ".sref", ".csv", ".tsv", ".log", ".py", ".js", ".mjs", ".css", ".html",
    ".htm", ".sh", ".bash", ".yml", ".yaml", ".toml", ".ini", ".cfg", ".conf",
    ".xml", ".rst", ".c", ".h", ".cpp", ".go", ".rs", ".sql", ".gitignore",
}

CONTENT_STATUS = ("SOURCE", "HISTORICAL", "WORKING", "PROPOSED", "REVISION",
                  "RELATED", "UNKNOWN")

_DOC_ROUTE = re.compile(r"^/api/codex/documents/([A-Za-z0-9_\-]+)$")
_CODEX_DOC_ROUTE = re.compile(r"^/api/codex/codex-documents/([A-Za-z0-9_\-]+)$")
_CONV_ROUTE = re.compile(r"^/api/solace/conversations/([A-Za-z0-9_\-]+)$")
_MSG_ROUTE = re.compile(r"^/api/solace/conversations/([A-Za-z0-9_\-]+)/messages$")
_ENGINE_PROP_ROUTE = re.compile(r"^/api/engine/proposals/([A-Za-z0-9_\-]+)$")
_ENGINE_ACCEPT_ROUTE = re.compile(r"^/api/engine/proposals/([A-Za-z0-9_\-]+)/accept$")
# Route-safe conversation id used by the explicit hybrid synthesize endpoint.
_CONV_ID_RE = re.compile(r"^[A-Za-z0-9_\-]{1,128}$")


def _as_bool(value) -> bool:
    """Coerce JSON/query-ish truthy values without surprising ``"false"``."""
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in ("1", "true", "yes", "on")
    return bool(value)


def _query_flag(query, name: str) -> bool:
    return _as_bool((query.get(name) or [""])[0])


def now_iso() -> str:
    import datetime as _dt
    return _dt.datetime.now(_dt.timezone.utc).replace(microsecond=0).isoformat()


def connect(db_path: str):
    """Open a short-lived connection. Use as ``with open_db(path) as conn:``."""
    conn = sqlite3.connect(db_path, timeout=15)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return closing(conn)


def connect_ro(db_path: str):
    """Open a short-lived READ-ONLY connection (never creates or writes the file)."""
    uri = pathlib.Path(db_path).resolve().as_uri() + "?mode=ro"
    conn = sqlite3.connect(uri, uri=True, timeout=15)
    conn.row_factory = sqlite3.Row
    return closing(conn)


def rows_to_dicts(rows) -> list[dict]:
    return [dict(r) for r in rows]


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


# ---------------------------------------------------------------------------
# Codex (read-only) queries
# ---------------------------------------------------------------------------
def codex_filters(query: dict) -> tuple[str, list]:
    where, params = [], []
    q = (query.get("q") or [""])[0].strip()
    if q:
        like = f"%{q}%"
        where.append("(sd.rel_path LIKE ? OR sd.probable_role LIKE ? OR sd.notes LIKE ?)")
        params += [like, like, like]
    for field, column in (("status", "sd.status"), ("role", "sd.probable_role"),
                          ("media", "sd.media_type"), ("root", "sd.corpus_root_id")):
        val = (query.get(field) or [""])[0].strip()
        if val:
            where.append(f"{column} = ?")
            params.append(val)
    sql = (" WHERE " + " AND ".join(where)) if where else ""
    return sql, params


def list_documents(conn, query) -> dict:
    limit = max(1, min(500, int((query.get("limit") or ["50"])[0] or 50)))
    offset = max(0, int((query.get("offset") or ["0"])[0] or 0))
    where_sql, params = codex_filters(query)
    total = conn.execute(
        f"SELECT COUNT(*) FROM source_document sd{where_sql}", params
    ).fetchone()[0]
    rows = conn.execute(
        f"""SELECT sd.id, sd.corpus_root_id, sd.rel_path, sd.media_type, sd.byte_size,
                   sd.mtime, sd.sha256, sd.probable_role, sd.inventory_status,
                   sd.status, sd.plurality_flags, sd.notes, sd.attribution,
                   sd.created_at, sd.updated_at,
                   cr.path AS corpus_root_path, cr.classification AS corpus_classification
            FROM source_document sd
            JOIN corpus_root cr ON cr.id = sd.corpus_root_id
            {where_sql}
            ORDER BY sd.rel_path COLLATE NOCASE
            LIMIT ? OFFSET ?""",
        params + [limit, offset],
    ).fetchall()
    return {"total": total, "limit": limit, "offset": offset,
            "documents": rows_to_dicts(rows)}


def codex_facets(conn) -> dict:
    def facet(sql):
        return [{"value": r[0], "count": r[1]}
                for r in conn.execute(sql).fetchall() if r[0] is not None]

    out = {
        "statuses": facet("SELECT status, COUNT(*) FROM source_document GROUP BY status ORDER BY 2 DESC"),
        "roles": facet("SELECT probable_role, COUNT(*) FROM source_document GROUP BY probable_role ORDER BY 2 DESC"),
        "media_types": facet("SELECT media_type, COUNT(*) FROM source_document GROUP BY media_type ORDER BY 2 DESC"),
        "corpus_roots": rows_to_dicts(conn.execute(
            """SELECT cr.id, cr.path, cr.classification, cr.role,
                      (SELECT COUNT(*) FROM source_document sd WHERE sd.corpus_root_id = cr.id) AS document_count
               FROM corpus_root cr ORDER BY document_count DESC, cr.path""").fetchall()),
        "canonical": "NONE",
    }
    # Stage 7: WORKING consolidated codex_document facets (may be absent on an
    # un-migrated store; fail soft).
    try:
        out["codex_statuses"] = facet(
            "SELECT status, COUNT(*) FROM codex_document GROUP BY status ORDER BY 2 DESC")
        out["codex_kinds"] = facet(
            "SELECT kind, COUNT(*) FROM codex_document GROUP BY kind ORDER BY 2 DESC")
        out["codex_total"] = conn.execute(
            "SELECT COUNT(*) FROM codex_document").fetchone()[0]
    except sqlite3.Error:
        out["codex_statuses"] = []
        out["codex_kinds"] = []
        out["codex_total"] = 0
    return out


def build_preview(document: dict, root_path: str | None) -> dict:
    """Read-only, capped, path-confined text preview. Never writes."""
    rel = document.get("rel_path") or ""
    media = (document.get("media_type") or "")
    if not root_path:
        return {"available": False, "reason": "document has no registered corpus root"}
    if root_path.startswith("CANDIDATE:"):
        return {"available": False, "reason": "corpus root is not a local path",
                "corpus_root": root_path}
    root_real = os.path.realpath(root_path)
    if not os.path.isdir(root_real):
        return {"available": False, "reason": "corpus root is not present on this machine",
                "corpus_root": root_path}

    candidate = os.path.realpath(os.path.join(root_real, rel))
    if candidate != root_real and not candidate.startswith(root_real + os.sep):
        return {"available": False, "reason": "path escapes the corpus root"}

    ext = os.path.splitext(candidate)[1].lower()
    text_like = (
        media.startswith("text/")
        or media in ("application/json", "application/x-ndjson", "application/x-sref")
        or ext in TEXT_EXTS
    )
    if not text_like:
        return {"available": False, "reason": f"not a text surface ({media or 'unknown'})"}

    if not os.path.isfile(candidate):
        return {"available": False, "reason": "file not present on this machine",
                "abs_path": candidate}

    try:
        size = os.path.getsize(candidate)
        with open(candidate, "rb") as fh:  # READ ONLY
            raw = fh.read(PREVIEW_CAP + 1)
    except OSError as exc:
        return {"available": False, "reason": f"could not read: {exc.strerror or exc}"}

    truncated = len(raw) > PREVIEW_CAP
    raw = raw[:PREVIEW_CAP]
    if b"\x00" in raw[:4096]:
        return {"available": False, "reason": "binary content (NUL bytes)",
                "abs_path": candidate, "size": size}
    text = raw.decode("utf-8", errors="replace")
    return {
        "available": True,
        "read_only": True,
        "abs_path": candidate,
        "corpus_root": root_path,
        "media_type": media,
        "size": size,
        "bytes_shown": len(raw),
        "cap": PREVIEW_CAP,
        "truncated": truncated,
        "text": text,
    }


def document_detail(conn, doc_id: str) -> dict | None:
    row = conn.execute(
        """SELECT sd.*, cr.path AS corpus_root_path, cr.classification AS corpus_classification
           FROM source_document sd
           JOIN corpus_root cr ON cr.id = sd.corpus_root_id
           WHERE sd.id = ?""", (doc_id,)).fetchone()
    if row is None:
        return None
    doc = dict(row)
    doc["preview"] = build_preview(doc, doc.get("corpus_root_path"))
    doc["read_only"] = True
    return doc


# ---------------------------------------------------------------------------
# Engine (read-only proposals) queries
# ---------------------------------------------------------------------------
ENGINE_COUNT_TABLES = (
    "source_document", "proposal", "concept", "relationship",
    "provenance_link", "analysis_run",
)


def engine_meta(db_path: str) -> dict:
    info = {
        "engine_db": db_path,
        "exists": os.path.isfile(db_path),
        "read_only": True,
        "canonical": "NONE",
        "counts": {},
        "proposal_statuses": [],
        "engine_versions": [],
    }
    if not info["exists"]:
        info["error"] = "engine store not found"
        return info
    try:
        with connect_ro(db_path) as conn:
            for table in ENGINE_COUNT_TABLES:
                try:
                    info["counts"][table] = conn.execute(
                        f"SELECT COUNT(*) FROM {table}").fetchone()[0]
                except sqlite3.Error:
                    continue
            try:
                info["proposal_statuses"] = [
                    r[0] for r in conn.execute(
                        "SELECT DISTINCT status FROM proposal ORDER BY status")]
            except sqlite3.Error:
                pass
            try:
                info["engine_versions"] = [
                    r[0] for r in conn.execute(
                        "SELECT DISTINCT engine_version FROM analysis_run "
                        "WHERE engine_version IS NOT NULL ORDER BY engine_version")]
            except sqlite3.Error:
                pass
    except sqlite3.Error as exc:
        info["error"] = str(exc)
    return info


def engine_facets(conn) -> dict:
    try:
        statuses = [{"value": r[0], "count": r[1]} for r in conn.execute(
            "SELECT status, COUNT(*) FROM proposal GROUP BY status ORDER BY 2 DESC")]
    except sqlite3.Error:
        statuses = []
    return {"statuses": statuses, "read_only": True, "canonical": "NONE"}


def list_engine_proposals(conn, query) -> dict:
    limit = max(1, min(500, int((query.get("limit") or ["50"])[0] or 50)))
    offset = max(0, int((query.get("offset") or ["0"])[0] or 0))
    # Quiet by default: only the hybrid:* synthesis rows, and Theme:* hidden.
    #   include_themes=1  -> keep hybrid:* but also show Theme:*
    #   all=1             -> show everything (older Stage-5 archaeology too)
    all_flag = _query_flag(query, "all")
    include_themes = _query_flag(query, "include_themes") or all_flag
    hybrid_only = not all_flag

    where, params = [], []
    q = (query.get("q") or [""])[0].strip()
    if q:
        like = f"%{q}%"
        where.append("(p.summary LIKE ? OR p.id LIKE ? OR p.attribution LIKE ?)")
        params += [like, like, like]
    status = (query.get("status") or [""])[0].strip()
    if status:
        where.append("p.status = ?")
        params.append(status)
    if hybrid_only:
        where.append("p.attribution LIKE 'hybrid:%'")
    if not include_themes:
        where.append("p.summary NOT LIKE 'Theme:%'")
    where_sql = (" WHERE " + " AND ".join(where)) if where else ""
    total = conn.execute(
        f"SELECT COUNT(*) FROM proposal p{where_sql}", params).fetchone()[0]
    rows = conn.execute(
        f"""SELECT p.id, p.status, p.summary, p.attribution, p.created_at, p.updated_at,
                   p.based_on_json,
                   (SELECT COUNT(*) FROM provenance_link v
                     WHERE v.subject_kind='proposal' AND v.subject_id=p.id) AS provenance_count
            FROM proposal p{where_sql}
            ORDER BY p.created_at DESC, p.id
            LIMIT ? OFFSET ?""",
        params + [limit, offset]).fetchall()
    try:
        unfiltered_total = conn.execute("SELECT COUNT(*) FROM proposal").fetchone()[0]
    except sqlite3.Error:
        unfiltered_total = total
    return {"total": total, "limit": limit, "offset": offset, "read_only": True,
            "canonical": "NONE", "unfiltered_total": unfiltered_total,
            "quiet": {"hybrid_only": hybrid_only, "include_themes": include_themes,
                      "all": all_flag},
            "proposals": rows_to_dicts(rows)}


def engine_proposal_detail(conn, pid: str) -> dict | None:
    row = conn.execute("SELECT * FROM proposal WHERE id = ?", (pid,)).fetchone()
    if row is None:
        return None
    prop = dict(row)
    try:
        prop["based_on"] = json.loads(prop.get("based_on_json") or "[]")
    except (ValueError, TypeError):
        prop["based_on"] = []
    prop["provenance"] = rows_to_dicts(conn.execute(
        """SELECT v.id, v.source_kind, v.source_id, v.confidence, v.status, v.note,
                  sd.rel_path AS source_rel_path, sd.probable_role AS source_role
           FROM provenance_link v
           LEFT JOIN source_document sd
                  ON sd.id = v.source_id AND v.source_kind = 'source_document'
           WHERE v.subject_kind = 'proposal' AND v.subject_id = ?
           ORDER BY v.source_kind, v.id""", (pid,)).fetchall())
    prop["relationships"] = rows_to_dicts(conn.execute(
        """SELECT id, from_kind, from_id, rel_type, to_kind, to_id, confidence, status
           FROM relationship WHERE from_id = ? OR to_id = ? ORDER BY id""",
        (pid, pid)).fetchall())
    prop["read_only"] = True
    prop["canonical"] = "NONE"
    return prop


def list_engine_runs(conn) -> dict:
    try:
        rows = conn.execute(
            """SELECT id, kind, status, engine_version, started_at, finished_at,
                      attribution, summary_json
               FROM analysis_run ORDER BY kind, id""").fetchall()
    except sqlite3.Error:
        rows = []
    runs = []
    for r in rows:
        d = dict(r)
        try:
            d["summary"] = json.loads(d.get("summary_json") or "{}")
        except (ValueError, TypeError):
            d["summary"] = {}
        runs.append(d)
    return {"runs": runs, "read_only": True, "canonical": "NONE"}


def engine_dry_run(engine_db: str, engine_py: str) -> tuple[dict | None, str | None]:
    """Shell to the Stage 5 engine with ``--dry-run`` on a throwaway copy.

    The real engine store is hashed before and after and never written; the
    dry-run itself commits nothing (the engine rolls the transaction back).
    """
    if not os.path.isfile(engine_py):
        return None, f"engine CLI not found: {engine_py}"
    if not os.path.isfile(engine_db):
        return None, f"engine store not found: {engine_db}"

    before = sha256_file(engine_db)
    tmpdir = tempfile.mkdtemp(prefix="stage4_engine_dryrun_")
    tmpdb = os.path.join(tmpdir, "codex_phase_i.sqlite")
    try:
        shutil.copyfile(engine_db, tmpdb)
        proc = subprocess.run(
            [sys.executable, engine_py, "--db", tmpdb, "run", "--dry-run"],
            cwd=os.path.dirname(engine_py), capture_output=True, text=True,
            timeout=ENGINE_TIMEOUT,
        )
        stdout, stderr, rc = proc.stdout, proc.stderr, proc.returncode
    except subprocess.TimeoutExpired:
        stdout, stderr, rc = "", f"engine timed out after {ENGINE_TIMEOUT}s", 124
    except OSError as exc:
        stdout, stderr, rc = "", str(exc), 1
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)
    after = sha256_file(engine_db)

    return {
        "dry_run": True,
        "read_only": True,
        "canonical": "NONE",
        "engine_db": engine_db,
        "engine_db_unchanged": before == after,
        "ran_on": "throwaway copy of the engine store (never the store itself)",
        "returncode": rc,
        "stdout": stdout,
        "stderr": stderr,
    }, None


class SynthesizeError(Exception):
    """Explicit synthesize request failed before the engine could run."""

    def __init__(self, message: str, status: int = 400):
        super().__init__(message)
        self.status = status


def _proposal_count(conn, where: str = "", params=()) -> int:
    return conn.execute(
        f"SELECT COUNT(*) FROM proposal {where}", params).fetchone()[0]


def _tail(text: str, n: int = 400) -> str:
    text = (text or "").strip()
    return text if len(text) <= n else "..." + text[-n:]


def _extract_llm_error(stderr: str) -> str | None:
    """Pull the fail-closed LLM reason out of the hybrid engine's stderr."""
    for line in reversed((stderr or "").splitlines()):
        low = line.lower()
        if "llm error" in low or "failed closed" in low:
            return line.split(":", 1)[-1].strip() or line.strip()
    return None


def synthesize_dialogue(db_path: str, hybrid_py: str, conversation_id: str,
                        use_llm: bool = False,
                        timeout: int = HYBRID_TIMEOUT) -> dict:
    """Explicitly synthesize PROPOSED dialogue candidates via the hybrid engine.

    Deterministic extraction is the default; ``use_llm`` only adds the optional
    LLM draft when the caller explicitly asked for it.  The engine is always
    invoked with ``--db <server living DB>`` (never the historical corpus) as an
    argv list (``shell=False``) with an explicit cwd, a timeout and captured
    output.  Nothing is ever auto-Accepted; results stay PROPOSED.
    """
    if not isinstance(conversation_id, str) or not _CONV_ID_RE.match(conversation_id):
        raise SynthesizeError(
            "conversation_id is required and must match [A-Za-z0-9_-]{1,128}", 400)
    if not os.path.isfile(hybrid_py):
        raise SynthesizeError(f"hybrid engine CLI not found: {hybrid_py}", 503)
    if not os.path.isfile(db_path):
        raise SynthesizeError(f"living store not found: {db_path}", 503)

    with connect_ro(db_path) as conn:
        conv = conn.execute(
            "SELECT id, title FROM conversation WHERE id = ?",
            (conversation_id,)).fetchone()
        if conv is None:
            raise SynthesizeError(f"conversation not found: {conversation_id}", 404)
        before_total = _proposal_count(conn)
        before_hybrid = _proposal_count(conn, "WHERE attribution LIKE 'hybrid:%'")
        before_llm = _proposal_count(conn, "WHERE attribution = 'hybrid:llm'")

    argv = [sys.executable, hybrid_py, "--db", db_path]
    if use_llm:
        argv.append("--llm")
    argv += ["synthesize-dialogue", "--conversation", conversation_id]

    timed_out = False
    try:
        proc = subprocess.run(
            argv, cwd=os.path.dirname(hybrid_py), shell=False,
            capture_output=True, text=True, timeout=timeout)
        returncode, stdout, stderr = proc.returncode, proc.stdout, proc.stderr
    except subprocess.TimeoutExpired as exc:
        timed_out = True
        returncode = 124
        out = exc.stdout
        stdout = out.decode("utf-8", "replace") if isinstance(out, bytes) else (out or "")
        err = exc.stderr
        stderr = (err.decode("utf-8", "replace") if isinstance(err, bytes) else (err or ""))
        stderr = (stderr + "\n" if stderr else "") + \
            f"hybrid engine timed out after {timeout}s"
    except OSError as exc:
        returncode, stdout, stderr = 1, "", str(exc)

    with connect_ro(db_path) as conn:
        after_total = _proposal_count(conn)
        after_hybrid = _proposal_count(conn, "WHERE attribution LIKE 'hybrid:%'")
        after_llm = _proposal_count(conn, "WHERE attribution = 'hybrid:llm'")
        offenders = living_store.scan_canonical(conn)

    new_total = after_total - before_total
    new_hybrid = after_hybrid - before_hybrid
    new_llm = after_llm - before_llm
    llm_drafted = bool(use_llm and new_llm > 0)
    llm_error = None
    if use_llm and not llm_drafted:
        llm_error = _extract_llm_error(stderr) or (
            "LLM draft unavailable (fail-closed); deterministic PROPOSED candidates "
            "were still created.")
    ok = returncode == 0 and not timed_out and not offenders
    result = {
        "ok": ok,
        "conversation_id": conversation_id,
        "conversation_title": conv["title"],
        "living_db": db_path,
        "hybrid_py": hybrid_py,
        "mode": "llm" if use_llm else "deterministic",
        "llm_requested": bool(use_llm),
        "llm_drafted": llm_drafted,
        "llm_error": llm_error,
        "returncode": returncode,
        "timed_out": timed_out,
        "stdout": stdout,
        "stderr": stderr,
        "proposals_before": before_total,
        "proposals_after": after_total,
        "new_proposals": new_total,
        "proposals_before_hybrid": before_hybrid,
        "new_hybrid_proposals": new_hybrid,
        "new_hybrid_llm_proposals": new_llm,
        "no_canonical": not offenders,
        "canonical": "NONE",
        "canonical_offenders": offenders,
        "read_only": False,
        "wrote_history": False,
        "auto_accepted": False,
    }
    if returncode != 0 or timed_out:
        result["error"] = (
            f"hybrid engine {'timed out' if timed_out else 'failed'} "
            f"(rc={returncode}): {_tail(stderr)}")
    return result


# ---------------------------------------------------------------------------
# Stage 7 living loop: engine run + controlled consolidation + WORKING browse
# ---------------------------------------------------------------------------
def living_meta_payload(db_path: str) -> dict:
    """Read-only summary of the living store (policy, counts, statuses)."""
    info = {"living_db": db_path, "exists": os.path.isfile(db_path),
            "read_only": True, "canonical": "NONE", "counts": {}}
    if not info["exists"]:
        info["error"] = "living store not found"
        return info
    try:
        with connect_ro(db_path) as conn:
            meta = living_store.living_meta(conn)
        info.update(meta)
        info["living_db"] = db_path
        info["read_only"] = True
    except sqlite3.Error as exc:
        info["error"] = str(exc)
    return info


def run_living_loop(db_path: str, engine_py: str, kinds=None) -> dict:
    """Run the Stage 5 engine against the living store, in place.

    Only PROPOSED/WORKING rows are written; ``source_document`` is digest-checked
    by the engine.  Returns an inspectable summary for the UI.
    """
    kinds = list(kinds or LIVING_LOOP_KINDS)
    with connect(db_path) as conn:
        seed = living_store.migrate(conn)
        before = conn.execute("SELECT COUNT(*) FROM proposal").fetchone()[0]
    run = living_store.run_engine(db_path, engine_py, kinds, timeout=ENGINE_TIMEOUT)
    with connect(db_path) as conn:
        after = conn.execute("SELECT COUNT(*) FROM proposal").fetchone()[0]
        codex_docs = conn.execute("SELECT COUNT(*) FROM codex_document").fetchone()[0]
        canonical = living_store.scan_canonical(conn)
    stdout_tail = "\n".join((run.get("stdout") or "").splitlines()[-8:])
    return {
        "ran": run["returncode"] == 0,
        "living_db": db_path,
        "kinds": kinds,
        "returncode": run["returncode"],
        "seeded_from_stage5": seed.get("seeded"),
        "proposals_before": before,
        "proposals_after": after,
        "new_proposals": after - before,
        "proposals_total": after,
        "codex_documents": codex_docs,
        "no_canonical": not canonical,
        "canonical": "NONE",
        "read_only": False,
        "stdout_tail": stdout_tail,
        "stderr": run.get("stderr") or "",
    }


def consolidate_proposal(db_path: str, proposal_id: str, actor: str = "stage4-ui") -> dict:
    """Controlled consolidation: explicit accept of ONE PROPOSED proposal."""
    with connect(db_path) as conn:
        return living_store.accept_proposal(conn, proposal_id, actor=actor)


def list_living_codex_documents(db_path: str, query) -> dict:
    with connect_ro(db_path) as conn:
        return living_store.list_codex_documents(conn, query)


def living_codex_document_detail(db_path: str, doc_id: str):
    with connect_ro(db_path) as conn:
        return living_store.codex_document_detail(conn, doc_id)


# ---------------------------------------------------------------------------
# Solace (conversation/message) queries — the ONLY writable tables
# ---------------------------------------------------------------------------
def _conversation_dict(row) -> dict:
    d = dict(row)
    try:
        d["participants_list"] = json.loads(d.get("participants") or "[]")
    except (ValueError, TypeError):
        d["participants_list"] = []
    return d


def list_conversations(conn) -> list[dict]:
    rows = conn.execute(
        """SELECT c.*, (SELECT COUNT(*) FROM message m WHERE m.conversation_id = c.id) AS message_count
           FROM conversation c
           ORDER BY COALESCE(c.started_at, c.updated_at, c.created_at) DESC, c.created_at DESC"""
    ).fetchall()
    out = []
    for r in rows:
        d = _conversation_dict(r)
        d["message_count"] = r["message_count"]
        out.append(d)
    return out


def get_conversation(conn, conv_id: str) -> dict | None:
    row = conn.execute("SELECT * FROM conversation WHERE id = ?", (conv_id,)).fetchone()
    if row is None:
        return None
    conv = _conversation_dict(row)
    msgs = conn.execute(
        """SELECT id, conversation_id, seq, role, body, sent_at, source_path, status,
                  created_at, updated_at
           FROM message WHERE conversation_id = ? ORDER BY seq""", (conv_id,)).fetchall()
    conv["messages"] = rows_to_dicts(msgs)
    conv["message_count"] = len(conv["messages"])
    return conv


def create_conversation(conn, payload: dict) -> dict:
    title = str(payload.get("title") or "").strip() or "Untitled conversation"
    notes = str(payload.get("notes") or "").strip()
    participants = payload.get("participants")
    if isinstance(participants, str):
        participants = [p.strip() for p in participants.split(",") if p.strip()]
    if not isinstance(participants, list) or not participants:
        participants = ["jd", "solace"]
    participants = [str(p) for p in participants]
    conv_id = f"conv_{uuid.uuid4().hex[:16]}"
    ts = now_iso()
    # status is fixed to WORKING; CANONICAL is not representable.
    conn.execute(
        """INSERT INTO conversation
             (id, title, participants, status, started_at, notes, attribution,
              created_at, updated_at)
           VALUES (?, ?, ?, 'WORKING', ?, ?, 'Stage 4 Solace surface', ?, ?)""",
        (conv_id, title, json.dumps(participants), ts, notes, ts, ts),
    )
    conn.commit()
    return get_conversation(conn, conv_id)


def append_message(conn, conv_id: str, payload: dict) -> tuple[dict | None, dict | None, str | None]:
    conv = conn.execute("SELECT id FROM conversation WHERE id = ?", (conv_id,)).fetchone()
    if conv is None:
        return None, None, "conversation not found"

    role = str(payload.get("role") or "").strip().lower()
    if role not in ("jd", "solace"):
        return None, None, "role must be 'jd' or 'solace'"
    body = str(payload.get("body") or "").strip()
    if not body:
        return None, None, "body must not be empty"
    if len(body) > MAX_MESSAGE_LEN:
        return None, None, f"body too long (max {MAX_MESSAGE_LEN} chars)"

    def _insert(msg_role: str, msg_body: str) -> dict:
        seq = conn.execute(
            "SELECT COALESCE(MAX(seq), 0) + 1 FROM message WHERE conversation_id = ?",
            (conv_id,)).fetchone()[0]
        msg_id = f"msg_{uuid.uuid4().hex[:16]}"
        ts = now_iso()
        conn.execute(
            """INSERT INTO message
                 (id, conversation_id, seq, role, body, sent_at, source_path, status,
                  created_at, updated_at)
               VALUES (?, ?, ?, ?, ?, ?, NULL, 'WORKING', ?, ?)""",
            (msg_id, conv_id, seq, msg_role, msg_body, ts, ts, ts),
        )
        conn.execute("UPDATE conversation SET updated_at = ? WHERE id = ?", (ts, conv_id))
        return dict(conn.execute("SELECT * FROM message WHERE id = ?", (msg_id,)).fetchone())

    message = _insert(role, body)

    reply = None
    if payload.get("stub_reply") and role == "jd":
        stub = (
            "[WORKING STUB — not LLM-backed] Received {n} character(s) from JD. "
            "This placeholder reply confirms the Solace message path works; a real "
            "Solace engine is Stage 5 and out of scope."
        ).format(n=len(body))
        reply = _insert("solace", stub)

    conn.commit()
    return message, reply, None


# ---------------------------------------------------------------------------
# HTTP handler
# ---------------------------------------------------------------------------
class Handler(BaseHTTPRequestHandler):
    server_version = "SolbianStage4/1.1"
    protocol_version = "HTTP/1.1"

    # -- helpers -----------------------------------------------------------
    def log_message(self, fmt, *args):  # quieter default logging
        if getattr(self.server, "verbose", False):
            sys.stderr.write("[http] %s - %s\n" % (self.address_string(), fmt % args))

    def _send(self, status: int, body: bytes, content_type: str) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Solbian-Surface", "stage4-three-surface")
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(body)

    def _json(self, status: int, obj) -> None:
        self._send(status, json.dumps(obj, ensure_ascii=False, indent=2).encode("utf-8"),
                   "application/json; charset=utf-8")

    def _error(self, status: int, message: str) -> None:
        self._json(status, {"error": message, "status": status})

    def _read_json(self):
        try:
            length = int(self.headers.get("Content-Length") or 0)
        except ValueError:
            return None, "invalid Content-Length"
        if length > MAX_BODY:
            return None, "request body too large"
        raw = self.rfile.read(length) if length else b"{}"
        try:
            data = json.loads(raw.decode("utf-8") or "{}")
        except (ValueError, UnicodeDecodeError):
            return None, "invalid JSON body"
        if not isinstance(data, dict):
            return None, "JSON body must be an object"
        return data, None

    def _serve_static(self, name: str) -> None:
        if name in ("", "/"):
            name = "index.html"
        if "/" in name or name.startswith("."):
            self._error(404, "not found")
            return
        full = os.path.join(STATIC_DIR, name)
        if not os.path.isfile(full):
            self._error(404, "not found")
            return
        ctype = mimetypes.guess_type(full)[0] or "application/octet-stream"
        if ctype.startswith("text/") or ctype in ("application/javascript", "application/json"):
            ctype += "; charset=utf-8"
        with open(full, "rb") as fh:
            self._send(200, fh.read(), ctype)

    # -- GET ---------------------------------------------------------------
    def do_GET(self):  # noqa: N802
        parsed = urlparse(self.path)
        path = unquote(parsed.path)
        query = parse_qs(parsed.query)

        if path in ("/", "/index.html"):
            self._serve_static("index.html")
            return
        if path.startswith("/static/"):
            self._serve_static(path[len("/static/"):])
            return
        if path == "/healthz":
            with connect(self.server.db_path) as conn:
                try:
                    codex_docs = conn.execute(
                        "SELECT COUNT(*) FROM codex_document").fetchone()[0]
                except sqlite3.Error:
                    codex_docs = 0
                payload = {
                    "ok": True, "service": "codex-solbian-stage4",
                    "db": self.server.db_path,
                    "source_documents": conn.execute("SELECT COUNT(*) FROM source_document").fetchone()[0],
                    "conversations": conn.execute("SELECT COUNT(*) FROM conversation").fetchone()[0],
                    "messages": conn.execute("SELECT COUNT(*) FROM message").fetchone()[0],
                    "codex_documents": codex_docs,
                    "canonical": "NONE",
                }
            emeta = engine_meta(self.server.engine_db_path)
            payload["engine_db"] = emeta["engine_db"]
            payload["engine_exists"] = emeta["exists"]
            payload["engine_proposals"] = emeta["counts"].get("proposal", 0)
            payload["living_db"] = self.server.db_path
            payload["engine_is_living_store"] = (
                os.path.abspath(self.server.db_path)
                == os.path.abspath(self.server.engine_db_path))
            self._json(200, payload)
            return
        if path == "/api/meta":
            with connect(self.server.db_path) as conn:
                try:
                    codex_docs = conn.execute(
                        "SELECT COUNT(*) FROM codex_document").fetchone()[0]
                except sqlite3.Error:
                    codex_docs = 0
                counts = {
                    t: conn.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
                    for t in ("corpus_root", "source_document", "conversation",
                              "message", "codex_document")
                }
                counts["codex_document_working"] = codex_docs
                self._json(200, {
                    "service": "Codex Solbian Phase I — Stage 4 (+ Stage 7 living loop)",
                    "canonical": "NONE",
                    "db": self.server.db_path,
                    "living_db": self.server.db_path,
                    "stage3_db": STAGE3_DB,
                    "preview_cap_bytes": PREVIEW_CAP,
                    # Backward-compatible Solace surface declaration.
                    "writable_tables": ["conversation", "message"],
                    # Stage 7: tables the living loop / consolidation may write.
                    "consolidation_tables": ["proposal", "codex_document", "revision",
                                             "provenance_link", "analysis_run"],
                    "engine_writable_tables": ["proposal", "concept", "relationship",
                                               "provenance_link", "analysis_run"],
                    "read_only_tables": ["source_document", "corpus_root",
                                         "proposal", "provenance_link", "analysis_run"],
                    "engine_db": self.server.engine_db_path,
                    "engine_is_living_store": (
                        os.path.abspath(self.server.db_path)
                        == os.path.abspath(self.server.engine_db_path)),
                    "engine_py": self.server.engine_py_path,
                    "hybrid_py": self.server.hybrid_py_path,
                    "hybrid_engine_available": os.path.isfile(self.server.hybrid_py_path),
                    "counts": counts,
                })
            return

        # ---- Solace ----
        if path == "/api/solace/conversations":
            with connect(self.server.db_path) as conn:
                self._json(200, {"conversations": list_conversations(conn)})
            return
        m = _CONV_ROUTE.match(path)
        if m:
            with connect(self.server.db_path) as conn:
                conv = get_conversation(conn, m.group(1))
            if conv is None:
                self._error(404, "conversation not found")
            else:
                self._json(200, {"conversation": conv})
            return

        # ---- Codex (read-only) ----
        if path == "/api/codex/roots":
            with connect(self.server.db_path) as conn:
                self._json(200, {"roots": codex_facets(conn)["corpus_roots"]})
            return
        if path == "/api/codex/facets":
            with connect(self.server.db_path) as conn:
                self._json(200, codex_facets(conn))
            return
        if path == "/api/codex/documents":
            with connect(self.server.db_path) as conn:
                self._json(200, list_documents(conn, query))
            return
        m = _DOC_ROUTE.match(path)
        if m:
            with connect(self.server.db_path) as conn:
                doc = document_detail(conn, m.group(1))
            if doc is None:
                self._error(404, "document not found")
            else:
                self._json(200, {"document": doc})
            return

        # ---- Codex (WORKING consolidated content, read-only here) ----
        if path == "/api/codex/codex-documents":
            try:
                self._json(200, list_living_codex_documents(self.server.db_path, query))
            except sqlite3.Error as exc:
                self._error(503, f"living store unavailable: {exc}")
            return
        m = _CODEX_DOC_ROUTE.match(path)
        if m:
            try:
                doc = living_codex_document_detail(self.server.db_path, m.group(1))
            except sqlite3.Error as exc:
                self._error(503, f"living store unavailable: {exc}")
                return
            if doc is None:
                self._error(404, "codex_document not found")
            else:
                self._json(200, {"codex_document": doc})
            return

        # ---- Living store meta ----
        if path == "/api/living/meta":
            self._json(200, living_meta_payload(self.server.db_path))
            return

        # ---- Engine (read-only proposals; Stage 5 store) ----
        if path == "/api/engine/meta":
            self._json(200, engine_meta(self.server.engine_db_path))
            return
        if path in ("/api/engine/facets", "/api/engine/proposals", "/api/engine/runs"):
            try:
                with connect_ro(self.server.engine_db_path) as conn:
                    if path == "/api/engine/facets":
                        data = engine_facets(conn)
                    elif path == "/api/engine/proposals":
                        data = list_engine_proposals(conn, query)
                    else:
                        data = list_engine_runs(conn)
            except sqlite3.Error as exc:
                self._error(503, f"engine store unavailable: {exc}")
                return
            self._json(200, data)
            return
        m = _ENGINE_PROP_ROUTE.match(path)
        if m:
            try:
                with connect_ro(self.server.engine_db_path) as conn:
                    prop = engine_proposal_detail(conn, m.group(1))
            except sqlite3.Error as exc:
                self._error(503, f"engine store unavailable: {exc}")
                return
            if prop is None:
                self._error(404, "proposal not found")
            else:
                self._json(200, {"proposal": prop})
            return

        self._error(404, "not found")

    # -- POST --------------------------------------------------------------
    def do_POST(self):  # noqa: N802
        path = unquote(urlparse(self.path).path)
        if path.startswith("/api/codex/"):
            self._error(405, "the Codex surface is read-only; no mutation endpoints exist")
            return

        # ---- Stage 7 living loop: run engine against the living store ----
        if path == "/api/engine/run":
            data, err = self._read_json()
            if err:
                self._error(400, err)
                return
            kinds = data.get("kinds") if isinstance(data, dict) else None
            if kinds is not None and not isinstance(kinds, list):
                self._error(400, "kinds must be a list")
                return
            try:
                self._json(200, run_living_loop(
                    self.server.db_path, self.server.engine_py_path, kinds))
            except (sqlite3.Error, living_store.LivingStoreError) as exc:
                self._error(503, f"living loop failed: {exc}")
            return

        # ---- Stage 7 controlled consolidation: accept ONE proposal ----
        m = _ENGINE_ACCEPT_ROUTE.match(path)
        if m:
            data, err = self._read_json()
            if err:
                self._error(400, err)
                return
            actor = str((data or {}).get("actor") or "stage4-ui")
            try:
                result = consolidate_proposal(self.server.db_path, m.group(1), actor)
            except living_store.LivingStoreError as exc:
                self._error(404 if "not found" in str(exc) else 400, str(exc))
                return
            except sqlite3.Error as exc:
                self._error(503, f"living store unavailable: {exc}")
                return
            self._json(200, result)
            return

        # ---- Stage 5b explicit hybrid synthesis (deterministic default) ----
        if path == "/api/engine/synthesize":
            data, err = self._read_json()
            if err:
                self._error(400, err)
                return
            if not isinstance(data, dict):
                self._error(400, "JSON body must be an object")
                return
            conv_id = str(data.get("conversation_id") or "").strip()
            use_llm = _as_bool(data.get("llm"))
            try:
                result = synthesize_dialogue(
                    self.server.db_path, self.server.hybrid_py_path,
                    conv_id, use_llm=use_llm)
            except SynthesizeError as exc:
                self._error(exc.status, str(exc))
                return
            if result["timed_out"]:
                code = 504
            elif result["returncode"] != 0 or not result["no_canonical"]:
                code = 503
            else:
                code = 200
            self._json(code, result)
            return

        if path == "/api/engine/dry-run":
            result, err = engine_dry_run(self.server.engine_db_path, self.server.engine_py_path)
            if err:
                self._error(503, err)
            else:
                self._json(200, result)
            return
        if path.startswith("/api/engine/"):
            self._error(405, "the Engine surface is read-only except POST "
                             "/api/engine/run, POST /api/engine/synthesize and "
                             "POST /api/engine/proposals/<id>/accept")
            return
        if path == "/api/solace/conversations":
            data, err = self._read_json()
            if err:
                self._error(400, err)
                return
            with connect(self.server.db_path) as conn:
                conv = create_conversation(conn, data)
            self._json(201, {"conversation": conv})
            return
        m = _MSG_ROUTE.match(path)
        if m:
            data, err = self._read_json()
            if err:
                self._error(400, err)
                return
            with connect(self.server.db_path) as conn:
                message, reply, err = append_message(conn, m.group(1), data)
            if err:
                code = 404 if "not found" in err else 400
                self._error(code, err)
                return
            payload = {"message": message, "reply": reply}
            # Stage 7(A): after a Solace message, run the durable analyzer on the
            # living store and surface the fresh proposal count.
            try:
                payload["living_loop"] = run_living_loop(
                    self.server.db_path, self.server.engine_py_path, SOLACE_KINDS)
            except (sqlite3.Error, living_store.LivingStoreError, OSError) as exc:
                payload["living_loop"] = {"ran": False, "error": str(exc)}
            self._json(201, payload)
            return
        self._error(404, "not found")

    # -- explicit read-only guards -----------------------------------------
    def _reject_mutation(self):
        path = unquote(urlparse(self.path).path)
        if path.startswith("/api/codex/"):
            self._error(405, "the Codex surface is read-only; no mutation endpoints exist")
        elif path.startswith("/api/engine/"):
            self._error(405, "the Engine surface only accepts POST /api/engine/run, "
                             "POST /api/engine/synthesize and "
                             "POST /api/engine/proposals/<id>/accept")
        else:
            self._error(405, "method not allowed")

    do_PUT = _reject_mutation      # noqa: N815
    do_PATCH = _reject_mutation    # noqa: N815
    do_DELETE = _reject_mutation   # noqa: N815


def ensure_db(db_path: str, allow_setup: bool = True) -> None:
    if not os.path.exists(db_path):
        if not allow_setup:
            raise FileNotFoundError(db_path)
        import setup_db  # local module
        print(f"[app] working store missing; building {db_path} from Stage 3 (read-only) ...")
        setup_db.build(db_path, inventory=DEFAULT_INVENTORY)
    # Stage 7: make the living store ready (analysis_run + one-time Stage 5 seed).
    try:
        with connect(db_path) as conn:
            living_store.ensure_base_schema(conn)
            seed = living_store.migrate(conn)
        if seed.get("seeded"):
            print(f"[app] living store seeded from Stage 5: {seed['copied']}")
        else:
            print(f"[app] living store engine tables ready ({seed.get('reason')})")
    except (sqlite3.Error, OSError) as exc:
        print(f"[app] WARNING: living-store prep failed ({exc}); "
              f"engine endpoints may be unavailable", file=sys.stderr)


def parse_args(argv=None):
    p = argparse.ArgumentParser(description="Stage 4/7 three-surface prototype server")
    p.add_argument("--host", default="127.0.0.1")
    p.add_argument("--port", type=int, default=8787)
    p.add_argument("--db", default=os.environ.get("SOLBIAN_DB", DEFAULT_DB))
    p.add_argument("--engine-db", default=DEFAULT_ENGINE_DB,
                   help="engine store to browse read-only (defaults to the living store)")
    p.add_argument("--engine-py", default=DEFAULT_ENGINE_PY,
                   help="Stage 5 engine CLI used by the living loop + dry-run")
    p.add_argument("--hybrid-py", default=DEFAULT_HYBRID_PY,
                   help="Stage 5b hybrid synthesis CLI used by /api/engine/synthesize")
    p.add_argument("--no-setup", action="store_true",
                   help="do not auto-build the working DB when missing")
    p.add_argument("--verbose", action="store_true")
    return p.parse_args(argv)


def main(argv=None) -> int:
    args = parse_args(argv)
    try:
        ensure_db(args.db, allow_setup=not args.no_setup)
    except FileNotFoundError:
        print(f"[app] ERROR: DB not found: {args.db} (run setup_db.py)", file=sys.stderr)
        return 2

    httpd = ThreadingHTTPServer((args.host, args.port), Handler)
    httpd.db_path = os.path.abspath(args.db)
    httpd.engine_db_path = os.path.abspath(args.engine_db)
    httpd.engine_py_path = os.path.abspath(args.engine_py)
    httpd.hybrid_py_path = os.path.abspath(args.hybrid_py)
    httpd.verbose = args.verbose
    host, port = httpd.server_address[:2]
    print(f"[app] Codex Solbian — Stage 4 (+ Stage 7 living loop)")
    print(f"[app] living db : {httpd.db_path}")
    print(f"[app] engine db : {httpd.engine_db_path}")
    print(f"[app] hybrid py : {httpd.hybrid_py_path}")
    print(f"[app] url       : http://{host}:{port}/")
    print(f"[app] CANONICAL: NONE · Solace + engine + explicit consolidation write "
          f"the living store · Codex browse read-only")
    sys.stdout.flush()
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[app] stopping")
    finally:
        httpd.server_close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
