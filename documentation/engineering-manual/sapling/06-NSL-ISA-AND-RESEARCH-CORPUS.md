# 06 — NSL ISA and Research Corpus

> The cognitive instruction set above SXL, and the
> research substrate that feeds it. NSL (the Neural
> Symbolic Language) and NSP (its processor) are
> in sapling at `~/solbian/sapling/NSLP/`, along
> with the `deep-research/` corpus. This chapter is
> the engineering-manual view; the canonical source
> is the `NSLP/` directory itself.

## The control plane above the data plane

The sapling chapters so far describe the symbolic
*substrate* that agents manipulate — SXL,
libsexpr, libschema, seedreasond, the canonical
predicates, the confidence system
([`02-SYMBOLIC-LAYER.md`](02-SYMBOLIC-LAYER.md)).
That substrate is the **data plane**: it describes
what is believed, intended, or known.

Sitting *above* SXL is a **control plane** — the
language and processor that describe *what to do*
with cognitive state. That layer is NSL/NSP, a
research-and-design prototype at
`~/solbian/sapling/NSLP/`. The prototype is
complete as a specification (`NSLP/README.md:1-9`);
the implementation is the work in §"Roadmap".

The canonical sources are `NSLP/README.md`
(overview and design principles), `NSLP/SPEC.md`
(formal NSL ISA: 33 primitives, type system,
operational semantics), `NSLP/ARCHITECTURE.md`
(NSP compiler pipeline, runtime, backend dispatch),
`NSLP/GAP-ANALYSIS.md` (gap assessment),
`NSLP/ROADMAP.md` (five-phase implementation
plan), `NSLP/INTEGRATION.md` (how NSL/NSP connects
to `seed-dev/`, the bus, libsmem, libseedllm, the
seedcogd cycle), and `NSLP/deep-research/README.md`
(the 200+ algorithm knowledge base and its five
confirmation flags).

This chapter is a curated synthesis, not a copy:
the canonical sources own the detail. Where a
section needs a number or a file path, it is cited
inline as `file:line`.

## The 4-layer cognitive ISA

The NSLP architecture defines cognition across
four layers, from concrete symbolic representations
to executable workflows
(`NSLP/ARCHITECTURE.md:27-51`):

```
 Layer 4: Cognitive Workflows
   (composed NSL procedures; replace hard-coded
    cycle phases)
       |  compose: sequence, parallel, branch,
       |          iterate, call/return
       v
 Layer 3: SXL Composite Operators
   (high-level verbs: reflect, plan, learn, ...)
       |  compile: NSL primitive graph -> dispatch
       v
 Layer 2: NSL Primitives
   (33 irreducible primitives across 11 groups)
       |  operate on
       v
 Layer 1: Symbolic Objects
   (SXL entities stored in libsmem partitions)
```

**Layer 1** is the SXL entity model documented in
[`02-SYMBOLIC-LAYER.md`](02-SYMBOLIC-LAYER.md). The
26+ entity types are the operands that NSL
primitives read, write, and transform. They are
stored in libsmem, the SST workspace
(`sst_workspace_t` in
`src/seed-transformer/include/sst.h:113-127`), and
the seedcogd ring buffer
(`seedcogd/main.c:57-103`).

**Layer 2** is the NSL ISA proper — 33 primitives
across 11 functional groups, each verified as
irreducible (`NSLP/SPEC.md:41-58`).

**Layer 3** is the composite operator layer: the
high-level verbs (`reflect`, `plan`, `learn`,
`simulate`, `evaluate`, ...) that appear in
cognitive cycle prompts. Each composite is a named
NSL procedure — a documented composition of
primitives with a signature, confidence model,
and error semantics. The 22 SST operators in
`src/seed-transformer/include/sst.h:86-109` are
natural candidates; the mapping is in
`ARCHITECTURE.md:198-222`.

**Layer 4** is the workflow layer: named, executable
NSL procedures that replace one or more hard-coded
phases in the current `seedcogd` cycle. Unlike the
fixed-phase loop in `seedcogd/main.c:2184-3504`
(the A–L phases of `cognitive_tick()`),
a workflow is dynamically selected based on
current state, with triggers, costs, and
confidence updated from execution history
(`ARCHITECTURE.md:226-269`).

The motivation is given in `README.md:46-69`: the
current S.E.E.D. cognitive engine (`seedcogd/main.c`,
3212 lines) executes a hard-coded 12-phase cycle.
Every cycle runs the same phases regardless of
what the system needs. The 14 SXL operators and 22
SST operators are implemented as C and Lua functions
— not as inspectable, composable symbolic
procedures. NSLP changes that.

## NSL — the Neuro-computational SEED Language

NSL is the **instruction set of cognition**: a
set of irreducible symbolic primitives that form
the algebra of thought
(`NSLP/README.md:19-32`). Unlike SXL (the data
plane — what is believed, intended, or known),
NSL is operational — *expressions execute*.

### The primitive test

A primitive is **primitive** iff it cannot be
expressed as a composition of other NSL primitives
(`SPEC.md:13-21`):

> operator `op` is primitive iff there exists no
> NSL expression `E` composed of other primitives
> such that `⟦op⟧ = ⟦E⟧` for all inputs.

