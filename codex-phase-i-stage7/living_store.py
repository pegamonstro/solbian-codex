#!/usr/bin/env python3
"""Codex Solbian — Phase I · Stage 7 — the living store core.

One SQLite store is *the* living store for the whole loop:

    Solace (conversation/message)
        + Stage 5 engine rows (analysis_run/proposal/concept/relationship/provenance_link)
        + controlled consolidation output (codex_document WORKING + revision + provenance_link)
        + Stage 3 source index (corpus_root/source_document, read-only history)

Living-store policy
-------------------
* **Living store** = ``/Users/archcore/solbian/codex-phase-i-stage4/data/codex_phase_i.sqlite``
  (override with ``SOLBIAN_LIVING_DB`` / ``--db``).  It is the Stage 4 working
  copy of the Stage 3 source-of-truth store, so it already holds
  ``corpus_root`` + ``source_document`` + ``conversation``/``message``.
* The Stage 3 SoT store is **never** written.  It is only read (or copied once
  to create the living store).
* The Stage 5 engine store ``.../codex-phase-i-stage5/data/codex_phase_i.sqlite``
  is a *seed*: its engine tables (``analysis_run`` + the PROPOSED rows) are
  copied into the living store **once** (idempotent ``INSERT OR IGNORE``) when
  the living store has no proposals yet.  After that, the living store and the
  Stage 5 store are independent and Stage 5 is never written again.
* Every write funnel here is constrained to content status ``WORKING`` (or
  ``PROPOSED`` for engine rows).  ``CANONICAL`` is not in the schema and this
  module refuses to write it.

Controlled consolidation
-------------------------
``accept_proposal`` is the *only* path that turns a PROPOSED proposal into
Codex content.  It requires an explicit call (CLI ``living_loop.py accept`` or
``POST /api/engine/proposals/<id>/accept``) — there is no auto-accept:

    proposal (PROPOSED)  ->  codex_document (WORKING)
                         ->  revision (target=codex_document, proposal_id=...)
                         ->  provenance_link (subject=codex_document/revision,
                                              copied from the proposal)
                         ->  proposal.status = WORKING (accepted, never CANONICAL)
"""

from __future__ import annotations

import hashlib
import json
import os
import sqlite3
import subprocess
import sys
from contextlib import contextmanager

# --------------------------------------------------------------------------- #
# Paths & policy constants
# --------------------------------------------------------------------------- #

HERE = os.path.dirname(os.path.abspath(__file__))
STAGE4_DATA = "/Users/archcore/solbian/codex-phase-i-stage4/data/codex_phase_i.sqlite"

# The one living store.  SOLBIAN_LIVING_DB or an explicit path overrides it.
LIVING_DB = os.environ.get("SOLBIAN_LIVING_DB", STAGE4_DATA)

# Read-only baseline + Stage 5 seed.
STAGE3_DB = os.environ.get(
    "SOLBIAN_SOT_DB", "/Users/archcore/solbian/codex-phase-i-stage3/codex_phase_i.sqlite")
STAGE5_DB = os.environ.get(
    "SOLBIAN_STAGE5_DB",
    "/Users/archcore/solbian/codex-phase-i-stage5/data/codex_phase_i.sqlite")
STAGE5_ENGINE = os.environ.get(
    "SOLBIAN_ENGINE_PY", "/Users/archcore/solbian/codex-phase-i-stage5/engine.py")
MAC_CORPUS = "/Users/archcore/solbian/codex"

ENGINE_ATTR_PREFIX = "engine:stage5:"
CONSOLIDATION_ATTR_PREFIX = "consolidation:accepted:"

# The only content status consolidation may ever write.
CONSOLIDATION_STATUS = "WORKING"
ALLOWED_WRITE_STATUS = {"PROPOSED", "WORKING"}
CANONICAL = "CANONICAL"  # deliberately absent from every CHECK constraint

