# Codex Solbian — Hybrid Synthesis Engine (ADMIT-thin slice)

Portable Stage 5b engine that turns a preserved Journey conversation into `PROPOSED`
`codex_document` candidates, with an optional LLM draft mode that never bypasses
human Accept.

## Quick start

```bash
# 1. Build the fixture DB from JSON
cd codex-phase-i-stage5b-hybrid
python3 fixtures/build_fixture_db.py

# 2. Run deterministic synthesis on the "Who are we?" conversation
python3 engine.py --db fixtures/who_are_we.sqlite \
    synthesize-dialogue --conversation conv_5bbf3990a8ce4b47

# 3. Inspect proposals (quiet by default: hybrid-only, Theme:* hidden)
python3 engine.py --db fixtures/who_are_we.sqlite list-proposed

# 4. Explicitly Accept a proposal -> WORKING
python3 engine.py --db fixtures/who_are_we.sqlite accept --document <ID>

# 5. Run smoke tests
python3 smoke_hybrid.py
# Optional mock-LLM smoke (no running model required)
SOLBIAN_LLM_MOCK=1 python3 smoke_hybrid.py
```

## Default living DB

`--db` is now optional.  When omitted the engine uses `SOLBIAN_LIVING_DB`, then
falls back to the Stage 4 living store:

```text
/Users/archcore/solbian/codex-phase-i-stage4/data/codex_phase_i.sqlite
```

Set `SOLBIAN_LIVING_DB` to override.

Safety:

- Writes to the Mac historical corpus (`~/solbian/codex`) are refused.
- If the DB looks like a Stage 3 SoT read-only corpus, the engine warns and
  refuses to write.

## Optional LLM mode

```bash
# Use default Ollama endpoint
python3 engine.py --db fixtures/who_are_we.sqlite --llm \
    synthesize-dialogue --conversation conv_5bbf3990a8ce4b47

# Or point at another OpenAI-compatible endpoint
export SOLBIAN_LLM_BASE="http://localhost:11434/v1"
export SOLBIAN_LLM_MODEL="kimi-k2.7-code:cloud"
export SOLBIAN_LLM_API_KEY=""   # only if required

# CI / deterministic mock when no model is running
export SOLBIAN_LLM_MOCK=1
```

The LLM client tries `/v1/chat/completions` first and falls back to Ollama's
native `/api/chat`.  It tolerates markdown fences, nested JSON keys, and
`body`/`content`/`synthesis` aliases.  If the model returns substantial text
that cannot be parsed as JSON, it is wrapped as a PROPOSED body behind an
epistemic fence.

The LLM may only produce `PROPOSED` rows.  If the endpoint is unreachable the
engine fails closed and the deterministic results still return.

## Quieter `list-proposed`

Default view shows only rows whose attribution looks like `hybrid:*`, newest
first, and suppresses `Theme:*` titles.

Flags:

- `--all` — include older Stage-5 archaeology proposals
- `--themes` — include `Theme:*` titles
- `--limit N` — cap output
- `--verbose` — equivalent to `--all --themes`

The header prints the number of hidden rows so filtering is obvious.

## Project layout

```
codex-phase-i-stage5b-hybrid/
├── codex_hybrid/          # engine package
│   ├── config.py          # runtime config + default DB
│   ├── db.py              # living-store wrapper + safety guards
│   ├── extract.py         # deterministic extractor
│   ├── llm_client.py      # OpenAI-compatible client with fallback + mock
│   └── synthesis.py       # hybrid runner
├── engine.py              # CLI entry point
├── smoke_hybrid.py        # smoke tests
├── fixtures/
│   ├── who_are_we.json    # "Who are we?" sample conversation
│   ├── build_fixture_db.py
│   └── who_are_we.sqlite  # generated fixture DB
├── stage4_ui/             # optional Stage 4 integration docs + button
├── HYBRID_SYNTHESIS.md    # design note
├── install_to_mac.sh      # install instructions for Partner
├── apply_to_stage4.sh     # Stage 4 UI hook instructions
├── APPLY_MAC.md           # concise Mac apply steps for Partner
└── DSH_RESULT.md          # slice completion status
```

## Guardrails

- **No auto-Accept.**  `accept` is a separate explicit command.
- **No CANONICAL writes.**  The engine never sets `status = 'CANONICAL'`.
- **Deterministic by default.**  LLM is OFF unless `--llm` is passed.
- **Mac historical corpus untouched.**  All writes target the Stage 4/7 living
  SQLite store.

## Install on Mac

See `install_to_mac.sh` and `APPLY_MAC.md` for exact copy targets under
`/Users/archcore/solbian/codex-phase-i-stage5/` and optional Stage 4 hooks.

## Token

When complete this slice reports `HYBRID_SLICE_POLISH_OK` in `DSH_RESULT.md`.
