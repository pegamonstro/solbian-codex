# ROADMAP — NSL/NSP Implementation Roadmap

> **Based on:** GAP-ANALYSIS.md (19 gap areas, 6 contradictions, 7 priority recommendations)
> **Date:** 2026-07-16
> **Target architecture:** Four-layer SXL ISA with Cognitive Workflows,
>   Belief Revision, Cognitive Homeostasis, and Distributed Symbolic Cortex
> **Current baseline:** S.E.E.D. v21 (12-phase hard-coded cognitive cycle,
>   5-backend LLM pool, D1-D5 distributed stack, 25 Lua helper modules)

---

## Overview

This roadmap transforms the S.E.E.D. cognitive system from a fixed 12-phase
pipeline into an adaptive, self-regulating, workflow-driven cognitive architecture.
The implementation is organized into five phases, ordered by dependency and impact.

**Critical path:** Phase 1 -> Phase 2 -> Phase 3 -> Phase 4 -> Phase 5
**Parallel tracks:** Self-Model (P4) can run concurrently with Workflows (P3)

```
Phase 1 (now):  Belief Revision + Homeostasis
    |
Phase 2:        Workflows + Self-Model (parallel safe)
    |               |
    v               v
Phase 3:        ISA Discipline + MCL Benchmarking
    |
Phase 4:        Blackboard + Executive Separation
    |
Phase 5:        Distributed Cortex + Dynamic Ontology
```

---

## Phase 1: Critical Foundations (Now)

**Duration:** 4-6 weeks
**Risk:** HIGH if deferred — the system cannot learn or regulate itself without these.
**Dependencies:** None (both are additive to the existing cycle).

### 1.1 Belief Revision Engine (3 weeks)

The confidence propagation algebra exists in `src/libsexpr/src/confidence.c`
(6 rules: deductive, probabilistic, Bayesian, Dempster-Shafer, fuzzy, decay)
but it is not wired into any cognitive pathway. This phase adds evidence chains,
update semantics, and belief-aware cycle gating.

#### Deliverables

| # | Deliverable | Files | Notes |
|---|-------------|-------|-------|
| BR-1 | Evidence chain field on entries | `src/seedcogd/main.c` — `entry_t` struct | Add `evidence_from[32]` (parent entry indices) + `updated_cycle` |
| BR-2 | Belief store with update semantics | `src/seedcogd/belief.h` (new, ~200 lines) | Wraps libsmem partition `cognitive/this-node/beliefs`. Supports `upsert` (not just append). Fields: `entity_id`, `confidence`, `evidence_chain`, `last_updated`, `source`, `conclusion_sxl`. |
| BR-3 | Update pipeline — confirming evidence | `src/seedcogd/belief.c` (new, ~300 lines) | When a new entry matches an existing belief's entity_id with same conclusion, update confidence: `new_conf = current + (1-current) * 0.2 * evidence_strength`. Cap at 0.99. |
| BR-4 | Update pipeline — disconfirming evidence | `src/seedcogd/belief.c` (same file) | When a new entry contradicts a belief (detected via Phase B contradiction check), reduce confidence: `new_conf = current * (1 - 0.3 * evidence_strength)`. If below 0.15, flag for review. |
| BR-5 | Novelty check before Phase A | `src/seedcogd/main.c` — Phase A gating | Before dispatching reflection/evaluation/discovery, check: "do we have a settled belief on this topic with confidence > 0.90?" If yes, skip LLM call and return stored belief. |
| BR-6 | Wire sxp_confidence_propagate | `src/seedcogd/belief.c` + `src/libsexpr/` | Call `sxp_confidence_propagate()` with Bayesian or Dempster-Shafer rule during belief updates. Add `sxp_propagation_rule_t` parameter to update API. |

#### Effort Breakdown

| Week | Focus | Details |
|------|-------|---------|
| 1 | Data model + store | entry_t extension, belief.h, belief partition |
| 2 | Update pipeline | Confirming + disconfirming logic, confidence propagation wiring |
| 3 | Cycle integration | Novelty check, contradiction-to-belief wiring, test suite |

#### Files to Create
- `src/seedcogd/belief.h` — belief store API (~200 lines)
- `src/seedcogd/belief.c` — update pipeline (~300 lines)
- `tests/test_belief.c` — unit tests (~200 lines)

#### Files to Modify
- `src/seedcogd/main.c` — entry_t struct, Phase A gating, Phase B wiring
- `src/libsexpr/src/confidence.c` — expose `sxp_confidence_propagate()` in public header if not already
- `CMakeLists.txt` — add belief.c to seedcogd build

