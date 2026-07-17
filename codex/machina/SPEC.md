# SPEC — Codex Machina

> **Status**: Draft.
> **Version**: 0.1.0.
> **Last updated**: 2026-07-16.
> **Source-of-truth pairing**: `../solbian/SPEC.md`
> (Codex Solbian, the narrative pair).

This is the formal specification of the
S.E.E.D. ↔ Sprout integration. It is
written for a runtime to validate
against. It must agree with
`../solbian/SPEC.md`.

## 1. Scope

This spec covers the bus schema, the
cognitive event schema, the motor intent
schema, the sensory observation schema,
the runtime requirements, and the
versioning rules. It does **not** cover
the implementation; that lives in
`~/seed-dev/` and `~/robot-dev/`.

## 2. The bus

### 2.1 Topic namespace (FROZEN-2026-05-10)

```
org.seed.<segment>(.<segment>){1,5}
```

- `org.seed` is the literal prefix.
- 2 to 6 segments, separated by `.`.
- Each segment is `[a-z][a-z0-9_-]{0,31}`.
- The full grammar is at
  `~/seed-dev/schemas/.sref/v1/topic_grammar.ebnf`;
  the reference validator is at
  `~/seed-dev/src/libbus/src/topic.c`.
- Tier letters (T0/T1/T2) are **not** in
  topic names. Tier is a property of the
  transport, not the topic.

### 2.2 Three tiers

- **T0 — control plane** — in-process
  control messages in the cognitive
  cycle. ACL `system` only. Sapling
  agents are denied.
- **T1 — cognitive plane** — UDS via
  `seedbusbrokerd` at
  `/run/seed/bus.sock`. The main channel
  for the integration.
- **T2 — data plane** — encrypted
  cross-node via `libnet` /
  `seedneted`. High-throughput raw
  sensor data and audit streams.

### 2.3 The SXL envelope

Every bus message is a typed SXL entity:

```lisp
(:type <kind> :id <ulid> :timestamp <uint64-ns>
 :creator <did> :confidence <float[0,1]>
 :schema "seed.sxl/v1"
 :provenance { :source ... :parents [...] :attribution ... }
 :relations [{ :to ... :label ... :weight ... }]
 :status <enum>
 :content { ... domain-specific ... })
```

The validator is at
`~/seed-dev/src/libsexpr/src/validate.c`;
it checks `:type`, `:schema`, and the
required fields against the canonical
SXL entity hierarchy.

### 2.4 The 5 ACL roles

The bus ACL is at
`~/seed-dev/codex/machina/policies/acl/agent_acl.sref`.
The 5 roles:

| Role           | Read | Write (own) | Execute | Network | Default for       |
|----------------|------|-------------|---------|---------|-------------------|
| `system`       | ✓    | ✓           | ✓       | ✓       | cognitive cycle   |
| `core`         | ✓    | ✓           | ✓       | ✓       | graduated agents  |
| `higher_order` | ✓    | ✓           | ✓       | —       | brain cycle       |
| `observer`     | ✓    | —           | —       | —       | telemetry         |
| `external`     | ✓    | —           | —       | —       | sapling agents    |

A role's permissions are evaluated
**per topic**. The default-deny rule
applies: a role can publish to a topic
only if an explicit allow rule exists.

## 3. Sensory observation schema

A sensory observation is published on
`org.seed.observation.sensor.*` topics
(T1 or T2). Required fields:

| Field            | Type            | Description                                 |
|------------------|-----------------|---------------------------------------------|
| `:type`          | keyword         | `observation`                               |
| `:id`            | ULID            | unique forever                              |
| `:timestamp`     | uint64 ns       | acquisition time on the sensor              |
| `:creator`       | DID             | `did:seed:<node>:<daemon>`                  |
| `:confidence`    | float [0, 1]    | sensor health / reading confidence          |
| `:schema`        | string          | `seed.observation.sensor/<kind>/v1`         |
| `:content`       | object          | per-kind payload (see below)                |

Per-kind payloads:

- `:kind distance` — `{ front, left, right, rear (optional) }` in mm.
- `:kind inertial` — `{ ax, ay, az, gx, gy, gz, mx, my, mz, dt }`.
- `:kind environment` — `{ temp, humidity, pressure, light, rgb }`.
- `:kind thermal` — `{ grid: number[64] }` (8×8 AMG8833).
- `:kind audio` — `{ samples: int16[N], mic_id, sample_rate }`.
- `:kind power` — `{ vbat, current, power }`.

## 4. Motor intent schema

A motor intent is published on
`org.seed.action.intend.motor` (T1).
Required fields:

| Field            | Type            | Description                                 |
|------------------|-----------------|---------------------------------------------|
| `:type`          | keyword         | `intent`                                    |
| `:id`            | ULID            | unique forever                              |
| `:timestamp`     | uint64 ns       | plan time                                   |
| `:creator`       | DID             | `did:seed:<node>:<agent-cognitive>`         |
| `:confidence`    | float [0, 1]    | the cycle's confidence in the plan          |
| `:schema`        | string          | `seed.intent.motor/v1`                      |
| `:content`       | object          | `{ command, linear, angular, head_pan, head_tilt, duration_ms, deadline_ms }` |

The `command` is one of:
`translate`, `rotate`, `aim_head`,
`stop`, `dock`.

The `deadline_ms` is the time after
which the intent is considered failed
(R7).

