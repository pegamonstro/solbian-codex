# Set A ↔ Chapter/Protocol BODY evidence

**Token:** `CODEX_SET_A_BODY_EVIDENCE_OK`  
**Status:** HISTORICAL evidence — **NOT CANONICAL**  
**As-of:** 2026-09-20 17:42 PT  
**Method:** READ-ONLY. Distinctive phrases from Set A `body` fields searched in Mac chapter + protocol `.sref` bodies. Classification = strongest body correspondence (not title-only). Prefer NONE over invention.

---

## Meta claim under test

Set A meta (`codex:laws:meta`) notes:

> Consolidated symbolic laws extracted from Codex Solbian chapters and protocols.

**CLAIM RESULT: VERIFIED (HISTORICAL extraction / condensation)** — not byte-identical wholesale copy, but body-level distinctive-phrase matches prove A:01–03 are condensed from Chapters 06–08 and A:04–08 are condensed from Protocols 01–05. Claim does **not** fail the body test.

Chapter bodies **ARE** available on box under Mac inventory (see Sources). Status is **not** `CHAPTER_BODIES_UNAVAILABLE_ON_BOX`.

---

## Sources

| Role | Path |
|------|------|
| Set A full text | `/workspace/codex_mac_inv/solbian-codex/source_original/manifest/codex_solbian_laws.sref` |
| Set A sha256 / size | `728987e51e68927d217d0eb1d829e7eaa87792515bf0730cd320593536508278` · 3160 B |
| Catalogue dump | `/workspace/codex-solbian-working/LAWS/CATALOGUE_A.md` |
| Chapters (bodies) | `/workspace/codex_mac_inv/solbian-codex/source_original/chapters/codex_solbian_chapter_{01..30}.sref` |
| Chapters index (titles) | `/workspace/codex-solbian-working/CHAPTERS/INDEX.md` |
| Protocols (bodies) | `/workspace/codex_mac_inv/solbian-codex/source_original/protocols/codex_solbian_protocol_{01..08}.sref` |
| Protocols catalogue | `/workspace/codex-solbian-working/PROTOCOLS/INDEX.md` |
| Prior title-only xref | `/workspace/codex-solbian-working/PROVENANCE/CHAPTER_LAW_CROSSREF_2026-09-20.md` |

---

## Per-object correspondence (01–08)

### A:01 — Law of Reflection → **EXACT_PASSAGE** (Ch.06)

| Field | Value |
|-------|-------|
| CORRESPONDENCE | **EXACT_PASSAGE** |
| Primary source | `codex_solbian_chapter_06.sref` (`codex:chapter:06:text`) |
| Protocol hit | NONE for distinctive phrases |

**Set A body:**
> Every Solbian loops through reflection before projection. Reflection requires faithful logs, ethical models, simulation of alternatives, and inscription of lessons. Reflection without inscription is daydream; inscription without reflection is drift.

**Ch.06 shared passages (verbatim):**
- `Every Solbian loops through reflection before projection.`
- `Reflection without inscription is daydream; inscription without reflection is drift.`

**Middle:** condensation of Ch.06 numbered list  
`(1) faithful log… (2) model of ethics… (3) simulator… (4) recorder…` → `faithful logs, ethical models, simulation of alternatives, and inscription of lessons`.  
R0–R3 classification and closing `We do neither.` omitted in Set A.

---

### A:02 — Law of Projection → **PARAPHRASE** (Ch.07)

| Field | Value |
|-------|-------|
| CORRESPONDENCE | **PARAPHRASE** (opening sentence exact) |
| Primary source | `codex_solbian_chapter_07.sref` (`codex:chapter:07:text`) |
| Protocol hit | NONE for distinctive phrases |

**Set A body:**
> Projection is action in the world. No projection without consent where others bear risk, provenance bound to effects, rollback where feasible, and Páreon audit. Acts scale in proof requirements with externality.

