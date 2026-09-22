#!/usr/bin/env python3
"""Stage 4 (+ Stage 7 living loop) HTTP smoke test.

Boots ``app.py`` on an ephemeral port against a throwaway copy of the living
store, exercises the Solace, Codex and Engine endpoints over real HTTP, then
walks the full living loop:

    Solace long message -> durable engine run (auto) -> PROPOSED proposal
        -> explicit Accept -> WORKING codex_document + revision + provenance
        -> Codex browse shows the WORKING document

Asserts the read-only guarantees (``source_document`` untouched, no
``CANONICAL`` anywhere, Mac corpus untouched, Stage 3 SoT byte-identical),
then kills the server.  Exits 0 only if every check passes.

    python3 smoke_ui.py
"""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import socket
import sqlite3
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
APP = os.path.join(HERE, "app.py")
DEFAULT_DB = os.path.join(HERE, "data", "codex_phase_i.sqlite")
STAGE3_DB = "/Users/archcore/solbian/codex-phase-i-stage3/codex_phase_i.sqlite"
STAGE5_DB = "/Users/archcore/solbian/codex-phase-i-stage5/data/codex_phase_i.sqlite"
MAC_CORPUS = "/Users/archcore/solbian/codex"

RESULTS: list[tuple[str, bool, str]] = []
SOURCE_SNAPSHOT: list = []

LONG_MESSAGE = (
    "Stage 7 living-loop smoke fixture. This deliberately long JD message is "
    "preserved conversation material: the durable analyzer promotes it to a "
    "PROPOSED proposal, and only an explicit accept may turn it into WORKING "
    "Codex content. Nothing here is ever CANONICAL, and the historical corpus "
    "is never written. Padding so the message clears the durable length floor: "
    + ("dialogue-preservation " * 8)
)

# Stage 5b hybrid smoke target: this conversation exists in the Stage 4 living
# store (copied throwaway) with the turn material the deterministic extractor
# turns into PROPOSED candidates, including hidden ``Theme:*`` rows.
TARGET_CONV = "conv_5bbf3990a8ce4b47"


def check(name: str, ok: bool, detail: str = "") -> None:
    RESULTS.append((name, bool(ok), detail))
    print(("PASS  " if ok else "FAIL  ") + name + ("" if ok or not detail else f"  — {detail}"))


def free_port() -> int:
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()
    return port


def request(method: str, url: str, body=None, timeout: float = 30.0):
    data = None
    if body is not None:
        data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Accept", "application/json")
    if data is not None:
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, resp.read(), dict(resp.headers)
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read(), dict(exc.headers)


def jget(url: str):
    status, raw, _ = request("GET", url)
    try:
        return status, json.loads(raw.decode("utf-8"))
    except (ValueError, UnicodeDecodeError):
        return status, None


def jget_post(url: str, body):
    status, raw, _ = request("POST", url, body=body)
    try:
        return status, json.loads(raw.decode("utf-8"))
    except (ValueError, UnicodeDecodeError):
        return status, None


def jget_asset(base: str, name: str):
    status, raw, headers = request("GET", base + "/static/" + name)
    return status, headers


def wait_for_server(base: str, proc: subprocess.Popen, timeout: float = 40.0) -> bool:
    deadline = time.time() + timeout
    while time.time() < deadline:
        if proc.poll() is not None:
            return False
        try:
            status, _ = jget(base + "/healthz")
            if status == 200:
                return True
        except (urllib.error.URLError, ConnectionError, OSError):
            pass
        time.sleep(0.15)
    return False


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


def snapshot_source_documents(db_path: str):
    conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    try:
        return conn.execute(
            """SELECT id, corpus_root_id, rel_path, media_type, byte_size, mtime, sha256,
                      probable_role, inventory_status, status, plurality_flags, notes,
                      attribution, created_at, updated_at
               FROM source_document ORDER BY id"""
        ).fetchall()
    finally:
        conn.close()


def snapshot_proposals(db_path: str):
    conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    try:
        return conn.execute(
            """SELECT id, status, summary, body, based_on_json, attribution,
                      created_at, updated_at
               FROM proposal ORDER BY id"""
        ).fetchall()
    finally:
        conn.close()


def snapshot_messages(db_path: str, conv_id: str):
    conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    try:
        return [tuple(r) for r in conn.execute(
            """SELECT id, conversation_id, seq, role, body, status, created_at, updated_at
               FROM message WHERE conversation_id = ? ORDER BY seq, id""",
            (conv_id,)).fetchall()]
    finally:
        conn.close()


def count_proposals(db_path: str, where: str = "", params=()) -> int:
    conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    try:
        return conn.execute(
            f"SELECT COUNT(*) FROM proposal {where}", params).fetchone()[0]
    finally:
        conn.close()


def assert_no_canonical(db_path: str, label: str) -> None:
    conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    try:
        tables = [r[0] for r in conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' "
            "AND name NOT LIKE 'sqlite_%'")]
        bad = []
        for table in tables:
            cols = [r[1] for r in conn.execute(f"PRAGMA table_info({table})")]
            for col in cols:
                if col in ("status", "confidence", "inventory_status", "classification"):
                    n = conn.execute(
                        f"SELECT COUNT(*) FROM {table} WHERE {col}='CANONICAL'").fetchone()[0]
                    if n:
                        bad.append(f"{table}.{col}")
        check(f"{label}: no CANONICAL value anywhere",
              not bad, ("offenders=" + ",".join(bad)) if bad else "")
    finally:
        conn.close()


def ensure_working_db() -> str:
    if os.path.exists(DEFAULT_DB):
        return DEFAULT_DB
    print("[smoke] working store missing — building it (setup_db.build) ...")
    import setup_db
    setup_db.build(DEFAULT_DB, quiet=True)
    return DEFAULT_DB


