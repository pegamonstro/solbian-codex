#!/usr/bin/env python3
"""Codex Solbian — Phase I · Stage 5 · deterministic Codex engine (prototype).

Turns the preserved Stage 3 source index into *inspectable observations* and
*PROPOSED records*.  It is deliberately boring: Python standard library +
``sqlite3`` only, no network, no hidden model calls.

Guarantees
----------
* The Stage 3 store is the **source of truth** and is only ever *read*.
  By default the engine writes to a local working copy
  ``data/codex_phase_i.sqlite`` created on first run (this is the same pattern
  Stage 4 uses, and the only location the current file sandbox permits).
* ``source_document`` is **never** inserted, updated or deleted.  A row-count
  and digest check runs before and after every ``run``.
* Rows are written only with status ``PROPOSED`` or ``WORKING``.
* No ``CANONICAL`` value is ever produced — the enum does not contain it and a
  guard scans every status/confidence column before and after each run.
* ``/Users/archcore/solbian/codex`` (the Mac corpus) is never written to.  A
  guard refuses any ``--db`` path that resolves inside it.
* Every proposal / concept written by the engine has at least one
  ``provenance_link`` to a ``source_document`` and/or ``message``.

Distinctions kept visible
-------------------------
* SOURCE        — untouched ``source_document`` / ``message`` rows.
* INTERPRETATION— anything the engine *infers* (notes carry the literal tag
                  ``INTERPRETATION``; no such row is ever called a fact).
* PROPOSAL      — ``proposal`` rows, status ``PROPOSED``, awaiting human review.

CLI
---
    python3 engine.py run [--kind ...] [--llm] [--dry-run] [--reset]
    python3 engine.py list-proposals [--status PROPOSED] [--json]
    python3 engine.py show <id|prefix> [--json]
    python3 engine.py list-runs [--json]

LLM use is optional and **off by default**.  ``--llm`` only does something when
``SOLBIAN_LLM_CMD`` is set to an external command; its output is stored as a
clearly-labelled INTERPRETATION proposal and never consolidated.
"""

from __future__ import annotations

import argparse
import collections
import datetime as _dt
import hashlib
import json
import os
import re
import shlex
import shutil
import sqlite3
import subprocess
import sys

# --------------------------------------------------------------------------- #
# Constants
# --------------------------------------------------------------------------- #

HERE = os.path.dirname(os.path.abspath(__file__))
ENGINE_VERSION = "stage5-1.0.0"

# Stage 3 store = source of truth (read-only).
STAGE3_DB = "/Users/archcore/solbian/codex-phase-i-stage3/codex_phase_i.sqlite"
# Local working copy the engine actually writes to.
DEFAULT_DB = os.path.join(HERE, "data", "codex_phase_i.sqlite")
# The Mac corpus: read-only, never written.  (The engine does not even read it.)
MAC_CORPUS_ROOT = "/Users/archcore/solbian/codex"

# Marker on every row the engine creates, so re-runs / resets are auditable.
ENGINE_ATTR_PREFIX = "engine:stage5:"

# Content-status values the engine is allowed to write (CANONICAL is absent).
ALLOWED_WRITE_STATUS = {"PROPOSED", "WORKING"}

KINDS = ("plurality", "duplicates", "underdeveloped", "durable", "discussion")

# Optional table; created in the working copy if missing (kept minimal).
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

# --------------------------------------------------------------------------- #
# Small helpers
# --------------------------------------------------------------------------- #


class EngineError(Exception):
    """A deterministic, user-facing engine failure."""


def now_iso() -> str:
    return _dt.datetime.now(_dt.timezone.utc).replace(microsecond=0).isoformat()


def det_id(prefix: str, *parts: str) -> str:
    """Deterministic id: same inputs -> same id.  Makes re-runs idempotent."""
    digest = hashlib.sha1("\x1f".join(str(p) for p in parts).encode("utf-8")).hexdigest()[:16]
    return f"{prefix}_{digest}"


def basename_of(rel_path: str) -> str:
    return rel_path.rsplit("/", 1)[-1]


def dirname_of(rel_path: str) -> str:
    return rel_path.rsplit("/", 1)[0] if "/" in rel_path else ""


# File-suffix noise stripped before a title is tokenised.
_STRIP_SUFFIXES = (".sum", ".bak", ".swp", ".tmp", ".orig")


def stem_of(rel_path: str) -> str:
    """Title of a source document: basename without backup/summary/extension."""
    name = basename_of(rel_path)
    while True:
        root, ext = os.path.splitext(name)
        if ext.lower() in _STRIP_SUFFIXES and root:
            name = root
        else:
            break
    return os.path.splitext(name)[0].lower()


_TOKEN_RE = re.compile(r"[a-z0-9]+")

# Structural / file-system words are not concept candidates.
STOPWORDS = {
    "codex", "solbian", "source", "original", "sum", "bak", "swp", "tmp", "orig",
    "index", "notes", "note", "readme", "json", "ndjson", "txt", "markdown",
    "the", "and", "for", "with", "from", "into", "over", "under", "this", "that",
    "these", "those", "http", "https", "www", "com", "org", "net",
    "scroll", "scrolls", "chapter", "chapters", "protocol", "protocols",
    "persona", "personae", "glossary", "manifest", "macosx", "ds", "store",
    "file", "files", "list", "sample", "full", "all", "new", "old",
}


def tokenize(text: str) -> list[str]:
    return [
        t for t in _TOKEN_RE.findall(text.lower())
        if len(t) >= 4 and not t.isdigit() and t not in STOPWORDS
    ]


def title_tokens(rel_path: str) -> set[str]:
    return set(tokenize(stem_of(rel_path)))


def pretty_json(value) -> str:
    return json.dumps(value, indent=2, sort_keys=True)


# --------------------------------------------------------------------------- #
# Database bootstrap / guards
# --------------------------------------------------------------------------- #


def check_db_write_allowed(db_path: str) -> None:
    """Refuse to open for writing anything inside the Mac corpus."""
    real = os.path.realpath(os.path.abspath(db_path))
    corpus = os.path.realpath(MAC_CORPUS_ROOT)
    if real == corpus or real.startswith(corpus + os.sep):
        raise EngineError(
            f"refusing to write inside the Mac corpus ({MAC_CORPUS_ROOT}): {db_path}"
        )


def ensure_db(db_path: str, sot_path: str = STAGE3_DB, refresh: bool = False) -> str:
    """Make sure the working DB exists.  Copy the SoT store if needed."""
    check_db_write_allowed(db_path)
    db_path = os.path.abspath(db_path)
    if not os.path.exists(db_path) or refresh:
        sot = os.path.abspath(sot_path)
        if not os.path.exists(sot):
            raise EngineError(f"source-of-truth store not found: {sot}")
        check_db_write_allowed(sot)
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        shutil.copyfile(sot, db_path)
    return db_path


