# Memory, Knowledge, and Reasoning Algorithms — Canonical Research

> **Knowledge base for the S.E.E.D.
> memory subsystem**. Memory
> architectures, knowledge representation
> schemes, multi-agent coordination,
> causal reasoning, and reinforcement
> learning. Each entry is sourced to its
> canonical reference.
>
> **Status (2026-07-17)**: 51 entries;
> 47 ✅, 3 🟢, 1 🔴 (Compressive
> Memory §1.5).

## 1. Memory Architectures

### 1.1 Hierarchical Temporal Memory (HTM)

- **Year / citation**: Hawkins & George 2006 (Numenta
  whitepaper). Hawkins & Ahmad 2017 ("Why Neurons
  Have Thousands of Synapses", *Frontiers in
  Neuroscience* 11:30).
- **Core idea**: A hierarchical network of *sparse
  distributed representations* (SDR). Each region learns
  temporal sequences via *spatial pooling* (sparsification)
  and *temporal memory* (prediction via column activation).
- **Confirmation flag**: 🟢 `confirmed-curated`
- **Ready-for-promotion**: ✅ Yes (Numenta implementation).

### 1.2 Sparse Distributed Memory (SDM)

- **Year / citation**: Kanerva 1988. *Sparse Distributed
  Memory*. MIT Press.
- **Core idea**: A memory of 2^n locations stored as
  d-dimensional binary vectors (n = 256, d = 1000). On
  read, the k nearest addresses contribute, weighted by
  Hamming distance. Probabilistic in nature.
- **Confirmation flag**: ✅ `confirmed-canonical`
- **Ready-for-promotion**: ✅ Yes.

### 1.3 Episodic Memory (Tulving)

- **Year / citation**: Tulving 1972 ("Episodic and
  Semantic Memory"); Tulving 1983 (*Elements of Episodic
  Memory*).
- **Core idea**: Episodic memory stores personally
  experienced events indexed by (what, where, when); it
  differs from semantic memory (general knowledge). The
  "encoding specificity principle" predicts that retrieval
  is most successful when context matches encoding.
- **Confirmation flag**: 🟢 `confirmed-curated`
- **Ready-for-promotion**: ✅ Yes (theoretical frame;
  implementations are many).

### 1.4 ACT-R Declarative Memory

