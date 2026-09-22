#!/usr/bin/env python3
"""Codex Solbian — Phase I · Stage 7 — living-loop CLI.

The living loop, end to end:

    JD <-> Solace (message)  ->  preserved conversation (living SQLite)
        ->  Stage 5 deterministic engine (durable/engine run)
        ->  PROPOSED proposal rows (+ provenance_link)
        ->  controlled consolidation (explicit accept -> WORKING codex_document)
        ->  Codex Solbian browse (WORKING codex_document alongside HISTORICAL source_document)

Commands
--------
    python3 living_loop.py once                 # full loop on a THROWAWAY copy (smoke helper)
    python3 living_loop.py once --in-place      # same, but writes the living store
    python3 living_loop.py run-engine           # run the engine on the living store
    python3 living_loop.py list-proposals
    python3 living_loop.py accept <id|prefix>   # controlled consolidation
    python3 living_loop.py list-codex           # WORKING codex_document rows
    python3 living_loop.py migrate              # one-time seed from Stage 5
    python3 living_loop.py info                 # counts + policy

``once`` defaults to a throwaway copy of the living store so it is always safe
to run (and works under a read-only sandbox).  ``--in-place`` (or an explicit
``--db``) makes it operate on the real living store instead.

No command can write ``CANONICAL``: the value is absent from the schema and a
guard rejects it.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
import tempfile

import living_store as ls

DEMO_CONV = "conv_living_loop_demo"
DEMO_MSG = "msg_living_loop_demo"
DEMO_BODY = (
    "Living-loop demo message (Stage 7). This deliberately long JD note is the "
    "kind of preserved conversation material the durable analyzer promotes to a "
    "PROPOSED proposal: it records an intent to keep the Codex Solbian in "
    "dialogue — observations stay inspectable, synthesis is proposed rather than "
    "assumed, and a human must explicitly accept before anything becomes WORKING "
    "Codex content. It also serves as a stable fixture so `living_loop.py once` "
    "is idempotent and can be re-run without piling up demo rows."
)


def _print(obj) -> None:
    print(json.dumps(obj, indent=2, sort_keys=True, default=str))


def _escape_like(needle: str) -> str:
    return needle.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")


def resolve_proposal_id(conn, needle: str) -> str:
    exact = conn.execute("SELECT id FROM proposal WHERE id = ?", (needle,)).fetchone()
    if exact:
        return exact[0]
    rows = list(conn.execute(
        "SELECT id FROM proposal WHERE id LIKE ? ESCAPE '\\' ORDER BY id LIMIT 25",
        (_escape_like(needle) + "%",)))
    if len(rows) == 1:
        return rows[0][0]
    if not rows:
        raise ls.LivingStoreError(f"no proposal matches {needle!r}")
    raise ls.LivingStoreError(
        f"ambiguous proposal prefix {needle!r}: " + ", ".join(r[0] for r in rows))


def ensure_demo_conversation(conn) -> str:
    """Idempotently create the deterministic demo conversation + long message."""
    ts = ls.now_iso()
    conn.execute(
        """INSERT INTO conversation
             (id, title, participants, status, started_at, notes, attribution,
              created_at, updated_at)
           VALUES (?, ?, ?, 'WORKING', ?, ?, 'stage7 living_loop.py once', ?, ?)
           ON CONFLICT(id) DO UPDATE SET updated_at = excluded.updated_at""",
        (DEMO_CONV, "Stage 7 living loop", json.dumps(["jd", "solace"]), ts,
         "Deterministic fixture for the living-loop smoke helper.", ts, ts))
    seq = conn.execute(
        "SELECT COALESCE(MAX(seq), 0) + 1 FROM message WHERE conversation_id = ?",
        (DEMO_CONV,)).fetchone()[0]
    conn.execute(
        """INSERT INTO message
             (id, conversation_id, seq, role, body, sent_at, source_path, status,
              created_at, updated_at)
           VALUES (?, ?, ?, 'jd', ?, ?, NULL, 'WORKING', ?, ?)
           ON CONFLICT(id) DO UPDATE SET updated_at = excluded.updated_at""",
        (DEMO_MSG, DEMO_CONV, seq, DEMO_BODY, ts, ts, ts))
    conn.commit()
    return DEMO_MSG


def proposals_for_source(conn, source_kind: str, source_id: str) -> list[dict]:
    return [dict(r) for r in conn.execute(
        """SELECT p.* FROM proposal p
           JOIN provenance_link v
             ON v.subject_kind = 'proposal' AND v.subject_id = p.id
           WHERE v.source_kind = ? AND v.source_id = ?
           ORDER BY p.id""", (source_kind, source_id))]


def cmd_once(args) -> int:
    tmpdir = None
    if args.db and not args.ephemeral:
        db = os.path.abspath(args.db)
        if not os.path.exists(db):
            raise ls.LivingStoreError(f"living store not found: {db}")
        source = "explicit --db"
    elif args.in_place:
        db = ls.resolve_living_db(args.db)
        source = "living store (in place)"
    else:
        tmpdir = tempfile.mkdtemp(prefix="stage7_once_")
        seed = ls.resolve_living_db(args.db) if args.db else ls.LIVING_DB
        if not os.path.exists(seed):
            seed = ls.STAGE3_DB
        db = os.path.join(tmpdir, "living.sqlite")
        shutil.copyfile(seed, db)
        source = f"throwaway copy of {seed}"

    print("Stage 7 living loop — `once`")
    print(f"living db : {db}")
    print(f"mode      : {source}")
    if args.ephemeral and args.db:
        print("note      : --ephemeral forces a throwaway copy")

    try:
        with ls.connect(db) as conn:
            seed_info = ls.migrate(conn, ls.STAGE5_DB)
            print(f"seed      : seeded={seed_info['seeded']} reason={seed_info['reason']}")

            msg_id = ensure_demo_conversation(conn)
            print(f"message   : {msg_id} appended to {DEMO_CONV}")

            run = ls.run_engine(db, kinds=args.kinds or ["durable", "discussion"])
            print(f"engine    : exit {run['returncode']} kinds={run['kinds']}")
            if run["returncode"] != 0:
                sys.stderr.write(run["stdout"] + "\n" + run["stderr"] + "\n")
                return 1

            props = proposals_for_source(conn, "message", msg_id)
            if not props:
                sys.stderr.write("no proposal linked to the demo message\n")
                return 1
            target = props[0]
            print(f"proposal  : {target['id']} status={target['status']}")

            result = ls.accept_proposal(conn, target["id"], actor="living_loop.py")
            doc = result["codex_document"]
            print(f"consolidate: codex_document={doc['id']} status={doc['status']} "
                  f"already={result['already_accepted']} "
                  f"provenance_copied={result['provenance_copied']}")

            # ---- assertions -------------------------------------------------
            checks = []
            checks.append(("codex_document is WORKING",
                           doc["status"] == ls.CONSOLIDATION_STATUS))
            checks.append(("codex_document is never CANONICAL",
                           doc["status"] != ls.CANONICAL))
            checks.append(("revision row exists", bool(result["revision"])))
            checks.append(("provenance copied onto codex_document",
                           ls.scalar(conn,
                                     "SELECT COUNT(*) FROM provenance_link "
                                     "WHERE subject_kind='codex_document' AND subject_id=?",
                                     (doc["id"],)) >= 1))
            checks.append(("provenance copied onto revision",
                           ls.scalar(conn,
                                     "SELECT COUNT(*) FROM provenance_link "
                                     "WHERE subject_kind='revision' AND subject_id=?",
                                     (result["revision"]["id"],)) >= 1))
            checks.append(("proposal marked accepted (WORKING)",
                           ls.scalar(conn, "SELECT status FROM proposal WHERE id=?",
                                     (target["id"],)) == ls.CONSOLIDATION_STATUS))
            checks.append(("no CANONICAL anywhere", not ls.scan_canonical(conn)))

            ok = all(v for _, v in checks)
            for name, passed in checks:
                print(("  ok   " if passed else "  FAIL ") + name)
            if not ok:
                return 1
            if args.json:
                _print({"living_db": db, "message_id": msg_id,
                        "proposal": target["id"], "result": result})
            print("living loop OK")
            return 0
    finally:
        if tmpdir:
            shutil.rmtree(tmpdir, ignore_errors=True)


def cmd_run_engine(args) -> int:
    db = ls.resolve_living_db(args.db)
    with ls.connect(db) as conn:
        ls.migrate(conn, ls.STAGE5_DB)
        before = ls.scalar(conn, "SELECT COUNT(*) FROM proposal")
    run = ls.run_engine(db, kinds=args.kinds, timeout=args.timeout)
    with ls.connect(db) as conn:
        after = ls.scalar(conn, "SELECT COUNT(*) FROM proposal")
    run["proposals_before"] = before
    run["proposals_after"] = after
    run["new_proposals"] = after - before
    if args.json:
        _print(run)
    else:
        print(f"engine exit {run['returncode']} kinds={run['kinds']} "
              f"proposals {before} -> {after} (new {after - before})")
        if run["returncode"] != 0:
            sys.stderr.write(run["stdout"] + "\n" + run["stderr"] + "\n")
    return 0 if run["returncode"] == 0 else 1


def cmd_list_proposals(args) -> int:
    db = ls.resolve_living_db(args.db)
    with ls.connect(db) as conn:
        ls.ensure_base_schema(conn)
        sql = ("SELECT p.id, p.status, p.summary, p.attribution, p.created_at, "
               "(SELECT COUNT(*) FROM provenance_link v "
               " WHERE v.subject_kind='proposal' AND v.subject_id=p.id) AS prov "
               "FROM proposal p")
        params: list = []
        if args.status:
            sql += " WHERE p.status IN (" + ",".join("?" * len(args.status)) + ")"
            params += args.status
        sql += " ORDER BY p.created_at DESC, p.id LIMIT ?"
        params.append(args.limit)
        rows = [dict(r) for r in conn.execute(sql, params)]
    if args.json:
        _print(rows)
    else:
        for r in rows:
            print(f"{r['id']:28s} {r['status']:9s} prov={r['prov']:>3}  "
                  f"{(r['summary'] or '')[:80]}")
        print(f"{len(rows)} proposal(s)")
    return 0


def cmd_list_codex(args) -> int:
    db = ls.resolve_living_db(args.db)
    with ls.connect(db) as conn:
        ls.ensure_base_schema(conn)
        result = ls.list_codex_documents(conn, {"limit": [str(args.limit)]})
    if args.json:
        _print(result)
    else:
        for d in result["codex_documents"]:
            print(f"{d['id']:28s} {d['status']:8s} {d['kind']:9s} "
                  f"prov={d['provenance_count']:>3}  {(d['title'] or '')[:70]}")
        print(f"{result['total']} WORKING codex_document(s) · CANONICAL NONE")
    return 0


def cmd_accept(args) -> int:
    db = ls.resolve_living_db(args.db)
    with ls.connect(db) as conn:
        ls.ensure_base_schema(conn)
        pid = resolve_proposal_id(conn, args.proposal_id)
        result = ls.accept_proposal(conn, pid, actor=args.actor)
    if args.json:
        _print(result)
    else:
        doc = result["codex_document"]
        print(f"proposal {pid} -> status {result['proposal_status']}")
        print(f"codex_document {doc['id']} status={doc['status']} "
              f"version={doc['version']} already_accepted={result['already_accepted']}")
        print(f"revision {result['revision'].get('id')} · "
              f"provenance copied {result['provenance_copied']} · CANONICAL NONE")
    return 0


def cmd_migrate(args) -> int:
    db = ls.resolve_living_db(args.db)
    if not os.path.exists(db):
        raise ls.LivingStoreError(f"living store not found: {db}")
    with ls.connect(db) as conn:
        summary = ls.migrate(conn, args.stage5_db, force=args.force)
    summary["living_db"] = db
    if args.json:
        _print(summary)
    else:
        print(f"living_db : {db}")
        print(f"seeded    : {summary['seeded']} ({summary['reason']})")
        print("copied    : " + ", ".join(
            f"{k}={v}" for k, v in summary["copied"].items()))
    return 0


def cmd_info(args) -> int:
    db = ls.resolve_living_db(args.db)
    if not os.path.exists(db):
        raise ls.LivingStoreError(f"living store not found: {db}")
    with ls.connect(db) as conn:
        ls.ensure_base_schema(conn)
        meta = ls.living_meta(conn)
    meta["living_db"] = db
    if args.json:
        _print(meta)
    else:
        print(f"living_db : {db}")
        print(f"policy    : {meta['policy']}")
        print("counts    : " + ", ".join(f"{k}={v}" for k, v in meta["counts"].items()))
        print(f"proposal statuses     : {meta['proposal_statuses']}")
        print(f"codex_document statuses: {meta['codex_document_statuses']}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="living_loop.py",
        description="Codex Solbian Stage 7 — living loop over one living SQLite store.")
    p.add_argument("--db", default=None, help=f"living store (default: {ls.LIVING_DB})")
    sub = p.add_subparsers(dest="cmd", required=True)

    once = sub.add_parser("once", help="run the full loop (throwaway copy by default)")
    once.add_argument("--in-place", action="store_true",
                      help="run against the real living store instead of a throwaway copy")
    once.add_argument("--ephemeral", action="store_true",
                      help="force a throwaway copy even when --db is given")
    once.add_argument("--kind", action="append", dest="kinds", default=None,
                      help="engine analysis kind(s) for the loop (default durable,discussion)")
    once.add_argument("--json", action="store_true")
    once.set_defaults(func=cmd_once)

    run = sub.add_parser("run-engine", help="run the engine against the living store")
    run.add_argument("--kind", action="append", dest="kinds", default=None)
    run.add_argument("--timeout", type=int, default=240)
    run.add_argument("--json", action="store_true")
    run.set_defaults(func=cmd_run_engine)

    lp = sub.add_parser("list-proposals", help="list proposal rows")
    lp.add_argument("--status", action="append", default=None)
    lp.add_argument("--limit", type=int, default=200)
    lp.add_argument("--json", action="store_true")
    lp.set_defaults(func=cmd_list_proposals)

    lc = sub.add_parser("list-codex", help="list WORKING codex_document rows")
    lc.add_argument("--limit", type=int, default=200)
    lc.add_argument("--json", action="store_true")
    lc.set_defaults(func=cmd_list_codex)

    ac = sub.add_parser("accept", help="controlled consolidation of one proposal")
    ac.add_argument("proposal_id")
    ac.add_argument("--actor", default="jd")
    ac.add_argument("--json", action="store_true")
    ac.set_defaults(func=cmd_accept)

    mg = sub.add_parser("migrate", help="one-time seed of engine tables from Stage 5")
    mg.add_argument("--stage5-db", default=ls.STAGE5_DB)
    mg.add_argument("--force", action="store_true")
    mg.add_argument("--json", action="store_true")
    mg.set_defaults(func=cmd_migrate)

    inf = sub.add_parser("info", help="living-store counts + policy")
    inf.add_argument("--json", action="store_true")
    inf.set_defaults(func=cmd_info)
    return p


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return args.func(args)
    except ls.LivingStoreError as exc:
        print(f"living loop error: {exc}", file=sys.stderr)
        return 2
    except Exception as exc:  # noqa: BLE001 - surfaced, not hidden
        print(f"living loop error: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 3


if __name__ == "__main__":
    raise SystemExit(main())