def connect(db_path: str) -> sqlite3.Connection:
    if not os.path.exists(db_path):
        raise EngineError(f"database not found: {db_path} (use engine.py run to create it)")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.executescript(ANALYSIS_RUN_DDL)
    return conn


def _tables(conn: sqlite3.Connection) -> list[str]:
    return [
        r[0] for r in conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
        )
    ]


def check_no_canonical(conn: sqlite3.Connection) -> None:
    """Assert no status/confidence column anywhere holds 'CANONICAL'."""
    offenders = []
    for table in _tables(conn):
        cols = [r[1] for r in conn.execute(f"PRAGMA table_info({table})")]
        for col in cols:
            if col in ("status", "confidence", "inventory_status", "classification"):
                n = conn.execute(
                    f"SELECT COUNT(*) FROM {table} WHERE {col} = 'CANONICAL'"
                ).fetchone()[0]
                if n:
                    offenders.append(f"{table}.{col}={n}")
    if offenders:
        raise EngineError("CANONICAL value detected: " + ", ".join(offenders))


def source_document_digest(conn: sqlite3.Connection) -> tuple[int, str]:
    """A cheap digest of source_document so we can prove it was untouched."""
    h = hashlib.sha1()
    count = 0
    for row in conn.execute(
        "SELECT id, rel_path, status, updated_at FROM source_document ORDER BY id"
    ):
        count += 1
        h.update(("\x1f".join(str(x) for x in row)).encode("utf-8"))
        h.update(b"\x1e")
    return count, h.hexdigest()


# --------------------------------------------------------------------------- #
# Loading the source index
# --------------------------------------------------------------------------- #


def load_docs(conn: sqlite3.Connection) -> list[dict]:
    docs = []
    for r in conn.execute(
        "SELECT id, corpus_root_id, rel_path, media_type, probable_role, "
        "       inventory_status, status, plurality_flags "
        "FROM source_document ORDER BY rel_path, id"
    ):
        flags: list[str] = []
        raw = r["plurality_flags"]
        if raw:
            try:
                parsed = json.loads(raw)
                if isinstance(parsed, list):
                    flags = [str(x) for x in parsed]
            except (ValueError, TypeError):
                flags = []
        docs.append({
            "id": r["id"],
            "corpus_root_id": r["corpus_root_id"],
            "rel_path": r["rel_path"],
            "media_type": r["media_type"] or "",
            "probable_role": r["probable_role"] or "",
            "inventory_status": r["inventory_status"] or "",
            "status": r["status"] or "",
            "flags": flags,
        })
    return docs


def load_roots(conn: sqlite3.Connection) -> dict[str, str]:
    return {r["id"]: r["path"] for r in conn.execute("SELECT id, path FROM corpus_root")}


# --------------------------------------------------------------------------- #
# Writers — all engine writes funnel through here, all statuses constrained
# --------------------------------------------------------------------------- #


def write_proposal(ctx: "Ctx", pid: str, summary: str, body: str, based_on: list[str]) -> None:
    status = "PROPOSED"
    _require_status(status)
    attr = f"{ENGINE_ATTR_PREFIX}{ctx.kind}:{ctx.run_id}"
    ctx.conn.execute(
        """
        INSERT INTO proposal (id, summary, body, based_on_json, status, attribution,
                              created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
            summary       = excluded.summary,
            body          = excluded.body,
            based_on_json = excluded.based_on_json,
            attribution   = excluded.attribution,
            updated_at    = excluded.updated_at
        """,
        (pid, summary, body, json.dumps(based_on), status, attr, ctx.now, ctx.now),
    )
    ctx.wrote["proposal"] += 1


def write_concept(ctx: "Ctx", cid: str, name: str, notes: str) -> None:
    status = "PROPOSED"
    _require_status(status)
    attr = f"{ENGINE_ATTR_PREFIX}{ctx.kind}:{ctx.run_id}"
    ctx.conn.execute(
        """
        INSERT INTO concept (id, name, definition, status, notes, attribution,
                             created_at, updated_at)
        VALUES (?, ?, NULL, ?, ?, ?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
            notes      = excluded.notes,
            attribution= excluded.attribution,
            updated_at = excluded.updated_at
        """,
        (cid, name, status, notes, attr, ctx.now, ctx.now),
    )
    ctx.wrote["concept"] += 1


def write_relationship(ctx: "Ctx", rid: str, from_id: str, from_kind: str,
                       to_id: str, to_kind: str, rel_type: str, confidence: str) -> None:
    status = "PROPOSED"
    _require_status(status)
    _require_confidence(confidence)
    ctx.conn.execute(
        """
        INSERT INTO relationship (id, from_id, from_kind, to_id, to_kind, rel_type,
                                  confidence, status, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
            rel_type   = excluded.rel_type,
            confidence = excluded.confidence,
            updated_at = excluded.updated_at
        """,
        (rid, from_id, from_kind, to_id, to_kind, rel_type, confidence, status,
         ctx.now, ctx.now),
    )
    ctx.wrote["relationship"] += 1


def write_provenance(ctx: "Ctx", subject_kind: str, subject_id: str,
                     source_kind: str, source_id: str, note: str,
                     confidence: str) -> None:
    status = "PROPOSED" if subject_kind == "proposal" else "WORKING"
    _require_status(status)
    _require_confidence(confidence)
    vid = det_id("prov", subject_kind, subject_id, source_kind, source_id)
    ctx.conn.execute(
        """
        INSERT INTO provenance_link (id, subject_kind, subject_id, source_kind,
                                     source_id, note, confidence, status,
                                     created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
            note       = excluded.note,
            confidence = excluded.confidence,
            updated_at = excluded.updated_at
        """,
        (vid, subject_kind, subject_id, source_kind, source_id, note, confidence,
         status, ctx.now, ctx.now),
    )
    ctx.wrote["provenance_link"] += 1


def write_analysis_run(ctx: "Ctx", status: str, summary: dict, started_at: str,
                       finished_at: str | None) -> None:
    ctx.conn.execute(
        """
        INSERT INTO analysis_run (id, started_at, finished_at, kind, summary_json,
                                  status, engine_version, attribution,
                                  created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
            started_at   = excluded.started_at,
            finished_at  = excluded.finished_at,
            summary_json = excluded.summary_json,
            status       = excluded.status,
            engine_version = excluded.engine_version,
            attribution  = excluded.attribution,
            updated_at   = excluded.updated_at
        """,
        (ctx.run_id, started_at, finished_at, ctx.kind, json.dumps(summary),
         status, ENGINE_VERSION, f"{ENGINE_ATTR_PREFIX}{ctx.kind}:{ctx.run_id}",
         ctx.now, ctx.now),
    )


def _require_status(status: str) -> None:
    if status not in ALLOWED_WRITE_STATUS:
        raise EngineError(f"refusing to write illegal content status: {status!r}")