def main() -> int:
    global SOURCE_SNAPSHOT
    source_db = ensure_working_db()
    live_db_hash = sha256_file(DEFAULT_DB)
    tmpdir = tempfile.mkdtemp(prefix="stage4_smoke_")
    tmp_db = os.path.join(tmpdir, "smoke.sqlite")
    shutil.copy2(source_db, tmp_db)
    SOURCE_SNAPSHOT = snapshot_source_documents(tmp_db)

    stage3_hash = sha256_file(STAGE3_DB)
    stage5_hash = sha256_file(STAGE5_DB) if os.path.exists(STAGE5_DB) else None
    mac_before = corpus_fingerprint()

    log_path = os.path.join(tmpdir, "server.log")
    port = free_port()
    base = f"http://127.0.0.1:{port}"
    env = dict(os.environ, PYTHONUNBUFFERED="1")
    # Force the optional-LLM path to fail closed deterministically unless the
    # caller explicitly opted into a live-LLM smoke run or the engine mock.
    #   SOLBIAN_LLM_SMOKE=1 -> real configured endpoint
    #   SOLBIAN_LLM_MOCK=1  -> engine's deterministic mock LLM (reachable branch)
    if (os.getenv("SOLBIAN_LLM_SMOKE") not in ("1", "true", "yes")
            and os.getenv("SOLBIAN_LLM_MOCK") not in ("1", "true", "yes")):
        env["SOLBIAN_LLM_BASE"] = "http://127.0.0.1:9/v1"
        env["SOLBIAN_LLM_TIMEOUT"] = "2"
    # Stage 7: one living store — the engine surface points at the same DB.
    cmd = [sys.executable, APP, "--port", str(port), "--db", tmp_db,
           "--engine-db", tmp_db, "--no-setup"]
    logf = open(log_path, "wb")
    proc = subprocess.Popen(cmd, cwd=HERE, stdout=logf, stderr=subprocess.STDOUT, env=env)

    try:
        up = wait_for_server(base, proc)
        check("server boots and /healthz returns 200", up,
              "server did not become ready" if not up else "")
        if up:
            run_checks(base, tmp_db)
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=6)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait(timeout=6)
        logf.close()
        check("server process stopped", proc.poll() is not None, f"poll={proc.poll()}")
        if not all(ok for _, ok, _ in RESULTS):
            try:
                with open(log_path, "r", encoding="utf-8", errors="replace") as fh:
                    tail = fh.read()[-3000:]
                if tail.strip():
                    print("\n--- server log tail ---")
                    print(tail)
            except OSError:
                pass

    # ---- outside-world invariants --------------------------------------
    check("Stage 3 SoT store byte-identical (sha256 unchanged)",
          sha256_file(STAGE3_DB) == stage3_hash)
    if stage5_hash is not None:
        check("Stage 5 seed store byte-identical (sha256 unchanged)",
              sha256_file(STAGE5_DB) == stage5_hash)
    check("live Stage 4 living DB byte-identical (sha256 unchanged)",
          sha256_file(DEFAULT_DB) == live_db_hash,
          f"{live_db_hash} != {sha256_file(DEFAULT_DB)}")
    check("Mac corpus fingerprint unchanged (never written)",
          corpus_fingerprint() == mac_before)

    shutil.rmtree(tmpdir, ignore_errors=True)

    passed = sum(1 for _, ok, _ in RESULTS if ok)
    failed = [(n, d) for n, ok, d in RESULTS if not ok]
    print()
    if failed:
        print(f"SMOKE UI FAILED — {passed}/{len(RESULTS)} checks passed")
        for name, detail in failed:
            print(f"  - {name}" + (f": {detail}" if detail else ""))
        return 1
    print(f"SMOKE UI PASSED — {passed}/{len(RESULTS)} checks")
    return 0


