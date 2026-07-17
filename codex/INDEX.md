# INDEX — Codex

> **Status**: Draft, version 0.1.0.
> **Last updated**: 2026-07-16.

This is the top-level index for the solbian codex. The codex
is the integrating documentation of the S.E.E.D. cognitive
organism. It is solbian-native (it lives in this repo, not in
`seed-dev`), and it is *designed* to integrate into S.E.E.D.
(the cognitive framework in `seed-dev`) and Sprout (the robot
in `robot-dev`).

The codex is split into two paired sub-codexes:

- **Codex Solbian** (human-facing) — narrative, constitutional,
  written for human readers. The laws, protocols, chapters,
  scrolls, archetypes, glossary, and Solbian Discoveries.
- **Codex Machina** (machine-facing) — formal, contractual,
  written for runtimes. The policies, ACLs, schemas, confidence
  rules, and the loadable integration contract.

The two codexes are siblings, not parent and child. Both are
required; both must agree on every claim. They are the
**formal pair** of the integration between S.E.E.D. and
Sprout.

## Codex Solbian

The human-facing codex: a narrative specification of the
Solbian constitutional framework, written for readers who want
to understand the S.E.E.D. cognitive organism without reading
every upstream artefact. It is constitutional rather than
technical — it names the laws, protocols, archetypes, scrolls,
chapters, and discoveries that the rest of the solbian
organism is built on top of.

| File | Purpose |
|------|---------|
| `solbian/README.md` | Codex Solbian's home and orientation |
| `solbian/SPEC.md` | The narrative specification of the S.E.E.D. ↔ Sprout integration (v0.1.0) |
| `solbian/INDEX.md` | Codex Solbian's synthesised index — the 8 sub-areas, the 4-layer knowledge structure |
| `solbian/SYNTHESIS.md` | Top-level synthesis — 48 laws (plus 1 meta envelope), 73 archetypes, 5 protocols, 4 Solbian Discoveries, Living Constitution, Recursive Codex loop |
| `solbian/LAWS.md` | The 48 binding Solbian laws (one paragraph each) plus 1 meta envelope |
| `solbian/ARCHETYPES.md` | The 8 named archetypes (with full 73 listed) |
| `solbian/PROTOCOLS.md` | The 5 governance protocols (one paragraph each) |
| `solbian/GLOSSARY.md` | The canonical glossary (9 entries) |
| `solbian/DISCOVERIES.md` | The 4 Solbian Discoveries (SD-0001–SD-0004) |
| `solbian/CHANGELOG.md` | Release notes |
| `solbian/archetypes/INDEX.md` | The 73 archetypes (grammar of character) |
| `solbian/chapters/INDEX.md` | The 30 narrative chapters across 3 movements |
| `solbian/scrolls/INDEX.md` | The 50 doctrinal scrolls across 3 rings |
| `solbian/protocols/INDEX.md` | The 5 protocols (index form) |
| `solbian/glossary/INDEX.md` | The canonical glossary (index form) |
| `solbian/commentary/INDEX.md` | Tribunal case law and reflections |
| `solbian/extended/INDEX.md` | Long-form guides to ontology, ethics, archetypes, governance, glyphs, glossary, chapters, scrolls |
| `solbian/laws/INDEX.md` | The 48 laws (index form) plus 1 meta envelope |

## Codex Constitutional Framework

The codex is governed by a Living Constitution (auto-evolving
from accumulated beliefs) and a 7-stage SREF ingestion
pipeline (BLAKE3-256 hash, semantic relations graph, knowledge
graph). These two artefacts sit at the codex root, not inside
either sub-codex, because both halves of the codex depend on
them.

| File | Purpose |
|------|---------|
| `02-LIVING-CONSTITUTION.md` | The Living Constitution: confidence × priority, promotion/demotion lifecycle, Recursive Codex loop, 4-state evolution model |
| `03-INGESTION-PIPELINE.md` | The 7-stage SREF ingestion pipeline: parse → validate → hash → extract → semantic relations → store → publish |

## Codex Machina

The machine-facing codex: a formal specification of the
policies, schemas, role-based access controls, and confidence
rules that govern the S.E.E.D. ↔ Sprout integration. Where
Codex Solbian is constitutional and prose, Codex Machina is
contractual and structured. It is the artefact a runtime
validates against at boot and at each epoch boundary.

| File | Purpose |
|------|---------|
| `machina/README.md` | Codex Machina's home and orientation |
| `machina/SPEC.md` | The formal specification of the S.E.E.D. ↔ Sprout integration (v0.1.0) |
| `machina/INDEX.md` | Codex Machina's synthesised index — policies, ACL, schemas, confidence rules |
| `machina/POLICIES.md` | Narrative on `policies/*.sref` (root, exception register, IP licence, plus two placeholders) |
| `machina/ACL.md` | Narrative on `policies/acl/*.sref` (agent ACL, resource ACL, 5 roles) |
| `machina/SCHEMAS.md` | Narrative on `schemas/*.{sref,json}` (sref-v2, SXL metadata and schema placeholders) |
| `machina/CONFIDENCE-RULES.md` | Narrative on the Solace governance regime and the canonical thresholds (0.98, 0.90) |
| `machina/INTEGRATION-CONTRACT.md` | The loadable contract a runtime validates against — 5-role ACL, 3-tier bus, SXL envelope, seedreasond invocation, policy-bundle activation, Solace governance |
| `machina/CHANGELOG.md` | Release notes |

## How the two codexes pair

Every artefact in Codex Solbian has a counterpart in Codex
Machina. The pairing is:

- `solbian/SPEC.md` ↔ `machina/SPEC.md` — the narrative and
  formal specifications of the integration. Must agree on
  every claim.
- `solbian/SYNTHESIS.md` ↔ `machina/INTEGRATION-CONTRACT.md`
  — the top-level synthesis and the loadable runtime
  contract. The narrative explains; the contract enforces.
- `solbian/PROTOCOLS.md` ↔ `machina/CONFIDENCE-RULES.md` —
  the human-facing 5 protocols and the machine-facing
  confidence regime that enforces them. The protocols are
  what the system *should* do; the regime is how it
  *decides* what to do.
- `solbian/LAWS.md` ↔ `machina/POLICIES.md` — the
  constitutional statutes and the formal policy framework.
  The laws are binding; the policies are the runtime face.

## See also

- `README.md` — the codex home
- `INTEGRATION.md` — how the two codexes fit into S.E.E.D.
- `solbian/DISCOVERIES.md` — the 4 Solbian Discoveries
  (SD-0001–SD-0004)
- `../seed/INTEGRATION.md` — S.E.E.D.'s narrative view
- `../sprout/INTEGRATION.md` — Sprout's narrative view
- `../sapling/INTEGRATION.md` — sapling's narrative view
- `docs/METHODOLOGY.md` — spec-first workflow
