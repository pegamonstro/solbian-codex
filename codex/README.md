# codex

> The integrating codexes of the organism. Two evolving
> sub-projects — Codex Solbian and Codex Machina — that ship
> on their own but are designed to integrate into S.E.E.D.

## The two codexes

| Sub-project    | Path                  | Audience                                |
|----------------|-----------------------|-----------------------------------------|
| Codex Solbian  | `solbian/`            | Humans reading the integration design   |
| Codex Machina  | `machina/`            | Runtimes consuming the integration contract |

They are siblings, not parent and child. Both are required for
a complete integration; neither alone is sufficient.

## Files in this directory

| File                       | Purpose                                          |
|----------------------------|--------------------------------------------------|
| `README.md`                | This file                                        |
| `INDEX.md`                 | Top-level codex index                            |
| `INTEGRATION.md`           | How the two codexes integrate into S.E.E.D.      |
| `solbian/README.md`        | Codex Solbian's home                             |
| `solbian/SPEC.md`          | Codex Solbian's formal specification             |
| `solbian/CHANGELOG.md`     | Codex Solbian's release notes                    |
| `machina/README.md`        | Codex Machina's home                             |
| `machina/SPEC.md`          | Codex Machina's formal specification             |
| `machina/CHANGELOG.md`     | Codex Machina's release notes                    |

The `solbian/` and `machina/` sub-directories are the
pre-existing scaffold directories that came with the repo;
they are reused verbatim.

## Solbian Discoveries (SD-XXXX)

The codex recognises a small set of **Solbian Discoveries
(SD)** — formal claims about cognitive architecture drawn
from the development history of S.E.E.D. Each discovery
is numbered `SD-XXXX` (zero-padded 4 digits) to leave
room for many more. The currently-formalised discoveries
are **SD-0001** (persistence precedes intelligence),
**SD-0002** (reflection requires explicit memory
topology), **SD-0003** (identity is symbolic continuity,
not execution continuity), and **SD-0004** (governance
must precede autonomy). The full text, evidence, and
implications of each is in
[`solbian/DISCOVERIES.md`](./solbian/DISCOVERIES.md). The
canonical source is
`/home/user/seed-dev/docs/DRAFTS/seed-cog3-specs.txt`
lines 1386–1417.

## Why two codexes?

A single codex would conflate the human-facing design
artefact (the spec) with the machine-facing integration
contract (the hooks and schemas). Splitting them gives each
audience a clean entry point.

When you read a codex, you should know immediately:

- If you are **a human** trying to understand what the
  integration is supposed to do, read `solbian/SPEC.md`.
- If you are **a runtime** trying to know what the
  integration is required to satisfy, read `machina/SPEC.md`.

Both specs must agree. When they diverge, that is a bug.

## Lifecycle of a codex release

1. **Draft**: the SPEC is drafted in the codex's directory,
   following `docs/METHODOLOGY.md`.
2. **Review**: the spec is reviewed per `docs/METHODOLOGY.md`'s
   validation step.
3. **Approve**: the spec is marked Approved. The codex now has
   a stable target.
4. **Develop**: the implementation lives in the appropriate
   source repo (`seed-dev` or `robot-dev`). The codex's
   `CHANGELOG.md` tracks the spec, not the code.
5. **Integrate**: when the code is ready, the codex
   `INTEGRATION.md` is updated to describe how S.E.E.D. and
   Sprout consume the codex.
6. **Release**: a codex release is a solbian release that
   tags a new SPEC version. The actual code release happens
   upstream.

## See also

- `INTEGRATION.md` — how the two codexes fit into S.E.E.D.
- `solbian/README.md` — Codex Solbian's home
- `machina/README.md` — Codex Machina's home
- `../seed/README.md` — the mind sub-project
- `../sprout/README.md` — the body sub-project
- `../sapling/README.md` — the agents sub-project
- `docs/projects/codex.md` — solbian's index of this sub-project
