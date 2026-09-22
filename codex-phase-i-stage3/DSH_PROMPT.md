# Task: Codex Solbian Phase I — Stage 3 Minimal Data Layer

Read `00_STAGE3_BRIEF.md` and `SCHEMA.md` in this cwd. Obey them strictly.

## Implement here (this cwd only)
1. Finalize `SCHEMA.md` if you improve it (keep simple).
2. Write `schema.sql` DDL for SQLite.
3. Create `codex_phase_i.sqlite` by applying DDL.
4. Write `ingest_baseline.py` that:
   - registers corpus_root for PRIMARY Mac path `/Users/archcore/solbian/codex` as CURRENT/HISTORICAL (notes only; do not modify that tree)
   - loads `baseline_inventory_sample.json` and inserts source_document rows (READ sample JSON only; optional READ of Mac paths for sha256 if easy — never WRITE Mac)
   - sets plurality_flags where roles mention laws/protocols/scrolls as appropriate
5. Write `smoke_test.py` that creates a sample conversation+messages, a proposal, a provenance_link, runs asserts, exits 0.
6. Write `README.md` with run instructions.
7. Write `DSH_RESULT.md` with STATUS COMPLETE/INCOMPLETE, what changed, smoke output.

## Forbidden
- Modify `/Users/archcore/solbian/codex` or any historical corpus
- Vector/graph DBs, microservices, SEED/GOLEM/Machina coupling
- Catalogue merges / inventing CANONICAL
- Silent rewriting of Codex content

## Verify
```bash
python3 smoke_test.py
```
must exit 0. Put smoke stdout/stderr into DSH_RESULT.md.

Prefer Python stdlib + sqlite3 only.
