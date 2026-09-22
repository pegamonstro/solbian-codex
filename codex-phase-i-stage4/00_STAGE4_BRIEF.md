# Phase I — Stage 4 Two-Surface Prototype
**As-of:** 2026-09-21 · **CANONICAL:** NONE  
**Authority:** SPEC 04/09/13 · Stage 3 store at sibling `../STAGE_3` path on Mac: `/Users/archcore/solbian/codex-phase-i-stage3/`

## Goal
Minimal two-tab (or two-route) local UI:
1. **Solace** — conversation view (list conversations, show messages, append a new message to a WORKING conversation in SQLite — not LLM-backed yet unless trivial stub reply marked WORKING)
2. **Codex Solbian** — **read-only** browser of `source_document` / optional `codex_document` from the Stage 3 SQLite (filter by kind/status/path; show metadata + optional file preview for text under Mac corpus **read-only**)

## Constraints
- Do **not** modify `/Users/archcore/solbian/codex` historical tree (read-only open for preview).
- Do **not** invent CANONICAL; UI must never offer a "make canonical" control.
- No SEED/GOLEM/Machina/vector/graph/microservices.
- Prefer Python stdlib: `http.server` + single HTML/JS page, **or** Flask/FastAPI only if already easy — simplest wins.
- DB path: `/Users/archcore/solbian/codex-phase-i-stage3/codex_phase_i.sqlite` (or copy into Stage 4 cwd — prefer open existing Stage 3 DB read-write for conversation append only).
- Calm, content-first, two tabs.

## Deliverables (cwd `/Users/archcore/solbian/codex-phase-i-stage4/`)
- `app.py` — local server
- `static/` or embedded templates — Solace + Codex tabs
- `README.md` — how to run (`python3 app.py` → localhost)
- `smoke_ui.py` or shell smoke: hits endpoints, asserts 200 + key JSON
- `DSH_RESULT.md` — STATUS COMPLETE/INCOMPLETE

## Acceptance
- `python3 smoke_ui.py` exit 0
- Codex view cannot mutate source_document bodies
- Solace can create conversation + append messages into SQLite
- Historical Mac corpus mtimes unchanged for source_original (except optional atime)

## Out of scope
Codex Engine synthesis (Stage 5), real Solace LLM (optional stub only), auth, deploy.
