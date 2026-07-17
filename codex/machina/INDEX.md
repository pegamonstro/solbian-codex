# INDEX — Codex Machina

> **Status**: Draft synthesis, version 0.1.0.
> **Last updated**: 2026-07-16.
> **Source-of-truth pairing**: `../solbian/INDEX.md` (Codex Solbian, the narrative pair).

This is the synthesised narrative index for Codex Machina. It is a curated
entry point for a reader who wants to understand what the codex contains
and how its parts fit together. It is paired with **Codex Solbian** (the
narrative specification, in the sibling `solbian/` directory); both must
agree on every claim.

The canonical source for the underlying artefacts lives in
`/home/user/seed-dev/codex/`. Per `/home/user/solbian/CLAUDE.md` rule 4,
the solbian copy is canonical *for solbian*; the seed-dev copy is the
upstream source-of-truth snapshot of the running code. When they
disagree, the seed-dev version reflects the current code; the solbian
version is the curated narrative. Divergences are recorded in
`docs/adr/` rather than silently overwritten.

## What Codex Machina is

Codex Machina is the machine-facing codex: a formal specification of the
policies, schemas, role-based access controls, and confidence rules that
govern the S.E.E.D. ↔ Sprout integration. Where Codex Solbian is
constitutional and prose, Codex Machina is contractual and structured. It
is the artefact a runtime validates against at boot and at each epoch
boundary. The current population of this codex covers four areas:

- **Policies** — the root SeedPolicy, the exception register, and the
  IP licence grant. These define *what* the system must do and *what*
  is forbidden.
- **ACL** — the agent and resource access-control lists. These
  define *who* may publish or read on which bus topic or namespace.
- **Schemas** — the sref-v2 JSON Schema, the SXL metadata, and the
  SXL schema stubs. These define the *shape* of every artefact that
  flows on the bus.
- **Confidence rules** — the canonical thresholds the Solace
  governance regime uses to auto-commit, review, or reject records.

A formal **Integration Contract** synthesises all four into a single
document a runtime can load and enforce.

## Files in this codex

| File                     | Purpose                                                |
|--------------------------|--------------------------------------------------------|
| `README.md`              | The codex's home and orientation                       |
| `SPEC.md`                | The formal specification (v0.1.0)                      |
| `INDEX.md`               | This file — a synthesised index                        |
| `POLICIES.md`            | Narrative on `policies/*.sref`                         |
| `ACL.md`                 | Narrative on `policies/acl/*.sref`                     |
| `SCHEMAS.md`             | Narrative on `schemas/*.{sref,json}`                   |
| `CONFIDENCE-RULES.md`    | Narrative on `meta/confidence_rules.sref`              |
| `INTEGRATION-CONTRACT.md`| The loadable contract a runtime validates against      |
| `CHANGELOG.md`           | Release notes                                          |

## Areas of the canonical source

### Policies

The `policies/` directory in `~/seed-dev/codex/machina/policies/` holds
the root policy framework, the exception register, and the IP licence
grant. These are the high-level governance documents that the rest of
the codex refers to. Each is an `.sref` v2 artefact (newline-delimited
JSON of structured entries). Three are populated; two are placeholders
(awaiting content from the Codex Solbian→Machina bridge).

→ See also: `POLICIES.md` in this codex, and
`/home/user/seed-dev/codex/machina/policies/`.

### ACL (agent + resource)

The `policies/acl/` directory holds the two ACL files: the
**agent ACL** (which bus topics each role may publish or subscribe)
and the **resource ACL** (which files, folders, APIs, services, and
vaults each role may read, write, execute, upload, or delete). The
agent ACL is what the bus broker consults; the resource ACL is what
the file and vault layers consult. Both share the same five-role
vocabulary: `system`, `core`, `higher_order`, `observer`, `external`.

→ See also: `ACL.md` in this codex, and
`/home/user/seed-dev/codex/machina/policies/acl/`.

### Schemas

The `schemas/` directory holds the sref-v2 JSON Schema (the contract
every `.sref` artefact must validate against), the SXL metadata
schema stub, the SXL schema stub, and a small set of NDJSON examples.
The populated JSON Schema is the load-bearing file. The two `.sref`
metadata and schema stubs are empty placeholders, awaiting
content from the SXL specification.

→ See also: `SCHEMAS.md` in this codex, and
`/home/user/seed-dev/codex/machina/schemas/`.

### Meta — confidence rules

The `meta/` directory in `~/seed-dev/codex/meta/` holds the canonical
confidence thresholds the Solace governance pipeline uses to decide
whether a record auto-commits, requires human review, or is rejected.
This is a single small `.sref` file with three threshold values
and the rationale for each.

→ See also: `CONFIDENCE-RULES.md` in this codex, and
`/home/user/seed-dev/codex/meta/confidence_rules.sref`.

## The integration contract

The `INTEGRATION-CONTRACT.md` file in this codex is a synthesised
contract that a runtime can load and enforce. It is the operational
manifest of all four areas above, expressed as the runtime sees them:
a 5-role ACL, a 3-tier bus, an SXL envelope shape, a `seedreasond`
invocation contract, a policy-bundle activation protocol, and the
Solace governance thresholds. It is the single most useful file for
a runtime implementer; the rest of the codex is reference material.

→ See also: `INTEGRATION-CONTRACT.md` in this codex, and the
parent `../INTEGRATION.md` for how this codex fits into S.E.E.D.

## See also

- `README.md` — Codex Machina's home
- `SPEC.md` — the formal spec
- `POLICIES.md` — narrative on policies
- `ACL.md` — narrative on ACLs
- `SCHEMAS.md` — narrative on schemas
- `CONFIDENCE-RULES.md` — narrative on confidence rules
- `INTEGRATION-CONTRACT.md` — the loadable runtime contract
- `CHANGELOG.md` — release notes
- `../solbian/SPEC.md` — the narrative pair
- `../solbian/INDEX.md` — the narrative index
- `../INTEGRATION.md` — how the two codexes fit into S.E.E.D.
- `../../docs/METHODOLOGY.md` — spec-first workflow
