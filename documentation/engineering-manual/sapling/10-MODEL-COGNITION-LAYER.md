# 10 — Model Cognition Layer

> The dispatcher between the S.E.E.D. cognitive engine
> and the five inference backends. The MCL (Model
> Cognition Layer) turns "I need a model to do X" into
> a concrete routing decision across native, ollama,
> openai, sst, and sidecar pools, with capability
> matching, health monitoring, cost-aware selection,
> and fallback.

This chapter sits between the cognitive engine
([`08-COGNITIVE-WORKFLOWS.md`](08-COGNITIVE-WORKFLOWS.md))
and the symbolic layer
([`02-SYMBOLIC-LAYER.md`](02-SYMBOLIC-LAYER.md)). It
answers the question the engine itself never has to
answer: which model, on which backend, at which
quality/latency/cost trade-off, executes this
cognitive task? The canonical sources are
`~/home/user/seed-dev/docs/DRAFTS/seed-models-specs.txt`
(744 lines) and the MCL section of
`~/solbian/seed/DRAFTS-INDEX.md` lines 706-789. The
policy frame is `~/solbian/codex/machina/POLICIES.md`.
## 1. The "models are not the mind" principle

Per `seed/DRAFTS-INDEX.md:749`, the overarching
principle is:

> "Models are not the mind; they are adaptive
> cognitive accelerators. S.E.E.D.'s intelligence
> resides in its symbolic memory, world model, self
> model, planning, and reflection. The Model
> Cognition Layer is responsible for selecting,
> composing, and orchestrating the most appropriate
> accelerators…"

Three claims follow. **The cognitive engine is the
mind.** The symbolic engine (NSL workflows, SST,
libsmem, libsexpr, the 20 cognitive domains) owns
long-term memory, the self model, the world model,
planning, and reflection. **The world model is the
long-term memory.** Every cognitive fact is an SXL
entity in a libsmem partition. **The models are
fast-but-imprecise accelerators.** LLMs, vision
models, audio models, code models, and embedding
models are interchangeable symbolic translators:
input in one modality, SXL out. They are accelerators
in the same sense a GPU kernel is an accelerator —
fast, sometimes flaky, untrusted by the substrate
that calls them.

Three operational consequences. First, the engine
never manipulates raw text, raw pixels, or raw audio;
it manipulates SXL (`seed-models-specs.txt:108-119`).
Second, models are swappable: a better vision model
plugs in as a perception module without changing the
cognitive core (`seed-models-specs.txt:741-743`).
Third, model failure is recoverable: when a model
returns malformed SXL, hallucinates, or times out,
the MCL falls back, the symbolic validator rejects,
and the engine continues with degraded perception
but full cognition.

## 2. The Model Cognition Layer

The MCL sits between the cognitive engine and the
five inference backends
(`seed/DRAFTS-INDEX.md:717-718`). It is a collection
of components that own model selection, scheduling,
and health — not a single binary.

### 2.1 Position in the stack

```
   Cognitive engine (NSL workflows, SST, 12-phase
   C cycle, Lua brain)
            |
            v
   +-----------------------+
   |  Cognitive Task       |   ← planner that
   |  Planner              |     decomposes an
   +-----------------------+     intent into
            |                   sub-tasks
            v
   +-----------------------+
   |  Model Cognition      |   ← the MCL
   |  Layer (this chapter) |
   +-----------------------+
            |
   +----+----+----+----+----+
   v    v    v    v    v    v
 native ollama openai sst sidecar
```

The Cognitive Task Planner is the *consumer* of the
MCL. It produces a decomposition — "this intent
requires a 7B language model with tool support at
medium latency" — and hands the sub-task to the MCL.
The MCL turns that into a routing decision: "route
to `qwen3-8b` on `ollama-local` because slot 2 is
HEALTHY and the capability profile matches."

### 2.2 The five backends

The MCL fronts the five-backend model pool owned by
`libseedllm` and described in
`seed/ARCHITECTURE.md:147-189`: **native** (C/C++
inference using llama.cpp directly, the deterministic
low-level substrate); **ollama** (the local model
server, the home-PC production backend); **openai**
(cloud-hosted models, for high-stakes synthesis and
fallback); **sst** (the Solbian Symbolic Transformer,
a peer of the router, not a model server in the LLM
sense); and **sidecar** (Unix Domain Socket interface
to a local model server). The pool is sized at
`POOL_MAX_BACKENDS=8` slots
(`seed/ARCHITECTURE.md:163`); each slot has its own
health, queue depth, and latency state.

