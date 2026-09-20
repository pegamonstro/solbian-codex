# WORKING_CODEX_ARCHITECTURE_REVIEW
**Track:** Wave 3 · T15 · Track E architecture  
**STATUS:** AUDIT / WORKING · **CANONICAL:** NONE  
**As-of:** 2026-09-20 ~21:10 PT  
**Scope:** `CURRENT_WORKING_CODEX/` (00–12, NAV, OUTLINE) against historical corpus + Wave 3 AUDIT deliverables already present  
**Rule:** Review only. **Do not** auto-implement restructuring. Prefer NOT ESTABLISHED over invention.  
**Token:** `CODEX_WAVE3_ARCH_REVIEW_OK`

---

## 0. Method & sources read

| Layer | Artefacts used |
|-------|----------------|
| Working Codex | `00_README`, `01_WHAT_IS_CODEX_SOLBIAN`, `02_ORIGIN_AND_HISTORY`, `03_FOUNDATIONAL_CONCEPTS`, `04_LAWS`, `04b_ETHICS`, `05_CANONS`, `06_COVENANTS`, `07_PROTOCOLS`, `08_SCROLLS`, `09_CHAPTERS`, `10_DIALOGUE_AND_METHOD`, `11_GLOSSARY`, `12_OPEN_QUESTIONS`, `NAV.md`, `OUTLINE.md` |
| AUDIT (skim) | Traceability · Stealth · WHAT_IS · Ontology · Ethics · Social · Laws · Protocols · Scroll themes · Scroll 20 · Intellectual development |
| Contrast | `SYNTHESIS/HISTORICAL_ARCHITECTURE` · chapter/law/protocol architecture synths |

**Epistemic frame:** Working Codex = **hypothesis under audit**, not adopted doctrine. Strength of prose ≠ strength of authority (`STEALTH_CANONICALITY`).

---

## 1. Current structure

### 1.1 Linear Working Codex sequence (00–12)

| # | Slot | Actual role in tree | Genre (working gloss) |
|---|------|---------------------|------------------------|
| 00 | README | Entry + reading rules | Meta / orientation |
| 01 | What Codex Solbian is | Identity, independence, Word+Journey pointer | Definitional / governance-framed SYNTHESIS |
| 02 | Origin and history | Governance locks + recovery events + layer diagram | **Project / recovery history**, not founding myth |
| 03 | Foundational concepts | Attested concept inventory; sovereignty NOT ESTABLISHED | Concept register (thin bodies) |
| 04 | Laws | Contested A / B / B′ / C; no pick | Normative catalogues (multi-genre) |
| 04b | Ethics | ETHICS seed framing + Canons + Pillars + Triadic overview | Normative umbrella (SOURCE pointer) |
| 05 | Canons | Five Ethical Canons (SOURCE extract) | Subset of ETHICS §1 |
| 06 | Covenants | Pillars + Triadic (+ Ch.04 sibling note) | Subset of ETHICS §2–3 + chapter sibling |
| 07 | Protocols | 5 vs 8 surfaces; Mac≡seed 01–05 | Procedural / runtime HISTORICAL |
| 08 | Scrolls | MD≠sref; deep theses 01–50 | Doctrinal expansions + **developmental genre arc** |
| 09 | Chapters | 30 titles; Ch.06–08→A verified | Discursive / narrative units |
| 10 | Dialogue and Method | Dialogue SOURCE + Phase A PROPOSED | Journey + pipeline (not ontology) |
| 11 | Glossary | Pointer to 76 titles | Lexicon index |
| 12 | Open questions | WAVE1 + contradictions digest | Contested / unresolved |

### 1.2 Parallel corpus layout (outside Working Codex)

Sibling directories preserve **Word** artefacts (`LAWS/`, `SCROLLS/`, `CHAPTERS/`, `PROTOCOLS/`, `ETHICS/`, `CANONS/`, `COVENANTS/`, `GLOSSARY/`) and **Journey** surfaces (`DIALOGUE/`, `PROVENANCE/`, `OPEN_QUESTIONS/`, `meta/`, `AUDIT/`, `SYNTHESIS/`). NAV correctly routes “what is historical vs reconstructed vs working vs proposed vs disputed.”