The set is **complete** iff every cognitive
operation expressible in S.E.E.D. can be written
as a composition of NSL primitives: all 14 SXL
operators, all 22 SST operators, and all 12
cognitive cycle phases (`SPEC.md:22-27`).

Design constraints (`SPEC.md:29-39`): primitives
are not allowed to assume a backend; bounded
non-determinism is explicit; side-effects are
annotated (`pure`, `read`, `write`, `alloc`); and
primitives are non-recursive (recursion is
achieved through composition).

### The 33 primitives

`SPEC.md:44-58` groups the primitives by
*computational mechanism*:

| # | Group | Primitives | Count |
|---|-------|-----------|-------|
| I | Object Lifecycle | `create`, `destroy`, `typeof` | 3 |
| II | Memory | `read`, `write` | 2 |
| III | Binding | `bind`, `unbind`, `resolve` | 3 |
| IV | Structure | `cons`, `car`, `cdr` | 3 |
| V | Control Flow | `branch`, `iterate`, `sequence`, `parallel` | 4 |
| VI | Subroutine | `call`, `return`, `yield` | 3 |
| VII | Pattern | `match`, `unify`, `substitute` | 3 |
| VIII | Comparison | `equal?`, `less?` | 2 |
| IX | Channel | `send`, `recv`, `spawn` | 3 |
| X | Cognitive | `observe`, `assert`, `retract`, `query`, `derive` | 5 |
| XI | Meta | `reflect`, `evaluate` | 2 |
| | **Total** | | **33** |

`ARCHITECTURE.md:78-192` regroups the primitives by
*cognitive function*: Perception (`observe`,
`extract`, `classify`); Memory (`store`, `recall`,
`forget`, `bind`); Query (`match`, `filter`, `join`);
Inference (`derive`, `abduce`, `induce`, `analogize`);
Comparison (`compare`, `similarity`, `contradicts`);
Control Flow (`sequence`, `parallel`, `branch`,
`iterate`, `call`); Confidence (`propagate`,
`reinforce`, `decay`); Transformation (`merge`,
`split`, `abstract`, `specialise`); Planning
(`decompose`, `schedule`); Evaluation (`evaluate`,
`verify`, `criticise`); and Meta-Cognition
(`reflect`, `trace`). The ARCHITECTURE.md grouping
totals 36 primitives across 11 groups — three
more than the SPEC.md grouping because the
ARCHITECTURE.md taxonomy adds `extract`, `classify`,
`store`, `recall`, `forget`, `bind`, `filter`,
`join`, `abduce`, `induce`, `analogize`,
`compare`, `similarity`, `contradicts`, `merge`,
`split`, `abstract`, `specialise`, `evaluate`,
`verify`, `criticise`, `trace` that the SPEC.md
mechanism-driven taxonomy rolls into compound
primitives (`observe`, `assert`, `retract`,
`query`, `bind`, `equal?`, `less?`, `reflect`,
`evaluate`). The two taxonomies cover the same
cognitive surface but split the primitives along
different axes: SPEC.md is a *flat* enumeration
by Lisp-style mechanism; ARCHITECTURE.md is a
*typed* enumeration by cognitive function. The
ARCHITECTURE document maps each group to existing
C/Lua components (e.g. `compare` →
`sxp_oper_compare()` in
`src/libsexpr/src/transform.c:182`; `derive`
→ `SST_OP_INFER` in
`src/seed-transformer/include/sst.h:90`).

### Composition: the five rules

Primitives compose through exactly **five**
mechanisms (`SPEC.md:247-288`): **Sequence** —
`(seq E1 E2 ... En)` evaluates left-to-right,
returns the last value. **Branch** — `(branch cond
then else)` evaluates the appropriate branch.
**Iterate** — `(iterate seq fn init)` fold-left
over the sequence. **Parallel** — `(par E1 E2 ...
En)` evaluates concurrently; partial success
semantics. **Call** — `(call proc arg1 ... argn)`
invokes a procedure in a fresh environment.

The **completeness theorem** (informal) is at
`SPEC.md:282-287`: the five composition rules plus
33 primitives suffice for all 14 SXL operators,
all 22 SST operators, and all 12 cognitive cycle
phases. The decomposition table for the 14 SXL
operators is at `SPEC.md:316-331`.

### The type system

Three layers (`SPEC.md:289-310`):

- **Base types**: `Nil`, `Boolean`, `Integer`,
  `Float`, `Symbol`, `String`, `Cell`, `Pair`,
  `Channel`, `Process`, `Procedure`, `Pattern`,
  `Substitution`, `Environment`, `Rule`, `Sensor`.
- **Compound types**: `Sequence = Pair*`,
  `Set = Pair*`, `Map = (Pair . Pair)*`,
  `SXL-Entity = Symbol × Fields`.
- **Effect types**: `Effect ::= pure | read |
  write | alloc`. Effects compose over `sequence`:
  `effects(seq E1 E2) = effects(E1) ∪ effects(E2)`.

### Mathematical foundations

