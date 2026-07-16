# Computational Metabolism

> The basal cognitive processes that maintain homeostasis
> in a symbol-processing machine — analogous to respiration,
> circulation, and autonomic regulation in biology.
>
> Status: **Research notes** (sapling prototype)

## 1. The Biological Analogy

Biological systems maintain homeostasis through autonomic
processes that operate without conscious direction:
respiration, circulation, digestion, temperature regulation,
immune response, cellular repair, sleep-wake cycles.

A cognitive machine needs analogous processes:
- **Cognitive respiration**: cycling context windows, clearing
  working memory, refreshing attention budgets
- **Cognitive circulation**: moving information between memory
  layers, distributing computational load
- **Cognitive digestion**: breaking down observations into
  beliefs, assimilating new knowledge into existing structures
- **Cognitive thermoregulation**: preventing runaway reflection,
  damping oscillations, balancing exploration/exploitation
- **Cognitive immune response**: detecting contradictions,
  isolating harmful beliefs, repairing damaged knowledge
- **Cognitive sleep**: consolidating memories, pruning obsolete
  knowledge, reconfiguring neural-symbolic mappings

## 2. The 6-Phase Basal Metabolic Cycle

### 2.1 Design Rationale

The metabolic cycle runs independently of the cognitive cycle.
It is the "autonomic nervous system" of S.E.E.D. — always
running, regulating resources, maintaining equilibrium.

### 2.2 Phase M1: Resource Sampling (every 5 seconds)

```
Algorithm M1: Resource Sampling
Input: system state
Output: resource vector R = (cpu, ram, gpu, tokens, context_free, disk)

1. Sample CPU utilization from /proc/stat
2. Sample RAM from /proc/meminfo or cgroups
3. Sample GPU utilization (nvidia-smi or equivalent)
4. Count tokens consumed this cycle (from libseedllm pool)
5. Measure free context window per active backend
6. Check disk space for libsmem partition growth
7. Publish R to org.seed.metabolic.resources
8. If any resource > 90% threshold: set metabolic_alert = true
```

### 2.3 Phase M2: Attention Budget Allocation (every 10 seconds)

```
Algorithm M2: Attention Budget Allocation
Input: current goals G, resource vector R, recent observations O
Output: attention budget B per cognitive domain

1. For each cognitive domain d:
   a. Compute urgency(d) from goal deadlines and dependencies
   b. Compute importance(d) from goal priority weights
   c. Compute novelty(O, d) from KL divergence of recent vs. expected observations
   d. Compute cost(d) from estimated tokens, memory, and latency
   e. score(d) = 0.25·urgency + 0.25·importance + 0.20·novelty + 0.15·(1-cost_norm) + 0.15·goal_relevance
2. Normalize scores → B = softmax(scores)
3. Apply resource constraints: B' = min(B, R.available_tokens / cost(d))
4. Publish B' to org.seed.metabolic.attention
5. If any score(d) < floor_threshold: mark domain d as dormant this cycle
```

### 2.4 Phase M3: Exploration-Exploitation Balancing (every 60 seconds)

```
Algorithm M3: E/E Balancing (dopamine/noradrenaline-inspired)
Input: recent performance P, diversity metric D, cycle count c
Output: mode ∈ {EXPLORE, EXPLOIT}, temperature τ

1. Compute performance trend: ΔP = P_current - P_rolling_average
2. Compute diversity: D = entropy of recent cognitive outputs
3. Compute exploitation_score = sigmoid(ΔP / σ_P) · (1 - D/D_max)
4. Compute exploration_score = (1 - sigmoid(ΔP / σ_P)) · D/D_max
5. If exploitation_score > exploration_score + hysteresis:
     mode = EXPLOIT; τ = 0.1  (low temperature, focused)
   Else if exploration_score > exploitation_score + hysteresis:
     mode = EXPLORE; τ = 1.0  (high temperature, diverse)
   Else:
     mode = BALANCED; τ = 0.5
6. Every 20 cycles: force EXPLORE mode for one cycle
   (stochastic resonance — prevents getting stuck in local optima)
7. Publish (mode, τ) to org.seed.metabolic.mode
```

