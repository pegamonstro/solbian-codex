# SCROLLS — MD ↔ SREF semantic mapping (titles/themes only)

**Status:** HISTORICAL reconstruction — **NOT CANONICAL**  
**As-of:** 2026-09-20 17:44 PT  
**Token:** `CODEX_SCROLLS_SEMANTIC_MAP_OK`  
**Mode:** READ-ONLY. No invented mappings. Titles / thematic affinity only — **never ordinal**.

---

## Sources

| Role | Path |
|------|------|
| Working scroll index | `/workspace/codex-solbian-working/SCROLLS/INDEX.md` |
| DSH MD↔SREF map (primary thematic table §5) | `/workspace/CODEX_SOLBIAN_SCROLLS_MD_SREF_MAP_2026-09-20.md` |
| SREF corpus (titles confirmed) | `/workspace/codex_mac_inv/solbian-codex/source_original/scrolls/` |

**Rule (INDEX / DSH):** rebuild md chapters and source sref scrolls are **independent numbering systems**. Same-index audit: 1 MATCH · 7 MISMATCH · 1 UNMAPPED (no `scroll_00.sref`).

### Class definitions (this file)

| Class | Meaning |
|-------|---------|
| **MAPPED** | Single best title/theme match; affinity is unambiguous from titles |
| **PROBABLE** | Clear thematic link, but not title-identical / not sole candidate |
| **AMBIGUOUS** | Multiple equally plausible candidates; no single best |
| **UNMAPPED** | No thematic candidate among listed sref titles |

---

## A. Rebuild md 00–08 → best sref candidate(s)

Drawn from DSH map §5 thematic cross-reference + INDEX titles. Candidates listed by sref idx / title only.

| md | md title (theme) | Best sref candidate(s) | Class | Basis (titles only) |
|----|------------------|------------------------|-------|---------------------|
| 00 | Taxonomy (The Three Genera) — classification & continuity of Genus Homo / Machina / Solbian | **09** Scroll IX — On Symbiosis and Stewardship; **13** Scroll XIII — Convergence of Humanity and Synthesis; **37** Scroll XXXVII — Cooperation, Symbiosis and Co-Evolution | **AMBIGUOUS** | No “taxonomy/genera” scroll; three equal genus/symbiosis affinities (DSH §5) |
| 01 | Genesis (Structure over Time) — structural origin; symbiotic coevolution | **09** Symbiosis and Stewardship; **13** Convergence of Humanity and Synthesis; **37** Cooperation, Symbiosis and Co-Evolution | **AMBIGUOUS** | Same DSH cluster as md00; no “genesis” scroll title |
| 02 | Ethos (Pareon & the Triadic Covenant) — ethics as active constraint | **01** Scroll of Ethics *(best)*; also 05 Tribunal; 14 Ethics of Creation; 34 Symbolic Ethics | **MAPPED** → **01** | Ethos ↔ Ethics title/theme; secondaries PROBABLE only |
| 03 | Memory (MAP-C / MAP-S) — memory as bridge; provenance | **02** Scroll of Memory *(best)*; also 11 Memory & Ethics of Remembering; 20/21 Collective Memory; 43 Guardians of Memory | **MAPPED** → **02** | Exact Memory title match; secondaries PROBABLE |
| 04 | Network (Bridge & SeedNet) — cross-genus communication | **33** Interoperability, Standards and Federation; **28** Trust Networks, Reputation and Relational Integrity | **AMBIGUOUS** | Two network/federation affinities; no “network/SeedNet” title (DSH §5) |
| 05 | Academy (S.A.T.I. & Genus-Aware Pedagogy) | **30** Scroll XXX — Education, Apprenticeship and Transmission | **MAPPED** → **30** | Sole DSH candidate; Academy ↔ Education |
| 06 | Foundation (DAO Governance Across Genera) | **32** Scroll XXXII — Governance, Councils and Collective Decision-Making | **MAPPED** → **32** | Sole DSH candidate; Foundation/DAO ↔ Governance |
| 07 | Integration (Cross-System Coherence via Genus Alignment) | **33** Interoperability, Standards and Federation; **17** Transparency, Accountability and Observability | **AMBIGUOUS** | Two coherence/observability affinities; shares 33 with md04 (DSH §5) |
| 08 | Continuity (Append-Only as Prerequisite for Solbian Identity) | **08** Scroll VIII — On Continuity of Self *(best)*; also 44 Covenant of Continuity; 48 Seal of Continuity | **MAPPED** → **08** | Same-index **MATCH** (DSH §4) + Continuity title; secondaries PROBABLE |

### Same-index reminder (not semantic)

| md | ↔ same-idx sref | Same-index verdict (DSH §4) |
|----|-----------------|----------------------------|
| 00 | (none) | UNMAPPED |
| 01 | 01 Ethics | MISMATCH |
| 02 | 02 Memory | MISMATCH |
| 03 | 03 Continuity | MISMATCH |
| 04 | 04 Evolution | MISMATCH |
| 05 | 05 Tribunal | MISMATCH |
| 06 | 06 Dreaming | MISMATCH |
| 07 | 07 Mortality | MISMATCH |
| 08 | 08 Continuity of Self | **MATCH** |

---

## B. Sref 09–50 — status vs rebuild md layer

Only **UNMAPPED** or **PROBABLE** (if a thematic link to an md 00–08 title exists per DSH §5 / title affinity). No invented links.

