#!/usr/bin/env python3
"""Stage 5 smoke test — run analysis on a throwaway copy of the Stage 3 store.

Exits 0 only if every assertion passes.  It never writes to the Stage 3 store
or to the Mac corpus; all work happens in a temporary directory inside this
Stage 5 workspace, removed on exit.

What it proves
--------------
1. ``engine.py run`` completes and writes >= 1 proposal, each with provenance.
2. No CANONICAL value appears in any status/confidence column or engine text.
3. ``source_document`` row count and digest are unchanged; the Stage 3 store's
   sha256 is unchanged; the Mac corpus fingerprint is unchanged.
4. Engine rows carry status PROPOSED/WORKING only and are attributable.
5. Re-running is idempotent (stable ids, stable row counts, stable run ids).
6. ``list-proposals`` / ``show`` work; ``--dry-run`` commits nothing.
7. The durable-message analyzer works when messages exist (synthetic fixture).
8. ``--db`` inside the Mac corpus is refused; ``--llm`` defaults off and exits 0.
"""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import sqlite3
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ENGINE = os.path.join(HERE, "engine.py")
STAGE3_DB = "/Users/archcore/solbian/codex-phase-i-stage3/codex_phase_i.sqlite"
MAC_CORPUS = "/Users/archcore/solbian/codex"

ALLOWED_STATUS = {"PROPOSED", "WORKING"}

FAILURES: list[str] = []
CHECKS = 0


def check(condition: bool, label: str) -> None:
    global CHECKS
    CHECKS += 1
    if condition:
        print(f"  ok   {label}")
    else:
        print(f"  FAIL {label}")
        FAILURES.append(label)


def run_cli(db: str, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, ENGINE, "--db", db, *args],
        cwd=HERE, capture_output=True, text=True,
    )


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def corpus_fingerprint() -> list:
    """mtime/size fingerprint of the Mac corpus root (must never change)."""
    out = []
    if not os.path.exists(MAC_CORPUS):
        return out
    st = os.stat(MAC_CORPUS)
    out.append((MAC_CORPUS, st.st_mtime_ns, st.st_size))
    for name in sorted(os.listdir(MAC_CORPUS))[:12]:
        path = os.path.join(MAC_CORPUS, name)
        try:
            st = os.stat(path)
        except OSError:
            continue
        out.append((name, st.st_mtime_ns, st.st_size))
    return out


def src_digest(conn: sqlite3.Connection) -> tuple[int, str]:
    h = hashlib.sha1()
    n = 0
    for row in conn.execute(
        "SELECT id, rel_path, status, updated_at FROM source_document ORDER BY id"
    ):
        n += 1
        h.update(("\x1f".join(str(x) for x in row)).encode())
        h.update(b"\x1e")
    return n, h.hexdigest()


def scalar(conn: sqlite3.Connection, sql: str, params=()):
    return conn.execute(sql, params).fetchone()[0]


def tables(conn: sqlite3.Connection) -> list[str]:
    return [r[0] for r in conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
    )]


ENGINE_TABLES = ("proposal", "concept", "relationship", "provenance_link", "analysis_run")


def assert_no_canonical(conn: sqlite3.Connection) -> None:
    """No CANONICAL status anywhere; no uppercase CANONICAL in engine text."""
    bad = []
    for table in tables(conn):
        for col in conn.execute(f"PRAGMA table_info({table})"):
            name = col[1]
            if name in ("status", "confidence", "inventory_status", "classification"):
                n = scalar(conn, f"SELECT COUNT(*) FROM {table} WHERE {name}='CANONICAL'")
                if n:
                    bad.append(f"{table}.{name}")
            # engine-created text must not even mention the uppercase word
            if table in ENGINE_TABLES and (col[2] or "").upper().startswith("TEXT"):
                n = scalar(
                    conn, f"SELECT COUNT(*) FROM {table} WHERE instr({name},'CANONICAL')>0"
                )
                if n:
                    bad.append(f"{table}.{name}(text)")
    check(not bad, "no CANONICAL value anywhere in the store" + (f" -> {bad}" if bad else ""))