### 2.3 Responsibilities

**Model discovery and registration.** When a backend
comes online, it advertises its available models.
Each is registered as a `(model ...)` capability
profile (§3). The registry is a living part of the
self model: it knows how each model has performed
historically.

**Capability matching.** A task that requires vision,
tools, and reasoning narrows the candidate set to
models whose profiles advertise all three. Capability
matching is the first filter; cost, latency, and
quality are second-stage optimisations.

**Health monitoring.** Each slot has a state —
`HEALTHY`, `DEGRADED`, or `FAILED`
(`seed/ARCHITECTURE.md:160-161`). The MCL reads
`seed_llm_pool_stats()` from
`src/libseedllm/src/pool.c`. `FAILED` slots are
excluded; `DEGRADED` slots are demoted; `HEALTHY`
slots are preferred.

**Cost / latency / quality trade-off selection.**
The MCL selects the slot that best matches the
task's resource policy (§6). High accuracy biases
toward larger remote models; low cost biases toward
local small models; low latency biases toward slots
with the lowest observed EWMA.

**Fallback routing.** When the selected slot fails,
the MCL walks the candidate set in priority order
and routes to the next best slot. Fallback is
automatic and logged.

**Cross-backend composition.** A scene-understanding
request may require a vision model for object
detection, a language model for scene-graph
synthesis, and a code model for query construction.
The MCL sequences these across backends, passing
SXL through the channel system
(`sapling/NSLP/ARCHITECTURE.md:444-456`).
### 2.4 The MCL is part of the self model

Per `seed/DRAFTS-INDEX.md:746-748`, the MCL "becomes
part of S.E.E.D.'s self-model, tracking dynamic
state, not just static capabilities." The system
should know not just *which* model is best for
abstract task X, but *which model is best right now*,
on this node, with this load, with this latency. The
MCL's state — registry size, fallback rate, average
latency, current health distribution — is published
to the self-model partitions and queried by the
meta-cognition phase (Phase K in
`seed/ARCHITECTURE.md:107-108`).

## 3. The model capability profile

Per `seed-models-specs.txt:723-728`, every model in
the registry is described by a symbolic capability
profile in SXL:

```sxl
(model
  :id "qwen3-8b"
  :backend "ollama"
  :modality "language"
  :parameters "8B"
  :context 32768
  :quantization "Q4_K_M"
  :supports_tools true
  :supports_reasoning true
  :vision false
  :embedding false
  :cost 0
  :latency 1.2)
```

Each field is a symbolic claim about a specific
model. The MCL uses the profile to match tasks to
models and to negotiate trade-offs.

### 3.1 Field reference

**`:id`** (string) — the model's stable identifier
(`"qwen3-8b"`, `"gpt-4o"`, `"nomic-embed-text"`).
**`:backend`** (string) — one of `native`, `ollama`,
`openai`, `sst`, `sidecar`. A single model may be
served by multiple backends; each hosts its own
profile. **`:modality`** (string) — `language`,
`vision`, `audio`, `code`, `embedding`, `multimodal`.
The *first* filter: a vision task is never routed to
a language-only model. **`:parameters`** (string) —
human-readable parameter count (`"8B"`, `"70B"`,
`"unknown"`). **`:context`** (integer) — maximum
context window in tokens. Per
`seed-models-specs.txt:729-732`, context is a
*first-class resource*: prompt sizing becomes a
scheduling decision. The MCL reserves context for
output, subtracts prompt overhead, and refuses to
schedule a task whose required context exceeds the
model's usable window. **`:quantization`** (string) —
`Q4_K_M`, `Q5_K_M`, `Q8_0`, `F16`, etc. Affects
latency, memory, and quality. The MCL records
quality deltas against an FP16 reference in the
benchmark log. **`:supports_tools`** (boolean) —
whether the model emits tool/function calls in the
SXL-shaped tool-calling format. **`:supports_reasoning`**
(boolean) — whether the model exposes a
chain-of-thought or extended-thinking mode. Tasks
with `:strategy "deep"`, `:depth 3` and above require
this. **`:vision`** (boolean) — whether the model
accepts image inputs. Independent of `modality`: a
multimodal model has `modality "multimodal"` and
`vision true`. **`:embedding`** (boolean) — whether
the model produces dense vector embeddings for the
vector index. Embedding models route through a
separate path because their output is not SXL; it
is a `vec.idx` entry. **`:cost`** (number) — per-token
cost in a normalised internal unit (conversion to
USD is a policy-layer concern). Cost is `0` for
local models served on-device. **`:latency`**
(number) — expected latency to first token in
seconds, under nominal load. The MCL updates this
with an EWMA from observed runs.

