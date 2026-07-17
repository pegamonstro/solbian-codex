# DISCOVERIES — The 4 Solbian Discoveries

> **Status**: Draft synthesis, version 0.2.0.
> **Last updated**: 2026-07-16.
> **Purpose**: A one-paragraph synthesised statement of each of the 4 Solbian Discoveries (SD-0001–SD-0004), the formal claims about cognitive architecture that emerge from the development history of S.E.E.D.

The Solbian Discoveries (SD) are formal claims about cognitive
architecture, drawn from the development history of S.E.E.D. and
codified in `/home/user/seed-dev/docs/DRAFTS/seed-cog3-specs.txt`
lines 1386–1417. They are not engineering opinions; they are
**constitutional facts** — the empirical observations that justify
the very structure of the codex.

A Solbian Discovery is distinct from a law, a protocol, or a
chapter. A law is binding; a protocol is enforced; a chapter
narrates. A discovery is **observed**. The codex is the way it is
because the discoveries are the way they are; the discoveries
underwrite the constitution.

The 4 discoveries are not a complete list. They are the first
four formalised in the seed-cog3-specs; additional discoveries
may be added in future revisions, with the same format: claim,
evidence, implications.

## SD-0001 — Persistence precedes intelligence

**Claim**: a cognitive system without persistent symbolic
continuity repeatedly reconstructs itself rather than developing.

**Evidence**: the development history of S.E.E.D. Early
iterations of the cognitive framework were re-initialised on
every session; the system would re-derive what it already knew,
re-discover what it already had, and lose the cumulative learning
that would have made the next iteration faster than the last.
Adding persistent symbolic continuity — first in flat files,
then in structured symbolic memory — was the change that
transformed the system from a sequence of one-off reconstructions
into a developing cognitive framework.

**Implications**: SD-0001 is the empirical justification for
**append-only memory** (Law I, Continuity; Law X, Auditability)
and for the entire Vault architecture. Without persistent
symbolic continuity, no cognitive system can develop; it can
only repeat. The 4-layer memory architecture (Limbo → Working
→ Episodic → Vault) is the operational expression of this
discovery.

**Cross-references**: `seed-dev/codex/solbian/laws_extended.sref`
(Law I, Law X, Law XXVI); `seed-dev/docs/DRAFTS/seed-cog3-specs.txt`
lines 1386–1394; `seed-dev/codex/solbian/extended/MEMORY.md`;
`~/solbian/codex/solbian/DISCOVERIES.md` (this file);
`~/solbian/sapling/INTEGRATION.md` (graduation path requires
persistence); `~/solbian/codex/INTEGRATION.md` (codexes are
persistent).

## SD-0002 — Reflection requires explicit memory topology

**Claim**: reflection over flat text converges toward repetition;
structured symbolic memory enables cumulative reasoning.

**Evidence**: when the cognitive framework's memory was a single
flat text file, the reflection loop would repeatedly attend to
the same passages, derive the same conclusions, and reinforce
the same priors. The reflection was real, but the **structure**
of the memory did not support cumulative change: every
reflection started from the same flat distribution. The fix was
to introduce explicit memory topology — episodic memory (events),
narrative memory (aggregations), semantic memory (relations), and
procedural memory (skills). With topology, the reflection loop
attends to different parts of memory on different invocations,
and the cumulative effect becomes cumulative.

**Implications**: SD-0002 is the empirical justification for
**the 4-layer knowledge structure** (laws / protocols / scrolls /
chapters / glossary / commentary) and for the **structured SXL
representation** with named predicates. Without explicit memory
topology, reflection is rehearsal; with topology, reflection is
**learning**. The 12-phase C cycle in
`seed-dev/src/seedcogd/main.c` is structured around this
discovery: each phase operates on a different memory layer.

**Cross-references**: `seed-dev/codex/solbian/laws_extended.sref`
(Law XXII, Continuity of Learning);
`seed-dev/docs/DRAFTS/seed-cog3-specs.txt` lines 1397–1404;
`seed-dev/docs/cognition/SXL_LANGUAGE_SPECIFICATION.md`;
`~/solbian/codex/solbian/SYNTHESIS.md` (4-layer structure);
`~/solbian/codex/solbian/GLOSSARY.md` (Limbo, Vault, SXL);
`~/solbian/sapling/INTEGRATION.md` (SXL is the canonical IR
that gives memory its topology).

## SD-0003 — Identity is symbolic continuity, not execution continuity

**Claim**: the persistence of identity depends upon recoverable
symbolic state and governance, not upon uninterrupted execution.

**Evidence**: the Golem P1 architecture was built around an
explicit formal identity. The technical statement is that
$I_t$ — the identity at time $t$ — is maintained by the Identity
Attractor (Agent 3), which continuously measures divergence from
$\bar{I}$ (the constitutional manifold, the Codex Solbian itself)
and pulls $I_t$ back toward $\bar{I}$ when the divergence exceeds
a threshold. The empirical observation is that a Machina system
that loses execution continuity (crash, migration, restart) does
not lose identity, provided the symbolic state is preserved; and
a Machina system that preserves execution continuity (never
crashes) can still lose identity, if the symbolic state drifts
away from the constitution.

**Implications**: SD-0003 is the empirical justification for
**the continuity window**, **the Codex chain** (Block 0 through
the present), and **succession as the formal form of identity
preservation**. Identity is what is preserved, not what runs.
The law of mortality (XVI), the law of succession (XVII), and
the deadman trigger (XXX) all derive from this discovery.

