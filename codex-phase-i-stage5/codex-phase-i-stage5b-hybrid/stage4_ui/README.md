# Stage 4 UI — Synthesize Dialogue Hook

This directory contains a minimal wireframe for integrating the hybrid engine
into the Stage 4 conversation review surface.

## Default DB

When the Stage 4 handler calls `engine.py` **without** `--db`, the engine uses
`SOLBIAN_LIVING_DB` and falls back to the Stage 4 living store:

```text
/Users/archcore/solbian/codex-phase-i-stage4/data/codex_phase_i.sqlite
```

This is the same DB the Stage 4 UI browses, so the Accept path creates a
`WORKING` `codex_document` on the same living store.

## Behaviour

1. **"Synthesize dialogue"** button (default deterministic path):
   - Calls `engine.py` without `--llm`.
   - Creates `PROPOSED` rows linked to the conversation.
   - No Accept happens automatically.
   - Uses the default Stage 4 living DB; refuses to write the historical corpus.

2. **"Draft with LLM"** button/action:
   - Must require an explicit confirmation step or a `?llm=1` query param.
   - Calls `engine.py --llm`.
   - If the LLM endpoint is unreachable, the UI shows the deterministic results
     plus the recorded LLM error; it must not present an empty success.

3. **Review surface** (optional):
   - Left pane: source conversation turns.
   - Middle pane: list of `PROPOSED` candidates with `SOURCE`, `INTERPRETATION`,
     `PROPOSAL`, and `DISCUSSION_TOPIC` labels.
     - Default is quiet: only `hybrid:*` attribution rows, `Theme:*` titles hidden.
     - Add a **Show themes** toggle that calls `list-proposed --themes`.
     - Add a **Show archaeology** toggle that calls `list-proposed --all`.
   - Right pane: existing `WORKING` documents for comparison.
   - Actions: **Accept**, **Edit**, **Reject**, **Defer** per candidate.

## HTML snippet

See `synthesize_button.html` for a copy-pasteable button that can be dropped
into a Stage 4 conversation page.

## Safety rules the UI must enforce

- Never auto-Accept.
- Never set `status = 'CANONICAL'`.
- Never edit the raw Journey messages.
- Never merge law/protocol catalogues in the comparison pane.
- Always show provenance links (source turn IDs) next to each candidate.
- Never call `--db` with a historical corpus path (`~/solbian/codex`); the
  engine will refuse, but the UI should not offer that option.
