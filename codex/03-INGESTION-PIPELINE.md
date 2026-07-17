# 03 — The SREF Ingestion Pipeline

> **Status**: Draft synthesis, version 0.1.0.
> **Last updated**: 2026-07-16.
> **Purpose**: A single document on the JSON / SREF-to-SXL ingestion
> pipeline, the semantic relations graph that the pipeline produces,
> and the knowledge-graph abstraction that the cognitive engine
> reasons over.

This document sits between `codex/02-LIVING-CONSTITUTION.md` (the
constitutional substrate) and `codex/machina/SCHEMAS.md` (the
machine-facing schema catalogue). Its job is to describe how a
canonical SREF file becomes a typed SXL entity in the cognitive
memory, how the SREFs collectively produce a semantic relations
graph, and how the cognitive engine turns that graph into a
queryable knowledge graph. The runtime implementation lives in
`/home/user/seed-dev/lua/helpers/codex_ingest.lua:1`; the v2
schema is at
`/home/user/seed-dev/codex/machina/schemas/sref_v2_schema.json:1`.

The pipeline is the bridge between the **canonical documents**
(the codex) and the **runtime memory** (the SXL world model). A
SREF is what the codex writes; an SXL entity is what the
cognitive engine reasons over; the pipeline is the
transformation between them.

## 1. The principle

A SREF file is **canon**: a frozen normative document whose
contents are governed by the codex. An SXL entity is **memory**:
a typed, partition-scoped record that the cognitive engine can
query, transform, and propagate confidence over. The ingestion
pipeline is the **canonical-to-runtime** translation: it takes a
SREF, validates it, parses it into a canonical S-expression,
assigns it a BLAKE3-256 identity hash, extracts its structure,
builds the semantic relations it implies, and stores the result
in the appropriate `libsmem` partition.

The principle has four operational implications:

- **The pipeline is the only path.** A SREF becomes a runtime
  entity by going through the pipeline. There is no side
  channel; there is no manual insertion. The audit trail depends
  on the pipeline being the single point of entry.
- **The pipeline is idempotent.** A SREF with a given BLAKE3-256
  hash produces the same SXL entity on every run. The pipeline
  can be re-executed safely; near-duplicates are linked, not
  re-stored (per
  `/home/user/seed-dev/docs/memory/MEMORY_SYSTEM_ARCHITECTURE.md:209`).
- **The pipeline is observable.** Every SREF ingestion emits a
  bus event. Downstream consumers can subscribe to the topic and
  react to new arrivals.
- **The pipeline is governed.** Every SREF is validated against
  the v2 schema before it is parsed. A SREF that fails validation
  is rejected at the parser boundary; the rejection is logged
  and the requester is informed.

The pipeline is also the operational expression of the
Recursive Codex loop (per `codex/02-LIVING-CONSTITUTION.md:237`).
Phase 1 (Perception, SD-0001) is the read step; Phase 2 (Ontology,
SD-0002) is the structure step; Phase 3 (Identity, SD-0003) is
the identity-hash step; Phase 4 (Governance, SD-0004) is the
validation step. The pipeline is the Recursive Codex loop
operationalised.

## 2. The SREF input

A SREF file is a text document in the `.sref` canonical dialect
(per
`/home/user/seed-dev/schemas/.sref/v1/_grammar.ebnf:1`). A SREF
file consists of an optional file header (`%SREF 1`), a sequence
of records, each separated by `LF --- LF`, and each record
consisting of a header block, a separator, and a body. The
header block carries the metadata (`@schema`, `@id`, `@actor`,
`@time`, `@parent`); the body carries the typed fields
(`:fields`).

The v2 schema for the SREF is at
`/home/user/seed-dev/codex/machina/schemas/sref_v2_schema.json:1`.
The v2 schema is required for any SREF that flows through the
codex ingestion pipeline; v1 SREFs are migrated to v2 by the
`migration` field of the v2 schema. The schema declares the
closed set of `kind` values:
`seed.module`, `seed.file`, `seed.test`, `seed.build`,
`seed.index`, `seed.policy`, `seed.migration`. A SREF whose
`kind` is not in the closed set is rejected at the schema
boundary; the rejection is logged with the offending `kind` and
the file path.

