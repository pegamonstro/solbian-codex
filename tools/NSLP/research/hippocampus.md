# Hippocampal Memory Architecture

> Algorithmic principles extracted from hippocampal
> neuroscience for symbolic memory systems: pattern
> separation, pattern completion, memory replay,
> and hierarchical consolidation.
>
> Status: **Research notes** (sapling prototype)

## 1. The Biological Hippocampus

The hippocampus performs three critical memory functions
that map directly to computational requirements in a
symbolic cognitive system:

| Biological Structure | Function | Computational Analog |
|---------------------|----------|---------------------|
| Dentate Gyrus (DG) | Pattern separation | Make similar experiences distinct |
| CA3 | Pattern completion | Reconstruct full memory from partial cue |
| CA1 | Sequence learning | Learn temporal order of events |
| Sharp-wave ripples | Memory replay | Consolidate during rest |
| Entorhinal cortex | Spatial indexing | Navigate memory space |

## 2. Pattern Separation (Dentate Gyrus)

### 2.1 Biological Mechanism

The DG contains ~1 million granule cells in rats — vastly
more than its input from entorhinal cortex (~200,000 cells).
This expansion creates a **sparse code**: similar inputs
activate mostly non-overlapping populations of granule cells,
making memories distinct even when experiences are similar.

### 2.2 Algorithm: Sparse Coding + Competitive Learning

```
Algorithm PS: Pattern Separation
Input: input vector x ∈ R^n (sensory/perceptual encoding)
Output: sparse code h ∈ R^m where m >> n, ||h||_0 << m

1. Initialize dictionary D ∈ R^{n×m} with random weights
2. Normalize columns of D to unit L2 norm
3. Sparse coding (forward pass):
   h = argmin_h ||x - Dh||_2^2 + λ||h||_1
   (L1 penalty encourages sparsity — few active cells)
4. Competitive learning (Hebbian update):
   For each active cell i where h_i > 0:
     D[:,i] += η · h_i · (x - D[:,i])
     (move encoding toward input pattern)
5. Lateral inhibition:
   After each update, for each active cell i:
     For all other cells j where |D[:,i] - D[:,j]| < ε:
       D[:,j] -= η_inhibit · (D[:,i] - D[:,j])
     (push overlapping encodings apart — the key to separation)
```

### 2.3 NSL Implementation

```
(define pattern-separate
  (lambda (input sparse-dim sparsity)
    (seq
      (resolve dictionary :memory)  ; get current encoding dict
      (iterate dictionary
        (lambda (col acc)
          (seq
            (derive sparse-code input col)  ; L1-minimal encoding
            (branch (less? sparsity (car (reflect sparsity h)))
              (write col :weights (derive hebbian-update input col))
              nil)))
        nil))))
```

**Key hyperparameters**:
- Expansion ratio m/n: 5-10x (biological: ~5x in rat DG)
- Target sparsity: 2-5% active cells
- Sparsity penalty λ: tuned so ||h||_0 ≈ 0.03·m

## 3. Pattern Completion (CA3)

### 3.1 Biological Mechanism

CA3 has extensive recurrent collateral connections — each
pyramidal cell connects to ~12,000 others. This auto-associative
network can reconstruct a full memory pattern from a partial
or noisy cue. This is the neural basis of **reminding** — a
fragment triggering the complete memory.

### 3.2 Algorithm: Modern Hopfield Network

Classical Hopfield networks (1982) store ~0.14·N patterns
where N is the number of neurons. **Modern Hopfield networks**
(Ramsauer et al., 2020; Krotov & Hopfield, 2016) achieve
exponential storage capacity using higher-order interactions.

```
Algorithm PC: Pattern Completion (Modern Hopfield)
Input: query pattern ξ ∈ R^d, stored memories {x_1, ..., x_M}
Output: completed pattern x*, confidence c

1. Compute attention scores (softmax over dot products):
   For each stored memory i:
     energy_i = ξ^T x_i / √d  (scaled dot-product attention)
   attention = softmax(energy_1, ..., energy_M)

2. Retrieve completed pattern:
   x* = Σ_i attention_i · x_i
   (weighted sum of stored memories, dominated by best matches)

3. Confidence:
   c = max_i attention_i  (how strongly one memory dominates)
   If c < threshold: pattern completion FAILED (no good match)

Note: This is EXACTLY the Transformer attention mechanism.
Query = current partial cue, Keys = stored memory patterns,
Values = complete memory content. The Hopfield-Transformer
equivalence (Ramsauer et al., 2020) unifies memory retrieval
with attention-based inference.
```

### 3.3 NSL Implementation

```
(define pattern-complete
  (lambda (partial-cue memory-partition)
    (seq
      (query (:type episodic :content partial-cue) memory-partition)
      (branch (equal? (car results) nil)
        nil  ; no match found
        (seq
          (derive modern-hopfield partial-cue results)
          (reflect confidence))))))
```

**Connection to existing code**: The SST (`src/seed-transformer/`)
already implements attention mechanisms. Pattern completion
via modern Hopfield is an SST operator — `SST_OP_RETRIEVE` —
so it can be dispatched to the SST backend directly from the
NSL `derive` primitive.

