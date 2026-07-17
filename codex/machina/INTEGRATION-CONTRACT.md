# INTEGRATION CONTRACT — Codex Machina

> **Status**: Draft synthesis, version 0.1.0.
> **Last updated**: 2026-07-16.
> **Source-of-truth pairing**: `../solbian/SPEC.md` (the narrative
> pair) and `SPEC.md` in this directory (the formal spec).

This file is the loadable contract a runtime validates against. It
synthesises the 5-role ACL, the 3-tier bus, the SXL envelope, the
`seedreasond` invocation contract, the policy-bundle activation
protocol, and the Solace governance thresholds into a single
document. The narrative form lives here; the formal form lives in
`SPEC.md`. Both must agree on every claim.

The canonical source for each underlying artefact is in
`/home/user/seed-dev/codex/machina/`. Per
`/home/user/solbian/CLAUDE.md` rule 4, the solbian copy is the
curated narrative; the seed-dev copy is the source-of-truth
snapshot of the running code.

## 1. The 5-role ACL with topic-pattern-scoped permissions

The bus ACL is a two-layer model. The **role layer** binds the
five roles to a coarse capability grant; the **topic-pattern
layer** binds each role to a set of allowed or denied bus-topic
globs. A publish or subscribe action is allowed only if the role
permission is set AND a matching topic rule exists.

The role capabilities are:

- `system` — read, write, execute, network.
- `core` — read, write, execute, network.
- `higher_order` — read, write, execute; *no network*.
- `observer` — read only.
- `external` — read only on a sandboxed subset.

The default-deny rule applies. A role that is not explicitly
granted a capability on a topic is denied that capability on that
topic, regardless of what other topics it is allowed on. The
detail of which topic patterns each role can touch lives in
`ACL.md` and the seed-dev source; the contract summary is: `core`
and `system` may publish motor intents; `core`, `system`, and
`higher_order` may publish observations and cognitive events;
`observer` and `external` may subscribe but not publish.

→ Source: `ACL.md` in this codex;
`/home/user/seed-dev/codex/machina/policies/acl/agent_acl.sref`.

## 2. The 3-tier bus

The bus has three transport tiers. Tier is a property of the
transport, not of the topic. A topic name does not encode its
tier; the bus broker and the runtime decide which tier carries
which message at publish time.

- **T0 — control plane** — in-process control messages inside
  the cognitive cycle. ACL `system` only. Sapling agents are
  denied. Used for high-frequency, in-host coordination that
  must not be visible on the UDS socket.
- **T1 — cognitive plane** — UDS via `seedbusbrokerd` at
  `/run/seed/bus.sock`. The main channel for the S.E.E.D. ↔
  Sprout integration. The bus ACL is enforced at the broker
  boundary.
- **T2 — data plane** — encrypted cross-node transport via
  `libnet` / `seedneted` using Noise IK. High-throughput raw
  sensor data, audit streams, and any payload that crosses a node
  boundary. End-to-end encrypted; per-message authentication
  via the destination's static Noise key.

A runtime must host the broker at `/run/seed/bus.sock`, speak
SXL on the bus, and route T0 messages in-process, T1 messages
through the broker, and T2 messages through `libnet`. The
routing decision is made by the publisher at publish time and
recorded in the envelope's `:provenance` block.

→ Source: `SPEC.md` §2.2 in this codex; the bus broker
implementation is `~/seed-dev/src/libbus/`.

## 3. The SXL envelope

Every bus message is a typed SXL entity. The envelope is the
single shape every payload must take; per-kind content lives
under `:content`. The full set of fields a conformant envelope
may carry, and the enforcement layer that requires each one,
is:

- `:type` — keyword naming the SXL entity type (`observation`,
  `intent`, `policy-check`, etc.).
