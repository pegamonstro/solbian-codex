# Plan 9 to Solbian: Integration Blueprint

> **Status**: Draft v0.1.0
> **Date**: 2026-07-16
> **Scope**: Mapping Plan 9 from Bell Labs concepts onto the Solbian/seed-dev architecture
> **Canonical references**: all seed-dev source paths relative to `~/seed-dev/`

---

## Table of Contents

1. [The 9P Protocol Fit](#1-the-9p-protocol-fit)
2. [Everything as a File for Solbian](#2-everything-as-a-file-for-solbian)
3. [Per-Process Namespaces for Cognitive Agents](#3-per-process-namespaces-for-cognitive-agents)
4. [Distributed Cognition via 9P](#4-distributed-cognition-via-9p)
5. [Modern Implementation Strategy](#5-modern-implementation-strategy)
6. [Architectural Patterns to Adopt](#6-architectural-patterns-to-adopt)
7. [Specific NSLP/NSP Integration Points](#7-specific-nslp-nsp-integration-points)
8. [Concrete Architecture Proposal](#8-concrete-architecture-proposal)
9. [Risks and Challenges](#9-risks-and-challenges)
10. [Recommended Phased Adoption](#10-recommended-phased-adoption)

---

## 1. The 9P Protocol Fit

### 1.1 9P Protocol Overview

9P (also called "Plan 9 File Protocol" or "Styx" in its Inferno variant) is a
wire protocol with exactly 17 message types organized as T-messages (request)
and R-messages (response). Every interaction is a transaction: client sends a
T-message, server replies with an R-message. The protocol has no concept of
"connection initiator" vs. "server" in the traditional sense -- once a
connection is established, either side can send T-messages.

The 17 messages fall into these categories:

| Category | Messages | Purpose |
|----------|----------|---------|
| Setup | Tauth/Rauth, Tattach/Rattach | Authentication and namespace attachment |
| File ops | Twalk/Rwalk, Topen/Ropen, Tcreate/Rcreate | Navigating and opening resources |
| I/O | Tread/Rread, Twrite/Rwrite | Reading and writing data |
| Metadata | Tclunk/Rclunk, Tremove/Rremove, Tstat/Rstat, Twstat/Rwstat | Close, delete, stat |
| Session | Tversion/Rversion, Tflush/Rflush | Version negotiation, cancelling pending ops |

From `~/sys/src/9/port/9p.h` in the Plan 9 source tree (or equivalently
`/n/sources/plan9/sys/src/9/port/9p.h`).

### 1.2 Current Solbian Bus Protocol (T0/T1/T2)

The Solbian bus (`src/libbus/`) has three tiers sharing a common API shape:

**T0 -- In-process pub/sub** (`src/libbus/src/bus.c`):
- Synchronous fan-out: publish blocks until all matching subscriber callbacks
  have been invoked.
- Topic-based subscription with glob patterns (`*` for single segment,
  `**` for multi-segment).
- Bounded per-subscription queues, drop policies (newest, oldest, evict).
- Priorities (CRITICAL > INTERACTIVE > NORMAL > BULK).
- Metrics: 12 counter events for observability.
- Frame: raw `(topic, payload, qos, prio)` tuple passed as C function args.

**T1 -- UDS broker** (`src/libbus/src/t1.c`):
- Connects to `seedbusbrokerd` over Unix-domain socket at
  `/run/seed/bus.sock`.
- Asynchronous delivery: publish returns after enqueueing; frames delivered
  via `seed_bus_poll()` and decoded `SEED_BROKER_FRAME_EVENT` dispatch.
- Wire format: broker frame v1 (see `seed/broker_frame.h`): byte-level
  frame with kind, topic, priority, QoS, payload.
- Reconnect with bounded exponential backoff (100ms min, 5000ms max).
- Request/reply via `.reply` topic suffix with correlation header
  (`t1_req_hton`/`t1_req_ntoh`, 8-byte envelope).

**T2 -- Network bridge** (`src/libbus/src/t2.c`):
- Wraps `seed_net_session` (Noise-IK encrypted sessions via `seedneted`).
- Topic-grant prefix enforcement (`topic_grant_prefix` field).
- Bounded outbound ring buffer (default 32 slots).
- `seed_bus_t2_feed_wire` for inbound ciphertext from `seedneted`.
- Encrypted with libsodium `crypto_box` (Curve25519 + XSalsa20-Poly1305).

### 1.3 9P vs. Bus: Structural Comparison

| Dimension | 9P (Plan 9) | Solbian Bus (T0/T1/T2) |
|-----------|-------------|------------------------|
| **Primitives** | 17 fixed messages (Twalk, Tread, Twrite, Topen, Tstat, ...) | 5 operations (publish, subscribe, unsubscribe, request, serve) + 12 broker frame types |
| **Resource model** | Hierarchical file tree, each node is a file | Flat topic namespace `org.seed.<seg>(.<seg>){1,5}` |
| **Addressing** | Path-based `/srv/plumber`, `/net/tcp/23/data` | Topic-name based with pattern matching |
| **State** | Connection holds fid (file ID), iounit, per-fid position | Connection holds subscriptions, each with queue depth + drop policy |
| **Data model** | Typed files with QID (type, version, path) | Opaque byte payloads (SXL in practice) |
| **Authentication** | Factotum -- /mnt/factotum serves auth info | ACL roles (system/core/higher_order/observer/external) |
| **Concurrency** | Per-fid I/O position, multiple fids per connection | Priority-class drain, bounded queues |
| **Transport** | Any reliable byte stream (TCP, UDS, IL) | UDS (T1), Noise-IK encrypted session ch (T2), in-process (T0) |

### 1.4 Could 9P Serve as a Unifying Protocol Across All Three Bus Layers?

**Yes, with caveats.** The mapping is:

**9P Twalk (navigate) -> T0/T1 subscription pattern**: Walking from `/` to
`/cognitive/this-node/observations` via successive Twalk messages parallels
subscribing to `org.seed.cog.observation.*`. But 9P walking implies a
hierarchical namespace the client must traverse, while the bus uses flat
topic patterns with wildcards. These are semantically different: 9P gives
you a position in a tree; the bus gives you a filter that matches topics.

**9P Tread/Twrite (I/O) -> T0/T1 publish/request**: Writing to a file is
analogous to publishing to a topic. Reading from a file is analogous to
subscribing to receive messages. However, 9P Tread is pull-based (client
requests data), while bus subscribe is push-based (server delivers matching
messages). The 9P model is more like a filesystem where each read returns
the latest "contents"; the bus model is a message queue.

**9P Topen (open) -- middleware state**: Opening a file in 9P creates a fid,
which is the handle for subsequent reads/writes. This explicit state
creation has no direct parallel in the bus -- subscriptions fill this role,
but a subscription is a persistent interest, not a transient open.

**Where the bus dominates 9P**: The bus's topic pattern matching (`*`, `**`)
provides expressive subscription that 9P's hierarchical walk does not
directly support. A 9P file server *can* implement pattern matching in its
read response, but that is application-level, not protocol-level.

**Where 9P dominates the bus**: 9P's Tstat/Twstat provide rich metadata on
every resource. The bus has no equivalent -- topics have no metadata beyond
what the publisher puts in the payload. 9P's Tremove provides explicit
deletion of resources. The bus has no destroy/remove primitive.

### 1.5 Concrete Comparison: 9P Operations vs. Current Bus Operations

```
9P Operation            Solbian Bus Equivalent         Gap
─────────────────────   ─────────────────────────      ─────────────────
Tattach (mount)         seed_bus_open_t1(socket_path)  Similar -- establish conn
Twalk (walk to path)    seed_bus_subscribe(pattern)    Weaker -- no tree struct
Topen (open for IO)     seed_bus_serve(pattern, cb)    Rough match for servers
Tread (read N bytes)    seed_bus_request(topic, ...)   Pull vs push semantics
Twrite (write N bytes)  seed_bus_publish(topic, ...)   Direct match
Tclunk (close fid)      seed_bus_unsubscribe(sub)     Rough match
Tremove (remove file)   (no equivalent)                Missing -- no destroy
Tstat (file metadata)   (no equivalent)                Missing -- no stat
Twstat (write metadata) (no equivalent)                Missing -- no metadata update
Tcreate (create file)   (no equivalent)                Missing -- no resource creation
Tflush (cancel)         (no equivalent)                Missing -- no cancellation
```

The gaps are instructive. The bus is fundamentally a **publish/subscribe
messaging system**; 9P is fundamentally a **remote filesystem protocol**.
Pub/sub is topic-oriented and push-based; 9P is path-oriented and pull-based.

### 1.6 What Does 9P Give Solbian That the Current Bus Doesn't?

1.  **Uniform resource model**: Every service, daemon, agent, and data source
    presents the same interface (read, write, open, stat). No special-case
    RPCs. The cognitive cycle becomes a filesystem.

2.  **Positional I/O**: 9P's per-fid read/write position means a subscriber
    can maintain cursor state (read from where I left off), enabling reliable,
    at-least-once delivery across crashes. The bus's push model cannot do
    this without application-level tracking.

3.  **Metadata on everything**: Every 9P resource has a stat structure with
    type, version, length, name, uid, gid, muid, mode, and modification time.
    In Solbian, every bus message has no inherent metadata -- publishers
    must embed it in the SXL payload.

4.  **Cancellation**: 9P Tflush lets a client abort an outstanding request.
    The bus has no cancel -- once a publish is dispatched, it completes.
    For long-running cognitive operations (delegated inference, consensus),
    cancellation is valuable.

5.  **Filesystem namespaces** (covered in Section 3): The ability to give
    each agent a private view of the system composited from multiple
    filesystem trees is not achievable with the flat bus topic model.

### 1.7 What Does the Current Bus Do That 9P Doesn't Handle Well?

1.  **Topic pattern matching**: `org.seed.observation.sensor.*` subscribing
    to all sensor observations is a one-step operation. In 9P, a client
    would need to walk a directory tree and open each matching file, or the
    server would need to implement a subscription mechanism over 9P (which
    Inferno's styx does not have natively).

2.  **Prioritized delivery**: The bus supports `SEED_PRIORITY_CRITICAL >
    INTERACTIVE > NORMAL > BULK`. 9P has no priority field -- all messages
    are equal. A 9P server would need to implement priority scheduling
    internally (e.g., multiple fids with different access patterns).

3.  **Backpressure and drop policies**: The bus has bounded queues per
    subscription with configurable overflow behavior (DROP_NEWEST,
    DROP_OLDEST, EVICT_SUBSCRIBER). 9P simply blocks on Twrite when the
    receiver is not reading; the equivalent is a kernel-buffered write
    that can overflow system buffers.

4.  **Async delivery**: The bus T1 transport is fully asynchronous (publish
    returns before subscribers see the message). 9P is fundamentally
    synchronous -- each Tmessage gets an Rmessage before the next. Inferno
    added asynchronous I/O via `alt` statements on channels, but that is an
    application-level pattern, not protocol-level.

5.  **Request/reply correlation**: The bus T1 has request/reply with
    `seed_bus_serve()` and `seed_bus_request()`, using 8-byte correlation
    headers. 9P has no native request/reply pattern beyond the Tmessage/Rmessage
    transaction pair. A "request" in 9P is writing to a file and reading
    from a different file; correlation is the client's responsibility.

### 1.8 Recommendation: 9P as a Wrapper, Not a Replacement

Rather than replacing the bus with 9P, the architectural recommendation is
to **layer 9P on top of the bus** as a universal access protocol, analogous
to how Plan 9's `exportfs` exports a namespace over 9P:

```
   Clients (agents, cognitive procedures, Lua brains)
        │
        │  9P protocol
        ▼
   9P <-> Bus bridge daemon (new: seed9pd)
        │
        │  libbus API (publish/subscribe/request)
        ▼
   Solbian bus (T0/T1/T2)
        │
        ├── seedcogd (cognitive cycle)
        ├── seedreasond (policy evaluation)
        ├── seedneted (network sessions)
        └── ...other daemons
```

This bridge daemon would:

- Export every bus topic as a 9P file (e.g., `org.seed.cog.observation` ->
  `/cognitive/observation`)
- Expose subscription patterns as directories the client can walk
- Provide stat metadata for every exported resource
- Translate between 9P Twrite and bus publish
- Translate between 9P Tread and bus subscription (with cursor tracking)

---

## 2. Everything as a File for Solbian

### 2.1 The Paradigm Shift

Plan 9's "everything is a file" means that every resource -- hardware,
network connection, service, authentication credential, process, kernel
data structure -- is accessed through the same filesystem operations:
read, write, open, stat, close. There are no ioctls, no special system
calls, no device-specific APIs.

For Solbian, "everything is a file" means:

- Cognitive state (beliefs, goals, plans, memories) is a synthetic filesystem
- Inference backends are files you write prompts to and read responses from
- Bus topics are directories containing message files
- Daemons are file servers
- Agents/processes are entries in `/proc`
- Network connections are files in `/net`

### 2.2 Synthetic Filesystem for Cognitive State

The central cognitive state filesystem would live at a well-known mount
point, say `/cognitive`:

```
/cognitive/
  beliefs/                -- belief store (currently libsmem partitions)
    active/               -- beliefs with status=active
      b-001               -- a single belief, readable as SXL
      b-002
    retracted/            -- beliefs with status=retracted
    schema                -- read: returns the belief SXL schema
    add                   -- write: create a new belief (9P Tcreate + Twrite)
    query                 -- write: pattern SXL, read: results

  goals/                  -- goal store
    active/
    completed/
    failed/
    add
    decompose             -- write: goal SXL, read: sub-goals

  plans/                  -- plan store
    current/
    history/
    schema

  memories/               -- episodic memory (libsmem partitions)
    recent/               -- last N memories
    search                -- write: query, read: results
    consolidate           -- write: trigger consolidation (Phase C)
    stats                 -- read: memory utilization, entry counts

  observations/           -- raw and processed observations
    sensor/               -- sensor data by type
    cognitive/            -- internally-generated observations
  /cognitive/this-node/
    observations/
    beliefs/
    knowledge/
    continuation/         -- suspended workflow continuations
    predictions/
    evaluations/
    self-model/           -- homeostasis metrics
      cognitive-load
      memory-pressure
      planning-quality
      error-history
      prediction-accuracy
      attention-saturation
```

Compare to the current partition model in `src/libsmem/src/sxl.c` and
`src/seedcogd/main.c`: memory is organized as SQLite-backed partitions
with names like `cognitive/this-node/observation`. The filesystem view
is a natural projection of the existing partition hierarchy.

File `src/libsmem/include/seed/smem.h:659-799` defines `seed_smem_entry_v_t`
with fields: `entry_id`, `parent_id`, `entity_type`, `status`, `confidence`,
`cycle`, `source`, `provenance`, `timestamp`, `content_sxl`, `ttl`, `version`,
`relations`. These map directly to stat fields on a 9P file:

```
9P stat field         seed_smem_entry_v_t field
──────────────────    ─────────────────────────
name                  entry_id
length                content_sxl length
type                  entity_type (mapped to QID type)
uid                   source
mtime                 timestamp
mode                  status -> permission bits (active=0644, abandoned=0000)
```

### 2.3 Inference Backends as Files

Currently, inference goes through `src/libseedllm/src/dispatch.c:47-71` which
classifies intent and routes to one of 5 backends (ollama, native, openai, sst,
uds). As files:

```
/cognitive/inference/
  backends/
    ollama/
      stats             -- read: backend health, model, queue depth
      prompt            -- write: prompt SXL, read: response SXL
      stream            -- write: prompt, read: streaming response
      config            -- read/write: backend parameters (temperature, etc.)
    native/
      stats
      prompt
      stream
      config
    sst/                 -- symbolic backend
      stats
      eval              -- write: SXL expression, read: evaluation result
    consensus/           -- multi-model consensus
      config            -- read/write: consensus parameters
      request           -- write: prompt SXL, read: consensus result
      status            -- read: current consensus health
  dispatch/              -- intent-based dispatch
    classify            -- write: task SXL, read: backend assignment
    stats               -- read: dispatch metrics, per-backend load
```

The current dispatch in `src/libseedllm/src/dispatch.c` uses a
`seed_llm_dispatch_config_t` that maps intents to backends. In a filesystem
model, this becomes a set of symlinks:

```
/cognitive/inference/dispatch/reflection -> ../backends/ollama
/cognitive/inference/dispatch/reasoning -> ../backends/ollama
/cognitive/inference/dispatch/symbolic  -> ../backends/sst
```

Changing dispatch is as simple as rewriting a symlink -- no config file
editing, no daemon restart.

### 2.4 Bus Topics as Directories

Each bus topic becomes a directory containing message files. The bus
pattern `org.seed.cog.observation.sensor` maps to:

```
/bus/org/seed/cog/observation/sensor/
  messages/
    001               -- timestamp-based message file
    002
    ...
  schema              -- read: topic payload schema
  stats               -- read: topic metrics (pub count, sub count, bytes)
  subscribe           -- write: create subscription, read: subscription ID
  latest              -- read: most recent message
  stream              -- read: blocking read, returns next message
```

This is directly analogous to how Plan 9 represents network connections:

```
/net/tcp/
  23/
    data              -- read/write: raw TCP data
    status            -- read: connection state
    listen            -- write: accept incoming connections
    local             -- read: local address
    remote            -- read: remote address
```

From Plan 9 `~/sys/src/9/port/devip.c` (IP device) and `~/sys/src/9/port/devether.c`.

### 2.5 Daemons as File Servers

Every Solbian daemon currently has C entry points, bus topics it
publishes/subscribes to, and in many cases a control interface. As a file
server, each daemon exports its namespace:

```
/daemons/
  seedcogd/            -- cognitive daemon
    control            -- write: commands (pause, resume, reload, cycle N)
    status             -- read: current cycle, phase, load
    cycle/             -- per-cycle information
      current/
        phase          -- read: current phase name
        entries        -- read: entries this cycle
        llm-calls      -- read: LLM call count
      last/
  seedreasond/         -- policy daemon
    evaluate           -- write: action SXL, read: policy decision
    policies/          -- policy namespace
      safety/
        R1 .. R8
      cognitive/
  seedneted/           -- networking daemon
    sessions/
    capabilities/      -- node capabilities (D3)
  seedsysresd/         -- system resources
    cpu
    memory
    disk
  seedbusbrokerd/      -- bus broker
    status
    clients
```

### 2.6 Processes/Agents as Files in /proc

Plan 9's `/proc` filesystem (from `~/sys/src/9/port/devproc.c`) exposes each
process as a directory with files like `ctl`, `note`, `mem`, `regs`, `status`,
`text`, `wait`.

For Solbian, cognitive agents and NSL processes would appear in `/cognitive/proc/`:

```
/cognitive/proc/
  wf-001/             -- workflow instance
    status            -- read: idle|running|suspended|completed|failed
    ctl               -- write: suspend|resume|kill|step
    graph             -- read: primitive graph (DAG of nsop_t nodes)
    state             -- read/write: current cognitive state (SXL)
    trace             -- read: execution trace
    continuations/    -- suspended continuation points
  a-002/              -- cognitive agent
    status
    ctl
    namespace/        -- the agent's private namespace (see Section 3)
```

### 2.7 Mapping to libsmem Partitioned Memory Model

The existing libsmem partition model uses a 2D addressing scheme
(scope/reach/name) from `src/libsmem/`:

- `cognitive/this-node/observations` -- local observations
- `cognitive/global/workflows` -- shared workflow definitions
- `cognitive/sprout/hypotheses` -- sprout subsystem hypotheses

The filesystem view is a direct 1:1 mapping of partition paths to directory
paths. The 9P server for cognitive state would:

1. Walk from root to the partition by successive Twalk messages.
2. Translate Topen on a partition to a scan operation on that partition.
3. Translate Topen on a specific SXL entry to a retrieval by ID.
4. Translate Tcreate + Twrite to create a new entry in that partition.

The key architectural difference:

- **Current model**: libsmem partitions are accessed via C API:
  `seed_smem_sxl_scan(memory_root_dir, sxl_type, callback, user_data, limit)`
  (`src/libsmem/src/sxl.c:25-54`)
- **9P model**: Partitions are accessed via filesystem operations:
  `open("/cognitive/this-node/observations") / read(fd, buf, n)`

The libsmem API becomes the implementation behind the 9P server, not the
public API for cognitive agents.

### 2.8 Practical Migration

**Changes gradually (layer-by-layer)**:

1. **Add a 9P server bridge** (`seed9pd`) that wraps libsmem partitions
   behind a 9P filesystem. Agents can choose to use either the old C API
   or the new filesystem API. This is an additive change -- no existing
   code breaks.

2. **Export inference backends as files**: Create `seed9pd` handlers for
   `/cognitive/inference/prompt` that wrap `seed_llm_chat()` from
   `src/libseedllm/`. Agents that write to this file get LLM responses
   back. The existing `dispatch.c` routing becomes filesystem structure.

3. **Export daemon control as files**: Each daemon adds a 9P export server
   (or uses `seed9pd` with in-process handlers) to expose its control
   interface at `/daemons/<name>/`.

**What requires an architectural shift**:

1. **Namespace-per-agent**: Giving each agent a private filesystem view
   (Section 3) requires that the mount point for `/cognitive` be per-process.
   This means either (a) each agent process runs its own 9P connection with
   a private namespace, or (b) the bridge daemon handles namespace
   composition server-side. Both are significant changes to the current
   shared-bus model.

2. **Replacing bus subscriptions with watch-on-files**: The current bus
   subscription model uses push delivery. Converting to a pull model
   (agent polls a file for new messages) requires rewiring notification
   patterns throughout the cognitive cycle.

---

## 3. Per-Process Namespaces for Cognitive Agents

### 3.1 Plan 9 Namespace Model

In Plan 9, each process has a **private namespace** -- its own view of the
filesystem tree. Namespaces are constructed by mounting filesystem servers
onto mount points. A process can mount any number of servers, and the same
server can be mounted at multiple points. Union mounts allow multiple
filesystems to be overlaid at the same point, with the leftmost mount
winning on lookup.

Key mechanisms:

```
# Bind /usr/glenda to /tmp/work (private overlay)
bind /usr/glenda /tmp/work

# Mount network filesystem at /net
mount -c /srv/net /net

# Union mount: /bin is /bin + /usr/glenda/bin
bind -a /usr/glenda/bin /bin

# Private mount: only this process (and its children) see it
mount -p /srv/cognitive /cognitive
```

From Plan 9 `~/sys/src/libc/port/bind.c` and the `rfork` documentation
(`rfork(RFNAMEG)` creates a new namespace group).

### 3.2 Cognitive Agent Namespaces in Solbian

Each cognitive agent (Lua brain, NSL procedure, SST operator invocation)
could get its **own namespace**. The agent's view of the cognitive state
filesystem is a composition of:

1. **Shared cognitive partitions** -- read-only, mounted from the global
   cognitive filesystem server.
2. **Agent-private partitions** -- read-write, stored in the agent's
   isolated scratch directory.
3. **Tool overlays** -- filesystem-based adapters for tools the agent
   can invoke.

Example namespace construction for an NSL procedure:

```
# Agent "wf-reflection-v1" namespace:
mount -c /srv/cognitive /cognitive                    # base cognitive FS
mount -b /usr/agents/wf-reflection-v1/scratch /cognitive/scratch
mount -b /srv/inference/ollama /cognitive/inference    # inference backend
# Override perceptions -- only see what this agent is configured to see
bind /cognitive/observations/sensor/camera /cognitive/observations
# Private working memory
mount /srv/mem/agent-wf-reflection-v1 /cognitive/working-memory

# Result: the agent sees:
# /cognitive/beliefs/...        (shared, read-only)
# /cognitive/observations/...   (only camera sensor)
# /cognitive/working-memory/... (private)
# /cognitive/inference/...      (inference backend files)
# /cognitive/scratch/...        (agent's private storage)
```

### 3.3 Union Mounts for Agent Perspective-Taking

A powerful application: agents can adopt different perspectives by mounting
different cognitive state overlays.

**Example: Agent analyzing a situation from a skeptic perspective**:

```
# Base: shared cognitive state
mount -c /srv/cognitive /cognitive

# Skeptic overlay: lower confidence threshold, highlight contradictions
mount /srv/overlay/skeptic /cognitive/beliefs
#   This overlay transforms reads:
#   - Every belief's confidence is halved
#   - Contradictions are annotated with "unreconciled" flag
#   - Write operations are logged separately
```

**Example: Agent simulating a counterfactual**:

```
# Clone the current cognitive state
mount -c /srv/cognitive /cognitive

# Apply the counterfactual: "what if goal X was completed?"
bind /srv/scenarios/completed-goal-X /cognitive/goals

# Now the agent runs an NSL procedure against this modified state
# All reads see the counterfactual goals; all writes go to a private log
```

**Example: Hierarchical agent delegation**:

```
# Supervisor agent gives a subordinate agent a constrained view:
mount -c /srv/cognitive /cognitive
bind -b /cognitive/beliefs /cognitive/beliefs         # read-only beliefs
bind /srv/scratch/subagent-001 /cognitive/scratch      # private scratch
bind /cognitive/inference/dispatch/summarize /cognitive/inference/dispatch
# Subordinate can only do summarization -- no full reasoning
```

### 3.4 Comparison: Plan 9 Namespace vs. NSL Binding Environment vs. SXL Memory Partitions

| Aspect | Plan 9 Namespace | NSL Binding Env | SXL Memory Partitions |
|--------|-----------------|-----------------|-----------------------|
| **Unit** | Mount points + union dirs | Symbol -> Value pairs | (scope/reach/name) triples |
| **Creation** | `mount`, `bind`, `rfork(RFNAMEG)` | `(bind :a id :b id ...)` | libsmem API: `seed_smem_log_create()` |
| **Lookup** | Path walk (leftmost wins in union) | `(resolve :symbol :env)` -> Value | `seed_smem_sxl_scan()` with filter |
| **Isolation** | Per-process (private namespace) | Per-procedure (fresh env) | Per-ACL-role (partition ACL) |
| **Composition** | Union mounts, bind mounts | Nested environments (shadowing) | Partition hierarchy (prefix matching) |
| **Override** | Bind over mount (shadows lower) | Bind shadows outer binding | Write to same key shadows old entry |
| **Inheritance** | Child inherits parent's namespace | Nested scope (lexical) | Shared partitions (global visibility) |
| **Dynamic** | Mount/unmount at runtime | Runtime extend with bind | Partition creation at runtime |

The NSL binding environment (`(bind :symbol :value :env) -> Env` from the
NSL ISA in SPEC.md Group III) is closest to a namespace concept at the
symbolic level. Variables in NSL are resolved in nested environments,
analogous to union-directory resolution in Plan 9. The SXL partition model
is more like a global filesystem -- all agents share the same hierarchy, with
ACL control at the partition level.

**The key insight**: Plan 9's per-process namespace gives you **private,
composable, dynamic views** over a shared underlying store. NSL bindings
give you the same thing for symbolic computation but not for I/O,
communication, or resource access. Bridging these two -- giving NSL
procedures access to Plan 9-style process namespaces -- would unify the
symbolic and systems-level isolation models.

### 3.5 Implementation: NSL Namespace Primitives

New NSL primitives for namespace manipulation:

```
ns-bind   : Path × Path × Flags → Nil     [write/write]
   Bind path-b to path-a. When flags=bind-before, path-a shadows path-b.
   When flags=bind-after, path-b shadows path-a.
   Maps to Plan 9 bind(2).

ns-mount  : Path × Path × Spec → Nil     [write/write]
   Mount the filesystem server at srv-path onto mount-point.
   Maps to Plan 9 mount(2).

ns-fork   : Nil → Namespace              [alloc]
   Create a new namespace inherited from current process.
   Maps to rfork(RFNAMEG).

ns-unmount: Path → Nil                    [write]
   Unmount a filesystem at the given point.
   Maps to Plan 9 unmount(2).
```

These give NSL procedures first-class control over their resource view.

---

## 4. Distributed Cognition via 9P

### 4.1 Plan 9 CPU Server Model

Plan 9's `cpu` command connects a client to a remote CPU server:

```
cpu -h server.address
```

This creates a local namespace that includes `/mnt/term` (the terminal's
filesystem) and the remote server's `/dev`, `/proc`, `/net`, etc. The
client process runs remotely but has transparent access to local files
(through `/mnt/term`).

Key insight: **The remote machine mounts your filesystem, not the other way
around.** When you run `cpu`, your local files are mounted on the remote
machine as `/mnt/term`. Your keyboard, mouse, and screen stay local; CPU
and memory are remote.

From Plan 9 `~/sys/src/cmd/cpu.c` and `/sys/src/9/cpu/port/devcputerm.c`.

### 4.2 From CPU Server to Distributed Cognitive Work

Instead of the current D1-D5 delegation model (`src/seedcogd/delegate.h`),
nodes would export their cognitive state as 9P filesystems and mount each
other's cognitive state:

```
Node A: seedcogd exports /cognitive at /srv/cognitive-a via 9P
Node B: mount -c /srv/cognitive-a /cognitive/peers/node-a

# After mounting, Node B sees:
# /cognitive/peers/node-a/beliefs/
# /cognitive/peers/node-a/observations/
# /cognitive/peers/node-a/inference/
# ...  (Node A's full cognitive state)
```

**Current D5 delegation** (`src/seedcogd/delegate.h:41-50`):
- 7 phases are delegatable via fire-and-forget publish + separate result
  subscription
- Load-based decision: `seed_cog_delegate_should_delegate()` checks
  `avg_llm_ms`, `cycle_time_sec`, `queue_depth`
- Phases are sent as SXL payloads over the bus

**9P-based delegation**:
- Node B reads Node A's `beliefs/` directory, sees what Node A already knows
- Node B writes to Node A's `/cognitive/inference/ollama/prompt` to run
  inference remotely
- No explicit delegation protocol -- it's just filesystem I/O
- Node A can restrict access (read-only partition, restricted directory) via
  file permissions

### 4.3 D1-D5 as 9P-Exported Filesystems

Each level of the distributed cognition stack maps to a 9P export:

**D1 -- T2 Sessions**: `seedneted` (`src/seedneted/`) establishes encrypted
sessions. In a 9P model, `seedneted` becomes a filesystem server that
exports session endpoints as directories in `/net/sessions/`:

```
/net/sessions/
  <session-id>/
    data               -- read/write: raw session bytes
    status             -- read: session state, encryption params
    peer               -- read: peer identity DID
    channel/           -- T2 channel multiplexing
      ch-1/            -- topic-grant-prefix scoped channel
        write          -- write: outbound ciphertext
        read           -- read: inbound ciphertext
        stats          -- read: channel metrics
```

**D2 -- Cross-node Entry Sync**: Current: entries published on
`org.seed.cognition.entry` (line 1164-1184 of `main.c`). In a 9P model,
each node's `/cognitive/` is exported. Nodes that want to sync mount
each other's `/cognitive/` and use union mounts:

```
# Node A mounts Node B's cognitive state
mount -c /net/sessions/session-b/cognitive /cognitive/peers/b

# Union mount: Node A's beliefs + Node B's beliefs, with A winning
bind -a /cognitive/peers/b/beliefs /cognitive/beliefs
```

This replaces the explicit publish/subscribe sync protocol with filesystem
operations. The kernel cache coherency (stat version numbers) handles
conflict detection.

**D3 -- Capability Advertisement**: Current:
`seed_cog_capability_announce()` publishes SXL to
`org.seed.cognition.capability` (`src/seedcogd/capability.h:158`). In a
9P model, the capability registry becomes a file in each node's export:

```
/daemons/seedcogd/capabilities    -- read: node's self-capabilities
/daemons/seedcogd/peers/          -- read: discovered peer capabilities

# Reading /capabilities returns:
# (:capabilities :backends ((:name ollama :model qwen2.5-coder:7b :active 1))
#  :domains ((:reflection full) (:reasoning full) (:planning partial))
#  :resources (:cpu_cores 4 :ram_total "8GB"))
```

**D4 -- KG Bloom Filter Sync**: Current
(`src/seedcogd/kg_sync.h`, 175 lines, 1024-byte bloom, 4 hash functions). In
a 9P model, the bloom filter is a file:

```
/daemons/seedcogd/kg-bloom          -- read: local bloom filter bytes
/cognitive/peers/<peer>/kg-bloom    -- read: peer's bloom filter bytes
```

Sync is: read both files, compare, request missing entries by walking the
peer's partition directories.

**D5 -- Workload Delegation**: Current (`src/seedcogd/delegate.c`):
phase-specific delegation with deadlines, pending tracking, and result
matching. In a 9P model, delegation is mounting a remote inference directory:

```
# Delegate reflection to Node B:
mount -c /net/sessions/session-b/inference /cognitive/delegated-inference
# Write prompt:
echo "(:reflect :depth 2)" > /cognitive/delegated-inference/ollama/prompt
# ... wait for Node B to process (inference file now has response)
# Read result:
cat /cognitive/delegated-inference/ollama/prompt
```

No delegation code required beyond filesystem I/O. The remote 9P server
handles scheduling the inference, and the stat version number on the prompt
file tells the client when a new result is available.

### 4.4 Import/Export of Cognitive Resources

The key operations become:

```
# Export: seedcogd running on each node exports /cognitive internally
# Export control: which partitions are shared, with what permissions
chmod 644 /cognitive/beliefs           # readable by all
chmod 600 /cognitive/private-scratch   # readable only by owner

# Import: mount a remote node's export
mount -c /srv/seed9p-peer-b /cognitive/peers/node-b

# Selective import: only import observations
mount -c /srv/seed9p-peer-b/observations /cognitive/observations-peer-b

# Bidirectional: mount part of local state on remote
# (This happens automatically via cpu-style /mnt/term)
# Remote node sees:
# /mnt/term/cognitive/beliefs  (from local node)
```

### 4.5 Authentication Implications: Factotum for Cognitive Operations

Plan 9's `factotum` (`/mnt/factotum`) is a per-process authentication server.
Applications read/write auth protocol messages to its filesystem at
`/mnt/factotum/auth`. There is no `su`, no `sudo`, no Unix-style setuid --
all identity is handled through factotum's key store.

For Solbian, a `seedfactotum` daemon would:

- Store private keys for the node's DID (`did:seed:nodeA`)
- Store ACL credentials for cognitive operations
- Respond to auth challenges when nodes mount each other's cognitive exports
- Expose its own filesystem at `/mnt/factotum`:

```
/mnt/factotum/
  ctl            -- write: sign, decrypt, authenticate operations
  auth           -- write/read: 9P auth protocol messages
  key            -- read/write: key management (protected by factotum itself)
  whoami         -- read: current identity
  capabilities   -- read: what this process can do (derived from ACL)
```

The current ACL system (`seed-dev/codex/machina/policies/acl/agent_acl.sref`)
with 5 roles (system, core, higher_order, observer, external) would map to
factotum keys:

```
# An agent with `external` role trying to write to /cognitive/beliefs:
# factotum provides the agent's credential
# The 9P server checks: does credential have write permission?
# No -> EPERM (Plan 9 equivalent: "permission denied")
```

---

## 5. Modern Implementation Strategy

### 5.1 Existing Open-Source 9P Implementations

**plan9port (lib9p)**
- Location: `https://github.com/9fans/plan9port` -- `src/lib9p/`
- Language: C (Plan 9's libc + ANSI C compatibility layer)
- Provides: `lib9p` (server library), `lib9pclient` (client library)
- Includes: `9p1` wire format, `9p2000` (Plan 9's standard), `9p2000.u` (Unix extensions: uid/gid as integers, symlinks, hard links)
- Assessment: Mature, battle-tested. However, plan9port is a large dependency
  (~12MB) and brings POSIX-aping semantics. The server library is well-designed
  -- you implement a `Srv` struct with handler callbacks.
- File paths in plan9port: `src/lib9p/srv.c`, `src/lib9p/fs.c`,
  `src/lib9p/rpc.c`, `include/lib9p.h`

**v9fs (Linux kernel)**
- Location: `~/kernel/fs/9p/` in the Linux kernel tree
- Language: C (kernel module)
- Provides: Kernel-level 9P client (mount a 9P export as a filesystem)
- Protocol: 9P2000.L (Linux extensions: inode numbers, open flags, link/unlink)
- Assessment: Not appropriate for userspace Solbian integration. However,
  if Solbian runs on Linux, agents could mount 9P exports via v9fs and
  access cognitive state via standard POSIX I/O. This would be a deployment
  optimization, not a development strategy.

**Go 9P Libraries**
- `github.com/fhs/mux9p` (Fermin Hernandez's fork, maintained): Full 9P2000
  server + client in Go. Used by `go-plan9` and `draw9p`.
- `github.com/davecheney/9p`: Lightweight Go 9P implementation. Less
  maintained but simpler.
- `github.com/hugelgupf/p9`: 9P2000.L implementation in Go with Linux virtio
  transport support. Focus on gVisor integration.
- Assessment: Go would be an excellent language for a `seed9pd` bridge daemon,
  given Solbian's existing C stack. However, introducing Go as a new language
  adds build complexity. If Solbian can accept Go as a build dependency,
  `mux9p` is the best maintained option.

**Lua 9P**:
- No production-quality Lua 9P library exists. This is a gap that would
  need filling if Lua agents are to use 9P natively.

### 5.2 Minimal Viable 9P Integration for Solbian

The minimum integration has three components:

**Component 1: A lightweight 9P wire library in C**
- Implement just enough of the 9P2000 protocol to handle the 7 core
  message types: Tversion, Tauth, Tattach, Twalk, Topen, Tread, Twrite.
  (Tclunk, Tstat, Twstat, Tremove, Tflush, Tcreate are nice-to-have.)
- Wire format: 4-byte size + 1-byte type + 2-byte tag + message-specific fields.
- Buffer management: reuse the existing `seed_buf_t` from `src/libbus/`
  (`bus_internal.h`).
- Reuse `seed_err_t` error handling, `seed_time_mono_ns()` for timeouts.
- Target: ~500 lines over 3 files: `src/lib9p/9p.h`, `src/lib9p/fcall.c`,
  `src/lib9p/srv.c`.

**Component 2: A bridge daemon `seed9pd`**
- Connects to the existing bus via libbus T1.
- Exports bus topics and memory partitions as a 9P filesystem.
- Uses the minimal 9P library from Component 1.
- Handles 0-1 simultaneous client connections initially (single-threaded
  event loop, reusing `seed_bus_poll()` style).
- Configuration: which partitions to export, at what path prefix, with what
  permissions.
- Target: ~800 lines in `src/seed9pd/main.c`.

**Component 3: A 9P client wrapper in libbus**
- Public API: `seed_bus_open_9p(socket_path)` returns a `seed_bus_t *`,
  like `seed_bus_open_t1()`.
- Internally: opens a 9P connection, does Tversion/Tattach, then maps
  bus publish/Twrite and subscribe/Twalk+Open+Read.
- This lets existing bus code transparently access 9P resources.
- Target: ~400 lines, extending `src/libbus/`.

### 5.3 Phased Implementation Plan

#### Phase 1: Scaffolding (weeks 1-2)

| Task | Files | Description |
|------|-------|-------------|
| C 9P wire library | `src/lib9p/9p.h`, `src/lib9p/fcall.c`, `src/lib9p/srv.c` | Encoder/decoder for 9P2000 messages, server skeleton |
| Test harness | `tests/test_lib9p.c` | Round-trip encode/decode for all 17 message types |
| Plan 9 documentation | `docs/plan9/9p-protocol.md` | Wire format reference, message types, key terms |

**Deliverable**: A C library that can encode and decode 9P messages,
with a server skeleton that accepts connections and dispatches to handler
callbacks.

**Build integration**: Add `src/lib9p/` to `CMakeLists.txt` with
`-DBUILD_LIB9P=ON` flag (default OFF -- additive, no effect on existing build).

#### Phase 2: Export bus topics as files (weeks 3-4)

| Task | Files | Description |
|------|-------|-------------|
| seed9pd server | `src/seed9pd/main.c`, `src/seed9pd/export.c` | Bridge daemon: 9P server that connects to bus |
| Topic-to-file mapping | `src/seed9pd/export.c` | Each bus topic prefix becomes a 9P directory tree |
| Subscribe-as-open | `src/seed9pd/subscription.c` | Opening a topic file subscribes; reading returns messages |
| Stat-based metadata | `src/seed9pd/stat.c` | Map bus topic metadata to 9P stat fields |

**Deliverable**: A running `seed9pd` that exports
`org.seed.cog.observation.*` as `/cognitive/observations/` such that a
9P client can walk the directory, open a topic file, and read messages.

#### Phase 3: Export memory partitions (weeks 5-6)

| Task | Files | Description |
|------|-------|-------------|
| Partition-to-directory | `src/seed9pd/memory.c` | Walk libsmem partition hierarchy as 9P directories |
| Entry-to-file | `src/seed9pd/memory.c` | Each SXL entry becomes a readable file |
| Query files | `src/seed9pd/memory.c` | Write a query to a special file, read results |
| Write/create | `src/seed9pd/memory.c` | Write to create/update entries in partitions |

**Deliverable**: Agents can read/write cognitive state by reading/writing
files in `/cognitive/` via 9P.

#### Phase 4: Namespace support (weeks 7-8)

| Task | Files | Description |
|------|-------|-------------|
| Per-connection namespace | `src/seed9pd/namespace.c` | Each 9P connection gets a private namespace root |
| Bind/mount operations | `src/seed9pd/namespace.c` | Support bind and mount within the private namespace |
| Union directory listing | `src/seed9pd/namespace.c` | Merge directory entries from union-mounted directories |
| NSL namespace primitives | `src/lib9p/ns-bind.c`, `src/lib9p/ns-mount.c` | C functions callable from NSP runtime |

**Deliverable**: Each agent connected to `seed9pd` has a private namespace.
The system supports `bind`, `mount`, and union semantics.

---

## 6. Architectural Patterns to Adopt

### 6.1 The Mount Table Pattern

**Plan 9**: The mount table (`/proc/$pid/ns`) maps mount points to mounted
file servers. Each process has its own mount table. Mounting is a privilege
controlled by the owning process -- you can mount over your own paths.

**Solbian adoption**: Replace hard-coded partition paths with a mount table
for cognitive state. Currently, partition paths like
`cognitive/this-node/observations` are compiled into `seedcogd/main.c` as
string constants. With a mount table, the path is resolved dynamically:

```c
// Current (hard-coded):
seed_smem_sxl_scan("cognitive/this-node/observations", ...);

// With mount table:
seed_smem_sxl_scan("/mem/observations/this-node", ...);
// ... which resolves through the process's mount table to:
//   /mem/observations/this-node -> /cognitive/observations (shared)
```

**Changes needed**:
- `src/libsmem/` -- add mount table lookup before partition access
- `src/seedcogd/main.c` -- replace hard-coded partition paths with mount
  table keys
- New: `src/libsmem/src/mount.c` -- mount table implementation (~200 lines)

### 6.2 The /srv Pattern: Service Registry

**Plan 9**: `/srv` is a directory (conventionally on `srvfs`) that contains
named file descriptors. A daemon posts a file in `/srv` (e.g.,
`/srv/cognitive`). Clients mount that file to access the daemon's exported
namespace:

```sh
# Server posts its service:
srvfs /srv/cognitive

# Client mounts the service:
mount /srv/cognitive /cognitive
```

From Plan 9 `/sys/src/9/port/devsrv.c`.

**Solbian adoption**: Replace the current daemon discovery mechanism (bus
topic `org.seed.cognition.capability` from `capability.h`) with a `/srv`-style
service directory:

```
/srv/
  seedcogd/            -- cognitive daemon
  seedreasond/         -- policy daemon
  seedneted/           -- network daemon
  seedbusbrokerd/      -- bus broker
  process-table/       -- NSL process registry
  inference/           -- LLM inference backends
```

**Changes needed**:
- New daemon: `seedsrvd` -- manages the `/srv` directory, accepts `post`
  and `mount` operations
- `src/seedcogd/main.c` -- post `/srv/seedcogd` at startup instead of
  (or in addition to) publishing capability announcements
- `delegate.c` -- mount peer's `/srv/seedcogd` to discover capabilities
  instead of parsing bus topic announcements

### 6.3 The /net Pattern: Network as Filesystem

**Plan 9**: `/net` contains directories for each network protocol:

```
/net/
  tcp/
    clone               -- write to create new TCP connection
    23/                 -- connection #23
      data              -- read/write: TCP data stream
      status            -- read: connection state
      ctl               -- write: control messages (hangup, etc.)
      local             -- read: local address:port
      remote            -- read: remote address:port
  udp/
    clone
    ...
```

From Plan 9 `~/sys/src/9/port/devip.c`.

**Solbian adoption**: The T2 network layer (`src/libbus/src/t2.c`,
`src/seedneted/`) currently hides connections behind `seed_net_session_t`
opaque handles. A `/net` filesystem would expose:

```
/net/
  t2/
    clone               -- write: create encrypted T2 session to peer
    sessions/
      <session-id>/
        data            -- read/write: raw channel bytes
        status          -- read: encryption state, nonce counters
        ctl             -- write: close, rekey, adjust QoS
        wire            -- read: captured wire frames (for debugging)
        channels/       -- T2 bus channels
          1/
            data        -- read/write: channel payloads
            stats       -- read: channel metrics
  did/                  -- DID-based addressing (seed-specific)
    resolve             -- write: DID string, read: endpoint + public key
    peers/              -- known peers (from D3 capability advertisement)
      node-a
        did             -- read: DID string
        endpoint        -- read: address
        pubkey          -- read: Ed25519 public key
```

### 6.4 Synthetic Filesystems as API Boundaries

**Plan 9**: Every device driver, service, and kernel facility presents as a
synthetic filesystem. Examples: `/proc` (process info), `/dev` (hardware),
`/net` (network), `/srv` (services), `/mnt/factotum` (authentication),
`/mnt/plumb` (inter-process messaging).

**Solbian adoption**: Every Solbian component that currently has a C API
should have a corresponding synthetic filesystem exported via 9P:

| Component | Current API | Synthetic FS Path |
|-----------|-------------|-------------------|
| libsmem | `seed_smem_sxl_scan()`, `seed_smem_entry_put()` | `/cognitive/` |
| libseedllm | `seed_llm_chat()`, `seed_llm_pool_dispatch()` | `/cognitive/inference/` |
| seedreasond | `seed_policy_eval()` | `/daemons/seedreasond/evaluate` |
| seedcogd | `cognitive_tick()`, `dsxl()` | `/daemons/seedcogd/` |
| libsexpr | `sxp_oper_compare()`, `sxp_confidence_propagate()` | `/cognitive/operators/` |

The synthetic filesystem becomes the **northbound API**. The C API becomes
the **southbound implementation**.

### 6.5 File Server as the Fundamental Service Abstraction

**Plan 9**: A "service" is a process that implements the 9P protocol and
posts a file in `/srv`. Every daemon, driver, and server is a file server.
There is no distinction between "local" and "remote" services -- a mount
is a mount regardless of whether the server is in-process, on the same
machine via UDS, or across the network via TCP.

**Solbian adoption**: Define `file_server` as the fundamental service
abstraction in the architecture:

```c
// Conceptual: base file server interface
typedef seed_err_t (*fs_walk_fn)(void *state, const char *path,
                                  fid_t *out_fid, seed_err_ctx_t *err);
typedef seed_err_t (*fs_open_fn)(void *state, fid_t fid, int mode,
                                  seed_err_ctx_t *err);
typedef seed_err_t (*fs_read_fn)(void *state, fid_t fid,
                                  void *buf, size_t *n,
                                  uint64_t offset, seed_err_ctx_t *err);
typedef seed_err_t (*fs_write_fn)(void *state, fid_t fid,
                                   const void *buf, size_t n,
                                   uint64_t offset, seed_err_ctx_t *err);
typedef seed_err_t (*fs_stat_fn)(void *state, fid_t fid,
                                  seed_stat_t *out, seed_err_ctx_t *err);
typedef seed_err_t (*fs_clunk_fn)(void *state, fid_t fid,
                                   seed_err_ctx_t *err);

// Daemon startup: register as a file server and post in /srv
seed_9p_srv_t srv = {
    .walk   = cogd_walk,
    .open   = cogd_open,
    .read   = cogd_read,
    .write  = cogd_write,
    .stat   = cogd_stat,
    .clunk  = cogd_clunk,
    .state  = &g_cogd_state,
};
seed_9p_post("/srv/seedcogd", &srv);
```

This replaces the current diversity of interfaces (bus topics, C APIs,
Lua bindings, RPC calls) with a single, uniform abstraction.

### 6.6 Union Mounts for Configuration Layering and Override

**Plan 9**: `bind -b` (before) and `bind -a` (after) create union
directories. Used extensively for configuration: `/bin` is a union of
`/bin` and `$HOME/bin`; `/lib` is a union of system and local libraries.

**Solbian adoption**: Use union mounts for configuration layering:

```
# Base configuration:
#   /cfg/defaults/  -- shipped defaults (read-only)
mount -c /srv/cfg-defaults /cfg

# Local overrides:
#   /cfg/local/     -- administrator settings (writable)
bind -b /cfg/local /cfg

# Runtime overrides:
#   /cfg/runtime/   -- dynamic adjustments by homeostasis module
bind -b /cfg/runtime /cfg

# Result: reading /cfg/inference/temperature returns:
#   1. runtime value (if set)
#   2. local value (if set)
#   3. default value
```

This is a simpler, more composable alternative to the current hierarchical
config approach (environment variables -> `.env` file -> CMake defaults).

---

## 7. Specific NSLP/NSP Integration Points

### 7.1 NSL Primitives as 9P Operations

The 33 NSL primitives (from `SPEC.md`) map to 9P operations as follows:

**Group I: Object Lifecycle**
| NSL Primitive | 9P Equivalent | Notes |
|---------------|---------------|-------|
| `create` | `Tcreate` on the parent directory | Creates a new file (SXL entity) |
| `destroy` | `Tremove` on the file | Deletes the file |
| `typeof` | `Tstat` -> QID type field | Read the file's type metadata |

**Group II: Memory**
| NSL Primitive | 9P Equivalent | Notes |
|---------------|---------------|-------|
| `read` | `Tread` on a file at offset 0 | Read the full SXL entity |
| `write` | `Twrite` on a file | Write new content |

**Group III: Binding**
| NSL Primitive | 9P Equivalent | Notes |
|---------------|---------------|-------|
| `bind` | `bind` system call (namespace operation) | Bind path into namespace |
| `unbind` | `unmount` | Remove path from namespace |
| `resolve` | `Twalk` to follow path | Resolve name through namespace |

**Group V: Control Flow**
| NSL Primitive | 9P Equivalent | Notes |
|---------------|---------------|-------|
| `sequence` | Sequential Tread/Twrite on files | Standard I/O ordering |
| `parallel` | Multiple concurrent Treads/Twrites | 9P handles this naturally (multiple fids) |
| `spawn` | Create a new 9P connection with fresh namespace | Rfork(RFNAMEG)-style |

**Group IX: Channel**
| NSL Primitive | 9P Equivalent | Notes |
|---------------|---------------|-------|
| `send` | `Twrite` to a channel file | Similar to `/mnt/plumb` |
| `recv` | `Tread` from a channel file | Blocks until message available |
| `spawn` | `Tcreate` in `/cognitive/proc/` + start execution | Creates a new process file |

**Group X: Cognitive**
| NSL Primitive | 9P Equivalent | Notes |
|---------------|---------------|-------|
| `observe` | `Tread` from a sensor file in `/cognitive/observations/sensor/` | Read observation data |
| `assert` | `Twrite` to `/cognitive/beliefs/add` | Write new belief |
| `retract` | `Tremove` from `/cognitive/beliefs/` or write status=retracted | Remove or update file |
| `query` | `Twalk` + `Tread` from partition directory | Read matching entries |
| `derive` | `Twrite` to `/cognitive/inference/<backend>/prompt` + `Tread` result | Inference via file I/O |

### 7.2 NSP Compiler Using 9P

The NSP compiler pipeline (ARCHITECTURE.md Section 3) currently reads NSL
expressions from bus topics or in-memory buffers. With 9P:

```
NSL Expression (read from /cognitive/workflows/current/procedure)
    │
    │  Stage 1: Parse (same as current -- libsexpr)
    ▼
AST in arena
    │
    │  Stage 2: Graph construction (same as current)
    ▼
nsgraph_t
    │
    │  Stage 3: Optimization (same as current)
    ▼
Optimized nsgraph_t
    │
    │  Stage 4: Backend dispatch
    │    │
    │    ├── Symbolic  -> /cognitive/operators/compare   (Twrite/Tread)
    │    ├── Neural    -> /cognitive/inference/ollama/prompt (Twrite/Tread)
    │    ├── Hybrid    -> Both symbolic + neural files
    │    ├── Native    -> Direct C function (internal)
    │    ├── SST       -> /cognitive/operators/sst/eval  (Twrite/Tread)
    │    └── Deferred  -> /cognitive/proc/<id>/continuation (Tcreate)
    ▼
Executable nsplan_t
```

The key change: **backend dispatch goes through filesystem operations** rather
than direct C function calls. The dispatcher in
`src/libseedllm/src/dispatch.c:47-71` becomes a file server handler:

```c
// Current dispatch:
backend = task_classify(task);
pool = pool_for_backend(backend);
response = seed_llm_chat(pool, prompt);

// With 9P dispatch:
int fd = open("/cognitive/inference/ollama/prompt", O_WRONLY);
write(fd, prompt_sxl, prompt_len);
close(fd);
fd = open("/cognitive/inference/ollama/prompt", O_RDONLY);
n = read(fd, response_sxl, sizeof(response_sxl));
close(fd);
```

### 7.3 NSL Spawn as 9P Import

The NSL `spawn` primitive (`SPEC.md` Group IX) creates a new concurrent
process. In a 9P model:

```
(spawn :procedure "wf-reflection-v1" :args ...)
    │
    ▼
1. Create a new 9P connection to seed9pd
2. Mount a fresh private namespace:
   mount -c /srv/cognitive /cognitive
   mount -b /srv/proc/wf-reflection-v1 /cognitive/scratch
3. Execute the procedure in this new namespace
4. The new process appears in /cognitive/proc/<id>/
```

The `spawn` result is a process handle that shows up as a file:

```
/cognitive/proc/wf-reflection-v1/
  status            -- "running"
  ctl               -- write "suspend" / "resume" / "kill"
  result            -- read: procedure result (blocks until completion)
```

This is exactly analogous to spawning a new process in Plan 9: it creates a
new namespace group (`rfork(RFNAMEG)`) and the process appears in `/proc`.

### 7.4 NSP Backend Dispatch via 9P for Remote Backends

The current delegation system (`src/seedcogd/delegate.h`) sends phase work
to peer nodes via bus publish + subscribe. With 9P, remote backends are
accessed by mounting the peer's inference filesystem:

```c
// NSP runtime: remote inference
// 1. Mount peer's inference filesystem
if (mount("/srv/peer-node-b/inference", "/cognitive/remote-inference") < 0)
    return fallback_to_local();

// 2. Write prompt to peer's inference file
int fd = open("/cognitive/remote-inference/ollama/prompt", O_WRONLY);
write(fd, prompt, prompt_len);
close(fd);

// 3. Read result (blocks until peer completes)
fd = open("/cognitive/remote-inference/ollama/prompt", O_RDONLY);
read(fd, result, sizeof(result));
close(fd);

// 4. The stat version changed -> we have a fresh result
```

The 9P stat version number serves as a "freshness" indicator -- if the
remote peer has completed processing, the stat version increments. This
replaces the explicit pending-request tracking in
`seed_cog_delegate_pending_t` (delegate.h:66-73).

### 7.5 Channel Primitives as 9P Transport

NSL channels (`send`, `recv` with types UNICAST, MULTICAST, PUBSUB from
ARCHITECTURE.md 4.3) map naturally to 9P files:

**UNICAST** channel: a file in `/cognitive/channels/`:

```
/cognitive/channels/ch-001/
  send              -- write to this file (blocks if buffer full)
  recv              -- read from this file (blocks if empty)
  stat              -- read: capacity, depth, producer/consumer ids
```

**MULTICAST** channel: a directory with a consumer file per consumer:

```
/cognitive/channels/ch-002/
  consumers/
    c-01/recv       -- consumer 1 reads here
    c-02/recv       -- consumer 2 reads here
  send              -- write: fans out to all consumers
```

**PUBSUB** channel: a directory with topic files:

```
/cognitive/channels/ch-003/
  topics/
    reflection      -- write: publish to reflection topic
    reasoning       -- write: publish to reasoning topic
  subscribe/        -- write: create a subscription file
    s-01/recv       -- read: messages matching subscription
```

This is directly inspired by Plan 9's plumbing ("plumber") at
`~/sys/src/cmd/plumb/`:

```
/mnt/plumb/
  send      -- write: send a plumb message
  rules     -- read/write: routing rules
  <port>    -- read: received messages for this port
```

Plumbing is Plan 9's inter-process messaging system, and its 9P interface
is the direct ancestor of what NSL channels would look like.

---

## 8. Concrete Architecture Proposal

### 8.1 High-Level Architecture

```
                          ┌────────────────────────────────────┐
                          │         Cognitive Agents           │
                          │  (Lua brains, NSL procedures,      │
                          │   SST operators, cognitive cycle)  │
                          └──────────┬─────────────────────────┘
                                     │
                          ┌──────────▼─────────────────────────┐
                          │        9P Protocol (lib9p)          │
                          │  Tversion/Tattach/Twalk/Topen/      │
                          │  Tread/Twrite/Tstat/Tclunk          │
                          └──────────┬─────────────────────────┘
                                     │
              ┌──────────────────────┼──────────────────────────┐
              │                      │                          │
   ┌──────────▼──────────┐ ┌─────────▼──────────┐  ┌──────────▼──────────┐
   │      seed9pd         │ │  Existing Daemons   │  │   External Nodes    │
   │   (9P bridge daemon) │ │  (with built-in     │  │   (via T2/seedneted)│
   │                      │ │   9P exports)       │  │                     │
   │  ┌─────────────────┐ │ │                      │  │   mount /cognitive  │
   │  │ Namespace Mgr   │ │ │  seedcogd ───►/srv/  │  │   mount /srv/...   │
   │  │ (per-connection │ │ │  seedreasond ──►/srv/│  │                     │
   │  │  private ns)    │ │ │  seedneted ────►/srv/│  └─────────────────────┘
   │  └─────────────────┘ │ │  seedsysresd ──►/srv/│
   │  ┌─────────────────┐ │ │                      │
   │  │ Bus Bridge      │ │ │  (export /cognitive, │
   │  │ (bus ↔ 9P)      │ │ │   /daemons, /proc)   │
   │  └─────────────────┘ │ │                      │
   │  ┌─────────────────┐ │ └──────────────────────┘
   │  │ Memory Export   │ │
   │  │ (libsmem ↔ 9P)  │ │
   │  └─────────────────┘ │
   │  ┌─────────────────┐ │
   │  │ Inference Export│ │
   │  │ (libseedllm↔9P) │ │
   │  └─────────────────┘ │
   └──────────────────────┘
              │
              │  libbus API (existing)
              ▼
   ┌──────────────────────────────────────────────────────────┐
   │                Solbian Bus (T0/T1/T2)                     │
   │  publish/subscribe/request/priority/backpressure          │
   └──────────────────────────────────────────────────────────┘
```

### 8.2 Protocol Stack

```
 Layer 5: Cognitive Workflows
    NSL procedures composed from primitives
        │
        │  ns-bind, ns-mount, ns-fork (namespace operations)
        ▼
 Layer 4: NSL Primitives
    33 primitives (SPEC.md)
        │
        │  Each maps to 9P Tread/Twrite/Tstat/Tcreate/Tremove
        ▼
 Layer 3: 9P Protocol (lib9p)
    17 message types over reliable byte stream
        │
        │  Transport abstraction
        ▼
 Layer 2: Transport
    UDS (T1/native 9P) | Noise-IK encrypted session (T2) | In-process (T0)
        │
        ▼
 Layer 1: Physical
    Local socket | Network (TCP/IP)
```

### 8.3 Current Component Mapping

| Current Component | Plan 9 Equivalent | Notes |
|-------------------|-------------------|-------|
| `seedbusbrokerd` | `/srv` + name server | Topic routing becomes filesystem routing |
| `seedcogd` | CPU server + `/proc` | Exports cognitive state as filesystem |
| `seedreasond` | Factotum (auth) + `/dev` (policy) | Policy evaluation as file read/write |
| `seedneted` | `/net` | Network connections as files in `/net/t2/` |
| `seedsysresd` | `/dev` hardware devices | CPU/memory as files |
| `libbus` | Plumber (`/mnt/plumb`) | Inter-process messaging via files |
| `libsmem` | File system (kfs) | Memory partitions are directory trees |
| `libseedllm` | Custom device | `/cognitive/inference/` synthetic FS |
| `libsexpr` | Standard library | `/cognitive/operators/` synthetic FS |
| NSL/NSP runtime | Shell + rc | Procedure execution with namespace control |
| ACL agent roles | Factotum keys | Per-connection credentials from factotum |

### 8.4 New Daemon/Service Boundaries

| New Component | Purpose | Depends On |
|---------------|---------|------------|
| `seed9pd` | 9P protocol bridge; exports bus, memory, inference as filesystem | `lib9p`, `libbus`, `libsmem`, `libseedllm` |
| `seedsrvd` | `/srv` directory manager; daemon service registry | `lib9p` |
| `seedfactotumd` | Auth credential store; issues 9P auth responses | `lib9p` |
| `lib9p` | 9P protocol library: encode/decode, server skeleton, client API | (none, pure C11) |

---

## 9. Risks and Challenges

### 9.1 Where Plan 9's Model Does NOT Fit Solbian

**Latency-sensitive cognitive operations**: Plan 9 was designed for a
single-site user environment with millisecond-latency file operations.
9P's Twalk-Topen-Tread round-trip for a single data access is 3 message
exchanges. The current bus delivers data in a single publish-subscribe
event. For the cognitive cycle's internal operations (running at ~200ms
per cycle on a Raspberry Pi), the 9P overhead is significant:

```
Current bus:  1 publish -> 1 callback invocation (microseconds)
9P model:     Twalk (1 RTT) + Topen (1 RTT) + Tread (1 RTT) + Tclunk (1 RTT)
              Minimum 4 round-trips per read operation
```

Mitigation: Use 9P2000's `topen` with `OTRUNC` to put fid in a known state
in one message, or use the `iounit` field to batch reads. For the
highest-latency paths (neural inference), add read-ahead and caching.

**Event-driven cognitive architecture**: The cognitive cycle is
fundamentally event-driven: observations trigger state changes, which
trigger phase execution, which produce new observations. 9P is pull-based:
a client must explicitly request new data. Push notification in 9P is
possible (the server keeps the fid open and returns data on subsequent
Treads), but it reverses the natural flow.

Mitigation: Keep the bus for event distribution (push) and add 9P for
resource access (pull). The two protocols coexist with different purposes.

**Backend diversity**: Solbian's 5-backend LLM pool (ollama, native,
openai, sst, uds) has diverse API patterns. Fitting all of them behind a
uniform `/cognitive/inference/<backend>/prompt` interface requires either
(a) a common denominator interface (losing backend-specific features) or
(b) backend-specific files within the directory. Option (b) is preferred
but adds complexity to the synthetic filesystem.

**Memory size and access patterns**: SXL entities can be large (hundreds
of KB for complex belief structures). 9P was designed for small messages
(8K default, but can negotiate up to 64K with `msize`). Reading a 200KB
SXL entity requires multiple 9P messages, increasing overhead.

**No root, but no capability model**: Plan 9 has no superuser, which is
philosophically appealing. But its permission model is Unix-style (rwx per
user/group/other). Solbian's ACL model (5 roles with fine-grained
topic-level permissions) is richer. Mapping ACL roles to 9P's permission
bits loses granularity.

### 9.2 Performance Concerns

| Operation | Current Bus Latency | 9P Latency (est.) | Ratio |
|-----------|---------------------|--------------------|-------|
| Publish & deliver (T0) | 1-5 us | N/A (different model) | — |
| Publish & deliver (T1 UDS) | 50-200 us | N/A | — |
| Read one SXL entity | 10-50 us (libsmem) | 100-500 us (9P over UDS) | 10x |
| Write one SXL entity | 10-50 us (libsmem) | 100-500 us (9P over UDS) | 10x |
| Query (scan + match) | 50-200 us (libsmem) | 200-1000 us (9P + libsmem) | 4-5x |
| Neural inference | 500ms-5s | Same (inference dominates) | ~1x |
| Cross-node access | 5-50ms (T2 encrypted) | 5-50ms (9P over T2) | ~1x |

The 9P overhead is most significant for **small, frequent operations**
within the cognitive cycle (reading/writing individual SXL entries).
For **high-latency operations** (neural inference, cross-node
communication), the 9P overhead is negligible.

Mitigation strategies:
1. **Batched reads**: Use 9P's `iounit` to read multiple SXL entries in
   a single `Tread` response.
2. **Cached file descriptors**: Keep fids open across multiple operations
   to avoid Twalk/Topen overhead.
3. **Hybrid access**: Fast-path operations (internal memory access within
   seedcogd) use the direct C API; cross-component and cross-node
   operations use 9P.
4. **Bulk transfer for large entities**: For SXL entities >64K, use a
   separate bulk transfer channel (9P Twrite with large `msize`).

### 9.3 Security Model Differences

| Aspect | Plan 9 | Solbian (Current) |
|--------|--------|-------------------|
| Authentication | Factotum (per-process keys) | ACL roles (5 levels) |
| Authorization | File permissions (rwx) | Topic pattern ACLs |
| Identity | User-level (no root) | Node DIDs (`did:seed:nodeA`) |
| Network security | Auth in 9P protocol layer | T2 encrypted (libsodium crypto_box) |
| Policy | No built-in policy engine | seedreasond (SXL policy evaluation) |

**Key divergence**: Solbian's ACL system is more expressive than Plan 9's
file permissions. A 9P integration must preserve the ACL model:

- An `external` role agent connecting to seed9pd gets a restricted
  namespace (can only read `/cognitive/beliefs`, cannot write)
- A `core` role agent gets read-write access to most partitions
- System-critical operations (motor intents) require specific role
  authorization

Implementation: seed9pd maps 9P auth responses to Solbian ACL roles. The
connection's `Tauth` message carries a token derived from the agent's DID,
which seed9pd validates against the ACL database. On successful auth, the
client's namespace is constructed according to the agent's role.

**Recommendation**: Keep the Solbian ACL model as the authorization source
of truth. Use 9P's auth as the transport mechanism only.

### 9.4 Complexity Cost

The primary complexity cost is **adding a second system interface**. Currently:

- Agents talk to the system via bus topics (SXL over publish/subscribe)
- Internal components talk via C APIs (libsmem, libseedllm, etc.)

With 9P integration:

- Agents can talk via 9P filesystem (new)
- Agents can still talk via bus topics (existing)
- Internal components use C APIs (unchanged)
- `seed9pd` bridges between 9P and the bus/APIs

This is two interfaces to maintain, document, and debug. The cognitive
cycle now has three I/O paths: direct C API, bus messages, and 9P filesystem.

**Mitigation**: Don't make everything use 9P from day one. Phase the
integration so that:
1. seed9pd is always additive (existing agents continue as-is)
2. Only agents that explicitly request 9P access use it
3. Internal cycle components never go through seed9pd (direct C API always)

### 9.5 What NOT to Adopt from Plan 9

1. **The `#` device naming convention**: Plan 9 uses `#S` for SCSI, `#I` for
   IP, `#P` for proc. This is cryptic and doesn't map well to Solbian's
   descriptive topic naming. Use descriptive paths instead.

2. **The `cputemp` file system style**: Plan 9 often puts multiple values
   in a single file separated by spaces (like `/dev/time`: "seconds
   milliseconds"). For cognitive state, each file should contain a single,
   well-formed SXL entity.

3. **Plan 9's lack of concurrent write protection**: Plan 9 filesystems
   typically don't handle concurrent writes to the same file gracefully.
   Solbian's memory model requires atomic upsert semantics. The 9P bridge
   must implement proper sequence numbers or locking.

4. **The `Fs` 3-level directory model**: Plan 9's `Fs` (from `libfs`) uses
   a rigid 3-level structure (top-level dirs are types, second-level are
   specific instances, files are data). Cognitive state is more hierarchical.
   Use a free-form directory tree that mirrors the partition namespace.

5. **9P's Tremove being permanent**: Plan 9 has no trashcan -- once a file
   is removed, it's gone. Solbian's memory model is append-only with status
   flags. Tremove on a cognitive entry should map to status=retracted, not
   actual deletion.

6. **No logging/observability**: Plan 9's filesystems typically have minimal
   instrumentation. Solbian's observability (metrics counters via
   `seed_bus_metrics_set_callback`, per-cycle `dsxl()`) must be preserved.

7. **Inferno's/dis legacy**: Inferno's `dis` VM and Limbo language were
   Plan 9's attempt at portable execution environments. Solbian already has
   Lua for scripting and C for performance. No need for another runtime.

---

## 10. Recommended Phased Adoption

### 10.1 Phase 1: Minimal (Weeks 1-4)

**Goal**: The smallest useful 9P integration that proves the concept.

**What ships**:
- `lib9p` -- minimal C 9P2000 wire library (~500 lines)
- `seed9pd` -- bridge daemon that exports bus topics as 9P files (~800 lines)
- One integration test: 9P client reads from a bus topic via seed9pd

**Concrete steps**:

| Step | Description | Files |
|------|-------------|-------|
| 1.1 | Implement 9P2000 encoder/decoder in C | `src/lib9p/9p.h`, `src/lib9p/fcall.c` |
| 1.2 | Implement 9P server skeleton (accept, dispatch fversion/fauth/fattach/fwalk/fopen/fread/fwrite/fclunk) | `src/lib9p/srv.c` |
| 1.3 | Build `seed9pd`: connects to bus, exports `org.seed.cog.observation.*` as `/cognitive/observations/` | `src/seed9pd/main.c` |
| 1.4 | Test: standalone 9P client reads observations | `tests/test_9p_integration.c` |
| 1.5 | Document: protocol reference, seed9pd configuration | `docs/plan9/` |

**Success criteria**:
- [ ] A C program can connect to `seed9pd`, walk to `/cognitive/observations`,
      open the current topic, read SXL entries.
- [ ] The same data is simultaneously available via the existing bus API.
- [ ] No existing Solbian code is modified (additive only).

**Architecture decision**: Put `lib9p` in its own directory, governed by
a `SEED_BUILD_9P` CMake option (default OFF). This keeps the core build
unaffected.

### 10.2 Phase 2: Core (Weeks 5-10)

**Goal**: Adopt key Plan 9 patterns into the Solbian architecture:
synthetic filesystems for key components, namespace isolation.

**What ships**:
- `seed9pd` extended: export libsmem partitions, inference backends, daemon
  control interfaces
- Per-connection namespace support in `seed9pd`
- ACL-integrated auth (9P auth -> Solbian role)

**Concrete steps**:

| Step | Description | Files |
|------|-------------|-------|
| 2.1 | Export libsmem partitions as directories in seed9pd | `src/seed9pd/memory.c` |
| 2.2 | Export libseedllm backends as inference files | `src/seed9pd/inference.c` |
| 2.3 | Per-connection namespace: each 9P client gets a private namespace root | `src/seed9pd/namespace.c` |
| 2.4 | Auth integration: map 9P Tauth -> Solbian ACL role, restrict namespace | `src/seed9pd/auth.c` |
| 2.5 | Export daemon status/control as files (seedcogd cycle count, load) | `src/seed9pd/daemon.c` |
| 2.6 | 9P Tstat on all files -> SXL metadata (type, version, confidence, etc.) | `src/seed9pd/stat.c` |

**Success criteria**:
- [ ] An agent can read/write cognitive state via filesystem operations
- [ ] An agent with role `external` sees a different namespace than `core`
- [ ] An agent can check daemon status via `stat("/daemons/seedcogd/status")`
- [ ] Inference requests go through `/cognitive/inference/prompt` files

**Architecture decision**: At this phase, `seed9pd` becomes the canonical
access point for **external agents** (sapling agents, remote nodes). Internal
cognitive cycle components continue to use the C API. This follows the existing
separation between `sapling` (external) and `core` (internal) from
`~/solbian/sapling/INTEGRATION.md`.

### 10.3 Phase 3: Deep (Weeks 11-20)

**Goal**: Comprehensive 9P-based distributed cognition. D1-D5 layers use
9P for resource sharing. NSL primitives use 9P as their I/O substrate.

**What ships**:
- D1-D5 over 9P (mount remote cognitive filesystems)
- /srv pattern (daemon service registry)
- /net pattern (network as filesystem)
- NSL primitives mapping (send/recv/spawn/bind/unbind as 9P ops)
- Union mount support for configuration layering

**Concrete steps**:

| Step | Description | Files |
|------|-------------|-------|
| 3.1 | D2 cross-node sync via 9P: mount remote node's cognitive FS | `src/seed9pd/remote.c` |
| 3.2 | D3 capability advertisement via `/srv` file stat | `src/seedsrvd/` |
| 3.3 | D5 workload delegation via remote inference file writes | `src/seed9pd/delegate.c` |
| 3.4 | `/net/t2/` synthetic FS for T2 session management | `src/seedneted/9p.c` |
| 3.5 | Union mount support in namespace manager | `src/seed9pd/union.c` |
| 3.6 | NSL -> 9P mapping: NSP runtime uses 9P for all I/O | `src/lib9p/nsl-bridge.c` |
| 3.7 | seedfactotumd: factotum-style auth credential store | `src/seedfactotumd/` |

**Success criteria**:
- [ ] Two nodes can mount each other's `/cognitive/` over T2
- [ ] Delegating inference to a peer uses file operations, not bus messages
- [ ] NSL `(send)` / `(recv)` use 9P channel files
- [ ] Configuration overlays work via union mounts
- [ ] All D1-D5 distributed cognition layers work over 9P or with 9P fallback

**Architecture decision**: At this phase, the 9P filesystem becomes the
**primary northbound interface** for the distributed cognition stack. The
bus remains as the **internal event transport** (within a single process)
and the **control plane** (for daemon-to-daemon signaling). External agents
and remote nodes interact primarily through 9P.

### 10.4 Phase 4: Optional (Future)

**Goal**: Full adoption. If 9P proves successful, consider deeper integration.

**What might ship**:
- Plan 9's `exportfs` running on the host (Linux or Plan 9) for remote access
- v9fs kernel mount for host processes that need direct `/cognitive/` access
- A Plan 9 distribution running the cognitive daemon natively
- `/proc` filesystem for NSL process management
- Plumber-style IPC for the cognitive cycle's internal event distribution

### 10.5 Assessment: Is 9P Worth It for Solbian?

**Verdict**: Yes, as a **secondary access protocol** and **distributed
resource abstraction**. No, as a **replacement for the bus**.

The strengths of the 9P model for Solbian:
- Universal access protocol (any client, any language, any location)
- Namespace isolation (per-agent cognitive state views)
- Uniform abstraction (every component looks like a file server)
- Proven distributed model (Plan 9's CPU server = Solbian's delegation)

The weaknesses for Solbian:
- Event-driven cognitive cycle doesn't map cleanly to pull-based I/O
- Latency overhead for small, frequent memory operations
- Two interfaces to maintain (bus + 9P)
- No pattern matching (bus's `*`/`**` subscriptions have no 9P equivalent)

**Recommendation**: Implement phases 1 and 2. Re-evaluate after practical
experience with the bridge daemon. Phase 3 (deep adoption) should proceed
only if phases 1-2 demonstrate clear value.

---

## References

### Plan 9 Source (as referenced)
- `/sys/src/9/port/9p.h` -- 9P protocol definitions
- `/sys/src/9/port/devip.c` -- IP device (`/net`)
- `/sys/src/9/port/devproc.c` -- Process device (`/proc`)
- `/sys/src/9/port/devsrv.c` -- Service device (`/srv`)
- `/sys/src/cmd/cpu.c` -- CPU server client
- `/sys/src/9/cpu/port/devcputerm.c` -- Terminal device for `cpu`
- `/sys/src/cmd/plumb/` -- Plumber (IPC messaging)
- `/sys/src/lib9p/` -- 9P server library
- `/sys/src/libc/port/bind.c` -- bind/mount system calls

### Plan 9 Documentation
- "The Organization of Networks in Plan 9"
- "Plan 9 from Bell Labs" (AT&T, 1995)
- "The Use of Name Spaces in Plan 9" (Pike et al., 1993)
- "Lexical File Names in Plan 9" (Pike, 1993)

### Solbian/seed-dev Source
- `src/libbus/` -- Bus protocol (T0, T1, T2)
- `src/libbus/include/seed/bus.h` -- Bus public API
- `src/libbus/src/t1.c` -- T1 UDS transport
- `src/libbus/src/t2.c` -- T2 network bridge
- `src/libsmem/` -- Partitioned symbolic memory
- `src/libsmem/include/seed/smem.h` -- Memory public API
- `src/libseedllm/src/dispatch.c` -- Capability-based backend routing
- `src/seedcogd/main.c` -- Cognitive daemon (3212 lines of cycle logic)
- `src/seedcogd/delegate.h` -- D5 delegation protocol
- `src/seedcogd/capability.h` -- D3 capability advertisement
- `src/seedcogd/kg_sync.h` -- D4 knowledge graph bloom filter sync
- `src/libsexpr/src/sexpr.c` -- S-expression parser
- `src/libsexpr/src/transform.c` -- S-expression transform ops
- `src/libsexpr/src/confidence.c` -- Confidence propagation
- `src/libsexpr/src/query.c` -- S-expression query engine
- `schemas/.sref/v1/sxl.sref` -- Canonical SXL schema
- `codex/machina/policies/acl/agent_acl.sref` -- ACL role definitions

### Solbian Architecture Documents
- `~/solbian/tools/NSLP/ARCHITECTURE.md` -- NSLP 4-layer ISA architecture
- `~/solbian/tools/NSLP/SPEC.md` -- NSL 33-primitive instruction set
- `~/solbian/tools/NSLP/INTEGRATION.md` -- NSLP integration with seed-dev
- `~/solbian/tools/NSLP/GAP-ANALYSIS.md` -- Gap analysis (19 gaps)
- `~/solbian/tools/NSLP/ROADMAP.md` -- Implementation roadmap (5 phases)
- `~/solbian/sapling/INTEGRATION.md` -- Sapling integration model
- `~/solbian/sapling/AGENTS.md` -- Sapling agent catalog
- `~/seed-dev/docs/architecture/SST_ARCHITECTURE.md` -- SST architecture
- `~/seed-dev/docs/cognition/SXL_LANGUAGE_SPECIFICATION.md` -- SXL spec

### Open-Source 9P Implementations
- `plan9port` (`github.com/9fans/plan9port`) -- `src/lib9p/`, `src/lib9pclient/`
- `v9fs` (Linux kernel) -- `~/kernel/fs/9p/`
- `mux9p` (`github.com/fhs/mux9p`) -- Go 9P2000 server/client
- `p9` (`github.com/hugelgupf/p9`) -- Go 9P2000.L with virtio transport

---
