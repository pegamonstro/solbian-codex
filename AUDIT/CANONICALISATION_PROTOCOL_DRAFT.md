# CANONICALISATION_PROTOCOL_DRAFT
**STATUS:** DRAFT for **FUTURE consideration only** · **CANONICAL:** NONE  
**Track:** Wave 4 · Track B · W4-12  
**As-of:** 2026-09-20 ~21:40 PT  
**Rule:** Define **questions and options**, not assumed answers. **Do not execute.** No infrastructure implementation. Silence ≠ consent.

**Token:** `CODEX_WAVE4_CANON_PROTOCOL_DRAFT_OK`

---

## 0. Frame

This file is **not** a live protocol. It does not elevate any artefact. It inventories decision *spaces* JD (and future reviewers) may later close. Related but distinct: Phase A step 7 (PROPOSED method) and Master Consolidation §§6, 20, 28, 35 (governance locks).

**Hard locks that any future protocol must respect unless JD explicitly amends governance:**
- No silent historical→canonical conversion.  
- A / B / B′ / C unmerged unless JD authorizes a *new* candidate set (not a quiet merge).  
- Protocols 5↔8 preserved until equivalence proven.  
- Grid / Igor out of Codex pipeline.  
- Filesystem path ≠ authority.

---

## 1. What does “canonical” mean?

**Question:** Which sense(s) of CANONICAL should the project adopt?

| Option id | Option (not ranked) | Notes / tensions |
|-----------|---------------------|------------------|
| Q1-a | **Binding doctrine** for Solbian practice / interpretation | Strongest; needs clear scope (who is bound?) |
| Q1-b | **Editorial current text** — “read this wording first” without civilisational binding | Weaker; may still stealth-elevate |
| Q1-c | **Publication class** — approved for public Word surface | Orthogonal to binding force |
| Q1-d | **Multi-tag** — separate flags: `binding`, `current_text`, `public`, `liturgical` | More precise; heavier process |
| Q1-e | Reserve CANONICAL only for **explicit JD metadata**; everything else stays WORKING/HISTORICAL/CANDIDATE | Matches present lock |

**Open sub-questions:** Does CANONICAL apply to whole documents, atomic claims, or both? Can a document be partly canonical?

---

## 2. Who elevates?

**Question:** Who may set `status: CANONICAL`?

| Option id | Option |
|-----------|--------|
| Q2-a | JD alone |
| Q2-b | JD + optional Solace review (Phase A wording) |
| Q2-c | JD + named human co-reviewer(s) |
| Q2-d | Quorum of designated stewards (future) |
| Q2-e | Synthetic agents may **draft elevation proposals only** — never flip the bit |

**Open sub-questions:** Emergency freeze / veto? Can elevation be delegated? Is silence ever consent? (**Present governance: silence ≠ consent.**)

---

## 3. What evidence is required before elevation?

**Question:** Minimum evidence packet for a Candidate → Canonical proposal?

| Option id | Evidence element | Required? (to decide later) |
|-----------|------------------|-----------------------------|
| Q3-a | Provenance pointers (path, hash, schema/id) | |
| Q3-b | SOURCE quotations or verified condensation chain | |
| Q3-c | Explicit list of **rejected alternatives** (Journey) | |
| Q3-d | Contradiction register impact analysis | |
| Q3-e | Dialogue week links **or** explicit “undiscussed” mark (§16) | |
| Q3-f | Cross-catalogue non-collision check (esp. Laws/Protocols) | |
| Q3-g | Redaction / publication review if public | |
| Q3-h | Statement of scope (what is *not* elevated nearby) | |

**Open sub-questions:** Different evidence bars for glossary term vs Law vs ETHICS pillar? May SYNTHESIS-only claims ever become canonical without new SOURCE?

---

## 4. Preserving historical alternatives

**Question:** How must non-chosen formulations survive elevation?

| Option id | Option |
|-----------|--------|
| Q4-a | Immutable archive blobs + catalogue letters unchanged |
| Q4-b | `history/superseded/` copies with reason codes |
| Q4-c | Inline “MULTIPLE FORMULATIONS” sections in Working Codex even after one is canonical |
| Q4-d | Journey digest (redacted) citing abandoned ideas without promoting them |
| Q4-e | Forbid deletion of HISTORICAL Layer-1 sources under all options |

**Open sub-questions:** Are B′ and Mac Protocol 06–08 “alternatives” or “other catalogues”? (Likely: keep as HISTORICAL surfaces, not “losers.”)

---

## 5. Amendments

**Question:** After elevation, how may text change?