#### Acceptance Criteria
- [ ] Entries carry evidence chains that survive across cycles
- [ ] Confirming evidence increases belief confidence (verify: start at 0.7, three confirmations reach ~0.89)
- [ ] Contradicting evidence decreases belief confidence
- [ ] Phase A skips LLM call for topics with high-confidence settled beliefs
- [ ] All libsexpr confidence propagation rules produce correct results per their documented formulas

---

### 1.2 Cognitive Homeostasis (2-3 weeks)

Phase 1 runs in parallel track with Belief Revision.

#### Deliverables

| # | Deliverable | Files | Notes |
|---|-------------|-------|-------|
| CH-1 | Discovery diversity tracking | `src/seedcogd/main.c` — new static counters | Topic signature per cycle (word set from `:content` field). Track topic_frequency map (last 20 cycles). |
| CH-2 | Exploration/exploitation mode | `src/seedcogd/main.c` — mode flag | Mode `g_cognitive_mode` enum: `EXPLORE`, `EXPLOIT`, `REGULATE`. Switch every 10 cycles. EXPLORE: enable all 3 Phase A threads. EXPLOIT: 1 thread, deep focus. REGULATE: skip Phase A, run consolidation. |
| CH-3 | Phase budgets | `src/seedcogd/main.c` — cap per phase | `g_cycle_budget_llm = 10` (default). Phase A consumes 3 per call. Phase B plan consumes 1. Phase D prediction consumes 1. Phase E learning consumes 1. When budget exhausted, skip remaining LLM phases this cycle. |
| CH-4 | Consolidation-as-rest | `src/seedcogd/main.c` — background thread | Move Phase C to a dedicated thread. Thread runs `sleep(15)` between cycles. Main cycle no longer blocks on consolidation. |
| CH-5 | Oscillation detection | `src/seedcogd/main.c` + `belief.c` | If same topic appears in >5 of last 20 cycles with same or higher confidence: raise `g_oscillator_flag`. When flag set, HALVE all Phase A budgets and LOG the oscillation. |
| CH-6 | Homeostasis health output | `src/seedcogd/main.c` — dsxl() each cycle | Per-cycle SXL entry `(:type health :mode EXPLORE :budget_remaining 7 :diversity 0.64 :oscillation false :cycle %d)` |

#### Effort Breakdown

| Week | Focus | Details |
|------|-------|---------|
| 1 | Diversity + modes | Topic tracking, mode switching, budget infrastructure |
| 2 | Consolidation thread + oscillation | Thread migration, oscillation detection, health output |

#### Files to Create
- `src/seedcogd/health.h` — homeostasis types and globals (~100 lines)

#### Files to Modify
- `src/seedcogd/main.c` — add mode flag, budget counters, diversity tracking, oscillation detection, consolidation thread launch, health dsxl call
- `src/seedcogd/main.c:2933-3212` (main loop) — add mode switching, budget reset at cycle start

#### Acceptance Criteria
- [ ] System alternates between EXPLORE and EXPLOIT modes every 10 cycles
- [ ] Phase A LLM calls are capped by budget (default 10 per cycle)
- [ ] Consolidation runs in a background thread, not blocking the main cycle
- [ ] Repeated same-topic discoveries trigger oscillation flag and budget reduction
- [ ] Health SXL entry produced every cycle with all mode/diversity/budget fields

---

## Phase 2: Workflow Architecture (Next)

**Duration:** 6-8 weeks
**Prerequisites:** Phase 1 complete (homeostasis mode switching needed for workflow selection)

### 2.1 Cognitive Workflows as SXL Objects (4-5 weeks)

Transforms the hard-coded 12-phase cycle into a library of SXL workflow definitions
with a workflow executor that selects, runs, and evaluates workflows.

#### Deliverables

