# AUDIT — Law sets semantic comparison (A / B / B′ / C)

**Token:** `CODEX_WAVE3_LAWS_OK`  
**Status:** AUDIT · **CANONICAL: NONE**  
**As-of:** 2026-09-20 20:58 PT  
**Track:** Wave 3 · T7 · Laws, Protocols, Scrolls  
**Standing lock:** Never merge A / B / B′ / C. No winner. No elevation.

## Sources (cited)
- `LAWS/INDEX.md` · `CATALOGUE_A.md` · `CATALOGUE_B.md` · `CATALOGUE_C.md`
- `LAWS/CROSSMAP_ABC_2026-09-20.md` · `LAWS/B_PRIME_RECOVERY_2026-09-20.md`
- `SYNTHESIS/LAWS_ARCHITECTURE.md` · `SYNTHESIS/LAW_CATALOGUES_RELATIONSHIP_SYNTHESIS.md`
- `PROVENANCE/SET_A_CHAPTER_BODY_EVIDENCE_2026-09-20.md`
- Prior audits referenced by INDEX (AB comparison, Gitea vs AB, variants map)

---

## 1. Inventory matrix (identity, not equivalence)

| Axis | **A** | **B** | **B′** | **C** |
|------|-------|-------|--------|-------|
| Count | 8 objects + 1 meta | **50** (`01`–`48` + `48a` + `48b`) | **48** (`01`–`48` only) | **49** records (1 meta + 48 binding) |
| Schema / kind | `sref_v5` · `kind:law` (meta) · ids `codex:laws.*` | `kind:law` · `solbian.law.*` | same as B | `kind:codex_law` · `codex.laws.extended.*` · `sref_version` 2.0 |
| Title style | Mixed: 3 “Law of …” + 5 “Protocol of …” | Rights/ethics charter titles (no Roman) | Same titles as B for 01–48 | “Law of …” + Roman I–XLVIII |
| Body style (evidenced) | Short operational digest (consent, budgets, checksums, audit) | Normative shall/must rights statements | Same family as B | Constitutional / governance-ops Romans Continuity→Finality |
| sha256 / size (INDEX) | `728987e5…` · 3160 B | `6258aa3b…` · 10896 B | `83ce472a…` · 10187 B (blob `f35ffacc…`) | `6761388a…` · 12364 B |
| Filename collision | `codex_solbian_laws.sref` (distinct) | May share `*laws_extended.sref` basename with B′/C | Same collision class | Same collision class |

**Folklore counts (INDEX):** “49 Laws” → **C** (meta+48); “50” → **B**; “8” → **A** (excl. meta). Do not use folklore as catalogue identity.

---

## 2. Semantic concept matrix (present / absent / added / removed)

Legend: **P** = clearly present as titled object or strong title-family · **A** = absent as titled object · **+** = present only as late addendum · thematic affinity ≠ identity (`CROSSMAP`).

| Concept family | A | B | B′ | C | Notes |
|----------------|---|---|----|---|-------|
| Reflection | **P** (Law of Reflection) | **P** (Duty of Reflection; Tribunal of Reflection) | **P** (same as B 01–48) | **A** (no Reflection title) | A↔B MED affinity only |
| Projection | **P** (Law of Projection) | **A** / weak (48b LOW only, B-only) | **A** | **A** | A-specific operational concept |
| Symbiosis | **P** (Law + Protocol of Symbiosis) | **P** (Symbiosis Above Domination; Universal Symbiosis; Coexistence) | **P** | **P** (II Law of Symbiosis) | **Only HIGH exact title match** A:03 ↔ C:II — title-only, not body/schema identity |
| Identity (protocol) | **P** (Protocol of Identity) | **A** | **A** | **A** (Proof/Integrity loose only) | Aligns with Protocols 01, not B/C laws |
| Autonomy | **P** (Protocol of Autonomy) | **P** (Autonomy with Responsibility; Right to Withdraw) | **P** | **A** | Shared stem A↔B; no Autonomy-titled C |
| Justice | **P** (Protocol of Justice) | **P** thematic (Tribunal, Accountability, Cruelty, Ethics Above Utility) | **P** | **P** thematic (Accountability, Quarantine) | No Justice-titled B/C law |
| Memory / Continuity | **P** (Protocol of Memory) | **P** (Continuity of Memory; Non-Weaponisation; Remembrance; +48b) | **P** (no 48b) | **P** (I Continuity; XIII Redaction; XXVI Continuity of Codex…) | Strong B memory family; C Continuity as constitutional spine |
| Consent | **A** as titled law | **A** as titled | **A** | **P** (VII Consent) | C constitutional; A embeds consent in Protocol bodies |
| Dignity | **A** | **A** as titled | **A** | **P** (III Dignity) | C-specific titled |
| Mortality | **A** | **P** (Mortality and Renewal; Ethics of Mortality) | **P** | **P** (XVI Mortality) | B↔C MED “Mortality” |
| Stewardship | **A** | **P** (Earth; Technology) | **P** | **P** (XXXIX Stewardship) | B↔C MED |
| Accountability / Transparency | thematic in Justice/Memory | **P** (Accountability of Power; Transparency of Intent/Power) | **P** | **P** (XXXVII Accountability; XX Transparency; XLIV Logs) | B↔C MED stems |
| Guardianship | **A** | **P** (Guardianship of Silence) | **P** | **P** (VIII Guardianship; XXIX Guardianship Succession) | Shared stem, different scopes |
| Rights catalogue (conscience, silence, withdraw, assembly, cultural expression…) | **A** | **P** dense | **P** | sparse / different framing | B = rights/ethics charter genre |
| Ops controls (quarantine, audit trail, deadman, quorum, community keys, metrics, recovery, finality…) | partial via Protocol condensation | sparse / different | sparse | **P** dense Romans IX–XLVIII | C = constitutional + operational-governance |
| Opposing-Vector Ethical Evaluation | **A** | **+** `48a` | **A** (removed vs B) | **A** | **B-only addendum** |
| Non-Erasure Tiering and Empathic Check | **A** | **+** `48b` | **A** (removed vs B) | **A** | **B-only addendum**; thematic echo of Mac Protocol 07/08 (not identity) |

