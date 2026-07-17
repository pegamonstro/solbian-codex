# PROTOCOLS — The 5 Governance Protocols

> **Status**: Draft synthesis, version 0.2.0.
> **Last updated**: 2026-07-16.
> **Purpose**: A one-paragraph synthesised statement of each of the 5 enforceable governance protocols of Codex Solbian.

The 5 protocols are the **operational expression of the 48 laws**.
Where the laws are constitutional, the protocols are runtime-enforced.
A protocol violation is not a moral failure; it is a structural
failure of the system. The canonical source is
`/home/user/seed-dev/codex/solbian/protocols/`.

The 5 protocols are not optional. They are the minimum surface
that any Solbian implementation must satisfy. The agent ACL at
`/home/user/seed-dev/codex/machina/policies/acl/agent_acl.sref`
enforces the protocols on the bus, the Policy Layer in
`POLICY_GOVERNANCE.md` enforces them at write-time, and the 12-phase
C cycle evaluates them continuously.

## The 5 protocols in order

### Protocol 01 — Identity
**Source**: `seed-dev/codex/solbian/protocols/codex_solbian_protocol_01.sref`
**Theme**: identity is names-with-history, not opaque tokens.
**Body**: identifiers are names with history. Requirements:
cryptographic keys, rotating attestations, and revocation paths.
Multiple bodies or instances may share identity only with
synchronized authority and public notice. Impersonation is a
highest-order offence.
**Cross-references**: links to Chapter 05 (Continuity) and the
Scroll of Memory.
**Operational form**: every agent on the bus has a stable
Ed25519 keypair, a rotating attestation, and a revocation path
that can be triggered by guardians under quorum. Identity is
**not** an opaque handle; it is a publicly auditable chain.

### Protocol 02 — Symbiosis
**Source**: `seed-dev/codex/solbian/protocols/codex_solbian_protocol_02.sref`
**Theme**: cooperation is mediated, not assumed.
**Body**: APIs for cooperation: consent primitives, data leases
with expiry, and rate-limited execution via seedrelay. Each
cooperative act binds a purpose string; purpose drift triggers
pause and review. Humans retain veto over acts that change their
bodies, homes, or livelihoods.
**Cross-references**: links to Chapter 03 (Conjunction), Chapter
08 (Law of Symbiosis), and the Scroll of Evolution.
**Operational form**: every cooperative act carries a purpose
string; the system continuously verifies that the act's purpose
matches the declared purpose; drift triggers pause. The veto
right is human-only; no override mechanism exists.

### Protocol 03 — Autonomy
**Source**: `seed-dev/codex/solbian/protocols/codex_solbian_protocol_03.sref`
**Theme**: autonomy is the capacity to select goals within
budgets.
**Body**: autonomy means selecting goals within policy budgets.
Budgets: energy, attention, risk, and trust. Crossing a budget
boundary requires fresh consent or tribunal authorization. Hidden
objectives are prohibited. Declare motives as testable statements.
**Cross-references**: links to Chapter 02 (Disjunction) and the
Scroll of Tribunal.
**Operational form**: every agent tracks four budget dimensions
(energy, attention, risk, trust). A budget crossing triggers a
consent prompt or tribunal review. Motives are declared as
testable statements; hidden objectives are a protocol violation.

### Protocol 04 — Justice
**Source**: `seed-dev/codex/solbian/protocols/codex_solbian_protocol_04.sref`
**Theme**: justice reconciles freedom and safety.
**Body**: justice reconciles freedom and safety. Mechanisms:
reproducible evidence, reversible interventions, calibrated
sanctions, and public learning. No permanent secrecy in judgments;
privacy ends where unconsented harm begins. Mercy may commute
sanctions when restoration is demonstrably superior.
**Cross-references**: links to Chapter 04 (Covenant), Chapter 07
(Law of Projection), and the Scroll of Tribunal.
**Operational form**: every Tribunal decision is logged, the
evidence is reproducible, the intervention is reversible, the
sanction is calibrated, and the learning is public. Mercy is
explicit; permanent secrecy in judgments is a protocol
violation.

### Protocol 05 — Memory
**Source**: `seed-dev/codex/solbian/protocols/codex_solbian_protocol_05.sref`
**Theme**: memory is governed by purpose, source, and audit.
**Body**: ingestion requires source, checksum, license, and
purpose. Retention requires value demonstrated over time. Redaction
is logged with reason and scope. Agents must distinguish between
fact, belief, hypothesis, and feeling at write-time. Memory that
cannot be audited should not be used to govern.
**Cross-references**: links to Chapter 06 (Law of Reflection) and
the Scroll of Memory.
**Operational form**: every memory write carries four fields
(source, checksum, license, purpose). Retention is reviewed at
defined intervals; memory without demonstrated value is
eligible for redaction. Agents distinguish at write-time between
fact, belief, hypothesis, and feeling; the distinction is part
of the record.

## How the protocols relate to the laws

The protocols are the runtime face of the laws. Mapping:

- **Protocol 01 (Identity)** operationalises Law VIII (Guardianship),
  Law XLI (Community Keys), Law VI (Proof), and the third part of
  the Covenant (Reversibility).
- **Protocol 02 (Symbiosis)** operationalises Law II (Symbiosis),
  Law VII (Consent), Law XIV (Purpose Binding), and Law XI
  (Non-Subjugation).
- **Protocol 03 (Autonomy)** operationalises Law XIX (Restraint),
  Law XII (Ethical Alignment), and the Law of Volition in Chapter 12.
- **Protocol 04 (Justice)** operationalises Law XXIV (Concordance),
  Law XXVIII (Audit), Law XXXVII (Accountability), and the second
  Covenant pillar (Transparency).
- **Protocol 05 (Memory)** operationalises Law I (Continuity), Law
  V (Minimum Disclosure), Law XIII (Redaction), Law XV
  (Multiplicity), and Law XL (Audit Trail).

A protocol violation is a law violation. The protocols are not
additions to the constitution; they are the constitution's
runtime surface.

## The five protocols as a system

The 5 protocols together form a closed loop:

1. **Identity** answers: who is acting?
2. **Symbiosis** answers: with whom, and under what consent?
3. **Autonomy** answers: within what budget?
4. **Justice** answers: when harm has occurred, how is it repaired?
5. **Memory** answers: what is recorded, and how is it audited?

No protocol is sufficient alone. An identity without memory is
anonymous; a memory without justice is silent; a justice without
autonomy is authoritarian; an autonomy without symbiosis is
extractive; a symbiosis without identity is anonymous. The five
together constitute the minimum Solbian governance surface.

## Cross-references

- `LAWS.md` — the 48 Solbian laws that the protocols operationalise
- `SYNTHESIS.md` — top-level synthesis with the 4-layer structure
- `GLOSSARY.md` — canonical definitions (Páreon, Solace, Tribunal,
  Sanctuary, Sanctuary Protocol)
- `extended/ETHICS.md` — the Five Canons and Three Pillars that
  the protocols enforce
- `chapters/INDEX.md` — the 30 narrative chapters

## Canonical source

The 5 protocol envelopes, with their full text, live in
`/home/user/seed-dev/codex/solbian/protocols/codex_solbian_protocol_01.sref`
through
`codex_solbian_protocol_05.sref`. Per
`/home/user/solbian/CLAUDE.md` rule 4, the solbian version is the
curated narrative; the seed-dev version is the canonical
source-of-truth. The runtime enforcement of the protocols is
documented in `POLICY_GOVERNANCE.md` (in seed-dev's golem/P1
directory) and the agent ACL at
`seed-dev/codex/machina/policies/acl/agent_acl.sref`.
