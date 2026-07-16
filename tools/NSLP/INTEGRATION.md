# NSLP Integration — Connecting NSL/NSP to S.E.E.D.

> **Status**: Draft 0.1.0  
> **Version**: 2026-07-16  
> **ACL role**: `external` (sapling prototype)  
> **Upstream home**: `~/solbian/tools/NSLP/`  
> **Canonical references**: `~/seed-dev/src/` (code), `~/solbian/sapling/INTEGRATION.md` (sapling model)

---

## 1. Integration Model Overview

NSLP integrates with S.E.E.D. as a **sapling-level component**. Per the sapling model in `~/solbian/sapling/INTEGRATION.md`, this means:

- NSLP is an **experimental client of the bus**, not a first-class S.E.E.D. component
- It connects on the `org.seed.*` namespace via T1 (cognitive plane) and T2 (data plane)
- It operates under the `external` ACL role: read-only for most partitions, publish to constrained topics
- It graduates to a `core` or `higher_order` role once stable

The integration has five surfaces:

| Surface | Protocol | Purpose |
|---------|----------|---------|
| **Bus** (T1) | `org.seed.cog.nsl.*` topics | NSL execution requests and results |
| **Memory** (libsmem) | `cognitive/this-node/*` partitions | SXL entity storage for primitives |
| **Backends** (libseedllm) | `seed_llm_chat()` / `seed_llm_pool_*` | Neural inference dispatch |
| **SST** (seed-transformer) | `sst_execute()` / `sst_workspace_t` | Operator execution and workspace access |
| **Cycle** (seedcogd) | `nsp_schedule()` / workflow table | Phase replacement and augmentation |

---

## 2. Bus Integration — T1 Cognitive Plane

### 2.1 Topic Namespace

NSLP uses the `org.seed.cog.nsl.*` sub-namespace, which follows the FROZEN-2026-05-10 topic naming convention (`org.seed.<segment>(.<segment>){1,5}`).

#### Published Topics (NSLP -> bus)

| Topic | Payload | Frequency | ACL Required |
|-------|---------|-----------|-------------|
| `org.seed.cog.nsl.execute` | NSL expression (SXL) | On demand | `external` (publish) |
| `org.seed.cog.nsl.workflow.completed` | Workflow result SXL | Per workflow | `external` (publish) |
| `org.seed.cog.nsl.workflow.failed` | Error SXL | On failure | `external` (publish) |
| `org.seed.cog.nsl.schedule` | `cognitive/this-node/workflows` entries | Every cycle | `external` (publish) |

#### Subscribed Topics (NSLP <- bus)

| Topic | Payload | Purpose |
|-------|---------|---------|
| `org.seed.cog.nsl.execute.reply` | Execution result | Reply from NSP runtime |
| `org.seed.cog.nsl.compile` | NSL expression | Compile-only request (no execution) |
| `org.seed.cog.nsl.compile.reply` | `nsplan_t` serialized | Compiled plan for inspection |
| `org.seed.cog.nsl.workflow.register` | `(:type workflow ...)` SXL | Register a new workflow |
| `org.seed.cog.nsl.workflow.unregister` | Workflow ID | Remove a workflow |
| `org.seed.cog.nsl.primitive.status` | Primitive query | List available primitives |
| `org.seed.cog.nsl.primitive.status.reply` | Primitive table | Backend-capability matrix |

### 2.2 Execution Request/Reply Flow

The canonical NSL execution flow over the bus:

```
Publisher (agent / cog cycle)          NSP Runtime
         │                                  │
         │  org.seed.cog.nsl.execute        │
         │ ──────────────────────────────►   │
         │  (NSL S-expression)               │
         │                                  │── parse
         │                                  │── compile (graph + optimize)
         │                                  │── dispatch to backends
         │                                  │── execute
         │                                  │
         │  org.seed.cog.nsl.execute.reply   │
         │ ◄──────────────────────────────  │
         │  (result SXL or error)           │
```

The request payload format:

```sxl
(:type nsl_request :id "req-001"
 :expression "(:derive :from ...)"
 :priority 0.8
 :max_cost 50.0
 :reply_to "org.seed.agent.cognitive.requests")
```