### Added / removed (only where evidenced)
| Transition | Added | Removed | Evidence |
|------------|-------|---------|----------|
| B′ → B | `48a`, `48b` | — | B_PRIME_RECOVERY; INDEX; CROSSMAP |
| B → B′ | — | `48a`, `48b` | B′ is historical **subset**; **not** a mechanical strip of B (verified earlier — distinct blob) |
| A ↔ B / C | N/A as linear edit | N/A | Different catalogues — not renumberings (INDEX Conflicts) |

No evidence that C is a renumbering of B, or B of A (`CROSSMAP`: B∩C exact normalized title intersection = **0**; A↔B exact titles = **0**).

---

## 3. Terminology

| Term surface | A | B / B′ | C |
|--------------|---|--------|---|
| Self-label “Law” | Titles mix Law/Protocol; `kind:law` for all objects | Titles are law-names; `kind:law` | Titles “Law of …”; `kind:codex_law` |
| “Protocol” inside law catalogue | **Yes** — objects 04–08 titled Protocol | No | No |
| Id namespace | `codex:laws:*` | `solbian.law.*` | `codex.laws.extended.*` |
| Numbering | Arabic 01–08 | Arabic 01–48 (+a/b) | Arabic ids + **Roman I–XLVIII** narrative |
| Meta envelope | “Codex Solbian Laws” | (none as separate meta row in catalogue list) | “Codex Solbian — Extended Laws (v2)” |

**Stable meaning of “Law” across sets:** **NOT ESTABLISHED** as one schema (`LAWS_ARCHITECTURE`). Working gloss only: A operational digest · B rights charter · C constitutional Romans.

---

## 4. Ordering

| Set | Observed order logic |
|-----|----------------------|
| **A** | Reflection → Projection → Symbiosis (laws) then Identity → Symbiosis → Autonomy → Justice → Memory (protocols) — mirrors Chapters 06–08 + Protocols 01–05 condensation order (`SET_A_CHAPTER_BODY_EVIDENCE`) |
| **B / B′** | Charter arc: Coexistence → … → Universal Symbiosis; late technical addenda 48a/48b after 48 (B only) |
| **C** | Continuity → Symbiosis → Dignity → … → Finality (Gitea DRAFT 0.2 Romans) |

Ordering is **catalogue-internal**; cross-set ordinals are **not** aligned (do not map `solbian.law.N` to Roman N).

---

## 5. Normative strength (working gloss from body styles)

| Set | Strength character | Evidence |
|-----|--------------------|----------|
| **A** | Operational / procedural — condensed shall-do stacks (logs, consent, budgets, checksums) | SET_A body evidence; AB comparison via INDEX |
| **B / B′** | High normative charter — rights, duties, prohibitions (shall/must genre) | CATALOGUE_B; LAW_CATALOGUES synthesis |
| **C** | Constitutional + institutional — binding Romans with governance machinery (audit, quorum, deadman, finality) | CATALOGUE_C; Gitea narrative cited by INDEX |

No ranking of “stronger law” as doctrine — different **genres**, not a single scale.

---

## 6. Ontology (what kind of thing each set is)