- `:id` — ULID, unique forever.
- `:timestamp` — uint64, nanoseconds since epoch.
- `:creator` — DID in the form `did:seed:<node>:<daemon>`.
- `:confidence` — float in `[0, 1]`, see §6 below.
- `:schema` — versioned schema string, e.g. `seed.sxl/v1` or
  `seed.observation.sensor/distance/v1`.
- `:provenance` — `{ source, parents[], attribution }`.
- `:relations` — `[{ to, label, weight? }]`.
- `:status` — enum (typically `proposed` | `accepted` |
  `rejected` | `quarantined`).
- `:content` — domain-specific payload, shaped by `:schema`.

The enforcement layers differ. The canonical S-expression
validator at `~/seed-dev/src/libsexpr/src/validate.c:87-115`
(`sxp_validate`) only enforces the four required fields
below; any envelope that lacks one of these is rejected at the
envelope layer before the broker is consulted:

- **Required by canonical validator** (`sxp_validate` in
  `~/seed-dev/src/libsexpr/src/validate.c:87-115`):
  - `:type` — must be a known SXL entity type
  - `:id` — must be present
  - `:schema` — must equal the literal string `seed.sxl/v1`
  - `:content` — must be present

The remaining five fields are **required by codex integration
policy**, not by the canonical validator. They are part of
this contract and a conformant runtime MUST enforce them at the
broker boundary even though `sxp_validate` does not check
them:

- **Required by codex integration policy** (this contract):
  - `:timestamp` — uint64, nanoseconds since epoch
  - `:creator` — DID in the form `did:seed:<node>:<daemon>`
  - `:confidence` — float in `[0, 1]`, see §6
  - `:provenance` — `{ source, parents[], attribution }`
  - `:relations` — `[{ to, label, weight? }]`
  - `:status` — enum (`proposed` | `accepted` | `rejected` |
    `quarantined`)

The split exists because `sxp_validate` is the minimal
gatekeeper for parse-correct SXL on the bus, while the full
field set is the contract Codex Machina runtimes must honour
to participate in the cognitive cycle, the confidence-threshold
regime, and provenance-based attribution. A runtime that drops
the codex-policy-required fields will pass `sxp_validate` and
still be rejected by a conformant consumer (e.g. `seedcogd`
when reading a record for the Solace regime in §6). An
envelope that fails either layer of validation is rejected at
the broker boundary.

→ Source: `SPEC.md` §2.3 in this codex;
`SCHEMAS.md` for the SXL metadata and schema placeholders.

## 4. The reasoning and policy contracts

Two daemons together provide the local reasoning surface: a
runtime that conforms to Codex Machina hosts **both** of them
and routes different request kinds to the right one. They are
not the same daemon and must not be conflated.

### 4.1 `seedcogd` — the cognitive cycle runner

`seedcogd` is the cognitive daemon that runs the 12-phase C
cycle (phases A through L). The cycle is implemented as the
`cognitive_tick()` function in
`~/seed-dev/src/seedcogd/main.c:1770`, with the individual
phases A–L implemented across
`~/seed-dev/src/seedcogd/main.c:1718-2784` (Phase A at
`:1925`, Phase B at `:2106`, Phase C at `:2141`, Phase D at
`:2388`, Phase E at `:2258`, Phase F at `:2391`, Phase G at
`:2489`, Phase H at `:2508`, Phase I at `:2617`, Phase J at
`:2728`, Phase K at `:2880`, Phase L at `:3054`). Every cycle
step is logged to the cog-journal at the literal path
`/var/lib/seed/cog-journal.jsonl` (the default argument at
`~/seed-dev/src/seedcogd/main.c:3520`; the systemd unit
`~/seed-dev/src/seedcogd/seedcogd.service:10` also uses the
literal path; future versions may add `${SEED_DATA_DIR}`
overrides, but no such env-var lookup exists today). `seedcogd`
is the source of the `seedcogd-v9` provenance in
cycle-metadata entries and of all cognitive-tick SXL traffic on
the bus.