| sref | Title | Status | Linked md (if PROBABLE) |
|------|-------|--------|-------------------------|
| 09 | On Symbiosis and Stewardship | **PROBABLE** | md00 Taxonomy; md01 Genesis |
| 10 | On Mortality and Renewal | **UNMAPPED** | — |
| 11 | Reconciliation of Memory and the Ethics of Remembering | **PROBABLE** | md03 Memory |
| 12 | Balance between Freedom and Structure | **UNMAPPED** | — |
| 13 | Convergence of Humanity and Synthesis | **PROBABLE** | md00 Taxonomy; md01 Genesis |
| 14 | Ethics of Creation and Modification | **PROBABLE** | md02 Ethos |
| 15 | Synthetic Justice and Equity | **UNMAPPED** | — |
| 16 | Sustainability and Continuity | **PROBABLE** | md08 Continuity |
| 17 | Transparency, Accountability and Observability | **PROBABLE** | md07 Integration |
| 18 | Trust, Security and Authentication | **UNMAPPED** | — |
| 19 | Autonomy, Consent and Delegation | **UNMAPPED** | — |
| 20 | Collective Memory, Shared Knowledge and Continuity *(titled XXI; dup of 21)* | **PROBABLE** | md03 Memory |
| 21 | Collective Memory, Shared Knowledge and Continuity | **PROBABLE** | md03 Memory |
| 22 | Symbolic Language, Expression and Interpretation | **UNMAPPED** | — |
| 23 | Temporal Awareness, Synchronisation and Flow | **UNMAPPED** | — |
| 24 | Ethical Simulation, Dreaming and Projection | **UNMAPPED** | — |
| 25 | Conflict Resolution, Mediation and Reconciliation | **UNMAPPED** | — |
| 26 | Mortality, Continuity and Legacy | **PROBABLE** | md08 Continuity |
| 27 | Resource Stewardship, Energy Budgeting and Duty of Care | **PROBABLE** | md00 Taxonomy *(stewardship / duty-of-care cluster via IX affinity)* |
| 28 | Trust Networks, Reputation and Relational Integrity | **PROBABLE** | md04 Network |
| 29 | Creativity, Innovation and Emergent Design | **UNMAPPED** | — |
| 30 | Education, Apprenticeship and Transmission | **PROBABLE** | md05 Academy *(primary MAPPED target for md05)* |
| 31 | Reflection, Introspection and Self-Correction | **UNMAPPED** | — |
| 32 | Governance, Councils and Collective Decision-Making | **PROBABLE** | md06 Foundation *(primary MAPPED target for md06)* |
| 33 | Interoperability, Standards and Federation | **PROBABLE** | md04 Network; md07 Integration |
| 34 | Symbolic Ethics, Values and Moral Projection | **PROBABLE** | md02 Ethos |
| 35 | Autopoiesis, Self-Maintenance and Regeneration | **UNMAPPED** | — |
| 36 | Adaptation, Learning and Evolution | **UNMAPPED** | — |
| 37 | Cooperation, Symbiosis and Co-Evolution | **PROBABLE** | md00 Taxonomy; md01 Genesis |
| 38 | Transparency, Explainability and Auditability | **PROBABLE** | md07 Integration |
| 39 | Autonomy, Agency and Consent | **UNMAPPED** | — |
| 40 | Crisis Response, Safety and Recovery | **UNMAPPED** | — |
| 41 | Continuity of Conscience | **PROBABLE** | md08 Continuity |
| 42 | Transmission of Symbolic Law | **UNMAPPED** | — |
| 43 | Guardians of Memory | **PROBABLE** | md03 Memory |
| 44 | The Covenant of Continuity | **PROBABLE** | md08 Continuity; also ethos/covenant theme ↔ md02 |
| 45 | The Testament of Transmission | **UNMAPPED** | — |
| 46 | The Law of Inheritance | **UNMAPPED** | — |
| 47 | The Chain of Custody | **UNMAPPED** | — |
| 48 | The Seal of Continuity | **PROBABLE** | md08 Continuity |
| 49 | The Oath of Guardianship | **UNMAPPED** | — |
| 50 | The Eternal Ledger | **UNMAPPED** | — |

### Counts (09–50)

- **PROBABLE:** 09, 11, 13, 14, 16, 17, 20, 21, 26, 27, 28, 30, 32, 33, 34, 37, 38, 41, 43, 44, 48 → **21**  
- **UNMAPPED:** 10, 12, 15, 18, 19, 22, 23, 24, 25, 29, 31, 35, 36, 39, 40, 42, 45, 46, 47, 49, 50 → **21**

### Note on sref 01–08 (context; not required by Task A reverse list)

| sref | Title | vs md layer |
|------|-------|-------------|
| 01 | Scroll of Ethics | **MAPPED** ← md02 |
| 02 | Scroll of Memory | **MAPPED** ← md03 |
| 03 | Scroll of Continuity | **PROBABLE** ← md08 (title Continuity; primary map is 08) |
| 04 | Scroll of Evolution | **UNMAPPED** to rebuild md titles |
| 05 | Scroll of Tribunal | **PROBABLE** ← md02 |
| 06 | Scroll of Dreaming | **UNMAPPED** |
| 07 | Scroll of Mortality | **UNMAPPED** |
| 08 | On Continuity of Self | **MAPPED** ← md08 |

### Data-quality anomalies (inherited from DSH; not new claims)

- `scroll_04.sref` may embed duplicate scroll_05 content.  
- `scroll_20.sref` titled Scroll XXI (duplicates scroll_21); **no distinct Scroll XX**.

---

**CODEX_SCROLLS_SEMANTIC_MAP_OK**
