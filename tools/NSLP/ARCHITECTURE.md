# NSLP Architecture — Neuro-computational SEED Symbolic Language Processor

> **Status**: Draft 0.1.0  
> **Version**: 2026-07-16  
> **ACL role**: `external` (sapling prototype)  
> **Upstream home**: `~/solbian/tools/NSLP/`  
> **Canonical references**: `~/seed-dev/docs/cognition/SXL_LANGUAGE_SPECIFICATION.md`, `~/seed-dev/docs/architecture/SST_ARCHITECTURE.md`, `~/seed-dev/docs/architecture/COGNITIVE_ENGINE_SPEC.md`

---

## 1. Overview

NSLP is the **compiler, optimizer, and runtime** for the NSL (Neural Symbolic Language) instruction set. It composes the 33 NSL cognitive primitives into executable operator graphs, optimizes them for available backends, and dispatches them across S.E.E.D.'s neural and symbolic execution substrates.

The system has three components:

| Component | Role | Substrate |
|-----------|------|-----------|
| **NSL** | Cognitive instruction set (ISA) | S-expressions parsed by `libsexpr` |
| **NSP compiler** | Expression -> primitive graph -> optimized plan | C / Lua |
| **NSP runtime** | Graph executor, continuation manager, channel system | C daemon + Lua orchestration |

NSL is a **control-plane language**: it describes *what to do* with cognitive state. SXL is the corresponding **data-plane language**: it describes *what is believed, intended, or known*. The two are complementary and share the same S-expression substrate defined in `~/seed-dev/docs/cognition/SXL_LANGUAGE_SPECIFICATION.md` and implemented by `~/seed-dev/src/libsexpr/`.

---

## 2. The 4-Layer ISA Stack

The NSLP architecture defines cognition across four layers of abstraction, from concrete symbolic representations to executable workflows:

```
 Layer 4: Cognitive Workflows
   (composed NSL procedures; replace hard-coded cycle phases)
       |
       |  compose: sequence, parallel, branch, iterate, call/return
       v
 Layer 3: SXL Composite Operators
   (high-level verbs: reflect, plan, learn, simulate, evaluate, ...)
       |
       |  compile: NSL primitive graph -> backend dispatch
       v
 Layer 2: NSL Primitives
   (33 irreducible primitives across 11 groups;
    the cognitive ISA — bind, match, branch, derive, ...)
       |
       |  operate on
       v
 Layer 1: Symbolic Objects
   (SXL entities stored in libsmem partitions;
    the data that primitives read, write, and transform)
```

### 2.1 Layer 1 — Symbolic Objects (SXL Data Plane)

The ground layer is the existing SXL entity model defined in `~/seed-dev/schemas/.sref/v1/sxl.sref` and `~/seed-dev/src/libsexpr/include/seed/sexpr.h`. Every cognitive fact is an S-expression with the following canonical shape:

```sxl
(:type belief :id "b-001" :timestamp 1720649591123456789
 :confidence 0.82 :creator "did:seed:nodeA:agent-cognitive"
 :schema "seed.sxl/v1"
 :provenance {:source "observation" :attribution "perception"}
 :relations [{:to "e-001" :label "evidence" :weight 0.9}]
 :status active
 :version 1
 :content {:hypothesis "Refactoring auth reduces latency by 20%"
           :evidence ("bench-001" "prof-002")})
```

The 26+ entity types defined in the SXL schema (goal, belief, plan, reflection, knowledge, observation, hypothesis, skill, context, memory, experience, prediction, simulation, intent, task, capability, resource, evidence, contradiction, meaning, entity, language-extension, scene, perceptual_state, decision, decision_outcome) are the **operands** upon which NSL primitives act.

These objects are stored in:
- **libsmem** (`~/seed-dev/src/libsmem/`) — SQLite-backed symbolic memory with FTS5, append-only `.sref` log, partition model (`cognitive/this-node/*`)
- **SST workspace** (`~/seed-dev/src/seed-transformer/include/sst.h:113-127`) — in-memory transient workspace with 16 hypothesis slots, 32 observation slots, 16 question slots, 8 agent slots, and a reasoning graph
- **seedcogd ring buffer** (`~/seed-dev/src/seedcogd/main.c:57-103`) — 80-entry capacity-bounded working memory with confidence decay

### 2.2 Layer 2 — NSL Primitives (Cognitive ISA)

The NSL instruction set consists of **33 primitives** organized into **11 functional groups**. Every primitive passes the *irreducibility test*: it cannot be expressed as a composition of simpler NSL primitives. The set is the smallest complete algebra of cognitive computation.

