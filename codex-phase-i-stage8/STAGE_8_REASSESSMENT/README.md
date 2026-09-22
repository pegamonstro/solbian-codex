# Codex Solbian — Phase I · Stage 8 Reassessment
**As-of:** 2026-09-21 ~02:24 PT · **CANONICAL:** NONE  
**Scope:** Docs / organise only. No code changes. No corpus writes. No elevation.

## What this is

Stage 8 (SPEC 13): *Only after the loop works decide what Phase II requires.*
This pack records completion of Stages 1–7, checks loop fidelity against SPEC 14’s
final test, scores candidate Phase II items with the SPEC 14 admission test, and
recommends **HOLD** on the Phase II feature gate (thin/ops exceptions only).

## Files

| File | Purpose |
| --- | --- |
| `00_STAGE8_BRIEF.md` | Mission receipt |
| `PHASE_I_COMPLETION.md` | Stages 1–7 status + evidence pointers |
| `LOOP_FIDELITY.md` | talk→preserve→analyse→propose→consolidate→browse |
| `ADMISSION_REGISTER.md` | Candidates scored → ADMIT / ADMIT-thin / DEFER / REJECT / OPS |
| `RECOMMENDED_NEXT.md` | ≤5 next necessary actions |
| `REASSESSMENT_REPORT.md` | A–H narrative + gate recommendation |
| `README.md` | This index |

## Locations

| Where | Path |
| --- | --- |
| Box (working) | `/workspace/codex-solbian-phase-i/STAGE_8_REASSESSMENT/` |
| Tarball-ready twin | `/workspace/codex-phase-i-stage8/` |
| Tarball | `/workspace/codex-consol/stage8-reassessment.tgz` |
| Partner Mac copy target | `~/solbian/codex-phase-i-stage8/` |

## Copy to Mac

```bash
# on box / transfer host
tar -tzf stage8-reassessment.tgz
# on Mac
mkdir -p ~/solbian/codex-phase-i-stage8
tar -xzf stage8-reassessment.tgz -C ~/solbian/codex-phase-i-stage8 --strip-components=1
# or copy the twin directory contents directly into ~/solbian/codex-phase-i-stage8/
```

## Judgment defaults (applied)

- Prefer **HOLD** Phase II gate.
- Real LLM, vector, SEED/GOLEM/Machina, multi-agent, blockchain → **DEFER**.
- ADMIT-thin only with evidence: analyzer quality, store export, GH code mirror, UI polish.
- Gitea Phase I backup → **OPS**, not feature admission.
- **CANONICAL: NONE.**

## Prior stage pointers (box)

```
/workspace/codex-solbian-phase-i/PHASE_I_BASELINE/
/workspace/codex-solbian-phase-i/STAGE_3_MINIMAL_DATA_LAYER/
/workspace/codex-solbian-phase-i/STAGE_4_TWO_SURFACE/
/workspace/codex-solbian-phase-i/STAGE_5_CODEX_ENGINE/
/workspace/codex-solbian-phase-i/STAGE_6_HISTORICAL_VALIDATION/
/workspace/codex-solbian-phase-i/STAGE_7_LIVING_LOOP/
```

SPEC pack: `/workspace/codex-solbian-working/SPEC/PHASE_I_SOFTWARE_STACK/`
