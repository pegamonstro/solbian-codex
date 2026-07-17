# 09 — Memory hierarchy and belief revision

> The seven-layer memory model, the belief
> revision engine that operates over it, the
> homeostatic regulation that keeps the engine
> stable, the hippocampal research substrate
> that grounds the design, and the
> 32-algorithm research corpus that maps onto
> it.

The canonical sources are
`~/seed-dev/docs/DRAFTS/seed-models-specs.txt`
(the symbolic-reasoning design notes on
long-term visual memory at lines 627-674, and
the symbolic scene graphs at lines 605-624);
`~/solbian/sapling/NSLP/research/hippocampus.md`
(hippocampal research substrate — pattern
separation, pattern completion, replay, and
the explicit five-layer hierarchy at lines
269-333, and the homeostatic regulation at
lines 234-333);
`~/solbian/sapling/NSLP/research/metabolism.md`
(six-phase metabolic cycle at lines 30-274);
and
`~/solbian/sapling/NSLP/deep-research/memory-reasoning.md`
(32-algorithm profile at lines 1-457).
This chapter is a curated synthesis; a
section that quotes a number or a code
reference cites it inline as `file:line`.

## 1. Why a memory hierarchy

A single flat memory store cannot serve a
cognitive system. S.E.E.D.'s `seedcogd`
already maintains three distinct memory
storage surfaces — the SST workspace
(`src/seed-transformer/include/sst.h:113-127`),
the `seedcogd` 80-entry ring buffer
(`src/seedcogd/main.c:57-103`), and the
libsmem memory partition model — but the
memory surfaces are not unified by an
explicit hierarchy. The seven-layer model
below subsumes the existing memory
surfaces, names each level, and binds each
level to a specific consolidation algorithm
that governs memory promotion and memory
eviction.

The seven layers are not a stand-alone
proposal. The five-layer form is what
`NSLP/research/hippocampus.md:269-281`
specifies explicitly; the seven-layer form
is a research extension that adds a
pre-sensory layer (the bus buffer where
unparsed observations queue) and an identity
layer (immutable self-model that the
cognitive cycle refuses to revise). The
mapping is in §5.

## 2. The seven-layer memory hierarchy

The hierarchy runs from the most volatile to
the most immutable. Each layer has a
**capacity**, a **retention**, a **retrieval
semantics**, a **decay function**, and a
**promotion criterion**. The substrate anchors
are: the bus broker for Layer 1, the `seedcogd`
80-entry ring buffer
(`src/seedcogd/main.c:57-103`) and the SST
workspace
(`src/seed-transformer/include/sst.h:113-127`)
for Layer 2, the libsmem partition model for
Layers 3-6, and the SXL `:creator` identity for
Layer 7.

| # | Layer | Substrate | Capacity | Retention | Retrieval | Decay | Promotion to next |
|---|-------|-----------|----------|-----------|-----------|-------|-------------------|
| 1 | Sensory Buffer | bus broker (`seedbusbrokerd`) | high-water mark | milliseconds | FIFO | overflow eviction | parse success |
| 2 | Working Memory | `seedcogd` ring + SST workspace | 5-9 active (Miller 7±2) | ~30 s | associative match | per-cycle `exp(-λ·t)` | temporal context + outgoing relation |
| 3 | Episode Memory | `cognitive/this-node/episode` | disk | minutes to hours | Modern Hopfield attention | utility-weighted (M4) | shared concepts or A→B causal pattern (≥80%) |
| 4 | Concept Memory | `cognitive/this-node/concept/*` | active cache | persistent | spreading activation | slow `exp(-μ·t)` | stable ≥N, referenced ≥M, confirmed ≥K |
| 5 | Principle Memory | `seed.sxl/v1` `:type principle` | hundreds–thousands | long-term | deductive + MLN | only via contradiction (severity > 0.3) | referenced by Layer 6 or self-model |
| 6 | Ontology Memory | `codex/solbian/`, `codex/machina/` | large, versioned | immutable per release | subsumption, DL, CG unification | none | self-defining, confidence ≥ 0.98 |
| 7 | Identity Memory | SXL `:creator` `did:seed:...` | very small | immutable | direct lookup | none | (sink) |