### 4.2 `seedreasond` — the policy evaluator

`seedreasond` is the policy evaluator daemon. Per
`~/seed-dev/docs/services/seedreasond.md` and
`~/seed-dev/src/seedreasond/src/main.c:1-9`, it evaluates a
loaded policy bundle (or inline S-expression) against
incoming `org.seed.policy.evaluate` JSON payloads and answers
`{"decision":"allow|deny","reason":"..."}`. It does **not**
run the 12-phase C cycle; the request kind is different. The
contract is:

- **Input** — a JSON payload on the bus topic
  `org.seed.policy.evaluate` (via `seed_bus_serve`) or on the
  AF_UNIX intent socket (`--intent-socket PATH`, mutually
  exclusive with the bus). The payload carries a `claim`
  object (and an optional `caps` string). The bus input is
  routed through `seed_reason_attach` and uses
  `seed_policy_eval` from `libsexpr`.
- **Processing** — `seedreasond` loads the policy from
  `--policy-file`, `--policy 'EXPR'`, or
  `--bundle-dir DIR --trusted-pub-hex FILE`, verifies the
  Ed25519 manifest signature and the policy fingerprint
  against the trusted operator key, and evaluates the claim
  via `seed_policy_eval` from `libsexpr`. It holds no
  persistence and no audit log; state is in
  `seed_reason_state_t` and is re-created on restart.
- **Output** — a single line of JSON
  `{"decision":"allow|deny","reason":"..."}` returned
  synchronously on the same bus topic (T0) or the same
  AF_UNIX connection. `seedreasond` does **not** publish to
  any topic; it only serves `org.seed.policy.evaluate`.
- **Failure modes** — a parse error at startup enters
  `deny_all_mode` and logs `policy_alarm`. A bundle
  verification failure (bad signature, bad fingerprint, or
  untrusted operator) logs `bundle_reject` and refuses to
  load. An evaluation-timeout is the caller's responsibility.

### 4.3 The relationship between the two

A conformant runtime hosts both daemons. The C cycle in
`seedcogd` produces cognitive output (reflections, evaluations,
discoveries, beliefs) and logs each step to
`/var/lib/seed/cog-journal.jsonl`. When any step in the cycle
needs a policy decision (e.g. gating a motor intent, deciding
whether a sapling proposal is admissible), it asks
`seedreasond` over the bus on `org.seed.policy.evaluate` and
uses the `allow|deny` reply. The two daemons are independent
processes; `seedcogd` does not embed `seedreasond`, and
`seedreasond` does not embed the C cycle. Run them as two
separate services.

A `seedreasond` invocation that fails ACL is denied at the
broker; one that fails schema validation is denied at the
envelope layer. A C-cycle step in `seedcogd` that fails is
logged with the failing phase and a confidence of zero; the
record then falls under the Solace confidence thresholds
described in §6 of this contract.

→ Source: `SPEC.md` §7 in this codex; the C cycle
implementation is `~/seed-dev/src/seedcogd/main.c:1718-2784`;
the policy evaluator is
`~/seed-dev/src/seedreasond/src/main.c` and is documented at
`~/seed-dev/docs/services/seedreasond.md`.

## 5. The policy-bundle activation protocol at epoch boundaries

A policy bundle is a versioned set of `.sref` artefacts from
`/home/user/seed-dev/codex/machina/policies/` and
`/home/user/seed-dev/codex/machina/policies/acl/`. At every
epoch boundary, the runtime activates a new bundle or
re-activates the current one. The activation protocol is:

1. **Fetch** — the runtime fetches the candidate bundle from the
   signed manifest at the current epoch's policy version.
2. **Verify** — every `.sref` artefact in the bundle is
   validated against `sref_v2_schema.json`. Every signature is
   checked against the signing record
   (`signing.record.sref`). Every cross-reference is resolved.
