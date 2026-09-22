# CORPUS_INVENTORY — Phase I Stage 2
**As-of:** 2026-09-20 ~22:57 PT  
**CANONICAL:** NONE  
**Machine-readable:** `CORPUS_INVENTORY.json` (966 path entries + 6 candidate roots)

## Primary inventory surface
`PHASE_I_BASELINE/_scratch/mac_wt/codex` ← Mac consolidation WT tgz (2026-09-20 22:10 PT).  
Live Mac Shell+machineId: **UNAVAILABLE** this executor (see SOURCE_BOUNDARY).

## Candidate roots (summary)

| ID | Path | Class | Notes |
|----|------|-------|-------|
| C1 | Mac `~/solbian/codex` | CURRENT + HISTORICAL payload | PRIMARY; dirty; HEAD e289bd8 |
| C2 | `/workspace/codex_mac_inv/solbian-codex` | HISTORICAL mirror | HEAD 6e4036a; stub MD scrolls |
| C3 | GH `pegamonstro/solbian-codex` | HUB multi-branch | main = WORKING tip |
| C4 | `/workspace/codex-solbian-working` | WORKING/DERIVED | not SoT |
| C5 | Helios `00_Codex_Solbian` | ARCHIVE/BACKUP | reachable |
| C6 | Gitea `00_codex_solbian` | HISTORICAL MD | partial via bundles |

## Top-level (Mac WT snapshot)

| Path | Type | Probable role | Status |
|------|------|---------------|--------|
| README.md / README.POINTER.md | file | docs / pointer | CURRENT dirty / untracked pointer |
| CHANGELOG.md LICENSE | file | meta | HISTORICAL |
| scrolls/*.md (00–08) | file | rebuild MD chapters labelled “Chapter” | CURRENT_WORKING_TREE_MD (full on Mac) |
| source_original/ | dir | historical sref corpus | HISTORICAL_CANDIDATE |
| projects/{dao_foundation,memory_blockchain,porto_lagoa,seed_integration,solbian_academy} | dir | related experiments | RELATED_BOUNDARY |
| core/ tests/ | dir | C/seednet experiments | RELATED / EXPERIMENT (untracked) |
| archetypes glyphs journal manifest schema backlog references codex_minsoo | dir | thin / support | UNKNOWN/HISTORICAL |

## source_original/* counts (files, excl AppleDouble)

| Bucket | Count | Probable role |
|--------|------:|---------------|
| personae | 460 | DIALOGUE_OR_PERSONA (incl. JD↔Solace weeks) |
| scrolls | 102 | SCROLL (+ .sum companions) — **51** `.sref` incl. index |
| chapters | 62 | CHAPTER — **30** chapter + index + sums |
| policy | 21 | OTHER/POLICY |
| agents | 38 | RELATED_AGENTS |
| archetypes | 19 | ARCHETYPE |
| protocols | 17 | PROTOCOL (8 bodies + sums + decision_protocol) |
| manifest | 15 | MANIFEST + **Laws A/B** |
| system | 16 | OTHER |
| codex_minsoo | 14 | OTHER/EXPERIMENT |
| projects | 10 | RELATED |
| logs | 8 | LOG |
| legal | 7 | LEGAL |
| sati | 6 | RELATED (academy) |
| schema | 6 | SCHEMA |
| hardware | 5 | HARDWARE |
| mem | 5 | MEMORY |
| net | 4 | NETWORK |
| security | 4 | SECURITY |
| glossary | 2 | GLOSSARY |
| programs | 2 | OTHER |
| social | 2 | SOCIAL |
| tools | 2 | TOOLS |
| appendices | 1 | APPENDIX |
| registers | 1 | REGISTER |
| glyphs | 1 | GLYPH |

Plus root files: `codex_solbian_index.sref`, `index.sref`, `canonjson.c`.

## Sample deep files (verified)

| Path | Size | Role | Notes |
|------|-----:|------|-------|
| source_original/manifest/codex_solbian_laws.sref | 3160 | LAW set **A** | sha256 `728987e5…` |
| source_original/manifest/codex_solbian_laws_extended.sref | 10896 | LAW set **B** | sha256 `6258aa3b…` · 49 lines |
| source_original/protocols/codex_solbian_protocol_01..08.sref | ~1K ea | PROTOCOL | 01–05 ≡ Gitea-5; 06–08 Mac extras |
| source_original/scrolls/codex_solbian_scroll_20.sref | 3611 | SCROLL anomaly | internal scroll_no **21** |
| source_original/personae/joao/personae/solace/joao_solace-2015-W*.sref | varies | DIALOGUE SOURCE | 31 week files (+2025-W10) |
| scrolls/01_Genesis.md | 4675 | MD rebuild | dirty vs git; ≠ sref ordinal |

## Relationships
- C1.source_original ↔ C2.source_original: laws/scrolls **byte-identical** (sampled).  
- C1.scrolls.md ↔ C2.scrolls.md / older GH stubs: **substantive ≠ stub**.  
- C3.main tip ↔ C1 tree shape: **different** (WORKING layout vs historical).  
- C4 ↔ C3.working/main: DERIVED working synthesis lineage.

## Status legend
CURRENT · HISTORICAL_CANDIDATE · WORKING_NOT_HISTORICAL_SOT · RELATED_BOUNDARY · UNKNOWN · NOISE_APPLEDOUBLE
