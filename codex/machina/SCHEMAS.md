# SCHEMAS — Codex Machina

> **Status**: Draft synthesis, version 0.1.0.
> **Last updated**: 2026-07-16.
> **Canonical source**: `/home/user/seed-dev/codex/machina/schemas/`.

This file is a synthesised narrative on the schema files in the
Codex Machina schemas directory. The canonical source is in
`/home/user/seed-dev/codex/machina/schemas/`; per
`/home/user/solbian/CLAUDE.md` rule 4, the solbian copy is the
curated narrative, the seed-dev copy is the source-of-truth
snapshot of the running code.

One schema is fully populated (the sref-v2 JSON Schema); two are
zero-byte placeholders awaiting content from the SXL
specification. The narrative below covers the populated schema in
detail and notes the placeholders.

## 1. SREF v2 JSON schema

**Source**: `sref_v2_schema.json`.

The sref-v2 JSON Schema is the contract every `.sref` artefact in
the Codex Solbian and S.E.E.D. system must validate against. It is
a JSON Schema 2020-12 document. The two top-level required fields
are `kind` and `version`. The `kind` field is an enum over seven
artefact types: `seed.module`, `seed.file`, `seed.test`,
`seed.build`, `seed.index`, `seed.policy`, `seed.migration`. The
`version` field is a string constant set to `sref_v2`. The schema
uses these two fields to dispatch the rest of the validation.

The body of an sref-v2 artefact is a set of optional sections, each
guarded by a sub-schema. The sections and their required fields
are:

- **`module`** — `{ name, lang, purpose }`. `lang` is enum
  `["C99"]`. Required: all three.
- **`artifacts`** — `{ headers, sources, bins, libs }` (all
  arrays of strings).
- **`interfaces`** — `{ api[], abi_stable? }`. Each `api` entry has
  a `header` and a list of `functions`; each function has a `sig`
  and an `errcodes` list. Required: `header`, `functions`.
- **`contracts`** — `{ pre[], post[] }`.
- **`build`** — `{ cc, c_std, cflags[], ldflags[], targets[] }`.
- **`deps`** — `{ internal[], system[] }`.
- **`tests`** — `{ unit[], coverage_min? }`. `coverage_min` is a
  number in `[0, 1]`.
- **`policy`** — `{ syscalls_allow_ref?, deny_net? }`.
- **`perf`** — `{ ingest_mib_s_min?, emit_ops_s_min?, fixture? }`.
- **`io`** — `{ reads[], writes[], schemas[] }`.
- **`telemetry`** — `{ logs: "ndjson", metrics[] }`. `logs` is
  enum `["ndjson"]`.
- **`security`** — `{ threats[], mitigations[] }`.
- **`migration`** — `{ from, to, steps[] }`.
- **`tasks`** — array of strings.
- **`acceptance`** — array of strings.
- **`determinism`** — `{ repro_build?, dirwalk_order? }`.
- **`make`** — `{ targets{}, vars{} }`. Both are
  `additionalProperties: string`.
- Top-level scalars: `path`, `suite`, `files`, `link_libs`,
  `fixtures`, `assert`, `exports`, `include_guard`, `includes`,
  `items[]`.

Validation rules the schema enforces:

- A missing `kind` or `version` fails the document outright.
- A `kind` not in the seven-element enum fails outright.
- A `version` other than the literal string `sref_v2` fails
  outright.
- The `module` section is validated only if present; all three of
  its required fields must appear together.
- The `interfaces.api.functions[].errcodes` field must be an
  array; the validator does not enforce that the codes are
  known, only that they are well-formed strings.

The schema is the load-bearing file of the schemas directory. A
runtime that ingests an `.sref` artefact calls a JSON Schema
validator against this file *before* any other processing. An
artefact that fails validation is rejected at the boundary.

→ See also:
`/home/user/seed-dev/codex/machina/schemas/sref_v2_schema.json`.

## 2. SXL metadata (placeholder)

**Source**: `from_system__codex_solbian_metadata.sref`.

This file is a zero-byte placeholder. The intended content is the
SXL metadata schema — the structure of the SXL envelope's
metadata fields (`:id`, `:timestamp`, `:creator`, `:confidence`,
`:schema`, `:provenance`, `:relations`, `:status`) as a formal
`.sref` artefact. Until the file is populated, the integration
contract treats SXL metadata as defined by `SPEC.md` §2.3 and
validated by `~/seed-dev/src/libsexpr/src/validate.c`.

→ See also:
`/home/user/seed-dev/codex/machina/schemas/from_system__codex_solbian_metadata.sref`.

## 3. SXL schema (placeholder)

**Source**: `from_system__codex_solbian_schema.sref`.

This file is a zero-byte placeholder. The intended content is the
formal SXL schema — the canonical hierarchy of SXL entity types
(observation, intent, policy-check, and any others) as a formal
`.sref` artefact. Until the file is populated, the integration
contract treats the SXL entity hierarchy as defined by
`SPEC.md` §3–§5 and validated by
`~/seed-dev/src/libsexpr/src/validate.c`.

→ See also:
`/home/user/seed-dev/codex/machina/schemas/from_system__codex_solbian_schema.sref`.

## 4. Examples

**Source**: `examples/*.ndjson`.

The schemas directory contains four example files using the
canonical `.ndjson` filename convention: `seed.build.ndjson`,
`seed.file.ndjson`, `seed.module.ndjson`, and
`seed.test.ndjson`. The NDJSON format allows one JSON object
per line and is the canonical naming convention across the
schemas directory; the current examples each contain a single
JSON object on the first (and only) line. Each file is a
small artefact of the named `kind` that round-trips through
the sref-v2 validator. A runtime maintainer who needs to add
a new artefact type should copy the closest existing example,
change `kind` and the relevant section, and run it through
the validator. Additional records may be appended one per
line to any of these files; the canonical parser treats each
line as a separate artefact.

→ See also:
`/home/user/seed-dev/codex/machina/schemas/examples/`.

## How the schemas relate

The sref-v2 JSON Schema validates the `.sref` policy, build, and
module artefacts. The SXL metadata and SXL schema placeholders,
once populated, will validate the bus-payload envelopes described
in `SPEC.md` §2.3 and §3–§5. A conformant runtime loads all three
schemas and validates every artefact it ingests against the one
whose `kind` or `:schema` it declares.

## See also

- `INDEX.md` — this codex's index
- `SPEC.md` — the formal spec, especially §2.3 (SXL envelope)
  and §3–§5 (per-kind schemas)
- `POLICIES.md` — the policy framework
- `INTEGRATION-CONTRACT.md` — the loadable runtime contract
- `../solbian/SPEC.md` — the narrative pair
- `../INTEGRATION.md` — how this codex fits into S.E.E.D.
- `/home/user/seed-dev/codex/machina/schemas/sref_v2_schema.json`
- `/home/user/seed-dev/codex/machina/schemas/from_system__codex_solbian_metadata.sref` (placeholder)
- `/home/user/seed-dev/codex/machina/schemas/from_system__codex_solbian_schema.sref` (placeholder)
- `/home/user/seed-dev/codex/machina/schemas/examples/`