### 1.3 Implied hierarchy (SYNTHESIS only)

Working `02` and `HISTORICAL_ARCHITECTURE` show:

```
DIALOGUE → CHAPTERS → SCROLLS → LAWS (A/B/B′/C) → PROTOCOLS
         ↘ ETHICS → Canons + Covenant → Glossary
```

This is an **analytical stack**, repeatedly labelled non-binding — but it is the intellectual picture readers absorb from reading order 01→09.

---

## 2. Strengths

1. **Epistemic labelling is first-class.** HISTORICAL / SOURCE / SYNTHESIS / WORKING / CONTESTED / NOT ESTABLISHED / PROPOSED appear consistently; stubs archived; tokens and Trace blocks support later audit.
2. **Hard locks preserved.** A/B/B′/C unmerged; Protocols 5↔8 uncollapsed; MD≠sref scroll numbering; Ch.04 Covenant ↔ ETHICS Covenant “do not merge”; no silent CANONICAL.
3. **Word + Journey structurally present.** Dialogue (§10) + Open Questions (§12) + PROVENANCE/OPEN_QUESTIONS/meta sit beside Law/Scroll/Chapter inventories; Master Consolidation rule is restated in `01`/`02`.
4. **Contestation is visible, not papered over.** `04_LAWS`, `07_PROTOCOLS`, `08_SCROLLS`, `12_OPEN_QUESTIONS` and CX-001…004 make multiple formulations legible to a careful reader.
5. **Provenance scaffolding for future canonisation.** Catalogue-letter + schema authority; stub archives; claims register / body-evidence paths; Phase A pipeline (PROPOSED) separates draft → review → CANONICAL metadata — JD can elevate **without rewriting the archive** if Working remains a pointer layer.
6. **Laws prominence matches corpus density.** Multi-catalogue treatment and “49≠50≠8” folklore resolution are among the strongest Working sections.
7. **Chapters correctly framed as discursive**, with the one verified crystallisation path (Ch.06–08 → A:01–03) marked VERIFIED rather than hierarchy-of-canon.

---

## 3. Weaknesses (mapped to Wave 3 §§17 criteria)

### 3.1 Does structure reflect intellectual structure?

**Partially — misaligned in order and nesting.**

Intellectual-development audit (chapters-as-evidence) suggests a **problem → concept → discursive Law → operational digest → rights/constitutional genres → scroll expansions → ETHICS crystallisation (2026-02-20 stamp)** picture, with Dialogue as journey (causality to chapters UNKNOWN).

Working sequence instead fronts **identity → recovery history → concepts → Laws → Ethics umbrella → Canons → Covenants → Protocols → Scrolls → Chapters → Dialogue**. That reads like a **doctrine handbook** (Laws early; Chapters/Dialogue late) rather than the attested developmental arc (Chapters/Dialogue early as generative surfaces; Laws as condensations; Scrolls as expansions with their own genre arc).

The ASCII stack in `02` also risks looking like a binding pyramid (stealth hit S-021).

### 3.2 Ethics vs Canons separation artificial?

**Yes — structurally artificial; content-wise overlapping.**

Historically, Five Canons + Pillars + Triadic live **inside one ETHICS SOURCE body**. Working splits them across **04b + 05 + 06**, with substantial duplicated imperative tables. Readers may infer three peer “books of doctrine” rather than one ETHICS surface with extractable parts plus a chapter sibling (Ch.04).

Audit `ETHICAL_STRUCTURE` further shows Canons are **not** the whole ethical vocabulary (consent, non-domination, stewardship, etc. recur across scrolls/laws). Splitting Canons out elevates one stack relative to that wider primitive field.

### 3.3 Laws prominence?

**Appropriate as contested multi-catalogue, but over-weighted as early “main law book.”**

