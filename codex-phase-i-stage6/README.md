# Codex Solbian Phase I — Stage 6 Historical Validation

**As-of:** 2026-09-21 · **CANONICAL: NONE**
**Authority:** SPEC 12 + Stage 2 inventory + Stage 3 SoT store + Stage 5 engine.

A self-contained validation suite that proves, against the **existing** corpus and
stores, that the Phase I data layer preserves the historical record and that the
Stage 5 engine behaves as specified. Python standard library only.

```
SoT (read-only)      /Users/archcore/solbian/codex-phase-i-stage3/codex_phase_i.sqlite
engine store (ro)    /Users/archcore/solbian/codex-phase-i-stage5/data/codex_phase_i.sqlite
engine CLI           /Users/archcore/solbian/codex-phase-i-stage5/engine.py
Mac corpus (ro)      /Users/archcore/solbian/codex
```

The suite **never writes** the Mac corpus or the Stage 3 SoT. Its only writes are
`VALIDATION_REPORT.md` inside this Stage 6 workspace and throwaway temp files
(deleted on exit).

---

## Run it

```bash
cd /Users/archcore/solbian/codex-phase-i-stage6
python3 validate_historical.py     # full suite, writes VALIDATION_REPORT.md, exit 0 on PASS
python3 smoke_stage6.py            # wrapper: runs the suite + re-asserts invariants, exit 0
```

Optional:

```bash
python3 validate_historical.py --report /tmp/report.md
python3 validate_historical.py --quiet
```

`smoke_stage6.py` exits 0 only if `validate_historical.py` exits 0, the report
states `VERDICT: PASS` with every expected check id and no `FAIL` rows, and the
Stage 3 SoT sha256, the Stage 5 store sha256 and the Mac `source_original`
fingerprint are unchanged by the run.

---

## Checks

### Baseline (SPEC 12)

| ID | Check |
| --- | --- |
| A1 | Stage 3/5 `source_document` ≥ 900; 8 known Stage 2 paths exist as rows |
| A2 | Stage 3 SoT sha256 stable; Mac `source_original` fingerprint (file count + listing digest + 20 sampled hashes) unchanged; Stage 5 store unchanged |
| A3 | inventory `entry_count` 966 vs 935 unique `rel_path`s vs 935 DB rows; gap == duplicate entries; no unique `rel_path` silently dropped |
| A4 | documents visible under chapters / scrolls / protocols / legal+laws / glossary / personae; roles CHAPTER, SCROLL, PROTOCOL, LAW, GLOSSARY present |
| A5 | plurality flags present (`law_material`, `protocol_material`, `scroll_material`, `sref_artefact`, `scroll_md_vs_sref_ordinals`, `scroll_20_anomaly`); A/B/B′/C catalogue variants stay distinct (functional probe of Stage 3's own `infer_plurality_flags`); protocol 01–08 all present |
| A6 | Stage 5 proposals all carry `provenance_link`; ≥1 link resolves to a `source_document` |
| A7 | engine `--dry-run` exits 0 and commits **no** engine rows; SoT/corpus never written |

### Engine

| ID | Check |
| --- | --- |
| E1 | re-run on a throwaway copy of the Stage 5 store: proposal/concept ids and row counts stable (idempotent); `source_document` untouched; only `PROPOSED`/`WORKING`; no CANONICAL |
| E2 | duplicate detector finds the known `readme.md` basename collision |
| E3 | engine refuses `--db` inside the Mac corpus (exit ≠ 0, no file created) |
| E4 | (optional) personae `week01_reflection.sref` → durable analyzer produces an `INTERPRETATION` proposal with `TEXT-SUPPORTED` evidence (skips with a reason if unreadable) |

Current result: **45/45 checks PASS** (see `VALIDATION_REPORT.md`).

---

## Files

| File | Purpose |
| --- | --- |
| `validate_historical.py` | the suite; prints PASS/FAIL, writes `VALIDATION_REPORT.md`, exit 0 on PASS |
| `smoke_stage6.py` | wrapper + independent outside-world invariant checks, exit 0 |
| `VALIDATION_REPORT.md` | generated human report (check table, numbers, engine transcripts) |
| `README.md` | this file |
| `DSH_RESULT.md` | run result, measurements, deviations |
| `_stage4_build/` | staged Stage 4 **Engine tab** bundle + `apply_to_stage4.sh` (see below) |

---

## Stage 4 Engine tab (staged)

The optional Stage 4 admin surface was implemented but could not be installed in
this session: the file sandbox permits writes only inside the Stage 6 workspace,
and the escalation request reported *"no approval channel is available"*.

The complete, verified implementation is staged in `_stage4_build/`:

| File | Purpose |
| --- | --- |
| `_stage4_build/app.py` | Stage 4 server with read-only `/api/engine/*` + safe dry-run |
| `_stage4_build/smoke_ui.py` | Stage 4 smoke extended with 35 Engine checks (96 total) |
| `_stage4_build/static/index.html`, `static/app.js` | the Engine tab UI |
| `_stage4_build/README.md`, `DSH_RESULT.md` | updated Stage 4 docs |
| `_stage4_build/apply_to_stage4.sh` | backs up + installs the files, then runs the smoke |
| `_stage4_build/stage4_smoke_engine_output.txt` | captured `96/96` smoke output |
| `_stage4_build/_orig/` | pristine copies of the original Stage 4 files |

Install with:

```bash
bash /Users/archcore/solbian/codex-phase-i-stage6/_stage4_build/apply_to_stage4.sh
```

It expected-outputs `SMOKE UI PASSED — 96/96 checks` and leaves the Solace/Codex
surfaces intact (the original 61 checks remain green).

---

## Guarantees

* **Read-only on history.** No code path writes `/Users/archcore/solbian/codex`.
* **Stage 3 SoT read-only.** Opened with SQLite `mode=ro`; sha256 asserted stable.
* **No CANONICAL.** No status/confidence column may hold `CANONICAL`; the engine
  guard is re-asserted in the validation.
* **Plurality preserved.** Law/protocol/scroll plurality flags and the protocol
  01–08 ordinals are verified present, and the A/B/B′/C catalogue distinctions
  are proven not to collapse.
* **Engine proposes, never decides.** All engine rows are `PROPOSED`/`WORKING`
  and carry provenance; re-runs are idempotent.
