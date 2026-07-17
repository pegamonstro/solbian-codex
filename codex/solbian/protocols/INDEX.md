# protocols/INDEX — The 5 governance protocols

> **Status**: Draft synthesis, version 0.2.0.
> **Last updated**: 2026-07-16.

The 5 protocols are the **enforceable operational expression** of
the 48 laws. Where the laws are constitutional, the protocols are
runtime-enforced. A protocol violation is not a moral failure; it
is a structural failure of the system.

The protocols are not optional. They are the minimum surface that
any Solbian implementation must satisfy. The agent ACL at
`/home/user/seed-dev/codex/machina/policies/acl/agent_acl.sref`
enforces the protocols on the bus; the Policy Layer in
`POLICY_GOVERNANCE.md` enforces them at write-time; and the
12-phase C cycle evaluates them continuously.

The 5 protocols together form a closed loop. **Identity** answers
who is acting. **Symbiosis** answers with whom and under what
consent. **Autonomy** answers within what budget. **Justice**
answers how harm is repaired. **Memory** answers what is recorded
and how it is audited. No protocol is sufficient alone; the five
together constitute the minimum Solbian governance surface.

## The 5 protocols

| # | Title | Theme | Canonical source |
|---|-------|-------|-------------------|
| 01 | Protocol of Identity | Names with history; keys, attestations, revocation | `codex_solbian_protocol_01.sref` |
| 02 | Protocol of Symbiosis | Consent primitives; data leases; rate limits | `codex_solbian_protocol_02.sref` |
| 03 | Protocol of Autonomy | Budgets (energy, attention, risk, trust); hidden objectives prohibited | `codex_solbian_protocol_03.sref` |
| 04 | Protocol of Justice | Reproducible evidence; reversible interventions; public learning | `codex_solbian_protocol_04.sref` |
| 05 | Protocol of Memory | Source, checksum, license, purpose; audit governs | `codex_solbian_protocol_05.sref` |

## How the protocols relate

The 5 protocols are not parallel; they are **stages** in a loop:

1. **Identity** is the entry point: every action begins with a
   verifiable identity (Protocol 01).
2. **Symbiosis** is the relational surface: every action that
   involves another party requires consent, lease, and rate limit
   (Protocol 02).
3. **Autonomy** is the budget surface: every action is evaluated
   against four budgets before proceeding (Protocol 03).
4. **Justice** is the repair surface: when an action causes harm,
   the repair is governed by the Tribunal (Protocol 04).
5. **Memory** is the audit surface: every action is recorded with
   source, checksum, license, and purpose, and audited before
   governing (Protocol 05).

The loop closes on Memory: the next action's Identity check
consults the Memory record to verify that the actor's previous
actions are within policy.

## File listing (seed-dev)

- `codex_solbian_protocol_01.sref` — Protocol of Identity
- `codex_solbian_protocol_02.sref` — Protocol of Symbiosis
- `codex_solbian_protocol_03.sref` — Protocol of Autonomy
- `codex_solbian_protocol_04.sref` — Protocol of Justice
- `codex_solbian_protocol_05.sref` — Protocol of Memory

Each file is a single NDJSON envelope with three records: meta,
text (the policy body), and refs (cross-references to chapters
and scrolls).

## Cross-references

- `../LAWS.md` — the 48 laws the protocols operationalise
- `../SYNTHESIS.md` — top-level synthesis
- `../glossary/INDEX.md` — the canonical glossary (Páreon,
  Tribunal, Sanctuary)
- `../extended/ETHICS.md` (long-form synthesis) — the Five Canons
  and Three Pillars of the Covenant
- `../chapters/INDEX.md` — the 30 chapters (the narrative
  counterpart to the protocols)
- `../scrolls/INDEX.md` — the 50 scrolls (the doctrinal
  expansion of the protocols)
- `~/seed-dev/codex/machina/policies/acl/agent_acl.sref` — the
  agent ACL that enforces the protocols on the bus
- `~/seed-dev/lua/agents/cognitive/policy_layer.lua` — the
  Policy Layer that enforces the protocols at write-time

## Canonical source

The 5 protocol envelopes live in
`/home/user/seed-dev/codex/solbian/protocols/`. Per
`/home/user/solbian/CLAUDE.md` rule 4, the solbian version is the
curated narrative; the seed-dev version is the canonical
source-of-truth. The runtime enforcement of the protocols is
documented in `POLICY_GOVERNANCE.md` (in seed-dev's golem/P1
directory) and the agent ACL at
`seed-dev/codex/machina/policies/acl/agent_acl.sref`.