## 4. Memory Replay (Sharp-Wave Ripples)

### 4.1 Biological Mechanism

During slow-wave sleep and quiet wakefulness, the hippocampus
generates **sharp-wave ripples** (SWRs) — brief (50-100ms)
high-frequency (150-250Hz) oscillations. During SWRs, CA3
and CA1 replay recently experienced sequences in **compressed
time** (~10-20x faster than original experience). This replay:
1. Consolidates memories from hippocampus to neocortex
2. Strengthens rewarded paths and weakens unrewarded ones
3. Enables inference of unobserved relationships
   (e.g., if A→B and B→C were experienced, replay may
    generate A→B→C sequences — transitive inference)

### 4.2 Algorithm: Prioritized Experience Replay with TD Learning

```
Algorithm MR: Memory Replay
Input: recent episodic memories E, value function V, discount γ
Output: consolidated memories, updated value estimates

1. Prioritize memories for replay:
   For each episode e in E:
     priority(e) = |TD_error(e)| + α · novelty(e) + β · goal_relevance(e)
   Sort E by priority descending

2. Replay top-K episodes in compressed time:
   For each episode e in replay_batch:
     For each transition (s_t, a_t, r_t, s_{t+1}) in e:
       // Temporal Difference update
       TD_target = r_t + γ · V(s_{t+1})
       TD_error = TD_target - V(s_t)
       V(s_t) += η · TD_error  // update value estimate

       // If TD_error is large → surprising outcome → mark for deeper analysis
       If |TD_error| > surprise_threshold:
         publish("org.seed.memory.surprising", (s_t, a_t, r_t, s_{t+1}))

3. Generate transitive inferences:
   For each pair of episodes (e_i, e_j) with overlapping concepts:
     If e_i ends with concept C and e_j begins with concept C:
       Merge: create candidate sequence e_i + e_j
       If merged sequence passes coherence check:
         Publish as hypothesis: "e_i may lead to e_j via C"

4. Cross-cortical consolidation:
   For each replayed memory:
     Extract declarative facts (what happened)
     Extract procedural patterns (how to respond)
     Promote to semantic memory (libsmem long-term partition)
```

### 4.3 NSL Implementation Sketch

```
(workflow memory-replay
  (seq
    (query (:type episodic :timestamp (range sleep-start now)) :recent)
    (iterate (sort (derive priority-score) results)
      (lambda (episode acc)
        (seq
          (derive td-update episode (resolve value-function))
          (branch (less? surprise-threshold (derive td-error episode))
            (assert (:type surprising-outcome :content episode) 0.7)
            nil)
          (branch (less? consolidation-threshold (derive confidence episode))
            (assert (:type semantic-knowledge :content (derive extract-facts episode)) 0.8)
            nil)))
      nil)))
```

## 5. Sparse Distributed Memory (Kanerva, 1988)

### 5.1 The Insight

Pentti Kanerva observed that the brain's memory is:
- **Sparse**: only a tiny fraction of neurons are active
- **Distributed**: each memory is stored across many neurons
- **Address-based**: retrieval works by matching addresses,
  not by searching content (content-addressable memory)

### 5.2 SDM Algorithm

```
Algorithm SDM: Sparse Distributed Memory
Parameters: N = address space dimension (e.g., 1000 bits)
            k = activation radius (e.g., 200 bits from address)
            M = number of hard locations (e.g., 1,000,000)

Storage:
  1. Generate M random hard-location addresses a_i ∈ {0,1}^N
  2. To store (address, data):
     For each hard location i where Hamming(a_i, address) < k:
       Update counter at location i with data

Retrieval:
  1. To retrieve from cue address:
     activated = {i : Hamming(a_i, cue) < k}
     If activated is empty: return nil (no memory near this cue)
     Sum the counters of all activated locations
     Threshold the sum to recover the stored data
     Confidence = |activated| / expected_activated
```

### 5.3 Connection to Modern Systems

SDM is the direct ancestor of:
- **Hopfield networks**: SDM with Hebbian learning
- **Transformer attention**: SDM retrieval = softmax over
  dot-product similarities
- **Vector databases**: SDM with embeddings instead of
  binary addresses

### 5.4 NSL Mapping

SDM maps to NSL's `query` + `assert` primitives:
- `assert` = SDM storage (write to memory)
- `query` = SDM retrieval (read from memory using address match)
- The libsmem FTS5 full-text index is a degenerate case of
  SDM (exact match, not radius-based)

A full SDM implementation for NSL would generalize `query`
to support radius-based approximate matching over embedding
vectors stored in libsmem.

## 6. Hierarchical Memory Organization

### 6.1 The 5-Layer Hierarchy

```
Layer 5: PRINCIPLE   (invariant truths, laws, identity)
           ↑ consolidation: extract invariants
Layer 4: SEMANTIC    (concepts, categories, facts)
           ↑ consolidation: cluster episodes into concepts
Layer 3: EPISODIC    (sequences of events, stories)
           ↑ consolidation: chunk sensory sequences
Layer 2: WORKING     (active items, ~7±2 chunks, 30s decay)
           ↑ attention: select what enters
Layer 1: SENSORY     (raw observations, percepts, bus messages)
```

