# Codex Solbian — repository organisation

**Product repo:** `pegamonstro/solbian-codex`  
**Rule:** one product repo on GitHub; do **not** create sibling product repos. Historic siblings live as **archive/** refs (intentional freezes only). **Never merge** unfinished / developmental software into `main`.

## What belongs on public `solbian-codex`

- Organisation / policy docs (this file, doctrine pointers)
- Intentional **historical archives** (`archive/*`)
- Finished / published material and thin **spec/** packs when intentionally published
- **Not** unfinished working branches or developmental Phase I software dumps

## Developmental / unfinished software (private)

**Rule:** Developmental and unfinished Phase I software stays **private**. It must **not** live as public `working/*` branches on this hub.

- **Active private lab forge (Helios down):** [`pegamonstro/phase-i-software`](https://github.com/pegamonstro/phase-i-software) — **private** GitHub repo (Gitea stand-in). This is a lab forge, **not** a second public product.
- Legacy private forge (when Helios returns): Gitea `00_Codex_Solbian/phase-i-software` on Helios — re-sync later; do not treat Helios as available for foreseeable downtime
- Public placement of unfinished Phase I implementation packs as `working/phase-i-software-*` is **retracted** (refs removed from this hub)

## Branches & tags

| Ref | Meaning |
|-----|---------|
| `main` | Current product tip (organisation / published material) |
| `archive/codex-solbian-seed-flat-md` | Former GH `codex-solbian-seed` flat MD pack |
| tag `archive/codex-solbian-seed-2026-09-20` | Frozen pointer to that archive |
| `archive/gitea-solbian-md` | Gitea `00_codex_solbian/solbian.git` (MD / Set C lab forge) |
| tag `archive-gitea-solbian-md-2026-09-20` | Frozen pointer |
| `archive/gitea-solbian-seed-scrolls` | Gitea `solbian-seed-scrolls` flat MD |
| tag `archive-gitea-solbian-seed-scrolls-2026-09-20` | Frozen pointer |
| `working/synthesis-2026-09-20` | Living Working Codex + AUDIT (Waves 2–4) — synthesis docs, not Phase I software |
| tag `working/synthesis-2026-09-20` | Frozen tag for that working snapshot |
| `spec/phase-i-software-stack` | Phase I software-stack SPEC pack (PROPOSED · not doctrine · not CANONICAL; thin specs only) |
| tag `spec-phase-i-2026-09-20` | Frozen pointer to Phase I specs |

~~`working/phase-i-software-2026-09` / tag `working/phase-i-software-2026-09-22`~~ — **removed from public hub** (unfinished implementation now on private `pegamonstro/phase-i-software`).

## Out of this repo
- **Codex Machina** → `pegamonstro/codex-machina` (separate product)
- **SEED** / seed zoo → separate repos (not Codex Solbian)
- **Private Phase I lab forge** → GitHub `pegamonstro/phase-i-software` (private; active while Helios down). Helios Gitea `00_Codex_Solbian/phase-i-software` is deferred. Corpus Gitea `00_Codex_Solbian/solbian.git` stays Helios-side when healthy. Do **not** create additional *public* product repos for Phase I.

## Operator rules
1. Do not `git merge archive/*` or `working/*` or `spec/*` into `main`.
2. Do **not** publish unfinished / developmental software as public `working/*` branches; use private `pegamonstro/phase-i-software` (or Mac-local) instead.
3. Inspect history: `git switch archive/…` or `git show <tag>`.
4. Retire sibling remotes: GitHub **Archive** first; hard-delete only after ARCH backup verify.
5. Git layout ≠ doctrine (CANONICAL is JD-only).
6. Do not publish living/stage `*.sqlite` Journey stores to this **public** hub or the private lab repo if avoidable; keep living DBs Mac-local.

## Backups
- Helios ARCH: `00_Codex_Solbian/_BACKUPS_CONSOLIDATION_2026-09-20/` (pause writes if Helios RAID/storage is unhealthy)
- Mac: `~/solbian/codex-audit-out/CONSOLIDATION_BACKUP_2026-09-20/`
- Mac (hub push prep): `~/solbian/codex-audit-out/PHASE_I_SOFTWARE_HUB_PUSH_BACKUP_2026-09-22/` (sqlite originals before public strip)

Consolidation date: 2026-09-20 · Public unfinished Phase I working-branch placement **retracted** 2026-09-22 · Private lab forge `pegamonstro/phase-i-software` **active** 2026-09-22 (Helios/Gitea down).
