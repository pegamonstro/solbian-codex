# SPEC — Codex Solbian

> **Status**: Draft.
> **Version**: 0.1.0.
> **Last updated**: 2026-07-16.
> **Source-of-truth pairing**: `../machina/SPEC.md`
> (Codex Machina, the formal pair).

This is the narrative specification of the
S.E.E.D. ↔ Sprout integration. It is
written for a human reader who wants to
understand the integration without
reading the source repos in detail. It
must agree with `../machina/SPEC.md`.

## 1. Summary

Codex Solbian describes the integration
between S.E.E.D. (the cognitive
framework in `~/seed-dev/`) and Sprout
(the robot in `~/robot-dev/`). The
integration is event-based, on a shared
event bus on the `org.seed.*` namespace
(FROZEN-2026-05-10), with a two-layered
safety policy as the trust boundary.
S.E.E.D. produces intentions; Sprout
turns them into physical actions, and
produces sensory observations back to
S.E.E.D. Sapling agents run as external
clients of the bus and may graduate into
first-class components.

## 2. Motivation

The Solbian organism is a single
distributed system with a mind
(S.E.E.D.), a body (Sprout), and a
nursery (sapling). Without a canonical
specification, the three sub-projects
drift apart: topic names diverge,
schemas disagree, and the safety policy
becomes ambiguous. Codex Solbian is the
narrative anchor. It is the entry point
for a human reader, and it is the source
of truth for **what the integration is
supposed to do** (the formal contract is
in Codex Machina).

## 3. Detailed design

The integration has three parts: the
**bus**, the **safety policy**, and the
**cognitive cycle**.

### 3.1 The bus

The bus is a topic-based publish /
subscribe system with three tiers:

- **T0 (control plane)** — in-process
  control messages in the cognitive
  cycle. Sapling agents do not connect
  here; the ACL prevents external
  subscriptions.
- **T1 (cognitive plane)** — the main
  channel. Motor intents, sensory
  observations, action proposals, policy
  check requests and verdicts, cognitive
  events. Carried over UDS via
  `seedbusbrokerd` at
  `/run/seed/bus.sock`.
- **T2 (data plane)** — high-throughput
  cross-node bus traffic, encrypted, for
  multi-node seednet deployments.

Topic names follow the FROZEN-2026-05-10
form `org.seed.<segment>(.<segment>){1,5}`.
Tier letters are not in topic names; tier
is a property of the transport.

### 3.2 The safety policy

The safety policy is the **trust
boundary** between S.E.E.D. and Sprout.
It is two-layered:

- **Host-side policy** in
  `~/robot-dev/src/neocortex/safety.py`.
  Validates against the schemas, checks
  against the cognitive cycle's current
  goals, verifies against the confidence
  threshold, cross-checks against the
  robot's state. Logs every decision to
  the cog-journal.
- **On-device policy** in
  `~/robot-dev/src/firmware-esp32/src/main.cpp`.
  Implements 8 reflex rules (R1–R8)
  driven by sensors, evaluated in order;
  the first rule that fails denies the
  command.

The on-device policy is **fail-safe**:
a policy that crashes or times out
denies the command. The on-device policy
runs in a FreeRTOS task with higher
priority than the motor-control task; a
compromised neocortex cannot stop it,
modify it, or bypass it.

The eight reflex rules (R1–R8):

- **R1 — Bump**: any bump switch
  pressed → stop.
- **R2 — Distance (front)**: front ToF
  below threshold → stop.
- **R3 — Distance (any)**: any ToF
  < 50 mm → stop.
- **R4 — VL53L0X fail**: a ToF sensor
  fails to return a reading for more
  than 5 ticks → stop.
- **R5 — Battery (INA226)**: Vbat
  below threshold → stop.
- **R6 — nFAULT**: motor driver nFAULT
  asserted → stop.
- **R7 — Deadline**: motor command
  missed its deadline → stop.
- **R8 — IMU free-fall**: IMU reports
  free-fall → stop.

### 3.3 The cognitive cycle

The 12-phase C cycle in
`~/seed-dev/src/seedcogd/main.c` is the
**conductor** of the integration. Phase
A subscribes to bus messages, stages
them in the `sst_workspace_t`, and
dispatches the cycle's work. Phase B
runs the contradiction check and plan
generation; the plan may include an
action intent, which becomes a publish
on `org.seed.action.intend.motor`. The
cycle's outputs are typed SXL entities
published on the bus.

The cycle is assisted by the Lua brain
cycle in
`~/seed-dev/lua/agents/cognitive/brain.lua`,
which runs the higher-level orchestration
helpers (one per cognitive domain).

## 4. Drawbacks

- **Two-language substrate** — C and
  Lua. The C cycle is the trusted
  substrate; Lua is the orchestration
  layer. The seccomp allowlist
  boundaries the Lua agent host, not
  the C cycle. The split is a feature
  (deterministic core + flexible
  orchestration) but it adds a learning
  curve and a debug boundary.