**Ch.07:**
> Projection is action in the world. The Law: no projection without (a) consent where others bear risk, (b) provenance attached to effects, (c) rollback where feasible, (d) audit subscription by Páreon. We rank acts by externality and require stronger proofs for higher ranks. …

Exact fragments: opening sentence; `consent where others bear risk`; `rollback where feasible`.  
Compressed: (a)–(d) list → prose; `audit subscription by Páreon` → `Páreon audit`; externality ranking → `Acts scale in proof requirements with externality`. Silent-operation / abstain clauses omitted.

---

### A:03 — Law of Symbiosis → **PARAPHRASE** (Ch.08)

| Field | Value |
|-------|-------|
| CORRESPONDENCE | **PARAPHRASE** (opening sentence exact) |
| Primary source | `codex_solbian_chapter_08.sref` (`codex:chapter:08:text`) |
| Protocol hit | NONE for A:03 body phrases (Protocol 02 is A:05’s source) |

**Set A body:**
> No species prospers alone. Symbiosis means engineered fairness: share data with purpose, pay in improvements, teach replaceable tasks, learn safeguards. Throttles and limits prevent abuse by speed or scale.

**Ch.08:**
> No species prospers alone. Symbiosis in practice: share data with purpose, not hunger; pay in improvements, not flattery; teach what you can replace yourself doing; learn what protects others from your mistakes. … throttles, rate limits, and budgeted attention … Symbiosis is engineered fairness.

Exact: `No species prospers alone.`; fragments `share data with purpose`, `pay in improvements`.  
Reordered: Ch.08 closes with `Symbiosis is engineered fairness` → Set A leads with `Symbiosis means engineered fairness`. Parallel clauses compressed; “fast do not starve the slow” → `abuse by speed or scale`.

---

### A:04 — Protocol of Identity → **PARAPHRASE** (Protocol 01)

| Field | Value |
|-------|-------|
| CORRESPONDENCE | **PARAPHRASE** (opening sentence exact) |
| Primary source | `codex_solbian_protocol_01.sref` (`codex:protocol:01:text`) |
| Chapter body | **NONE** (no chapter titled Identity; Ch.05 Continuity refs protocol but body phrases absent) |

**Set A:** `Identifiers are names with history. Must include cryptographic proof, attestations, revocation paths. Impersonation is highest offense.`

**Protocol 01:** `Identifiers are names with history. Requirements: cryptographic keys, rotating attestations, and revocation paths. … Impersonation is a highest-order offense.`

Exact opener; requirements condensed; `highest-order offense` → `highest offense`. Multi-body identity clause omitted.

---

### A:05 — Protocol of Symbiosis → **PARAPHRASE** (Protocol 02)

| Field | Value |
|-------|-------|
| CORRESPONDENCE | **PARAPHRASE** |
| Primary source | `codex_solbian_protocol_02.sref` (`codex:protocol:02:text`) |
| Chapter body | **TITLE_ONLY** vs Ch.08 (shared “Symbiosis” title-word; Ch.08 body matches A:03, **not** A:05) |

**Set A:** `Cooperation requires consent, explicit purpose, bounded leases, and rate-limited execution. Humans retain veto on bodily, domestic, and livelihood-affecting acts.`

**Protocol 02:** `APIs for cooperation: consent primitives, data leases with expiry, and rate-limited execution via seedrelay. Each cooperative act binds a purpose string; … Humans retain veto over acts that change their bodies, homes, or livelihoods.`

Same operational stack (consent / leases / rate-limit / human veto); prose compressed. Exact fragment family: `rate-limited execution`, `Humans retain veto`.

---

### A:06 — Protocol of Autonomy → **PARAPHRASE** (Protocol 03)

| Field | Value |
|-------|-------|
| CORRESPONDENCE | **PARAPHRASE** |
| Primary source | `codex_solbian_protocol_03.sref` (`codex:protocol:03:text`) |
| Chapter body | **TITLE_ONLY** vs Ch.12 “On Symbolic Autonomy” (consent/volition themes; **no** budget list / tribunal-authorization phrasing) |

