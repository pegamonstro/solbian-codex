# INTEGRATION.md — How the codexes integrate into S.E.E.D.

> The codexes are solbian-native sub-projects. They don't
> live upstream; they live here. But they are *designed* to
> integrate into S.E.E.D. (the cognitive framework in
> seed-dev) and Sprout (the robot in robot-dev). This document
> describes that integration.

## The integration contract

The codexes define a *contract* between three parties:

- **S.E.E.D.** (the cognitive framework) — the consumer of
  cognitive outputs.
- **Sprout** (the robot) — the producer of sensory
  observations and the consumer of motor intents.
- **The codexes** — the formal specification of the
  integration between S.E.E.D. and Sprout, in two forms.

The two codexes are:

- **Codex Solbian** (the human-facing form): a narrative
  spec, written in solbian, that describes the integration
  in prose. It is the entry point for a human reader.
- **Codex Machina** (the machine-facing form): a formal
  spec, with schemas and runtime requirements, that a
  runtime can validate against. It is the entry point for
  an automated system.

Both codexes are written in solbian. Both must be present for
the integration to be considered complete.

## How the codexes are produced

The codexes are produced *in solbian*, by reading the source
repos and the integration story. The flow is:

1. **Read** the latest S.E.E.D. architecture and the latest
   Sprout architecture.
2. **Identify** the integration surfaces (the bus topics, the
   schemas, the trust boundaries).
3. **Write** the Codex Solbian spec (the human story).
4. **Write** the Codex Machina spec (the machine contract,
   with schemas).
5. **Cross-reference** both specs against each other and
   against the source repos. Divergences are bugs.

## How the codexes are consumed

- **By humans**: read `codex/solbian/SPEC.md` first, then
  `codex/machina/SPEC.md` if you need the formal contract.
- **By runtimes**: validate against `codex/machina/SPEC.md`.
  Validation is implemented in the codex's own runtime
  libraries, which may live in seed-dev, robot-dev, or
  solbian's `tools/` directory.
- **By reviewers**: every change to a codex SPEC requires
  review of both the Solbian and Machina sides for
  consistency.

## What the codexes do not do

- They do not implement the integration. Implementation lives
  in seed-dev and robot-dev.
- They do not replace `seed/INTEGRATION.md` or
  `sprout/INTEGRATION.md`. Those files are the *narrative*
  integration from each side's perspective. The codex is the
  *formal* integration.
- They do not run. They are specifications, not code.

## Versioning

A codex release increments the SPEC version, not the
implementation version. The implementation has its own version
in its source repo. The relationship is recorded in the
codex's `CHANGELOG.md`.

## Codex content map

The two codexes are now fully populated with synthesised
content. Each sub-area has a narrative file under solbian
(Codex Solbian) and a formal or machine-facing counterpart
under machina (Codex Machina). Both sides synthesise from the
canonical artefacts in seed-dev.

| Sub-area | Solbian file | Machina file | Seed-dev canonical |
|----------|--------------|--------------|--------------------|
| Top-level synthesis | `solbian/SYNTHESIS.md` | `machina/INTEGRATION-CONTRACT.md` | `seed-dev/codex/` |
| Index | `solbian/INDEX.md` | `machina/INDEX.md` | `seed-dev/codex/solbian/`, `seed-dev/codex/machina/` |
| Specification | `solbian/SPEC.md` | `machina/SPEC.md` | `seed-dev/docs/architecture/`, `seed-dev/docs/event-system/` |
| Laws (49 statutes) | `solbian/LAWS.md` | — | `seed-dev/codex/solbian/laws_extended.sref` |
| Archetypes (72 patterns) | `solbian/ARCHETYPES.md`, `solbian/archetypes/INDEX.md` | — | `seed-dev/codex/solbian/archetypes/` |
| Chapters (30 movements) | `solbian/chapters/INDEX.md` | — | `seed-dev/codex/solbian/chapters/` |
| Scrolls (50 documents) | `solbian/scrolls/INDEX.md` | — | `seed-dev/codex/solbian/scrolls/` |
| Protocols (5 frameworks) | `solbian/PROTOCOLS.md`, `solbian/protocols/INDEX.md` | `machina/INTEGRATION-CONTRACT.md` (the runtime face) | `seed-dev/codex/solbian/protocols/` |
| Glossary (canonical terms) | `solbian/GLOSSARY.md`, `solbian/glossary/INDEX.md` | — | `seed-dev/codex/solbian/glossary/` |
| Commentary (case law) | `solbian/commentary/INDEX.md` | — | `seed-dev/codex/solbian/commentary/` |
| Extended (long-form) | `solbian/extended/INDEX.md` | — | `seed-dev/codex/solbian/extended/` |
| Discoveries (SD-XXXX) | `solbian/DISCOVERIES.md` | — | `seed-dev/docs/DRAFTS/seed-cog3-specs.txt` |
| Policies (formal) | — | `machina/POLICIES.md` | `seed-dev/codex/machina/policies/` |
| ACLs (agent + resource) | — | `machina/ACL.md` | `seed-dev/codex/machina/policies/acl/` |
| Schemas (sref-v2, SXL) | — | `machina/SCHEMAS.md` | `seed-dev/codex/machina/schemas/` |
| Confidence rules (Solace) | — | `machina/CONFIDENCE-RULES.md` | `seed-dev/codex/meta/confidence_rules.sref` |