The reply payload format:

```sxl
(:type nsl_result :id "req-001"
 :status completed
 :confidence 0.82
 :result (:type observation ...)
 :cost 12.5
 :backends (:ollama :libsexpr)
 :trace (:nodes 5 :parallel 2 :backends 2))
```

### 2.3 Bus Transport Details

Per `src/libbus/src/t1.c` and `src/seedbusbrokerd/`:

- **Socket**: UDS at `/run/seed/bus.sock` (default)
- **Framing**: SXL S-expression text, CBOR envelope per `RFC-0001` / `ADR-0005`
- **QoS**: `SEED_QOS_TIMELY` for execution requests (fast, no persistence); `SEED_QOS_STREAMING` for workflow registration (reliable)
- **Priority**: `SEED_PRIORITY_HIGH` for direct execution; `SEED_PRIORITY_NORMAL` for scheduling

The existing `seed_bus_publish()` and `seed_bus_subscribe()` functions from `src/libbus/src/bus.c` are used directly. The `seed_bus_request()` convenience from `src/libbus/src/bus.c` provides the request/reply pattern with automatic reply-topic routing (the `.reply` suffix convention used by `seedcogd/main.c:874-884`).

---

## 3. libsmem Integration — Symbolic Memory Partitions

NSL primitives operate on SXL entities stored in libsmem partitions. The existing `seed_smem_sxl_scan()` and `seed_smem_sxl_get()` wrappers in `src/libsmem/src/sxl.c` provide the base API for scanning cognitive partitions.

### 3.1 Partition Access by Primitive Group

| Primitive Group | Partitions Read | Partitions Written | Access Pattern |
|----------------|-----------------|--------------------|----------------|
| Perception | (raw input) | `cognitive/this-node/observation` | Write-only |
| Memory | `cognitive/this-node/*`, `cognitive/this-node/world/*` | `cognitive/this-node/`, `cognitive/this-node/relations` | Read/write |
| Query | `cognitive/this-node/*` | (read-only) | Read-only |
| Inference | `cognitive/this-node/knowledge`, `cognitive/this-node/world` | `cognitive/this-node/knowledge`, `cognitive/this-node/hypotheses` | Read/write |
| Comparison | `cognitive/this-node/*` | (read-only) | Read-only |
| Control Flow | (implicit — workflow state) | `cognitive/this-node/continuations` | Internal |
| Confidence | `cognitive/this-node/*` | `cognitive/this-node/confidence` | Read/write |
| Transformation | `cognitive/this-node/knowledge` | `cognitive/this-node/knowledge` | Read/write |
| Planning | `cognitive/this-node/goals` | `cognitive/this-node/plans` | Read/write |
| Evaluation | `cognitive/this-node/knowledge`, `cognitive/this-node/policies` | `cognitive/this-node/evaluations` | Read/write |
| Meta-Cognition | `cognitive/this-node/reflection`, `cognitive/this-node/history` | `cognitive/this-node/reflection` | Read/write |

### 3.2 Concrete Memory Operations

The NSP runtime maps NSL primitives to existing `seed_smem_*` functions:

**`(recall :query expr :from partition :limit n)`** maps to:
```c
// src/libsmem/src/sxl.c:25-54
seed_err_t seed_smem_sxl_scan(memory_root_dir, sxl_type, callback, user_data, limit)
```
The query SXL entity is compiled into a `seed_smem_scan_filter_t` (declared in `src/libsmem/include/seed/smem.h`), which supports type filtering, field matching, and limit. For complex queries, the filter is built by extracting `:type`, `:status`, and `:confidence` keywords from the query SXL.

**`(store :what sxl :where partition)`** maps to:
```c
// src/seedcogd/main.c:374-399 (journal append + index_add)
// via seed_smem_entry_put() from libsmem
```
The SXL entity is serialized as a `memory_entry/v1` record, written to the append-only `.sref` log and the JSONL journal (`cog-journal.jsonl`), and indexed in the 2048-entry ring buffer (`src/seedcogd/main.c:57-103`).