- **Two-protocol bus** — the
  integration speaks SXL to the bus and
  JSON to the firmware. The
  `IntegrationBridge` in
  `~/robot-dev/src/neocortex/integration.py`
  translates between them. The
  translation is small but real, and
  must be kept in lockstep with both
  sides.
- **Off-robot neocortex** — Robot A's
  neocortex runs off-robot (home-PC
  Ollama in production, Pi 3 B+ in dev).
  The robot is safe with the neocortex
  offline (the on-device policy
  remains) but a full system requires
  the neocortex to be reachable.

## 5. Alternatives

- **Direct IPC instead of a bus.**
  Rejected: a topic-based bus is
  naturally multi-party, naturally
  recorded, and naturally
  multi-language. Direct IPC would
  couple the cognitive cycle to the
  firmware's transport and lock the
  integration to a single topology.
- **Single-language substrate**
  (everything in C, or everything in
  Lua). Rejected: the C substrate is
  the trust boundary; pure Lua would
  require the seccomp allowlist to
  cover the entire cognitive cycle,
  which is too coarse-grained. Pure
  C would force the orchestration
  helpers into a build cycle, which
  makes them harder to evolve.
- **Robot A with on-board Pi
  (Robot B design today).** Rejected
  for Robot A: the canonical Robot A
  is ESP32-only with the neocortex
  off-robot (per the sensor-head ADR
  0003). Robot B's design (ESP32 deep
  brain + on-board Pi SBC) is the
  planned evolution.

## 6. Open questions

- **The graduation path for sapling
  agents** — the criteria are in
  `~/solbian/documentation/engineering-manual/sapling/04-GRADUATION-PATH.md`,
  but the actual graduation of a
  specific agent has not happened
  yet. The first graduation will
  exercise the path end-to-end.
- **The T2 bus encryption** — T2 is
  encrypted, but the cipher and the
  key-rotation policy are TBD.
- **The seccomp aarch64 path** — the
  aarch64 seccomp allowlist is enabled
  in the codebase with compile guards
  and runtime success returns; the
  real aarch64 deployment is future
  work.
- **The robot B chassis** — the
  sensor-head ADR 0003 plans an
  on-board SBC and a heavier sensor
  head. The Robot B spec is
  forthcoming; the Robot A spec in
  `~/robot-dev/docs/hardware/sensor-head.md`
  is the current source of truth.

## 7. Glossary

- **S.E.E.D.** — the cognitive
  framework in `~/seed-dev/`. The
  "mind".
- **Sprout** — the physical robot in
  `~/robot-dev/`. The "body".
- **Sapling** — the agents and
  symbolic-operations level. The
  "nursery".
- **SXL** — SEED Expression Language.
  The canonical IR of all cognition
  in S.E.E.D. Self-describing
  S-expressions with ULID ids,
  nanosecond timestamps, confidence,
  and provenance.
- **T0 / T1 / T2** — the three bus
  tiers. Control, cognitive, data.
- **R1–R8** — the eight robot reflex
  rules. The minimum on-device safety
  surface.
- **ByteSource** — the transport-
  agnostic protocol between the
  neocortex and the firmware
  (`StdioSource`, `SerialSource`,
  `HTTPSource`).
- **IntegrationBridge** — the
  neocortex class that translates
  internal JSON to SXL on the bus.
- **FROZEN-2026-05-10** — the
  canonical topic namespace freeze
  date.
- **SREF** — the `.sref` file format
  used by the codex and the policies.

## 8. Cross-references

This spec is the narrative side. The
formal side is in
[`../machina/SPEC.md`](../machina/SPEC.md).
Both must agree.

The narrative from each sub-project's
view:

- `../../seed/INTEGRATION.md` —
  S.E.E.D.'s view.
- `../../sprout/INTEGRATION.md` —
  Sprout's view.
- `../../sapling/INTEGRATION.md` —
  Sapling's view.

The Engineering Manual's canonical
content:

- `~/solbian/documentation/engineering-manual/seed/`
  — 9 chapters covering infrastructure,
  substrate, daemons, bus, seccomp,
  persistence, deployment, build, and
  DRAFTS reconciliation.
- `~/solbian/documentation/engineering-manual/sprout/`
  — 9 chapters covering engines
  overview, daemons, model router,
  cognitive cycle, sensor head, safety
  policy, IO matrix, bus client, and
  integration tests.
- `~/solbian/documentation/engineering-manual/sapling/`
  — 6 chapters covering the agents
  overview, catalog, symbolic layer,
  agent integration, graduation path,
  and untrusted-agent safety model.

## 9. See also

- `README.md` — Codex Solbian's home
- `CHANGELOG.md` — release notes
- `../machina/SPEC.md` — the formal
  pair
- `../README.md` — the codex parent
  directory
- `../INTEGRATION.md` — how the two
  codexes fit together
- `../../docs/METHODOLOGY.md` —
  spec-first workflow
