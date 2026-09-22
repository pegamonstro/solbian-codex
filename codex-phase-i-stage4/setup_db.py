#!/usr/bin/env python3
"""Stage 4 — build the local working copy of the Stage 3 store.

Why this exists
---------------
Stage 4 must open the Stage 3 store for *conversation writes*. On this machine the
DSH file sandbox only permits writes inside this Stage 4 workspace, and the brief
explicitly allows the alternative: "or copy into Stage 4 cwd". So this script makes
a local working copy at ``data/codex_phase_i.sqlite`` and leaves the Stage 3 store
untouched.

It also completes the source_document ingest: the Stage 3 ingest read the key
``entries_sample`` while the full inventory uses ``entries``, so only 80 of the 966
inventory entries ever landed. Here we top the copy up from
``baseline_inventory_full.json`` (read-only), giving the Codex browser its full
corpus index.

Guarantees
----------
* Never writes to ``/Users/archcore/solbian/codex`` (opens files read-only, at most).
* Never writes to the Stage 3 store — only reads it.
* Writes only to the Stage 4 working copy.
* No CANONICAL value is ever produced (enum never contains it).

Usage
-----
    python3 setup_db.py                     # default: data/codex_phase_i.sqlite
    python3 setup_db.py --force             # re-copy from Stage 3 first
    python3 setup_db.py --no-sha256         # never open corpus files
    python3 setup_db.py --db other.sqlite --inventory other.json
"""

from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import json
import os
import shutil
import sqlite3
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_DB = os.path.join(HERE, "data", "codex_phase_i.sqlite")
DEFAULT_SCHEMA = os.path.join(HERE, "schema.sql")
DEFAULT_INVENTORY = os.path.join(HERE, "baseline_inventory_full.json")
STAGE3_DB = "/Users/archcore/solbian/codex-phase-i-stage3/codex_phase_i.sqlite"
STAGE3_SCHEMA = "/Users/archcore/solbian/codex-phase-i-stage3/schema.sql"

# The primary historical corpus. Only ever opened read-only.
PRIMARY_MAC_ROOT = "/Users/archcore/solbian/codex"

CONTENT_STATUS = {
    "SOURCE", "HISTORICAL", "WORKING", "PROPOSED", "REVISION", "RELATED", "UNKNOWN",
}
SHA256_MAX_BYTES = 20 * 1024 * 1024  # never hash anything absurd


def now_iso() -> str:
    return _dt.datetime.now(_dt.timezone.utc).replace(microsecond=0).isoformat()


def stable_id(prefix: str, *parts: str) -> str:
    digest = hashlib.sha1("\x1f".join(parts).encode("utf-8")).hexdigest()[:16]
    return f"{prefix}_{digest}"


def map_content_status(raw: str) -> str:
    """Map a raw Stage 2 label onto the enum without inventing CANONICAL."""
    up = (raw or "").upper()
    if up in CONTENT_STATUS:
        return up
    if "HISTORICAL" in up:
        return "HISTORICAL"
    if "WORKING" in up:
        return "WORKING"
    if "CURRENT" in up or "LIVE" in up or "SOURCE" in up:
        return "SOURCE"
    if "PROPOS" in up:
        return "PROPOSED"
    return "UNKNOWN"


def infer_plurality_flags(rel_path: str, probable_role: str, notes: str) -> list[str]:
    """Preserve law/protocol/scroll plurality as flags. Nothing is merged."""
    hay = f"{rel_path} {probable_role} {notes}".lower()
    flags: list[str] = []
    if any(k in hay for k in ("law", "legal", "justice")):
        flags.append("law_material")
        for token, flag in (("law a", "law_catalogue_A"), ("law b", "law_catalogue_B"),
                            ("law c", "law_catalogue_C"), ("law b\u2032", "law_catalogue_Bprime"),
                            ("law b'", "law_catalogue_Bprime")):
            if token in hay:
                flags.append(flag)
    if "protocol" in hay:
        flags.append("protocol_material")
        if "gitea" in hay:
            flags.append("protocol_catalogue_gitea5")
    if "scroll" in hay or "sref" in hay:
        flags.append("scroll_material")
    if rel_path.lower().endswith(".sref") or ".sref." in rel_path.lower():
        flags.append("sref_artefact")
    if "scroll" in hay and "sref" in hay:
        flags.append("scroll_md_vs_sref_ordinals")
    if "scroll 20" in hay or "scroll_20" in hay:
        flags.append("scroll_20_anomaly")
    if "mac_wt" in hay or "mac_" in hay:
        flags.append("mac_only_surface")
    seen: set[str] = set()
    out: list[str] = []
    for f in flags:
        if f not in seen:
            seen.add(f)
            out.append(f)
    return out


