# GAP-ANALYSIS — NSL/NSP Implementation Gap Assessment

> **Assessment:** Current S.E.E.D. v21 codebase evaluated against `seed-cog3-specs.txt`
> and `seed-misc-specs.txt`.
>
> **Date:** 2026-07-16
> **Evaluator:** seedcogd architecture audit
> **Status:** Complete — 19 gap areas identified, 6 contradictions documented, 7 priority recommendations produced

---

## Executive Summary

The S.E.E.D. codebase (v21, commit c4bd98a) has a strong operational foundation:
a working 12-phase cognitive cycle (A-L) in `src/seedcogd/main.c` (3212 lines), a
5-backend LLM abstraction in `libseedllm` (~15 source files), a multi-tier bus
(T0/T1/T2) in `libbus`, a symbolic memory system with replication in `libsmem`
(~20 source files), an S-expression engine with confidence propagation in `libsexpr`
(8 source files, 1711 lines), and 25 Lua helper modules totaling 10,619 lines.

However, the speculative architecture documents describe capabilities that are
partially or entirely absent. The analysis below maps each proposal to specific
code evidence, identifies contradictions between the specs and the codebase as
it evolved, and ranks the gaps by impact.

**The three most impactful gaps are:**
1. **Belief Revision** (0% implemented) — No mechanism to update prior knowledge
   with new evidence. Every discovery is treated as new regardless of prior
   conclusions.
2. **Cognitive Homeostasis** (0% implemented) — No regulation prevents runaway
   cognitive loops, excessive repetition, or resource exhaustion.
3. **Cognitive Workflows** (0% implemented) — The 12-phase cycle is a fixed
   algorithm, not an adaptive composition of selectable workflows.

---

## 1. Current Implementation Baseline

### 1.1 Daemon Topology

| Daemon | Path | Purpose | Lines |
|--------|------|---------|-------|
| **seedcogd** | `src/seedcogd/main.c` | 12-phase cognitive cycle | 3212 |
| **seedcored** | `src/seedcored/src/main.c` | Runtime service registry, epoch management | ~1200 |
| **seedreasond** | `src/seedreasond/src/main.c` | SXL policy evaluation, Ed25519 bundle verify | 1104 |
| **seedneted** | `src/seedneted/` | Noise-IK T2 encrypted sessions, topic forwarding | — |
| **seedsysresd** | `src/seedsysresd/` | CPU/memory monitoring via proc, cgroups | — |
| **seedbusbrokerd** | `src/bus-broker/` | T1 UDS broker | — |

### 1.2 12-Phase Cognitive Cycle (seedcogd)

The cycle runs in `cognitive_tick()` at line 1605 of `main.c`:

| Phase | Lines | Frequency | Function |
|-------|-------|-----------|----------|
| **A** — Parallel LLM | 1718-1844 | Every cycle | 3 parallel threads: reflection, evaluation, discovery. Uses multi-model consensus when >= 3 backends. Delegation to peers via D5 if overloaded. |
| **B** — Contradiction + Plan | 1845-1869 | Every cycle | Check for contradicting entries; code generation pipeline every 3rd cycle. |
| **C** — Consolidation | 1870-1985 | Every 5 cycles | Hippocampus compose (merge same-source), generalise (extract cross-source patterns), forget (decay + tombstone). |
| **D** — Prediction | 1453-1601 | Every cycle | `predict_next_state()` — gather recent observations, dispatch to SST backend, forecast cycle+1 entries. |
| **E** — Learning | 1987-2116 | Every cycle | Metrics detection (prediction error, confidence trends, drop rates, backend health). Propose improvements; auto-deploy if confidence > 0.98. |
| **F** — Language Evolution | 2120-2217 | Every 20 cycles | Detect parse failures, unrecognized `:type` values, translator gaps. Propose SXL extensions via SST. |
| **G** — Vision | 2218-2235 | Every 30 cycles | Publish perceptual state; Lua `vision_translator.lua` processes. |
| **H** — Attention | 2247-2343 | Every cycle | 6-dimension scoring (urgency 0.25, importance 0.25, novelty 0.20, goal_relevance 0.15, prediction_error 0.10, recency 0.05). **Telemetry-only — no resource gating.** |
| **I** — Working Memory | 2346-2454 | Every cycle | Temporal decay at 0.92x/cycle, purge below 0.05 floor, evict at soft cap 64/80. 4 eviction policies in Lua. |
| **J** — Goal Management | 2457-2608 | Every 7 cycles | Extract goal structure from plans/proposals, detect conflicts, compute utility scores. |
| **K** — Meta-Cognition | 2621-2781 | Every 11 cycles | Confidence calibration (over/under-confidence detection vs prediction error), 8-domain coverage analysis, 6-strategy success evaluation. |
| **L** — Creativity | 2793-2930 | Every 13 cycles | 4-dimension novelty scoring, diversity detection, stagnation measurement, strategy recommendation. |

### 1.3 Library Stack

- **libsexpr** (`src/libsexpr/`, 1711 lines) — S-expression engine: arena-based memory (4096 cells, depth 32). Parse, canonicalize, validate, query, transform (merge/split/criticise), confidence propagate (6 rules: deductive, probabilistic, Bayesian, Dempster-Shafer, fuzzy, decay).
- **libsmem** (`src/libsmem/`, ~20 files) — Two-dimensional partition model (scope/reach/name). Append-only log with segment rotation, SQLite shadow with FTS5. Entry signing, replication with capability tokens and vector clocks. Datachain for accountability.
- **libseedllm** (`src/libseedllm/`, ~15 files) — 5 backends: Ollama, native (llama.cpp), OpenAI-compatible, SST (symbolic), UDS sidecar. Pool with health tracking. Consensus (parallel multi-model response synthesis). Intent-based dispatch with task complexity classification.
- **libbus** (`src/libbus/`) — T0 (in-process ring), T1 (UDS broker request/reply), T2 (cross-network Noise-IK encrypted).
- **libdfs** (`src/libdfs/`) — Content-addressed blob store: BLAKE3-256, 2-byte fan-out sharding, atomic put (write-temp + rename), idempotent dedup.

### 1.4 Lua Layer

25 helper modules totaling 10,619 lines in `lua/helpers/`. Largest: `consolidation.lua` (1005), `language_evolution.lua` (1010), `decision_engine.lua` (820), `goal_manager.lua` (617), `self_improve.lua` (581), `metacognition.lua` (544), `learning.lua` (529).

### 1.5 Distributed Cognition Stack (D1-D5)