Prominence is justified by corpus volume and JD locks. Weakness: placing Laws at §04 **before** Chapters/Scrolls/Dialogue hides that Set A is largely **condensation of chapters/protocols**, and that B/C are distinct genres — so “Laws” can be misread as the primary generative layer rather than one of several normative surfaces.

### 3.4 Scrolls as doctrine vs developmental?

**Working Codex treats Scrolls mainly as contested inventory + deep theses (doctrine catalogue); thematic audit shows a developmental genre arc.**

`SCROLL_THEMATIC_EVOLUTION`: 01–07 short foundations → 08–15 essays → 16–40 structured S.E.E.D. ops → 41–50 poetic-legal covenant/custody — **source-genre arc, not supersession**. Working `08` documents MD≠sref and theses well but does **not** foreground that developmental reading; a new reader may treat 50 scrolls as a flat canonical series.

### 3.5 Chapters mistaken for canon sections?

**Risk is moderate and partly mitigated.**

`09` correctly says discursive/narrative, movements NOT ESTABLISHED, hierarchy NOT ESTABLISHED. Residual risks: (a) Ch.06–08 **titles** “Law of …” sit next to Law catalogues; (b) Ch.10–20 embed intra-chapter Law/Protocol/Covenant micro-pipelines that can be confused with Mac Protocols / ETHICS Covenant; (c) late placement after Canons/Laws invites reading chapters as **commentary on already-settled canons** rather than generative discursive evidence.

### 3.6 Origin vs doctrine?

**Mostly clear; residual conflation risk.**

`02` explicitly refuses founding myth and separates governance origin locks, corpus architecture, and 2026-09 recovery events. Weakness: Constitution §1 definitional sentence is repeated across `01`/`02` and can feel like **doctrinal creed** (stealth S-001/S-002) rather than project-governance framing. ETHICS “Golem as Machina Partner” seed title in `04b` can blur independence lock if fences drop.

### 3.7 Concepts representation?

**Under-powered relative to ontology/ethics audits.**

`03` + `11` are honest (titles, NOT ESTABLISHED sovereignty, no invented bodies) but:
- No dedicated ontology slot (noted in `10`: outline once meant Ontology).
- Relational ontology (continuity, synthetic conscience, Bridge, memory-as-substrate) is richer in AUDIT ontology/ethics than in Working §03.
- Concepts appear **before** the discursive surfaces that generate them — reverse of intellectual development.

### 3.8 Unresolved tensions visible?

**Yes for structural contests; weaker for philosophical tensions.**

Visible: CX-001…004, catalogue/protocol/scroll contests, open JD items in §12. Weaker: scroll-level unresolved poles (forgetting vs immutable ledger; councils vs guardians; freedom–structure vs dense regulation — per scroll themes) are mostly **outside** Working Codex prose; `12` still says body-level philosophical contradictions “to be filled.” Stealth audit: architecture glosses can sound settled while forks remain open.

### 3.9 Historical vs synthetic clear to a new reader?

**Clear if they read NAV + labels; easy to miss if they only read fluent V2 prose.**

Headers say CANONICAL: NO; NAV table is excellent. Risks: long SOURCE imperative blocks in `04b`/`05`/`06` without constant “SOURCE quote / Working elevation NOT ESTABLISHED” fences; “normative spine,” “operational core,” “runtime layer” glosses (stealth top hits); stub vs V2 dual files can confuse which is current.

### 3.10 Traceability of claims?

**Strong scaffolding; uneven enforcement.**

Per-section SOURCE BASIS + Trace; Wave 3 T1 registers ~48 propositions; Set A body evidence VERIFIED. Gaps: some Working glosses still outrun attestation (complementary A/B/C audience model = SYNTHESIS only); scroll deep theses can read as “Codex teaches”; Constitution multi-aspect list truncation easy to miss.

### 3.11 Can JD canonize later without rewriting archive?

**Yes — if Working stays a non-authoritative pointer/synthesis layer.**

