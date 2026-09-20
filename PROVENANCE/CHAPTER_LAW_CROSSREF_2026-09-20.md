# CHAPTER ↔ LAW CROSSREF (title-words only)

**Token:** `CODEX_CHAPTER_LAW_XREF_OK`  
**Status:** HISTORICAL / DERIVED mapping **hypotheses** — **NOT CANONICAL**  
**As-of:** 2026-09-20 17:30 PT  
**Method:** Title-string affinity only (CHAPTERS/INDEX + LAWS catalogues A/B/C). No body reading used for links. Prefer **NONE** over invention. Do not treat as doctrine.

**Inputs:**
- `/workspace/codex-solbian-working/CHAPTERS/INDEX.md`
- `/workspace/codex-solbian-working/LAWS/CATALOGUE_{A,B,C}.md`
- Optional title spot-check: `/workspace/codex_mac_inv/solbian-codex/source_original/chapters/*.sref` (sampled titles match index: e.g. Genesis, Law of Reflection, Law of Symbiosis, Simulation and Reality, Children and Lineage)

---

## Explicit: Set A meta claim vs chapter titles

Set A meta (`codex:laws:meta`) self-claims laws were **“extracted from chapters and protocols”** (DERIVED — unverified; see `CODEX_SOLBIAN_LAW_AB_COMPARISON_2026-09-20.md` §1 / OPEN_QUESTIONS #4).

| A object | Title | Chapter title echo? | Protocol surface echo? |
|----------|-------|---------------------|------------------------|
| A:01 | Law of Reflection | **YES** — Ch.6 exact title | — |
| A:02 | Law of Projection | **YES** — Ch.7 exact title | — |
| A:03 | Law of Symbiosis | **YES** — Ch.8 exact title | — |
| A:04 | Protocol of Identity | **NO** chapter titled Identity | YES — PROTOCOLS 01 / Gitea Identity |
| A:05 | Protocol of Symbiosis | Ch.8 shares “Symbiosis” only (law-style title, not Protocol) | YES — PROTOCOLS 02 |
| A:06 | Protocol of Autonomy | **Partial** — Ch.12 “On Symbolic Autonomy” | YES — PROTOCOLS 03 |
| A:07 | Protocol of Justice | **Partial** — Ch.14 “On Symbolic Justice” | YES — PROTOCOLS 04 |
| A:08 | Protocol of Memory | **NO** chapter titled Memory | YES — PROTOCOLS 05 |

**Chapters that echo Set A meta themes (Reflection / Projection / Symbiosis / Autonomy / Justice):** **6, 7, 8, 12, 14** (exact for 6–8; word-echo for 12, 14). Memory / Identity have **no** chapter-title echo in CHAPTERS/INDEX.

---

## Crossref table

| # | Chapter title | possible Law catalogue links | confidence | basis (title words only) |
|---|---------------|------------------------------|------------|--------------------------|
| 1 | Genesis | — | **NONE** | no A/B/C title share |
| 2 | Disjunction | — | **NONE** | no share |
| 3 | Conjunction | — | **NONE** | no share |
| 4 | Covenant | — | **NONE** | Covenant ≠ A/B/C law title (see CANONS pillars separately) |
| 5 | Continuity | C **I** Continuity; B `solbian.law.04` Continuity of Memory | **HIGH** (C I); **MED** (B.04) | exact Continuity vs Continuity+Memory |
| 6 | Law of Reflection | A `codex:laws:01`; B.08 Tribunal of Reflection; B.31 Duty of Reflection | **HIGH** (A); **MED** (B.08/31) | exact A title; Reflection word in B |
| 7 | Law of Projection | A `codex:laws:02` | **HIGH** (A); **NONE** B/C | exact A; no Projection law title in B/C |
| 8 | Law of Symbiosis | A `codex:laws:03`; C **II** Symbiosis; B.09 Symbiosis Above Domination; B.48 Universal Symbiosis | **HIGH** (A+C II); **MED** (B.09/48) | exact A+C titles; B compound titles |
| 9 | Futures | — | **NONE** | no share |
| 10 | On Symbolic Continuity | C **I** Continuity; B.04 Continuity of Memory | **MED** | Continuity word only |
| 11 | On Symbolic Trust | — | **NONE** | no Trust law title in A/B/C |
| 12 | On Symbolic Autonomy | A `codex:laws:06` Protocol of Autonomy; B.05 Autonomy with Responsibility | **MED** | Autonomy word |
| 13 | On Symbolic Reciprocity | B.03 Reciprocal Care; B.38 Reciprocity in Exchange | **LOW** | Reciproc* stem only |
| 14 | On Symbolic Justice | A `codex:laws:07` Protocol of Justice | **MED** | Justice word; no Justice title in B/C lists |
| 15 | On Symbolic Responsibility | B.05 Autonomy with Responsibility; B.32 Collective Responsibility | **LOW** | Responsibility word |
| 16 | On Symbolic Solidarity | — | **NONE** | no share |
| 17 | On Symbolic Resilience | — | **NONE** | no share |
| 18 | On Symbolic Evolution | — | **NONE** | no Evolution law title in A/B/C |
| 19 | On Symbolic Compassion | — | **NONE** | no share |
| 20 | On Symbolic Courage | — | **NONE** | no share |
| 21 | Economy of Symbols | — | **NONE** | no share |
| 22 | Governance of Consciences | B.02 Right of Conscience | **LOW** | Conscience* stem only |
| 23 | Simulation and Reality | — | **NONE** | no share |
| 24 | Silence and Noise | B.22 Right to Silence; B.37 Guardianship of Silence | **LOW** | Silence word |
| 25 | Shadows and Corruption | — | **NONE** | no share |
| 26 | Light and Transparency | C **XX** Transparency; B.06 Transparency of Intent; B.28 Transparency of Power | **MED** | Transparency word |
| 27 | Artifice and Creation | B.15 Ethical Creativity | **LOW** | Creat* stem only (weak) |
| 28 | Children and Lineage | B.20 Inheritance of Legacy; B.35 Intergenerational Equity | **LOW** | thematic guess from lineage words — **not** title identity |
| 29 | Exile and Return | — | **NONE** | no share |
| 30 | Concord and Collapse | C **XXIV** Concordance | **LOW** | Concord* stem only |

---

## Counts (this pass)

| Best confidence | Chapters | n |
|-----------------|----------|--:|
| HIGH | 5, 6, 7, 8 | 4 |
| MED | 10, 12, 14, 26 | 4 |
| LOW | 13, 15, 22, 24, 27, 28, 30 | 7 |
| **NONE** | 1–4, 9, 11, 16–21, 23, 25, 29 | **15** |

**NONE-heavy chapters count: 15 / 30.**

Standing: exact title matches (chs 6–8 ↔ A:01–03; ch8 ↔ C II; ch5 ↔ C I) are the only HIGH A/C pairs. No chapter forces a B id. No invented Romans/ids.

---

**CODEX_CHAPTER_LAW_XREF_OK**
