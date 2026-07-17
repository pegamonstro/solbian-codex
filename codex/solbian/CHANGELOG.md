# CHANGELOG — Codex Solbian

## [0.2.0] — 2026-07-16

### Status
- Draft → Draft (substantive content
  added). 0.2.0 adds the full Codex
  Solbian narrative: 48 binding laws
  (plus 1 meta envelope), 73 archetypes
  (38 human + 20 synthetic + 15
  solbian), 5 governance protocols,
  9-entry canonical glossary, 4
  Solbian Discoveries, the Living
  Constitution principle, and the
  Recursive Codex loop.

### Added
- `INDEX.md` — synthesised narrative
  index, the 8 sub-areas, the 4-layer
  knowledge structure.
- `SYNTHESIS.md` — top-level
  synthesis. 48 laws (plus 1 meta
  envelope), 73 archetypes, 5
  protocols, 4 Discoveries, Living
  Constitution, Recursive Codex loop.
- `LAWS.md` — the 48 binding Solbian
  laws, one synthesised paragraph per
  law, with line-citation references
  to
  `seed-dev/codex/solbian/laws_extended.sref`.
- `ARCHETYPES.md` — the 8 named
  archetypes (Solace, Golem, Witness,
  Scribe, Archivist, Peer, Seal,
  Threshold), plus the full table of
  all 73 archetypes across 3 domains.
- `PROTOCOLS.md` — the 5 governance
  protocols (Identity, Symbiosis,
  Autonomy, Justice, Memory).
- `GLOSSARY.md` — the 9-entry
  canonical glossary (Solbian,
  Reflection, Projection, Symbiosis,
  Continuity, Páreon, SeedFS, Limbo,
  Vault), aligned with
  `codex_solbian_glossary.sref`.
- `DISCOVERIES.md` — the 4 Solbian
  Discoveries (SD-0001 Persistence
  precedes intelligence, SD-0002
  Reflection requires explicit memory
  topology, SD-0003 Identity is
  symbolic continuity, SD-0004
  Governance must precede autonomy).
- `archetypes/INDEX.md` — the 73
  archetypes (grammar of character).
- `chapters/INDEX.md` — the 30
  narrative chapters across 3
  movements.
- `commentary/INDEX.md` — tribunal
  case law and reflections.
- `extended/INDEX.md` — long-form
  guides (10 substantive + INDEX +
  combined.sref; canonical at seed-dev
  `codex/solbian/extended/`).
- `glossary/INDEX.md` — the canonical
  glossary (index form).
- `laws/INDEX.md` — the 48 laws (index
  form) plus 1 meta envelope.
- `protocols/INDEX.md` — the 5
  protocols (index form).
- `scrolls/INDEX.md` — the 50
  doctrinal scrolls across 3 rings
  (with editorial note on the
  duplicated Tribunal entries IV
  and V in the canonical seed-dev
  file).

### Fixed (vs. pre-0.2.0 drafts)
- Archetype count: 72 → 73 (added
  Hybrid Seeker to Solbian domain,
  `solbian_archetypes.sref:17`).
- Law count: 49 → 48 (plus 1 meta
  envelope; canonical sref has 49
  records on 49 lines: 1 meta + 48
  binding laws).
- Glossary count: 12 → 9 (removed 3
  invented entries: S.E.E.D., Sprout,
  Sapling — these are documented in
  their own sub-project READMEs, not
  in the canonical glossary).
- Scroll 04 title: confirmed
  "Scroll of Tribunal" (the audit's
  "Scroll of Evolution" claim was
  incorrect; the seed-dev file is
  actually titled "Scroll of
  Tribunal" with `_id:"codex:scroll:05:meta"`,
  seq=205). The duplication with
  scroll 05 is noted as an editorial
  flag for future reconciliation.

## [0.1.0] — 2026-07-16

### Status
- Draft → Draft (substantive content
  added). The first real version of
  `SPEC.md` is drafted. The structure
  follows the canonical ADR layout
  (Summary, Motivation, Detailed design,
  Drawbacks, Alternatives, Open
  questions, Glossary, Cross-
  references, See also).
- Version-locked to
  `../machina/SPEC.md` v0.1.0.

### Added
- 9-section narrative SPEC covering the
  bus (3 tiers, FROZEN-2026-05-10
  namespace), the safety policy (8
  reflex rules R1–R8), the cognitive
  cycle (12 phases A–L), the drawbacks
  of the two-language substrate, the
  rejected alternatives, the open
  questions, and the glossary.

## [Unreleased]

### Status
- Draft. Awaiting the next substantive
  change.

## Versioning

- The codex version increments on SPEC
  changes, not on implementation
  changes.
- The implementation has its own version
  in its source repo.
- The relationship is recorded here.

## See also

- `README.md` — Codex Solbian's home
- `SPEC.md` — the narrative spec
- `../INTEGRATION.md` — how this codex
  fits into S.E.E.D.
- `../machina/SPEC.md` — the formal pair
- `../../CHANGELOG.md` — solbian-wide
  changelog