**Layer 1 — Sensory Buffer.** The bus
receives observations from Sprout on
`org.seed.observation.sensor.*`
(`seed/INTEGRATION.md:40-45`); the messages
queue in `seedbusbrokerd` before being
parsed into SXL. The buffer is the T0
control plane (`seed/INTEGRATION.md:96-98`);
sapling agents do not connect here.

**Layer 2 — Working Memory.** The
80-entry ring buffer in
`seedcogd/main.c:57-103` is the substrate.
Each slot decays per cycle; the buffer
evicts the lowest-confidence entry on
overflow. The attention gate in Phase H
promotes or demotes slots based on goal
relevance. The NSL primitives are `store`,
`recall`, and `forget`
(`NSLP/ARCHITECTURE.md:91-99`). Promotion
to Layer 3 follows `hippocampus.md:298-303`.

### 2.3 Layer 3 — Episode Memory

Episodes are SXL entities of type `experience`
or `episode` in
`cognitive/this-node/episode`. They carry a
`(:what, :where, :when)` Tulving triple
(`deep-research/memory-reasoning.md:38-49`)
plus optional `(:who, :why, :outcome)`
extensions. Retrieval uses Modern Hopfield
attention over encoded patterns
(`hippocampus.md:79-138`); the
Hopfield-Transformer equivalence (Ramsauer et
al. 2020) means the SST `SST_OP_RETRIEVE`
operator (`NSLP/ARCHITECTURE.md:209`) is the
natural executor. Decay is governed by the
metabolic M4 triage
(`metabolism.md:103-124`): KEEP / COMPRESS /
ARCHIVE / DELETE bins by
`triage_score = 0.3·recency + 0.3·utility +
0.2·confidence_decay + 0.2·goal_relevance`.
Promotion to Layer 4 follows
`hippocampus.md:306-313`. The operator family
is `episode-encode` / `episode-retrieve`
(`deep-research/memory-reasoning.md:417`).

**Layer 4 — Concept Memory.** Concepts
are SXL entities of type `knowledge`,
`concept`, or `entity` in
`cognitive/this-node/concept/*` —
generalisations that emerge when episodic
clusters stabilise. Retrieval is spreading
activation via `frame-match` and `cd-parse`
(`deep-research/memory-reasoning.md:68-76`).
Decay is slow (`exp(-μ·t)` with μ ≪ λ).
Promotion to Layer 5 follows
`hippocampus.md:315-320`.

### 2.5 Layer 5 — Principle Memory

Principles are invariant rules, laws, and
stable generalisations — `seed.sxl/v1`
entities with `(:type principle)` and a
confidence saturated near 1.0. Retrieval is
deductive forward chaining plus Markov Logic
Network inference
(`deep-research/memory-reasoning.md:110-111`).
Principles are not pruned by metabolic
triage; they are candidates for
re-evaluation only when the M5 contradiction
sweep (`metabolism.md:127-148`) finds
severity above 0.3.

**Layer 6 — Ontology Memory.** Ontology
memory holds the **type hierarchy** and the
**cross-domain mappings** — the substrate of
the codex. The `codex/solbian/` and
`codex/machina/` files are persistent
representations of parts of ontology memory.
Retrieval is subsumption, OWL 2 / Description
Logic reasoning, and conceptual graph
unification (Sowa 1984; ISO/IEC 24707 Common
Logic, see
`deep-research/memory-reasoning.md:98-111`).
Ontologies are revised only at epoch
boundaries, with the revision going through
human review per
`codex/machina/CONFIDENCE-RULES.md:18-30`.

**Layer 7 — Identity Memory.** Identity
memory holds the **cognitive core** — the
model of self, the immutable values, the
network identity (`did:seed:nodeA:...`), and
the load-bearing commitments. The cognitive
cycle refuses to revise this layer except
through a deliberate, human-reviewed
procedure. Retrieval is direct lookup; the
identity is the root of the self-model. The
identity layer is the **trust anchor** for
everything else: every SXL entity carries a
`:creator` field that resolves to a
`did:seed:...` identity, and the 5-role ACL
in `codex/machina/INTEGRATION-CONTRACT.md`
gates writes by identity role.

