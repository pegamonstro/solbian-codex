# ACL — Codex Machina

> **Status**: Draft synthesis, version 0.1.0.
> **Last updated**: 2026-07-16.
> **Canonical source**: `/home/user/seed-dev/codex/machina/policies/acl/`.

This file is a synthesised narrative on the two access-control
files in the Codex Machina ACL directory: the **agent ACL** (which
bus topics each role may publish or subscribe) and the **resource
ACL** (which files, folders, APIs, services, and vaults each role
may read, write, execute, upload, or delete). Both files share the
same five-role vocabulary.

## The five roles

The ACL vocabulary has exactly five roles. They are not arbitrary;
they map to a graduated capability model that mirrors the S.E.E.D.
agent hierarchy.

| Role           | Purpose                                                |
|----------------|--------------------------------------------------------|
| `system`       | The cognitive cycle itself. Unrestricted.             |
| `core`         | Graduated agents (scribe, mem, reason, train).         |
| `higher_order` | Brain-cycle agents (ethics, finance, dialogue, conscience). |
| `observer`     | Telemetry and audit consumers. Read-only.              |
| `external`     | Sapling agents and outside clients. Most restricted.   |

A role's permissions are evaluated **per topic** (agent ACL) or
**per resource** (resource ACL). The default-deny rule applies: a
role can act on a topic or resource only if an explicit allow rule
exists.

## 1. Agent ACL (file)

**Source**: `acl/agent_acl.sref`.

The agent ACL is the file the bus broker consults on every
publish and subscribe. It binds the five roles to four
capabilities: **read**, **write**, **execute**, and **network**.
The role-by-role grant is:

- **`system`** — read, write, execute, network. Unrestricted; the
  cognitive cycle itself. Sapling agents are denied this role.
- **`core`** — read, write, execute, network. The default for
  graduated agents (`seedscribe`, `seedmem`, `seedreason`,
  `seedtrain`).
- **`higher_order`** — read, write, execute, *no network*. The
  higher-order agents (`Páreon`, `Solace`, `Argureon`, `Simaetron`)
  may compute and propose but must not open network connections
  themselves; their network access is mediated by `core` agents.
- **`observer`** — read only. Telemetry consumers; may not modify
  state. Cannot execute or open network connections.
- **`external`** — read only, on a sandboxed subset. The default
  for sapling agents and outside clients.

The agent ACL binds every action to a **log entry**. Sensitive
artefacts require **guardian approval**. External agents are
**sandboxed** — they cannot reach topics outside their allow list,
and any attempt to escalate is itself a logged event.

### Bus topic scoping

The agent ACL is the *role-level* layer; the *topic-pattern* layer
is enforced by the bus broker at publish time. A `core` agent that
holds the `system` permission in the role matrix can still only
publish to the topics for which an explicit topic allow-rule
exists. This two-layer model is what makes the bus safe to share
across agents with very different privileges.

### Failure modes

Misassigned roles, guardian-approval bypass, sandbox escape,
observer escalation, and external abuse. Mitigations are
quarterly ACL audits, signature gates, sandbox enforcement, and
council alerts.

→ See also:
`/home/user/seed-dev/codex/machina/policies/acl/agent_acl.sref`.

## 2. Resource ACL (file)

**Source**: `acl/resource_acl.sref`.

The resource ACL is the file the file, vault, and service layers
consult on every read, write, execute, upload, or delete. It binds
the five roles to **namespaces** (`codex`, `identity`, `legal`,
`security`, `logs`, `vecspace`, `backup`, `public`) and to
**sensitivity levels** (`low`, `medium`, `high`, `critical`).

### Resource inventory (initial)

The resource ACL ships with a small inventory of canonical
resources. Each entry has a `resource_id`, a `kind`
(`file`/`folder`/`api`/`service`/`vault`), a `path_glob` or
`endpoint`, a `namespace`, an `owner`, a `sensitivity`, a `pii`
flag, a `retention` period, and the allowed `operations`. The
initial inventory is:

- `res.codex.scrolls` — codex scrolls; medium sensitivity;
  read-only.
- `res.identity.core` — identity artefacts; high sensitivity;
  PII; read/write for guardians.
- `res.legal.docs` — legal documents; high sensitivity; PII;
  read/write for legal stewards.
- `res.security.keys` — security and key artefacts; critical
  sensitivity; read/write for guardians.
- `res.logs.public` — public logs; medium sensitivity; 365-day
  retention; read/upload.
- `res.vecspace.indices` — vector-space indices; medium
  sensitivity; read/write for memory agents.
- `res.vault.public` — public export vault; low sensitivity;
  read/upload.

### Role→Resource permission matrix

The matrix is the default grant per role. The default is least
privilege; specific rules may narrow further.

- **`system`** — all resources; full operations
  (read, write, execute, upload, delete).
- **`core`** — `res.codex.scrolls`, `res.logs.public`,
  `res.vecspace.indices`, `res.vault.public`; read, write, upload
  (no delete or execute).
- **`higher_order`** — `res.codex.scrolls`,
  `res.vecspace.indices`; read, write (no upload, no delete, no
  execute).
- **`observer`** — `res.codex.scrolls`, `res.logs.public`; read
  only.
- **`external`** — `res.vault.public`; read only.

### Conditions and safeguards

Operations on resources of `high` or `critical` sensitivity
require **guardian approval** and **countersignatures**. Reads of
identity or legal resources require **purpose-bound consent**.
Public uploads require **signature and checksum verification**.
Every action is logged with a **correlation ID**.

### Example rules

- **R1** — `core` may read and write vecspace indices; uploads
  blocked.
- **R2** — `higher_order` may edit codex drafts; no uploads.
- **R3** — `observer` read-only on public logs.
- **R4** — `external` read-only on public export.

### Approvals and governance

Guardians approve security and identity operations; legal
stewards approve legal and beneficiary artefacts; the Seed
Council arbitrates disputes. All approvals are signed and
logged; exceptions must reference the exception register.

### Failure modes

Over-broad globs, missing consent on identity/legal reads,
guardian-approval bypass, unsigned public uploads, and drift
between the inventory and the real resources. Mitigations are
pre-merge linting, consent gates, signature gates, and nightly
inventory-sync jobs.

→ See also:
`/home/user/seed-dev/codex/machina/policies/acl/resource_acl.sref`.

## How the two ACLs relate

The agent ACL answers "may this agent publish or subscribe to
this bus topic?"; the resource ACL answers "may this agent read,
write, or upload to this file, folder, API, or vault?". Both
share the same role vocabulary, both default-deny, both log every
action, and both require guardian approval for high-sensitivity
operations. A runtime that claims to be conformant with Codex
Machina must enforce both at the appropriate layer.

## See also

- `INDEX.md` — this codex's index
- `SPEC.md` — the formal spec, especially §2.4 (the 5 ACL roles)
- `POLICIES.md` — the policy framework
- `INTEGRATION-CONTRACT.md` — the loadable runtime contract
- `../solbian/SPEC.md` — the narrative pair
- `../INTEGRATION.md` — how this codex fits into S.E.E.D.
- `/home/user/seed-dev/codex/machina/policies/acl/agent_acl.sref`
- `/home/user/seed-dev/codex/machina/policies/acl/resource_acl.sref`