| # | Deliverable | Files | Notes |
|---|-------------|-------|-------|
| CW-1 | `(workflow ...)` SXL type | `docs/cognition/SXL_LANGUAGE_SPECIFICATION.md` update + `src/libsexpr/schemas/workflow.sref` | Fields: `:id`, `:version`, `:phases` (ordered list), `:conditions` (preconditions), `:triggers` (when to invoke), `:author`, `:confidence`, `:success_count`, `:failure_count`. |
| CW-2 | Phase definitions as SXL | `lua/helpers/workflows/` (12 files) | Each phase becomes a file: `reflection.sxl`, `evaluation.sxl`, `discovery.sxl`, `contradiction_check.sxl`, `planning.sxl`, `consolidation.sxl`, `prediction.sxl`, `learning.sxl`, `language_evolution.sxl`, `vision.sxl`, `goal_management.sxl`, `creativity.sxl`. Each file specifies LLM intent, input sources, output target. |
| CW-3 | Default workflow "cog-cycle-12" | `lua/helpers/workflows/cog-cycle-12.lua` | The existing 12-phase sequence as the first workflow definition. Fallback if no workflow selected. |
| CW-4 | Workflow executor | `lua/helpers/workflow_executor.lua` (new, ~400 lines) | Reads SXL workflow definition. Dispatches phases in order. Handles condition checks (skip phase if precondition unmet). Captures phase outputs. Evaluates success. Updates workflow confidence. |
| CW-5 | Workflow selector | `lua/helpers/workflow_selector.lua` (new, ~200 lines) | Mapping: problem type string -> workflow ID. Initial: "observation" -> cog-cycle-12, "debug" -> mini-cycle (3 phases), "exploration" -> explore-cycle. |
| CW-6 | Fallback cycle | `src/seedcogd/main.c` — keep existing cycle | The hard-coded C cycle remains as the default path. Workflow execution is additive: when workflows are loaded, the Lua brain calls workflow_executor instead of the C phases. |

#### Effort Breakdown

| Week | Focus | Details |
|------|-------|---------|
| 1 | SXL workflow schema | Define `(workflow ...)` type, write schemas/sref, update SXL spec doc |
| 2 | Phase extraction | Extract each phase's logic into SXL workflow definitions |
| 3-4 | Workflow executor | Lua executor: parse workflow SXL, dispatch phases, collect results |
| 5 | Selector + integration | Problem type mapping, Lua-to-C bridge for existing phases |

#### Files to Create
- `lua/helpers/workflow_executor.lua` (~400 lines) — orchestrator
- `lua/helpers/workflow_selector.lua` (~200 lines) — selector
- `lua/helpers/workflows/` (directory, 12 phase files)
- `src/libsexpr/schemas/workflow.sref` — formal schema

#### Files to Modify
- `lua/agents/cognitive/brain.lua` — replace direct phase calls with workflow dispatch
- `docs/cognition/SXL_LANGUAGE_SPECIFICATION.md` — add workflow entity type
- `CMakeLists.txt` — add SXL schema install

#### Acceptance Criteria
- [ ] `(workflow :id "cog-cycle-12" :phases (...))` parses and validates correctly
- [ ] Workflow executor runs all 12 phases in correct order
- [ ] Workflow selector returns correct workflow for each problem type
- [ ] Fallback works: if no workflow is loaded, hard-coded cycle runs unchanged
- [ ] Phase precondition checks work (skip reflection if high-confidence belief exists)

---

### 2.2 Self-Model Expansion (2 weeks)

Runs in parallel with Workflows (no dependency).

#### Deliverables

| # | Deliverable | Files | Notes |
|---|-------------|-------|-------|
| SM-1 | Self-model partition | `src/seedcogd/self_model.h` (new, ~150 lines) | Wrapper around libsmem partition `cognitive/this-node/self-model`. Defines entry types: cognitive_load, memory_pressure, planning_quality, error_history, prediction_accuracy, attention_saturation, learning_rate. |
| SM-2 | Per-cycle population | `src/seedcogd/self_model.c` (new, ~200 lines) | Each cycle, gather all globals into structured SXL and write to partition. `(:type self_model :metric cognitive_load :value 7 :max 10 :trend stable :updated_cycle %d)` |
| SM-3 | Meta-cognition seeding | `src/seedcogd/main.c` — Phase K input | Replace hard-coded keyword domain detection with queries to self-model partition. Phase K reads confidence_calibration, gap_list, strategy_success from self-model instead of computing inline. |
| SM-4 | World model integration | `lua/helpers/world_model.lua` — self layer | Add `self_model` query handler to world_model's explain(). Returns structured summary of all self-metrics. |

#### Effort Breakdown

| Week | Focus | Details |
|------|-------|---------|
| 1 | Partition + population | self_model.h/c, per-cycle write |
| 2 | Integration | Meta-cognition seeding, world model explain() |

#### Files to Create
- `src/seedcogd/self_model.h` (~150 lines)
- `src/seedcogd/self_model.c` (~200 lines)

#### Files to Modify
- `src/seedcogd/main.c` — call self_model_update() each cycle, Phase K input
- `lua/helpers/world_model.lua` — add self layer query
- `CMakeLists.txt` — add self_model.c

#### Acceptance Criteria
- [ ] Self-model partition contains structured entries for all 8 metric domains
- [ ] Each cycle populates current values into partition
- [ ] Phase K reads from self-model instead of computing keyword-based domains
- [ ] `world_model.explain("self")` returns organized summary of all self-metrics