### 2.8 Promotion and demotion

Promotion is monotonic in stability: an entry
moves up the hierarchy when its support and
corroboration grow. Demotion is non-monotonic
and is triggered by contradiction, not by age.
The `forget` primitive
(`NSLP/ARCHITECTURE.md:96`) marks an entry
for decay rather than deleting it; the
metabolic triage `M4` performs the actual
eviction. A belief is demoted before it is
discarded, and the demotion is logged per
`codex/machina/CONFIDENCE-RULES.md`.

## 3. The belief revision engine

Beliefs are SXL entities of type `belief`,
`hypothesis`, or `knowledge`. They carry, in
addition to the standard SXL envelope, a
**revision record** that the engine uses to
update confidence in light of new evidence.

### 3.1 Belief envelope

The canonical belief shape is at
`NSLP/ARCHITECTURE.md:57-67`. A belief stores
`:confidence` (a real in `[0, 1]`), `:source`
(SXL reference to the originating entity),
`:evidence` (a list of supporting SXL
references with weights), `:timestamp`
(epoch nanoseconds), `:provenance`
(`:source` and `:attribution`),
`:relations` (outgoing typed relations), and
`:version` (incremented on each revision).
The engine never mutates a belief in place —
it writes a new version and links them. The
envelope is a strict superset of the SXL
entity model.

### 3.2 Revision operations

Three operations update a belief in light of
new evidence:

- **Confirmation**. The NSL `reinforce`
  primitive
  (`NSLP/ARCHITECTURE.md:147-152`) raises
  confidence: `confidence_new = confidence_old
  + delta`, capped at 1.0. The delta is
  computed by `propagate` (Group 7) using the
  rules in `libsexpr/src/confidence.c`
  (deductive, Bayesian, Dempster-Shafer,
  fuzzy, decay). When confidence reaches the
  `auto_commit_threshold` of 0.98
  (`codex/machina/CONFIDENCE-RULES.md:18`),
  the belief is queued for auto-commit at the
  next epoch transition.
- **Contradiction**. The NSL `contradicts`
  primitive
  (`NSLP/ARCHITECTURE.md:127-130`) detects
  logical contradiction; the M5 contradiction
  sweep (`metabolism.md:127-148`) applies the
  policy. If severity (the absolute
  confidence delta) exceeds 0.3, the
  lower-confidence belief is demoted
  (`confidence *= 0.5`) and its evidence
  chain is annotated with
  `"contradicted by <higher-belief-id>"`. If
  confidences are close, both are flagged for
  re-evaluation in the next reflection cycle
  and the contradiction is published to
  `org.seed.cog.contradiction`. A belief
  whose confidence falls below 0.90 (the
  `human_review_threshold`) is rejected and
  logged.
- **Refinement**. New evidence that sharpens
  the belief (adds a sub-case, a quantitative
  bound, or a contextual scope) leaves
  confidence unchanged and updates the
  evidence chain. The NSL `specialise`
  primitive
  (`NSLP/ARCHITECTURE.md:159-161`) implements
  this. Refinement is the most common
  operation; the others are reserved for
  moments when the model itself shifts.

### 3.3 Conflict resolution

When two beliefs contradict, the engine
does not delete the loser. The
higher-confidence, more-recently-evidenced
belief wins, and the loser is recorded as a
**competing hypothesis** — an SXL entity of
type `competing-hypothesis` linking the two
beliefs with a `:severity` field and a
`:resolution` field of `pending`. The
resolution is left open so that future
evidence can break the tie. This is the
**AGM** belief-revision tradition
(Alchourrón, Gärdenfors, Makinson 1985)
extended with a probabilistic confidence
model — the `metabolism.md:225-237`
reference to AGM's three postulates
(Inclusion, Success, Recovery) is the
formal anchor. The engine never discards
evidence: even when a belief is demoted, the
evidence chain is preserved and the version
is incremented. The append-only `.sref` log
in libsmem makes this a structural
property. The metabolic sleep-wake cycle
(`metabolism.md:151-180`) is the only
process that may renormalise confidence
across a belief cluster, and it does so
explicitly in the `Synaptic Normalization`
step (Phase S3).