**Biological basis**: Basal ganglia dopamine encodes reward
prediction error (ΔP). Noradrenaline modulates exploration
intensity via subthalamic nucleus (STN) regulation.
Two-dimensional Ising network in the indirect pathway
generates adaptive structured exploration (Chakravarthy &
Balasubramani, 2018).

### 2.5 Phase M4: Memory Triage (every 5 cognitive cycles)

```
Algorithm M4: Memory Triage (autophagy-inspired)
Input: memory partitions P, access patterns A, age thresholds T
Output: triage decisions (KEEP, COMPRESS, ARCHIVE, DELETE)

1. For each memory entry e:
   a. Compute recency_score = exp(-λ · (now - e.last_access))
   b. Compute utility_score = e.access_count / (now - e.created)
   c. Compute confidence_decay = e.confidence · exp(-μ · (now - e.last_reinforced))
   d. triage_score = 0.3·recency + 0.3·utility + 0.2·confidence_decay + 0.2·goal_relevance(e)
2. Sort entries by triage_score ascending
3. KEEP: triage_score > keep_threshold (top 60%)
4. COMPRESS: keep_threshold ≥ triage_score > compress_threshold (next 25%)
   → Extract key facts, discard details, store as summary
5. ARCHIVE: compress_threshold ≥ triage_score > archive_threshold (next 10%)
   → Move to cold storage (compressed, offline-accessible)
6. DELETE: triage_score ≤ archive_threshold (bottom 5%)
   → Permanent removal, log deletion reason
7. Publish triage summary to org.seed.metabolic.memory
```

### 2.6 Phase M5: Contradiction Sweep (every 20 cycles)

```
Algorithm M5: Contradiction Sweep (immune-inspired)
Input: all asserted beliefs B
Output: contradiction set C, resolution actions

1. For each pair (b1, b2) in B where b1 and b2 share a domain:
   a. If contradicts(b1, b2):
      - Compute contradiction severity = |b1.confidence - b2.confidence|
      - If severity > threshold: add (b1, b2, severity) to C
2. For each contradiction in C (ordered by severity descending):
   a. If one belief has significantly higher confidence (>0.3 delta):
      - Demote the lower-confidence belief: confidence *= 0.5
      - Add evidence chain: "contradicted by <higher-belief-id>"
   b. If both have similar confidence:
      - Flag both for re-evaluation in next reflection cycle
      - Publish to org.seed.cog.contradiction
3. If |C| > spike_threshold (3σ above rolling average):
   - Trigger metabolic_alert = true
   - Schedule emergency belief audit
4. Publish contradiction report
```

### 2.7 Phase M6: Sleep-Wake Cycle (background, configurable)

```
Algorithm M6: Sleep-Wake Consolidation
Input: all memory partitions
Output: consolidated knowledge, pruned memories

Phase S1 — SWS Replay (Slow-Wave Sleep analog):
  1. Select high-utility episodic memories from the wake period
  2. Replay them in compressed time (10x speed)
  3. For each replayed sequence:
     a. Extract common patterns across episodes
     b. Identify causal relationships (A preceded B in >80% of sequences)
     c. Generate generalization hypotheses

Phase S2 — REM Recombination (REM sleep analog):
  1. Randomly pair concepts from different domains
  2. Test each pair for productive recombination:
     a. Does the combination produce a novel insight?
     b. Is the combination plausible (passes basic consistency checks)?
  3. Promote promising recombinations to creative output queue
  4. Discard unproductive recombinations

Phase S3 — Synaptic Normalization:
  1. For each active belief cluster:
     a. Compute total "weight" (sum of confidences)
     b. Renormalize: scale all confidences so sum = 1.0
     c. This prevents confidence inflation from repeated reinforcement
  2. Decay all access frequencies by factor 0.5
     (ready for next wake period's accumulation)
```

## 3. Metabolic Homeostasis Targets

| Variable | Target Range | Action if Low | Action if High |
|----------|-------------|---------------|----------------|
| Free context window | > 25% of max | Drop lowest-priority entries from working memory | None |
| Token consumption rate | < 80% of budget | Increase temperature (explore simpler paths) | Reduce batch sizes, defer non-urgent queries |
| Memory fragmentation | < 30% | Trigger compaction cycle | None |
| Belief contradiction count | < 5% of total beliefs | None | Trigger emergency audit (M5) |
| Prediction error EMA | 0.1–0.3 | Model may be overfitting; increase exploration | Model underperforming; check backend health |
| Cognitive diversity (entropy) | 0.3–0.7 | Force exploration mode | Reduce temperature, focus on best paths |
| Reflection depth | 1–5 recursive levels | None (shallow is efficient) | Cap recursion at 5 to prevent runaway reflection |

