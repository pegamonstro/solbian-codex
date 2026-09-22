# Task: Codex Solbian Phase I — Stage 6 Historical Validation + Stage 4 Engine tab

Read `00_STAGE6_BRIEF.md`. Do both A and B.

## Paths
- Stage 6 cwd: `/Users/archcore/solbian/codex-phase-i-stage6/`
- Stage 3 SoT DB (read-only): `/Users/archcore/solbian/codex-phase-i-stage3/codex_phase_i.sqlite`
- Stage 5 engine + working DB: `/Users/archcore/solbian/codex-phase-i-stage5/` and `…/data/codex_phase_i.sqlite`
- Stage 4 UI: `/Users/archcore/solbian/codex-phase-i-stage4/`
- Mac corpus (read-only): `/Users/archcore/solbian/codex`

## A — Stage 6
Implement validate_historical.py, smoke_stage6.py, VALIDATION_REPORT.md, README.md, DSH_RESULT.md under stage6 cwd. Exit 0 on PASS. Never write Mac corpus or Stage 3 SoT.

## B — Stage 4 Engine tab
Add Engine/Proposals tab to Stage 4 (read-only list/detail of Stage 5 proposals + provenance). Keep Solace/Codex smokes green; extend smoke. No CANONICAL controls. Optional dry-run button only if safe.

## Verify
```bash
cd /Users/archcore/solbian/codex-phase-i-stage6 && python3 smoke_stage6.py
cd /Users/archcore/solbian/codex-phase-i-stage4 && python3 smoke_ui.py
```
Both exit 0. Document in DSH_RESULT.md.