The confidence thresholds and gates
referenced throughout this section are the
single source of truth defined in
`codex/machina/CONFIDENCE-RULES.md`
(`auto_commit_threshold` = 0.98,
`human_review_threshold` = 0.90, implicit
rejection below 0.90). The
`codex/machina/CONFIDENCE-RULES.md` file is
canonical; any local threshold in the belief
revision engine MUST be loaded from there at
startup, never hard-coded.

## 4. Cognitive homeostatic regulation

The belief revision engine can oscillate,
runaway, or get stuck. The metabolic cycle
(`metabolism.md:1-274`) is the autonomic
regulator that keeps it stable. It runs in
six phases, M1 through M6, on its own cadence
independent of the cognitive cycle.

**Oscillation damping.** The M5
contradiction sweep (`metabolism.md:127-148`)
computes a rolling average of contradiction
counts and a spike threshold (3σ above the
rolling average); a spike triggers
`metabolic_alert = true`, deferring
non-critical phases and forcing a belief
audit. Hysteresis in M3
(`metabolism.md:75-102`) is the second
dampening mechanism: mode transitions
require the new score to exceed the old
score by more than a hysteresis margin, so
the system does not chatter between EXPLORE
and EXPLOIT.

**Runaway reflection.** The `reflect`
primitive is bounded by depth
(`NSLP/ARCHITECTURE.md:188`). The metabolic
cycle enforces a global
**reflection-depth cap** of 5 recursive
levels (`metabolism.md:191-193`); any
reflect call that would exceed the cap is
truncated and the truncation is logged. A
**compute budget** is enforced per cycle:
the sum of `cost_estimate` across active
workflows (`NSLP/ARCHITECTURE.md:231`) is
checked against M1's resource vector
(`metabolism.md:38-53`); if the budget is
exhausted, the cycle defers non-critical
workflows to continuation state
(`NSLP/ARCHITECTURE.md:419-436`).

**Exploration vs exploitation.** M3
computes an exploration_score and an
exploitation_score and selects a mode
(`EXPLORE`, `EXPLOIT`, or `BALANCED`) with
a temperature τ. The schedule is
**adaptive**: every 20 cycles, the
algorithm forces an `EXPLORE` tick to
escape local optima. The two-dimensional
Ising model (Chakravarthy & Balasubramani
2018) at `metabolism.md:96-101` is the
biological inspiration.

**Reflective maintenance.** The M6
sleep-wake cycle (`metabolism.md:151-180`)
is the scheduled maintenance window.
Phase S1 (SWS Replay) re-runs recent
episodes in compressed time and extracts
common patterns — the cross-cortical
consolidation that promotes episodic to
semantic. Phase S2 (REM Recombination)
pairs concepts from different domains to
generate creative hypotheses. Phase S3
(Synaptic Normalization) renormalises
confidence sums to prevent inflation from
repeated reinforcement. The default
cadence is every 120 ticks (~10 minutes);
the schedule is configurable. The full
design is at `metabolism.md:1-274`, with
biological and computational references
at `metabolism.md:215-237` and interaction
points with the cognitive cycle at
`metabolism.md:194-213`.

## 5. Mapping the hippocampal five-layer model onto the seven-layer hierarchy

`NSLP/research/hippocampus.md:269-281` specifies
a five-layer hierarchy as the research target.
The seven-layer form in §2 is a research
extension that adds a pre-sensory Layer 1
(bus buffer, separated from the SST-level
sensory layer) and an identity Layer 7
(separated from principles because it is
immutable). The mapping is:

| Hippocampal | Engineering | Rationale |
|-------------|-------------|-----------|
| Layer 1 SENSORY (raw observations) | Engineering Layer 2 (Working) | Hippocampal Layer 1 includes parsed SXL; the bus buffer is engineering-only. |
| Layer 2 WORKING | Engineering Layer 2 | Direct. Miller's 7±2 cap. |
| Layer 3 EPISODIC | Engineering Layer 3 | Direct. |
| Layer 4 SEMANTIC | Engineering Layer 4 | Direct. |
| Layer 5 PRINCIPLE | Engineering Layer 5 | Direct. |
| (none) | Engineering Layer 6 (Ontology) | Extension. |
| (none) | Engineering Layer 7 (Identity) | Extension. |