### 6.2 Promotion Algorithm

```
Algorithm HP: Hierarchical Promotion
Input: memory at layer L, promotion criteria C_L
Output: promoted memory at layer L+1

Layer 1→2 (Sensory→Working):
  attention_score(s) = urgency(s)·0.25 + importance(s)·0.25 +
                       novelty(s)·0.20 + goal_relevance(s)·0.15 +
                       prediction_error(s)·0.10 + recency(s)·0.05
  If attention_score(s) > threshold: promote to working memory
  Capacity: 5-9 items (Miller's Law, 7±2)

Layer 2→3 (Working→Episodic):
  If working memory item is associated with:
    - A temporal sequence (start time, end time)
    - A context (what task/cycle was active)
    - An outcome (what happened next)
  Then: promote to episodic memory as (context, sequence, outcome) tuple
  Confidence: product of component confidences

Layer 3→4 (Episodic→Semantic):
  Cluster episodes by shared concepts using:
    - Co-occurrence: concepts that appear together in >3 episodes
    - Causal: A precedes B in >80% of episodes containing both
    - Taxonomic: A is-a B (from type hierarchy)
  For each cluster with >min_cluster_size episodes:
    Extract common pattern → semantic concept
    Confidence: 1 - (variance in cluster / total variance)

Layer 4→5 (Semantic→Principle):
  For each semantic concept:
    If concept has been stable (unchanged) for >N cycles
    AND concept is referenced by >M other concepts
    AND concept has been confirmed by >K independent sources:
      Promote to principle (invariant knowledge)
      Confidence: product of stability, centrality, and corroboration
```

### 6.3 Integration with Existing Code

The current consolidation system in `seedcogd/main.c` Phase C
and `lua/helpers/hippocampus.lua` implements a subset:
- Episodic → Semantic (compose + generalise)
- No explicit Sensory→Working promotion (done ad-hoc in Phase H)
- No Working→Episodic promotion (entries stay in the index)
- No Semantic→Principle promotion (not implemented)

The NSL hippocampal architecture extends the existing 2-level
consolidation to the full 5-level hierarchy.

## 7. Predictive Coding and Free Energy

### 7.1 The Free Energy Principle (Friston, 2010)

All adaptive systems minimize **free energy** — the difference
between their internal model's predictions and actual sensory
input. This unifies perception, learning, and action:

```
F = D_KL(q(θ) || p(θ)) - E_q[log p(data|θ)]
  = complexity - accuracy
```

- Minimize complexity: prefer simpler models (Occam's razor)
- Maximize accuracy: prefer models that predict observations
- The balance is a variational optimization problem

### 7.2 NSL Application

```
(define free-energy-update
  (lambda (belief evidence)
    (seq
      (derive predict belief)  ; what does belief predict?
      (derive prediction-error evidence)
      (branch (less? prediction-error tolerance)
        belief  ; prediction confirmed, no update needed
        (seq
          (derive natural-gradient belief evidence)
          (assert updated-belief (+ (reflect confidence belief) 0.01)))))))
```

### 7.3 Key References
- Friston, K. (2010). "The free-energy principle: a unified brain theory." *Nat. Rev. Neurosci.*
- Friston, K. & Kiebel, S. (2009). "Predictive coding under the free-energy principle." *Phil. Trans. R. Soc. B.*
- Rao, R. P. N. & Ballard, D. H. (1999). "Predictive coding in the visual cortex." *Nat. Neurosci.*

## 8. Key References

### Neuroscience
- O'Keefe, J. & Nadel, L. (1978). *The Hippocampus as a Cognitive Map.* Oxford.
- Buzsáki, G. (2006). *Rhythms of the Brain.* Oxford.
- Buzsáki, G. (2015). "Hippocampal sharp wave-ripple." *Hippocampus.*
- Marr, D. (1971). "Simple memory: a theory for archicortex." *Phil. Trans. R. Soc. B.*

### Computational Models
- Hopfield, J. J. (1982). "Neural networks and physical systems with emergent collective computational abilities." *PNAS.*
- Ramsauer, H. et al. (2020). "Hopfield Networks is All You Need." *ICLR 2021.*
- Krotov, D. & Hopfield, J. J. (2016). "Dense associative memory for pattern recognition." *NeurIPS.*
- Kanerva, P. (1988). *Sparse Distributed Memory.* MIT Press.
- Kanerva, P. (2009). "Hyperdimensional computing: An introduction to computing in distributed representation." *Cognitive Computation.*

### Hierarchical Memory
- Hawkins, J. & Blakeslee, S. (2004). *On Intelligence.* Times Books.
- Hawkins, J. & Ahmad, S. (2016). "Why neurons have thousands of synapses." *Frontiers in Neural Circuits.*
- Hassabis, D. et al. (2017). "Neuroscience-inspired artificial intelligence." *Neuron.*
