# DSH_RESULT — Stage 5 Codex Engine Prototype

**As-of:** 2026-09-21 · **Engine:** `stage5-1.0.0` · **CANONICAL:** NONE
**Workspace:** `/Users/archcore/solbian/codex-phase-i-stage5/`
**Verification:** `python3 smoke_engine.py` → **exit 0** (37/37 checks)

---

## 1. What was built

A deterministic, standard-library Codex engine over the preserved Stage 3 store.
It produces inspectable observations and `PROPOSED` records — nothing is
consolidated, nothing is elevated, source data is untouched.

| File | Purpose |
| --- | --- |
| `engine.py` | analyzers + CLI (`run`, `list-proposals`, `show`, plus `list-runs`) |
| `smoke_engine.py` | end-to-end verification on throwaway copies, exits `0` |
| `README.md` | operator documentation |
| `schema_engine.sql` | documentation of the single added table (`analysis_run`) |
| `data/codex_phase_i.sqlite` | working copy the engine writes to (935 `source_document` rows) |

The Stage 3 store (`/Users/archcore/solbian/codex-phase-i-stage3/codex_phase_i.sqlite`)
is the source of truth and is opened **read-only**. The first `run` copies it into
`data/` (the same local-working-copy pattern Stage 4 uses, and the only location
the current file sandbox permits writes). Stage 4 was **not modified**.

---

## 2. Acceptance criteria → evidence

| Brief / task requirement | Status | Evidence |
| --- | --- | --- |
| `engine.py` with `run`, `list-proposals`, `show <id>` | done | `engine.py --help`; smoke step [3] |
| Writes only PROPOSED/WORKING to proposal/concept/relationship/provenance_link (+ analysis_run) | done | writer functions `_require_status`; smoke asserts distinct statuses ⊆ {PROPOSED, WORKING} |
| Never mutate `source_document` | done | row-count + sha1 digest checked before/after every run inside `cmd_run`; smoke asserts count 935 and digest stable across two runs |
| Never invent CANONICAL | done | enum lacks it; `check_no_canonical()` scans all status/confidence columns; smoke scans engine text case-sensitively |
| Never write Mac corpus | done | `check_db_write_allowed()` refuses paths under `/Users/archcore/solbian/codex`; smoke asserts exit ≠ 0 and no file created; corpus fingerprint unchanged |
| Each proposal has provenance to a source_document and/or message | done | `write_provenance()` on every finding; smoke asserts 0 unlinked proposals/concepts |
| `smoke_engine.py` exit 0 | done | `SMOKE PASSED: 37/37 checks` |
| `README.md`, `DSH_RESULT.md` | done | this file + `README.md` |
| Analysis 1 — plurality reminders | done | 6 flag proposals + coverage gaps; `prop_plurality_*` |
| Analysis 2 — duplicate basename detection | done | 6 file groups + 1 directory aggregate; `prop_dupe_*`, `BASENAME_COLLISION` links |
| Analysis 3 — underdeveloped tokens | done | 20 `PROPOSED` `concept` candidates + proposals; `prop_under_*` / `concept_under_*` |
| Analysis 4 — long messages → durable candidates (INTERPRETATION) | done | implemented; Stage 3 has 0 messages → records `skipped`; smoke exercises it with a synthetic conversation and asserts a `TEXT-SUPPORTED` message link |
| Analysis 5 — discussion-topic proposals for gaps | done | 11 topics from underdeveloped tokens, plurality anomalies and duplicate clusters; `prop_disc_*` |
| LLM optional behind `--llm`, default OFF | done | `--llm` without `SOLBIAN_LLM_CMD` prints a notice and exits 0; no network code path exists otherwise |
| Re-run idempotent / clear analysis_run ids | done | content-derived proposal/concept ids and `arun_<sha1(kind, version)>`; smoke asserts identical ids and counts across re-runs |
| Distinguish SOURCE vs INTERPRETATION vs PROPOSAL | done | SOURCE = untouched rows; INTERPRETATION = literal tag in `notes`/`body`; PROPOSAL = `status='PROPOSED'`; `run` prints the legend |

---

## 3. Run snapshot (working copy)

```
python3 engine.py run
[...]
source_document before: 935
[plurality     ] status=OK  proposal=6,  provenance_link=52
[duplicates    ] status=OK  proposal=7,  provenance_link=22, relationship=13
[underdeveloped] status=OK  proposal=20, provenance_link=314, relationship=120
[durable       ] status=OK  no writes            (skip: 0 messages)
[discussion    ] status=OK  proposal=11, provenance_link=52
source_document after : 935 (unchanged)
store totals: proposal=44, concept=20, relationship=133, provenance_link=440
```

Stored artifacts:

