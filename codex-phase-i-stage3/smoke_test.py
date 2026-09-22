#!/usr/bin/env python3
"""Stage 3 smoke test.

Creates a throwaway SQLite DB from ``schema.sql``, asserts the tables exist,
inserts a sample conversation -> messages -> codex document -> proposal ->
revision -> provenance_link chain, round-trips the data, and exits 0.

The shipped ``codex_phase_i.sqlite`` is inspected read-only; this test never
writes to it. Nothing under the historical corpus is touched.

Usage:
    python3 smoke_test.py
"""

from __future__ import annotations

import datetime as _dt
import os
import sqlite3
import sys
import tempfile
import traceback

HERE = os.path.dirname(os.path.abspath(__file__))
SCHEMA = os.path.join(HERE, "schema.sql")
SHIPPED_DB = os.path.join(HERE, "codex_phase_i.sqlite")

REQUIRED_TABLES = [
    "corpus_root", "source_document", "conversation", "message", "codex_document",
    "concept", "relationship", "proposal", "revision", "provenance_link",
]
CONTENT_STATUS = [
    "SOURCE", "HISTORICAL", "WORKING", "PROPOSED", "REVISION", "RELATED", "UNKNOWN",
]


def now_iso() -> str:
    return _dt.datetime.now(_dt.timezone.utc).replace(microsecond=0).isoformat()


def check(cond: bool, label: str) -> None:
    if not cond:
        raise AssertionError(label)
    print(f"  ok  {label}")


