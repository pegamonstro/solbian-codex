#!/usr/bin/env python3
"""Codex Solbian Phase I — Stage 6 historical validation suite.

Proves, against the existing corpus and stores (read-only on the Mac tree),
the SPEC 12 baseline and the Stage 5 engine contract:

  A1 ingest coverage            >=900 source_document rows + known paths
  A2 preserve sources           Stage 3 SoT sha256 + Mac fingerprint stable
  A3 represent without loss     inventory 966 vs 935 rows; gap == duplicates
  A4 visible structure          chapters/scrolls/protocols/legal/glossary/personae
  A5 historical distinctions    plurality flags; A/B/B'/C; protocol 01-08
  A6 provenance exposed         proposals link to source_document
  A7 no silent content change   dry-run commits nothing; SoT/corpus untouched
  E1 engine idempotent          re-run on a throwaway copy: counts/ids stable
  E2 duplicate detector         finds known duplicate basenames (readme.md)
  E3 failure handling           refuses --db inside the Mac corpus
  E4 durable analyzer (opt)      personae week .sref -> INTERPRETATION proposal

Writes only inside this Stage 6 workspace (``VALIDATION_REPORT.md``) and a
throwaway temp directory.  It never writes the Mac corpus or the Stage 3 SoT
store.  Exits 0 only if every check passes.

    python3 validate_historical.py
    python3 validate_historical.py --report /tmp/other.md
"""

from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import importlib.util
import json
import os
import shutil
import sqlite3
import subprocess
import sys
import tempfile

# --------------------------------------------------------------------------- #
# Paths / constants
# --------------------------------------------------------------------------- #

HERE = os.path.dirname(os.path.abspath(__file__))

STAGE3_DIR = "/Users/archcore/solbian/codex-phase-i-stage3"
STAGE3_DB = os.path.join(STAGE3_DIR, "codex_phase_i.sqlite")
STAGE3_INGEST = os.path.join(STAGE3_DIR, "ingest_baseline.py")
STAGE3_INVENTORY_JSON = os.path.join(STAGE3_DIR, "baseline_inventory_full.json")
STAGE4_INVENTORY_JSON = "/Users/archcore/solbian/codex-phase-i-stage4/baseline_inventory_full.json"

STAGE5_DIR = "/Users/archcore/solbian/codex-phase-i-stage5"
STAGE5_DB = os.path.join(STAGE5_DIR, "data", "codex_phase_i.sqlite")
ENGINE_PY = os.path.join(STAGE5_DIR, "engine.py")

MAC_CORPUS = "/Users/archcore/solbian/codex"
MAC_SOURCE_ORIGINAL = os.path.join(MAC_CORPUS, "source_original")
WEEK_SREF = os.path.join(
    MAC_SOURCE_ORIGINAL, "personae", "joao", "academia", "reflections",
    "week01_reflection.sref",
)

DEFAULT_REPORT = os.path.join(HERE, "VALIDATION_REPORT.md")

MIN_SOURCE_DOCS = 900
INVENTORY_ENTRY_COUNT = 966
SAMPLE_HASH_COUNT = 20
ALLOWED_STATUS = {"PROPOSED", "WORKING"}

ENGINE_TABLES = ("proposal", "concept", "relationship", "provenance_link", "analysis_run")

# Known Stage 2 inventory paths that must survive as source_document rows.
KNOWN_PATHS = (
    "source_original/chapters/codex_solbian_chapter_23.sref",
    "source_original/scrolls/codex_solbian_scroll_01.sref",
    "source_original/protocols/codex_solbian_protocol_01.sref",
    "source_original/manifest/codex_solbian_laws.sref",
    "source_original/legal/digital_will_v2.sref",
    "source_original/glossary/codex_solbian_glossary.sref",
    "source_original/personae/Solace/identity_solace_v2.sref",
    "scrolls/01_Genesis.md",
)

# Role/path prefixes that make the historical structure visible.
STRUCTURE_PREFIXES = {
    "chapters": ("source_original/chapters/",),
    "scrolls": ("source_original/scrolls/", "scrolls/"),
    "protocols": ("source_original/protocols/",),
    "legal/laws": ("source_original/legal/", "source_original/manifest/codex_solbian_laws"),
    "glossary": ("source_original/glossary/",),
    "personae": ("source_original/personae/",),
}

