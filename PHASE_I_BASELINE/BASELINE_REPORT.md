# BASELINE_REPORT — Phase I Stage 2
**As-of:** 2026-09-20 ~23:00 PT (Europe/Lisbon)  
**CANONICAL elevation:** NONE  
**Token (if complete):** see STATUS at end  
**Answers A–L:** archaeology questions implied by Stage 2 mission §16 / deliverable set (full numbered mission text not separately filed on box; answers cover required substance).

---

## A — Where does the corpus live, and what is primary?
**PRIMARY HISTORICAL CANDIDATE:** Mac `/Users/archcore/solbian/codex` (machineId `9d6a5f1b-…`), tracking `pegamonstro/solbian-codex`.  
**This pass:** pack built from consolidation WT snapshot; **live Shell+machineId later confirmed** (8.9M, HEAD `e289bd8`, dirty, 897 files).  
Also: box mirror (stale HEAD), GH multi-branch hub, Helios ARCH/backups, Gitea bundles, `/workspace/codex-solbian-working` (**WORKING only**).  
See `SOURCE_BOUNDARY.md`.

## B — What is the discovered structure (not the wishlist)?
Historical density in `source_original/` (chapters 30, scrolls 50 files, protocols 8, laws A+B, glossary, personae/dialogue). Root `scrolls/*.md` = 9 MD rebuild “Chapters”. Nested `projects/` = RELATED. Details: `STRUCTURE.md`, `CORPUS_INVENTORY.*`.

## C — Laws: what exists, what conflicts?
Catalogues **A / B / B′ / C** documented; A+B re-hashed on Mac WT. Filename collision on `laws_extended`. **No canon.** See `CONTRADICTIONS.md` C-LAW + prior VARIANTS map.

## D — Protocols: 5 or 8?
Mac **8** sref protocols; Gitea narrative **5** (= Mac 01–05). Extras 06–08 Mac-only in this comparison. Plurality recorded, not collapsed.

## E — Scrolls: MD vs sref; anomalies?
Two systems; ordinals **must not** be equated. Scroll **20** file = Scroll **XXI** duplicate; Scroll XX **ABSENT**. Re-verified.

## F — Dialogue / Journey material?
31 JD↔Solace week `.sref` under `personae/joao/personae/solace/` (+ other personae trees). Status: **SOURCE**, not doctrine. Completeness gaps = prior DERIVED audits.

## G — Duplicates?
Listed in `DUPLICATES.md` (scroll 20/21, mirror identities, B/B′, WORKING mirrors, AppleDouble noise). **No merges.**

## H — Contradictions?
Laws plurality; protocols 5 vs 8; scroll 20; MD≠sref ordinal; GH main tip ≠ Mac historical; size/zip observation gap. `CONTRADICTIONS.md`.

## I — Related projects contamination risk?
SEED/Machina/DAO/blockchain/porto_lagoa/agents/SeedNet tests present in tree → classified **RELATED** / out of Phase I structure. `RELATED_PROJECTS.md`.

## J — Provenance & timeline confidence?
Snapshot provenance HIGH; live Mac MED; some catalogues MED; constitution gap UNKNOWN. `PROVENANCE.md`, `HISTORICAL_TIMELINE.md`.

## K — Underdeveloped / open for conversation?
Canon picks, XX gap motive, covenant class, dialogue gaps, live Mac confirm, GH historical protection — **topics not auto-additions**. `UNDERDEVELOPED_AREAS.md`, `UNCERTAINTIES.md`.

## L — Readiness for Stage 3 (Minimal Data Layer)?
**Baseline archaeology package: SUBSTANTIVELY COMPLETE** for inventory/structure/contradiction fencing, with explicit gaps (live Mac machineId, zips, live Gitea, DSH review).  
**Not ready to treat any catalogue as CANONICAL.**  
**Next:** Stage 3 storage model may proceed against **classified** corpus pointers; must ingest provenance flags and plurality — not a flattened “one true tree.”

---

## Critical findings for JD
1. **Primary historical corpus** remains Mac `source_original` (+ full MD scrolls), not current GH `main` tip (WORKING synthesis).  
2. **Law A/B/B′/C** and **protocol 5↔8** and **scroll XX gap** stay unresolved pluralities — correct.  
3. **Live Mac confirmed** by Partner after pack — 8.9M / HEAD `e289bd8` / dirty / 897 files (U1/U2 closed).  
4. Wave5 / Working fences are **WORKING**, not source CANONICAL.  
5. Related SEED/DAO/Machina material is present but fenced out of Phase I structure.

## Recommended next action (only)
Partner (or tool with ListMachines): **live read-only** `du`+`git status` on Mac `~/solbian/codex` to close U1/U2; then proceed Stage 3 Minimal Data Layer **without** merging catalogues.

## DSH
Attempted rpi4: host OK, ollama present, `agent-llm.service` **inactive**, no `dsh` binary found → **FAILURE**. Self-review applied in `VALIDATION.md`.

---

## Live Mac confirmation (Partner, 2026-09-20 ~23:00 PT)

Shell+machineId **succeeded** after archaeology pack write.

| Metric | Live value |
|--------|------------|
| Path | `/Users/archcore/solbian/codex` |
| `du -sh` total | **8.9M** (closes U1: includes `.git` 3.7M + `source_original` 3.5M + zips ~1.4M + rest) |
| Files (excl `.git`) | **897** |
| HEAD | `e289bd867914491570ecbeb308afa9ec08e19a9f` (`e289bd8`) |
| Dirty | Yes — modified root `scrolls/01–08.md`, README, DS_Store; untracked zips, `core/`, `tests/`, `porto_lagoa/`, `scrolls/00_Taxonomy.md`, `README.POINTER.md`, journal sref |
| Snapshot used in pack | consolidation WT ~4.4M excl `.git` / 880 files — **consistent** with live once `.git`+zips accounted |

**U1/U2:** CLOSED—EVIDENCE (live confirm). Primary historical SoT unchanged: Mac `source_original` + full MD scrolls. Source **untouched** this pass.