#### Group 1: Perception (3 primitives)

| Primitive | Signature | Semantics |
|-----------|-----------|-----------|
| `observe` | `(observe :source string :into partition)` | Convert raw input to SXL observation, store in partition |
| `extract` | `(extract :from sxl :selector pattern)` | Extract substructure from SXL via pattern match |
| `classify` | `(classify :what sxl :ontology string)` | Tag SXL entity with ontology category |

Corresponds to: `lua/helpers/sxl_translator.lua` (NL -> SXL), `libsexpr/sexpr.c` (parse), `seedcogd/main.c` Phase G (vision observation).

#### Group 2: Memory (4 primitives)

| Primitive | Signature | Semantics |
|-----------|-----------|-----------|
| `store` | `(store :what sxl :where partition)` | Write SXL entity to persistent partition |
| `recall` | `(recall :query sxl :from partition :limit n)` | Retrieve matching entities from partition |
| `forget` | `(forget :target id :reason string)` | Mark entity for decay, set status to abandoned |
| `bind` | `(bind :a id :b id :label relation_type :weight float)` | Create a directed relation between two entities |

Corresponds to: `src/libsmem/src/sxl.c` (SXL scan/get wrappers), `src/seedcogd/main.c:298-399` (memory load/store), `sst_remember()` / `sst_retrieve()` from `sst.h:148-154`.

#### Group 3: Query (3 primitives)

| Primitive | Signature | Semantics |
|-----------|-----------|-----------|
| `match` | `(match :pattern sxl :against sxl)` | Structural pattern match: does SXL fit pattern? |
| `filter` | `(filter :set sxl[] :predicate sxl)` | Return subset matching predicate |
| `join` | `(join :left sxl[] :right sxl[] :on relation)` | Relational join across entity sets |

Corresponds to: `src/libsexpr/src/query.c` (sxp_query_count, sxp_query_find).

#### Group 4: Inference (4 primitives)

| Primitive | Signature | Semantics |
|-----------|-----------|-----------|
| `derive` | `(derive :from sxl[] :using rule :confidence float)` | Deduce new SXL from premises |
| `abduce` | `(abduce :observation sxl :explain sxl[])` | Generate best explanation for observation |
| `induce` | `(induce :cases sxl[] :target type)` | Generalize pattern from examples |
| `analogize` | `(analogize :source sxl :target sxl :domain string)` | Map structure from source to target domain |

Corresponds to: `src/seed-transformer/src/sst_execute.c` (SST_OP_INFER, SST_OP_GENERALISE), `src/libseedllm/src/consensus.c` (multi-model consensus), `src/seedreasond/src/evaluate.c` (symbolic policy eval).

#### Group 5: Comparison (3 primitives)

| Primitive | Signature | Semantics |
|-----------|-----------|-----------|
| `compare` | `(compare :a sxl :b sxl :lens string)` | Structural comparison along dimension |
| `similarity` | `(similarity :a sxl :b sxl :metric string)` | Compute similarity score |
| `contradicts` | `(contradicts :a sxl :b sxl) -> bool` | Check for logical contradiction |

Corresponds to: `src/libsexpr/src/transform.c` (`sxp_oper_compare`), `src/seedcogd/main.c:1845-1868` (Phase B contradiction check), `memory_similarity()` (trigram overlap).

#### Group 6: Control Flow (5 primitives)

| Primitive | Signature | Semantics |
|-----------|-----------|-----------|
| `sequence` | `(seq :steps primitive[] :state sxl)` | Execute primitives in order, passing state |
| `parallel` | `(par :branches primitive[] :merge string)` | Execute concurrently, merge results |
| `branch` | `(branch :condition sxl :then primitive :else primitive)` | Conditional execution |
| `iterate` | `(iterate :until sxl :body primitive :state sxl)` | Repeated execution until condition met |
| `call` | `(call :procedure id :args sxl[])` | Invoke a named NSL procedure |

Corresponds to: SST_OP_SEQUENCE (19), SST_OP_PARALLEL (20) from `src/seed-transformer/include/sst.h:106-108`.

#### Group 7: Confidence (3 primitives)

| Primitive | Signature | Semantics |
|-----------|-----------|-----------|
| `propagate` | `(propagate :rule string :premises sxl[] :prior float)` | Compute resultant confidence |
| `reinforce` | `(reinforce :target sxl :delta float)` | Adjust confidence upward |
| `decay` | `(decay :target sxl :rate float :floor float)` | Reduce confidence over time |