Implemented in `src/seedcogd/`:
- **D1**: T2 sessions via `seedneted` (Noise-IK + datachain) — functional
- **D2**: Cross-node entry sync via T1 bus publish on `org.seed.cognition.entry` — functional (line 1164-1184)
- **D3**: Capability advertisement via `org.seed.cognition.capability` — functional (`capability.h`, 206 lines)
- **D4**: KG bloom filter sync — functional (`kg_sync.h`, 175 lines, 1024-byte bloom, 4 hash functions)
- **D5**: Workload delegation — functional (`delegate.h`, 175 lines, 7 delegatable phases)

---

## 2. Gap Analysis: seed-cog3-specs.txt

### Gap 2.1: Four-Layer SXL ISA (proposal lines 3100-3693)

**Proposal summary:**
Four distinct layers: (1) ~30-40 Core Symbolic Objects (nouns), (2) ~25-40 Primitive Operators (irreducible ISA, passes the "primitive operator test"), (3) ~100-300 Composite Operators (standard library expressed in SXL, not C/Lua), (4) Cognitive Workflows (symbolic objects the engine can inspect, rewrite, and compose).

**Current state:**
- ~30 entity types documented in `docs/cognition/SXL_LANGUAGE_SPECIFICATION.md` — partially implemented
- 22 SST operators (`src/seed-transformer/include/sst.h:86-109`): `SST_OP_OBSERVE` (0) through `SST_OP_TRAIN` (21)
- 14 SXP cognitive operators defined in `docs/cognition/SXL_LANGUAGE_SPECIFICATION.md` (compare, infer, explain, simulate, project, reflect, criticise, merge, split, abstract, reconcile, evaluate, reinforce, decay)
- **No formal layering.** SST operators and SXP operators coexist at different abstraction levels with no documented hierarchy.
- **No primitive operator test.** `SST_OP_REFLECT` (line 98) is structurally composite (should decompose into retrieve, compare, evaluate, generate, store) but is treated as primitive.
- **Composite operators are C or Lua functions**, not SXL procedures. No composition system exists.
- **No macro-expansion or procedure definition mechanism** in the SXL runtime.

**Key evidence:**
- `src/seed-transformer/include/sst.h:86-109`: All 22 operators are enums at the same level — no layering.
- `src/libsexpr/src/transform.c:517`: Dempster-Shafer merge implemented as C, not SXL.
- `src/libsexpr/include/seed/sexpr.h` (lines 40-70): SXP API has `sxp_oper_merge`, `sxp_oper_split`, `sxp_oper_criticise` — all free-standing C functions.
- `docs/cognition/SXL_LANGUAGE_SPECIFICATION.md:53-98`: Entity hierarchy defined in text, not in executable SXL schemas.

**Severity: Architecture-level.** The ISA layering is a prerequisite for the "cognitive compiler" described in the spec. Without it, every new capability adds a new "primitive" rather than composing from existing ones. Operator proliferation without a composition system makes the cognitive vocabulary unmanageable at scale.

---

### Gap 2.2: Cognitive Workflows (proposal lines 2047-2564, 3469-3500)

**Proposal summary:**
A library of workflows (scientific, engineering, debug, learning, creative, ethical, strategic) defined as SXL objects. The engine selects workflows by problem type, customizes them, executes them step by step, evaluates results, and improves workflow definitions over time. Key insight: "workflow itself becomes symbolic."

**Current state:**
- **Zero workflow infrastructure.** The 12-phase cognitive_tick() at lines 1605-2931 is a single hard-coded pipeline.
- Phase scheduling uses fixed coprime intervals (cycle%5, cycle%11, cycle%13) — no problem-type-based selection.
- Intents (reflection, evaluation, creative, planning, code_gen, symbolic) are used only for LLM routing, not for workflow selection.
- No `(workflow ...)` SXL object type exists.
- No workflow executor, selector, or evaluator exists.

**Key evidence:**
- `src/seedcogd/main.c:1605`: `void cognitive_tick(void)` — monolithic function, 1326 lines.
- `src/seedcogd/main.c:1686`: `int queue_depth = 3;` — hard-coded parallel depth.
- `src/seedcogd/main.c:1870`: `if (cycle % 5 == 0)` — consolidation frequency.
- `src/seedcogd/main.c:2621`: `if (cycle % 11 == 2)` — meta-cognition frequency.
- `src/seedcogd/main.c:2793`: `if (cycle % 13 == 3)` — creativity frequency.
- `lua/agents/cognitive/brain.lua:203-248`: Command dispatch loop — sequential, not workflow-based.

**Severity: Highest architectural gap.** This is the spec's "if I could only add one thing." Without workflows, the cognitive cycle cannot adapt to problem type, cannot be customized, and cannot improve its own structure. The fixed cycle is the single most rigid aspect of the architecture.

**Mitigation opportunity:** The 12 phases are already modular — each operates on the same `entries[]` array and calls the same `chat()` function. Extracting each phase into an SXL workflow definition is feasible without disrupting the rest of the cycle.

---

### Gap 2.3: Workflow Synthesis Engine (proposal lines 3687-3693)

**Proposal summary:**
"When none of the existing workflows adequately satisfy the current goal, S.E.E.D. reasons over the symbolic properties of its primitive operators — preconditions, postconditions, resource costs, information effects, confidence propagation, and semantic contracts — to synthesize a new workflow."

**Current state:**
- **Not implemented.** This depends entirely on Gap 2.1 (operator metadata) and Gap 2.2 (workflow infrastructure).
- No operator metadata (preconditions, postconditions, costs) exists.
- No workflow synthesis capability exists at any level.

**Severity: Advanced research capability.** Cannot be implemented until the ISA discipline (Gap 2.1) and workflow infrastructure (Gap 2.2) exist. Not a priority for the near term.

---

### Gap 2.4: DataChain as Cognitive Timeline (proposal lines 2823-2878)

**Proposal summary:**
"Every cognitive event is linked — Observation -> Thought -> Decision -> Action -> Result -> Reflection -> Lesson — forming a hash-linked chain. Almost like Git. Or a blockchain. Except semantic."

**Current state:**
- The datachain (`src/libsmem/src/datachain.c`) exists but is an **accountability ledger for infrastructure events**, not a cognitive timeline.
- Block types per `docs/network/DATACHAIN.md`: `trust.granted`, `cap.issued`, `channel.opened`, `schema.activated` — all infrastructure operations.
- The cognitive journal (`cog-journal.jsonl`) stores cognitive entries as flat JSONL with base64-encoded SXL.

**Key evidence:**
- `src/seedcogd/main.c:1155-1158`: Journal entries: `{"ts":"...","source":"reflection","cycle":%d,"confidence":0.95,"provenance":"seedcogd-v9","sxl_b64":"..."}` — flat JSONL, no hash links.
- `docs/network/DATACHAIN.md` (line 5): "The datachain is not a blockchain. It is not a consensus mechanism. It is a Merkle-linked local log used for accountability and forensics."
- `src/libsmem/src/datachain.c`: Block format has `@parent`, `@hash`, `@sig`, `prev_hash`, `state_root` — infrastructure scope only.

