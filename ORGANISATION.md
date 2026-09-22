# Codex Solbian — repository organisation

**Product repo:** `pegamonstro/solbian-codex`  
**Rule:** one product repo; historic siblings live as **archive/** and **working/** refs. **Never merge** those into `main` as melted history.

## Branches & tags

| Ref | Meaning |
|-----|---------|
| `main` | Current product tip (Mac-tracked historical checkout) |
| `archive/codex-solbian-seed-flat-md` | Former GH `codex-solbian-seed` flat MD pack |
| tag `archive/codex-solbian-seed-2026-09-20` | Frozen pointer to that archive |
| `archive/gitea-solbian-md` | Gitea `00_codex_solbian/solbian.git` (MD / Set C lab forge) |
| tag `archive-gitea-solbian-md-2026-09-20` | Frozen pointer |
| `archive/gitea-solbian-seed-scrolls` | Gitea `solbian-seed-scrolls` flat MD |
| tag `archive-gitea-solbian-seed-scrolls-2026-09-20` | Frozen pointer |
| `working/synthesis-2026-09-20` | Living Working Codex + AUDIT (Waves 2–4) |
| tag `working/synthesis-2026-09-20` | Frozen tag for that working snapshot |
| `spec/phase-i-software-stack` | Phase I software-stack SPEC pack (PROPOSED · not doctrine · not CANONICAL) |
| tag `spec-phase-i-2026-09-20` | Frozen pointer to Phase I specs |
| `working/phase-i-software-2026-09` | Phase I Stages 3–8 **implementation** pack + hybrid Stage 5b polish (**code-only**; no SQLite) |
| tag `working/phase-i-software-2026-09-22` | Frozen pointer to that software pack |


## Out of this repo
- **Codex Machina** → `pegamonstro/codex-machina` (separate product)
- **SEED** / seed zoo → separate repos (not Codex Solbian)
- **Gitea lab forge** → `00_Codex_Solbian/solbian.git` (corpus) and `00_Codex_Solbian/phase-i-software` (Phase I code when Helios is up); do **not** duplicate as new GitHub product repos

## Operator rules
1. Do not `git merge archive/*` or `working/*` or `spec/*` into `main`.
2. Inspect history: `git switch archive/…` / `working/…` or `git show <tag>`.
3. Retire sibling remotes: GitHub **Archive** first; hard-delete only after ARCH backup verify.
4. Git layout ≠ doctrine (CANONICAL is JD-only).
5. Do not publish living/stage `*.sqlite` Journey stores to this **public** hub; keep DBs Mac-local (and private Gitea when available).

## Backups
- Helios ARCH: `00_Codex_Solbian/_BACKUPS_CONSOLIDATION_2026-09-20/`
- Mac: `~/solbian/codex-audit-out/CONSOLIDATION_BACKUP_2026-09-20/`
- Mac (hub push prep): `~/solbian/codex-audit-out/PHASE_I_SOFTWARE_HUB_PUSH_BACKUP_2026-09-22/` (sqlite originals before public strip)

Consolidation date: 2026-09-20 · Phase I software working-branch placement: 2026-09-22.