**`(forget :target id :reason string)`** maps to:
```c
// src/seedcogd/main.c memory management
// Entry status set to 'abandoned', confidence decayed to floor
```
Sets `status: abandoned` on the target entry. The entry remains in the append-only log (per the immutability principle) but is excluded from query results. Physical reclamation is handled by the existing decay and compaction logic at `seedcogd/main.c:2384-2414`.

**`(bind :a id :b id :label relation :weight float)`** maps to:
```c
// src/seedcogd/main.c:78-88 (relation table)
// index_add_relation() / relation query
```
The 8192-entry relation table in `seedcogd/main.c` supports directed, typed edges between entities. The 14 canonical relation labels are defined in `sxl.sref:34-38`: supports, contradicts, derives, causes, depends, refines, generalises, specialises, related, evidence, inspires, precedes.

### 3.3 Continuation Storage

Workflow continuations (see ARCHITECTURE.md 4.2) are stored in `cognitive/this-node/continuations` partition using the same `memory_entry/v1` record format but with an explicit `:type continuation` discriminator. The NSP scheduler scans this partition at cycle start:

```c
// Conceptual: NSP scheduler check at top of seedcogd cycle
static void nsp_check_continuations(seed_smem_t *mem) {
    seed_smem_scan_filter_t filter = {0};
    filter.type = "continuation";
    filter.limit = 16;
    // ... scan cognitive/this-node/continuations
    // ... for each continuation, restore and resume
}
```

---

## 4. libseedllm Integration — Neural Backend Dispatch

NSL primitives that require neural inference (derive, abduce, analogize, evaluate, reflect, criticise) dispatch through `libseedllm`. The integration uses the same capability-based routing defined in `src/libseedllm/src/dispatch.c:47-71`.

### 4.1 Primitive-to-Backend Mapping

The dispatcher maintains a capability matrix that maps each NSL primitive to its supported backends:

| Primitive | Symbolic (libsexpr) | Neural (LLM) | Hybrid | SST |
|-----------|-------------------|---------------|--------|-----|
| observe | Parser only | NL-to-SXL | Translation + validation | Parse |
| extract | Pattern match | — | — | — |
| classify | Keyword match | Semantic classification | Both | — |
| store | — | — | — | — |
| recall | Query engine | Semantic search | Both | Retrieve |
| forget | Status update | — | — | — |
| bind | Relation table | — | — | Add relation |
| match | `sxp_query_find` | — | — | — |
| filter | Iterator | — | — | — |
| join | Relational merge | — | — | — |
| derive | Policy eval | LLM inference | Both | SST_OP_INFER |
| abduce | — | LLM inference | + validation | — |
| induce | — | LLM inference | + validation | SST_OP_LEARN |
| analogize | — | LLM inference | + validation | — |
| compare | `sxp_oper_compare` | — | — | SST_OP_COMPARE |
| similarity | Trigram overlap | Embedding cosine | Combined | Attention |
| contradicts | Logic check | — | — | — |
| propagate | `sxp_confidence_propagate` | — | — | — |
| reinforce | Score update | — | — | Set confidence |
| decay | Score update | — | — | — |
| merge | `sxp_oper_merge` | — | — | Compose |
| split | `sxp_oper_split` | — | — | Decompose |
| abstract | — | LLM summarize | + validation | Generalise |
| specialise | — | LLM adaptation | + validation | — |
| decompose | — | LLM planning | + validation | SST_OP_DECOMPOSE |
| schedule | Topological sort | — | — | SST_OP_PLAN |
| evaluate | Policy eval | LLM scoring | Both | SST_OP_EVALUATE |
| verify | Contradiction check | LLM verification | Both | SST_OP_VERIFY |
| criticise | — | LLM critique | + validation | SST_OP_CRITICISE |
| reflect | — | LLM reflection | + validation | SST_OP_REFLECT |
| trace | Logger | — | — | — |

### 4.2 Backend Selection Algorithm

The per-primitive backend selection extends the existing `task_classify()` function from `src/libseedllm/src/task_classify.c`:

```c
// Conceptual: NSP backend selector
nsp_backend_t nsp_select_backend(nsp_primitive_t prim,
                                  seed_sx_ref_t args,
                                  nsp_backend_context_t *ctx) {
    // 1. Check primitive-backend capability matrix
    if (!capability_matrix[prim].has_neural)
        return NSP_BACKEND_SYMBOLIC;
    if (!capability_matrix[prim].has_symbolic)
        return NSP_BACKEND_NEURAL;

    // 2. Check confidence requirement
    double conf_req = sx_extract_confidence(args); // from :confidence kw
    if (conf_req > 0.85 && ctx->symbolic_healthy)
        return NSP_BACKEND_SYMBOLIC;  // high confidence -> symbolic
    if (conf_req < 0.50 && ctx->neural_healthy)
        return NSP_BACKEND_NEURAL;    // generative -> neural

    // 3. Check backend health (from seed_llm_pool_stats)
    if (!ctx->neural_healthy) return NSP_BACKEND_SYMBOLIC;
    if (!ctx->symbolic_healthy) return NSP_BACKEND_NEURAL;

    // 4. Default: hybrid for inference primitives, symbolic for structural
    switch (prim.group) {
        case NSP_GROUP_INFERENCE:
        case NSP_GROUP_EVALUATION:
        case NSP_GROUP_META:
            return NSP_BACKEND_HYBRID;
        default:
            return NSP_BACKEND_SYMBOLIC;
    }
}
```

### 4.3 Confidence Scoring Across Backends

When a primitive is dispatched to `NSP_BACKEND_HYBRID`, the neural result is validated symbolically, and the final confidence is computed by `sxp_confidence_propagate()` (`src/libsexpr/src/confidence.c`):

```
propagation_rule = "deductive"
neural_conf = 0.82   (from LLM response)
symbolic_conf = sxp_validate(result) ? 0.95 : 0.10
final_conf = sxp_confidence_propagate(deductive, {neural_conf, symbolic_conf}, ...)
```

The propagate function supports 5 rules (`src/libsexpr/src/confidence.c`):
- **deductive**: minimum of premises (conservative conjunction)
- **bayesian**: Bayesian update with prior and likelihood
- **ds**: Dempster-Shafer combination
- **fuzzy**: Fuzzy logic min/max
- **decay**: Exponential decay over time

---

## 5. seedcogd Integration — Phase Replacement

The most significant integration is the gradual replacement of hard-coded cognitive cycle phases with NSL workflows. This section describes the concrete integration points in `src/seedcogd/main.c`.

### 5.1 Current Phase Structure

The cognitive cycle in `seedcogd/main.c:1718-2925` has this structure:

```c
// In cognitive_cycle() function, called every iteration:
// Line 1718: Phase A — parallel reflection + evaluation + discovery
// Line 1845: Phase B — contradiction check + plan
// Line 1870: Phase C — hippocampus consolidation (every 5)
// Line 2117: Phase D — prediction
// Line 1987: Phase E — learning
// Line 2120: Phase F — language evolution (every 20)
// Line 2218: Phase G — vision observation (every 30)
// Line 2246: Phase H — attention gate
// Line 2354: Phase I — working memory
// Line 2457: Phase J — goal management (every 7)
// Line 2609: Phase K — meta-cognition (every 11)
// Line 2783: Phase L — creativity gate (every 13)
```

### 5.2 Workflow Table Integration

The NSP runtime maintains a workflow registry as an in-memory table, loaded from `cognitive/this-node/workflows` partition at daemon startup:

```c
// Conceptual: workflow table loaded by NSP at seedcogd startup
typedef struct nsp_workflow_s {
    char            id[64];         /* ULID */
    char           *procedure_sxl;  /* NSL S-expression */
    int             version;
    double          confidence;
    nsp_trigger_t   trigger;        /* schedule or event */
    nsp_state_t     last_state;
    int             last_cycle;
    double          avg_cost;
} nsp_workflow_t;

// In seedcogd main(), after config_load() and pool init:
// nsp_init();                 // init NSP runtime
// nsp_load_workflows(mem);    // load workflow table from memory
```

### 5.3 Integration Point: Phase A

Phase A (reflection + evaluation + discovery, `seedcogd/main.c:1718-1843`) is the best candidate for the first pilot. The current implementation:

1. Builds 3 thread structs with hard-coded prompts (`refl_prompts[cycle%4]`, `law_prompts[cycle%4]`, `disc_prompts[cycle%4]`)
2. Delegates to peers or runs locally based on `seed_cog_delegate_should_delegate()`
3. Spawns 1-3 threads depending on backend availability
4. Each thread calls `run_phase()` which calls `chat()` -> `seed_llm_pool_dispatch()`

With NSL, the pilot replaces this with:

```c
// Conceptual: NSP-driven Phase A
nsp_plan_t *plan = nsp_compile(
    "(reflect :on (:recall :query (:type observation) "
    "                     :from \"cognitive/this-node\" :limit 16)"
    "          :depth 2 :strategy \"pattern.detect\")");
nsp_result_t *result = nsp_execute(plan, pool);
```

The phase variable prompts (`refl_prompts[cycle%4]`) become workflow parameters:

```sxl
(:type workflow :id "wf-reflection"
 :trigger (:schedule :every 1 :cycles)
 :params ((:name "rotation" :type int :default 0))
 :procedure
   ;; Use params.rotation to select from prompt variants
   ...)
```

### 5.4 Integration Point: Phase K (Meta-Cognition)

Phase K (`seedcogd/main.c:2609-2780`) is the most self-contained phase: it performs three tasks (confidence calibration, knowledge gap detection, strategy evaluation) using only local computation (no LLM calls). This makes it an ideal early candidate because the NSL workflow can be executed entirely on `NSP_BACKEND_SYMBOLIC`.

The current C code:
```c
if (cycle % 11 == 0 && cycle > 0) {
    // 1. Confidence calibration (lines 2625-2645)
    // 2. Knowledge gap detection (lines 2648-2682)
    // 3. Strategy evaluation (lines 2686-2728)
    // 4. Build and publish SXL (lines 2730-2780)
}
```

The NSL workflow equivalent:
```sxl
(:type workflow :id "wf-metacognition"
 :trigger (:schedule :every 11 :cycles)
 :procedure
   (:seq :steps (
     ;; Gather prediction history
     (:recall :query (:type prediction)
              :from "cognitive/this-node/predictions"
              :limit 50)
     ;; Gather domain coverage
     (:recall :query (:type observation)
              :from "cognitive/this-node"
              :limit 128)
     ;; Evaluate strategies
     (:evaluate :what (:2) :against (:1) :metric "strategy_success")
     ;; Build metacognition SXL
     (:merge :a (:1) :b (:3) :strategy "metacognition_report")
     ;; Store result
     (:store :where "cognitive/this-node/metacognition" :what (:4))
   )))
```

### 5.5 Integration Point: The Lua Brain Cycle

The Lua brain cycle in `lua/agents/cognitive/brain.lua` runs phases H-Q on a 10-second tick. Integration here follows the same workflow-replacement pattern but through the Lua API:

```lua
-- Current (brain.lua:201):
local function cognitive_tick()
    cycle_count = cycle_count + 1
    -- ... hard-coded phase checks ...

-- Target:
local function cognitive_tick()
    cycle_count = cycle_count + 1
    -- NSL workflow scheduler replaces individual phase checks
    local ready = nsp.schedule_ready(cycle_count)
    for _, wf in ipairs(ready) do
        local result = nsp.execute(wf.procedure_sxl)
        -- store result via seed.mem.put or bus publish
    end
end
```

The 25 Lua helper modules (`lua/helpers/`) will not be removed; they become the **implementation bodies** that NSL procedures call into. For example, the `(reflect)` primitive dispatches to `lua/helpers/reflection.lua` when running in a Lua context, or to `sst_execute(SST_OP_REFLECT, ...)` when running in a C context.

### 5.6 Lua NSP Bindings

The NSP runtime is exposed to Lua through the same binding mechanism used by SXP (`src/libagent/src/sxp_bindings.c`):