- **See `cognitive-cycles.md` §1.1 (canonical reference:
  https://act-r.psy.cmu.edu/)**.
- **Confirmation flag**: ✅ `confirmed-canonical`

### 1.5 Compressive Memory

- **Year / citation**: Jazayeri & Fiete 2014.
  "Compressive Memory: A Flexible Memory Formation
  Mechanism for Efficient Learning of Episodic
  Traces". arXiv:1401.4410.
- **Core idea**: A framework where episodic traces are
  stored as compressed sparse codes; the memory is
  queried by content-based addressing in a single
  associative lookup.
- **Confirmation flag**: 🔴 `speculative`
- **Ready-for-promotion**: ⚠️ Pending primary-source pass.

## 2. Knowledge Representation

### 2.1 Semantic Networks

- **Year / citation**: Quillian 1968. "Semantic Memory".
  In Minsky (ed.) *Semantic Information Processing*.
- **Core idea**: Concepts are nodes; relations are labelled
  edges. *Spreading activation* propagates energy from
  activation sources outward.
- **Confirmation flag**: ✅ `confirmed-canonical`
- **Ready-for-promotion**: ✅ Yes (frame model).

### 2.2 Frames (Minsky)

- **Year / citation**: Minsky 1975. "A Framework for
  Representing Knowledge". In Winston (ed.) *The
  Psychology of Computer Vision*.
- **Core idea**: A *frame* is a data structure with slots
  and slot values. Frames are organised in a hierarchy;
  inheritance propagates default values.
- **Confirmation flag**: ✅ `confirmed-canonical`
- **Ready-for-promotion**: ✅ Yes.

### 2.3 Conceptual Dependency (Schank)

- **Year / citation**: Schank 1972 ("Conceptual
  Dependency: A Theory of Natural Language
  Understanding", *Cognitive Psychology* 3(4):
  552–631). Schank & Abelson 1977 *Scripts,
  Plans, Goals*.
- **Core idea**: A canonical set of 11 primitive acts
  (PTRANS, ATRANS, MTRANS, MBUILD, ATTEND, etc.) that
  compose to describe any action. The basis of script-
  based NLU.
- **Confirmation flag**: 🟢 `confirmed-curated`
- **Ready-for-promotion**: ✅ Yes.

### 2.4 Conceptual Graphs (Sowa)

- **Year / citation**: Sowa 1976, 1984. ISO/IEC 24707
  Common Logic.
- **See `sxl-operators.md` §6.1 (canonical reference:
  https://www.w3.org/2001/sw/wiki/Conceptual_Graphs)**.
- **Confirmation flag**: ✅ `confirmed-canonical`

### 2.5 OWL 2 / Description Logics

- **See `sxl-operators.md` §2.1-2.3 (canonical reference:
  https://www.w3.org/TR/owl2-overview/)**.
- **Confirmation flag**: ✅ `confirmed-canonical`

### 2.6 Markov Logic Networks (MLN)

- **See `sxl-operators.md` §6.3 (canonical reference:
  https://en.wikipedia.org/wiki/Markov_logic_network)**.
- **Confirmation flag**: ✅ `confirmed-canonical`

### 2.7 Knowledge Graph Embeddings

- **See `sxl-operators.md` §6.5 (canonical reference:
  https://arxiv.org/abs/1707.01449)**.
- **Confirmation flag**: ✅ `confirmed-canonical`

## 3. Reasoning and Inference Algorithms

### 3.1 Variable Elimination for BNs

- **See `sxl-operators.md` §5.1 (canonical reference:
  https://en.wikipedia.org/wiki/Variable_elimination)**.
- **Confirmation flag**: ✅ `confirmed-canonical`

### 3.2 Belief Propagation

- **See `sxl-operators.md` §5.2 (canonical reference:
  https://en.wikipedia.org/wiki/Belief_propagation)**.
- **Confirmation flag**: ✅ `confirmed-canonical`

### 3.3 MCMC and Gibbs Sampling

- **See `sxl-operators.md` §5.3 (canonical reference:
  https://en.wikipedia.org/wiki/Markov_chain_Monte_Carlo)**.
- **Confirmation flag**: ✅ `confirmed-canonical`

### 3.4 CDCL (SAT)

- **See `sxl-operators.md` §3.1 (canonical reference:
  https://en.wikipedia.org/wiki/Conflict-driven_clause_learning)**.
- **Confirmation flag**: ✅ `confirmed-canonical`

### 3.5 Simulated Annealing

- **See `sxl-operators.md` §7.3 (canonical reference:
  https://en.wikipedia.org/wiki/Simulated_annealing)**.
- **Confirmation flag**: ✅ `confirmed-canonical`

### 3.6 Genetic Algorithm

- **See `sxl-operators.md` §7.4 (canonical reference:
  https://en.wikipedia.org/wiki/Genetic_algorithm)**.
- **Confirmation flag**: ✅ `confirmed-canonical`

### 3.7 CMA-ES

- **See `sxl-operators.md` §7.5 (canonical reference:
  https://arxiv.org/abs/1604.00772)**.
- **Confirmation flag**: ✅ `confirmed-canonical`

### 3.8 Particle Swarm Optimisation

- **See `sxl-operators.md` §7.6 (canonical reference:
  https://en.wikipedia.org/wiki/Particle_swarm_optimization)**.
- **Confirmation flag**: ✅ `confirmed-canonical`

### 3.9 Ant Colony Optimisation

- **See `sxl-operators.md` §7.7 (canonical reference:
  https://en.wikipedia.org/wiki/Ant_colony_optimization_algorithms)**.
- **Confirmation flag**: ✅ `confirmed-canonical`

### 3.10 Rete Algorithm

- **See `sxl-operators.md` §8.1 (canonical reference:
  https://en.wikipedia.org/wiki/Rete_algorithm)**.
- **Confirmation flag**: ✅ `confirmed-canonical`

### 3.11 Answer Set Programming (ASP)

- **See `sxl-operators.md` §8.3 (canonical reference:
  https://en.wikipedia.org/wiki/Answer_set_programming)**.
- **Confirmation flag**: ✅ `confirmed-canonical`

## 4. Multi-Agent and Distributed Reasoning

### 4.1 Contract Net Protocol

- **Year / citation**: Smith 1980. "The Contract Net
  Protocol: High-Level Communication and Control in a
  Distributed Problem Solver". *IEEE TC* C-29(12):
  1104–1113.
- **Core idea**: A manager announces a task; agents bid;
  the manager awards the contract to the best bid. Used
  in FIPA-compliant multi-agent systems.
- **Confirmation flag**: ✅ `confirmed-canonical`
- **Ready-for-promotion**: ✅ Yes (FIPA standard).

### 4.2 VCG Auction (Vickrey-Clarke-Groves)

- **Year / citation**: Vickrey 1961; Clarke 1971; Groves
  1973. Truthful mechanism design.
- **Core idea**: An auction where each agent's payment
  equals the externality the agent imposes on the others'
  utilities. Dominant strategy is to bid truthfully.
- **Confirmation flag**: ✅ `confirmed-canonical`
- **Ready-for-promotion**: ✅ Yes.

### 4.3 PBFT (Practical Byzantine Fault Tolerance)

- **Year / citation**: Castro & Liskov 1999. "Practical
  Byzantine Fault Tolerance". OSDI 1999.
- **Core idea**: A replicated state machine that
  tolerates f Byzantine faults with 3f+1 replicas
  through a three-phase protocol (pre-prepare, prepare,
  commit). O(n²) messages per request.
- **Confirmation flag**: ✅ `confirmed-canonical`
- **Ready-for-promotion**: ✅ Yes (industry: IBM
  Hyperledger Fabric, etc.).

### 4.4 Raft Consensus

- **Year / citation**: Ongaro & Ousterhout 2014. "In
  Search of an Understandable Consensus Algorithm".
  USENIX ATC.
- **Core idea**: Leader-based consensus with leader
  election, log replication, and a joint-consensus
  membership change. Designed for understandability
  (vs Paxos).
- **Confirmation flag**: ✅ `confirmed-canonical`
- **Ready-for-promotion**: ✅ Yes.

### 4.5 Paxos

- **Year / citation**: Lamport 1998. "The Part-Time
  Parliament". *ACM TOCS* 16(2): 133–169.
- **Core idea**: A two-phase consensus protocol with
  proposers, acceptors, and learners. Multi-Paxos
  amortises phase 1.
- **Confirmation flag**: ✅ `confirmed-canonical`
- **Ready-for-promotion**: ✅ Yes (foundational).

### 4.6 Federated Learning (FedAvg)

- **Year / citation**: McMahan, Moore, Ramage, Hampson,
  y Arcas 2017. "Communication-Efficient Learning of
  Deep Networks from Decentralized Data". AISTATS.
- **Core idea**: Each client trains on local data; the
  server averages model updates periodically. Reduces
  communication by 10-100× vs naive distributed SGD.
- **Confirmation flag**: ✅ `confirmed-canonical`
- **Ready-for-promotion**: ✅ Yes.

### 4.7 CRDTs (Conflict-Free Replicated Data Types)

- **Year / citation**: Shapiro, Preguiça, Baquero, Zawirski
  2011. "A Comprehensive Study of Convergent and
  Commutative Replicated Data Types". INRIA RR-7506.
- **Core idea**: Data types whose concurrent updates
  *commute* and *converge* without coordination.
  Two families: state-based (CvRDTs, joined by the
  semi-lattice join) and op-based (CmRDTs, with causal
  delivery).
- **Confirmation flag**: ✅ `confirmed-canonical`
- **Ready-for-promotion**: ✅ Yes.

## 5. Causal Reasoning

### 5.1 Pearl's do-Calculus

- **Year / citation**: Pearl 1995, 2009.
- **Covered in sxl-operators.md §10.1**.
- **Confirmation flag**: ✅ `confirmed-canonical`

### 5.2 PC Algorithm

- **Year / citation**: Spirtes, Glymour, Scheines 2000.
- **See `sxl-operators.md` §10.2 (canonical reference:
  https://en.wikipedia.org/wiki/PC_algorithm)**.
- **Confirmation flag**: ✅ `confirmed-canonical`

### 5.3 GES (Greedy Equivalence Search)

- **Year / citation**: Chickering 2002.
- **Covered in sxl-operators.md §12.1**.
- **Confirmation flag**: ✅ `confirmed-canonical`

### 5.4 LiNGAM

- **Year / citation**: Shimizu et al. 2006.
- **Covered in sxl-operators.md §12.2**.
- **Confirmation flag**: ✅ `confirmed-canonical`

### 5.5 Convergent Cross Mapping (CCM)

- **Year / citation**: Sugihara et al. 2012.
- **Covered in sxl-operators.md §10.3**.
- **Confirmation flag**: ✅ `confirmed-canonical`

### 5.6 Granger Causality

- **Year / citation**: Granger 1969. "Investigating
  Causal Relations by Econometric Models and Cross-
  spectral Methods". *Econometrica* 37(3): 424–438.
- **Core idea**: X Granger-causes Y if past values of X
  improve the prediction of Y beyond using only past Y.
  Tested via F-test on the restricted vs unrestricted
  regression.
- **Confirmation flag**: ✅ `confirmed-canonical`
- **Ready-for-promotion**: ✅ Yes (Nobel-cited).

## 6. Reinforcement Learning

### 6.1 UCB1 (Multi-Armed Bandit)

- **Year / citation**: Auer, Cesa-Bianchi, Fischer 2002.
  "Finite-Time Analysis of the Multiarmed Bandit Problem".
  *Machine Learning* 47: 235–256.
- **Core idea**: a_t = argmax_a (Q̂(a) + √(2 ln t / N(a))).
  The bonus is the UCB1 confidence term.
- **Confirmation flag**: ✅ `confirmed-canonical`
- **Ready-for-promotion**: ✅ Yes.

### 6.2 Thompson Sampling

- **Year / citation**: Thompson 1933. "On the Likelihood
  that One Unknown Probability Exceeds Another in View of
  the Evidence of Two Samples". *Biometrika* 25: 285–294.
  Chapelle & Li 2011 (empirical study).
- **Core idea**: Sample θ from the posterior
  P(θ | D), then take a_t = argmax_a E[R | θ, a]. The
  posterior shrinks as data accumulates.
- **Confirmation flag**: ✅ `confirmed-canonical`
- **Ready-for-promotion**: ✅ Yes.

### 6.3 Value Iteration

- **Year / citation**: Bellman 1957 *Dynamic Programming*.
- **Core idea**: V_{k+1}(s) = max_a Σ_{s', r} p(s', r | s, a)
  [r + γ V_k(s')]. Converges in polynomial time; for
  discount factor γ, error decays as γ^k.
- **Confirmation flag**: ✅ `confirmed-canonical`
- **Ready-for-promotion**: ✅ Yes.

### 6.4 Q-Learning

- **Year / citation**: Watkins & Dayan 1992. "Q-Learning".
  *Machine Learning* 8: 279–292.
- **Core idea**: Off-policy TD control:
  Q(s, a) ← Q(s, a) + α [r + γ max_{a'} Q(s', a') - Q(s, a)].
  Converges to Q* with appropriate learning-rate decay
  and visit conditions.
- **Confirmation flag**: ✅ `confirmed-canonical`
- **Ready-for-promotion**: ✅ Yes.

### 6.5 DQN

- **Year / citation**: Mnih et al. 2015. "Human-Level
  Control Through Deep Reinforcement Learning". *Nature*
  518: 529–533.
- **Core idea**: Q-learning with a deep network
  parameterised by θ, a target network parameterised by
  θ_target (periodically synced), and experience replay.
  Loss: (r + γ max_{a'} Q(s', a'; θ_target) - Q(s, a; θ))².
- **Confirmation flag**: ✅ `confirmed-canonical`
- **Ready-for-promotion**: ✅ Yes.

### 6.6 Policy Gradient (REINFORCE)

- **Year / citation**: Williams 1992. "Simple Statistical
  Gradient-Following Algorithms for Connectionist
  Reinforcement Learning". *Machine Learning* 8: 229–256.
- **Core idea**: ∇_θ J(θ) = E_τ[Σ_t ∇_θ log π_θ(a_t|s_t) G_t].
  The REINFORCE update: θ ← θ + α G_t ∇_θ log π_θ(a_t|s_t).
- **Confirmation flag**: ✅ `confirmed-canonical`
- **Ready-for-promotion**: ✅ Yes.

### 6.7 A2C / A3C

- **Year / citation**: Mnih et al. 2016. "Asynchronous
  Methods for Deep Reinforcement Learning". ICML.
- **Core idea**: n-step actor-critic with parallel
  workers (A3C) or synchronous update (A2C). Loss
  combines policy gradient with a value baseline.
- **Confirmation flag**: ✅ `confirmed-canonical`
- **Ready-for-promotion**: ✅ Yes.

### 6.8 PPO

- **See `cognitive-cycles.md` §6.5 (canonical reference:
  https://arxiv.org/abs/1707.06347)**.
- **Confirmation flag**: ✅ `confirmed-canonical`

### 6.9 SAC

- **See `cognitive-cycles.md` §6.4 (canonical reference:
  https://arxiv.org/abs/1801.01290)**.
- **Confirmation flag**: ✅ `confirmed-canonical`

### 6.10 AlphaZero / MuZero

- **See `cognitive-cycles.md` §6.3 (canonical reference:
  https://www.nature.com/articles/s41586-020-03157-9)**.
- **Confirmation flag**: ✅ `confirmed-canonical`

### 6.11 TD3 (Twin Delayed DDPG)

- **Year / citation**: Fujimoto, van Hoof, Meger 2018.
  "Addressing Function Approximation Error in Actor-
  Critic Methods". ICML.
- **Core idea**: Clipped double Q-learning (two Q-networks,
  take the min), delayed policy update, target policy
  smoothing. Stabilises actor-critic in continuous action
  spaces.
- **Confirmation flag**: ✅ `confirmed-canonical`
- **Ready-for-promotion**: ✅ Yes.

### 6.12 World Models

- **Year / citation**: Ha & Schmidhuber 2018. "World
  Models". arXiv:1803.10122.
- **Core idea**: Three networks: V (vision), M (memory),
  C (controller). V encodes frames to a latent; M predicts
  the next latent in the latent space; C is a small linear
  controller that takes z_t and h_t as input and outputs
  actions. Trained inside the dreamed world.
- **Confirmation flag**: ✅ `confirmed-canonical`
- **Ready-for-promotion**: ✅ Yes.

### 6.13 Hindsight Experience Replay (HER)

- **Year / citation**: Andrychowicz et al. 2017.
  "Hindsight Experience Replay". NeurIPS 2017.
- **Core idea**: Replay each trajectory with a *virtual
  goal* set to the actually-achieved final state, in
  addition to the original (failed) goal. Solves the
  sparse-reward problem in goal-conditioned RL.
- **Confirmation flag**: ✅ `confirmed-canonical`
- **Ready-for-promotion**: ✅ Yes.

### 6.14 Curiosity-Driven Exploration (ICM)

- **Year / citation**: Pathak, Agrawal, Efros, Darrell
  2017. "Curiosity-Driven Exploration by Self-Supervised
  Prediction". ICML.
- **Core idea**: An *intrinsic curiosity module* (ICM)
  predicts the next state encoding φ(s_{t+1}) from the
  current (φ(s_t), a_t). The prediction error is the
  intrinsic reward. The forward model is trained with
  inverse-dynamics as an auxiliary loss.
- **Confirmation flag**: ✅ `confirmed-canonical`
- **Ready-for-promotion**: ✅ Yes.

### 6.15 Empowerment

- **Year / citation**: Klyubin, Polani, Nehaniv 2005.
  "All Else Being Equal Be Empowered". ECAL 2005.
- **Core idea**: Empowerment is the maximum mutual
  information between the agent's action sequence and
  the next state, E(s) = max_{p(a|s)} I(A; S' | S=s).
  It is intrinsic, channel-capacity-based, and
  state-dependent.
- **Confirmation flag**: ✅ `confirmed-canonical`
- **Ready-for-promotion**: ✅ Yes.

## 7. Promotion Summary

All 51 entries are catalogued below with
their current verification status. 47 are
✅, 3 are 🟢, and 1 is 🔴
(§1.5 Compressive Memory).

| #   | Entry                                | Section | Status |
|-----|--------------------------------------|---------|--------|
| 1   | Hierarchical Temporal Memory (HTM)   | 1.1     | 🟢 |
| 2   | Sparse Distributed Memory (SDM)      | 1.2     | ✅ |
| 3   | Episodic Memory (Tulving)            | 1.3     | 🟢 |
| 4   | ACT-R Declarative Memory             | 1.4     | ✅ |
| 5   | Compressive Memory                   | 1.5     | 🔴 |
| 6   | Semantic Networks                    | 2.1     | ✅ |
| 7   | Frames (Minsky)                      | 2.2     | ✅ |
| 8   | Conceptual Dependency (Schank)       | 2.3     | 🟢 |
| 9   | Conceptual Graphs (Sowa)             | 2.4     | ✅ |
| 10  | OWL 2 / Description Logics           | 2.5     | ✅ |
| 11  | Markov Logic Networks (MLN)          | 2.6     | ✅ |
| 12  | Knowledge Graph Embeddings           | 2.7     | ✅ |
| 13  | Variable Elimination for BNs         | 3.1     | ✅ |
| 14  | Belief Propagation                   | 3.2     | ✅ |
| 15  | MCMC and Gibbs Sampling              | 3.3     | ✅ |
| 16  | CDCL (SAT)                           | 3.4     | ✅ |
| 17  | Simulated Annealing                  | 3.5     | ✅ |
| 18  | Genetic Algorithm                    | 3.6     | ✅ |
| 19  | CMA-ES                               | 3.7     | ✅ |
| 20  | Particle Swarm Optimisation          | 3.8     | ✅ |
| 21  | Ant Colony Optimisation              | 3.9     | ✅ |
| 22  | Rete Algorithm                       | 3.10    | ✅ |
| 23  | Answer Set Programming (ASP)         | 3.11    | ✅ |
| 24  | Contract Net Protocol                | 4.1     | ✅ |
| 25  | VCG Auction (Vickrey-Clarke-Groves)  | 4.2     | ✅ |
| 26  | PBFT (Practical Byzantine Fault Tol.) | 4.3    | ✅ |
| 27  | Raft Consensus                       | 4.4     | ✅ |
| 28  | Paxos                                | 4.5     | ✅ |
| 29  | Federated Learning (FedAvg)          | 4.6     | ✅ |
| 30  | CRDTs (Conflict-Free Replicated DT)  | 4.7     | ✅ |
| 31  | Pearl's do-Calculus                  | 5.1     | ✅ |
| 32  | PC Algorithm                         | 5.2     | ✅ |
| 33  | GES (Greedy Equivalence Search)      | 5.3     | ✅ |
| 34  | LiNGAM                               | 5.4     | ✅ |
| 35  | Convergent Cross Mapping (CCM)       | 5.5     | ✅ |
| 36  | Granger Causality                    | 5.6     | ✅ |
| 37  | UCB1 (Multi-Armed Bandit)            | 6.1     | ✅ |
| 38  | Thompson Sampling                    | 6.2     | ✅ |
| 39  | Value Iteration                      | 6.3     | ✅ |
| 40  | Q-Learning                           | 6.4     | ✅ |
| 41  | DQN                                  | 6.5     | ✅ |
| 42  | Policy Gradient (REINFORCE)          | 6.6     | ✅ |
| 43  | A2C / A3C                            | 6.7     | ✅ |
| 44  | PPO                                  | 6.8     | ✅ |
| 45  | SAC                                  | 6.9     | ✅ |
| 46  | AlphaZero / MuZero                   | 6.10    | ✅ |
| 47  | TD3 (Twin Delayed DDPG)              | 6.11    | ✅ |
| 48  | World Models                         | 6.12    | ✅ |
| 49  | Hindsight Experience Replay (HER)    | 6.13    | ✅ |
| 50  | Curiosity-Driven Exploration (ICM)   | 6.14    | ✅ |
| 51  | Empowerment                          | 6.15    | ✅ |

## 8. See also

- `sxl-operators.md` — symbolic cognitive algorithms
  (AGM, Dung, DLs, SAT, planning, BNs, MLNs, KG
  embeddings).
- `cognitive-cycles.md` — cognitive cycle and time-series
  algorithms (memory consolidation, prediction, attention,
  RL).
- `neuro-primitives.md` — neuro-computational primitives
  and neural network algorithms.
- `README.md` — overview of the research knowledge base.
- `INTEGRATION.md` — how sapling agents connect to the
  bus.