**Severity: Medium-high.** The cognitive journal is the primary evidence of the system's cognition. Making it hash-linked would enable provenance verification. The infrastructure (datachain blocks) exists; routing cognitive entries through the datachain API instead of flat JSONL is a storage layer change.

---

### Gap 2.5: DFS as Distributed Symbolic Cortex (proposal lines 2884-2991)

**Proposal summary:**
"Distributed Symbolic Cortex — nodes specialize (vision, science, engineering, planning). Each node maintains its own symbolic memory. The network reasons collectively, routing cognitive work to specialized peers."

**Current state:**
- `libdfs` (`src/libdfs/`) is a content-addressed **blob store** — not a distributed symbolic memory.
- Address format: `blake3:<64hex>:<size>` — pure content hash, no semantic routing.
- On-disk store: 2-byte fan-out sharding (256-entry directories) — filesystem layout.
- Node capability advertisement (D3 in `capability.h`) enables workload **delegation** (offload a phase to a peer with capacity), not **role specialization** (this node is the vision specialist).

**Key evidence:**
- `src/libdfs/include/seed/dfs.h:100+`: API = `put`, `get`, `has`, `open`, `close` — file operations, no cognitive data model.
- `docs/network/DFS.md:2-6`: Explicit non-goals: "not a POSIX filesystem," "not general-purpose distributed filesystem," "strong consistency not a goal."
- `src/seedcogd/capability.h:206`: `seed_cog_capability_best_peer()` — matches on domain string + backend count + CPU load. No role-based routing.
- `src/seedcogd/kg_sync.h:175`: KG sync uses bloom filter for index discovery. On-demand fetch, not distributed cortex.

**Severity: Architecture-level.** The DFS would need to be fundamentally redesigned. The current DFS is explicitly scoped as a blob store and its non-goals conflict with the spec's requirements for a distributed symbolic memory. A separate layer on top of `libsmem` replication (which already exists) would be a better foundation.

---

## 3. Gap Analysis: seed-misc-specs.txt

### Gap 3.1: Model Cognition Layer (proposal lines 1-490)

**Proposal summary:**
Rich model profiles (20+ fields: `:id`, `:backend`, `:modality`, `:parameters`, `:context`, `:quantization`, `:supports_tools`, `:supports_reasoning`, `:vision`, `:embedding`, `:latency`, `:tokens_per_second`, `:memory_required`, `:cost`, `:availability`). Dynamic benchmarking. Cost-aware reasoning with budgets. Multi-level orchestration (cloud planner + local executors).

**Current state:**
- Model info at `src/libseedllm/include/seed/llm.h:87-96`: 8 fields (name, backend, param_count_b, context_len, embedding_dim, capabilities bitmask, est_latency_ms, cost_factor).
- Capabilities bitmask: 7 flags (completion, tools, vision, thinking, insert, embedding, symbolic, image_gen).
- Task classification: LIGHT, MEDIUM, HEAVY, CRITICAL (`src/libseedllm/src/task_classify.c`).
- Dispatch: routes by intent name string match (`src/libseedllm/src/dispatch.c`).
- Model probing: at startup and SIGHUP only (`src/seedcogd/main.c:367-410`).

**Detailed gaps:**
- No symbolic capability profiles — no `(model ...)` SXL expressions
- No dynamic benchmarking — probing is static (startup + SIGHUP)
- `cost_factor` stored but never read in any scheduling path
- No queue depth or load tracking per backend
- No multi-level orchestration (cloud planner + local executors)
- No budget system for inference resources
- No per-model quality tracking (success rates, prediction accuracy)

**Severity: Medium.** The infrastructure pool (5 backends, health tracking, dispatch) is already in place. The gaps are in the metadata richness, dynamic benchmarking, and scheduling intelligence.

---

### Gap 3.2: Cognitive Blackboard (proposal lines 498-528)

**Proposal summary:**
"Instead of agents talking directly to each other, create a shared symbolic workspace. Every cognitive process publishes and subscribes to symbolic facts. Perception, reasoning, planning, memory, and reflection all contribute to and read from the same shared space."

**Current state:**
- **Not implemented as a blackboard.** Three closest approximations:
  1. The bus (pub/sub for events — not a shared state workspace)
  2. The seedcogd `entries[]` array (in-process, seedcogd-private)
  3. `world_model.lua` (Lua process-scoped)

**Key evidence:**
- `lua/agents/cognitive/brain.lua:206-218`: cognitive_tick reads from `seed.mem.get("cognitive/this-node/inbox")` — point-to-point queue, not a blackboard.
- `src/seedcogd/main.c:2329-2342`: Attention scores logged via `dsxl("attention-gate", ...)` but not published to a shared fact space.
- No shared fact schema `(:type fact :domain <str> :confidence <float> :source <str> :content <sxl>)` exists.
- No fact listener pattern for cross-domain pattern detection.

**Severity: Medium.** This is primarily a decoupling and extensibility issue. The blackboard would replace the hard-coded phase dependencies with a publish-query pattern, making the system extensible without modifying `cognitive_tick()`.

---

### Gap 3.3: Attention Manager (proposal lines 530-575)

**Proposal summary:**
"The engine continuously decides what deserves cognitive resources" — importance, novelty, urgency, goal relevance, prediction error, user attention, resource cost -> Attention -> Working Memory. Attention scarcity drives prioritization.

**Current state:**
- Phase H (`src/seedcogd/main.c:2247-2343`): 6-dimension scoring implemented.
- `attention.lua` (437 lines): Configurable budgets, signal ranking, stochastic attention decay.
- **BUT:** Attention output is telemetry-only. No phase is gated by attention scores. No resource cost dimension. No feedback loop from attention to scheduling.

**Key evidence:**
- `src/seedcogd/main.c:2329-2342`: Attention results logged via `dsxl("attention-gate", ...)`. Results are never read back.
- `src/seedcogd/main.c:2336-2342`: Attention is computed per entry but no code gates any subsequent phase based on it.
- `lua/helpers/attention.lua:320-330`: Scoring logic exists but outputs are consumed as telemetry only.

**Severity: Medium-low.** The scoring infrastructure exists. The gap is in converting scores into action — adding a threshold gate before Phase A that selects which entries to reflect on based on attention scores, and a feedback loop that adjusts scoring weights based on prediction error.

---

### Gap 3.4: Prediction Everywhere (proposal lines 577-599)

**Proposal summary:**
"Every subsystem predicts: 'I expect to need this memory soon,' 'The object should still be here,' 'GPU temperature will exceed threshold,' 'This task will probably fail.' Prediction errors become learning signals."

