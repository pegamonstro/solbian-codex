-- Codex Solbian — Phase I · Stage 5
-- The ONLY table the engine adds to the Stage 3 store (created in the working
-- copy on demand).  Docs only; the engine embeds the same DDL in engine.py.
--
-- analysis_run records one row per analysis kind per engine version.  The id is
-- deterministic (arun_<sha1(kind, engine_version)>) so a re-run updates the same
-- row instead of appending history.  summary_json is a small, inspectable JSON
-- object with the counts/decisions of that pass.
--
-- status is free-form here (RUNNING / OK / ERROR) because it is run bookkeeping,
-- not Codex content.  CANONICAL is never a value.

CREATE TABLE IF NOT EXISTS analysis_run (
    id             TEXT PRIMARY KEY,
    started_at     TEXT NOT NULL,
    finished_at    TEXT,
    kind           TEXT NOT NULL,
    summary_json   TEXT,
    status         TEXT NOT NULL,
    engine_version TEXT,
    attribution    TEXT,
    created_at     TEXT NOT NULL,
    updated_at     TEXT NOT NULL
);
