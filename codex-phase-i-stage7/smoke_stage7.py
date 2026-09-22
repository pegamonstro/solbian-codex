#!/usr/bin/env python3
"""Stage 7 living-loop acceptance smoke.

Runs the whole loop on a **throwaway** living store (a copy of the Stage 4
living store / Stage 3 SoT), then proves the Stage 4 UI changes work by
installing the staged Stage 4 build into a private overlay and running its
extended ``smoke_ui.py`` there.

Checks, in order:

  1. one-time seed of the Stage 5 engine tables into the living store
  2. preserved Solace message -> durable engine run -> PROPOSED proposal
  3. explicit accept -> WORKING codex_document + revision + copied provenance
  4. WORKING document is browsable and the proposal is marked accepted
  5. ``living_loop.py once`` exits 0
  6. the staged Stage 4 ``smoke_ui.py`` exits 0 (overlay install)
  7. no CANONICAL anywhere; Stage 3/5 stores byte-identical; Mac corpus untouched

    python3 smoke_stage7.py
"""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile

import living_loop
import living_store as ls

HERE = os.path.dirname(os.path.abspath(__file__))
BUILD_DIR = os.path.join(HERE, "_stage4_build")
STAGE4_DIR = os.environ.get("SOLBIAN_STAGE4_DIR",
                            "/Users/archcore/solbian/codex-phase-i-stage4")
MAC_CORPUS = "/Users/archcore/solbian/codex"
STAGE5_ENGINE = os.path.join(os.path.dirname(HERE), "codex-phase-i-stage5", "engine.py")

LONG_BODY = (
    "Stage 7 smoke fixture: a preserved JD message long enough for the durable "
    "analyzer. The loop must keep this as conversation material, propose it, and "
    "only turn it into WORKING Codex content after an explicit accept. It must "
    "never become CANONICAL and must never touch the historical corpus. "
    + ("provenance-preserving-dialogue " * 8)
)

RESULTS: list[tuple[str, bool, str]] = []


def check(name: str, ok: bool, detail: str = "") -> None:
    RESULTS.append((name, bool(ok), detail))
    print(("PASS  " if ok else "FAIL  ") + name + ("" if ok or not detail else f"  — {detail}"))


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def corpus_fingerprint() -> list:
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


def insert_conversation(conn, conv_id: str, msg_id: str, body: str) -> None:
    ts = ls.now_iso()
    conn.execute(
        """INSERT OR IGNORE INTO conversation
             (id, title, participants, status, started_at, notes, attribution,
              created_at, updated_at)
           VALUES (?, ?, ?, 'WORKING', ?, ?, 'stage7 smoke_stage7.py', ?, ?)""",
        (conv_id, "Stage 7 smoke", json.dumps(["jd", "solace"]), ts,
         "throwaway living-store fixture", ts, ts))
    seq = conn.execute(
        "SELECT COALESCE(MAX(seq), 0) + 1 FROM message WHERE conversation_id = ?",
        (conv_id,)).fetchone()[0]
    conn.execute(
        """INSERT OR IGNORE INTO message
             (id, conversation_id, seq, role, body, sent_at, source_path, status,
              created_at, updated_at)
           VALUES (?, ?, ?, 'jd', ?, ?, NULL, 'WORKING', ?, ?)""",
        (msg_id, conv_id, seq, body, ts, ts, ts))
    conn.commit()


