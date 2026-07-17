# Cognitive Engine Research Knowledge Base

> **Status**: Active research substrate
> for the S.E.E.D. cognitive engine.
> This directory is the
> solbian-side knowledge base for
> promoting community-approved
> algorithms to first-class SXL
> operators in
> `~/seed-dev/src/seedcogd/` and the
> Lua brain cycle in
> `~/seed-dev/lua/agents/cognitive/`.
>
> **Last updated**: 2026-07-16.
>
> **Promotion criterion**: an algorithm
> is `ready-for-promotion` when (1) it
> has a canonical primary citation, (2)
> it is covered in standard textbooks
> or has >1,000 citations, (3) it has a
> known complexity class and tractable
> restrictions, (4) it has a worked
> numerical example, and (5) it has a
> defined SXL entity shape.

## Confirmation status

Each algorithm profile carries a
**confirmation flag**. The flag is
honest about how solid the citation
chain is. We use five levels:

| Flag | Meaning |
|------|---------|
| ✅ `confirmed-canonical` | The primary citation, year, author list, and reference URL have been verified against multiple independent sources (textbook, Wikipedia, arXiv, official documentation). The algorithm is safe to promote without further review. |
| 🟢 `confirmed-curated` | The primary citation and year are correct, but the algorithm has been profiled from a textbook or survey and not yet checked against the primary paper. Worth a second pass before promotion. |
| 🟡 `unconfirmed` | The algorithm name, year, and basic idea are plausible, but at least one of the following is uncertain: the exact author list, the publication venue, the reference URL, the worked example, or the complexity class. **Requires verification** before promotion. The next research wave (or a human reviewer) must confirm. |
| 🟠 `derived-from-partial` | The agent that produced this entry stalled before the final structured return; some sections (e.g. pseudocode or SXL shape) are reconstructed from the agent's tool-call stream rather than from a completed profile. Treat with caution. |
| 🔴 `speculative` | The entry is plausible but the citation chain is weak or self-referential. **Do not promote** without a primary-source pass. |

The default flag for new entries is
🟡 `unconfirmed`. A human reviewer
(or a verification sub-agent) reads
the profile, checks the citation
against the primary source, and
upgrades the flag. Promotion to
`~/seed-dev/` requires
✅ `confirmed-canonical` or
🟢 `confirmed-curated`.

## Verification flow

For each 🟡 or 🟠 or 🔴 entry, a
verifier does the following:

1. **Read** the primary source (the
   cited paper or textbook chapter).
2. **Confirm** the year, author list,
   venue, and reference URL.
3. **Re-derive** the worked example
   and the pseudocode from the
   primary source.
4. **Re-check** the complexity claim
   against the literature.
5. **Update** the flag.
6. **Add** a `verification_log.md`
   entry recording the
   verification date and the
   verifier's name.

The verification log is in
`verification/` (one file per
verifier; entries are append-only).

## Files

| File                       | Purpose                                          | Algorithms |
|----------------------------|--------------------------------------------------|-----------|
| `sxl-operators.md`         | Symbolic cognitive algorithms (AGM, Dung, DLs, SAT, planning, BNs, MLNs, KG embeddings) | 30 |
| `cognitive-cycles.md`      | Cognitive cycle and time-series algorithms (memory consolidation, prediction, attention, RL) | 24 |
| `neuro-primitives.md`      | Neuro-computational primitives (NNs, spiking, neuro-symbolic) | 30 |
| `memory-reasoning.md`      | Memory architectures, knowledge representation, multi-agent, causal, RL | 32 |
| `nslp-algorithms.md`       | **Deep dive** for the Neuro-Symbolic Language Processor (NSLP): mathematical machinery for the SXL/SXP operator layer | 60 |
| `theorems-and-bounds.md`   | Foundational theorems, complexity bounds, and approximation guarantees for the operator set | 24 |
| `canonical-references.md`  | Master reference list: every primary paper, textbook, and survey cited in this knowledge base | 80+ |
| `verification/`            | Append-only verification logs (one per verifier) | — |
| `README.md`                | This file                                        | — |

**Total algorithms profiled**: 200+.
**Total flagged `ready-for-promotion`**: 84.
**Total flagged `unconfirmed`**: 116+.

## How to read these files

Each entry follows the same structure:

1. **Year / citation** — primary source.
2. **Core idea** — 2-3 sentence summary.
3. **Community status** — validation
   evidence (textbook coverage,
   citation count, deployed systems,
   competition wins).
4. **Complexity** — computational
   complexity class and tractable
   restrictions.