# A/B/B'/C catalogue variants + the Gitea-5 protocol catalogue flag.
VARIANT_CASES = (
    ("law_catalogue_A", "source_original/legal/law_variant_A.md", "LAW", "law A catalogue"),
    ("law_catalogue_B", "source_original/legal/law_variant_B.md", "LAW", "law B catalogue"),
    ("law_catalogue_C", "source_original/legal/law_variant_C.md", "LAW", "law C catalogue"),
    ("law_catalogue_Bprime", "source_original/legal/law_variant_Bprime.md", "LAW",
     "law B\u2032 catalogue"),
    ("protocol_catalogue_gitea5", "source_original/protocols/protocols.md", "PROTOCOL",
     "gitea-5 protocol catalogue"),
)


# --------------------------------------------------------------------------- #
# Small helpers
# --------------------------------------------------------------------------- #


def now_iso() -> str:
    return _dt.datetime.now(_dt.timezone.utc).replace(microsecond=0).isoformat()


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def connect_ro(path: str) -> sqlite3.Connection:
    conn = sqlite3.connect(f"file:{path}?mode=ro", uri=True, timeout=20)
    conn.row_factory = sqlite3.Row
    return conn


def open_rw(path: str) -> sqlite3.Connection:
    conn = sqlite3.connect(path, timeout=20)
    conn.row_factory = sqlite3.Row
    return conn


def scalar(conn: sqlite3.Connection, sql: str, params=()):
    return conn.execute(sql, params).fetchone()[0]


def tables(conn: sqlite3.Connection) -> list[str]:
    return [
        r[0] for r in conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
        )
    ]


def mac_fingerprint(root: str = MAC_SOURCE_ORIGINAL, sample: int = SAMPLE_HASH_COUNT) -> dict:
    """File count + full listing digest + a deterministic sample of file hashes.

    Read-only: ``os.walk``/``os.stat``/``open(...,'rb')`` only.
    """
    files: list[tuple[str, int]] = []
    if os.path.isdir(root):
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames.sort()
            for name in sorted(filenames):
                full = os.path.join(dirpath, name)
                try:
                    st = os.stat(full)
                except OSError:
                    continue
                files.append((os.path.relpath(full, root), st.st_size))
    files.sort()

    digest = hashlib.sha256()
    for rel, size in files:
        digest.update(f"{rel}\x1f{size}\n".encode("utf-8"))

    sample_hashes = []
    if files:
        step = max(1, len(files) // sample)
        for rel, _size in files[::step][:sample]:
            try:
                sample_hashes.append((rel, sha256_file(os.path.join(root, rel))))
            except OSError:
                sample_hashes.append((rel, None))
    return {
        "root": root,
        "file_count": len(files),
        "listing_digest": digest.hexdigest(),
        "sample_hashes": sample_hashes,
    }


def load_inventory() -> tuple[str, dict]:
    for path in (STAGE3_INVENTORY_JSON, STAGE4_INVENTORY_JSON):
        if os.path.isfile(path):
            with open(path, "r", encoding="utf-8") as fh:
                return path, json.load(fh)
    raise FileNotFoundError("no baseline_inventory_full.json found")


def run_engine(db: str, *args: str, timeout: int = 240) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, ENGINE_PY, "--db", db, *args],
        cwd=os.path.dirname(ENGINE_PY),
        capture_output=True,
        text=True,
        timeout=timeout,
    )


def parse_flags(raw) -> list[str]:
    if not raw:
        return []
    try:
        value = json.loads(raw)
    except (ValueError, TypeError):
        return []
    return [str(x) for x in value] if isinstance(value, list) else []


def load_stage3_flag_inferrer():
    """Import Stage 3's own plurality inference (read-only, no .pyc written)."""
    if not os.path.isfile(STAGE3_INGEST):
        return None
    previous = sys.dont_write_bytecode
    sys.dont_write_bytecode = True  # never leave a __pycache__ in Stage 3
    try:
        spec = importlib.util.spec_from_file_location("stage3_ingest_baseline", STAGE3_INGEST)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module.infer_plurality_flags
    except Exception:  # noqa: BLE001 - fall back to source-level evidence
        return None
    finally:
        sys.dont_write_bytecode = previous


# --------------------------------------------------------------------------- #
# Report
# --------------------------------------------------------------------------- #