def run_checks(base: str, tmp_db: str) -> None:
    # ---- static shell ---------------------------------------------------
    status, raw, _ = request("GET", base + "/")
    html = raw.decode("utf-8", "replace")
    check("GET / returns 200", status == 200, f"status={status}")
    check("page has all three tabs",
          "Solace" in html and "Codex Solbian" in html and 'data-tab="engine"' in html)
    check("page states CANONICAL: NONE", "CANONICAL: NONE" in html)
    low = html.lower()
    check("page has no canonical form control",
          'name="canonical"' not in low and 'id="canonical"' not in low
          and "make_canonical" not in low and ">make canonical<" not in low)
    check("page shows the WORKING codex_document layer",
          "codex_document" in html and "WORKING" in html and "HISTORICAL" in html)
    check("page offers Run living loop + Accept controls",
          'id="engineRunLoop"' in html and "Accept" in html)
    check("page offers explicit hybrid synthesis controls",
          'id="synthDeterministic"' in html and 'id="synthLLM"' in html
          and "Synthesize dialogue" in html and "Draft with LLM" in html)
    check("page offers quiet Engine toggles (themes / all archaeology)",
          'id="eIncludeThemes"' in html and 'id="eAll"' in html)
    status, raw_js, _ = request("GET", base + "/static/app.js")
    js = raw_js.decode("utf-8", "replace")
    check("app.js wires the hybrid synthesize endpoint and quiet flags",
          "/api/engine/synthesize" in js and "include_themes" in js
          and "synthDeterministic" in js)
    for asset in ("style.css", "app.js"):
        s, _ = jget_asset(base, asset)
        check(f"GET /static/{asset} returns 200", s == 200, f"status={s}")

    # ---- meta / health --------------------------------------------------
    status, health = jget(base + "/healthz")
    check("GET /healthz -> 200 ok", status == 200 and health and health.get("ok") is True,
          f"status={status}")
    check("healthz reports CANONICAL NONE", bool(health) and health.get("canonical") == "NONE")
    doc_count = health.get("source_documents") if health else None
    check("source_document rows present", isinstance(doc_count, int) and doc_count > 0,
          f"count={doc_count}")
    check("healthz points engine at the living store",
          bool(health) and os.path.abspath(health.get("living_db", "")) == os.path.abspath(tmp_db)
          and health.get("engine_is_living_store") is True)

    status, meta = jget(base + "/api/meta")
    check("GET /api/meta -> 200", status == 200 and isinstance(meta, dict))
    if isinstance(meta, dict):
        check("meta writable tables are conversation+message only",
              sorted(meta.get("writable_tables", [])) == ["conversation", "message"],
              str(meta.get("writable_tables")))
        check("meta marks source_document read-only",
              "source_document" in (meta.get("read_only_tables") or []))
        check("meta count matches healthz",
              meta.get("counts", {}).get("source_document") == doc_count)
        check("meta names the living store",
              os.path.abspath(meta.get("living_db", "")) == os.path.abspath(tmp_db))
        check("meta declares consolidation tables",
              "codex_document" in (meta.get("consolidation_tables") or [])
              and "revision" in (meta.get("consolidation_tables") or []))
        check("meta declares CANONICAL NONE", meta.get("canonical") == "NONE")

    # ---- living store meta ---------------------------------------------
    status, living = jget(base + "/api/living/meta")
    check("GET /api/living/meta -> 200", status == 200 and isinstance(living, dict),
          f"status={status}")
    if isinstance(living, dict):
        check("living meta reports CANONICAL NONE", living.get("canonical") == "NONE")
        check("living store seeded proposals from Stage 5",
              (living.get("counts") or {}).get("proposal", 0) >= 1,
              str(living.get("counts")))
        check("living store records analysis_run rows",
              (living.get("counts") or {}).get("analysis_run", 0) >= 1)
        statuses = set(living.get("proposal_statuses") or [])
        check("living proposal statuses are PROPOSED/WORKING only",
              statuses <= {"PROPOSED", "WORKING"}, str(statuses))

    # ---- codex browse (HISTORICAL) -------------------------------------
    status, facets = jget(base + "/api/codex/facets")
    check("GET /api/codex/facets -> 200", status == 200 and isinstance(facets, dict))
    if isinstance(facets, dict):
        check("facets expose statuses", bool(facets.get("statuses")))
        check("facets expose corpus roots", bool(facets.get("corpus_roots")))
        statuses = [s.get("value") for s in (facets.get("statuses") or [])]
        check("no CANONICAL value exists in the data model",
              "CANONICAL" not in statuses, str(statuses))
        check("facets expose WORKING codex_document layer",
              "codex_total" in facets and "codex_kinds" in facets)

    status, listing = jget(base + "/api/codex/documents?limit=5")
    check("GET /api/codex/documents -> 200", status == 200 and isinstance(listing, dict))
    docs = (listing or {}).get("documents", [])
    check("document list respects limit", 0 < len(docs) <= 5, f"len={len(docs)}")
    check("document list reports a total", (listing or {}).get("total", 0) >= len(docs))
    first = docs[0] if docs else {}
    for key in ("id", "rel_path", "status", "corpus_root_path", "probable_role"):
        check(f"listed document carries '{key}'", key in first)

    if first:
        status, detail = jget(base + "/api/codex/documents/" + first["id"])
        doc = (detail or {}).get("document") if isinstance(detail, dict) else None
        check("GET document detail -> 200", status == 200 and isinstance(doc, dict))
        check("document detail is flagged read_only", bool(doc) and doc.get("read_only") is True)
        check("document detail includes a preview block",
              bool(doc) and isinstance(doc.get("preview"), dict))

    # text preview + mtime invariant
    status, text_listing = jget(base + "/api/codex/documents?limit=200&q=.md")
    candidates = (text_listing or {}).get("documents", []) if isinstance(text_listing, dict) else []
    preview_doc = next(
        (d for d in candidates
         if (d.get("byte_size") or 0) > 0
         and (d.get("media_type") or "").startswith("text/")),
        None,
    )
    if preview_doc is None:
        print("NOTE  no local text document found to preview; skipping preview assertions")
    else:
        abs_path = os.path.join(preview_doc["corpus_root_path"], preview_doc["rel_path"])
        if not os.path.isfile(abs_path):
            print(f"NOTE  corpus file not present locally: {abs_path}; skipping preview assertions")
        else:
            before = os.stat(abs_path).st_mtime_ns
            status, detail = jget(base + "/api/codex/documents/" + preview_doc["id"])
            preview = ((detail or {}).get("document") or {}).get("preview", {})
            after = os.stat(abs_path).st_mtime_ns
            check("text preview is available for a real corpus file",
                  status == 200 and preview.get("available") is True,
                  f"reason={preview.get('reason')}")
            check("text preview returns content", bool(preview.get("text")))
            check("text preview is flagged read-only", preview.get("read_only") is True)
            check("text preview honours the 200KB cap",
                  isinstance(preview.get("bytes_shown"), int)
                  and preview["bytes_shown"] <= 200 * 1024)
            check("previewing a corpus file does not change its mtime", before == after,
                  f"{before} != {after}")

    # ---- codex is read-only --------------------------------------------
    for method in ("POST", "PUT", "PATCH", "DELETE"):
        s, _, _ = request(method, base + "/api/codex/documents", body={"x": 1})
        check(f"{method} /api/codex/documents rejected (405)", s == 405, f"status={s}")
    if first:
        for method in ("PUT", "PATCH", "DELETE"):
            s, _, _ = request(method, base + "/api/codex/documents/" + first["id"], body={"x": 1})
            check(f"{method} /api/codex/documents/<id> rejected (405)", s == 405, f"status={s}")
    s, _, _ = request("POST", base + "/api/codex/canonical",
                      body={"id": first.get("id") if first else None})
    check("no canonical elevation endpoint exists", s == 405, f"status={s}")

    # ---- WORKING codex_document layer (initially empty) ----------------
    status, cd0 = jget(base + "/api/codex/codex-documents?limit=10")
    check("GET /api/codex/codex-documents -> 200",
          status == 200 and isinstance(cd0, dict), f"status={status}")
    check("WORKING codex_document listing reports CANONICAL NONE",
          (cd0 or {}).get("canonical") == "NONE")
    before_codex_total = (cd0 or {}).get("total", 0)

    # ---- engine read-only browse ---------------------------------------
    run_engine_checks(base, tmp_db)

    # ---- Stage 5b hybrid synthesis wiring ------------------------------
    run_hybrid_wiring_checks(base, tmp_db)
    run_live_llm_optional(base, tmp_db)

    # ---- engine: Run living loop ---------------------------------------
    status, loop = jget_post(base + "/api/engine/run", {})
    check("POST /api/engine/run -> 200",
          status == 200 and isinstance(loop, dict), f"status={status}")
    if isinstance(loop, dict):
        check("living loop ran and exited 0",
              loop.get("ran") is True and loop.get("returncode") == 0,
              f"rc={loop.get('returncode')}")
        check("living loop reports CANONICAL NONE", loop.get("canonical") == "NONE")
        check("living loop reports no canonical offenders", loop.get("no_canonical") is True)
        check("living loop ran against the living store",
              os.path.abspath(loop.get("living_db", "")) == os.path.abspath(tmp_db))
        check("living loop reports proposal totals",
              isinstance(loop.get("proposals_total"), int) and loop["proposals_total"] >= 1)

    # ---- solace write path + auto living loop --------------------------
    status, before_list = jget(base + "/api/solace/conversations")
    check("GET /api/solace/conversations -> 200",
          status == 200 and isinstance(before_list, dict))
    before_n = len((before_list or {}).get("conversations", []))
    check("conversation list is a list",
          isinstance((before_list or {}).get("conversations"), list))

    status, created = jget_post(base + "/api/solace/conversations",
                                {"title": "Stage 7 smoke", "participants": "jd, solace",
                                 "notes": "created by smoke_ui.py"})
    conv = (created or {}).get("conversation") if isinstance(created, dict) else None
    check("POST create conversation -> 201", status == 201 and bool(conv), f"status={status}")
    conv_id = (conv or {}).get("id")
    check("created conversation is WORKING", (conv or {}).get("status") == "WORKING")

    long_msg_id = None
    long_prop_id = None
    doc_id = None
    if conv_id:
        status, m1 = jget_post(f"{base}/api/solace/conversations/{conv_id}/messages",
                               {"role": "jd", "body": "Hello from the smoke test.",
                                "stub_reply": True})
        msg = (m1 or {}).get("message") if isinstance(m1, dict) else None
        reply = (m1 or {}).get("reply") if isinstance(m1, dict) else None
        check("POST jd message -> 201", status == 201 and bool(msg), f"status={status}")
        check("jd message role persisted", (msg or {}).get("role") == "jd")
        check("stub reply is appended and labelled WORKING",
              bool(reply) and reply.get("role") == "solace" and "WORKING" in (reply.get("body") or ""))
        check("short-message POST still reports a living-loop run",
              isinstance((m1 or {}).get("living_loop"), dict)
              and (m1 or {}).get("living_loop", {}).get("returncode") == 0)

        status, m2 = jget_post(f"{base}/api/solace/conversations/{conv_id}/messages",
                               {"role": "solace", "body": "A direct solace message."})
        check("POST solace message -> 201", status == 201 and (m2 or {}).get("message"),
              f"status={status}")

        # the long message is the durable candidate
        status, m3 = jget_post(f"{base}/api/solace/conversations/{conv_id}/messages",
                               {"role": "jd", "body": LONG_MESSAGE})
        lmsg = (m3 or {}).get("message") if isinstance(m3, dict) else None
        check("POST long jd message -> 201", status == 201 and bool(lmsg), f"status={status}")
        if lmsg:
            long_msg_id = lmsg.get("id")
            ll = (m3 or {}).get("living_loop") or {}
            check("posting a message runs the durable living loop",
                  ll.get("ran") is True and ll.get("returncode") == 0,
                  str(ll)[:200])
            check("durable living loop produced a new proposal",
                  (ll.get("new_proposals") or 0) >= 1, str(ll)[:200])
            check("message-path living loop reports CANONICAL NONE",
                  ll.get("canonical") == "NONE")

        status, bad = jget_post(f"{base}/api/solace/conversations/{conv_id}/messages",
                                {"role": "canonical", "body": "nope"})
        check("invalid message role rejected (400)", status == 400, f"status={status}")
        status, bad = jget_post(f"{base}/api/solace/conversations/{conv_id}/messages",
                                {"role": "jd", "body": "   "})
        check("empty message body rejected (400)", status == 400, f"status={status}")

        status, full = jget(f"{base}/api/solace/conversations/{conv_id}")
        conversation = (full or {}).get("conversation") if isinstance(full, dict) else None
        messages = (conversation or {}).get("messages", [])
        check("conversation detail returns messages", status == 200 and len(messages) >= 4,
              f"n={len(messages)}")
        seqs = [m.get("seq") for m in messages]
        check("messages are ordered by seq", seqs == sorted(seqs) and len(set(seqs)) == len(seqs))
        roles = {m.get("role") for m in messages}
        check("both jd and solace messages persisted", {"jd", "solace"} <= roles, str(roles))

        status, after_list = jget(base + "/api/solace/conversations")
        after_n = len((after_list or {}).get("conversations", []))
        check("conversation list grew by one", after_n == before_n + 1,
              f"{before_n} -> {after_n}")

    # ---- controlled consolidation --------------------------------------
    if long_msg_id:
        # The durable analyzer writes non-hybrid archaeology, which the quiet
        # Engine default intentionally hides; opt in with all=1 to find it.
        status, plist = jget(base + "/api/engine/proposals?all=1&limit=200&q=" + long_msg_id)
        props = (plist or {}).get("proposals", []) if isinstance(plist, dict) else []
        durable = [p for p in props if long_msg_id in (p.get("summary") or "")]
        check("durable proposal is listed for the long message", len(durable) >= 1,
              f"matches={len(durable)}")
        if durable:
            long_prop_id = durable[0]["id"]
            check("durable proposal is PROPOSED",
                  durable[0].get("status") == "PROPOSED", str(durable[0].get("status")))

            status, pdetail = jget(base + "/api/engine/proposals/" + long_prop_id)
            prop = (pdetail or {}).get("proposal") if isinstance(pdetail, dict) else None
            prov = (prop or {}).get("provenance", []) if prop else []
            msg_links = [v for v in prov
                         if v.get("source_kind") == "message" and v.get("source_id") == long_msg_id]
            check("proposal provenance links the preserved message", len(msg_links) >= 1,
                  f"links={len(msg_links)}")
            check("message provenance is TEXT-SUPPORTED",
                  bool(msg_links) and msg_links[0].get("confidence") == "TEXT-SUPPORTED")

            # explicit accept (controlled consolidation)
            status, acc = jget_post(
                base + f"/api/engine/proposals/{long_prop_id}/accept", {"actor": "smoke_ui"})
            check("POST accept proposal -> 200",
                  status == 200 and isinstance(acc, dict), f"status={status}")
            if isinstance(acc, dict):
                cd = acc.get("codex_document") or {}
                doc_id = cd.get("id")
                check("consolidation creates a WORKING codex_document",
                      cd.get("status") == "WORKING", str(cd.get("status")))
                check("consolidation uses WORKING, never CANONICAL",
                      cd.get("status") == "WORKING"
                      and acc.get("proposal_status") == "WORKING"
                      and acc.get("canonical") == "NONE")
                check("consolidation returns CANONICAL NONE", acc.get("canonical") == "NONE")
                check("consolidation records a revision",
                      bool((acc.get("revision") or {}).get("id")))
                check("consolidation copies provenance",
                      (acc.get("provenance_copied") or 0) >= 1)
                check("consolidation marks the proposal accepted (WORKING)",
                      acc.get("proposal_status") == "WORKING")

            # the WORKING document is browsable and read-only
            status, cdlist = jget(base + "/api/codex/codex-documents?limit=50")
            cdocs = (cdlist or {}).get("codex_documents", []) if isinstance(cdlist, dict) else []
            check("WORKING codex_document list grew",
                  (cdlist or {}).get("total", 0) >= before_codex_total + 1,
                  f"before={before_codex_total} after={(cdlist or {}).get('total')}")
            match = [d for d in cdocs if d.get("id") == doc_id]
            check("consolidated document appears in the WORKING list", bool(match))
            if match:
                check("consolidated document is labelled WORKING",
                      match[0].get("status") == "WORKING")

            if doc_id:
                status, cddetail = jget(base + "/api/codex/codex-documents/" + doc_id)
                cdoc = (cddetail or {}).get("codex_document") if isinstance(cddetail, dict) else None
                check("GET WORKING document detail -> 200",
                      status == 200 and isinstance(cdoc, dict))
                if cdoc:
                    check("WORKING document is flagged read_only", cdoc.get("read_only") is True)
                    check("WORKING document carries copied message provenance",
                          any(v.get("source_kind") == "message"
                              and v.get("source_id") == long_msg_id
                              for v in (cdoc.get("provenance") or [])))
                    check("WORKING document revision links the proposal",
                          any(r.get("proposal_id") == long_prop_id
                              for r in (cdoc.get("revisions") or [])))

            # idempotent: accepting again does not create a second document
            status, acc2 = jget_post(
                base + f"/api/engine/proposals/{long_prop_id}/accept", {"actor": "smoke_ui"})
            check("re-accept is idempotent (already accepted)",
                  status == 200 and (acc2 or {}).get("already_accepted") is True,
                  f"status={status}")
            check("re-accept keeps status WORKING",
                  ((acc2 or {}).get("codex_document") or {}).get("status") == "WORKING")

            status, pdetail2 = jget(base + "/api/engine/proposals/" + long_prop_id)
            prop2 = (pdetail2 or {}).get("proposal") if isinstance(pdetail2, dict) else None
            check("proposal row is now WORKING",
                  bool(prop2) and prop2.get("status") == "WORKING")

    # accept route rejects other methods
    if long_prop_id:
        for method in ("PUT", "PATCH", "DELETE"):
            s, _, _ = request(
                method, base + f"/api/engine/proposals/{long_prop_id}/accept", body={"x": 1})
            check(f"{method} accept route rejected (405)", s == 405, f"status={s}")

    # ---- source_document must be untouched ------------------------------
    snapshot_after = snapshot_source_documents(tmp_db)
    check("source_document rows were not mutated by any request",
          snapshot_after == SOURCE_SNAPSHOT,
          f"before={len(SOURCE_SNAPSHOT)} after={len(snapshot_after)}")

    # ---- persistence check ---------------------------------------------
    conn = sqlite3.connect(f"file:{tmp_db}?mode=ro", uri=True)
    try:
        n_conv = conn.execute("SELECT COUNT(*) FROM conversation").fetchone()[0]
        n_msg = conn.execute("SELECT COUNT(*) FROM message").fetchone()[0]
        n_cdoc = conn.execute("SELECT COUNT(*) FROM codex_document").fetchone()[0]
        n_rev = conn.execute("SELECT COUNT(*) FROM revision").fetchone()[0]
    finally:
        conn.close()
    check("conversation row persisted to SQLite", n_conv >= 1, f"n={n_conv}")
    check("message rows persisted to SQLite", n_msg >= 4, f"n={n_msg}")
    check("codex_document row persisted to SQLite", n_cdoc >= 1, f"n={n_cdoc}")
    check("revision row persisted to SQLite", n_rev >= 1, f"n={n_rev}")

    # ---- no CANONICAL anywhere in the living store ----------------------
    assert_no_canonical(tmp_db, "living store")

    # ---- unknown route ---------------------------------------------------
    status, _ = jget(base + "/api/does-not-exist")
    check("unknown route -> 404", status == 404, f"status={status}")


