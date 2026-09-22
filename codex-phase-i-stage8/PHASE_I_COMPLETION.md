# PHASE_I_COMPLETION — Stages 1–7 status
**As-of:** 2026-09-21 ~02:24 PT · **CANONICAL:** NONE  
**Verdict:** Phase I stages 1–7 are **substantively complete** for the living loop.
Stage 8 is reassessment only (this pack). Nothing here elevates content to CANONICAL.

## Summary table

| Stage | Name | Status | Key evidence | Mac path (primary) | Box path |
| --- | --- | --- | --- | --- | --- |
| 1 | Freeze / SPEC pack | COMPLETE (PROPOSED) | SPEC 00–14 on hub branch `spec/phase-i-software-stack` | (hub / consol packs) | `/workspace/codex-solbian-working/SPEC/PHASE_I_SOFTWARE_STACK/` |
| 2 | Baseline archaeology | COMPLETE | Inventory, structure, timeline, contradictions, plurality A/B/B′/C, protocols 5 vs 8 | `~/solbian/codex-phase-i-stage*` WTs; corpus `~/solbian/codex` | `PHASE_I_BASELINE/` |
| 3 | Minimal data layer | COMPLETE | SQLite schema 10 tables; ingest; smoke exit 0; later full ingest → 935 `source_document` | `~/solbian/codex-phase-i-stage3/` | `STAGE_3_MINIMAL_DATA_LAYER/` |
| 4 | Two-surface UI (+ Engine tab) | COMPLETE | Solace + Codex + Engine; living store `data/codex_phase_i.sqlite`; smokes 61→96→149 | `~/solbian/codex-phase-i-stage4/` | `STAGE_4_TWO_SURFACE/` |
| 5 | Codex Engine | COMPLETE | Deterministic analyzers; 44 proposals; smoke **37/37**; no CANONICAL | `~/solbian/codex-phase-i-stage5/` | `STAGE_5_CODEX_ENGINE/` |
| 6 | Historical validation | COMPLETE (PASS) | **45/45** checks; SoT + Mac corpus fingerprints unchanged | `~/solbian/codex-phase-i-stage6/` | `STAGE_6_HISTORICAL_VALIDATION/` |
| 7 | Living loop | COMPLETE (per mission) | message→engine→Accept→WORKING; smoke_ui **149/149**; never CANONICAL | `~/solbian/codex-phase-i-stage7/` (+ Stage 4 wiring) | `STAGE_7_LIVING_LOOP/` (brief on box) |
| 8 | Reassessment | THIS PACK | Docs only | `~/solbian/codex-phase-i-stage8/` (copy target) | `STAGE_8_REASSESSMENT/` |

## Stage-by-stage evidence

### Stage 1 — Freeze
- SPEC pack defines Phase I as the small loop; Constitution + SPEC 13/14 bound later work.
- Placement: PROPOSED on hub `spec/phase-i-software-stack` (not product doctrine).
- Pointers: `SPEC/13_PHASE_I_ROADMAP.md`, `SPEC/14_SCOPE_CREEP_GUARDRAILS.md`.

### Stage 2 — Baseline archaeology
- Delivered: `CORPUS_INVENTORY.*`, `STRUCTURE.md`, `CONTRADICTIONS.md`, `DUPLICATES.md`,
  `HISTORICAL_TIMELINE.md`, `RELATED_PROJECTS.md`, `UNDERDEVELOPED_AREAS.md`, `BASELINE_REPORT.md`.
- Critical posture preserved: Law catalogues A/B/B′/C distinct; protocols 5 vs 8 recorded;
  scroll XX gap / XXI duplicate; MD≠sref ordinals; SEED/GOLEM/Machina/DAO fenced RELATED.
- Live Mac confirm (Partner): `~/solbian/codex` ~8.9M, HEAD `e289bd8`, dirty, 897 files.
- **CANONICAL:** NONE throughout.

### Stage 3 — Minimal data layer
- Schema: conversations, messages, source_document, codex_document, proposal, revision,
  concept, relationship, provenance_link, corpus_root (+ status CHECKs without CANONICAL).
- Ingest from Stage 2 inventory; plurality flags preserved; Mac corpus never written.
- Later full ingest measured in Stage 6: **935** PRIMARY `source_document` rows
  (966 inventory entries − 31 duplicates).
- SoT store sha256 (Stage 6): `8c6e15a6c98c…` — byte-stable across validation.

### Stage 4 — Two-surface (+ Engine)
- Surfaces: **Solace** (write conversation/message only), **Codex** (read-only browse),
  later **Engine** (proposals / dry-run / Accept→WORKING in Stage 7).
- Living store: `stage4/data/codex_phase_i.sqlite` (working copy pattern; Stage 3 SoT RO).
- Smoke progression: 61 (two-surface) → 96 (Engine tab staged) → **149** (living loop, Stage 7).
- Stub Solace reply labelled `[WORKING STUB — not LLM-backed]`.

### Stage 5 — Codex Engine
- Deterministic stdlib engine: plurality, duplicates, underdeveloped, durable (messages),
  discussion topics; optional LLM behind `--llm` default OFF.
- Working store proposals: **44**; concepts **20**; provenance on all proposals.
- Smoke **37/37**; refuses `--db` inside Mac corpus; no CANONICAL in status columns.

### Stage 6 — Historical validation
- `VALIDATION_REPORT.md`: **VERDICT PASS — 45/45**.
- Coverage, plurality non-collapse, idempotent re-runs, dry-run rollback, corpus/SoT
  fingerprints identical before/after.
- Engine tab bundle staged; install noted as sandbox-limited then Partner-applied path.

### Stage 7 — Living loop
- Goal loop (SPEC 13 / brief): JD↔Solace → preserve → Engine → propose → explicit Accept →
  WORKING `codex_document` (+ revision / provenance) → browse includes WORKING.
- Acceptance (mission): `smoke_stage7` / Stage 4 `smoke_ui` **149/149**; consolidation max
  status WORKING; **never CANONICAL**.
- Box note: only `00_STAGE7_BRIEF.md` present under `STAGE_7_LIVING_LOOP/`; full Mac
  deliverables (`living_loop.py`, DSH_RESULT, Stage 4 install) live under
  `~/solbian/codex-phase-i-stage7/` and updated stage4 — Partner/mission evidence is
  authoritative for Stage 7 completion.

## What Phase I did **not** claim

- No catalogue merge; no doctrine pick among A/B/B′/C or protocol 5 vs 8.
- No real LLM Solace; no vector/graph/blockchain store; no SEED/GOLEM/Machina coupling.
- No CANONICAL elevation path in schema, UI, or engine.
- No silent auto-accept of proposals.

## Readiness for Stage 8 judgment

The loop is operable and tested. Stage 8 therefore **may** decide Phase II needs —
and by SPEC 13 **must not** auto-admit historical features. See `ADMISSION_REGISTER.md`
and `REASSESSMENT_REPORT.md`.