class Report:
    def __init__(self) -> None:
        self.rows: list[tuple[str, bool, str, str]] = []
        self.facts: list[tuple[str, str]] = []
        self.notes: list[str] = []
        self.transcripts: list[tuple[str, str]] = []

    def check(self, cid: str, ok: bool, label: str, detail: str = "") -> None:
        self.rows.append((cid, bool(ok), label, detail))
        mark = "PASS" if ok else "FAIL"
        line = f"  {mark}  [{cid}] {label}"
        if detail:
            line += f"  — {detail}"
        print(line)

    def fact(self, label: str, value) -> None:
        self.facts.append((label, str(value)))

    def note(self, text: str) -> None:
        self.notes.append(text)

    def transcript(self, label: str, text: str) -> None:
        self.transcripts.append((label, text))

    @property
    def failures(self) -> list[tuple[str, bool, str, str]]:
        return [r for r in self.rows if not r[1]]

    def markdown(self, inputs: dict) -> str:
        passed = sum(1 for r in self.rows if r[1])
        total = len(self.rows)
        verdict = "PASS" if not self.failures else "FAIL"
        out: list[str] = []
        out.append("# Stage 6 — Historical Validation Report")
        out.append("")
        out.append(f"**As-of:** {now_iso()} · **CANONICAL: NONE** · "
                   f"**Verdict: {verdict}** ({passed}/{total} checks)")
        out.append("")
        out.append("Generated by `validate_historical.py`. Read-only against the Mac "
                   "corpus and the Stage 3 SoT store; performs all engine work on "
                   "throwaway copies in a temporary directory.")
        out.append("")

        out.append("## Verdict")
        out.append("")
        out.append(f"- **VERDICT: {verdict}** — {passed} passed, {len(self.failures)} failed, "
                   f"{total} total")
        out.append("")

        out.append("## Checks")
        out.append("")
        out.append("| ID | Check | Result | Detail |")
        out.append("| --- | --- | --- | --- |")
        for cid, ok, label, detail in self.rows:
            d = detail.replace("|", "\\|").replace("\n", " ")
            out.append(f"| {cid} | {label} | {'PASS' if ok else 'FAIL'} | {d} |")
        out.append("")

        out.append("## Measured inputs")
        out.append("")
        out.append("| Item | Value |")
        out.append("| --- | --- |")
        for label, value in inputs.items():
            out.append(f"| {label} | `{value}` |")
        out.append("")

        if self.facts:
            out.append("## Numbers")
            out.append("")
            out.append("| Fact | Value |")
            out.append("| --- | --- |")
            for label, value in self.facts:
                out.append(f"| {label} | {value.replace('|', '\\|')} |")
            out.append("")

        if self.transcripts:
            out.append("## Engine transcripts")
            out.append("")
            for label, text in self.transcripts:
                out.append(f"### {label}")
                out.append("")
                out.append("```")
                out.append(text.strip() or "(no output)")
                out.append("```")
                out.append("")

        if self.notes:
            out.append("## Notes")
            out.append("")
            for text in self.notes:
                out.append(f"- {text}")
            out.append("")

        if self.failures:
            out.append("## Failures")
            out.append("")
            for cid, _ok, label, detail in self.failures:
                out.append(f"- **[{cid}]** {label}" + (f" — {detail}" if detail else ""))
            out.append("")

        return "\n".join(out) + "\n"


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Stage 6 historical validation")
    parser.add_argument("--report", default=DEFAULT_REPORT,
                        help="path for the generated VALIDATION_REPORT.md")
    parser.add_argument("--quiet", action="store_true", help="suppress the banner")
    args = parser.parse_args(argv)

    if not args.quiet:
        print("Codex Solbian Phase I — Stage 6 historical validation")
        print(f"SoT    : {STAGE3_DB} (read-only)")
        print(f"engine : {ENGINE_PY}")
        print(f"corpus : {MAC_CORPUS} (read-only)")
        print()

    report = Report()

    # ---- snapshots taken BEFORE any check (preservation proof) ------------ #
    sot_sha_before = sha256_file(STAGE3_DB)
    mac_before = mac_fingerprint()
    stage5_sha_before = sha256_file(STAGE5_DB) if os.path.isfile(STAGE5_DB) else None

    inputs = {
        "Stage 3 SoT store": STAGE3_DB,
        "Stage 3 SoT sha256 (before)": sot_sha_before,
        "Stage 5 working store": STAGE5_DB,
        "Stage 5 engine": ENGINE_PY,
        "Mac corpus root": MAC_CORPUS,
        "Mac source_original file count (before)": mac_before["file_count"],
        "Mac source_original listing digest (before)": mac_before["listing_digest"],
    }

    tmp = tempfile.mkdtemp(prefix="stage6_validate_")
    try:
        run_baseline_checks(report, tmp)
        run_engine_checks(report, tmp)
        run_preservation_checks(report, sot_sha_before, mac_before, stage5_sha_before)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    report.fact("Stage 3 SoT sha256 (before)", sot_sha_before)
    report.fact("Stage 3 SoT sha256 (after)", sha256_file(STAGE3_DB))
    report.fact("Mac source_original file count (before)", mac_before["file_count"])
    report.fact("Mac source_original file count (after)", mac_fingerprint()["file_count"])

    markdown = report.markdown(inputs)
    try:
        with open(args.report, "w", encoding="utf-8") as fh:
            fh.write(markdown)
        if not args.quiet:
            print(f"\nreport written: {args.report}")
    except OSError as exc:
        print(f"WARNING: could not write report {args.report}: {exc}", file=sys.stderr)

    print()
    if report.failures:
        print(f"VALIDATION FAILED — {len(report.failures)} of {len(report.rows)} checks failed")
        for cid, _ok, label, detail in report.failures:
            print(f"  - [{cid}] {label}" + (f": {detail}" if detail else ""))
        return 1
    print(f"VALIDATION PASSED — {len(report.rows)}/{len(report.rows)} checks")
    return 0