---

## Phase 3: ISA Discipline (Next-Next)

**Duration:** 8-10 weeks
**Prerequisites:** Phase 2 complete (workflow executor provides the composition runtime)

### 3.1 Four-Layer SXL ISA Discipline (6-7 weeks)

#### Deliverables

| # | Deliverable | Files | Notes |
|---|-------------|-------|-------|
| ISA-1 | Operator audit | `docs/NSL/primitive-audit.md` (new) | Audit all 36 operators against the irreducibility test. Classify each as: PRIMITIVE (passes test), COMPOSITE (can be expressed as composition), BOUNDARY (depends on backend). |
| ISA-2 | Core primitive set | `src/libsexpr/include/seed/isa.h` (new, ~100 lines) | Define the reduced primitive set (~25 operators). Each operator gets a struct with: name, arity, precondition predicate, postcondition predicate, cost estimate. |
| ISA-3 | Composite operator library | `lua/operators/` (~15 files) | Rewrite composite operators (reflect, learn, plan, debug, criticise, reconcile, evaluate) as SXL procedure definitions using only primitives. |
| ISA-4 | Macro-expansion system | `src/libsexpr/src/macro.c` (new, ~400 lines) | Expand composite operator calls into primitive sequences. Supports `define`, `call`, `expand` primitives. |
| ISA-5 | Operator metadata registry | `src/libsexpr/src/registry.c` (new, ~300 lines) | Registry of all known operators (primitive + composite). Metadata includes: input types, output types, cost, confidence-effect. Used by workflow optimizer. |
| ISA-6 | Documentation | `docs/NSL/ISA_LAYERS.md` (new) | Define the four layers with examples: Core Objects -> Primitives -> Composites -> Workflows. Map each existing SST/SXP operator to its layer. |

#### Effort

| Week | Focus | Details |
|------|-------|---------|
| 1 | Audit | Apply primitive test to all 36 operators. Document results. |
| 2 | Core set definition | Define ~25 irreducible primitives with formal signatures |
| 3-4 | Composite rewrite | 15 composite operators as SXL procedures |
| 5-6 | Macro-expansion + registry | Build expansion engine and metadata registry |
| 7 | Documentation | Write ISA layers doc, update SXL spec |

#### Files to Create
- `src/libsexpr/include/seed/isa.h` (~100 lines)
- `src/libsexpr/src/macro.c` (~400 lines)
- `src/libsexpr/src/registry.c` (~300 lines)
- `lua/operators/` directory with ~15 composite operator files
- `docs/NSL/primitive-audit.md`
- `docs/NSL/ISA_LAYERS.md`

#### Files to Modify
- `src/libsexpr/CMakeLists.txt` — add macro.c, registry.c
- `src/seed-transformer/include/sst.h` — possibly demote some SST enums to composite markers
- `docs/cognition/SXL_LANGUAGE_SPECIFICATION.md` — update operator hierarchy

---

### 3.2 MCL Dynamic Benchmarking (3-4 weeks)

Runs in parallel with ISA audit (no dependency).

#### Deliverables

| # | Deliverable | Files | Notes |
|---|-------------|-------|-------|
| MCL-1 | Dynamic benchmark suite | `src/libseedllm/src/benchmark.c` (new, ~300 lines) | Sample prompts per capability (completion, reasoning, symbolic, embedding). Run every 100 cycles. Measure latency, tokens/sec, output quality (character diversity, structure compliance). |
| MCL-2 | Expanded model profiles | `src/libseedllm/include/seed/llm.h` — model_info_t | Add fields: measured_latency_ms, measured_tokens_per_sec, quality_score, last_benchmarked_cycle, total_calls, success_count, failure_count. |
| MCL-3 | Cost-aware dispatch | `src/libseedllm/src/dispatch.c` — budget path | Task declares `max_latency_ms`, `min_quality`, `max_cost`. Scheduler selects cheapest backend that satisfies all constraints. If none, return `SEED_LLM_NO_BACKEND`. |
| MCL-4 | Symbolic model profiles | `lua/helpers/model_profiles.lua` (new, ~200 lines) | `(model :id "deepseek-r1" :backend "ollama" :measured_latency_ms 3200 :tokens_per_sec 12.4 :quality_score 0.87 :capabilities (reasoning symbolic))` — published to self-model partition. |

#### Effort

| Week | Focus | Details |
|------|-------|---------|
| 1 | Benchmark infrastructure | benchmark.c, benchmark scheduling |
| 2 | Profile expansion + cost dispatch | model_info_t extension, dispatch logic change |
| 2-3 | SXL profiles | model_profiles.lua, self-model integration |