Corresponds to: `src/libsexpr/src/confidence.c` (`sxp_confidence_propagate` — deductive, Bayesian, DS, fuzzy, decay rules), `src/seedcogd/main.c:318-323` (confidence decay).

#### Group 8: Transformation (4 primitives)

| Primitive | Signature | Semantics |
|-----------|-----------|-----------|
| `merge` | `(merge :a sxl :b sxl :strategy string)` | Combine two entities into one |
| `split` | `(split :what sxl :criteria string[])` | Decompose entity along criteria |
| `abstract` | `(abstract :from sxl[] :level int)` | Generalize from specifics, dropping detail |
| `specialise` | `(specialise :what sxl :context sxl)` | Adapt general to specific context |

Corresponds to: `src/libsexpr/src/transform.c` (`sxp_oper_merge`, `sxp_oper_split`), SST_OP_DECOMPOSE (13), SST_OP_COMPOSE (14), SST_OP_GENERALISE (17).

#### Group 9: Planning (2 primitives)

| Primitive | Signature | Semantics |
|-----------|-----------|-----------|
| `decompose` | `(decompose :goal sxl :into sxl[])` | Break goal into sub-goals |
| `schedule` | `(schedule :steps sxl[] :constraints sxl[])` | Order steps respecting constraints |

Corresponds to: SST_OP_DECOMPOSE, SST_OP_PLAN (5), `src/seedcogd/main.c:1854-1868` (plan generation), `lua/helpers/goal_manager.lua` (hierarchical goal decomposition).

#### Group 10: Evaluation (3 primitives)

| Primitive | Signature | Semantics |
|-----------|-----------|-----------|
| `evaluate` | `(evaluate :what sxl :against sxl[] :metric string)` | Score entity against evidence |
| `verify` | `(verify :claim sxl :evidence sxl[]) -> bool` | Verify claim against evidence |
| `criticise` | `(criticise :target sxl :lens string)` | Generate adversarial critique |

Corresponds to: SST_OP_EVALUATE (6), SST_OP_VERIFY (7), SST_OP_CRITICISE (12), `src/libsexpr/src/transform.c` (`sxp_oper_criticise`), `src/seedreasond/src/evaluate.c`.

#### Group 11: Meta-Cognition (2 primitives)

| Primitive | Signature | Semantics |
|-----------|-----------|-----------|
| `reflect` | `(reflect :on sxl :depth int :strategy string)` | Generate meta-cognitive analysis |
| `trace` | `(trace :procedure id :state sxl) -> sxl[]` | Record execution trace for audit/replay |

Corresponds to: SST_OP_REFLECT (11), `lua/helpers/reflection.lua`, `lua/helpers/metacognition.lua`, `src/seedcogd/main.c:1720-1740` (reflection phase), `src/seedcogd/main.c:2620-2780` (meta-cognition phase K).

### 2.3 Layer 3 — SXL Composite Operators

SXL Composite Operators are the high-level verbs that appear in cognitive cycle prompts and cognitive agent code. Each composite is a named NSL procedure — a composition of primitives with a documented signature, confidence model, and error semantics.

The existing SST operator enum (`src/seed-transformer/include/sst.h:86-109`) defines 22 operators that are natural candidates for NSL composite procedures:

| SST Operator | NSL Composite | Primary Primitives Used |
|-------------|---------------|------------------------|
| `SST_OP_OBSERVE` | `(observe)` | observe, extract, classify |
| `SST_OP_COMPARE` | `(compare)` | compare, similarity, contradicts |
| `SST_OP_INFER` | `(infer)` | derive, abduce |
| `SST_OP_SIMULATE` | `(simulate)` | sequence, iterate, evaluate |
| `SST_OP_PREDICT` | `(predict)` | derive, analogize, evaluate |
| `SST_OP_PLAN` | `(plan)` | decompose, schedule, sequence |
| `SST_OP_EVALUATE` | `(evaluate)` | evaluate, verify |
| `SST_OP_VERIFY` | `(verify)` | verify, contradicts |
| `SST_OP_RETRIEVE` | `(retrieve)` | match, recall |
| `SST_OP_REMEMBER` | `(remember)` | store, bind |
| `SST_OP_FORGET` | `(forget)` | forget, decay |
| `SST_OP_REFLECT` | `(reflect)` | reflect, trace, derive |
| `SST_OP_CRITICISE` | `(criticise)` | criticise, compare |
| `SST_OP_DECOMPOSE` | `(decompose)` | decompose, split |
| `SST_OP_COMPOSE` | `(compose)` | merge, specialise |
| `SST_OP_LEARN` | `(learn)` | induce, store, reinforce |
| `SST_OP_GENERALISE` | `(generalise)` | abstract, induce |
| `SST_OP_RECONCILE` | `(reconcile)` | compare, merge, propagate |
| `SST_OP_SEQUENCE` | sequence primitive | (composition rule) |
| `SST_OP_PARALLEL` | parallel primitive | (composition rule) |
| `SST_OP_OPTIMISE` | `(optimise)` | evaluate, iterate, merge |
| `SST_OP_TRAIN` | `(train)` | induce, store, reinforce |

