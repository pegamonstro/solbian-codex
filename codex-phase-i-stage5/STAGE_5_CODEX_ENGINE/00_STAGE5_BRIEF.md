# Phase I — Stage 5 Codex Engine Prototype
**As-of:** 2026-09-21 · **CANONICAL:** NONE  
**Authority:** SPEC 05/08/12/14 · Stage 3 DB · Stage 4 UI (optional thin admin surface)

## Goal
Smallest engine that turns preserved sources into **inspectable observations + PROPOSED records**, never silent doctrine.

## Inputs (read)
- SQLite: `/Users/archcore/solbian/codex-phase-i-stage3/codex_phase_i.sqlite` (or Stage 4 `data/` copy — prefer Stage 3 path as SoT store; Stage 4 may symlink/use same file)
- Conversations + messages (Solace)
- `source_document` rows (+ optional read-only text preview ≤200KB from Mac corpus)
- Do **not** modify `/Users/archcore/solbian/codex` except read

## Outputs (write — status PROPOSED / WORKING only)
Into existing tables where possible:
- `proposal` — drafted additions/revisions/discussion topics
- `concept` — extracted concept candidates (status WORKING/PROPOSED)
- `relationship` — candidate links with confidence TITLE-LEVEL|SYNTHESIS|UNKNOWN (TEXT-SUPPORTED only if quote evidence stored)
- `provenance_link` — every proposal/concept must link to message and/or source_document
- Optional new table `analysis_run` (id, started_at, finished_at, kind, summary_json, status) if needed — keep minimal

**Forbidden writes:** elevating CANONICAL; mutating `source_document` bodies/rows; catalogue merges; deleting historical pointers.

## Engine behaviour (prototype)
Prefer **deterministic** analysis (stdlib only) so the Codex stays model-independent:
1. Scan conversations for candidate durable sentences (length/heuristics; mark as INTERPRETATION).
2. Scan source_document titles/roles/paths for concept-name frequency vs definitions (underdeveloped if mentioned often without glossary hit).
3. Flag plurality: law/protocol/scroll flags already on rows → emit proposals “preserve plurality / do not merge”.
4. Detect simple title-level duplicates (same basename under different roots).
5. Emit discussion-topic proposals from UNDERDEVELOPED patterns.
6. CLI: `python3 engine.py run` → prints summary + inserts proposals.
7. Optional: `python3 engine.py list-proposals` / `show <id>`
8. Optional thin Stage 4 admin tab **or** `/api/engine/*` endpoints in a small `engine_api.py` / extend Stage 4 app carefully — if extending Stage 4, do not break Solace/Codex smoke; add `smoke_engine.py`.

LLM calls are **optional** and must be behind `--llm` flag default OFF. If used, label outputs INTERPRETATION/PROPOSED and never auto-consolidate.

## Deliverables (cwd `/Users/archcore/solbian/codex-phase-i-stage5/`)
- `engine.py` — main CLI
- `README.md`
- `smoke_engine.py` — exit 0 (run analysis on DB; assert ≥1 proposal with provenance; assert no CANONICAL; assert source_document count unchanged; assert Mac corpus not written)
- `DSH_RESULT.md`
- Optional UI wiring docs if Stage 4 extended

## Acceptance
- `python3 smoke_engine.py` exit 0
- Distinguishes SOURCE vs INTERPRETATION vs PROPOSAL in stored status/notes
- No silent consolidation into accepted Codex content
- Re-run idempotent or clearly versioned analysis_run

## Out of scope
Stage 6 historical validation suite expansion; Stage 7 living LLM Solace; polity/SEED/GOLEM.
