#!/usr/bin/env python3
"""Stage 4 HTTP smoke test.

Boots ``app.py`` on an ephemeral port against a throwaway copy of the working
store, exercises the Solace and Codex endpoints over real HTTP, asserts the
read-only guarantees, then kills the server. Exits 0 only if every check passes.

    python3 smoke_ui.py
"""

from __future__ import annotations

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

RESULTS: list[tuple[str, bool, str]] = []
SOURCE_SNAPSHOT: list = []


def check(name: str, ok: bool, detail: str = "") -> None:
    RESULTS.append((name, bool(ok), detail))
    print(("PASS  " if ok else "FAIL  ") + name + ("" if ok or not detail else f"  — {detail}"))


def free_port() -> int:
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()
    return port


def request(method: str, url: str, body=None, timeout: float = 15.0):
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


def wait_for_server(base: str, proc: subprocess.Popen, timeout: float = 25.0) -> bool:
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
    tmpdir = tempfile.mkdtemp(prefix="stage4_smoke_")
    tmp_db = os.path.join(tmpdir, "smoke.sqlite")
    shutil.copy2(source_db, tmp_db)
    SOURCE_SNAPSHOT = snapshot_source_documents(tmp_db)
    log_path = os.path.join(tmpdir, "server.log")

    port = free_port()
    base = f"http://127.0.0.1:{port}"
    env = dict(os.environ, PYTHONUNBUFFERED="1")
    logf = open(log_path, "wb")
    proc = subprocess.Popen(
        [sys.executable, APP, "--port", str(port), "--db", tmp_db, "--no-setup"],
        cwd=HERE, stdout=logf, stderr=subprocess.STDOUT, env=env,
    )

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
        killed = proc.poll() is not None
        check("server process stopped", killed, f"poll={proc.poll()}")
        if not all(ok for _, ok, _ in RESULTS):
            try:
                with open(log_path, "r", encoding="utf-8", errors="replace") as fh:
                    tail = fh.read()[-2000:]
                if tail.strip():
                    print("\n--- server log tail ---")
                    print(tail)
            except OSError:
                pass
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
    check("page has both tabs", "Solace" in html and "Codex Solbian" in html)
    check("page states CANONICAL: NONE", "CANONICAL: NONE" in html)
    low = html.lower()
    check("page has no canonical form control",
          'name="canonical"' not in low and 'id="canonical"' not in low
          and "make_canonical" not in low and ">make canonical<" not in low)
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

    # ---- codex browse ---------------------------------------------------
    status, facets = jget(base + "/api/codex/facets")
    check("GET /api/codex/facets -> 200", status == 200 and isinstance(facets, dict))
    if isinstance(facets, dict):
        check("facets expose statuses", bool(facets.get("statuses")))
        check("facets expose corpus roots", bool(facets.get("corpus_roots")))
        statuses = [s.get("value") for s in (facets.get("statuses") or [])]
        check("no CANONICAL value exists in the data model",
              "CANONICAL" not in statuses, str(statuses))

    status, listing = jget(base + "/api/codex/documents?limit=5")
    check("GET /api/codex/documents -> 200", status == 200 and isinstance(listing, dict))
    docs = (listing or {}).get("documents", [])
    check("document list respects limit", 0 < len(docs) <= 5, f"len={len(docs)}")
    check("document list reports a total", (listing or {}).get("total", 0) >= len(docs))
    first = docs[0] if docs else {}
    for key in ("id", "rel_path", "status", "corpus_root_path", "probable_role"):
        check(f"listed document carries '{key}'", key in first)

    # detail for the first document
    if first:
        status, detail = jget(base + "/api/codex/documents/" + first["id"])
        doc = (detail or {}).get("document") if isinstance(detail, dict) else None
        check("GET document detail -> 200", status == 200 and isinstance(doc, dict))
        check("document detail is flagged read_only", bool(doc) and doc.get("read_only") is True)
        check("document detail includes a preview block",
              bool(doc) and isinstance(doc.get("preview"), dict))

    # find a text document that exists locally and verify preview + mtime
    status, text_listing = jget(
        base + "/api/codex/documents?limit=200&q=.md")
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

    # ---- solace write path ---------------------------------------------
    status, before_list = jget(base + "/api/solace/conversations")
    check("GET /api/solace/conversations -> 200",
          status == 200 and isinstance(before_list, dict))
    before_n = len((before_list or {}).get("conversations", []))
    check("conversation list is a list",
          isinstance((before_list or {}).get("conversations"), list))

    status, created = jget_post(base + "/api/solace/conversations",
                                {"title": "Stage 4 smoke", "participants": "jd, solace",
                                 "notes": "created by smoke_ui.py"})
    conv = (created or {}).get("conversation") if isinstance(created, dict) else None
    check("POST create conversation -> 201", status == 201 and bool(conv), f"status={status}")
    conv_id = (conv or {}).get("id")
    check("created conversation is WORKING", (conv or {}).get("status") == "WORKING")

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

        status, m2 = jget_post(f"{base}/api/solace/conversations/{conv_id}/messages",
                               {"role": "solace", "body": "A direct solace message."})
        check("POST solace message -> 201", status == 201 and (m2 or {}).get("message"),
              f"status={status}")

        status, bad = jget_post(f"{base}/api/solace/conversations/{conv_id}/messages",
                                {"role": "canonical", "body": "nope"})
        check("invalid message role rejected (400)", status == 400, f"status={status}")
        status, bad = jget_post(f"{base}/api/solace/conversations/{conv_id}/messages",
                                {"role": "jd", "body": "   "})
        check("empty message body rejected (400)", status == 400, f"status={status}")

        status, full = jget(f"{base}/api/solace/conversations/{conv_id}")
        conversation = (full or {}).get("conversation") if isinstance(full, dict) else None
        messages = (conversation or {}).get("messages", [])
        check("conversation detail returns messages", status == 200 and len(messages) >= 3,
              f"n={len(messages)}")
        seqs = [m.get("seq") for m in messages]
        check("messages are ordered by seq", seqs == sorted(seqs) and len(set(seqs)) == len(seqs))
        roles = {m.get("role") for m in messages}
        check("both jd and solace messages persisted", {"jd", "solace"} <= roles, str(roles))

        status, after_list = jget(base + "/api/solace/conversations")
        after_n = len((after_list or {}).get("conversations", []))
        check("conversation list grew by one", after_n == before_n + 1,
              f"{before_n} -> {after_n}")

    # ---- source_document must be untouched ------------------------------
    snapshot_after = snapshot_source_documents(tmp_db)
    check("source_document rows were not mutated by any request",
          snapshot_after == SOURCE_SNAPSHOT,
          f"before={len(SOURCE_SNAPSHOT)} after={len(snapshot_after)}")

    # ---- persistence check (direct read-only DB look) -------------------
    conn = sqlite3.connect(f"file:{tmp_db}?mode=ro", uri=True)
    try:
        n_conv = conn.execute("SELECT COUNT(*) FROM conversation").fetchone()[0]
        n_msg = conn.execute("SELECT COUNT(*) FROM message").fetchone()[0]
    finally:
        conn.close()
    check("conversation row persisted to SQLite", n_conv >= 1, f"n={n_conv}")
    check("message rows persisted to SQLite", n_msg >= 3, f"n={n_msg}")

    # ---- unknown route ---------------------------------------------------
    status, _ = jget(base + "/api/does-not-exist")
    check("unknown route -> 404", status == 404, f"status={status}")


def jget_asset(base: str, name: str):
    status, raw, headers = request("GET", base + "/static/" + name)
    return status, headers


def jget_post(url: str, body):
    status, raw, _ = request("POST", url, body=body)
    try:
        return status, json.loads(raw.decode("utf-8"))
    except (ValueError, UnicodeDecodeError):
        return status, None


if __name__ == "__main__":
    sys.exit(main())