The NSL primitives are derived from six
mathematical foundations (`SPEC.md:391-441`):
**lambda calculus** (`call` + `bind` + `resolve` =
β-reduction; Y combinator via `evaluate`);
**π-calculus** (the channel group: `send = āx.P`,
`recv = a(x).P`, `spawn = !P`); **SKI combinators**
(Turing-complete via `branch` + `iterate` + `call`);
**term rewriting** (the pattern group: `match` =
LHS matching, `substitute` = RHS instantiation);
**category theory** (NSL primitives form a
symmetric monoidal category with the cognitive
effect monad `T: Value → Value`); and
**information geometry** (belief updating via
natural gradient on the statistical manifold;
Fisher metric per Chentsov's theorem).

### Non-determinism

Three primitives — `derive`, `observe`, and
`evaluate` — may produce different results across
invocations (`SPEC.md:382-389`). `derive` and
`evaluate` are seed-deterministic. `observe` is
non-deterministic by definition (the external
world is not deterministic). The operational
state model is at `SPEC.md:344-351`:

```
σ = (μ, ε, κ, χ, π)
  μ : Cell → (Type × Fields)    — memory
  ε : Symbol → Value            — environment
  κ : Channel → Queue[Value]    — channels
  χ : Continuation*             — continuation stack
  π : Process*                  — active processes
```

For the full semantics — every small-step rule,
the formal decomposition proofs for all 14 SXL
operators, and the full citation list — see
`~/solbian/sapling/NSLP/SPEC.md`. The 33
primitives, the 5 composition rules, the type
system, and the 6 mathematical pillars are the
irreducible substrate from which all cognition
is built.

## NSP — the compiler, optimizer, and runtime

NSP is the compiler, optimizer, and executor for
NSL expressions — to NSL what a CPU is to its ISA
(`NSLP/README.md:27-31`). The full design is
`NSLP/ARCHITECTURE.md`.

### The four-stage compiler pipeline

`ARCHITECTURE.md:273-294`:

```
 NSL Expression (SXL)
       |  Stage 1: Parse
       v
   Abstract Syntax Tree (libsexpr arena)
       |  Stage 2: Primitive Graph Construction
       v
   Primitive Operator Graph (DAG of nsop_t nodes)
       |  Stage 3: Optimization Passes
       v
   Optimized Graph (backend-tagged nsop_t nodes)
       |  Stage 4: Backend Dispatch
       v
   Executable Plan (nsplan_t with per-operator
   backend assignments)
```

**Stage 1 — Parse** (`ARCHITECTURE.md:296-306`).
Reuses `libsexpr` directly (`seed_sx_parse()` in
`src/libsexpr/src/sexpr.c`). The NSL grammar is a
strict subset of SXL: top-level forms are
`(:primitive-name :keyword value ...)`, nested
forms use `(:seq)`, `(:par)`, `(:branch)`,
variables use `?name`, and SXL entity expressions
are valid as data literals.

**Stage 2 — Primitive graph construction**
(`ARCHITECTURE.md:309-334`). The parser output is
a tree; Stage 2 linearises it into a **directed
acyclic graph** of `nsop_t` nodes (the C type is
at `ARCHITECTURE.md:312-327`). `:seq` serialises
steps; `:par` emits independent sub-graphs with a
merge point; `:branch` produces a conditional fork;
`:iterate` produces a loop sub-graph with an exit
condition; `:call` produces a graph expansion from
the called procedure's body.

**Stage 3 — Optimization passes**
(`ARCHITECTURE.md:336-353`). Five passes: dead
primitive elimination (DPE); common subexpression
elimination (CSE); parallelization analysis
(topological analysis tags nodes with
`NSP_EXEC_PARALLEL`); backend-aware operator
fusion (fuses sequences the same backend can
execute as a unit); and constant folding
(evaluates primitives with all-constant inputs
at compile time).

**Stage 4 — Backend dispatch**
(`ARCHITECTURE.md:355-387`). Uses the same
capability-based routing as
`src/libseedllm/src/dispatch.c:47-71` but at
primitive granularity. The `nsp_backend_t` enum
has six values: `NSP_BACKEND_SYMBOLIC`,
`NSP_BACKEND_NEURAL`, `NSP_BACKEND_HYBRID`,
`NSP_BACKEND_NATIVE`, `NSP_BACKEND_SST`,
`NSP_BACKEND_DEFERRED`. The dispatch decision
considers the primitive-backend capability matrix,
current backend health (`seed_llm_pool_stats()`),
predicted latency and cost (EMA-tracked per
primitive per backend), confidence required, and
data locality. The output of Stage 4 is an
`nsplan_t` (declared at `ARCHITECTURE.md:379-386`).

### The runtime

`ARCHITECTURE.md:389-483`:

- **Graph executor** (`ARCHITECTURE.md:395-415`):
  walks the optimised graph in topological order.
  Six backends route to: `sxp_oper_*` functions,
  `seed_llm_chat()`, neural + symbolic validation
  via `sxp_validate()`, direct C function calls,
  `sst_execute()`, and the continuation manager.
- **Continuation management**
  (`ARCHITECTURE.md:418-436`): primitives that
  cannot complete in a single cycle (multi-round
  consensus, peer-gathered reflection, unknown
  iteration count) are suspended as
  `(:type continuation ...)` SXL entities with
  `resume_at`, `accumulated`, and `ttl` fields.
  Continuations live in
  `cognitive/this-node/continuations`.
- **Channel system** (`ARCHITECTURE.md:438-456`):
  typed, buffered SXL channels replace ad-hoc
  shared-state access to the SST workspace. Three
  channel types: UNICAST (`:seq` step passing),
  MULTICAST (`:par` branch fan-out), PUBSUB
  (cross-primitive event notification).
- **Process scheduler**
  (`ARCHITECTURE.md:458-483`): a lightweight
  cooperative scheduler runs up to
  `MAX_ACTIVE_PROCESSES` (default 4) per cycle,
  preempts processes that exceed their time slice,
  and migrates long-running processes to
  continuation state.

### How NSL replaces hard-coded cycle phases

`ARCHITECTURE.md:485-548` documents the migration
from the current hard-coded `seedcogd` cycle
(phases A-L in `seedcogd/main.c:2184-3504`) to a
**workflow scheduler** that (1) checks continuations,
(2) calls `nsp_schedule()` to select ready workflows
based on triggers, (3) executes selected workflows
via NSP runtime, (4) collects results, (5) repeats.
Workflow triggers replace the modulo arithmetic
(`cycle%5`, `cycle%11`, `cycle%13`) that currently
schedules Phase C, Phase K, and Phase L
(`ARCHITECTURE.md:520-536`). The migration is
incremental: Phase 0 keeps the current cycle; Phase
1 pilots one phase replacement; Phase 2 migrates
3-4 phases; Phase 3 makes the main loop a thin
`nsp_schedule()` call. The C code for each phase
remains as a fallback throughout.

## Gap analysis — what the spec demands vs. what the code has

`NSLP/GAP-ANALYSIS.md` evaluates the S.E.E.D. v21
codebase (commit c4bd98a) against the proposals
in `seed-cog3-specs.txt` and `seed-misc-specs.txt`.
The baseline is strong
(`GAP-ANALYSIS.md:14-19`): a working 12-phase
cognitive cycle (A-L) in `src/seedcogd/main.c`
(3212 lines), a 5-backend LLM abstraction in
`libseedllm` (~15 source files), a multi-tier bus
(T0/T1/T2), a symbolic memory system with
replication in `libsmem` (~20 source files), an
S-expression engine with confidence propagation in
`libsexpr` (8 source files, 1711 lines), and 25
Lua helper modules totalling 10,619 lines.

**Total**: 19 gap areas, 6 contradictions, 7
priority recommendations
(`GAP-ANALYSIS.md:1-9`).

### The three most-impactful gaps

Per `GAP-ANALYSIS.md:24-34`:

1. **Belief Revision** (0% implemented). No
   mechanism to update prior knowledge with new
   evidence. Every discovery is treated as new.
   Confidence is set once at creation
   (`atof(conf) : 0.95` at `main.c:188-189`) and
   decays monotonically (0.85x per cycle, floor
   0.2). The 6 confidence propagation rules in
   `src/libsexpr/src/confidence.c` exist but are
   not wired into any belief revision pipeline.
2. **Cognitive Homeostasis** (0% implemented).
   No regulation prevents runaway cognitive loops,
   excessive repetition, or resource exhaustion.
   The cycle runs continuously (`while(1) {
   cognitive_tick(); sleep(gap_seconds); }` at
   `main.c:2933-3212`). Phase A runs 3 parallel
   LLM calls every cycle with no limit; learning
   can trigger auto-deployment every cycle with no
   resource check.
3. **Cognitive Workflows** (0% implemented). The
   12-phase cycle is a fixed algorithm, not an
   adaptive composition of selectable workflows.
   No `(workflow ...)` SXL object type, no
   workflow executor, selector, or evaluator.

### The 6 contradictions

`GAP-ANALYSIS.md` §4:

1. **Primitive operator count** — spec says 25-40
   verified primitives; code has 22 SST + 14 SXP =
   36 operators, none verified. Resolution: demote
   ~15 operators to composites.
2. **DataChain vs journal purpose** — spec wants
   DataChain as a cognitive timeline; code's
   `docs/network/DATACHAIN.md:5` says
   "Merkle-linked local log used for accountability
   and forensics." Resolution: keep them separate.
3. **DFS scope** — spec wants DFS as a Distributed
   Symbolic Cortex; code's `docs/network/DFS.md:2-6`
   says "not a POSIX filesystem." Resolution: build
   the cortex on libsmem replication, not DFS.
4. **Blackboard vs separation of concerns** —
   blackboard centralises what was intentionally
   distributed. Resolution: shared-partitions
   model with a well-known
   `cognitive/this-node/blackboard` partition.
5. **Executive function daemon** — spec wants a
   separate governance daemon; code combines
   executive and worker in `seedcogd`.
   Resolution: extract executive logic into a
   distinct `executive.c` module within `seedcogd`.
6. **Homeostasis vs continuous operation** — spec
   wants rest periods; code's `main.c:2933-3212`
   is
   `while(1) { cognitive_tick(); sleep(gap_seconds); }`.
   Resolution: add a "throttle" phase that can skip
   phases or extend `sleep` based on cognitive
   load metrics.

### The 7 priority recommendations

`GAP-ANALYSIS.md` §5 (P1–P7):

- **P1 — Belief Revision Engine** (Critical).
  2-3 weeks.
- **P2 — Cognitive Homeostasis** (Critical).
  2-3 weeks.
- **P3 — Cognitive Workflows as SXL Objects**
  (High). 3-4 weeks.
- **P4 — Self-Model Expansion** (High). 1-2 weeks.
- **P5 — 4-Layer SXL ISA Discipline** (Medium).
  4-6 weeks.
- **P6 — MCL with Dynamic Benchmarking** (Medium).
  2-3 weeks.
- **P7 — Cognitive Blackboard** (Medium). 3-4
  weeks.

For the gap-by-gap evidence (file paths, line
numbers, severity assessments) and per-gap
implementation paths, see
`~/solbian/sapling/NSLP/GAP-ANALYSIS.md`.

## Roadmap — five phases, ~8 months wall-clock

`NSLP/ROADMAP.md` transforms the gap analysis
into a five-phase implementation plan. The
critical path is
`Phase 1 → Phase 2 → Phase 3 → Phase 4 → Phase 5`;
parallel tracks exist inside each phase
(`ROADMAP.md:14-19`).

**Phase 1 — Critical Foundations (4-6 weeks)**
(`ROADMAP.md:36-122`). Adds the two zero-percent
features: **1.1 Belief Revision Engine** (3 weeks;
evidence chain field on entries, belief store with
update semantics, confirming + disconfirming
pipelines, novelty check before Phase A, wire
`sxp_confidence_propagate` into the cycle) and
**1.2 Cognitive Homeostasis** (2-3 weeks; discovery
diversity tracking, explore/exploit mode, per-phase
budgets, consolidation-as-rest background thread,
oscillation detection, per-cycle health SXL).

**Phase 2 — Workflow architecture (6-8 weeks)**
(`ROADMAP.md:125-216`). Replaces the hard-coded
cycle with SXL workflow definitions: **2.1
Cognitive Workflows as SXL Objects** (4-5 weeks;
`(workflow ...)` SXL type, phase definitions as
SXL, default workflow `cog-cycle-12`, workflow
executor in Lua, workflow selector, fallback
cycle) and **2.2 Self-Model Expansion** (2 weeks;
self-model partition, per-cycle population,
meta-cognition seeding, world model integration —
parallel with 2.1).

**Phase 3 — ISA discipline (8-10 weeks)**
(`ROADMAP.md:219-296`). Establishes the four-layer
hierarchy: **3.1 Four-Layer SXL ISA Discipline**
(6-7 weeks; operator audit, core primitive set,
composite operator library, macro-expansion system,
operator metadata registry, four-layer documentation)
and **3.2 MCL Dynamic Benchmarking** (3-4 weeks;
dynamic benchmark suite, expanded model profiles,
cost-aware dispatch, symbolic model profiles —
parallel with 3.1).

**Phase 4 — Cognitive infrastructure (8-10 weeks)**
(`ROADMAP.md:299-358`). Introduces the blackboard
and separates executive function: **4.1 Cognitive
Blackboard** (5-6 weeks; fact schema, blackboard
partition, phase migration across all 12 phases,
attention-as-blackboard-gate, cross-domain listener)
and **4.2 Executive Function Separation** (3-4
weeks; executive module, per-cycle executive SXL,
seedreasond as policy governor, decision audit
trail).

**Phase 5 — Distributed cognition (10-14 weeks)**
(`ROADMAP.md:360-422`). Completes the distributed
and dynamic story: **5.1 Distributed Symbolic
Cortex** (8-10 weeks; node role advertisement,
role-aware routing, libsmem replication with
role-filtered sync, cortex health monitoring) and
**5.2 Dynamic Ontology** (4-5 weeks; pattern
discovery module, ontology proposal pipeline,
approval gate, schema generation).

**Effort**: 38-50 weeks (9-12 months) on the
critical path alone. With parallel tracks
(Self-Model with Workflows, MCL with ISA,
Executive with Blackboard), wall-clock timeline
is **~34 weeks (~8 months)**
(`ROADMAP.md:466-479`). The risk register
(belief-revision feedback loops, homeostasis
starvation, ISA audit producing more primitives,
blackboard migration breakage, role-specialisation
resilience) is at `ROADMAP.md:483-493`.

For the per-deliverable acceptance criteria,
file maps, and measurement metrics, see
`~/solbian/sapling/NSLP/ROADMAP.md`.

## The deep-research corpus

`NSLP/deep-research/` is the knowledge base from
which new SXL operators and cognitive engine
capabilities are sourced. It holds 200+ algorithm
profiles across 7 files
(`deep-research/README.md:76-89`):

| File | Algorithms | Coverage |
|------|-----------|----------|
| `sxl-operators.md` | 30 | Symbolic cognitive algorithms (AGM, Dung, DLs, SAT, planning, BNs, MLNs, KG embeddings) |
| `cognitive-cycles.md` | 24 | Cognitive cycle and time-series algorithms (memory consolidation, prediction, attention, RL) |
| `neuro-primitives.md` | 30 | Neuro-computational primitives (NNs, spiking, neuro-symbolic) |
| `memory-reasoning.md` | 32 | Memory architectures, knowledge representation, multi-agent, causal, RL |
| `nslp-algorithms.md` | 60 | Deep dive for the Neuro-Symbolic Language Processor: mathematical machinery for the SXL/SXP operator layer |
| `theorems-and-bounds.md` | 24 | Foundational theorems, complexity bounds, and approximation guarantees |
| `canonical-references.md` | 80+ | Master reference list: every primary paper, textbook, and survey |

**Total**: 200+ algorithm profiles. The README
header counts (lines 89-91) show **84 flagged
`ready-for-promotion`** and **116+ flagged
`unconfirmed`**.

### The five confirmation flags

Every profile carries a confirmation flag
(`deep-research/README.md:28-49`):

- **Confirmed-canonical** — primary citation,
  year, author list, and URL verified against
  multiple independent sources. Safe to promote.
- **Confirmed-curated** — primary citation and
  year correct, but profiled from a textbook or
  survey and not yet checked against the primary
  paper. Worth a second pass.
- **Unconfirmed** (the default) — algorithm name,
  year, and basic idea plausible, but at least
  one of: author list, venue, URL, worked example,
  or complexity class is uncertain. Requires
  verification.
- **Derived-from-partial** — the producing agent
  stalled before the final structured return;
  some sections are reconstructed from the
  agent's tool-call stream. Treat with caution.
- **Speculative** — citation chain is weak or
  self-referential. Do not promote without a
  primary-source pass.

The default flag for new entries is
**`unconfirmed`**. Promotion to `~/seed-dev/`
requires `confirmed-canonical` or
`confirmed-curated`.

### The promotion path

A `ready-for-promotion` algorithm becomes a
first-class SXL operator in `~/seed-dev/` via
(`deep-research/README.md:122-159`): (1) spec
entry in `~/seed-dev/codex/machina/` as an
`(:type operator ...)`; (2) C implementation in
`~/seed-dev/src/libseedcog/`; (3) Lua binding in
`~/seed-dev/lua/agents/cognitive/`; (4) tests in
`~/seed-dev/tests/seedcog/`; (5) conformance
corpus entry in `~/seed-dev/tests/conformance/`;
(6) bus topic (if needed) on
`org.seed.cog.<algorithm>` following the
FROZEN-2026-05-10 namespace.

The verification flow (read primary source,
confirm year/author/venue/URL, re-derive worked
example and pseudocode, re-check complexity,
update flag, append to verification log) is at
`deep-research/README.md:51-74`. The five-layer
mapping (L1 C cycle, L2 Lua orchestration,
L3 cross-node, L4 user-facing, L0 codex) is at
`deep-research/README.md:183-219`.

## The cognitive-operator-promoter agent

`~/solbian/sapling/AGENTS.md` catalogues one
proposed sapling agent that consumes the
deep-research corpus:

- **Name**: `cognitive-operator-promoter`.
- **Concept**: An agent that takes a
  `ready-for-promotion` entry from the
  deep-research files and generates the artifacts
  required to promote a community-approved
  algorithm to a first-class SXL operator in
  `~/seed-dev/`. It generates the C signature,
  the Lua binding, the test scaffold, the
  conformance corpus entry, and the bus topic
  proposal (if needed). The agent itself runs off
  the bus; the promotion it produces is reviewed
  by a human before any code lands in
  `~/seed-dev/`.
- **Cognitive domain(s)**: meta-cognition.
- **Upstream pointer**: `sapling-only`.
- **Status**: `concept`.
- **ACL role**: `external` (default for sapling
  agents; promotion to `core` on graduation).
- **Provenance**: Phase 1 follow-through session,
  2026-07-16. The 84 `ready-for-promotion`
  algorithms are the upstream substrate.

See
[`01-SAPLING-CATALOG.md`](01-SAPLING-CATALOG.md)
for the catalog schema, and
[`03-AGENT-INTEGRATION.md`](03-AGENT-INTEGRATION.md)
for the bus-topic and ACL conventions the agent
must follow once it moves from `concept` to
`prototype`.

## The cognitive-engine-research-corpus entity

`~/solbian/sapling/ENTITIES.md` catalogues the
corpus itself:

- **Name**: `cognitive-engine-research-corpus`.
- **Kind**: `dataset` (also `runtime-concept`).
- **Description**: The structured research
  knowledge base at `sapling/NSLP/deep-research/`.
  Holds 200+ algorithm profiles across 7 files,
  each profile containing the year, primary
  citation, core idea, community status,
  complexity, pseudocode, worked numerical example,
  canonical reference URL, failure modes, SXL
  entity shape, and `ready-for-promotion` flag.
  The corpus is the substrate from which the
  `cognitive-operator-promoter` agent generates
  first-class SXL operators in `~/seed-dev/`.
- **Where it lives**:
  `~/solbian/sapling/NSLP/deep-research/` (7
  files + verification logs).
- **Where it is referenced**:
  `sapling/AGENTS.md` (the promoter agent consumes
  it); `sapling/README.md` (level overview);
  [`02-SYMBOLIC-LAYER.md`](02-SYMBOLIC-LAYER.md)
  (symbolic substrate doc); the 20 cognitive
  domain chapters in `~/seed-dev/src/seedcogd/`
  as algorithms are promoted.
- **Status**: `canonical`.

See
[`01-SAPLING-CATALOG.md`](01-SAPLING-CATALOG.md)
for the entity entry schema, and
[`04-GRADUATION-PATH.md`](04-GRADUATION-PATH.md)
for how promoted algorithms move into
`~/seed-dev/` or `~/robot-dev/`.

## Integration — how NSL/NSP connects to the rest

The full integration surface is documented in
`NSLP/INTEGRATION.md`. The summary below is the
engineering-manual view; the canonical document is
the source of truth.

### The five integration surfaces

`INTEGRATION.md:19-28`:

| Surface | Protocol | Purpose |
|---------|----------|---------|
| **Bus** (T1) | `org.seed.cog.nsl.*` topics | NSL execution requests and results |
| **Memory** (libsmem) | `cognitive/this-node/*` partitions | SXL entity storage for primitives |
| **Backends** (libseedllm) | `seed_llm_chat()` / `seed_llm_pool_*` | Neural inference dispatch |
| **SST** (seed-transformer) | `sst_execute()` / `sst_workspace_t` | Operator execution and workspace access |
| **Cycle** (seedcogd) | `nsp_schedule()` / workflow table | Phase replacement and augmentation |

### Bus topics

NSL/NSP publishes on `org.seed.cog.nsl.*`
(`INTEGRATION.md:36-57`): `org.seed.cog.nsl.execute`
(NSL expression, on demand),
`org.seed.cog.nsl.workflow.completed` (workflow
result, per workflow),
`org.seed.cog.nsl.workflow.failed` (error, on
failure), `org.seed.cog.nsl.schedule` (workflow
entries, every cycle). It subscribes to
`org.seed.cog.nsl.execute.reply`,
`org.seed.cog.nsl.compile`,
`org.seed.cog.nsl.compile.reply`,
`org.seed.cog.nsl.workflow.register`,
`org.seed.cog.nsl.workflow.unregister`,
`org.seed.cog.nsl.primitive.status`, and
`org.seed.cog.nsl.primitive.status.reply`.

### Memory and backend mappings

The NSP runtime maps NSL primitives to existing
`seed_smem_*` functions and `libseedllm` calls
(`INTEGRATION.md:116-279`). Concrete examples:
`(recall ...)` → `seed_smem_sxl_scan()` in
`src/libsmem/src/sxl.c:25-54`; `(store ...)` →
`seed_smem_entry_put()`, with SXL serialised as
`memory_entry/v1` and written to the append-only
`.sref` log and JSONL journal; `(forget ...)` →
entry status set to `abandoned`, confidence
decayed to floor; `(bind ...)` →
`index_add_relation()` in `seedcogd/main.c:78-88`,
with the 8192-entry relation table supporting 12
canonical relation labels from `sxl.sref:34-38`
(supports, contradicts, derives, causes, depends,
refines, generalises, specialises, related,
evidence, inspires, precedes).
Neural-bound primitives (`derive`, `abduce`,
`analogize`, `evaluate`, `reflect`, `criticise`)
dispatch through `libseedllm` via a per-primitive
capability matrix that extends `task_classify()`
in `src/libseedllm/src/task_classify.c`. For
`NSP_BACKEND_HYBRID`, the neural result is
validated symbolically and the final confidence
is computed by `sxp_confidence_propagate()` from
`src/libsexpr/src/confidence.c`.

### seedcogd cycle integration

`INTEGRATION.md:283-419`. The current 12-phase
structure is at `seedcogd/main.c:2184-3504`. The
NSP runtime maintains a workflow registry loaded
from `cognitive/this-node/workflows` at daemon
startup. Integration candidates, in order of
feasibility: **Phase A** (parallel reflection +
evaluation + discovery, `seedcogd/main.c:2184-2354`)
is the best pilot — the hard-coded
`refl_prompts[cycle%4]` / `law_prompts[cycle%4]` /
`disc_prompts[cycle%4]` rotation becomes a
workflow parameter. **Phase K** (meta-cognition,
`seedcogd/main.c:2609-2780`) is the most
self-contained phase — it performs only local
computation (no LLM calls) and can run entirely
on `NSP_BACKEND_SYMBOLIC`. The **Lua brain cycle**
(`lua/agents/cognitive/brain.lua`) integrates via
the 25 Lua helper modules becoming the
**implementation bodies** that NSL procedures
call into — the `(reflect)` primitive dispatches
to `lua/helpers/reflection.lua` when running in
a Lua context, or to
`sst_execute(SST_OP_REFLECT, ...)` when running
in a C context.

### Graduation path

`INTEGRATION.md:574-620`. NSLP starts at the
`external` ACL role and graduates to `core` when:
(1) NSLP has run as a prototype for at least one
full release cycle of `~/seed-dev/`; (2) the NSL
grammar is stable and versioned; (3) the NSP
compiler passes the test suite; (4) at least one
cognitive cycle phase is successfully replaced by
an NSL workflow; (5) graduation is recorded in
`~/solbian/LOG.md`. After graduation, the ACL is
upgraded to `core`, granting write access to
`cognitive/this-node/*` partitions, publish access
to `org.seed.memory.*` topics, and direct access
to actuator bus topics (via safety policy gate).
Destinations: `~/seed-dev/src/nsp/` for the NSP
compiler and runtime;
`~/seed-dev/lua/agents/cognitive/brain.lua` for
the Lua bindings and workflow table; and
`~/solbian/codex/solbian/` for the NSL language
spec, once it is stable.

For the full integration model — T1 transport
details (UDS at `/run/seed/bus.sock`, SXL
S-expression framing, QoS levels), the per-primitive
ACL table, the sandboxing parameters, and the
safety considerations — see
`~/solbian/sapling/NSLP/INTEGRATION.md`.

## How to read this chapter

If you are reviewing the NSLP prototype for
promotion, read this chapter for the level model,
then read `NSLP/README.md` for the design
principles, `NSLP/SPEC.md` for the formal ISA,
`NSLP/ARCHITECTURE.md` for the NSP compiler and
runtime, `NSLP/GAP-ANALYSIS.md` for what the spec
demands versus what the code has,
`NSLP/ROADMAP.md` for the implementation plan, and
`NSLP/INTEGRATION.md` for the bus and seed-dev
integration.

If you are building an NSL workflow, read
`NSLP/SPEC.md` §5 for the decomposition proofs of
the 14 SXL operators, `NSLP/ARCHITECTURE.md` §3
for the compiler pipeline and the five optimization
passes, and `NSLP/INTEGRATION.md` §3-5 for the
per-primitive memory, backend, and seedcogd
mappings.

## See also

- [`00-AGENTS-OVERVIEW.md`](00-AGENTS-OVERVIEW.md) —
  sapling level overview
- [`01-SAPLING-CATALOG.md`](01-SAPLING-CATALOG.md) —
  the catalog schema and graduation criterion
- [`02-SYMBOLIC-LAYER.md`](02-SYMBOLIC-LAYER.md) —
  the SXL substrate that NSL operates on
- [`03-AGENT-INTEGRATION.md`](03-AGENT-INTEGRATION.md) —
  the bus topics and ACLs for sapling agents
- [`04-GRADUATION-PATH.md`](04-GRADUATION-PATH.md) —
  when and how an agent leaves sapling
- [`05-UNTRUSTED-AGENT-MODEL.md`](05-UNTRUSTED-AGENT-MODEL.md) —
  the limits on sapling agents
- [`07-NSL-DEEP-DIVE.md`](07-NSL-DEEP-DIVE.md) —
  the four-layer cognitive ISA, the 33 NSL
  primitives, and the cognitive compiler
- [`08-COGNITIVE-WORKFLOWS.md`](08-COGNITIVE-WORKFLOWS.md) —
  the 16-workflow catalogue, the 50+ SXL
  operator families, and the 27 cognitive
  entity types
- [`09-MEMORY-HIERARCHY.md`](09-MEMORY-HIERARCHY.md) —
  the seven-layer memory hierarchy, the belief
  revision engine, and cognitive homeostatic
  regulation
- [`10-MODEL-COGNITION-LAYER.md`](10-MODEL-COGNITION-LAYER.md) —
  the Model Cognition Layer (MCL), the
  capability-matching dispatcher, and the 16
  cognitive capabilities
- [`11-COGNITIVE-JOURNAL-WEAKNESSES.md`](11-COGNITIVE-JOURNAL-WEAKNESSES.md) —
  the eight known weaknesses of cognitive
  journaling and their mitigations
- [`12-DISCOVERY-PATTERN.md`](12-DISCOVERY-PATTERN.md) —
  the DRIRR document pattern and the four
  Solbian Discoveries (SD-0001 to SD-0004)
- `~/solbian/sapling/NSLP/README.md` — NSLP project
  overview and design principles
- `~/solbian/sapling/NSLP/SPEC.md` — formal NSL ISA
  specification
- `~/solbian/sapling/NSLP/ARCHITECTURE.md` — NSP
  compiler, optimizer, runtime
- `~/solbian/sapling/NSLP/GAP-ANALYSIS.md` — 19
  gaps, 6 contradictions, 7 priority recommendations
- `~/solbian/sapling/NSLP/ROADMAP.md` — five-phase
  implementation plan
- `~/solbian/sapling/NSLP/INTEGRATION.md` — how
  NSL/NSP connects to S.E.E.D.
- `~/solbian/sapling/NSLP/deep-research/README.md` —
  the 200+ algorithm knowledge base and confirmation
  flags
- `~/solbian/sapling/AGENTS.md` — the catalog of
  emerging agents (including
  `cognitive-operator-promoter`)
- `~/solbian/sapling/ENTITIES.md` — the catalog of
  entities (including
  `cognitive-engine-research-corpus`)
- `~/seed-dev/docs/cognition/SXL_LANGUAGE_SPECIFICATION.md` —
  the canonical SXL spec (the data plane)
- `~/seed-dev/docs/architecture/COGNITIVE_ENGINE_SPEC.md` —
  the 20 cognitive domains