### 3.2 Complete example profile

The full shape from `seed-models-specs.txt:723-728`
includes three extra fields the MCL tracks for
scheduling but does not require for capability
matching: `:tokens_per_second`,
`:memory_required`, and `:availability`.

```sxl
(model :id "qwen3-8b" :backend "ollama" :modality "language"
 :parameters "8B" :context 32768 :quantization "Q4_K_M"
 :supports_tools true :supports_reasoning true
 :vision false :embedding false
 :latency 1.2 :tokens_per_second 58
 :memory_required "7.8GB" :cost 0 :availability "local")
```

### 3.3 Registration, update, query

A model is registered when its backend reports it.
The flow: backend advertises (`/available-models`),
MCL parses the list, MCL synthesises a profile
(some fields backend-reported, some probed, some
benchmarked), MCL stores the profile in
`cognitive/this-node/model-registry` as an SXL
entity of type `(:type model ...)`.

The profile is updated on three triggers:
backend-side change (model added or removed);
periodic health probe (the MCL pings each slot and
refreshes the latency and health fields); and
benchmark run (a new `model-benchmark` workflow
completes and updates `:tokens_per_second` and the
quality-delta log).

Profiles are queried by the dispatcher in
`src/libseedllm/src/dispatch.c:47-71`. The
dispatcher is capability-based: it filters profiles
by `:modality`, `:supports_tools`,
`:supports_reasoning`, and `:vision`, sorts by the
resource policy, then selects the top candidate.

## 4. The hierarchical cognition diagram

Per `seed-models-specs.txt:426-480` and
`seed/DRAFTS-INDEX.md:743-745`, cognition is
organised into three tiers. The tiers are not fixed
to specific models; they are roles the MCL assigns
based on the cognitive task.

```
   ┌──────────────────────────────┐
   │       Executive cognition    │  ← large cloud planners
   │ (planning, long-horizon)     │
   └──────────────┬───────────────┘
                  ▼
   ┌──────────────────────────────┐
   │      Operational cognition   │  ← local reasoning models
   │ (workflow sequencing)        │  (MCL's primary dispatch tier)
   └──────────────┬───────────────┘
                  ▼
   ┌──────────────────────────────┐
   │      Perceptual cognition    │  ← vision, audio, OCR, sensors
   │ (sensory input)              │
   └──────────────────────────────┘
```

**Executive tier** — high-level decisions: mission
planning, goal-decomposition, multi-step
reflection. The natural home of large-context models
(cloud or local 70B+). Executive tasks have long
contexts, accept higher latency, and are infrequent.

**Operational tier** — workflow sequencing:
dispatching an NSL workflow, applying an operator,
executing a single primitive. The *primary* tier the
MCL dispatches to. Local small and medium models
(7B-14B, quantised) live here, because operational
tasks dominate the cycle volume and benefit from low
latency. The MCL's capability matching and
trade-off-selection both target this tier.

**Perceptual tier** — sensory input: vision models
that extract scene graphs, audio models that
transcribe, OCR models that read dashboards. Always
modality-specific; the MCL routes perceptual tasks
to the matching modality profile.

The three tiers communicate through SXL. The
perceptual tier returns Vision-SXL or Audio-SXL to
the operational tier; the operational tier returns
NSL-composed results to the executive tier. No tier
ever passes raw pixels, raw audio, or raw text to
the next.

### 4.1 Multi-level orchestration

The diagram is logical; the physical view, per
`seed/DRAFTS-INDEX.md:733-735`, is multi-level:
"Cloud planner creates decomposition; local Qwen /
Gemma / Vision / Code model execute specialised
subtasks." A single cognitive task may fan out
across multiple backends — cloud planner
decomposes, local language model summarises, local
vision model extracts, local code model composes,
results return to the planner for synthesis. The MCL
owns the fan-out.

## 5. The 16 cognitive capabilities

Per `seed/DRAFTS-INDEX.md:755-788`, the architect
identified 16 cognitive capabilities the system
should build into S.E.E.D. The list is the catalogue
of cognitive *competences* the cycle draws on. Each
capability is supported by one or more model
backends and serves one or more of the 20 cognitive
domains (per `seed/COGNITIVE-DOMAINS.md`).

