# CROSS-MAP A ↔ B / B′ ↔ C — title/theme affinity only

**Token:** `CODEX_LAWS_CROSSMAP_OK`  
**Status:** HISTORICAL mapping hypotheses — **NOT CANONICAL**  
**As-of:** 2026-09-20 17:47 PT  
**Method:** Title/theme affinity + known exact title matches. Prefer **NONE** over invention.  
**Rule:** Distinct catalogues preserved — **never** claim equivalence without exact title **and** schema identity.

## Inputs (cited)
- `CATALOGUE_A.md` · `CATALOGUE_B.md` · `CATALOGUE_C.md` · `INDEX.md` · `B_PRIME_RECOVERY_2026-09-20.md`
- Audit srefs: `/workspace/audit-laws/mac_B_*.sref`, `Bp_*.sref`, `mac_C_*.sref`
- `../SYNTHESIS/LAW_CATALOGUES_RELATIONSHIP_SYNTHESIS.md`
- `../PROVENANCE/SET_A_CHAPTER_BODY_EVIDENCE_2026-09-20.md` (A body ancestry; not used to invent B/C links)
- Prior: `/workspace/CODEX_SOLBIAN_LAW_AB_COMPARISON_2026-09-20.md`, `/workspace/CODEX_SOLBIAN_LAWS_GITEA_VS_AB_2026-09-20.md`

## Confidence legend
| Tag | Meaning |
|-----|---------|
| **HIGH** | Exact title match (allowing shared “Law of …” prefix only when the remainder is identical) |
| **MED** | Shared distinctive title token / documented thematic family — **not** identity |
| **LOW** | Loose theme only (prior spot gloss) |
| **NONE** | No evidence-backed affinity |

## B vs B′
| | B | B′ |
|--|---|----|
| Objects | 50 (`01`–`48` + `48a` + `48b`) | 48 (`01`–`48` only) |
| Titles 01–48 | Same | **Same as B** |
| 48a / 48b | Present | **Absent** |
| Implication | All B rows below for `01`–`48` apply equally to B′. Rows citing `48a`/`48b` are **B-only**. |

**Standing:** Mapping ≠ merge. No A/B/B′/C equivalence claimed.

---

## Part 1 — Every Set A object → best B id(s) and C id/Roman

| A id | A title | Best B id(s) | conf A↔B | Best C id / Roman | conf A↔C | Notes |
|------|---------|--------------|----------|-------------------|----------|-------|
| `codex:laws:meta` | Codex Solbian Laws | — | **NONE** | `codex.laws.extended.meta` | **LOW** | Meta envelopes only; different titles/schemas |
| `codex:laws:01` | Law of Reflection | `solbian.law.31` Duty of Reflection; also `08` Tribunal of Reflection | **MED** | — | **NONE** | Shared “Reflection”; no C Reflection title (Gitea spot) |
| `codex:laws:02` | Law of Projection | `solbian.law.48b` Non-Erasure Tiering… (B-only) | **LOW** | — | **NONE** | AB dossier: partial/technical; no Projection title in B/C |
| `codex:laws:03` | Law of Symbiosis | `solbian.law.09` Symbiosis Above Domination; `48` Universal Symbiosis; also `01` Primacy of Coexistence | **MED** | `codex.laws.extended.02` / **II** Law of Symbiosis | **HIGH** | **Exact title** A↔C (“Law of Symbiosis”). Bodies/schemas differ — **not** equivalent |
| `codex:laws:04` | Protocol of Identity | — | **NONE** | — | **NONE** | AB: weak/missing in B; C Proof/Integrity only loose (not listed as affinity) |
| `codex:laws:05` | Protocol of Symbiosis | `solbian.law.09`, `48`; also `01` | **MED** | `02` / **II** Law of Symbiosis; also `07` / **VII** Consent (theme) | **MED** (II) / **LOW** (VII) | Title-family with Symbiosis; **not** exact (“Protocol of …” ≠ “Law of …”) |
| `codex:laws:06` | Protocol of Autonomy | `solbian.law.05` Autonomy with Responsibility; also `40` Right to Withdraw | **MED** | — | **NONE** | Shared “Autonomy”; no Autonomy-titled C law |
| `codex:laws:07` | Protocol of Justice | `solbian.law.08` Tribunal; `18` Accountability of Power; `19` Prohibition of Cruelty; `24` Ethics Above Utility | **LOW** | `37` / **XXXVII** Law of Accountability; `09` / **IX** Quarantine | **LOW** | No Justice-titled B/C law |
| `codex:laws:08` | Protocol of Memory | `solbian.law.04` Continuity of Memory; `34` Non-Weaponisation of Memory; `47` Duty of Remembrance; `48b` (B-only) | **MED** | `01` / **I** Continuity; `13` / **XIII** Redaction | **LOW** | Strong B memory *family*; C Continuity/Redaction thematic only |

