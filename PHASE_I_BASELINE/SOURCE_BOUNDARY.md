# SOURCE_BOUNDARY — Phase I Stage 2
**As-of:** 2026-09-20 ~22:57 PT (Europe/Lisbon, WEST)  
**CANONICAL elevation:** NONE (archaeology ≠ Codex)  
**Mode:** READ-ONLY on historical corpora

## Purpose
Classify every corpus candidate before deeper analysis. Prefer NOT ESTABLISHED / UNKNOWN over invention.

## Access limitation (this executor)
- **ListMachines / Shell+machineId:** NOT AVAILABLE in this subagent tool schema. Live Mac path `/Users/archcore/solbian/codex` could not be opened directly.
- **Proxy used:** Mac consolidation snapshot `mac-codex-working-tree.tgz` (sha256 `5d3cdcfc8e0705ebc8cc38e102d82b4f494052ac69b2ceea53dd016de9b2807b`) from `/workspace/uploads/CONSOLIDATION_BACKUP_2026-09-20-mac.tgz`, taken ~2026-09-20 22:10 PT and verified ALL_OK on Helios. Extracted read-only under `PHASE_I_BASELINE/_scratch/mac_wt/codex`.
- Prior live Mac audit (2026-09-19, Partner, machineId `9d6a5f1b-715e-4317-b70d-7785f8fa2786`) cited as LEAD only; key claims re-checked against this snapshot.

---

## Candidate classification table

| ID | Location | Size (approx) | Remotes / refs | Classification | Role |
|----|----------|---------------|----------------|----------------|------|
| **C1** | Mac `/Users/archcore/solbian/codex` (via WT snapshot) | Snapshot 4.4M excl `.git` / **880** files excl AppleDouble; prior live claim **~8.9M / ~1792** | `origin` → `https://github.com/pegamonstro/solbian-codex.git`; HEAD **`e289bd8`**; dirty WT | **CURRENT** (live candidate) + **HISTORICAL** payload in `source_original/` | **PRIMARY HISTORICAL CORPUS CANDIDATE** |
| **C2** | Box `/workspace/codex_mac_inv/solbian-codex` | 4.8M / 911 files | same remote; HEAD **`6e4036a`** | **HISTORICAL** mirror (stale vs Mac WT HEAD) | Compare / offline archaeology |
| **C3** | GH `pegamonstro/solbian-codex` | multi-branch | **main** `fe23afa`; **archive/**×3; **working/synthesis-2026-09-20**; **spec/phase-i-software-stack** | **HUB** — branch-dependent | Document only; **do not merge** |
| **C4** | `/workspace/codex-solbian-working/` | WORKING tree | mirrors GH working/synthesis content | **WORKING / DERIVED** | Archaeology already done; **not** historical SoT |
| **C5** | Helios ARCH `00_Codex_Solbian/` | WORKING 1.2M; backups 71M; SEED 491M (RELATED) | Tailscale `helios4` 100.104.187.4 | **ARCHIVE / BACKUP / POINTERS** | Consolidation backups; thin `codex/` |
| **C6** | Gitea `00_codex_solbian/*` | bundles on Helios | lab forge | **HISTORICAL** MD narratives | VARIANT vs Mac sref; live API not re-probed |
| **C7** | Prior box docs `CODEX_SOLBIAN_*` | various | n/a | **DERIVED** leads | Re-verify; do not copy blindly as fact |

---

## C1 — Mac working tree (PRIMARY)

| Field | Value |
|-------|-------|
| machineId (claimed) | `9d6a5f1b-715e-4317-b70d-7785f8fa2786` (vega-2 / mb-m1-air Tailscale) |
| Path | `/Users/archcore/solbian/codex` |
| Snapshot HEAD | `e289bd8` *Merge remote-tracking branch origin/main* (2025-10-27) |
| Dirty (snapshot) | **M** `README.md`, `scrolls/01`–`08`*.md*; **??** `core/`, `tests/`, `projects/porto_lagoa/`, `scrolls/00_Taxonomy.md`, `README.POINTER.md`, AppleDoubles; **D** various `.DS_Store` |
| Zips | Prior audit listed untracked `codex-solbian.zip` / `codex_original.zip` — **NOT present** in 22:10 PT tgz → status **UNKNOWN on live Mac** |
| Structure root | `archetypes/ backlog/ codex_minsoo/ core/ glyphs/ journal/ manifest/ projects/ references/ schema/ scrolls/ source_original/ tests/` + LICENSE CHANGELOG README* |
| Historical density | `source_original/` ≈ bulk (chapters 30+index, scrolls 50+index, protocols 8, laws A+B, personae 460 files, …) |

**Do not clean / commit / rewrite.**

---

## C2 — Box mirror vs C1

| Check | Result |
|-------|--------|
| Laws A/B hashes | **IDENTICAL** to Mac WT |
| Scroll sref 01/20 | **IDENTICAL** |
| `scrolls/*.md` | Box = thin stubs (~347 B Genesis); Mac WT = full (~4675 B Genesis) — **VARIANT** |
| HEAD | Box `6e4036a` ≠ Mac `e289bd8` |
| Extra on Mac WT | `core/`, `tests/`, `porto_lagoa/`, fuller README |
| Extra on Box | `MACHINA.md` |

---

## C3 — GitHub hub branches (listed; not merged)

| Branch | SHA (short) | Classification |
|--------|-------------|----------------|
| `main` | `fe23afa` | **WORKING** tip — Partner consolidation layout (CHAPTERS/SCROLLS/AUDIT/…); **≠** Mac historical tree |
| `working/synthesis-2026-09-20` | `40449f51` | WORKING snapshot |
| `spec/phase-i-software-stack` | `d514a95` | Phase I **spec** (software design; out of Stage 2 implement scope) |
| `archive/codex-solbian-seed-flat-md` | `44452cb` | ARCHIVE flat MD |
| `archive/gitea-solbian-md` | `542881d` | ARCHIVE |
| `archive/gitea-solbian-seed-scrolls` | `064e269` | ARCHIVE flat MD (CHAPTERS.md SCROLLS.md ETHICS.md …) |

Historical sref corpus remains on older commits (e.g. `e289bd8` / `6e4036a`) and Mac WT — **not** at current `main` tip tree shape.

---

## C4 — Working synthesis

Path: `/workspace/codex-solbian-working/`  
Contains AUDIT/, CURRENT_WORKING_CODEX/, Wave5 fences, SPEC/PHASE_I_SOFTWARE_STACK.  
**Fence:** WORKING / DERIVED. Wave5 fences = **WORKING fences**, not source doctrine.

---

## C5–C6 — Helios / Gitea

- Helios **REACHABLE** via Tailscale IP.  
- Gitea bare repos present under `/var/lib/gitea/.../00_codex_solbian/`.  
- Live Gitea HTTP/API: **not re-verified** this pass → treat content via bundles/dumps as **PARTIALLY AVAILABLE**.  
- SEED tree on ARCH (491M) = **RELATED**, not Phase I Codex structure.

---

## Boundary rules (locked for Stage 2)

1. Archaeology outputs only under `/workspace/codex-solbian-phase-i/PHASE_I_BASELINE/`.  
2. No rewrite/rename/reorganise/delete/merge of C1–C3 historical material.  
3. SEED / GOLEM / Machina / DAO / blockchain / agents / porto_lagoa → **RELATED** if present.  
4. JD↔Solace dialogue = **SOURCE**, not doctrine.  
5. CANONICAL elevation for this report package: **NONE**.

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
