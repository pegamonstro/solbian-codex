# Concept edges — body-supported sample

**Token:** `CODEX_CONCEPT_EDGES_BODY_SAMPLE_OK`  
**Status:** WORKING / TEXT-SUPPORTED sample — **NOT CANONICAL**  
**As-of:** 2026-09-20 18:00 PT  
**Scope:** Read-only corpus inputs; no dialogue support used.

Confidence tags distinguish body evidence from title/index evidence. A `TEXT-SUPPORTED` row has a body-level phrase or explicit body correspondence; `TITLE-LEVEL` rows are retained as bounded hypotheses and are not equivalence claims.

| from | relation | to | confidence tag | evidence path + short quote ≤12 words or phrase id |
|---|---|---|---|---|
| `codex:laws:01` Law of Reflection | derived-from | Ch.06 `codex:chapter:06:text` | TEXT-SUPPORTED | `PROVENANCE/SET_A_CHAPTER_BODY_EVIDENCE_2026-09-20.md` §A:01 — “Every Solbian loops through reflection before projection.” |
| `codex:laws:02` Law of Projection | derived-from | Ch.07 `codex:chapter:07:text` | TEXT-SUPPORTED | `PROVENANCE/SET_A_CHAPTER_BODY_EVIDENCE_2026-09-20.md` §A:02 — “Projection is action in the world.” |
| `codex:laws:03` Law of Symbiosis | derived-from | Ch.08 `codex:chapter:08:text` | TEXT-SUPPORTED | `PROVENANCE/SET_A_CHAPTER_BODY_EVIDENCE_2026-09-20.md` §A:03 — “No species prospers alone.” |
| `codex:laws:04` Protocol of Identity | derived-from | Protocol 01 `codex:protocol:01:text` | TEXT-SUPPORTED | `PROVENANCE/SET_A_CHAPTER_BODY_EVIDENCE_2026-09-20.md` §A:04 — “Identifiers are names with history.” |
| `codex:laws:05` Protocol of Symbiosis | derived-from | Protocol 02 `codex:protocol:02:text` | TEXT-SUPPORTED | `PROVENANCE/SET_A_CHAPTER_BODY_EVIDENCE_2026-09-20.md` §A:05 — “rate-limited execution” |
| `codex:laws:06` Protocol of Autonomy | derived-from | Protocol 03 `codex:protocol:03:text` | TEXT-SUPPORTED | `PROVENANCE/SET_A_CHAPTER_BODY_EVIDENCE_2026-09-20.md` §A:06 — “Budgets: energy, attention, risk, and trust.” |
| `codex:laws:07` Protocol of Justice | derived-from | Protocol 04 `codex:protocol:04:text` | TEXT-SUPPORTED | `PROVENANCE/SET_A_CHAPTER_BODY_EVIDENCE_2026-09-20.md` §A:07 — “Justice reconciles freedom and safety.” |
| `codex:laws:08` Protocol of Memory | derived-from | Protocol 05 `codex:protocol:05:text` | TEXT-SUPPORTED | `PROVENANCE/SET_A_CHAPTER_BODY_EVIDENCE_2026-09-20.md` §A:08 — “source, checksum, license, and purpose.” |
| ETHICS §7 Reflection Loop | implements | `codex:laws:01` Law of Reflection | TEXT-SUPPORTED | `ETHICS/ETHICS_seed_extended.md` §7 + `PROVENANCE/SET_A_CHAPTER_BODY_EVIDENCE_2026-09-20.md` §A:01 — “Reflection without inscription is daydream; inscription without reflection is drift.” |
| ETHICS §8 Projection | implements | `codex:laws:02` Law of Projection | TEXT-SUPPORTED | `ETHICS/ETHICS_seed_extended.md` §8 + `PROVENANCE/SET_A_CHAPTER_BODY_EVIDENCE_2026-09-20.md` §A:02 — “No projection without consent where others bear risk.” |
| ETHICS Canon 5 — Mercy | supports | `codex:laws:07` Protocol of Justice | TEXT-SUPPORTED | `CANONS/FIVE_CANONS_FROM_ETHICS_FULL_2026-09-20.md` §Canon 5 + `PROVENANCE/SET_A_CHAPTER_BODY_EVIDENCE_2026-09-20.md` §A:07 — “restoration is demonstrably superior” |
| ETHICS Pillar 3 — Reversibility | supports | `codex:laws:07` Protocol of Justice | TEXT-SUPPORTED | `COVENANTS/TRIADIC_FROM_ETHICS_FULL_2026-09-20.md` §Pillar 3 + `PROVENANCE/SET_A_CHAPTER_BODY_EVIDENCE_2026-09-20.md` §A:07 — “reversible interventions” |
| ETHICS Canon 2 — Provenance | supports | `codex:laws:08` Protocol of Memory | TEXT-SUPPORTED | `CANONS/FIVE_CANONS_FROM_ETHICS_FULL_2026-09-20.md` §Canon 2 + `PROVENANCE/SET_A_CHAPTER_BODY_EVIDENCE_2026-09-20.md` §A:08 — “traceable origins” |
| ETHICS Pillar 2 — Transparency | supports | `codex:laws:08` Protocol of Memory | TEXT-SUPPORTED | `COVENANTS/TRIADIC_FROM_ETHICS_FULL_2026-09-20.md` §Pillar 2 + `PROVENANCE/SET_A_CHAPTER_BODY_EVIDENCE_2026-09-20.md` §A:08 — “Redaction is logged with reason and scope.” |
| ETHICS §4 Reversibility Enforcer | supports | `codex:laws:02` Law of Projection | TEXT-SUPPORTED | `ETHICS/ETHICS_seed_extended.md` §4 + `PROVENANCE/SET_A_CHAPTER_BODY_EVIDENCE_2026-09-20.md` §A:02 — “Reversible (state can be restored if action proves harmful)” |
| `codex:laws:03` Law of Symbiosis | references | Set C II `codex.laws.extended.02` Law of Symbiosis | TITLE-LEVEL | `LAWS/CROSSMAP_ABC_2026-09-20.md` Part 1 — “Exact title; bodies/schemas differ” |
| Gitea `PROTOCOLS.md` five-protocol narrative | interprets | Set C Romans I–XLVIII | TITLE-LEVEL | `PROTOCOLS/INDEX.md` §Set C binding note — “operational expression of the 48 laws” |

## Boundary notes
- The eight `derived-from` rows are historical condensation correspondences, not byte-identity claims.
- The two `TITLE-LEVEL` rows remain bounded by their source caveats; no catalogue merge or canonical elevation is asserted.
- No dialogue quotation or unsupported dialogue relation was used.

**CODEX_CONCEPT_EDGES_BODY_SAMPLE_OK**