**1. Cognitive Blackboard.** A shared symbolic
workspace where models and the engine deposit
intermediate results — the substrate the channel
system writes to
(`sapling/NSLP/ARCHITECTURE.md:444-456`).
**2. True Attention Manager.** A multi-factor
attention allocator scoring pending items by
importance, novelty, urgency, goal relevance,
prediction error, user attention, and resource
cost.
**3. Prediction everywhere.** Memory / vision /
system / planner predictions; prediction errors
become learning signals.
**4. Multi-layer memory.** Sensory Buffer → Working
→ Episode → Concept → Principle → Ontology →
Identity, documented in
[`09-MEMORY-HIERARCHY.md`](09-MEMORY-HIERARCHY.md).
**5. Belief revision engine.** Stores beliefs with
confidence and source; new evidence updates through
the confidence propagation rules in
`src/libsexpr/src/confidence.c`.
**6. Internal simulation engine.** The "Current World
→ Apply Action → Future World → Evaluate → Choose"
loop. Backends: hybrid (neural for world-model
approximation, symbolic for validation).
**7. Meta-cognition.** Continuous self-improvement:
monitoring reasoning quality, flagging drift,
suggesting workflow changes.
**8. Cognitive energy.** Tracking CPU / RAM / GPU /
latency / cost / battery / network / context /
attention.
**9. Dynamic ontology.** Observe → Find patterns →
Suggest concepts → Reflect → Accept → Update
ontology.
**10. Native uncertainty.** Every symbol carries
uncertainty; reasoning over confidence distributions.
**11. World models as digital twins.** Kitchen /
chair / table / objects / relationships / dynamics /
history / affordances / predictions / goals.
**12. Self Model.** Cognitive load, memory pressure,
planning quality, reflection quality, vision
confidence, reasoning confidence, attention
saturation, learning rate, error history, agent
trust, backend health, model performance.
**13. Experience.** Goal / Actions / Observations /
Mistakes / Lessons / Generalisations — not logs.
**14. Executive Function.** Separate thinking from
execution: mission → planner → scheduler → workers
→ reflection.
**15. Scientific Method.** Observation → Hypothesis
→ Prediction → Experiment → Evaluation → Knowledge
Update.
**16. Cognitive Homeostasis.** Avoid oscillation,
prevent runaway recursive reflection, balance
exploration vs. exploitation, schedule rest periods
for consolidation / benchmarking / GC.

The 16 capabilities are not a fixed hierarchy. They
overlap, share backends, and co-evolve. The MCL's
job is to ensure that when a cognitive domain
requests one, the right backend is selected — and
that the capability registry itself is the part of
the self-model the system reflects on. The list is
exactly the 16-item enumeration in
`seed/DRAFTS-INDEX.md:755-788`; the architect is
authoritative on this.

## 6. Cost, latency, and dynamic benchmarking

Per `seed-models-specs.txt:736-738`, the resource
policy is itself an SXL expression:

```sxl
(resource-policy
  :latency high :cost low :accuracy high :energy medium)
```

The four axes — latency, cost, accuracy, energy —
are the dimensions along which model selection makes
trade-offs. The policy is configurable per cognitive
domain, per workflow, and per task. The default is
`:latency medium :cost low :accuracy high :energy
medium` — bias toward local, accurate, low-cost
selection, with latency tolerance for infrequent
high-stakes synthesis.

Per `seed/DRAFTS-INDEX.md:739-742`, the capability
registry is refreshed by dynamic benchmarks that
measure: `tokens_per_second` (sustained throughput
on a fixed prompt); `latency` (time to first token);
**reasoning benchmarks** (task-specific scores
against a held-out set); **symbolic correctness**
(does the model produce SXL that parses, validates,
and canonicalises without error?); **SXL adherence**
(does the model follow the SXL schema and keyword
conventions?); **hallucination frequency** (rate of
outputs that introduce entities not derivable from
the input); **context degradation** (quality decay
as the prompt approaches the context limit);
**memory usage** (peak RSS during inference); and
**energy consumption** (joules per thousand tokens,
where measurable). The benchmark runs as a cognitive
workflow on a low-priority trigger (`:trigger
:schedule :every 100 :cycles :priority :background`).
The results update the capability profile and feed
the self-model's record of model performance over
time.

## 7. Cross-references