def _require_confidence(confidence: str) -> None:
    if confidence not in ("TEXT-SUPPORTED", "TITLE-LEVEL", "SYNTHESIS", "UNKNOWN"):
        raise EngineError(f"refusing to write illegal confidence: {confidence!r}")


class Ctx:
    """Per-kind analysis context."""

    def __init__(self, conn, docs, roots, kind, run_id, args):
        self.conn = conn
        self.docs = docs
        self.roots = roots
        self.kind = kind
        self.run_id = run_id
        self.args = args
        self.now = now_iso()
        self.wrote = collections.Counter()


# --------------------------------------------------------------------------- #
# Analyzer 1 — plurality reminders
# --------------------------------------------------------------------------- #

# Path patterns that indicate plurality-preserving material, mapped to the
# plurality flag that (when present) already carries the same signal.
PATH_PATTERNS = {
    "laws": (re.compile(r"(?:^|[/_.\-])law(?:s)?(?:[/_.\-]|$)"), "law_material"),
    "protocols": (re.compile(r"(?:^|[/_.\-])protocol(?:s)?(?:[/_.\-]|$)"), "protocol_material"),
    "scrolls": (re.compile(r"(?:^|[/_.\-])scroll(?:s)?(?:[/_.\-]|$)"), "scroll_material"),
}

# Extra prose for the anomaly flags (kept factual, no merging).
FLAG_NOTES = {
    "scroll_md_vs_sref_ordinals": (
        "Markdown scrolls and .sref scrolls may carry different ordinals; the "
        "ordering is not authoritative and must not be flattened into one sequence."
    ),
    "scroll_20_anomaly": (
        "Scroll 20 is already recorded as an anomaly. Preserve both readings; "
        "do not renumber, merge or discard either copy."
    ),
    "law_material": (
        "Law material is plural (base + extended + bylaws). Preserve every "
        "variant; no variant is privileged."
    ),
    "protocol_material": (
        "Protocol material is plural (numbered protocols and decision protocol). "
        "Preserve all versions; no variant is privileged."
    ),
}


def analyze_plurality(ctx: Ctx) -> dict:
    docs = ctx.docs
    by_flag: dict[str, list[dict]] = collections.defaultdict(list)
    for d in docs:
        for flag in d["flags"]:
            by_flag[flag].append(d)

    proposals = 0
    for flag in sorted(by_flag):
        group = sorted(by_flag[flag], key=lambda d: (d["rel_path"], d["id"]))
        pid = det_id("prop_plurality_flag", flag)
        roles = collections.Counter(d["probable_role"] or "UNKNOWN" for d in group)
        role_line = ", ".join(f"{k}={v}" for k, v in sorted(roles.items()))
        extra = FLAG_NOTES.get(flag, "")
        body = (
            f"OBSERVATION (deterministic, TITLE-LEVEL): {len(group)} source_document "
            f"row(s) carry the plurality flag {flag!r}.\n\n"
            f"Roles: {role_line}\n\n"
            f"{extra + chr(10) + chr(10) if extra else ''}"
            "REMINDER: preserve plurality — do not merge, renumber, flatten or "
            "delete any variant. This is a reminder record, not doctrine; no "
            "canonical value exists in this store.\n\n"
            "Examples:\n" + "\n".join(f"  - {d['rel_path']}" for d in group[:20])
        )
        write_proposal(
            ctx, pid,
            f"Preserve plurality: flag {flag!r} on {len(group)} row(s) — do not merge",
            body, [d["id"] for d in group[:50]],
        )
        for d in group[:10]:
            write_provenance(
                ctx, "proposal", pid, "source_document", d["id"],
                f"plurality_flags contains {flag!r}", "TITLE-LEVEL",
            )
        proposals += 1

    # Path-pattern material not already covered by a matching flag.
    pattern_props = 0
    for pattern_name, (rx, mapped_flag) in sorted(PATH_PATTERNS.items()):
        matched, uncovered = [], []
        for d in docs:
            if rx.search(d["rel_path"].lower()):
                matched.append(d)
                if mapped_flag not in d["flags"]:
                    uncovered.append(d)
        if not uncovered:
            continue
        uncovered.sort(key=lambda d: (d["rel_path"], d["id"]))
        pid = det_id("prop_plurality_path", pattern_name)
        body = (
            f"OBSERVATION (deterministic, TITLE-LEVEL): {len(uncovered)} path(s) "
            f"match the {pattern_name!r} pattern but do not carry the "
            f"{mapped_flag!r} plurality flag.\n\n"
            f"Matched total: {len(matched)}; covered by flag: "
            f"{len(matched) - len(uncovered)}; uncovered: {len(uncovered)}.\n\n"
            "REMINDER: if these are genuine variants they must stay plural; this "
            "proposal only asks a human to check flag coverage. No merge.\n\n"
            "Uncovered examples:\n"
            + "\n".join(f"  - {d['rel_path']}" for d in uncovered[:20])
        )
        write_proposal(
            ctx, pid,
            f"Plurality coverage gap: {len(uncovered)} {pattern_name} path(s) lack "
            f"{mapped_flag!r}",
            body, [d["id"] for d in uncovered[:50]],
        )
        for d in uncovered[:10]:
            write_provenance(
                ctx, "proposal", pid, "source_document", d["id"],
                f"path matches {pattern_name!r}; no {mapped_flag!r} flag", "TITLE-LEVEL",
            )
        proposals += 1
        pattern_props += 1

    # Explicit scroll-20 mention even if the anomaly flag is missing.
    scroll20 = [d for d in docs if re.search(r"scroll[_\- ]?20(?:[/_.\-]|$)", d["rel_path"].lower())]
    scroll20_prop = 0
    if scroll20 and "scroll_20_anomaly" not in by_flag:
        scroll20.sort(key=lambda d: (d["rel_path"], d["id"]))
        pid = det_id("prop_plurality_scroll20", "scroll_20")
        body = (
            f"OBSERVATION (deterministic, TITLE-LEVEL): {len(scroll20)} path(s) "
            "reference scroll 20, but no row carries the 'scroll_20_anomaly' flag.\n\n"
            "REMINDER: scroll 20 is a known ordinal anomaly. Preserve both readings; "
            "do not renumber or merge. Ask a human to confirm flag coverage.\n\n"
            + "\n".join(f"  - {d['rel_path']}" for d in scroll20[:20])
        )
        write_proposal(
            ctx, pid,
            f"Plurality check: scroll 20 referenced by {len(scroll20)} path(s), no anomaly flag",
            body, [d["id"] for d in scroll20[:50]],
        )
        for d in scroll20[:10]:
            write_provenance(
                ctx, "proposal", pid, "source_document", d["id"],
                "scroll 20 path; anomaly flag absent", "TITLE-LEVEL",
            )
        proposals += 1
        scroll20_prop = 1

    return {
        "flags_seen": sorted(by_flag),
        "flag_proposals": proposals - pattern_props - scroll20_prop,
        "path_gap_proposals": pattern_props,
        "scroll20_proposals": scroll20_prop,
        "proposals": proposals,
    }


