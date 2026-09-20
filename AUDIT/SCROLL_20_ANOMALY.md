# AUDIT — Scroll 20 anomaly (filename / index vs body XXI)

**Token:** `CODEX_WAVE3_SCROLL20_OK`  
**Status:** AUDIT · **CANONICAL: NONE**  
**As-of:** 2026-09-20 20:58 PT  
**Track:** Wave 3 · T9  
**Rule:** Investigate only. **Do not rename sources.** Prefer UNKNOWN over invention.

## Sources
- `SCROLLS/INDEX.md` · `SCROLLS/ANOMALIES_2026-09-20.md` · `SCROLLS/SEMANTIC_MAP_2026-09-20.md`
- `SCROLLS/SCROLLS_DEEP_16_30_2026-09-20.md` · `SCROLLS_DEEP_16_22_2026-09-20.md` · `SCROLLS_DEEP_ALL_SUMMARY_2026-09-20.md`
- On-box bodies: `/workspace/codex_mac_inv/solbian-codex/source_original/scrolls/codex_solbian_scroll_20.sref` · `…_21.sref`

---

## 1. Observed facts (re-verified 2026-09-20)

| Observation | Evidence |
|-------------|----------|
| Filename `codex_solbian_scroll_20.sref` exists in the 50-file sequence | INDEX; Mac inventory |
| Internal `scroll_no` in that file is **21**, not 20 | Deep 16–30; python load of NDJSON |
| Internal ids are `cs.scroll.21.*` (meta, purpose, principles, …) | Same |
| Title string: **“Scroll XXI — Collective Memory, Shared Knowledge and Continuity”** | INDEX; file meta |
| File `codex_solbian_scroll_21.sref` carries the **same** `scroll_no` 21, same ids `cs.scroll.21.*`, same title | INDEX; deep reads |
| Semantic body identity 20↔21 | **Equal** when comparing JSON rows with `created_at`/`updated_at` stripped (`body_sig_no_ts` match) |
| Raw file hashes differ | sha256 `a2b70723…` (20) vs `44e1a45d…` (21); size 3611 vs 3612 B — difference is packaging (e.g. leading newlines on 21), not distinct thesis |
| Timestamps in meta | Both `created_at`/`updated_at` `2025-09-12T23:30:00Z` |
| Neighbour Roman sequence | XIX (`scroll_19`, 23:00Z) → **XXI** (dup) → XXII (`scroll_22`, 23:45Z) |
| Any `.sref` with `scroll_no` **20** or title **“Scroll XX — …”** in Mac scrolls dir | **NONE** (search) |
| Working INDEX lists both 20 and 21 with the XXI title | INDEX §B |
| Deep-read policy | Document Scroll 20 as **absent**; document XXI once under Scroll 21 | DEEP_16_30 |

**Standing INDEX rule:** Never match MD↔SREF by ordinal alone. This anomaly is an **intra-sref** filename vs `scroll_no` collision, independent of rebuild md chapters.

---

## 2. What is missing

| Missing item | Status |
|--------------|--------|
| Distinct **Scroll XX** body | **ABSENT** from recovered sources |
| Content that would fill “slot 20” thematically between Autonomy/Consent (XIX) and Collective Memory (XXI) | **UNKNOWN** — not reconstructed |
| Authorial note explaining the skip / duplicate | **NOT FOUND** in cited working-tree audits |

---

## 3. Possible explanations (with evidence weight)

| # | Explanation | Evidence for | Evidence against / limits | Weight |
|---|-------------|--------------|---------------------------|--------|
| E1 | **Duplicate file / copy error:** `scroll_20.sref` is a second copy of XXI mis-filed under ordinal 20 | Identical `scroll_no`, ids, title, body_sig; dual INDEX rows | Why keep both in sequence 01–50? Intent unknown | **HIGH** (describes state of files) |
| E2 | **Off-by-one / skipped Roman XX:** Author jumped XIX→XXI; filename sequence still filled 20–21 with the same XXI payload | No Scroll XX title anywhere; Roman gap at XX; timestamps identical for both XXI files | Does not explain *why* XX skipped (superstition, unfinished draft, merge accident) | **HIGH** for gap; **motive UNKNOWN** |
| E3 | **Unfinished Scroll XX replaced by early paste of XXI** into the `scroll_20` filename | Filename reserved; body is already XXI | No stub XX, no partial XX text found | **MED** (compatible, unproven) |
| E4 | **Intentional dual-path publish** (same scroll shipped as two filenames for tooling) | Two filenames, near-identical bytes | Unusual; no manifest note found in cited sources | **LOW** |
| E5 | **Distinct XX existed elsewhere and was lost** | Folklore of 50 scrolls implies contiguous Romans | Zero residual XX string/`scroll_no` 20 on Mac inventory | **LOW** — absence ≠ proof of prior existence |
| E6 | **MD rebuild confusion** (ordinal mix-up with chapter 20) | General ordinal mismatch culture in corpus | Rebuild md only goes 00–08; anomaly is inside sref band 16–30 | **NONE** as cause |

**Preferred AUDIT reading (non-doctrinal):** **E1 + E2 together** — there is **no distinct Scroll XX** in sources; filename `scroll_20` **hosts a duplicate of Scroll XXI**, producing a Roman gap at XX and a double XXI. Packaging byte differences do not create a second work.

---

## 4. Consequences for readers / Working Codex

| Practice | Guidance |
|----------|----------|
| Citing “Scroll 20” by **filename ordinal** | Ambiguous — resolves to XXI body |
| Citing **Scroll XXI / Collective Memory** | Use `scroll_21` as primary documentation locus (deep-read practice); note `scroll_20` as duplicate carrier |
| Inventing XX content | **Forbidden** in this audit |
| Renaming source files | **Forbidden** (task lock) |
| Canon / count folklore “50 scrolls” | Still 50 **files**; **49 unique scroll_no values** in this band anomaly (20 missing, 21 duplicated) — count rhetoric must disambiguate files vs unique Romans |

---

## 5. Related anomaly (context only)

`scroll_04.sref` may embed duplicate Tribunal (=05) content (`ANOMALIES`, INDEX). Pattern family: **filename ordinal ≠ reliable unique scroll identity**. Reinforces INDEX rule — titles / ids / `scroll_no` over bare numbers.

---

## 6. Open (non-blocking)

- Whether any external tree (non-Mac) holds a true Scroll XX — **not searched beyond cited Mac inventory in this task**.
- Whether B-law / protocol “tiering” materials were ever drafted as XX — **NOT ESTABLISHED**.

**CODEX_WAVE3_SCROLL20_OK**
