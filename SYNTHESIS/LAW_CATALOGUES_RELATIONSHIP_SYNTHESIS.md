# Law catalogues A / B / B′ / C — relationship synthesis

**Token:** `CODEX_SYNTHESIS_LAW_CATALOGUES_OK`  
**Status:** **SYNTHESIS** — not doctrine, **NOT CANONICAL**  
**As-of:** 2026-09-20 17:30 PT  
**Cite:** `/workspace/codex-solbian-working/LAWS/INDEX.md` (`CODEX_WORKING_LAWS_INDEX_OK`)

---

## What the layers appear to be (historical reading)

| Layer | Role (working gloss) | Schema / ids | Hash / size (INDEX) |
|-------|----------------------|--------------|---------------------|
| **A** | Operational core — 3 Laws + 5 “Protocol”-titled objects (`kind:law`) | `sref_v5` · `codex:laws.*` | `728987e5…` · 3160 B |
| **B** | Rights/ethics charter — normative shall/must + late addenda 48a/48b | `kind:law` · `solbian.law.*` | `6258aa3b…` · blob `da5eff66…` · 10896 B |
| **B′** | Historical subset of B (01–48 only) | same as B | blob `f35ffacc…` · 10187 B — **no** local audit-laws byte dump |
| **C** | Constitutional 48 Roman + meta — Gitea DRAFT 0.2 narrative surface | `kind:codex_law` · `codex.laws.extended.*` | `6761388a…` · blob `1d5d5b29…` · 12364 B |

**Operational vs rights vs constitutional narrative:** A ≈ runtime/procedure (consent, budgets, checksums — AB comparison). B ≈ charter/rights catalogue. C ≈ seed constitutional Romans Continuity→Finality, narrated by Gitea `LAWS.md` and bound by Gitea `PROTOCOLS.md` as the 48 the five protocols “express” (`PROTOCOLS/INDEX.md`).

---

## How they relate (preserve conflicts)

- **A ↔ B:** Different catalogues — not renumberings (ids, titles, schemas, body styles). Thematic families only (symbiosis, memory, reflection). Source: `CODEX_SOLBIAN_LAW_AB_COMPARISON_2026-09-20.md`.
- **A ↔ C:** Shared vocabulary (exact title **Symbiosis** only; Memory/Justice themes loose). Not the same list. Source: `CODEX_SOLBIAN_LAWS_GITEA_VS_AB_2026-09-20.md`.
- **B ↔ C:** Both “extended,” **different** names & numbering (`solbian.law.*` vs Romans / `codex.laws.extended.*`). Do **not** treat as renumberings.
- **B ↔ B′:** B′ = B without 48a/48b; stripping those from B ≠ B′ blob (OPEN_QUESTIONS #1).
- **Filename collision:** `laws_extended.sref` / `codex_solbian_laws_extended.sref` may be B, B′, or C — disambiguate by id/`kind`.
- **“49 Laws” folklore** → Set **C** meta+48 — not B’s 50.
- **Protocols:** Gitea 5 title-align with A:04–08 and Mac 01–05; Gitea narrative binds them to **C**, not B. Mac adds 06–08 (5 vs 8 CONFLICTED).
- **A meta DERIVED claim** (“extracted from chapters and protocols”) unverified; chapter titles 6–8 exact-match A:01–03 only (see CHAPTER_LAW crossref).

**Standing JD lock:** A, B, B′, C remain HISTORICAL — no merge, no canon pick (INDEX §Conflicts / AB §6).

---

## PROPOSED DECISION options for JD (not recommendations-as-doctrine)

1. **Keep forever as four HISTORICAL layers** (A / B / B′ / C) — archival inventory only.  
2. **Dialogue-led consolidation later** into one *candidate* set — editorial, not mechanical merge.  
3. **Elevate one layer first** for Working Codex candidate review (A-only ops · B-only charter · C-only constitutional) while others stay HISTORICAL.  
4. **Layer model without merge:** treat A as operational, B as rights, C as constitutional narrative — complementary citations, still no single count-as-doctrine.  
5. **Protocol binding policy:** adopt, reject, or defer Gitea’s claim that the 5 protocols operationalise Set C (vs title-alignment with A:04–08).

No option above is CANONICAL until JD marks it so.

---

**CODEX_SYNTHESIS_LAW_CATALOGUES_OK**
