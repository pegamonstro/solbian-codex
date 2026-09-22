#!/usr/bin/env python3
"""Codex Solbian Phase I — Stage 4 two-surface prototype server.

Two surfaces over one local SQLite store (Python stdlib only; no frameworks):

* **Solace**  — list / create conversations and append messages. The only tables
  this server ever writes are ``conversation`` and ``message``.
* **Codex Solbian** — strictly READ-ONLY browse of ``source_document`` plus an
  optional read-only text preview of files under a registered corpus root.

Safety
------
* ``source_document`` is never inserted, updated or deleted by this server.
* The historical corpus ``/Users/archcore/solbian/codex`` is only ever opened
  read-only, and only for a capped text preview (200 KB) of a regular file that
  resolves inside a registered corpus root.
* ``CANONICAL`` does not exist in the data model and is never offered or emitted.

Run
---
    python3 app.py                 # -> http://127.0.0.1:8787
    python3 app.py --port 9000
    python3 app.py --db /path/to/codex_phase_i.sqlite
"""

from __future__ import annotations

import argparse
import json
import mimetypes
import os
import re
import sqlite3
import sys
import uuid
from contextlib import closing
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, unquote, urlparse

HERE = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(HERE, "static")
DEFAULT_DB = os.path.join(HERE, "data", "codex_phase_i.sqlite")
STAGE3_DB = "/Users/archcore/solbian/codex-phase-i-stage3/codex_phase_i.sqlite"
DEFAULT_INVENTORY = os.path.join(HERE, "baseline_inventory_full.json")

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
_CONV_ROUTE = re.compile(r"^/api/solace/conversations/([A-Za-z0-9_\-]+)$")
_MSG_ROUTE = re.compile(r"^/api/solace/conversations/([A-Za-z0-9_\-]+)/messages$")


def now_iso() -> str:
    import datetime as _dt
    return _dt.datetime.now(_dt.timezone.utc).replace(microsecond=0).isoformat()


def connect(db_path: str):
    """Open a short-lived connection. Use as ``with open_db(path) as conn:``."""
    conn = sqlite3.connect(db_path, timeout=15)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return closing(conn)


def rows_to_dicts(rows) -> list[dict]:
    return [dict(r) for r in rows]


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

    return {
        "statuses": facet("SELECT status, COUNT(*) FROM source_document GROUP BY status ORDER BY 2 DESC"),
        "roles": facet("SELECT probable_role, COUNT(*) FROM source_document GROUP BY probable_role ORDER BY 2 DESC"),
        "media_types": facet("SELECT media_type, COUNT(*) FROM source_document GROUP BY media_type ORDER BY 2 DESC"),
        "corpus_roots": rows_to_dicts(conn.execute(
            """SELECT cr.id, cr.path, cr.classification, cr.role,
                      (SELECT COUNT(*) FROM source_document sd WHERE sd.corpus_root_id = cr.id) AS document_count
               FROM corpus_root cr ORDER BY document_count DESC, cr.path""").fetchall()),
    }


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
    server_version = "SolbianStage4/1.0"
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
        self.send_header("X-Solbian-Surface", "stage4-two-surface")
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
                self._json(200, {
                    "ok": True, "service": "codex-solbian-stage4",
                    "db": self.server.db_path,
                    "source_documents": conn.execute("SELECT COUNT(*) FROM source_document").fetchone()[0],
                    "conversations": conn.execute("SELECT COUNT(*) FROM conversation").fetchone()[0],
                    "messages": conn.execute("SELECT COUNT(*) FROM message").fetchone()[0],
                    "canonical": "NONE",
                })
            return
        if path == "/api/meta":
            with connect(self.server.db_path) as conn:
                self._json(200, {
                    "service": "Codex Solbian Phase I — Stage 4",
                    "canonical": "NONE",
                    "db": self.server.db_path,
                    "stage3_db": STAGE3_DB,
                    "preview_cap_bytes": PREVIEW_CAP,
                    "writable_tables": ["conversation", "message"],
                    "read_only_tables": ["source_document", "corpus_root"],
                    "counts": {
                        t: conn.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
                        for t in ("corpus_root", "source_document", "conversation",
                                  "message", "codex_document")
                    },
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

        self._error(404, "not found")

    # -- POST --------------------------------------------------------------
    def do_POST(self):  # noqa: N802
        path = unquote(urlparse(self.path).path)
        if path.startswith("/api/codex/"):
            self._error(405, "the Codex surface is read-only; no mutation endpoints exist")
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
            self._json(201, {"message": message, "reply": reply})
            return
        self._error(404, "not found")

    # -- explicit read-only guard for Codex --------------------------------
    def _reject_mutation(self):
        path = unquote(urlparse(self.path).path)
        if path.startswith("/api/codex/"):
            self._error(405, "the Codex surface is read-only; no mutation endpoints exist")
        else:
            self._error(405, "method not allowed")

    do_PUT = _reject_mutation      # noqa: N815
    do_PATCH = _reject_mutation    # noqa: N815
    do_DELETE = _reject_mutation   # noqa: N815


def ensure_db(db_path: str, allow_setup: bool = True) -> None:
    if os.path.exists(db_path):
        return
    if not allow_setup:
        raise FileNotFoundError(db_path)
    import setup_db  # local module
    print(f"[app] working store missing; building {db_path} from Stage 3 (read-only) ...")
    setup_db.build(db_path, inventory=DEFAULT_INVENTORY)


def parse_args(argv=None):
    p = argparse.ArgumentParser(description="Stage 4 two-surface prototype server")
    p.add_argument("--host", default="127.0.0.1")
    p.add_argument("--port", type=int, default=8787)
    p.add_argument("--db", default=os.environ.get("SOLBIAN_DB", DEFAULT_DB))
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
    httpd.verbose = args.verbose
    host, port = httpd.server_address[:2]
    print(f"[app] Codex Solbian — Stage 4 two-surface prototype")
    print(f"[app] db  : {httpd.db_path}")
    print(f"[app] url : http://{host}:{port}/")
    print(f"[app] CANONICAL: NONE · Solace writes conversation/message only · Codex read-only")
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