def run_living_loop_case(tmpdir: str) -> tuple[str | None, str | None]:
    """Steps 1-4 on a throwaway living store. Returns (proposal_id, doc_id)."""
    seed = ls.LIVING_DB if os.path.exists(ls.LIVING_DB) else ls.STAGE3_DB
    db = os.path.join(tmpdir, "living.sqlite")
    shutil.copyfile(seed, db)
    check("throwaway living store created", os.path.isfile(db), db)

    conv_id, msg_id = "conv_stage7_smoke", "msg_stage7_smoke"
    with ls.connect(db) as conn:
        tables = ls.table_names(conn)
        check("living store starts without analysis_run (un-migrated)",
              "analysis_run" not in tables)
        summary = ls.migrate(conn, ls.STAGE5_DB)
        check("one-time Stage 5 seed ran", summary.get("seeded") is True,
              str(summary.get("reason")))
        check("seed copied proposal rows",
              summary.get("copied", {}).get("proposal", 0) >= 1,
              str(summary.get("copied")))
        check("seed copied analysis_run rows",
              summary.get("copied", {}).get("analysis_run", 0) >= 1,
              str(summary.get("copied")))
        check("analysis_run table now exists", "analysis_run" in ls.table_names(conn))
        # re-run is a no-op
        again = ls.migrate(conn, ls.STAGE5_DB)
        check("second migrate is a no-op", again.get("seeded") is False,
              str(again.get("reason")))

        insert_conversation(conn, conv_id, msg_id, LONG_BODY)
        check("preserved Solace message inserted",
              ls.scalar(conn, "SELECT COUNT(*) FROM message WHERE id=?", (msg_id,)) == 1)

    run = ls.run_engine(db, kinds=["durable", "discussion"])
    check("engine durable run exits 0", run["returncode"] == 0,
          (run.get("stderr") or "")[:200])

    proposal_id = None
    with ls.connect(db) as conn:
        props = living_loop.proposals_for_source(conn, "message", msg_id)
        check("durable analyzer proposed the message", len(props) >= 1,
              f"proposals={len(props)}")
        if props:
            proposal_id = props[0]["id"]
            check("proposal is PROPOSED", props[0]["status"] == "PROPOSED",
                  str(props[0]["status"]))
            prov = conn.execute(
                "SELECT source_kind, confidence FROM provenance_link "
                "WHERE subject_kind='proposal' AND subject_id=? "
                "AND source_kind='message' AND source_id=?",
                (proposal_id, msg_id)).fetchall()
            check("proposal provenance links the message", len(prov) >= 1)
            check("message evidence is TEXT-SUPPORTED",
                  bool(prov) and prov[0]["confidence"] == "TEXT-SUPPORTED")

    doc_id = None
    if proposal_id:
        with ls.connect(db) as conn:
            result = ls.accept_proposal(conn, proposal_id, actor="smoke_stage7.py")
            doc = result["codex_document"]
            doc_id = doc["id"]
            check("consolidation produced a WORKING codex_document",
                  doc["status"] == "WORKING", str(doc["status"]))
            check("consolidation never writes CANONICAL",
                  doc["status"] != ls.CANONICAL)
            check("revision row links the proposal",
                  result["revision"].get("proposal_id") == proposal_id)
            check("provenance copied onto the codex_document",
                  ls.scalar(conn,
                            "SELECT COUNT(*) FROM provenance_link "
                            "WHERE subject_kind='codex_document' AND subject_id=?",
                            (doc_id,)) >= 1)
            check("provenance copied onto the revision",
                  ls.scalar(conn,
                            "SELECT COUNT(*) FROM provenance_link "
                            "WHERE subject_kind='revision' AND subject_id=?",
                            (result["revision"]["id"],)) >= 1)
            check("proposal marked accepted (WORKING)",
                  ls.scalar(conn, "SELECT status FROM proposal WHERE id=?",
                            (proposal_id,)) == "WORKING")
            # idempotent
            again = ls.accept_proposal(conn, proposal_id, actor="smoke_stage7.py")
            check("re-accept is idempotent", again["already_accepted"] is True)
            check("codex_document count did not double",
                  ls.scalar(conn, "SELECT COUNT(*) FROM codex_document") == 1)

            listing = ls.list_codex_documents(conn, {"limit": ["50"]})
            check("WORKING document is browsable",
                  any(d["id"] == doc_id for d in listing["codex_documents"]))
            detail = ls.codex_document_detail(conn, doc_id)
            check("document detail exposes copied message provenance",
                  any(v["source_kind"] == "message" and v["source_id"] == msg_id
                      for v in detail["provenance"]))
            check("no CANONICAL anywhere in the living store",
                  not ls.scan_canonical(conn), str(ls.scan_canonical(conn)))
    return proposal_id, doc_id


def run_cli_once() -> None:
    cmd = [sys.executable, os.path.join(HERE, "living_loop.py"), "once"]
    proc = subprocess.run(cmd, cwd=HERE, capture_output=True, text=True, timeout=300)
    check("living_loop.py once exits 0", proc.returncode == 0,
          (proc.stderr or proc.stdout)[-300:])


