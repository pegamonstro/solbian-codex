-- Codex Solbian Phase I — Stage 3 minimal data layer
-- SQLite DDL. No vector DB, no graph DB, no microservices.
-- Content status enum deliberately excludes CANONICAL (no explicit JD flag exists).
-- Idempotent: safe to re-apply to an existing database.

PRAGMA foreign_keys = ON;

-- ---------------------------------------------------------------------------
-- corpus_root: pointer to a corpus location (read-only; notes only)
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS corpus_root (
    id             TEXT PRIMARY KEY,
    path           TEXT NOT NULL,
    classification TEXT NOT NULL
                   CHECK (classification IN
                          ('CURRENT','HISTORICAL','WORKING','HUB','ARCHIVE','RELATED','UNKNOWN')),
    role           TEXT,
    notes          TEXT,
    status         TEXT NOT NULL DEFAULT 'UNKNOWN'
                   CHECK (status IN
                          ('SOURCE','HISTORICAL','WORKING','PROPOSED','REVISION','RELATED','UNKNOWN')),
    attribution    TEXT,
    created_at     TEXT NOT NULL,
    updated_at     TEXT NOT NULL
);

-- ---------------------------------------------------------------------------
-- source_document: pointer into a corpus root, NOT a copy replacing SoT
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS source_document (
    id               TEXT PRIMARY KEY,
    corpus_root_id   TEXT NOT NULL REFERENCES corpus_root(id),
    rel_path         TEXT NOT NULL,
    media_type       TEXT,
    byte_size        INTEGER,
    mtime            TEXT,
    sha256           TEXT,
    probable_role    TEXT,
    inventory_status TEXT,          -- raw Stage 2 label, preserved verbatim
    status           TEXT NOT NULL DEFAULT 'UNKNOWN'
                     CHECK (status IN
                            ('SOURCE','HISTORICAL','WORKING','PROPOSED','REVISION','RELATED','UNKNOWN')),
    plurality_flags  TEXT,          -- JSON array, e.g. ["law_material"]
    notes            TEXT,
    attribution      TEXT,
    created_at       TEXT NOT NULL,
    updated_at       TEXT NOT NULL,
    UNIQUE (corpus_root_id, rel_path)
);