def guess_media_type(rel_path: str, entry_type: str) -> str:
    if entry_type in ("directory", "directory_summary"):
        return "inode/directory"
    low = rel_path.lower()
    for ext, mt in ((".md", "text/markdown"), (".sref", "application/x-sref"),
                    (".json", "application/json"), (".ndjson", "application/x-ndjson"),
                    (".sum", "text/plain"), (".txt", "text/plain"),
                    (".bak", "application/octet-stream")):
        if low.endswith(ext):
            return mt
    return "application/octet-stream"


def sha256_readonly(path: str) -> str | None:
    """Read-only sha256. Never writes, never changes mtime."""
    try:
        if not os.path.isfile(path):
            return None
        if os.path.getsize(path) > SHA256_MAX_BYTES:
            return None
        h = hashlib.sha256()
        with open(path, "rb") as fh:  # READ ONLY
            for chunk in iter(lambda: fh.read(1 << 20), b""):
                h.update(chunk)
        return h.hexdigest()
    except OSError:
        return None


def _read_schema(path: str) -> str:
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


def ensure_schema(conn: sqlite3.Connection, schema_path: str) -> None:
    if not os.path.isfile(schema_path):
        if os.path.isfile(STAGE3_SCHEMA):
            schema_path = STAGE3_SCHEMA
        else:
            raise FileNotFoundError(schema_path)
    conn.executescript(_read_schema(schema_path))
    conn.commit()


def resolve_mac_root_id(conn: sqlite3.Connection) -> str:
    row = conn.execute(
        "SELECT id FROM corpus_root WHERE path = ? ORDER BY created_at LIMIT 1",
        (PRIMARY_MAC_ROOT,),
    ).fetchone()
    return row["id"] if row else stable_id("croot", PRIMARY_MAC_ROOT)


