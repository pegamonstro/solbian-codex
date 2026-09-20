# Wave 1 — Consolidation status report
**As-of:** 2026-09-20 17:28 PT
**Format:** Master Consolidation §36
**Token:** CODEX_WAVE1_STATUS_OK

## DISCOVERED
- Master Consolidation Directive active (Constitution §§2–34 non-blocking).
- Prior audit artefacts linked under `PROVENANCE/`.

## RECONSTRUCTED
HISTORICAL indexes (NOT CANONICAL):
| Area | Path | Token |
|------|------|-------|
| Laws overview + A/B/B′/C | `LAWS/INDEX.md` + catalogues | CODEX_WORKING_LAWS_INDEX_OK |
| Scrolls (50 sref + 9 md) | `SCROLLS/INDEX.md` | CODEX_WORKING_SCROLLS_INDEX_OK |
| Protocols 5↔8 | `PROTOCOLS/INDEX.md` | CODEX_WORKING_PROTOCOLS_INDEX_OK |
| Five Canons + pillars | `CANONS/INDEX.md` | CODEX_WORKING_CANONS_INDEX_OK |
| Triadic Covenant (titles) | `COVENANTS/INDEX.md` | CODEX_WORKING_COVENANTS_INDEX_OK |
| Open questions | `OPEN_QUESTIONS/WAVE1.md` | — |

## CONSOLIDATED
Private working corpus root: `/workspace/codex-solbian-working/`  
Governance: `CONSTITUTION/MASTER_CONSOLIDATION_DIRECTIVE_2026-09-20.md` + incomplete Constitution stub.

## PROVENANCE
Indexes cite upstream audits (`CODEX_SOLBIAN_*_2026-09-19/20.md`), `audit-laws/` byte copies for B/C, Gitea LAWS dump, Mac inv for A. B′ documented without local byte copy.

## CONFLICTS
- Law catalogues A vs B vs C (not renumberings).
- Scrolls MD↔SREF same-index mostly MISMATCH.
- Protocols 5 (Gitea) vs 8 (Mac).
- ETHICS on seed, missing in Gitea HEAD; PROTOCOLS broken link.

## UNKNOWN
See `OPEN_QUESTIONS/WAVE1.md` (15 items). Notably: B′ local hash, A→chapters DERIVED claim, protocol body identity, Working Codex binding policy.

## SYNTHESIS
None yet this wave (indexes only — no doctrinal merge).

## CANONICALITY
```
SOURCE / HISTORICAL — catalogues and indexes
WORKING — private corpus tree
PROPOSED — Master Consolidation / Phase A method
CANONICAL — none declared
UNRESOLVED — open questions list
```

## NEXT AUTONOMOUS ACTION
1. Stub `CURRENT_WORKING_CODEX/OUTLINE.md` (traceable placeholders; NOT ESTABLISHED where silent).
2. Add `DIALOGUE/INDEX.md` from completeness pass.
3. Optional: pull B′ byte copy via GH for hash parity.
4. Chapter title index from Mac/Gitea (thin).
