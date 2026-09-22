# Stage 3 — Implemented minimal schema (SQLite)

**As-of:** 2026-09-20 · **CANONICAL:** NONE
**Store:** `codex_phase_i.sqlite` (single file, inspectable, backup-friendly)
**Rule:** smallest durable store. Pointers into the historical corpus — never copies that replace SoT.
No vector DB, no graph DB, no microservices, no SEED/GOLEM/Machina coupling.

This file is the implemented schema; `schema.sql` is the executable DDL and is the
source of truth if the two ever disagree.

## Enumerations

- **content status** (`status`, every table):
  `SOURCE` | `HISTORICAL` | `WORKING` | `PROPOSED` | `REVISION` | `RELATED` | `UNKNOWN`
  — `CANONICAL` is deliberately **absent** (no explicit JD flag exists; default is absent).
- **corpus classification**: `CURRENT` | `HISTORICAL` | `WORKING` | `HUB` | `ARCHIVE` | `RELATED` | `UNKNOWN`
- **provenance confidence**: `TEXT-SUPPORTED` | `TITLE-LEVEL` | `SYNTHESIS` | `UNKNOWN`
- **provenance source_kind**: `message` | `source_document` | `conversation` | `external` | `unknown`

Every row carries `id`, `created_at`, `updated_at` and a `status` from the content
status enum. `attribution` is present where content/claims apply. `source_document.inventory_status`
preserves the raw Stage 2 inventory label verbatim so ingestion never silently flattens it.

## Tables

### corpus_root
Pointer to a corpus location. Notes/classification only; the store never writes to it.
- `id` TEXT PK
- `path` TEXT NOT NULL
- `classification` TEXT NOT NULL — enum above
- `role` TEXT — e.g. `PRIMARY_HISTORICAL_WORKING_TREE`
- `notes` TEXT — free text preservation of provenance caveats
- `status` TEXT NOT NULL — content status enum
- `attribution` TEXT
- `created_at` TEXT NOT NULL
- `updated_at` TEXT NOT NULL

### source_document
A pointer into a corpus root (NOT a replacement for SoT).
- `id` TEXT PK
- `corpus_root_id` TEXT NOT NULL FK → corpus_root(id)
- `rel_path` TEXT NOT NULL — path relative to the corpus root
- `media_type` TEXT
- `byte_size` INTEGER
- `mtime` TEXT
- `sha256` TEXT — NULL unless a read-only hash was computed
- `probable_role` TEXT
- `inventory_status` TEXT — raw Stage 2 status label, verbatim
- `status` TEXT NOT NULL — content status enum (mapped; raw kept above)
- `plurality_flags` TEXT — JSON array, e.g. `["law_material","protocol_material"]`
- `notes` TEXT
- `attribution` TEXT
- `created_at` TEXT NOT NULL
- `updated_at` TEXT NOT NULL
- UNIQUE (`corpus_root_id`, `rel_path`)

### conversation
- `id` TEXT PK
- `title` TEXT
- `participants` TEXT — JSON array
- `status` TEXT NOT NULL — default `WORKING`
- `started_at` TEXT
- `notes` TEXT
- `attribution` TEXT
- `created_at` TEXT NOT NULL
- `updated_at` TEXT NOT NULL

### message
- `id` TEXT PK
- `conversation_id` TEXT NOT NULL FK → conversation(id) ON DELETE CASCADE
- `seq` INTEGER NOT NULL
- `role` TEXT — `jd` | `solace` | `system` | `other`
- `body` TEXT
- `sent_at` TEXT — when the message was authored (row `created_at` is DB insert time)
- `source_path` TEXT — optional pointer to a week `.sref` etc.
- `status` TEXT NOT NULL
- `created_at` TEXT NOT NULL
- `updated_at` TEXT NOT NULL
- UNIQUE (`conversation_id`, `seq`)

### codex_document
Codex content; `WORKING`/`PROPOSED` by default. Prefer pointer for large `SOURCE`.
- `id` TEXT PK
- `kind` TEXT — `chapter`|`scroll`|`protocol`|`law`|`glossary`|`section`|`other`
- `title` TEXT
- `body` TEXT
- `source_document_id` TEXT NULL FK → source_document(id)
- `status` TEXT NOT NULL — default `WORKING`
- `version` INTEGER NOT NULL DEFAULT 1
- `attribution` TEXT
- `created_at` TEXT NOT NULL
- `updated_at` TEXT NOT NULL

### concept
- `id` TEXT PK
- `name` TEXT NOT NULL
- `definition` TEXT
- `status` TEXT NOT NULL
- `notes` TEXT
- `attribution` TEXT
- `created_at` TEXT NOT NULL
- `updated_at` TEXT NOT NULL

### relationship
Generic, non-graph-DB edge table (plain rows, no graph engine).
- `id` TEXT PK
- `from_id` TEXT NOT NULL
- `from_kind` TEXT NOT NULL
- `to_id` TEXT NOT NULL
- `to_kind` TEXT NOT NULL
- `rel_type` TEXT NOT NULL
- `confidence` TEXT — enum above
- `status` TEXT NOT NULL
- `created_at` TEXT NOT NULL
- `updated_at` TEXT NOT NULL

### proposal
- `id` TEXT PK
- `summary` TEXT NOT NULL
- `body` TEXT
- `based_on_json` TEXT — JSON array of provenance/proposal ids
- `status` TEXT NOT NULL — default `PROPOSED`
- `attribution` TEXT
- `created_at` TEXT NOT NULL
- `updated_at` TEXT NOT NULL

### revision
Append-only record of a proposed/applied change; never rewrites target text in place.
- `id` TEXT PK
- `target_kind` TEXT
- `target_id` TEXT
- `proposal_id` TEXT NULL FK → proposal(id)
- `prev_version` INTEGER
- `next_version` INTEGER
- `diff_summary` TEXT
- `status` TEXT NOT NULL
- `reversible` INTEGER NOT NULL DEFAULT 1
- `created_at` TEXT NOT NULL
- `updated_at` TEXT NOT NULL

### provenance_link
Why a stored artifact is believed; links subjects to sources.
- `id` TEXT PK
- `subject_kind` TEXT NOT NULL
- `subject_id` TEXT NOT NULL
- `source_kind` TEXT NOT NULL — enum above
- `source_id` TEXT
- `note` TEXT
- `confidence` TEXT
- `status` TEXT NOT NULL
- `created_at` TEXT NOT NULL
- `updated_at` TEXT NOT NULL

## Indexes
- `source_document(corpus_root_id, rel_path)` UNIQUE
- `source_document(status)`
- `message(conversation_id, seq)` UNIQUE
- `provenance_link(subject_kind, subject_id)`
- `provenance_link(source_kind, source_id)`
- `codex_document(kind, status)`
- `relationship(from_id, to_id)`

## Plurality preservation
Wave5 Working fences are `WORKING` metadata, not source `CANONICAL`. Catalogue
plurality (Law A/B/B′/C, Protocols 01–08 vs Gitea-5, scroll MD ≠ sref ordinals,
scroll 20 anomaly) is carried as `status` / `plurality_flags` / `notes`, never
flattened and never merged. No `CANONICAL` value is invented.