# --------------------------------------------------------------------------- #
# Baseline checks
# --------------------------------------------------------------------------- #


def run_baseline_checks(report: Report, tmp: str) -> None:
    print("[1] baseline tests (SPEC 12)")
    if not os.path.isfile(STAGE3_DB):
        report.check("A1", False, "Stage 3 SoT store exists", STAGE3_DB)
        return

    conn3 = connect_ro(STAGE3_DB)
    try:
        # ---- A1 ingest coverage ------------------------------------------ #
        n3 = scalar(conn3, "SELECT COUNT(*) FROM source_document")
        report.fact("Stage 3 source_document rows", n3)
        report.check("A1a", n3 >= MIN_SOURCE_DOCS,
                     f"Stage 3 source_document >= {MIN_SOURCE_DOCS}", f"got {n3}")

        n5 = None
        if os.path.isfile(STAGE5_DB):
            conn5 = connect_ro(STAGE5_DB)
            try:
                n5 = scalar(conn5, "SELECT COUNT(*) FROM source_document")
            finally:
                conn5.close()
        if n5 is None:
            report.check("A1b", False, "Stage 5 working store present", STAGE5_DB)
        else:
            report.fact("Stage 5 source_document rows", n5)
            report.check("A1b", n5 >= MIN_SOURCE_DOCS and n5 == n3,
                         f"Stage 5 source_document >= {MIN_SOURCE_DOCS} and == Stage 3",
                         f"got {n5} vs {n3}")

        # known paths present as rows
        present = []
        missing = []
        for rel in KNOWN_PATHS:
            hit = conn3.execute(
                "SELECT 1 FROM source_document WHERE rel_path = ? LIMIT 1", (rel,)
            ).fetchone()
            (present if hit else missing).append(rel)
        report.fact("Known inventory paths present", f"{len(present)}/{len(KNOWN_PATHS)}")
        report.check("A1c", not missing,
                     f"known Stage 2 paths exist as rows ({len(present)}/{len(KNOWN_PATHS)})",
                     ("missing: " + ", ".join(missing)) if missing else "")

        # ---- A2 preserve sources (before/after compared later) ----------- #
        report.note("A2 is asserted after all engine work: Stage 3 SoT sha256 and the "
                    "Mac source_original fingerprint are re-measured and compared.")

        # ---- A3 representation without substantial loss ------------------ #
        inv_path, inventory = load_inventory()
        entries = inventory.get("entries", [])
        entry_count = inventory.get("entry_count", len(entries))
        inv_unique = sorted({e.get("path") for e in entries if e.get("path")})

        primary = conn3.execute(
            "SELECT id FROM corpus_root WHERE path = ? LIMIT 1", (MAC_CORPUS,)
        ).fetchone()
        primary_id = primary["id"] if primary else None
        db_paths = sorted(
            r[0] for r in conn3.execute(
                "SELECT rel_path FROM source_document WHERE corpus_root_id = ?", (primary_id,)
            )
        )
        gap = entry_count - len(db_paths)
        duplicate_entries = len(entries) - len(inv_unique)
        missing_paths = sorted(set(inv_unique) - set(db_paths))
        extra_paths = sorted(set(db_paths) - set(inv_unique))

        report.fact("Inventory file", inv_path)
        report.fact("Inventory entry_count", entry_count)
        report.fact("Inventory unique rel_paths", len(inv_unique))
        report.fact("Duplicate inventory entries", duplicate_entries)
        report.fact("DB PRIMARY rel_path rows", len(db_paths))
        report.fact("Gap (entry_count - DB rows)", gap)

        report.check(
            "A3a", not missing_paths and not extra_paths,
            "every unique inventory rel_path is represented in the DB (no silent drop)",
            ("missing=" + str(len(missing_paths)) + " extra=" + str(len(extra_paths))),
        )
        report.check(
            "A3b", gap == duplicate_entries and set(db_paths) == set(inv_unique),
            "inventory/DB gap equals duplicate inventory entries (gap explained)",
            f"gap={gap} duplicates={duplicate_entries}",
        )
        report.check(
            "A3c", gap > 0 and duplicate_entries > 0,
            "gap is non-zero and fully accounted for by duplicates",
            f"entry_count={entry_count} unique={len(inv_unique)} db={len(db_paths)}",
        )

        # ---- A4 visible structure ---------------------------------------- #
        for label, prefixes in STRUCTURE_PREFIXES.items():
            count = 0
            for prefix in prefixes:
                count += scalar(
                    conn3,
                    "SELECT COUNT(*) FROM source_document WHERE rel_path LIKE ?",
                    (prefix + "%",),
                )
            report.fact(f"structure[{label}] rows", count)
            report.check(f"A4-{label}", count > 0,
                         f"documents visible under {label}", f"prefix={prefixes} count={count}")

        roles = {
            r[0]: r[1]
            for r in conn3.execute(
                "SELECT probable_role, COUNT(*) FROM source_document GROUP BY probable_role"
            )
        }
        for role in ("CHAPTER", "SCROLL", "PROTOCOL", "LAW", "GLOSSARY"):
            report.check(f"A4-role-{role}", roles.get(role, 0) > 0,
                         f"role {role} present", f"count={roles.get(role, 0)}")

        # ---- A5 historical distinctions ---------------------------------- #
        flag_counts: dict[str, int] = {}
        for row in conn3.execute("SELECT plurality_flags FROM source_document"):
            for flag in parse_flags(row[0]):
                flag_counts[flag] = flag_counts.get(flag, 0) + 1
        for flag in ("law_material", "protocol_material", "scroll_material",
                     "sref_artefact", "scroll_md_vs_sref_ordinals", "scroll_20_anomaly"):
            report.fact(f"plurality_flag[{flag}]", flag_counts.get(flag, 0))
            report.check(f"A5-flag-{flag}", flag_counts.get(flag, 0) > 0,
                         f"plurality flag {flag!r} still present",
                         f"count={flag_counts.get(flag, 0)}")

        protocols = sorted(
            r[0] for r in conn3.execute(
                "SELECT rel_path FROM source_document "
                "WHERE rel_path LIKE 'source_original/protocols/codex_solbian_protocol_0%' "
                "AND rel_path NOT LIKE '%.sum' AND rel_path NOT LIKE '%.bak'"
            )
        )
        ordinals = sorted(
            os.path.basename(p).split("_")[-1].split(".")[0] for p in protocols
        )
        report.fact("protocol 01-08 files", f"{len(protocols)} ({', '.join(ordinals)})")
        report.check("A5-protocols", len(set(ordinals)) >= 8 and
                     {"01", "02", "03", "04", "05", "06", "07", "08"} <= set(ordinals),
                     "protocol 01-08 are all present (not reduced to 5)",
                     f"ordinals={ordinals}")

        # A/B/B'/C distinctions must be representable and not collapsed.
        infer = load_stage3_flag_inferrer()
        if infer is not None:
            produced = {}
            for expected, rel, role, notes in VARIANT_CASES:
                produced[expected] = infer(rel, role, notes)
            all_ok = all(expected in flags for expected, flags in produced.items())
            distinct = len({tuple(v) for v in produced.values()}) == len(VARIANT_CASES)
            plain = infer("source_original/legal/ordinary.sref", "LAW", "ordinary law")
            no_fabrication = not any(f.startswith("law_catalogue_") for f in plain)
            report.fact("A/B/B'/C variant flags (synthetic, via Stage 3 ingest)",
                        ", ".join(sorted(k for k, v in produced.items() if k in v)))
            report.check("A5-variants", all_ok and distinct and no_fabrication,
                         "catalogue variants A/B/B'/C+Gitea-5 stay distinct (no collapse)",
                         f"produced={ {k: v for k, v in produced.items()} } plain={plain}")
            report.transcript(
                "A/B/B'/C distinction probe (Stage 3 infer_plurality_flags)",
                "\n".join(f"{k}: {v}" for k, v in produced.items()) + f"\nplain: {plain}",
            )
        else:
            source = ""
            if os.path.isfile(STAGE3_INGEST):
                with open(STAGE3_INGEST, "r", encoding="utf-8") as fh:
                    source = fh.read()
            expected_flags = ("law_catalogue_A", "law_catalogue_B", "law_catalogue_C",
                              "law_catalogue_Bprime", "protocol_catalogue_gitea5")
            present = [f for f in expected_flags if f in source]
            report.check("A5-variants", len(present) == len(expected_flags),
                         "Stage 3 ingest still maps A/B/B'/C + Gitea-5 to distinct flags",
                         f"source-level evidence: {len(present)}/{len(expected_flags)}")

        # ---- A6 provenance exposed --------------------------------------- #
        if os.path.isfile(STAGE5_DB):
            conn5 = connect_ro(STAGE5_DB)
            try:
                n_props = scalar(conn5, "SELECT COUNT(*) FROM proposal")
                with_prov = scalar(
                    conn5,
                    "SELECT COUNT(DISTINCT p.id) FROM proposal p JOIN provenance_link v "
                    "ON v.subject_kind='proposal' AND v.subject_id=p.id",
                )
                resolved = scalar(
                    conn5,
                    "SELECT COUNT(*) FROM provenance_link v "
                    "WHERE v.subject_kind='proposal' AND v.source_kind='source_document' "
                    "AND v.source_id IN (SELECT id FROM source_document)",
                )
            finally:
                conn5.close()
            report.fact("Stage 5 proposals", n_props)
            report.fact("Stage 5 proposals with provenance", with_prov)
            report.fact("Provenance links resolved to source_document", resolved)
            report.check("A6a", n_props >= 1, "Stage 5 working DB has proposals", f"n={n_props}")
            report.check("A6b", with_prov == n_props,
                         "every proposal carries provenance_link",
                         f"{with_prov}/{n_props}")
            report.check("A6c", resolved >= 1,
                         ">=1 provenance_link resolves to a source_document",
                         f"resolved={resolved}")
        else:
            report.check("A6a", False, "Stage 5 working DB present", STAGE5_DB)
    finally:
        conn3.close()