### 2.4 Layer 4 — Cognitive Workflows

Cognitive Workflows are the highest level of the ISA stack. A workflow is a **named, executable NSL procedure** that replaces one or more hard-coded phases in the existing cognitive cycle. Unlike the current fixed-phase loop in `seedcogd/main.c` (phases A-L, hard-coded frequencies and order), a workflow is dynamically selected based on current state.

Each workflow is a first-class SXL entity with:
- `:type workflow` — type discriminator
- `:id` — unique identifier (ULID)
- `:procedure` — NSL expression body (the composition of primitives)
- `:trigger` — condition or schedule for activation
- `:state` — current execution state (idle, running, suspended, completed, failed)
- `:confidence` — expected success rate (updated from execution history)
- `:cost_estimate` — expected compute cost (updated by runtime)
- `:backend_hints` — preferred backends for sub-operations

Example workflow for the reflection composite:

```sxl
(:type workflow :id "wf-reflect-v1"
 :version 1
 :confidence 0.85
 :status active
 :trigger (:schedule :every 1 :cycles)
 :procedure
   (:seq :steps (
     ;; Step 1: Gather recent observations
     (:recall :query (:type observation :cycle (:within 5))
              :from "cognitive/this-node"
              :limit 16)
     ;; Step 2: Detect patterns (parallel)
     (:par :branches (
       (:derive :from (:1) :using "pattern.detect"
                :confidence 0.70)
       (:compare :a (:1) :b (:previous-reflection)
                 :lens "change")
     ) :merge "union")
     ;; Step 3: Generate insight
     (:derive :from (:2) :using "insight.synthesize"
              :confidence 0.75)
     ;; Step 4: Store result
     (:store :where "cognitive/this-node/reflection"
             :what (:3))
   ))
 :cost_estimate (:compute 1.0 :llm 0.5)
 :backend_hints (:derive "hybrid" :compare "symbolic"))
```

---

## 3. The NSP Compiler Pipeline

The NSP compiler transforms NSL expressions into executable primitive graphs through four stages:

```
 NSL Expression (SXL)
       |
       |  Stage 1: Parse
       v
   Abstract Syntax Tree (libsexpr arena)
       |
       |  Stage 2: Primitive Graph Construction
       v
   Primitive Operator Graph (DAG of nsop_t nodes)
       |
       |  Stage 3: Optimization Passes
       v
   Optimized Graph (backend-tagged nsop_t nodes)
       |
       |  Stage 4: Backend Dispatch
       v
   Executable Plan (nsplan_t with per-operator backend assignments)
```

### 3.1 Stage 1 — Parse

The front-end parser reuses `libsexpr` directly. The function `seed_sx_parse()` (`src/libsexpr/src/sexpr.c`) parses the NSL S-expression into an arena-allocated AST. If the S-expression does not match the NSL grammar (unrecognized primitive, invalid signature, type mismatch), the parser returns a structured error with location and expected forms.

The NSL grammar is a strict subset of SXL syntax:
- Top-level form is always `(:primitive-name :keyword value ...)`
- Nested forms use `(:seq)`, `(:par)`, `(:branch)` for composition
- Variables use the `?name` convention for pattern variables
- SXL entity expressions are valid as data literals

Validation is performed by `sxp_validate()` (`src/libsexpr/src/validate.c`) extended with NSL-specific type checking from a compiled NSL grammar table.

### 3.2 Stage 2 — Primitive Graph Construction

The parser output is a tree. Stage 2 linearizes the tree into a **directed acyclic graph** of `nsop_t` nodes:

```c
typedef struct nsop_s {
    nsp_primitive_t   primitive;   /* enum from NSL primitive group */
    seed_sx_ref_t     args;        /* SXL keyword arguments */
    int               n_inputs;    /* number of inputs */
    struct nsop_s    *inputs[];   /* incoming edges */
} nsop_t;

typedef struct nsgraph_s {
    nsop_t          **nodes;      /* all nodes in execution order */
    int               n_nodes;
    nsop_t           *root;       /* output node (result) */
    int               n_externals; /* external data references */
    char            *externals[]; /* partition paths / entity ids */
} nsgraph_t;
```

The graph construction follows these rules:
- `:seq` steps are serialized as a chain
- `:par` branches are emitted as independent sub-graphs with a merge point
- `:branch` produces a conditional fork (left and right sub-graphs)
- `:iterate` produces a loop sub-graph with an exit condition
- `:call` produces a graph expansion from the called procedure's body

### 3.3 Stage 3 — Optimization Passes

The optimizer applies a sequence of transform passes, each implemented as a function `void optimize(nsgraph_t *g)`:

#### Pass 1: Dead Primitive Elimination (DPE)
Removes primitives whose outputs are never consumed. A `store` whose result is discarded by a subsequent `merge` with no side-effect path is elided. This mirrors LLVM's DCE but operates on cognitive semantics: a `reflect` whose result is never stored or used is removed.

#### Pass 2: Common Subexpression Elimination (CSE)
Identifies identical primitive invocations (same primitive, same arguments, same inputs) and merges them. If two branches in a `:par` block both call `(similarity :a X :b Y ...)`, the second reuses the first's result.

#### Pass 3: Parallelization Analysis
Analyzes data dependencies to identify sub-graphs that can execute concurrently. Uses a simple topological analysis: any two nodes where neither depends on the other's output can be parallelized. Tags nodes with `NSP_EXEC_PARALLEL` where the backend pool (`g_pool_n_backends` from `seedcogd/main.c:2946`) has capacity.

#### Pass 4: Backend-Aware Operator Fusion
Fuses sequences of primitives that the same backend can execute more efficiently as a unit. For example, `(match ...)` followed by `(filter ...)` on the same dataset can be fused into a single LLM call when dispatched to the `hybrid` backend. Fusion rules are backend-specific and declared in a backend capability table.

#### Pass 5: Constant Folding
Evaluates primitives whose inputs are all constant SXL entities at compile time. `(similarity :a (:type constant ...) :b (:type constant ...))` is evaluated once and replaced with the result.

### 3.4 Stage 4 — Backend Dispatch

The final stage assigns each primitive to an execution backend. The dispatcher uses the same capability-based routing as `src/libseedllm/src/dispatch.c:47-71` but at primitive granularity rather than intent granularity.

```c
typedef enum {
    NSP_BACKEND_SYMBOLIC,   /* libsexpr / seedreasond — pure symbolic eval */
    NSP_BACKEND_NEURAL,     /* libseedllm — LLM inference */
    NSP_BACKEND_HYBRID,     /* neural + symbolic validation */
    NSP_BACKEND_NATIVE,     /* native C function */
    NSP_BACKEND_SST,        /* SST runtime (seed-transformer) */
    NSP_BACKEND_DEFERRED,   /* deferred to continuation / external peer */
} nsp_backend_t;
```

The dispatch decision for each primitive considers:
1. **Primitive-backend capability matrix** — which backends implement which primitives
2. **Current backend health** — read from `seed_llm_pool_stats()` (from `src/libseedllm/src/pool.c`)
3. **Predicted latency and cost** — EMA-tracked per-primitive-per-backend from runtime history
4. **Confidence required** — high-confidence tasks prefer symbolic; generative tasks prefer neural
5. **Data locality** — primitives on the same entity set prefer the same backend

The output of Stage 4 is a `nsplan_t`:

```c
typedef struct nsplan_s {
    nsgraph_t       *graph;       /* optimized primitive graph */
    nsp_backend_t   *assignments; /* per-node backend assignment */
    int              n_nodes;
    double           estimated_cost;   /* total compute cost estimate */
    double           estimated_confidence; /* expected output confidence */
} nsplan_t;
```

---

## 4. The NSP Runtime

The runtime executes optimized plans across the available backends, manages continuations for long-running or interactive primitives, and provides the channel system for cross-primitive communication.

### 4.1 Graph Executor

The executor walks the optimized graph in topological order, dispatching each primitive to its assigned backend:

```
for each node in plan.graph->nodes (topological order):
    if node.is_parallel and n_backends_available >= 2:
        spawn thread(s) for parallel sub-graph
    else:
        result = backend_dispatch(node.backend, node.primitive, node.inputs)
        node.output = result
plan.result = graph.root->output
```