The SREF envelope is at
`/home/user/seed-dev/schemas/.sref/v1/envelope.sref:1`. The
envelope carries the bus-level metadata: `topic`, `ts_mono`,
`ts_wall`, `qos`, `prio`, `schema_fp`, and `payload`. The
`schema_fp` is the lowercase 64-character hex BLAKE2b-256 of
the canonical text of the payload's schema (per
`/home/user/seed-dev/schemas/.sref/v1/envelope.sref:38`). The
envelope is the on-the-wire shape; the SREF body is the
in-memory shape; the pipeline ingests the body and produces an
SXL entity that carries the envelope's `schema_fp` as its
`:schema` field.

A SREF file is a JSON-line document. The Lua ingest path at
`/home/user/seed-dev/lua/helpers/codex_ingest.lua:88` reads one
JSON object per line, parses it with `cjson`, and feeds the
parsed entry into the conversion step. The pipeline is
line-oriented: a malformed line is dropped with a warning, the
remaining lines are still processed. The pipeline does not
abort on a single bad line; it logs the failure and continues.

## 3. The seven stages

The pipeline has seven stages, each with a defined input, output,
time budget, and failure mode. The stages are described
sequentially; the pipeline is implemented as a single Lua
function call (`M.ingest_file` in
`/home/user/seed-dev/lua/helpers/codex_ingest.lua:81`) but the
seven stages are logical; a re-implementation in another
language would preserve the same boundaries.

### 3.1 Stage 1 — Parse (JSON to S-expr)

**Input** — a path to a `.sref` file or a JSON string.

**Output** — a sequence of S-expressions in the SXL dialect.

**Mechanism** — the parser at
`/home/user/seed-dev/src/libsexpr/src/sexpr.c:1` reads the
JSON-line document, parses each line with `cjson`, and
converts the parsed entry into an S-expression using the
mapping in
`/home/user/seed-dev/lua/helpers/codex_ingest.lua:9` (the
`CODE_TYPE` table). The mapping is:

- `codex_law` → `:type belief` (laws are beliefs about how
  to act).
- `text` → `:type knowledge` (glossary entries are
  knowledge).
- `protocol` → `:type knowledge` (protocols are procedural
  knowledge).
- `scroll` → `:type knowledge` (scrolls are canonical
  knowledge).
- `index` → `:type context` (section headers are context
  markers).
- `personae` → `:type identity` (personae are identity
  models).
- `chapter` → `:type knowledge` (chapters are structured
  knowledge).
- `meta` → `:type context` (metadata is context).

A `kind` not in the `CODE_TYPE` table is mapped to
`:type knowledge` by default. The mapping is normative; a
runtime that changes it without an RFC is non-conformant.

**Time budget** — ≤ 5 ms per SREF line on a Raspberry Pi
class CPU. The full codex (~305 files, per
`/home/user/seed-dev/docs/architecture/DEVELOPMENT_STATUS.md:213`)
must complete in ≤ 30 s at startup.

**Failure modes** — `cjson.decode` failure (malformed JSON
line) drops the line with a warning. A missing `kind` or
`version` field rejects the entry at the schema boundary.
A `version` other than `sref_v2` triggers a migration step
or a rejection, depending on policy.

### 3.2 Stage 2 — Validate (against `sref_v2_schema.json`)

**Input** — the parsed JSON entry from Stage 1.

**Output** — a validated entry, or a rejection.

**Mechanism** — the entry is validated against
`/home/user/seed-dev/codex/machina/schemas/sref_v2_schema.json:1`.
The validator checks `kind` against the closed enum,
`version` against the constant `sref_v2`, and the per-`kind`
required fields. The SXL envelope at
`/home/user/seed-dev/schemas/.sref/v1/sxl.sref:1` is the
secondary check; the SXL entity produced by Stage 3 must
validate against the SXL schema before it is stored.

**Time budget** — ≤ 1 ms per entry.

**Failure modes** — schema mismatch (missing required field,
wrong `kind` enum value, invalid `version`) rejects the entry.
The rejection is logged with the schema violation, the file
path, and the line number. The pipeline does not abort; the
remaining entries are still processed.

### 3.3 Stage 3 — Hash (BLAKE3-256 canonical identity)

**Input** — the validated entry from Stage 2.

**Output** — a 32-byte BLAKE3-256 digest.