def main() -> int:
    ts = now_iso()
    tmpdir = tempfile.mkdtemp(prefix="stage3_smoke_")
    db_path = os.path.join(tmpdir, "smoke.sqlite")

    print("== Stage 3 smoke test ==")
    print(f"schema      : {SCHEMA}")
    print(f"scratch db  : {db_path}")

    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON")
    with open(SCHEMA, "r", encoding="utf-8") as fh:
        conn.executescript(fh.read())
    conn.commit()

    # -- 1. tables exist -----------------------------------------------------
    print("\n[1] schema")
    tables = {r[0] for r in conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table'")}
    for t in REQUIRED_TABLES:
        check(t in tables, f"table exists: {t}")
    check("CANONICAL" not in CONTENT_STATUS, "status enum excludes CANONICAL")
    schema_text = open(SCHEMA, encoding="utf-8").read()
    check("'CANONICAL'" not in schema_text,
          "no CHECK constraint admits a CANONICAL value")

    # -- 2. corpus_root + source_document (pointer only) ---------------------
    print("\n[2] corpus root + source pointer")
    conn.execute(
        """INSERT INTO corpus_root
               (id, path, classification, role, notes, status, attribution, created_at, updated_at)
           VALUES (?,?,?,?,?,?,?,?,?)""",
        ("croot_smoke", "/Users/archcore/solbian/codex", "CURRENT",
         "PRIMARY_HISTORICAL_WORKING_TREE", "notes only; never written",
         "SOURCE", "smoke", ts, ts),
    )
    conn.execute(
        """INSERT INTO source_document
               (id, corpus_root_id, rel_path, media_type, byte_size, mtime, sha256,
                probable_role, inventory_status, status, plurality_flags, notes,
                attribution, created_at, updated_at)
           VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        ("sdoc_smoke", "croot_smoke", "source_original/scrolls", "inode/directory",
         None, ts, None, "SCROLL", "HISTORICAL_CANDIDATE", "HISTORICAL",
         '["scroll_material","mac_only_surface"]', "", "smoke", ts, ts),
    )

    # -- 3. conversation + messages ------------------------------------------
    print("\n[3] conversation + messages")
    conn.execute(
        """INSERT INTO conversation
               (id, title, participants, status, started_at, notes, attribution,
                created_at, updated_at)
           VALUES (?,?,?,?,?,?,?,?,?)""",
        ("conv_smoke", "Smoke: Stage 3 chat", '["jd","solace"]', "WORKING",
         ts, "", "smoke", ts, ts),
    )
    msg_rows = [
        ("msg_smoke_1", "conv_smoke", 1, "jd", "Does the store preserve plurality?", ts),
        ("msg_smoke_2", "conv_smoke", 2, "solace", "Yes — as status and flags.", ts),
    ]
    conn.executemany(
        """INSERT INTO message
               (id, conversation_id, seq, role, body, sent_at, source_path, status,
                created_at, updated_at)
           VALUES (?,?,?,?,?,?,?,?,?,?)""",
        [(*r, None, "WORKING", ts, ts) for r in msg_rows],
    )

    # -- 4. codex document (WORKING by default) ------------------------------
    print("\n[4] codex document")
    conn.execute(
        """INSERT INTO codex_document
               (id, kind, title, body, source_document_id, status, version,
                attribution, created_at, updated_at)
           VALUES (?,?,?,?,?,?,?,?,?,?)""",
        ("doc_smoke", "scroll", "Smoke working note", "draft text",
         "sdoc_smoke", "WORKING", 1, "smoke", ts, ts),
    )

    # -- 5. proposal + revision ----------------------------------------------
    print("\n[5] proposal + revision")
    conn.execute(
        """INSERT INTO proposal
               (id, summary, body, based_on_json, status, attribution, created_at, updated_at)
           VALUES (?,?,?,?,?,?,?,?)""",
        ("prop_smoke", "Promote draft working note", "keep WORKING until reviewed",
         '["msg_smoke_1","msg_smoke_2"]', "PROPOSED", "smoke", ts, ts),
    )
    conn.execute(
        """INSERT INTO revision
               (id, target_kind, target_id, proposal_id, prev_version, next_version,
                diff_summary, status, reversible, created_at, updated_at)
           VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
        ("rev_smoke", "codex_document", "doc_smoke", "prop_smoke", 1, 2,
         "bump version only; body untouched", "REVISION", 1, ts, ts),
    )

    # -- 6. provenance links -------------------------------------------------
    print("\n[6] provenance links")
    prov_rows = [
        ("prov_smoke_1", "proposal", "prop_smoke", "message", "msg_smoke_1",
         "proposal grounded in chat", "TEXT-SUPPORTED", "UNKNOWN", ts, ts),
        ("prov_smoke_2", "codex_document", "doc_smoke", "source_document", "sdoc_smoke",
         "points at historical scroll surface, not a copy", "TITLE-LEVEL",
         "UNKNOWN", ts, ts),
    ]
    conn.executemany(
        """INSERT INTO provenance_link
               (id, subject_kind, subject_id, source_kind, source_id, note,
                confidence, status, created_at, updated_at)
           VALUES (?,?,?,?,?,?,?,?,?,?)""",
        prov_rows,
    )
    conn.commit()

    # -- 7. round-trip reads -------------------------------------------------
    print("\n[7] round-trip queries")
    title, = conn.execute(
        "SELECT title FROM conversation WHERE id='conv_smoke'").fetchone()
    check(title == "Smoke: Stage 3 chat", "conversation round-trips")

    bodies = [r[0] for r in conn.execute(
        "SELECT body FROM message WHERE conversation_id='conv_smoke' ORDER BY seq")]
    check(bodies == ["Does the store preserve plurality?",
                     "Yes — as status and flags."], "messages round-trip in seq order")

    joined = conn.execute(
        """SELECT c.title, m.seq, m.body
           FROM message m JOIN conversation c ON c.id = m.conversation_id
           WHERE c.id='conv_smoke' ORDER BY m.seq""").fetchall()
    check(len(joined) == 2, "conversation->message join returns 2 rows")

    prov = conn.execute(
        """SELECT p.summary, pl.source_kind
           FROM proposal p
           JOIN provenance_link pl
             ON pl.subject_kind='proposal' AND pl.subject_id=p.id
           WHERE p.id='prop_smoke'""").fetchone()
    check(prov == ("Promote draft working note", "message"),
          "proposal->provenance join round-trips")

    kinds = {r[0] for r in conn.execute("SELECT DISTINCT subject_kind FROM provenance_link")}
    check(kinds == {"proposal", "codex_document"}, "both provenance subjects present")

    # -- 8. invariants -------------------------------------------------------
    print("\n[8] invariants")
    fk = conn.execute("PRAGMA foreign_key_check").fetchall()
    check(fk == [], "foreign_key_check clean")

    dup = conn.execute(
        "SELECT corpus_root_id, rel_path, COUNT(*) FROM source_document "
        "GROUP BY 1,2 HAVING COUNT(*)>1").fetchall()
    check(dup == [], "source_document root+rel_path unique")

    check(conn.execute("SELECT status FROM codex_document WHERE id='doc_smoke'")
          .fetchone()[0] == "WORKING", "codex_document defaults WORKING")

    try:
        conn.execute(
            """INSERT INTO concept (id, name, definition, status, notes, attribution,
                                    created_at, updated_at)
               VALUES ('c_bad','x','y','CANONICAL','','',?,?)""", (ts, ts))
        conn.rollback()
        raise AssertionError("CANONICAL status was accepted — enum guard failed")
    except sqlite3.IntegrityError:
        conn.rollback()
        print("  ok  CHECK rejects invented CANONICAL status")

    conn.close()

    # -- 9. shipped DB, read-only inspection ---------------------------------
    print("\n[9] shipped database (read-only)")
    if os.path.exists(SHIPPED_DB):
        ro = sqlite3.connect(f"file:{SHIPPED_DB}?mode=ro", uri=True)
        shipped = {r[0] for r in ro.execute(
            "SELECT name FROM sqlite_master WHERE type='table'")}
        missing = [t for t in REQUIRED_TABLES if t not in shipped]
        counts = {t: ro.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
                  for t in REQUIRED_TABLES}
        ro.close()
        check(missing == [], f"shipped DB has all tables ({SHIPPED_DB})")
        print(f"  --  shipped row counts: {counts}")
    else:
        print(f"  --  shipped DB not present yet ({SHIPPED_DB}); "
              "run ingest_baseline.py to create it")

    print("\nSMOKE TEST PASSED")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:  # noqa: BLE001 - smoke test must report and fail loudly
        traceback.print_exc()
        print("\nSMOKE TEST FAILED", file=sys.stderr)
        sys.exit(1)