Archive (sibling HISTORICAL trees, stubs, provenance, epistemic metadata, Phase A PROPOSED pipeline) supports elevation by **status metadata / selection**, not rewrite. Threats to that property: (a) merging catalogues in place; (b) deleting contested alternatives; (c) replacing SOURCE with paraphrased Working voice; (d) renumbering scrolls by ordinal “fix.” Current locks resist (a)–(d); restructuring that collapses 04b/05/06 or reorders files is fine **only** if done non-destructively (pointers, redirects, stubs kept).

### 3.12 Word vs Journey preserved?

**Yes at project scale; Journey is under-weighted in the linear Working read.**

Word artefacts dominate §§04–09. Journey appears late (§10) and as digests (§12). Dialogue bodies remain private/not composed — correct — but a new reader of Working alone meets doctrine surfaces long before journey. Intellectual structure would put Journey/Chapters earlier as **generative context**, with Word digests following.

---

## 4. Proposed changes (**non-destructive only**)

Do **not** merge catalogues, collapse protocols, rewrite SOURCE, or elevate anything. Optional later JD-approved editorial moves:

### P1 — Reorder reading path (NAV/OUTLINE first; files may stay numbered)

Add an explicit **“Intellectual reading order”** in `NAV.md` / `00_README` that does not require renumbering:

1. NAV + 00  
2. 01 What-is (identity fences)  
3. 10 Dialogue & Method (Journey / pipeline)  
4. 09 Chapters (discursive generation)  
5. 08 Scrolls (**with genre-arc pointer** to AUDIT thematic evolution)  
6. 03 Concepts (after generative surfaces)  
7. 04 Laws / 07 Protocols (as condensations & contested catalogues)  
8. 04b Ethics as **single normative umbrella**; 05/06 as **extract annexes**  
9. 02 Origin/recovery (meta-history of the project)  
10. 11 Glossary · 12 Open questions  

Keep current filenames for stability; change **recommended path**, not archive identity.

### P2 — Demote artificial Ethics/Canons/Covenants split (pointers, not deletion)

- Treat `04b_ETHICS.md` as the **primary Working ethics map**.  
- Make `05_CANONS` / `06_COVENANTS` thin **annex pointers** (names + link to ETHICS extract + “do not elevate”) rather than parallel full restatements — **archive full V2 text into stubs or SYNTHESIS**, do not destroy.  
- Add one-line standing: “Canons/Covenant are ETHICS-internal strata + Ch.04 sibling; not peer ‘books’ to Laws.”

### P3 — Reframe Scrolls & Chapters as developmental / generative

- In `08_SCROLLS`, add a short **genre-arc** subsection (01–07 / 08–15 / 16–40 / 41–50) citing `AUDIT/SCROLL_THEMATIC_EVOLUTION.md` — descriptive, not supersession.  
- In `09_CHAPTERS`, lead with “generative discursive evidence; not canon sections”; keep verified A condensation in a clearly labelled **downstream digest** box.  
- Cross-link `03` concepts **to** chapter/scroll attestations rather than presenting concepts as prior axioms.

### P4 — Soften stealth-canonical glosses (editorial, in place)

Reuse stealth soft phrases: attribute Constitution/ETHICS quotes; mark “Working gloss”; avoid “normative spine / absolute foundation” in unfenced Working voice; keep architecture stack labelled SYNTHESIS-only.

### P5 — Surface philosophical tensions in §12 (pointer expansion)

Non-blocking digest rows pointing to scroll-theme unresolved poles + AUDIT contradictions — still **not** inventing conflict narratives.

### P6 — Canonisation readiness checklist (meta only)

Document in NAV or a one-page AUDIT annex: elevation = JD metadata on chosen artefacts; retain losers as HISTORICAL; never overwrite SOURCE; Working may gain “adopted pointer” banners without deleting contested sections.

---

## 5. Justification