# Engine seed tables, in FK-safe order (none of them have FKs, so order is only
# cosmetic).  analysis_run is the run bookkeeping table.
ENGINE_SEED_TABLES = ("proposal", "concept", "relationship", "provenance_link",
                      "analysis_run")

ANALYSIS_RUN_DDL = """
CREATE TABLE IF NOT EXISTS analysis_run (
    id           TEXT PRIMARY KEY,
    started_at   TEXT NOT NULL,
    finished_at  TEXT,
    kind         TEXT NOT NULL,
    summary_json TEXT,
    status       TEXT NOT NULL,
    engine_version TEXT,
    attribution  TEXT,
    created_at   TEXT NOT NULL,
    updated_at   TEXT NOT NULL
);
"""

# Metadata table recording the one-time seed + policy, so the migration is
# auditable and cannot silently re-run.
LIVING_META_DDL = """
CREATE TABLE IF NOT EXISTS living_store_meta (
    key        TEXT PRIMARY KEY,
    value      TEXT,
    updated_at TEXT NOT NULL
);
"""

CODEX_DOC_KINDS = ("chapter", "scroll", "protocol", "law", "glossary",
                   "section", "other")
PROVENANCE_CONFIDENCE = ("TEXT-SUPPORTED", "TITLE-LEVEL", "SYNTHESIS", "UNKNOWN")


class LivingStoreError(Exception):
    """A deterministic, user-facing living-store failure."""


# --------------------------------------------------------------------------- #
# Small helpers
# --------------------------------------------------------------------------- #

def _now() -> str:
    import datetime as _dt
    return _dt.datetime.now(_dt.timezone.utc).replace(microsecond=0).isoformat()


now_iso = _now


def det_id(prefix: str, *parts: str) -> str:
    """Deterministic id: same inputs -> same id (re-runs stay idempotent)."""
    digest = hashlib.sha1(
        "\x1f".join(str(p) for p in parts).encode("utf-8")).hexdigest()[:16]
    return f"{prefix}_{digest}"


def resolve_living_db(path: str | None = None) -> str:
    return os.path.abspath(path or LIVING_DB)


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


@contextmanager
def connect(db_path: str):
    """Short-lived read/write connection with Row factory + FK enforcement."""
    conn = sqlite3.connect(db_path, timeout=30)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        yield conn
    finally:
        conn.close()


def table_names(conn: sqlite3.Connection) -> list[str]:
    return [r[0] for r in conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' "
        "AND name NOT LIKE 'sqlite_%' ORDER BY name")]


def scalar(conn: sqlite3.Connection, sql: str, params=()):
    return conn.execute(sql, params).fetchone()[0]


def counts(conn: sqlite3.Connection, tables=None) -> dict:
    out = {}
    for t in (tables or table_names(conn)):
        try:
            out[t] = scalar(conn, f"SELECT COUNT(*) FROM {t}")
        except sqlite3.Error:
            continue
    return out


# --------------------------------------------------------------------------- #
# Guards
# --------------------------------------------------------------------------- #

def scan_canonical(conn: sqlite3.Connection) -> list[str]:
    """Return every ``table.column`` that holds a CANONICAL *value*.

    Only status/enum columns are inspected.  Preserved user prose (for example a
    message quote inside ``proposal.body``) may legitimately mention the word;
    the guarantee is that no row ever carries ``CANONICAL`` as a status value,
    and the schema ``CHECK`` constraints do not even admit it.
    """
    offenders: list[str] = []
    for table in table_names(conn):
        try:
            cols = [r[1] for r in conn.execute(f"PRAGMA table_info({table})")]
        except sqlite3.Error:
            continue
        for col in cols:
            if col not in ("status", "confidence", "inventory_status", "classification"):
                continue
            try:
                n = scalar(
                    conn,
                    f"SELECT COUNT(*) FROM {table} WHERE {col} = ?",
                    (CANONICAL,))
            except sqlite3.Error:
                continue
            if n:
                offenders.append(f"{table}.{col}={n}")
    return offenders


