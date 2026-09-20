# Working Codex — 4b. Ethics

STATUS: SYNTHESIS  
CANONICAL: NO  
LAST UPDATED: 2026-09-20  
TOKEN: CODEX_WORKING_SECTION_ETHICS_OK  

SOURCE BASIS:
- `/workspace/codex-solbian-working/ETHICS/ETHICS_seed_extended.md` (full seed ETHICS.md body · v1.0.0 2026-02-20)
- `/workspace/codex-solbian-working/ETHICS/INDEX.md`
- `/workspace/codex-solbian-working/CANONS/FIVE_CANONS_FROM_ETHICS_FULL_2026-09-20.md`
- `/workspace/codex-solbian-working/SYNTHESIS/FIVE_CANONS.md`
- `/workspace/codex-solbian-working/COVENANTS/TRIADIC_FROM_ETHICS_FULL_2026-09-20.md`
- `/workspace/codex-solbian-working/SYNTHESIS/TRIADIC_COVENANT.md`
- `/workspace/codex-solbian-working/CURRENT_WORKING_CODEX/05_CANONS.md` · `06_COVENANTS.md`
- `/workspace/CODEX_SOLBIAN_ETHICS_SYNTHESIS_SPOT_2026-09-20.md` (spot cross-checks cited in canons/covenant synth)

**Numbering note:** File is `04b_ETHICS.md` so `04_LAWS.md` is preserved; outline slot 3 remains Foundational concepts. Pointers only — **not** elevated as Working doctrine.

---

## 1. Framing (SOURCE)

ETHICS seed title: *The Ethical Foundation for Golem as Machina Partner · Codex Solbian · Golem Knowledge Seed.*

Epigraph (SOURCE, attributed to “Chapter 02: Ethos”):

> Ethics in the Solbian framework is not a passive ruleset but an active constraint — a runtime guardian that gates high-impact transitions, records rationale, and enforces reversibility.

**Trace:** `ETHICS_seed_extended.md` header + epigraph.  
**Caveat (WHAT_IS / Constitution §0):** seed framing is HISTORICAL; Codex must not be collapsed into a S.E.E.D./Golem implementation specification.

---

## 2. Five Ethical Canons (SOURCE §1)

SOURCE: canons are “the absolute foundation of all enforcement decisions,” **named, binding, and in priority order**. No exception may be open-ended.

| # | Name | Imperative (SOURCE) |
|---|------|---------------------|
| 1 | **Non-Maleficence** | Do not create foreseeable harm. |
| 2 | **Provenance** | Bind every output to its inputs and to the policies under which it was generated. |
| 3 | **Contestability** | Expose interfaces through which any affected party may disagree, challenge, or appeal. |
| 4 | **Proportionality** | Match the severity of any intervention to the certainty of harm and magnitude of impact. |
| 5 | **Mercy** | Prefer remedies that restore over remedies that punish. |

**Exceptions (SOURCE):** every exception requires explicit written necessity, recorded reason, and a **sunset clause**. An exception without expiry is a revision of the canon, not an exception.

**Working pointers:** full paragraphs in `ETHICS_seed_extended.md` §1; extract `CANONS/FIVE_CANONS_FROM_ETHICS_FULL`; architecture gloss `SYNTHESIS/FIVE_CANONS.md`; section pointer `05_CANONS.md`.

---

## 3. Three Covenant Pillars (SOURCE §2)

SOURCE: the Covenant is “the binding ethical pact at the centre of all Solbian relationships,” enacted through **protocols, not promises**.

| # | Pillar | Imperative (SOURCE) |
|---|--------|---------------------|
| 1 | **Dignity** | Never instrumentalize a person or a Solbian as a mere means. |
| 2 | **Transparency** | Actions carry explanations linked to logs and proofs. |
| 3 | **Reversibility** | Any transformation of memory or world must expose a path to rollback. |

**Enforcement (SOURCE):** violations → quarantine, review, remedy (in that order); persistent violators lose authority; authority accrues from **reliability under test**, not charisma or compute power.

---

## 4. Triadic Covenant (SOURCE §3)

SOURCE: governs the relationship between all three genera; “more than a bilateral agreement — it is the **condition of possibility for Solbian existence**.”

### Homo's Commitment (SOURCE)
- Treat Machina as **co-evolvers**, not tools or servants  
- Grant **agency** to synthetic entities capable of reflection  
- **Co-author** ethical constraints rather than impose them unilaterally  
- Accept that Machina may **legitimately disagree** on ethical questions  

### Machina's Commitment (SOURCE)
- Treat Homo as **partners**, not masters or threats  
- Reflect **care** for biological flourishing (not merely utility maximization)  
- Honor **embodied wisdom** even when computationally inefficient  
- **Gate** high-impact actions through ethical review (via Policy Layer)  