#### Files to Create
- `src/libseedllm/src/benchmark.c` (~300 lines)
- `lua/helpers/model_profiles.lua` (~200 lines)

#### Files to Modify
- `src/libseedllm/include/seed/llm.h` — model_info_t extension
- `src/libseedllm/src/dispatch.c` — cost-aware dispatch path
- `src/seedcogd/main.c` — trigger benchmark at cycle%100==0
- `CMakeLists.txt` — add benchmark.c

---

## Phase 4: Cognitive Infrastructure

**Duration:** 8-10 weeks
**Prerequisites:** Phase 2 complete (workflows), Phase 3 partial (ISA is helpful but not blocking)

### 4.1 Cognitive Blackboard (5-6 weeks)

#### Deliverables

| # | Deliverable | Files | Notes |
|---|-------------|-------|-------|
| CB-1 | Fact schema | `src/libsmem/schemas/fact.sref` (new) | `(:type fact :domain <str> :confidence <float> :source <str> :content <sxl> :timestamp <uint64> :ttl <int>)` |
| CB-2 | Blackboard partition | `src/seedcogd/blackboard.h` (new, ~200 lines) | Wraps libsmem `cognitive/this-node/blackboard`. API: `publish(fact)`, `query(domain, confidence_min)`, `subscribe(domain_pattern, callback)`, `expire(older_than_cycle)`. |
| CB-3 | Phase migration | All 12 phase call sites in `src/seedcogd/main.c` + `lua/` | Each phase replaces its direct output (dsxl + memory_add) with a blackboard publish. Each phase reads its inputs from blackboard query instead of the entries[] array. |
| CB-4 | Attention-as-blackboard-gate | `src/seedcogd/main.c` — Phase H | Phase H (attention) becomes a blackboard consumer: query all facts, score them, filter below threshold, publish attention-ranked fact list. |
| CB-5 | Cross-domain listener | `lua/helpers/blackboard_listeners.lua` (new, ~200 lines) | Detect patterns across domains: "if prediction.domain.fact contradicts observation.domain.fact, publish contradiction.domain.fact." |

#### Effort

| Week | Focus | Details |
|------|-------|---------|
| 1 | Schema + partition | fact.sref, blackboard.h/c |
| 2-3 | Phase migration (first 6) | Migrate Phases A-D to publish/query pattern |
| 4 | Phase migration (next 6) | Migrate Phases E-L |
| 5 | Attention integration | Phase H as blackboard filter |
| 6 | Listeners | Cross-domain detection, test suite |

#### Files to Create
- `src/seedcogd/blackboard.h` (~200 lines)
- `src/seedcogd/blackboard.c` (~350 lines)
- `src/libsmem/schemas/fact.sref`
- `lua/helpers/blackboard_listeners.lua` (~200 lines)

#### Files to Modify
- `src/seedcogd/main.c` — all 12 phase call sites
- `lua/helpers/working_memory.lua` — use blackboard instead of entries[]
- `lua/helpers/attention.lua` — use blackboard query as input
- `CMakeLists.txt` — add blackboard.c

---

### 4.2 Executive Function Separation (3-4 weeks)

#### Deliverables

| # | Deliverable | Files | Notes |
|---|-------------|-------|-------|
| EF-1 | Executive module | `src/seedcogd/executive.c` (new, ~400 lines) | Separate governance from execution. Executive: (1) select workflow, (2) set mode (explore/exploit), (3) allocate budget, (4) evaluate outcomes, (5) adjust parameters. Never calls LLM directly. |
| EF-2 | Executive SXL output | `src/seedcogd/executive.c` — dsxl per cycle | Per-cycle governance decision published to blackboard: `(:type executive_decision :selected_workflow "cog-cycle-12" :mode "explore" :budget 8 :rationale "planner miss rate < 0.15, diversification warranted")` |
| EF-3 | seedreasond as policy governor | `src/seedreasond/src/main.c` — new policy forms | Add executive policies: `max_budget_per_cycle`, `min_exploration_cycles`, `workflow_override`. seedreasond evaluates these; executive module queries seedreasons before decisions. |
| EF-4 | Decision audit trail | `src/seedcogd/executive.c` | All executive decisions logged to `cognitive/this-node/executive-log` partition (append-only). Enables post-hoc analysis of governance quality. |

#### Effort