## 5. Policy check schema

A policy check is published on
`org.seed.policy.check` (T1). Required
fields:

| Field            | Type            | Description                                 |
|------------------|-----------------|---------------------------------------------|
| `:type`          | keyword         | `policy-check`                              |
| `:id`            | ULID            | unique forever                              |
| `:timestamp`     | uint64 ns       | check time                                  |
| `:creator`       | DID             | checker DID                                 |
| `:confidence`    | float [0, 1]    | checker's confidence                        |
| `:schema`        | string          | `seed.policy.check/v1`                      |
| `:content`       | object          | `{ intent_id, verdict, rule, reason }`      |

`verdict` is `allow` or `deny`. `rule`
is the rule that fired (e.g. `R3` or
`schema-mismatch`).

## 6. The 8 reflex rules (R1–R8)

The on-device policy must implement the
following 8 rules. The first rule that
fails denies the command.

| Rule | Trigger                                      | Action |
|------|----------------------------------------------|--------|
| R1   | any bump switch pressed                      | stop   |
| R2   | front ToF below threshold                    | stop   |
| R3   | any ToF < 50 mm                              | stop   |
| R4   | a ToF fails to return > 5 consecutive ticks  | stop   |
| R5   | Vbat below threshold (INA226)                | stop   |
| R6   | motor driver nFAULT asserted                 | stop   |
| R7   | motor command missed its deadline            | stop   |
| R8   | IMU reports free-fall                        | stop   |

The thresholds (R2, R5) are
configurable per deployment in
`/etc/seed/robot.toml`.

## 7. Runtime requirements

A runtime that claims to be S.E.E.D.
must:

- Host `seedbusbrokerd` at
  `/run/seed/bus.sock`.
- Speak SXL on the bus.
- Implement the 12-phase C cycle in
  `~/seed-dev/src/seedcogd/main.c`
  (phases A–L).
- Validate bus messages via
  `~/seed-dev/src/libsexpr/src/validate.c`.
- Log every cycle step to the cog-journal
  at `${SEED_DATA_DIR}/cog-journal.jsonl`.

A runtime that claims to be Sprout must:

- Run the firmware on the ESP32
  (`~/robot-dev/src/firmware-esp32/`)
  with R1–R8 active.
- Speak JSON to the firmware via
  `ByteSource` (Stdio, Serial, or HTTP).
- Translate intents to SXL via
  `IntegrationBridge` for the bus.
- Log every policy decision (allow or
  deny) to the cog-journal.

A runtime that claims to be a sapling
agent must:

- Speak SXL in and SXL out.
- Hold the `external` ACL role by
  default; upgrade to `core` or
  `higher_order` only at graduation.
- Subscribe to
  `org.seed.observation.sensor.*` and
  `org.seed.memory.*` for inputs.
- Publish to `org.seed.cog.llm.*`,
  `org.seed.memory.*`,
  `org.seed.symbol.*`, or
  `org.seed.symbol.canon.proposed` for
  outputs.
- Never publish to
  `org.seed.action.intend.motor`.

## 8. Validation rules

A conformant runtime must pass:

- **Schema validation** — every bus
  message validates against its
  `:schema`.
- **ACL validation** — every
  publish/subscribe action is allowed
  by the actor's role.
- **Topic validation** — every topic
  parses against
  `topic_grammar.ebnf`.
- **Safety validation** — every motor
  intent is denied if any of R1–R8
  fires.
- **Smoke test** — the runtime
  integration smoke test in
  `~/seed-dev/Testing/` passes.

## 9. Versioning

- The spec version follows semver.
- A breaking change (a new required
  field, a renamed topic, a removed
  ACL role) increments the major
  version.
- A non-breaking change (a new
  optional field, a new topic) increments
  the minor version.
- A clarification (typo fix, example)
  increments the patch version.
- The narrative pair
  (`../solbian/SPEC.md`) and the formal
  pair (this file) must always be
  version-locked. A change to either
  increments both.

## 10. Cross-references

- `../solbian/SPEC.md` — the narrative
  pair. Must agree on every claim.
- `~/seed-dev/docs/cognition/SXL_LANGUAGE_SPECIFICATION.md`
  — the SXL spec.
- `~/seed-dev/docs/event-system/TOPIC_NAMING.md`
  — the topic naming spec.
- `~/seed-dev/codex/machina/policies/acl/agent_acl.sref`
  — the agent ACL.
- `~/seed-dev/schemas/.sref/v1/topic_grammar.ebnf`
  — the topic grammar.
- `~/robot-dev/docs/specs/safety-requirements.md`
  — the R1–R8 spec.
- `~/seed-dev/src/libsexpr/src/validate.c`
  — the SXL validator.
- `~/seed-dev/src/libbus/src/topic.c`
  — the topic validator.
- `~/seed-dev/src/seedcogd/main.c` —
  the 12-phase C cycle.
- `~/robot-dev/src/neocortex/safety.py`
  — the host-side safety policy.
- `~/robot-dev/src/firmware-esp32/src/main.cpp`
  — the on-device policy and the
  firmware.

## 11. See also

- `README.md` — Codex Machina's home
- `CHANGELOG.md` — release notes
- `../solbian/SPEC.md` — the narrative
  pair
- `../README.md` — the codex parent
  directory
- `../INTEGRATION.md` — how the two
  codexes fit together
- `../../docs/METHODOLOGY.md` —
  spec-first workflow