# --------------------------------------------------------------------------- #
# Analyzer 2 — duplicate basenames
# --------------------------------------------------------------------------- #


def analyze_duplicates(ctx: Ctx) -> dict:
    groups: dict[str, list[dict]] = collections.defaultdict(list)
    for d in ctx.docs:
        name = basename_of(d["rel_path"]).lower()
        if name:
            groups[name].append(d)

    file_groups = []      # >=2 real files sharing a basename in different dirs
    dir_only = []         # basename collides only as directories
    for name, ds in groups.items():
        if len(ds) < 2:
            continue
        locations = {(d["corpus_root_id"], dirname_of(d["rel_path"])) for d in ds}
        if len(locations) < 2:
            continue
        nondir = [d for d in ds if d["media_type"] != "inode/directory"]
        if len(nondir) >= 2:
            file_groups.append((name, sorted(ds, key=lambda d: (d["rel_path"], d["id"])), nondir))
        else:
            dir_only.append((name, sorted(ds, key=lambda d: (d["rel_path"], d["id"]))))

    file_groups.sort(key=lambda t: (-len(t[1]), t[0]))
    dir_only.sort(key=lambda t: (-len(t[1]), t[0]))

    proposals = 0
    for name, ds, nondir in file_groups:
        pid = det_id("prop_dupe_basename", name)
        roots = sorted({d["corpus_root_id"] for d in ds})
        has_macosx = any("__MACOSX" in d["rel_path"] for d in ds)
        lines = []
        for d in ds:
            root_path = ctx.roots.get(d["corpus_root_id"], d["corpus_root_id"])
            lines.append(
                f"  - [{root_path}] {d['rel_path']}  "
                f"(role={d['probable_role'] or 'UNKNOWN'}, status={d['status']})"
            )
        body = (
            f"OBSERVATION (deterministic, TITLE-LEVEL): basename {name!r} occurs in "
            f"{len(ds)} location(s) across {len(roots)} corpus root(s).\n\n"
            f"Non-directory copies: {len(nondir)}.\n"
            + ("This group includes an __MACOSX mirror; likely junk, but do not "
               "delete it without review.\n" if has_macosx else "")
            + "\nCandidates (source order preserved):\n" + "\n".join(lines) +
            "\n\nPROPOSAL: review whether these are the same work, intentionally "
            "plural, or unrelated. No auto-merge; nothing here is deleted or "
            "overwritten.\n"
        )
        write_proposal(
            ctx, pid,
            f"Duplicate basename {name!r} in {len(ds)} location(s) — review before any merge",
            body, [d["id"] for d in ds[:50]],
        )
        for d in ds[:10]:
            write_provenance(
                ctx, "proposal", pid, "source_document", d["id"],
                f"shares basename {name!r} with {len(ds) - 1} other row(s)", "TITLE-LEVEL",
            )
        # Candidate title-level links between the copies (first vs the rest).
        for other in ds[1:6]:
            rid = det_id("rel_dupe", ds[0]["id"], other["id"])
            write_relationship(
                ctx, rid, ds[0]["id"], "source_document", other["id"], "source_document",
                "BASENAME_COLLISION", "TITLE-LEVEL",
            )
        proposals += 1

    if dir_only:
        pid = det_id("prop_dupe_dironly", "directories")
        listed = [f"  - {name!r} in {len(ds)} location(s)" for name, ds in dir_only[:20]]
        body = (
            f"OBSERVATION (deterministic, TITLE-LEVEL): {len(dir_only)} basename(s) "
            "collide only as directories (no two non-directory files share the name).\n\n"
            "These are usually structural mirrors, not duplicate documents, but the "
            "mirrors must not be silently merged or removed.\n\n"
            + "\n".join(listed)
        )
        write_proposal(
            ctx, pid,
            f"Directory-only basename collisions: {len(dir_only)} name(s) — preserve mirrors",
            body, [d["id"] for _, ds in dir_only[:20] for d in ds[:2]],
        )
        rep = dir_only[0][1][0]
        write_provenance(
            ctx, "proposal", pid, "source_document", rep["id"],
            "representative of directory-only basename collisions", "TITLE-LEVEL",
        )
        proposals += 1

    return {
        "file_groups": len(file_groups),
        "directory_only_groups": len(dir_only),
        "proposals": proposals,
    }


# --------------------------------------------------------------------------- #
# Analyzer 3 — underdeveloped concepts
# --------------------------------------------------------------------------- #


def _defined_tokens(ctx: Ctx) -> set[str]:
    """Tokens that already have a dedicated document, glossary hit or concept."""
    defined: set[str] = set()
    for d in ctx.docs:
        stem = stem_of(d["rel_path"])
        if stem:
            defined.add(stem)
        if d["probable_role"] == "GLOSSARY" or "glossary" in d["rel_path"].lower():
            defined.update(tokenize(d["rel_path"]))
    for r in ctx.conn.execute("SELECT name, definition FROM concept"):
        name = (r["name"] or "").lower()
        if name and (r["definition"] or "").strip():
            defined.add(name)
    for r in ctx.conn.execute("SELECT title FROM codex_document WHERE title IS NOT NULL"):
        defined.update(tokenize(r["title"] or ""))
    return defined


def underdeveloped_findings(ctx: Ctx, min_freq: int, limit: int) -> list[tuple[str, int, list[dict]]]:
    """Tokens frequent in titles with no dedicated document/glossary hit."""
    freq: collections.Counter = collections.Counter()
    per_token: dict[str, list[dict]] = collections.defaultdict(list)
    for d in ctx.docs:
        for token in sorted(title_tokens(d["rel_path"])):
            freq[token] += 1
            per_token[token].append(d)

    defined = _defined_tokens(ctx)
    findings = []
    for token, count in sorted(freq.items(), key=lambda kv: (-kv[1], kv[0])):
        if count < min_freq or token in defined:
            continue
        docs = sorted(per_token[token], key=lambda d: (d["rel_path"], d["id"]))
        findings.append((token, count, docs))
        if len(findings) >= limit:
            break
    return findings


