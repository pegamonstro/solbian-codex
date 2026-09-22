# Mac hotfix after hybrid polish install (2026-09-22)

CANONICAL: NONE

## Issues found on Mac apply

1. **False-positive historical corpus refuse** — `is_historical_corpus` used substring match on `/Users/archcore/solbian/codex`, which also matched `codex-phase-i-*` paths. Fixed to `Path.relative_to` exact tree roots.
2. **Stage-3 SoT warn raised on write** — `_write_guard` treated advisory warnings as hard errors. Softened to refuse historical only.
3. **Quiet `list-proposed` hybrid filter inverted** — SQL bound `(0 if hybrid_only else 1)` with `(? = 0 OR LIKE hybrid)`, so hybrid_only=True always passed. Fixed binding to `(1 if hybrid_only else 0)`.
4. **Hidden count** — now `all - filtered` (quiet filters), not `all - shown` (which went negative under `--limit`).

## Verified after hotfix

- Fixture `smoke_hybrid.py` OVERALL PASS
- Living-copy synthesize deterministic OK
- Live `--llm` produced hybrid:llm body ~3628 chars (no empty-body)
- Quiet list shows hybrid:* only; Theme:* and engine:stage5 archaeology require `--themes` / `--all`