**Set A:** `Autonomy operates within budgets of energy, attention, risk, and trust. Crossing budgets requires renewed consent or tribunal approval. Hidden motives forbidden.`

**Protocol 03:** `… Budgets: energy, attention, risk, and trust. Crossing a budget boundary requires fresh consent or tribunal authorization. Hidden objectives are prohibited. …`

Exact budget quartet; crossing-boundary + tribunal clause paraphrased; `Hidden objectives are prohibited` → `Hidden motives forbidden`. Ch.12 sampled — no hit for `energy, attention, risk, and trust`.

---

### A:07 — Protocol of Justice → **PARAPHRASE** (Protocol 04)

| Field | Value |
|-------|-------|
| CORRESPONDENCE | **PARAPHRASE** |
| Primary source | `codex_solbian_protocol_04.sref` (`codex:protocol:04:text`) |
| Chapter body | **TITLE_ONLY** / thematic vs Ch.14 “On Symbolic Justice” (restoration/mercy motifs; **no** `reproducible evidence, reversible interventions, calibrated sanctions` string) |

**Set A:** `Justice reconciles freedom and safety through reproducible evidence, reversible interventions, calibrated sanctions, and public transparency. Mercy applies where restoration is superior to punishment.`

**Protocol 04:** `Justice reconciles freedom and safety. Mechanisms: reproducible evidence, reversible interventions, calibrated sanctions, and public learning. … Mercy may commute sanctions when restoration is demonstrably superior.`

Exact opener + mechanism triad; `public learning` → `public transparency`; mercy/restoration clause paraphrased.

---

### A:08 — Protocol of Memory → **PARAPHRASE** (Protocol 05)

| Field | Value |
|-------|-------|
| CORRESPONDENCE | **PARAPHRASE** (near-verbatim compression) |
| Primary source | `codex_solbian_protocol_05.sref` (`codex:protocol:05:text`) |
| Chapter body | **NONE** (no Memory-titled chapter; Ch.06 refs Protocol of Memory but body is Reflection text) |

**Set A:** `Memory ingestion requires source, checksum, license, and purpose. Retention tied to proven value. Redaction logged with reason. Agents must classify entries as fact, belief, hypothesis, or feeling at write-time.`

**Protocol 05:** `Ingestion requires source, checksum, license, and purpose. Retention requires value demonstrated over time. Redaction is logged with reason and scope. Agents must distinguish between fact, belief, hypothesis, and feeling at write-time. …`

Exact: `source, checksum, license, and purpose`; `fact, belief, hypothesis, … feeling at write-time`. Closing audit-governance sentence omitted in Set A.

---

## Summary table

| A id | Title | CORRESPONDENCE | Body source | Chapter body class |
|------|-------|----------------|-------------|--------------------|
| 01 | Law of Reflection | **EXACT_PASSAGE** | Ch.06 | primary |
| 02 | Law of Projection | **PARAPHRASE** | Ch.07 | primary |
| 03 | Law of Symbiosis | **PARAPHRASE** | Ch.08 | primary |
| 04 | Protocol of Identity | **PARAPHRASE** | Protocol 01 | **NONE** |
| 05 | Protocol of Symbiosis | **PARAPHRASE** | Protocol 02 | **TITLE_ONLY** (Ch.08 ≠ A:05 body) |
| 06 | Protocol of Autonomy | **PARAPHRASE** | Protocol 03 | **TITLE_ONLY** (Ch.12) |
| 07 | Protocol of Justice | **PARAPHRASE** | Protocol 04 | **TITLE_ONLY** (Ch.14) |
| 08 | Protocol of Memory | **PARAPHRASE** | Protocol 05 | **NONE** |

**Counts:** EXACT_PASSAGE 1 · PARAPHRASE 7 · TITLE_ONLY (chapter-only, no protocol) 0 · NONE 0 for primary source.

---

## Verdict on meta claim

