#!/usr/bin/env python3
"""Stage 3 baseline ingest — read-only registration of corpus roots + Stage 2 inventory sample.

What it does
------------
1. Applies ``schema.sql`` to ``codex_phase_i.sqlite`` (idempotent).
2. Registers corpus roots, including the PRIMARY Mac path
   ``/Users/archcore/solbian/codex`` as CURRENT/HISTORICAL (notes only).
3. Reads ``baseline_inventory_sample.json`` (READ ONLY) and inserts
   ``source_document`` rows pointing at the historical corpus. It never copies
   or rewrites corpus content.
4. Sets ``plurality_flags`` where roles/paths mention laws, protocols or scrolls.
5. Optionally computes sha256 of the referenced Mac files, READ ONLY
   (``--no-sha256`` disables; on by default).

Hard guarantee: this script only ever OPENS corpus files read-only
(``open(path, "rb")``). It contains no write, move, delete or chmod call against
any corpus path.

Usage
-----
    python3 ingest_baseline.py                  # default DB, sha256 on if files exist
    python3 ingest_baseline.py --no-sha256      # skip corpus reads entirely
    python3 ingest_baseline.py --db other.sqlite --json other.json
"""

from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import json
import os
import sqlite3
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_DB = os.path.join(HERE, "codex_phase_i.sqlite")
DEFAULT_SCHEMA = os.path.join(HERE, "schema.sql")
DEFAULT_JSON = os.path.join(HERE, "baseline_inventory_sample.json")

# The primary historical corpus. This path is only ever read.
PRIMARY_MAC_ROOT = "/Users/archcore/solbian/codex"

CONTENT_STATUS = {
    "SOURCE", "HISTORICAL", "WORKING", "PROPOSED", "REVISION", "RELATED", "UNKNOWN",
}


def now_iso() -> str:
    return _dt.datetime.now(_dt.timezone.utc).replace(microsecond=0).isoformat()


def stable_id(prefix: str, *parts: str) -> str:
    """Deterministic id so re-running the ingest is idempotent."""
    digest = hashlib.sha1("\x1f".join(parts).encode("utf-8")).hexdigest()[:16]
    return f"{prefix}_{digest}"


def apply_schema(conn: sqlite3.Connection, schema_path: str) -> None:
    with open(schema_path, "r", encoding="utf-8") as fh:
        conn.executescript(fh.read())
    conn.commit()


# ---------------------------------------------------------------------------
# Classification / status mapping (never invents CANONICAL)
# ---------------------------------------------------------------------------
def classify_root(status: str, role: str, path: str) -> str:
    up = f"{status} {role} {path}".upper()
    if "GITHUB" in up or "REMOTE_HUB" in up or ":GH:" in up:
        return "HUB"
    if "BOX_MIRROR" in up or "MIRROR" in up or "ARCHIVE" in up:
        return "ARCHIVE"
    if "WORKING" in up and "HISTORICAL" not in up:
        return "WORKING"
    if "PRIMARY" in up or "LIVE" in up:
        return "CURRENT"
    if "HISTORICAL" in up:
        return "HISTORICAL"
    return "UNKNOWN"


def map_content_status(raw: str) -> str:
    """Map a raw Stage 2 label onto the content-status enum without inventing CANONICAL."""
    up = (raw or "").upper()
    if up in CONTENT_STATUS:
        return up
    if "HISTORICAL" in up:
        return "HISTORICAL"
    if "WORKING" in up:
        return "WORKING"
    if "CURRENT" in up or "LIVE" in up or "SOURCE" in up:
        return "SOURCE"  # a live/source surface, never CANONICAL
    if "PROPOS" in up:
        return "PROPOSED"
    return "UNKNOWN"


def infer_plurality_flags(rel_path: str, probable_role: str, notes: str) -> list[str]:
    """Preserve law/protocol/scroll plurality as flags. Flags only; nothing is merged."""
    hay = f"{rel_path} {probable_role} {notes}".lower()
    flags: list[str] = []

    if any(k in hay for k in ("law", "legal", "justice")):
        flags.append("law_material")
        # Named catalogue variants, when the label explicitly names them.
        for token, flag in (("law a", "law_catalogue_A"), ("law b", "law_catalogue_B"),
                            ("law c", "law_catalogue_C"), ("law b\u2032", "law_catalogue_Bprime"),
                            ("law b'", "law_catalogue_Bprime")):
            if token in hay:
                flags.append(flag)

    if "protocol" in hay:
        flags.append("protocol_material")
        if "gitea" in hay or "gitea-5" in hay:
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

    # de-duplicate, keep first-seen order
    seen: set[str] = set()
    out: list[str] = []
    for f in flags:
        if f not in seen:
            seen.add(f)
            out.append(f)
    return out


def guess_media_type(rel_path: str, entry_type: str) -> str:
    if entry_type == "directory":
        return "inode/directory"
    low = rel_path.lower()
    if low.endswith(".md"):
        return "text/markdown"
    if low.endswith(".sref"):
        return "application/x-sref"
    if low.endswith(".json"):
        return "application/json"
    if low.endswith(".ndjson"):
        return "application/x-ndjson"
    if low.endswith(".sum"):
        return "text/plain"
    if low.endswith(".bak"):
        return "application/octet-stream"
    return "application/octet-stream"