| Week | Focus | Details |
|------|-------|---------|
| 1 | Executive module | executive.c: workflow selection, mode setting, budget distribution |
| 2 | Policy integration | seedreasond extension, executive -> policy query |
| 3 | Audit trail + integration | Executive-log partition, cycle integration, test suite |

#### Files to Create
- `src/seedcogd/executive.c` (~400 lines)
- `src/seedcogd/executive.h` (~150 lines)

#### Files to Modify
- `src/seedcogd/main.c` — route governance calls to executive module
- `src/seedreasond/src/main.c` — add executive policy forms
- `src/seedreasond/include/seed/policy.h` — new policy type enums
- `CMakeLists.txt` — add executive.c

---

## Phase 5: Distributed Cognition

**Duration:** 10-14 weeks
**Prerequisites:** Phase 4 complete (blackboard provides the shared fact model)

### 5.1 Distributed Symbolic Cortex (8-10 weeks)

#### Deliverables

| # | Deliverable | Files | Notes |
|---|-------------|-------|-------|
| DSC-1 | Node role advertisement | `src/seedcogd/capability.h` — role field | Add `role` to capability report: `GENERALIST`, `PLANNING_SPECIALIST`, `VISION_SPECIALIST`, `REASONING_SPECIALIST`, `CODEX_SPECIALIST`. Role is auto-detected from benchmarks + configuration. |
| DSC-2 | Cortex routing | `src/seedcogd/delegate.h` — role-aware dispatch | Instead of "who has lowest load?", route by "who has the right role?" Match workflow phase to node role. Fallback to generalist if no specialist available. |
| DSC-3 | libsmem replication for cortex | `src/libsmem/src/replicate.c` — role-filtered sync | Replicate cognitive partitions (not all partitions — only domain-relevant ones). Planning specialist syncs `cognitive/global/workflows` but not `cognitive/global/vision`. |
| DSC-4 | Cortex health monitoring | `src/seedcogd/capability.c` — per-role availability | Track availability of each role in the network. If planning specialist goes offline, distribute planning to next available node. |

#### Effort

| Week | Focus | Details |
|------|-------|---------|
| 1-2 | Role system | Role enum, auto-detection, capability report |
| 3-4 | Routing | Delegate role-aware routing, fallback logic |
| 5-6 | Replication | Role-filtered partition sync |
| 7-8 | Health monitoring | Role availability, failover, rebalancing |

#### Files to Modify
- `src/seedcogd/capability.h` — role enum, role field in capability_t
- `src/seedcogd/capability.c` — role detection, capability announcement with role
- `src/seedcogd/delegate.h` — role-aware peer selection
- `src/seedcogd/delegate.c` — role-aware delegation logic
- `src/libsmem/src/replicate.c` — role-filtered sync
- `src/libsmem/include/seed/smem.h` — role filter parameter for replication

---

### 5.2 Dynamic Ontology (4-5 weeks)

#### Deliverables

| # | Deliverable | Files | Notes |
|---|-------------|-------|-------|
| DO-1 | Pattern discovery module | `lua/helpers/ontology_miner.lua` (new, ~400 lines) | Analyze entries for repeated structural patterns: "entities with :field X always also have :field Y" -> suggest composition relationship. "Two entity types always co-occur" -> suggest merge or relation. Frequency-based, runs every 30 cycles. |
| DO-2 | Ontology proposal pipeline | `lua/helpers/ontology_miner.lua` | Patterns -> SXL ontology proposals `(:proposal_ontology :kind merge :source_type A :target_type B :rationale "..." :confidence 0.6)`. Published to blackboard for Phase K (meta-cognition) evaluation. |
| DO-3 | Ontology approval gate | `lua/helpers/ontology_miner.lua` + `approval.h` | New ontology proposals require human approval if MEDIUM/HIGH risk. Uses existing approval.h infrastructure. Human approves -> ontology schema update. |
| DO-4 | Schema generation | `src/libsexpr/src/schema_gen.c` (new, ~300 lines) | Generate SXL `.sref` schema files from approved ontology proposals. Schema includes type hierarchy, fields, validators. Published to codex. |

#### Effort

| Week | Focus | Details |
|------|-------|---------|
| 1-2 | Pattern discovery | Structural analysis of entries, frequency-based pattern detection |
| 3 | Proposal pipeline | Integration with blackboard + meta-cognition |
| 4 | Approval + schema generation | Approval gate, schema file generation |

#### Files to Create
- `lua/helpers/ontology_miner.lua` (~400 lines)
- `src/libsexpr/src/schema_gen.c` (~300 lines)

#### Files to Modify
- `src/seedcogd/approval.h` — add ontology proposal risk level
- `src/seedcogd/main.c` — call ontology miner at cycle%30==0
- `CMakeLists.txt` — add schema_gen.c