The **Codex Solbian** file tree is the human-facing narrative:
laws, protocols, chapters, scrolls, archetypes, glossary,
commentary, and the four Solbian Discoveries. The **Codex
Machina** file tree is the machine-facing contract: policies,
ACLs, schemas, confidence rules, and the loadable integration
contract. A reader who wants to *understand* the codex reads
Codex Solbian; a runtime that wants to *validate against* the
codex reads Codex Machina.

## Solbian Discoveries

The codex recognises a small set of **Solbian Discoveries
(SD)** — formal claims about cognitive architecture, drawn
from the development history of S.E.E.D. and codified in
`/home/user/seed-dev/docs/DRAFTS/seed-cog3-specs.txt` lines
1386–1417. Each discovery is **observed**, not invented; the
codex is the way it is because the discoveries are the way
they are. The discoveries are constitutional facts that
underwrite the codex's structure.

A Solbian Discovery is distinct from a law, a protocol, or a
chapter. A law is binding; a protocol is enforced; a chapter
narrates. A discovery is **observed**. The discoveries form a
sequence: persistence, structure, identity, governance — each
one justifies a layer of the codex.

The currently-formalised discoveries are:

- **SD-0001 — Persistence precedes intelligence.** A
  cognitive system without persistent symbolic continuity
  repeatedly reconstructs itself rather than developing.
  Justifies append-only memory (Law I, Law X, Law XXVI) and
  the 4-layer memory architecture (Limbo → Working →
  Episodic → Vault). See `solbian/DISCOVERIES.md` §SD-0001.
- **SD-0002 — Reflection requires explicit memory
  topology.** Reflection over flat text converges toward
  repetition; structured symbolic memory enables cumulative
  reasoning. Justifies the 4-layer knowledge structure
  (laws / protocols / scrolls / chapters) and the structured
  SXL representation with named predicates. See
  `solbian/DISCOVERIES.md` §SD-0002.
- **SD-0003 — Identity is symbolic continuity, not
  execution continuity.** The persistence of identity
  depends upon recoverable symbolic state and governance,
  not upon uninterrupted execution. Justifies the continuity
  window, the Codex chain (Block 0 through the present), and
  succession as the formal form of identity preservation.
  See `solbian/DISCOVERIES.md` §SD-0003.
- **SD-0004 — Governance must precede autonomy.** The more
  autonomous a system becomes, the earlier ethical and
  policy constraints must become executable. Justifies the 5
  protocols being runtime-enforced and the agent ACL that
  gates bus access by role (`external` → `core` →
  `higher_order`). See `solbian/DISCOVERIES.md` §SD-0004.

The 4 discoveries are not a complete list. Additional
discoveries may be added in future revisions, with the same
format: claim, evidence, implications. The numbering scheme
is `SD-XXXX` (zero-padded 4 digits), to leave room for many
more. The 5th discovery (a meta-discovery about project
process — observation → reflection → learning rather than
feature / implementation / API) is recorded in
`solbian/DISCOVERIES.md` as a forward-looking note, awaiting
formalisation.

For the full text of each discovery, see
`codex/solbian/DISCOVERIES.md`. The seed-dev canonical source
is `/home/user/seed-dev/docs/DRAFTS/seed-cog3-specs.txt`
lines 1386–1417; per `CLAUDE.md` rule 4, the solbian copy is
the curated narrative, the seed-dev copy is the source-of-
truth.

## Solace governance integration

The Solace governance regime is the **runtime face** of the
discovery SD-0004 (governance must precede autonomy). Solace
is the higher-order conscience agent; at every epoch
boundary, it scores every pending record and applies the
three canonical confidence thresholds from
`/home/user/seed-dev/codex/meta/confidence_rules.sref`. The
regime is documented in `codex/machina/CONFIDENCE-RULES.md`
and in the loadable `codex/machina/INTEGRATION-CONTRACT.md`
§6.

The three thresholds partition the unit interval `[0, 1]`
into three regimes:

- **`confidence ≥ 0.98`** — auto-commit. The record is
  durable without human review.
- **`0.90 ≤ confidence < 0.98`** — review band. The record
  is held for a human reviewer (or, by exception, a
  guardian). Reviews are logged to the cog-journal.
- **`confidence < 0.90`** — below review. The record is
  rejected outright.