| Table | Count |
| --- | --- |
| `proposal` (all `PROPOSED`) | 44 |
| `concept` (all `PROPOSED`, INTERPRETATION notes) | 20 |
| `relationship` (all `PROPOSED`) | 133 |
| `provenance_link` (`PROPOSED`/`WORKING`) | 440 |
| `analysis_run` (`OK`) | 5 |
| `source_document` (unchanged) | 935 |

Examples the engine produced:

* `Preserve plurality: flag 'scroll_material' on 761 row(s) — do not merge`
* `Preserve plurality: flag 'scroll_20_anomaly' on 2 row(s) — do not merge`
* `Duplicate basename 'readme.md' in 8 location(s) — review before any merge`
* `Directory-only basename collisions: 46 name(s) — preserve mirrors`
* `UNDERDEVELOPED: 'topology' in 11 titles with no definition (min_freq=5)`
* concept candidates: `prompts, profile, metrics, goals, capabilities, events, minsoo, audit, extended, topology, continuity, usage, identity, runtime, s12025, upgrade, voice, crypto, human, methods`
* `Discussion topic: define or drop underdeveloped token 'minsoo'`

---

## 4. Read-only guarantees (measured)

* Stage 3 store `sha256` before and after the full smoke:
  `8c6e15a6c98ceed92559b0642241d83bddc336f4a1187a652e55b465bfb56dac` — unchanged.
* Mac corpus (`/Users/archcore/solbian/codex`) mtime/size fingerprint before and
  after — unchanged; the engine never opens a corpus file (it works purely from
  the SQLite index).
* `source_document` count `935` and sha1 digest identical across runs; `cmd_run`
  rolls back and raises if either changes.
* `--db` inside the Mac corpus is refused with exit code 2 and a named reason.

---

## 5. Idempotency / re-run behaviour

* Proposal / concept / relationship / provenance ids are content-derived
  (`det_id`), so re-running updates rows in place: ids and counts are identical
  across runs (asserted).
* Re-runs refresh engine-owned text but preserve human decisions — a changed
  `proposal.status` and a filled `concept.definition` are never overwritten.
* `analysis_run` ids are deterministic per `(kind, engine_version)`; a re-run
  updates the same row.
* `--reset` removes only rows bearing the `engine:stage5:*` marker (and links
  whose subject/endpoint is such a row), then re-runs.
* `--dry-run` runs the full pass in one transaction, prints the summary, and
  rolls back — verified to leave 0 engine rows.

---

## 6. Optional LLM

`--llm` is a no-op unless `SOLBIAN_LLM_CMD` names an external command. Its output
becomes a `PROPOSED` proposal labelled `INTERPRETATION (LLM-generated …)` with
provenance to the context documents, and is never consolidated. With no backend
the flag prints `deterministic results only (no network calls)` and exits 0.

---

## 7. Commands exercised

```bash
python3 engine.py run                       # exit 0, writes PROPOSED rows
python3 engine.py run --dry-run             # exit 0, commits nothing
python3 engine.py run --reset               # exit 0, engine rows recreated
python3 engine.py run --kind durable --llm  # exit 0, LLM notice, no backend
python3 engine.py list-proposals --json     # exit 0, JSON list
python3 engine.py show <id|prefix>          # exit 0; unknown id exits 2
python3 engine.py list-runs                  # exit 0
python3 engine.py --db /Users/archcore/solbian/codex/x.sqlite run   # exit 2 (refused)
python3 smoke_engine.py                     # exit 0, 37/37 checks
```

---

## 8. Notes & limitations (honest)

* **Single corpus root carries rows.** All 935 `source_document` rows belong to
  `croot_719e65317ad787b7`; the five CANDIDATE roots have no documents. Basename
  duplication is therefore reported across *paths* (which subsumes cross-root
  duplication when other roots have rows), and the body records root ids.
* **No conversations in Stage 3** (`conversation`/`message` = 0). The `durable`
  analyzer detects this and records a `skipped` summary rather than fabricating
  proposals; its code path is covered by a synthetic fixture in the smoke test.
* **No body reads.** The engine does not read corpus file contents (the brief
  makes ≤200 KB previews optional). All reasoning is title/role/path/flag level,
  so most confidence values are `TITLE-LEVEL`; `TEXT-SUPPORTED` appears only for
  stored message quotes.
* **Stage 4 untouched.** Wiring a thin admin surface is documented in
  `README.md` as optional and was intentionally not performed, to avoid breaking
  Stage 4's smoke tests.
* The engine writes its working copy under `data/`. On a host where the Stage 3
  path is writable, `--db` can point directly at it; the engine adds only
  `analysis_run` and the PROPOSED rows.

---

## 9. Deliverable checklist

- [x] `engine.py` (`run`, `list-proposals`, `show`, `list-runs`)
- [x] `smoke_engine.py` → exit 0
- [x] `README.md`
- [x] `DSH_RESULT.md` (this file)
- [x] `schema_engine.sql`
- [x] `data/codex_phase_i.sqlite` (working copy; 44 proposals, 20 concepts, 133 relationships, 440 provenance links)
