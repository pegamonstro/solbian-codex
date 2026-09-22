# Phase I — Stage 3 Minimal Data Layer
**As-of:** 2026-09-20 ~23:20 PT · **CANONICAL:** NONE  
**Authority:** Phase I SPEC 06/10/13 + Stage 2 baseline  
**Rule:** smallest durable store; no SEED/GOLEM/Machina/vector/graph/microservice; no silent corpus rewrite; no catalogue merges.

## Goal
Implement the smallest durable storage model capable of representing:
- conversations (+ messages)
- source material (pointers into historical corpus — **not copies that replace SoT**)
- Codex content (documents/sections — **WORKING/PROPOSED** by default)
- proposals
- revisions
- provenance links

## Hard constraints
1. **Do not modify** Mac `/Users/archcore/solbian/codex` historical files (read-only ingest).
2. Primary historical SoT remains Mac `source_original/` (+ full MD scrolls). GH `main` tip ≠ historical.
3. Preserve plurality: Law A/B/B′/C, Protocols 01–08 vs Gitea-5, scroll MD≠sref ordinals, scroll 20 anomaly — as **status/flags**, not flattened.
4. Wave5 Working fences are WORKING metadata, not source CANONICAL.
5. Prefer SQLite + plain files (inspectable, backup-friendly). No vector DB, no graph DB.
6. All rows: id, created_at, updated_at, status enum, attribution where applicable.
7. Content status enum at minimum: `SOURCE` | `HISTORICAL` | `WORKING` | `PROPOSED` | `REVISION` | `RELATED` | `UNKNOWN` — never invent `CANONICAL` without explicit JD flag (default absent).

## Suggested schema (implement or improve if simpler)
See `SCHEMA.md`.

## Deliverables (under this STAGE_3 dir on Mac workspace)
- `SCHEMA.md` — final implemented schema
- `schema.sql` — DDL
- `codex_phase_i.sqlite` — empty or sample DB
- `ingest_baseline.py` — read-only: register corpus roots + sample entries from Stage 2 inventory JSON (copy of inventory provided)
- `smoke_test.py` — assert tables exist; insert sample conversation→message→proposal→provenance; round-trip query
- `README.md` — how to run smoke
- `DSH_RESULT.md` — what was done, failures, deviations

## Acceptance
- Smoke test exits 0
- Original Mac corpus untouched (script must only READ if it touches Mac path)
- No catalogue merge logic
- Status COMPLETE or INCOMPLETE with remainder

## Out of scope (Stage 4+)
UI, Solace chat, engine synthesis, LLM calls inside the store.
