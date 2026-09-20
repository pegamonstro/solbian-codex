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

## Out of this repo
- **Codex Machina** → `pegamonstro/codex-machina` (separate product)
- **SEED** / seed zoo → separate repos (not Codex Solbian)
- **Gitea** `00_codex_solbian/solbian.git` → lab forge; archive import when bundle ready

## Operator rules
1. Do not `git merge archive/*` or `working/*` into `main`.
2. Inspect history: `git switch archive/…` or `git show <tag>`.
3. Retire sibling remotes: GitHub **Archive** first; hard-delete only after ARCH backup verify.
4. Git layout ≠ doctrine (CANONICAL is JD-only).

## Backups
- Helios ARCH: `00_Codex_Solbian/_BACKUPS_CONSOLIDATION_2026-09-20/`
- Mac: `~/solbian/codex-audit-out/CONSOLIDATION_BACKUP_2026-09-20/`

Consolidation date: 2026-09-20.
