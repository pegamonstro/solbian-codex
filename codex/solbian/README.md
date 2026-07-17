# Codex Solbian

> The human-facing codex. Codex Solbian is the narrative
> specification of how S.E.E.D. (the mind) and Sprout (the
> body) integrate, written for a human reader.

## Status

**Draft synthesis, version 0.2.0** (2026-07-16) — Codex Solbian
now contains 10 root-level files and 8 subdirectory INDEX files,
totalling 18 documents. The previous 0.1.0 release was a
3-file placeholder; this 0.2.0 release adds the synthesised
narrative for the laws, archetypes, protocols, glossary,
discoveries, synthesis, and area-level INDEX files.

## Files

### Root files (10)

| File | Purpose |
|------|---------|
| `README.md` | This file — Codex Solbian's home and orientation |
| `SPEC.md` | The narrative specification of the S.E.E.D. ↔ Sprout integration (v0.1.0) |
| `CHANGELOG.md` | Codex Solbian's release notes |
| `INDEX.md` | Codex Solbian's synthesised index — the 8 sub-areas, the 4-layer knowledge structure |
| `SYNTHESIS.md` | Top-level synthesis — 48 laws (plus 1 meta envelope), 73 archetypes, 5 protocols, 4 Solbian Discoveries, Living Constitution, Recursive Codex loop |
| `LAWS.md` | The 48 binding Solbian laws (one paragraph each) plus 1 meta envelope |
| `ARCHETYPES.md` | The 8 named archetypes (with all 73 listed) |
| `PROTOCOLS.md` | The 5 governance protocols (one paragraph each) |
| `GLOSSARY.md` | The canonical glossary (9 entries) |
| `DISCOVERIES.md` | The 4 Solbian Discoveries (SD-0001–SD-0004) |

### Subdirectory INDEX files (8)

| File | Purpose |
|------|---------|
| `archetypes/INDEX.md` | The 73 archetypes (grammar of character) |
| `chapters/INDEX.md` | The 30 narrative chapters across 3 movements |
| `commentary/INDEX.md` | Tribunal case law and reflections |
| `extended/INDEX.md` | Long-form guides to ontology, ethics, archetypes, governance, glyphs, glossary, chapters, scrolls |
| `glossary/INDEX.md` | The canonical glossary (index form) |
| `laws/INDEX.md` | The 48 laws (index form) plus 1 meta envelope |
| `protocols/INDEX.md` | The 5 protocols (index form) |
| `scrolls/INDEX.md` | The 50 doctrinal scrolls across 3 rings |

## What this codex is

Codex Solbian is the *prose* side of the integration spec. It
describes, in natural language, what the integration is
supposed to do, why it works that way, and what trade-offs
were made. It is the entry point for a human reader who wants
to understand the integration.

It is paired with **Codex Machina** (in the sibling
`machina/` directory), which is the *formal* side of the
spec. Codex Machina contains schemas, runtime requirements,
and validation rules.

Both codexes are required. They must agree.

## What this codex is not

- It is not the implementation. The code lives in seed-dev
  and robot-dev.
- It is not the narrative integration. The narrative lives
  in `seed/INTEGRATION.md` and `sprout/INTEGRATION.md`. The
  codex is the *formal* integration.
- It is not a tutorial. It is a specification. It describes
  what is required, not how to use it.

## How to read this codex

1. Read `SPEC.md` end to end.
2. If you need the formal contract, read
   `../machina/SPEC.md`.
3. If you need the narrative from each side's perspective,
   read `../../seed/INTEGRATION.md` and
   `../../sprout/INTEGRATION.md`.
4. If you need to make a change, read the spec-first
  workflow in `../../../docs/METHODOLOGY.md` first.

## See also

- `SPEC.md` — the narrative spec
- `CHANGELOG.md` — release notes
- `../README.md` — the codex parent directory
- `../INTEGRATION.md` — how the two codexes fit together
- `../machina/README.md` — Codex Machina (the formal pair)