def main() -> int:
    print("Stage 5 smoke — deterministic engine")
    print(f"engine : {ENGINE}")
    print(f"SoT    : {STAGE3_DB} (read-only)")

    sot_hash_before = sha256_file(STAGE3_DB)
    mac_before = corpus_fingerprint()

    tone = sqlite3.connect(f"file:{STAGE3_DB}?mode=ro", uri=True)
    sot_count = scalar(tone, "SELECT COUNT(*) FROM source_document")
    tone.close()

    tmp = tempfile.mkdtemp(prefix="stage5_smoke_", dir=HERE)
    db1 = os.path.join(tmp, "db1.sqlite")
    db2 = os.path.join(tmp, "db2.sqlite")
    db3 = os.path.join(tmp, "db3.sqlite")
    try:
        # ------------------------------------------------------------------ #
        print("\n[1] first run")
        proc = run_cli(db1, "run")
        check(proc.returncode == 0, f"engine run exit 0 (got {proc.returncode})")
        if proc.returncode != 0:
            print(proc.stdout)
            print(proc.stderr, file=sys.stderr)

        conn = sqlite3.connect(db1)
        conn.row_factory = sqlite3.Row
        n_props = scalar(conn, "SELECT COUNT(*) FROM proposal")
        check(n_props >= 1, f"at least one proposal written (got {n_props})")

        # every proposal links to a source_document and/or message
        no_prov = [r[0] for r in conn.execute(
            "SELECT p.id FROM proposal p WHERE NOT EXISTS ("
            "  SELECT 1 FROM provenance_link v WHERE v.subject_kind='proposal'"
            "  AND v.subject_id=p.id AND v.source_kind IN ('source_document','message'))"
        )]
        check(not no_prov, f"every proposal has source provenance ({len(no_prov)} missing)")

        # every concept links to a source
        no_cprov = [r[0] for r in conn.execute(
            "SELECT c.id FROM concept c WHERE NOT EXISTS ("
            "  SELECT 1 FROM provenance_link v WHERE v.subject_kind='concept'"
            "  AND v.subject_id=c.id AND v.source_kind IN ('source_document','message'))"
        )]
        check(not no_cprov, f"every concept has source provenance ({len(no_cprov)} missing)")

        # statuses restricted
        bad_status = []
        for table in ("proposal", "concept", "relationship", "provenance_link"):
            for r in conn.execute(f"SELECT DISTINCT status FROM {table}"):
                if r[0] not in ALLOWED_STATUS:
                    bad_status.append(f"{table}:{r[0]}")
        check(not bad_status, f"only PROPOSED/WORKING statuses written -> {bad_status}")

        # attribution marker present on engine proposals/concepts
        unattributed = scalar(
            conn, "SELECT COUNT(*) FROM proposal WHERE attribution NOT LIKE 'engine:stage5:%'"
        ) + scalar(
            conn, "SELECT COUNT(*) FROM concept WHERE attribution NOT LIKE 'engine:stage5:%'"
        )
        check(unattributed == 0, "all engine rows are attributable to engine:stage5:*")

        assert_no_canonical(conn)

        # source_document untouched
        n_after, dig_after = src_digest(conn)
        check(n_after == sot_count, f"source_document count unchanged ({n_after} == {sot_count})")

        # analysis_run coverage
        n_runs = scalar(conn, "SELECT COUNT(*) FROM analysis_run")
        check(n_runs >= 4, f"analysis_run rows recorded (got {n_runs})")
        durable = conn.execute(
            "SELECT summary_json, status FROM analysis_run WHERE kind='durable'"
        ).fetchone()
        check(durable is not None and durable["status"] == "OK",
              "durable analyzer recorded OK (0 messages -> skipped, no crash)")
        if durable:
            check("no message rows" in (durable["summary_json"] or ""),
                  "durable correctly reports empty conversation store")

        run_ids_1 = {r[0] for r in conn.execute("SELECT id FROM analysis_run")}
        prop_ids_1 = {r[0] for r in conn.execute("SELECT id FROM proposal")}
        concept_ids_1 = {r[0] for r in conn.execute("SELECT id FROM concept")}
        counts_1 = (
            n_props,
            scalar(conn, "SELECT COUNT(*) FROM concept"),
            scalar(conn, "SELECT COUNT(*) FROM relationship"),
            scalar(conn, "SELECT COUNT(*) FROM provenance_link"),
        )
        conn.close()

        # ------------------------------------------------------------------ #
        print("\n[2] re-run is idempotent")
        proc = run_cli(db1, "run")
        check(proc.returncode == 0, "second run exit 0")
        conn = sqlite3.connect(db1)
        conn.row_factory = sqlite3.Row
        prop_ids_2 = {r[0] for r in conn.execute("SELECT id FROM proposal")}
        concept_ids_2 = {r[0] for r in conn.execute("SELECT id FROM concept")}
        run_ids_2 = {r[0] for r in conn.execute("SELECT id FROM analysis_run")}
        counts_2 = (
            scalar(conn, "SELECT COUNT(*) FROM proposal"),
            scalar(conn, "SELECT COUNT(*) FROM concept"),
            scalar(conn, "SELECT COUNT(*) FROM relationship"),
            scalar(conn, "SELECT COUNT(*) FROM provenance_link"),
        )
        check(prop_ids_1 == prop_ids_2, "proposal ids stable across re-run")
        check(concept_ids_1 == concept_ids_2, "concept ids stable across re-run")
        check(run_ids_1 == run_ids_2, "analysis_run ids stable across re-run")
        check(counts_1 == counts_2, f"row counts stable across re-run {counts_1} == {counts_2}")
        n_after2, dig_after2 = src_digest(conn)
        check(n_after2 == sot_count and dig_after2 == dig_after,
              "source_document still unchanged after re-run")
        conn.close()

        # ------------------------------------------------------------------ #
        print("\n[3] inspectors")
        proc = run_cli(db1, "list-proposals", "--json")
        ok_json = False
        if proc.returncode == 0:
            try:
                data = json.loads(proc.stdout)
                ok_json = isinstance(data, list) and len(data) >= 1
            except ValueError:
                ok_json = False
        check(proc.returncode == 0 and ok_json, "list-proposals --json returns proposals")

        sample_id = sorted(prop_ids_1)[0]
        proc = run_cli(db1, "show", sample_id)
        check(proc.returncode == 0 and sample_id in proc.stdout,
              "show <full id> prints the proposal")
        proc = run_cli(db1, "show", sample_id[:14])
        check(proc.returncode == 0 and sample_id[:14] in proc.stdout,
              "show <prefix> resolves the proposal")
        proc = run_cli(db1, "show", "does_not_exist_xyz")
        check(proc.returncode != 0, "show <unknown> fails closed")

        sample_cid = sorted(concept_ids_1)[0]
        proc = run_cli(db1, "show", sample_cid)
        check(proc.returncode == 0 and "CONCEPT" in proc.stdout,
              "show <concept id> resolves a concept (LIKE wildcards escaped)")
        proc = run_cli(db1, "show", "concept_under_")
        check(proc.returncode == 2 and "ambiguous" in proc.stderr,
              "show <ambiguous concept prefix> fails closed")

        proc = run_cli(db1, "list-runs")
        check(proc.returncode == 0 and "OK" in proc.stdout, "list-runs works")

        # ------------------------------------------------------------------ #
        print("\n[4] dry-run commits nothing")
        proc = run_cli(db2, "run", "--dry-run")
        check(proc.returncode == 0, "dry-run exit 0")
        conn = sqlite3.connect(db2)
        conn.row_factory = sqlite3.Row
        dry_total = sum(
            scalar(conn, f"SELECT COUNT(*) FROM {t}")
            for t in ("proposal", "concept", "relationship", "provenance_link", "analysis_run")
        )
        check(dry_total == 0, f"dry-run left no engine rows (got {dry_total})")
        conn.close()

        # ------------------------------------------------------------------ #
        print("\n[5] durable analyzer with a synthetic conversation fixture")
        shutil.copyfile(STAGE3_DB, db3)
        fconn = sqlite3.connect(db3)
        fconn.execute("PRAGMA foreign_keys = ON")
        body_text = (
            "Synthetic smoke fixture message. " * 12
            + "This paragraph is intentionally long so the durable-candidate "
              "heuristic (>=280 characters) has something to extract."
        )
        now = "2026-09-21T00:00:00+00:00"
        fconn.execute(
            "INSERT INTO conversation (id, title, participants, status, started_at, "
            "notes, attribution, created_at, updated_at) "
            "VALUES ('conv_smoke','Smoke fixture','[\"jd\",\"solace\"]','WORKING',?,"
            "'synthetic test fixture, not corpus data','smoke',?,?)",
            (now, now, now),
        )
        fconn.execute(
            "INSERT INTO message (id, conversation_id, seq, role, body, sent_at, "
            "source_path, status, created_at, updated_at) "
            "VALUES ('msg_smoke_1','conv_smoke',1,'jd',?,?,NULL,'WORKING',?,?)",
            (body_text, now, now, now),
        )
        fconn.commit()
        conv_before = scalar(fconn, "SELECT COUNT(*) FROM conversation")
        fconn.close()

        proc = run_cli(db3, "run", "--kind", "durable")
        check(proc.returncode == 0, "durable-only run exit 0 with messages present")
        conn = sqlite3.connect(db3)
        conn.row_factory = sqlite3.Row
        check(scalar(conn, "SELECT COUNT(*) FROM proposal") >= 1,
              "long message produced a durable-candidate proposal")
        hit = conn.execute(
            "SELECT v.id, v.confidence, p.body FROM provenance_link v "
            "JOIN proposal p ON p.id = v.subject_id "
            "WHERE v.subject_kind='proposal' AND v.source_kind='message' "
            "AND v.source_id='msg_smoke_1'"
        ).fetchone()
        check(hit is not None, "durable proposal links to the message")
        check(hit is not None and hit["confidence"] == "TEXT-SUPPORTED",
              "durable message evidence is TEXT-SUPPORTED (quote stored)")
        check(hit is not None and "INTERPRETATION" in (hit["body"] or ""),
              "durable proposal is labelled INTERPRETATION")
        check(scalar(conn, "SELECT COUNT(*) FROM conversation") == conv_before,
              "engine did not add/remove conversations")
        conn.close()

        # ------------------------------------------------------------------ #
        print("\n[6] guards")
        evil = os.path.join(MAC_CORPUS, "stage5_should_not_exist.sqlite")
        proc = run_cli(evil, "run")
        check(proc.returncode != 0 and not os.path.exists(evil),
              "engine refuses --db inside the Mac corpus")
        check("Mac corpus" in (proc.stderr + proc.stdout),
              "refusal names the Mac corpus")

        proc = run_cli(db1, "run", "--kind", "plurality", "--llm")
        check(proc.returncode == 0, "--llm defaults off and still exits 0")

        # ------------------------------------------------------------------ #
        print("\n[7] outside-world invariants")
        check(sha256_file(STAGE3_DB) == sot_hash_before,
              "Stage 3 SoT store byte-identical (sha256 unchanged)")
        check(corpus_fingerprint() == mac_before,
              "Mac corpus fingerprint unchanged (never written)")
        return 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    try:
        rc = main()
    finally:
        print()
        if FAILURES:
            print(f"SMOKE FAILED: {len(FAILURES)} of {CHECKS} checks failed")
            for f in FAILURES:
                print(f"  - {f}")
        else:
            print(f"SMOKE PASSED: {CHECKS}/{CHECKS} checks")
    raise SystemExit(1 if FAILURES else 0)