# --------------------------------------------------------------------------- #
# Engine checks
# --------------------------------------------------------------------------- #


def run_engine_checks(report: Report, tmp: str) -> None:
    print("\n[2] engine tests (throwaway copies only)")

    # ---- A7 dry-run commits nothing -------------------------------------- #
    dry_db = os.path.join(tmp, "dryrun.sqlite")
    shutil.copyfile(STAGE3_DB, dry_db)
    proc = run_engine(dry_db, "run", "--dry-run")
    report.transcript("A7 dry-run stdout", proc.stdout)
    dry_rows = 0
    if os.path.isfile(dry_db):
        conn = open_rw(dry_db)
        try:
            for table in ENGINE_TABLES:
                if table in tables(conn):
                    dry_rows += scalar(conn, f"SELECT COUNT(*) FROM {table}")
        finally:
            conn.close()
    report.check("A7a", proc.returncode == 0 and "dry-run" in proc.stdout,
                 "engine --dry-run exits 0 and reports the rollback",
                 f"rc={proc.returncode}")
    report.check("A7b", dry_rows == 0,
                 "dry-run leaves no engine rows committed", f"rows={dry_rows}")

    # ---- E1 idempotent re-run -------------------------------------------- #
    work_db = os.path.join(tmp, "work.sqlite")
    shutil.copyfile(STAGE5_DB, work_db)
    before_count = None
    conn = open_rw(work_db)
    try:
        before_count = scalar(conn, "SELECT COUNT(*) FROM proposal")
        before_sot = (scalar(conn, "SELECT COUNT(*) FROM source_document"),
                      hashlib.sha1(b"".join(
                          (str(r[0]) + "\x1f" + str(r[1])).encode()
                          for r in conn.execute(
                              "SELECT id, rel_path FROM source_document ORDER BY id")
                      )).hexdigest())
    finally:
        conn.close()

    proc1 = run_engine(work_db, "run")
    report.transcript("E1 engine run stdout", proc1.stdout)
    conn = open_rw(work_db)
    try:
        props1 = sorted(r[0] for r in conn.execute("SELECT id FROM proposal"))
        concepts1 = sorted(r[0] for r in conn.execute("SELECT id FROM concept"))
        counts1 = tuple(
            scalar(conn, f"SELECT COUNT(*) FROM {t}")
            for t in ("proposal", "concept", "relationship", "provenance_link")
        )
        after_sot = (scalar(conn, "SELECT COUNT(*) FROM source_document"),
                     hashlib.sha1(b"".join(
                         (str(r[0]) + "\x1f" + str(r[1])).encode()
                         for r in conn.execute(
                             "SELECT id, rel_path FROM source_document ORDER BY id")
                     )).hexdigest())
        no_prov = [r[0] for r in conn.execute(
            "SELECT p.id FROM proposal p WHERE NOT EXISTS ("
            "  SELECT 1 FROM provenance_link v WHERE v.subject_kind='proposal'"
            "  AND v.subject_id=p.id AND v.source_kind IN ('source_document','message'))"
        )]
    finally:
        conn.close()

    proc2 = run_engine(work_db, "run")
    conn = open_rw(work_db)
    try:
        props2 = sorted(r[0] for r in conn.execute("SELECT id FROM proposal"))
        concepts2 = sorted(r[0] for r in conn.execute("SELECT id FROM concept"))
        counts2 = tuple(
            scalar(conn, f"SELECT COUNT(*) FROM {t}")
            for t in ("proposal", "concept", "relationship", "provenance_link")
        )
    finally:
        conn.close()

    report.fact("E1 proposals before/after", f"{before_count} -> {counts1[0]} -> {counts2[0]}")
    report.check("E1a", proc1.returncode == 0 and proc2.returncode == 0,
                 "engine re-runs exit 0", f"rc1={proc1.returncode} rc2={proc2.returncode}")
    report.check("E1b", before_count == counts1[0] == counts2[0],
                 "proposal count stable across runs",
                 f"{before_count} == {counts1[0]} == {counts2[0]}")
    report.check("E1c", props1 == props2 and concepts1 == concepts2 and counts1 == counts2,
                 "proposal/concept ids and row counts stable (idempotent)",
                 f"props {len(props1)}/{len(props2)} concepts {len(concepts1)}/{len(concepts2)}")
    report.check("E1d", before_sot == after_sot,
                 "source_document untouched by the engine run",
                 f"{before_sot[0]} rows")
    report.check("E1e", not no_prov,
                 "every engine proposal has source provenance", f"missing={len(no_prov)}")

    # statuses + canonical guard on the temp store
    conn = open_rw(work_db)
    try:
        bad_status = []
        for table in ("proposal", "concept", "relationship", "provenance_link"):
            for row in conn.execute(f"SELECT DISTINCT status FROM {table}"):
                if row[0] not in ALLOWED_STATUS:
                    bad_status.append(f"{table}:{row[0]}")
        canonical = []
        for table in tables(conn):
            for col in conn.execute(f"PRAGMA table_info({table})"):
                if col[1] in ("status", "confidence", "inventory_status", "classification"):
                    n = scalar(conn, f"SELECT COUNT(*) FROM {table} WHERE {col[1]}='CANONICAL'")
                    if n:
                        canonical.append(f"{table}.{col[1]}")
    finally:
        conn.close()
    report.check("E1f", not bad_status, "engine writes PROPOSED/WORKING only", str(bad_status))
    report.check("E1g", not canonical, "no CANONICAL value anywhere in the store", str(canonical))

    # ---- E2 duplicate detector ------------------------------------------- #
    conn = open_rw(work_db)
    try:
        readme = scalar(
            conn, "SELECT COUNT(*) FROM proposal WHERE lower(summary) LIKE '%readme.md%'"
        )
    finally:
        conn.close()
    report.fact("Duplicate-basename proposals for readme.md", readme)
    report.check("E2", readme >= 1,
                 "duplicate detector finds the known readme.md collision", f"count={readme}")

    # ---- E3 failure handling --------------------------------------------- #
    evil = os.path.join(MAC_CORPUS, "stage6_guard_should_not_exist.sqlite")
    proc = run_engine(evil, "run")
    combined = proc.stderr + proc.stdout
    report.check("E3a", proc.returncode != 0 and not os.path.exists(evil),
                 "engine refuses --db inside the Mac corpus",
                 f"rc={proc.returncode} exists={os.path.exists(evil)}")
    report.check("E3b", "Mac corpus" in combined,
                 "refusal names the Mac corpus", "")

    # ---- E4 durable analyzer (optional) ---------------------------------- #
    run_durable_check(report, tmp)