The dispatch function `backend_dispatch()` routes to:
- **`NSP_BACKEND_SYMBOLIC`** -> `sxp_oper_*` functions from `src/libsexpr/src/transform.c` (merge, split, criticise, compare) or `seed_policy_eval()` from `src/seedreasond/src/evaluate.c`
- **`NSP_BACKEND_NEURAL`** -> `seed_llm_chat()` from `src/libseedllm/` with backend chosen by per-intent routing (`dispatch.c`)
- **`NSP_BACKEND_HYBRID`** -> neural inference followed by symbolic validation via `sxp_validate()`
- **`NSP_BACKEND_NATIVE`** -> direct C function call (e.g., confidence propagation from `src/libsexpr/src/confidence.c`)
- **`NSP_BACKEND_SST`** -> `sst_execute()` from `src/seed-transformer/src/sst_execute.c`
- **`NSP_BACKEND_DEFERRED`** -> continuation management (see 4.2)

### 4.2 Continuation Management

Some primitives cannot complete in a single cycle:
- An `(evaluate)` primitive that requires multiple rounds of LLM consensus
- A `(reflect)` that requires gathering data from peer nodes via `seed_cog_delegate_*` (from `src/seedcogd/delegate.c`)
- An `(iterate)` with an unknown number of steps

The continuation system captures partial state as an SXL entity:

```sxl
(:type continuation :id "cont-001"
 :plan_ref "plan-reflect-v1"
 :resume_at 3    ;; resume at node index 3
 :accumulated (:observations [...] :partial_result "...")
 :created 1720649591123456789
 :ttl 3600       ;; seconds before abandonment
 :status suspended)
```

Continuations are stored in `cognitive/this-node/continuations` partition and checked at the start of each cognitive cycle (analogous to how `seedcogd/main.c` checks predictions at cycle start via `check_predictions()`). The runtime resumes by restoring the graph state and executing from the saved node index.

### 4.3 Channel System

The channel system provides **typed, buffered SXL channels** for communication between primitives executing in parallel. Channels replace ad-hoc shared-state access to the SST workspace.

```c
typedef struct nsp_channel_s {
    char             id[64];        /* channel ULID */
    seed_sx_ref_t   *buffer;        /* ring buffer of SXL entities */
    int              capacity;      /* buffer capacity */
    int              head, tail;    /* ring buffer indices */
    nsp_channel_type_t type;        /* UNICAST, MULTICAST, or PUBSUB */
} nsp_channel_t;
```

- **UNICAST**: single producer, single consumer. Used for `:seq` step passing.
- **MULTICAST**: single producer, multiple consumers. Used for `:par` branch fan-out.
- **PUBSUB**: multiple producers, multiple consumers. Used for cross-primitive event notification.

Channels are registered in the runtime registry and referenced by ID in the primitive graph. A `(parallel)` primitive creates a MULTICAST channel for each branch output, then a merge channel for the join point.

### 4.4 Process Scheduler

The NSP runtime implements a lightweight cooperative scheduler for NSL procedures:

```
 NSP Scheduler                 seedcogd main loop
  ┌───────────────────┐        ┌──────────────────────┐
  │                   │        │                      │
  │  Process Table    │◄──────►│  Phase A: Reflection  │
  │  - ready queue    │  bus   │  Phase B: Contradict  │
  │  - suspended q    │  events│  ...                  │
  │  - completed q    │        │  Phase L: Creativity  │
  │                   │        │                      │
  │  Time-slice: 1    │        │  On each cycle tick: │
  │  cognitive cycle  │        │  nsp_schedule()       │
  │  per process      │        │                      │
  └───────────────────┘        └──────────────────────┘
```

Each NSL process is a `(workflow)` instance with its own continuation state. The scheduler:
1. Checks for ready processes (workflow trigger condition met, or continuation ready to resume)
2. Runs up to `MAX_ACTIVE_PROCESSES` (default 4, matching the 4-agent slot heuristic from the SST workspace)
3. Preempts processes that exceed their time slice (one cycle)
4. Migrates long-running processes to continuation state

---

## 5. How NSL Replaces Hard-Coded Cognitive Cycle Phases

The current cognitive cycle in `seedcogd/main.c` phases A-L and `brain.lua` phases H-Q is hard-coded: phase order, frequency, and dispatch logic are compiled into C and Lua. NSL workflows replace this with **dynamic procedure selection**.