**Mechanism** — the canonical form of the entry is computed
(whitespace-normalised, key-sorted), and BLAKE3-256 is
applied. The hash is the entry's canonical identity. Two
entries with the same BLAKE3-256 hash are byte-identical
modulo whitespace and key order. The hash is the entry's
`:id` field; the entry's ULID (from the SREF header) is the
`:id` for runtime bookkeeping, but the BLAKE3-256 hash is the
identity that the cognitive engine reasons over (because the
ULID is not deterministic).

The BLAKE3-256 hash function is the canonical hash for
`libsmem` (per
`/home/user/seed-dev/src/libsmem/src/datachain.c:7` —
"each block is signed and chained to its predecessor by a
BLAKE3-256 hash"). The BLAKE2b-256 hash used for `schema_fp`
in the SREF envelope (per
`/home/user/seed-dev/schemas/.sref/v1/envelope.sref:38`) is a
different surface: `schema_fp` is the hash of the schema
document, not the hash of the record. A runtime that confuses
the two is non-conformant.

**Time budget** — ≤ 0.1 ms per entry.

**Failure modes** — none. BLAKE3-256 is a pure function with
no failure modes. The hash is always computed; the result is
always 32 bytes.

### 3.4 Stage 4 — Extract (objects, relations, tags, refs)

**Input** — the validated and hashed entry from Stage 3.

**Output** — a typed SXL entity, plus a list of relations
(references, tags, same-collection links).

**Mechanism** — the `codex_entry_to_sxl` function at
`/home/user/seed-dev/lua/helpers/codex_ingest.lua:30` builds
the SXL expression. The body is escaped for SXL (newlines
become spaces, double-quotes are backslash-escaped), and
truncated to 1021 characters with a trailing `...`. The SXL
expression carries `:type`, `:id`, `:source "codex"`,
`:schema "seed.sxl/v1"`, `:timestamp`, `:confidence 0.99`,
`:title`, and `:content` with `:body` and `:tags`.

The relations are extracted by the `build_relations` function
at
`/home/user/seed-dev/lua/helpers/codex_ingest.lua:57`. For
each entry, the function generates one relation per `ref`
field (label `references`) and one relation per `tag` (label
`tagged`). The relations are SXL entities of `:type relation`
themselves, with `:from` set to the entry's id, `:to` set to
the ref, `:label` set to the relation kind, and `:source
"codex"`.

**Time budget** — ≤ 0.5 ms per entry.

**Failure modes** — body escaping failure (a SREF body that
contains a malformed UTF-8 sequence) is dropped. The entry
is still stored, but the body is replaced with the literal
string `<<unprintable>>` and the drop is logged.

### 3.5 Stage 5 — Build semantic relations

**Input** — the SXL entities and relations from Stage 4.

**Output** — a semantic relations graph, indexed by entity id
and by tag.

**Mechanism** — the entities and relations are added to an
in-memory graph keyed by entity id. The graph supports three
query types:

- **By id** — return the entity and its outgoing relations.
- **By tag** — return all entities with a given tag (the
  `tagged` relations from Stage 4).
- **By ref** — return all entities that reference a given
  id (the `references` relations from Stage 4).

The graph is built incrementally as entries are ingested; it
is not materialised to disk at this stage. The graph is
materialised to `libsmem` in Stage 6.

**Time budget** — ≤ 1 ms per entry; the full graph build for
the codex (~305 files) must complete in ≤ 5 s.

**Failure modes** — duplicate entry (same BLAKE3-256 hash as
a previously-seen entry) is dropped. The drop is logged; the
first entry wins. A near-duplicate (different BLAKE3-256 hash
but same content modulo whitespace) is linked, not stored
twice (per
`/home/user/seed-dev/docs/memory/MEMORY_SYSTEM_ARCHITECTURE.md:209`).

### 3.6 Stage 6 — Store (write to `libsmem` partition)

**Input** — the SXL entities and relations from Stages 4–5.

**Output** — durable records in the appropriate `libsmem`
partition.

**Mechanism** — each SXL entity is written to
`cognitive/this-node/codex` by default (per
`/home/user/seed-dev/lua/helpers/codex_ingest.lua:137`).
The partition id follows the three-component
`<scope>/<reach>/<name>` form (per
`/home/user/seed-dev/docs/memory/MEMORY_SYSTEM_ARCHITECTURE.md:24`):

- `scope` — `cognitive` (the codex is the cognitive
  constitution of the system).
- `reach` — `this-node` (the ingested codex is
  node-local; cross-node distribution is a separate
  step).
- `name` — `codex` (the canonical codex partition).

The `seed.mem.put` call at
`/home/user/seed-dev/lua/helpers/codex_ingest.lua:141`
writes the SXL entity to the partition's append-only log.
The `libsmem` engine canonicalises the entity, hashes it
with BLAKE3-256, and updates the partition's vector index
(if the partition has the vector-index feature enabled).

**Time budget** — ≤ 0.5 ms per entity; the full codex store
must complete in ≤ 10 s.

**Failure modes** — partition not found is a fatal error;
the pipeline aborts. Permission denied (the actor's role
lacks `seed.mem.put` on the partition) is a fatal error; the
pipeline aborts and the actor is informed. Append-only log
full (disk exhausted) is a fatal error; the pipeline aborts
and an alert is raised.

### 3.7 Stage 7 — Publish (emit the bus topic)

**Input** — the stored entities from Stage 6.

**Output** — a bus event on `org.seed.codex.ingested`.

**Mechanism** — the `seed.bus.publish` call at
`/home/user/seed-dev/lua/helpers/codex_ingest.lua:145`
emits a bus event with the partition name and the count of
stored entities. The event is a typed SXL entity with
`:type "codex-ingested"`, `:schema "seed.codex.ingested/v1"`,
and `:content { partition, count }`. Downstream consumers
subscribe to the topic and react to new arrivals.

**Time budget** — ≤ 0.1 ms per event; the publish is
non-blocking (the bus broker is asynchronous).

**Failure modes** — bus broker unavailable is a
soft-failure; the storage has succeeded, the publish is
skipped, and the failure is logged. A retry loop is started
in the background.

## 4. The semantic relations graph

The semantic relations graph is the immediate output of Stage 5.
For a corpus of N SREFs, the graph has N nodes (the SREFs) and
M edges (the relations). The edge types are:

- **tag-co-occurrence** — two SREFs that share a tag are
  connected by a `tagged` relation (per
  `/home/user/seed-dev/lua/helpers/codex_ingest.lua:69`).
- **ref-link** — a SREF that names another SREF in its `refs`
  field is connected by a `references` relation (per
  `/home/user/seed-dev/lua/helpers/codex_ingest.lua:61`).
- **same-collection** — two SREFs from the same source file
  are connected by a `same-collection` relation (Stage 5
  extension; not in the base ingest path).
- **same-author** — two SREFs by the same `@actor` are
  connected by a `same-author` relation (Stage 5 extension).
- **time-proximity** — two SREFs whose `@time` is within a
  threshold (default 1 hour) are connected by a
  `time-proximity` relation (Stage 5 extension).

The graph is stored in `libsmem` with the same BLAKE3-256
identity as the underlying SREFs. Each edge is a SXL entity of
`:type relation` with `:from`, `:to`, `:label`, and
optionally `:weight`. The graph is queryable through
`seed.mem.search` (per
`/home/user/seed-dev/lua/helpers/codex_ingest.lua:154`).

The cognitive engine queries the graph for four patterns:

- **Related concepts** — given a SREF, return the SREFs
  connected to it by any edge. The result is a list of
  related SREFs sorted by edge weight and edge label.
- **Divergent sources** — given a SREF, return the SREFs
  that contradict it. The result is a list of SREFs whose
  `tagged` or `references` relations are inverses.
- **Consensus / disagreement** — given a topic, return the
  SREFs that address the topic and the relations among them.
  A topic with many SREFs and few `contradicts` relations is
  consensus; a topic with many `contradicts` relations is
  disagreement.
- **Evolutionary trajectory** — given a SREF id, return the
  SREFs that supersede, refine, or contradict it over time.
  The result is a chronological sequence of SREFs that
  documents the evolution of the concept.

The semantic relations graph is the **raw evidence**; the
knowledge graph (next section) is the **abstraction** the
cognitive engine reasons over.

## 5. The knowledge graph

The knowledge graph is a higher-level view: a typed graph
where nodes are **concepts** (extracted from SREFs) and edges
are **typed relations** (`is-a`, `has-property`, `related-to`,
`contradicts`, `supports`, etc.). The semantic relations graph
is the raw evidence; the knowledge graph is the abstraction.

The transformation from semantic relations to knowledge graph
happens in the cognitive engine, not in the pipeline. The
pipeline produces the semantic relations graph; the cognitive
engine reads the graph, extracts concepts (entities that
appear as the target of `references` or `tagged` relations),
and materialises the knowledge graph as a separate SXL
partition (`cognitive/this-node/knowledge`).

The knowledge graph is the substrate for cognitive engine
reasoning. The 12-phase C cycle (per
`/home/user/seed-dev/src/seedcogd/main.c:1`) reads the
knowledge graph in Phase A, queries it in Phase B, updates
it in Phase C (every 5 cycles), and propagates confidence
over it in Phase D. The four query types from §4 are
reformulated as knowledge-graph queries:

- **Related concepts** — return the concepts connected to
  the query concept by an `is-a`, `has-property`, or
  `related-to` edge.
- **Divergent sources** — return the concepts that
  contradict the query concept.
- **Consensus / disagreement** — return the subgraph rooted
  at the query concept and compute the consensus /
  disagreement score.
- **Evolutionary trajectory** — return the temporal
  sequence of knowledge-graph states that contain the
  query concept.

The difference between the semantic relations graph and the
knowledge graph is the difference between **raw evidence**
and **abstraction**. The semantic relations graph is the
`WHERE` of SREF-to-SREF relationships; the knowledge graph is
the `WHAT` of concept-to-concept relationships. The semantic
relations graph is built by the pipeline; the knowledge graph
is built by the cognitive engine. The semantic relations
graph is deterministic; the knowledge graph is
probabilistic.

## 6. The SREF ingestion API

For a runtime that wants to ingest a SREF, the API is exposed
as three bus topics. The topics are part of the FROZEN-2026-05-10
namespace (per
`/home/user/seed-dev/docs/event-system/TOPIC_NAMING.md:1` and
`codex/machina/SPEC.md:27`).

### 6.1 `seed.codex.ingest v1` — submit a SREF

A runtime publishes a SREF to `org.seed.codex.ingest` (T1,
cognitive plane). The SREF is the body; the envelope is the
standard SXL envelope with `:schema "seed.codex.ingest/v1"`.
The pipeline runs synchronously; the response is a SXL envelope
of `:type "codex-ingested"` (or `:type "codex-rejected"`) with
`:relations[0].to` pointing to the request envelope's `:id`.

A request that fails validation is rejected with a
`codex-rejected` envelope and a `:confidence` of zero. A
request that succeeds returns a `codex-ingested` envelope with
the partition name and the count of stored entities.

### 6.2 `seed.codex.query v1` — query the knowledge graph

A runtime publishes a query to `org.seed.codex.query` (T1,
cognitive plane). The query is a SXL envelope of
`:type "codex-query"` with `:content { pattern, kind, limit }`.
The cognitive engine runs the query against the knowledge
graph and returns a SXL envelope of `:type "codex-result"`
with `:content { matches: [...] }`.

The four query types from §4 are exposed as `kind` values:
`related`, `divergent`, `consensus`, `trajectory`. The
`pattern` is a SXL pattern expression; the `limit` is the
maximum number of matches (default 10).

### 6.3 `seed.codex.subscribe v1` — subscribe to new SREF arrivals

A runtime subscribes to `org.seed.codex.ingested` (T1, cognitive
plane) to receive notifications of new SREF arrivals. The
subscription is a standard bus subscription; the runtime
receives a SXL envelope of `:type "codex-ingested"` for each
new arrival. The envelope carries the partition name and the
count of stored entities.

The subscription is durable; the bus broker retains the
subscription across restarts. A subscription that is not
consumed within the `ttl` window is dropped; the runtime must
re-subscribe.

### 6.4 The bus topic contract

The request / response envelope for all three topics is the
standard SXL envelope (per `codex/machina/SPEC.md:59`). The
required fields are:

- `:type` — the request / response kind.
- `:id` — ULID, unique forever.
- `:timestamp` — uint64 nanoseconds since epoch.
- `:creator` — DID in the form `did:seed:<node>:<daemon>`.
- `:confidence` — float in `[0, 1]`.
- `:schema` — versioned schema string.
- `:provenance` — `{ source, parents[], attribution }`.
- `:relations` — `[{ to, label, weight? }]`.
- `:status` — enum (`proposed`, `accepted`, `rejected`).
- `:content` — domain-specific payload.

A request that fails the envelope validation is rejected at
the broker boundary; the requester is informed via a
`:type "codex-rejected"` response.

### 6.5 The `seedreasond` validation step

Per `codex/machina/INTEGRATION-CONTRACT.md:107`, every
`seedreasond` invocation is validated against the ACL and the
12-phase C cycle. A SREF ingestion that goes through
`seedreasond` (rather than the direct bus publish) is validated
twice: once at the broker boundary (ACL + envelope) and once
in the C cycle (SXL schema + `libsmem` permission). A SREF
that fails either validation is rejected.

The `seedreasond` path is the recommended path for sapling
agents; the direct bus publish is the path for `core` and
`higher_order` agents. The path is selected by the agent's
ACL role; a sapling agent (`external`) cannot publish to
`org.seed.codex.ingest` directly and must go through
`seedreasond`.

## 7. The cognitive engine's use of the graph

The cognitive engine reads the knowledge graph in the 12-phase
C cycle (per
`/home/user/seed-dev/src/seedcogd/main.c:1`). The relevant
phases are:

- **Phase A** — subscribe to bus messages, stage them in the
  `sst_workspace_t`, dispatch the cycle's work.
- **Phase B** — run the contradiction check and plan
  generation. A new SREF that contradicts an existing SREF
  triggers a plan to reconcile the contradiction.
- **Phase C** (every 5 cycles) — run hippocampus
  consolidation (episodic → semantic). The consolidation
  extracts new concepts and adds them to the knowledge
  graph.
- **Phase D** — run prediction and compare against the
  previous cycle's predictions; the prediction-error EMA
  feeds into attention, reflection, learning, and
  meta-cognition.
- **Phase H** — run the attention gate on incoming bus
  messages.
- **Phase J** (every 7 cycles) — update the goal state.

The cognitive engine's use of the graph is the operational
expression of the Recursive Codex loop (per
`codex/02-LIVING-CONSTITUTION.md:237`). Phase 1 (Perception)
is the bus-subscribe step; Phase 2 (Ontology) is the
consolidation step; Phase 3 (Identity) is the
identity-divergence step; Phase 4 (Governance) is the
contradiction-check step.

## 8. Cross-references

- `codex/README.md` — codex home.
- `codex/02-LIVING-CONSTITUTION.md` — the Living
  Constitution principle and the Recursive Codex loop.
- `codex/INTEGRATION.md` — how the codexes integrate into
  S.E.E.D.
- `codex/machina/SPEC.md` — the machine-facing contract.
- `codex/machina/INTEGRATION-CONTRACT.md` — the loadable
  runtime contract (the `seedreasond` validation step).
- `codex/solbian/SPEC.md` — the human-facing spec.
- `../seed/INTEGRATION.md` — S.E.E.D.'s narrative view of
  the integration.
- `/home/user/seed-dev/lua/helpers/codex_ingest.lua:1` —
  the pipeline implementation.
- `/home/user/seed-dev/codex/machina/schemas/sref_v2_schema.json:1`
  — the v2 schema.
- `/home/user/seed-dev/schemas/.sref/v1/_grammar.ebnf:1` —
  the v1 SREF grammar.
- `/home/user/seed-dev/schemas/.sref/v1/envelope.sref:1` —
  the bus envelope.
- `/home/user/seed-dev/schemas/.sref/v1/sxl.sref:1` — the
  SXL entity schema.
- `/home/user/seed-dev/src/libsexpr/src/sexpr.c:1` — the
  S-expression parser.
- `/home/user/seed-dev/src/libsmem/include/seed/smem.h:1` —
  the `libsmem` partition model.
- `/home/user/seed-dev/docs/memory/MEMORY_SYSTEM_ARCHITECTURE.md:24`
  — the scope / reach / partition model.
- `/home/user/seed-dev/docs/architecture/DEVELOPMENT_STATUS.md:207`
  — the codex ingestion pipeline section.
- `/home/user/seed-dev/docs/architecture/MASTER_ARCHITECTURE.md:209`
  — the Codex Access section.
- `/home/user/seed-dev/docs/DRAFTS/seed-codex-specs.txt:1` —
  the canonical source of the codex specifications.
- `/home/user/seed-dev/docs/DRAFTS/seed-misc-specs.txt:1` —
  the canonical source of the four-representation model.
- `/home/user/seed-dev/docs/DRAFTS/seed-cog3-specs.txt:1` —
  the canonical source of the cognitive workflow and the
  Recursive Codex loop.