def build(db_path: str = DEFAULT_DB, *, source: str = STAGE3_DB,
          schema: str = DEFAULT_SCHEMA, inventory: str = DEFAULT_INVENTORY,
          do_sha256: bool = True, force: bool = False, quiet: bool = False) -> dict:
    """Copy the Stage 3 store (once) and top up source_document from the full inventory."""
    log = (lambda *a: None) if quiet else print
    os.makedirs(os.path.dirname(os.path.abspath(db_path)), exist_ok=True)

    copied = False
    if force or not os.path.exists(db_path):
        if os.path.isfile(source):
            shutil.copy2(source, db_path)
            copied = True
            log(f"[setup] copied Stage 3 store -> {db_path}")
        else:
            log(f"[setup] source Stage 3 store not found ({source}); creating fresh store")

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    ensure_schema(conn, schema)

    ts = now_iso()
    mac_root_id = resolve_mac_root_id(conn)

    # Make sure the primary Mac root exists even on a fresh store.
    if not conn.execute("SELECT 1 FROM corpus_root WHERE id = ?", (mac_root_id,)).fetchone():
        conn.execute(
            """INSERT INTO corpus_root
               (id, path, classification, role, notes, status, attribution, created_at, updated_at)
               VALUES (?, ?, 'CURRENT', 'PRIMARY_HISTORICAL_WORKING_TREE', ?, 'SOURCE', ?, ?, ?)""",
            (mac_root_id, PRIMARY_MAC_ROOT,
             "Registered notes-only. Stage 4 never writes to this tree.",
             "Stage 4 setup_db", ts, ts),
        )

    with open(inventory, "r", encoding="utf-8") as fh:
        inv = json.load(fh)
    entries = inv.get("entries") or inv.get("entries_sample") or []

    inserted = updated = hashed = skipped = 0
    seen: set[str] = set()
    for entry in entries:
        rel_path = str(entry.get("path", "")).strip()
        if not rel_path:
            skipped += 1
            continue
        seen.add(rel_path)
        probable_role = entry.get("probable_role") or "UNKNOWN"
        notes = entry.get("notes") or ""
        inventory_status = entry.get("status") or "UNKNOWN"
        flags = infer_plurality_flags(rel_path, probable_role, notes)

        sha = None
        if do_sha256 and entry.get("type") == "file":
            sha = sha256_readonly(os.path.join(PRIMARY_MAC_ROOT, rel_path))
            if sha:
                hashed += 1

        row = (
            stable_id("sdoc", mac_root_id, rel_path),
            mac_root_id,
            rel_path,
            guess_media_type(rel_path, entry.get("type", "")),
            entry.get("size_bytes"),
            entry.get("mtime_iso"),
            sha,
            probable_role,
            inventory_status,
            map_content_status(inventory_status),
            json.dumps(flags, ensure_ascii=False),
            notes,
            entry.get("source_surface") or "baseline_inventory_full.json",
            ts, ts,
        )
        existed = conn.execute(
            "SELECT 1 FROM source_document WHERE corpus_root_id = ? AND rel_path = ?",
            (mac_root_id, rel_path),
        ).fetchone()
        conn.execute(
            """INSERT INTO source_document
                 (id, corpus_root_id, rel_path, media_type, byte_size, mtime, sha256,
                  probable_role, inventory_status, status, plurality_flags, notes,
                  attribution, created_at, updated_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
               ON CONFLICT(corpus_root_id, rel_path) DO UPDATE SET
                 media_type=excluded.media_type,
                 byte_size=excluded.byte_size,
                 mtime=excluded.mtime,
                 sha256=COALESCE(excluded.sha256, source_document.sha256),
                 probable_role=excluded.probable_role,
                 inventory_status=excluded.inventory_status,
                 status=excluded.status,
                 plurality_flags=excluded.plurality_flags,
                 notes=excluded.notes,
                 attribution=excluded.attribution,
                 updated_at=excluded.updated_at""",
            row,
        )
        if existed:
            updated += 1
        else:
            inserted += 1

    conn.commit()
    counts = {
        t: conn.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
        for t in ("corpus_root", "source_document", "conversation", "message",
                  "codex_document", "concept", "relationship", "proposal",
                  "revision", "provenance_link")
    }
    conn.close()

    result = {
        "db": os.path.abspath(db_path),
        "copied_from_stage3": copied,
        "inventory": os.path.abspath(inventory),
        "entries_in_json": len(entries),
        "unique_paths": len(seen),
        "inserted": inserted,
        "updated": updated,
        "sha256_computed": hashed,
        "counts": counts,
    }
    log(f"[setup] db                : {result['db']}")
    log(f"[setup] copied from stage3: {copied}")
    log(f"[setup] inventory entries : {len(entries)} ({len(seen)} unique paths)")
    log(f"[setup] source_document   : {counts['source_document']} rows "
        f"(+{inserted} new, ~{updated} refreshed, sha256={hashed})")
    log(f"[setup] table counts      : {json.dumps(counts, sort_keys=True)}")
    return result


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Stage 4 working-copy setup (read-only corpus)")
    parser.add_argument("--db", default=DEFAULT_DB)
    parser.add_argument("--source", default=STAGE3_DB, help="Stage 3 store to copy (read-only)")
    parser.add_argument("--schema", default=DEFAULT_SCHEMA)
    parser.add_argument("--inventory", default=DEFAULT_INVENTORY)
    parser.add_argument("--no-sha256", action="store_true", help="never open corpus files")
    parser.add_argument("--force", action="store_true", help="re-copy from Stage 3 first")
    args = parser.parse_args(argv)
    try:
        build(args.db, source=args.source, schema=args.schema, inventory=args.inventory,
              do_sha256=not args.no_sha256, force=args.force)
    except FileNotFoundError as exc:
        print(f"[setup] ERROR: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