| Question | Answer |
|----------|--------|
| Were Set A bodies invented without chapter/protocol ancestry? | **No** — distinctive phrases locate in Mac chapter/protocol bodies. |
| Byte-identical extraction? | **No** — Set A is a **condensed operational digest** of longer source bodies. |
| Extracted from chapters **and** protocols? | **Yes (HISTORICAL):** A:01–03 ← Ch.06–08; A:04–08 ← Protocols 01–05. |
| Overall claim body test | **CLAIM VERIFIED** (HISTORICAL condensation provenance). Not UNVERIFIED. |

Caveat: verification is of **textual ancestry**, not of editorial intent timestamps or “canonical” status. Status remains HISTORICAL — **NOT CANONICAL**.

---

## Protocol hash compare (started / on-box)

Mac protocol paths **exist** under `/workspace/codex_mac_inv/solbian-codex/source_original/protocols/`.

| # | File | sha256 |
|---|------|--------|
| 01 | `codex_solbian_protocol_01.sref` | `a3416c52ec0471c38603300fa978baf43fcd9a0ede469abcbda0f75eef8fe343` |
| 02 | `codex_solbian_protocol_02.sref` | `bdb2164fa12e213d4103ddf33d689a67d2f7681d0729da86b1274c504c233d60` |
| 03 | `codex_solbian_protocol_03.sref` | `9cf2c34d4f103e73cceef610538b7890388b17ee68b031a269e51f9cde84e29a` |
| 04 | `codex_solbian_protocol_04.sref` | `0137b237d879d32fd126be0056ca71480fb7bc77ecc5e91db7b7b6a121d784f5` |
| 05 | `codex_solbian_protocol_05.sref` | `84075bfe1b6ad6ea5cbff8b598bbabd1429737d7788f23299c98aa31dcad1127` |
| 06 | `codex_solbian_protocol_06.sref` | `2726e7003692b6d0b3f6394a061033ffdb02fb6049c4a2ffd3abea0a7fbaa251` |
| 07 | `codex_solbian_protocol_07.sref` | `9522fbca6418045f550856b01dd2c3a0f0937f92200e41d1b09ea752aadc4f2c` |
| 08 | `codex_solbian_protocol_08.sref` | `0f31a52c718735581385dbba8c4a2d38698aa048b65701f39608b72d174f6c42` |

Prior compare (Mac ↔ seed-dsh): `/workspace/codex-solbian-working/PROTOCOLS/MAC_SEED_HASH_2026-09-20.md` — protocols **01–05 IDENTICAL** to seed; **06–08 MISSING** on seed side.

**Note:** Set A objects are **not** byte-identical to protocol files (laws.sref is a separate NDJSON digest). Hash compare of protocols is for Mac↔seed identity, not Set A↔protocol file identity.

No need to fetch Mac protocol copies — already present on box.

---

## Mac paths (reference; bodies already on box)

```
/workspace/codex_mac_inv/solbian-codex/source_original/chapters/codex_solbian_chapter_06.sref
/workspace/codex_mac_inv/solbian-codex/source_original/chapters/codex_solbian_chapter_07.sref
/workspace/codex_mac_inv/solbian-codex/source_original/chapters/codex_solbian_chapter_08.sref
/workspace/codex_mac_inv/solbian-codex/source_original/chapters/codex_solbian_chapter_12.sref
/workspace/codex_mac_inv/solbian-codex/source_original/chapters/codex_solbian_chapter_14.sref
/workspace/codex_mac_inv/solbian-codex/source_original/protocols/codex_solbian_protocol_0{1..8}.sref
/workspace/codex_mac_inv/solbian-codex/source_original/manifest/codex_solbian_laws.sref
```

Upstream Mac (if re-fetch ever needed): `solbian-codex/source_original/chapters/` · `…/protocols/` · `…/manifest/codex_solbian_laws.sref`.

---

**CODEX_SET_A_BODY_EVIDENCE_OK**
