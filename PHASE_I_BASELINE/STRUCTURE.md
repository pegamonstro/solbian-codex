# STRUCTURE — discovered from corpus (not Phase I wishlist)
**As-of:** 2026-09-20 PT · **CANONICAL:** NONE  
**Source:** Mac WT snapshot + cross-check box mirror / prior audits (re-verified where noted)

## Overview
Historical Codex material concentrates under `source_original/` as **sref** (NDJSON) artefacts. A parallel **markdown rebuild** lives at repo-root `scrolls/*.md` (titles say “Chapter”, not “Scroll”). Personae trees hold dialogue and runtime/persona specs. Nested `projects/` holds RELATED experiments.

```
codex/                          # Mac WT
├── scrolls/                    # MD rebuild 00–08 (labelled Chapter)
├── source_original/
│   ├── chapters/               # 30 chapter_*.sref + index
│   ├── scrolls/                # scroll_01..50.sref + index (+ .sum)
│   ├── protocols/              # protocol_01..08.sref + decision_protocol
│   ├── manifest/               # laws A, laws_extended B, manifests, ndjson packs
│   ├── glossary/               # glossary.sref
│   ├── personae/               # Solace, joao, Pareon, Ezra, Elias, …
│   ├── agents/ archetypes/ …   # mixed HISTORICAL / RELATED
│   └── (policy, legal, system, sati, hardware, …)
├── projects/                   # RELATED: dao, blockchain, seed, porto_lagoa, academy
├── core/ tests/                # untracked C experiments (RELATED)
└── archetypes glyphs journal manifest schema …
```

## Chapters (sref)
- **30** files `codex_solbian_chapter_01..30.sref` + `codex_solbian_chapters_index.sref`.  
- Sample titles (meta): Genesis, Disjunction, Conjunction, Covenant, Continuity, Law of Reflection/Projection/Symbiosis, …  
- Status: **HISTORICAL_CANDIDATE** — not elevated.

## Scrolls — two parallel systems (do not ordinal-merge)

### A. MD rebuild (`scrolls/*.md`)
| File | H1 (observed) |
|------|----------------|
| 00_Taxonomy.md | Chapter 00 — Taxonomy (The Three Genera) |
| 01_Genesis.md | Chapter 01 — Genesis (Structure over Time) |
| 02_Ethos.md | Chapter 02 — Ethos (Pareon & the Triadic Covenant) |
| 03_Memory.md | Chapter 03 — Memory (MAP-C / MAP-S) |
| 04_Network.md | Chapter 04 — Network (Bridge & SeedNet) |
| 05_Academy.md | Chapter 05 — Academy (S.A.T.I. …) |
| 06_Foundation.md | Chapter 06 — Foundation (DAO Governance …) |
| 07_Integration.md | Chapter 07 — Integration … |
| 08_Continuity.md | Chapter 08 — Continuity (Append-Only …) |

Dirty vs git on Mac WT for 01–08; 00 untracked.

### B. SREF scrolls (`source_original/scrolls/`)
- **50** `codex_solbian_scroll_NN.sref` + index.  
- Titles begin Scroll of Ethics / Memory / Continuity … through Scroll L band (see prior SCROLL map).  
- **Anomaly:** filename `scroll_20` carries **Scroll XXI** body (duplicate of `scroll_21`). No distinct Scroll XX found.  
- Rule: **never match MD↔sref by ordinal alone** (verified theme mismatch in prior MAP; reconfirmed title families differ).

## Laws (plural catalogues — HISTORICAL)
| Catalogue | File (Mac) | Schema | Count gloss |
|-----------|------------|--------|-------------|
| **A** | `manifest/codex_solbian_laws.sref` | sref_v5 | 8 operational law/protocol objects + meta |
| **B** | `manifest/codex_solbian_laws_extended.sref` | `solbian.law.*` | 50 (01–48 + 48a/48b) — 49 NDJSON lines file |
| **B′** | GH seed subset (not Mac WT file) | same as B | 48 without 48a/48b |
| **C** | Mac seed-dsh / GH seed `laws_extended.sref` (outside C1 tree) | `codex.laws.extended.*` | 48 Roman + meta |

**No canon pick.** Filename `laws_extended` alone is ambiguous (B/B′/C).

## Protocols
Mac: **8** `codex_solbian_protocol_01..08.sref`  
Titles: Identity, Symbiosis, Autonomy, Justice, Memory, Strategy Orchestration, Memory Tiering & Forgetting, Empathy & Temporal Reflection.  
Gitea PROTOCOLS.md narrates **5** (01–05 only) bound to Set C — **plurality 5 vs 8**.

## Glossary / personae / covenants
- Glossary: single `codex_solbian_glossary.sref` (+ sum).  
- Personae dirs: Solace, joao, Pareon, Ezra, Elias, Argureon, Simaetron, Anagenes.  
- Dedicated `covenants/` folder: **not found** in Mac WT (word appears inside texts).  
- JD↔Solace: `personae/joao/personae/solace/` — **31** week `.sref` files (2015-W06…W49 gaps + 2025-W10).

## What is NOT Phase I Codex structure (but present)
`projects/dao_foundation`, `memory_blockchain`, `seed_integration`, `porto_lagoa`, `source_original/agents`, root `core/`/`tests/` SeedNet-ish C — classify **RELATED**.