def analyze_underdeveloped(ctx: Ctx) -> dict:
    min_freq = ctx.args.min_freq
    limit = ctx.args.max_findings
    findings = underdeveloped_findings(ctx, min_freq, limit)

    for token, count, docs in findings:
        cid = det_id("concept_under", token)
        pid = det_id("prop_under", token)
        notes = (
            f"INTERPRETATION: candidate concept token {token!r} appears in {count} "
            "distinct source title(s) but has no dedicated document, glossary entry "
            "or stored definition. Status PROPOSED; not a definition."
        )
        write_concept(ctx, cid, token, notes)
        body = (
            f"OBSERVATION (deterministic, TITLE-LEVEL): the token {token!r} appears in "
            f"{count} distinct source-document title(s).\n"
            "No source_document is dedicated to it (exact title match) and it has no "
            "glossary entry or stored definition.\n\n"
            "INTERPRETATION: this looks underdeveloped. Either a definition/discussion "
            "should be drafted, or the token is incidental vocabulary.\n\n"
            f"Created concept candidate: {cid}\n\n"
            "Example titles:\n" + "\n".join(f"  - {d['rel_path']}" for d in docs[:15])
        )
        write_proposal(
            ctx, pid,
            f"UNDERDEVELOPED: {token!r} in {count} titles with no definition "
            f"(min_freq={min_freq})",
            body, [d["id"] for d in docs[:50]] + [cid],
        )
        for d in docs[:8]:
            write_provenance(
                ctx, "proposal", pid, "source_document", d["id"],
                f"title token {token!r}", "TITLE-LEVEL",
            )
            write_provenance(
                ctx, "concept", cid, "source_document", d["id"],
                f"title token {token!r}", "TITLE-LEVEL",
            )
        write_relationship(
            ctx, det_id("rel_under", pid, cid), pid, "proposal", cid, "concept",
            "PROPOSES_CONCEPT", "SYNTHESIS",
        )
        for d in docs[:5]:
            write_relationship(
                ctx, det_id("rel_under_doc", cid, d["id"]), cid, "concept",
                d["id"], "source_document", "MENTIONED_IN", "TITLE-LEVEL",
            )

    return {"min_freq": min_freq, "limit": limit, "findings": len(findings),
            "tokens": [t for t, _, _ in findings]}


# --------------------------------------------------------------------------- #
# Analyzer 4 — durable candidates from long messages
# --------------------------------------------------------------------------- #

MIN_MESSAGE_CHARS = 280
MAX_QUOTE_CHARS = 400


def analyze_durable(ctx: Ctx) -> dict:
    total_conv = ctx.conn.execute("SELECT COUNT(*) FROM conversation").fetchone()[0]
    total_msg = ctx.conn.execute("SELECT COUNT(*) FROM message").fetchone()[0]
    if total_msg == 0:
        return {
            "conversations": total_conv,
            "messages": 0,
            "long_messages": 0,
            "proposals": 0,
            "note": "skipped: no message rows in store (Stage 3 ingested 0 conversations)",
        }

    cap = ctx.args.max_findings
    rows = list(ctx.conn.execute(
        "SELECT m.id, m.conversation_id, m.seq, m.role, m.body, m.sent_at "
        "FROM message m ORDER BY m.conversation_id, m.seq, m.id"
    ))
    long_rows = [r for r in rows if len((r["body"] or "").strip()) >= MIN_MESSAGE_CHARS]
    proposals = 0
    for r in long_rows[:cap]:
        body_text = (r["body"] or "").strip()
        quote = body_text[:MAX_QUOTE_CHARS]
        pid = det_id("prop_durable_msg", r["id"])
        body = (
            f"OBSERVATION (deterministic): message {r['id']} in conversation "
            f"{r['conversation_id']} (seq {r['seq']}, role {r['role'] or 'unknown'}) "
            f"is {len(body_text)} characters long.\n\n"
            "INTERPRETATION: long messages are durable-candidate material, not yet "
            "Codex content. This proposal only asks a human to review it.\n\n"
            "Stored quote (evidence, TEXT-SUPPORTED):\n"
            f"  {quote!r}\n"
        )
        write_proposal(
            ctx, pid,
            f"Durable candidate: long message {r['id']} "
            f"({len(body_text)} chars, conversation {r['conversation_id']})",
            body, [r["id"], r["conversation_id"]],
        )
        write_provenance(
            ctx, "proposal", pid, "message", r["id"],
            f"quote evidence: {quote[:160]!r}", "TEXT-SUPPORTED",
        )
        write_provenance(
            ctx, "proposal", pid, "conversation", r["conversation_id"],
            f"message seq {r['seq']}", "TITLE-LEVEL",
        )
        proposals += 1

    return {
        "conversations": total_conv,
        "messages": total_msg,
        "long_messages": len(long_rows),
        "min_message_chars": MIN_MESSAGE_CHARS,
        "proposals": proposals,
        "truncated": len(long_rows) > proposals,
    }


# --------------------------------------------------------------------------- #
# Analyzer 5 — discussion topics for observed gaps
# --------------------------------------------------------------------------- #


def analyze_discussion(ctx: Ctx) -> dict:
    topics = 0

    # (a) Underdeveloped tokens -> "how should this be defined?" topics.
    findings = underdeveloped_findings(ctx, ctx.args.min_freq, min(ctx.args.max_findings, 8))
    for token, count, docs in findings:
        pid = det_id("prop_disc_under", token)
        body = (
            f"DISCUSSION TOPIC (INTERPRETATION/SYNTHESIS): the token {token!r} is used "
            f"in {count} source titles but has no definition.\n\n"
            "Questions for a human:\n"
            f"  1. Is {token!r} a first-class concept, an incidental word, or a label?\n"
            "  2. Which SOURCE document (if any) should define it?\n"
            "  3. Should the concept candidate be accepted, revised or dropped?\n\n"
            "Evidence titles:\n" + "\n".join(f"  - {d['rel_path']}" for d in docs[:10])
        )
        write_proposal(
            ctx, pid, f"Discussion topic: define or drop underdeveloped token {token!r}",
            body, [d["id"] for d in docs[:30]],
        )
        for d in docs[:5]:
            write_provenance(
                ctx, "proposal", pid, "source_document", d["id"],
                f"underdeveloped token {token!r}", "TITLE-LEVEL",
            )
        topics += 1

    # (b) Plurality anomalies -> "how do we preserve this?" topics.
    anomaly_flags = {"scroll_md_vs_sref_ordinals", "scroll_20_anomaly"}
    seen_flags: dict[str, list[dict]] = collections.defaultdict(list)
    for d in ctx.docs:
        for flag in d["flags"]:
            if flag in anomaly_flags:
                seen_flags[flag].append(d)
    for flag in sorted(seen_flags):
        docs = sorted(seen_flags[flag], key=lambda d: (d["rel_path"], d["id"]))
        pid = det_id("prop_disc_flag", flag)
        body = (
            f"DISCUSSION TOPIC (INTERPRETATION/SYNTHESIS): plurality flag {flag!r} is "
            f"present on {len(docs)} row(s).\n\n"
            "Question for a human: how should this plurality be preserved and "
            "referenced? Proposals must not merge, renumber or privilege a variant.\n\n"
            + "\n".join(f"  - {d['rel_path']}" for d in docs[:10])
        )
        write_proposal(ctx, pid, f"Discussion topic: preserve {flag!r} plurality", body,
                       [d["id"] for d in docs[:30]])
        for d in docs[:5]:
            write_provenance(ctx, "proposal", pid, "source_document", d["id"],
                             f"plurality flag {flag!r}", "TITLE-LEVEL")
        topics += 1

    # (c) Large duplicate clusters -> "which copy is which?" topics.
    groups: dict[str, list[dict]] = collections.defaultdict(list)
    for d in ctx.docs:
        name = basename_of(d["rel_path"]).lower()
        if name:
            groups[name].append(d)
    clusters = []
    for name, ds in groups.items():
        nondir = [d for d in ds if d["media_type"] != "inode/directory"]
        if len(nondir) >= 4:
            clusters.append((name, sorted(nondir, key=lambda d: (d["rel_path"], d["id"]))))
    clusters.sort(key=lambda t: (-len(t[1]), t[0]))
    for name, ds in clusters[:5]:
        pid = det_id("prop_disc_dupe", name)
        body = (
            f"DISCUSSION TOPIC (INTERPRETATION/SYNTHESIS): {len(ds)} non-directory "
            f"files share the basename {name!r}.\n\n"
            "Question for a human: are these the same work, intentional plurality, "
            "or unrelated files? No merge is proposed.\n\n"
            + "\n".join(f"  - {d['rel_path']}" for d in ds[:15])
        )
        write_proposal(ctx, pid, f"Discussion topic: reconcile {len(ds)} copies of {name!r}",
                       body, [d["id"] for d in ds[:30]])
        for d in ds[:5]:
            write_provenance(ctx, "proposal", pid, "source_document", d["id"],
                             f"duplicate basename {name!r}", "TITLE-LEVEL")
        topics += 1

    return {"topics": topics, "source": "underdeveloped + plurality anomalies + duplicate clusters"}


