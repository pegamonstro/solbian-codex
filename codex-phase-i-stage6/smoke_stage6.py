#!/usr/bin/env python3
"""Stage 6 smoke test — runs the historical validation suite and re-asserts the
outside-world invariants independently.

Exits 0 only if:

  1. ``validate_historical.py`` exits 0.
  2. ``VALIDATION_REPORT.md`` is written and reports VERDICT: PASS with every
     expected check id present and no FAIL rows.
  3. The Stage 3 SoT store sha256, the Stage 5 working store sha256 and the Mac
     ``source_original`` fingerprint are exactly what they were before the run
     (validation never wrote the SoT or the Mac corpus).

    python3 smoke_stage6.py
"""

from __future__ import annotations

import hashlib
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
VALIDATE = os.path.join(HERE, "validate_historical.py")
REPORT = os.path.join(HERE, "VALIDATION_REPORT.md")

STAGE3_DB = "/Users/archcore/solbian/codex-phase-i-stage3/codex_phase_i.sqlite"
STAGE5_DB = "/Users/archcore/solbian/codex-phase-i-stage5/data/codex_phase_i.sqlite"
MAC_SOURCE_ORIGINAL = "/Users/archcore/solbian/codex/source_original"

SAMPLE_HASH_COUNT = 20

EXPECTED_IDS = (
    "A1a", "A1b", "A1c",
    "A2a", "A2b", "A3a", "A3b", "A3c",
    "A4-chapters", "A4-scrolls", "A4-protocols", "A4-legal/laws", "A4-glossary",
    "A4-personae",
    "A5-flag-law_material", "A5-flag-protocol_material", "A5-flag-scroll_material",
    "A5-flag-scroll_20_anomaly", "A5-protocols", "A5-variants",
    "A6a", "A6b", "A6c",
    "A7a", "A7b", "A7c",
    "E1a", "E1b", "E1c", "E1d", "E1e", "E1f", "E1g",
    "E2", "E3a", "E3b", "E4",
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


def mac_fingerprint(root: str = MAC_SOURCE_ORIGINAL) -> dict:
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
    sample = []
    if files:
        step = max(1, len(files) // SAMPLE_HASH_COUNT)
        for rel, _size in files[::step][:SAMPLE_HASH_COUNT]:
            try:
                sample.append((rel, sha256_file(os.path.join(root, rel))))
            except OSError:
                sample.append((rel, None))
    return {"file_count": len(files), "digest": digest.hexdigest(), "sample": sample}


def main() -> int:
    print("Stage 6 smoke — historical validation wrapper")
    print(f"suite  : {VALIDATE}")
    print(f"report : {REPORT}")
    print()

    sot_before = sha256_file(STAGE3_DB)
    s5_before = sha256_file(STAGE5_DB)
    mac_before = mac_fingerprint()

    report_before_mtime = os.path.getmtime(REPORT) if os.path.isfile(REPORT) else None

    proc = subprocess.run(
        [sys.executable, VALIDATE, "--report", REPORT],
        cwd=HERE, capture_output=True, text=True, timeout=1200,
    )
    print(proc.stdout.rstrip())
    if proc.stderr.strip():
        print("--- stderr ---")
        print(proc.stderr.rstrip(), file=sys.stderr)
    print()

    check("validate_historical.py exits 0", proc.returncode == 0,
          f"rc={proc.returncode}")
    check("validation stdout reports PASS",
          "VALIDATION PASSED" in proc.stdout and "VALIDATION FAILED" not in proc.stdout,
          "stdout missing VALIDATION PASSED")

    exists = os.path.isfile(REPORT)
    check("VALIDATION_REPORT.md exists", exists, REPORT)
    if exists:
        check("report was (re)written this run",
              report_before_mtime is None or os.path.getmtime(REPORT) >= report_before_mtime)
        with open(REPORT, "r", encoding="utf-8") as fh:
            text = fh.read()
        check("report states VERDICT: PASS", "VERDICT: PASS" in text)
        fail_rows = text.count("| FAIL |")
        check("report has no FAIL rows", fail_rows == 0, f"fail_rows={fail_rows}")
        missing = [cid for cid in EXPECTED_IDS if f"| {cid} |" not in text]
        check("report contains every expected check id", not missing,
              "missing: " + ", ".join(missing) if missing else "")
        check("report states CANONICAL: NONE", "CANONICAL: NONE" in text)

    sot_after = sha256_file(STAGE3_DB)
    s5_after = sha256_file(STAGE5_DB)
    mac_after = mac_fingerprint()
    check("Stage 3 SoT store unchanged (sha256)",
          sot_after == sot_before, f"{sot_before[:12]}… vs {sot_after[:12]}…")
    check("Stage 5 working store unchanged (sha256)",
          s5_after == s5_before, f"{s5_before[:12]}… vs {s5_after[:12]}…")
    check("Mac source_original unchanged (count + digest + sample hashes)",
          mac_after == mac_before,
          f"before={mac_before['file_count']} after={mac_after['file_count']}")

    print()
    passed = sum(1 for _n, ok, _d in RESULTS if ok)
    failed = [(n, d) for n, ok, d in RESULTS if not ok]
    if failed:
        print(f"SMOKE STAGE 6 FAILED — {passed}/{len(RESULTS)} checks passed")
        for name, detail in failed:
            print(f"  - {name}" + (f": {detail}" if detail else ""))
        return 1
    print(f"SMOKE STAGE 6 PASSED — {passed}/{len(RESULTS)} checks")
    return 0


if __name__ == "__main__":
    sys.exit(main())
