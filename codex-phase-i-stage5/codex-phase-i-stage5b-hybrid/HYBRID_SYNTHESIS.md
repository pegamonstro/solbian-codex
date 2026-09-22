# Hybrid Synthesis Engine — Design Note

**As-of:** 2026-09-22 · **CANONICAL:** NONE · **Phase II:** HOLD

## What changed

Stage 5 previously produced only shallow deterministic proposals from preserved
Journeys.  This ADMIT-thin slice adds a **hybrid engine** that:

1. Always runs a **deterministic extractor** over a preserved conversation,
   producing `PROPOSED` rows with provenance links back to source `message` IDs.
2. Optionally, with `--llm` / `SOLBIAN_LLM_BASE`, calls an **OpenAI-compatible
   local chat-completion endpoint** (with fallback to Ollama native `/api/chat`)
   to draft a richer synthesis body.  The LLM may only create `PROPOSED` rows; if
   the endpoint is unreachable the engine **fails closed** and records the
   error, never inventing empty success.  If the model returns substantial text
   that is not valid JSON, the engine wraps it as a PROPOSED body behind an
   epistemic fence.
3. Leaves the existing **Accept -> WORKING** path untouched.  `accept` is an
   explicit CLI subcommand (and can be wired to the existing Stage 4/7 UI).
4. Targets the **Stage 4/7 living store** by default:
   - `SOLBIAN_LIVING_DB` overrides the default DB path.
   - `--db` still wins when provided.
   - Refuses to write the historical Mac corpus (`~/solbian/codex`).
   - Warns and refuses if the DB looks like a Stage 3 SoT read-only corpus.
5. Makes `list-proposed` quiet by default:
   - Only rows whose attribution looks like `hybrid:*` are shown.
   - `Theme:*` titles are hidden unless `--themes` or `--verbose`.
   - `--all` includes older Stage-5 archaeology proposals.
   - Hidden-row count is printed in the header.

## What did NOT change

- No auto-Accept.
- No automatic `PROPOSED -> CANONICAL` elevation.
- No write to historical Mac corpus (`~/solbian/codex`).
- No merge of law/protocol catalogues (A/B/B′/C).
- No SEED / GOLEM / Codex Machina / Hermes coupling.
- No vector DB, graph DB, blockchain, or distributed sync.

## Pipeline

```text
Journey (conversation + messages)       read-only source
        ↓
Deterministic extraction                questions, concepts, claims, themes
        ↓
Optional LLM draft                      richer PROPOSED body (only if --llm)
        ↓
PROPOSED codex_document + provenance_link
        ↓
Human review (Stage 4/7)
        ↓
Explicit Accept                         PROPOSED → WORKING
        ↓
Future JD decision                        WORKING → CANONICAL (Phase I: never automatic)
```

## Deterministic extraction

The extractor scans messages for:

- **Durable questions** (`who are we`, `what is`, `should we`, ...)
- **Concepts / definitions** (`X is a kind of ...`, `X means ...`)
- **Normative claims / principles** (`we should ...`, `it is important ...`)
- **Recurring themes** across adjacent turns

Every candidate is labelled with epistemic tags:

- `SOURCE` — verbatim turn text
- `INTERPRETATION` — what the engine thinks the turn expresses
- `PROPOSAL` — candidate Codex content
- `DISCUSSION_TOPIC` — prompt for a future JD↔Solace turn when evidence is thin

## LLM boundary

| Property | Rule |
|---|---|
| Default | OFF (`--llm` required) |
| Endpoint | `SOLBIAN_LLM_BASE` (default `http://localhost:11434/v1`) |
| Fallback | `/api/chat` if `/v1/chat/completions` fails |
| Model | `SOLBIAN_LLM_MODEL` (default `kimi-k2.7-code:cloud`) |
| Mock CI path | `SOLBIAN_LLM_MOCK=1` returns a deterministic PROPOSED draft |
| What LLM can write | Only `status = 'PROPOSED'` + `provenance_link` |
| What LLM cannot write | `WORKING`, `CANONICAL`, raw Journey rows |
| Body requirement | ≥ ~400 characters; one synthesis doc, not dozens |
| JSON tolerance | Fences, nested `synthesis`, `body`/`content`/`text` aliases |
| On failure | Deterministic results still returned; LLM error recorded |
| On unreachable endpoint | Fail closed: no LLM proposal, no empty success |
| On unparseable substantial text | Wrapped as PROPOSED body with epistemic fence |

## Data model (minimal)

Assumes the Mac living store has tables compatible with:

- `conversation(id, external_id, title, created_at)`
- `message(id, conversation_id, role, body/content, created_at)`
- `proposal(id, summary, body, based_on_json, status, attribution, created_at, updated_at)` (Phase I)
- `codex_document(id, title, body, status, provenance, engine, attribution, created_at, updated_at)` (fixture)
- `provenance_link(id, subject_kind/document_id, source_kind/source_type, source_id, ...)`

The smoke fixture creates these tables; the Mac DB may have additional columns.

## CLI

```bash
# Default DB: SOLBIAN_LIVING_DB or Stage 4 living store
python engine.py synthesize-dialogue --conversation conv_5bbf3990a8ce4b47
python engine.py --llm synthesize-dialogue --conversation conv_5bbf3990a8ce4b47

# Explicit DB
python engine.py --db fixtures/who_are_we.sqlite synthesize-dialogue --conversation conv_5bbf3990a8ce4b47
python engine.py --db fixtures/who_are_we.sqlite --llm synthesize-dialogue --conversation conv_5bbf3990a8ce4b47

# Quiet list (hybrid-only, Theme:* hidden)
python engine.py --db fixtures/who_are_we.sqlite list-proposed

# Noisy list
python engine.py --db fixtures/who_are_we.sqlite list-proposed --verbose

python engine.py --db fixtures/who_are_we.sqlite accept --document <ID>
```

## Smoke tests

`smoke_hybrid.py` verifies:

1. Default DB path points at the Stage 4 living store and `SOLBIAN_LIVING_DB`
   can override it.
2. Writes to the historical corpus are refused.
3. Deterministic path creates ≥1 `PROPOSED` from `conv_5bbf3990a8ce4b47`.
4. Explicit Accept moves a `PROPOSED` to `WORKING`.
5. `list-proposed` is quiet by default and flags work.
6. LLM path fails closed when no model is reachable.
7. No `CANONICAL` rows are written.
8. `SOLBIAN_LLM_MOCK=1` produces a hybrid:llm PROPOSED row.
9. `SOLBIAN_LLM_SMOKE=1` runs a live optional LLM test (skipped if unreachable).

## Stage 4 / Stage 7 integration notes

See `stage4_ui/README.md` for a minimal HTML button sketch, `apply_to_stage4.sh`
for copy instructions, and `APPLY_MAC.md` for the Partner install steps.  The
engine is designed to be called from a Stage 4 tab ("Synthesize dialogue") via
the deterministic path; the LLM path requires an explicit confirm or `?llm=1`
query parameter.