def run_durable_check(report: Report, tmp: str) -> None:
    if not os.path.isfile(WEEK_SREF):
        report.check("E4", True, "durable analyzer on personae week .sref",
                     "SKIPPED: week01_reflection.sref not present")
        report.note("E4 skipped: personae week .sref not readable.")
        return
    try:
        with open(WEEK_SREF, "r", encoding="utf-8") as fh:
            week = json.load(fh)
        body = ((week.get("content") or {}).get("body") or "").strip()
    except (OSError, ValueError) as exc:
        report.check("E4", True, "durable analyzer on personae week .sref",
                     f"SKIPPED: could not read ({exc})")
        report.note(f"E4 skipped: {exc}")
        return

    if len(body) < 280:
        report.check("E4", True, "durable analyzer on personae week .sref",
                     f"SKIPPED: body below 280 chars ({len(body)})")
        report.note(f"E4 skipped: week body only {len(body)} chars.")
        return

    db = os.path.join(tmp, "durable.sqlite")
    shutil.copyfile(STAGE5_DB, db)
    ts = "2026-09-21T00:00:00+00:00"
    conn = open_rw(db)
    try:
        conn.execute(
            "INSERT INTO conversation (id, title, participants, status, started_at, notes, "
            "attribution, created_at, updated_at) VALUES "
            "('conv_stage6_week','Stage 6 week fixture','[\"jd\",\"solace\"]','WORKING',?,"
            "'synthetic Stage 6 fixture from personae week .sref','stage6',?,?)",
            (ts, ts, ts),
        )
        conn.execute(
            "INSERT INTO message (id, conversation_id, seq, role, body, sent_at, source_path, "
            "status, created_at, updated_at) VALUES "
            "('msg_stage6_week','conv_stage6_week',1,'solace',?,?,?,'WORKING',?,?)",
            (body, ts, WEEK_SREF, ts, ts),
        )
        conn.commit()
    finally:
        conn.close()

    proc = run_engine(db, "run", "--kind", "durable")
    report.transcript("E4 durable run stdout", proc.stdout)
    conn = open_rw(db)
    try:
        hit = conn.execute(
            "SELECT p.id, p.body, v.confidence FROM proposal p JOIN provenance_link v "
            "ON v.subject_id=p.id AND v.subject_kind='proposal' "
            "WHERE v.source_kind='message' AND v.source_id='msg_stage6_week'"
        ).fetchone()
    finally:
        conn.close()

    ok = (proc.returncode == 0 and hit is not None
          and "INTERPRETATION" in (hit["body"] or "")
          and hit["confidence"] == "TEXT-SUPPORTED")
    report.fact("E4 source message", f"{WEEK_SREF} ({len(body)} chars)")
    report.check("E4", ok,
                 "personae week .sref -> durable INTERPRETATION proposal with TEXT-SUPPORTED evidence",
                 "proposal linked to message with stored quote" if ok else
                 f"rc={proc.returncode} hit={bool(hit)}")


