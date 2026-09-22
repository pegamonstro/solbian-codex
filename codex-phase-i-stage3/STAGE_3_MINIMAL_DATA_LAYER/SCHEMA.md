# Stage 3 — Proposed minimal schema (SQLite)

## Tables

### corpus_root
- id TEXT PK
- path TEXT NOT NULL
- classification TEXT NOT NULL  -- CURRENT|HISTORICAL|WORKING|HUB|ARCHIVE|RELATED|UNKNOWN
- role TEXT
- notes TEXT
- recorded_at TEXT NOT NULL

### source_document
- id TEXT PK
- corpus_root_id TEXT FK → corpus_root
- rel_path TEXT NOT NULL
- media_type TEXT
- byte_size INTEGER
- mtime TEXT
- sha256 TEXT
- probable_role TEXT
- status TEXT NOT NULL  -- SOURCE|HISTORICAL|RELATED|UNKNOWN|…
- plurality_flags TEXT  -- JSON array e.g. ["law_catalogue_B","mac_only_protocol"]
- notes TEXT

### conversation
- id TEXT PK
- title TEXT
- participants TEXT  -- JSON
- status TEXT NOT NULL  -- SOURCE|WORKING|…
- started_at TEXT
- notes TEXT

### message
- id TEXT PK
- conversation_id TEXT FK
- seq INTEGER
- role TEXT  -- jd|solace|system|other
- body TEXT
- created_at TEXT
- source_path TEXT  -- optional pointer to week .sref etc.
- status TEXT NOT NULL

### codex_document
- id TEXT PK
- kind TEXT  -- chapter|scroll|protocol|law|glossary|section|other
- title TEXT
- body TEXT  -- optional; prefer pointer for large SOURCE
- source_document_id TEXT FK NULL
- status TEXT NOT NULL  -- default WORKING or SOURCE
- version INTEGER NOT NULL DEFAULT 1

### concept
- id TEXT PK
- name TEXT NOT NULL
- definition TEXT
- status TEXT NOT NULL
- notes TEXT

### relationship
- id TEXT PK
- from_id TEXT NOT NULL
- from_kind TEXT NOT NULL
- to_id TEXT NOT NULL
- to_kind TEXT NOT NULL
- rel_type TEXT NOT NULL
- confidence TEXT  -- TEXT-SUPPORTED|TITLE-LEVEL|SYNTHESIS|UNKNOWN
- status TEXT NOT NULL

### proposal
- id TEXT PK
- summary TEXT NOT NULL
- body TEXT
- based_on_json TEXT  -- provenance ids
- status TEXT NOT NULL  -- PROPOSED
- created_at TEXT

### revision
- id TEXT PK
- target_kind TEXT
- target_id TEXT
- proposal_id TEXT FK NULL
- prev_version INTEGER
- next_version INTEGER
- diff_summary TEXT
- status TEXT NOT NULL
- created_at TEXT
- reversible INTEGER NOT NULL DEFAULT 1

### provenance_link
- id TEXT PK
- subject_kind TEXT NOT NULL
- subject_id TEXT NOT NULL
- source_kind TEXT NOT NULL  -- message|source_document|conversation|external|unknown
- source_id TEXT
- note TEXT
- confidence TEXT

## Indexes
- source_document(corpus_root_id, rel_path) UNIQUE
- message(conversation_id, seq)
- provenance_link(subject_kind, subject_id)