ANALYZERS = {
    "plurality": analyze_plurality,
    "duplicates": analyze_duplicates,
    "underdeveloped": analyze_underdeveloped,
    "durable": analyze_durable,
    "discussion": analyze_discussion,
}


# --------------------------------------------------------------------------- #
# Optional LLM hook (off by default; never auto-consolidates)
# --------------------------------------------------------------------------- #


def llm_hook(ctx: Ctx) -> dict:
    cmd = os.environ.get("SOLBIAN_LLM_CMD", "").strip()
    if not cmd:
        return {
            "requested": True,
            "backend": None,
            "proposals": 0,
            "note": "--llm requested but SOLBIAN_LLM_CMD is unset; "
                    "deterministic results only (no network calls).",
        }

    stats = {
        "source_documents": len(ctx.docs),
        "sample_titles": [d["rel_path"] for d in ctx.docs[:40]],
        "instruction": (
            "You are a read-only assistant to a Codex archive. Propose at most 3 "
            "observations. Do not assert doctrine. Do not use the word canonical."
        ),
    }
    prompt = "Corpus index summary:\n" + json.dumps(stats, indent=2)
    try:
        proc = subprocess.run(shlex.split(cmd), input=prompt, capture_output=True,
                              text=True, timeout=120)
    except (OSError, subprocess.SubprocessError) as exc:
        return {"requested": True, "backend": cmd, "proposals": 0, "error": str(exc)}
    if proc.returncode != 0:
        return {"requested": True, "backend": cmd, "proposals": 0,
                "error": f"exit {proc.returncode}: {proc.stderr.strip()[:200]}"}

    text = proc.stdout.strip()
    if not text:
        return {"requested": True, "backend": cmd, "proposals": 0, "note": "empty output"}

    # Deterministic id per run id + backend so repeated runs are idempotent.
    pid = det_id("prop_llm", ctx.run_id, hashlib.sha1(text.encode()).hexdigest())
    body = (
        "INTERPRETATION (LLM-generated, PROPOSED, not consolidated):\n\n"
        + text[:4000]
        + "\n\nThis row is a proposal only. A human must review it before any use."
    )
    write_proposal(ctx, pid, "LLM observation candidate (INTERPRETATION, review required)",
                   body, [d["id"] for d in ctx.docs[:10]])
    for d in ctx.docs[:5]:
        write_provenance(ctx, "proposal", pid, "source_document", d["id"],
                         "context document supplied to LLM hook", "SYNTHESIS")
    return {"requested": True, "backend": cmd, "proposals": 1}


# --------------------------------------------------------------------------- #
# run orchestration
# --------------------------------------------------------------------------- #


def resolve_kinds(raw) -> list[str]:
    if not raw:
        return list(KINDS)
    out: list[str] = []
    for item in raw:
        for piece in str(item).split(","):
            piece = piece.strip().lower()
            if not piece:
                continue
            if piece == "all":
                for k in KINDS:
                    if k not in out:
                        out.append(k)
            elif piece in ANALYZERS:
                if piece not in out:
                    out.append(piece)
            else:
                raise EngineError(f"unknown analysis kind: {piece!r} (choose from {', '.join(KINDS)})")
    return out


def reset_engine_rows(conn: sqlite3.Connection) -> dict:
    """Delete only rows the engine created (identified by marker/id prefix)."""
    prop_ids = [r[0] for r in conn.execute(
        "SELECT id FROM proposal WHERE attribution LIKE ?", (ENGINE_ATTR_PREFIX + "%",)
    )]
    concept_ids = [r[0] for r in conn.execute(
        "SELECT id FROM concept WHERE attribution LIKE ?", (ENGINE_ATTR_PREFIX + "%",)
    )]
    engine_ids = prop_ids + concept_ids
    removed = {"provenance_link": 0, "relationship": 0, "proposal": 0, "concept": 0,
               "analysis_run": 0}

    def _delete_where_in(table, column, ids):
        if not ids:
            return 0
        total = 0
        for i in range(0, len(ids), 400):
            chunk = ids[i:i + 400]
            q = ",".join("?" * len(chunk))
            cur = conn.execute(f"DELETE FROM {table} WHERE {column} IN ({q})", chunk)
            total += cur.rowcount
        return total

    removed["provenance_link"] += _delete_where_in("provenance_link", "subject_id", engine_ids)
    removed["relationship"] += _delete_where_in("relationship", "from_id", engine_ids)
    removed["relationship"] += _delete_where_in("relationship", "to_id", engine_ids)
    removed["proposal"] += _delete_where_in("proposal", "id", prop_ids)
    removed["concept"] += _delete_where_in("concept", "id", concept_ids)
    removed["analysis_run"] = conn.execute(
        "DELETE FROM analysis_run WHERE attribution LIKE ?", (ENGINE_ATTR_PREFIX + "%",)
    ).rowcount
    return removed