**Current state:**
- Prediction exists only for the next cognitive cycle. `prediction.lua` (190 lines) + Phase D at `src/seedcogd/main.c:1453-1601`.
- Predictions are limited to type/status/confidence of expected entries for cycle+1.
- Check at `src/seedcogd/main.c:1458-1516`: compares predicted type against actual observations for the predicted cycle.

**Key evidence:**
- `src/seedcogd/main.c:1521-1602`: `predict_next_state()` gathers recent observations, sends to SST backend, stores predictions in `predictions[]` array.
- `src/seedcogd/main.c:418-426`: `prediction_t` struct has `sxl`, `cycle_made`, `cycle_target`, `confidence`, `predicted_type` — limited to type-level predictions.
- No predictions for: memory access patterns, resource utilization, task outcomes, confidence shifts.

**Severity: Medium.** The prediction mechanism (gather -> predict -> compare -> learn) exists and works. Extending it to other subsystems requires adding prediction hooks in those subsystems, not building a new framework.

---

### Gap 3.5: Multi-Layer Memory with Promotion (proposal lines 601-649)

**Proposal summary:**
"Sensory Buffer -> Working Memory -> Episode -> Concept -> Principle -> Ontology -> Identity. Reflection promotes information upward. Most information never reaches long-term memory."

**Current state:**
- Working memory exists (Phase I, `working_memory.lua` 424 lines).
- Long-term memory exists (libsmem partitions with append-only log + SQLite shadow).
- Consolidation exists (Phase C, `hippocampus.lua` 330 lines, `consolidation.lua` 1005 lines).
- **BUT:** The promotion pipeline is not implemented as a hierarchy. Consolidation composes entries and extracts abstractions but does not systematically promote through the spec's seven layers.

**Key evidence:**
- `src/seedcogd/main.c:1871-1985`: Consolidation has compose (merge same-source entries) then generalise (extract cross-source patterns). Two stages, not seven layers.
- `lua/helpers/hippocampus.lua:330`: Episodic to semantic bridge — single transition, not a pipeline.
- `lua/helpers/consolidation.lua:1005`: Detailed consolidation with forgetting but no explicit layer hierarchy.
- No gating logic at each layer ("most information never reaches long-term memory").
- No identity-level consolidation (beliefs about self that persist across sessions).

**Severity: Medium.** The storage infrastructure for a multi-layer hierarchy exists. The gap is in the promotion logic — the algorithms that decide when episodic patterns become concepts, when concepts become principles, etc.

---

### Gap 3.6: Belief Revision Engine (proposal lines 651-669)

**Proposal summary:**
"Instead of storing facts, store beliefs — Earth radius: Confidence 0.99999, Source: Scientific literature. New evidence updates beliefs. Prior beliefs constrain new beliefs."

**Current state:**
- **Not implemented.** Entries carry scalar confidence (set once, never updated upward).
- No mechanism stores evidence sources as part of a belief.
- No mechanism updates prior beliefs when new confirming or disconfirming evidence arrives.
- Confidence is set once at creation (`atof(conf) : 0.95`) and decays linearly (0.85x per cycle, floor at 0.2).
- The confidence propagation library (`src/libsexpr/src/confidence.c`) has 6 rules but is **not wired into any belief revision pipeline** — it is used only during explicit SXP transform operations.

**Key evidence:**
- `src/seedcogd/main.c:188-189`: `e->confidence = conf[0] ? atof(conf) : 0.95` — initial confidence from SXL or default 0.95.
- `src/seedcogd/main.c:449-454`: `memory_decayed_confidence()` multiplies by 0.85 per cycle — decay-only, no increase mechanism.
- `src/seedcogd/main.c:1959-1964`: Consolidation applies decay: `entries[i].confidence *= decayed` — never increased.
- `src/libsexpr/src/confidence.c:38-118`: `sxp_confidence_propagate()` implements 6 rules but is only reachable through explicit `sxp_oper_infer()` calls in `src/libsexpr/src/transform.c:765` — not in the cognitive cycle.
- No evidence chain field in any entry struct (`src/seedcogd/main.c:168-198`): `entry_t` has `sxl`, `ts`, `cycle`, `source`, `type`, `entity_id`, `confidence`, `vec` — no `evidence_chain`.

**Severity: CRITICAL.** This is the most impactful single gap. The spec's #1 critique ("the journal repeatedly rediscovers the same things") is a direct consequence of missing belief revision. Without it:
1. Every discovery is treated as new — there is no check against prior settled beliefs.
2. The system cannot learn that it has already solved a problem.
3. Confidence monotonically decreases — nothing the system learns ever becomes *more* certain.
4. The "novelty detection" in Gaps A and L is purely syntactic (trigram overlap), not semantic.

**Implementation path:** The confidence propagation algebra already exists in `libsexpr`. The gaps are: (a) adding evidence chain fields to entries, (b) implementing a belief store that supports update semantics (not just append), (c) wiring contradiction detection into belief updates (contradicting entries reduce confidence), (d) adding a "novelty check" before Phase A that skips reflection on established beliefs, (e) adding confirming-evidence-based confidence increase.

---

### Gap 3.7: Internal Simulation Engine (proposal lines 671-713)

**Proposal summary:**
"Instead of asking an LLM 'What happens?', the engine simulates — Current World -> Apply Action -> Future World -> Evaluate -> Choose. The simulation can be symbolic. Only difficult parts require AI."

**Current state:**
- `simulation.lua` (231 lines) exists with `run()` (scenario/steps/instruction) and `adversarial_test()` (hypothesis testing).
- SST defines `SST_OP_SIMULATE = 3` at `src/seed-transformer/include/sst.h:90`.
- **BUT:** Simulation is called only from brain.lua's command dispatch (manual trigger), not from the cognitive cycle.
- Simulation world model is separate from the main world model.
- Results are not fed into decision-making or planning.

**Key evidence:**
- `lua/helpers/simulation.lua:run()` — creates a fresh scenario context, does not use the main `world_model`.
- `lua/agents/cognitive/brain.lua:151-158` — simulation is a command (`"simulate"`), not an automatic cognitive phase.
- `src/seedcogd/main.c` — no simulation phase in the 12-phase cycle.
- No simulation result integration into Phase B (planning) or Phase J (goal management).

**Severity: Medium.** The building blocks exist (scenario runner, SST operator, Lua module). Wiring simulation into the cognitive cycle and feeding from the world model is straightforward engineering.

---

### Gap 3.8: Meta-Cognition (proposal lines 715-741)

**Proposal summary:**
"Why did I choose this model? Was it correct? Could another model be cheaper? How much confidence? What assumptions existed? What failed? Should policies change?"

