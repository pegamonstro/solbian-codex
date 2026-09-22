# Task: Codex Solbian Phase I — Stage 4 Two-Surface Prototype

Read `00_STAGE4_BRIEF.md`. Implement entirely under this cwd:
`/Users/archcore/solbian/codex-phase-i-stage4/`

## Use existing Stage 3 DB
Path: `/Users/archcore/solbian/codex-phase-i-stage3/codex_phase_i.sqlite`
(~966 source_document rows already ingested). Open it for:
- Solace tab: read/write conversations + messages only
- Codex tab: **read-only** source_document (+ optional text preview by opening Mac paths read-only)

## Implement
Minimal local web UI (prefer Python stdlib `http.server` + one HTML page with two tabs, or tiny Flask if simpler for you). Must include:
1. Tab **Solace**: list conversations; open one; show messages; form to create conversation; form to append message (role jd|solace). Persist to SQLite. Optional stub Solace reply clearly labeled WORKING — not required.
2. Tab **Codex**: browse/filter source_document (path, status, role); detail pane with metadata; if file exists under registered corpus root, show text preview (cap size e.g. 200KB) **read-only**. No edit controls for Codex content.
3. `README.md`, `smoke_ui.py` (HTTP checks exit 0), `DSH_RESULT.md`.

## Forbidden
Modify historical corpus under `/Users/archcore/solbian/codex` (except read). CANONICAL controls. Vector/graph/SEED/GOLEM. Heavy frameworks.

## Verify
Start server in smoke, hit endpoints, kill server, exit 0. Document how JD runs: `python3 app.py` → http://127.0.0.1:PORT
