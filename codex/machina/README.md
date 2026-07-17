# Codex Machina

> The machine-facing codex. Codex Machina is the formal
> specification of how S.E.E.D. (the mind) and Sprout (the
> body) integrate, written for a runtime to validate against.

## Status

**Draft** — at bootstrap, this codex's content is a
placeholder. The next session will draft the first version
following `docs/METHODOLOGY.md`'s spec-first workflow.

## Files

| File            | Purpose                                |
|-----------------|----------------------------------------|
| `README.md`     | This file                              |
| `SPEC.md`       | The formal specification               |
| `CHANGELOG.md`  | Codex Machina's release notes          |

## What this codex is

Codex Machina is the *formal* side of the integration spec.
It contains:

- **Schemas** for the bus payloads, the cognitive events,
  and the motor intents.
- **Runtime requirements** for any component that claims to
  satisfy the integration (S.E.E.D., Sprout, sapling agents,
  external clients).
- **Validation rules** for confirming that a runtime
  implementation conforms to the spec.
- **Versioning rules** for the schema and the runtime
  contract.

It is paired with **Codex Solbian** (in the sibling
`solbian/` directory), which is the *narrative* side of the
spec.

Both codexes are required. They must agree.

## What this codex is not

- It is not the implementation. The code lives in seed-dev
  and robot-dev.
- It is not a tutorial. It is a specification. It describes
  what is required, not how to use it.
- It is not human-readable in the same way Codex Solbian is.
  It is meant to be consumed by tools and validated
  automatically.

## How to consume this codex

1. Read `SPEC.md` for the formal contract.
2. Validate your runtime against the schemas and rules.
3. If the validation passes, your runtime is conformant with
   the spec version.
4. To make a change to the spec, follow
   `docs/METHODOLOGY.md`'s spec-first workflow and update the
   matching `../solbian/SPEC.md` for consistency.

## See also

- `SPEC.md` — the formal spec
- `CHANGELOG.md` — release notes
- `../README.md` — the codex parent directory
- `../INTEGRATION.md` — how the two codexes fit together
- `../solbian/README.md` — Codex Solbian (the narrative pair)