**Current state:**
- Phase K (`src/seedcogd/main.c:2621-2780`): Confidence calibration (prediction error EMA comparison), knowledge gap detection across 8 domains, strategy evaluation (success rate per cognitive phase).
- `metacognition.lua` (544 lines): Confidence recalibration (EMA with asymmetric adjustment), question generation (10 archetypes), strategy evaluation (8 strategy types).

**Detailed gaps:**
- **No per-model calibration.** Global prediction error EMA only (`g_prediction_error`).
- **Domain coverage is keyword-based.** Lines 2651-2682: domain detection by substring match ("security", "performance", etc.) — no semantic boundary model.
- **No model selection analysis.** No tracking of which model was used for which inference and how it performed.
- **No assumption tracking.** The cognitive cycle generates conclusions but does not record the assumptions that led to them.
- **No policy change recommendations.** Meta-cognition SXL is published but not read back to adjust the cycle.
- **No strategy execution tracking.** Strategies are evaluated but their recommendations are not followed up.

**Key evidence:**
- `src/seedcogd/main.c:2625-2646`: `double global_pe = g_prediction_error;` — single global scalar for calibration.
- `src/seedcogd/main.c:2651-2682`: `strstr(entries[sm_res[i]].sxl, "security")` — keyword domain detection.
- `src/seedcogd/main.c:2780`: Phase K outputs SXL via `dsxl("meta-cognition", ...)` — outputs published, never consumed.

**Severity: Medium.** The meta-cognition infrastructure is surprisingly solid for an initial implementation. The gaps are in depth (per-model calibration, semantic domains) and in closing the loop (using meta-cognition to modify cognitive parameters).

---

### Gap 3.9: Cognitive Energy (proposal lines 747-775)

**Proposal summary:**
"Every task has a cost: CPU, RAM, GPU, latency, API cost, battery, network, context, attention. Planning becomes constrained optimization — maximize cognitive value within resource budget."

**Current state:**
- **Minimally implemented.** `seedsysresd` monitors CPU/RAM via `/proc/stat` and `/proc/meminfo`.
- `libseedllm` tracks latency per slot.
- `seedcogd` has adaptive timing: `gap_seconds` adjusted based on `avg_llm_ms` (line 1304).

**Detailed gaps:**
- No GPU monitoring.
- No network cost tracking.
- No API cost accounting (important for OpenAI backend usage).
- No context window utilization tracking.
- No unified resource model across compute, memory, latency, and cost.
- No constrained optimization in planning or dispatch.

**Key evidence:**
- `src/seedsysresd/src/proc_sample.c` — reads `/proc/stat` and `/proc/meminfo` only.
- `src/seedcogd/main.c:1301-1304`: `avg_llm_ms=avg_llm_ms*0.7+ms*0.3;` — latency EMA drives `gap_seconds` but no other resource feedback.
- `src/libseedllm/src/pool.c` — slot latency tracking but no energy model.

**Severity: Low-medium.** This is an optimization, not a missing capability. The system functions without it. Worth adding when the MCL is expanded (Gap 3.1), since cost awareness is part of model selection.

---

### Gap 3.10: Dynamic Ontology (proposal lines 777-815)

**Proposal summary:**
"The ontology shouldn't be fixed. Observe -> Find patterns -> Suggest concepts -> Reflect -> Accept -> Update ontology."

**Current state:**
- **Not implemented.** The SXL entity hierarchy is fixed in `docs/cognition/SXL_LANGUAGE_SPECIFICATION.md`.
- Phase F (Language Evolution, `src/seedcogd/main.c:2124-2217`) detects parse failures and unrecognized `:type` values and proposes extensions — but this is **syntactic** gap detection, not **ontological** pattern discovery.

**Key evidence:**
- `src/seedcogd/main.c:2138-2200`: Language evolution detects patterns like `(:parse_error`, `unrecognized :type`, `cannot translate` — all parse-level failures.
- `docs/cognition/SXL_LANGUAGE_SPECIFICATION.md:53-98`: Entity hierarchy documented as fixed.
- No ontology/ directory in the codex.
- No mechanism analyzes entry patterns and suggests new entity types.

**Severity: Low-medium.** Dynamic ontology is a research capability. The system can function for long periods with a fixed ontology. Not a priority for the near term.

---

### Gap 3.11: Self Model (proposal lines 877-926)

**Proposal summary:**
"S.E.E.D. literally understands itself" — cognitive load, memory pressure, planning quality, reflection quality, vision confidence, reasoning confidence, attention saturation, learning rate, error history, agent trust, backend health, model performance.

**Current state:**
- `ingest_self_model()` at `src/seedcogd/main.c:1311-1319` writes a static self-model snapshot at startup.
- `world_model.lua` has a "self" layer.
- Runtime metrics tracked as globals: `g_prediction_error`, `stored`, `dropped`, `avg_llm_ms`, `n_entries`, `n_relations`, `n_vectors`.
- **BUT:** No unified self-model partition. Metrics are scattered globals never assembled into a self-model SXL that the system could query.

**Key evidence:**
- `src/seedcogd/main.c:1311-1319`: Self-model entries are: identity (static), codebase-stats (static), capabilities (static string), codex-summary (static), system-status (static) — all set once at startup, never updated.
- `src/seedcogd/main.c:348-351`: Globals: `cycle`, `stored`, `dropped`, `avg_llm_ms`, `gap_seconds` — tracked but never structured.
- `src/seedcogd/main.c:417-430`: `g_prediction_error`, `n_predictions` — tracked for meta-cognition but not in self-model.
- `src/seedcogd/main.c:340`: `static FILE *journal` — no self-model pointer or partition ID.

**Severity: Medium.** The metrics are all being tracked. The gap is in assembling them into a structured self-model partition (`cognitive/this-node/self-model`) and updating it each cycle. This is low-effort and high-leverage since it enables all self-referential capabilities (homeostasis, meta-cognition, executive function).

---

### Gap 3.12: Executive Function (proposal lines 957-993)

**Proposal summary:**
"Separate thinking from execution. Executive -> Mission -> Planner -> Scheduler -> Workers -> Reflection. The executive never performs inference. It governs cognition."

**Current state:**
- The cognitive engine combines executive, planner, scheduler, and worker into one process.
- `goal_manager.lua` (617 lines) provides goal management.
- `decision_engine.lua` (820 lines) provides 6-dimension action scoring and selection.
- **BUT:** No clear separation between governance (executive) and execution (workers).
- `brain.lua` command dispatch loop handles goals, commands, and heartbeat in a single path.
- `seedreasond` is proposed as the executive in some docs but is currently only a policy evaluator.

