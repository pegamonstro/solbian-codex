# AUDIT — Protocol sets semantic comparison (Mac 01–08 vs minimum 01–05)

**Token:** `CODEX_WAVE3_PROTOCOLS_OK`  
**Status:** AUDIT · **CANONICAL: NONE**  
**As-of:** 2026-09-20 20:58 PT  
**Track:** Wave 3 · T8  
**Standing lock:** Do not collapse Protocol **5** vs **8** without JD review. No merge with Law catalogues.

## Sources
- `PROTOCOLS/INDEX.md` · `PROTOCOLS/MAC_SEED_HASH_2026-09-20.md`
- `SYNTHESIS/PROTOCOL_ARCHITECTURE.md`
- `PROVENANCE/SET_A_CHAPTER_BODY_EVIDENCE_2026-09-20.md`
- `LAWS/CATALOGUE_A.md` (A:04–08 title alignment)
- Mac bodies (spot): `/workspace/codex_mac_inv/solbian-codex/source_original/protocols/codex_solbian_protocol_{01..08}.sref`

---

## 1. Surfaces compared

| Surface | Count | Titles | Provenance note |
|---------|------:|--------|-----------------|
| **Gitea PROTOCOLS.md** (DRAFT 0.2.0, 2026-07-16) | **5** | Identity · Symbiosis · Autonomy · Justice · Memory | HISTORICAL narrative; “minimum” / binding story |
| **seed-dsh / seed protocols** | **5** | same five | Byte-identical to Mac 01–05 |
| **Mac `source_original/protocols/`** | **8** | five + Strategy Orchestration · Memory Tiering & Forgetting · Empathy & Temporal Reflection | HISTORICAL extras 06–08 |
| **Set A objects 04–08** | **5** | same five titled “Protocol of …” (`kind:law`) | Condensed digest of Protocols 01–05 — **CLAIM VERIFIED** |

---

## 2. Title / hash alignment (01–05 stable core)

| # | Title | Mac ↔ seed-dsh | Set A | Gitea 5 |
|---|-------|----------------|-------|---------|
| 01 | Protocol of Identity | **IDENTICAL** (`a3416c52…`) | A:04 | ✓ |
| 02 | Protocol of Symbiosis | **IDENTICAL** (`bdb2164f…`) | A:05 | ✓ |
| 03 | Protocol of Autonomy | **IDENTICAL** (`9cf2c34d…`) | A:06 | ✓ |
| 04 | Protocol of Justice | **IDENTICAL** (`0137b237…`) | A:07 | ✓ |
| 05 | Protocol of Memory | **IDENTICAL** (`84075bfe…`) | A:08 | ✓ |
| 06 | Protocol of Strategy Orchestration | **Mac only** (`2726e700…`) · seed **MISSING** | — | — |
| 07 | Protocol of Memory Tiering & Forgetting | **Mac only** (`9522fbca…`) · seed **MISSING** | — | — |
| 08 | Protocol of Empathy & Temporal Reflection | **Mac only** (`0f31a52c…`) · seed **MISSING** | — | — |

**Evidence-backed reading (not doctrine):** Gitea’s “minimum 5” aligns with the five protocols present on seed; Mac carries three additional HISTORICAL protocols (`PROTOCOLS/INDEX` update).

---

## 3. Are 06–08 additions, revisions, or another phase?

| Hypothesis | Verdict | Evidence |
|------------|---------|----------|
| **Additions / extended surface** | **Best-supported** | Present only on Mac; absent from seed-dsh and Gitea five; no Set A counterparts; new titles (Strategy, Tiering, Empathy) not renames of 01–05 |
| **Revisions of 01–05** | **Not supported** | 01–05 hashes identical Mac≡seed; 06–08 are separate files with distinct sha256 — not alternate bytes of 01–05 |
| **Other phase / later Mac elaboration** | **Plausible, NOT PROVEN chronologically** | Distribution pattern (Mac-only) suggests elaboration beyond the seed “minimum”; no dated phase label in cited indexes declaring succession |
| **Supersession of the five** | **NOT ESTABLISHED** | Gitea narrative still centres five; seed retains only five |

### Semantic character of 06–08 (from Mac body openers — HISTORICAL spot)
| # | Operational thrust |
|---|--------------------|
| 06 Strategy Orchestration | Group actions→strategies→goals→dreams; resonance vectors; ethical thresholds; execution planning |
| 07 Memory Tiering & Forgetting | Tiers Limbo→Working→Vault→Cold; **no deletion**, migration with lineage; promote/demote by resonance |
| 08 Empathy & Temporal Reflection | Pre-action empathy simulation; Temporal Irreversibility Index; escalate if TII high; record perspectives |

