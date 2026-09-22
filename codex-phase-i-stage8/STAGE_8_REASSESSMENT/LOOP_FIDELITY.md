# LOOP_FIDELITY — SPEC 14 final test
**As-of:** 2026-09-21 ~02:24 PT · **CANONICAL:** NONE  
**Final test (SPEC 14):** If the system cannot be explained simply as  
**talk → preserve → analyse → propose → consolidate → browse**  
it has probably become more complicated than Phase I requires.

## Verdict

**PASS — the living system explains as that chain.**  
Stage 7 closed the last gap (controlled consolidation + browse of WORKING).
Complexity that exists (plurality flags, dual stores, Engine tab) is *supporting*
the chain, not replacing it with another architecture.

## Mapping

| Step | Meaning | Phase I realisation | Evidence |
| --- | --- | --- | --- |
| **talk** | JD ↔ Solace | Solace tab: conversations + messages; stub reply clearly WORKING | Stage 4/7 UI; Solace write surface only |
| **preserve** | Durable conversation + source corpus | SQLite `conversation`/`message`; `source_document` index of Mac corpus (RO) | Stage 3 schema; Stage 6: 935 source rows; corpus fingerprint stable |
| **analyse** | Inspect preserved material | Stage 5 engine analyzers (plurality, duplicates, underdeveloped, durable, discussion) + `analysis_run` | Stage 5 smoke 37/37; Stage 6 E1 idempotent |
| **propose** | Synthesis as proposal, not doctrine | `proposal` / `concept` / `relationship` status PROPOSED (+ INTERPRETATION notes) | 44 proposals, 44/44 provenance; no CANONICAL |
| **consolidate** | Explicit accept into Codex | Engine **Accept → WORKING**; creates/updates `codex_document` WORKING + `revision` + provenance; no silent auto-accept | Stage 7 living loop; max status WORKING |
| **browse** | Read Codex + sources | Codex tab: HISTORICAL `source_document` + WORKING `codex_document` (labelled) | Stage 4/7 UI; Engine tab for proposals |

## Does anything break the simple story?

| Concern | Breaks the chain? | Notes |
| --- | --- | --- |
| Solace is stub, not real LLM | **No** | Talk still works; quality is thin, not architectural failure of the loop |
| Stage 3 SoT vs living store | **No** | Preserve has a clear RO baseline + living write surface; documentable |
| Deterministic engine, not neural | **No** | Analyse/propose are inspectable; LLM optional and OFF by default |
| Plurality / contradictions retained | **No** | Correct: analyse proposes discussion, does not collapse catalogues |
| RELATED projects in corpus tree | **No** | Fenced RELATED; loop does not require SEED/GOLEM/Machina to explain |
| Engine tab as third surface | **Borderline OK** | Still “propose / consolidate controls,” not a fourth product |
| No CANONICAL path | **Strengthens fidelity** | Consolidate stops at WORKING — honest Phase I |

## Fidelity statement (one paragraph)

A user can say: *I talk to Solace; my words are stored; the engine looks at sources and
messages and writes proposals; I accept one into WORKING Codex; I browse sources and
WORKING docs.* That is the whole product story for Phase I. Anything that needs SEED,
GOLEM, Machina, vectors, graphs, blockchain, or multi-agent frameworks to explain the
basic loop fails SPEC 14’s architecture-smell test and is out of Phase I explanation
space — see `ADMISSION_REGISTER.md`.

## Residual frictions (do **not** redefine the loop)

These hurt daily use or ops; they do **not** mean the loop failed:

1. Solace quality (stub) — talk is weak, chain intact.
2. Analyzer depth — proposals are useful but shallow vs human synthesis.
3. Living-store backup / export — preserve is local-file fragile.
4. Codebase mirror (GH / Gitea) — product SoT for *code* vs corpus SoT.
5. UI polish for JD daily use — discoverability, not architecture.

None of these require inventing a new Phase I story. Treat as HOLD or ADMIT-thin only
when evidenced — Partner defaults prefer HOLD unless a demonstrated loop failure.