def run_engine_checks(base: str, tmp_db: str) -> None:
    """Engine tab: PROPOSED browse + provenance + safe dry-run."""
    status, emeta = jget(base + "/api/engine/meta")
    check("GET /api/engine/meta -> 200", status == 200 and isinstance(emeta, dict),
          f"status={status}")
    if isinstance(emeta, dict):
        check("engine meta reports CANONICAL NONE", emeta.get("canonical") == "NONE")
        check("engine meta is flagged read-only", emeta.get("read_only") is True)
        check("engine store exists", emeta.get("exists") is True,
              str(emeta.get("engine_db")))
        check("engine meta reports proposals",
              (emeta.get("counts") or {}).get("proposal", 0) >= 1,
              str(emeta.get("counts")))

    status, efacets = jget(base + "/api/engine/facets")
    check("GET /api/engine/facets -> 200", status == 200 and isinstance(efacets, dict))
    check("engine facets expose proposal statuses",
          bool((efacets or {}).get("statuses")))

    status, runs = jget(base + "/api/engine/runs")
    check("GET /api/engine/runs -> 200", status == 200 and isinstance(runs, dict))
    check("engine runs are recorded", len((runs or {}).get("runs", [])) >= 1)

    status, listing = jget(base + "/api/engine/proposals?all=1&limit=5")
    check("GET /api/engine/proposals -> 200",
          status == 200 and isinstance(listing, dict), f"status={status}")
    props = (listing or {}).get("proposals", [])
    check("engine proposal list respects limit", 0 < len(props) <= 5, f"len={len(props)}")
    check("engine proposal list reports a total",
          (listing or {}).get("total", 0) >= len(props))
    check("engine proposal list is flagged read-only",
          (listing or {}).get("read_only") is True)
    sample = props[0] if props else {}
    for key in ("id", "status", "summary", "attribution", "created_at", "provenance_count"):
        check(f"listed proposal carries '{key}'", key in sample)

    # quiet default (no flags) must hide non-hybrid archaeology
    status, quiet0 = jget(base + "/api/engine/proposals?limit=500")
    q0 = (quiet0 or {}).get("proposals", []) if isinstance(quiet0, dict) else []
    check("default engine listing is quiet (hybrid:* only)",
          all((r.get("attribution") or "").startswith("hybrid:") for r in q0),
          f"rows={len(q0)}")

    if sample:
        status, detail = jget(base + "/api/engine/proposals/" + sample["id"])
        prop = (detail or {}).get("proposal") if isinstance(detail, dict) else None
        check("GET engine proposal detail -> 200", status == 200 and isinstance(prop, dict))
        check("engine proposal detail is flagged read-only",
              bool(prop) and prop.get("read_only") is True)
        check("engine proposal detail exposes provenance",
              bool(prop) and isinstance(prop.get("provenance"), list)
              and len(prop["provenance"]) >= 1)
        check("engine proposal detail exposes based_on",
              bool(prop) and isinstance(prop.get("based_on"), list))
        # The newest proposal may be message-linked (durable candidates), so pick
        # a proposal that the DB records as source_document-linked and confirm the
        # API resolves the path. (Pre-existing check made robust; no intent change.)
        conn = sqlite3.connect(f"file:{tmp_db}?mode=ro", uri=True)
        try:
            row = conn.execute(
                """SELECT p.id FROM proposal p
                   JOIN provenance_link v ON v.subject_kind='proposal'
                        AND v.subject_id=p.id AND v.source_kind='source_document'
                   ORDER BY p.id LIMIT 1""").fetchone()
        finally:
            conn.close()
        if row:
            status, sdetail = jget(base + "/api/engine/proposals/" + row[0])
            sprop = (sdetail or {}).get("proposal") if isinstance(sdetail, dict) else None
            resolved = [p for p in ((sprop or {}).get("provenance") or [])
                        if p.get("source_kind") == "source_document"
                        and p.get("source_rel_path")]
            check("engine provenance resolves to a source_document path",
                  status == 200 and len(resolved) >= 1, f"resolved={len(resolved)}")
        else:
            print("NOTE  no source_document-linked proposal in store; skipping resolve check")

    # non-dry-run mutations on the collection are refused
    s, _, _ = request("POST", base + "/api/engine/proposals", body={"x": 1})
    check("POST /api/engine/proposals rejected (405)", s == 405, f"status={s}")
    for method in ("PUT", "PATCH", "DELETE"):
        s, _, _ = request(method, base + "/api/engine/proposals/" + (sample.get("id") or "x"),
                          body={"x": 1})
        check(f"{method} /api/engine/... rejected (405)", s == 405, f"status={s}")

    # safe dry-run: shells to Stage 5 on a throwaway copy, commits nothing
    status, dry = jget_post(base + "/api/engine/dry-run", {})
    check("POST /api/engine/dry-run -> 200",
          status == 200 and isinstance(dry, dict), f"status={status}")
    if isinstance(dry, dict):
        check("dry-run reports dry_run true", dry.get("dry_run") is True)
        check("dry-run reports CANONICAL NONE", dry.get("canonical") == "NONE")
        check("dry-run leaves the engine store byte-identical",
              dry.get("engine_db_unchanged") is True)
        check("dry-run exit 0 and shows the rollback",
              dry.get("returncode") == 0 and "dry-run" in (dry.get("stdout") or ""))


