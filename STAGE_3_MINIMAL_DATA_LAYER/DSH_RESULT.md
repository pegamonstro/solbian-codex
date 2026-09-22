# DSH_RESULT — Codex Solbian Phase I, Stage 3 Minimal Data Layer

**STATUS: COMPLETE**

**As-of:** 2026-09-20 · **CANONICAL: NONE**
**Scope:** implemented entirely under `/Users/archcore/solbian/codex-phase-i-stage3`.

## What changed (files written)

| File | Change |
| --- | --- |
| `SCHEMA.md` | Finalized the implemented schema: added `created_at`/`updated_at` to every table (brief constraint 6), added `attribution` where content applies, added `status` + enum `CHECK` constraints (no `CANONICAL`), added `source_document.inventory_status` to preserve the raw Stage 2 label verbatim, added `message.sent_at` to separate authored time from row time, and documented indexes/plurality preservation. |
| `schema.sql` | New. Executable SQLite DDL for all 10 tables + indexes. Idempotent (`IF NOT EXISTS`), `PRAGMA foreign_keys = ON`, `CHECK` constraints on every `status`, classification, confidence and provenance `source_kind`. |
| `codex_phase_i.sqlite` | New. Created by applying `schema.sql` during `ingest_baseline.py`. Contains 6 `corpus_root` rows and 80 `source_document` rows; all other tables empty and ready. |
| `ingest_baseline.py` | New. Read-only ingest (see below). |
| `smoke_test.py` | New. Self-contained test on a throwaway DB; read-only inspection of the shipped DB. |
| `README.md` | New. Run instructions, read-only guarantee, inspection queries. |
| `DSH_RESULT.md` | New. This file. |

Nothing under `/Users/archcore/solbian/codex` (or any other corpus) was modified.
The nested `STAGE_3_MINIMAL_DATA_LAYER/` directory shipped with the task is an input
copy and was left untouched.

## `ingest_baseline.py` behavior

- Applies `schema.sql` to `codex_phase_i.sqlite` (idempotent).
- Registers **PRIMARY Mac path** `/Users/archcore/solbian/codex` as
  `classification=CURRENT`, `role=PRIMARY_HISTORICAL_WORKING_TREE`, notes-only. Notes
  record that the historical SoT lives inside this tree (`source_original/` + full MD
  scrolls), that GH `main` tip is *not* historical, and that the tree is never written.
- Registers the other five Stage 2 candidate roots: Box mirror (`ARCHIVE`), GH remote
  (`HUB`), Working synthesis (`HISTORICAL`), Helios (`UNKNOWN`), Gitea (`HISTORICAL`).
- Reads **only** `baseline_inventory_sample.json` and inserts one `source_document` row
  per sample entry (80 rows). Raw Stage 2 status is preserved in `inventory_status`;
  the mapped enum value goes in `status`. No corpus content is copied or rewritten.
- Sets `plurality_flags` where roles/paths mention laws, protocols or scrolls.
- Optionally computes sha256 by opening referenced files **read-only** (`open(path,"rb")`);
  `--no-sha256` disables all corpus reads. All 35 file entries hashed successfully.
- Idempotent: re-running left counts at 6 roots / 80 documents.

### Ingest stdout (as run)

```
db                 : /Users/archcore/solbian/codex-phase-i-stage3/codex_phase_i.sqlite
schema applied     : /Users/archcore/solbian/codex-phase-i-stage3/schema.sql
inventory json     : /Users/archcore/solbian/codex-phase-i-stage3/baseline_inventory_sample.json
roots registered   : 6
source_documents   : 80 (from 80 sample entries; sha256 computed=35)
plurality flag use : {"law_material": 7, "protocol_material": 1, "scroll_material": 31, "sref_artefact": 29}
table counts       : {"codex_document": 0, "concept": 0, "conversation": 0, "corpus_root": 6, "message": 0, "proposal": 0, "provenance_link": 0, "relationship": 0, "revision": 0, "source_document": 80}
```