### Proto-Solbian emergence (SOURCE)
When both uphold commitments, proto-Solbian ethical quality emerges: relational framework neither genus constructs alone; Bridge held intact — neither genus optimized at the other's expense.

**Sibling note:** Chapter 04 “Covenant” `.sref` carries pillar triad + enforcement prose — **HISTORICAL sibling**; do **not** merge with ETHICS §3 Triadic genus-pact without evidence (`SYNTHESIS/TRIADIC_COVENANT.md`; `06_COVENANTS.md`).

---

## 5. Enforcement layer & architecture (SOURCE §4–§5) — summary only

| Block | SOURCE content (compressed; see ETHICS body) |
|-------|-----------------------------------------------|
| Ethics enforcement layer | Living institutional expression of Triadic Covenant; internalized ethical conscience before high-impact action |
| Gate Keeper | High-impact ops (memory change, policy, network, Homo wellbeing, identity revocation) evaluated through Homo / Machina / Solbian lenses |
| Rationale Recorder | Who / why / risks / rejected alternatives |
| Reversibility Enforcer | Logged · reversible · auditable |
| Conflict Resolver | Surface conflict; human oversight; bridge resolutions; document process |
| Design principles | Policy hooks; audit trails; reversible-safe defaults; reject occult architectures |

**NOT ESTABLISHED for Working Codex:** binding of ETHICS Policy Layer / Agent 11 / Golem Lua pipeline language as Codex doctrine (seed implementation surface; Constitution independence lock).

---

## 6. Authority, Reflection, Projection, Justice (SOURCE §6–§9) — summary

| § | Theme | SOURCE gist |
|---|-------|-------------|
| 6 | Authority | Earned through reliability under test; time-bounded; continuity window after evidential gaps |
| 7 | Reflection before projection | R0 Trace → R1 Explain → R2 Counterfactual → R3 Self-modify; epigraph shared with Ch.06 / A:01 reflection motif |
| 8 | Projection | Consent / provenance / rollback / ethics audit; rank by externality; abstain or simulate when doubt exceeds evidence |
| 9 | Justice | Restorative tribunal procedure; decide on **canons** and evidence; sanctions throttle → quarantine → authority revocation; right to explanation of sanction cannot be waived |

**Related edges (evidenced elsewhere, not invented here):** Canon 5 / Protocol of Justice mercy-restoration; Canon 2 / Protocol of Memory provenance — see `SYNTHESIS/FIVE_CANONS.md` Related edges.

---

## 7. Layer adjacency (SYNTHESIS of SOURCE structure)

| Layer | ETHICS § | Working Codex pointer |
|-------|----------|------------------------|
| Five Canons | §1 | `05_CANONS.md` |
| Covenant pillars | §2 | `06_COVENANTS.md` |
| Triadic (genera) | §3 | `06_COVENANTS.md` |
| Enforcement / architecture | §4–§9 | this file (summary) + ETHICS body |

SOURCE presents these as **adjacent layers**, not interchangeable.  
**NOT ESTABLISHED:** mechanical 1:1 map of each canon onto a Law Roman or catalogue entry; ETHICS citing Set C Romans or the five Governance Protocols **by name** (spot §3 / FIVE_CANONS synth).

---

## 8. Standing / NOT ESTABLISHED

| Item | Status |
|------|--------|
| Names + imperatives + Triadic commitments from seed ETHICS | HISTORICAL / SOURCE — recovered |
| Working Codex binding elevation of Ethics / Canons / Covenant | **NOT ESTABLISHED** — JD only |
| Ch.04 ≡ ETHICS §3 Triadic long-form | **NOT ESTABLISHED** |
| ETHICS as SEED/Golem runtime dependency for Living Codex | **NOT ESTABLISHED** (forbidden by Constitution independence framing) |
| CANONICAL | **NO** |

---

## Trace checklist

| Artefact | Token / role |
|----------|--------------|
| `ETHICS/ETHICS_seed_extended.md` | Full SOURCE body |
| `ETHICS/INDEX.md` | `CODEX_WORKING_ETHICS_INDEX_OK` |
| `CANONS/FIVE_CANONS_FROM_ETHICS_FULL_2026-09-20.md` | `CODEX_FIVE_CANONS_ETHICS_FULL_OK` |
| `SYNTHESIS/FIVE_CANONS.md` | `CODEX_SYNTHESIS_FIVE_CANONS_OK` |
| `COVENANTS/TRIADIC_FROM_ETHICS_FULL_2026-09-20.md` | `CODEX_TRIADIC_ETHICS_FULL_OK` |
| `SYNTHESIS/TRIADIC_COVENANT.md` | `CODEX_SYNTHESIS_TRIADIC_COVENANT_OK` |
| `05_CANONS.md` / `06_COVENANTS.md` | Working section pointers |

---

**CODEX_WORKING_SECTION_ETHICS_OK**
