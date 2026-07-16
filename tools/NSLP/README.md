# NSLP — Neuro-computational SEED Symbolic Language Processor

> **The cognitive ISA and its processor.** Full research, design,
> and specifications for the Neural Symbolic Language (NSL) —
> the minimal irreducible instruction set of cognition — and the
> Neural Symbolic Processor (NSP) — the compiler, optimizer, and
> executor for NSL expressions.
>
> Status: **Research & Design — Complete** (sapling prototype, v0.1.0)
> Created: 2026-07-16
> ACL role: `external` (prototype)

## What NSLP is

NSLP is the **neuro-computational core** of the S.E.E.D.
symbolic cognitive engine. It comprises two tightly-coupled
components:

**NSL (Neural Symbolic Language)** — the instruction set of
cognition. A set of ~33 irreducible symbolic primitives that
form the algebra of thought. NSL is the **control plane** of
cognition: it describes *what to do* at the most fundamental
level. Unlike SXL (the **data plane**, which describes
cognitive state), NSL is operational — its expressions execute.

**NSP (Neural Symbolic Processor)** — the compiler, optimizer,
and executor for NSL. It compiles NSL expressions into
primitive operator graphs, optimizes them (dead-code
elimination, parallelization, backend-aware fusion), and
dispatches them to available inference backends (LLMs, SST,
symbolic evaluator). NSP is to NSL what a CPU is to its ISA.

Together they form the 4-layer cognitive ISA:

```
Cognitive Workflows     (composed NSL procedures, inspectable SXL objects)
    ↓
SXL Composite Operators (high-level verbs expressed in NSL: reflect, plan, learn)
    ↓
NSL Primitives          (irreducible ISA: bind, match, branch, derive, ...)
    ↓
Inference Backends      (LLMs, SST, symbolic evaluation, native code)
```

## Why NSLP matters

The current S.E.E.D. cognitive engine (`seedcogd/main.c`, 3212
lines) executes a hard-coded 12-phase cycle. Every cycle runs
the same phases regardless of what the system needs. The 14 SXL
operators and 22 SST operators are implemented as C and Lua
functions — not as inspectable, composable symbolic procedures.

NSLP changes this. It provides:

1. **A well-defined cognitive ISA** — the minimal set of
   operations from which all cognition can be composed, each
   verified as truly irreducible.

2. **Composable cognition** — cognitive operations that the
   system can inspect, reason about, and recombine to form
   new workflows.

3. **Backend-agnostic execution** — NSL primitives don't assume
   LLM, symbolic, or any specific backend. The NSP routes each
   primitive to the best available backend dynamically.

4. **Self-modifying capability** — because NSL expressions are
   symbolic data, the system can generate, optimize, and evolve
   its own cognitive programs.

## Design principles

1. **Irreducible primitives.** Every NSL primitive passes the
   primitive test: it cannot be expressed as a composition of
   simpler NSL primitives.

2. **Minimal complete set.** The ~33 primitives are the smallest
   set sufficient to express all 14 SXL operators, all 22 SST
   operators, and all 12 cognitive cycle phases.

3. **Compositional.** Primitives compose through exactly five
   mechanisms: sequence, branch, iterate, parallel, call.
   There is no other way to combine operations.

4. **Symbolic, not neural.** NSL operates on S-expressions.
   Neural inference is a *backend*, not part of the language.

5. **Deterministic semantics.** Every primitive has formal
   operational semantics. Non-determinism (from LLM backends)
   is explicitly bounded and tracked via confidence.

## Project structure

```
tools/NSLP/
  README.md              — this file
  SPEC.md                — formal NSL ISA specification (33 primitives, semantics)
  ARCHITECTURE.md        — NSP compiler, optimizer, runtime design
  INTEGRATION.md         — how NSLP connects to S.E.E.D. (bus, libsmem, libseedllm, seedcogd)
  GAP-ANALYSIS.md        — gap analysis: cog3/misc specs vs current implementation
  ROADMAP.md             — phased implementation roadmap
  research/
    primitives.md        — derivation of the primitive set from mathematical foundations
    metabolism.md        — computational metabolism (basal cognitive processes)
    hippocampus.md       — hippocampal memory algorithms and structures
    foundations.md       — mathematical foundations (lambda calculus, π-calculus, category theory, etc.)
```

## Document index

| Document | Purpose | Status |
|----------|---------|--------|
| `README.md` | Project overview and design principles | **Complete** |
| `SPEC.md` | Formal NSL ISA: 33 primitives, type system, operational semantics | **Complete** |
| `ARCHITECTURE.md` | NSP compiler pipeline, runtime, backend dispatch | **Complete** |
| `INTEGRATION.md` | Bus/libsmem/libseedllm/seedcogd integration, graduation path | **Complete** |
| `GAP-ANALYSIS.md` | 19 gap areas, 6 contradictions, 7 priority recommendations | **Complete** |
| `ROADMAP.md` | 5-phase implementation plan with deliverables and dependencies | **Complete** |
| `research/primitives.md` | Derivation of 48 candidates from λ-calculus, SKI, π-calculus, ASM | **Complete** |
| `research/metabolism.md` | 6-phase basal cycle, attention budgets, AGM revision, sleep-wake cycles | **Complete** |
| `research/hippocampus.md` | Pattern separation/completion, Hopfield, SDM, 5-layer hierarchy | **Complete** |
| `research/foundations.md` | 7 pillars: Y combinator, CPS, abstract interpretation, TRS, category theory, info geometry, optimal transport | **Complete** |

## Relationship to SXL

| | SXL | NSL |
|---|---|---|
| **Nature** | Data IR | Control IR |
| **Layer** | Data plane | Control plane |
| **Describes** | Cognitive state (beliefs, goals, plans) | Cognitive operations (assert, query, derive) |
| **Example** | `(belief :id "b-1" :confidence 0.8 ...)` | `(seq (query ...) (derive modus-ponens ...) (assert ...))` |
| **Lifetime** | Persistent (stored in libsmem) | Ephemeral (executed, then gone) |
| **Composition** | Via entity relations and confidence propagation | Via control-flow primitives (seq, par, branch, iterate, call) |

## Relationship to the current codebase

NSLP is a **new layer** that sits between the existing SXL
infrastructure and the inference backends:

```
Current:   seedcogd (hard-coded C phases) → libseedllm (backend dispatch)
                                    ↘ libsexpr (SXL parse/validate/query)
                                    ↘ libsmem (symbolic memory)

Future:    seedcogd (NSL workflow executor) → NSP (compile + dispatch)
                    ↘ NSL procedures (symbolic, inspectable)
                    ↘ SXL operators (composed from NSL primitives)
                    ↘ libseedllm (backend for derive primitive)
                    ↘ libsexpr (SXL data manipulation)
                    ↘ libsmem (memory for query/assert/retract)
```

## See also

- `~/seed-dev/docs/DRAFTS/seed-cog3-specs.txt` — 4-layer ISA proposal, cognitive workflows, DataChain
- `~/seed-dev/docs/DRAFTS/seed-misc-specs.txt` — MCL, cognitive blackboard, homeostasis, self-model
- `~/seed-dev/docs/cognition/SXL_LANGUAGE_SPECIFICATION.md` — SXL language specification
- `~/seed-dev/docs/architecture/COGNITIVE_ENGINE_SPEC.md` — 20 cognitive domains
- `~/seed-dev/docs/architecture/MASTER_ARCHITECTURE.md` — anchor architecture
- `~/solbian/sapling/README.md` — sapling proving ground overview
- `~/solbian/sapling/INTEGRATION.md` — sapling integration model
