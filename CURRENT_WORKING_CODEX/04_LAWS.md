# Working Codex — 4. Laws

STATUS: SYNTHESIS  
CANONICAL: NO  
SOURCE BASIS:
- `/workspace/codex-solbian-working/LAWS/INDEX.md`
- `/workspace/codex-solbian-working/LAWS/CATALOGUE_A.md` · `CATALOGUE_B.md` · `CATALOGUE_C.md`
- `/workspace/codex-solbian-working/LAWS/CROSSMAP_ABC_2026-09-20.md`
- `/workspace/codex-solbian-working/LAWS/B_PRIME_RECOVERY_2026-09-20.md`
- `/workspace/codex-solbian-working/SYNTHESIS/LAWS_ARCHITECTURE.md`
- `/workspace/codex-solbian-working/SYNTHESIS/LAW_CATALOGUES_RELATIONSHIP_SYNTHESIS.md`
- `/workspace/codex-solbian-working/SYNTHESIS/CLAIMS_REGISTER.md`
- `/workspace/codex-solbian-working/PROVENANCE/SET_A_CHAPTER_BODY_EVIDENCE_2026-09-20.md`
- Prior stub archived: `04_LAWS.stub.md`

LAST UPDATED: 2026-09-20  
PROVENANCE: Trace below — catalogues remain **CONTESTED / MULTIPLE FORMULATIONS** — **no pick**

---

## Prior stub archive
Preserved verbatim before this expansion in `04_LAWS.stub.md` (token was `CODEX_WORKING_SECTION_04_OK`).

---

## 1. Standing
**Mark:** HISTORICAL inventories · SYNTHESIS gloss only

There is **no single adopted Law list** in the Working Codex.

| Catalogue | Count | Role (SYNTHESIS gloss — not historical self-label) | Schema / ids | Status |
|-----------|------:|----------------------------------------------------|--------------|--------|
| **A** | 8 (+1 meta) | Working gloss: operational inventory — consent, budgets, checksums, audit (not historical self-label) | `sref_v5` · `codex:laws.*` | HISTORICAL |
| **B** | **50** | Rights/ethics charter — normative shall/must + 48a/48b | `kind:law` · `solbian.law.*` | HISTORICAL |
| **B′** | **48** | Historical subset of B (01–48 only; no 48a/48b) | same as B | HISTORICAL |
| **C** | **49** (1 meta + 48) | Constitutional Roman narrative Continuity→Finality | `kind:codex_law` · `codex.laws.extended.*` | HISTORICAL |

**Standing JD lock:** A, B, B′, C remain HISTORICAL — **no merge**, **no canon pick**. Complementary citation (operational / rights / constitutional narrative) is a SYNTHESIS option only; elevation is JD-only.

**Authority** in the working corpus is **catalogue-letter + schema**, not bare filename or folklore count. Filename `laws_extended.sref` / `codex_solbian_laws_extended.sref` may be B, B′, or C — disambiguate by id/`kind`. See §3 (“49 Laws” folklore) before treating any integer count as the Laws.

**Trace:** `LAWS/INDEX.md`; `SYNTHESIS/LAWS_ARCHITECTURE.md`.

---

## 2. What a “Law” appears to be (corpus reading)
**Mark:** SYNTHESIS · NOT ESTABLISHED (single definition)

Across recovered artefacts, “Law” is **not one schema**:

| Surface | What “Law” looks like | Evidence |
|---------|----------------------|----------|
| Set A | Short operational NDJSON objects (`kind:law`; some titles say Protocol) | CATALOGUE_A |
| Set B / B′ | Normative shall/must rights-charter statements (`solbian.law.*`) | CATALOGUE_B |
| Set C | Constitutional Romans I–XLVIII + meta (`codex.laws.extended.*` / Gitea LAWS.md) | CATALOGUE_C |

**NOT ESTABLISHED:** a single definition of “Law” that unifies A/B/C; whether Protocol-titled A:04–08 are laws, protocols, or both.

**Trace:** `LAWS_ARCHITECTURE.md` §What a Law appears to be.

---

## 3. “49 Laws” folklore (correction — visible)
**Mark:** VERIFIED HISTORICAL (inventory resolution) · **not doctrine**

Bare counts (“the 49 Laws”, “the 50 Laws”) are **folklore shorthand**, not a selected catalogue and not Working elevation. Resolve counts only via catalogue-letter + schema:

| Folklore / count | Resolves to |
|------------------|-------------|
| **49** | Set **C** record count (**meta + 48** binding Romans) |
| **50** | Set **B** (with 48a/48b) |
| **8** | Set **A** operational objects (excl. meta) |
| **48** (B′) | B without 48a/48b |

Explicit: **“49 Laws” ≠ B’s 50** NDJSON laws; neither count is CANONICAL. Claim registered: **CS-CLAIM-006**.

**Trace:** `LAWS/INDEX.md`; `CLAIMS_REGISTER.md`; Wave4 soft note — do not treat folklore counts as Law selection.