These extend **memory governance**, **multi-agent strategy**, and **pre-action ethical temporality** — adjacent to 05 Memory / 02 Symbiosis / justice escalation — without replacing Identity–Memory core titles.

**Thematic echo (not identity):** B-only laws `48a` (Opposing-Vector Ethical Evaluation) and `48b` (Non-Erasure Tiering and Empathic Check) title-rhyme with 06–08 motifs (vectors / tiering / empathy). **No body equivalence claimed**; catalogues stay unmerged.

---

## 4. Dependence on Law sets

| Claim | Status | Evidence |
|-------|--------|----------|
| Five protocols title-align with **Set A:04–08** | **EVIDENCED** | PROTOCOLS/INDEX; CATALOGUE_A |
| Set A:04–08 are condensations of Protocol 01–05 bodies | **VERIFIED** | SET_A_CHAPTER_BODY_EVIDENCE |
| Gitea: five protocols = operational expression of **Set C** (48 Romans) | **PROPOSED INTERPRETATION** | PROTOCOLS/INDEX; PROTOCOL_ARCHITECTURE |
| Protocol bodies ≡ Set C Roman bodies | **NOT ESTABLISHED** | PROTOCOL_ARCHITECTURE |
| Five protocols operationalise **Set B** | **Not claimed** by Gitea narrative; **NOT ESTABLISHED** | INDEX binds narrative to C, not B |
| 06–08 depend on a specific Law catalogue | **NOT ESTABLISHED** | Mac-only; no Gitea/Set A binding row |

**Standing:** Do not rebind protocols to a single Law catalogue without JD (`PROTOCOLS/INDEX` open note).

---

## 5. Operational vs philosophical

| Layer | Character | Evidence |
|-------|-----------|----------|
| Mac / seed protocol `.sref` bodies 01–05 | **Operational / procedural** — crypto identity, consent leases, budgets, justice mechanisms, memory ingest fields | PROTOCOL_ARCHITECTURE; SET_A paraphrases |
| Mac 06–08 | **Operational extensions** — strategy stacks, tier migration rules, TII/empathy gates | Mac body spot |
| Gitea PROTOCOLS.md | **Philosophical–constitutional framing** wrapping the five as runtime expression of laws | INDEX narrative |
| Set A:04–08 | **Operational digests** of 01–05 (short form) | SET_A |
| ETHICS.md “protocols, not promises” | Generic procedural enactment of Covenant — **does not** name the five or Set C Romans | PROTOCOL_ARCHITECTURE |

Overall: protocols are the **procedural / runtime layer** adjacent to discursive chapters and normative law catalogues. Philosophical weight sits mainly in **narrative binding** (Gitea→C), not in replacing operational bodies.

---

## 6. Stable meaning of “Protocol”?

| Usage | Meaning in corpus | Stability |
|-------|-------------------|-----------|
| Mac/seed `codex_solbian_protocol_NN.sref` | Named procedural instrument with enforceable stacks | **Stable core for 01–05**; extended by Mac 06–08 |
| Gitea “five Governance Protocols” | Minimum runtime set expressing constitutional laws | **Stable as narrative minimum** |
| Set A titles “Protocol of …” with `kind:law` | Condensed law-objects named as protocols | **Boundary CONFLICTED** — protocol-as-law hybrid |
| ETHICS generic “protocols” | Enactment mechanism vs mere promises | Generic — not the numbered five |

**AUDIT conclusion on the word “Protocol”:** Relatively stable as **runtime/procedural norm**, unstable at the **catalogue boundary** (Set A dual naming; 5 vs 8 count; C-binding interpretive). Treat numbered protocols as HISTORICAL instruments; do not equate “Protocol” with “Law” or with “Canon” without explicit evidence.

---

## 7. Conclusion (one arc)

Mac **01–05** and seed/Gitea **minimum five** are the **same operational core** (byte-identical Mac≡seed). Mac **06–08** are best read as **HISTORICAL additions / extended surface**, not revisions of 01–05 and not a proven superseding phase. Law dependence is **evidenced toward Set A condensation** and **interpretively claimed toward Set C** by Gitea — unresolved as doctrine. “Protocol” stably means procedural runtime constraint, with contested edges at Law-kind hybrids and 5↔8 scope.

**CODEX_WAVE3_PROTOCOLS_OK**