**Key evidence:**
- `lua/agents/cognitive/brain.lua:203-248`: Single dispatch loop handles all responsibilities.
- `src/seedreasond/src/main.c`: Policy evaluation — `if/and/or/not/eq/match` forms. No executive function.
- `src/seedcogd/main.c:2457-2608`: Phase J (Goal Management) runs inside cognitive_tick() — executive and worker are the same process.
- `docs/cognition/COGNITIVE_ARCHITECTURE_SPEC.md:626`: `seedreasond` described as "policy evaluation engine" — not executive.

**Severity: Medium-low.** The components of executive function (goal management, decision engine, policy evaluation) exist. What's missing is the architectural boundary between governance and execution. This is primarily a refactoring effort.

---

### Gap 3.13: Cognitive Homeostasis (proposal lines 1037-1051)

**Proposal summary:**
"Regulate its own cognitive state — avoiding oscillation between competing goals, preventing runaway recursive reflection, delaying non-urgent learning when resources are constrained, balancing exploration against exploitation, monitoring confidence calibration, maintaining sufficient free context and working memory, scheduling rest periods for consolidation."

**Current state:**
- **Not implemented.** No cognitive state regulation exists.
- The cycle runs continuously: `while(max_cycles==0||cycle<max_cycles){cognitive_tick();sleep(gap_seconds);}`.
- Phase A runs 3 parallel LLM calls every cycle with no limit on repetition.
- Learning can trigger auto-deployment every cycle with no resource check.
- No oscillation detection.
- No exploration/exploitation balancing.
- Rest periods do not exist (consolidation runs inside the active cycle).

**Key evidence:**
- `src/seedcogd/main.c:2933-3212`: `while(1)` around cognitive_tick with `sleep(gap_seconds)` — runs forever.
- `src/seedcogd/main.c:1736-1843`: Phase A runs 3 parallel LLM calls every cycle unconditionally.
- `src/seedcogd/main.c:1990-2115`: Learning phase runs every cycle — auto-deployment at line 2093 fires if confidence > 0.98, no resource or repetition check.
- `src/seedcogd/main.c:1640`: Cycle header line — no cycle limit or regulation logic.
- No exploration/exploitation mode flag exists.
- No cycle repetition detection (same discovery appearing N times triggers no mechanism).

**Severity: CRITICAL.** Without homeostasis, the system has no defense against the observed pattern of "excessive repetition" — it has no mechanism to recognize that it is in a cognitive loop and break out of it. This is the second most impactful gap after belief revision because without it, belief revision alone would still not prevent runaway reflection on the same topics.

**Implementation path:** (a) Track discovery diversity — if the same topic generates similar conclusions N times, trigger a "diversion" (schedule a different workflow or skip reflection on that topic). (b) Add exploration/exploitation mode switching. (c) Move consolidation off the main cycle to a background process (consolidation-as-rest). (d) Add resource budgets per phase that cap LLM calls per cycle.

---

### Gap 3.14: Scientific Method (proposal lines 997-1033)

**Proposal summary:**
"Reflection becomes formal: Observation -> Hypothesis -> Prediction -> Experiment -> Evaluation -> Knowledge Update. The engine literally performs science on itself."

**Current state:**
- The cognitive cycle approximates this progression: observation (ingest via Phase A/API), reflection (Phase A), prediction (Phase D), evaluation (contradiction check in Phase B).
- **BUT:** No formal "experiment" step. The system does not design experiments to test hypotheses, execute them, and update knowledge from results.
- Code generation pipeline (`src/seedcogd/main.c:1339-1422`) is engineering-focused (compile and run), not scientific (test a hypothesis).

**Key evidence:**
- `src/seedcogd/main.c:1339-1422`: `code_gen_pipeline()` generates C code, sandbox-compiles it, checks exit code — tests compilation, not a cognitive hypothesis.
- No experiment design: "if hypothesis H is true, then observation O should have value V."
- No formal comparison of predicted vs actual outcomes beyond type matching (line 1483: `if (strcmp(pred_type, obs_type) == 0)`).
- No knowledge update from experimental results.

**Severity: Low-medium for now.** The scientific method depends on belief revision (Gap 3.6) to be useful. Without belief revision, experiments produce results but the system cannot learn from them. This should follow belief revision implementation.

---

## 4. Contradictions Between Specs and Current Codebase

### Contradiction 1: Primitive Operator Count

**Spec says:** 25-40 primitive operators verified by the irreducibility test.
**Codebase has:** 22 SST operator enums + 14 SXP functions = 36 operators total, none verified by the irreducibility test.

Several SST operators (`SST_OP_REFLECT`, `SST_OP_LEARN`, `SST_OP_PLAN`) are structurally composite — they should decompose into smaller primitives. The spec's claim that 25-40 operators can be "irreducible" conflicts with the current codebase where operators at different abstraction levels are stored as flat enums.

**Resolution needed:** Either (a) demote ~15 operators from "primitive" to "composite" by rewriting them as SXL compositions, or (b) accept that SST operators are a higher-level abstraction than SXP operators and document a two-tier (not four-tier) ISA for now.

---

### Contradiction 2: DataChain vs Journal Purpose

**Spec says:** DataChain is a cognitive timeline linking every thought.
**Codebase (`docs/network/DATACHAIN.md:5`):** "The datachain is not a blockchain. It is not a consensus mechanism. It is a Merkle-linked local log used for accountability and forensics."

The datachain's documented purpose (infrastructure accountability) contradicts the spec's vision (cognitive timeline). Block types are `trust.granted`, `cap.issued`, `channel.opened` — not observations, reflections, or plans. The cognitive journal is flat JSONL with no hash links.

**Resolution needed:** Keep them separate. The datachain serves its documented accountability purpose. A cognitive timeline can be built as a cross-reference layer that links journal entries into causal chains without changing either storage format.

---

### Contradiction 3: DFS Scope

**Spec says:** DFS is the "Distributed Symbolic Cortex" with role specialization and distributed symbolic memory.
**Codebase (`docs/network/DFS.md:2-6`):** "Not a POSIX filesystem," "not general-purpose distributed filesystem," "strong consistency not a goal." Explicitly scoped to "sharing content-addressed artifacts (datasets, model files, large attachments)."

The DFS's documented non-goals directly contradict what the Distributed Symbolic Cortex would require. A distributed cognitive memory needs consistency guarantees and semantic routing that DFS explicitly rejects.

**Resolution needed:** Build the Distributed Symbolic Cortex as a separate layer on top of libsmem replication (which already supports vector clocks, capability tokens, and entry signing), not on top of DFS. Node specialization can use capability advertisement with filtering (route planning tasks only to planning-capable nodes).

---

### Contradiction 4: Blackboard vs Separation of Concerns

**Spec says:** Shared symbolic state visible to all processes.
**Codebase designed for:** Separated concerns — `libsmem` owns memory, `seedreasond` owns policy, `seedcogd` owns cognition, the bus provides message-passing.