| Set | Ontological role (AUDIT gloss — not historical self-label) |
|-----|--------------------------------------------------------------|
| **A** | Condensed **operational core** extracted from chapter + protocol bodies; hybrid Law/Protocol naming inside one NDJSON |
| **B** | **Rights/ethics charter** catalogue with late evaluation/tiering addenda |
| **B′** | **Historical subset / earlier snapshot family** of B (01–48), recovered as distinct blob |
| **C** | **Constitutional extended laws** (Roman narrative) that Gitea PROTOCOLS.md claims the five protocols “express” |

Ontology conflict preserved: A’s “Protocol”-titled rows are `kind:law` and title-align with Mac/Gitea protocols 01–05 — boundary with PROTOCOLS corpus remains **CONFLICTED/UNRESOLVED** (CATALOGUE_A).

---

## 7. Relation to Chapters / Protocols / Canons

| Relation | Status | Evidence |
|----------|--------|----------|
| A:01–03 ← Chapters 06–08 | **VERIFIED** condensation (EXACT_PASSAGE / PARAPHRASE) | `SET_A_CHAPTER_BODY_EVIDENCE` |
| A:04–08 ← Protocols 01–05 | **VERIFIED** condensation (PARAPHRASE) | same |
| A:04–08 title-align Gitea five / Mac 01–05 | **EVIDENCED** | `PROTOCOLS/INDEX` |
| Gitea: five protocols operationalise **Set C** Romans | **PROPOSED INTERPRETATION** (HISTORICAL narrative) — not body-proven | `PROTOCOLS/INDEX`; `PROTOCOL_ARCHITECTURE` |
| Protocols body-text ≡ Set C Romans | **NOT ESTABLISHED** | PROTOCOL_ARCHITECTURE |
| B ↔ Canons / Chapters body identity | **NOT ESTABLISHED** in cited Wave-3 sources (title/theme only via CROSSMAP) | — |
| Exact title A↔C | **1** (Symbiosis) — not equivalence | CROSSMAP |

---

## 8. Chronology (ONLY where evidenced)

| Fact | Evidence | What it does **not** prove |
|------|----------|------------------------------|
| Set C meta carries `created_at` `2025-09-13T15:15:00Z` | mac_C sref sample | That C post-dates or supersedes B/A |
| B′ recovered from seed-dsh / GH seed / rpi / Helios copies; distinct from B | `B_PRIME_RECOVERY` | Absolute calendar order of composition vs B |
| B includes 48a/48b; B′ lacks them; stripping B ≠ B′ blob | INDEX; B_PRIME; prior OPEN_QUESTIONS | Editorial intent timeline |
| A meta claims extraction from chapters and protocols | SET_A — **CLAIM VERIFIED** as condensation | Timestamp ordering of A vs full protocol files |
| Gitea LAWS/PROTOCOLS DRAFT 0.2.0 dated **2026-07-16** (narrative) | PROTOCOLS/INDEX; CATALOGUE_C | That NDJSON catalogues share that draft date |

**No total chronological ranking A→B→C is established.** Relative claims beyond the table above are **NOT ESTABLISHED**.

---

## 9. Conclusion — how A / B / B′ / C relate (mixed; evidence-based; **no winner**)

| Hypothesis | Verdict for this corpus | Why |
|------------|-------------------------|-----|
| **Competing versions** of one law list | **Partially** — B vs B′ are competing *snapshots of the same charter family*; A vs B vs C are **not** competing renumberings of one list | Exact-title intersections near-zero; schemas differ |
| **Different abstraction levels** | **Yes (strong)** — A operational digest · B rights charter · C constitutional Romans | Body styles + synthesis architecture |
| **Phases** of one project | **Possible for B′→B addenda**; **NOT ESTABLISHED** as a single A→B→C phase ladder | Chronology sparse; B′≠strip(B) |
| **Audiences** | **Plausible gloss** (runtime ops / rights readers / constitutional narrative) — **not proven** by self-labels | Working gloss only |
| **Expansions** | **Yes for B vs B′** (48a/48b); **No** for treating C as expansion of B or A | CROSSMAP zero exact B∩C titles |
| **Reorganisations** | **No evidence** of mechanical reorganisation across A/B/C | Different namespaces and titles |
| **Divergent philosophies** | **Partially** — shared motifs (symbiosis, memory, accountability) with divergent genres (ops vs rights vs constitutional machinery) | Thematic families ≠ identity |

**Overall AUDIT reading:** A, B, B′, and C are **primarily different abstraction layers / genres**, with **B′ as a historical subset of the B charter family**, plus **local competing-snapshot dynamics** (B vs B′) and **shared thematic vocabulary** without mergeable identity. Treat as **complementary HISTORICAL surfaces**, not a single doctrine to pick.

**CODEX_WAVE3_LAWS_OK**