def run_hybrid_wiring_checks(base: str, tmp_db: str) -> None:
    """Stage 5b hybrid wiring: synthesize endpoint, quiet filters, LLM
    fail-closed, explicit Accept, provenance, and preserved raw messages."""
    msgs_before = snapshot_messages(tmp_db, TARGET_CONV)
    check("hybrid smoke target conversation present",
          len(msgs_before) >= 1, f"messages={len(msgs_before)}")

    # ---- validation: route-safe id + DB existence ----------------------
    s, _ = jget_post(base + "/api/engine/synthesize", {})
    check("POST /api/engine/synthesize without conversation_id -> 400",
          s == 400, f"status={s}")
    s, _ = jget_post(base + "/api/engine/synthesize",
                     {"conversation_id": "../escape"})
    check("synthesize rejects route-unsafe conversation_id -> 400",
          s == 400, f"status={s}")
    s, _ = jget_post(base + "/api/engine/synthesize",
                     {"conversation_id": "conv_nope"})
    check("synthesize unknown conversation -> 404", s == 404, f"status={s}")

    # ---- deterministic synthesis (default path) ------------------------
    status, syn = jget_post(base + "/api/engine/synthesize",
                            {"conversation_id": TARGET_CONV, "llm": False})
    check("POST /api/engine/synthesize (deterministic) -> 200",
          status == 200 and isinstance(syn, dict), f"status={status}")
    if isinstance(syn, dict):
        check("synthesis reports deterministic mode",
              syn.get("mode") == "deterministic", str(syn.get("mode")))
        check("synthesis reports llm_requested false",
              syn.get("llm_requested") is False)
        check("synthesis returncode is 0", syn.get("returncode") == 0,
              str(syn.get("returncode")))
        check("synthesis reports CANONICAL NONE / no_canonical",
              syn.get("canonical") == "NONE" and syn.get("no_canonical") is True)
        check("synthesis created new hybrid:deterministic PROPOSED rows",
              (syn.get("new_hybrid_proposals") or 0) >= 1
              and (syn.get("new_proposals") or 0) >= 1, str(syn)[:300])
        check("synthesis ran against the server living DB",
              os.path.abspath(syn.get("living_db", "")) == os.path.abspath(tmp_db))

    # DB: hybrid proposals linked to the target conversation's messages
    conn = sqlite3.connect(f"file:{tmp_db}?mode=ro", uri=True)
    try:
        det = conn.execute(
            "SELECT COUNT(*) FROM proposal WHERE attribution = 'hybrid:deterministic' "
            "AND status = 'PROPOSED' AND summary NOT LIKE 'Theme:%'").fetchone()[0]
        themes = conn.execute(
            "SELECT COUNT(*) FROM proposal WHERE attribution LIKE 'hybrid:%' "
            "AND summary LIKE 'Theme:%'").fetchone()[0]
        msg_ids = {r[0] for r in conn.execute(
            "SELECT id FROM message WHERE conversation_id = ?", (TARGET_CONV,))}
        linked = conn.execute(
            """SELECT v.source_id FROM provenance_link v
               JOIN proposal p ON p.id = v.subject_id
               WHERE v.subject_kind = 'proposal' AND v.source_kind = 'message'
                 AND p.attribution LIKE 'hybrid:%'""").fetchall()
    finally:
        conn.close()
    check("hybrid:deterministic PROPOSED rows exist", det >= 1, f"count={det}")
    check("hybrid Theme:* rows exist (exercise the quiet filter)", themes >= 1,
          f"count={themes}")
    check("hybrid provenance links resolve to target conversation messages",
          bool(linked) and all(r[0] in msg_ids for r in linked),
          f"links={len(linked)} msgs={len(msg_ids)}")

    # ---- quiet default + widening flags --------------------------------
    status, quiet = jget(base + "/api/engine/proposals?limit=500")
    qrows = (quiet or {}).get("proposals", []) if isinstance(quiet, dict) else []
    check("default engine listing returns hybrid rows", len(qrows) >= 1)
    check("default engine listing contains only hybrid:* rows",
          all((r.get("attribution") or "").startswith("hybrid:") for r in qrows))
    check("default engine listing hides Theme:* rows",
          not any((r.get("summary") or "").startswith("Theme:") for r in qrows))

    status, wt = jget(base + "/api/engine/proposals?limit=500&include_themes=1")
    trows = (wt or {}).get("proposals", []) if isinstance(wt, dict) else []
    status, ar = jget(base + "/api/engine/proposals?limit=500&all=1")
    arows = (ar or {}).get("proposals", []) if isinstance(ar, dict) else []
    check("include_themes=1 widens the quiet list",
          len(trows) >= len(qrows)
          and (wt or {}).get("total", 0) >= (quiet or {}).get("total", 0))
    check("include_themes=1 shows Theme:* rows",
          any((r.get("summary") or "").startswith("Theme:") for r in trows))
    check("include_themes=1 still restricts to hybrid:*",
          all((r.get("attribution") or "").startswith("hybrid:") for r in trows))
    check("all=1 widens beyond hybrid (archaeology visible)",
          len(arows) >= len(trows)
          and any(not (r.get("attribution") or "").startswith("hybrid:")
                  for r in arows))
    check("all=1 still flags read-only / CANONICAL NONE",
          (ar or {}).get("read_only") is True
          and (ar or {}).get("canonical") == "NONE")

    # ---- optional LLM: fail closed without empty success ---------------
    llm_before = count_proposals(tmp_db, "WHERE attribution = 'hybrid:llm'")
    status, llm = jget_post(base + "/api/engine/synthesize",
                            {"conversation_id": TARGET_CONV, "llm": True})
    check("POST /api/engine/synthesize (llm) -> 200 with deterministic floor",
          status == 200 and isinstance(llm, dict), f"status={status}")
    llm_after = count_proposals(tmp_db, "WHERE attribution = 'hybrid:llm'")
    if isinstance(llm, dict) and llm.get("llm_drafted"):
        check("LLM reachable: hybrid:llm PROPOSED created",
              llm_after >= llm_before + 1, f"before={llm_before} after={llm_after}")
    else:
        check("LLM unreachable: fail closed (no false success)",
              isinstance(llm, dict) and llm.get("llm_drafted") is False
              and bool(llm.get("llm_error")),
              str((llm or {}).get("llm_error"))[:200])
        check("LLM unreachable: zero hybrid:llm rows written",
              llm_after == llm_before, f"before={llm_before} after={llm_after}")
        check("LLM fail-closed kept the deterministic floor",
              isinstance(llm, dict) and (llm.get("new_hybrid_proposals") or 0) >= 1)

    # ---- explicit Accept of ONE proposal -> WORKING --------------------
    status, listing = jget(base + "/api/engine/proposals?limit=500")
    proposed = [r for r in (listing or {}).get("proposals", [])
                if r.get("status") == "PROPOSED"]
    accept_id = next((r["id"] for r in proposed
                      if (r.get("attribution") or "") == "hybrid:deterministic"), None)
    check("a hybrid:deterministic PROPOSED row is available to Accept",
          accept_id is not None, f"proposed={len(proposed)}")
    if accept_id:
        status, acc = jget_post(
            base + "/api/engine/proposals/" + accept_id + "/accept",
            {"actor": "smoke_ui_hybrid"})
        check("explicit Accept of hybrid proposal -> 200",
              status == 200 and isinstance(acc, dict), f"status={status}")
        check("Accept moved proposal -> WORKING (max status)",
              (acc or {}).get("proposal_status") == "WORKING"
              and (acc or {}).get("status") == "WORKING"
              and (acc or {}).get("canonical") == "NONE", str(acc)[:200])
        conn = sqlite3.connect(f"file:{tmp_db}?mode=ro", uri=True)
        try:
            prow = conn.execute(
                "SELECT status FROM proposal WHERE id = ?", (accept_id,)).fetchone()
            cdoc = conn.execute(
                """SELECT d.id FROM codex_document d JOIN revision r
                     ON r.target_id = d.id
                   WHERE r.proposal_id = ? AND d.status = 'WORKING'""",
                (accept_id,)).fetchone()
            rev = conn.execute(
                "SELECT COUNT(*) FROM revision WHERE proposal_id = ?",
                (accept_id,)).fetchone()[0]
            prov = conn.execute(
                """SELECT COUNT(*) FROM provenance_link
                   WHERE subject_kind IN ('codex_document','revision')
                     AND subject_id IN (SELECT id FROM revision WHERE proposal_id = ?)""",
                (accept_id,)).fetchone()[0]
        finally:
            conn.close()
        check("accepted proposal row is WORKING in the DB",
              prow is not None and prow[0] == "WORKING", str(prow))
        check("Accept produced a WORKING codex_document linked by revision",
              cdoc is not None)
        check("revision row links the accepted proposal", rev >= 1, f"n={rev}")
        check("Accept copied provenance onto document/revision", prov >= 1, f"n={prov}")

    # ---- raw Journey messages preserved --------------------------------
    check("raw Journey messages preserved byte-for-byte",
          snapshot_messages(tmp_db, TARGET_CONV) == msgs_before)

    # ---- no CANONICAL writes anywhere ----------------------------------
    assert_no_canonical(tmp_db, "living store after hybrid synthesis")


def run_live_llm_optional(base: str, tmp_db: str) -> None:
    """Optional live-LLM synthesis check, gated by SOLBIAN_LLM_SMOKE=1."""
    if os.getenv("SOLBIAN_LLM_SMOKE") not in ("1", "true", "yes"):
        print("NOTE  SOLBIAN_LLM_SMOKE not set; live LLM check skipped")
        return
    status, llm = jget_post(base + "/api/engine/synthesize",
                            {"conversation_id": TARGET_CONV, "llm": True})
    check("live LLM synthesis -> 200", status == 200 and isinstance(llm, dict))
    if isinstance(llm, dict) and llm.get("llm_drafted"):
        n = count_proposals(tmp_db, "WHERE attribution = 'hybrid:llm'")
        check("live LLM produced hybrid:llm PROPOSED", n >= 1, f"n={n}")
    else:
        print(f"NOTE  live LLM unavailable: {(llm or {}).get('llm_error')}")


if __name__ == "__main__":
    sys.exit(main())