```c
// Conceptual: NSP Lua bindings in src/libagent/src/nsp_bindings.c
static int l_nsp_compile(lua_State *L) {
    const char *nsl_expr = luaL_checkstring(L, 1);
    nsp_plan_t *plan;
    seed_err_t e = nsp_compile(nsl_expr, &plan);
    // ... convert to Lua table ...
}

static int l_nsp_execute(lua_State *L) {
    nsp_plan_t *plan = /* extract from Lua userdata */;
    nsp_result_t *result;
    seed_err_t e = nsp_execute(plan, &g_pool);
    // ... return result as SXL string ...
}

static int l_nsp_schedule(lua_State *L) {
    int cycle = luaL_checkinteger(L, 1);
    // ... return table of ready workflow IDs ...
}
```

Registered in `src/libagent/src/bindings.c` (the master binding table) as `seed.nsp.compile`, `seed.nsp.execute`, `seed.nsp.schedule`.

---

## 6. libsexpr Integration — Symbolic Foundation

Every NSL primitive relies on libsexpr for data representation and basic operations. This section documents which libsexpr components each primitive group depends on.

### 6.1 Parser Dependency

All 33 primitives depend on `seed_sx_parse()` from `src/libsexpr/src/sexpr.c`. The NSL parser is a thin wrapper that:

1. Calls `seed_sx_parse()` to produce an arena AST
2. Validates the top-level form is a recognized primitive name
3. Checks keyword argument signatures against the primitive table
4. Recursively validates nested NSL sub-expressions (for `:seq`, `:par`, `:branch`, `:iterate`)

```c
// Conceptual: NSL validator wrapper
seed_err_t nsp_validate(seed_sx_arena_t *arena, seed_sx_ref_t root,
                         nsp_primitive_t *out_prim, seed_err_ctx_t *err) {
    // Parse first (reuses existing parser)
    seed_err_t e = seed_sx_parse(arena, raw_sxl, &root, err);
    if (e != SEED_OK) return e;

    // Extract primitive name from first element
    seed_sx_ref_t first = seed_sx_car(arena, root);
    if (!is_primitive_name(arena, first, out_prim))
        return SEED_ERR(err, SEED_SCHEMA_FIELD_TYPE, "unrecognized NSL primitive");

    // Validate keyword arguments match primitive signature
    return nsp_validate_args(arena, root, *out_prim, err);
}
```

### 6.2 Transform Dependency

Primitives from Group 8 (Transformation) and Group 5 (Comparison) map directly to libsexpr transform functions:

| NSL Primitive | libsexpr Function | File |
|---------------|-------------------|------|
| `compare` | `sxp_oper_compare()` | `src/libsexpr/src/transform.c:182` |
| `merge` | `sxp_oper_merge()` | `src/libsexpr/src/transform.c:218` |
| `split` | `sxp_oper_split()` | `src/libsexpr/src/transform.c:220` |
| `criticise` | `sxp_oper_criticise()` | `src/libsexpr/src/transform.c:222` |

### 6.3 Confidence Dependency

Primitives from Group 7 (Confidence) map to `sxp_confidence_propagate()`:

```c
// src/libsexpr/src/confidence.c
double sxp_confidence_propagate(sxp_propagation_rule_t rule,
                                 const double *premises, size_t n,
                                 double prior, double likelihood,
                                 double marginal);
```

From `src/libsexpr/include/seed/sexpr.h:226-229`. The 5 propagation rules provide the mathematical foundation for `(propagate)`, `(reinforce)`, and `(decay)`.

### 6.4 Query Dependency

Primitives from Group 3 (Query) map to SXP query functions:

```c
// src/libsexpr/src/query.c
size_t sxp_query_count(const seed_sx_arena_t *a, const sxp_query_t *q);
size_t sxp_query_find(const seed_sx_arena_t *a, const sxp_query_t *q,
                       seed_sx_ref_t *out, size_t out_cap);
size_t sxp_traverse(const seed_sx_arena_t *a, seed_sx_ref_t root,
                     seed_sx_visitor_t visitor, void *user_data);
```

From `src/libsexpr/include/seed/sexpr.h:211-215`.

---

## 7. SST Integration — Operator Abstraction

The Solbian Symbolic Transformer (`src/seed-transformer/`) provides the CABI layer that NSL composite operators map onto.

### 7.1 Operator Mapping