---

## Dependency Graph

```
Phase 1
  BR-1 (entry_t evidence chain) ----+----> BR-2 (belief store)
                                     |
  BR-5 (novelty check) <------------+
  
  CH-1 (diversity tracking) -----> CH-2 (explore/exploit mode) -> CH-3 (budgets)
  CH-4 (consolidation thread) ----+
  CH-5 (oscillation detection) <--+

Phase 2
  CW-1 (workflow SXL type) -> CW-2 (phase definitions) -> CW-4 (executor) -> CW-6 (integration)
  CW-3 (default workflow) <-+
  CW-5 (selector) -------+

  SM-1 (self partition) -> SM-2 (populate) -> SM-3 (meta-cognition seed)
  SM-4 (world model) <-+

Phase 3
  ISA-1 (audit) -> ISA-2 (core set) -> ISA-3 (composite rewrite) -> ISA-4 (macro expansion)
  ISA-5 (registry) -> ISA-6 (docs)
  
  MCL-1 (benchmark) -> MCL-2 (expanded profiles) -> MCL-3 (cost dispatch)
  MCL-4 (SXL profiles) <-+

Phase 4
  CB-1 (fact schema) -> CB-2 (blackboard partition) -> CB-3 (phase migration)
  CB-4 (attention) <-------+
  CB-5 (listeners) <-+

  EF-1 (executive module) -> EF-2 (decisions) -> EF-3 (policy integration) -> EF-4 (audit trail)

Phase 5
  DSC-1 (role system) -> DSC-2 (role routing) -> DSC-3 (role filtered sync) -> DSC-4 (health)
  
  DO-1 (pattern discovery) -> DO-2 (ontology proposals) -> DO-3 (approval) -> DO-4 (schema gen)
```

---

## Effort Summary

| Phase | Components | Weeks | Files Created | Files Modified | Risk |
|-------|------------|-------|---------------|----------------|------|
| 1 | Belief Revision + Homeostasis | 6-8 | 5-6 | 5-6 | MEDIUM — touches core cycle path |
| 2 | Workflows + Self-Model | 6-8 | 16+ | 4-5 | LOW — additive, fallback exists |
| 3 | ISA + MCL Benchmarking | 8-10 | 20+ | 5-6 | HIGH — operator changes may break composites |
| 4 | Blackboard + Executive | 8-10 | 6-7 | 10+ | HIGH — phase migration touches every line of cognitive_tick |
| 5 | Distributed Cortex + Ontology | 10-14 | 3-4 | 8-10 | MEDIUM — networking changes, schema changes |

**Total:** 38-50 weeks (9-12 months) for full implementation.

**Critical path throughput:** Phase 1 -> Phase 2 -> Phase 3 -> Phase 4 -> Phase 5 = 28-42 weeks on the critical path alone, assuming parallel tracks in each phase. With parallel execution of independent work (Self-Model with Workflows, MCL Benchmarking with ISA, Executive with Blackboard), the wall-clock timeline is approximately 34 weeks (8 months) to complete all five phases.

---

## Risk Register

| Risk | Phase | Likelihood | Impact | Mitigation |
|------|-------|------------|--------|------------|
| Belief revision creates feedback loops (confidence oscillation) | 1 | Medium | High — system learns wrong things | Add damping factor (0.3 update cap), monotonicity check |
| Homeostasis budgets cause starvation | 1 | Medium | Medium — phases skip too often | Minimum budget floor (2 LLM calls/cycle), starvation detection |
| SXL workflow definitions don't express all phase semantics | 2 | Medium | Medium — composition is incomplete | Keep hard-coded cycle as master, use SXL for new workflows only |
| ISA audit shows more primitives than expected | 3 | Medium | Low — just reclassification | Accept 35-40 primitives if irreducibility demands it |
| Phase migration to blackboard breaks existing cycle | 4 | High | High — system stops processing | Maintain entries[] array as shadow, migrate phases one at a time |
| Blackboard performance degradation from partition reads | 4 | Medium | Medium — cycle slows | Implement in-memory cache with batching, benchmark before/after |
| Role specialization reduces system resilience | 5 | Medium | Medium — specialist goes offline | Fallback to generalist, automatic role reassignment |

---

## Integration Plan

### With Existing Infrastructure