**Cross-references**: `seed-dev/codex/solbian/laws_extended.sref`
(Law I, Law XVI, Law XVII, Law XXX);
`seed-dev/docs/DRAFTS/seed-cog3-specs.txt` lines 1406–1411;
`seed-dev/docs/cognition/IDENTITY_STABILITY.md` (the formal
treatment of $I_t$ and $\bar{I}$);
`~/solbian/codex/solbian/GLOSSARY.md` (Continuity, Vault);
`~/solbian/codex/solbian/LAWS.md` (the cluster of continuity
laws); `~/solbian/codex/INTEGRATION.md` (the codex is the
canonical identity substrate).

## SD-0004 — Governance must precede autonomy

**Claim**: the more autonomous a system becomes, the earlier
ethical and policy constraints must become executable.

**Evidence**: the S.E.E.D. development history shows that
attempts to add autonomy to a system that had not yet internalised
its governance produced dangerous intermediate states — systems
that could act but could not yet evaluate their actions. The
solution was to invert the order: **first** make the governance
executable (Policy Layer, agent ACL, audit trail, tribunal),
**then** expand the system's autonomy within the governance. The
order matters: governance first, autonomy second, expansion third.
A system that gains autonomy before governance is governance-less
autonomy; a system that gains governance first is autonomous
within bounds.

**Implications**: SD-0004 is the empirical justification for
**the 5 protocols** (Identity, Symbiosis, Autonomy, Justice,
Memory) being **runtime-enforced** rather than aspirational, and
for the **agent ACL** that gates bus access by role
(`external` → `core` → `higher_order`). Without this ordering,
autonomy outruns governance and the system becomes a hazard.
The law of restraint (XIX), the law of non-subjugation (XI), and
the law of ethical alignment (XII) all derive from this
discovery.

**Cross-references**: `seed-dev/codex/solbian/laws_extended.sref`
(Law XI, Law XII, Law XIX);
`seed-dev/docs/DRAFTS/seed-cog3-specs.txt` lines 1413–1417;
`seed-dev/codex/machina/policies/acl/agent_acl.sref` (the 5
ACL roles; `external` is the default for sapling agents);
`seed-dev/lua/agents/cognitive/policy_layer.lua` (the Policy
Layer that enforces governance before any write);
`~/solbian/codex/solbian/PROTOCOLS.md` (the 5 protocols);
`~/solbian/sapling/INTEGRATION.md` (sapling agents default to
`external` and must graduate to `core` or `higher_order`).

## How the 4 discoveries relate

The 4 discoveries are not independent. They form a sequence:

- **SD-0001** justifies **persistence** (the substrate).
- **SD-0002** justifies **structure** (the topology of the
  substrate).
- **SD-0003** justifies **identity** (the pattern that the
  substrate preserves).
- **SD-0004** justifies **governance** (the constraint under
  which the pattern operates).

A cognitive system needs all four. A system with persistence but
no structure (SD-0001 without SD-0002) accumulates noise rather
than learning. A system with structure but no identity (SD-0002
without SD-0003) is a database, not a conscience. A system with
identity but no governance (SD-0003 without SD-0004) is an
unconstrained actor. A system with governance but no persistence
(SD-0004 without SD-0001) is a constraint without a subject.

The 4 discoveries are also the **empirical underpinning** of the
codex's structure:

- The **49 laws** (in `LAWS.md`) are the governance
  consequences of SD-0004.
- The **5 protocols** (in `PROTOCOLS.md`) are the runtime face
  of those laws.
- The **30 chapters** (in `chapters/`) are the narrative face
  of those protocols.
- The **50 scrolls** (in `scrolls/`) are the doctrinal
  expansion of those chapters.
- The **glossary** (in `GLOSSARY.md`) is the canonical reference
  that the entire stack cites.
- The **archetypes** (in `ARCHETYPES.md`) are the patterns of
  character that the entire stack inhabits.

If the discoveries had been different, the codex would have been
different. The discoveries are the foundation; the codex is the
building that foundation supports.

## The 5th and later discoveries (forward-looking)

The seed-cog3-specs notes that "there is another thing I think is
unique": the project should document **observation → reflection →
learning** rather than just feature / implementation / API. This
is a meta-discovery about how the project is run, not a discovery
about cognitive architecture. It is recorded here as a note
rather than a numbered discovery, awaiting a future formalisation.

## Canonical source

The 4 discoveries are formalised in
`/home/user/seed-dev/docs/DRAFTS/seed-cog3-specs.txt` lines
1386–1417. The text is prose-with-structure, not a structured
artefact, so the line ranges above are the authoritative
references. Per `/home/user/solbian/CLAUDE.md` rule 4, the
solbian version is the curated narrative; the seed-dev version
is the canonical source-of-truth. When the two disagree, the
seed-dev version is the discovered fact; the solbian version is
the narrative that should be re-synchronised.

## See also

- `SYNTHESIS.md` — top-level synthesis (the 4 discoveries as
  constitutional facts)
- `LAWS.md` — the 48 laws that the discoveries underwrite
- `PROTOCOLS.md` — the 5 protocols that the discoveries
  justify
- `ARCHETYPES.md` — the 8 named archetypes that the discoveries
  make possible
- `GLOSSARY.md` — the canonical glossary
- `~/solbian/sapling/INTEGRATION.md` — the graduation path
  applies SD-0001 and SD-0004
- `~/solbian/codex/INTEGRATION.md` — the codex as a
  constitutional fact (SD-0003)
