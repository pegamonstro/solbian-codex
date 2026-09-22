# DSH Result — Hybrid Slice Polish

**STATUS:** COMPLETE  
**Model used:** `kimi-k2.7-code:cloud` (via Ollama for optional LLM draft verification)  
**As-of:** 2026-09-22  
**CANONICAL:** NONE

## Files read

- `/home/igor/work/hybrid-slice-polish-2026-09-22/00_POLISH_BRIEF.md`
- `/home/igor/work/hybrid-slice-polish-2026-09-22/inputs/codex-phase-i-stage5b-hybrid/README.md`
- `/home/igor/work/hybrid-slice-polish-2026-09-22/inputs/codex-phase-i-stage5b-hybrid/HYBRID_SYNTHESIS.md`
- `/home/igor/work/hybrid-slice-polish-2026-09-22/inputs/codex-phase-i-stage5b-hybrid/codex_hybrid/*.py`
- `/home/igor/work/hybrid-slice-polish-2026-09-22/inputs/codex-phase-i-stage5b-hybrid/engine.py`
- `/home/igor/work/hybrid-slice-polish-2026-09-22/inputs/codex-phase-i-stage5b-hybrid/smoke_hybrid.py`

## Files written

Portable package under `/home/igor/work/hybrid-slice-polish-2026-09-22/codex-phase-i-stage5b-hybrid/`:

| File | Purpose |
|---|---|
| `README.md` | Quick-start, default DB, quiet list, mock LLM, guardrails |
| `HYBRID_SYNTHESIS.md` | Design note: deterministic + optional LLM + safety + quiet list |
| `APPLY_MAC.md` | Concise Partner install/apply steps for Mac |
| `requirements.txt` | Standard-library-only note |
| `engine.py` | CLI: default DB, `--db` optional, `list-proposed` filters |
| `smoke_hybrid.py` | Smoke tests: wiring, guards, quiet list, mock LLM, fail-closed |
| `codex_hybrid/config.py` | Runtime config + `SOLBIAN_LIVING_DB` default + historical corpus paths |
| `codex_hybrid/db.py` | Dual-schema wrapper + safety guards + filtered `list_proposed_documents` |
| `codex_hybrid/extract.py` | Deterministic extractor (questions, concepts, claims, themes) |
| `codex_hybrid/llm_client.py` | OpenAI-compatible client + `/api/chat` fallback + tolerant JSON + text fallback + mock |
| `codex_hybrid/synthesis.py` | Hybrid runner |
| `fixtures/who_are_we.json` | Sample "Who are we?" conversation (15 msgs) |
| `fixtures/build_fixture_db.py` | Build `who_are_we.sqlite` from JSON |
| `fixtures/who_are_we.sqlite` | Generated fixture DB |
| `install_to_mac.sh` | Exact Mac Stage 5 install instructions |
| `apply_to_stage4.sh` | Stage 4 UI hook instructions (default DB, deterministic + LLM buttons) |
| `stage4_ui/README.md` | Integration behaviour + safety rules + quiet list toggle guidance |
| `stage4_ui/synthesize_button.html` | Copy-pasteable button wireframe |

## Smoke results

```text
[SMOKE] default living DB path              PASS
[SMOKE] refuse writes to historical corpus  PASS
[SMOKE] deterministic path                  PASS
[SMOKE] explicit Accept path                PASS
[SMOKE] quiet list-proposed hides Theme:*   PASS
[SMOKE] list-proposed flags                 PASS
[SMOKE] LLM fail-closed path                PASS
[SMOKE] no CANONICAL writes                 PASS
[SMOKE] mock LLM path                       PASS
[SMOKE] optional live LLM                   PASS (skipped by default)
OVERALL: PASS
```

Optional mock-LLM smoke produced a non-empty `hybrid:llm` PROPOSED document.
Live LLM smoke is skipped when `SOLBIAN_LLM_SMOKE` is unset; when set and a
reachable Ollama endpoint exists it will verify a real `hybrid:llm` draft.

## Self-check against 00_POLISH_BRIEF hard rules

- [x] No auto-Accept: `accept` is a separate explicit CLI action.
- [x] No CANONICAL writes: engine never inserts/updates `status = 'CANONICAL'`.
- [x] Deterministic analyzers remain default baseline.
- [x] LLM draft mode is optional and OFF by default (`--llm` / `SOLBIAN_LLM_BASE`).
- [x] LLM only creates/updates `PROPOSED` rows + provenance links.
- [x] No write to Mac historical corpus; writes target the Stage 4/7 living SQLite store.
- [x] Default DB path wired to Stage 4 living store; `SOLBIAN_LIVING_DB` and `--db` both work.
- [x] Accept path creates a WORKING `codex_document` on the same living DB.
- [x] `list-proposed` is quiet by default (hybrid-only, Theme:* hidden, hidden count shown).
- [x] LLM client hardened: `/v1/chat/completions` + `/api/chat` fallback, tolerant JSON, text fallback.
- [x] No SEED/GOLEM/Machina/vector/graph/blockchain introduced.
- [x] `install_to_mac.sh`, `apply_to_stage4.sh`, and `APPLY_MAC.md` provide Mac Partner steps.
- [x] `DSH_RESULT.md` contains status and token `HYBRID_SLICE_POLISH_OK`.

## Token

`HYBRID_SLICE_POLISH_OK`