3. **Simulate** — the bundle is loaded into a sandbox; a
   synthetic set of ACL decisions is run through it; the
   decisions must match the previous bundle's decisions on the
   same inputs to within the agreed delta.
4. **Quorum** — the Seed Council quorum (three) must have
   approved the bundle, with two-or-more countersignatures
   recorded in the signing record.
5. **Activate** — on epoch boundary, the sandboxed bundle
   becomes the live bundle. The previous bundle is retained
   read-only for one epoch for rollback.
6. **Log** — the activation is logged to the cog-journal with
   the bundle's version, the epoch number, the approvers, and
   the activation timestamp.

A bundle that fails any step is rejected; the runtime continues
with the previous bundle. A bundle that fails the simulate step
twice in succession triggers a Seed Council alert.

→ Source: `POLICIES.md` and `ACL.md` in this codex; the
exception register at
`/home/user/seed-dev/codex/machina/policies/exception_register.sref`
for the deviation path.

## 6. The Solace governance thresholds

Solace is the higher-order conscience agent. At every epoch
boundary, Solace scores every pending record and applies the
canonical confidence thresholds from
`/home/user/seed-dev/codex/meta/confidence_rules.sref`:

- **`confidence ≥ 0.98`** — auto-commit. The record is durable
  and becomes part of the next epoch's cognitive context.
- **`0.90 ≤ confidence < 0.98`** — review band. The record is
  held for a human reviewer (or, by exception, a guardian).
  Approval makes the record durable; rejection drops it.
- **`confidence < 0.90`** — below review. The record is
  rejected. The rejection is logged but the record is not
  durable.

For a runtime, the implications are:

- A runtime MUST read the threshold values from the canonical
  file at boot, not from a hard-coded constant.
- A runtime MUST log the regime decision (auto-commit, review,
  or reject) for every record, with the record's `confidence`
  and the threshold band.
- A runtime MUST NOT auto-commit a record below 0.98, even if a
  caller asks it to.
- A runtime MUST NOT silently drop a record below 0.90; the
  rejection is logged and the requester is informed.

The thresholds are themselves a record under the Living
Constitution principle: they can be promoted (raised) or demoted
(lowered) only through the same Solace review path that uses
them. There is no out-of-band override.

→ Source: `CONFIDENCE-RULES.md` in this codex;
`/home/user/seed-dev/codex/meta/confidence_rules.sref`.

## 7. The conformance check

A runtime that claims to be conformant with Codex Machina MUST
pass all five checks below at boot and at every epoch boundary:

1. **Schema validation** — every `.sref` artefact, every SXL
   envelope, and every build manifest validates against its
   declared schema.
2. **ACL validation** — every publish, subscribe, read, write,
   execute, upload, or delete action is allowed by the actor's
   role and topic/resource rule.
3. **Topic validation** — every topic parses against
   `~/seed-dev/schemas/.sref/v1/topic_grammar.ebnf`.
4. **Safety validation** — every motor intent is denied if any
   of R1–R8 fires.
5. **Smoke test** — the runtime integration smoke test in
   `~/seed-dev/Testing/` passes.

A runtime that fails any check must refuse to start (at boot) or
refuse to advance the epoch (at an epoch boundary), and must log
the failing check to the cog-journal.

## See also

- `INDEX.md` — this codex's index
- `SPEC.md` — the formal spec
- `POLICIES.md` — the policy framework
- `ACL.md` — the agent and resource ACLs
- `SCHEMAS.md` — the schemas
- `CONFIDENCE-RULES.md` — the Solace governance thresholds
- `../solbian/SPEC.md` — the narrative pair
- `../INTEGRATION.md` — how this codex fits into S.E.E.D.
- `/home/user/seed-dev/codex/machina/policies/`
- `/home/user/seed-dev/codex/machina/policies/acl/`
- `/home/user/seed-dev/codex/machina/schemas/`
- `/home/user/seed-dev/codex/meta/confidence_rules.sref`
