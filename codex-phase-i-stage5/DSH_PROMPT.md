# Task: Codex Solbian Phase I — Stage 5 Codex Engine Prototype

Read `00_STAGE5_BRIEF.md`. Implement under `/Users/archcore/solbian/codex-phase-i-stage5/`.

## Store
Use existing DB: `/Users/archcore/solbian/codex-phase-i-stage3/codex_phase_i.sqlite`
(~935 source_document rows). You may also read Stage 4 app patterns at `/Users/archcore/solbian/codex-phase-i-stage4/` but do not break Stage 4.

## Implement
Deterministic engine (stdlib + sqlite3). LLM optional behind `--llm` default OFF.

Required:
- `engine.py` with `run`, `list-proposals`, `show <id>`
- Writes only PROPOSED/WORKING to proposal/concept/relationship/provenance_link (+ optional analysis_run)
- Never mutate source_document; never invent CANONICAL; never write Mac corpus
- Each proposal has provenance_link to a source_document and/or message
- `smoke_engine.py` exit 0
- `README.md`, `DSH_RESULT.md`

Analysis ideas (implement at least these):
1. Plurality reminders from plurality_flags / path patterns (laws, protocols, scrolls, scroll_20)
2. Duplicate basename detection across corpus roots → proposal
3. Underdeveloped: high-frequency tokens in titles/roles without matching glossary/doc
4. If conversations exist, extract long messages as durable candidates (INTERPRETATION note)
5. Discussion-topic proposals for gaps

Keep it boring and inspectable. Prefer idempotent analysis_run ids or clear re-run behaviour.

## Verify
```bash
python3 smoke_engine.py
```