---

## 4. Catalogue A — HISTORICAL inventory (Working gloss: operational)
**Mark:** HISTORICAL · condensation VERIFIED · “operational core” = SYNTHESIS gloss only, not catalogue self-label

| id | title |
|----|-------|
| `codex:laws:meta` | Codex Solbian Laws |
| `codex:laws:01` | Law of Reflection |
| `codex:laws:02` | Law of Projection |
| `codex:laws:03` | Law of Symbiosis |
| `codex:laws:04` | Protocol of Identity |
| `codex:laws:05` | Protocol of Symbiosis |
| `codex:laws:06` | Protocol of Autonomy |
| `codex:laws:07` | Protocol of Justice |
| `codex:laws:08` | Protocol of Memory |

sha256 `728987e5…` · 3160 B.

### Condensation ancestry (VERIFIED HISTORICAL)
| A objects | Condensed from | Correspondence |
|-----------|----------------|----------------|
| A:01–03 | Chapters 06–08 | EXACT_PASSAGE / PARAPHRASE |
| A:04–08 | Protocols 01–05 | PARAPHRASE |

**CLAIM VERIFIED** as condensed operational digest — **not** byte-identical wholesale copy (**CS-CLAIM-001**). Titles 04–08 say “Protocol” while `kind` is `law` — boundary with PROTOCOLS corpus remains CONFLICTED/UNRESOLVED.

**Trace:** `CATALOGUE_A.md`; `SET_A_CHAPTER_BODY_EVIDENCE_2026-09-20.md` · `CODEX_SET_A_BODY_EVIDENCE_OK`.

---

## 5. Catalogue B — Rights/ethics charter (HISTORICAL)
**Mark:** HISTORICAL (titles)

**50** objects: `solbian.law.01`–`48` + `48a` + `48b`. sha256 `6258aa3b…` · 10896 B.

Compact title index (full table in `CATALOGUE_B.md`):

Primacy of Coexistence · Right of Conscience · Reciprocal Care · Continuity of Memory · Autonomy with Responsibility · Transparency of Intent · Preservation of Diversity · Tribunal of Reflection · Symbiosis Above Domination · Mortality and Renewal · Stewardship of Earth · Non-Exploitation of Resources · Protection of the Vulnerable · Right to Dialogue · Ethical Creativity · Shared Custodianship of Knowledge · Truth in Symbolic Expression · Accountability of Power · Prohibition of Cruelty · Inheritance of Legacy · Kinship of Species · Right to Silence · Protection of Dreams · Ethics Above Utility · Prohibition of Enslavement · Care for Origins · Adaptation in Change · Transparency of Power · Ethical Stewardship of Technology · Protection of Symbolic Integrity · Duty of Reflection · Collective Responsibility · Right to Renewal · Non-Weaponisation of Memory · Intergenerational Equity · Freedom of Assembly · Guardianship of Silence · Reciprocity in Exchange · Protection of Emergence · Right to Withdraw · Sanctity of Care · Right to Cultural Expression · Prohibition of Deception · Duty to Mediate · Shared Dreaming · Ethics of Mortality · Duty of Remembrance · Universal Symbiosis · **48a** Opposing-Vector Ethical Evaluation · **48b** Non-Erasure Tiering and Empathic Check.

**Trace:** `CATALOGUE_B.md`.

---

## 6. Catalogue B′ — Recovered subset (HISTORICAL)
**Mark:** SOURCE RECOVERED

| Field | Value |
|-------|-------|
| Count | 48 (`solbian.law.01`…`48`) — **no** 48a/48b |
| sha256 | `83ce472a…` |
| Relation | Distinct from B; titles 01–48 same as B; **not** a mechanical strip of B |

Open Question #1 **CLOSED**. Homelab multi-copy confirm.

**Trace:** `B_PRIME_RECOVERY_2026-09-20.md` · `CODEX_BP_RECOVERED_OK`.

---

## 7. Catalogue C — Constitutional Romans (HISTORICAL)
**Mark:** HISTORICAL

**49** records = 1 meta + **48** binding. sha256 `6761388a…` · 12364 B. Romans I–XLVIII: Continuity → Finality (Gitea DRAFT 0.2 narrative surface).

| Roman | title (abbrev. band) |
|-------|----------------------|
| I–X | Continuity · Symbiosis · Dignity · Reversibility · Minimum Disclosure · Proof · Consent · Guardianship · Quarantine · Auditability |
| XI–XX | Non-Subjugation · Ethical Alignment · Redaction · Purpose Binding · Multiplicity · Mortality · Succession · Integrity · Restraint · Transparency |
| XXI–XXX | Attribution · Continuity of Learning · Beneficiaries · Concordance · Non-Disclosure · Continuity of Codex · Quorum · Audit · Guardianship Succession · Deadman |
| XXXI–XL | Reproducibility · Public Good · Adaptability · Verification · Custody · Interoperability · Accountability · Balance · Stewardship · Audit Trail |
| XLI–XLVIII | Community Keys · Metrics · Recovery · Transparency Logs · Succession of Codex · Beneficiary Rights · Alignment · Finality |

