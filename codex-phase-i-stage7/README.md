# Codex Solbian — Phase I · Stage 7 Living Loop

**As-of:** 2026-09-21 · **CANONICAL: NONE**

Stage 7 makes the whole Codex loop operable end to end in the Stage 4 UI (plus a
thin CLI), over **one living SQLite store**:

```
JD ↔ Solace (UI)
      ↓
preserved conversation (living SQLite: conversation / message)
      ↓
Codex Engine — durable + deterministic analyzers (analysis_run)
      ↓
PROPOSED proposals (+ provenance_link to message/source_document)
      ↓
controlled consolidation — explicit Accept → WORKING codex_document + revision
      ↓
Codex Solbian browse — WORKING codex_document alongside HISTORICAL source_document
```

Nothing in this stage can write `CANONICAL`. The value is absent from the schema
`CHECK` constraints and consolidation is capped at `WORKING`.

---

## 1. Living-store policy

**One living store:**

```
/Users/archcore/solbian/codex-phase-i-stage4/data/codex_phase_i.sqlite
```

(override with `SOLBIAN_LIVING_DB`, `--db`, or `app.py --db`).

| Concern | Decision |
|---|---|
| Living store | Stage 4 `data/codex_phase_i.sqlite` — the working copy of the Stage 3 SoT. It already holds `corpus_root` + `source_document` + `conversation`/`message`. |
| Stage 3 SoT | `/Users/archcore/solbian/codex-phase-i-stage3/codex_phase_i.sqlite` is **read-only**. It is only read, or copied once to create the living store. |
| Stage 5 engine store | `/Users/archcore/solbian/codex-phase-i-stage5/data/codex_phase_i.sqlite` is a **seed**. Its engine tables (`proposal`, `concept`, `relationship`, `provenance_link`, `analysis_run`) are copied into the living store **once** (`INSERT OR IGNORE`, skipped when the living store already has proposals). Stage 5 is then never written again. |
| Extra table | `analysis_run` (Stage 5 DDL) + `living_store_meta` (seed bookkeeping/policy) are created idempotently in the living store. |
| Writers | Solace append (`conversation`/`message`), the engine run (PROPOSED/WORKING rows), and explicit consolidation (`codex_document` WORKING, `revision`, `provenance_link`, `proposal.status`). |
| Read-only browse | `source_document`/`corpus_root` and the Codex browse surfaces; SQLite opened `mode=ro`. |
| Mac corpus | `/Users/archcore/solbian/codex` is never written (only a capped, read-only text preview ≤ 200 KB). |

Migration is idempotent and runs automatically on app startup
(`living_store.migrate`) and via `migrate_living_store.py` / `living_loop.py migrate`.

### Consolidation (the only path from proposal to content)

```
proposal (PROPOSED)
  └─ accept_proposal()
       ├─ codex_document  status = WORKING   (kind,title,body from the proposal)
       ├─ revision        target=codex_document, proposal_id=<proposal>, status=WORKING
       ├─ provenance_link subject=codex_document  (copied from the proposal)
       ├─ provenance_link subject=revision        (copied from the proposal)
       └─ proposal.status = WORKING  ("accepted-into-working")
```

It requires an explicit call (`POST /api/engine/proposals/<id>/accept` or
`living_loop.py accept <id>`). There is **no accept-all** and **no capacity to
write `CANONICAL`**. Re-accepting is idempotent (no duplicate document/revision).

---

## 2. Files

Under `/Users/archcore/solbian/codex-phase-i-stage7/`:

| File | Role |
|---|---|
| `living_store.py` | Core: living-store policy, one-time Stage 5 seed, guarded consolidation, WORKING-browse queries, engine runner. |
| `living_loop.py` | CLI: `once` (full loop on a throwaway copy), `run-engine`, `list-proposals`, `accept`, `list-codex`, `migrate`, `info`. |
| `migrate_living_store.py` | Thin CLI wrapper for the one-time migration. |
| `smoke_stage7.py` | Acceptance smoke: full loop on a throwaway DB + runs the staged Stage 4 extended smoke. |
| `_stage4_build/` | Staged Stage 4 changes: `app.py`, `smoke_ui.py`, `static/{index.html,app.js,style.css}`. |
| `apply_to_stage4.sh` | Installs `_stage4_build/` + `living_store.py` into the Stage 4 tree and migrates the living store. |

Stage 4 additions (installed by `apply_to_stage4.sh`):

* `POST /api/engine/run` — **Run living loop**: runs the Stage 5 engine against
  the living store, in place.
* `POST /api/engine/proposals/<id>/accept` — **Accept → WORKING**.
* `GET /api/codex/codex-documents` and `.../<id>` — WORKING `codex_document`
  browse (read-only).
* `GET /api/living/meta` — living-store policy/counts.
* Appending a Solace message auto-runs the `durable` analyzer.
* Codex tab: a clearly labelled **WORKING · codex_document** layer next to the
  **HISTORICAL · source_document** layer.
* Engine tab: **Run living loop** + **Accept → WORKING** (dry-run kept).

---

## 3. Run

### Stage 4 UI

```bash
cd /Users/archcore/solbian/codex-phase-i-stage4
python3 apply_to_stage4.sh          # from Stage 7 if Stage 4 is not yet installed
python3 app.py                      # -> http://127.0.0.1:8787
```

`app.py --db <living.sqlite> --engine-db <living.sqlite>` (the engine surface
defaults to the living store).

### Stage 7 CLI

```bash
cd /Users/archcore/solbian/codex-phase-i-stage7
python3 living_loop.py once                 # full loop on a throwaway copy (safe)
python3 living_loop.py once --in-place      # same, writing the living store
python3 living_loop.py run-engine           # engine against the living store
python3 living_loop.py list-proposals --status PROPOSED
python3 living_loop.py accept <id|prefix>
python3 living_loop.py list-codex
python3 migrate_living_store.py             # one-time seed
```

`once` defaults to a throwaway copy of the living store, so it is safe to run and
works under a read-only sandbox. `--in-place` (or an explicit `--db`) targets the
real living store.

### Verify

```bash
cd /Users/archcore/solbian/codex-phase-i-stage7 && python3 smoke_stage7.py   # 31/31
cd /Users/archcore/solbian/codex-phase-i-stage4 && python3 smoke_ui.py       # 149/149
```

`smoke_stage7.py` also installs the staged Stage 4 build into a private overlay
and runs the extended `smoke_ui.py` there (149 checks) — so the Stage 4 changes
are verified even when the sandbox cannot write the Stage 4 tree.

---

## 4. Safety invariants

* `source_document` is never inserted, updated or deleted (row + digest check by
  the engine; snapshot check in both smokes).
* No `CANONICAL` value exists anywhere: the status enums omit it, every write is
  constrained to `PROPOSED`/`WORKING`, and `living_store.scan_canonical` verifies
  it. (Prose may mention the word; a *status* never holds it.)
* Stage 3 SoT and the Stage 5 seed store stay byte-identical during every smoke.
* The Mac corpus fingerprint is unchanged; previews are read-only and capped.
* Engine rows are always attributable (`engine:stage5:*`); consolidations are
  attributable (`consolidation:accepted:<proposal_id>`).

## 5. Out of scope

Stage 8 Phase II, real LLM Solace, auto-accept-all, SEED/GOLEM.
