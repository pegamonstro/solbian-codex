# Apply Hybrid Slice on Mac

**As-of:** 2026-09-22 · **CANONICAL:** NONE

This is the Partner-facing checklist for installing the `codex-phase-i-stage5b-hybrid`
portable package on the Mac.

## 1. Copy the package

On the Mac, copy the entire `codex-phase-i-stage5b-hybrid/` directory to the
Stage 5 area:

```bash
MAC_STAGE5="/Users/archcore/solbian/codex-phase-i-stage5"
rm -rf "${MAC_STAGE5}/codex-phase-i-stage5b-hybrid"
cp -R "/path/to/dsh-results/codex-phase-i-stage5b-hybrid" "${MAC_STAGE5}/"
cd "${MAC_STAGE5}/codex-phase-i-stage5b-hybrid"
chmod +x engine.py smoke_hybrid.py fixtures/build_fixture_db.py
```

## 2. Run smoke tests

```bash
cd "${MAC_STAGE5}/codex-phase-i-stage5b-hybrid"
python3 smoke_hybrid.py
# Optional mock-LLM smoke (no model required)
SOLBIAN_LLM_MOCK=1 python3 smoke_hybrid.py
```

Expected: `OVERALL: PASS`.

## 3. Test against a throwaway copy of the living store

The engine defaults to the Stage 4 living DB:

```text
/Users/archcore/solbian/codex-phase-i-stage4/data/codex_phase_i.sqlite
```

Make a copy and test on that copy first:

```bash
cd "${MAC_STAGE5}/codex-phase-i-stage5b-hybrid"
python3 -c "
import sqlite3
src = sqlite3.connect('file:/Users/archcore/solbian/codex-phase-i-stage4/data/codex_phase_i.sqlite?mode=ro', uri=True)
dst = sqlite3.connect('_smoke_living.sqlite')
src.backup(dst)
dst.close()
"
python3 engine.py --db _smoke_living.sqlite synthesize-dialogue --conversation conv_5bbf3990a8ce4b47
python3 engine.py --db _smoke_living.sqlite list-proposed
python3 engine.py --db _smoke_living.sqlite accept --document prop_...
```

## 4. Optional: run against the live Stage 4 DB

Only after smoke and throwaway-copy tests pass:

```bash
python3 engine.py synthesize-dialogue --conversation conv_5bbf3990a8ce4b47
python3 engine.py list-proposed
python3 engine.py accept --document prop_...
```

## 5. Optional: enable LLM draft

Requires a reachable OpenAI-compatible endpoint (default Ollama).

```bash
export SOLBIAN_LLM_BASE=http://localhost:11434/v1
export SOLBIAN_LLM_MODEL=kimi-k2.7-code:cloud
python3 engine.py --llm synthesize-dialogue --conversation conv_5bbf3990a8ce4b47
```

If the model is unreachable, the deterministic path still runs and a fail-closed
LLM error is printed. No empty proposals are created.

## 6. Optional: Stage 4 UI hook

See:

- `stage4_ui/README.md`
- `stage4_ui/synthesize_button.html`
- `apply_to_stage4.sh`

Summary:

- Add a **"Synthesize dialogue"** button that POSTs to `/api/synthesize` and
  calls `engine.py synthesize-dialogue --conversation <id>` (deterministic,
  default DB, no `--db` needed).
- Add a **"Draft with LLM"** action behind explicit confirmation or `?llm=1`
  that calls `engine.py --llm synthesize-dialogue --conversation <id>`.
- Keep **Accept** as a human-only UI action that calls
  `engine.py accept --document <id>`.
- Review surface should default to the quiet `list-proposed` view; add toggles
  for `--themes` and `--all` if desired.

## 7. Quieter list flags

```bash
python3 engine.py list-proposed              # hybrid-only, Theme:* hidden
python3 engine.py list-proposed --themes     # include Theme:*
python3 engine.py list-proposed --all        # include older Stage-5 archaeology
python3 engine.py list-proposed --verbose  # --all --themes
python3 engine.py list-proposed --limit 10   # cap output
```

The header prints how many rows were hidden by the default filter.

## Safety reminders

- The engine **refuses** to write the historical corpus (`~/solbian/codex`).
- If the DB looks like a Stage 3 SoT read-only corpus, the engine warns and
  refuses to write.
- No auto-Accept. No `CANONICAL` writes. No catalogue merges.
