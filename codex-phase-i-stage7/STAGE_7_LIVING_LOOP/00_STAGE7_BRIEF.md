# Phase I — Stage 7 Living Loop
**As-of:** 2026-09-21 · **CANONICAL:** NONE  
**Authority:** SPEC 05/08/09/13 · Stages 3–6 on Mac

## Goal
Make this loop operable end-to-end in the Stage 4 UI (+ thin CLI if needed):

```
JD ↔ Solace (UI)
      ↓
preserved conversation (SQLite)
      ↓
Codex Engine (durable + optional full run)
      ↓
proposed synthesis (proposal rows)
      ↓
controlled consolidation (explicit accept → WORKING Codex content)
      ↓
Codex Solbian (read-only browse includes WORKING docs)
```

## Hard rules
- **Never** invent or write `CANONICAL`. Consolidation max status = `WORKING` (or keep as accepted proposal + `codex_document` status WORKING).
- Do not write Mac `/Users/archcore/solbian/codex` historical tree.
- Stage 3 SoT DB remains read-only baseline; living writes go to a **living store** (prefer Stage 4 `data/codex_phase_i.sqlite` and/or Stage 5 `data/` — unify to one living DB if practical, document clearly).
- Controlled consolidation requires an explicit API/UI action (no silent auto-accept of all proposals).
- Preserve provenance_link from proposal → message/source_document onto the consolidated `codex_document` / `revision`.

## Implement (cwd `/Users/archcore/solbian/codex-phase-i-stage7/` + wire Stage 4)

### A. Living store policy
Document + implement one clear living DB path used by Solace + Engine + consolidation. If copying from Stage 3/5, say so. Prefer: Stage 4 `data/codex_phase_i.sqlite` as living store; ensure it has engine tables (`analysis_run`) and can hold proposals (migrate/copy from Stage 5 working DB once if needed).

### B. Loop triggers in Stage 4 UI
1. After appending a Solace message (or via Engine tab button **Run living loop**):
   - run Stage 5 durable analyzer (and/or lightweight `engine.py run` subset) against living DB
   - refresh Engine proposals list
2. Engine tab: for a PROPOSED proposal, button **Accept → WORKING** (controlled consolidation):
   - create/update `codex_document` status WORKING with body/summary from proposal
   - create `revision` row linking proposal_id
   - copy/attach provenance_link
   - set proposal status to something like WORKING or leave PROPOSED with note "accepted" — prefer status field `WORKING` meaning accepted-into-working-codex, or add `notes` Accepted — do **not** use CANONICAL
3. Codex tab: show `codex_document` rows (WORKING) in addition to `source_document` HISTORICAL — clearly labeled

### C. CLI
`python3 living_loop.py once` — smoke helper: create convo+msg → engine → list new proposals → consolidate one → assert codex_document WORKING exists.

### D. Deliverables
Under stage7: `living_loop.py`, `smoke_stage7.py`, `README.md`, `DSH_RESULT.md`, any migrate script.  
Update Stage 4 `app.py`/`static/*`/`smoke_ui.py` (install in place; Partner can apply if sandbox blocks).

## Acceptance
- `python3 smoke_stage7.py` exit 0 (full loop on throwaway DB)
- Stage 4 smoke still exit 0 (extended checks for loop/consolidation)
- No CANONICAL anywhere; Mac corpus fingerprint unchanged; Stage 3 SoT unchanged

## Out of scope
Stage 8 Phase II reassessment; real LLM Solace (stub OK); auto-accept all proposals; SEED/GOLEM.