def assert_no_canonical(conn: sqlite3.Connection) -> None:
    offenders = scan_canonical(conn)
    if offenders:
        raise LivingStoreError("CANONICAL value detected: " + ", ".join(offenders))


def _require_status(status: str) -> None:
    if status not in ALLOWED_WRITE_STATUS:
        raise LivingStoreError(f"refusing to write illegal content status: {status!r}")


# --------------------------------------------------------------------------- #
# Schema + one-time seed from Stage 5
# --------------------------------------------------------------------------- #

def ensure_base_schema(conn: sqlite3.Connection) -> None:
    """Idempotently add the analysis_run + living_store_meta tables."""
    conn.executescript(ANALYSIS_RUN_DDL)
    conn.executescript(LIVING_META_DDL)


def _meta_get(conn, key: str):
    try:
        row = conn.execute(
            "SELECT value FROM living_store_meta WHERE key = ?", (key,)).fetchone()
        return row[0] if row else None
    except sqlite3.Error:
        return None


def _meta_set(conn, key: str, value: str) -> None:
    conn.execute(
        """INSERT INTO living_store_meta (key, value, updated_at)
           VALUES (?, ?, ?)
           ON CONFLICT(key) DO UPDATE SET value = excluded.value,
                                          updated_at = excluded.updated_at""",
        (key, value, now_iso()))


