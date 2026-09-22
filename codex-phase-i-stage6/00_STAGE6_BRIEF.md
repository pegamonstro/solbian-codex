# Phase I — Stage 6 Historical Validation (+ optional Stage 4 Engine tab)
**As-of:** 2026-09-21 · **CANONICAL:** NONE  
**Authority:** SPEC 12 + Stages 2–5 artefacts on Mac

## A. Historical Validation suite
Cwd: `/Users/archcore/solbian/codex-phase-i-stage6/`

Build `validate_historical.py` (+ helpers) that proves against the **existing corpus / stores** (read-only on Mac historical tree):

### Baseline tests (SPEC 12)
1. **Ingest coverage** — Stage 3/5 DB has substantial `source_document` count (≥900); sample of known paths from Stage 2 inventory exist as rows (chapters, scrolls, protocols, laws).
2. **Preserve sources** — Stage 3 SoT sqlite sha256 stable across validation; Mac `/Users/archcore/solbian/codex/source_original` fingerprint (file count + sample hashes) unchanged by validation run.
3. **Represent without substantial loss** — compare inventory entry_count (966) vs DB rows; report gap; assert gap explained (duplicates) not silent drop of unique rel_paths for PRIMARY root.
4. **Visible structure** — DB contains documents under expected role/path prefixes: chapters, scrolls, protocols, legal/laws, glossary, personae (at least presence checks).
5. **Historical distinctions preserved** — plurality_flags still present for law/protocol/scroll/scroll_20; A/B/B′/C not collapsed; protocol 01–08 not reduced to 5.
6. **Provenance exposed** — Stage 5 working DB has proposals with provenance_link; ≥1 link resolves to source_document.
7. **No silent content change** — engine dry-run / validation never writes Stage 3 SoT or Mac corpus.

### Engine tests
- Re-run Stage 5 `engine.py run` on a **throwaway copy** of Stage 5 data DB: proposal counts stable (idempotent).
- Duplicate detector finds known duplicate basenames (e.g. readme.md).
- Failure handling: refuse `--db` under Mac corpus path.
- Optional: if personae week `.sref` readable, ingest 1–3 messages into throwaway conversation and confirm durable analyzer produces INTERPRETATION proposal (or skip with reason).

### Deliverables
- `validate_historical.py` — exit 0 on PASS
- `VALIDATION_REPORT.md` — human summary of each check PASS/FAIL + numbers
- `smoke_stage6.py` — wraps validate + asserts
- `README.md`, `DSH_RESULT.md`

## B. Optional — Stage 4 Engine/Proposals admin tab
Extend `/Users/archcore/solbian/codex-phase-i-stage4/` carefully:
- Third tab **Engine** (or admin): list proposals from Stage 5 working DB (`…/codex-phase-i-stage5/data/codex_phase_i.sqlite`) **read-only** by default; show detail + provenance.
- Optional button “Run engine (dry-run)” that shells to Stage 5 with `--dry-run` and shows stdout — must not elevate CANONICAL; must not write historical corpus.
- Wire Stage 4 app to open Stage 5 DB read-only for proposals (path configurable).
- Re-run `python3 smoke_ui.py` must still exit 0; add a few Engine-tab checks to smoke or `smoke_ui_engine.py`.
- Do not break Solace/Codex tabs.

## Hard rules
- CANONICAL: NONE; no catalogue merges; no Mac corpus writes; Stage 3 SoT read-only.
- Prefer stdlib.

## Acceptance
- `python3 smoke_stage6.py` exit 0
- Stage 4 smoke still exit 0 after Engine tab