The 22 SST operators (`src/seed-transformer/include/sst.h:24-42, 70-78, 86-109`) provide a direct execution target for NSL composites. The mapping table in ARCHITECTURE.md 2.3 shows the correspondence. At runtime, when the NSP dispatcher assigns a primitive to `NSP_BACKEND_SST`, it calls:

```c
seed_err_t sst_execute(sst_operator_t op,
                        sst_node_t **inputs, int n_inputs,
                        sst_node_t **out, seed_err_ctx_t *err);
```

From `src/seed-transformer/include/sst.h:139-141`. The NSP runtime constructs `sst_node_t` inputs from the primitive's SXL arguments:

```c
// Conceptual: NSP -> SST bridge
static seed_err_t nsp_dispatch_sst(nsp_primitive_t prim,
                                    nsop_t *node,
                                    sst_node_t **out) {
    sst_operator_t sst_op = nsp_primitive_to_sst_op(prim);
    sst_node_t *inputs[4];
    int n = nsp_sxl_to_sst_nodes(node->args, inputs, 4);
    return sst_execute(sst_op, inputs, n, out, NULL);
}
```

### 7.2 Workspace Access

The SST workspace (`sst_workspace_t` from `src/seed-transformer/include/sst.h:113-127`) is the transient memory that NSL primitives read from and write to during execution. The NSP runtime maps workspace slots:

| NSL Primitive | SST Workspace Field |
|---------------|---------------------|
| `(recall :type hypothesis ...)` | `active_hypotheses[]` |
| `(recall :type observation ...)` | `recent_observations[]` |
| `(store :what (:type goal ...))` | `current_goal` |
| `(store :what (:type plan ...))` | `current_plan` |
| `(bind ...)` | `confidence_map` (relation edges) |

---

## 8. ACL Requirements and Safety Boundaries

Per the sapling integration model (`~/solbian/sapling/INTEGRATION.md`), NSLP starts at the `external` role and graduates to `core`.

### 8.1 Prototype Phase (external role)

| Resource | Access | Rationale |
|----------|--------|-----------|
| T1 bus topic `org.seed.cog.nsl.*` | Publish/subscribe | Isolated namespace, no impact on control plane |
| T1 bus topic `org.seed.memory.*` | Read-only (constrained) | Query existing state; cannot mutate |
| T1 bus topic `org.seed.symbol.*` | Read-only | Read symbolic statements |
| `cognitive/this-node` partitions | Read-only via libsmem | Query for primitives; writes blocked |
| LLM backends | Via `seed_llm_chat()` | Uses same pool as cognitive cycle |
| SST runtime | Via `sst_execute()` | Sandboxed operator execution |
| seedreasond policy | Via `seed_policy_eval()` | Read-only policy queries |

### 8.2 Graduated Phase (core role)

Graduation criteria (from `~/solbian/sapling/INTEGRATION.md`):

1. NSLP has run as a prototype for at least one full release cycle of `~/seed-dev/`
2. NSL grammar is stable and versioned
3. NSP compiler passes the test suite
4. At least one cognitive cycle phase is successfully replaced by an NSL workflow
5. Graduation is recorded in `~/solbian/LOG.md`

After graduation, the ACL is upgraded to `core`, granting:
- Write access to `cognitive/this-node/*` partitions
- Publish to `org.seed.memory.*` topics
- Direct access to actuator bus topics (via safety policy gate)
- Registration of new workflows in the cognitive cycle

---

## 9. Graduation Path

The graduation path from sapling prototype to first-class S.E.E.D. component follows the canonical process in `~/solbian/sapling/INTEGRATION.md`.

### 9.1 Destination Options

| Destination | When | What moves |
|-------------|------|------------|
| `~/seed-dev/src/` | NSLP is stable, tests pass, integrated with seedcogd | C source (`nsp_*.c`) moves to `~/seed-dev/src/nsp/` |
| `~/seed-dev/lua/agents/cognitive/brain.lua` | NSL workflow scheduler replaces phase selectors | Lua bindings + workflow table |
| `~/solbian/codex/` | NSL language spec is stable | SPEC.md moves to `~/solbian/codex/solbian/` |

### 9.2 Milestones