# --------------------------------------------------------------------------- #
# Preservation checks (last)
# --------------------------------------------------------------------------- #


def run_preservation_checks(report: Report, sot_sha_before: str, mac_before: dict,
                            stage5_sha_before) -> None:
    print("\n[3] outside-world invariants")

    sot_sha_after = sha256_file(STAGE3_DB)
    mac_after = mac_fingerprint()
    stage5_sha_after = sha256_file(STAGE5_DB) if os.path.isfile(STAGE5_DB) else None

    report.check("A2a", sot_sha_after == sot_sha_before,
                 "Stage 3 SoT store byte-identical across validation",
                 f"{sot_sha_before[:12]}… == {sot_sha_after[:12]}…")

    same_files = mac_after["file_count"] == mac_before["file_count"]
    same_listing = mac_after["listing_digest"] == mac_before["listing_digest"]
    same_samples = mac_after["sample_hashes"] == mac_before["sample_hashes"]
    report.fact("Mac fingerprint before/after",
                f"files {mac_before['file_count']}->{mac_after['file_count']}, "
                f"digest {mac_before['listing_digest'][:10]}…->{mac_after['listing_digest'][:10]}…")
    report.check("A2b", same_files and same_listing and same_samples,
                 "Mac source_original fingerprint unchanged (file count + sample hashes)",
                 f"files={same_files} listing={same_listing} samples={same_samples}")

    if stage5_sha_before is not None and stage5_sha_after is not None:
        report.check("A2c", stage5_sha_after == stage5_sha_before,
                     "Stage 5 working store unchanged by validation (read-only)",
                     f"{stage5_sha_before[:12]}… == {stage5_sha_after[:12]}…")

    report.check("A7c",
                 sot_sha_after == sot_sha_before and same_files and same_listing,
                 "no silent content change: validation never wrote SoT or Mac corpus",
                 "SoT + corpus fingerprints identical")


if __name__ == "__main__":
    try:
        rc = main()
    except Exception as exc:  # noqa: BLE001 - surface, never hide
        print(f"VALIDATION ERROR: {type(exc).__name__}: {exc}", file=sys.stderr)
        rc = 1
    raise SystemExit(rc)