A blackboard centralizes what was intentionally distributed. Every daemon reading/writing to a shared state space violates the principle of least privilege and creates coupling between independently evolvable modules.

**Resolution needed:** Adopt a "shared partitions" model. Cognitive processes already share libsmem partitions. Add a well-known `cognitive/this-node/blackboard` partition with a defined fact schema. This achieves the blackboard goal without making the bus into a stateful store and without giving seedsysresd access to cognitive internals.

---

### Contradiction 5: Executive Function Daemon

**Spec says:** The Executive "never performs inference. It governs cognition." Describes a separate governance daemon.
**Codebase (`docs/cognition/COGNITIVE_ARCHITECTURE_SPEC.md:626`):** `seedreasond` is documented as "policy evaluation engine" — not executive. `seedcogd` performs both executive control and inference.

Splitting executive function from inference would require either: (a) migrating executive logic from seedcogd to seedreasond (expanding seedreasond's scope), or (b) creating a new `seedexecd` daemon — both contradicting the spec's (and codebase's) "not more daemons" principle.

**Resolution needed:** Keep executive logic in seedcogd but extract governance operations (workflow selection, goal prioritization, resource allocation) into a distinct module (`executive.c`) within seedcogd. This achieves the separation without creating a new daemon.

---

### Contradiction 6: Homeostasis vs Continuous Operation

**Spec says:** System should regulate cognitive state, including rest periods for consolidation.
**Codebase (`src/seedcogd/main.c:2933-3212`):** `while(1) { cognitive_tick(); sleep(gap_seconds); }` — continuous operation.

Homeostasis requires the system to sometimes rest, pause, or reduce activity. The current design has no mechanism for this. Adding proper rest periods (minutes/hours of reduced cognitive activity) would fundamentally change the system's operational profile and could affect use cases that depend on continuous responsiveness.

**Resolution needed:** Add a "throttle" phase at the start of `cognitive_tick()` that can skip phases or extend `sleep(gap_seconds)` based on cognitive load metrics. Run consolidation as a background thread with separate scheduling. This preserves continuous responsiveness while adding regulation.

---

## 5. Priority Recommendations

### P1: Belief Revision Engine (Critical)

**Why:** Directly addresses the spec's #1 critique. Without it, every discovery is treated as new. The system cannot learn that it has solved a problem. Confidence monotonically decreases — nothing ever becomes *more* certain.

**What to build:**
1. Add evidence chain field to entry struct (parent entries, confirming/disconfirming observations)
2. Implement update semantics in the memory store (confidence increase on confirming evidence, decrease on disconfirming evidence)
3. Wire contradiction detection (Phase B) into belief revision (contradicting entries reduce confidence)
4. Add "novelty check" before Phase A: skip reflection on topics with high-confidence settled beliefs
5. Wire `sxp_confidence_propagate()` from libsexpr into the belief update pipeline

**Dependencies:** None. The confidence propagation library already exists. The change is wiring it into the storage layer and cognitive cycle.

**Effort:** 2-3 weeks for a complete implementation (1 week for evidence chain + update semantics, 1 week for belief store, 1 week for cycle integration).

---

### P2: Cognitive Homeostasis (Critical)

**Why:** Without regulation, the system cannot prevent repetitive loops, runaway reflection, or resource exhaustion. This is the second-most impactful gap.

**What to build:**
1. Track discovery diversity (topic signatures per cycle)
2. Mode switching: exploration (10 cycles: diverse discovery) vs exploitation (10 cycles: deepen existing threads)
3. Consolidation-as-rest: move Phase C off the main cycle to a background thread
4. Phase budgets: cap LLM calls per cycle per phase
5. Oscillation detection: if same topic appears N times, raise oscillator flag and escalate

**Dependencies:** Self-model (P4) for feeding metrics into regulation decisions.

**Effort:** 2-3 weeks (1 week for tracking and modes, 1 week for budgets and oscillation, 1 week for consolidation migration).

---

### P3: Cognitive Workflows as SXL Objects (High)

**Why:** The spec's highest-priority recommendation. Transforms the cognitive cycle from a fixed algorithm into an adaptive process.

**What to build:**
1. Define `(workflow ...)` SXL object type with phases, conditions, transitions, resource requirements
2. Extract each of the 12 phases into an SXL workflow definition
3. Build a workflow executor in Lua (reads SXL workflow definitions, dispatches phases)
4. Add workflow selector (problem type -> workflow mapping)
5. Parallel track: keep the current hard-coded cycle as fallback

**Dependencies:** None initially (workflow definitions can coexist with the current cycle). Workflow selection benefits from self-model (P4) and belief revision (P1).

**Effort:** 3-4 weeks (1 week for SXL workflow schema, 2 weeks for executor, 1 week for migration).

---

### P4: Self-Model Expansion (High)

**Why:** The self-model is the foundation for meta-cognition, belief revision, and homeostasis. All regulatory loops need a self-model to observe.

**What to build:**
1. Create `cognitive/this-node/self-model` libsmem partition
2. Each cycle, populate: cognitive load (LLM calls pending/completed), memory pressure (index fullness, entry count, relation count), planning quality (recent plan execution rate), prediction error (existing EMA), attention saturation (recent attention scores), learning rate (new knowledge per cycle), error history (drops, failures)
3. Seed Phase K (meta-cognition) from the self-model partition
4. Add self-model queries to the world model's `explain()` for human introspection

**Dependencies:** None. All metrics are already tracked as globals.

**Effort:** 1-2 weeks (1 week for partition and population, 1 week for integration).

---

### P5: 4-Layer SXL ISA Discipline (Medium)

**Why:** Without the ISA discipline, SXL operators will continue to proliferate without a composition system. The "cognitive compiler" cannot exist without it.

**What to build:**
1. Audit all 36 operators (22 SST + 14 SXP) against the primitive operator test
2. Identify the irreducible core (~25 operators)
3. Rewrite composite operators as SXL procedures (not C/Lua functions)
4. Build a macro-expansion system that decomposes composites into primitives
5. Add operator metadata (preconditions, postconditions, resource costs)
6. Document the four-layer hierarchy

**Dependencies:** Workflow infrastructure (P3) provides the execution model for composite operators.

**Effort:** 4-6 weeks (2 weeks for audit and core identification, 2 weeks for composite rewrite, 2 weeks for expansion system).

---

### P6: MCL with Dynamic Benchmarking (Medium)

**Why:** The richest multi-backend infrastructure but with static profiles. Dynamic benchmarking makes inference routing adaptive.

**What to build:**
1. Expand model profiles with measured latency, tokens-per-second, quality scores
2. Add periodic benchmarking tasks (every 100 cycles: run sample prompts, measure results)
3. Implement cost-aware dispatch with budgets (task declares max cost, scheduler selects cheapest capable model)
4. Add queue depth and load tracking per backend
5. Symbolic model profiles as SXL expressions `(model :id ...)`

**Dependencies:** Self-model (P4) for storing benchmark results.

**Effort:** 2-3 weeks (1 week for benchmarking infrastructure, 1 week for cost-aware dispatch, 1 week for SXL profiles).

---

### P7: Cognitive Blackboard (Medium)

**Why:** Decouples all cognitive processes. Makes the system extensible without modifying the core cycle. Enables the distributed cognition model.

**What to build:**
1. Define shared fact schema `(:type fact :domain <str> :confidence <float> :source <str> :content <sxl> :timestamp <ts>)`
2. Implement blackboard as a well-known libsmem partition with pub/sub
3. Migrate each phase to publish outputs as facts and query needed facts as inputs
4. Phase H (attention) becomes the fact ranking and filtering mechanism
5. Add fact listeners for cross-domain pattern detection

**Dependencies:** Workflow infrastructure (P3) for fact-driven dispatch. Self-model (P4) for blackboard health monitoring.

**Effort:** 3-4 weeks (1 week for fact schema and partition, 2 weeks for phase migration, 1 week for attention integration).

---

## 6. Summary Assessment Table

| Domain | Score | Evidence |
|--------|-------|----------|
| **Model Cognition Layer** | 5/10 | 5 backends, pool, health tracking, task classification exist. No dynamic benchmarking, cost awareness, or symbolic profiles. |
| **Blackboard** | 1/10 | No shared fact workspace. Bus provides pub/sub but not shared state. |
| **Attention** | 6/10 | 6-dimension scoring implemented (C + Lua). Telemetry-only — scores never gate resources. |
| **Prediction** | 5/10 | Prediction mechanism exists for next cycle. Limited scope (type-level only). No multi-subsystem predictions. |
| **Multi-Layer Memory** | 4/10 | Working memory, long-term, consolidation exist. No explicit 7-layer hierarchy or promotion pipeline. |
| **Belief Revision** | 0/10 | No mechanism updates beliefs with new evidence. Confidence decays only. |
| **Simulation** | 3/10 | Scenario runner exists but not wired into cognitive cycle. |
| **Meta-Cognition** | 6/10 | Calibration, gap detection, strategy evaluation exist (C + Lua). No per-model analysis, no closure loop. |
| **Cognitive Energy** | 2/10 | CPU/RAM monitoring. No GPU, network, cost tracking. No unified resource model. |
| **Dynamic Ontology** | 1/10 | Language evolution detects syntactic gaps. No ontological pattern discovery. |
| **Self Model** | 3/10 | Static startup snapshot. Runtime metrics tracked as globals but not unified. |
| **Executive Function** | 4/10 | Goal management, decision engine, policy evaluation exist. No governance/execution separation. |
| **Homeostasis** | 0/10 | No regulation. Cycle runs continuously. No oscillation/runaway detection. |
| **Scientific Method** | 2/10 | Approximates observe-reflect-predict-evaluate but no formal experiment design. |
| **Four-Layer ISA** | 2/10 | 36 operators exist without layering or irreducibility test. No composition system. |
| **Cognitive Workflows** | 0/10 | 12-phase cycle is a fixed algorithm. No workflow definitions, executor, or selector. |
| **Workflow Synthesis** | 0/10 | Requires ISA + workflows. Not feasible yet. |
| **DataChain Timeline** | 2/10 | Infrastructure datachain exists. Cognitive journal is flat JSONL with no hash links. |
| **Distributed Cortex** | 3/10 | D1-D5 stack functional. Delegation, not role specialization. DFS is a blob store. |

---

## 7. Key Source File Index

All paths are relative to `/home/user/seed-dev/` (the main S.E.E.D. codebase).

| File | Key Lines | Contains |
|------|-----------|----------|
| `src/seedcogd/main.c` | 1605-2931 | 12-phase cognitive_tick() |
| `src/seedcogd/main.c` | 1155-1158 | Journal write format (flat JSONL) |
| `src/seedcogd/main.c` | 1311-1319 | Static self-model ingestion |
| `src/seedcogd/main.c` | 2247-2343 | Attention gate (telemetry-only) |
| `src/seedcogd/main.c` | 2621-2780 | Meta-cognition phase |
| `src/seedcogd/main.c` | 185-198 | entry_t struct, index_add, confidence init |
| `src/seedcogd/main.c` | 448-454 | memory_decayed_confidence (monotonic decay) |
| `src/seedcogd/main.c` | 1458-1601 | Prediction check + predict_next_state |
| `src/seedcogd/main.c` | 1339-1422 | Code generation pipeline |
| `src/seedcogd/delegate.h` | 175 | Delegation protocol |
| `src/seedcogd/capability.h` | 206 | Capability advertisement |
| `src/seedcogd/kg_sync.h` | 175 | KG bloom filter sync |
| `src/seed-transformer/include/sst.h` | 86-109 | 22 SST operators |
| `src/libsexpr/src/confidence.c` | 1-118 | 6 confidence propagation rules |
| `src/libsexpr/include/seed/sexpr.h` | 60-120 | SXP ABI — parse/validate/query/transform |
| `src/libseedllm/include/seed/llm.h` | 87-96 | Model info struct (8 fields, 7-bit cap mask) |
| `src/libsmem/include/seed/smem.h` | 60-200 | Partition model, log API |
| `src/libdfs/include/seed/dfs.h` | 30-100 | Content-addressed store API |
| `lua/helpers/metacognition.lua` | 544 | Confidence calibration, gap detection |
| `lua/helpers/decision_engine.lua` | 820 | 6-dimension action scoring |
| `lua/helpers/consolidation.lua` | 1005 | Memory consolidation |
| `lua/helpers/working_memory.lua` | 424 | Eviction policies |
| `lua/helpers/attention.lua` | 437 | Attention budget allocation |
| `lua/helpers/prediction.lua` | 190 | Next-cycle prediction |
| `lua/helpers/simulation.lua` | 231 | Scenario simulation |
| `lua/helpers/goal_manager.lua` | 617 | Goal management |
| `lua/agents/cognitive/brain.lua` | 200-250 | Command dispatch loop |
| `docs/cognition/COGNITIVE_ARCHITECTURE_SPEC.md` | — | Canonical architecture spec (v1.3) |
| `docs/cognition/SXL_LANGUAGE_SPECIFICATION.md` | — | SXL language spec |
| `docs/network/DATACHAIN.md` | — | Datachain scope (accountability) |
| `docs/network/DFS.md` | — | DFS scope (blob store) |

---

*End of GAP-ANALYSIS.md*
