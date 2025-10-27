# Memory Blockchain — Draft Spec
DOC_VERSION: 0.3.0
DATE: 2025-10-25
STATUS: research

## Intent
Provide **immutability and provenance** for symbolic memories using a lightweight chain-of-hashes,
compatible with S.E.E.D.'s memory vaults and append-only journals.

## Core
- Append-only NDJSON records (SREF envelopes) with ``prev_hash`` and ``content_hash``
- Periodic anchors (e.g., Merkle roots or external timestamps)
- Compatibility with **MAP-S** for symbolic overlays

## Minimal Record
```json
{
  "_id": "blk-...",
  "_type": "mem_block",
  "_version": "1.0.0",
  "_ts": "ISO-8601",
  "tags": ["codex","memchain"],
  "body": {
    "height": 42,
    "prev_hash": "hex",
    "content_hash": "hex",
    "payload_ref": "manifest path or CAS id"
  }
}
```