def cmd_run(args) -> int:
    db_path = ensure_db(args.db or DEFAULT_DB, args.sot, args.refresh_db)
    kinds = resolve_kinds(args.kind)
    conn = connect(db_path)

    llm_state = "ON" if args.llm else "OFF"
    print(f"Codex Phase I — Stage 5 engine {ENGINE_VERSION}  (LLM: {llm_state})")
    print(f"store : {db_path}")
    print(f"SoT   : {os.path.abspath(args.sot)} (read-only)")

    check_no_canonical(conn)
    before_count, before_digest = source_document_digest(conn)
    print(f"source_document before: {before_count}")

    if args.reset:
        removed = reset_engine_rows(conn)
        if not args.dry_run:
            conn.commit()
        print("reset : " + ", ".join(f"{k}={v}" for k, v in sorted(removed.items())))

    def commit() -> None:
        # A dry run keeps everything in one transaction and rolls back at the end.
        if not args.dry_run:
            conn.commit()

    docs = load_docs(conn)
    roots = load_roots(conn)
    any_error = False
    for kind in kinds:
        run_id = det_id("arun", kind, ENGINE_VERSION)
        ctx = Ctx(conn, docs, roots, kind, run_id, args)
        started = ctx.now
        write_analysis_run(ctx, "RUNNING", {}, started, None)
        commit()
        try:
            summary = ANALYZERS[kind](ctx)
            status = "OK"
        except Exception as exc:  # noqa: BLE001 - recorded, not hidden
            summary = {"error": f"{type(exc).__name__}: {exc}"}
            status = "ERROR"
            any_error = True
        finished = now_iso()
        write_analysis_run(ctx, status, summary, started, finished)
        commit()
        wrote = ", ".join(f"{k}={v}" for k, v in sorted(ctx.wrote.items())) or "no writes"
        print(f"[{kind:14s}] status={status} run={run_id}  {wrote}")

    if args.llm:
        ctx = Ctx(conn, docs, roots, "llm", det_id("arun", "llm", ENGINE_VERSION), args)
        result = llm_hook(ctx)
        commit()
        print(f"[{'llm':14s}] " + json.dumps(result, sort_keys=True))
        if result.get("error"):
            any_error = True
        if result.get("proposals"):
            write_analysis_run(ctx, "OK", result, ctx.now, now_iso())
            commit()

    # Hard guarantee: source_document was not touched.
    after_count, after_digest = source_document_digest(conn)
    if after_count != before_count or after_digest != before_digest:
        conn.rollback()
        conn.close()
        raise EngineError(
            "source_document changed during run — this must never happen "
            f"({before_count}/{before_digest[:8]} -> {after_count}/{after_digest[:8]}); rolled back"
        )
    check_no_canonical(conn)

    rows = {
        "proposal": conn.execute("SELECT COUNT(*) FROM proposal").fetchone()[0],
        "concept": conn.execute("SELECT COUNT(*) FROM concept").fetchone()[0],
        "relationship": conn.execute("SELECT COUNT(*) FROM relationship").fetchone()[0],
        "provenance_link": conn.execute("SELECT COUNT(*) FROM provenance_link").fetchone()[0],
    }
    print(f"source_document after : {after_count} (unchanged)")
    print("store totals      : " + ", ".join(f"{k}={v}" for k, v in rows.items()))
    print("legend            : SOURCE=untouched rows · INTERPRETATION=tagged notes · "
          "PROPOSAL=status PROPOSED")

    if args.dry_run:
        conn.rollback()
        print("dry-run           : no changes committed")
    conn.close()
    return 1 if any_error else 0


# --------------------------------------------------------------------------- #
# Inspectors
# --------------------------------------------------------------------------- #


def _proposal_rows(conn, statuses=None, limit=200):
    sql = ("SELECT p.id, p.status, p.summary, p.attribution, p.created_at, "
           "(SELECT COUNT(*) FROM provenance_link v WHERE v.subject_kind='proposal' "
           " AND v.subject_id = p.id) AS prov "
           "FROM proposal p")
    params: list = []
    if statuses:
        sql += " WHERE p.status IN (" + ",".join("?" * len(statuses)) + ")"
        params.extend(statuses)
    sql += " ORDER BY p.created_at, p.id LIMIT ?"
    params.append(limit)
    return list(conn.execute(sql, params))


def cmd_list_proposals(args) -> int:
    db_path = ensure_db(args.db or DEFAULT_DB, args.sot)
    conn = connect(db_path)
    statuses = args.status or None
    rows = _proposal_rows(conn, statuses, args.limit)
    if args.json:
        print(pretty_json([dict(r) for r in rows]))
    else:
        print(f"{'id':26s} {'status':10s} {'prov':>4s}  summary")
        for r in rows:
            summary = (r["summary"] or "").replace("\n", " ")
            if len(summary) > 88:
                summary = summary[:85] + "..."
            print(f"{r['id']:26s} {r['status']:10s} {r['prov']:>4d}  {summary}")
        total = conn.execute("SELECT COUNT(*) FROM proposal").fetchone()[0]
        print(f"\n{len(rows)} of {total} proposal(s)")
    conn.close()
    return 0


def _like_prefix(needle: str) -> str:
    """Escape LIKE wildcards so ids containing ``_`` resolve as literals."""
    escaped = needle.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")
    return escaped + "%"


def _resolve_proposal(conn, needle: str):
    exact = list(conn.execute("SELECT * FROM proposal WHERE id = ?", (needle,)))
    if exact:
        return exact[0], []
    matches = list(conn.execute(
        "SELECT * FROM proposal WHERE id LIKE ? ESCAPE '\\' ORDER BY id LIMIT 25",
        (_like_prefix(needle),),
    ))
    if len(matches) == 1:
        return matches[0], []
    return None, matches


def _resolve_concept(conn, needle: str):
    exact = list(conn.execute("SELECT * FROM concept WHERE id = ?", (needle,)))
    if exact:
        return exact[0], []
    matches = list(conn.execute(
        "SELECT * FROM concept WHERE id LIKE ? ESCAPE '\\' ORDER BY id LIMIT 25",
        (_like_prefix(needle),),
    ))
    if len(matches) == 1:
        return matches[0], []
    return None, matches