-- ---------------------------------------------------------------------------
-- conversation / message
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS conversation (
    id           TEXT PRIMARY KEY,
    title        TEXT,
    participants TEXT,              -- JSON array
    status       TEXT NOT NULL DEFAULT 'WORKING'
                 CHECK (status IN
                        ('SOURCE','HISTORICAL','WORKING','PROPOSED','REVISION','RELATED','UNKNOWN')),
    started_at   TEXT,
    notes        TEXT,
    attribution  TEXT,
    created_at   TEXT NOT NULL,
    updated_at   TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS message (
    id              TEXT PRIMARY KEY,
    conversation_id TEXT NOT NULL REFERENCES conversation(id) ON DELETE CASCADE,
    seq             INTEGER NOT NULL,
    role            TEXT CHECK (role IN ('jd','solace','system','other')),
    body            TEXT,
    sent_at         TEXT,
    source_path     TEXT,           -- optional pointer, e.g. week .sref
    status          TEXT NOT NULL DEFAULT 'WORKING'
                    CHECK (status IN
                           ('SOURCE','HISTORICAL','WORKING','PROPOSED','REVISION','RELATED','UNKNOWN')),
    created_at      TEXT NOT NULL,
    updated_at      TEXT NOT NULL,
    UNIQUE (conversation_id, seq)
);

-- ---------------------------------------------------------------------------
-- codex_document: Codex content, WORKING/PROPOSED by default
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS codex_document (
    id                 TEXT PRIMARY KEY,
    kind               TEXT CHECK (kind IN
                           ('chapter','scroll','protocol','law','glossary','section','other')),
    title              TEXT,
    body               TEXT,        -- optional; prefer pointer for large SOURCE
    source_document_id TEXT REFERENCES source_document(id),
    status             TEXT NOT NULL DEFAULT 'WORKING'
                       CHECK (status IN
                              ('SOURCE','HISTORICAL','WORKING','PROPOSED','REVISION','RELATED','UNKNOWN')),
    version            INTEGER NOT NULL DEFAULT 1,
    attribution        TEXT,
    created_at         TEXT NOT NULL,
    updated_at         TEXT NOT NULL
);

-- ---------------------------------------------------------------------------
-- concept
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS concept (
    id          TEXT PRIMARY KEY,
    name        TEXT NOT NULL,
    definition  TEXT,
    status      TEXT NOT NULL DEFAULT 'UNKNOWN'
                CHECK (status IN
                       ('SOURCE','HISTORICAL','WORKING','PROPOSED','REVISION','RELATED','UNKNOWN')),
    notes       TEXT,
    attribution TEXT,
    created_at  TEXT NOT NULL,
    updated_at  TEXT NOT NULL
);

-- ---------------------------------------------------------------------------
-- relationship: plain edge rows (no graph engine)
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS relationship (
    id         TEXT PRIMARY KEY,
    from_id    TEXT NOT NULL,
    from_kind  TEXT NOT NULL,
    to_id      TEXT NOT NULL,
    to_kind    TEXT NOT NULL,
    rel_type   TEXT NOT NULL,
    confidence TEXT CHECK (confidence IN
                           ('TEXT-SUPPORTED','TITLE-LEVEL','SYNTHESIS','UNKNOWN')),
    status     TEXT NOT NULL DEFAULT 'UNKNOWN'
               CHECK (status IN
                      ('SOURCE','HISTORICAL','WORKING','PROPOSED','REVISION','RELATED','UNKNOWN')),
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

-- ---------------------------------------------------------------------------
-- proposal
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS proposal (
    id            TEXT PRIMARY KEY,
    summary       TEXT NOT NULL,
    body          TEXT,
    based_on_json TEXT,             -- JSON array of provenance/proposal ids
    status        TEXT NOT NULL DEFAULT 'PROPOSED'
                  CHECK (status IN
                         ('SOURCE','HISTORICAL','WORKING','PROPOSED','REVISION','RELATED','UNKNOWN')),
    attribution   TEXT,
    created_at    TEXT NOT NULL,
    updated_at    TEXT NOT NULL
);

-- ---------------------------------------------------------------------------
-- revision: append-only; never rewrites target content in place
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS revision (
    id           TEXT PRIMARY KEY,
    target_kind  TEXT,
    target_id    TEXT,
    proposal_id  TEXT REFERENCES proposal(id),
    prev_version INTEGER,
    next_version INTEGER,
    diff_summary TEXT,
    status       TEXT NOT NULL DEFAULT 'REVISION'
                 CHECK (status IN
                        ('SOURCE','HISTORICAL','WORKING','PROPOSED','REVISION','RELATED','UNKNOWN')),
    reversible   INTEGER NOT NULL DEFAULT 1,
    created_at   TEXT NOT NULL,
    updated_at   TEXT NOT NULL
);

-- ---------------------------------------------------------------------------
-- provenance_link
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS provenance_link (
    id           TEXT PRIMARY KEY,
    subject_kind TEXT NOT NULL,
    subject_id   TEXT NOT NULL,
    source_kind  TEXT NOT NULL
                 CHECK (source_kind IN
                        ('message','source_document','conversation','external','unknown')),
    source_id    TEXT,
    note         TEXT,
    confidence   TEXT CHECK (confidence IN
                             ('TEXT-SUPPORTED','TITLE-LEVEL','SYNTHESIS','UNKNOWN')),
    status       TEXT NOT NULL DEFAULT 'UNKNOWN'
                 CHECK (status IN
                        ('SOURCE','HISTORICAL','WORKING','PROPOSED','REVISION','RELATED','UNKNOWN')),
    created_at   TEXT NOT NULL,
    updated_at   TEXT NOT NULL
);

-- ---------------------------------------------------------------------------
-- Indexes
-- ---------------------------------------------------------------------------
CREATE INDEX IF NOT EXISTS idx_source_document_status
    ON source_document(status);
CREATE INDEX IF NOT EXISTS idx_codex_document_kind_status
    ON codex_document(kind, status);
CREATE INDEX IF NOT EXISTS idx_message_conversation_seq
    ON message(conversation_id, seq);
CREATE INDEX IF NOT EXISTS idx_provenance_subject
    ON provenance_link(subject_kind, subject_id);
CREATE INDEX IF NOT EXISTS idx_provenance_source
    ON provenance_link(source_kind, source_id);
CREATE INDEX IF NOT EXISTS idx_relationship_endpoints
    ON relationship(from_id, to_id);