| Milestone | Criteria | Evidence |
|-----------|----------|----------|
| M1: Prototype | NSP compiles and executes one NSL expression end-to-end | Test run against a local S.E.E.D. instance |
| M2: Phase pilot | One hard-coded phase replaced by NSL workflow | Phase K runs as NSL workflow; C code is fallback |
| M3: Test suite | Full test coverage for parser, graph, optimizer, runtime | `tests/` directory passes |
| M4: Integration | NSL workflows run alongside or replace 4+ phases | seedcogd cycle uses nsp_schedule() |
| M5: Graduation | All criteria met, recorded in LOG.md | ACL role upgraded to `core` |

---

## 10. Safety Considerations

### 10.1 Primitive Sandboxing

Each NSL primitive is sandboxed by:
- **Resource limits**: max cells (`SEED_SEXPR_MAX_CELLS = 4096`), max depth (`SEED_SEXPR_MAX_DEPTH = 32`), max input (`SEED_SEXPR_MAX_INPUT = 65536`)
- **Time limits**: primitives in `NSP_BACKEND_SYMBOLIC` have a 2ms budget; neural primitives have the same timeout as the LLM pool (configurable via `SEED_LLM_TIMEOUT`)
- **Side-effect isolation**: only `(store)`, `(forget)`, and `(bind)` can write to persistent memory; all other primitives are read-only or produce ephemeral results

### 10.2 Workflow Safety

- **No infinite loops**: `(iterate)` is bounded by `max_iterations` (default 100) and `max_wallclock` (default 30s)
- **No cross-cycle memory leaks**: continuations expire via TTL field (default 3600s)
- **No unbounded parallelism**: the `:par` primitive is limited to `MAX_BRANCHES` (default 8), matching the maximum concurrent backend count
- **Policy gate**: all NSL execution passes through `policy_gate_allow()` (from `seedcogd/main.c:69-100`) before the plan is executed

### 10.3 Integration Safety

NSL workflows that replace cognitive cycle phases inherit the same safety properties as the phases they replace:
- They cannot bypass Sprout's safety policy (R1-R8 on firmware + host-side gate in `~/robot-dev/src/neocortex/safety.py`)
- They cannot write to long-term memory partitions without `core` ACL role
- Their outputs pass through the existing contradiction check (Phase B) before being accepted into the world model

---

## 11. References

- `~/seed-dev/src/libbus/src/t1.c` — T1 bus implementation
- `~/seed-dev/src/libbus/src/bus.c` — Bus publish/subscribe/request
- `~/seed-dev/src/libsmem/src/sxl.c` — SXL query wrappers
- `~/seed-dev/src/libsmem/include/seed/smem.h` — Memory API
- `~/seed-dev/src/libseedllm/src/dispatch.c` — Capability-based routing
- `~/seed-dev/src/libseedllm/src/pool.c` — Backend pool management
- `~/seed-dev/src/libseedllm/src/consensus.c` — Multi-model consensus
- `~/seed-dev/src/libsexpr/src/transform.c` — SXP transform operations
- `~/seed-dev/src/libsexpr/src/confidence.c` — Confidence propagation
- `~/seed-dev/src/libsexpr/src/query.c` — SXP query engine
- `~/seed-dev/src/libsexpr/src/validate.c` — SXP validator
- `~/seed-dev/src/seed-transformer/src/sst_execute.c` — SST operator execution
- `~/seed-dev/src/seed-transformer/include/sst.h` — SST workspace and types
- `~/seed-dev/src/seedcogd/main.c` — Cognitive daemon main loop
- `~/seed-dev/src/seedcogd/delegate.c` — Cross-node delegation
- `~/seed-dev/src/seedreasond/src/evaluate.c` — Policy evaluation
- `~/seed-dev/src/libagent/src/sxp_bindings.c` — SXP Lua bindings (model for NSP bindings)
- `~/seed-dev/lua/agents/cognitive/brain.lua` — Lua brain cycle
- `~/seed-dev/schemas/.sref/v1/sxl.sref` — SXL schema
- `~/solbian/sapling/INTEGRATION.md` — Sapling integration model
- `~/solbian/sapling/README.md` — Sapling overview
