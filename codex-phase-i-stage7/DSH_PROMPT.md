# Task: Codex Solbian Phase I — Stage 7 Living Loop

Read `00_STAGE7_BRIEF.md`. Implement the living loop.

## Paths
- Stage 7 cwd: `/Users/archcore/solbian/codex-phase-i-stage7/`
- Stage 4 UI (modify in place if sandbox allows; else stage under `_stage4_build/` + `apply_to_stage4.sh`): `/Users/archcore/solbian/codex-phase-i-stage4/`
- Stage 5 engine: `/Users/archcore/solbian/codex-phase-i-stage5/engine.py`
- Stage 3 SoT (read-only): `/Users/archcore/solbian/codex-phase-i-stage3/codex_phase_i.sqlite`
- Mac corpus (read-only): `/Users/archcore/solbian/codex`

## Requirements
1. One living SQLite store policy (document + implement). Prefer Stage 4 `data/codex_phase_i.sqlite` as living store; ensure engine tables + proposals available (migrate/copy from Stage 5 data once if needed).
2. Stage 4: after Solace message (or Engine "Run living loop"), run durable/engine against living DB; refresh proposals.
3. Controlled consolidation: Accept proposal → WORKING `codex_document` + `revision` + provenance. **Never CANONICAL.**
4. Codex tab shows WORKING `codex_document` clearly labeled alongside HISTORICAL `source_document`.
5. `living_loop.py once` + `smoke_stage7.py` exit 0.
6. Stage 4 smoke still exit 0 (extended).
7. README.md, DSH_RESULT.md under stage7.

## Verify
```bash
cd /Users/archcore/solbian/codex-phase-i-stage7 && python3 smoke_stage7.py
cd /Users/archcore/solbian/codex-phase-i-stage4 && python3 smoke_ui.py
```
