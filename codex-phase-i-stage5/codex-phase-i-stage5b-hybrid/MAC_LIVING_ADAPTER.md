# Mac living-store adapter note
**As-of:** 2026-09-22 · Partner post-install

DSH portable package uses a fixture schema with a **dual-schema** `codex_hybrid/db.py`:
- Fixture smoke still PASS
- Phase I living store (`message.body`, `conversation.id`, `proposal` + `revision` + `provenance_link`) supported
- `attribution` is set to `hybrid:deterministic` or `hybrid:llm` so `list-proposed` stays quiet

## Default living DB

`--db` is now optional.  When omitted, the engine uses `SOLBIAN_LIVING_DB` and
falls back to:

```text
/Users/archcore/solbian/codex-phase-i-stage4/data/codex_phase_i.sqlite
```

Set `SOLBIAN_LIVING_DB` on the Mac to point at the live store if it lives
elsewhere.

## Smoke on Who are we? (throwaway copy)

```bash
cd ~/solbian/codex-phase-i-stage5/codex-phase-i-stage5b-hybrid
# snapshot living DB while app may hold lock
python3 -c "import sqlite3; s=sqlite3.connect('file:/Users/archcore/solbian/codex-phase-i-stage4/data/codex_phase_i.sqlite?mode=ro',uri=True); d=sqlite3.connect('_smoke_living.sqlite'); s.backup(d); d.close()"
python3 engine.py --db _smoke_living.sqlite synthesize-dialogue --conversation conv_5bbf3990a8ce4b47
python3 engine.py --db _smoke_living.sqlite list-proposed
# Accept a hybrid proposal id (attribution hybrid:deterministic or hybrid:llm) — not older Stage-5 proposals
python3 engine.py --db _smoke_living.sqlite accept --document prop_...
```

Because the default path is the Stage 4 living store, you can also run against
the live DB with care:

```bash
python3 engine.py synthesize-dialogue --conversation conv_5bbf3990a8ce4b47
python3 engine.py list-proposed
python3 engine.py accept --document prop_...
```

## Optional LLM

```bash
export SOLBIAN_LLM_BASE=http://localhost:11434/v1
export SOLBIAN_LLM_MODEL=kimi-k2.7-code:cloud
python3 engine.py --db _smoke_living_llm.sqlite --llm synthesize-dialogue --conversation conv_5bbf3990a8ce4b47
```

If Ollama is not reachable, the deterministic path still produces PROPOSED rows
and the LLM error is printed.

## Quieter list

```bash
python3 engine.py list-proposed              # hybrid-only, Theme:* hidden
python3 engine.py list-proposed --themes     # include Theme:* rows
python3 engine.py list-proposed --all        # include older Stage-5 archaeology
python3 engine.py list-proposed --verbose    # --all --themes
python3 engine.py list-proposed --limit 10   # cap output
```

**Note:** Deterministic extracts are intentionally broad (many theme/claim rows). Prefer Accepting LLM drafts or curated deterministic rows. Filter `attribution LIKE 'hybrid:%'`.