The hippocampal substrate adds three
algorithms that the engineering layers rely
on. **Pattern Separation (DG)** —
`hippocampus.md:24-78`: sparse coding with
lateral inhibition; `pattern-separate` in NSL;
used at the Engineering Layer 1→2 boundary.
**Pattern Completion (CA3)** —
`hippocampus.md:79-138`: Modern Hopfield
attention; `pattern-complete` in NSL; used at
the Engineering Layer 3 retrieval boundary.
The Hopfield-Transformer equivalence (Ramsauer
et al. 2020) means the SST backend's
`SST_OP_RETRIEVE` operator
(`NSLP/ARCHITECTURE.md:209`) is the natural
executor. **Memory Replay (SWR)** —
`hippocampus.md:141-211`: prioritised
experience replay with TD learning; the
`memory-replay` workflow; used by the
metabolic M6 sleep-wake consolidation cycle
(`metabolism.md:151-180`).

The SDM substrate (`hippocampus.md:213-265`)
generalises the `query` and `assert` memory
primitives into radius-based approximate
matching over embedding vectors — a roadmap
item, not yet wired into the production
memory substrate. The predictive-coding /
free-energy substrate
(`hippocampus.md:335-365`) is what
`hippocampus.md:355-365` calls
`free-energy-update`: predict, compare to
observation, update if the prediction error
exceeds tolerance. This is the loop the
belief revision engine follows; the
`propagate` primitive
(`NSLP/ARCHITECTURE.md:147`) is the formal
substrate. The memory substrate is the
common denominator across all seven memory
layers.

## 6. The 32-algorithm research corpus

`NSLP/deep-research/memory-reasoning.md:1-457`
profiles 32 algorithms across six categories that
feed the memory hierarchy and belief revision
engine. The full table is at lines 413-445; 26 of
the 32 are flagged `ready-for-promotion`.

### 6.1 Memory architectures (5)

Layer substrates the seven-layer hierarchy can
inherit from: **HTM** (Hawkins & George 2006) —
sparse distributed representations with spatial
pooling; substrate for Layer 2-3.
**SDM** (Kanerva 1988) — Hamming-distance
activation; Layer 3 retrieval, generalised to
radius queries. **Episodic Memory** (Tulving
1972) — `(what, where, when)` indexing; Layer 3
organisation. **ACT-R Declarative Memory** —
covered in `deep-research/cognitive-cycles.md`;
the activation-decay substrate for Layer 2.
**Compressive Memory** (Sullivan & Harding
2019) — compressed sparse codes; candidate for
Layer 3-4 compression; not yet
ready-for-promotion.

### 6.2 Knowledge representation (7)

Representations for the layers above Episode:
**Semantic Networks** (Quillian 1968) — spreading
activation, Layer 4. **Frames** (Minsky 1975) —
slots and inheritance, Layer 4-5.
**Conceptual Dependency** (Schank 1975) — 11
primitive acts, Layer 3-4. **Conceptual Graphs**
(Sowa 1976/1984) — ISO 24707, Layer 6. **OWL 2
/ Description Logics** — Layer 6. **Markov Logic
Networks** — Layer 5-6. **Knowledge Graph
Embeddings** — Layer 4-6.

### 6.3 Reasoning and inference (11)

Algorithms that operate over the hierarchy:
**Variable Elimination for BNs**, **Belief
Propagation**, **MCMC and Gibbs Sampling** —
Layer 4-6. **CDCL (SAT)** — Layer 5-6. **Simulated
Annealing** — Layer 4-6. **Genetic Algorithm**,
**CMA-ES**, **Particle Swarm Optimisation**,
**Ant Colony Optimisation** — Layer 4-5.
**Rete Algorithm** — Layer 4-5. **Answer Set
Programming (ASP)** — Layer 5-6. Each is covered
in `deep-research/sxl-operators.md`.