### 5.1 Current Architecture

In `seedcogd/main.c:1718-2925`, the cycle is:

```c
// Phase A (every cycle): parallel reflection + evaluation + discovery
// Phase B (every cycle): contradiction check + plan
// Phase C (every 5): hippocampus consolidation
// Phase D (every cycle): prediction
// ... hard-coded phase ordering in C
```

Each phase has:
- Fixed trigger condition (cycle modulo N)
- Hard-coded prompt text (e.g., `refl_prompts[cycle%4]` at line 1721)
- Fixed backend dispatch (the `chat()` function always goes through pool dispatch)
- No dynamic reordering or substitution

### 5.2 Target Architecture

With NSL, the cognitive cycle becomes a **workflow scheduler**:

```
seedcogd main loop (simplified):
  1. Check continuations — resume suspended workflows
  2. nsp_schedule() — select ready workflows based on triggers
  3. Execute selected workflows via NSP runtime
  4. Collect results, update world model
  5. Repeat
```

Workflow triggers replace modulo arithmetic:
```sxl
;; Reflection workflow trigger: every cycle
(:trigger :schedule :every 1 :cycles)

;; Hippocampus consolidation trigger: every 5 cycles
(:trigger :schedule :every 5 :cycles
          :priority :background)

;; Creativity gate trigger: every 13 cycles
(:trigger :schedule :every 13 :cycles
          :priority :low)

;; Event-driven trigger: on specific bus topic
(:trigger :event "org.seed.observation.sensor.*"
          :priority :high)
```

The workflow selection function `nsp_schedule()` evaluates all registered workflow triggers against current state and returns the set of ready workflows, ordered by priority. This is analogous to how OS schedulers select processes but operates on cognitive state rather than time slices.

### 5.3 Migration Path

The migration from hard-coded phases to NSL workflows is incremental:

1. **Phase 0** (current): All phases hard-coded. NSP runtime exists but is unused by the main cycle.
2. **Phase 1** (pilot): One phase replaced by an NSL workflow (e.g., Phase K Meta-Cognition at `seedcogd/main.c:2620`). The workflow is loaded from a `.sref` file and executed by NSP. The C code for Phase K becomes a fallback.
3. **Phase 2** (partial): 3-4 phases migrated. Workflow selection augments the hard-coded loop.
4. **Phase 3** (full): The main loop is a thin `nsp_schedule()` call. All phases are workflows loaded from the cognitive partition at startup.

---

## 6. Integration Points Summary

| Integration | Mechanism | Key Code References |
|-------------|-----------|---------------------|
| SXL data plane | libsexpr S-expression arena | `src/libsexpr/src/sexpr.c`, `include/seed/sexpr.h` |
| libsmem partitions | NSP primitives call `seed_smem_*` | `src/libsmem/src/sxl.c`, `include/seed/smem.h` |
| SST workspace | NSP reads/writes `sst_workspace_t` | `src/seed-transformer/include/sst.h:113-127` |
| libseedllm backends | `backend_dispatch()` -> `seed_llm_chat()` | `src/libseedllm/src/dispatch.c`, `src/libseedllm/src/pool.c` |
| T1 bus | NSL execution request/reply topics | `src/libbus/src/t1.c`, `src/seedbusbrokerd/` |
| seedcogd cycle | Workflow scheduler replaces phase selectors | `src/seedcogd/main.c:1718-2925` |
| seedreasond policy | NSL `(evaluate)` calls `seed_policy_eval()` | `src/seedreasond/src/evaluate.c` |
| SST operators | Composite operators map to SST_OP_ enums | `src/seed-transformer/src/sst_execute.c` |
| Lua brain | Lua `brain.lua` phases replaced by workflow dispatch | `lua/agents/cognitive/brain.lua` |

---

## 7. Data Flow Example — Full NSL Execution

Below is a concrete walkthrough of an NSL expression entering the pipeline, being compiled, executed, and producing a stored result.

**Input NSL expression** (from a cognitive agent or the scheduler):

```sxl
(:reflect :on (:recall :query (:type observation :status active)
                       :from "cognitive/this-node"
                       :limit 8)
          :depth 2
          :strategy "pattern.detect")
```

**Stage 1 — Parse**: `seed_sx_parse()` produces an AST with three nodes: `(:reflect ...)`, `(:recall ...)`, and the SXL query pattern. The primitive table recognizes `reflect` (Group 11) and `recall` (Group 2).

