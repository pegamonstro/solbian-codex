# Codex ↔ S.E.E.D. Integration
DOC_VERSION: 0.3.0
DATE: 2025-10-25

## Scope
- Align Codex structures with S.E.E.D. **MAP-C/MAP-S**
- Use `schema/*.json` as contract for ingestion (mem.a / PMM)
- Embrace journaling: `manifest/index.sref` and `journal/*.sref`

## Touchpoints
- **seed-0.2.x (deployed):** memory vault, router, seedbus, observability
- **seed-0.3 (dev):** PMM, SREF v5, LLM runner hooks, Solace hooks
- **seed-0.4 (dev):** modular build, LISP interop exploration

## Export/Import
- NDJSON streams, 1 object per line
- Bloom/dedup recommended in ingestion