Plurality flags observed: `law_material` (7, from `source_original/legal` and related),
`protocol_material` (1, `source_original/protocols`), `scroll_material` (31),
`sref_artefact` (29). The named-variant flags (`law_catalogue_A/B/Bprime/C`,
`protocol_catalogue_gitea5`, `scroll_md_vs_sref_ordinals`, `scroll_20_anomaly`) are
emitted only when a label explicitly names them; the sample inventory does not, so none
were fabricated.

## Verification

Command:

```bash
python3 smoke_test.py
```

Result: **exit 0**. stdout below, stderr empty.

### Smoke stdout

```
== Stage 3 smoke test ==
schema      : /Users/archcore/solbian/codex-phase-i-stage3/schema.sql
scratch db  : /var/folders/sh/sg28hf0s1nl0p_8y5h28l02c0000gn/T/stage3_smoke_xfjpupw_/smoke.sqlite

[1] schema
  ok  table exists: corpus_root
  ok  table exists: source_document
  ok  table exists: conversation
  ok  table exists: message
  ok  table exists: codex_document
  ok  table exists: concept
  ok  table exists: relationship
  ok  table exists: proposal
  ok  table exists: revision
  ok  table exists: provenance_link
  ok  status enum excludes CANONICAL
  ok  no CHECK constraint admits a CANONICAL value

[2] corpus root + source pointer

[3] conversation + messages

[4] codex document

[5] proposal + revision

[6] provenance links

[7] round-trip queries
  ok  conversation round-trips
  ok  messages round-trip in seq order
  ok  conversation->message join returns 2 rows
  ok  proposal->provenance join round-trips
  ok  both provenance subjects present

[8] invariants
  ok  foreign_key_check clean
  ok  source_document root+rel_path unique
  ok  codex_document defaults WORKING
  ok  CHECK rejects invented CANONICAL status

[9] shipped database (read-only)
  ok  shipped DB has all tables (/Users/archcore/solbian/codex-phase-i-stage3/codex_phase_i.sqlite)
  --  shipped row counts: {'corpus_root': 6, 'source_document': 80, 'conversation': 0, 'message': 0, 'codex_document': 0, 'concept': 0, 'relationship': 0, 'proposal': 0, 'revision': 0, 'provenance_link': 0}

SMOKE TEST PASSED
```

### Smoke stderr

```
(empty)
```

## Acceptance check

- [x] Smoke test exits 0.
- [x] Original Mac corpus untouched — ingest only opens files `"rb"`; DB stores pointers only.
- [x] No catalogue merge logic anywhere.
- [x] No vector/graph DB, microservices, or SEED/GOLEM/Machina coupling; Python stdlib + `sqlite3` only.
- [x] No `CANONICAL` value invented (`CHECK` constraints reject it; smoke test asserts this).
- [x] Plurality preserved as `status` / `plurality_flags` / verbatim `inventory_status`.

## Deviations & limitations

1. **Schema additions beyond `SCHEMA.md` draft (intentional):** `created_at`/`updated_at`
   on every table, `attribution` fields, enum `CHECK` constraints, `inventory_status`,
   and `message.sent_at`. These implement brief constraint 6 without adding new concepts.
2. **`classification='CURRENT'`.** The brief said "CURRENT/HISTORICAL"; the classification
   column is single-valued, so the CURRENT live path value was used and the HISTORICAL SoT
   role is recorded in `role` + `notes` (and the enum constraint is respected).
3. **Sample only.** The inventory JSON exposes `entries_sample` (80 of `entry_count` 966);
   only those 80 are ingested. The full 966-entry inventory can be ingested later by
   pointing `--json` at the complete file — no schema change needed.
4. **sha256 is best-effort.** Hashes were computed for the 35 sample file entries that
   exist under the Mac path at ingest time; directories and missing paths stay NULL.
5. **`relationship` table is plain rows**, not a graph engine — present for the schema but
   unused by the sample ingest (out-of-scope data not fabricated).

**Remainder:** none required for Stage 3 acceptance. Stage 4+ (UI, Solace chat, engine
synthesis, LLM calls) is explicitly out of scope.
