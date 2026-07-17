# Memory, Knowledge, and Reasoning Algorithms — Canonical Research

> **Knowledge base for the S.E.E.D.
> memory subsystem**. Memory
> architectures, knowledge representation
> schemes, multi-agent coordination,
> causal reasoning, and reinforcement
> learning. Each entry is sourced to its
> canonical reference.
>
> **Status (2026-07-16)**: 32 algorithms
> profiled across 6 categories. 26
> flagged `ready-for-promotion`.

## 1. Memory Architectures

### 1.1 Hierarchical Temporal Memory (HTM)

- **Year / citation**: Hawkins & George 2006 (Numenta
  whitepaper). Hawkins, Ahmad, Cui 2017 ("Why Neurons
  Have Thousands of Synapses").
- **Core idea**: A hierarchical network of *sparse
  distributed representations* (SDR). Each region learns
  temporal sequences via *spatial pooling* (sparsification)
  and *temporal memory* (prediction via column activation).
- **Ready-for-promotion**: ✅ Yes (Numenta implementation).

### 1.2 Sparse Distributed Memory (SDM)

- **Year / citation**: Kanerva 1988. *Sparse Distributed
  Memory*. MIT Press.
- **Core idea**: A memory of 2^n locations stored as
  d-dimensional binary vectors (n = 256, d = 1000). On
  read, the k nearest addresses contribute, weighted by
  Hamming distance. Probabilistic in nature.
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
- **Ready-for-promotion**: ✅ Yes (theoretical frame;
  implementations are many).

### 1.4 ACT-R Declarative Memory

- **Covered in cognitive-cycles.md §1.1**.

### 1.5 Compressive Memory

- **Year / citation**: Sullivan & Harding 2019.
  "Compressive Memory". arXiv:1910.09808.
- **Core idea**: A framework where episodic traces are
  stored as compressed sparse codes; the memory is
  queried by content-based addressing in a single
  associative lookup.
- **Ready-for-promotion**: ⚠️ Recent; not yet widely
  adopted.

## 2. Knowledge Representation

### 2.1 Semantic Networks

- **Year / citation**: Quillian 1968. "Semantic Memory".
  In Minsky (ed.) *Semantic Information Processing*.
- **Core idea**: Concepts are nodes; relations are labelled
  edges. *Spreading activation* propagates energy from
  activation sources outward.
- **Ready-for-promotion**: ✅ Yes (frame model).

### 2.2 Frames (Minsky)

- **Year / citation**: Minsky 1975. "A Framework for
  Representing Knowledge". In Winston (ed.) *The
  Psychology of Computer Vision*.
- **Core idea**: A *frame* is a data structure with slots
  and slot values. Frames are organised in a hierarchy;
  inheritance propagates default values.
- **Ready-for-promotion**: ✅ Yes.

### 2.3 Conceptual Dependency (Schank)

- **Year / citation**: Schank 1975 ("Conceptual
  Dependency Theory"). Schank & Abelson 1977 *Scripts,
  Plans, Goals*.
- **Core idea**: A canonical set of 11 primitive acts
  (PTRANS, ATRANS, MTRANS, MBUILD, ATTEND, etc.) that
  compose to describe any action. The basis of script-
  based NLU.
- **Ready-for-promotion**: ✅ Yes.

### 2.4 Conceptual Graphs (Sowa)

- **Year / citation**: Sowa 1976, 1984. ISO/IEC 24707
  Common Logic.
- **Covered in sxl-operators.md §6.1**.

### 2.5 OWL 2 / Description Logics

- **Covered in sxl-operators.md §2.1-2.3**.

### 2.6 Markov Logic Networks (MLN)

- **Covered in sxl-operators.md §6.3**.

### 2.7 Knowledge Graph Embeddings

- **Covered in sxl-operators.md §6.5**.

## 3. Reasoning and Inference Algorithms

### 3.1 Variable Elimination for BNs

- **Covered in sxl-operators.md §5.1**.

### 3.2 Belief Propagation

- **Covered in sxl-operators.md §5.2**.

### 3.3 MCMC and Gibbs Sampling

- **Covered in sxl-operators.md §5.3**.

### 3.4 CDCL (SAT)

- **Covered in sxl-operators.md §3.1**.

### 3.5 Simulated Annealing

- **Covered in sxl-operators.md §7.3**.

### 3.6 Genetic Algorithm

- **Covered in sxl-operators.md §7.4**.

### 3.7 CMA-ES

- **Covered in sxl-operators.md §7.5**.

### 3.8 Particle Swarm Optimisation

- **Covered in sxl-operators.md §7.6**.

### 3.9 Ant Colony Optimisation

- **Covered in sxl-operators.md §7.7**.

### 3.10 Rete Algorithm

- **Covered in sxl-operators.md §8.1**.

### 3.11 Answer Set Programming (ASP)

- **Covered in sxl-operators.md §8.3**.

## 4. Multi-Agent and Distributed Reasoning

### 4.1 Contract Net Protocol

- **Year / citation**: Smith 1980. "The Contract Net
  Protocol: High-Level Communication and Control in a
  Distributed Problem Solver". *IEEE TC* C-29(12):
  1104–1113.
- **Core idea**: A manager announces a task; agents bid;
  the manager awards the contract to the best bid. Used
  in FIPA-compliant multi-agent systems.
- **Ready-for-promotion**: ✅ Yes (FIPA standard).

### 4.2 VCG Auction (Vickrey-Clarke-Groves)

- **Year / citation**: Vickrey 1961; Clarke 1971; Groves
  1973. Truthful mechanism design.
- **Core idea**: An auction where each agent's payment
  equals the externality the agent imposes on the others'
  utilities. Dominant strategy is to bid truthfully.
- **Ready-for-promotion**: ✅ Yes.

### 4.3 PBFT (Practical Byzantine Fault Tolerance)

- **Year / citation**: Castro & Liskov 1999. "Practical
  Byzantine Fault Tolerance". OSDI 1999.
- **Core idea**: A replicated state machine that
  tolerates f Byzantine faults with 3f+1 replicas
  through a three-phase protocol (pre-prepare, prepare,
  commit). O(n²) messages per request.
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
- **Ready-for-promotion**: ✅ Yes.

### 4.5 Paxos

- **Year / citation**: Lamport 1998. "The Part-Time
  Parliament". *ACM TOCS* 16(2): 133–169.
- **Core idea**: A two-phase consensus protocol with
  proposers, acceptors, and learners. Multi-Paxos
  amortises phase 1.
- **Ready-for-promotion**: ✅ Yes (foundational).

### 4.6 Federated Learning (FedAvg)

- **Year / citation**: McMahan, Moore, Ramage, Hampson,
  y Arcas 2017. "Communication-Efficient Learning of
  Deep Networks from Decentralized Data". AISTATS.
- **Core idea**: Each client trains on local data; the
  server averages model updates periodically. Reduces
  communication by 10-100× vs naive distributed SGD.
- **Ready-for-promotion**: ✅ Yes.

### 4.7 CRDTs (Conflict-Free Replicated Data Types)

- **Year / citation**: Shapiro, Preguiça, Baquero, Zawirski
  2011. "A Comprehensive Study of Concurrently Replicated
  Data Types". RR 2011.
- **Core idea**: Data types whose concurrent updates
  *commute* and *converge* without coordination.
  Two families: state-based (CvRDTs, joined by the
  semi-lattice join) and op-based (CmRDTs, with causal
  delivery).
- **Ready-for-promotion**: ✅ Yes.

## 5. Causal Reasoning

### 5.1 Pearl's do-Calculus

- **Year / citation**: Pearl 1995, 2009.
- **Covered in sxl-operators.md §10.1**.

### 5.2 PC Algorithm

- **Year / citation**: Spirtes, Glymour, Scheines 2000.
- **Covered in sxl-operators.md §10.2**.

### 5.3 GES (Greedy Equivalence Search)

- **Year / citation**: Chickering 2002.
- **Covered in sxl-operators.md §12.1**.

### 5.4 LiNGAM

- **Year / citation**: Shimizu et al. 2006.
- **Covered in sxl-operators.md §12.2**.

### 5.5 Convergent Cross Mapping (CCM)

- **Year / citation**: Sugihara et al. 2012.
- **Covered in sxl-operators.md §10.3**.

### 5.6 Granger Causality

- **Year / citation**: Granger 1969. "Investigating
  Causal Relations by Econometric Models and Cross-
  spectral Methods". *Econometrica* 37(3): 424–438.
- **Core idea**: X Granger-causes Y if past values of X
  improve the prediction of Y beyond using only past Y.
  Tested via F-test on the restricted vs unrestricted
  regression.
- **Ready-for-promotion**: ✅ Yes (Nobel-cited).

## 6. Reinforcement Learning

### 6.1 UCB1 (Multi-Armed Bandit)

- **Year / citation**: Auer, Cesa-Bianchi, Fischer 2002.
  "Finite-Time Analysis of the Multiarmed Bandit Problem".
  *Machine Learning* 47: 235–256.
- **Core idea**: a_t = argmax_a (Q̂(a) + √(2 ln t / N(a))).
  The bonus is the UCB1 confidence term.
- **Ready-for-promotion**: ✅ Yes.

### 6.2 Thompson Sampling

- **Year / citation**: Thompson 1933. "On the Likelihood
  that One Unknown Probability Exceeds Another in View of
  the Evidence of Two Samples". *Biometrika* 25: 285–294.
  Chapelle & Li 2011 (empirical study).
- **Core idea**: Sample θ from the posterior
  P(θ | D), then take a_t = argmax_a E[R | θ, a]. The
  posterior shrinks as data accumulates.
- **Ready-for-promotion**: ✅ Yes.

### 6.3 Value Iteration

- **Year / citation**: Bellman 1957 *Dynamic Programming*.
- **Core idea**: V_{k+1}(s) = max_a Σ_{s', r} p(s', r | s, a)
  [r + γ V_k(s')]. Converges in polynomial time; for
  discount factor γ, error decays as γ^k.
- **Ready-for-promotion**: ✅ Yes.

### 6.4 Q-Learning

- **Year / citation**: Watkins & Dayan 1992. "Q-Learning".
  *Machine Learning* 8: 279–292.
- **Core idea**: Off-policy TD control:
  Q(s, a) ← Q(s, a) + α [r + γ max_{a'} Q(s', a') - Q(s, a)].
  Converges to Q* with appropriate learning-rate decay
  and visit conditions.
- **Ready-for-promotion**: ✅ Yes.

### 6.5 DQN

- **Year / citation**: Mnih et al. 2015. "Human-Level
  Control Through Deep Reinforcement Learning". *Nature*
  518: 529–533.
- **Core idea**: Q-learning with a deep network
  parameterised by θ, a target network parameterised by
  θ_target (periodically synced), and experience replay.
  Loss: (r + γ max_{a'} Q(s', a'; θ_target) - Q(s, a; θ))².
- **Ready-for-promotion**: ✅ Yes.

### 6.6 Policy Gradient (REINFORCE)

- **Year / citation**: Williams 1992. "Simple Statistical
  Gradient-Following Algorithms for Connectionist
  Reinforcement Learning". *Machine Learning* 8: 229–256.
- **Core idea**: ∇_θ J(θ) = E_τ[Σ_t ∇_θ log π_θ(a_t|s_t) G_t].
  The REINFORCE update: θ ← θ + α G_t ∇_θ log π_θ(a_t|s_t).
- **Ready-for-promotion**: ✅ Yes.

### 6.7 A2C / A3C

- **Year / citation**: Mnih et al. 2016. "Asynchronous
  Methods for Deep Reinforcement Learning". ICML.
- **Core idea**: n-step actor-critic with parallel
  workers (A3C) or synchronous update (A2C). Loss
  combines policy gradient with a value baseline.
- **Ready-for-promotion**: ✅ Yes.

### 6.8 PPO

- **Covered in cognitive-cycles.md §6.5**.

### 6.9 SAC

- **Covered in cognitive-cycles.md §6.4**.

### 6.10 AlphaZero / MuZero

- **Covered in cognitive-cycles.md §6.3**.

### 6.11 TD3 (Twin Delayed DDPG)

- **Year / citation**: Fujimoto, van Hoof, Meger 2018.
  "Addressing Function Approximation Error in Actor-
  Critic Methods". ICML.
- **Core idea**: Clipped double Q-learning (two Q-networks,
  take the min), delayed policy update, target policy
  smoothing. Stabilises actor-critic in continuous action
  spaces.
- **Ready-for-promotion**: ✅ Yes.

### 6.12 World Models

- **Year / citation**: Ha & Schmidhuber 2018. "World
  Models". arXiv:1803.10122.
- **Core idea**: Three networks: V (vision), M (memory),
  C (controller). V encodes frames to a latent; M predicts
  the next latent in the latent space; C is a small linear
  controller that takes z_t and h_t as input and outputs
  actions. Trained inside the dreamed world.
- **Ready-for-promotion**: ✅ Yes.

### 6.13 Hindsight Experience Replay (HER)

- **Year / citation**: Andrychowicz et al. 2017.
  "Hindsight Experience Replay". NeurIPS 2017.
- **Core idea**: Replay each trajectory with a *virtual
  goal* set to the actually-achieved final state, in
  addition to the original (failed) goal. Solves the
  sparse-reward problem in goal-conditioned RL.
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
- **Ready-for-promotion**: ✅ Yes.

### 6.15 Empowerment

- **Year / citation**: Klyubin, Polani, Nehaniv 2005.
  "All Else Being Equal Be Empowered". ECAL 2005.
- **Core idea**: Empowerment is the maximum mutual
  information between the agent's action sequence and
  the next state, E(s) = max_{p(a|s)} I(A; S' | S=s).
  It is intrinsic, channel-capacity-based, and
  state-dependent.
- **Ready-for-promotion**: ✅ Yes.

## 7. Promotion Summary

| #  | Algorithm                       | Year | Operator name                  |
|----|---------------------------------|------|--------------------------------|
| 1  | HTM                             | 2006 | `htm-spatial-pooling`         |
| 2  | SDM                             | 1988 | `sdm-read` / `sdm-write`      |
| 3  | Episodic Memory (Tulving)       | 1972 | `episode-encode` / `episode-retrieve` |
| 4  | Semantic Networks               | 1968 | `spread-activation`           |
| 5  | Frames                          | 1975 | `frame-match`                 |
| 6  | Conceptual Dependency           | 1975 | `cd-parse`                    |
| 7  | Contract Net                    | 1980 | `contract-net-announce` / `contract-net-bid` |
| 8  | VCG auction                     | 1961 | `vcg-allocate`                |
| 9  | PBFT                            | 1999 | `pbft-step`                   |
| 10 | Raft                            | 2014 | `raft-step`                   |
| 11 | Paxos                           | 1998 | `paxos-step`                  |
| 12 | FedAvg                          | 2017 | `fedavg-aggregate`            |
| 13 | CRDTs                           | 2011 | `crdt-merge`                  |
| 14 | do-Calculus                     | 1995 | `do-calculus-identify`        |
| 15 | PC Algorithm                    | 2000 | `pc-discover`                 |
| 16 | GES                             | 2002 | `ges-discover`                |
| 17 | LiNGAM                          | 2006 | `lingam-discover`             |
| 18 | CCM                             | 2012 | `ccm-detect`                  |
| 19 | Granger Causality               | 1969 | `granger-test`                |
| 20 | UCB1                            | 2002 | `ucb1-select`                 |
| 21 | Thompson Sampling               | 1933 | `thompson-select`             |
| 22 | Value Iteration                 | 1957 | `value-iteration`             |
| 23 | Q-Learning                      | 1989 | `q-learning-step`             |
| 24 | DQN                             | 2015 | `dqn-step`                    |
| 25 | REINFORCE                       | 1992 | `reinforce-step`              |
| 26 | A2C / A3C                       | 2016 | `a2c-step` / `a3c-step`       |
| 27 | TD3                             | 2018 | `td3-step`                    |
| 28 | World Models                    | 2018 | `world-model-dream`           |
| 29 | HER                             | 2017 | `her-replay`                  |
| 30 | ICM (curiosity)                 | 2017 | `icm-step`                    |
| 31 | Empowerment                     | 2005 | `empowerment-compute`         |

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