| Option id | Option |
|-----------|--------|
| Q5-a | Amendments require same evidence bar as initial elevation |
| Q5-b | Typo/errata track vs substantive amendment track |
| Q5-c | Amendment must record WHAT/WHY/WHEN/WHO/previous formulation (Master Consolidation §31) |
| Q5-d | Temporary WORKING overlay allowed without touching canonical bit |
| Q5-e | No silent AI cleanup (§23) — editorial diff must be visible |

---

## 6. Supersession

**Question:** When canonical text B replaces canonical text A?

| Option id | Option |
|-----------|--------|
| Q6-a | A → SUPERSEDED; B → CANONICAL; A retained immutable |
| Q6-b | Version graph (A v1, v2) without “superseded” semantics |
| Q6-c | Parallel canonicity forbidden (only one current per `slot_id`) |
| Q6-d | Parallel canonicity allowed for distinct slots (e.g. Law-A-ops vs Covenant) |
| Q6-e | Supersession reason taxonomy: correction / development / conflict-resolution / scope-split |

**Open sub-questions:** Can Journey materials be “superseded,” or only Word?

---

## 7. Provenance requirements (standing)

**Question:** What provenance must cling to canonical artefacts forever?

| Option id | Option |
|-----------|--------|
| Q7-a | Hash + source path(s) + elevation event record |
| Q7-b | Link to Candidate packet id |
| Q7-c | Link to Journey pointers (optional body) |
| Q7-d | Machine-readable frontmatter status fields (Phase A sketch) — **schema TBD, not implemented here** |
| Q7-e | Prefer existing id schemes (`codex:laws.*`, Romans, sref ids) over new competing namespaces (§22) |

---

## 8. Disagreements

**Question:** How to treat unresolved disagreement at elevation time?

| Option id | Option |
|-----------|--------|
| Q8-a | **Block** elevation until JD resolves |
| Q8-b | Elevate one formulation; mark dissent CONTESTED in Journey register |
| Q8-c | Elevate a **disjunction** (“Canonical conflict record”) — rare |
| Q8-d | Split slot into two scoped canonical texts |
| Q8-e | Return to WORKING / CANDIDATE; publish Open Question |

**Present stop condition (Master Consolidation §35):** substantive philosophical conflicts and choosing between equally supported historical formulations require human review — not autonomous resolution.

---

## 9. Word / Journey coexistence under canonicity

**Question:** How do dual layers behave after some Word is canonical?

| Option id | Option |
|-----------|--------|
| Q9-a | Canonical Word cites Journey by pointer only |
| Q9-b | Journey never carries CANONICAL bit (asymmetric authority) |
| Q9-c | Public Word / private Journey split |
| Q9-d | Canonical amendments must update Journey supersession log |
| Q9-e | “Undiscussed canonical” allowed only with explicit UNKNOWN dialogue link |

See `WORD_AND_JOURNEY.md` — **do not turn Journey into canon by preservation.**

---

## 10. Immutable vs amendable vs versioned

**Question:** Which mutability class for which layer?

| Layer / class | Candidate policy options (choose later) |
|---------------|----------------------------------------|
| HISTORICAL Layer-1 sources | Immutable bytes; replace only by adding new objects |
| Reconstructed artefacts | Versioned; provenance-mandatory |
| SYNTHESIS | Amendable; must remain labelled SYNTHESIS |
| WORKING Codex | Versioned evolving; not automatically canonical |
| CANDIDATE | Mutable until review freeze |
| CANONICAL | Choose: **immutable until supersession** vs **in-place amendable with audit** vs **versioned canonical line** (Q10-a/b/c) |

| Option id | Canonical mutability model |
|-----------|----------------------------|
| Q10-a | Immutable object + superseding object |
| Q10-b | Single object amendable with signed amendment log |
| Q10-c | Version line `canonical@vN` always pointing “current” |
| Q10-d | Hybrid: normative sentences immutable; commentary amendable |

---

## 11. Explicit non-goals of this draft

- Does not run Phase A step 7.  
- Does not create schemas, DB, or elevation UI.  
- Does not pick among Law catalogues or Protocol counts.  
- Does not treat preservation of alternatives as ranking or “winner.”

---

## 12. Possible next governance steps (only if JD asks)

1. Answer Q1–Q2 first (meaning + who).  
2. Map answers onto Phase A step 7 or replace Phase A.  
3. Pilot on **one** low-stakes Candidate (e.g. a glossary disambiguation), not Laws.  
4. Reconcile with missing Constitution §§2–34 when recovered.

Until then: **CANONICAL: NONE**.

---

**CODEX_WAVE4_CANON_PROTOCOL_DRAFT_OK**