| Proposal | Why |
|----------|-----|
| P1 reading order | Aligns reader path with INTELLECTUAL_DEVELOPMENT + HISTORICAL_ARCHITECTURE without breaking file IDs or tokens. |
| P2 ethics annexing | Removes artificial peer-book illusion; matches SOURCE nesting; reduces duplicate stealth-canonical restatement. |
| P3 scrolls/chapters | Matches thematic evolution + chapter evidence roles; reduces “chapters = canon commentary” and “scrolls = flat doctrine list” errors. |
| P4 stealth soften | Traceability/stealth audits show prose strength outrunning authority marks. |
| P5 tensions | Makes unresolved poles visible to new readers without forcing NORMATIVE picks. |
| P6 checklist | Answers “canonize later without rewriting archive” with an explicit non-destructive path. |

**Non-justified (explicitly rejected here):** merging A/B/B′/C; picking Protocols 5 or 8; renumbering scrolls to force MD≡sref; inventing ontology file as doctrine; reconstructing Constitution §§2–34; auto-implementing any restructure in this Wave.

---

## 6. Confidence

| Judgment | Confidence | Notes |
|----------|------------|-------|
| Ethics/Canons/Covenants split is artificial relative to SOURCE | **High** | Single ETHICS body; Working duplicates |
| Linear 00–12 ≠ intellectual generative order | **High** | Chapters→A verified; Dialogue early in pipeline; Working puts Laws early |
| Laws multi-catalogue prominence is warranted | **High** | Corpus + locks; AUDIT laws conclusion |
| Scrolls need developmental framing, not only inventory | **High** | Thematic evolution genre arc |
| Chapters not currently labelled as canons, but placement risks misread | **Medium–High** | Mitigations exist in `09` |
| Origin vs doctrine mostly separated | **High** | `02` scope rules clear |
| Concepts under-represent relational ontology | **Medium** | AUDIT ontology richer; Working honest but thin |
| Tensions: structural yes / philosophical partial | **High** | §12 + CX vs scroll poles |
| New reader can confuse SYNTHESIS for doctrine if skimming | **High** | Stealth catalogue |
| JD can canonize without archive rewrite **if locks held** | **High** | Pointer architecture + stubs + provenance |
| Word+Journey preserved at project scale; Journey under-weighted in Working linear read | **High** | §10 late |
| Any specific new numbering scheme as “correct” | **Low / NOT ESTABLISHED** | No CANONICAL outline from JD |

**Overall review confidence:** **High** for diagnosis; **Medium** for exact future outline numbering (JD decision).

---

## 7. Top structural recommendations (summary)

1. **Keep filenames; change the recommended intellectual reading order** so Dialogue/Chapters/Scrolls precede Laws/Canons as generative context (P1).  
2. **Collapse Ethics presentation to one umbrella + annex pointers** for Canons/Covenants without deleting SOURCE extracts (P2).  
3. **Frame Scrolls as genre-developmental and Chapters as discursive generators**, not flat doctrine / canon commentary (P3).

---

## Trace

- Working: `CURRENT_WORKING_CODEX/00`–`12`, `NAV.md`, `OUTLINE.md`  
- AUDIT: `WAVE3_PROPOSITION_TRACEABILITY`, `STEALTH_CANONICALITY`, `WHAT_CODEX_SOLBIAN_IS`, `ONTOLOGICAL_STRUCTURE`, `ETHICAL_STRUCTURE`, `SOCIAL_AND_GOVERNANCE_STRUCTURE`, `LAW_SETS_SEMANTIC_COMPARISON`, `PROTOCOL_SETS_SEMANTIC_COMPARISON`, `SCROLL_THEMATIC_EVOLUTION`, `SCROLL_20_ANOMALY`, `INTELLECTUAL_DEVELOPMENT`  
- Synth contrast: `SYNTHESIS/HISTORICAL_ARCHITECTURE_2026-09-20.md`

**CANONICAL: NONE. No restructuring implemented.**

**CODEX_WAVE3_ARCH_REVIEW_OK**