def build_overlay(dest: str) -> None:
    shutil.copytree(STAGE4_DIR, dest, dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".git"))
    for rel in ("app.py", "smoke_ui.py", "static/index.html", "static/app.js",
                "static/style.css"):
        src = os.path.join(BUILD_DIR, rel)
        dst = os.path.join(dest, rel)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copyfile(src, dst)
    shutil.copyfile(os.path.join(HERE, "living_store.py"),
                    os.path.join(dest, "living_store.py"))


def run_stage4_smoke(tmpdir: str) -> None:
    overlay = os.path.join(tempfile.mkdtemp(prefix="stage4_overlay_", dir=tmpdir),
                           "stage4")
    build_overlay(overlay)
    check("staged Stage 4 overlay built", os.path.isfile(os.path.join(overlay, "app.py")))
    proc = subprocess.run([sys.executable, "smoke_ui.py"], cwd=overlay,
                          capture_output=True, text=True, timeout=600)
    ok = proc.returncode == 0 and "SMOKE UI PASSED" in proc.stdout
    detail = ""
    if not ok:
        tail = (proc.stdout or "")[-1500:] + "\n" + (proc.stderr or "")[-800:]
        detail = tail.replace("\n", " | ")[:600]
    check("staged Stage 4 smoke_ui.py exits 0", ok, detail)
    if ok:
        for line in proc.stdout.splitlines():
            if line.startswith("SMOKE UI PASSED"):
                print("      " + line.strip())

    # If Stage 4 has actually been installed in place, verify it directly too.
    in_place_app = os.path.join(STAGE4_DIR, "app.py")
    try:
        with open(in_place_app, "r", encoding="utf-8", errors="replace") as fh:
            installed = "living_store" in fh.read()
    except OSError:
        installed = False
    if installed:
        proc2 = subprocess.run([sys.executable, "smoke_ui.py"], cwd=STAGE4_DIR,
                               capture_output=True, text=True, timeout=600)
        check("installed Stage 4 smoke_ui.py exits 0",
              proc2.returncode == 0 and "SMOKE UI PASSED" in proc2.stdout,
              (proc2.stdout or "")[-300:])
    else:
        print("NOTE  Stage 4 not installed in place (read-only sandbox); "
              "run apply_to_stage4.sh with write access")


def main() -> int:
    print("Stage 7 smoke — living loop")
    print(f"living store policy: {ls.LIVING_DB}")

    stage3_hash = sha256_file(ls.STAGE3_DB)
    stage5_hash = sha256_file(ls.STAGE5_DB) if os.path.exists(ls.STAGE5_DB) else None
    mac_before = corpus_fingerprint()

    tmpdir = tempfile.mkdtemp(prefix=".stage7_smoke_", dir=HERE)
    try:
        print("\n[1-4] full loop on a throwaway living store")
        proposal_id, doc_id = run_living_loop_case(tmpdir)
        check("full loop produced a proposal and a WORKING document",
              bool(proposal_id) and bool(doc_id))

        print("\n[5] CLI helper")
        run_cli_once()

        print("\n[6] staged Stage 4 extended smoke")
        run_stage4_smoke(tmpdir)

        print("\n[7] outside-world invariants")
        check("Stage 3 SoT store byte-identical (sha256 unchanged)",
              sha256_file(ls.STAGE3_DB) == stage3_hash)
        if stage5_hash is not None:
            check("Stage 5 seed store byte-identical (sha256 unchanged)",
                  sha256_file(ls.STAGE5_DB) == stage5_hash)
        check("Mac corpus fingerprint unchanged (never written)",
              corpus_fingerprint() == mac_before)
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)

    passed = sum(1 for _, ok, _ in RESULTS if ok)
    failed = [(n, d) for n, ok, d in RESULTS if not ok]
    print()
    if failed:
        print(f"SMOKE STAGE7 FAILED — {passed}/{len(RESULTS)} checks passed")
        for name, detail in failed:
            print(f"  - {name}" + (f": {detail}" if detail else ""))
        return 1
    print(f"SMOKE STAGE7 PASSED — {passed}/{len(RESULTS)} checks")
    return 0


if __name__ == "__main__":
    sys.exit(main())
