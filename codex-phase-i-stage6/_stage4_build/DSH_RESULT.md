# DSH_RESULT — Stage 4 Engine/Proposals tab (addendum)

**STATUS: COMPLETE (verified in a staging copy; install script provided)**
**As-of:** 2026-09-21 · **CANONICAL: NONE**
**CWD (target):** `/Users/archcore/solbian/codex-phase-i-stage4/`

---

## What changed

Stage 4 gained a third, strictly **read-only** surface: **Engine** (proposals).

| File | Change |
| --- | --- |
| `app.py` | Added `--engine-db` / `--engine-py` (env `SOLBIAN_ENGINE_DB`, `SOLBIAN_ENGINE_PY`); read-only engine queries; `/api/engine/*` GET endpoints; `POST /api/engine/dry-run`; 405 guards for all other non-GET engine calls; engine info in `/healthz` and `/api/meta`. |
| `static/index.html` | Added the **Engine** tab button + panel (filter bar, proposal list, detail pane, dry-run output). |
| `static/app.js` | Added lazy Engine loading, proposal list/detail rendering (body + provenance + relationships), paging/filtering, and the dry-run button. |
| `smoke_ui.py` | Boots the app against throwaway copies of the Stage 4 **and** Stage 5 stores and adds 35 Engine checks (96 total). |
| `README.md` | Documents the third surface, its API and its guarantees. |
| `DSH_RESULT.md` | This file. |

### Engine behaviour

* List/filter proposals from the Stage 5 working store
  (`/Users/archcore/solbian/codex-phase-i-stage5/data/codex_phase_i.sqlite`,
  configurable) — the store is opened with SQLite `mode=ro`.
* Detail shows the proposal body, `based_on`, every `provenance_link`
  (resolved to its `source_document.rel_path` where applicable) and any
  `relationship` rows.
* `analysis_run` bookkeeping is exposed read-only at `/api/engine/runs`.
* **Run engine (dry-run)** copies the engine store to a temp dir, shells to
  `engine.py --db <tmp> run --dry-run`, returns the stdout, deletes the copy and
  re-hashes the real store to prove it is byte-identical.
* No CANONICAL value or control anywhere; every non-GET `/api/engine/*` call
  except the dry-run returns 405. The Solace and Codex surfaces are unchanged.

### New endpoints

| Method | Path | Purpose |
| --- | --- | --- |
| `GET` | `/api/engine/meta` | store path/existence, table counts, statuses, `canonical: NONE` |
| `GET` | `/api/engine/facets` | proposal status counts |
| `GET` | `/api/engine/proposals` | list/filter `q`, `status`, `limit`, `offset` |
| `GET` | `/api/engine/proposals/<id>` | row + based_on + provenance + relationships |
| `GET` | `/api/engine/runs` | `analysis_run` rows |
| `POST` | `/api/engine/dry-run` | Stage 5 `run --dry-run` on a temp copy |

---

## Verification

The modified files were assembled and exercised in a **staging copy**
(`/Users/archcore/solbian/codex-phase-i-stage6/_stage4_verify/`) built from the
shipped Stage 4 tree plus these files, against real Stage 4/Stage 5 stores.

```
SMOKE UI PASSED — 96/96 checks   (exit 0)
```

The 96 checks include all 61 original Solace/Codex checks (still green) plus 35
Engine checks, notably:

```
PASS  page has all three tabs
PASS  GET /api/engine/meta -> 200
PASS  engine meta reports CANONICAL NONE
PASS  engine meta is flagged read-only
PASS  engine proposal statuses are PROPOSED/WORKING only
PASS  GET /api/engine/proposals -> 200
PASS  engine proposal list is flagged read-only
PASS  GET engine proposal detail -> 200
PASS  engine proposal detail exposes provenance
PASS  engine provenance resolves to a source_document path
PASS  POST /api/engine/proposals rejected (405)
PASS  PUT/PATCH/DELETE /api/engine/... rejected (405)
PASS  POST /api/engine/dry-run -> 200
PASS  dry-run reports CANONICAL NONE
PASS  dry-run leaves the engine store byte-identical
PASS  dry-run exit 0 and shows the rollback
PASS  source_document rows were not mutated by any request
PASS  engine store proposal rows were not mutated by any request
```

The unmodified shipped Stage 4 smoke remains green (`61/61`, exit 0), so no
Solace/Codex behaviour regressed.

### Why a staging copy

The Stage 6 session's file sandbox permits writes only inside
`/Users/archcore/solbian/codex-phase-i-stage6`. Writing to the Stage 4 workspace
is denied (`Operation not permitted`), and escalation to `danger-full-access`
reported *"requires approval, but no approval channel is available"*. The
Engine-tab files therefore live in
`/Users/archcore/solbian/codex-phase-i-stage6/_stage4_build/` and are installed
by running:

```bash
bash /Users/archcore/solbian/codex-phase-i-stage6/_stage4_build/apply_to_stage4.sh
```

The script backs up the current files, copies the six Engine-tab files in, and
runs `python3 smoke_ui.py` (expected: `SMOKE UI PASSED — 96/96`, exit 0). The
originals are also preserved in `_stage4_build/_orig/`.

---

## Forbidden-item compliance

| Forbidden | Status |
| --- | --- |
| Modify historical corpus | **No** — no new corpus access at all; previews unchanged |
| CANONICAL controls / values | **Absent** — no endpoint, no UI control, `canonical: NONE` everywhere |
| Write the Stage 5 store | **No** — `mode=ro` reads; dry-run uses a temp copy (asserted byte-identical) |
| Break Solace/Codex | **No** — all 61 original smoke checks still pass |
| Heavy frameworks | **Absent** — stdlib + vanilla JS only |