### 6.4 Multi-agent and distributed reasoning (7)

Algorithms that coordinate across nodes:
**Contract Net Protocol** (Smith 1980), **VCG
Auction**, **PBFT** (Castro & Liskov 1999),
**Raft** (Ongaro & Ousterhout 2014), **Paxos**
(Lamport 1998), **Federated Learning
(FedAvg)**, **CRDTs** (Shapiro et al. 2011).
These are not memory layers, but they govern
how memory is replicated across nodes (the
`memory partition replication` referenced in
`appendices/A-GLOSSARY.md:91`).

### 6.5 Causal reasoning (6)

Algorithms that produce causal links between
episodes and concepts — the primary promotion
criterion for episodes (Layer 3→4) and
concepts (Layer 4→5) per
`hippocampus.md:308-309`: **Pearl's
do-Calculus** (Layer 5), **PC Algorithm**
(Spirtes, Glymour, Scheines 2000), **GES**
(Chickering 2002), **LiNGAM** (Shimizu et al.
2006), **Convergent Cross Mapping** (Sugihara
2012), and **Granger Causality** (Granger
1969, Nobel-cited).

### 6.6 Reinforcement learning (15)

Algorithms that drive belief revision and the
exploration-exploitation balance. **UCB1**
(Auer et al. 2002) and **Thompson Sampling**
(1933/2011) are the M3 substrate. **Value
Iteration** (Bellman 1957) and **Q-Learning**
(Watkins & Dayan 1992) serve Layer 3-5.
**DQN** (Mnih et al. 2015), **REINFORCE**
(Williams 1992), **A2C / A3C**, **PPO**,
**SAC**, **AlphaZero / MuZero**, **TD3**
(Fujimoto et al. 2018) are the deep-RL stack.
**World Models** (Ha & Schmidhuber 2018),
**HER** (Andrychowicz et al. 2017), **ICM**
(Pathak et al. 2017) — the Layer 2
novelty-signal substrate — and **Empowerment**
(Klyubin et al. 2005) close the category. PPO,
SAC, and AlphaZero / MuZero are covered in
`deep-research/cognitive-cycles.md`.

The full table with operator names and
ready-for-promotion flags is at
`deep-research/memory-reasoning.md:413-445`;
`Compressive Memory` and the §6.3 covered-out
items are the exceptions.

## 7. Cross-references

- `NSLP/ARCHITECTURE.md` — the four-layer ISA
  stack; Layer 2 NSL primitives (`store`,
  `recall`, `forget`, `bind` from Group 2;
  `reinforce`, `propagate`, `decay` from
  Group 7) are the substrate of the
  seven-layer memory hierarchy.
- `codex/machina/INTEGRATION-CONTRACT.md` —
  the 5-role ACL and policy bundle that gate
  writes to the memory partitions. Layer 7
  (Identity) is what the ACL binds to.
- `seed/INTEGRATION.md` — the memory
  partition model at the bus level. The
  `org.seed.memory.*` topic family
  (`seed/INTEGRATION.md:130`) is the
  publication channel for memory events
  (consolidation, contradiction, retrieval);
  the seedcogd cycle (Phase A subscribes to
  `org.seed.memory.*`, Phase C runs
  hippocampus consolidation every 5 cycles)
  is the conductor.
- `NSLP/research/metabolism.md` — M1-M6
  are the autonomic processes that keep the
  seven layers stable and govern the belief
  revision engine's damping, budget,
  exploration-exploitation balance, and
  scheduled maintenance.
- `NSLP/research/hippocampus.md` — the
  five-layer substrate, the
  pattern-separation / pattern-completion /
  replay algorithms, the SDM generalisation,
  and the predictive-coding free-energy
  principle.
- `NSLP/deep-research/memory-reasoning.md`
  — the 32-algorithm profile (six
  categories) that maps onto the seven
  layers and the belief revision engine.
- `codex/machina/CONFIDENCE-RULES.md` —
  the three confidence thresholds
  (0.98 / 0.90 / below-0.90) that the belief
  revision engine loads at startup.