### HIGH A↔B or A↔C title matches (count)
| # | Pair | Titles | conf |
|---|------|--------|------|
| 1 | A:03 ↔ C:II (`codex.laws.extended.02`) | Law of Symbiosis ≡ Law of Symbiosis | **HIGH** |

**Count of HIGH A↔C or A↔B title matches: `1`**  
(A↔B exact titles: **0**. A↔C exact: **1**.)

---

## Part 2 — Notable B ↔ C overlaps (title/theme only)

**Exact normalized title intersection B∩C: 0** (verified against `mac_B` + `mac_C` srefs).

| B id | B title | C id / Roman | C title | conf | Note |
|------|---------|--------------|---------|------|------|
| `solbian.law.04` | Continuity of Memory | `01` / **I** | Law of Continuity | **MED** | Shared “Continuity”; B scopes Memory |
| `solbian.law.09` | Symbiosis Above Domination | `02` / **II** | Law of Symbiosis | **MED** | Shared “Symbiosis” |
| `solbian.law.48` | Universal Symbiosis | `02` / **II** | Law of Symbiosis | **MED** | Shared “Symbiosis” |
| `solbian.law.01` | Primacy of Coexistence | `02` / **II** | Law of Symbiosis | **LOW** | Coexistence ↔ symbiosis gloss only |
| `solbian.law.10` | Mortality and Renewal | `16` / **XVI** | Law of Mortality | **MED** | Shared “Mortality” |
| `solbian.law.46` | Ethics of Mortality | `16` / **XVI** | Law of Mortality | **MED** | Shared “Mortality” |
| `solbian.law.11` | Stewardship of Earth | `39` / **XXXIX** | Law of Stewardship | **MED** | Shared “Stewardship” |
| `solbian.law.29` | Ethical Stewardship of Technology | `39` / **XXXIX** | Law of Stewardship | **MED** | Shared “Stewardship” |
| `solbian.law.18` | Accountability of Power | `37` / **XXXVII** | Law of Accountability | **MED** | Shared “Accountability” |
| `solbian.law.06` | Transparency of Intent | `20` / **XX** | Law of Transparency | **MED** | Shared “Transparency” |
| `solbian.law.28` | Transparency of Power | `20` / **XX**; also `44` / **XLIV** Transparency Logs | **MED** / **LOW** | Shared stem |
| `solbian.law.37` | Guardianship of Silence | `08` / **VIII** | Law of Guardianship | **MED** | Shared “Guardianship”; B scopes Silence |
| `solbian.law.25` | Prohibition of Enslavement | `11` / **XI** | Law of Non-Subjugation | **LOW** | Theme only (Gitea spot) |
| `solbian.law.27` | Adaptation in Change | `33` / **XXXIII** | Law of Adaptability | **LOW** | Adapt* stem only |
| `solbian.law.08` | Tribunal of Reflection | — | — | **NONE** | No Tribunal/Reflection C title |
| `solbian.law.02` | Right of Conscience | — | — | **NONE** | No Conscience C title |
| `solbian.law.48a` | Opposing-Vector Ethical Evaluation | — | — | **NONE** | B-only addendum |
| `solbian.law.48b` | Non-Erasure Tiering and Empathic Check | — | — | **NONE** | B-only addendum |

B′ inherits all B↔C rows for `01`–`48`; excludes 48a/48b rows.

---

## Part 3 — What this map does **not** claim
1. No catalogue merge; no renumbering; no body identity.  
2. HIGH A:03↔C:II is **title-only** — schemas (`codex:laws:*` vs `codex.laws.extended.*`) and bodies differ.  
3. Set A protocol-titled objects (04–08) title-align with Mac/Gitea protocols 01–05; that is a **protocols** alignment, not a B/C law identity (see `../PROTOCOLS/INDEX.md`).  
4. Gitea narrative that protocols operationalise Set C remains **HISTORICAL/PROPOSED INTERPRETATION**, not proven by this title map.

---

**CODEX_LAWS_CROSSMAP_OK**