def migrate(conn: sqlite3.Connection, stage5_db: str | None = None,
            force: bool = False) -> dict:
    """Seed the living store's engine tables from the Stage 5 store once.

    Idempotent: every copied row uses ``INSERT OR IGNORE`` and the seed is only
    attempted when the living store has no proposals (or ``force`` is set).
    Returns an inspectable summary.  Never touches Stage 5 or the SoT store.
    """
    stage5_db = os.path.abspath(stage5_db or STAGE5_DB)
    ensure_base_schema(conn)
    summary = {"stage5_db": stage5_db, "seeded": False, "reason": None,
               "already_seeded": _meta_get(conn, "seeded_from_stage5"), "copied": {}}
    living_props = scalar(conn, "SELECT COUNT(*) FROM proposal")
    if not os.path.isfile(stage5_db):
        summary["reason"] = "stage5 store not found"
        conn.commit()
        return summary
    if not force and living_props > 0:
        summary["reason"] = f"living store already has {living_props} proposal(s)"
        conn.commit()
        return summary

    src_conn = sqlite3.connect(f"file:{stage5_db}?mode=ro", uri=True)
    src_conn.row_factory = sqlite3.Row
    try:
        src_tables = {r[0] for r in src_conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table'")}
        for table in ENGINE_SEED_TABLES:
            if table not in src_tables:
                summary["copied"][table] = 0
                continue
            cols = [r[1] for r in src_conn.execute(f"PRAGMA table_info({table})")]
            if not cols:
                summary["copied"][table] = 0
                continue
            col_sql = ", ".join(cols)
            placeholders = ", ".join("?" * len(cols))
            rows = [tuple(r) for r in src_conn.execute(
                f"SELECT {col_sql} FROM {table}")]
            before = scalar(conn, f"SELECT COUNT(*) FROM main.{table}")
            if rows:
                conn.executemany(
                    f"INSERT OR IGNORE INTO main.{table} ({col_sql}) "
                    f"VALUES ({placeholders})", rows)
            after = scalar(conn, f"SELECT COUNT(*) FROM main.{table}")
            summary["copied"][table] = after - before
    finally:
        src_conn.close()
    _meta_set(conn, "seeded_from_stage5", stage5_db)
    _meta_set(conn, "policy", "living store: Stage 4 data/codex_phase_i.sqlite; "
                              "engine seed copied once from Stage 5; "
                              "consolidation max status WORKING; CANONICAL NONE")
    conn.commit()
    summary["seeded"] = True
    summary["reason"] = "seeded engine tables from Stage 5"
    return summary


def open_living(db_path: str | None = None, stage5_db: str | None = None,
                migrate_seed: bool = True) -> tuple[sqlite3.Connection, dict]:
    """Open (creating from the SoT if missing) and return (conn, migration)."""
    path = resolve_living_db(db_path)
    if not os.path.exists(path):
        if not os.path.exists(STAGE3_DB):
            raise LivingStoreError(f"living store missing and SoT not found: {path}")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        import shutil
        shutil.copyfile(STAGE3_DB, path)
    conn = sqlite3.connect(path, timeout=30)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    info = migrate(conn, stage5_db) if migrate_seed else {"seeded": False}
    return conn, info


# --------------------------------------------------------------------------- #
# Engine execution against the living store
# --------------------------------------------------------------------------- #

def run_engine(db_path: str, engine_py: str | None = None,
               kinds: list[str] | None = None, sot: str | None = None,
               timeout: int = 240) -> dict:
    """Run the Stage 5 deterministic engine against the living store.

    The engine writes only PROPOSED/WORKING rows; ``source_document`` is
    digest-checked by the engine itself.  Returns an inspectable result.
    """
    engine_py = os.path.abspath(engine_py or STAGE5_ENGINE)
    sot = os.path.abspath(sot or STAGE3_DB)
    if not os.path.isfile(engine_py):
        raise LivingStoreError(f"engine CLI not found: {engine_py}")
    cmd = [sys.executable, engine_py, "--db", os.path.abspath(db_path),
           "--sot", sot, "run"]
    if kinds:
        cmd += ["--kind", ",".join(kinds)]
    try:
        proc = subprocess.run(cmd, cwd=os.path.dirname(engine_py),
                              capture_output=True, text=True, timeout=timeout)
        rc, out, err = proc.returncode, proc.stdout, proc.stderr
    except subprocess.TimeoutExpired:
        rc, out, err = 124, "", f"engine timed out after {timeout}s"
    return {"returncode": rc, "kinds": kinds or ["all"], "engine_py": engine_py,
            "db": os.path.abspath(db_path), "stdout": out, "stderr": err}


# --------------------------------------------------------------------------- #
# Controlled consolidation
# --------------------------------------------------------------------------- #

def _derive_kind(proposal: dict) -> str:
    hay = " ".join(str(proposal.get(k) or "") for k in ("summary", "body")).lower()
    for kind, needle in (("glossary", "glossary"), ("protocol", "protocol"),
                         ("law", "law"), ("scroll", "scroll"),
                         ("chapter", "chapter"), ("section", "section")):
        if needle in hay:
            return kind
    return "other"


def _proposal_provenance(conn, proposal_id: str) -> list[dict]:
    return [dict(r) for r in conn.execute(
        """SELECT id, source_kind, source_id, note, confidence, status
           FROM provenance_link
           WHERE subject_kind = 'proposal' AND subject_id = ?
           ORDER BY source_kind, id""", (proposal_id,))]


def accept_proposal(conn: sqlite3.Connection, proposal_id: str,
                    actor: str = "jd", allow_reaccept: bool = True) -> dict:
    """Controlled consolidation: PROPOSED proposal -> WORKING codex_document.

    Requires an explicit call.  Creates/updates a ``codex_document`` with status
    ``WORKING`` (never CANONICAL), a ``revision`` row linking the proposal, and
    copies the proposal's ``provenance_link`` rows onto both the document and
    the revision.  Idempotent: a second call returns ``already_accepted``.
    """
    assert_no_canonical(conn)
    row = conn.execute("SELECT * FROM proposal WHERE id = ?",
                       (proposal_id,)).fetchone()
    if row is None:
        raise LivingStoreError(f"proposal not found: {proposal_id}")
    proposal = dict(row)
    if proposal.get("status") == CANONICAL:
        raise LivingStoreError("refusing to consolidate a CANONICAL row")

    doc_id = det_id("cdoc", proposal_id)
    rev_id = det_id("rev", proposal_id)
    existing = conn.execute("SELECT * FROM codex_document WHERE id = ?",
                            (doc_id,)).fetchone()
    if existing is not None and proposal.get("status") == CONSOLIDATION_STATUS:
        _require_status(CONSOLIDATION_STATUS)
        return {
            "already_accepted": True if allow_reaccept else False,
            "proposal_id": proposal_id,
            "proposal_status": proposal.get("status"),
            "codex_document": dict(existing),
            "revision": dict(conn.execute(
                "SELECT * FROM revision WHERE id = ?", (rev_id,)).fetchone() or {}),
            "provenance_copied": 0,
            "status": CONSOLIDATION_STATUS,
            "canonical": "NONE",
        }

    _require_status(CONSOLIDATION_STATUS)
    ts = now_iso()
    kind = _derive_kind(proposal)
    if kind not in CODEX_DOC_KINDS:
        kind = "other"
    title = (proposal.get("summary") or "").strip()[:200] or f"Consolidated {proposal_id}"
    body = proposal.get("body") or proposal.get("summary") or ""
    prov = _proposal_provenance(conn, proposal_id)
    source_doc_id = next(
        (p["source_id"] for p in prov if p["source_kind"] == "source_document"), None)

    prev_version = int(existing["version"]) if existing is not None else 0
    next_version = prev_version + 1 if existing is not None else 1
    attribution = f"{CONSOLIDATION_ATTR_PREFIX}{proposal_id}"

    conn.execute(
        """INSERT INTO codex_document
             (id, kind, title, body, source_document_id, status, version,
              attribution, created_at, updated_at)
           VALUES (?, ?, ?, ?, ?, 'WORKING', ?, ?, ?, ?)
           ON CONFLICT(id) DO UPDATE SET
               kind               = excluded.kind,
               title              = excluded.title,
               body               = excluded.body,
               source_document_id = excluded.source_document_id,
               status             = 'WORKING',
               version            = excluded.version,
               attribution        = excluded.attribution,
               updated_at         = excluded.updated_at""",
        (doc_id, kind, title, body, source_doc_id, next_version, attribution,
         ts, ts),
    )
    conn.execute(
        """INSERT INTO revision
             (id, target_kind, target_id, proposal_id, prev_version, next_version,
              diff_summary, status, reversible, created_at, updated_at)
           VALUES (?, 'codex_document', ?, ?, ?, ?, ?, 'WORKING', 1, ?, ?)
           ON CONFLICT(id) DO UPDATE SET
               target_kind  = excluded.target_kind,
               target_id    = excluded.target_id,
               proposal_id  = excluded.proposal_id,
               prev_version = excluded.prev_version,
               next_version = excluded.next_version,
               diff_summary = excluded.diff_summary,
               status       = 'WORKING',
               updated_at   = excluded.updated_at""",
        (rev_id, doc_id, proposal_id, prev_version, next_version,
         f"Accept proposal {proposal_id} into WORKING codex_document {doc_id} "
         f"(v{next_version}) by {actor}", ts, ts),
    )

    copied = 0
    for link in prov:
        note = (f"accepted from proposal {proposal_id}"
                + (f": {link['note']}" if link.get("note") else ""))
        confidence = link.get("confidence") or "UNKNOWN"
        if confidence not in PROVENANCE_CONFIDENCE:
            confidence = "UNKNOWN"
        for subject_kind, subject_id in (("codex_document", doc_id),
                                         ("revision", rev_id)):
            vid = det_id("provAcc", subject_kind, subject_id,
                         link["source_kind"], link["source_id"])
            conn.execute(
                """INSERT INTO provenance_link
                     (id, subject_kind, subject_id, source_kind, source_id,
                      note, confidence, status, created_at, updated_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?, 'WORKING', ?, ?)
                   ON CONFLICT(id) DO UPDATE SET
                       note       = excluded.note,
                       confidence = excluded.confidence,
                       status     = 'WORKING',
                       updated_at = excluded.updated_at""",
                (vid, subject_kind, subject_id, link["source_kind"],
                 link["source_id"], note, confidence, ts, ts),
            )
            copied += 1

    # The proposal itself is marked accepted-into-working (WORKING), not CANONICAL.
    conn.execute("UPDATE proposal SET status = 'WORKING', updated_at = ? WHERE id = ?",
                 (ts, proposal_id))
    conn.commit()
    assert_no_canonical(conn)

    doc = dict(conn.execute("SELECT * FROM codex_document WHERE id = ?",
                            (doc_id,)).fetchone())
    rev = dict(conn.execute("SELECT * FROM revision WHERE id = ?",
                            (rev_id,)).fetchone())
    return {
        "already_accepted": False,
        "proposal_id": proposal_id,
        "proposal_status": CONSOLIDATION_STATUS,
        "codex_document": doc,
        "revision": rev,
        "source_document_id": source_doc_id,
        "provenance_copied": copied,
        "status": CONSOLIDATION_STATUS,
        "canonical": "NONE",
    }


# --------------------------------------------------------------------------- #
# Codex (WORKING) read queries
# --------------------------------------------------------------------------- #

def list_codex_documents(conn: sqlite3.Connection, query: dict) -> dict:
    def one(field, default):
        v = query.get(field)
        return (v[0] if isinstance(v, list) and v else v) if v is not None else default

    limit = max(1, min(500, int(one("limit", "50") or 50)))
    offset = max(0, int(one("offset", "0") or 0))
    where, params = [], []
    q = (one("q", "") or "").strip()
    if q:
        like = f"%{q}%"
        where.append("(cd.title LIKE ? OR cd.body LIKE ? OR cd.id LIKE ? "
                     "OR cd.attribution LIKE ?)")
        params += [like, like, like, like]
    status = (one("status", "") or "").strip()
    if status:
        where.append("cd.status = ?")
        params.append(status)
    kind = (one("kind", "") or "").strip()
    if kind:
        where.append("cd.kind = ?")
        params.append(kind)
    where_sql = (" WHERE " + " AND ".join(where)) if where else ""
    total = scalar(conn, f"SELECT COUNT(*) FROM codex_document cd{where_sql}", params)
    rows = conn.execute(
        f"""SELECT cd.id, cd.kind, cd.title, cd.status, cd.version,
                   cd.source_document_id, cd.attribution, cd.created_at, cd.updated_at,
                   (SELECT COUNT(*) FROM provenance_link v
                     WHERE v.subject_kind='codex_document' AND v.subject_id=cd.id)
                     AS provenance_count,
                   (SELECT r.id FROM revision r
                     WHERE r.target_kind='codex_document' AND r.target_id=cd.id
                     ORDER BY r.created_at DESC LIMIT 1) AS revision_id
            FROM codex_document cd{where_sql}
            ORDER BY cd.updated_at DESC, cd.id
            LIMIT ? OFFSET ?""",
        params + [limit, offset]).fetchall()
    return {"total": total, "limit": limit, "offset": offset,
            "codex_documents": [dict(r) for r in rows],
            "status": "WORKING", "canonical": "NONE"}


def codex_document_detail(conn: sqlite3.Connection, doc_id: str) -> dict | None:
    row = conn.execute("SELECT * FROM codex_document WHERE id = ?",
                       (doc_id,)).fetchone()
    if row is None:
        return None
    doc = dict(row)
    doc["provenance"] = [dict(r) for r in conn.execute(
        """SELECT v.id, v.source_kind, v.source_id, v.confidence, v.status, v.note,
                  sd.rel_path AS source_rel_path,
                  m.body AS message_body, m.role AS message_role
           FROM provenance_link v
           LEFT JOIN source_document sd
                  ON sd.id = v.source_id AND v.source_kind = 'source_document'
           LEFT JOIN message m
                  ON m.id = v.source_id AND v.source_kind = 'message'
           WHERE v.subject_kind = 'codex_document' AND v.subject_id = ?
           ORDER BY v.source_kind, v.id""", (doc_id,))]
    doc["revisions"] = [dict(r) for r in conn.execute(
        """SELECT id, target_kind, target_id, proposal_id, prev_version,
                  next_version, diff_summary, status, reversible,
                  created_at, updated_at
           FROM revision WHERE target_kind='codex_document' AND target_id = ?
           ORDER BY created_at DESC, id""", (doc_id,))]
    doc["read_only"] = True
    doc["canonical"] = "NONE"
    return doc


def living_meta(conn: sqlite3.Connection) -> dict:
    return {
        "living_db": None,  # filled by caller that knows the path
        "policy": _meta_get(conn, "policy"),
        "seeded_from_stage5": _meta_get(conn, "seeded_from_stage5"),
        "counts": counts(conn, ("corpus_root", "source_document", "conversation",
                                "message", "proposal", "concept", "relationship",
                                "provenance_link", "analysis_run",
                                "codex_document", "revision")),
        "proposal_statuses": [r[0] for r in conn.execute(
            "SELECT DISTINCT status FROM proposal ORDER BY status")],
        "codex_document_statuses": [r[0] for r in conn.execute(
            "SELECT DISTINCT status FROM codex_document ORDER BY status")],
        "canonical": "NONE",
    }


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #

def _print_json(obj) -> None:
    print(json.dumps(obj, indent=2, sort_keys=True, default=str))


def main(argv=None) -> int:
    import argparse
    p = argparse.ArgumentParser(
        prog="living_store.py",
        description="Codex Solbian Stage 7 — living store policy/migration helpers.")
    p.add_argument("--db", default=None,
                   help=f"living store (default: {LIVING_DB})")
    p.add_argument("--stage5-db", default=STAGE5_DB)
    sub = p.add_subparsers(dest="cmd", required=True)

    m = sub.add_parser("migrate", help="seed engine tables from Stage 5 (once)")
    m.add_argument("--force", action="store_true")
    m.add_argument("--json", action="store_true")

    i = sub.add_parser("info", help="show living-store counts + policy")
    i.add_argument("--json", action="store_true")

    a = sub.add_parser("accept", help="controlled consolidation of one proposal")
    a.add_argument("proposal_id")
    a.add_argument("--actor", default="jd")
    a.add_argument("--json", action="store_true")

    args = p.parse_args(argv)
    db = resolve_living_db(args.db)
    if args.cmd == "migrate":
        if not os.path.exists(db):
            raise LivingStoreError(f"living store not found: {db}")
        with connect(db) as conn:
            summary = migrate(conn, args.stage5_db, force=args.force)
            summary["living_db"] = db
        (_print_json if args.json else lambda s: print(
            f"migrate: seeded={s['seeded']} reason={s['reason']} copied={s['copied']}"
        ))(summary)
        return 0
    if args.cmd == "info":
        if not os.path.exists(db):
            raise LivingStoreError(f"living store not found: {db}")
        with connect(db) as conn:
            ensure_base_schema(conn)
            meta = living_meta(conn)
        meta["living_db"] = db
        if args.json:
            _print_json(meta)
        else:
            print(f"living_db: {db}")
            print(f"policy   : {meta['policy']}")
            print("counts   : " + ", ".join(f"{k}={v}" for k, v in meta["counts"].items()))
        return 0
    if args.cmd == "accept":
        if not os.path.exists(db):
            raise LivingStoreError(f"living store not found: {db}")
        with connect(db) as conn:
            result = accept_proposal(conn, args.proposal_id, actor=args.actor)
        if args.json:
            _print_json(result)
        else:
            print(f"proposal {result['proposal_id']} -> {result['proposal_status']}")
            print(f"codex_document {result['codex_document']['id']} "
                  f"status={result['codex_document']['status']} "
                  f"already_accepted={result['already_accepted']}")
            print(f"provenance copied: {result['provenance_copied']} · CANONICAL NONE")
        return 0
    return 2


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except LivingStoreError as exc:
        print(f"living store error: {exc}", file=sys.stderr)
        raise SystemExit(2)