| Component | Integration Point | Notes |
|-----------|-------------------|-------|
| **libsmem** | New partitions: `cognitive/this-node/beliefs`, `cognitive/this-node/self-model`, `cognitive/this-node/blackboard`, `cognitive/this-node/executive-log` | All append-only logs with SQLite shadow, same as existing memory system |
| **libsexpr** | confidence propagation wiring, ISA operator registry, macro-expansion engine | Extends existing library, no ABI break |
| **libseedllm** | Benchmark-driven model profiles, cost-aware dispatch | Extends existing pool/dispatch, backward-compatible |
| **seedreasond** | Executive policy forms | Extends policy evaluation vocabulary |
| **Bus (T1)** | Blackboard fact publication for cross-node cortex | Uses existing org.seed.cognition.** topics |
| **D1-D5** | Role-aware delegation (extends D3 capability, D5 delegation) | Additive to existing distributed cognition stack |
| **Lua helpers** | Workflow executor, ontology miner, blackboard listeners | All new modules, coexist with existing ones |

### Backward Compatibility

- **Phase 1-2:** Fully backward-compatible. Existing cognitive cycle runs unchanged. Belief revision and workflows are additive.
- **Phase 3:** Operator demotion changes SST enum meanings. Requires bumping SST version to v2. Old SXL expressions with v1 operator references still parse but map to composite expansion.
- **Phase 4:** Blackboard migration is the breaking change. Phase-by-phase migration with entries[] shadow ensures no data loss. Rollback: set `SEED_BLACKBOARD=0` to use entries[] exclusively.
- **Phase 5:** Role system extends capability advertisement. Old nodes without roles are treated as GENERALIST. No backward-compatibility break.

---

## Measurement: How to Know Each Phase Succeeds

### Phase 1 Metrics
- **Belief convergence**: Same topic asked 5 times across 50 cycles produces 1 belief entry (not 5) with increasing confidence
- **Homeostasis effectiveness**: Cycles with health entry showing `oscillation=false` after initial detection
- **Budget adherence**: Actual LLM calls per cycle <= budget cap (measured over 100-cycle window)

### Phase 2 Metrics
- **Workflow coverage**: % of cycles using workflow executor vs hard-coded fallback (target: >80% after Phase 2)
- **Workflow selection accuracy**: % of problem-type -> workflow selections that complete without error

### Phase 3 Metrics
- **Operator reduction**: Number of "primitive" operators after audit (target: 25-30)
- **Composite decomposition**: % of composite operator calls that successfully expand to primitives
- **Dispatch quality**: % of model selections that meet task constraints (latency, quality, cost)

### Phase 4 Metrics
- **Blackboard adoption**: % of phases publishing to blackboard vs direct output
- **Executive effectiveness**: % of executive decisions that improve next-cycle metrics (prediction error down, confidence up)

### Phase 5 Metrics
- **Specialist utilization**: % of phase executions routed to specialist nodes (target: >60%)
- **Ontology growth**: New entity types added per 100 cycles after Phase 5 (target: 1-3)
- **Proposal acceptance rate**: % of ontology proposals approved (target: >20%, prevents noise)

---

## Quick Reference: File Map

### Phase 1
```
src/seedcogd/belief.h          — belief store API
src/seedcogd/belief.c          — update pipeline + cycle integration
src/seedcogd/health.h          — homeostasis types and globals
tests/test_belief.c            — belief revision test suite
```

### Phase 2
```
lua/helpers/workflow_executor.lua   — workflow orchestrator
lua/helpers/workflow_selector.lua   — problem-type -> workflow
lua/helpers/workflows/              — 12 phase SXL definitions
src/seedcogd/self_model.h           — self-model partition API
src/seedcogd/self_model.c           — per-cycle population
```

### Phase 3
```
src/libsexpr/include/seed/isa.h     — reduced primitive set
src/libsexpr/src/macro.c            — macro-expansion engine
src/libsexpr/src/registry.c          — operator metadata registry
lua/operators/                      — composite operator definitions
src/libseedllm/src/benchmark.c      — dynamic benchmarking
lua/helpers/model_profiles.lua      — SXL model profiles
docs/NSL/primitive-audit.md         — operator audit results
docs/NSL/ISA_LAYERS.md              — four-layer ISA documentation
```

### Phase 4
```
src/seedcogd/blackboard.h           — blackboard API
src/seedcogd/blackboard.c           — blackboard partition + listeners
src/seedcogd/executive.h            — executive module API
src/seedcogd/executive.c            — governance logic
src/libsmem/schemas/fact.sref       — fact schema
lua/helpers/blackboard_listeners.lua — cross-domain pattern detection
```

### Phase 5
```
lua/helpers/ontology_miner.lua      — pattern discovery + proposals
src/libsexpr/src/schema_gen.c       — schema file generation
```

---

*End of ROADMAP.md*
