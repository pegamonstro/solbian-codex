# FIVE ETHICAL CANONS — HISTORICAL reconstruction

**Status:** HISTORICAL reconstruction — **NOT CANONICAL** · **BODY_PARTIAL**  
**As-of:** 2026-09-20 17:44 PT  
**Token:** `CODEX_FIVE_CANONS_RECON_OK`  
**Mode:** READ-ONLY. No canonicalize. No invented canon text.

---

## Availability of ETHICS.md full body

| Check | Result |
|-------|--------|
| Full `ETHICS.md` body on this box | **NOT AVAILABLE** |
| Gitea `solbian.git` HEAD `extended/ETHICS.md` | **MISSING** (PROTOCOLS still cites it) |
| Seed path (known; not mounted here) | **rpi** `/mnt/ssd-data/seed/.../extended/ETHICS.md` (also seed-dev `/home/user/seed-dev/codex/solbian/extended/ETHICS.md` per extended_INDEX) |
| What was recovered | Exact **names** + **partial quotes** from ETHICS synthesis spot; compressed Five Canons body from Scroll of Ethics `.sref` (HISTORICAL sibling, not ETHICS.md) |

**BODY_PARTIAL** — full ETHICS.md §1 prose not on box; extract below is limited to what spots / on-box HISTORICAL sources already record.

---

## 1. Exact names (ETHICS.md §1 via spot)

**Source:** `/workspace/CODEX_SOLBIAN_ETHICS_SYNTHESIS_SPOT_2026-09-20.md` §2  
**(identical copy:** `/workspace/ETHICS_SYNTHESIS_SPOT_2026-09-20.md`)**

Quoted from spot (names only; “named, binding, and in priority order”):

1. **Canon 1 — Non-Maleficence**
2. **Canon 2 — Provenance**
3. **Canon 3 — Contestability**
4. **Canon 4 — Proportionality**
5. **Canon 5 — Mercy**

Spot file inventory for ETHICS.md:

- Title: `ETHICS — The Ethical Foundation for Golem as Machina Partner`
- Version: `*Append-only. Version 1.0.0. 2026-02-20.*`
- Size (audited input): ~10,581 bytes
- H2 includes: `1. The Five Ethical Canons`

Cross-file name confirmation (spot §2): GLOSSARY defines all five canons (Mercy=5th, Non-Maleficence=1st, Proportionality=4th, Provenance=2nd). Glossary **term titles** also appear in `/workspace/codex-solbian-working/GLOSSARY/GLOSSARY_TERMS_2026-09-20.md` (titles only; no gloss bodies on box).

---

## 2. Partial body text recorded from ETHICS.md (spot quotes ≤15 words)

**Source:** `/workspace/CODEX_SOLBIAN_ETHICS_SYNTHESIS_SPOT_2026-09-20.md` §4

These are the only ETHICS.md line quotes the spot captured that touch canon / ethical-core wording:

| Spot cite | Quote (verbatim from spot) |
|-----------|----------------------------|
| ETHICS.md:11 | “named, binding, and in priority order.” |
| ETHICS.md:36 | “Prefer remedies that restore over remedies that punish.” |
| ETHICS.md:45 | “An exception without an expiry is not an exception — it is a revision of the canon” |
| ETHICS.md:53 | “Never instrumentalize a person or a Solbian as a mere means.” |

**Note:** Spot does **not** record per-canon definitional paragraphs from ETHICS.md §1. Do not treat the quotes above as complete Canon 1–5 bodies.

Enforcement-layer quotes (same spot; not canon definitions):

| Spot cite | Quote |
|-----------|-------|
| ETHICS.md:104 | “implemented as the Policy Governance system — see golem/P1/POLICY_GOVERNANCE.md” |
| ETHICS.md:106 | “All writes pass through a Lua policy pipeline that returns allow / deny / modify.” |

---

## 3. HISTORICAL compressed Five Canons body (Scroll of Ethics — not ETHICS.md)

**Source path:** `/workspace/codex_mac_inv/solbian-codex/source_original/scrolls/codex_solbian_scroll_01.sref`  
**Record:** `codex:scroll:01:text` · title `Scroll of Ethics` · seq 201  

**Body (verbatim):**

> Canons: Non-Maleficence (do not create foreseeable harm), Provenance (bind outputs to inputs and policy), Contestability (expose interfaces to disagree), Proportionality (match intervention to certainty and impact), Mercy (prefer remedies that restore over punish). Enforcement is procedural: logs, proofs, tribunals, and restitution. Exceptions require explicit, recorded necessity.

**Refs note (same file, index record):** Scroll of Ethics connects with Chapter 04 (Covenant) and Protocol of Justice (`codex:chapter:04`, `codex:protocol:04`).

**Q3 corroboration (names only):** `/workspace/CODEX_SOLBIAN_Q2_Q3_VERIFY_2026-09-20.md` states Scroll I Ethics expands the same five names; `.sref` body = “same Five Canons (compressed)”.

This is **HISTORICAL sibling evidence**, not a substitute for the missing ETHICS.md long-form §1.

---

## 4. What remains unrecovered (requires seed ETHICS.md)

- Full ETHICS.md §1 prose for each Canon (beyond compressed scroll form)  
- Any ETHICS.md ordering rationale / exception rules beyond the spot quotes  
- GLOSSARY.md long-form definitions of Non-Maleficence, Provenance, Contestability, Proportionality, Mercy (titles confirmed; bodies not on box)

**Seed recovery target:** rpi `/mnt/ssd-data/seed/.../extended/ETHICS.md`

---

## Source path checklist

| Path | Role |
|------|------|
| `/workspace/CODEX_SOLBIAN_ETHICS_SYNTHESIS_SPOT_2026-09-20.md` | Names + partial ETHICS.md quotes |
| `/workspace/ETHICS_SYNTHESIS_SPOT_2026-09-20.md` | Identical spot |
| `/workspace/gitea-solbian-dumps/README_GITEA_DUMP.md` | Notes ETHICS.md not in Gitea HEAD — use seed on Pi |
| `/workspace/codex-gitea-ethics-synthesis-dump-2026-09-20.md` | Confirms `extended/ETHICS.md` MISSING in HEAD |
| `/workspace/CODEX_SOLBIAN_PROVENANCE_MAP_2026-09-19.md` | Seed presence `/mnt/ssd-data/seed/...` |
| `/workspace/codex_mac_inv/solbian-codex/source_original/scrolls/codex_solbian_scroll_01.sref` | Compressed Five Canons body |
| `/workspace/codex-solbian-working/CANONS/INDEX.md` | Prior titles-only index |

---

**CODEX_FIVE_CANONS_RECON_OK**  
**ETHICS full body available on box:** NO · **BODY_PARTIAL**