## 4. Integration with the Cognitive Cycle

The metabolic cycle (M1-M6) runs as a **background process**
alongside the cognitive cycle (A-L). Key integration points:

1. **Before Phase A (Reflection)**: Check metabolic mode
   (EXPLORE/EXPLOIT) to set reflection temperature and scope.

2. **Before Phase H (Attention)**: Read M2's attention budget
   allocation instead of computing scores from scratch.

3. **Before Phase I (Working Memory)**: Apply M4's triage
   decisions (KEEP/COMPRESS/ARCHIVE/DELETE) to entry eviction.

4. **Phase C (Consolidation)**: Extended by M6's sleep-wake
   consolidation during rest periods.

5. **Resource-constrained phases**: Check M1's resource
   vector before launching expensive LLM calls. If token
   budget is exhausted, defer non-critical phases.

## 5. Key References

### Biological Foundations
- Chakravarthy, V. S. & Balasubramani, P. P. (2018). "The basal ganglia as an engine for exploration." In *Computational Neuroscience Models of the Basal Ganglia.* Springer.
- Moustafa, A. A. et al. (2018). "The motor, cognitive, affective, and autonomic functions of the basal ganglia."
- Friston, K. (2010). "The free-energy principle: a unified brain theory." *Nat. Rev. Neurosci.*
- Buzsáki, G. (2015). "Hippocampal sharp wave-ripple: A cognitive biomarker for episodic memory and planning." *Hippocampus.*
- Diekelmann, S. & Born, J. (2010). "The memory function of sleep." *Nat. Rev. Neurosci.*

### Computational Foundations
- Alchourrón, C. E., Gärdenfors, P., & Makinson, D. (1985). "On the logic of theory change: Partial meet contraction and revision functions." *J. Symb. Logic* 50(2):510-530.
- Gärdenfors, P. (1988). *Knowledge in Flux: Modeling the Dynamics of Epistemic States.* MIT Press.
- Sutton, R. S. & Barto, A. G. (2018). *Reinforcement Learning: An Introduction.* 2nd ed. MIT Press.
- Mnih, V. et al. (2015). "Human-level control through deep reinforcement learning." *Nature.*

### AGM Belief Revision
The three AGM postulates for belief contraction:
1. **Inclusion**: K÷φ ⊆ K (contraction removes beliefs, never adds)
2. **Success**: If φ is not a tautology, then φ ∉ K÷φ
3. **Recovery**: K ⊆ (K÷φ)+φ (re-expanding recovers original beliefs)

NSL's `retract` implements AGM contraction; `assert` with
updated confidence implements AGM expansion.

## 6. Pseudocode: Full Metabolic Tick

```
function metabolic_tick(state):
    // M1: Resource sampling (every tick)
    R = sample_resources()
    publish("org.seed.metabolic.resources", R)

    // M2: Attention budget (every 2nd tick)
    if tick % 2 == 0:
        B = allocate_attention(state.goals, R, state.recent_obs)
        publish("org.seed.metabolic.attention", B)

    // M3: E/E balancing (every 12th tick ~ 60s)
    if tick % 12 == 0:
        (mode, tau) = balance_exploration(state.performance, state.diversity, tick)
        publish("org.seed.metabolic.mode", {mode, tau})

    // M4: Memory triage (every tick)
    decisions = triage_memory(state.memory, state.access_patterns)
    apply_triage(decisions)

    // M5: Contradiction sweep (every 4th tick)
    if tick % 4 == 0:
        contradictions = sweep_contradictions(state.beliefs)
        if len(contradictions) > state.contradiction_baseline * 3:
            trigger_alert("contradiction_spike")

    // M6: Sleep-wake (every 120th tick ~ 10 min)
    if tick % 120 == 0:
        if state.mode == REST:
            consolidate_sleep(state.memory)
        else:
            // Light consolidation during active mode
            light_consolidate(state.memory, max_duration_ms=5000)
```