**Stage 2 — Graph construction**: The compiler produces a 5-node DAG:
1. `recall` — node 0 (input: query pattern)
2. `compare` — node 1 (input: node 0 output, previous reflection)
3. `derive` — node 2 (input: node 0 output, pattern library)
4. `reflect` composite — node 3 (input: node 1, node 2)
5. `store` — node 4 (input: node 3 output, partition path)

**Stage 3 — Optimization**: CSE detects the pattern library is constant; constant folding replaces it. Parallelization analysis marks nodes 1 and 2 as parallel (no dependency between them).

**Stage 4 — Dispatch**:
- Node 0 (`recall`) -> `NSP_BACKEND_NATIVE` -> `seed_smem_scan()` (pure C, no LLM)
- Node 1 (`compare`) -> `NSP_BACKEND_SYMBOLIC` -> `sxp_oper_compare()` (pure C)
- Node 2 (`derive`) -> `NSP_BACKEND_HYBRID` -> LLM + `sxp_validate()`
- Node 3 (`reflect`) -> `NSP_BACKEND_HYBRID` -> composite expansion
- Node 4 (`store`) -> `NSP_BACKEND_NATIVE` -> `seed_smem_entry_put()`

**Runtime execution**: Nodes 1 and 2 execute in parallel (2 backends available). Node 0 completes first. Nodes 1 and 2 complete. Node 3 expands into its own sub-plan. Node 4 stores the final reflection.

**Output**: The reflection SXL is stored in `cognitive/this-node/reflection` and the workflow result is published to `org.seed.cog.workflow.completed`.

---

## 8. File Layout

```
tools/NSLP/
  README.md           — this directory's overview
  ARCHITECTURE.md     — this file
  INTEGRATION.md      — integration with S.E.E.D. components
  SPEC.md             — formal NSL ISA specification (33 primitives, 11 groups)
  src/
    nsp_parser.c      — NSL grammar parser (extends libsexpr)
    nsp_graph.c       — primitive graph construction
    nsp_optimize.c    — optimization passes (DPE, CSE, parallelism, fusion, folding)
    nsp_dispatch.c    — backend-aware operator dispatch
    nsp_runtime.c     — graph executor and continuation manager
    nsp_channel.c     — channel system implementation
    nsp_schedule.c    — workflow scheduler
    nsp_types.h       — NSL/NSP type definitions
    nsp_primitives.h  — primitive table and metadata
  include/
    seed/nsp.h        — public NSP API (compiler + runtime entry points)
  tests/
    test_nsp_parser.c
    test_nsp_graph.c
    test_nsp_optimize.c
    test_nsp_dispatch.c
    test_nsp_runtime.c
  research/
    primitives.md     — derivation of the 33-primitive set
    metabolism.md     — computational metabolism model
    foundations.md    — mathematical foundations of NSL semantics
```

---

## 9. References

- `~/seed-dev/docs/cognition/SXL_LANGUAGE_SPECIFICATION.md` — SXL language spec (Canonical 1.0)
- `~/seed-dev/docs/architecture/SST_ARCHITECTURE.md` — SST architecture (Canonical 1.0)
- `~/seed-dev/docs/architecture/COGNITIVE_ENGINE_SPEC.md` — Cognitive engine 20-domain spec
- `~/seed-dev/src/libsexpr/include/seed/sexpr.h` — SXP C ABI
- `~/seed-dev/src/libsexpr/src/` — SXP implementation (parse, canonicalize, validate, hash, query, transform, confidence)
- `~/seed-dev/src/seed-transformer/include/sst.h` — SST CABI types and operators
- `~/seed-dev/src/seed-transformer/src/sst_execute.c` — SST operator execution engine
- `~/seed-dev/src/seedcogd/main.c` — seedcogd 12-phase C cycle
- `~/seed-dev/lua/agents/cognitive/brain.lua` — Lua brain 12-phase cycle
- `~/seed-dev/lua/helpers/` — 25 Lua cognitive modules
- `~/seed-dev/src/libseedllm/src/dispatch.c` — capability-based backend routing
- `~/seed-dev/src/libseedllm/src/consensus.c` — multi-model consensus
- `~/seed-dev/src/libsmem/src/sxl.c` — SXL-aware memory wrappers
- `~/seed-dev/src/seedreasond/src/evaluate.c` — symbolic policy evaluator
- `~/seed-dev/schemas/.sref/v1/sxl.sref` — canonical SXL schema
- `~/solbian/sapling/INTEGRATION.md` — sapling bus integration model
- `~/solbian/sapling/README.md` — sapling level overview
