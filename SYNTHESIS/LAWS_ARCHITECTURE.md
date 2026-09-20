# SYNTHESIS — Laws architecture (working gloss)

STATUS: SYNTHESIS  
CANONICAL: NO  
LAST UPDATED: 2026-09-20  
TOKEN: CODEX_SYNTHESIS_LAWS_ARCHITECTURE_OK  

SOURCE BASIS:
- `/workspace/codex-solbian-working/LAWS/INDEX.md`
- `/workspace/codex-solbian-working/LAWS/CATALOGUE_A.md` · `CATALOGUE_B.md` · `CATALOGUE_C.md`
- `/workspace/codex-solbian-working/LAWS/CROSSMAP_ABC_2026-09-20.md`
- `/workspace/codex-solbian-working/LAWS/B_PRIME_RECOVERY_2026-09-20.md`
- `/workspace/codex-solbian-working/PROVENANCE/SET_A_CHAPTER_BODY_EVIDENCE_2026-09-20.md`
- `/workspace/codex-solbian-working/SYNTHESIS/LAW_CATALOGUES_RELATIONSHIP_SYNTHESIS.md`
- `/workspace/CODEX_SOLBIAN_LAW_AB_COMPARISON_2026-09-20.md`
- `/workspace/CODEX_SOLBIAN_LAWS_GITEA_VS_AB_2026-09-20.md`
- `/workspace/CODEX_SOLBIAN_LAWS_VARIANTS_MAP_2026-09-20.md`

---

## What a Law appears to be (corpus reading)

Across recovered artefacts, “Law” is **not one schema**. Evidence shows at least:

| Surface | What “Law” looks like | Evidence |
|---------|----------------------|----------|
| Set A | Short operational NDJSON objects (`kind:law`; some titles say Protocol) | CATALOGUE_A; AB comparison |
| Set B / B′ | Normative shall/must rights-charter statements (`solbian.law.*`) | CATALOGUE_B; AB comparison |
| Set C | Constitutional Romans I–XLVIII + meta (`codex.laws.extended.*` / Gitea LAWS.md) | CATALOGUE_C; Gitea vs AB |

**NOT ESTABLISHED:** a single definition of “Law” that unifies A/B/C; whether Protocol-titled A:04–08 are laws, protocols, or both.

---

## Authority (as evidenced)

| Claim | Status |
|-------|--------|
| Any catalogue is CANONICAL Working Codex doctrine | **NOT ESTABLISHED** — standing JD lock: all HISTORICAL |
| Nested seed / seed-dsh copies imply SEED runtime dependency for this tree | **NOT ESTABLISHED** (LAWS/INDEX standing rules) |
| Filename `laws_extended.sref` uniquely identifies one catalogue | **False** — may be B, B′, or C; disambiguate by id/`kind` |

Authority in the working corpus is **catalogue-letter + schema**, not bare filename or folklore count.

---

## A / B / B′ / C roles (SYNTHESIS gloss only)

| Layer | Count | Role (working gloss — not historical self-label) | Schema / ids |
|-------|------:|--------------------------------------------------|--------------|
| **A** | 8 (+1 meta) | Operational core — consent, budgets, checksums, audit | `sref_v5` · `codex:laws.*` |
| **B** | 50 | Rights/ethics charter — normative shall/must + late 48a/48b | `kind:law` · `solbian.law.*` |
| **B′** | 48 | Historical subset of B (01–48 only; no 48a/48b) | same as B |
| **C** | **49** (1 meta + 48) | Constitutional Roman narrative Continuity→Finality | `kind:codex_law` · `codex.laws.extended.*` |

**Preserve conflicts:** A↔B different catalogues (not renumberings). A↔C shared vocabulary only (exact title **Symbiosis** once). B↔C both “extended,” different names/numbering. Mapping ≠ equivalence (`CROSSMAP_ABC`).

---

## Set A condensation (VERIFIED HISTORICAL)

Set A meta claims extraction from chapters and protocols. Body evidence:

| A objects | Condensed from | Correspondence |
|-----------|----------------|----------------|
| A:01–03 (Reflection, Projection, Symbiosis) | Chapters 06–08 | EXACT_PASSAGE / PARAPHRASE |
| A:04–08 (Identity…Memory Protocols) | Protocols 01–05 | PARAPHRASE |

Result: **CLAIM VERIFIED** as condensed operational digest — **not** byte-identical wholesale copy. Status remains HISTORICAL — **NOT CANONICAL**.

---

## “49 Laws” folklore = Set C

| Folklore / count | Resolves to |
|------------------|-------------|
| **49** | Set **C** record count (**meta + 48** binding Romans) |
| **50** | Set **B** (with 48a/48b) |
| **8** | Set **A** operational objects (excl. meta) |

Explicit: “49 Laws” ≠ B’s 50 NDJSON laws.

---

## No merge

**Standing JD lock:** A, B, B′, C remain HISTORICAL — **no merge**, no canon pick. Complementary citation (operational / rights / constitutional narrative) is a SYNTHESIS option only; elevation is JD-only.

**PROPOSED DECISION options:** see `LAW_CATALOGUES_RELATIONSHIP_SYNTHESIS.md` — none enacted here.

---

**CODEX_SYNTHESIS_LAWS_ARCHITECTURE_OK**