# ---------------------------------------------------------------------------
# Read-only sha256 (never writes)
# ---------------------------------------------------------------------------
def sha256_readonly(path: str) -> str | None:
    """Read-only sha256 of a corpus file, or None if absent/not a regular file."""
    try:
        if not os.path.isfile(path):
            return None
        h = hashlib.sha256()
        with open(path, "rb") as fh:          # READ ONLY
            for chunk in iter(lambda: fh.read(1 << 20), b""):
                h.update(chunk)
        return h.hexdigest()
    except OSError:
        return None


def upsert_root(conn, *, root_id, path, classification, role, notes, attribution, ts):
    conn.execute(
        """
        INSERT INTO corpus_root
            (id, path, classification, role, notes, status, attribution, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
            path=excluded.path,
            classification=excluded.classification,
            role=excluded.role,
            notes=excluded.notes,
            status=excluded.status,
            attribution=excluded.attribution,
            updated_at=excluded.updated_at
        """,
        (root_id, path, classification, role, notes, map_content_status(classification),
         attribution, ts, ts),
    )


def upsert_source_document(conn, row, ts):
    conn.execute(
        """
        INSERT INTO source_document
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
            updated_at=excluded.updated_at
        """,
        row,
    )


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Stage 3 read-only baseline ingest")
    parser.add_argument("--db", default=DEFAULT_DB, help="SQLite DB path")
    parser.add_argument("--schema", default=DEFAULT_SCHEMA, help="DDL path")
    parser.add_argument("--json", default=DEFAULT_JSON, help="Stage 2 inventory JSON")
    parser.add_argument("--no-sha256", action="store_true",
                        help="do not read corpus files for hashes")
    args = parser.parse_args(argv)

    ts = now_iso()

    conn = sqlite3.connect(args.db)
    conn.execute("PRAGMA foreign_keys = ON")
    apply_schema(conn, args.schema)

    with open(args.json, "r", encoding="utf-8") as fh:
        inv = json.load(fh)

    # -- 1. PRIMARY Mac root (CURRENT live path; HISTORICAL SoT inside) --------
    mac_notes = (
        "PRIMARY Mac working tree. CURRENT live path and the historical SoT "
        "(source_original/ + full MD scrolls). Registered notes-only; this "
        "ingest never modifies this tree. GH main tip is NOT historical. "
        f"Inventory provenance: {inv.get('primary_inventory_root')} "
        f"(generated_from {inv.get('generated_from')})."
    )
    upsert_root(
        conn,
        root_id=stable_id("croot", PRIMARY_MAC_ROOT),
        path=PRIMARY_MAC_ROOT,
        classification="CURRENT",
        role="PRIMARY_HISTORICAL_WORKING_TREE",
        notes=mac_notes,
        attribution="Stage 2 baseline inventory (CONSOLIDATION mac-codex-working-tree.tgz)",
        ts=ts,
    )
    mac_root_id = stable_id("croot", PRIMARY_MAC_ROOT)

    # -- 2. Other candidate corpus roots from the inventory -------------------
    root_ids: dict[str, str] = {}
    for cand in inv.get("candidates", []):
        raw_path = str(cand.get("path", ""))
        # Normalise the Mac candidate onto the real, canonical Mac path.
        if "CANDIDATE:Mac:" in raw_path:
            path = PRIMARY_MAC_ROOT
            role = "PRIMARY_HISTORICAL_WORKING_TREE"
            classification = "CURRENT"
        else:
            path = raw_path
            role = cand.get("probable_role") or "UNKNOWN"
            classification = classify_root(cand.get("status", ""), role, raw_path)

        root_id = stable_id("croot", path)
        root_ids[raw_path] = root_id
        if root_id == mac_root_id:
            continue  # already registered from the authoritative path
        notes = cand.get("notes") or ""
        rel = cand.get("relationships") or []
        if rel:
            notes = (notes + " | relationships: " + "; ".join(map(str, rel))).strip(" |")
        upsert_root(
            conn,
            root_id=root_id,
            path=path,
            classification=classification,
            role=role,
            notes=notes,
            attribution=cand.get("source_surface") or raw_path,
            ts=ts,
        )

    conn.commit()

    # -- 3. source_document rows from entries_sample --------------------------
    inserted = 0
    hashed = 0
    flag_counts: dict[str, int] = {}
    for entry in inv.get("entries_sample", []):
        rel_path = str(entry.get("path", "")).strip()
        if not rel_path:
            continue
        probable_role = entry.get("probable_role") or "UNKNOWN"
        notes = entry.get("notes") or ""
        inventory_status = entry.get("status") or "UNKNOWN"
        flags = infer_plurality_flags(rel_path, probable_role, notes)
        for f in flags:
            flag_counts[f] = flag_counts.get(f, 0) + 1

        sha = None
        if not args.no_sha256 and entry.get("type") == "file":
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
            entry.get("source_surface") or "baseline_inventory_sample.json",
            ts,
            ts,
        )
        upsert_source_document(conn, row, ts)
        inserted += 1

    conn.commit()

    counts = {
        t: conn.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
        for t in ("corpus_root", "source_document", "conversation", "message",
                  "codex_document", "concept", "relationship", "proposal",
                  "revision", "provenance_link")
    }
    conn.close()

    print(f"db                 : {args.db}")
    print(f"schema applied     : {args.schema}")
    print(f"inventory json     : {args.json}")
    print(f"roots registered   : {counts['corpus_root']}")
    print(f"source_documents   : {counts['source_document']} "
          f"(from {inserted} sample entries; sha256 computed={hashed})")
    print(f"plurality flag use : {json.dumps(flag_counts, sort_keys=True)}")
    print(f"table counts       : {json.dumps(counts, sort_keys=True)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
