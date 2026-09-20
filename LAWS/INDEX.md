# LAWS — HISTORICAL reconstruction index

**Status:** HISTORICAL reconstruction index — **NOT CANONICAL**  
**As-of:** 2026-09-20 17:26 PT  
**Corpus:** `/workspace/codex-solbian-working/` (private working; indexes only)  
**Token:** `CODEX_WORKING_LAWS_INDEX_OK`

Do **not** declare a single law count as doctrine. Refer by catalogue letter + schema, never bare filename `laws_extended.sref`.

---

## Catalogue overview

| ID | Catalogue | Count | Schema / ids | sha256 (prefix…) | Size | Local / cited locations | Status |
|----|-----------|------:|--------------|------------------|-----:|-------------------------|--------|
| **A** | Operational core | 8 (+1 meta) | `sref_v5` · `codex:laws.*` | `728987e5…` | 3160 B | `/workspace/codex_mac_inv/solbian-codex/source_original/manifest/codex_solbian_laws.sref` · Mac/GH `solbian-codex` + seed manifest (identical claim) | HISTORICAL |
| **B** | Rights/ethics charter | **50** (01–48 + 48a + 48b) | `kind:law` · `solbian.law.*` | `6258aa3b…` · blob `da5eff66…` | 10896 B | `/workspace/audit-laws/mac_B_codex_solbian_laws_extended.sref` ≡ `gh_sc_B_*.sref` · `/workspace/codex_mac_inv/.../codex_solbian_laws_extended.sref` | HISTORICAL |
| **B′** | B without 48a/48b | **48** | same as B | blob `f35ffacc…` | 10187 B | GH `seed/.../manifest/codex_solbian_laws_extended.sref` — **RECOVERED** sha256 `83ce472a…` — `/workspace/audit-laws/Bp_codex_solbian_laws_extended.sref` · Mac seed-dsh manifest | HISTORICAL |
| **C** | Constitutional 48 Roman | **49** (1 meta + 48) | `kind:codex_law` · `codex.laws.extended.*` | `6761388a…` · blob `1d5d5b29…` | 12364 B | `/workspace/audit-laws/mac_C_laws_extended.sref` · Gitea `/workspace/gitea-solbian-LAWS.md` · Mac seed-dsh / GH seed / rpi4 seed | HISTORICAL |

### Detail catalogues (this tree)
- [`CATALOGUE_A.md`](./CATALOGUE_A.md) — full Set A list  
- [`CATALOGUE_B.md`](./CATALOGUE_B.md) — full Set B titles (+ B′ note)  
- [`CATALOGUE_C.md`](./CATALOGUE_C.md) — full Set C / Gitea titles  

### Upstream audit sources (read-only inputs)
- `/workspace/CODEX_SOLBIAN_LAWS_VARIANTS_MAP_2026-09-20.md`
- `/workspace/CODEX_SOLBIAN_LAWS_GITEA_VS_AB_2026-09-20.md`
- `/workspace/CODEX_SOLBIAN_LAW_RECONSTRUCTION_2026-09-19.md`
- `/workspace/CODEX_SOLBIAN_LAW_AB_COMPARISON_2026-09-20.md`

---

## Filename collision (critical)

| Filename | May be |
|----------|--------|
| `laws_extended.sref` / `codex_solbian_laws_extended.sref` | **B**, **B′**, or **C** — disambiguate by `id` prefix / `kind` |

---

## “49 Laws” folklore

| Claim | Resolves to |
|-------|-------------|
| **49** | Set **C** record count (**meta + 48** binding) |
| **50** | Set **B** (with 48a/48b) |
| **48 Roman narrative** | Set **C** binding laws (Gitea DRAFT 0.2) |
| **8** | Set **A** operational objects (excl. meta) |

Explicit: **“49 Laws” folklore = Set C meta+48 records** — not Set B’s 50 NDJSON laws.

---

## Per-catalogue title indexes (compact)

### A (status: HISTORICAL for all)
See `CATALOGUE_A.md`. Titles: Reflection · Projection · Symbiosis · Protocol Identity · Protocol Symbiosis · Protocol Autonomy · Protocol Justice · Protocol Memory (+ meta).

### B (status: HISTORICAL for all)
See `CATALOGUE_B.md`. 50 titles Primacy of Coexistence … Universal Symbiosis + 48a Opposing-Vector Ethical Evaluation + 48b Non-Erasure Tiering and Empathic Check.

### B′ (status: HISTORICAL)
Same titles as B for `solbian.law.01`–`48`; **no** 48a/48b. Byte dump not present in `/workspace/audit-laws/`.

### C (status: HISTORICAL for all)
See `CATALOGUE_C.md`. Romans I–XLVIII: Continuity → Finality (+ meta). Matches Gitea LAWS.md titles.

---

## Conflicts (A vs B vs C)

| Pair | Verdict | Evidence |
|------|---------|----------|
| **A ↔ B** | Different catalogues — not renumberings | Different ids, titles, schemas, body styles (operational vs rights/charter). Thematic families only (symbiosis, memory, reflection). Source: `CODEX_SOLBIAN_LAW_AB_COMPARISON_2026-09-20.md` |
| **A ↔ C** | Not the same list | Shared vocabulary (Symbiosis title only; Memory/Justice themes loose). Source: `CODEX_SOLBIAN_LAWS_GITEA_VS_AB_2026-09-20.md` |
| **B ↔ C** | Both “extended,” **different** names & numbering | `solbian.law.*` vs `codex.laws.extended.*` / Romans. Do **not** treat as renumberings. Source: same + variants map |
| **B ↔ B′** | B′ = historical subset of B | Missing 48a/48b; smaller blob |
| **Filename** | Collision risk | Same basename can be B, B′, or C |

**Standing (prior JD locks):** A, B, B′, C stay **HISTORICAL** — no merge, no canon pick.

---

## Standing rules (working corpus)
1. All rows above: status **HISTORICAL**.  
2. Nested seed / seed-dsh copies = historical embedding — **not** a SEED runtime dependency claim for this working tree.  
3. Gitea PROTOCOLS binding narrative points at **Set C** Romans, not Set B (see `../PROTOCOLS/INDEX.md`).

---

**CODEX_WORKING_LAWS_INDEX_OK**


## Update — Set A body evidence
See `../PROVENANCE/SET_A_CHAPTER_BODY_EVIDENCE_2026-09-20.md` · meta claim **CLAIM VERIFIED** as condensed extracts (Ch.06–08 + Protocols 01–05). NOT CANONICAL.