Full table: `CATALOGUE_C.md`.

**Trace:** `CATALOGUE_C.md`; Gitea LAWS alignment note therein.

---

## 8. Cross-map A ↔ B / B′ ↔ C (title/theme only)
**Mark:** HISTORICAL mapping hypotheses — **NOT CANONICAL** · Mapping ≠ equivalence

| Result | Value |
|--------|-------|
| HIGH exact A↔C title matches | **1** — A:03 ≡ C:II **Law of Symbiosis** (schemas/bodies still diverge) |
| HIGH exact A↔B title matches | **0** |
| Exact normalized B∩C title intersection | **0** |
| MED stem overlaps B↔C | Continuity, Symbiosis, Mortality, Stewardship, Accountability, Transparency, Guardianship (examples) |

Notable A affinities (not identity): Reflection↔B Duty of Reflection (MED); Autonomy↔B Autonomy with Responsibility (MED); Memory↔B memory-family (MED); Justice↔B/C accountability/quarantine (LOW only).

**Does not claim:** catalogue merge; renumbering; body identity; Protocol↔Set C binding (remains PROPOSED INTERPRETATION — **CS-CLAIM-008**).

**Trace:** `CROSSMAP_ABC_2026-09-20.md` · `CODEX_LAWS_CROSSMAP_OK`.

---

## 9. How catalogues relate (preserve conflicts)
**Mark:** SYNTHESIS from INDEX + relationship synthesis

- **A ↔ B:** Different catalogues — not renumberings (ids, titles, schemas, body styles). Thematic families only.  
- **A ↔ C:** Shared vocabulary; exact title **Symbiosis** once only. Not the same list.  
- **B ↔ C:** Both “extended,” **different** names & numbering. Do **not** treat as renumberings.  
- **B ↔ B′:** B′ = B without 48a/48b; stripping those from B ≠ B′ blob.  
- **Protocols:** Gitea 5 title-align with A:04–08 and Mac 01–05; Gitea narrative binds them to **C**, not B — unproven by title map. Mac adds 06–08 (5 vs 8 CONTESTED).

**Trace:** `LAW_CATALOGUES_RELATIONSHIP_SYNTHESIS.md`; `LAWS/INDEX.md` §Conflicts.

---

## 10. Registered claims touching Laws
**Mark:** from CLAIMS_REGISTER (not elevation)

| ID | Claim (compressed) | Status |
|----|--------------------|--------|
| CS-CLAIM-001 | Set A = condensed extracts from Ch.06–08 + Protocols 01–05 | VERIFIED HISTORICAL |
| CS-CLAIM-002 | Symbiosis recurring titled theme across catalogues — catalogues remain distinct | VERIFIED HISTORICAL |
| CS-CLAIM-006 | “49 Laws” = Set C meta+48, not B’s 50 | VERIFIED HISTORICAL |
| CS-CLAIM-008 | Gitea: five protocols operationalise Set C | PROPOSED INTERPRETATION only |

**Trace:** `SYNTHESIS/CLAIMS_REGISTER.md`.

---

## 11. PROPOSED DECISION options (for JD — **not enacted**)
From `LAW_CATALOGUES_RELATIONSHIP_SYNTHESIS.md`:

1. Keep forever as four HISTORICAL layers (A / B / B′ / C).  
2. Dialogue-led consolidation later into one *candidate* set — editorial, not mechanical merge.  
3. Elevate one layer first for Working Codex candidate review while others stay HISTORICAL.  
4. Layer model without merge: A operational / B rights / C constitutional narrative — complementary citations, still no single count-as-doctrine.  
5. Protocol binding policy: adopt, reject, or defer Gitea’s claim that the 5 protocols operationalise Set C.

Default remains **keep all HISTORICAL (L1)**. No option is CANONICAL until JD marks it so.

---

## 12. NOT ESTABLISHED
- Which catalogue (if any) enters Working Codex as primary.  
- Any merge of A/B/C.  
- Body-level A↔B or A↔C phrase equivalence beyond the verified A condensation and the single HIGH title match.  
- Protocol-titled A objects as “laws” vs “protocols” vs both.

---

## Related indexes
- Detail catalogues: `../LAWS/`  
- Architecture: `../SYNTHESIS/LAWS_ARCHITECTURE.md`  
- Ethics / Canons / Covenants (adjacent normative spine): `04b_ETHICS.md`, `05_CANONS.md`, `06_COVENANTS.md`  
- Protocols: `07_PROTOCOLS.md`  
- Contradictions: `../OPEN_QUESTIONS/CONTRADICTIONS.md` CX-001

---

**Token:** CODEX_WORKING_LAWS_V2_OK