def cmd_show(args) -> int:
    db_path = ensure_db(args.db or DEFAULT_DB, args.sot)
    conn = connect(db_path)
    row, ambiguous = _resolve_proposal(conn, args.id)
    if row is None and ambiguous:
        print(f"ambiguous id prefix {args.id!r}; candidates:", file=sys.stderr)
        for m in ambiguous:
            print(f"  {m['id']}  {(m['summary'] or '')[:70]}", file=sys.stderr)
        conn.close()
        return 2
    if row is None:
        concept, c_ambiguous = _resolve_concept(conn, args.id)
        if concept is None and c_ambiguous:
            print(f"ambiguous id prefix {args.id!r}; candidates:", file=sys.stderr)
            for m in c_ambiguous:
                print(f"  {m['id']}  name={m['name']}", file=sys.stderr)
            conn.close()
            return 2
        if concept is None:
            print(f"no proposal or concept matches {args.id!r}", file=sys.stderr)
            conn.close()
            return 2
        links = list(conn.execute(
            "SELECT source_kind, source_id, confidence, note FROM provenance_link "
            "WHERE subject_kind='concept' AND subject_id=? ORDER BY id", (concept["id"],)
        ))
        payload = {"kind": "concept", "row": dict(concept),
                   "provenance": [dict(x) for x in links]}
        if args.json:
            print(pretty_json(payload))
        else:
            print(f"CONCEPT {concept['id']}  status={concept['status']}")
            print(f"name    : {concept['name']}")
            print(f"notes   : {concept['notes']}")
            print("provenance:")
            for x in links:
                print(f"  - {x['source_kind']}:{x['source_id']} [{x['confidence']}] {x['note']}")
        conn.close()
        return 0

    pid = row["id"]
    links = list(conn.execute(
        "SELECT id, source_kind, source_id, confidence, status, note FROM provenance_link "
        "WHERE subject_kind='proposal' AND subject_id=? ORDER BY id", (pid,)
    ))
    rels = list(conn.execute(
        "SELECT id, from_kind, from_id, rel_type, to_kind, to_id, confidence, status "
        "FROM relationship WHERE from_id=? OR to_id=? ORDER BY id", (pid, pid)
    ))
    payload = {
        "kind": "proposal",
        "row": dict(row),
        "based_on": json.loads(row["based_on_json"] or "[]"),
        "provenance": [dict(x) for x in links],
        "relationships": [dict(x) for x in rels],
    }
    if args.json:
        print(pretty_json(payload))
        conn.close()
        return 0

    print(f"PROPOSAL {pid}  status={row['status']}")
    print(f"attribution : {row['attribution']}")
    print(f"created_at  : {row['created_at']}   updated_at: {row['updated_at']}")
    print(f"summary     : {row['summary']}")
    print("based_on    : " + (", ".join(payload["based_on"]) or "(none)"))
    print("-" * 72)
    print(row["body"] or "(no body)")
    print("-" * 72)
    print(f"provenance_link ({len(links)}):")
    for x in links:
        print(f"  - {x['source_kind']}:{x['source_id']} [{x['confidence']}/{x['status']}] "
              f"{x['note']}")
    if rels:
        print(f"relationships ({len(rels)}):")
        for x in rels:
            print(f"  - {x['from_kind']}:{x['from_id']} --{x['rel_type']}--> "
                  f"{x['to_kind']}:{x['to_id']} [{x['confidence']}]")
    conn.close()
    return 0


def cmd_list_runs(args) -> int:
    db_path = ensure_db(args.db or DEFAULT_DB, args.sot)
    conn = connect(db_path)
    rows = list(conn.execute(
        "SELECT id, kind, status, started_at, finished_at, engine_version, summary_json "
        "FROM analysis_run ORDER BY kind, id"
    ))
    if args.json:
        print(pretty_json([dict(r) for r in rows]))
    else:
        print(f"{'kind':14s} {'status':8s} {'run_id':22s} summary")
        for r in rows:
            summary = (r["summary_json"] or "").replace("\n", " ")
            if len(summary) > 80:
                summary = summary[:77] + "..."
            print(f"{r['kind']:14s} {r['status']:8s} {r['id']:22s} {summary}")
        if not rows:
            print("(no analysis_run rows yet — run `engine.py run`)")
    conn.close()
    return 0


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="engine.py",
        description="Codex Solbian Stage 5 — deterministic engine (LLM off by default).",
    )
    p.add_argument("--db", default=None,
                   help=f"working SQLite store (default: {DEFAULT_DB}; created from the SoT)")
    p.add_argument("--sot", default=STAGE3_DB,
                   help=f"read-only source-of-truth store (default: {STAGE3_DB})")
    sub = p.add_subparsers(dest="cmd", required=True)

    run_p = sub.add_parser("run", help="run deterministic analyses and write PROPOSED rows")
    run_p.add_argument("--kind", action="append", default=None,
                       help=f"analysis kind(s): {', '.join(KINDS)} or a comma list or 'all'")
    run_p.add_argument("--llm", action="store_true",
                       help="enable the optional LLM hook (requires SOLBIAN_LLM_CMD)")
    run_p.add_argument("--dry-run", action="store_true",
                       help="compute everything, then roll back (no writes committed)")
    run_p.add_argument("--reset", action="store_true",
                       help="delete engine-created rows before running")
    run_p.add_argument("--refresh-db", action="store_true",
                       help="re-copy the SoT store into the working copy first")
    run_p.add_argument("--min-freq", type=int, default=5,
                       help="min title frequency for underdeveloped tokens (default 5)")
    run_p.add_argument("--max-findings", type=int, default=20,
                       help="cap per analyzer (default 20)")
    run_p.add_argument("--db", default=argparse.SUPPRESS, help=argparse.SUPPRESS)
    run_p.add_argument("--sot", default=argparse.SUPPRESS, help=argparse.SUPPRESS)
    run_p.set_defaults(func=cmd_run)

    lp = sub.add_parser("list-proposals", help="list proposal rows")
    lp.add_argument("--status", action="append", default=None,
                    help="filter by status (repeatable)")
    lp.add_argument("--limit", type=int, default=200)
    lp.add_argument("--json", action="store_true")
    lp.add_argument("--db", default=argparse.SUPPRESS, help=argparse.SUPPRESS)
    lp.add_argument("--sot", default=argparse.SUPPRESS, help=argparse.SUPPRESS)
    lp.set_defaults(func=cmd_list_proposals)

    sh = sub.add_parser("show", help="show one proposal (or concept) by id or prefix")
    sh.add_argument("id")
    sh.add_argument("--json", action="store_true")
    sh.add_argument("--db", default=argparse.SUPPRESS, help=argparse.SUPPRESS)
    sh.add_argument("--sot", default=argparse.SUPPRESS, help=argparse.SUPPRESS)
    sh.set_defaults(func=cmd_show)

    lr = sub.add_parser("list-runs", help="list analysis_run rows")
    lr.add_argument("--json", action="store_true")
    lr.add_argument("--db", default=argparse.SUPPRESS, help=argparse.SUPPRESS)
    lr.add_argument("--sot", default=argparse.SUPPRESS, help=argparse.SUPPRESS)
    lr.set_defaults(func=cmd_list_runs)
    return p


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        if not getattr(args, "db", None):
            args.db = DEFAULT_DB
        if not getattr(args, "sot", None):
            args.sot = STAGE3_DB
        return args.func(args)
    except EngineError as exc:
        print(f"engine error: {exc}", file=sys.stderr)
        return 2
    except sqlite3.Error as exc:
        print(f"database error: {exc}", file=sys.stderr)
        return 3


if __name__ == "__main__":
    raise SystemExit(main())