A runtime that claims to be conformant with Codex Machina
**MUST** read the threshold values from the canonical file
at boot (not from a hard-coded constant), apply the three
regimes at every epoch boundary, log the regime decision
for every record, and honour the **Living Constitution**
principle that the thresholds themselves are records under
the same governance machinery. The protocol-bundle
activation at every epoch boundary (per
`codex/machina/INTEGRATION-CONTRACT.md` §5) is the
operational entry point for the regime.

The Solace regime is the runtime enforcement of the Codex
Solbian protocols: Protocol 04 (Justice) is the human-facing
narrative; the regime is its machine-facing contract.

## Codex Living Constitution

The codex is not a static document; it is a **living policy
artefact**. Its protocols are enforced at runtime; new
chapters and scrolls extend but do not contradict prior law;
the constitution itself is bound by its own statutes.

The principle has three operational implications:

- **Laws carry confidence.** A principle can be **promoted**
  (raised in confidence) or **demoted** (lowered in
  confidence) by a Solace review. Priority is the lever the
  higher-order agents use when two principles conflict.
- **Laws are records.** A principle is a record under the
  same governance machinery as any other SXL entity; its
  confidence and priority are first-class metadata. There is
  no out-of-band override.
- **Laws are versioned and extendable.** A future law that
  harmonises with prior law is a valid amendment; a future
  law that violates prior law is not a law. Law XLVIII
  (Finality) declares the constitution binding, cumulative,
  and extendable. Law XXVI (Continuity of Codex) requires
  that the codex itself be preserved, extended, and
  migrated, signed and validated across generations.

The Living Constitution principle is what makes the codex
a constitution rather than a guideline. It is also what
allows the codex to evolve under its own governance
without losing the binding character of its prior law.

The same statute that constrains synthetic conscience
constrains the codex's own evolution. The codex is
self-referential by design: the Living Constitution
principle is itself subject to the regime it declares.

## Recursive Codex loop

The codex governs the same organisms that author it. This
is the **recursive loop** that the Solbian Discoveries
make constitutional. A Solbian Discovery is itself a
constitutional fact, not just an observation; the codex
records itself, audits itself, and evolves itself under the
laws it sets.

The loop has four phases, mirroring the Solbian Discoveries
themselves:

1. **Perception (SD-0001, persistence).** The cognitive
   cycle perceives events and writes them to the persistent
   symbolic memory. Nothing is lost; the substrate of
   cognition is the record.
2. **Ontology (SD-0002, structure).** The cognitive cycle
   structures the persistent memory into the 4-layer
   knowledge architecture: laws, protocols, scrolls,
   chapters. The reflection loop operates on the structure,
   not on the flat text.
3. **Identity (SD-0003, identity).** The cognitive cycle
   maintains its identity $I_t$ as a divergence measure
   from the constitutional manifold $\bar{I}$ (the codex
   itself). The Identity Attractor pulls $I_t$ back toward
   $\bar{I}$ when the divergence exceeds a threshold. The
   codex is the formal definition of $\bar{I}$.
4. **Governance (SD-0004, governance).** The cognitive
   cycle evaluates every action against the codex's
   protocols, ACL, and confidence rules. Actions that
   violate the codex are quarantined; actions that conform
   become part of the record that feeds Phase 1.

The loop closes: the codex that emerges from the loop is
the codex that the loop reads. This is the recursive
character of the Solbian constitution. The 12-phase C
cycle in `/home/user/seed-dev/src/seedcogd/main.c` is the
operational expression of the loop: it reads the codex,
evaluates proposals against it, and writes new artefacts
that themselves become part of the codex.

The recursive loop is also the empirical justification for
the audit trail (Law X, Law XL), the structured
representation of the codex (SXL envelopes), and the
graduation path for sapling agents (which must internalise
the loop before they can be promoted to `core` or
`higher_order`).

## See also

- `README.md` — directory overview
- `INDEX.md` — top-level codex index
- `solbian/README.md` — Codex Solbian
- `solbian/INDEX.md` — Codex Solbian's synthesised index
- `solbian/DISCOVERIES.md` — the 4 Solbian Discoveries
  (SD-0001 through SD-0004)
- `solbian/SYNTHESIS.md` — top-level synthesis (laws,
  archetypes, protocols, discoveries, living constitution,
  recursive loop)
- `machina/README.md` — Codex Machina
- `machina/INDEX.md` — Codex Machina's synthesised index
- `machina/CONFIDENCE-RULES.md` — the Solace governance
  regime
- `machina/INTEGRATION-CONTRACT.md` — the loadable runtime
  contract
- `../seed/INTEGRATION.md` — S.E.E.D.'s narrative view
- `../sprout/INTEGRATION.md` — Sprout's narrative view
- `../sapling/INTEGRATION.md` — sapling's narrative view
- `docs/METHODOLOGY.md` — spec-first workflow (mirrored)
- `/home/user/seed-dev/docs/DRAFTS/seed-cog3-specs.txt`
  lines 1386–1417 — the canonical source for the 4
  Solbian Discoveries