The five-backend pool and per-intent routing table
are in `~/solbian/seed/ARCHITECTURE.md` §"Model-aware
routing" (lines 145-189); pool sizes, backend types,
and `HEALTHY / DEGRADED / FAILED` semantics are
defined there. The model-related entries in
`~/solbian/seed/CANONICAL-REFERENCE.md` (§10 SXL,
§11 SST, §12 Memory) anchor the symbolic layer the
MCL dispatches over; the capability profile SXL
reuses the entity patterns from §10.

The policy frame is
`~/solbian/codex/machina/POLICIES.md`. The
`llm_use.lisp` bundle and the SeedPolicy Root
together define the governance of model use: which
models may serve which cognitive domains, which
capabilities require countersignature, and how the
exception register applies to deliberate deviations
from the routing defaults. The MCL is not a policy
actor; it is a routing layer. Policy lives one level
up, in `seedreasond` and the Codex Machina lisp
rules.

The NSL/NSP control plane, which compiles NSL
expressions into primitive graphs and dispatches
them to backends, is in
`sapling/NSLP/ARCHITECTURE.md` §3.4 and §4.1. The
NSP dispatcher uses the same capability-based
routing as `src/libseedllm/src/dispatch.c:47-71`
but at primitive granularity rather than intent
granularity. The MCL and the NSP dispatcher are
sibling components of the model-aware routing
substrate; they share the capability registry and
the backend pool, but the MCL handles intent-level
routing and the NSP dispatcher handles
primitive-level routing. The C substrate that hosts
the model pool is in `~/solbian/seed/ARCHITECTURE.md`
(L1, L2, L4 layers). The cognitive cycle phases A-L
are the schedule the model pool serves; the health
of the pool feeds back into the self-model's
monitoring of LLM latency EWMA
(`seed/ARCHITECTURE.md:117-121`).

The 20 cognitive domains — perception, attention,
working memory, long-term memory, reflection,
reasoning, goal management, planning, executive
control, learning, self model, world model,
prediction, decision making, meta-cognition,
cognitive monitoring, creativity, ethics,
communication, consolidation — are the *consumers*
of the MCL. Each domain declares its preferred
backends, its resource policy, and its fallback
chain. The MCL serves the union of these
declarations.

## 8. Summary

The Model Cognition Layer is the answer to "which
model does the engine talk to right now?" It is a
dispatcher, not a mind. It sits between the
cognitive engine and the five inference backends,
owning model discovery, capability matching, health
monitoring, cost-aware selection, fallback routing,
and cross-backend composition.

The "models are not the mind" principle keeps the
cognitive engine independent of any particular
foundation model. The capability profile SXL is the
registry that makes models swappable. The
three-tier hierarchical cognition is the role
assignment that makes multi-level orchestration
tractable. The 16 cognitive capabilities are the
catalogue of competences the cycle draws on.
Dynamic benchmarking keeps the registry honest.
The Codex Machina policies are the governance above
the routing.

The MCL is part of the self-model. The system
reflects on the registry the same way it reflects
on memory, planning, and the world model. When a
model degrades, the self-model notices. When a
fallback fires too often, the self-model asks why.
When a new backend comes online, the self-model
asks what it should be used for. That loop — engine
registers model, model serves engine, engine
reflects on model, reflection improves registration
— is the MCL's full lifecycle. It is the
operational form of "models are not the mind." The
mind is the loop. The models are the loop's
accelerators. The MCL is the loop's planner.

## See also

- [`06-NSL-ISA-AND-RESEARCH-CORPUS.md`](06-NSL-ISA-AND-RESEARCH-CORPUS.md) — the NSL/NSP control plane
- [`07-NSL-DEEP-DIVE.md`](07-NSL-DEEP-DIVE.md) — the 33-primitive ISA in detail
- [`08-COGNITIVE-WORKFLOWS.md`](08-COGNITIVE-WORKFLOWS.md) — how workflows replace the hard-coded phase cycle
- [`02-SYMBOLIC-LAYER.md`](02-SYMBOLIC-LAYER.md) — the SXL substrate the MCL dispatches over
- `~/solbian/seed/ARCHITECTURE.md` §"Model-aware routing" — the five-backend pool
- `~/solbian/seed/CANONICAL-REFERENCE.md` — the canonical model-related entries
- `~/solbian/codex/machina/POLICIES.md` — the Codex Machina policy frame
- `~/solbian/sapling/NSLP/ARCHITECTURE.md` §3.4 — the NSP backend dispatch
- `~/home/user/seed-dev/docs/DRAFTS/seed-models-specs.txt` — the canonical 744-line design discussion
- `~/solbian/seed/DRAFTS-INDEX.md` lines 706-789 — the MCL section summary
