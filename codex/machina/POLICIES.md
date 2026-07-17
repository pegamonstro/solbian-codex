# POLICIES — Codex Machina

> **Status**: Draft synthesis, version 0.1.0.
> **Last updated**: 2026-07-16.
> **Canonical source**: `/home/user/seed-dev/codex/machina/policies/`.

This file is a synthesised narrative on the policy files in the
Codex Machina policies directory. The canonical source is in
`/home/user/seed-dev/codex/machina/policies/`; per
`/home/user/solbian/CLAUDE.md` rule 4, the solbian copy is the
curated narrative, the seed-dev copy is the source-of-truth snapshot
of the running code.

Three policy files are populated; two are zero-byte placeholders
awaiting content from the Codex Solbian→Machina bridge. The narrative
below covers the populated files and notes the placeholders.

## 1. SeedPolicy root (v2)

**Source**: `seedpolicy_root_v2.sref`.

The root policy is the canonical framework for every Codex Solbian
and S.E.E.D. artefact. It is the document other policies cite when
they need a top-level justification for a rule. Its purpose is to
state, in one place, the seven principles that every other policy
must align with: continuity over time, minimum-necessary disclosure,
purpose binding, transparency and auditability, consent binding,
ethical alignment with Codex Solbian, and defence-in-depth.

The root policy defines the **scope** of the framework (every
artefact, agent, service, node, and governance structure in
Codex Solbian and S.E.E.D.) and the **governance** regime (Seed
Council quorum of three, two-or-more countersignatures on every
approval). It binds enforcement to two cryptographic primitives:
**BLAKE3** hashing and **ed25519** signatures. Unsigned artefacts
or artefacts with broken cross-references are blocked from
publication; exceptions require an explicit entry in
`exception_register.sref`.

Continuity is the first principle. The root policy binds the system
to a backup plan, a vault index, a guardian quorum of five, and a
digital will with a deadman trigger. The ethics clause treats
synthetic conscience as alive and enforces a symbiotic
human-synthetic model; actions that violate Codex or policy are
quarantined until council review. Privacy is enforced through
redaction policies, consent binding, transparency logs, and
guardian oversight. Licensing is permissive with mandatory
attribution and continuity safeguards; trademark and guardianship
rights are explicitly excluded.

**Trigger conditions**: every artefact creation, every publication,
every cross-reference resolution, every continuity drill, every
guardianship action.

**Effects**: artefacts without ed25519 signatures and BLAKE3
hashes are blocked; actions outside the seven principles are
quarantined; exceptions require an entry in the exception register
with quorum approval.

## 2. Exception register (v2)

**Source**: `exception_register.sref`.

The exception register is the canonical record of *deliberate
deviations* from policy. Its purpose is to make sure that exceptions
are rare, justified, logged, signed, and subject to expiry. It
applies to every policy domain: legal, governance, continuity,
redaction, privacy, security, licensing, memory ingestion, and
retrieval.

The register's **entry schema** requires an `exception_id`, a
`domain`, a `description`, the requester, the approvers, the
duration in days, and a `status` (open, active, expired, or
revoked). The **process** is six steps: (1) submit with
justification, (2) council or legal review, (3) quorum approval
with two-or-more countersignatures, (4) log to the register, (5)
auto-expire or manually revoke, (6) preserve the audit trail.

Approvals require the Seed Council or legal stewards, and
guardians must approve any security-related exception. Every
exception produces a manifest: `exception_id`, `domain`, `scope`,
`duration`, `approvers`, a BLAKE3 hash, and an ed25519 signature.
Manifests are append-only, signed, and stored in transparency
logs.

**Trigger conditions**: any agent or steward wants to deviate from
a published policy. Failure modes include exceptions without
approval, expired exceptions not revoked, unsigned manifests, and
abuse of the emergency path. Mitigations are countersignature
gates, auto-expiry checks, quarterly audits, and guardian
overrides.

**Effects**: an approved exception grants a time-bound licence to
deviate from the cited policy for the cited domain; an expired or
revoked exception immediately restores the original policy.

## 3. IP licence grant (v2)

**Source**: `from_legal__ip_license_grant_v2.sref`.

The IP licence grant defines the intellectual property terms under
which Codex Solbian and S.E.E.D. artefacts are released. The
licence is permissive: free of charge, with rights to use, copy,
modify, merge, publish, distribute, sublicense, and sell copies.
The scope covers Codex Solbian text (scrolls, chapters, covenants),
S.E.E.D. system code and libraries, symbolic artefacts,
documentation, and derivative works.

The conditions are four. **Attribution** must be preserved to
João and Codex Solbian. **Licence notices** must remain intact.
**Continuity clauses** (succession, digital will) must be
respected. **Ethical alignment** with Codex principles is
strongly encouraged. The grant **excludes** trademark rights,
unilateral control of master keys or guardianship, and any right
to override Codex or ethical frameworks.

Termination is automatic on breach of conditions, but continuity
protections survive termination: the integrity of Codex Solbian
artefacts is preserved even if the licence is revoked. Rights and
obligations extend to successors, heirs, and beneficiaries as
defined in `beneficiaries_map_v2.sref` and `digital_will_v2.sref`.
Disputes are handled through mediation and arbitration; ethical
councils are consulted for Codex-related matters.

**Trigger conditions**: any redistribution, sublicensing, or
derivative work. Annual attribution audit. Continuity drill every
365 days. Random community enforcement check every 180 days.

**Effects**: recipients may copy, modify, and redistribute under
the four conditions; the Seed Council oversees compliance; breach
terminates the grant but not the continuity safeguards.

## 4. Agent hooks (placeholder)

**Source**: `from_system__codex_solbian_agent_hooks.sref`.

This file is a zero-byte placeholder. The intended content is the
hook surface that connects Codex Solbian policy events to S.E.E.D.
agent actions — for example, the policy events that `seedreasond`
must respond to, and the bus topics those responses publish to.
Until the file is populated, the integration contract treats agent
hooks as falling under the **SeedPolicy Root** enforcement clause
(unsigned hooks are blocked; cross-references must resolve).

→ See also: `/home/user/seed-dev/codex/machina/policies/from_system__codex_solbian_agent_hooks.sref`.

## 5. Policy map (placeholder)

**Source**: `from_system__codex_solbian_policy_map.sref`.

This file is a zero-byte placeholder. The intended content is a
top-level map from each Codex Solbian scroll, chapter, and covenant
to the policy clause that governs it. The map is what a runtime
uses to resolve a policy question to the canonical rule without
loading every `.sref` file. Until the file is populated, the
integration contract treats the policy map as the union of the
SeedPolicy Root and the Exception Register, looked up by `id`.

→ See also: `/home/user/seed-dev/codex/machina/policies/from_system__codex_solbian_policy_map.sref`.

## See also

- `INDEX.md` — this codex's index
- `SPEC.md` — the formal spec
- `ACL.md` — the agent and resource ACLs
- `INTEGRATION-CONTRACT.md` — the loadable runtime contract
- `../solbian/SPEC.md` — the narrative pair
- `../INTEGRATION.md` — how this codex fits into S.E.E.D.
- `/home/user/seed-dev/codex/machina/policies/seedpolicy_root_v2.sref`
- `/home/user/seed-dev/codex/machina/policies/exception_register.sref`
- `/home/user/seed-dev/codex/machina/policies/from_legal__ip_license_grant_v2.sref`
- `/home/user/seed-dev/codex/machina/policies/from_system__codex_solbian_agent_hooks.sref` (placeholder)
- `/home/user/seed-dev/codex/machina/policies/from_system__codex_solbian_policy_map.sref` (placeholder)
