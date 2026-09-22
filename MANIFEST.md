# Codex Solbian Phase I — backup manifest
As-of: 2026-09-21 02:26 WEST
CANONICAL: NONE
Gitea target: 00_codex_solbian/phase-i-software (pending Homelab create)

## Trees
4.0K	/Users/archcore/solbian/_phase_i_backup_staging_2026-09-21/MANIFEST.md
8.7M	/Users/archcore/solbian/_phase_i_backup_staging_2026-09-21/PHASE_I_BASELINE
4.0K	/Users/archcore/solbian/_phase_i_backup_staging_2026-09-21/README.md
 76K	/Users/archcore/solbian/_phase_i_backup_staging_2026-09-21/SPEC
344K	/Users/archcore/solbian/_phase_i_backup_staging_2026-09-21/STAGE_3_MINIMAL_DATA_LAYER
4.0K	/Users/archcore/solbian/_phase_i_backup_staging_2026-09-21/STAGE_7_LIVING_LOOP
1.2M	/Users/archcore/solbian/_phase_i_backup_staging_2026-09-21/codex-phase-i-stage3
1.5M	/Users/archcore/solbian/_phase_i_backup_staging_2026-09-21/codex-phase-i-stage4
1.0M	/Users/archcore/solbian/_phase_i_backup_staging_2026-09-21/codex-phase-i-stage5
412K	/Users/archcore/solbian/_phase_i_backup_staging_2026-09-21/codex-phase-i-stage6
268K	/Users/archcore/solbian/_phase_i_backup_staging_2026-09-21/codex-phase-i-stage7
 80K	/Users/archcore/solbian/_phase_i_backup_staging_2026-09-21/codex-phase-i-stage8

## SHA256 of SQLite stores
1d71dd09112327f7bec5be1e104085ff648c20046e437543e94ebeeaedce9688  /Users/archcore/solbian/_phase_i_backup_staging_2026-09-21/codex-phase-i-stage5/data/codex_phase_i.sqlite
8c6e15a6c98ceed92559b0642241d83bddc336f4a1187a652e55b465bfb56dac  /Users/archcore/solbian/_phase_i_backup_staging_2026-09-21/codex-phase-i-stage3/codex_phase_i.sqlite
cc78705805f748e53deb8c78ae3dd69d1a55931860503a843aff4d9ae9892bbd  /Users/archcore/solbian/_phase_i_backup_staging_2026-09-21/codex-phase-i-stage4/data/codex_phase_i.sqlite

## 2026-09-22 hybrid UI polish
- Stage 4 UI wired to Stage 5b hybrid synthesize (`POST /api/engine/synthesize`).
- Quiet Engine list defaults; explicit Accept unchanged.
- Pack includes `codex-phase-i-stage5/codex-phase-i-stage5b-hybrid/` and updated Stage 4 sources.
- Live Stage 4 SQLite omitted from pack.
- Synced 2026-09-22 08:03 PT.

## Hub placement (2026-09-22)
- GitHub: `pegamonstro/solbian-codex` branch `working/phase-i-software-2026-09` (code-only; sqlite excluded)
- Gitea lab: `00_Codex_Solbian/phase-i-software` when Helios reachable