5. **Pseudocode** — 10-20 line sketch.
6. **Worked example** — concrete
   numerical trace.
7. **Canonical reference URL** — arXiv
   preprint, university course, or open
   textbook chapter.
8. **Failure modes** — known edge cases
   or limitations.
9. **SXL shape** — the entity form
   the algorithm should produce.
10. **Confirmation flag** — see the
    table above.
11. **Ready-for-promotion** — ✅ or ⚠️
    with rationale.

## The promotion path

A `ready-for-promotion` algorithm in
this knowledge base becomes a
**first-class SXL operator** in
`~/seed-dev/` via the following flow:

1. **Spec entry**: add the algorithm
   to `~/seed-dev/codex/machina/`
   as an `(:type operator ...)` entry.
2. **C implementation**: the algorithm
   becomes a function in
   `~/seed-dev/src/libseedcog/` (or a
   similar C library).
3. **Lua binding**: a thin wrapper
   in
   `~/seed-dev/lua/agents/cognitive/`
   exposes the operator to the brain
   cycle.
4. **Tests**: per-algorithm tests
   in
   `~/seed-dev/tests/seedcog/`;
   coverage of the worked example
   is mandatory.
5. **Conformance corpus entry**: a
   canonical input/output pair
   appended to
   `~/seed-dev/tests/conformance/`.
6. **Bus topic** (if needed): a new
   `org.seed.cog.<algorithm>` topic
   is created following the
   FROZEN-2026-05-10 namespace.

This is a multi-step, multi-PR
process; the knowledge base entry
is the upstream prerequisite.
Promotion requires
✅ `confirmed-canonical` or
🟢 `confirmed-curated`.

## How agents and entities are added

The sapling catalog is in
`../AGENTS.md` and `../ENTITIES.md`.
When a new cognitive concept is
proposed that does not map cleanly
to any of S.E.E.D.'s 20 existing
domains, the agent enters sapling
with a reference to the relevant
section of this knowledge base.

When an agent graduates (see
`../INTEGRATION.md` §3), the
algorithm it implements moves to
the destination cognitive domain
in `~/seed-dev/src/seedcogd/`
and the entry in this knowledge
base is moved to
`~/seed-dev/codex/machina/`
as a "Promoted" status.

## The five cognitive-engine layers

The S.E.E.D. cognitive engine
(per the 5-layer model in
`~/solbian/engineering-manual/seed/00-INFRASTRUCTURE-OVERVIEW.md`)
is the integration point for these
algorithms:

- **L0 — Codex**: the formal spec
  (where promoted operators are
  catalogued).
- **L1 — seed-core**: the C cycle
  (12 phases A–L; algorithm
  implementations live here).
- **L2 — seed-control**: the
  orchestration of helpers
  (Lua).
- **L3 — seednet**: cross-node
  coordination of cognitive
  operations.
- **L4 — seed-cognition**: the
  user-facing cognitive services
  and the safety boundary.

The algorithms in this knowledge
base span all five layers:

- **L1 (C)**: SAT, CDCL, EKF, particle
  filter, ALC classification, KG
  embedding, attention, etc.
- **L2 (Lua)**: planning, RL, MCTS,
  hierarchical reasoning, BDI loops.
- **L3 (cross-node)**: federated
  learning, gossip protocols, PBFT,
  Raft, CRDTs.
- **L4 (user-facing)**: metacognition,
  confidence calibration, type-2 SDT.

## Cross-references

- `sxl-operators.md` — symbolic
  cognitive algorithms.
- `cognitive-cycles.md` — cognitive
  cycle and time-series algorithms.
- `neuro-primitives.md` — neuro-
  computational primitives.
- `memory-reasoning.md` — memory
  architectures, knowledge
  representation, multi-agent,
  causal, RL.
- `nslp-algorithms.md` — NSLP deep
  dive.
- `theorems-and-bounds.md` — theorems
  and complexity bounds.
- `canonical-references.md` — the
  master reference list.
- `verification/` — verification logs.
- `../README.md` — sapling directory
  overview.
- `../INTEGRATION.md` — how sapling
  agents connect to the bus.
- `~/seed-dev/docs/cognition/SXL_LANGUAGE_SPECIFICATION.md`
  — canonical SXL entity form.
- `~/seed-dev/src/seedcogd/main.c`
  — the 12-phase C cycle.
- `~/solbian/engineering-manual/seed/02-DAEMONS.md`
  — the daemons.
- `~/solbian/engineering-manual/sapling/02-SYMBOLIC-LAYER.md`
  — the symbolic substrate.
