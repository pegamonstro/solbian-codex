# Phase I software pack — hub placement

**Hub:** `pegamonstro/solbian-codex`  
**Ref:** `working/phase-i-software-2026-09` (this branch)  
**Rule:** one product repo; do **not** merge this branch into `main`.

## What this is
Mac staging backup of Phase I Stages 3–8 implementation + hybrid Stage 5b polish
(tip lineage includes `0abe18b` hybrid UI wiring), for Helios-down failover and
code recovery.

## What this is not
- Not CANONICAL doctrine
- Not the historical corpus (`main` / archive refs)
- Not a replacement for Gitea lab forge `00_Codex_Solbian/phase-i-software`
  (re-sync there when Helios is back)

## Privacy
`*.sqlite` living/stage stores are **excluded** from this public hub branch.
Restore DBs only from Mac backups or private lab forge.
