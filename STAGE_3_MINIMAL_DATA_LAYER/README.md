# Codex Solbian Phase I — Stage 3 Minimal Data Layer

Smallest durable storage model for Phase I: conversations + messages, source-material
pointers into the historical corpus, Codex content documents, proposals, revisions and
provenance links. **SQLite + Python stdlib only.** No vector DB, no graph DB, no
microservices, no SEED/GOLEM/Machina coupling, no `CANONICAL` invented.

**CANONICAL: NONE.** The historical SoT remains Mac `/Users/archcore/solbian/codex`
(`source_original/` + full MD scrolls). This store holds *pointers*, never replacements,
and never writes to that tree.

## Files

| File | Purpose |
| --- | --- |
| `SCHEMA.md` | Implemented schema (human-readable). |
| `schema.sql` | Executable SQLite DDL (source of truth). |
| `codex_phase_i.sqlite` | The store (created by `ingest_baseline.py`). |
| `ingest_baseline.py` | Read-only baseline ingest: roots + inventory sample. |
| `smoke_test.py` | Self-contained test; exits 0 on success. |
| `baseline_inventory_sample.json` | Stage 2 inventory sample (read-only input). |
| `DSH_RESULT.md` | Run result, what changed, deviations. |

## Quick start

```bash
cd /Users/archcore/solbian/codex-phase-i-stage3

# 1. Create / refresh the store from the DDL and the sample inventory.
python3 ingest_baseline.py

# 2. Verify (must exit 0).
python3 smoke_test.py
```

`ingest_baseline.py` flags:

```bash
python3 ingest_baseline.py --no-sha256     # never open corpus files
python3 ingest_baseline.py --db other.sqlite --json other.json
```

Re-running the ingest is idempotent: deterministic ids plus
`UNIQUE(corpus_root_id, rel_path)` upserts keep row counts stable.

## What the ingest does

1. Applies `schema.sql` (idempotent) to `codex_phase_i.sqlite`.
2. Registers the **primary Mac path** `/Users/archcore/solbian/codex` as
   `classification=CURRENT`, `role=PRIMARY_HISTORICAL_WORKING_TREE`, with notes recording
   that the historical SoT lives inside it (`source_original/` + full MD scrolls), that
   GH `main` tip is *not* historical, and that the tree is never modified. Also registers
   the other Stage 2 candidate roots (Box mirror, GH hub, Working synthesis, Helios, Gitea).
3. Reads only `baseline_inventory_sample.json` and inserts one `source_document` row per
   sample entry, pointing at the corpus. The raw Stage 2 status label is preserved verbatim
   in `inventory_status`; the mapped enum value goes in `status`.
4. Sets `plurality_flags` (JSON array) where roles/paths mention laws, protocols or scrolls —
   e.g. `law_material`, `protocol_material`, `scroll_material`, `sref_artefact`.
5. Optionally computes each file's sha256 by opening it **read-only** (`open(path, "rb")`);
   `--no-sha256` skips all corpus reads.

### Read-only guarantee

The script contains no write/move/delete/chmod call against any corpus path. Its only
corpus access is `open(..., "rb")` inside `sha256_readonly()`.

## Inspecting the store

```bash
sqlite3 codex_phase_i.sqlite ".tables"
sqlite3 codex_phase_i.sqlite "SELECT path, classification, role FROM corpus_root;"
sqlite3 codex_phase_i.sqlite \
  "SELECT rel_path, status, plurality_flags FROM source_document WHERE plurality_flags != '[]';"
```

## Status enum

`SOURCE` | `HISTORICAL` | `WORKING` | `PROPOSED` | `REVISION` | `RELATED` | `UNKNOWN`

`CANONICAL` is deliberately absent. `CHECK` constraints reject any attempt to store it.
Codex content defaults to `WORKING`; proposals default to `PROPOSED`.

## Out of scope (Stage 4+)

UI, Solace chat, engine synthesis, LLM calls inside the store.
