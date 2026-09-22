# DSH_RESULT — Stage 7 Living Loop

**STATUS: COMPLETE**

**Stage:** Codex Solbian Phase I — Stage 7 (Living Loop)
**cwd:** `/Users/archcore/solbian/codex-phase-i-stage7/`
**As-of:** 2026-09-21 · **CANONICAL: NONE**

---

## What was built

1. **Living-store policy (documented + implemented)** — one living SQLite store
   at Stage 4 `data/codex_phase_i.sqlite`. The Stage 5 engine store is a *seed*:
   `analysis_run` + the PROPOSED engine rows are copied in once (`INSERT OR
   IGNORE`, skipped when the living store already has proposals). Stage 3 SoT is
   read-only; the Mac corpus is never written.
2. **Living loop in Stage 4** — appending a Solace message auto-runs the
   `durable` analyzer; an Engine button **Run living loop** runs the full
   deterministic engine against the living store; proposals refresh.
3. **Controlled consolidation** — explicit **Accept → WORKING** creates a
   `codex_document` (`status=WORKING`), a `revision` (`proposal_id` set) and
   copies the proposal's `provenance_link` rows onto the document and revision.
   The proposal is marked `WORKING` ("accepted-into-working"). Never `CANONICAL`;
   never auto-accept-all; re-accept is idempotent.
4. **Codex tab** — a clearly labelled **WORKING · codex_document** layer beside
   the **HISTORICAL · source_document** layer (segmented switch, counts, badges).
5. **CLI** — `living_loop.py once` (full loop on a throwaway copy), plus
   `run-engine` / `accept` / `list-proposals` / `list-codex` / `migrate` / `info`.
6. **Acceptance smokes** — `smoke_stage7.py` (full loop + staged Stage 4 smoke)
   and the extended Stage 4 `smoke_ui.py`.

## Deliverables

| Deliverable | Location |
|---|---|
| Living-store core | `living_store.py` |
| Loop CLI | `living_loop.py` |
| Migration CLI | `migrate_living_store.py` |
| Stage 7 smoke | `smoke_stage7.py` |
| Stage 4 changes (staged) | `_stage4_build/{app.py,smoke_ui.py,static/*}` |
| Stage 4 installer | `apply_to_stage4.sh` |
| Docs | `README.md`, `DSH_RESULT.md` |

## Verification

```
$ cd /Users/archcore/solbian/codex-phase-i-stage7 && python3 smoke_stage7.py
SMOKE STAGE7 PASSED — 31/31 checks
  [1-4] one-time seed; message -> durable proposal -> accept -> WORKING doc
  [5]   living_loop.py once exits 0
  [6]   staged Stage 4 overlay smoke: SMOKE UI PASSED — 149/149 checks
  [7]   Stage 3 SoT / Stage 5 seed byte-identical; Mac corpus unchanged

$ cd /Users/archcore/solbian/codex-phase-i-stage7 && python3 living_loop.py once
living loop OK

$ cd /Users/archcore/solbian/codex-phase-i-stage4 && python3 smoke_ui.py
SMOKE UI PASSED — 149/149 checks        # after `apply_to_stage4.sh`
```

The staged Stage 4 build was additionally verified two ways in the sandbox:

* overlay install (new app/static/smoke) → `SMOKE UI PASSED — 149/149`;
* new app + the **old** Stage 4 `smoke_ui.py` → `SMOKE UI PASSED — 96/96`
  (backward compatible).

## Living-store policy (short form)

* Living store: `/Users/archcore/solbian/codex-phase-i-stage4/data/codex_phase_i.sqlite`.
* Seed (once) from `/Users/archcore/solbian/codex-phase-i-stage5/data/codex_phase_i.sqlite`.
* SoT (read-only): `/Users/archcore/solbian/codex-phase-i-stage3/codex_phase_i.sqlite`.
* Consolidation max status: `WORKING`. `CANONICAL` is not in the schema and is
  never written; `living_store.scan_canonical` asserts it.

## Sandbox note (important)

This session's file policy is **workspace-write for the Stage 7 directory only**;
the Stage 4/5/3 trees and the Mac corpus are read-only, and escalation required
an approval channel that was not available. The Stage 4 changes are therefore
**staged under `_stage4_build/`** exactly as the brief allows, with an idempotent
installer:

```bash
cd /Users/archcore/solbian/codex-phase-i-stage7
bash apply_to_stage4.sh          # copies app.py/static/smoke_ui.py + living_store.py,
                                 # backs up originals, migrates the living store
cd /Users/archcore/solbian/codex-phase-i-stage4 && python3 smoke_ui.py
```

The Stage 4 app also auto-runs the living-store migration on startup, so the
explicit migration step is optional.

## Invariants held

* `source_document` row snapshot unchanged across all HTTP requests (both smokes).
* No `CANONICAL` value anywhere in the living store (`scan_canonical`).
* Stage 3 SoT and Stage 5 seed stores byte-identical (sha256) before/after.
* Mac corpus fingerprint unchanged; previews read-only, ≤ 200 KB.
* Every engine row is attributable (`engine:stage5:*`); every consolidation is
  attributable (`consolidation:accepted:<proposal_id>`) and reversible.

## Notes / follow-ups

* `apply_to_stage4.sh` must be run by an actor with write access to the Stage 4
  tree (the sandbox denies writes there).
* Real LLM Solace, auto-accept-all, and Stage 8 reassessment remain out of scope.
